"""Vektorsatz TP-02 gegen tp02.py (02-golden-anchors.md §1-§2)."""

from __future__ import annotations

from tools.export_tp02 import VECTORS_PATH, build_profiles, dumps


def test_vectors_02_tp02_matches_tp02() -> None:
    on_disk = VECTORS_PATH.read_text(encoding="utf-8")
    assert on_disk == dumps(build_profiles())
