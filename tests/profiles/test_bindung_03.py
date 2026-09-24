"""Bindungen aus 03: Quittung, Zustimmung, uint (D458)."""

from __future__ import annotations

import pytest

from symbolon import cbor_canon
from symbolon.atom import claim_id
from symbolon.policy import NucleusPolicy
from symbolon.profiles import (
    Finding,
    MembershipState,
    ProfileFinding,
    SettlementState,
    VerdictStatus,
    membership,
    resolve_policy,
    settlement,
    verdict_status,
)
from tests.helpers import store_with

from .fixtures import (
    CONSTITUTION_A,
    CONSTITUTION_HASH_A,
    GENESIS_A,
    N_A,
    N_B,
    NOW,
    fresh_alice,
    fresh_bob,
    fresh_carol,
    nuc,
)


def _policy():
    return resolve_policy(
        scope=N_A,
        genesis_obj=GENESIS_A,
        constitution_hash=CONSTITUTION_HASH_A,
        constitution_obj=CONSTITUTION_A,
    ).policy


def test_quittung_gilt_nur_fuer_die_genannte_obligation() -> None:
    """Quittung auf die erste Obligation lässt die zweite offen (03 §3.3.2, D458, C6)."""
    alice, bob = fresh_alice(), fresh_bob()
    erste = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    zweite = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=2, N=N_A)
    quittung = bob.claim(
        p=nuc(N_A, "receipt"), J=(2, claim_id(erste)), t=3, N=N_A
    )
    ergebnis = settlement(
        store_with(erste, zweite, quittung),
        obligation=zweite,
        scope=N_A,
        now=NOW,
        policy=_policy(),
    )
    assert ergebnis.state == SettlementState.OPEN
    assert ergebnis.receipt_claim_id is None


def test_fremde_annahme_ist_kein_einverstaendnis() -> None:
    """accept-rules eines anderen lässt das Subjekt bei GRANT_ONLY (03 §4, D458, M3)."""
    alice, bob, carol = fresh_alice(), fresh_bob(), fresh_carol()
    fremd = carol.claim(
        p=nuc(N_A, "accept-rules"), J=(3, CONSTITUTION_HASH_A), t=1, N=N_A
    )
    grant = alice.claim(
        p=nuc(N_A, "grant-membership"), J=(1, bob.pub), t=2, N=N_A
    )
    ergebnis = membership(
        store_with(fremd, grant),
        subject=bob.pub,
        scope=N_A,
        constitution_hash=CONSTITUTION_HASH_A,
        now=NOW,
        authorized_keys=frozenset({alice.pub}),
    )
    assert ergebnis.state == MembershipState.GRANT_ONLY
    assert ergebnis.accept_claim_id is None
    assert ergebnis.grant_claim_id == claim_id(grant)


def test_bool_ist_kein_uint_der_quittung() -> None:
    """receipt.v Key 0 als bool (03 §1.3, D458, C18)."""
    alice, bob = fresh_alice(), fresh_bob()
    obligation = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    receipt = bob.claim(
        p=nuc(N_A, "receipt"),
        J=(2, claim_id(obligation)),
        t=2,
        v=cbor_canon.encode({0: True}),
        N=N_A,
    )
    ergebnis = settlement(
        store_with(obligation, receipt),
        obligation=obligation,
        scope=N_A,
        now=NOW,
        policy=_policy(),
    )
    assert Finding(ProfileFinding.PARTIAL_RECEIPT_UNSUPPORTED, claim_id(receipt)) in ergebnis.findings
    assert Finding(ProfileFinding.INVALID_V_TYPE, claim_id(receipt)) in ergebnis.findings


def test_negativer_betrag_ist_kein_uint() -> None:
    """obligation.v und receipt.v mit {0: -5} (03 §1.3, D458, Beschluss 1)."""
    alice, bob = fresh_alice(), fresh_bob()
    betrag = cbor_canon.encode({0: -5})
    obligation = alice.claim(
        p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, v=betrag, N=N_A
    )
    ohne_quittung = settlement(
        store_with(obligation),
        obligation=obligation,
        scope=N_A,
        now=NOW,
        policy=_policy(),
    )
    assert Finding(ProfileFinding.INVALID_V_TYPE, claim_id(obligation)) in ohne_quittung.findings

    alice, bob = fresh_alice(), fresh_bob()
    schuld = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    quittung = bob.claim(
        p=nuc(N_A, "receipt"),
        J=(2, claim_id(schuld)),
        t=2,
        v=betrag,
        N=N_A,
    )
    mit_quittung = settlement(
        store_with(schuld, quittung),
        obligation=schuld,
        scope=N_A,
        now=NOW,
        policy=_policy(),
    )
    assert Finding(ProfileFinding.INVALID_V_TYPE, claim_id(quittung)) in mit_quittung.findings


