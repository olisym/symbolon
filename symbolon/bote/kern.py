"""Holen ohne Transport: der eigene Knoten holt von einem Nachbarn (D584 Beschluss 1 und 2).

Der Nachbar wird nur gefragt, nie beliefert. Was ein Holen meldet, steht in D585 Beschluss 3,
geändert durch D614 Beschluss 4 und D617 Beschluss 4.
"""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from symbolon import buendel
from symbolon.bote import rbsr

_ZEITLIMIT = 10
RUNDRUF_MARKE = b"symbolon-rundruf-1"
RUNDRUF_KOPF = 80
RUNDRUF_ANZAHL = 16
RUNDRUF_GEHALTEN = 16


class Getrennt(Exception):
    """Ein Knoten oder ein Nachbar ist nicht erreichbar oder getrennt (D516 Beschluss 3)."""


class Formwidrig(Exception):
    """Eine Antwort hat nicht die Form auf dem Draht (D585 Beschluss 2)."""


@dataclass(frozen=True)
class Ergebnis:
    """Was ein Holen meldet (D585 Beschluss 3, D614 Beschluss 4, D516 Beschluss 4)."""

    geholt: int
    abgewiesen: dict[str, int]
    getrennt: bool
    fehlend: int
    formwidrig: int


class Quelle(Protocol):
    """Was ein Bote lesen kann; keine Methode zum Einliefern (D584 Beschluss 2)."""

    def bestand(self) -> tuple[list[bytes], list[bytes]]: ...

    def abgleich(self, roh: bytes) -> bytes: ...

    def paket(self, claims: list[bytes], objekte: list[bytes]) -> bytes: ...


class HttpKnoten:
    """Der eigene Knoten über die Routen unter ``/peer/`` (D516 Beschluss 2 und 3)."""

    def __init__(self, url: str) -> None:
        self.url = url.rstrip("/")
        self.eingeliefert: set[tuple[int, bytes]] = set()
        self.sperre = threading.Lock()

    def _anfrage(self, method: str, route: str, payload: object = None) -> tuple[int, Any]:
        """503 und jeder ``OSError`` beim Verbinden sind getrennt (D516 Beschluss 3)."""
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.url + route,
            data=data,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=_ZEITLIMIT) as response:
                status, body = response.status, response.read()
        except urllib.error.HTTPError as exc:
            status, body = exc.code, exc.read()
        except OSError as exc:
            raise Getrennt() from exc
        if status == 503:
            raise Getrennt()
        if method == "GET" and status == 404:
            return status, None
        if status == 200 or (method == "POST" and status == 400):
            return status, json.loads(body)
        raise RuntimeError(f"{method} {route}: {status}")

    def bestand(self) -> tuple[list[bytes], list[bytes]]:
        _status, body = self._anfrage("GET", "/peer/bestand")
        claims = [bytes.fromhex(item) for item in body["claims"]]
        objekte = [bytes.fromhex(item) for item in body["objects"]]
        return claims, objekte

    def claim(self, cid: bytes) -> bytes | None:
        status, body = self._anfrage("GET", f"/peer/claims/{cid.hex()}")
        if status == 404:
            return None
        return bytes.fromhex(body["data"])

    def objekt(self, digest: bytes) -> tuple[str, bytes] | None:
        status, body = self._anfrage("GET", f"/peer/objects/{digest.hex()}")
        if status == 404:
            return None
        return body["kind"], bytes.fromhex(body["data"])

    def paket(self, claims: list[bytes], objekte: list[bytes]) -> bytes:
        """Das Bündel aus ``claim`` und ``objekt``; Fehlendes fehlt (D614 Beschluss 4)."""
        gehalten_objekte: list[tuple[str, bytes]] = []
        for digest in objekte:
            found = self.objekt(digest)
            if found is not None:
                gehalten_objekte.append(found)
        gehalten_claims: list[bytes] = []
        for cid in claims:
            data = self.claim(cid)
            if data is not None:
                gehalten_claims.append(data)
        return buendel.schreiben(gehalten_claims, gehalten_objekte)

    def abgleich(self, roh: bytes) -> bytes:
        """Antwort aus dem eigenen Bestand (D617 Beschluss 4 und 5)."""
        claims, objekte = self.bestand()
        teile = rbsr.lesen(roh, vom_boten=True)
        antwort = rbsr.antworten(rbsr.schluessel(claims, objekte), teile)
        return rbsr.kodieren(antwort)

    def stand(self) -> bytes:
        """``GET /stand``: 64 Hexzeichen sind der Stand, sonst getrennt (D611 Beschluss 1)."""
        try:
            status, body = self._anfrage("GET", "/stand")
        except (RuntimeError, json.JSONDecodeError) as exc:
            raise Getrennt() from exc
        if status == 200 and isinstance(body, str) and len(body) == 64:
            try:
                roh = bytes.fromhex(body)
            except ValueError as exc:
                raise Getrennt() from exc
            if len(roh) == 32 and all(c in "0123456789abcdefABCDEF" for c in body):
                return roh
        raise Getrennt()

    def liefern_claim(self, data: bytes) -> str | None:
        """``None`` bei Annahme, sonst der Name der Abweisung (D516 Beschluss 2 und 4).

        Bei Annahme kommt ``claim_id`` nach ``eingeliefert`` (D636 Beschluss 2).
        """
        with self.sperre:
            status, body = self._anfrage("POST", "/peer/claims", {"data": data.hex()})
            if status == 200:
                self.eingeliefert.add((rbsr.ART_CLAIM, bytes.fromhex(body["claim_id"])))
            return None if status == 200 else _name(body)

    def liefern_objekt(self, kind: str, data: bytes) -> str | None:
        """``None`` bei Annahme, sonst der Name der Abweisung (D516 Beschluss 2 und 4).

        Bei Annahme kommt ``hash`` nach ``eingeliefert`` (D636 Beschluss 2).
        """
        with self.sperre:
            status, body = self._anfrage(
                "POST", "/peer/objects", {"kind": kind, "data": data.hex()}
            )
            if status == 200:
                self.eingeliefert.add((rbsr.ART_OBJEKT, bytes.fromhex(body["hash"])))
            return None if status == 200 else _name(body)


