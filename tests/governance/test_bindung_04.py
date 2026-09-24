"""Bindungen aus 04: Ratifizierung, Grenze, fremder Scope (D458)."""

from __future__ import annotations

import hashlib

from symbolon import cbor_canon
from symbolon.atom import claim_id
from symbolon.domains import DOM_NUC_GEN
from symbolon.governance import (
    Epoch,
    Finding,
    GovernanceFinding,
    Proposal,
    TallyState,
    verify_ratification,
)
from symbolon.governance.tally import applied_threshold, reached, threshold_class
from symbolon.policy import constitution_hash
from tests.helpers import store_with

from .fixtures import (
    ALICE,
    BOB,
    C1,
    C1_AMEND,
    C2,
    EPOCH_1,
    GENESIS_D,
    N_D,
    NOW,
    P1,
    PROPOSAL_1,
    PROPOSAL_AMEND_E1,
    fresh_alice,
    fresh_bob,
    fresh_carol,
    fresh_dave,
    fresh_frank,
    nuc,
    policy_of,
    vote,
    _tally,
)


def _mitglieder():
    return [fresh_alice(), fresh_bob(), fresh_carol(), fresh_dave()]


def _ja_schwelle(alt: dict, neu: dict) -> tuple[int, int, int, int]:
    klasse = threshold_class(alt, neu, GENESIS_D)
    num, den = applied_threshold(alt, neu, klasse)
    n = len(alt["participants"])
    ja = next(k for k in range(n + 1) if reached(k, n, num, den))
    return n, num, den, ja


def _ratify(identity, proposal, witnesses: list[bytes], t: int, scope: bytes):
    return identity.claim(
        p=nuc(scope, "ratify"),
        J=(3, proposal.proposal_hash),
        t=t,
        N=scope,
        v=cbor_canon.encode({0: witnesses}),
    )


def test_nichtmitglied_ratifiziert_nicht() -> None:
    """Ratifizierung eines Nichtmitglieds trägt nicht (04 §4.1, D458, E6)."""
    _n, _num, _den, ja = _ja_schwelle(C1, C2)
    stimmen = [vote(person, PROPOSAL_1, choice=1, t=1) for person in _mitglieder()[:ja]]
    zeugen = [claim_id(stimme) for stimme in stimmen]
    frank = fresh_frank()
    assert frank.pub not in P1
    ratify = _ratify(frank, PROPOSAL_1, zeugen, 10, N_D)
    store = store_with(*stimmen, ratify)
    tally = _tally(store)
    ergebnis = verify_ratification(
        store,
        ratify=ratify,
        epoch=EPOCH_1,
        proposal=PROPOSAL_1,
        tally=tally,
        target_constitution_obj=C2,
        now=NOW,
        policy=policy_of(C1),
    )
    assert ergebnis.next_epoch is None
    assert Finding(GovernanceFinding.UNSUPPORTED_RATIFICATION, claim_id(ratify)) in ergebnis.findings


def test_doppelt_zitierte_stimme_zaehlt_einmal() -> None:
    """Eine Ja-Stimme zweimal zitiert trägt nicht (04 §4.1, D458, E14)."""
    num, den = C1["thresholds"]["ordinary"]
    n = next(
        k
        for k in range(1, len(P1) + 1)
        if not reached(1, k, num, den) and reached(2, k, num, den)
    )
    teilnehmer = P1[:n]
    paar = [num, den]
    schwellen = {name: list(paar) for name in ("ordinary", "membership", "amendment")}
    alt = {
        "irrevocable_predicates": ["obligation@1", "ratify@1", "vote@1"],
        "thresholds": {name: list(werte) for name, werte in schwellen.items()},
        "arbitration": {"arbitrators": [ALICE.pub]},
        "participants": list(teilnehmer),
    }
    neu = {
        "irrevocable_predicates": ["obligation@1", "ratify@1", "vote@1"],
        "thresholds": {name: list(werte) for name, werte in schwellen.items()},
        "arbitration": {"arbitrators": [BOB.pub]},
        "participants": list(teilnehmer),
    }
    genesis = {
        0: 1,
        1: [ALICE.pub],
        2: 0,
        3: [ALICE.pub],
        4: constitution_hash(alt),
        5: 2,
        6: 0,
        7: 0,
    }
    scope = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis)).digest()
    epoche = Epoch(scope=scope, index=1, constitution_hash=constitution_hash(alt))
    vorschlag = Proposal(
        scope=scope,
        predecessor=epoche.epoch_id,
        constitution_hash=constitution_hash(neu),
    )
    nach_schluessel = {person.pub: person for person in _mitglieder()}
    stimme = vote(nach_schluessel[teilnehmer[0]], vorschlag, choice=1, t=1, scope=scope)
    zeugen = [claim_id(stimme), claim_id(stimme)]
    ratify = _ratify(nach_schluessel[teilnehmer[0]], vorschlag, zeugen, 10, scope)
    store = store_with(stimme, ratify)
    tally = _tally(
        store,
        epoch=epoche,
        proposal=vorschlag,
        constitution=alt,
        target=neu,
        genesis=genesis,
    )
    ergebnis = verify_ratification(
        store,
        ratify=ratify,
        epoch=epoche,
        proposal=vorschlag,
        tally=tally,
        target_constitution_obj=neu,
        now=NOW,
        policy=policy_of(alt, scope),
    )
    assert ergebnis.next_epoch is None
    assert Finding(GovernanceFinding.UNSUPPORTED_RATIFICATION, claim_id(ratify)) in ergebnis.findings


