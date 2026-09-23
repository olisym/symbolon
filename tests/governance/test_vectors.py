"""GV-1 … GV-34 — Governance-Vektoren (04-golden-anchors.md)."""

from __future__ import annotations

import hashlib

import pytest

from symbolon import cbor_canon
from symbolon.atom import claim_id
from symbolon.domains import DOM_NUC_GEN
from symbolon.governance import (
    Finding,
    GovernanceFinding,
    verify_ratification,
)
from symbolon.governance.objects import Epoch, Proposal
from symbolon.governance.tally import TallyResult, TallyState, reached
from symbolon.policy import constitution_hash
from symbolon.profiles import MembershipState, membership
from tests.helpers import Identity, store_with

from .fixtures import (
    C1,
    C1_AMEND,
    C2,
    C2_ALT_A,
    C2_ALT_B,
    C2_HALF,
    C2_HIGH,
    C2_LOWER,
    C3,
    CONSTITUTION_HASH_2,
    EPOCH_1,
    EPOCH_2,
    EPOCH_2_HALF,
    EVE,
    GENESIS_D,
    N_D,
    NOW,
    P2,
    PROPOSAL_1,
    PROPOSAL_2,
    PROPOSAL_ALT_A,
    PROPOSAL_ALT_B,
    PROPOSAL_AMEND_E1,
    PROPOSAL_HIGH,
    PROPOSAL_LOWER,
    _tally,
    fresh_p1,
    fresh_p2,
    nuc,
    policy_of,
    propose_claim,
    ratify_claim,
    vote,
    vote_noncanonical_v,
    vote_unparsable_v,
)


def _kinds(result) -> set[GovernanceFinding]:
    return {f.kind for f in result.findings}


def _paired(constitution: dict, target: dict = C3, *, index: int = 2):
    epoch = Epoch(
        scope=N_D, index=index, constitution_hash=constitution_hash(constitution)
    )
    proposal = Proposal(
        scope=N_D,
        predecessor=epoch.epoch_id,
        constitution_hash=constitution_hash(target),
    )
    return epoch, proposal


def _c2_amendment(pair: list) -> dict:
    obj = dict(C2)
    obj["thresholds"] = dict(C2["thresholds"])
    obj["thresholds"]["amendment"] = pair
    return obj


def test_GV_1() -> None:
    alice, bob, carol, dave = fresh_p1()
    votes = [
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
        vote(carol, PROPOSAL_1, choice=1, t=1),
        vote(dave, PROPOSAL_1, choice=1, t=1),
    ]
    yes = [claim_id(v) for v in votes]
    store = store_with(*votes)
    tally = _tally(store)
    assert tally.state is TallyState.PASSED
    r1 = ratify_claim(alice, PROPOSAL_1, witnesses=yes[:3], t=10)
    r2 = ratify_claim(bob, PROPOSAL_1, witnesses=yes[1:], t=10)
    store.add(r1)
    store.add(r2)
    policy = policy_of(C1)
    a = verify_ratification(
        store, ratify=r1, epoch=EPOCH_1, proposal=PROPOSAL_1, tally=tally, target_constitution_obj=C2, now=NOW, policy=policy
    )
    b = verify_ratification(
        store, ratify=r2, epoch=EPOCH_1, proposal=PROPOSAL_1, tally=tally, target_constitution_obj=C2, now=NOW, policy=policy
    )
    assert a.next_epoch is not None
    assert b.next_epoch is not None
    assert a.next_epoch.epoch_id == b.next_epoch.epoch_id == EPOCH_2.epoch_id


def test_GV_2() -> None:
    alice, bob, carol, dave = fresh_p1()
    votes = [
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
        vote(carol, PROPOSAL_1, choice=1, t=1),
    ]
    extra = vote(dave, PROPOSAL_1, choice=0, t=1)
    store = store_with(*votes, extra)
    tally = _tally(store)
    cited = [claim_id(v) for v in votes] + [claim_id(extra)]
    r = ratify_claim(alice, PROPOSAL_1, witnesses=cited, t=10)
    store.add(r)
    result = verify_ratification(
        store, ratify=r, epoch=EPOCH_1, proposal=PROPOSAL_1, tally=tally, target_constitution_obj=C2, now=NOW, policy=policy_of(C1)
    )
    assert result.next_epoch is None
    assert GovernanceFinding.UNSUPPORTED_RATIFICATION in _kinds(result)
    assert GovernanceFinding.UNKNOWN_WITNESS_VOTE not in _kinds(result)


def test_GV_3() -> None:
    alice, bob, carol, _dave = fresh_p1()
    store = store_with(
        vote(alice, PROPOSAL_AMEND_E1, choice=1, t=1),
        vote(bob, PROPOSAL_AMEND_E1, choice=1, t=1),
        vote(carol, PROPOSAL_AMEND_E1, choice=1, t=1),
    )
    result = _tally(store, proposal=PROPOSAL_AMEND_E1, target=C1_AMEND)
    assert result.state is TallyState.PENDING
    assert result.n == 4
    assert result.threshold == (3, 4)


