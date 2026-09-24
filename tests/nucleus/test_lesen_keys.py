"""Lesen von Genesis-Schlüsseln und der Rotationsordnung (00 §4, 01 §6, D462)."""

from __future__ import annotations

import hashlib

import pytest

from symbolon import cbor_canon
from symbolon.atom import claim_id
from symbolon.domains import DOM_NUC_GEN
from symbolon.genesis import genesis_scope
from symbolon.governance.chain import resolve_epoch
from symbolon.governance.objects import Epoch, Proposal
from symbolon.governance.tally import decide
from symbolon.index import classify_all
from symbolon.keys import resolve_authorized_keys, resolve_current_key
from symbolon.profiles.policy import resolve_policy
from symbolon.trust.params import resolve_trust_params
from symbolon.verifier import State
from tests.helpers import Identity, scope_id, store_with
from tests.nucleus.test_anchor import _world
from tests.nucleus.test_rotate_key import _ack, _rotate

NOW = 1000


def _uint_genesis() -> dict:
    _scope, genesis, _ch = _world([b"\x11" * 32], {})
    genesis = dict(genesis)
    genesis[9] = {0: 1, 1: 1, 2: 2, 3: 3}
    return genesis


def _schluessel_statt(obj: dict, alt: int, neu: object) -> dict:
    kopie: dict = {}
    for key, value in obj.items():
        if key == alt and type(key) is int:
            kopie[neu] = value
        else:
            kopie[key] = value
    return kopie


def _true_statt_eins(genesis: dict) -> dict:
    return _schluessel_statt(genesis, 1, True)


def _scope_von(genesis: dict) -> bytes:
    return hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis)).digest()


def test_genesis_scope_gleicht_dem_hash() -> None:
    """uint-Genesis: derselbe Hash wie die Domänenformel (00 §4, D462)."""
    genesis = _uint_genesis()
    assert genesis_scope(genesis) == _scope_von(genesis)


def test_true_statt_key_1_ist_kein_genesis() -> None:
    """``True`` statt Key ``1`` ist kein uint (00 §4, D462)."""
    with pytest.raises(ValueError, match="non-uint map key"):
        genesis_scope(_true_statt_eins(_uint_genesis()))


def test_float_statt_key_1_ist_kein_genesis() -> None:
    """``1.0`` statt Key ``1`` ist kein uint (00 §4, D462)."""
    with pytest.raises(ValueError, match="non-uint map key"):
        genesis_scope(_schluessel_statt(_uint_genesis(), 1, 1.0))


def test_negativer_schluessel_ist_kein_genesis() -> None:
    """Zusätzlicher Key ``-1`` ist kein uint (00 §4, D462)."""
    genesis = _uint_genesis()
    genesis[-1] = genesis[0]
    with pytest.raises(ValueError, match="non-uint map key"):
        genesis_scope(genesis)


def test_bool_in_trust_params_ist_kein_genesis() -> None:
    """In Key ``9`` ``False`` statt ``0`` und ``True`` statt ``1`` (00 §4, D462)."""
    genesis = _uint_genesis()
    genesis[9] = _schluessel_statt(genesis[9], 0, False)
    genesis[9] = _schluessel_statt(genesis[9], 1, True)
    with pytest.raises(ValueError, match="non-uint map key"):
        genesis_scope(genesis)


def test_resolve_authorized_keys_weist_true_key_ab() -> None:
    """``resolve_authorized_keys`` liest kein Genesis mit ``True`` statt Key ``1`` (00 §4, D462)."""
    variante = _true_statt_eins(_uint_genesis())
    with pytest.raises(ValueError, match="non-uint map key"):
        resolve_authorized_keys(
            store_with(),
            scope=_scope_von(variante),
            genesis_obj=variante,
            constitution_hash=variante[4],
            now=NOW,
        )


def test_resolve_epoch_weist_true_key_ab() -> None:
    """``resolve_epoch`` liest kein Genesis mit ``True`` statt Key ``1`` (00 §4, D462)."""
    variante = _true_statt_eins(_uint_genesis())
    with pytest.raises(ValueError, match="non-uint map key"):
        resolve_epoch(
            store_with(),
            scope=_scope_von(variante),
            genesis_obj=variante,
            known_constitutions={},
            known_proposals={},
            now=NOW,
        )