def test_zeugen_map_ist_keine_liste() -> None:
    """v[0] als Map der claim_ids trägt nicht (04 §2.3, D458, E19)."""
    _n, _num, _den, ja = _ja_schwelle(C1, C2)
    leute = _mitglieder()
    stimmen = [vote(person, PROPOSAL_1, choice=1, t=1) for person in leute[:ja]]
    zeugen = {claim_id(stimme): 0 for stimme in stimmen}
    alice = leute[0]
    ratify = alice.claim(
        p=nuc(N_D, "ratify"),
        J=(3, PROPOSAL_1.proposal_hash),
        t=10,
        N=N_D,
        v=cbor_canon.encode({0: zeugen}),
    )
    store = store_with(*stimmen, ratify)
    tally = _tally(store)
    ergebnis = verify_ratification(
        store,
        ratify=ratify,
        epoch=EPOCH_1,
        proposal=PROPOSAL_1,
        tally=tally,
        target_constitution_obj=C2,
        now=NOW,
        policy=policy_of(C1),
    )
    assert ergebnis.next_epoch is None
    assert Finding(GovernanceFinding.UNSUPPORTED_RATIFICATION, claim_id(ratify)) in ergebnis.findings


def test_grenze_der_hoffnungslosigkeit() -> None:
    """Gleichheit in (n - Nein) * den == num * n ist FAILED (04 §3.2, D458, T3)."""
    klasse = threshold_class(C1, C1_AMEND, GENESIS_D)
    num, den = applied_threshold(C1, C1_AMEND, klasse)
    n = len(P1)
    nein = next(k for k in range(n + 1) if (n - k) * den == num * n)
    leute = _mitglieder()

    def auszaehlung(anzahl: int):
        stimmen = [
            vote(leute[i], PROPOSAL_AMEND_E1, choice=0, t=1) for i in range(anzahl)
        ]
        return _tally(
            store_with(*stimmen),
            proposal=PROPOSAL_AMEND_E1,
            target=C1_AMEND,
        )

    assert auszaehlung(nein).state is TallyState.FAILED
    assert auszaehlung(nein - 1).state is TallyState.PENDING


def test_ja_in_fremdem_scope_setzt_nicht_aus() -> None:
    """Ja-Stimme in einem anderen Scope auf Unbekanntes zählt hier (04 §4.4, D458, T31)."""
    alice = fresh_alice()
    ja = vote(alice, PROPOSAL_1, choice=1, t=1)
    fremd = dict(GENESIS_D)
    fremd[7] = 1
    fremder_scope = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(fremd)).digest()
    assert fremder_scope != N_D
    unbekannt = Proposal(
        scope=fremder_scope,
        predecessor=hashlib.sha256(b"o84-vorgaenger").digest(),
        constitution_hash=constitution_hash(C1),
    )
    andere = vote(alice, unbekannt, choice=1, t=2, scope=fremder_scope)
    ergebnis = _tally(store_with(ja, andere))
    assert claim_id(ja) in ergebnis.yes
    assert GovernanceFinding.UNKNOWN_PROPOSAL not in {fund.kind for fund in ergebnis.findings}
