"""Bindungen aus 04: Ratifizierung, Grenze, fremder Scope (D458)."""

from __future__ import annotations

import hashlib
from dataclasses import replace

import pytest

from symbolon import cbor_canon
from symbolon.atom import claim_id
from symbolon.domains import DOM_NUC_GEN
from symbolon.governance import (
    Epoch,
    Finding,
    GovernanceFinding,
    Proposal,
    TallyState,
    resolve_epoch,
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
    CONSTITUTION_HASH_1,
    EPOCH_1,
    EPOCH_2,
    GENESIS_D,
    N_D,
    NOW,
    P1,
    PROPOSAL_1,
    PROPOSAL_2,
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


def _fremder_scope() -> bytes:
    genesis = dict(GENESIS_D)
    genesis[7] = 1
    scope = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis)).digest()
    assert scope != N_D
    return scope


def _tragend():
    _n, _num, _den, ja = _ja_schwelle(C1, C2)
    leute = _mitglieder()
    stimmen = [vote(person, PROPOSAL_1, choice=1, t=1) for person in leute[:ja]]
    zeugen = [claim_id(stimme) for stimme in stimmen]
    return leute, ja, stimmen, zeugen


def _pruefe(store, ratify, tally, **kwargs):
    return verify_ratification(
        store,
        ratify=ratify,
        epoch=kwargs.get("epoch", EPOCH_1),
        proposal=kwargs.get("proposal", PROPOSAL_1),
        tally=tally,
        target_constitution_obj=kwargs.get("target", C2),
        now=NOW,
        policy=policy_of(C1),
    )


def test_schwelle_null_ist_formwidrig() -> None:
    """Schwelle [0, 0] der angewandten Klasse (04 §3.5, D458, T5)."""
    klasse = threshold_class(C1, C2, GENESIS_D)

    def mit(quelle: dict) -> dict:
        schwellen = {name: list(werte) for name, werte in quelle["thresholds"].items()}
        schwellen[klasse] = [0, 0]
        return {**quelle, "thresholds": schwellen}

    alt, neu = mit(C1), mit(C2)
    epoche = Epoch(scope=N_D, index=1, constitution_hash=constitution_hash(alt))
    vorschlag = Proposal(
        scope=N_D,
        predecessor=epoche.epoch_id,
        constitution_hash=constitution_hash(neu),
    )
    ergebnis = _tally(
        store_with(),
        epoch=epoche,
        proposal=vorschlag,
        constitution=alt,
        target=neu,
    )
    assert ergebnis.state is TallyState.UNEVALUABLE
    assert Finding(GovernanceFinding.MALFORMED_THRESHOLD, epoche.constitution_hash) in ergebnis.findings


def test_schwelle_aus_bool_ist_formwidrig() -> None:
    """Schwelle [True, True] der angewandten Klasse (04 §3.5, D112, D458, T8)."""
    klasse = threshold_class(C1, C2, GENESIS_D)

    def mit(quelle: dict) -> dict:
        schwellen = {name: list(werte) for name, werte in quelle["thresholds"].items()}
        schwellen[klasse] = [True, True]
        return {**quelle, "thresholds": schwellen}

    alt, neu = mit(C1), mit(C2)
    epoche = Epoch(scope=N_D, index=1, constitution_hash=constitution_hash(alt))
    vorschlag = Proposal(
        scope=N_D,
        predecessor=epoche.epoch_id,
        constitution_hash=constitution_hash(neu),
    )
    ergebnis = _tally(
        store_with(),
        epoch=epoche,
        proposal=vorschlag,
        constitution=alt,
        target=neu,
    )
    assert ergebnis.state is TallyState.UNEVALUABLE
    assert Finding(GovernanceFinding.MALFORMED_THRESHOLD, epoche.constitution_hash) in ergebnis.findings


def test_zielverfassung_hasht_nicht_auf_den_vorschlag() -> None:
    """Zielobjekt hasht nicht auf proposal.constitution_hash (04 §3.5, D458, T19)."""
    assert constitution_hash(C1) != PROPOSAL_1.constitution_hash
    ergebnis = _tally(store_with(), target=C1)
    assert ergebnis.state is TallyState.UNEVALUABLE
    assert (
        Finding(
            GovernanceFinding.PROPOSAL_CONSTITUTION_UNAVAILABLE,
            PROPOSAL_1.constitution_hash,
        )
        in ergebnis.findings
    )