def _in_beiden_reihenfolgen(fest: tuple, a, b, pruefen) -> None:
    pruefen(store_with(*fest, a, b))
    pruefen(store_with(*fest, b, a))


def test_obligation_aus_fremdem_scope() -> None:
    """Obligation eines anderen Scopes wirft (03 §3.3.2, D458, C1)."""
    alice, bob = fresh_alice(), fresh_bob()
    fremd = alice.claim(p=nuc(N_B, "obligation"), J=(1, bob.pub), t=1, N=N_B)
    with pytest.raises(ValueError):
        settlement(
            store_with(fremd),
            obligation=fremd,
            scope=N_A,
            now=NOW,
            policy=_policy(),
        )


def test_policy_aus_fremdem_scope() -> None:
    """Policy eines anderen Scopes wirft (03 §3.3.2, D458, C2)."""
    alice, bob = fresh_alice(), fresh_bob()
    obligation = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    with pytest.raises(ValueError):
        settlement(
            store_with(obligation),
            obligation=obligation,
            scope=N_A,
            now=NOW,
            policy=NucleusPolicy(scope=N_B),
        )


def test_obligation_j_traegt_kein_identity() -> None:
    """J mit Tag claim-ref, Quittung ohne v bleibt offen (03 §3.3.1, D458, C9)."""
    alice, bob = fresh_alice(), fresh_bob()
    obligation = alice.claim(p=nuc(N_A, "obligation"), J=(2, bob.pub), t=1, N=N_A)
    quittung = bob.claim(
        p=nuc(N_A, "receipt"), J=(2, claim_id(obligation)), t=1, N=N_A
    )
    ergebnis = settlement(
        store_with(obligation, quittung),
        obligation=obligation,
        scope=N_A,
        now=NOW,
        policy=_policy(),
    )
    assert ergebnis.state is SettlementState.OPEN
    assert ergebnis.receipt_claim_id is None


def test_teilquittungen_benennen_die_kleinere() -> None:
    """Zwei Quittungen mit Betrag, beide Ordnungen (03 §3.3.2, 01 §4.1, D458, C12, C13)."""
    alice, bob = fresh_alice(), fresh_bob()
    obligation = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    betrag = cbor_canon.encode({0: 5})
    erste = bob.claim(
        p=nuc(N_A, "receipt"),
        J=(2, claim_id(obligation)),
        t=2,
        v=betrag,
        N=N_A,
    )
    zweite = bob.claim(
        p=nuc(N_A, "receipt"),
        J=(2, claim_id(obligation)),
        t=3,
        v=betrag,
        N=N_A,
    )
    kleiner = min(claim_id(erste), claim_id(zweite))

    def pruefen(store) -> None:
        ergebnis = settlement(
            store, obligation=obligation, scope=N_A, now=NOW, policy=_policy()
        )
        assert ergebnis.state is SettlementState.OPEN
        assert ergebnis.receipt_claim_id == kleiner

    _in_beiden_reihenfolgen((obligation,), erste, zweite, pruefen)


def test_vollquittungen_benennen_die_kleinere() -> None:
    """Zwei Quittungen ohne v, beide Ordnungen (03 §3.3.2, D458, C14)."""
    alice, bob = fresh_alice(), fresh_bob()
    obligation = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    erste = bob.claim(
        p=nuc(N_A, "receipt"), J=(2, claim_id(obligation)), t=2, N=N_A
    )
    zweite = bob.claim(
        p=nuc(N_A, "receipt"), J=(2, claim_id(obligation)), t=3, N=N_A
    )
    kleiner = min(claim_id(erste), claim_id(zweite))

    def pruefen(store) -> None:
        ergebnis = settlement(
            store, obligation=obligation, scope=N_A, now=NOW, policy=_policy()
        )
        assert ergebnis.state is SettlementState.SETTLED
        assert ergebnis.receipt_claim_id == kleiner

    _in_beiden_reihenfolgen((obligation,), erste, zweite, pruefen)


