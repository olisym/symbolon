"""Epochenkette — resolve_epoch (04-governance.md §4.5, D174, D175, D178)."""

from __future__ import annotations

import pytest

from symbolon.atom import claim_id
from symbolon.governance import (
    Finding,
    GovernanceFinding,
    resolve_epoch,
)
from symbolon.governance.findings import dedupe_sort
from symbolon.governance.tally import TallyState
from symbolon.predicates import is_nuc_name
from tests.helpers import store_with

from .fixtures import (
    C1,
    C2,
    C3,
    CONSTITUTION_HASH_1,
    CONSTITUTION_HASH_2,
    CONSTITUTION_HASH_3,
    EPOCH_1,
    EPOCH_2,
    EPOCH_3,
    GENESIS_D,
    N_D,
    NOW,
    PROPOSAL_1,
    PROPOSAL_2,
    PROPOSAL_ALT_A,
    STOCK_N,
    _tally,
    fresh_frank,
    fresh_p2,
    ratify_claim,
    vote,
)


class _World:
    def __init__(self, *, extra_epoch1_ratify: bool = False) -> None:
        alice, bob, carol, dave, eve = fresh_p2()
        self.alice = alice
        self.bob = bob
        v1 = [
            vote(alice, PROPOSAL_1, choice=1, t=1),
            vote(bob, PROPOSAL_1, choice=1, t=1),
            vote(carol, PROPOSAL_1, choice=1, t=1),
            vote(dave, PROPOSAL_1, choice=1, t=1),
        ]
        self.yes1 = [claim_id(v) for v in v1]
        self.r1 = ratify_claim(alice, PROPOSAL_1, witnesses=self.yes1[:3], t=10)
        claims = [*v1, self.r1]
        if extra_epoch1_ratify:
            claims.append(ratify_claim(bob, PROPOSAL_1, witnesses=[], t=11))
        v2 = [
            vote(alice, PROPOSAL_2, choice=1, t=20),
            vote(bob, PROPOSAL_2, choice=1, t=20),
            vote(carol, PROPOSAL_2, choice=1, t=20),
            vote(dave, PROPOSAL_2, choice=1, t=20),
            vote(eve, PROPOSAL_2, choice=1, t=20),
        ]
        yes2 = [claim_id(v) for v in v2]
        self.r2 = ratify_claim(alice, PROPOSAL_2, witnesses=yes2[:4], t=30)
        claims.extend([*v2, self.r2])
        self.store = store_with(*claims)


def _two_transitions(*, extra_epoch1_ratify: bool = False) -> _World:
    return _World(extra_epoch1_ratify=extra_epoch1_ratify)


def _resolve(
    store,
    *,
    constitutions: dict | None = None,
    proposals: dict | None = None,
    scope: bytes = N_D,
    genesis: dict = GENESIS_D,
):
    if constitutions is None:
        constitutions = {
            CONSTITUTION_HASH_1: C1,
            CONSTITUTION_HASH_2: C2,
            CONSTITUTION_HASH_3: C3,
        }
    if proposals is None:
        proposals = {
            PROPOSAL_1.proposal_hash: PROPOSAL_1,
            PROPOSAL_2.proposal_hash: PROPOSAL_2,
        }
    return resolve_epoch(
        store,
        scope=scope,
        genesis_obj=genesis,
        known_constitutions=constitutions,
        known_proposals=proposals,
        now=NOW,
    )


def test_chain_two_transitions() -> None:
    result = _resolve(_two_transitions().store)
    assert result.epoch.epoch_id == EPOCH_3.epoch_id
    assert result.constitution_obj == C3
    assert result.findings == ()


def test_chain_without_ratification_stays_at_epoch_1() -> None:
    alice, bob, carol, dave, _eve = fresh_p2()
    store = store_with(
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
        vote(carol, PROPOSAL_1, choice=1, t=1),
        vote(dave, PROPOSAL_1, choice=1, t=1),
    )
    result = _resolve(store)
    assert result.epoch.index == 1
    assert result.constitution_obj == C1
    assert result.findings == ()


def test_chain_missing_c3_stops_at_epoch_2() -> None:
    """Das Verfassungsobjekt von i+1 ist das Zielobjekt des Übergangs (04 §3.5, 04 §4.1)."""
    world = _two_transitions()
    result = _resolve(
        world.store,
        constitutions={
            CONSTITUTION_HASH_1: C1,
            CONSTITUTION_HASH_2: C2,
        },
    )
    assert result.epoch.epoch_id == EPOCH_2.epoch_id
    assert result.constitution_obj == C2
    assert result.findings == dedupe_sort(
        [
            Finding(
                GovernanceFinding.TALLY_UNEVALUABLE,
                claim_id(world.r2),
            ),
            Finding(
                GovernanceFinding.PROPOSAL_CONSTITUTION_UNAVAILABLE,
                PROPOSAL_2.constitution_hash,
            ),
        ]
    )


