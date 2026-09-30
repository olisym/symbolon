"""Das Bündel: Hülle, Kompression, Obergrenze und der formwidrige Fall (D614)."""

from __future__ import annotations

import zlib

import pytest

from symbolon import buendel, cbor_canon
from symbolon.buendel import GRENZE, KENNUNG, VERSION, Formwidrig, lesen, packen, schreiben
from symbolon.node import api

_C = [b"claim-eins", b"claim-zwei"]
_O = [("proposal", b"objekt-eins")]


def _huelle(innen: bytes, kennung: object = KENNUNG, version: object = VERSION) -> bytes:
    return cbor_canon.encode([kennung, version, zlib.compress(innen)])


def _innen_der_laenge(n: int) -> bytes:
    """Ein gültiges Inneres mit genau ``n`` Bytes: ein Claim aus Nullbytes."""
    for k in range(n - 16, n):
        innen = cbor_canon.encode([[bytes(k)], []])
        if len(innen) == n:
            return innen
    raise AssertionError(n)


def test_festwerte() -> None:
    """Kennung, Version und Grenze; die Grenze ist das ``_LIMIT`` des Knotens (D614 Beschluss 3)."""
    assert (KENNUNG, VERSION) == ("symbolon-buendel", 1)
    assert GRENZE == api._LIMIT


def test_hin_und_zurueck() -> None:
    """Was ``schreiben`` packt, gibt ``lesen`` gleich zurück."""
    assert lesen(schreiben(_C, _O)) == (_C, _O)
    assert lesen(schreiben([], [])) == ([], [])


def test_hülle_lesbar_ohne_entpacken() -> None:
    """Kennung und Version stehen ungepackt in kanonischem CBOR (D614 Beschluss 2)."""
    huelle = cbor_canon.decode(schreiben(_C, _O))
    assert huelle[:2] == [KENNUNG, VERSION]
    assert cbor_canon.decode(zlib.decompress(huelle[2])) == [_C, [list(o) for o in _O]]


def test_objekte_vor_claims_beim_kuerzen() -> None:
    """Über der Grenze zuerst die Objekte, dann die Claims; der Rest zählt als weggelassen."""
    gross = GRENZE // 4
    claims = [b"c" * gross, b"d" * gross]
    objekte = [("proposal", b"o" * gross), ("motion", b"m" * gross)]
    roh, weggelassen = packen(claims, objekte)
    assert weggelassen == 1
    assert lesen(roh) == ([claims[0]], objekte)


def test_nach_einem_weggelassenen_nichts_mehr() -> None:
    """Weggelassen wird ab dem ersten Eintrag, der nicht passt; kein kleinerer rückt nach."""
    roh, weggelassen = packen([b"klein"], [("proposal", b"o" * GRENZE)])
    assert weggelassen == 2
    assert lesen(roh) == ([], [])


def test_grenze_genau() -> None:
    """Genau ``GRENZE`` Bytes entpackt gilt, ein Byte mehr ist formwidrig (D614 Beschluss 3)."""
    genau = _innen_der_laenge(GRENZE)
    assert lesen(_huelle(genau))[0] == [bytes(len(cbor_canon.decode(genau)[0][0]))]
    with pytest.raises(Formwidrig):
        lesen(_huelle(_innen_der_laenge(GRENZE + 1)))


def test_bombe() -> None:
    """Ein kleines Bündel, das weit über die Grenze entpackt, wird nicht ganz entpackt."""
    innen = cbor_canon.encode([[bytes(64 * GRENZE)], []])
    roh = _huelle(innen)
    assert len(roh) < GRENZE // 8
    with pytest.raises(Formwidrig):
        lesen(roh)


_GUT = cbor_canon.encode([_C, [list(o) for o in _O]])


@pytest.mark.parametrize(
    "roh",
    [
        None,
        "text",
        b"",
        b"\xff",
        _huelle(_GUT, kennung="symbolon-bündel"),
        _huelle(_GUT, kennung=b"symbolon-buendel"),
        _huelle(_GUT, version=2),
        _huelle(_GUT, version=True),
        cbor_canon.encode([KENNUNG, VERSION]),
        cbor_canon.encode([KENNUNG, VERSION, zlib.compress(_GUT), b""]),
        cbor_canon.encode([KENNUNG, VERSION, "kein zlib"]),
        cbor_canon.encode([KENNUNG, VERSION, b"kein zlib"]),
        cbor_canon.encode([KENNUNG, VERSION, zlib.compress(_GUT)[:-4]]),
        cbor_canon.encode([KENNUNG, VERSION, zlib.compress(_GUT) + b"\x00"]),
        cbor_canon.encode([KENNUNG, VERSION, zlib.compress(_GUT) + zlib.compress(_GUT)]),
        _huelle(b"\x82\x18\x00"),
        _huelle(b"\x82\x80\x98\x00"),
        _huelle(cbor_canon.encode([_C])),
        _huelle(cbor_canon.encode([_C, [["proposal"]]])),
        _huelle(cbor_canon.encode([_C, [[1, b"x"]]])),
        _huelle(cbor_canon.encode([["text"], []])),
        _huelle(cbor_canon.encode({"claims": _C})),
    ],
)
def test_formwidrig(roh: object) -> None:
    """Jedes Bündel ausserhalb der Form ist ``Formwidrig`` (D614 Beschluss 2)."""
    with pytest.raises(Formwidrig):
        lesen(roh)


def test_nicht_kanonische_huelle() -> None:
    """Eine nicht kanonische Hülle mit sonst gutem Inhalt ist formwidrig (01 §3)."""
    gut = schreiben(_C, _O)
    schlecht = b"\x83\x78\x10" + gut[2:]
    assert cbor_canon.decode(schlecht) == cbor_canon.decode(gut)
    with pytest.raises(Formwidrig):
        lesen(schlecht)


def test_formwidrig_ist_valueerror() -> None:
    """``Formwidrig`` ist ein ``ValueError``; ``holen`` fängt es genau so (D614 Beschluss 4)."""
    assert issubclass(buendel.Formwidrig, ValueError)