def test_nicht_kanonisches_v_der_obligation() -> None:
    """Nicht kanonisches v der Obligation (03 §1.3, D458, C22)."""
    alice, bob = fresh_alice(), fresh_bob()
    obligation = alice.claim(
        p=nuc(N_A, "obligation"),
        J=(1, bob.pub),
        t=1,
        v=bytes.fromhex("a1001801"),
        N=N_A,
    )
    ergebnis = settlement(
        store_with(obligation),
        obligation=obligation,
        scope=N_A,
        now=NOW,
        policy=_policy(),
    )
    assert (
        Finding(ProfileFinding.NON_CANONICAL_V, claim_id(obligation))
        in ergebnis.findings
    )


def test_leeres_v_benennt_die_kleinere_quittung() -> None:
    """Zwei Quittungen mit leerem v, beide Ordnungen (03 §3.3.2, D458, C23)."""
    alice, bob = fresh_alice(), fresh_bob()
    obligation = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    leer = cbor_canon.encode({})
    erste = bob.claim(
        p=nuc(N_A, "receipt"),
        J=(2, claim_id(obligation)),
        t=2,
        v=leer,
        N=N_A,
    )
    zweite = bob.claim(
        p=nuc(N_A, "receipt"),
        J=(2, claim_id(obligation)),
        t=3,
        v=leer,
        N=N_A,
    )
    kleiner = min(claim_id(erste), claim_id(zweite))

    def pruefen(store) -> None:
        ergebnis = settlement(
            store, obligation=obligation, scope=N_A, now=NOW, policy=_policy()
        )
        assert ergebnis.state is SettlementState.SETTLED
        assert ergebnis.receipt_claim_id == kleiner

    _in_beiden_reihenfolgen((obligation,), erste, zweite, pruefen)


def test_verdikt_policy_aus_fremdem_scope() -> None:
    """Policy eines anderen Scopes wirft (03 §2.4.2, D458, V2)."""
    alice, bob = fresh_alice(), fresh_bob()
    anklage = alice.claim(p=nuc(N_A, "accusation"), J=(1, bob.pub), t=1, N=N_A)
    verdikt = fresh_carol().claim(
        p=nuc(N_A, "verdict"), J=(2, claim_id(anklage)), t=1, N=N_A
    )
    with pytest.raises(ValueError):
        verdict_status(
            store_with(anklage, verdikt),
            verdict=verdikt,
            scope=N_A,
            arbitrators=frozenset(),
            now=NOW,
            policy=NucleusPolicy(scope=N_B),
        )


def test_beschuldigter_ist_der_autor_des_claims() -> None:
    """Nur der Ankläger unterworfen, Beschuldigter ist der Autor (03 §2.4.4, D458, V10)."""
    anklaeger, schiedsrichter, autor = fresh_alice(), fresh_bob(), fresh_carol()
    bestritten = autor.claim(p=nuc(N_A, "obligation"), J=(1, anklaeger.pub), t=1, N=N_A)
    anklage = anklaeger.claim(
        p=nuc(N_A, "accusation"), J=(2, claim_id(bestritten)), t=1, N=N_A
    )
    unterwerfung = anklaeger.claim(
        p=nuc(N_A, "submit-arbitration"), J=(1, schiedsrichter.pub), t=2, N=N_A
    )
    verdikt = schiedsrichter.claim(
        p=nuc(N_A, "verdict"), J=(2, claim_id(anklage)), t=1, N=N_A
    )
    ergebnis = verdict_status(
        store_with(bestritten, anklage, unterwerfung, verdikt),
        verdict=verdikt,
        scope=N_A,
        arbitrators=frozenset(),
        now=NOW,
        policy=_policy(),
    )
    assert ergebnis.status is VerdictStatus.ATTRIBUTED_OPINION