def test_GV_4() -> None:
    alice, bob, carol, dave = fresh_p1()
    store = store_with(
        vote(alice, PROPOSAL_AMEND_E1, choice=1, t=1),
        vote(bob, PROPOSAL_AMEND_E1, choice=1, t=1),
        vote(carol, PROPOSAL_AMEND_E1, choice=1, t=1),
        vote(dave, PROPOSAL_AMEND_E1, choice=1, t=1),
    )
    result = _tally(store, proposal=PROPOSAL_AMEND_E1, target=C1_AMEND)
    assert result.state is TallyState.PASSED


def test_GV_5() -> None:
    alice, bob, _carol, _dave = fresh_p1()
    store = store_with(
        vote(alice, PROPOSAL_AMEND_E1, choice=0, t=1),
        vote(bob, PROPOSAL_AMEND_E1, choice=0, t=1),
    )
    result = _tally(store, proposal=PROPOSAL_AMEND_E1, target=C1_AMEND)
    assert result.state is TallyState.FAILED


def test_GV_6() -> None:
    alice, bob, carol, _dave = fresh_p1()
    store = store_with(
        vote(alice, PROPOSAL_AMEND_E1, choice=1, t=1),
        vote(bob, PROPOSAL_AMEND_E1, choice=0, t=1),
        vote(carol, PROPOSAL_AMEND_E1, choice=0, t=1),
    )
    result = _tally(store, proposal=PROPOSAL_AMEND_E1, target=C1_AMEND)
    assert result.state is TallyState.FAILED


def test_GV_7() -> None:
    alice, bob, _carol, _dave = fresh_p1()
    store = store_with(
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
    )
    result = _tally(store)
    assert result.state is TallyState.PENDING
    assert result.threshold == (2, 3)


def test_GV_8() -> None:
    alice, bob, carol, _dave = fresh_p1()
    store = store_with(
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
        vote(carol, PROPOSAL_1, choice=1, t=1),
    )
    result = _tally(store)
    assert result.state is TallyState.PASSED
    member = membership(
        store,
        subject=EVE.pub,
        scope=N_D,
        constitution_hash=CONSTITUTION_HASH_2,
        now=NOW,
        authorized_keys=frozenset(),
        constitution_obj=C2,
    )
    assert member.state is MembershipState.GRANT_ONLY
    assert member.grant_claim_id is None


def test_GV_9() -> None:
    alice, bob, carol, _dave, _eve = fresh_p2()
    store = store_with(
        vote(alice, PROPOSAL_2, choice=1, t=1),
        vote(bob, PROPOSAL_2, choice=1, t=1),
        vote(carol, PROPOSAL_2, choice=1, t=1),
    )
    result = _tally(
        store, epoch=EPOCH_2, proposal=PROPOSAL_2, constitution=C2, target=C3
    )
    assert result.state is TallyState.PENDING
    assert result.n == 5
    assert result.threshold == (3, 4)


def test_GV_10() -> None:
    alice, bob, carol, dave, _eve = fresh_p2()
    store = store_with(
        vote(alice, PROPOSAL_2, choice=1, t=1),
        vote(bob, PROPOSAL_2, choice=1, t=1),
        vote(carol, PROPOSAL_2, choice=1, t=1),
        vote(dave, PROPOSAL_2, choice=1, t=1),
    )
    result = _tally(
        store, epoch=EPOCH_2, proposal=PROPOSAL_2, constitution=C2, target=C3
    )
    assert result.state is TallyState.PASSED


def test_GV_11() -> None:
    alice, bob, carol, _dave, _eve = fresh_p2()
    store = store_with(
        vote(alice, PROPOSAL_LOWER, choice=1, t=1),
        vote(bob, PROPOSAL_LOWER, choice=1, t=1),
        vote(carol, PROPOSAL_LOWER, choice=1, t=1),
    )
    result = _tally(
        store, epoch=EPOCH_2, proposal=PROPOSAL_LOWER, constitution=C2, target=C2_LOWER
    )
    assert result.state is TallyState.PENDING
    assert result.threshold == (3, 4)


def test_GV_12_gegenbild() -> None:
    """Ohne ratio_max wären drei von fünf unter [1,2] PASSED."""
    assert reached(3, 5, 1, 2) is True
    alice, bob, carol, _dave, _eve = fresh_p2()
    store = store_with(
        vote(alice, PROPOSAL_LOWER, choice=1, t=1),
        vote(bob, PROPOSAL_LOWER, choice=1, t=1),
        vote(carol, PROPOSAL_LOWER, choice=1, t=1),
    )
    result = _tally(
        store, epoch=EPOCH_2, proposal=PROPOSAL_LOWER, constitution=C2, target=C2_LOWER
    )
    assert result.state is TallyState.PENDING
    assert result.threshold == (3, 4)


