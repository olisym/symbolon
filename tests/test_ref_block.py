"""Referenzdrucker in der Blockform (D391, rs/AUFTRAG.md Schnittstelle)."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from tools.ref_block import KEYWORDS, load_profiles, render

ROOT = Path(__file__).resolve().parent.parent
VECTORS = ROOT / "tests" / "vectors"
VECTOR_PATHS = (
    VECTORS / "vectors_02_tp02.json",
    VECTORS / "vectors_02_tz02.json",
    VECTORS / "vectors_02_fall02.json",
)
ANCHORS = ROOT / "02-golden-anchors.md"
_KEYWORDS = frozenset(KEYWORDS)
_TP02_PROFILE = "F"


def _blocks(text: str) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in text.splitlines():
        if line.startswith("profil "):
            if current:
                blocks.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        blocks.append(current)
    return blocks


def _anchor_row(name: str) -> tuple[int, int, int, int]:
    """trust→g1, trust→g2, trust→g3, simultan aus 02-golden-anchors.md §3."""
    text = ANCHORS.read_text(encoding="utf-8")
    start = text.index("## 3. Anker 1–3")
    end = text.index("### Rechenwege", start)
    section = text[start:end]
    wanted = name.replace("0", "₀") if name.endswith("0") else name
    for line in section.splitlines():
        cells = [re.sub(r"[`*]", "", cell).strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6 or cells[0] != wanted:
            continue
        return int(cells[1]), int(cells[2]), int(cells[3]), int(cells[5])
    raise AssertionError(f"no 02-golden-anchors.md §3 row for {name}")


@pytest.mark.parametrize("path", VECTOR_PATHS, ids=lambda p: p.name)
def test_ref_block_runs(path: Path) -> None:
    render(path)


@pytest.mark.parametrize("path", VECTOR_PATHS, ids=lambda p: p.name)
def test_profil_count_matches_file(path: Path) -> None:
    profiles = load_profiles(path)
    text = render(path)
    n_profil = sum(1 for line in text.splitlines() if line.startswith("profil "))
    assert n_profil == len(profiles)


@pytest.mark.parametrize("path", VECTOR_PATHS, ids=lambda p: p.name)
def test_every_line_starts_with_a_keyword(path: Path) -> None:
    for line in render(path).splitlines():
        assert line.split()[0] in _KEYWORDS


@pytest.mark.parametrize("path", VECTOR_PATHS, ids=lambda p: p.name)
def test_block_order_matches_file(path: Path) -> None:
    names = [profile["profil"] for profile in load_profiles(path)]
    printed = [
        line.split(" ", 1)[1]
        for line in render(path).splitlines()
        if line.startswith("profil ")
    ]
    assert printed == names


@pytest.mark.parametrize("path", VECTOR_PATHS, ids=lambda p: p.name)
def test_budget_lines_sorted_by_identity(path: Path) -> None:
    for block in _blocks(render(path)):
        identities = [line.split()[1] for line in block if line.startswith("budget ")]
        assert identities == sorted(identities)


def test_tp02_profile_matches_golden_anchor_section3() -> None:
    path = VECTORS / "vectors_02_tp02.json"
    profiles = json.loads(path.read_text(encoding="utf-8"))
    profile = next(item for item in profiles if item["profil"] == _TP02_PROFILE)
    labels = profile["labels"]
    g1, g2, g3, simultan = _anchor_row(_TP02_PROFILE)
    expected = {
        labels["g1"]: g1,
        labels["g2"]: g2,
        labels["g3"]: g3,
    }
    block = next(
        b for b in _blocks(render(path)) if b[0] == f"profil {_TP02_PROFILE}"
    )
    flows = {
        parts[1]: int(parts[2])
        for line in block
        if line.startswith("fluss ")
        for parts in [line.split()]
    }
    assert flows == expected
    printed_simultan = next(line for line in block if line.startswith("simultan "))
    assert int(printed_simultan.split()[1]) == simultan
