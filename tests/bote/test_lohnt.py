"""Holen nur vom Nachbarn mit mindestens so vielen Einträgen (D619 Beschluss 2)."""

from __future__ import annotations

import hashlib
import random

from hypothesis import given, settings
from hypothesis import strategies as st

from symbolon.bote.kern import lohnt


def _stand(menge: frozenset[int]) -> bytes:
    return hashlib.sha256(repr(sorted(menge)).encode()).digest()


def test_lohnt() -> None:
    """Anderer Stand und mindestens so viele Einträge; gleich viele genügen."""
    a, b = bytes(32), bytes([1]) * 32
    assert lohnt((b, 5), a, 5)
    assert lohnt((b, 6), a, 5)
    assert not lohnt((b, 4), a, 5)
    assert not lohnt((a, 9), a, 5)
    assert lohnt((b, 0), None, 0)


@settings(max_examples=200, deadline=None)
@given(
    st.lists(st.frozensets(st.integers(0, 30), max_size=12), min_size=2, max_size=6),
    st.integers(0, 2**32),
)
def test_holen_endet_bei_der_vereinigung(mengen: list[frozenset[int]], samen: int) -> None:
    """Wer nach der Regel holt, findet immer etwas, und alle enden bei der Vereinigung.

    Jedes Gerät hört jedes andere. Holt ``a`` bei ``b``, weil es lohnt, hat ``b`` mindestens so
    viele Einträge und einen anderen Bestand, also etwas, das ``a`` fehlt. Danach hat ``a`` die
    Vereinigung beider. Gleich viele Einträge mit verschiedenem Bestand holen beide (D619 Befund).
    """
    r = random.Random(samen)
    bestand = list(mengen)
    ziel = frozenset().union(*bestand)
    for _ in range(10 * len(bestand) ** 2):
        paare = [
            (a, b)
            for a in range(len(bestand))
            for b in range(len(bestand))
            if a != b
            and lohnt((_stand(bestand[b]), len(bestand[b])), _stand(bestand[a]), len(bestand[a]))
        ]
        if not paare:
            break
        a, b = r.choice(paare)
        assert bestand[b] - bestand[a], "vergeblich geholt"
        bestand[a] = bestand[a] | bestand[b]
    assert all(m == ziel for m in bestand)
