"""Die Bytes zwischen zwei Boten, ohne Transport (D585 Beschluss 1 und 2, D617 Beschluss 5).

Jede Antwort ist kanonisches CBOR (01 §3): ``[0, inhalt]`` bei Erfolg, ``[1]`` getrennt,
``[3]`` formwidrige Anfrage. ``[2]`` bleibt vergeben und ist auf jedem Pfad formwidrig
(D614 Beschluss 4). ``abgleich`` trägt die Nachricht als Bytes (D617 Beschluss 5).
"""

from __future__ import annotations

from symbolon import cbor_canon
from symbolon.bote import rbsr
from symbolon.bote.kern import Formwidrig, Getrennt, Quelle

OK = 0
GETRENNT = 1
FEHLT = 2
FORMWIDRIG = 3
PFADE = ("bestand", "paket", "abgleich")


def _anfrage_gilt(pfad: str, data: object) -> bool:
    """Die Form einer Anfrage (D585 Beschluss 1, D614 Beschluss 4, D617 Beschluss 5)."""
    if pfad == "bestand":
        return data is None
    if pfad == "paket":
        return isinstance(data, list) and len(data) == 2 and all(map(_liste32, data))
    if pfad == "abgleich":
        return _abgleich_gilt(data)
    return False


def _abgleich_gilt(data: object) -> bool:
    """Boten-Nachricht, sonst wird die Quelle nicht gefragt (D617 Beschluss 5)."""
    if type(data) is not bytes:
        return False
    try:
        rbsr.lesen(data, vom_boten=True)
    except rbsr.Formwidrig:
        return False
    return True


def beantworten(quelle: Quelle, pfad: str, data: object) -> bytes:
    """Die Antwort auf eine Anfrage; eine formwidrige fragt die Quelle nicht (D585 Beschluss 2)."""
    if not _anfrage_gilt(pfad, data):
        return cbor_canon.encode([FORMWIDRIG])
    try:
        if pfad == "bestand":
            claims, objekte = quelle.bestand()
            return cbor_canon.encode([OK, [list(claims), list(objekte)]])
        if pfad == "abgleich":
            return cbor_canon.encode([OK, quelle.abgleich(data)])
        inhalt = quelle.paket(data[0], data[1])
        return cbor_canon.encode([OK, inhalt])
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
    """Eine Antwort in der Form aus D614 Beschluss 4; alles andere ist ``Formwidrig``.

    ``[2]`` bleibt vergeben und ist auf jedem Pfad formwidrig (D614 Beschluss 4).
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
    if _ist_code(wert, FEHLT):
        raise Formwidrig()
    if not (isinstance(wert, list) and len(wert) == 2 and type(wert[0]) is int and wert[0] == OK):
        raise Formwidrig()
    inhalt = wert[1]
    if pfad == "bestand":
        if isinstance(inhalt, list) and len(inhalt) == 2 and all(map(_liste32, inhalt)):
            return inhalt[0], inhalt[1]
    elif pfad == "paket" and isinstance(inhalt, bytes):
        return inhalt
    elif pfad == "abgleich" and type(inhalt) is bytes:
        return inhalt
    raise Formwidrig()
