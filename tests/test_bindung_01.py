"""Bindungen aus 01: geschlossenes core, uint-Schlüssel, sechs Lücken (D452)."""

from __future__ import annotations

import hashlib
from dataclasses import replace

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from symbolon.atom import Claim, build_signed, claim_id, id_genesis_anchor, signed_bytes
from symbolon.domains import DOM_ID_GEN
from symbolon.errors import ErrorCode
from symbolon.index import classify_all
from symbolon.policy import NucleusPolicy
from symbolon.verifier import State, classify, read_claim
from tests.helpers import Identity, scope_id, store_with

NOW = 1000
T_EXP = 5000


def _signiert(
    label: str,
    *,
    h_prev: bytes,
    p: str,
    J: tuple[int, bytes],
    t: int,
    N: bytes | None = None,
) -> Claim:
    """Claim mit frei gewähltem h_prev. Seed wie tests.helpers.Identity."""
    seed = hashlib.sha256(b"identity:" + label.encode()).digest()
    sk = Ed25519PrivateKey.from_private_bytes(seed)
    assert sk.public_key().public_bytes_raw() == Identity(label).pub
    return build_signed(sk, J=J, p=p, t=t, h_prev=h_prev, N=N, t_exp=T_EXP)


def _vouch(autor: str, subjekt: str, scope_label: str, h_prev: bytes, t: int) -> Claim:
    scope = scope_id(scope_label)
    return _signiert(
        autor,
        h_prev=h_prev,
        p=f"nuc:{scope.hex()}/vouch@1",
        J=(1, Identity(subjekt).pub),
        t=t,
        N=scope,
    )


@pytest.mark.parametrize("name", ["revoke", "supersede"])
def test_core_at_2_ist_reserviert(name: str) -> None:
    """core/*@2 ist RESERVED_CORE_PREDICATE (01 §2.4 Invariante 4, D452)."""
    a = Identity("o82-a")
    v = a.vouch(Identity("o82-as"), n=1, scope=scope_id("o82-s"), t=1, t_exp=T_EXP)
    lebenszyklus = a.claim(p=f"core/{name}@2", J=(2, claim_id(v)), t=2)
    assert read_claim(signed_bytes(lebenszyklus)) == ErrorCode.RESERVED_CORE_PREDICATE


@pytest.mark.parametrize("name", ["revoke", "supersede"])
def test_core_at_2_wirkt_nicht(name: str) -> None:
    """core/*@2 wirkt nicht als Lebenszyklus (01 §2.2, 01 §6, D452)."""
    a = Identity("o82-a")
    v = a.vouch(Identity("o82-as"), n=1, scope=scope_id("o82-s"), t=1, t_exp=T_EXP)
    lebenszyklus = a.claim(p=f"core/{name}@2", J=(2, claim_id(v)), t=2)
    store = store_with(v, lebenszyklus)
    assert classify(v, store, NOW).state == State.ACTIVE
    assert classify_all(store, NOW)[claim_id(v)].state == State.ACTIVE


@pytest.mark.parametrize(
    ("stelle", "ersatz"),
    [(3, b"\xf5"), (1, b"\xf4")],
)
def test_bool_schluessel_ist_malformed(stelle: int, ersatz: bytes) -> None:
    """Ein bool-Schlüssel ist MALFORMED_CBOR (01 Anhang B.2, D452)."""
    a = Identity("o82-a")
    v = a.vouch(Identity("o82-as"), n=1, scope=scope_id("o82-s"), t=1, t_exp=T_EXP)
    draht = bytearray(signed_bytes(v))
    assert bytes(draht[:6]) == bytes.fromhex("aa0001015820")
    draht[stelle : stelle + 1] = ersatz
    assert read_claim(bytes(draht)) == ErrorCode.MALFORMED_CBOR


