"""Abgleich zweier Knoten in einer Runde (D516 Beschluss 1 und 4, D514 Beschluss 2)."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

_ZEITLIMIT = 10


@dataclass(frozen=True)
class Runde:
    """Was eine Runde meldet (D516 Beschluss 4)."""

    eingeliefert: int
    abgewiesen: dict[str, int]
    getrennt: bool


class _Getrennt(Exception):
    """Ein Knoten antwortet mit 503 (D516 Beschluss 3 und 4)."""


def _anfrage(url: str, method: str, route: str, payload: object = None) -> tuple[int, Any]:
    """Eine Anfrage an einen Knoten; 503 beendet die Runde (D516 Beschluss 4)."""
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url.rstrip("/") + route,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=_ZEITLIMIT) as response:
            status, body = response.status, response.read()
    except urllib.error.HTTPError as exc:
        status, body = exc.code, exc.read()
    if status == 503:
        raise _Getrennt()
    if status not in {200, 400} or (status == 400 and method != "POST"):
        raise RuntimeError(f"{method} {route}: {status}")
    return status, json.loads(body)


def _lesen(url: str, route: str) -> Any:
    return _anfrage(url, "GET", route)[1]


def _hex32(item: object) -> bool:
    if not isinstance(item, str) or len(item) != 64:
        return False
    try:
        return bytes.fromhex(item).hex() == item
    except ValueError:
        return False


def pruefen(bestand: object) -> tuple[set[str], set[str]]:
    """Form einer Bestandsliste: Claims und Objekte, je Hex zu 32 Byte (D516 Beschluss 2 und 4)."""
    if not isinstance(bestand, dict) or set(bestand) != {"claims", "objects"}:
        raise ValueError("Bestandsliste ist kein Objekt mit claims und objects")
    for key in ("claims", "objects"):
        entries = bestand[key]
        if not isinstance(entries, list) or not all(_hex32(item) for item in entries):
            raise ValueError(f"{key} ist keine Liste aus Hex zu 32 Byte")
    return set(bestand["claims"]), set(bestand["objects"])


def _holen(
    url: str, claims: set[str], objects: set[str]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Fehlende Objekte und Claims beim Knoten, der sie hält, je nach Hex sortiert (D516 Beschluss 1)."""
    geholt_objekte = [_lesen(url, f"/peer/objects/{digest}") for digest in sorted(objects)]
    geholt_claims = [_lesen(url, f"/peer/claims/{cid}") for cid in sorted(claims)]
    return geholt_objekte, geholt_claims


def runde(url_a: str, url_b: str) -> Runde:
    """Eine Runde: zuerst lesen, dann einliefern, an A vor B (D516 Beschluss 1 und 4)."""
    eingeliefert = 0
    abgewiesen: dict[str, int] = {}
    try:
        claims_a, objects_a = pruefen(_lesen(url_a, "/peer/bestand"))
        claims_b, objects_b = pruefen(_lesen(url_b, "/peer/bestand"))
        fuer_a = _holen(url_b, claims_b - claims_a, objects_b - objects_a)
        fuer_b = _holen(url_a, claims_a - claims_b, objects_a - objects_b)
        for url, (objekte, claims) in ((url_a, fuer_a), (url_b, fuer_b)):
            lieferungen = [("/peer/objects", item) for item in objekte]
            lieferungen += [("/peer/claims", item) for item in claims]
            for route, payload in lieferungen:
                status, answer = _anfrage(url, "POST", route, payload)
                if status == 200:
                    eingeliefert += 1
                else:
                    name = answer if isinstance(answer, str) else json.dumps(answer)
                    abgewiesen[name] = abgewiesen.get(name, 0) + 1
    except _Getrennt:
        return Runde(eingeliefert, abgewiesen, True)
    return Runde(eingeliefert, abgewiesen, False)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: python -m tools.abgleich <url_a> <url_b>")
    result = runde(sys.argv[1], sys.argv[2])
    print(
        f"eingeliefert={result.eingeliefert} "
        f"abgewiesen={json.dumps(result.abgewiesen, sort_keys=True)} "
        f"getrennt={result.getrennt}"
    )


if __name__ == "__main__":
    main()
