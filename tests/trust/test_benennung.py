"""Vertauschungsprobe fuer kante_claim_id (01 §4.1, 02 §3.1, D172)."""

from __future__ import annotations

from symbolon.atom import claim_id, signed_bytes
from symbolon.trust import TrustFinding, TrustParams, trust
from symbolon.trust.derive import derive

from tests.helpers import Identity, scope_id, store_with
from .tp02 import NOW, T_EXP

PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=4)

# t von v2: begrenzt und im Test sichtbar. t ist inert (ACTIVE, t_exp >> now).
_T_V2 = range(2, 256)


def _world(t_v2: int):
    scope = scope_id("benennung-B")
    alice = Identity("ben-B-alice")
    bob = Identity("ben-B-bob")
    carol = Identity("ben-B-carol")
    g1 = Identity("ben-B-g1")
    rump = [
        alice.vouch(bob, n=4, scope=scope, t=1, t_exp=T_EXP),
        bob.vouch(carol, n=4, scope=scope, t=1, t_exp=T_EXP),
    ]
    v1 = carol.vouch(g1, n=2, scope=scope, t=1, t_exp=T_EXP)
    v2 = carol.vouch(g1, n=2, scope=scope, t=t_v2, t_exp=T_EXP)
    store = store_with(*rump, v1, v2)
    return {
        "alice": alice,
        "carol": carol,
        "g1": g1,
        "v1": v1,
        "v2": v2,
        "store": store,
        "scope": scope,
    }


def _named_and_rest(w: dict):
    store = w["store"]
    anchors = frozenset({w["alice"].pub})
    targets = frozenset({w["g1"].pub})
    scope = w["scope"]
    carol, g1 = w["carol"], w["g1"]
    der = derive(
        store, anchors=anchors, scope=scope, now=NOW, params=PARAMS,
        include_flagged=True,
    )
    r = trust(
        store, anchors=anchors, targets=targets, scope=scope,
        now=NOW, params=PARAMS, include_flagged=True,
    )
    named = next(
        e.claim_id
        for e in der.bfs.edges
        if e.author == carol.pub and e.subject == g1.pub
    )
    edges = tuple(
        (e.author, e.subject, e.cap, e.n_kante) for e in der.bfs.edges
    )
    findings = frozenset(
        (f.kind, f.subject)
        for f in der.findings
        if f.kind != TrustFinding.SUBGRANULAR_VOUCH
    )
    n_sub = sum(
        1 for f in der.findings if f.kind == TrustFinding.SUBGRANULAR_VOUCH
    )
    rest = (
        der.bfs.distance,
        der.bfs.node_capacity,
        edges,
        r.value,
        r.disjoint_paths,
        r.cut,
        findings,
        n_sub,
    )
    return named, rest


def test_vertauschungsprobe_kante_claim_id() -> None:
    world_v1_min = None
    world_v2_min = None
    for t_v2 in _T_V2:
        w = _world(t_v2)
        id1, id2 = claim_id(w["v1"]), claim_id(w["v2"])
        if id1 < id2 and world_v1_min is None:
            world_v1_min = w
        if id2 < id1 and world_v2_min is None:
            world_v2_min = w
        if world_v1_min is not None and world_v2_min is not None:
            break
    assert world_v1_min is not None
    assert world_v2_min is not None
    assert signed_bytes(world_v1_min["v1"]) == signed_bytes(world_v2_min["v1"])

    named_a, rest_a = _named_and_rest(world_v1_min)
    named_b, rest_b = _named_and_rest(world_v2_min)
    candidates_a = {claim_id(world_v1_min["v1"]), claim_id(world_v1_min["v2"])}
    candidates_b = {claim_id(world_v2_min["v1"]), claim_id(world_v2_min["v2"])}
    assert named_a in candidates_a
    assert named_b in candidates_b
    assert named_a != named_b
    assert rest_a == rest_b


def _world_vermerke(t_v2: int):
    """Wie ``_world``, zusätzlich je mindestens ein Überziehung und ein Unterkorn."""
    scope = scope_id("benennung-vermerke")
    alice = Identity("ben-V-alice")
    bob = Identity("ben-V-bob")
    mid = Identity("ben-V-mid")
    far = Identity("ben-V-far")
    leaf = Identity("ben-V-leaf")
    carol = Identity("ben-V-carol")
    g1 = Identity("ben-V-g1")
    extra_subject = Identity("ben-V-extra")
    rump = [
        alice.vouch(bob, n=4, scope=scope, t=1, t_exp=T_EXP),
        alice.vouch(carol, n=4, scope=scope, t=2, t_exp=T_EXP),
        bob.vouch(mid, n=4, scope=scope, t=1, t_exp=T_EXP),
        mid.vouch(far, n=4, scope=scope, t=1, t_exp=T_EXP),
        far.vouch(leaf, n=1, scope=scope, t=1, t_exp=T_EXP),
    ]
    v1 = carol.vouch(g1, n=2, scope=scope, t=1, t_exp=T_EXP)
    v2 = carol.vouch(g1, n=2, scope=scope, t=t_v2, t_exp=T_EXP)
    extra = carol.vouch(extra_subject, n=3, scope=scope, t=256, t_exp=T_EXP)
    store = store_with(*rump, v1, v2, extra)
    return {
        "alice": alice,
        "carol": carol,
        "g1": g1,
        "v1": v1,
        "v2": v2,
        "store": store,
        "scope": scope,
    }


def test_vertauschungsprobe_mit_vermerken() -> None:
    """Beide Varianten tragen Überziehung und Unterkorn; der Rest bleibt gleich (D427)."""
    world_v1_min = None
    world_v2_min = None
    for t_v2 in _T_V2:
        w = _world_vermerke(t_v2)
        id1, id2 = claim_id(w["v1"]), claim_id(w["v2"])
        if id1 < id2 and world_v1_min is None:
            world_v1_min = w
        if id2 < id1 and world_v2_min is None:
            world_v2_min = w
        if world_v1_min is not None and world_v2_min is not None:
            break
    assert world_v1_min is not None
    assert world_v2_min is not None
    assert signed_bytes(world_v1_min["v1"]) == signed_bytes(world_v2_min["v1"])

    named_a, rest_a = _named_and_rest(world_v1_min)
    named_b, rest_b = _named_and_rest(world_v2_min)
    for rest in (rest_a, rest_b):
        findings, n_sub = rest[6], rest[7]
        assert n_sub >= 1
        assert any(kind is TrustFinding.OVERCOMMITTED_AUTHOR for kind, _subject in findings)
    candidates_a = {claim_id(world_v1_min["v1"]), claim_id(world_v1_min["v2"])}
    candidates_b = {claim_id(world_v2_min["v1"]), claim_id(world_v2_min["v2"])}
    assert named_a in candidates_a
    assert named_b in candidates_b
    assert named_a != named_b
    assert rest_a == rest_b
