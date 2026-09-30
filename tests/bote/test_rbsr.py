"""Der Abgleich nach Bereichen: Vollständigkeit, Rahmen, Form (D617)."""

from __future__ import annotations

import random
import time

import pytest
import RNS
from hypothesis import given, settings
from hypothesis import strategies as st
from RNS.vendor import umsgpack

from symbolon import cbor_canon
from symbolon.bote import rbsr
from symbolon.bote.rbsr import (
    ANFRAGE,
    FEHLT,
    FP,
    IDS,
    RAHMEN,
    RUNDEN,
    SKIP,
    Abgleich,
    Formwidrig,
    antworten,
    fingerabdruck,
    kodieren,
    lesen,
    schluessel,
)


def _k(r: random.Random) -> bytes:
    return bytes([r.choice([0, 1])]) + r.randbytes(32)


def _abgleich(bote: list[bytes], nachbar: list[bytes]) -> tuple[set[bytes], int, list[int]]:
    """Ein ganzer Abgleich wie in ``holen``, jede Nachricht über ``lesen``."""
    a = Abgleich(sorted(bote))
    s = sorted(nachbar)
    groessen = []
    while (anfrage := a.naechste()) is not None:
        groessen.append(len(anfrage))
        antwort = kodieren(antworten(s, lesen(anfrage, vom_boten=True)))
        groessen.append(len(antwort))
        a.auswerten(lesen(antwort, vom_boten=False))
    return a.fehlt, a.runden, groessen


def test_festwerte() -> None:
    """Die Parameter aus D617 Beschluss 3."""
    assert (rbsr.TEILUNG, rbsr.LISTE, rbsr.FP_LAENGE, RAHMEN, ANFRAGE, RUNDEN) == (
        4,
        3,
        16,
        380,
        190,
        64,
    )
    assert (SKIP, FP, IDS, FEHLT, rbsr.ART_OBJEKT, rbsr.ART_CLAIM) == (0, 1, 2, 3, 0, 1)


def test_rahmen_passt_in_ein_paket() -> None:
    """Anfrage und Antwort mit ``RAHMEN`` Bytes passen in ein Paket eines Links (D617 Beschluss 3).

    Gepackt wie RNS eine Anfrage und eine Antwort packt, die Antwort in ``[0, …]`` des Drahts.
    """
    anfrage = umsgpack.packb([time.time(), bytes(16), bytes(RAHMEN)])
    antwort = umsgpack.packb([bytes(16), cbor_canon.encode([0, bytes(RAHMEN)])])
    assert max(len(anfrage), len(antwort)) <= RNS.Link.MDU


def test_fingerabdruck_vektoren() -> None:
    """SHA-256 über Anzahl und Schlüssel, 16 Byte (D617 Beschluss 2)."""
    assert fingerabdruck([]).hex() == "af5570f5a1810b7af78caf4bc70a660f"
    assert fingerabdruck([bytes([1]) + bytes(32)]).hex() == "17322efefdc9500b78ffd0ec1d2a8444"


def test_schluessel() -> None:
    """Objekte vor Claims, je die Art als ein Byte vor der Kennung."""
    c, o = bytes(range(32)), bytes(range(1, 33))
    assert schluessel([c], [o]) == [b"\x00" + o, b"\x01" + c]


@settings(max_examples=200, deadline=None)
@given(
    st.integers(0, 300),
    st.integers(0, 40),
    st.integers(0, 40),
    st.integers(0, 2**32),
)
def test_findet_genau_was_fehlt(gemein: int, nur_nachbar: int, nur_bote: int, samen: int) -> None:
    """Der Bote lernt genau, was ihm fehlt; jede Nachricht passt in ``RAHMEN`` (D617)."""
    r = random.Random(samen)
    g = [_k(r) for _ in range(gemein)]
    xn = [_k(r) for _ in range(nur_nachbar)]
    xb = [_k(r) for _ in range(nur_bote)]
    fehlt, runden, groessen = _abgleich(g + xb, g + xn)
    assert fehlt == set(xn)
    assert runden < RUNDEN
    assert max(groessen) <= RAHMEN


def test_gleiche_bestaende_eine_runde() -> None:
    """Bei gleichem Bestand genügt eine Runde, und es fehlt nichts."""
    r = random.Random(7)
    g = [_k(r) for _ in range(300)]
    assert _abgleich(g, g)[:2] == (set(), 1)


