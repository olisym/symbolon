"""FALL-02 gegen die Referenz (02 §3, 02 §4, 02-golden-anchors.md §0 K9)."""

from __future__ import annotations

import pytest

from symbolon.trust import trust
from symbolon.trust.derive import derive
from symbolon.trust.graph import infinity

from .fall02 import NOW, PARAMS, PROFILES, build

# value, disjoint_paths, cut is CAROL, findings empty; INF; (g1, g2, g3)
EXPECTED = {
    "R1": (
        288230376151711744,
        1,
        4467570830351532033,
        (144115188075855872, 72057594037927936, 72057594037927936),
    ),
    "R2": (
        864691128455135232,
        1,
        13402712491054596097,
        (432345564227567616, 216172782113783808, 216172782113783808),
    ),
    "R3": (
        1152921504606846976,
        1,
        17870283321406128129,
        (576460752303423488, 288230376151711744, 288230376151711744),
    ),
}

INT64_MAX = 2**63 - 1


@pytest.mark.parametrize("profil", PROFILES)
def test_simultaneous(profil: str) -> None:
    value, disjoint_paths, _inf, _single = EXPECTED[profil]
    g = build(profil)
    r = trust(
        g.store(),
        anchors=frozenset({g.ALICE.pub}),
        targets=frozenset({g.g1.pub, g.g2.pub, g.g3.pub}),
        scope=g.scope,
        now=NOW,
        params=PARAMS[profil],
    )
    assert r.value == value
    assert r.disjoint_paths == disjoint_paths
    assert r.cut == (g.CAROL.pub,)
    assert r.findings == ()


@pytest.mark.parametrize("profil", PROFILES)
def test_individual(profil: str) -> None:
    _value, _disjoint, _inf, (e1, e2, e3) = EXPECTED[profil]
    g = build(profil)
    store = g.store()
    for target, expected in ((g.g1, e1), (g.g2, e2), (g.g3, e3)):
        r = trust(
            store,
            anchors=frozenset({g.ALICE.pub}),
            targets=frozenset({target.pub}),
            scope=g.scope,
            now=NOW,
            params=PARAMS[profil],
        )
        assert r.value == expected, target.label
        assert r.findings == ()


@pytest.mark.parametrize("profil", PROFILES)
def test_infinity_sentinel(profil: str) -> None:
    _value, _disjoint, inf, _single = EXPECTED[profil]
    g = build(profil)
    der = derive(
        g.store(),
        anchors=frozenset({g.ALICE.pub}),
        scope=g.scope,
        now=NOW,
        params=PARAMS[profil],
    )
    assert infinity(der.bfs) == inf


def test_inf_signed_int64_threshold() -> None:
    """R1 passt in int64, R2 und R3 nicht (02 §4)."""
    infs: dict[str, int] = {}
    for profil in PROFILES:
        g = build(profil)
        der = derive(
            g.store(),
            anchors=frozenset({g.ALICE.pub}),
            scope=g.scope,
            now=NOW,
            params=PARAMS[profil],
        )
        infs[profil] = infinity(der.bfs)
    assert infs["R1"] <= INT64_MAX
    assert infs["R2"] > INT64_MAX
    assert infs["R3"] > INT64_MAX