def test_GV_13() -> None:
    alice, bob, carol, dave, _eve = fresh_p2()
    store = store_with(
        vote(alice, PROPOSAL_HIGH, choice=1, t=1),
        vote(bob, PROPOSAL_HIGH, choice=1, t=1),
        vote(carol, PROPOSAL_HIGH, choice=1, t=1),
        vote(dave, PROPOSAL_HIGH, choice=1, t=1),
    )
    result = _tally(
        store,
        epoch=EPOCH_2_HALF,
        proposal=PROPOSAL_HIGH,
        constitution=C2_HALF,
        target=C2_HIGH,
    )
    assert result.state is TallyState.PENDING
    assert result.threshold == (4, 5)


def test_GV_14_gegenbild() -> None:
    """Ohne ratio_max wären vier von fünf unter [1,2] PASSED."""
    assert reached(4, 5, 1, 2) is True
    alice, bob, carol, dave, _eve = fresh_p2()
    store = store_with(
        vote(alice, PROPOSAL_HIGH, choice=1, t=1),
        vote(bob, PROPOSAL_HIGH, choice=1, t=1),
        vote(carol, PROPOSAL_HIGH, choice=1, t=1),
        vote(dave, PROPOSAL_HIGH, choice=1, t=1),
    )
    result = _tally(
        store,
        epoch=EPOCH_2_HALF,
        proposal=PROPOSAL_HIGH,
        constitution=C2_HALF,
        target=C2_HIGH,
    )
    assert result.state is TallyState.PENDING
    assert result.threshold == (4, 5)


def test_GV_15() -> None:
    alice, bob, carol, dave, eve = fresh_p2()
    known = {
        PROPOSAL_ALT_A.proposal_hash: PROPOSAL_ALT_A,
        PROPOSAL_ALT_B.proposal_hash: PROPOSAL_ALT_B,
    }
    store = store_with(
        vote(eve, PROPOSAL_ALT_A, choice=1, t=1),
        vote(bob, PROPOSAL_ALT_A, choice=1, t=2),
        vote(alice, PROPOSAL_ALT_A, choice=1, t=3),
        vote(dave, PROPOSAL_ALT_A, choice=1, t=4),
        vote(eve, PROPOSAL_ALT_B, choice=1, t=5),
        vote(bob, PROPOSAL_ALT_B, choice=1, t=6),
        vote(alice, PROPOSAL_ALT_B, choice=1, t=7),
        vote(carol, PROPOSAL_ALT_B, choice=1, t=8),
    )
    a = _tally(
        store,
        epoch=EPOCH_2,
        proposal=PROPOSAL_ALT_A,
        constitution=C2,
        target=C2_ALT_A,
        known=known,
    )
    b = _tally(
        store,
        epoch=EPOCH_2,
        proposal=PROPOSAL_ALT_B,
        constitution=C2,
        target=C2_ALT_B,
        known=known,
    )
    assert a.state is TallyState.PENDING
    assert b.state is TallyState.PENDING
    assert len(a.yes) == 1
    assert len(b.yes) == 1
    assert GovernanceFinding.CONFLICTING_APPROVAL in _kinds(a)
    assert GovernanceFinding.CONFLICTING_APPROVAL in _kinds(b)


def test_GV_16() -> None:
    alice, _bob, _carol, _dave, _eve = fresh_p2()
    first = vote(alice, PROPOSAL_2, choice=1, t=1)
    second = vote(alice, PROPOSAL_2, choice=0, t=2)
    store = store_with(first, second)
    result = _tally(
        store, epoch=EPOCH_2, proposal=PROPOSAL_2, constitution=C2, target=C3
    )
    assert result.state is TallyState.PENDING
    assert result.yes == ()
    assert result.no == ()
    assert GovernanceFinding.AMBIGUOUS_VOTE in _kinds(result)
    subjects = {f.subject for f in result.findings if f.kind is GovernanceFinding.AMBIGUOUS_VOTE}
    assert subjects == {claim_id(first), claim_id(second)}


def test_GV_17() -> None:
    outsider = Identity("outsider")
    alice, _bob, _carol, _dave, _eve = fresh_p2()
    outsider_vote = vote(outsider, PROPOSAL_2, choice=1, t=1)
    store = store_with(outsider_vote, vote(alice, PROPOSAL_2, choice=1, t=1))
    result = _tally(
        store, epoch=EPOCH_2, proposal=PROPOSAL_2, constitution=C2, target=C3
    )
    assert result.state is TallyState.PENDING
    assert claim_id(outsider_vote) not in result.yes
    assert GovernanceFinding.NON_MEMBER_VOTE in _kinds(result)


