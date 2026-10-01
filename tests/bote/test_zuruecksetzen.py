"""Ein anderer Stand setzt Trickle zurück, nicht von gesperrten Nachbarn (D623)."""

from __future__ import annotations

import pytest

from symbolon.bote.kern import zuruecksetzen

A = bytes(32)
B = bytes([1]) * 32
ZIEL = bytes([2]) * 16
ANDERER = bytes([3]) * 16


@pytest.mark.parametrize(
    ("fremd", "stand", "gesperrt", "erwartet"),
    [
        (B, A, frozenset(), True),
        (B, A, frozenset({ANDERER}), True),
        (A, A, frozenset(), False),
        (B, None, frozenset(), False),
        (B, A, frozenset({ZIEL}), False),
        (B, A, None, False),
    ],
    ids=["anders", "anderer-gesperrt", "gleich", "ohne-stand", "gesperrt", "formwidrig"],
)
def test_zuruecksetzen(fremd, stand, gesperrt, erwartet) -> None:
    assert zuruecksetzen(ZIEL, fremd, stand, gesperrt) is erwartet
