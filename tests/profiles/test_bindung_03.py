"""Bindungen aus 03: Quittung, Zustimmung, uint (D458)."""

from __future__ import annotations

from symbolon import cbor_canon
from symbolon.atom import claim_id
from symbolon.profiles import (
    Finding,
    MembershipState,
    ProfileFinding,
    SettlementState,
    membership,
    resolve_policy,
    settlement,
)
from tests.helpers import store_with

from .fixtures import (
    CONSTITUTION_A,
    CONSTITUTION_HASH_A,
    GENESIS_A,
    N_A,
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
