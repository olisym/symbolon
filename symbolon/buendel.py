"""Das Bündel: Hülle, Kompression und Obergrenze (D614 Beschluss 2 und 3, 01 §3)."""

from __future__ import annotations

import zlib

from symbolon import cbor_canon

KENNUNG = "symbolon-buendel"
VERSION = 1
GRENZE = 1048576


class Formwidrig(ValueError):
    """Ein Bündel hat nicht die Form aus D614 Beschluss 2."""


def _kopf(anzahl: int) -> int:
    """Bytes eines CBOR-Arraykopfes, höchstens 9 (D614 Beschluss 3)."""
    if anzahl < 24:
        return 1
    if anzahl < 256:
        return 2
    if anzahl < 65536:
        return 3
    if anzahl < 2**32:
        return 5
    return 9


def _groesse(summe: int, claims: int, objekte: int) -> int:
    """Summe der kodierten Einträge plus die drei Arrayköpfe (D614 Beschluss 3)."""
    return summe + _kopf(2) + _kopf(claims) + _kopf(objekte)


def packen(claims: list[bytes], objekte: list[tuple[str, bytes]]) -> tuple[bytes, int]:
    """Objekte vor Claims; ab dem ersten, der nicht passt, fällt der Rest (D614 Beschluss 3).

    Die Grösse des Inneren ist die Summe der kodierten Einträge plus höchstens drei
    Kopfzeilen von je 9 Bytes, ohne das Innere je Eintrag neu zu kodieren.
    """
    genommen_claims: list[bytes] = []
    genommen_objekte: list[tuple[str, bytes]] = []
    summe = 0
    vollstaendig = True
    for art, daten in objekte:
        roh = cbor_canon.encode([art, daten])
        if _groesse(summe + len(roh), 0, len(genommen_objekte) + 1) > GRENZE:
            vollstaendig = False
            break
        genommen_objekte.append((art, daten))
        summe += len(roh)
    if vollstaendig:
        for claim in claims:
            roh = cbor_canon.encode(claim)
            naechste = _groesse(summe + len(roh), len(genommen_claims) + 1, len(genommen_objekte))
            if naechste > GRENZE:
                break
            genommen_claims.append(claim)
            summe += len(roh)
    weggelassen = (len(objekte) - len(genommen_objekte)) + (len(claims) - len(genommen_claims))
    innen = cbor_canon.encode(
        [genommen_claims, [[art, daten] for art, daten in genommen_objekte]]
    )
    return cbor_canon.encode([KENNUNG, VERSION, zlib.compress(innen)]), weggelassen


def schreiben(claims: list[bytes], objekte: list[tuple[str, bytes]]) -> bytes:
    """``packen`` ohne die Zahl der weggelassenen Einträge (D614 Beschluss 2)."""
    roh, _weggelassen = packen(claims, objekte)
    return roh


def _entpacken(komprimiert: bytes) -> bytes:
    """Höchstens ``GRENZE + 1`` Bytes; abgeschnitten oder gefolgt ist formwidrig
    (D614 Beschluss 2)."""
    dec = zlib.decompressobj()
    try:
        innen = dec.decompress(komprimiert, max_length=GRENZE + 1)
    except zlib.error as exc:
        raise Formwidrig() from exc
    if dec.unused_data or dec.unconsumed_tail or not dec.eof:
        raise Formwidrig()
    if len(innen) > GRENZE:
        raise Formwidrig()
    return innen


def _innen(wert: object) -> tuple[list[bytes], list[tuple[str, bytes]]]:
    """Claims als Bytes, Objekte als Paar aus Art und Bytes (D614 Beschluss 2)."""
    if not isinstance(wert, list) or len(wert) != 2:
        raise Formwidrig()
    claims, objekte = wert
    if not isinstance(claims, list) or not all(type(item) is bytes for item in claims):
        raise Formwidrig()
    if not isinstance(objekte, list):
        raise Formwidrig()
    paare: list[tuple[str, bytes]] = []
    for eintrag in objekte:
        if (
            not isinstance(eintrag, list)
            or len(eintrag) != 2
            or type(eintrag[0]) is not str
            or type(eintrag[1]) is not bytes
        ):
            raise Formwidrig()
        paare.append((eintrag[0], eintrag[1]))
    return claims, paare


def lesen(data: object) -> tuple[list[bytes], list[tuple[str, bytes]]]:
    """Hülle und Inneres; jeder formwidrige Fall aus D614 Beschluss 2."""
    if type(data) is not bytes:
        raise Formwidrig()
    try:
        kanonisch = cbor_canon.is_canonical(data)
    except Exception as exc:
        raise Formwidrig() from exc
    if not kanonisch:
        raise Formwidrig()
    wert = cbor_canon.decode(data)
    if not isinstance(wert, list) or len(wert) != 3:
        raise Formwidrig()
    kennung, version, komprimiert = wert
    if type(kennung) is not str or kennung != KENNUNG:
        raise Formwidrig()
    if type(version) is not int or version != VERSION:
        raise Formwidrig()
    if type(komprimiert) is not bytes:
        raise Formwidrig()
    innen = _entpacken(komprimiert)
    try:
        kanonisch = cbor_canon.is_canonical(innen)
    except Exception as exc:
        raise Formwidrig() from exc
    if not kanonisch:
        raise Formwidrig()
    return _innen(cbor_canon.decode(innen))