def test_decide_weist_true_key_ab() -> None:
    """``decide`` liest kein Genesis mit ``True`` statt Key ``1`` (00 §4, D462)."""
    variante = _true_statt_eins(_uint_genesis())
    scope = _scope_von(variante)
    epoch = Epoch(scope=scope, index=1, constitution_hash=variante[4])
    proposal = Proposal(
        scope=scope,
        predecessor=epoch.epoch_id,
        constitution_hash=variante[4],
    )
    with pytest.raises(ValueError, match="non-uint map key"):
        decide(
            store_with(),
            epoch=epoch,
            proposal=proposal,
            genesis_obj=variante,
            constitution_obj=None,
            target_constitution_obj=None,
            known_proposals={},
            now=NOW,
        )


def test_resolve_policy_weist_true_key_ab() -> None:
    """``resolve_policy`` liest kein Genesis mit ``True`` statt Key ``1`` (00 §4, D462)."""
    variante = _true_statt_eins(_uint_genesis())
    with pytest.raises(ValueError, match="non-uint map key"):
        resolve_policy(
            scope=_scope_von(variante),
            genesis_obj=variante,
            constitution_hash=variante[4],
        )


def test_resolve_trust_params_weist_true_key_ab() -> None:
    """``resolve_trust_params`` liest kein Genesis mit ``True`` statt Key ``1`` (00 §4, D462)."""
    variante = _true_statt_eins(_uint_genesis())
    with pytest.raises(ValueError, match="non-uint map key"):
        resolve_trust_params(scope=_scope_von(variante), genesis_obj=variante)


def _nuc(scope: bytes, name: str) -> str:
    return f"nuc:{scope.hex()}/{name}@1"


def _kette(mit_x: bool):
    scope = scope_id("o86-kette")
    root = Identity("o86-root")
    a = Identity("o86-a")
    b = Identity("o86-b")
    dritte = Identity("o86-dritte")
    fremd = dritte.claim(
        p=_nuc(scope, "obligation"),
        J=(1, dritte.pub),
        t=1,
        N=scope,
    )
    r1 = _rotate(root, a, scope, t=1)
    x = root.revoke(fremd, t=2) if mit_x else None
    p = root.claim(
        p=_nuc(scope, "obligation"),
        J=(1, root.pub),
        t=3 if mit_x else 2,
        N=scope,
    )
    r2 = _rotate(root, b, scope, t=4 if mit_x else 3)
    ack1 = _ack(a, r1, scope, t=2)
    ack2 = _ack(b, r2, scope, t=2)
    claims = [fremd, r1, p, r2, ack1, ack2]
    if x is not None:
        claims.insert(2, x)
    return scope, root, a, r1, x, r2, store_with(*claims)


def test_ungueltiges_glied_liefert_keinen_kopf() -> None:
    """Widerruf auf fremden Claim trennt die Rotationen; die Wurzel hat keinen Kopf (01 §6, 00 §6.4, D462)."""
    scope, root, _a, r1, x, r2, store = _kette(True)
    assert x is not None
    by_cid = classify_all(store, NOW)
    assert claim_id(x) not in by_cid
    assert by_cid[claim_id(r1)].state is State.ACTIVE
    assert by_cid[claim_id(r2)].state is State.ACTIVE
    assert resolve_current_key(
        store,
        scope=scope,
        anchor_keys=frozenset({root.pub}),
        now=NOW,
    ) == frozenset()


def test_ohne_ungueltiges_glied_folgt_die_fruehere_rotation() -> None:
    """Dieselbe Welt ohne den Widerruf: Kopf ist der Nachfolger der früheren Rotation (00 §6.4, D462)."""
    scope, root, a, _r1, x, _r2, store = _kette(False)
    assert x is None
    assert resolve_current_key(
        store,
        scope=scope,
        anchor_keys=frozenset({root.pub}),
        now=NOW,
    ) == frozenset({a.pub})