def test_GV_18() -> None:
    alice, _bob, _carol, _dave, _eve = fresh_p2()
    stale = vote(alice, PROPOSAL_1, choice=1, t=1)
    result = _tally(
        store_with(stale),
        epoch=EPOCH_2,
        proposal=PROPOSAL_1,
        constitution=C2,
        target=C2,
    )
    assert result.state is TallyState.UNEVALUABLE
    assert result.findings == (
        Finding(GovernanceFinding.STALE_EPOCH_VOTE, PROPOSAL_1.proposal_hash),
    )


def test_GV_19() -> None:
    alice, _bob, _carol, _dave, _eve = fresh_p2()
    bad = alice.claim(
        p=nuc(N_D, "vote"),
        J=(3, PROPOSAL_2.proposal_hash),
        t=1,
        N=N_D,
        v=cbor_canon.encode({0: 2}),
    )
    store = store_with(bad)
    result = _tally(
        store, epoch=EPOCH_2, proposal=PROPOSAL_2, constitution=C2, target=C3
    )
    assert result.state is TallyState.PENDING
    assert GovernanceFinding.UNKNOWN_VOTE_CHOICE in _kinds(result)


def test_GV_20() -> None:
    alice, _bob, _carol, _dave, _eve = fresh_p2()
    other = bytes(32)
    foreign = vote(alice, PROPOSAL_2, choice=1, t=1, scope=other)
    store = store_with(foreign)
    result = _tally(
        store, epoch=EPOCH_2, proposal=PROPOSAL_2, constitution=C2, target=C3
    )
    assert result.state is TallyState.PENDING
    assert GovernanceFinding.SCOPE_MISMATCH in _kinds(result)


def test_GV_21() -> None:
    result = _tally(
        store_with(),
        epoch=EPOCH_2,
        proposal=PROPOSAL_2,
        constitution=None,
        target=C3,
    )
    assert result.state is TallyState.UNEVALUABLE
    assert result.findings == (
        Finding(GovernanceFinding.CONSTITUTION_UNAVAILABLE, EPOCH_2.constitution_hash),
    )


def test_GV_22() -> None:
    bare = {k: v for k, v in C2.items() if k != "participants"}
    epoch, proposal = _paired(bare)
    result = _tally(
        store_with(),
        epoch=epoch,
        proposal=proposal,
        constitution=bare,
        target=C3,
    )
    assert result.state is TallyState.UNEVALUABLE
    assert GovernanceFinding.PARTICIPANTS_UNDECLARED in _kinds(result)


def test_GV_23() -> None:
    unsorted = dict(C2)
    unsorted["participants"] = list(reversed(P2))
    epoch, proposal = _paired(unsorted)
    result = _tally(
        store_with(),
        epoch=epoch,
        proposal=proposal,
        constitution=unsorted,
        target=C3,
    )
    assert result.state is TallyState.UNEVALUABLE
    assert GovernanceFinding.MALFORMED_PARTICIPANTS in _kinds(result)


def test_GV_24() -> None:
    genesis = dict(GENESIS_D)
    genesis[6] = 1
    scope = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis)).digest()
    epoch = Epoch(
        scope=scope, index=2, constitution_hash=constitution_hash(C2)
    )
    proposal = Proposal(
        scope=scope,
        predecessor=epoch.epoch_id,
        constitution_hash=constitution_hash(C3),
    )
    result = _tally(
        store_with(),
        epoch=epoch,
        proposal=proposal,
        constitution=C2,
        target=C3,
        genesis=genesis,
    )
    assert result.state is TallyState.UNEVALUABLE
    assert GovernanceFinding.UNSUPPORTED_WEIGHT_MODE in _kinds(result)


def test_GV_25() -> None:
    alice, _bob, _carol, _dave, _eve = fresh_p2()
    unknown_hash = bytes(range(32))
    on_this = vote(alice, PROPOSAL_2, choice=1, t=1)
    other = alice.claim(
        p=nuc(N_D, "vote"),
        J=(3, unknown_hash),
        t=2,
        N=N_D,
        v=cbor_canon.encode({0: 1}),
    )
    store = store_with(on_this, other)
    result = _tally(
        store,
        epoch=EPOCH_2,
        proposal=PROPOSAL_2,
        constitution=C2,
        target=C3,
        known={PROPOSAL_2.proposal_hash: PROPOSAL_2},
    )
    assert result.state is TallyState.PENDING
    assert result.yes == ()
    assert GovernanceFinding.UNKNOWN_PROPOSAL in _kinds(result)
    assert Finding(GovernanceFinding.UNKNOWN_PROPOSAL, claim_id(other)) in result.findings


def test_GV_26() -> None:
    alice, _bob, _carol, _dave, _eve = fresh_p2()
    expiring = vote(alice, PROPOSAL_2, choice=1, t=1, t_exp=5000)
    store = store_with(expiring)
    result = _tally(
        store, epoch=EPOCH_2, proposal=PROPOSAL_2, constitution=C2, target=C3
    )
    assert result.state is TallyState.PENDING
    assert result.yes == ()
    assert GovernanceFinding.VOTE_WITH_EXPIRY in _kinds(result)


