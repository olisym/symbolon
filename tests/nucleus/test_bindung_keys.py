"""Sieben Welten zu den Rotationsbedingungen und Formprüfungen (D464)."""

from __future__ import annotations

import pytest

from symbolon.atom import claim_id
from symbolon.findings import Finding, NucleusFinding
from symbolon.genesis import genesis_scope
from symbolon.index import classify_all
from symbolon.keys import resolve_authorized_keys, resolve_current_key
from symbolon.policy import constitution_hash
from symbolon.verifier import State
from tests.helpers import Identity, scope_id, store_with
from tests.nucleus.test_anchor import _world
from tests.nucleus.test_rotate_key import _ack, _rotate

NOW = 1000


def test_g1_ack_auf_obligation_bleibt_bei_der_wurzel() -> None:
    """G1: Gegenzeichnung eines obligation@1 ist keine Rotation (00 §6.1, D152, D464)."""
    scope = scope_id("g1-binden")
    r = Identity("g1-r")
    a = Identity("g1-a")
    obligation = r.claim(
        p=f"nuc:{scope.hex()}/obligation@1",
        J=(1, a.pub),
        t=1,
        N=scope,
    )
    ack = _ack(a, obligation, scope, t=2)
    store = store_with(obligation, ack)
    classified = classify_all(store, NOW)
    assert classified[claim_id(obligation)].state is State.ACTIVE
    assert classified[claim_id(ack)].state is State.ACTIVE
    assert resolve_current_key(
        store,
        scope=scope,
        anchor_keys=frozenset({r.pub}),
        now=NOW,
    ) == frozenset({r.pub})


def test_g2_pending_rotation_bleibt_bei_der_wurzel() -> None:
    """G2: pending Rotation ohne Vorgänger zählt nicht (00 §6.4, D155, D464)."""
    scope = scope_id("g2-binden")
    r = Identity("g2-r")
    a = Identity("g2-a")
    r.claim(
        p=f"nuc:{scope.hex()}/obligation@1",
        J=(1, a.pub),
        t=1,
        N=scope,
    )
    rotation = _rotate(r, a, scope, t=2)
    ack = _ack(a, rotation, scope, t=3)
    store = store_with(rotation, ack)
    classified = classify_all(store, NOW)
    assert classified[claim_id(rotation)].state is State.PENDING
    assert classified[claim_id(ack)].state is State.ACTIVE
    assert resolve_current_key(
        store,
        scope=scope,
        anchor_keys=frozenset({r.pub}),
        now=NOW,
    ) == frozenset({r.pub})


def test_g3_ack_einer_anderen_rotation_bleibt_bei_der_wurzel() -> None:
    """G3: Gegenzeichnung einer fremden Rotation bindet die eigene nicht (00 §6.1, D152, D464)."""
    scope = scope_id("g3-binden")
    r = Identity("g3-r")
    a = Identity("g3-a")
    j = Identity("g3-j")
    r0 = _rotate(j, a, scope, t=1)
    r1 = _rotate(r, a, scope, t=2)
    ack = _ack(a, r0, scope, t=3)
    store = store_with(r0, r1, ack)
    classified = classify_all(store, NOW)
    assert classified[claim_id(r1)].state is State.ACTIVE
    assert classified[claim_id(ack)].state is State.ACTIVE
    assert resolve_current_key(
        store,
        scope=scope,
        anchor_keys=frozenset({r.pub}),
        now=NOW,
    ) == frozenset({r.pub})


def test_g4_pending_ack_bleibt_bei_der_wurzel() -> None:
    """G4: pending Gegenzeichnung zählt nicht (00 §6.4, D155, D464)."""
    scope = scope_id("g4-binden")
    r = Identity("g4-r")
    a = Identity("g4-a")
    rotation = _rotate(r, a, scope, t=1)
    a.claim(
        p=f"nuc:{scope.hex()}/obligation@1",
        J=(1, r.pub),
        t=2,
        N=scope,
    )
    ack = _ack(a, rotation, scope, t=3)
    store = store_with(rotation, ack)
    classified = classify_all(store, NOW)
    assert classified[claim_id(rotation)].state is State.ACTIVE
    assert classified[claim_id(ack)].state is State.PENDING
    assert resolve_current_key(
        store,
        scope=scope,
        anchor_keys=frozenset({r.pub}),
        now=NOW,
    ) == frozenset({r.pub})


def test_g5_root_keys_keine_liste_wirft_value_error() -> None:
    """G5: genesis[1] keine Liste wirft ValueError mit root_keys (00 §6.4, D464)."""
    r = Identity("g5-r")
    constitution: dict = {}
    _scope, genesis, ch = _world([r.pub], constitution)
    genesis[1] = 5
    scope = genesis_scope(genesis)
    with pytest.raises(ValueError, match="root_keys"):
        resolve_authorized_keys(
            store_with(),
            scope=scope,
            genesis_obj=genesis,
            constitution_hash=ch,
            constitution_obj=constitution,
            now=NOW,
        )


def test_g6_nucleus_keys_als_map_ist_leerer_anker() -> None:
    """G6: nucleus_keys als Map fällt nicht auf root_keys zurück (00 §5.4, D163, D464)."""
    r = Identity("g6-r")
    schluessel = Identity("g6-schluessel")
    constitution = {"nucleus_keys": {schluessel.pub: 0}}
    _scope, genesis, _ch = _world([r.pub], {})
    ch = constitution_hash(constitution)
    genesis[4] = ch
    scope = genesis_scope(genesis)
    result = resolve_authorized_keys(
        store_with(),
        scope=scope,
        genesis_obj=genesis,
        constitution_hash=ch,
        constitution_obj=constitution,
        now=NOW,
    )
    assert result.keys == frozenset()
    assert Finding(NucleusFinding.MALFORMED_NUCLEUS_KEY, ch) in result.findings


def test_g7_nicht_uint_in_der_tiefe_wirft() -> None:
    """G7: nicht-uint Schlüssel in der Tiefe ist kein Genesis (00 §4, D462, D464)."""
    r = Identity("g7-r")
    _scope, genesis, _ch = _world([r.pub], {})
    genesis[3] = [{True: 0}]
    with pytest.raises(ValueError, match="non-uint map key"):
        genesis_scope(genesis)
