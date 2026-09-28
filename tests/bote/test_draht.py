"""Die Bytes zwischen zwei Boten (D584 Beschluss 3)."""

from __future__ import annotations

import cbor2
import pytest

from symbolon import cbor_canon
from symbolon.bote.draht import FEHLT, FORMWIDRIG, GETRENNT, OK, PFADE, beantworten, lesen
from symbolon.bote.kern import Formwidrig, Getrennt

_C = bytes(range(32))
_O = bytes(range(32, 64))


class _Quelle:
    def __init__(self, getrennt: bool = False) -> None:
        self.getrennt = getrennt
        self.aufrufe = 0

    def _pruefen(self) -> None:
        self.aufrufe += 1
        if self.getrennt:
            raise Getrennt()

    def bestand(self):
        self._pruefen()
        return [_C], [_O]

    def claim(self, cid: bytes):
        self._pruefen()
        return b"claim-bytes" if cid == _C else None

    def objekt(self, digest: bytes):
        self._pruefen()
        return ("proposal", b"objekt-bytes") if digest == _O else None


def test_codes() -> None:
    """Die Codes und die Pfade sind fest (D584 Beschluss 3)."""
    assert (OK, GETRENNT, FEHLT, FORMWIDRIG) == (0, 1, 2, 3)
    assert PFADE == ("bestand", "claim", "object")
    assert beantworten(_Quelle(getrennt=True), "bestand", None) == bytes.fromhex("8101")


def test_hin_und_zurueck() -> None:
    """Was ein Bote beantwortet, liest der andere so, wie die Quelle es gab."""
    q = _Quelle()
    assert lesen("bestand", beantworten(q, "bestand", None)) == ([_C], [_O])
    assert lesen("claim", beantworten(q, "claim", _C)) == b"claim-bytes"
    assert lesen("claim", beantworten(q, "claim", _O)) is None
    assert lesen("object", beantworten(q, "object", _O)) == ("proposal", b"objekt-bytes")
    assert lesen("object", beantworten(q, "object", _C)) is None
    for pfad, data in (("bestand", None), ("claim", _C), ("object", _O)):
        with pytest.raises(Getrennt):
            lesen(pfad, beantworten(_Quelle(getrennt=True), pfad, data))


@pytest.mark.parametrize(
    ("pfad", "data"),
    [
        ("bestand", b""),
        ("claim", _C[:31]),
        ("claim", _C + b"\x00"),
        ("claim", _C.hex()),
        ("claim", None),
        ("object", 5),
        ("liefern", _C),
    ],
)
def test_formwidrige_anfrage(pfad: str, data: object) -> None:
    """Eine formwidrige Anfrage bekommt [3] und fragt den Knoten nicht."""
    q = _Quelle()
    assert beantworten(q, pfad, data) == cbor_canon.encode([FORMWIDRIG])
    assert q.aufrufe == 0


_GUT = cbor_canon.encode([OK, [[_C], [_O]]])


@pytest.mark.parametrize(
    ("pfad", "antwort"),
    [
        ("bestand", None),
        ("bestand", "8101"),
        ("bestand", b"\xff"),
        ("bestand", _GUT[:-1]),
        ("bestand", b"\x82\x18\x00" + _GUT[2:]),
        ("bestand", cbor_canon.encode([OK])),
        ("bestand", cbor_canon.encode([FEHLT])),
        ("bestand", cbor_canon.encode([FORMWIDRIG])),
        ("bestand", cbor_canon.encode([GETRENNT, 1])),
        ("bestand", cbor_canon.encode([OK, [[_C[:31]], []]])),
        ("bestand", cbor_canon.encode([OK, [[_C]]])),
        ("bestand", cbor_canon.encode([OK, [[_C.hex()], []]])),
        ("bestand", cbor_canon.encode([True, [[], []]])),
        ("bestand", cbor_canon.encode([])),
        ("bestand", cbor_canon.encode({"claims": []})),
        ("claim", cbor_canon.encode([OK, "text"])),
        ("claim", cbor_canon.encode([7])),
        ("object", cbor_canon.encode([OK, [1, b""]])),
        ("object", cbor_canon.encode([OK, ["proposal"]])),
    ],
)
def test_formwidrige_antwort(pfad: str, antwort: object) -> None:
    """Jede Antwort ausserhalb der Form ist Formwidrig, auch nicht kanonisches CBOR (01 §3)."""
    with pytest.raises(Formwidrig):
        lesen(pfad, antwort)


def test_nicht_kanonisch_ist_sonst_gut() -> None:
    """Der nicht kanonische Fall wäre ohne die Prüfung ein guter Bestand."""
    schlecht = b"\x82\x18\x00" + _GUT[2:]
    assert cbor2.loads(schlecht) == cbor2.loads(_GUT)
    assert lesen("bestand", _GUT) == ([_C], [_O])