def _name(body: object) -> str:
    return body if isinstance(body, str) else json.dumps(body)


def ankuendigung(stand: bytes, anzahl: int) -> bytes:
    """Stand und Zahl der Einträge, die Zahl gekappt bei 2^32 - 1 (D619 Beschluss 1)."""
    return stand + min(anzahl, 2**32 - 1).to_bytes(4, "big")


def ankuendigung_aus(app_data: object) -> tuple[bytes, int] | None:
    """Genau 36 Byte vom Typ ``bytes`` sind Stand und Zahl, sonst ``None`` (D619 Beschluss 1)."""
    if type(app_data) is bytes and len(app_data) == 36:
        return app_data[:32], int.from_bytes(app_data[32:], "big")
    return None


def lohnt(gehoert: tuple[bytes, int], stand: bytes | None, anzahl: int) -> bool:
    """Wahr, wenn der gehörte Stand anders ist und seine Zahl mindestens die eigene
    (D619 Beschluss 2)."""
    fremd, zahl = gehoert
    return fremd != stand and zahl >= anzahl


def zuruecksetzen(
    ziel: bytes, fremd: bytes, stand: bytes | None, gesperrt: frozenset[bytes] | None
) -> bool:
    """Wahr, wenn ein anderer Stand von einem nicht gesperrten Nachbarn gehört wird
    (RFC 6206, Abschnitt 4.2, D623 Beschluss 2)."""
    return (
        stand is not None and fremd != stand and gesperrt is not None and ziel not in gesperrt
    )