def test_GV_27() -> None:
    stripped = dict(C2)
    stripped["irrevocable_predicates"] = ["obligation@1", "ratify@1"]
    epoch, proposal = _paired(stripped)
    result = _tally(
        store_with(),
        epoch=epoch,
        proposal=proposal,
        constitution=stripped,
        target=C3,
    )
    assert result.state is TallyState.UNEVALUABLE
    assert GovernanceFinding.VOTE_REVOCABLE in _kinds(result)


def test_GV_28() -> None:
    alice, bob, carol, _dave, _eve = fresh_p2()
    v = vote(alice, PROPOSAL_2, choice=1, t=1)
    rev = alice.revoke(v, t=2)
    store = store_with(
        v,
        rev,
        vote(bob, PROPOSAL_2, choice=1, t=1),
        vote(carol, PROPOSAL_2, choice=1, t=1),
    )
    result = _tally(
        store, epoch=EPOCH_2, proposal=PROPOSAL_2, constitution=C2, target=C3
    )
    assert claim_id(v) in result.yes
    assert result.findings == ()


def test_GV_29() -> None:
    genesis = dict(GENESIS_D)
    genesis[5] = 3
    scope = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis)).digest()
    epoch = Epoch(
        scope=scope, index=2, constitution_hash=constitution_hash(C2)
    )
    proposal = Proposal(
        scope=scope,
        predecessor=epoch.epoch_id,
        constitution_hash=constitution_hash(C3),
    )
    result = _tally(
        store_with(),
        epoch=epoch,
        proposal=proposal,
        constitution=C2,
        target=C3,
        genesis=genesis,
    )
    assert result.state is TallyState.UNEVALUABLE
    assert GovernanceFinding.MALFORMED_THRESHOLD in _kinds(result)


def test_GV_30() -> None:
    alice, bob, carol, _dave = fresh_p1()
    votes = [
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
        vote(carol, PROPOSAL_1, choice=1, t=1),
    ]
    store = store_with(*votes)
    tally = _tally(store)
    missing = bytes(range(32))
    r = ratify_claim(
        alice, PROPOSAL_1, witnesses=[claim_id(v) for v in votes] + [missing], t=10
    )
    store.add(r)
    result = verify_ratification(
        store, ratify=r, epoch=EPOCH_1, proposal=PROPOSAL_1, tally=tally, target_constitution_obj=C2, now=NOW, policy=policy_of(C1)
    )
    assert result.next_epoch is None
    assert GovernanceFinding.UNKNOWN_WITNESS_VOTE in _kinds(result)
    assert GovernanceFinding.UNSUPPORTED_RATIFICATION not in _kinds(result)
    assert Finding(GovernanceFinding.UNKNOWN_WITNESS_VOTE, missing) in result.findings


def test_GV_31() -> None:
    stripped = dict(C2)
    stripped["irrevocable_predicates"] = ["obligation@1", "vote@1"]
    epoch, proposal = _paired(stripped)
    result = _tally(
        store_with(),
        epoch=epoch,
        proposal=proposal,
        constitution=stripped,
        target=C3,
    )
    assert result.state is TallyState.UNEVALUABLE
    assert GovernanceFinding.RATIFY_REVOCABLE in _kinds(result)


def test_GV_32() -> None:
    alice, bob, carol, _dave = fresh_p1()
    votes = [
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
        vote(carol, PROPOSAL_1, choice=1, t=1),
    ]
    store = store_with(*votes)
    tally = _tally(store)
    r = ratify_claim(alice, PROPOSAL_1, witnesses=[claim_id(v) for v in votes], t=10)
    store.add(r)
    policy = policy_of(C1)
    first = verify_ratification(
        store, ratify=r, epoch=EPOCH_1, proposal=PROPOSAL_1, tally=tally, target_constitution_obj=C2, now=NOW, policy=policy
    )
    assert first.next_epoch is not None
    store.add(alice.revoke(r, t=11))
    second = verify_ratification(
        store, ratify=r, epoch=EPOCH_1, proposal=PROPOSAL_1, tally=tally, target_constitution_obj=C2, now=NOW, policy=policy
    )
    assert second.next_epoch is not None
    assert second.next_epoch.epoch_id == first.next_epoch.epoch_id
    assert second.findings == ()


def test_GV_33() -> None:
    alice, bob, carol, _dave = fresh_p1()
    votes = [
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
        vote(carol, PROPOSAL_1, choice=1, t=1),
    ]
    store = store_with(*votes)
    tally = _tally(store)
    r = ratify_claim(
        alice, PROPOSAL_1, witnesses=[claim_id(v) for v in votes], t=10, t_exp=5000
    )
    store.add(r)
    result = verify_ratification(
        store, ratify=r, epoch=EPOCH_1, proposal=PROPOSAL_1, tally=tally, target_constitution_obj=C2, now=NOW, policy=policy_of(C1)
    )
    assert result.next_epoch is None
    assert GovernanceFinding.RATIFY_WITH_EXPIRY in _kinds(result)


