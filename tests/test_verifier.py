"""Tests für Verifizierer und Zustandsmaschine."""

import hashlib
import json
from pathlib import Path

import cbor2
import pytest

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_from_bytes, claim_id, is_equivocation_pair
from symbolon.errors import (
    BadScopeBinding,
    BadSignature,
    ErrorCode,
    ForeignLifecycle,
    IncoherentExpiry,
    InvalidGenesisAnchor,
    MalformedCbor,
    NonCanonicalEncoding,
    ReservedCorePredicate,
    UnknownJTag,
    UnknownNamespace,
    UnsupportedVersion,
)
from symbolon.index import classify_all
from symbolon.verifier import (
    InMemoryStore,
    State,
    classify,
    read_claim,
    structural_check,
)
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


def _add_chain(store: InMemoryStore, *names: str) -> None:
    for n in names:
        store.add(_claim(n))


# --- Positive structural checks ---


@pytest.mark.parametrize("name", ["TV1", "TV2", "TV3", "TV4", "TV5"])
def test_structural_check_valid_vectors(name: str):
    structural_check(bytes.fromhex(_vec(name)["signed_bytes"]))


def test_nv1_invalid_genesis_anchor_not_pending():
    with pytest.raises(InvalidGenesisAnchor) as exc:
        structural_check(bytes.fromhex(_vec("NV1")["signed_bytes"]))
    assert exc.value.code == ErrorCode.INVALID_GENESIS_ANCHOR


def _nv2_wire() -> bytes:
    return bytes.fromhex(_vec("NV2")["wire_bytes"])


def test_nv2_non_canonical_encoding():
    with pytest.raises(NonCanonicalEncoding):
        structural_check(_nv2_wire())


def test_nv2_non_canonical_encoding_read_claim():
    assert read_claim(_nv2_wire()) == ErrorCode.NON_CANONICAL_ENCODING


@pytest.mark.parametrize(
    "name, exc",
    [
        ("BV1", MalformedCbor),
        ("BV2", MalformedCbor),
        ("BV3", NonCanonicalEncoding),
    ],
)
def test_bv_structural_check(name: str, exc: type):
    with pytest.raises(exc):
        structural_check(bytes.fromhex(_vec(name)["wire_bytes"]))


def _reject_vectors_with_wire() -> list[dict]:
    out: list[dict] = []
    for v in VECTORS["vectors"]:
        if "expect_reject" not in v:
            continue
        if "wire_bytes" not in v and "signed_bytes" not in v:
            continue
        out.append(v)
    return out


@pytest.mark.parametrize(
    "v",
    _reject_vectors_with_wire(),
    ids=lambda v: v["name"],
)
def test_read_claim_reject_vectors(v: dict):
    hex_bytes = v["wire_bytes"] if "wire_bytes" in v else v["signed_bytes"]
    assert read_claim(bytes.fromhex(hex_bytes)) == ErrorCode[v["expect_reject"]]


def test_reject_vectors_all_carry_wire():
    """Jeder Vektor mit expect_reject trägt Drahtbytes (D291)."""
    missing = {
        v["name"]
        for v in VECTORS["vectors"]
        if "expect_reject" in v
        and "wire_bytes" not in v
        and "signed_bytes" not in v
    }
    assert missing == set()


def test_read_claim_tv1_matches_structural_check():
    data = bytes.fromhex(_vec("TV1")["signed_bytes"])
    checked = structural_check(data)
    result = read_claim(data)
    assert isinstance(result, Claim)
    assert claim_id(result) == claim_id(checked)


def test_tv6_read_claim_accepts():
    """core/* mit t >= t_exp: read_claim liefert einen Claim (01 §5.3, D264)."""
    result = read_claim(bytes.fromhex(_vec("TV6")["signed_bytes"]))
    assert isinstance(result, Claim)


