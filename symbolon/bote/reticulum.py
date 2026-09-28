"""Die Bindung des Boten an Reticulum (D584 Beschluss 1, D585 Beschluss 1, Befund 1 und 2)."""

from __future__ import annotations

import time
from collections.abc import Callable
from pathlib import Path

import RNS

from symbolon.bote.draht import PFADE, beantworten, lesen
from symbolon.bote.kern import Getrennt, HttpKnoten, Quelle, holen

APP = "symbolon"
ASPEKT = "bote"

_LINK_FRIST = 10.0
_ANTWORT_FRIST = 15.0
_WARTEN = 0.05


def identitaet(pfad) -> RNS.Identity:
    """Die Identität aus der Datei, sonst neu und gespeichert (D585 Beschluss 1)."""
    pfad = Path(pfad)
    if pfad.exists():
        ident = RNS.Identity.from_file(str(pfad))
        if ident is None:
            raise ValueError(f"{pfad}: keine Identität")
        return ident
    ident = RNS.Identity()
    ident.to_file(str(pfad))
    return ident


def adresse(ident: RNS.Identity) -> bytes:
    """Die Adresse ist der Hash der Destination ``symbolon.bote`` (D585 Beschluss 1)."""
    return RNS.Destination.hash(ident, APP, ASPEKT)


def _antwort(quelle: Quelle, pfad: str):
    """Ein Handler mit genau den sechs Parametern, die RNS verlangt (D585 Befund 1 und 2)."""

    def antwort(_path, data, _request_id, _link_id, _remote_identity, _requested_at):
        return beantworten(quelle, pfad, data)

    return antwort


def anbieten(destination, quelle: Quelle) -> None:
    """Nur die lesenden Pfade, keiner zum Einliefern (D584 Beschluss 2, D585 Beschluss 1)."""
    for pfad in PFADE:
        destination.register_request_handler(
            pfad, _antwort(quelle, pfad), RNS.Destination.ALLOW_ALL
        )


class RnsNachbar:
    """Ein Nachbar über einen Link zu ``symbolon.bote`` an seiner Adresse (D584 Beschluss 1)."""

    def __init__(self, ziel: bytes) -> None:
        self.ziel = ziel
        self._link: RNS.Link | None = None

    def _verbinden(self) -> RNS.Link:
        if self._link is not None and self._link.status == RNS.Link.ACTIVE:
            return self._link
        if not RNS.Transport.has_path(self.ziel):
            RNS.Transport.request_path(self.ziel)
            raise Getrennt()
        ident = RNS.Identity.recall(self.ziel)
        if ident is None:
            raise Getrennt()
        destination = RNS.Destination(
            ident, RNS.Destination.OUT, RNS.Destination.SINGLE, APP, ASPEKT
        )
        link = RNS.Link(destination)
        begun = time.monotonic()
        while link.status != RNS.Link.ACTIVE:
            if time.monotonic() - begun > _LINK_FRIST:
                raise Getrennt()
            time.sleep(_WARTEN)
        self._link = link
        return link

    def _anfrage(self, pfad: str, data: bytes | None) -> object:
        """Ohne Fortschritt über die Frist wird der Link abgebaut: getrennt (D586 Beschluss 2)."""
        link = self._verbinden()
        receipt = link.request(pfad, data)
        if not receipt:
            raise Getrennt()
        fortschritt = receipt.get_progress()
        seit = time.monotonic()
        while not receipt.concluded():
            jetzt = receipt.get_progress()
            if jetzt != fortschritt:
                fortschritt = jetzt
                seit = time.monotonic()
            elif time.monotonic() - seit > _ANTWORT_FRIST:
                link.teardown()
                self._link = None
                raise Getrennt()
            time.sleep(_WARTEN)
        if receipt.get_status() != RNS.RequestReceipt.READY:
            raise Getrennt()
        return lesen(pfad, receipt.get_response())

    def bestand(self) -> tuple[list[bytes], list[bytes]]:
        return self._anfrage("bestand", None)

    def claim(self, cid: bytes) -> bytes | None:
        return self._anfrage("claim", cid)

    def objekt(self, digest: bytes) -> tuple[str, bytes] | None:
        return self._anfrage("object", digest)


def laufen(
    knoten_url: str,
    konfiguration,
    ident: RNS.Identity,
    nachbarn: list[bytes],
    takt: float,
    melden: Callable[[str], None],
) -> None:
    """Anbieten und im Takt von jedem Nachbarn holen (D584 Beschluss 1 und 2, D585 Beschluss 3)."""
    RNS.Reticulum(configdir=str(konfiguration))
    destination = RNS.Destination(
        ident, RNS.Destination.IN, RNS.Destination.SINGLE, APP, ASPEKT
    )
    mein = HttpKnoten(knoten_url)
    anbieten(destination, mein)
    quellen = [(ziel, RnsNachbar(ziel)) for ziel in nachbarn]
    while True:
        destination.announce()
        for ziel, nachbar in quellen:
            e = holen(mein, nachbar)
            if e.geholt or e.abgewiesen or e.fehlend or e.formwidrig:
                melden(
                    f"{ziel.hex()}: geholt={e.geholt} abgewiesen={e.abgewiesen} "
                    f"fehlend={e.fehlend} formwidrig={e.formwidrig}"
                )
        time.sleep(takt)