def test_GV_34() -> None:
    alice, bob, carol, _dave, _eve = fresh_p2()
    votes = [
        vote(alice, PROPOSAL_2, choice=1, t=2),
        vote(bob, PROPOSAL_2, choice=1, t=3),
        vote(carol, PROPOSAL_2, choice=1, t=4),
    ]
    prop = propose_claim(alice, PROPOSAL_2, t=1)
    store = store_with(prop, *votes)
    before = _tally(
        store, epoch=EPOCH_2, proposal=PROPOSAL_2, constitution=C2, target=C3
    )
    store.add(alice.revoke(prop, t=5))
    after = _tally(
        store, epoch=EPOCH_2, proposal=PROPOSAL_2, constitution=C2, target=C3
    )
    assert before.state == after.state
    assert before.yes == after.yes
    assert before.no == after.no
    assert before.findings == after.findings


def _malformed_amendment(pair: list):
    target = _c2_amendment(pair)
    proposal = Proposal(
        scope=N_D,
        predecessor=EPOCH_2.epoch_id,
        constitution_hash=constitution_hash(target),
    )
    return _tally(
        store_with(),
        epoch=EPOCH_2,
        proposal=proposal,
        constitution=C2,
        target=target,
    )


def test_GV_35() -> None:
    result = _malformed_amendment([1, 3])
    assert result.state is TallyState.UNEVALUABLE
    assert GovernanceFinding.MALFORMED_THRESHOLD in _kinds(result)


def test_GV_36() -> None:
    result = _malformed_amendment([2, 5])
    assert result.state is TallyState.UNEVALUABLE
    assert GovernanceFinding.MALFORMED_THRESHOLD in _kinds(result)


def test_GV_37() -> None:
    result = _malformed_amendment([-1, 2])
    assert result.state is TallyState.UNEVALUABLE
    assert GovernanceFinding.MALFORMED_THRESHOLD in _kinds(result)
    assert result.state is not TallyState.PASSED


def test_GV_38() -> None:
    result = _malformed_amendment([5, 4])
    assert result.state is TallyState.UNEVALUABLE
    assert GovernanceFinding.MALFORMED_THRESHOLD in _kinds(result)


def test_GV_39() -> None:
    result = _malformed_amendment([1, 0])
    assert result.state is TallyState.UNEVALUABLE
    assert GovernanceFinding.MALFORMED_THRESHOLD in _kinds(result)


def test_GV_40() -> None:
    empty = dict(C2)
    empty["participants"] = []
    epoch, proposal = _paired(empty)
    result = _tally(
        store_with(),
        epoch=epoch,
        proposal=proposal,
        constitution=empty,
        target=C3,
    )
    assert result.state is TallyState.UNEVALUABLE
    assert GovernanceFinding.MALFORMED_PARTICIPANTS in _kinds(result)


def test_GV_41() -> None:
    result = _tally(
        store_with(),
        epoch=EPOCH_2,
        proposal=PROPOSAL_1,
        constitution=C2,
        target=C2,
    )
    assert result.state is TallyState.UNEVALUABLE
    assert result.findings == (
        Finding(GovernanceFinding.STALE_EPOCH_VOTE, PROPOSAL_1.proposal_hash),
    )
    assert result.epoch_id == EPOCH_2.epoch_id
    assert result.proposal_hash == PROPOSAL_1.proposal_hash


def test_GV_42() -> None:
    result = _tally(
        store_with(),
        epoch=EPOCH_2,
        proposal=PROPOSAL_2,
        constitution=C1,
        target=C3,
    )
    assert result.state is TallyState.UNEVALUABLE
    assert result.findings == (
        Finding(GovernanceFinding.CONSTITUTION_UNAVAILABLE, EPOCH_2.constitution_hash),
    )


def test_GV_43() -> None:
    alice, _bob, _carol, _dave = fresh_p1()
    tally = _tally(store_with(), constitution=None, proposal=PROPOSAL_1, target=C2)
    assert tally.state is TallyState.UNEVALUABLE
    r = ratify_claim(alice, PROPOSAL_1, witnesses=[], t=10)
    result = verify_ratification(
        store_with(r),
        ratify=r,
        epoch=EPOCH_1,
        proposal=PROPOSAL_1,
        tally=tally,
        target_constitution_obj=C2,
        now=NOW,
        policy=policy_of(C1),
    )
    assert result.next_epoch is None
    assert GovernanceFinding.TALLY_UNEVALUABLE in _kinds(result)
    assert GovernanceFinding.UNSUPPORTED_RATIFICATION not in _kinds(result)


