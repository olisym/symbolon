"""Holen ohne Transport: der eigene Knoten holt von einem Nachbarn (D584 Beschluss 1 und 2).

Der Nachbar wird nur gefragt, nie beliefert. Was ein Holen meldet, steht in D585 Beschluss 3,
geändert durch D614 Beschluss 4: formwidrig ist nur das Bündel.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from symbolon import buendel

_ZEITLIMIT = 10


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

    def paket(self, claims: list[bytes], objekte: list[bytes]) -> bytes: ...


class HttpKnoten:
    """Der eigene Knoten über die Routen unter ``/peer/`` (D516 Beschluss 2 und 3)."""

    def __init__(self, url: str) -> None:
        self.url = url.rstrip("/")

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
        """``None`` bei Annahme, sonst der Name der Abweisung (D516 Beschluss 2 und 4)."""
        status, body = self._anfrage("POST", "/peer/claims", {"data": data.hex()})
        return None if status == 200 else _name(body)

    def liefern_objekt(self, kind: str, data: bytes) -> str | None:
        """``None`` bei Annahme, sonst der Name der Abweisung (D516 Beschluss 2 und 4)."""
        status, body = self._anfrage("POST", "/peer/objects", {"kind": kind, "data": data.hex()})
        return None if status == 200 else _name(body)


def _name(body: object) -> str:
    return body if isinstance(body, str) else json.dumps(body)


def stand_aus(app_data: object) -> bytes | None:
    """Nur genau 32 Bytes sind ein Stand; alles andere ist formwidrig (D611 Beschluss 1)."""
    if type(app_data) is bytes and len(app_data) == 32:
        return app_data
    return None


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
    """Beide Bestände, bei Fehlendem genau einmal ``paket``, sortiert (D614 Beschluss 4).

    Fehlt nichts, gibt es keine Anfrage. Ein formwidriges Bündel oder eine formwidrige Antwort
    zählt einmal und liefert nichts ein. ``fehlend`` ist je Art angefragt weniger geliefert,
    nie negativ. Was ungefragt im Bündel steht, wird eingeliefert; der Knoten urteilt.
    """
    try:
        meine_claims, meine_objekte = mein.bestand()
    except Getrennt:
        return Ergebnis(0, {}, True, 0, 0)
    try:
        seine_claims, seine_objekte = nachbar.bestand()
    except Formwidrig:
        return Ergebnis(0, {}, False, 0, 1)
    except Getrennt:
        return Ergebnis(0, {}, True, 0, 0)
    fehlende_claims = sorted(set(seine_claims) - set(meine_claims))
    fehlende_objekte = sorted(set(seine_objekte) - set(meine_objekte))
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
    except ValueError:
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
