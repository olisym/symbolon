"""Die Bindung des Boten an Reticulum (D584 Beschluss 1, D585 Beschluss 1, Befund 1 und 2)."""

from __future__ import annotations

import random
import threading
import time
from collections.abc import Callable
from pathlib import Path

import RNS

from symbolon.bote.draht import PFADE, beantworten, lesen
from symbolon.bote.kern import (
    Getrennt,
    HttpKnoten,
    Quelle,
    ankuendigung,
    ankuendigung_aus,
    lohnt,
    rundgang,
    sperrstand,
)
from symbolon.bote.trickle import Trickle, Zeiten, zeiten

APP = "symbolon"
ASPEKT = "bote"

_ZUSTELL_MIN = 1.0
_ZUSTELL_FAKTOR = 20.0
_VERSUCHE = 3
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
    """Die lesenden Pfade, auch ``abgleich``; keiner zum Einliefern (D617 Beschluss 5)."""
    for pfad in PFADE:
        destination.register_request_handler(
            pfad, _antwort(quelle, pfad), RNS.Destination.ALLOW_ALL
        )


def _zustellfrist(link) -> float:
    """Die Frist bis zum erneuten Senden wächst mit der Laufzeit des Links (D591 Beschluss 1)."""
    return max(_ZUSTELL_MIN, _ZUSTELL_FAKTOR * (link.rtt or 0.0))


def _bitrate() -> float | None:
    """Die kleinste ``bitrate`` unter den Schnittstellen, ohne eine ``None`` (D611 Beschluss 2)."""
    werte = [
        interface.bitrate
        for interface in RNS.Transport.interfaces
        if interface.bitrate is not None
    ]
    return min(werte) if werte else None


class RnsNachbar:
    """Ein Nachbar über einen Link; die Fristen trägt er selbst (D584 Beschluss 1, D611 Beschluss 2)."""

    def __init__(self, ziel: bytes, zeit: Zeiten | None = None) -> None:
        self.ziel = ziel
        self.zeit = zeiten(None) if zeit is None else zeit
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
            if time.monotonic() - begun > self.zeit.link:
                raise Getrennt()
            time.sleep(_WARTEN)
        self._link = link
        return link

    def _anfrage(self, pfad: str, data: object) -> object:
        """Ohne Fortschritt über die Frist wird der Link abgebaut: getrennt (D586 Beschluss 2).

        Bleibt eine Anfrage über die Zustellfrist unzugestellt, geht sie auf demselben Link erneut,
        bis zu ``_VERSUCHE`` Anfragen (D591 Beschluss 1). Eine doppelte Anfrage schadet nicht, weil
        der Bote nur liest (D584 Beschluss 2).
        """
        link = self._verbinden()
        receipt = link.request(pfad, data)
        if not receipt:
            raise Getrennt()
        anfragen = 1
        gesendet = time.monotonic()
        fortschritt = receipt.get_progress()
        seit = gesendet
        while not receipt.concluded():
            if (
                anfragen < _VERSUCHE
                and receipt.get_status() == RNS.RequestReceipt.SENT
                and time.monotonic() - gesendet > _zustellfrist(link)
            ):
                receipt = link.request(pfad, data)
                if not receipt:
                    raise Getrennt()
                anfragen += 1
                fortschritt = receipt.get_progress()
                seit = gesendet = time.monotonic()
                continue
            jetzt = receipt.get_progress()
            if jetzt != fortschritt:
                fortschritt = jetzt
                seit = time.monotonic()
            elif time.monotonic() - seit > self.zeit.antwort:
                link.teardown()
                self._link = None
                raise Getrennt()
            time.sleep(_WARTEN)
        if receipt.get_status() != RNS.RequestReceipt.READY:
            raise Getrennt()
        return lesen(pfad, receipt.get_response())

    def bestand(self) -> tuple[list[bytes], list[bytes]]:
        return self._anfrage("bestand", None)

    def paket(self, claims: list[bytes], objekte: list[bytes]) -> bytes:
        """Die Anfrage geht als ``[claims, objekte]`` über ``_anfrage`` (D614 Beschluss 4)."""
        return self._anfrage("paket", [claims, objekte])

    def abgleich(self, roh: bytes) -> bytes:
        """Die Nachricht geht als Bytes über ``_anfrage`` (D617 Beschluss 5)."""
        return self._anfrage("abgleich", roh)


