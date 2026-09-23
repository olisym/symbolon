"""Kettenwelt: der Schlüsselsatz wandert mit der Epoche (D183, D190)."""

from __future__ import annotations

from symbolon.atom import claim_id
from symbolon.governance import Finding, GovernanceFinding
from symbolon.governance.findings import dedupe_sort
from symbolon.keys import resolve_authorized_keys
from symbolon.predicates import is_nuc_name
from symbolon.profiles.policy import resolve_policy
from symbolon.resolve import resolve_state
from tests.helpers import Identity
from tests.kettenwelt import Kettenwelt, kettenwelt


def _welt() -> tuple[Kettenwelt, Identity, Identity, Identity]:
    a = Identity("A")
    b = Identity("B")
    c = Identity("C")
    people = sorted([a.pub, b.pub, c.pub])
    schwellen = {
        "ordinary": [1, 2],
        "membership": [1, 2],
        "amendment": [1, 2],
    }
    basis = {
        "irrevocable_predicates": ["obligation@1", "ratify@1", "vote@1"],
        "thresholds": schwellen,
        "arbitration": {"arbitrators": people},
        "participants": people,
    }
    erste = dict(basis)
    zweite = dict(basis)
    zweite["nucleus_keys"] = [b.pub]
    welt = kettenwelt(
        identitaeten=(a, b, c),
        root_keys=(a.pub,),
        verfassungen=(erste, zweite),
    )
    return welt, a, b, c


def _welt3(*, c2_ohne_participants: bool = False) -> tuple[Kettenwelt, Identity, Identity, Identity]:
    a = Identity("A")
    b = Identity("B")
    c = Identity("C")
    people = sorted([a.pub, b.pub, c.pub])
    schwellen = {
        "ordinary": [1, 2],
        "membership": [1, 2],
        "amendment": [1, 2],
    }
    basis = {
        "irrevocable_predicates": ["obligation@1", "ratify@1", "vote@1"],
        "thresholds": schwellen,
        "arbitration": {"arbitrators": people},
        "participants": people,
    }
    erste = dict(basis)
    zweite = dict(basis)
    zweite["nucleus_keys"] = [b.pub]
    if c2_ohne_participants:
        del zweite["participants"]
    dritte = dict(basis)
    dritte["nucleus_keys"] = [c.pub]
    welt = kettenwelt(
        identitaeten=(a, b, c),
        root_keys=(a.pub,),
        verfassungen=(erste, zweite, dritte),
    )
    return welt, a, b, c


def _welt_policy() -> tuple[Kettenwelt, Identity, Identity, Identity]:
    """Zweite Verfassung erweitert irrevocable_predicates um ``propose@1`` (01 §5.4.3 b)."""
    a = Identity("A")
    b = Identity("B")
    c = Identity("C")
    people = sorted([a.pub, b.pub, c.pub])
    schwellen = {
        "ordinary": [1, 2],
        "membership": [1, 2],
        "amendment": [1, 2],
    }
    basis = {
        "irrevocable_predicates": ["obligation@1", "ratify@1", "vote@1"],
        "thresholds": schwellen,
        "arbitration": {"arbitrators": people},
        "participants": people,
    }
    erste = dict(basis)
    zweite = dict(basis)
    zweite["irrevocable_predicates"] = [*basis["irrevocable_predicates"], "propose@1"]
    welt = kettenwelt(
        identitaeten=(a, b, c),
        root_keys=(a.pub,),
        verfassungen=(erste, zweite),
    )
    return welt, a, b, c


def test_kettenwelt_policy_follows_epoch() -> None:
    """``state.policy`` ist die Policy der zweiten Verfassung (D430)."""
    welt, _a, _b, _c = _welt_policy()
    state = resolve_state(
        welt.store,
        scope=welt.scope,
        genesis_obj=welt.genesis_obj,
        known_constitutions=welt.known_constitutions,
        known_proposals=welt.known_proposals,
        now=welt.now,
    )
    erste = resolve_policy(
        scope=welt.scope,
        genesis_obj=welt.genesis_obj,
        constitution_hash=welt.verfassungs_hashes[0],
        constitution_obj=welt.verfassungen[0],
    ).policy
    zweite = resolve_policy(
        scope=welt.scope,
        genesis_obj=welt.genesis_obj,
        constitution_hash=welt.verfassungs_hashes[1],
        constitution_obj=welt.verfassungen[1],
    ).policy
    assert state.epoch.index == 2
    assert state.epoch == welt.epochen[1]
    assert state.policy == zweite
    assert state.policy != erste