def test_ja_mit_ablauf_auf_anderen_vorschlag_zaehlt_nicht_doppelt() -> None:
    """Ja mit t_exp auf einen anderen Vorschlag setzt nicht aus (04 §3.1, 04 §4.4, D458, T32)."""
    alice = fresh_alice()
    ja = vote(alice, PROPOSAL_1, choice=1, t=1)
    andere = vote(alice, PROPOSAL_AMEND_E1, choice=1, t=2, t_exp=NOW)
    bekannt = {
        PROPOSAL_1.proposal_hash: PROPOSAL_1,
        PROPOSAL_AMEND_E1.proposal_hash: PROPOSAL_AMEND_E1,
    }
    ergebnis = _tally(store_with(ja, andere), known=bekannt)
    assert claim_id(ja) in ergebnis.yes
    assert GovernanceFinding.CONFLICTING_APPROVAL not in {fund.kind for fund in ergebnis.findings}


def test_pending_ja_auf_anderen_vorschlag_setzt_nicht_aus() -> None:
    """Pending-Ja auf einen anderen Vorschlag setzt nicht aus (04 §4.4, D458, T33)."""
    alice = fresh_alice()
    ja = vote(alice, PROPOSAL_1, choice=1, t=1)
    alice.claim(p=nuc(N_D, "vote"), J=(3, PROPOSAL_1.proposal_hash), t=2, N=N_D)
    andere = vote(alice, PROPOSAL_AMEND_E1, choice=1, t=3)
    bekannt = {
        PROPOSAL_1.proposal_hash: PROPOSAL_1,
        PROPOSAL_AMEND_E1.proposal_hash: PROPOSAL_AMEND_E1,
    }
    ergebnis = _tally(store_with(ja, andere), known=bekannt)
    assert claim_id(ja) in ergebnis.yes
    assert GovernanceFinding.CONFLICTING_APPROVAL not in {fund.kind for fund in ergebnis.findings}


def test_ja_als_bool_auf_anderen_vorschlag_setzt_nicht_aus() -> None:
    """v = {0: true} ist kein Ja (04 §2.2, D458, T41)."""
    alice = fresh_alice()
    ja = vote(alice, PROPOSAL_1, choice=1, t=1)
    andere = alice.claim(
        p=nuc(N_D, "vote"),
        J=(3, PROPOSAL_AMEND_E1.proposal_hash),
        t=2,
        N=N_D,
        v=cbor_canon.encode({0: True}),
    )
    bekannt = {
        PROPOSAL_1.proposal_hash: PROPOSAL_1,
        PROPOSAL_AMEND_E1.proposal_hash: PROPOSAL_AMEND_E1,
    }
    ergebnis = _tally(store_with(ja, andere), known=bekannt)
    assert claim_id(ja) in ergebnis.yes
    assert GovernanceFinding.CONFLICTING_APPROVAL not in {fund.kind for fund in ergebnis.findings}


def test_ja_mit_identity_tag_ist_unbekannt() -> None:
    """J mit Tag identity auf einen bekannten Hash (04 §2.2, 04 §4.4, D458, T44)."""
    alice = fresh_alice()
    ja = vote(alice, PROPOSAL_1, choice=1, t=1)
    andere = alice.claim(
        p=nuc(N_D, "vote"),
        J=(1, PROPOSAL_AMEND_E1.proposal_hash),
        t=2,
        N=N_D,
        v=cbor_canon.encode({0: 1}),
    )
    bekannt = {
        PROPOSAL_1.proposal_hash: PROPOSAL_1,
        PROPOSAL_AMEND_E1.proposal_hash: PROPOSAL_AMEND_E1,
    }
    ergebnis = _tally(store_with(ja, andere), known=bekannt)
    assert Finding(GovernanceFinding.UNKNOWN_PROPOSAL, claim_id(andere)) in ergebnis.findings
    assert GovernanceFinding.CONFLICTING_APPROVAL not in {fund.kind for fund in ergebnis.findings}