def laufen(
    knoten_url: str,
    konfiguration,
    ident: RNS.Identity,
    nachbarn: list[bytes],
    takt: float,
    melden: Callable[[str], None],
    sperren: Path | None = None,
) -> None:
    """Anbieten, nach Trickle ankündigen und je Takt höchstens einen Nachbarn holen.

    Die Ankündigung trägt Stand und Zahl der Einträge (D584 Beschluss 1 und 2, D619 Beschluss 1).
    Fällig wird ein Nachbar nur, wenn das Holen lohnt (D619 Beschluss 2). Die Fristen kommen aus
    der kleinsten Bitrate (D611 Beschluss 2). ``sperrstand`` liest die Sperrliste in jedem Takt,
    auch ohne Holen (D594 Beschluss 3, D611 Beschluss 3). Der Bote holt, er schiebt nie.
    """
    RNS.Reticulum(configdir=str(konfiguration))
    destination = RNS.Destination(
        ident, RNS.Destination.IN, RNS.Destination.SINGLE, APP, ASPEKT
    )
    mein = HttpKnoten(knoten_url)
    anbieten(destination, mein)
    zeit = zeiten(_bitrate())
    quellen = {ziel: RnsNachbar(ziel, zeit) for ziel in nachbarn}
    trickle = Trickle(zeit.imin, 6, 2, time.monotonic(), random.Random())
    sperre = threading.Lock()
    gehoerte: dict[bytes, tuple[bytes, int]] = {}
    faellig: dict[bytes, float] = {}
    pausen: dict[bytes, float] = {}
    eigener: list[bytes | None] = [None]
    eigene_zahl: list[int] = [0]

    class _Hoerer:
        """Hört Ankündigungen; die Parameternamen sind die von RNS (D611 Beschluss 1, Befund 1)."""

        aspect_filter = "symbolon.bote"
        receive_path_responses = True

        def received_announce(self, destination_hash, announced_identity, app_data) -> None:
            # RNS ruft mit Namen auf. Die Identität hat ``aspect_filter`` schon geprüft
            # (D611 Befund 1); hier zählen Stand und Zahl (D619 Beschluss 1 und 2).
            if announced_identity is None and destination_hash is None:
                return
            paar = ankuendigung_aus(app_data)
            if destination_hash not in quellen or paar is None:
                return
            with sperre:
                gehoerte[destination_hash] = paar
                if eigener[0] is not None and paar[0] == eigener[0]:
                    trickle.gleich()
                if lohnt(paar, eigener[0], eigene_zahl[0]):
                    if destination_hash not in faellig:
                        faellig[destination_hash] = time.monotonic()
                else:
                    faellig.pop(destination_hash, None)

    RNS.Transport.register_announce_handler(_Hoerer())
    zuletzt: frozenset[bytes] | None = frozenset()
    while True:
        jetzt = time.monotonic()
        try:
            stand = mein.stand()
        except Getrennt:
            stand = None
        with sperre:
            geaendert = stand is not None and stand != eigener[0]
        zahl: int | None = None
        if geaendert:
            try:
                claims, objekte = mein.bestand()
                zahl = len(claims) + len(objekte)
            except Getrennt:
                zahl = None
        with sperre:
            if geaendert:
                trickle.neu(jetzt)
                eigener[0] = stand
                if zahl is not None:
                    eigene_zahl[0] = zahl
                for ziel, gehoert in gehoerte.items():
                    if lohnt(gehoert, stand, eigene_zahl[0]):
                        faellig[ziel] = jetzt
                        pausen.pop(ziel, None)
                    else:
                        faellig.pop(ziel, None)
                        pausen.pop(ziel, None)
            if stand is not None and trickle.ankuendigen(jetzt):
                meldung: bytes | None = ankuendigung(stand, eigene_zahl[0])
            else:
                meldung = None
            kandidaten = [(wann, ziel) for ziel, wann in faellig.items() if wann <= jetzt]
        if meldung is not None:
            destination.announce(app_data=meldung)
        gelesen = sperrstand(sperren, zuletzt, melden)
        zuletzt = gelesen
        if gelesen is not None and kandidaten:
            _wann, gewaehlt = min(kandidaten)
            zuletzt = rundgang(
                mein, [(gewaehlt, quellen[gewaehlt])], sperren, zuletzt, melden
            )
            try:
                danach = mein.stand()
            except Getrennt:
                danach = None
            with sperre:
                gehoert = gehoerte.get(gewaehlt)
                geaendert = eigener[0] is not None and danach is not None and danach != eigener[0]
                gleich = gehoert is not None and danach == gehoert[0]
                if geaendert or gleich:
                    faellig.pop(gewaehlt, None)
                    pausen.pop(gewaehlt, None)
                else:
                    # Kein gleicher Stand: doppelt so lange, von imin bis 300 s (D611 Beschluss 1).
                    pause = min(300.0, max(zeit.imin, 2 * pausen.get(gewaehlt, 0.0)))
                    pausen[gewaehlt] = pause
                    faellig[gewaehlt] = time.monotonic() + pause
        time.sleep(takt)
