"""Subjekte der Auszählungsvermerke (04-governance.md §3.5, D198)."""

from __future__ import annotations

import hashlib

from symbolon import cbor_canon
from symbolon.atom import claim_id
from symbolon.domains import DOM_NUC_GEN
from symbolon.governance.epoch import verify_ratification
from symbolon.governance.findings import Finding, GovernanceFinding, dedupe_sort
from symbolon.governance.objects import Epoch, Proposal
from symbolon.governance.tally import TallyState
from symbolon.policy import constitution_hash
from tests.helpers import store_with

from .fixtures import (
    C1,
    C2,
    C3,
    EPOCH_1,
    GENESIS_D,
    N_D,
    NOW,
    PROPOSAL_1,
    _tally,
    fresh_p1,
    policy_of,
    ratify_claim,
    vote,
)


def _paar(cons, ziel, *, scope=N_D, index=2):
    epoch = Epoch(
        scope=scope, index=index, constitution_hash=constitution_hash(cons)
    )
    proposal = Proposal(
        scope=scope,
        predecessor=epoch.epoch_id,
        constitution_hash=constitution_hash(ziel),
    )
    return epoch, proposal


def test_malformed_threshold_in_target_addresses_proposal() -> None:
    """Formwidrige Schwelle in der Zielverfassung adressiert deren Hash (04 §3.5, D198)."""
    ziel = dict(C2)
    ziel["thresholds"] = dict(C2["thresholds"])
    ziel["thresholds"]["amendment"] = [3, 2]
    epoch, proposal = _paar(C2, ziel)
    result = _tally(
        store_with(),
        epoch=epoch,
        proposal=proposal,
        constitution=C2,
        target=ziel,
        known={proposal.proposal_hash: proposal},
    )
    assert result.state is TallyState.UNEVALUABLE
    assert len(result.findings) == 1
    assert result.findings[0].kind == GovernanceFinding.MALFORMED_THRESHOLD
    assert result.findings[0].subject == proposal.constitution_hash
    assert result.findings[0].subject != epoch.constitution_hash


def test_unsupported_weight_mode_addresses_scope() -> None:
    """genesis[6] ≠ 0 adressiert den Scope (04 §3.5, D198)."""
    genesis = dict(GENESIS_D)
    genesis[6] = 1
    scope = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis)).digest()
    epoch, proposal = _paar(C2, C3, scope=scope)
    result = _tally(
        store_with(),
        epoch=epoch,
        proposal=proposal,
        constitution=C2,
        target=C3,
        genesis=genesis,
        known={proposal.proposal_hash: proposal},
    )
    assert result.state is TallyState.UNEVALUABLE
    assert len(result.findings) == 1
    assert result.findings[0].kind == GovernanceFinding.UNSUPPORTED_WEIGHT_MODE
    assert result.findings[0].subject == epoch.scope


def test_malformed_genesis_threshold_addresses_scope() -> None:
    """genesis[5] außerhalb der Klassen adressiert den Scope (04 §3.5, D198)."""
    genesis = dict(GENESIS_D)
    genesis[5] = 3
    scope = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis)).digest()
    epoch, proposal = _paar(C2, C3, scope=scope)
    result = _tally(
        store_with(),
        epoch=epoch,
        proposal=proposal,
        constitution=C2,
        target=C3,
        genesis=genesis,
        known={proposal.proposal_hash: proposal},
    )
    assert result.state is TallyState.UNEVALUABLE
    assert len(result.findings) == 1
    assert result.findings[0].kind == GovernanceFinding.MALFORMED_THRESHOLD
    assert result.findings[0].subject == epoch.scope


def test_participants_undeclared_addresses_epoch_constitution() -> None:
    """participants fehlt in der Epochenverfassung: Subjekt ist deren Hash (D200)."""
    cons = dict(C2)
    del cons["participants"]
    epoch, proposal = _paar(cons, C3)
    result = _tally(
        store_with(),
        epoch=epoch,
        proposal=proposal,
        constitution=cons,
        target=C3,
        known={proposal.proposal_hash: proposal},
    )
    assert result.state is TallyState.UNEVALUABLE
    assert len(result.findings) == 1
    assert result.findings[0].kind == GovernanceFinding.PARTICIPANTS_UNDECLARED
    assert result.findings[0].subject == epoch.constitution_hash
    assert result.findings[0].subject != proposal.constitution_hash


def test_cited_non_claim_id_and_non_yes_are_unsupported_ratification() -> None:
    """Nicht-claim_id und Nein-Stimme: UNSUPPORTED_RATIFICATION auf den ratify (04 §4.1, D207)."""
    alice, bob, _c, _d = fresh_p1()
    ja = vote(alice, PROPOSAL_1, choice=1, t=1)
    nein = vote(bob, PROPOSAL_1, choice=0, t=1)
    store = store_with(ja, nein)
    tally = _tally(store)
    ratify = ratify_claim(alice, PROPOSAL_1, witnesses=[claim_id(nein), 42], t=10)
    store.add(ratify)
    result = verify_ratification(
        store,
        ratify=ratify,
        epoch=EPOCH_1,
        proposal=PROPOSAL_1,
        tally=tally,
        target_constitution_obj=C2,
        now=NOW,
        policy=policy_of(C1),
    )
    assert tally.state is TallyState.PENDING
    assert tally.findings == ()
    assert claim_id(nein) not in tally.yes
    assert result.next_epoch is None
    assert result.findings == (
        Finding(GovernanceFinding.UNSUPPORTED_RATIFICATION, claim_id(ratify)),
    )


def test_vote_with_expiry_unsupported_ratification_names_the_ratify() -> None:
    """Ratifizierung scheitert bei Tally-Vermerken: Subjekt ist der ratify (04 §4.1, D94, D203)."""
    alice, bob, carol, _dave = fresh_p1()
    votes = [
        vote(alice, PROPOSAL_1, choice=1, t=1, t_exp=5000),
        vote(bob, PROPOSAL_1, choice=1, t=1, t_exp=5000),
        vote(carol, PROPOSAL_1, choice=1, t=1, t_exp=5000),
    ]
    store = store_with(*votes)
    tally = _tally(store)
    ratify = ratify_claim(
        alice, PROPOSAL_1, witnesses=[claim_id(v) for v in votes], t=10
    )
    store.add(ratify)
    result = verify_ratification(
        store,
        ratify=ratify,
        epoch=EPOCH_1,
        proposal=PROPOSAL_1,
        tally=tally,
        target_constitution_obj=C2,
        now=NOW,
        policy=policy_of(C1),
    )
    expected = dedupe_sort(
        [
            Finding(
                GovernanceFinding.UNSUPPORTED_RATIFICATION, claim_id(ratify)
            ),
            *[
                Finding(GovernanceFinding.VOTE_WITH_EXPIRY, claim_id(v))
                for v in votes
            ],
        ]
    )
    assert result.next_epoch is None
    assert result.findings == expected