def test_zwei_ja_derselben_epoche_nennen_beide() -> None:
    """Zwei Ja benennen beide claim_id (04 §4.4, D458, T45)."""
    alice = fresh_alice()
    ja = vote(alice, PROPOSAL_1, choice=1, t=1)
    andere = vote(alice, PROPOSAL_AMEND_E1, choice=1, t=2)
    bekannt = {
        PROPOSAL_1.proposal_hash: PROPOSAL_1,
        PROPOSAL_AMEND_E1.proposal_hash: PROPOSAL_AMEND_E1,
    }
    ergebnis = _tally(store_with(ja, andere), known=bekannt)
    subjekte = {
        fund.subject
        for fund in ergebnis.findings
        if fund.kind is GovernanceFinding.CONFLICTING_APPROVAL
    }
    assert claim_id(ja) in subjekte
    assert claim_id(andere) in subjekte


def test_auszaehlung_fremder_epoche() -> None:
    """tally.epoch_id einer anderen Epoche wirft (04 §4.1, D458, E1)."""
    _leute, _ja, stimmen, zeugen = _tragend()
    alice = _leute[0]
    ratify = _ratify(alice, PROPOSAL_1, zeugen, 10, N_D)
    store = store_with(*stimmen, ratify)
    tally = _tally(store)
    fremd = replace(tally, epoch_id=EPOCH_2.epoch_id)
    assert fremd.epoch_id != EPOCH_1.epoch_id
    with pytest.raises(ValueError):
        _pruefe(store, ratify, fremd)


def test_auszaehlung_fremden_vorschlags() -> None:
    """tally.proposal_hash eines anderen Vorschlags wirft (04 §4.1, D458, E1b)."""
    _leute, _ja, stimmen, zeugen = _tragend()
    alice = _leute[0]
    ratify = _ratify(alice, PROPOSAL_1, zeugen, 10, N_D)
    store = store_with(*stimmen, ratify)
    tally = _tally(store)
    fremd = replace(tally, proposal_hash=PROPOSAL_2.proposal_hash)
    assert fremd.proposal_hash != PROPOSAL_1.proposal_hash
    with pytest.raises(ValueError):
        _pruefe(store, ratify, fremd)


def test_ratify_aus_fremdem_scope_traegt_nicht() -> None:
    """Sonst tragende Ratifizierung mit fremdem N (04 §4.1, D458, E4)."""
    _leute, _ja, stimmen, zeugen = _tragend()
    alice = _leute[0]
    scope = _fremder_scope()
    ratify = _ratify(alice, PROPOSAL_1, zeugen, 10, scope)
    store = store_with(*stimmen, ratify)
    ergebnis = _pruefe(store, ratify, _tally(store))
    assert ergebnis.next_epoch is None


def test_ratify_auf_anderen_vorschlag_traegt_nicht() -> None:
    """Sonst tragende Ratifizierung mit J auf einen anderen Vorschlag (04 §4.1, D458, E4b)."""
    _leute, _ja, stimmen, zeugen = _tragend()
    alice = _leute[0]
    ratify = _ratify(alice, PROPOSAL_2, zeugen, 10, N_D)
    store = store_with(*stimmen, ratify)
    ergebnis = _pruefe(store, ratify, _tally(store))
    assert ergebnis.next_epoch is None


def test_vote_statt_ratify_traegt_nicht() -> None:
    """Prädikat vote@1 trägt nicht (04 §4.1, D458, E5)."""
    leute, ja, stimmen, zeugen = _tragend()
    autor = leute[ja]
    assert autor.pub in P1
    schein = autor.claim(
        p=nuc(N_D, "vote"),
        J=(3, PROPOSAL_1.proposal_hash),
        t=10,
        N=N_D,
        v=cbor_canon.encode({0: zeugen}),
    )
    store = store_with(*stimmen, schein)
    ergebnis = _pruefe(store, schein, _tally(store))
    assert ergebnis.next_epoch is None