def einliefern(
    mein: HttpKnoten, claims: list[bytes], objekte: list[tuple[str, bytes]]
) -> tuple[int, dict[str, int], bool]:
    """Objekte vor Claims. Getrennt mitten darin gibt den Stand zurück (D614 Beschluss 4)."""
    geholt = 0
    abgewiesen: dict[str, int] = {}
    lieferungen: list[tuple[str | None, bytes]] = [*objekte, *((None, data) for data in claims)]
    for kind, data in lieferungen:
        try:
            if kind is None:
                name = mein.liefern_claim(data)
            else:
                name = mein.liefern_objekt(kind, data)
        except Getrennt:
            return geholt, abgewiesen, True
        if name is None:
            geholt += 1
        else:
            abgewiesen[name] = abgewiesen.get(name, 0) + 1
    return geholt, abgewiesen, False


def holen(mein: HttpKnoten, nachbar: Quelle) -> Ergebnis:
    """Gleicht ab und fragt dann einmal ``paket`` (D617 Beschluss 4, D614 Beschluss 4).

    ``nachbar.bestand`` wird nicht gefragt. Eine formwidrige Antwort, vom Draht oder aus
    dem Abgleich, zählt einmal und liefert nichts ein. Nach ``RUNDEN`` holt er, was bis
    dahin fehlt. ``fehlend`` ist je Art angefragt weniger geliefert, nie negativ. Was
    ungefragt im Bündel steht, wird eingeliefert; der Knoten urteilt (D615 Beschluss 2).
    """
    try:
        meine_claims, meine_objekte = mein.bestand()
    except Getrennt:
        return Ergebnis(0, {}, True, 0, 0)
    abgleich = rbsr.Abgleich(rbsr.schluessel(meine_claims, meine_objekte))
    try:
        while (anfrage := abgleich.naechste()) is not None:
            roh = nachbar.abgleich(anfrage)
            abgleich.auswerten(rbsr.lesen(roh, vom_boten=False))
    except Formwidrig:
        return Ergebnis(0, {}, False, 0, 1)
    except rbsr.Formwidrig:
        return Ergebnis(0, {}, False, 0, 1)
    except Getrennt:
        return Ergebnis(0, {}, True, 0, 0)
    fehlende_claims = sorted(key[1:] for key in abgleich.fehlt if key[0] == rbsr.ART_CLAIM)
    fehlende_objekte = sorted(key[1:] for key in abgleich.fehlt if key[0] == rbsr.ART_OBJEKT)
    if not fehlende_claims and not fehlende_objekte:
        return Ergebnis(0, {}, False, 0, 0)
    try:
        roh = nachbar.paket(fehlende_claims, fehlende_objekte)
    except Formwidrig:
        return Ergebnis(0, {}, False, 0, 1)
    except Getrennt:
        return Ergebnis(0, {}, True, 0, 0)
    try:
        claims, objekte = buendel.lesen(roh)
    except buendel.Formwidrig:
        return Ergebnis(0, {}, False, 0, 1)
    fehlend = max(0, len(fehlende_claims) - len(claims)) + max(
        0, len(fehlende_objekte) - len(objekte)
    )
    geholt, abgewiesen, getrennt = einliefern(mein, claims, objekte)
    return Ergebnis(geholt, abgewiesen, getrennt, fehlend, 0)


def sperrliste(text: str) -> frozenset[bytes]:
    """Je Zeile leer oder eine Adresse aus 16 Bytes in Hex, sonst formwidrig (D594 Beschluss 3)."""
    adressen: set[bytes] = set()
    for zeile in text.splitlines():
        zeile = zeile.strip()
        if not zeile:
            continue
        try:
            adresse = bytes.fromhex(zeile)
        except ValueError as exc:
            raise Formwidrig() from exc
        if len(adresse) != 16:
            raise Formwidrig()
        adressen.add(adresse)
    return frozenset(adressen)


def sperren_lesen(pfad: Path) -> frozenset[bytes] | None:
    """Ohne Datei ist niemand gesperrt; unlesbar oder formwidrig ``None`` (D594 Beschluss 3)."""
    try:
        text = pfad.read_text(encoding="utf-8")
    except FileNotFoundError:
        return frozenset()
    except (OSError, UnicodeDecodeError):
        return None
    try:
        return sperrliste(text)
    except Formwidrig:
        return None


