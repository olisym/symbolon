"""SE-1 … SE-12 — Tilgung (03-golden-anchors.md §8)."""

from __future__ import annotations

from symbolon.atom import claim_id, is_equivocation_pair
from symbolon.profiles import (
    Finding,
    ProfileFinding,
    SettlementState,
    resolve_policy,
    settlement,
)
from tests.helpers import store_with

from .fixtures import (
    CONSTITUTION_A,
    CONSTITUTION_B,
    CONSTITUTION_HASH_A,
    CONSTITUTION_HASH_B,
    GENESIS_A,
    GENESIS_B,
    N_A,
    N_B,
    NOW,
    fresh_alice,
    fresh_bob,
    nuc,
)


def _policy_a():
    return resolve_policy(
        scope=N_A,
        genesis_obj=GENESIS_A,
        constitution_hash=CONSTITUTION_HASH_A,
        constitution_obj=CONSTITUTION_A,
    ).policy


def _policy_b():
    return resolve_policy(
        scope=N_B,
        genesis_obj=GENESIS_B,
        constitution_hash=CONSTITUTION_HASH_B,
        constitution_obj=CONSTITUTION_B,
    ).policy


def test_SE_1() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    O = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    R = bob.claim(p=nuc(N_A, "receipt"), J=(2, claim_id(O)), t=2, N=N_A)
    result = settlement(
        store_with(O, R), obligation=O, scope=N_A, now=NOW, policy=_policy_a()
    )
    assert result.state == SettlementState.SETTLED
    assert result.receipt_claim_id == claim_id(R)
    assert result.findings == ()


def test_SE_2() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    O = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    result = settlement(
        store_with(O), obligation=O, scope=N_A, now=NOW, policy=_policy_a()
    )
    assert result.state == SettlementState.OPEN
    assert result.receipt_claim_id is None
    assert result.findings == ()


def test_SE_3() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    O = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    R = bob.claim(
        p=nuc(N_A, "receipt"),
        J=(2, claim_id(O)),
        t=2,
        v=bytes.fromhex("a1001906d6"),
        N=N_A,
    )
    result = settlement(
        store_with(O, R), obligation=O, scope=N_A, now=NOW, policy=_policy_a()
    )
    assert result.state == SettlementState.OPEN
    assert result.findings == (
        Finding(ProfileFinding.PARTIAL_RECEIPT_UNSUPPORTED, claim_id(R)),
    )


def test_SE_4() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    O = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    R = alice.claim(p=nuc(N_A, "receipt"), J=(2, claim_id(O)), t=2, N=N_A)
    result = settlement(
        store_with(O, R), obligation=O, scope=N_A, now=NOW, policy=_policy_a()
    )
    assert result.state == SettlementState.OPEN
    assert result.receipt_claim_id is None
    assert result.findings == ()


def test_SE_5() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    O = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    R = bob.claim(p=nuc(N_B, "receipt"), J=(2, claim_id(O)), t=2, N=N_B)
    result = settlement(
        store_with(O, R), obligation=O, scope=N_A, now=NOW, policy=_policy_a()
    )
    assert result.state == SettlementState.OPEN
    assert result.findings == (
        Finding(ProfileFinding.SCOPE_MISMATCH, claim_id(R)),
    )


def test_SE_6() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    X = bob.claim(p=nuc(N_A, "vouch"), J=(1, alice.pub), t=1, N=N_A, t_exp=5000)
    O = alice.claim(p=nuc(N_A, "obligation"), J=(2, claim_id(X)), t=2, N=N_A)
    R = bob.claim(p=nuc(N_A, "receipt"), J=(2, claim_id(O)), t=3, N=N_A)
    result = settlement(
        store_with(X, O, R), obligation=O, scope=N_A, now=NOW, policy=_policy_a()
    )
    assert result.state == SettlementState.OPEN
    assert result.receipt_claim_id is None
    assert result.findings == ()


def test_SE_7() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    O = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    R = bob.claim(p=nuc(N_A, "receipt"), J=(2, claim_id(O)), t=2, N=N_A)
    rev = bob.revoke(R, t=3)
    result = settlement(
        store_with(O, R, rev), obligation=O, scope=N_A, now=NOW, policy=_policy_a()
    )
    assert result.state == SettlementState.OPEN
    assert result.findings == ()


def test_SE_8() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    O = alice.claim(
        p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A, t_exp=500
    )
    result = settlement(
        store_with(O), obligation=O, scope=N_A, now=NOW, policy=_policy_a()
    )
    assert result.state == SettlementState.EXPIRED
    assert result.receipt_claim_id is None
    assert result.findings == (
        Finding(ProfileFinding.EXPIRING_OBLIGATION, claim_id(O)),
    )


def test_SE_9() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    O = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=2, N=N_A)
    result = settlement(
        store_with(O), obligation=O, scope=N_A, now=NOW, policy=_policy_a()
    )
    assert result.state == SettlementState.INDETERMINATE
    assert result.receipt_claim_id is None
    assert result.findings == (
        Finding(ProfileFinding.OBLIGATION_PENDING, claim_id(O)),
    )


def test_SE_10() -> None:
    alice_a, alice_b = fresh_alice(), fresh_alice()
    bob = fresh_bob()
    O = alice_a.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    fork = alice_b.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=2, N=N_A)
    assert is_equivocation_pair(O, fork)
    result = settlement(
        store_with(O, fork), obligation=O, scope=N_A, now=NOW, policy=_policy_a()
    )
    assert result.state == SettlementState.INDETERMINATE
    assert result.receipt_claim_id is None
    assert result.findings == (
        Finding(ProfileFinding.OBLIGATION_AUTHOR_FLAGGED, claim_id(O)),
    )


def test_SE_11() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    O = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    rev = alice.revoke(O, t=2)
    result = settlement(
        store_with(O, rev), obligation=O, scope=N_A, now=NOW, policy=_policy_a()
    )
    assert result.state == SettlementState.OPEN
    assert result.receipt_claim_id is None
    assert result.findings == ()


def test_SE_12() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    O = alice.claim(p=nuc(N_B, "obligation"), J=(1, bob.pub), t=1, N=N_B)
    rev = alice.revoke(O, t=2)
    result = settlement(
        store_with(O, rev), obligation=O, scope=N_B, now=NOW, policy=_policy_b()
    )
    assert result.state == SettlementState.OPEN
    assert result.receipt_claim_id is None
    assert result.findings == ()


def test_SE_13() -> None:
    """Aktive Obligation mit t_exp in der Zukunft → OPEN + EXPIRING_OBLIGATION (03a B2)."""
    alice, bob = fresh_alice(), fresh_bob()
    O = alice.claim(
        p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A, t_exp=5000
    )
    result = settlement(
        store_with(O), obligation=O, scope=N_A, now=NOW, policy=_policy_a()
    )
    assert result.state == SettlementState.OPEN
    assert result.receipt_claim_id is None
    assert result.findings == (
        Finding(ProfileFinding.EXPIRING_OBLIGATION, claim_id(O)),
    )


def test_settlement_obligation_time_regression() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    pred = alice.claim(p=nuc(N_A, "vouch"), J=(1, bob.pub), t=2, N=N_A)
    O = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    result = settlement(
        store_with(pred, O), obligation=O, scope=N_A, now=NOW, policy=_policy_a()
    )
    assert result.state == SettlementState.INDETERMINATE
    assert result.receipt_claim_id is None
    assert result.findings == (
        Finding(ProfileFinding.OBLIGATION_TIME_REGRESSION, claim_id(O)),
    )
