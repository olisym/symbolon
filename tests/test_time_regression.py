"""time-regression-flagged (01 §6, 01 §B.1, D353, D356)."""

from __future__ import annotations

import json
from pathlib import Path

from symbolon.atom import claim_from_bytes, claim_id, is_equivocation_pair
from symbolon.index import classify_all
from symbolon.trust.groups import BUDGET_STATES
from symbolon.verifier import InMemoryStore, State, classify

from tests.helpers import Identity, scope_id, store_with

VECTORS = json.loads(
    (Path(__file__).resolve().parent / "vectors" / "vectors_01.json").read_text()
)


def _vec(name: str) -> dict:
    for v in VECTORS["vectors"]:
        if v["name"] == name:
            return v
    raise KeyError(name)


def _claim(name: str):
    return claim_from_bytes(bytes.fromhex(_vec(name)["signed_bytes"]))


def test_nv32_classify_time_regression_flagged() -> None:
    store = InMemoryStore()
    store.add(_claim("TV6"))
    nv32 = _claim("NV32")
    store.add(nv32)
    result = classify(nv32, store, now=1_700_000_000)
    assert result.state == State.TIME_REGRESSION_FLAGGED
    assert result.trust_usable is False


def test_nv32_classify_all_time_regression_flagged() -> None:
    store = InMemoryStore()
    store.add(_claim("TV6"))
    nv32 = _claim("NV32")
    store.add(nv32)
    result = classify_all(store, 1_700_000_000)[claim_id(nv32)]
    assert result.state == State.TIME_REGRESSION_FLAGGED
    assert result.trust_usable is False


def test_nv32_full_vector_store_time_regression_tv2_active() -> None:
    store = InMemoryStore()
    for v in VECTORS["vectors"]:
        if "signed_bytes" not in v:
            continue
        store.add(claim_from_bytes(bytes.fromhex(v["signed_bytes"])))
    now = 1_700_000_000
    nv32 = _claim("NV32")
    tv2 = _claim("TV2")
    results = classify_all(store, now)
    assert results[claim_id(nv32)].state == State.TIME_REGRESSION_FLAGGED
    assert results[claim_id(tv2)].state == State.ACTIVE
    assert classify(nv32, store, now).state == State.TIME_REGRESSION_FLAGGED
    assert classify(tv2, store, now).state == State.ACTIVE


def test_equal_t_is_active() -> None:
    scope = scope_id("tr-equal-t")
    alice, bob = Identity("tr-equal-t"), Identity("tr-equal-t-bob")
    pred = alice.vouch(bob, n=1, scope=scope, t=100)
    same = alice.vouch(bob, n=1, scope=scope, t=100)
    result = classify(same, store_with(pred, same), now=100)
    assert result.state == State.ACTIVE


def test_genesis_is_not_time_regression_checked() -> None:
    tv1 = _claim("TV1")
    result = classify(tv1, store_with(tv1), now=1_700_000_000)
    assert result.state == State.ACTIVE


def test_unknown_predecessor_remains_pending() -> None:
    nv32 = _claim("NV32")
    result = classify(nv32, store_with(nv32), now=1_700_000_000)
    assert result.state == State.PENDING


def test_core_revoke_with_smaller_t_is_time_regression_flagged() -> None:
    scope = scope_id("tr-core")
    alice, bob = Identity("tr-core"), Identity("tr-core-bob")
    pred = alice.vouch(bob, n=1, scope=scope, t=100)
    rev = alice.revoke(pred, t=99)
    result = classify(rev, store_with(pred, rev), now=100)
    assert result.state == State.TIME_REGRESSION_FLAGGED
    assert result.trust_usable is False


def test_equivocation_precedes_time_regression() -> None:
    scope = scope_id("tr-eq-prec")
    alice_a = Identity("tr-eq-prec-alice")
    alice_b = Identity("tr-eq-prec-alice")
    bob = Identity("tr-eq-prec-bob")
    pred_a = alice_a.vouch(bob, n=1, scope=scope, t=100)
    pred_b = alice_b.vouch(bob, n=1, scope=scope, t=100)
    assert claim_id(pred_a) == claim_id(pred_b)
    backdated = alice_a.vouch(bob, n=1, scope=scope, t=50)
    fork = alice_b.vouch(bob, n=2, scope=scope, t=150)
    assert is_equivocation_pair(backdated, fork)
    result = classify(backdated, store_with(pred_a, backdated, fork), now=200)
    assert result.state == State.EQUIVOCATION_FLAGGED


def test_time_regression_precedes_revoked() -> None:
    scope = scope_id("tr-rev-prec")
    alice, bob = Identity("tr-rev-prec"), Identity("tr-rev-prec-bob")
    pred = alice.vouch(bob, n=1, scope=scope, t=100)
    backdated = alice.vouch(bob, n=1, scope=scope, t=50)
    rev = alice.revoke(backdated, t=200)
    result = classify(backdated, store_with(pred, backdated, rev), now=200)
    assert result.state == State.TIME_REGRESSION_FLAGGED


def test_budget_states_excludes_linked_and_expired() -> None:
    # D135, D356: jeder neue Zustand muss ins Budget-Set oder ausdrücklich raus.
    assert BUDGET_STATES == set(State) - {State.LINKED, State.EXPIRED}