def test_kettenwelt_authorized_keys_follow_epoch() -> None:
    """Ein Fehlgriff in der Epoche liefert einen anderen Schlüsselsatz (D183, D190)."""
    welt, a, b, _c = _welt()
    state = resolve_state(
        welt.store,
        scope=welt.scope,
        genesis_obj=welt.genesis_obj,
        known_constitutions=welt.known_constitutions,
        known_proposals=welt.known_proposals,
        now=welt.now,
    )
    assert state.epoch == welt.epochen[1]
    assert state.constitution_obj == welt.verfassungen[1]
    assert state.authorized_keys == frozenset([b.pub])
    from_first = resolve_authorized_keys(
        welt.store,
        scope=welt.scope,
        genesis_obj=welt.genesis_obj,
        constitution_hash=welt.verfassungs_hashes[0],
        constitution_obj=welt.verfassungen[0],
        now=welt.now,
        policy=resolve_policy(
            scope=welt.scope,
            genesis_obj=welt.genesis_obj,
            constitution_hash=welt.verfassungs_hashes[0],
            constitution_obj=welt.verfassungen[0],
        ).policy,
    )
    assert from_first.keys == frozenset(welt.genesis_obj[1])
    assert from_first.keys == frozenset([a.pub])
    assert state.authorized_keys != from_first.keys


def test_kettenwelt_chain_has_no_findings() -> None:
    """Die Kette läuft ohne Vermerke (D190)."""
    welt, _a, _b, _c = _welt()
    state = resolve_state(
        welt.store,
        scope=welt.scope,
        genesis_obj=welt.genesis_obj,
        known_constitutions=welt.known_constitutions,
        known_proposals=welt.known_proposals,
        now=welt.now,
    )
    assert state.epoch_findings == ()
    assert state.policy_findings == ()
    assert state.key_findings == ()


def test_kettenwelt_missing_middle_constitution_blocks_chain() -> None:
    """Fehlende Zwischenverfassung sperrt die Kette (D195)."""
    welt, _a, _b, _c = _welt3()
    known = dict(welt.known_constitutions)
    del known[welt.verfassungs_hashes[1]]
    state = resolve_state(
        welt.store,
        scope=welt.scope,
        genesis_obj=welt.genesis_obj,
        known_constitutions=known,
        known_proposals=welt.known_proposals,
        now=welt.now,
    )
    erster_ratify = next(
        claim
        for claim in welt.store.all_claims()
        if is_nuc_name(claim, "ratify")
        and claim.J == (3, welt.vorschlaege[0].proposal_hash)
    )
    assert state.epoch == welt.epochen[0]
    assert state.constitution_obj == welt.verfassungen[0]
    assert state.authorized_keys == frozenset(welt.genesis_obj[1])
    assert state.policy_findings == ()
    assert state.key_findings == ()
    assert state.epoch_findings == dedupe_sort(
        [
            Finding(
                GovernanceFinding.PROPOSAL_CONSTITUTION_UNAVAILABLE,
                welt.verfassungs_hashes[1],
            ),
            Finding(
                GovernanceFinding.TALLY_UNEVALUABLE,
                claim_id(erster_ratify),
            ),
        ]
    )


def test_kettenwelt_unusable_middle_constitution_blocks_chain() -> None:
    """Die untaugliche Zwischenverfassung sperrt die Kette vor dem Übergang (D200)."""
    welt, _a, _b, _c = _welt3(c2_ohne_participants=True)
    state = resolve_state(
        welt.store,
        scope=welt.scope,
        genesis_obj=welt.genesis_obj,
        known_constitutions=welt.known_constitutions,
        known_proposals=welt.known_proposals,
        now=welt.now,
    )
    assert state.epoch == welt.epochen[0]
    assert state.constitution_obj == welt.verfassungen[0]
    assert state.authorized_keys == frozenset(welt.genesis_obj[1])
    assert state.policy_findings == ()
    assert state.key_findings == ()
    assert state.epoch_findings == dedupe_sort(
        [
            Finding(
                GovernanceFinding.PARTICIPANTS_UNDECLARED,
                welt.verfassungs_hashes[1],
            ),
        ]
    )