def test_GV_44() -> None:
    alice, bob, carol, _dave = fresh_p1()
    votes = [
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
        vote(carol, PROPOSAL_1, choice=1, t=1),
    ]
    tally = _tally(store_with(*votes))
    r = ratify_claim(alice, PROPOSAL_2, witnesses=[claim_id(v) for v in votes], t=10)
    with pytest.raises(ValueError):
        verify_ratification(
            store_with(*votes, r),
            ratify=r,
            epoch=EPOCH_2,
            proposal=PROPOSAL_2,
            tally=tally,
            target_constitution_obj=C3,
            now=NOW,
            policy=policy_of(C2),
        )


def test_GV_45() -> None:
    with pytest.raises(ValueError):
        membership(
            store_with(),
            subject=EVE.pub,
            scope=N_D,
            constitution_hash=CONSTITUTION_HASH_2,
            now=NOW,
            authorized_keys=frozenset(),
            constitution_obj=C1,
        )


def test_GV_46_decide() -> None:
    foreign = Proposal(
        scope=bytes(32),
        predecessor=EPOCH_1.epoch_id,
        constitution_hash=CONSTITUTION_HASH_2,
    )
    with pytest.raises(ValueError):
        _tally(store_with(), proposal=foreign, constitution=C1, target=C2)


def test_GV_46_verify_ratification() -> None:
    alice, _bob, _carol, _dave = fresh_p1()
    foreign = Proposal(
        scope=bytes(32),
        predecessor=EPOCH_1.epoch_id,
        constitution_hash=CONSTITUTION_HASH_2,
    )
    tally = TallyResult(
        state=TallyState.PASSED,
        yes=(),
        no=(),
        participants=frozenset(),
        threshold=(2, 3),
        findings=(),
        epoch_id=EPOCH_1.epoch_id,
        proposal_hash=foreign.proposal_hash,
    )
    r = ratify_claim(alice, foreign, witnesses=[], t=10)
    with pytest.raises(ValueError):
        verify_ratification(
            store_with(r),
            ratify=r,
            epoch=EPOCH_1,
            proposal=foreign,
            tally=tally,
            target_constitution_obj=C2,
            now=NOW,
            policy=policy_of(C1),
        )


def test_GV_47() -> None:
    for pair in (["3", "4"], ["a", "b"]):
        result = _malformed_amendment(pair)
        assert result.state is TallyState.UNEVALUABLE
        assert GovernanceFinding.MALFORMED_THRESHOLD in _kinds(result)


def test_GV_48() -> None:
    alice, _bob, _carol, _dave, _eve = fresh_p2()
    bad = vote_noncanonical_v(alice, PROPOSAL_2, t=1)
    result = _tally(
        store_with(bad),
        epoch=EPOCH_2,
        proposal=PROPOSAL_2,
        constitution=C2,
        target=C3,
        known={PROPOSAL_2.proposal_hash: PROPOSAL_2},
    )
    assert result.state is TallyState.PENDING
    assert result.yes == ()
    assert result.no == ()
    assert _kinds(result) == {GovernanceFinding.NON_CANONICAL_V}
    assert result.findings == (
        Finding(GovernanceFinding.NON_CANONICAL_V, claim_id(bad)),
    )


def test_GV_49() -> None:
    alice, _bob, _carol, _dave, _eve = fresh_p2()
    first = vote(alice, PROPOSAL_2, choice=1, t=1)
    second = vote_noncanonical_v(alice, PROPOSAL_2, t=2)
    result = _tally(
        store_with(first, second),
        epoch=EPOCH_2,
        proposal=PROPOSAL_2,
        constitution=C2,
        target=C3,
        known={PROPOSAL_2.proposal_hash: PROPOSAL_2},
    )
    assert result.state is TallyState.PENDING
    assert result.yes == (claim_id(first),)
    assert result.no == ()
    assert Finding(GovernanceFinding.NON_CANONICAL_V, claim_id(second)) in result.findings
    assert GovernanceFinding.AMBIGUOUS_VOTE not in _kinds(result)


def test_GV_50() -> None:
    alice, _bob, _carol, _dave, _eve = fresh_p2()
    first = vote(alice, PROPOSAL_2, choice=1, t=1)
    second = vote_noncanonical_v(alice, PROPOSAL_ALT_A, t=2)
    result = _tally(
        store_with(first, second),
        epoch=EPOCH_2,
        proposal=PROPOSAL_2,
        constitution=C2,
        target=C3,
        known={
            PROPOSAL_2.proposal_hash: PROPOSAL_2,
            PROPOSAL_ALT_A.proposal_hash: PROPOSAL_ALT_A,
        },
    )
    assert result.yes == (claim_id(first),)
    assert Finding(GovernanceFinding.NON_CANONICAL_V, claim_id(second)) in result.findings
    assert GovernanceFinding.CONFLICTING_APPROVAL not in _kinds(result)