def test_unterwerfung_ohne_identity_tag() -> None:
    """J mit Tag claim-ref zählt nicht (03 §2.4.2, D458, V15)."""
    partei_a, partei_b, schiedsrichter = fresh_alice(), fresh_bob(), fresh_carol()
    anklage = partei_a.claim(
        p=nuc(N_A, "accusation"), J=(1, partei_b.pub), t=1, N=N_A
    )
    unter_a = partei_a.claim(
        p=nuc(N_A, "submit-arbitration"),
        J=(2, schiedsrichter.pub),
        t=2,
        N=N_A,
    )
    unter_b = partei_b.claim(
        p=nuc(N_A, "submit-arbitration"),
        J=(2, schiedsrichter.pub),
        t=1,
        N=N_A,
    )
    verdikt = schiedsrichter.claim(
        p=nuc(N_A, "verdict"), J=(2, claim_id(anklage)), t=1, N=N_A
    )
    ergebnis = verdict_status(
        store_with(anklage, unter_a, unter_b, verdikt),
        verdict=verdikt,
        scope=N_A,
        arbitrators=frozenset(),
        now=NOW,
        policy=_policy(),
    )
    assert ergebnis.status is VerdictStatus.ATTRIBUTED_OPINION


def test_annahme_mit_identity_tag_ohne_versionsvermerk() -> None:
    """accept-rules mit Tag identity erzeugt keinen Versionsvermerk (03 §4, D458, M5)."""
    bob = fresh_bob()
    annahme = bob.claim(
        p=nuc(N_A, "accept-rules"), J=(1, bob.pub), t=1, N=N_A
    )
    ergebnis = membership(
        store_with(annahme),
        subject=bob.pub,
        scope=N_A,
        constitution_hash=CONSTITUTION_HASH_A,
        now=NOW,
        authorized_keys=frozenset(),
    )
    assert ProfileFinding.CONSTITUTION_VERSION_MISMATCH not in {
        fund.kind for fund in ergebnis.findings
    }


def test_grant_ohne_identity_tag_zaehlt_nicht() -> None:
    """grant-membership mit Tag claim-ref zählt nicht (03 §4, D458, M7)."""
    alice, bob = fresh_alice(), fresh_bob()
    grant = alice.claim(
        p=nuc(N_A, "grant-membership"), J=(2, bob.pub), t=1, N=N_A
    )
    ergebnis = membership(
        store_with(grant),
        subject=bob.pub,
        scope=N_A,
        constitution_hash=CONSTITUTION_HASH_A,
        now=NOW,
        authorized_keys=frozenset({alice.pub}),
    )
    assert ergebnis.grant_claim_id is None
    assert ergebnis.state is MembershipState.NONE


def test_zwei_annahmen_benennen_die_kleinere() -> None:
    """Zwei aktive accept-rules, beide Ordnungen (03 §4, D458, M11)."""
    bob = fresh_bob()
    erste = bob.claim(
        p=nuc(N_A, "accept-rules"), J=(3, CONSTITUTION_HASH_A), t=1, N=N_A
    )
    zweite = bob.claim(
        p=nuc(N_A, "accept-rules"), J=(3, CONSTITUTION_HASH_A), t=2, N=N_A
    )
    kleiner = min(claim_id(erste), claim_id(zweite))

    def pruefen(store) -> None:
        ergebnis = membership(
            store,
            subject=bob.pub,
            scope=N_A,
            constitution_hash=CONSTITUTION_HASH_A,
            now=NOW,
            authorized_keys=frozenset(),
        )
        assert ergebnis.accept_claim_id == kleiner

    _in_beiden_reihenfolgen((), erste, zweite, pruefen)


def test_zwei_grants_benennen_die_kleinere() -> None:
    """Zwei aktive grant-membership, beide Ordnungen (03 §4, D458, M12)."""
    alice, bob = fresh_alice(), fresh_bob()
    erste = alice.claim(
        p=nuc(N_A, "grant-membership"), J=(1, bob.pub), t=1, N=N_A
    )
    zweite = alice.claim(
        p=nuc(N_A, "grant-membership"), J=(1, bob.pub), t=2, N=N_A
    )
    kleiner = min(claim_id(erste), claim_id(zweite))

    def pruefen(store) -> None:
        ergebnis = membership(
            store,
            subject=bob.pub,
            scope=N_A,
            constitution_hash=CONSTITUTION_HASH_A,
            now=NOW,
            authorized_keys=frozenset({alice.pub}),
        )
        assert ergebnis.grant_claim_id == kleiner

    _in_beiden_reihenfolgen((), erste, zweite, pruefen)
