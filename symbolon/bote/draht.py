"""Die Bytes zwischen zwei Boten, ohne Transport (D585 Beschluss 1 und 2, D584 Beschluss 3).

Jede Antwort ist kanonisches CBOR (01 §3): ``[0, inhalt]`` bei Erfolg, ``[1]`` getrennt,
``[2]`` fehlt, ``[3]`` formwidrige Anfrage.
"""

from __future__ import annotations

from symbolon import cbor_canon
from symbolon.bote.kern import Formwidrig, Getrennt, Quelle

OK = 0
GETRENNT = 1
FEHLT = 2
FORMWIDRIG = 3
PFADE = ("bestand", "claim", "object")


def _anfrage_gilt(pfad: str, data: object) -> bool:
    """Die Form einer Anfrage (D585 Beschluss 1)."""
    if pfad == "bestand":
        return data is None
    if pfad in ("claim", "object"):
        return isinstance(data, bytes) and len(data) == 32
    return False


def beantworten(quelle: Quelle, pfad: str, data: object) -> bytes:
    """Die Antwort auf eine Anfrage; eine formwidrige fragt die Quelle nicht (D585 Beschluss 2)."""
    if not _anfrage_gilt(pfad, data):
        return cbor_canon.encode([FORMWIDRIG])
    try:
        if pfad == "bestand":
            claims, objekte = quelle.bestand()
            return cbor_canon.encode([OK, [list(claims), list(objekte)]])
        if pfad == "claim":
            found = quelle.claim(data)
            return cbor_canon.encode([FEHLT] if found is None else [OK, found])
        found = quelle.objekt(data)
        return cbor_canon.encode([FEHLT] if found is None else [OK, list(found)])
    except Getrennt:
        return cbor_canon.encode([GETRENNT])


def _ist_code(wert: object, code: int) -> bool:
    """Genau ``[code]``, ohne Wahrheitswert oder Gleitkommazahl."""
    return isinstance(wert, list) and len(wert) == 1 and type(wert[0]) is int and wert[0] == code


def _liste32(wert: object) -> bool:
    return isinstance(wert, list) and all(
        isinstance(item, bytes) and len(item) == 32 for item in wert
    )


def lesen(pfad: str, antwort: object) -> object:
    """Eine Antwort in der Form aus D585 Beschluss 1; alles andere ist ``Formwidrig``.

    ``[2]`` auf ``bestand`` ist formwidrig (D585 Beschluss 2).
    """
    if not isinstance(antwort, bytes):
        raise Formwidrig()
    try:
        kanonisch = cbor_canon.is_canonical(antwort)
    except Exception as exc:
        raise Formwidrig() from exc
    if not kanonisch:
        raise Formwidrig()
    wert = cbor_canon.decode(antwort)
    if _ist_code(wert, GETRENNT):
        raise Getrennt()
    if pfad in ("claim", "object") and _ist_code(wert, FEHLT):
        return None
    if not (isinstance(wert, list) and len(wert) == 2 and type(wert[0]) is int and wert[0] == OK):
        raise Formwidrig()
    inhalt = wert[1]
    if pfad == "bestand":
        if isinstance(inhalt, list) and len(inhalt) == 2 and all(map(_liste32, inhalt)):
            return inhalt[0], inhalt[1]
    elif pfad == "claim":
        if isinstance(inhalt, bytes):
            return inhalt
    elif pfad == "object":
        if (
            isinstance(inhalt, list)
            and len(inhalt) == 2
            and isinstance(inhalt[0], str)
            and isinstance(inhalt[1], bytes)
        ):
            return inhalt[0], inhalt[1]
    raise Formwidrig()