def test_chain_missing_proposal_2() -> None:
    """D178: Ja auf unbekannten Vorschlag von i+1 setzt denselben Autor in i aus."""
    world = _two_transitions()
    result = _resolve(
        world.store,
        proposals={PROPOSAL_1.proposal_hash: PROPOSAL_1},
    )
    assert result.epoch.epoch_id == EPOCH_1.epoch_id
    expected = [
        Finding(
            GovernanceFinding.EPOCH_PROPOSAL_UNAVAILABLE,
            PROPOSAL_2.proposal_hash,
        ),
        Finding(
            GovernanceFinding.UNSUPPORTED_RATIFICATION,
            claim_id(world.r1),
        ),
    ]
    unknown = [
        claim
        for claim in world.store.all_claims()
        if is_nuc_name(claim, "vote")
        and claim.J == (3, PROPOSAL_2.proposal_hash)
        and claim.I in C1["participants"]
    ]
    assert len(unknown) == 4
    for claim in unknown:
        expected.append(Finding(GovernanceFinding.UNKNOWN_PROPOSAL, claim_id(claim)))
    assert result.findings == dedupe_sort(expected)


def test_chain_miskeyed_c3_stops_at_epoch_1() -> None:
    """C3 unter dem Hash von C2: das Zielobjekt des ersten Übergangs fehlt (04 §3.5)."""
    world = _two_transitions()
    result = _resolve(
        world.store,
        constitutions={
            CONSTITUTION_HASH_1: C1,
            CONSTITUTION_HASH_2: C3,
        },
    )
    assert result.epoch.epoch_id == EPOCH_1.epoch_id
    assert result.constitution_obj == C1
    assert result.findings == dedupe_sort(
        [
            Finding(
                GovernanceFinding.TALLY_UNEVALUABLE,
                claim_id(world.r1),
            ),
            Finding(
                GovernanceFinding.PROPOSAL_CONSTITUTION_UNAVAILABLE,
                PROPOSAL_1.constitution_hash,
            ),
        ]
    )


def test_chain_wrong_scope_raises() -> None:
    with pytest.raises(ValueError):
        _resolve(_two_transitions().store, scope=STOCK_N)


def test_chain_stale_epoch_findings_absent() -> None:
    result = _resolve(_two_transitions(extra_epoch1_ratify=True).store)
    assert result.epoch.epoch_id == EPOCH_3.epoch_id
    assert result.findings == ()


def test_decide_miskeyed_proposal_is_unknown() -> None:
    alice, *_rest = fresh_p2()
    on_this = vote(alice, PROPOSAL_2, choice=1, t=1)
    other = vote(alice, PROPOSAL_ALT_A, choice=1, t=2)
    store = store_with(on_this, other)
    result = _tally(
        store,
        epoch=EPOCH_2,
        proposal=PROPOSAL_2,
        constitution=C2,
        target=C3,
        known={
            PROPOSAL_2.proposal_hash: PROPOSAL_2,
            PROPOSAL_ALT_A.proposal_hash: PROPOSAL_1,
        },
    )
    assert result.state is TallyState.PENDING
    assert result.yes == ()
    assert Finding(GovernanceFinding.UNKNOWN_PROPOSAL, claim_id(other)) in result.findings
    kinds = {f.kind for f in result.findings}
    assert GovernanceFinding.CONFLICTING_APPROVAL not in kinds


def test_chain_epoch_1_constitution_missing() -> None:
    result = _resolve(store_with(), constitutions={})
    assert result.epoch.epoch_id == EPOCH_1.epoch_id
    assert result.constitution_obj is None
    assert result.findings == ()


def test_chain_unknown_proposal_without_section_4_4() -> None:
    world = _two_transitions()
    r_alt = ratify_claim(world.bob, PROPOSAL_ALT_A, witnesses=[], t=31)
    world.store.add(r_alt)
    result = _resolve(world.store)
    assert result.epoch.epoch_id == EPOCH_3.epoch_id
    assert result.findings == (
        Finding(
            GovernanceFinding.EPOCH_PROPOSAL_UNAVAILABLE,
            PROPOSAL_ALT_A.proposal_hash,
        ),
    )


def test_chain_miskeyed_current_constitution_no_valueerror() -> None:
    result = _resolve(
        store_with(),
        constitutions={CONSTITUTION_HASH_1: C2},
    )
    assert result.epoch.epoch_id == EPOCH_1.epoch_id
    assert result.constitution_obj is None


def test_chain_equivocated_unknown_ratify_is_silent() -> None:
    """D107: Equivocation nimmt ratify@1 aus ACTIVE, Widerruf nicht."""
    world = _two_transitions()
    a = fresh_frank()
    b = fresh_frank()
    world.store.add(ratify_claim(a, PROPOSAL_ALT_A, witnesses=[], t=31))
    world.store.add(ratify_claim(b, PROPOSAL_ALT_A, witnesses=[], t=32))
    result = _resolve(world.store)
    assert result.epoch.epoch_id == EPOCH_3.epoch_id
    assert result.findings == ()