def test_GV_51() -> None:
    alice, bob, carol, dave, _eve = fresh_p2()
    votes = [
        vote(alice, PROPOSAL_2, choice=1, t=1),
        vote(bob, PROPOSAL_2, choice=1, t=1),
        vote(carol, PROPOSAL_2, choice=1, t=1),
        vote(dave, PROPOSAL_2, choice=1, t=1),
    ]
    store = store_with(*votes)
    tally = _tally(
        store, epoch=EPOCH_2, proposal=PROPOSAL_2, constitution=C2, target=C3
    )
    assert tally.state is TallyState.PASSED
    assert len(tally.yes) == 4
    canonical_v = cbor_canon.encode({0: list(tally.yes)})
    assert canonical_v[:2] == bytes.fromhex("a100")
    assert canonical_v[2:3] == bytes.fromhex("84")
    noncanonical_v = canonical_v[:2] + bytes.fromhex("9804") + canonical_v[3:]
    r = alice.claim(
        p=nuc(N_D, "ratify"),
        J=(3, PROPOSAL_2.proposal_hash),
        t=5,
        N=N_D,
        v=noncanonical_v,
    )
    store.add(r)
    result = verify_ratification(
        store,
        ratify=r,
        epoch=EPOCH_2,
        proposal=PROPOSAL_2,
        tally=tally,
        target_constitution_obj=C3,
        now=NOW,
        policy=policy_of(C2),
    )
    assert result.next_epoch is None
    assert Finding(GovernanceFinding.NON_CANONICAL_V, claim_id(r)) in result.findings
    assert GovernanceFinding.UNSUPPORTED_RATIFICATION not in _kinds(result)


def test_GV_52() -> None:
    alice, _bob, _carol, _dave, _eve = fresh_p2()
    bad = vote_unparsable_v(alice, PROPOSAL_2, t=1)
    result = _tally(
        store_with(bad),
        epoch=EPOCH_2,
        proposal=PROPOSAL_2,
        constitution=C2,
        target=C3,
        known={PROPOSAL_2.proposal_hash: PROPOSAL_2},
    )
    assert result.state is TallyState.PENDING
    assert result.yes == ()
    assert result.no == ()
    assert _kinds(result) == {GovernanceFinding.UNPARSABLE_V}
    assert result.findings == (
        Finding(GovernanceFinding.UNPARSABLE_V, claim_id(bad)),
    )
    assert GovernanceFinding.NON_CANONICAL_V not in _kinds(result)
    assert GovernanceFinding.UNKNOWN_VOTE_CHOICE not in _kinds(result)


def test_GV_53() -> None:
    alice, _bob, _carol, _dave, _eve = fresh_p2()
    first = vote(alice, PROPOSAL_2, choice=1, t=1)
    second = vote_unparsable_v(alice, PROPOSAL_ALT_A, t=2)
    result = _tally(
        store_with(first, second),
        epoch=EPOCH_2,
        proposal=PROPOSAL_2,
        constitution=C2,
        target=C3,
        known={
            PROPOSAL_2.proposal_hash: PROPOSAL_2,
            PROPOSAL_ALT_A.proposal_hash: PROPOSAL_ALT_A,
        },
    )
    assert result.yes == (claim_id(first),)
    assert Finding(GovernanceFinding.UNPARSABLE_V, claim_id(second)) in result.findings
    assert GovernanceFinding.CONFLICTING_APPROVAL not in _kinds(result)


def test_GV_54() -> None:
    alice, bob, carol, dave, _eve = fresh_p2()
    votes = [
        vote(alice, PROPOSAL_2, choice=1, t=1),
        vote(bob, PROPOSAL_2, choice=1, t=1),
        vote(carol, PROPOSAL_2, choice=1, t=1),
        vote(dave, PROPOSAL_2, choice=1, t=1),
    ]
    store = store_with(*votes)
    tally = _tally(
        store, epoch=EPOCH_2, proposal=PROPOSAL_2, constitution=C2, target=C3
    )
    assert tally.state is TallyState.PASSED
    assert len(tally.yes) == 4
    r = alice.claim(
        p=nuc(N_D, "ratify"),
        J=(3, PROPOSAL_2.proposal_hash),
        t=5,
        N=N_D,
        v=bytes.fromhex("a2000101ff"),
    )
    store.add(r)
    result = verify_ratification(
        store,
        ratify=r,
        epoch=EPOCH_2,
        proposal=PROPOSAL_2,
        tally=tally,
        target_constitution_obj=C3,
        now=NOW,
        policy=policy_of(C2),
    )
    assert result.next_epoch is None
    assert Finding(GovernanceFinding.UNPARSABLE_V, claim_id(r)) in result.findings
    assert GovernanceFinding.UNSUPPORTED_RATIFICATION not in _kinds(result)