def test_pending_ratify_traegt_nicht() -> None:
    """Pending-Ratifizierung trägt nicht (04 §4.1, D458, E8)."""
    leute, ja, stimmen, zeugen = _tragend()
    autor = leute[ja]
    autor.claim(p=nuc(N_D, "vote"), J=(3, PROPOSAL_1.proposal_hash), t=1, N=N_D)
    ratify = _ratify(autor, PROPOSAL_1, zeugen, 10, N_D)
    store = store_with(*stimmen, ratify)
    ergebnis = _pruefe(store, ratify, _tally(store))
    assert ergebnis.next_epoch is None


def test_genesis_hasht_nicht_auf_den_scope() -> None:
    """Genesis, das nicht auf scope hasht, wirft (04 §4.5, D458, H1)."""
    genesis = {key: value for key, value in GENESIS_D.items() if key != 4}
    abweichend = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis)).digest()
    assert abweichend != N_D
    with pytest.raises(ValueError):
        resolve_epoch(
            store_with(),
            scope=N_D,
            genesis_obj=genesis,
            known_constitutions={constitution_hash(C1): C1},
            known_proposals={},
            now=NOW,
        )


def test_ratify_fremden_scopes_nennt_keinen_fehlenden_vorschlag() -> None:
    """Mitglieds-ratify aus fremdem Scope auf unbekannten Hash (04 §4.5, D458, H2)."""
    alice = fresh_alice()
    assert alice.pub in P1
    unbekannt = hashlib.sha256(b"o85-unbekannt-h2").digest()
    scope = _fremder_scope()
    claim = alice.claim(
        p=nuc(scope, "ratify"),
        J=(3, unbekannt),
        t=1,
        N=scope,
        v=cbor_canon.encode({0: []}),
    )
    ergebnis = resolve_epoch(
        store_with(claim),
        scope=N_D,
        genesis_obj=GENESIS_D,
        known_constitutions={CONSTITUTION_HASH_1: C1},
        known_proposals={},
        now=NOW,
    )
    assert GovernanceFinding.EPOCH_PROPOSAL_UNAVAILABLE not in {
        fund.kind for fund in ergebnis.findings
    }


def test_pending_ratify_nennt_keinen_fehlenden_vorschlag() -> None:
    """Pending-ratify auf unbekannten Hash (04 §4.5, D458, H3)."""
    alice = fresh_alice()
    assert alice.pub in P1
    alice.claim(p=nuc(N_D, "ratify"), J=(3, PROPOSAL_1.proposal_hash), t=1, N=N_D)
    unbekannt = hashlib.sha256(b"o85-unbekannt-h3").digest()
    claim = alice.claim(
        p=nuc(N_D, "ratify"),
        J=(3, unbekannt),
        t=2,
        N=N_D,
        v=cbor_canon.encode({0: []}),
    )
    ergebnis = resolve_epoch(
        store_with(claim),
        scope=N_D,
        genesis_obj=GENESIS_D,
        known_constitutions={CONSTITUTION_HASH_1: C1},
        known_proposals={},
        now=NOW,
    )
    assert GovernanceFinding.EPOCH_PROPOSAL_UNAVAILABLE not in {
        fund.kind for fund in ergebnis.findings
    }


def test_vorschlag_unter_fremdem_schluessel_ist_unbekannt() -> None:
    """known_proposals-Objekt hasht nicht auf den Schlüssel (04 §4.5, D175, D458, H11)."""
    alice = fresh_alice()
    assert alice.pub in P1
    schluessel = hashlib.sha256(b"o85-schluessel-h11").digest()
    assert PROPOSAL_2.proposal_hash != schluessel
    claim = alice.claim(
        p=nuc(N_D, "ratify"),
        J=(3, schluessel),
        t=1,
        N=N_D,
        v=cbor_canon.encode({0: []}),
    )
    ergebnis = resolve_epoch(
        store_with(claim),
        scope=N_D,
        genesis_obj=GENESIS_D,
        known_constitutions={CONSTITUTION_HASH_1: C1},
        known_proposals={schluessel: PROPOSAL_2},
        now=NOW,
    )
    assert Finding(GovernanceFinding.EPOCH_PROPOSAL_UNAVAILABLE, schluessel) in ergebnis.findings