def test_genesis_anker_an_identitaet() -> None:
    """Genesis nur mit dem eigenen Anker SHA-256(DOM_ID_GEN ‖ I) (01 §4, D452)."""
    fremd = id_genesis_anchor(Identity("o82-fremd").pub)
    for h_prev in (hashlib.sha256(DOM_ID_GEN).digest(), fremd):
        vouch = _vouch("o82-d", "o82-ds", "o82-sd", h_prev, 1)
        assert isinstance(read_claim(signed_bytes(vouch)), Claim)
        assert classify(vouch, store_with(vouch), NOW).state == State.PENDING


def test_vorgaenger_vom_selben_autor() -> None:
    """Ein Vorgänger eines anderen Autors verlinkt nicht (01 §6, D452)."""
    e = Identity("o82-e")
    pe = e.vouch(Identity("o82-es"), n=1, scope=scope_id("o82-se"), t=1, t_exp=T_EXP)
    fv = _vouch("o82-f", "o82-fs", "o82-sf", claim_id(pe), 1)
    store = store_with(pe, fv)
    assert classify(fv, store, NOW).state == State.PENDING
    assert classify_all(store, NOW)[claim_id(fv)].state == State.PENDING


def test_widerruf_nur_vom_autor() -> None:
    """Nur der eigene Widerruf wirkt (01 §5.1, 01 §6, D452)."""
    a = Identity("o82-a")
    v = a.vouch(Identity("o82-as"), n=1, scope=scope_id("o82-s"), t=1, t_exp=T_EXP)
    fremd = Identity("o82-b").revoke(v, t=1)
    store = store_with(v, fremd)
    assert classify(v, store, NOW).state == State.ACTIVE
    assert classify_all(store, NOW)[claim_id(v)].state == State.ACTIVE


def test_supersede_nur_vom_autor() -> None:
    """Nur das eigene Supersede wirkt (01 §5.1, 01 §6, D452)."""
    a = Identity("o82-a")
    v = a.vouch(Identity("o82-as"), n=1, scope=scope_id("o82-s"), t=1, t_exp=T_EXP)
    fremd = Identity("o82-b").supersede(v, t=1)
    store = store_with(v, fremd)
    assert classify(v, store, NOW).state == State.ACTIVE
    assert classify_all(store, NOW)[claim_id(v)].state == State.ACTIVE


def test_widerruf_nur_strukturell_gueltig() -> None:
    """Nur ein strukturell gültiger Widerruf wirkt (01 §6, D452)."""
    a = Identity("o82-a")
    v = a.vouch(Identity("o82-as"), n=1, scope=scope_id("o82-s"), t=1, t_exp=T_EXP)
    widerruf = replace(a.revoke(v, t=2), sigma=bytes(64))
    assert read_claim(signed_bytes(widerruf)) == ErrorCode.BAD_SIGNATURE
    store = store_with(v, widerruf)
    assert classify(v, store, NOW).state == State.ACTIVE
    assert classify_all(store, NOW)[claim_id(v)].state == State.ACTIVE


def test_policy_nur_im_eigenen_scope() -> None:
    """Die Policy gilt nur im eigenen Scope (01 §5.4, 03 §6, D91, D452)."""
    g = Identity("o82-g")
    s1 = scope_id("o82-s1")
    s2 = scope_id("o82-s2")
    subjekt = Identity("o82-gs").pub
    p1 = g.claim(p=f"nuc:{s1.hex()}/pledge@1", J=(1, subjekt), t=1, N=s1, t_exp=T_EXP)
    r1 = g.revoke(p1, t=2)
    p2 = g.claim(p=f"nuc:{s2.hex()}/pledge@1", J=(1, subjekt), t=3, N=s2, t_exp=T_EXP)
    r2 = g.revoke(p2, t=4)
    store = store_with(p1, r1, p2, r2)
    policy = NucleusPolicy(scope=s1, declared=["pledge@1"])
    klassen = classify_all(store, NOW, policy)
    assert klassen[claim_id(p1)].state == State.ACTIVE
    assert klassen[claim_id(p2)].state == State.REVOKED
