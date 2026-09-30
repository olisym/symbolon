"""Die Bytes zwischen zwei Boten (D584 Beschluss 3)."""

from __future__ import annotations

import cbor2
import pytest

from symbolon import buendel, cbor_canon
from symbolon.bote import rbsr
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

    def abgleich(self, roh: bytes):
        self._pruefen()
        self.abgeglichen = roh
        return rbsr.kodieren([(None, rbsr.SKIP, None)])

    def paket(self, claims: list[bytes], objekte: list[bytes]):
        self._pruefen()
        self.gefragt = (claims, objekte)
        return buendel.schreiben(
            [b"claim-bytes" for c in claims if c == _C],
            [("proposal", b"objekt-bytes") for o in objekte if o == _O],
        )


def test_codes() -> None:
    """Die Codes und die Pfade sind fest (D584 Beschluss 3)."""
    assert (OK, GETRENNT, FEHLT, FORMWIDRIG) == (0, 1, 2, 3)
    assert PFADE == ("bestand", "paket", "abgleich")
    assert beantworten(_Quelle(getrennt=True), "bestand", None) == bytes.fromhex("8101")


def test_hin_und_zurueck() -> None:
    """Was ein Bote beantwortet, liest der andere so, wie die Quelle es gab."""
    q = _Quelle()
    assert lesen("bestand", beantworten(q, "bestand", None)) == ([_C], [_O])
    roh = lesen("paket", beantworten(q, "paket", [[_C, _O], [_O]]))
    assert q.gefragt == ([_C, _O], [_O])
    assert buendel.lesen(roh) == ([b"claim-bytes"], [("proposal", b"objekt-bytes")])
    assert buendel.lesen(lesen("paket", beantworten(q, "paket", [[], []]))) == ([], [])
    anfrage = rbsr.kodieren([(None, rbsr.FP, bytes(16))])
    assert lesen("abgleich", beantworten(q, "abgleich", anfrage)) == rbsr.kodieren(
        [(None, rbsr.SKIP, None)]
    )
    assert q.abgeglichen == anfrage
    for pfad, data in (("bestand", None), ("paket", [[_C], []]), ("abgleich", anfrage)):
        with pytest.raises(Getrennt):
            lesen(pfad, beantworten(_Quelle(getrennt=True), pfad, data))


@pytest.mark.parametrize(
    ("pfad", "data"),
    [
        ("bestand", b""),
        ("paket", None),
        ("paket", _C),
        ("paket", [[_C]]),
        ("paket", [[_C], [], []]),
        ("paket", [[_C[:31]], []]),
        ("paket", [[], [_O + b"\x00"]]),
        ("paket", [[_C.hex()], []]),
        ("paket", [_C, _O]),
        ("abgleich", None),
        ("abgleich", [[None, 0, None]]),
        ("abgleich", b"\xff"),
        ("abgleich", rbsr.kodieren([(None, rbsr.FEHLT, [])])),
        ("abgleich", bytes(rbsr.RAHMEN + 1)),
        ("claim", _C),
        ("object", _O),
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
        ("paket", cbor_canon.encode([OK, "text"])),
        ("paket", cbor_canon.encode([OK, [b""]])),
        ("paket", cbor_canon.encode([FEHLT])),
        ("paket", cbor_canon.encode([7])),
        ("abgleich", cbor_canon.encode([OK, [[None, 0, None]]])),
        ("abgleich", cbor_canon.encode([FEHLT])),
        ("claim", cbor_canon.encode([OK, b"claim-bytes"])),
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
