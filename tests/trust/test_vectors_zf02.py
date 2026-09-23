"""Vektorsatz ZF-02 gegen zf02.py (D438, 01 §6, 02 §3.1)."""

from __future__ import annotations

import pytest

from symbolon.atom import claim_id
from symbolon.trust import classify_all, trust
from symbolon.trust.groups import build_groups
from symbolon.verifier import State

from tests.trust.zf02 import (
    BOB_BUDGET,
    DISJOINT,
    FLOW_PER_TARGET,
    NAMED_STATES,
    OTHER_STATE,
    PARAMS,
    PROFILES,
    SIMULTANEOUS,
    Graph,
    iter_profiles,
)
from tools.export_zf02 import VECTORS_PATH, build_profiles, dumps


def _row(profil: str) -> tuple[Graph, int]:
    for name, graph, now in iter_profiles():
        if name == profil:
            return graph, now
    raise AssertionError(profil)


def test_vectors_02_zf02_matches_zf02() -> None:
    """Die Datei auf der Platte gleicht dem Exporter (D438 Beschluss 4)."""
    on_disk = VECTORS_PATH.read_text(encoding="utf-8")
    assert on_disk == dumps(build_profiles())


@pytest.mark.parametrize("profil", PROFILES)
def test_zf02_states(profil: str) -> None:
    """Benannte Claims nach D438, jeder andere active (01 §6, 01 Anhang B.1)."""
    graph, now = _row(profil)
    classified = classify_all(graph.store(), now)
    expected = NAMED_STATES[profil]
    held = {claim_id(claim) for claim in graph.claims}
    named_held = {
        claim_name
        for claim_name, claim in graph.named.items()
        if claim_id(claim) in held
    }
    assert named_held == set(expected)
    by_id = {claim_id(graph.named[name]): state for name, state in expected.items()}
    for cid, row in classified.items():
        assert row.state == by_id.get(cid, OTHER_STATE)


@pytest.mark.parametrize("profil", PROFILES)
def test_zf02_flow_and_budget(profil: str) -> None:
    """Fluss, Disjunktheit und BOBs Budget wie ref_block, include_flagged (D438, 02 §3.1)."""
    graph, now = _row(profil)
    store = graph.store()
    classifications = classify_all(store, now)
    claims = store.all_claims()
    groups, _payload_findings = build_groups(
        claims, classifications, graph.scope, PARAMS.D, now
    )
    anchors = frozenset({graph.ALICE.pub})
    targets = frozenset({graph.g1.pub, graph.g2.pub, graph.g3.pub})
    for target in sorted(targets):
        single = trust(
            store,
            anchors=anchors,
            targets=frozenset({target}),
            scope=graph.scope,
            now=now,
            params=PARAMS,
            include_flagged=True,
        )
        assert single.value == FLOW_PER_TARGET
    simultaneous = trust(
        store,
        anchors=anchors,
        targets=targets,
        scope=graph.scope,
        now=now,
        params=PARAMS,
        include_flagged=True,
    )
    assert simultaneous.value == SIMULTANEOUS
    assert simultaneous.disjoint_paths == DISJOINT
    budget = sum(
        group.n_budget for group in groups.values() if group.author == graph.BOB.pub
    )
    assert budget == BOB_BUDGET[profil]
    assert budget <= PARAMS.D


def test_zf02_observed_states_include_pending_and_flags() -> None:
    """Der Satz belegt pending und beide Flags (D438, 01 Anhang B.1)."""
    seen: set[State] = set()
    for _name, graph, now in iter_profiles():
        classified = classify_all(graph.store(), now)
        seen |= {row.state for row in classified.values()}
    assert State.PENDING in seen
    assert State.EQUIVOCATION_FLAGGED in seen
    assert State.TIME_REGRESSION_FLAGGED in seen
