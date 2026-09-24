"""Ratify-Vorbedingung und Zeugenlänge (04 §4.1, 04 §4.5, D456)."""

from __future__ import annotations

from symbolon.atom import claim_id
from symbolon.governance import (
    Finding,
    GovernanceFinding,
    resolve_epoch,
    verify_ratification,
)
from symbolon.governance.tally import TallyState
from tests.helpers import store_with

from .fixtures import (
    C1,
    C2,
    C3,
    CONSTITUTION_HASH_1,
    CONSTITUTION_HASH_2,
    CONSTITUTION_HASH_3,
    EPOCH_1,
    GENESIS_D,
    N_D,
    NOW,
    PROPOSAL_1,
    PROPOSAL_2,
    _tally,
    fresh_alice,
    fresh_frank,
    nuc,
    policy_of,
    ratify_claim,
    vote,
)

_UNBEKANNT = bytes(range(32))


def _resolve(store, *, constitutions: dict | None = None):
    if constitutions is None:
        constitutions = {
            CONSTITUTION_HASH_1: C1,
            CONSTITUTION_HASH_2: C2,
            CONSTITUTION_HASH_3: C3,
        }
    return resolve_epoch(
        store,
        scope=N_D,
        genesis_obj=GENESIS_D,
        known_constitutions=constitutions,
        known_proposals={
            PROPOSAL_1.proposal_hash: PROPOSAL_1,
            PROPOSAL_2.proposal_hash: PROPOSAL_2,
        },
        now=NOW,
    )


def _ratify(identity, t: int):
    return identity.claim(
        p=nuc(N_D, "ratify"),
        J=(3, _UNBEKANNT),
        t=t,
        N=N_D,
    )


def test_tag_1_bekannter_vorschlag() -> None:
    """Tag 1 auf bekannten Vorschlag: UNSUPPORTED_RATIFICATION (04 §4.1, D456)."""
    alice = fresh_alice()
    ratify = alice.claim(
        p=nuc(N_D, "ratify"),
        J=(1, PROPOSAL_1.proposal_hash),
        t=1,
        N=N_D,
    )
    result = _resolve(store_with(ratify))
    assert result.findings == (
        Finding(GovernanceFinding.UNSUPPORTED_RATIFICATION, claim_id(ratify)),
    )


def test_tag_1_unbekannter_vorschlag_ohne_vermerk() -> None:
    """Tag 1 auf unbekannten Vorschlag: kein EPOCH_PROPOSAL_UNAVAILABLE (04 §4.5, D456)."""
    alice = fresh_alice()
    ratify = alice.claim(
        p=nuc(N_D, "ratify"),
        J=(1, _UNBEKANNT),
        t=1,
        N=N_D,
    )
    result = _resolve(store_with(ratify))
    assert GovernanceFinding.EPOCH_PROPOSAL_UNAVAILABLE not in {
        f.kind for f in result.findings
    }


def test_nichtmitglied_ohne_vermerk() -> None:
    """Nichtmitglied auf unbekannten Vorschlag: kein Vermerk (04 §4.5, D456)."""
    frank = fresh_frank()
    result = _resolve(store_with(_ratify(frank, 1)))
    assert GovernanceFinding.EPOCH_PROPOSAL_UNAVAILABLE not in {
        f.kind for f in result.findings
    }


def test_mitglied_mit_vermerk() -> None:
    """Mitglied auf unbekannten Vorschlag: EPOCH_PROPOSAL_UNAVAILABLE (04 §4.5, D456)."""
    alice = fresh_alice()
    result = _resolve(store_with(_ratify(alice, 1)))
    assert result.findings == (
        Finding(GovernanceFinding.EPOCH_PROPOSAL_UNAVAILABLE, _UNBEKANNT),
    )


def test_unbekannte_verfassung_nichtmitglied_mit_vermerk() -> None:
    """Unbekannte Verfassung: auch ein Nichtmitglied trägt den Vermerk (04 §4.5, D456)."""
    frank = fresh_frank()
    result = _resolve(store_with(_ratify(frank, 1)), constitutions={})
    assert result.findings == (
        Finding(GovernanceFinding.EPOCH_PROPOSAL_UNAVAILABLE, _UNBEKANNT),
    )


def test_zeuge_mit_31_byte() -> None:
    """bstr mit 31 Byte ist keine claim_id (04 §4.1, D456)."""
    alice = fresh_alice()
    ja = vote(alice, PROPOSAL_1, choice=1, t=1)
    store = store_with(ja)
    tally = _tally(store)
    ratify = ratify_claim(alice, PROPOSAL_1, witnesses=[b"\x11" * 31], t=2)
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
    assert result.next_epoch is None
    assert result.findings == (
        Finding(GovernanceFinding.UNSUPPORTED_RATIFICATION, claim_id(ratify)),
    )