def sperrstand(
    sperren: Path | None,
    zuletzt: frozenset[bytes] | None,
    melden: Callable[[str], None],
) -> frozenset[bytes] | None:
    """Liest die Sperrliste wie der Rundgang; ohne Datei ist niemand gesperrt (D611 Beschluss 3).

    Weicht sie von ``zuletzt`` ab, steht einmal ``gesperrt=<Zahl>`` oder ``sperren formwidrig``.
    Rückgabe: die gelesene Liste.
    """
    gesperrt = frozenset() if sperren is None else sperren_lesen(sperren)
    if gesperrt != zuletzt:
        melden("sperren formwidrig" if gesperrt is None else f"gesperrt={len(gesperrt)}")
    return gesperrt


def rundgang(
    mein: HttpKnoten,
    quellen: list[tuple[bytes, Quelle]],
    sperren: Path | None,
    zuletzt: frozenset[bytes] | None,
    melden: Callable[[str], None],
) -> frozenset[bytes] | None:
    """Vor jedem Nachbarn ``sperrstand``, keinen gesperrten fragen (D594 Beschluss 3, D611 Beschluss 3).

    Ändert sich die gelesene Liste gegenüber ``zuletzt``, steht das einmal als Zeile; ist sie
    formwidrig, wird kein Nachbar gefragt. Rückgabe: die zuletzt gelesene Liste.
    """
    for ziel, nachbar in quellen:
        gesperrt = sperrstand(sperren, zuletzt, melden)
        zuletzt = gesperrt
        if gesperrt is None or ziel in gesperrt:
            continue
        e = holen(mein, nachbar)
        if e.geholt or e.abgewiesen or e.fehlend or e.formwidrig:
            melden(
                f"{ziel.hex()}: geholt={e.geholt} abgewiesen={e.abgewiesen} "
                f"fehlend={e.fehlend} formwidrig={e.formwidrig}"
            )
    return zuletzt


def rundruf_stuecke(
    claims: list[bytes], objekte: list[tuple[str, bytes]], platz: int
) -> list[bytes]:
    """Passt alles in ``platz``, geht ein Bündel; sonst je Eintrag, Objekte vor Claims
    (D636 Beschluss 3)."""
    if not claims and not objekte:
        return []
    alles = buendel.schreiben(claims, objekte)
    if len(alles) <= platz:
        return [alles]
    stuecke: list[bytes] = []
    for art, daten in objekte:
        stueck = buendel.schreiben([], [(art, daten)])
        if len(stueck) <= platz:
            stuecke.append(stueck)
    for claim in claims:
        stueck = buendel.schreiben([claim], [])
        if len(stueck) <= platz:
            stuecke.append(stueck)
    return stuecke


class Grenze:
    """Höchstens ``anzahl`` Aufrufe je Absender innerhalb ``fenster`` (D636 Beschluss 5)."""

    def __init__(self, anzahl: int, fenster: float) -> None:
        self.anzahl = anzahl
        self.fenster = fenster
        self._aufrufe: dict[bytes, list[float]] = {}

    def erlaubt(self, wer: bytes, jetzt: float) -> bool:
        """Wahr und gezählt, wenn im Fenster weniger als ``anzahl`` liegen (D636 Beschluss 5).

        Ein Aufruf, der genau ``fenster`` alt ist, zählt nicht mehr. Ein abgelehnter zählt nicht.
        """
        bisher = [zeit for zeit in self._aufrufe.get(wer, ()) if jetzt - zeit < self.fenster]
        if len(bisher) >= self.anzahl:
            self._aufrufe[wer] = bisher
            return False
        bisher.append(jetzt)
        self._aufrufe[wer] = bisher
        return True