def test_runden_begrenzt() -> None:
    """Ein Nachbar, der immer ungleich antwortet, hält den Boten höchstens ``RUNDEN`` Runden."""
    r = random.Random(3)
    a = Abgleich(sorted(_k(r) for _ in range(50)))
    n = 0
    while a.naechste() is not None and n <= RUNDEN:
        n += 1
        a.auswerten([(None, FP, bytes(16))])
    assert n == RUNDEN


def test_leerer_bote_wenige_runden() -> None:
    """Einem leeren Boten schickt der Nachbar volle ``FEHLT``-Listen statt zu teilen (D617).

    Dreissig fehlende Einträge in höchstens vier Runden; ohne das Füllen bis zum Rahmen wären es
    fünf (D617 Befund 8).
    """
    r = random.Random(11)
    nachbar = [_k(r) for _ in range(30)]
    fehlt, runden, _ = _abgleich([], nachbar)
    assert fehlt == set(nachbar)
    assert runden <= 4


def test_kurze_antwort_laesst_rest_offen() -> None:
    """Endet eine Antwort nach dem ersten gefragten Bereich, fragt der Bote die übrigen wieder."""
    r = random.Random(5)
    bote = sorted(_k(r) for _ in range(40))
    nachbar = sorted(_k(r) for _ in range(40))
    a = Abgleich(bote)
    erste = antworten(nachbar, lesen(a.naechste(), vom_boten=True))
    a.auswerten(lesen(kodieren(erste), vom_boten=False))
    gefragt = lesen(a.naechste(), vom_boten=True)
    bereiche = [t for t in gefragt if t[1] != SKIP]
    assert len(bereiche) >= 2
    erste_grenze = bereiche[0][0]
    antwort = [t for t in antworten(nachbar, gefragt) if t[0] is not None and t[0] <= erste_grenze]
    a.auswerten(antwort)
    wieder = lesen(a.naechste(), vom_boten=True)
    assert [t for t in wieder if t[1] != SKIP][0] == bereiche[1]


_GUTE_ID = bytes([1]) + bytes(32)


@pytest.mark.parametrize(
    "wert",
    [
        None,
        [],
        [[None, SKIP]],
        [[None, SKIP, None, 1]],
        [[b"", SKIP, None]],
        [[bytes(34), SKIP, None]],
        [[b"\x05", SKIP, None], [b"\x05", SKIP, None]],
        [[b"\x05", SKIP, None], [b"\x04", SKIP, None]],
        [[None, SKIP, None], [b"\x05", SKIP, None]],
        [[None, 4, None]],
        [[None, True, None]],
        [[None, SKIP, b""]],
        [[None, FP, bytes(15)]],
        [[None, FP, None]],
        [[None, IDS, [bytes(32)]]],
        [[None, IDS, [bytes([2]) + bytes(32)]]],
        [[None, IDS, [_GUTE_ID, _GUTE_ID]]],
        [[b"\x01", IDS, [_GUTE_ID]]],
        [[None, IDS, "keine liste"]],
    ],
)
def test_formwidrig(wert: object) -> None:
    """Jede Nachricht ausserhalb der Form ist ``Formwidrig``, in beide Richtungen (D617)."""
    roh = cbor_canon.encode(wert)
    for vom_boten in (True, False):
        with pytest.raises(Formwidrig):
            lesen(roh, vom_boten=vom_boten)


def test_fehlt_nur_vom_nachbarn() -> None:
    """``FEHLT`` schickt nur der Nachbar."""
    roh = cbor_canon.encode([[None, FEHLT, [_GUTE_ID]]])
    assert lesen(roh, vom_boten=False) == [(None, FEHLT, [_GUTE_ID])]
    with pytest.raises(Formwidrig):
        lesen(roh, vom_boten=True)


def test_formwidrige_bytes() -> None:
    """Keine Bytes, zu lang, nicht kanonisch."""
    gut = cbor_canon.encode([[None, SKIP, None]])
    assert lesen(gut, vom_boten=True) == [(None, SKIP, None)]
    schlecht = b"\x81\x83\xf6\x18\x00\xf6"
    for roh in ("text", b"", b"\xff", gut + b"\x00", bytes(RAHMEN + 1), schlecht):
        with pytest.raises(Formwidrig):
            lesen(roh, vom_boten=True)