def test_nv12_read_claim_malformed_cbor():
    """core/* mit J.tag != claim-ref: MALFORMED_CBOR (01 §6 Punkt 4, D263)."""
    result = read_claim(bytes.fromhex(_vec("NV12")["signed_bytes"]))
    assert result == ErrorCode.MALFORMED_CBOR


def test_nv2_reserializes_to_tv1_signed():
    nv2 = bytes.fromhex(_vec("NV2")["wire_bytes"])
    tv1_signed = bytes.fromhex(_vec("TV1")["signed_bytes"])
    assert cbor_canon.reserialize(nv2) == tv1_signed


def test_bv3_reserializes_to_tv1_signed():
    bv3 = bytes.fromhex(_vec("BV3")["wire_bytes"])
    tv1_signed = bytes.fromhex(_vec("TV1")["signed_bytes"])
    assert cbor_canon.reserialize(bv3) == tv1_signed


def test_bv3_is_one_byte_longer_than_tv1_signed():
    bv3 = bytes.fromhex(_vec("BV3")["wire_bytes"])
    tv1_signed = bytes.fromhex(_vec("TV1")["signed_bytes"])
    assert len(bv3) == len(tv1_signed) + 1


# --- Classification ---


def test_tv1_active_when_genesis():
    store = InMemoryStore()
    tv1 = _claim("TV1")
    store.add(tv1)
    result = classify(tv1, store, now=1_700_000_000)
    assert result.state == State.ACTIVE
    assert result.trust_usable is True


def test_tv2_pending_without_predecessor():
    store = InMemoryStore()
    tv2 = _claim("TV2")
    result = classify(tv2, store, now=1_700_000_100)
    assert result.state == State.PENDING


def test_tv2_active_with_predecessor():
    store = InMemoryStore()
    _add_chain(store, "TV1", "TV2")
    result = classify(_claim("TV2"), store, now=1_700_000_100)
    assert result.state == State.ACTIVE


def test_tv3_revokes_tv1():
    store = InMemoryStore()
    _add_chain(store, "TV1", "TV2", "TV3")
    assert classify(_claim("TV1"), store, now=1_700_000_200).state == State.REVOKED
    assert classify(_claim("TV3"), store, now=1_700_000_200).state == State.ACTIVE


def test_nv3_equivocation_flags_pair():
    store = InMemoryStore()
    tv1 = _claim("TV1")
    nv3 = _claim("NV3")
    assert is_equivocation_pair(tv1, nv3)
    store.add(tv1)
    store.add(nv3)
    assert classify(tv1, store, now=1_700_000_000).state == State.EQUIVOCATION_FLAGGED
    assert classify(nv3, store, now=1_700_000_001).state == State.EQUIVOCATION_FLAGGED


def test_equivocation_does_not_invalidate_downstream():
    store = InMemoryStore()
    _add_chain(store, "TV1", "TV2")
    store.add(_claim("NV3"))
    assert classify(_claim("TV2"), store, now=1_700_000_100).state == State.ACTIVE


def test_idempotent_add():
    store = InMemoryStore()
    tv1 = _claim("TV1")
    store.add(tv1)
    store.add(tv1)
    assert len(store.all_claims()) == 1


def test_tv1_linked_when_now_missing_and_t_exp_set():
    store = InMemoryStore()
    tv1 = _claim("TV1")
    store.add(tv1)
    result = classify(tv1, store, now=None)
    assert result.state == State.LINKED
    assert result.trust_usable is False


def test_expired_when_now_past_t_exp():
    store = InMemoryStore()
    tv1 = _claim("TV1")
    store.add(tv1)
    result = classify(tv1, store, now=1_800_000_000)
    assert result.state == State.EXPIRED
    assert result.trust_usable is False


def test_core_revoke_without_t_exp_stays_active():
    """core/*-Claim ohne t_exp bleibt jenseits jedes now aktiv."""
    store = InMemoryStore()
    _add_chain(store, "TV1", "TV2")
    tv3 = _claim("TV3")
    store.add(tv3)
    result = classify(tv3, store, now=9_999_999_999)
    assert result.state == State.ACTIVE


