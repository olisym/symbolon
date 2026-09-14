"""Vektorsatz TZ-02 gegen tz02.py (02-golden-anchors.md §5)."""

from __future__ import annotations

from symbolon.index import classify_all
from symbolon.verifier import State

from tests.trust.tz02 import iter_profiles
from tools.export_tz02 import VECTORS_PATH, build_profiles, dumps


def test_vectors_02_tz02_matches_tz02() -> None:
    on_disk = VECTORS_PATH.read_text(encoding="utf-8")
    assert on_disk == dumps(build_profiles())


def test_vectors_02_tz02_exposes_lifecycle_states() -> None:
    """Der Satz misst Widerruf, Supersede und Ablauf, nicht nur active."""
    seen: set[State] = set()
    for _name, graph, now in iter_profiles():
        classified = classify_all(graph.store(), now)
        seen |= {row.state for row in classified.values()}
    assert seen - {State.ACTIVE}
    assert State.REVOKED in seen
    assert State.SUPERSEDED in seen
    assert State.EXPIRED in seen
