"""Vektoren des Geräts aus einem gültigen Kern (D481 Beschluss 1 und 2, 01 §2, 01 §3, 01 §4)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cbor2
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
)

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id, core_bytes, core_map, id_genesis_anchor, sign
from symbolon.domains import DOM_CID, DOM_ID_GEN, DOM_SIG

ZIEL = Path(__file__).resolve().parent.parent / "symbolon" / "node" / "static" / "vektoren.json"
_SEED = b"p5-geraet"


def _sk() -> Ed25519PrivateKey:
    return Ed25519PrivateKey.from_private_bytes(hashlib.sha256(_SEED).digest())


def _pairs(claim: Claim) -> list[tuple[bytes, bytes]]:
    mapping = core_map(claim)
    return [
        (cbor_canon.encode(key), cbor_canon.encode(mapping[key])) for key in sorted(mapping)
    ]


def _head(major: int, count: int) -> bytes:
    return bytes([(major << 5) | count])


def _map(pairs: list[tuple[bytes, bytes]]) -> bytes:
    return _head(5, len(pairs)) + b"".join(key + value for key, value in pairs)


def _uint_long(value: int) -> bytes:
    """Dieselbe Zahl eine Breite länger als die kürzeste Form (01 §3 Regel 3)."""
    if value < 24:
        return bytes([(0 << 5) | 24, value])
    if value < 256:
        return bytes([(0 << 5) | 25]) + value.to_bytes(2, "big")
    raise ValueError("value needs no longer form here")


def _replace(pairs: list[tuple[bytes, bytes]], key: int, value: bytes) -> list[tuple[bytes, bytes]]:
    encoded = cbor_canon.encode(key)
    return [(item, value if item == encoded else current) for item, current in pairs]


def _drop(pairs: list[tuple[bytes, bytes]], key: int) -> list[tuple[bytes, bytes]]:
    encoded = cbor_canon.encode(key)
    return [(item, current) for item, current in pairs if item != encoded]


def _claim(sk: Ed25519PrivateKey, **fields: object) -> Claim:
    author = sk.public_key().public_bytes_raw()
    base = {
        "version": 1,
        "I": author,
        "J": (2, hashlib.sha256(_SEED + b"-ziel").digest()),
        "p": "core/revoke@1",
        "t": 1_700_000_000,
        "h_prev": hashlib.sha256(_SEED + b"-vorgaenger").digest(),
    }
    base.update(fields)
    return Claim(**base)  # type: ignore[arg-type]


def _accept(sk: Ed25519PrivateKey, claim: Claim, tip: bytes) -> dict[str, str]:
    return {
        "I": claim.I.hex(),
        "anchor": id_genesis_anchor(claim.I).hex(),
        "claim_id": claim_id(claim).hex(),
        "core": core_bytes(claim).hex(),
        "expect": "ACCEPT",
        "sigma": sign(sk, claim).hex(),
        "tip": tip.hex(),
    }


def _reject(core: bytes, author: bytes, tip: bytes, expect: str) -> dict[str, str]:
    return {"I": author.hex(), "core": core.hex(), "expect": expect, "tip": tip.hex()}


def build() -> dict[str, object]:
    """Fälle, deren Bytes aus einem gültigen Kern entstehen (D481 Beschluss 1, 01 §2, 01 §4)."""
    sk = _sk()
    author = sk.public_key().public_bytes_raw()
    tip = hashlib.sha256(_SEED + b"-vorgaenger").digest()
    anchor = id_genesis_anchor(author)
    bare = _claim(sk)
    full = _claim(
        sk,
        v=b"wert",
        N=hashlib.sha256(_SEED + b"-scope").digest(),
        t_exp=1_800_000_000,
    )
    wide = _claim(sk, t_exp=2**53 + 1)
    genesis = _claim(sk, h_prev=anchor)
    pairs = _pairs(bare)
    canonical = core_bytes(bare)
    cases = [
        _accept(sk, bare, tip),
        _accept(sk, full, tip),
        _accept(sk, wide, tip),
        _accept(sk, genesis, anchor),
        _reject(canonical + canonical[:1], author, tip, "MALFORMED"),
        _reject(canonical[:-1], author, tip, "MALFORMED"),
        _reject(
            _head(5, 31) + b"".join(key + value for key, value in pairs) + _head(7, 31),
            author,
            tip,
            "MALFORMED",
        ),
        _reject(_head(6, 0) + canonical, author, tip, "MALFORMED"),
        _reject(_map(_replace(pairs, 0, cbor2.dumps(float(bare.version)))), author, tip, "MALFORMED"),
        _reject(_map(_replace(pairs, 0, cbor2.dumps(-bare.version))), author, tip, "MALFORMED"),
        _reject(_map([pairs[0], *pairs]), author, tip, "MALFORMED"),
        _reject(_map(_replace(pairs, 0, _uint_long(bare.version))), author, tip, "NOT_CANONICAL"),
        _reject(_map(list(reversed(pairs))), author, tip, "NOT_CANONICAL"),
        _reject(
            cbor_canon.encode({**core_map(bare), 9: author[:8]}),
            author,
            tip,
            "SCHEMA",
        ),
        _reject(cbor_canon.encode({**core_map(bare), 10: 0}), author, tip, "SCHEMA"),
        _reject(_map(_drop(pairs, 6)), author, tip, "SCHEMA"),
        _reject(
            cbor_canon.encode({**core_map(bare), 1: bare.I[:-1]}),
            author,
            tip,
            "SCHEMA",
        ),
        _reject(
            cbor_canon.encode({**core_map(bare), 2: [bare.J[0], bare.J[1], bare.J[1][:1]]}),
            author,
            tip,
            "SCHEMA",
        ),
        _reject(
            _map(_replace(pairs, 3, _head(2, len(bare.p.encode())) + bare.p.encode())),
            author,
            tip,
            "SCHEMA",
        ),
        _reject(core_bytes(_claim(sk, version=2)), author, tip, "WRONG_VERSION"),
        _reject(
            core_bytes(_claim(sk, I=hashlib.sha256(_SEED + b"-fremd").digest())),
            author,
            tip,
            "WRONG_AUTHOR",
        ),
        _reject(canonical, author, anchor, "WRONG_PREDECESSOR"),
    ]
    return {
        "cases": cases,
        "domains": {
            "DOM_CID": DOM_CID.hex(),
            "DOM_ID_GEN": DOM_ID_GEN.hex(),
            "DOM_SIG": DOM_SIG.hex(),
        },
        "key": {
            "pkcs8": sk.private_bytes(Encoding.DER, PrivateFormat.PKCS8, NoEncryption()).hex(),
            "public": author.hex(),
        },
    }


def render() -> bytes:
    """Stabile Bytes der Vektordatei (D481 Beschluss 1)."""
    return json.dumps(build(), indent=2, sort_keys=True).encode() + b"\n"


def main() -> None:
    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    ZIEL.write_bytes(render())


if __name__ == "__main__":
    main()