def test_core_revoke_with_expired_t_exp_stays_active():
    """core/*-Claim mit gesetztem t_exp bleibt jenseits von t_exp active (01 §5.3, TV5)."""
    store = InMemoryStore()
    _add_chain(store, "TV1", "TV2", "TV3")
    tv5 = _claim("TV5")
    store.add(tv5)
    result = classify(tv5, store, now=1_800_000_000)
    assert result.state == State.ACTIVE


def test_classify_superseded() -> None:
    """Ziel eines eigenen core/supersede@1 ist State.SUPERSEDED (01 §B.1, D278)."""
    scope = hashlib.sha256(b"scope:d278").digest()
    alice = Identity("alice")
    bob = Identity("bob")
    v = alice.vouch(bob, n=1, scope=scope, t=100)
    sup = alice.supersede(v, t=200)
    store = store_with(v, sup)
    result = classify(v, store, now=300)
    assert result.state == State.SUPERSEDED


def test_classify_revoked() -> None:
    """Gegenprobe: Ziel eines eigenen core/revoke@1 ist State.REVOKED (01 §B.1, D278)."""
    scope = hashlib.sha256(b"scope:d278").digest()
    alice = Identity("alice")
    bob = Identity("bob")
    v = alice.vouch(bob, n=1, scope=scope, t=100)
    rev = alice.revoke(v, t=200)
    store = store_with(v, rev)
    result = classify(v, store, now=300)
    assert result.state == State.REVOKED


def test_classify_foreign_lifecycle() -> None:
    """Fremder Widerruf: classify wirft ForeignLifecycle (D283)."""
    erste = Identity("erste")
    zweite = Identity("zweite")
    vouch = erste.vouch(zweite, n=1, scope=scope_id("foreign-lifecycle"), t=1000)
    revoke = zweite.revoke(vouch, t=1001)
    store = store_with(vouch, revoke)
    with pytest.raises(ForeignLifecycle):
        classify(revoke, store)


def test_classify_all_foreign_lifecycle() -> None:
    """Fremder Widerruf: classify_all übergeht ihn, Ziel bleibt active (D283, D452)."""
    erste = Identity("erste")
    zweite = Identity("zweite")
    vouch = erste.vouch(zweite, n=1, scope=scope_id("foreign-lifecycle"), t=1000)
    revoke = zweite.revoke(vouch, t=1001)
    store = store_with(vouch, revoke)
    result = classify_all(store, 1500)
    assert claim_id(revoke) not in result
    assert result[claim_id(vouch)].state == State.ACTIVE


# --- Error class coverage ---


def test_unsupported_version():
    data = bytearray.fromhex(_vec("TV1")["signed_bytes"])
    data[2] = 0x02  # corrupt version value byte — use proper construction
    obj = cbor2.loads(bytes.fromhex(_vec("TV1")["signed_bytes"]))
    obj[0] = 99
    wire = cbor_canon.encode(obj)
    with pytest.raises(UnsupportedVersion):
        structural_check(wire)


def test_malformed_cbor():
    with pytest.raises(MalformedCbor):
        structural_check(b"\xff\xff\xff")


def test_unknown_j_tag():
    obj = cbor2.loads(bytes.fromhex(_vec("TV1")["signed_bytes"]))
    obj[2] = [99, obj[2][1]]
    wire = cbor_canon.encode(obj)
    with pytest.raises(UnknownJTag):
        structural_check(wire)


