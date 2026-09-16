"""Vektorsatz FALL-02 gegen fall02.py (02 §3, 02 §4)."""

from __future__ import annotations

from tools.export_fall02 import VECTORS_PATH, build_profiles, dumps


def test_vectors_02_fall02_matches_fall02() -> None:
    on_disk = VECTORS_PATH.read_text(encoding="utf-8")
    assert on_disk == dumps(build_profiles())
