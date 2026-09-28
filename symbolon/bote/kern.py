"""Holen ohne Transport: der eigene Knoten holt von einem Nachbarn (D584 Beschluss 1 und 2).

Der Nachbar wird nur gefragt, nie beliefert. Was ein Holen meldet, steht in D585 Beschluss 3.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Protocol

_ZEITLIMIT = 10


class Getrennt(Exception):
    """Ein Knoten oder ein Nachbar ist nicht erreichbar oder getrennt (D516 Beschluss 3)."""


class Formwidrig(Exception):
    """Eine Antwort hat nicht die Form auf dem Draht (D585 Beschluss 2)."""


@dataclass(frozen=True)
class Ergebnis:
    """Was ein Holen meldet (D585 Beschluss 3, D516 Beschluss 4)."""

    geholt: int
    abgewiesen: dict[str, int]
    getrennt: bool
    fehlend: int
    formwidrig: int


class Quelle(Protocol):
    """Was ein Bote lesen kann; keine Methode zum Einliefern (D584 Beschluss 2)."""

    def bestand(self) -> tuple[list[bytes], list[bytes]]: ...

    def claim(self, cid: bytes) -> bytes | None: ...

    def objekt(self, digest: bytes) -> tuple[str, bytes] | None: ...


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


def holen(mein: HttpKnoten, nachbar: Quelle) -> Ergebnis:
    """Zuerst lesen, dann einliefern, Objekte vor Claims (D584 Beschluss 2, D516 Beschluss 1).

    Ein fehlender oder formwidriger Eintrag wird gezählt und übersprungen, ein formwidriger
    Bestand beendet das Holen (D585 Beschluss 2 und 3).
    """
    try:
        meine_claims, meine_objekte = mein.bestand()
    except Getrennt:
        return Ergebnis(0, {}, True, 0, 0)
    fehlend = 0
    formwidrig = 0
    objekte: list[tuple[str, bytes]] = []
    claims: list[bytes] = []
    try:
        try:
            seine_claims, seine_objekte = nachbar.bestand()
        except Formwidrig:
            return Ergebnis(0, {}, False, fehlend, formwidrig + 1)
        for digest in sorted(set(seine_objekte) - set(meine_objekte)):
            try:
                found = nachbar.objekt(digest)
            except Formwidrig:
                formwidrig += 1
                continue
            if found is None:
                fehlend += 1
            else:
                objekte.append(found)
        for cid in sorted(set(seine_claims) - set(meine_claims)):
            try:
                data = nachbar.claim(cid)
            except Formwidrig:
                formwidrig += 1
                continue
            if data is None:
                fehlend += 1
            else:
                claims.append(data)
    except Getrennt:
        return Ergebnis(0, {}, True, fehlend, formwidrig)
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
            return Ergebnis(geholt, abgewiesen, True, fehlend, formwidrig)
        if name is None:
            geholt += 1
        else:
            abgewiesen[name] = abgewiesen.get(name, 0) + 1
    return Ergebnis(geholt, abgewiesen, False, fehlend, formwidrig)