def test_unknown_namespace_in_structural():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from symbolon.atom import Claim, sign, signed_bytes

    sk = Ed25519PrivateKey.from_private_bytes(b"\x01" * 32)
    base = _claim("TV1")
    c = Claim(
        version=1,
        I=base.I,
        J=base.J,
        p="svc:foo/bar@1",
        t=base.t,
        h_prev=base.h_prev,
        N=base.N,
        sigma=None,
    )
    wire = signed_bytes(
        Claim(
            version=c.version,
            I=c.I,
            J=c.J,
            p=c.p,
            t=c.t,
            h_prev=c.h_prev,
            N=c.N,
            sigma=sign(sk, c),
        )
    )
    with pytest.raises(UnknownNamespace):
        structural_check(wire)


def test_bad_scope_binding_structural():
    obj = cbor2.loads(bytes.fromhex(_vec("TV1")["signed_bytes"]))
    del obj[5]
    wire = cbor_canon.encode(obj)
    with pytest.raises(BadScopeBinding):
        structural_check(wire)


def test_reserved_core_predicate_structural():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from symbolon.atom import Claim, sign, signed_bytes

    sk = Ed25519PrivateKey.from_private_bytes(b"\x01" * 32)
    base = _claim("TV1")
    c = Claim(
        version=1,
        I=base.I,
        J=(2, claim_id(base)),
        p="core/vouch@1",
        t=1,
        h_prev=base.h_prev,
        sigma=None,
    )
    wire = signed_bytes(
        Claim(
            version=c.version,
            I=c.I,
            J=c.J,
            p=c.p,
            t=c.t,
            h_prev=c.h_prev,
            sigma=sign(sk, c),
        )
    )
    with pytest.raises(ReservedCorePredicate):
        structural_check(wire)


def test_foreign_lifecycle():
    store = InMemoryStore()
    store.add(_claim("TV4"))  # Bob's claim as target
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from symbolon.atom import Claim, sign, signed_bytes

    sk = Ed25519PrivateKey.from_private_bytes(b"\x01" * 32)
    target = _claim("TV4")
    c = Claim(
        version=1,
        I=bytes.fromhex(VECTORS["params"]["ALICE"]),
        J=(2, claim_id(target)),
        p="core/revoke@1",
        t=1,
        h_prev=bytes.fromhex(VECTORS["params"]["id_genesis_anchor_ALICE"]),
        sigma=None,
    )
    wire = signed_bytes(
        Claim(
            version=c.version,
            I=c.I,
            J=c.J,
            p=c.p,
            t=c.t,
            h_prev=c.h_prev,
            sigma=sign(sk, c),
        )
    )
    with pytest.raises(ForeignLifecycle):
        structural_check(wire, store=store)


def test_bad_signature():
    wire = bytearray.fromhex(_vec("TV1")["signed_bytes"])
    wire[-1] ^= 0xFF
    with pytest.raises(BadSignature):
        structural_check(bytes(wire))


def test_incoherent_expiry():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from symbolon.atom import Claim, sign, signed_bytes

    sk = Ed25519PrivateKey.from_private_bytes(b"\x01" * 32)
    base = _claim("TV1")
    c = Claim(
        version=base.version,
        I=base.I,
        J=base.J,
        p=base.p,
        t=1_735_689_600,
        h_prev=base.h_prev,
        v=base.v,
        N=base.N,
        t_exp=1_700_000_000,
        sigma=None,
    )
    wire = signed_bytes(
        Claim(
            version=c.version,
            I=c.I,
            J=c.J,
            p=c.p,
            t=c.t,
            h_prev=c.h_prev,
            v=c.v,
            N=c.N,
            t_exp=c.t_exp,
            sigma=sign(sk, c),
        )
    )
    with pytest.raises(IncoherentExpiry):
        structural_check(wire)


def test_non_canonical_positive_canonical_passes():
    wire = bytes.fromhex(_vec("TV1")["signed_bytes"])
    assert cbor_canon.is_canonical(wire)


def test_error_code_value_equals_member_name() -> None:
    """Membername und Wert von ErrorCode sind identisch (01 §B.2, D279)."""
    for member in ErrorCode:
        assert member.value == member.name
