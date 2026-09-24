"""Anklage-Prädikat und Quittungsvermerke (03 §2.4.4, 03 §3.3.2, D456)."""

from __future__ import annotations

from symbolon import cbor_canon
from symbolon.atom import claim_id
from symbolon.profiles import (
    Finding,
    ProfileFinding,
    SettlementState,
    VerdictStatus,
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


def test_vouch_ist_keine_anklage() -> None:
    """vouch@1 als verdict.J: UNKNOWN_ACCUSATION, Subjekt das Verdikt (03 §2.4.4, D456)."""
    alice, bob, carol = fresh_alice(), fresh_bob(), fresh_carol()
    vouch = alice.claim(p=nuc(N_B, "vouch"), J=(1, bob.pub), t=1, N=N_B)
    sub_alice = alice.claim(
        p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=2, N=N_B
    )
    sub_bob = bob.claim(
        p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=1, N=N_B
    )
    verdict = carol.claim(
        p=nuc(N_B, "verdict"), J=(2, claim_id(vouch)), t=1, N=N_B
    )
    result = verdict_status(
        store_with(vouch, sub_alice, sub_bob, verdict),
        verdict=verdict,
        scope=N_B,
        arbitrators=frozenset(),
        now=NOW,
    )
    assert result.status == VerdictStatus.ATTRIBUTED_OPINION
    assert result.findings == (
        Finding(ProfileFinding.UNKNOWN_ACCUSATION, claim_id(verdict)),
    )


def _policy():
    return resolve_policy(
        scope=N_A,
        genesis_obj=GENESIS_A,
        constitution_hash=CONSTITUTION_HASH_A,
        constitution_obj=CONSTITUTION_A,
    ).policy


def _paar(t_teil: int):
    alice, bob = fresh_alice(), fresh_bob()
    obligation = alice.claim(
        p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A
    )
    voll = bob.claim(
        p=nuc(N_A, "receipt"), J=(2, claim_id(obligation)), t=2, N=N_A
    )
    teil = bob.claim(
        p=nuc(N_A, "receipt"),
        J=(2, claim_id(obligation)),
        t=t_teil,
        v=cbor_canon.encode({0: 5}),
        N=N_A,
    )
    return obligation, voll, teil


def test_vermerke_beider_quittungen_in_beiden_ordnungen() -> None:
    """Tilgende und Teil-Quittung: Vermerk in beiden claim_id-Ordnungen (03 §3.3.2, D456)."""
    ordnungen: dict[str, tuple] = {}
    t_teil = 3
    while len(ordnungen) < 2:
        obligation, voll, teil = _paar(t_teil)
        schluessel = (
            "teil-zuerst" if claim_id(teil) < claim_id(voll) else "voll-zuerst"
        )
        ordnungen.setdefault(schluessel, (obligation, voll, teil))
        t_teil += 1
        if t_teil > 10000:
            raise AssertionError("beide Ordnungen nicht erreicht")
    assert set(ordnungen) == {"teil-zuerst", "voll-zuerst"}
    pol = _policy()
    for obligation, voll, teil in ordnungen.values():
        result = settlement(
            store_with(obligation, voll, teil),
            obligation=obligation,
            scope=N_A,
            now=NOW,
            policy=pol,
        )
        assert result.state == SettlementState.SETTLED
        assert result.receipt_claim_id == claim_id(voll)
        assert Finding(
            ProfileFinding.PARTIAL_RECEIPT_UNSUPPORTED, claim_id(teil)
        ) in result.findings