class Rundruf:
    """Eigene neue Einträge einmal hinaus, Annahme nur von Nachbarn (D636)."""

    def __init__(
        self,
        mein: HttpKnoten,
        eigene: bytes,
        signieren: Callable[[bytes], bytes],
        pruefen: Callable[[bytes, bytes, bytes], bool | None],
        quellen: Sequence[bytes],
        platz: int,
        fenster: float,
        melden: Callable[[str], None],
    ) -> None:
        self.mein = mein
        self.eigene = eigene
        self.signieren = signieren
        self.pruefen = pruefen
        self.quellen = quellen
        self.platz = platz
        self.melden = melden
        self._grenze = Grenze(RUNDRUF_ANZAHL, fenster)
        self._vorher: set[tuple[int, bytes]] | None = None
        self._gehalten: list[bytes] = []
        self._sperre = threading.Lock()

    def senden(self, claims: list[bytes], objekte: list[bytes], jetzt: float) -> list[bytes]:
        """Neu seit dem letzten Bestand, der erste nicht; höchstens die Grenze
        (D636 Beschluss 2, 3 und 5)."""
        bestand = {(rbsr.ART_OBJEKT, kennung) for kennung in objekte}
        bestand.update((rbsr.ART_CLAIM, kennung) for kennung in claims)
        with self.mein.sperre:
            vorher = self._vorher
            self._vorher = bestand
            if vorher is None:
                neu: set[tuple[int, bytes]] = set()
            else:
                neu = bestand - vorher - self.mein.eingeliefert
            self.mein.eingeliefert -= bestand
        if not neu:
            return []
        objekte_neu: list[tuple[str, bytes]] = []
        for kennung in sorted(k for art, k in neu if art == rbsr.ART_OBJEKT):
            gefunden = self.mein.objekt(kennung)
            if gefunden is not None:
                objekte_neu.append(gefunden)
        claims_neu: list[bytes] = []
        for kennung in sorted(k for art, k in neu if art == rbsr.ART_CLAIM):
            daten = self.mein.claim(kennung)
            if daten is not None:
                claims_neu.append(daten)
        pakete: list[bytes] = []
        for stueck in rundruf_stuecke(claims_neu, objekte_neu, self.platz):
            with self._sperre:
                if not self._grenze.erlaubt(self.eigene, jetzt):
                    break
            pakete.append(self.eigene + self.signieren(RUNDRUF_MARKE + stueck) + stueck)
        return pakete

    def empfangen(self, data: object, jetzt: float, gesperrt: frozenset[bytes] | None) -> None:
        """Angenommen nur aus ``quellen``, ungesperrt, mit gültiger Signatur (D636 Beschluss 4 und 5)."""
        if type(data) is not bytes or len(data) <= RUNDRUF_KOPF:
            return
        von = data[:16]
        if von not in self.quellen or gesperrt is None or von in gesperrt:
            return
        stueck = data[RUNDRUF_KOPF:]
        ergebnis = self.pruefen(von, data[16:RUNDRUF_KOPF], RUNDRUF_MARKE + stueck)
        if ergebnis is None:
            with self._sperre:
                if len(self._gehalten) < RUNDRUF_GEHALTEN and data not in self._gehalten:
                    self._gehalten.append(data)
            return
        if not ergebnis:
            return
        with self._sperre:
            if not self._grenze.erlaubt(von, jetzt):
                return
        try:
            claims, objekte = buendel.lesen(stueck)
        except buendel.Formwidrig:
            return
        geholt, abgewiesen, _getrennt = einliefern(self.mein, claims, objekte)
        if geholt or abgewiesen:
            self.melden(f"{von.hex()}: rundruf geholt={geholt} abgewiesen={abgewiesen}")

    def nachholen(self, von: bytes, jetzt: float, gesperrt: frozenset[bytes] | None) -> None:
        """Gibt Gehaltenes dieses Absenders an ``empfangen`` (D636 Beschluss 4)."""
        with self._sperre:
            weiter = [item for item in self._gehalten if item[:16] == von]
            self._gehalten = [item for item in self._gehalten if item[:16] != von]
        for item in weiter:
            self.empfangen(item, jetzt, gesperrt)
