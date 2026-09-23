"""Weitergabe der Auszählungsvermerke ohne Folgeepoche (04 §4.1, 04 §4.5, D203)."""

from __future__ import annotations

from symbolon.atom import claim_id
from symbolon.governance import Finding, GovernanceFinding, verify_ratification
from symbolon.governance.findings import dedupe_sort
from symbolon.governance.objects import Proposal
from symbolon.governance.tally import TallyState
from symbolon.policy import constitution_hash
from symbolon.resolve import resolve_state
from tests.helpers import Identity, store_with
from tests.test_kettenwelt import _welt

from .fixtures import (
    C1,
    C2,
    EPOCH_1,
    NOW,
    PROPOSAL_1,
    _tally,
    fresh_p1,
    policy_of,
    ratify_claim,
    vote,
)


def _fremd() -> Identity:
    fremd = Identity("fremder")
    assert fremd.pub not in C1["participants"]
    return fremd


def test_pending_tally_findings_reach_unsupported_ratification() -> None:
    """Zwei gültige Ja und ein fremdes: PENDING trägt NON_MEMBER_VOTE mit (D203)."""
    alice, bob, _carol, _dave = fresh_p1()
    fremd = _fremd()
    yes = [
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
    ]
    fremd_vote = vote(fremd, PROPOSAL_1, choice=1, t=1)
    store = store_with(*yes, fremd_vote)
    tally = _tally(store)
    r = ratify_claim(alice, PROPOSAL_1, witnesses=[claim_id(v) for v in yes], t=10)
    store.add(r)
    result = verify_ratification(
        store,
        ratify=r,
        epoch=EPOCH_1,
        proposal=PROPOSAL_1,
        tally=tally,
        target_constitution_obj=C2,
        now=NOW,
        policy=policy_of(C1),
    )
    assert tally.state is TallyState.PENDING
    assert result.next_epoch is None
    assert result.findings == dedupe_sort(
        [
            Finding(GovernanceFinding.UNSUPPORTED_RATIFICATION, claim_id(r)),
            Finding(GovernanceFinding.NON_MEMBER_VOTE, claim_id(fremd_vote)),
        ]
    )


def test_pending_tally_findings_reach_ratify_with_expiry() -> None:
    """Auszählungsvermerke erreichen ``RATIFY_WITH_EXPIRY`` (04 §4.1, D203, D431)."""
    alice, bob, _carol, _dave = fresh_p1()
    fremd = _fremd()
    yes = [
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
    ]
    fremd_vote = vote(fremd, PROPOSAL_1, choice=1, t=1)
    store = store_with(*yes, fremd_vote)
    tally = _tally(store)
    r = ratify_claim(
        alice,
        PROPOSAL_1,
        witnesses=[claim_id(v) for v in yes],
        t=10,
        t_exp=10**9,
    )
    store.add(r)
    result = verify_ratification(
        store,
        ratify=r,
        epoch=EPOCH_1,
        proposal=PROPOSAL_1,
        tally=tally,
        target_constitution_obj=C2,
        now=NOW,
        policy=policy_of(C1),
    )
    assert len(tally.findings) >= 1
    assert tally.state is TallyState.PENDING
    assert result.next_epoch is None
    assert Finding(GovernanceFinding.RATIFY_WITH_EXPIRY, claim_id(r)) in result.findings
    for vermerk in tally.findings:
        assert vermerk in result.findings


def test_governability_block_carries_tally_findings() -> None:
    """Bedingung 6 trägt die Auszählungsvermerke mit (D203)."""
    alice, bob, carol, dave = fresh_p1()
    fremd = _fremd()
    ziel = dict(C2)
    del ziel["participants"]
    proposal = Proposal(
        scope=EPOCH_1.scope,
        predecessor=EPOCH_1.epoch_id,
        constitution_hash=constitution_hash(ziel),
    )
    yes = [
        vote(alice, proposal, choice=1, t=1),
        vote(bob, proposal, choice=1, t=1),
        vote(carol, proposal, choice=1, t=1),
        vote(dave, proposal, choice=1, t=1),
    ]
    fremd_vote = vote(fremd, proposal, choice=1, t=1)
    store = store_with(*yes, fremd_vote)
    tally = _tally(store, proposal=proposal, constitution=C1, target=ziel)
    r = ratify_claim(alice, proposal, witnesses=[claim_id(v) for v in yes], t=10)
    store.add(r)
    result = verify_ratification(
        store,
        ratify=r,
        epoch=EPOCH_1,
        proposal=proposal,
        tally=tally,
        target_constitution_obj=ziel,
        now=NOW,
        policy=policy_of(C1),
    )
    assert tally.state is TallyState.PASSED
    assert result.next_epoch is None
    assert result.findings == dedupe_sort(
        [
            Finding(GovernanceFinding.PARTICIPANTS_UNDECLARED, proposal.constitution_hash),
            Finding(GovernanceFinding.NON_MEMBER_VOTE, claim_id(fremd_vote)),
        ]
    )


def test_carried_ratification_drops_tally_findings() -> None:
    """Eine tragende Ratifizierung gibt die Auszählungsvermerke nicht weiter (04 §4.1, D203)."""
    alice, bob, carol, dave = fresh_p1()
    fremd = _fremd()
    yes = [
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
        vote(carol, PROPOSAL_1, choice=1, t=1),
        vote(dave, PROPOSAL_1, choice=1, t=1),
    ]
    fremd_vote = vote(fremd, PROPOSAL_1, choice=1, t=1)
    store = store_with(*yes, fremd_vote)
    tally = _tally(store)
    r = ratify_claim(alice, PROPOSAL_1, witnesses=[claim_id(v) for v in yes], t=10)
    store.add(r)
    result = verify_ratification(
        store,
        ratify=r,
        epoch=EPOCH_1,
        proposal=PROPOSAL_1,
        tally=tally,
        target_constitution_obj=C2,
        now=NOW,
        policy=policy_of(C1),
    )
    assert tally.state is TallyState.PASSED
    assert tally.findings == (
        Finding(GovernanceFinding.NON_MEMBER_VOTE, claim_id(fremd_vote)),
    )
    assert result.next_epoch is not None
    assert result.findings == ()


def test_carried_transition_drops_tally_findings() -> None:
    """Ein tragender Übergang gibt die Auszählungsvermerke nicht weiter (04 §4.5, D203)."""
    welt, _a, _b, _c = _welt()
    fremd = _fremd()
    welt.store.add(
        vote(fremd, welt.vorschlaege[0], choice=1, t=2, scope=welt.scope)
    )
    state = resolve_state(
        welt.store,
        scope=welt.scope,
        genesis_obj=welt.genesis_obj,
        known_constitutions=welt.known_constitutions,
        known_proposals=welt.known_proposals,
        now=welt.now,
    )
    assert state.epoch == welt.epochen[1]
    assert state.epoch_findings == ()
