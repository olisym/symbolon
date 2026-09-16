"""VOUCH_WITHOUT_TEXP: Vermerk ohne Wirkung (D119, 02 §6.2)."""

from __future__ import annotations

from symbolon.atom import claim_id
from symbolon.index import classify_all
from symbolon.trust import Finding, TrustFinding, TrustParams, trust
from symbolon.trust.derive import derive
from symbolon.trust.groups import build_groups
from symbolon.verifier import State

from tests.helpers import Identity, scope_id, store_with
from .tp02 import NOW, T_EXP

PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=4)


def test_vouch_without_texp_finding_fires() -> None:
    scope = scope_id("vouch-no-texp")
    alice, bob = Identity("no-texp-A"), Identity("no-texp-B")
    claim = alice.vouch(bob, n=1, scope=scope, t=1)
    store = store_with(claim)
    r = trust(
        store,
        anchors=frozenset({alice.pub}),
        targets=frozenset({bob.pub}),
        scope=scope,
        now=NOW,
        params=PARAMS,
        include_flagged=True,
    )
    assert r.findings == (
        Finding(kind=TrustFinding.VOUCH_WITHOUT_TEXP, subject=claim_id(claim)),
    )


def test_vouch_without_texp_is_inert() -> None:
    scope = scope_id("vouch-texp-inert")

    def run(*, t_exp: int | None):
        alice, bob = Identity("inert-A"), Identity("inert-B")
        claim = alice.vouch(bob, n=2, scope=scope, t=1, t_exp=t_exp)
        store = store_with(claim)
        classifications = classify_all(store, NOW)
        groups, findings = build_groups(
            store.all_claims(), classifications, scope, PARAMS.D, NOW
        )
        derivation = derive(
            store,
            anchors=frozenset({alice.pub}),
            scope=scope,
            now=NOW,
            params=PARAMS,
        )
        return groups, findings, derivation.bfs.node_capacity, claim

    groups_wo, findings_wo, cap_wo, claim_wo = run(t_exp=None)
    groups_w, findings_w, cap_w, _claim_w = run(t_exp=T_EXP)

    assert set(groups_wo) == set(groups_w)
    for key in groups_wo:
        assert groups_wo[key].n_budget == groups_w[key].n_budget
        assert groups_wo[key].n_kante == groups_w[key].n_kante
    assert cap_wo == cap_w
    assert findings_w == ()
    assert findings_wo == (
        Finding(kind=TrustFinding.VOUCH_WITHOUT_TEXP, subject=claim_id(claim_wo)),
    )


def test_no_vouch_without_texp_on_unparsable_v() -> None:
    scope = scope_id("vouch-no-texp-bad-v")
    alice, bob = Identity("bad-v-A"), Identity("bad-v-B")
    claim = alice.vouch_raw(bob, v=b"\xff", scope=scope, t=1)
    store = store_with(claim)
    r = trust(
        store,
        anchors=frozenset({alice.pub}),
        targets=frozenset({bob.pub}),
        scope=scope,
        now=NOW,
        params=PARAMS,
        include_flagged=True,
    )
    cid = claim_id(claim)
    assert r.findings == (
        Finding(kind=TrustFinding.UNPARSABLE_VOUCH_PAYLOAD, subject=cid),
    )
    assert not any(f.kind == TrustFinding.VOUCH_WITHOUT_TEXP for f in r.findings)


def test_vouch_without_texp_fires_on_flagged_author() -> None:
    scope = scope_id("vouch-no-texp-outside")
    a1 = Identity("out-A")
    a2 = Identity("out-A")
    bob = Identity("out-B")
    carol = Identity("out-C")
    v1 = a1.vouch(bob, n=1, scope=scope, t=1)
    v2 = a2.vouch(carol, n=1, scope=scope, t=1)
    store = store_with(v1, v2)
    classifications = classify_all(store, NOW)
    assert classifications[claim_id(v1)].state == State.EQUIVOCATION_FLAGGED
    assert classifications[claim_id(v2)].state == State.EQUIVOCATION_FLAGGED
    _groups, findings = build_groups(
        store.all_claims(), classifications, scope, PARAMS.D, NOW
    )
    expected = tuple(
        sorted(
            Finding(kind=TrustFinding.VOUCH_WITHOUT_TEXP, subject=claim_id(v))
            for v in (v1, v2)
        )
    )
    assert findings == expected


def test_no_vouch_without_texp_on_expired_vouch() -> None:
    scope = scope_id("vouch-expired-texp")
    alice, bob = Identity("exp-A"), Identity("exp-B")
    claim = alice.vouch(bob, n=1, scope=scope, t=1, t_exp=NOW - 1)
    store = store_with(claim)
    classifications = classify_all(store, NOW)
    groups, findings = build_groups(
        store.all_claims(), classifications, scope, PARAMS.D, NOW
    )
    assert not any(f.kind == TrustFinding.VOUCH_WITHOUT_TEXP for f in findings)
    assert groups == {}


def test_no_payload_finding_on_expired_vouch() -> None:
    scope = scope_id("payload-expired")
    alice, bob = Identity("payload-exp-A"), Identity("payload-exp-B")
    claim = alice.vouch_raw(bob, v=b"\xff", scope=scope, t=1, t_exp=NOW - 1)
    store = store_with(claim)
    classifications = classify_all(store, NOW)
    cid = claim_id(claim)
    assert classifications[cid].state == State.EXPIRED
    groups, findings = build_groups(
        store.all_claims(), classifications, scope, PARAMS.D, NOW
    )
    assert findings == ()
    assert groups == {}


def test_payload_finding_on_unexpired_vouch() -> None:
    scope = scope_id("payload-unexpired")
    alice, bob = Identity("payload-unexp-A"), Identity("payload-unexp-B")
    claim = alice.vouch_raw(bob, v=b"\xff", scope=scope, t=1, t_exp=T_EXP)
    store = store_with(claim)
    classifications = classify_all(store, NOW)
    cid = claim_id(claim)
    groups, findings = build_groups(
        store.all_claims(), classifications, scope, PARAMS.D, NOW
    )
    assert findings == (
        Finding(kind=TrustFinding.UNPARSABLE_VOUCH_PAYLOAD, subject=cid),
    )
    assert groups == {}


def test_payload_finding_on_revoked_vouch() -> None:
    scope = scope_id("payload-revoked")
    alice, bob = Identity("payload-rev-A"), Identity("payload-rev-B")
    claim = alice.vouch_raw(bob, v=b"\xff", scope=scope, t=1, t_exp=T_EXP)
    revoke = alice.revoke(claim, t=2)
    store = store_with(claim, revoke)
    classifications = classify_all(store, NOW)
    cid = claim_id(claim)
    assert classifications[cid].state == State.REVOKED
    groups, findings = build_groups(
        store.all_claims(), classifications, scope, PARAMS.D, NOW
    )
    assert findings == (
        Finding(kind=TrustFinding.UNPARSABLE_VOUCH_PAYLOAD, subject=cid),
    )
    assert groups == {}
