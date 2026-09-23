"""Autor-Flag an ZF-02 F2 (D443 Beschluss 5, 01 §4, 02 §3.1, 02 §8, 02 §11.4)."""

from __future__ import annotations

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id
from symbolon.trust import classify_all, trust
from symbolon.trust.groups import build_groups
from symbolon.verifier import State

from tests.helpers import Identity, scope_id
from tests.trust.zf02 import FLOW_PER_TARGET, NOW, PARAMS, SCOPE, Graph, build_f2


def _f2_zweiter_scope() -> Graph:
    """F2, f1 und f2 im zweiten Scope, b und der Rest in SCOPE (02 §8)."""
    base = build_f2()
    anderer_scope = scope_id("ZF-02-F2-Gabel")
    by_pub = {ident.pub: ident for ident in base.identities.values()}
    bob = Identity(base.BOB.label)
    fork = Identity(base.BOB.label)
    plan = (
        ("f1", bob, anderer_scope),
        ("f2", fork, anderer_scope),
        ("b", bob, SCOPE),
    )
    neu: dict[str, Claim] = {}
    for name, author, scope in plan:
        src = base.named[name]
        v = src.v
        assert v is not None
        neu[name] = author.vouch(
            by_pub[src.J[1]],
            n=cbor_canon.decode(v)[0],
            scope=scope,
            t=src.t,
            t_exp=src.t_exp,
        )
    alt = tuple(base.named[name] for name, _, _ in plan)
    claims = [claim for claim in base.claims if claim not in alt]
    claims.extend(neu[name] for name, _, _ in plan)
    return Graph(base.identities, claims, SCOPE, neu)


def test_flagged_claim_carries_no_edge() -> None:
    """BOB→X und BOB→Y ohne Kante, BOB→CAROL mit n aus b (02 §3.1, 02 §8)."""
    graph = build_f2()
    now = NOW
    store = graph.store()
    classifications = classify_all(store, now)
    claims = store.all_claims()
    groups, _payload_findings = build_groups(
        claims, classifications, graph.scope, PARAMS.D, now
    )
    v_b = graph.named["b"].v
    assert v_b is not None
    n_b = cbor_canon.decode(v_b)[0]
    bob = graph.BOB.pub
    assert groups[(bob, graph.X.pub)].n_kante == 0
    assert groups[(bob, graph.Y.pub)].n_kante == 0
    assert groups[(bob, graph.CAROL.pub)].n_kante == n_b
    anker = frozenset({graph.ALICE.pub})
    ziele = frozenset({graph.g1.pub, graph.g2.pub, graph.g3.pub})
    for ziel in sorted(ziele):
        einzeln = trust(
            store,
            anchors=anker,
            targets=frozenset({ziel}),
            scope=graph.scope,
            now=now,
            params=PARAMS,
            include_flagged=True,
        )
        assert einzeln.value == FLOW_PER_TARGET


def test_equivocating_author_loses_edges() -> None:
    """f1 und f2 geflaggt, Fluss je Ziel und simultan 0 (02 §8, 02 §11.4)."""
    graph = build_f2()
    now = NOW
    store = graph.store()
    classified = classify_all(store, now)
    for name in ("f1", "f2"):
        assert classified[claim_id(graph.named[name])].state == State.EQUIVOCATION_FLAGGED
    anker = frozenset({graph.ALICE.pub})
    ziele = frozenset({graph.g1.pub, graph.g2.pub, graph.g3.pub})
    for ziel in sorted(ziele):
        einzeln = trust(
            store,
            anchors=anker,
            targets=frozenset({ziel}),
            scope=graph.scope,
            now=now,
            params=PARAMS,
            include_flagged=False,
        )
        assert einzeln.value == 0
    simultan = trust(
        store,
        anchors=anker,
        targets=ziele,
        scope=graph.scope,
        now=now,
        params=PARAMS,
        include_flagged=False,
    )
    assert simultan.value == 0


def test_equivocation_flags_author_across_scopes() -> None:
    """Equivocation im zweiten Scope flaggt den Autor in SCOPE (01 §4, 02 §8)."""
    graph = _f2_zweiter_scope()
    now = NOW
    store = graph.store()
    classified = classify_all(store, now)
    for name in ("f1", "f2"):
        assert classified[claim_id(graph.named[name])].state == State.EQUIVOCATION_FLAGGED
    anker = frozenset({graph.ALICE.pub})
    ziele = frozenset({graph.g1.pub, graph.g2.pub, graph.g3.pub})
    for ziel in sorted(ziele):
        ohne = trust(
            store,
            anchors=anker,
            targets=frozenset({ziel}),
            scope=SCOPE,
            now=now,
            params=PARAMS,
            include_flagged=False,
        )
        assert ohne.value == 0
    for ziel in sorted(ziele):
        mit = trust(
            store,
            anchors=anker,
            targets=frozenset({ziel}),
            scope=SCOPE,
            now=now,
            params=PARAMS,
            include_flagged=True,
        )
        assert mit.value == FLOW_PER_TARGET
