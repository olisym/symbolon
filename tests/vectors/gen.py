#!/usr/bin/env python3
"""Reproduziert Test-Vektoren aus Anhang C (feste Seeds, kanonisches CBOR)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from symbolon.atom import (
    Claim,
    claim_id,
    core_bytes,
    core_map,
    id_genesis_anchor,
    sign,
    signed_bytes,
    signed_map,
)
from symbolon.domains import DOM_NUC_GEN, DOM_SIG
from symbolon import cbor_canon
from tests.helpers import SEED_ALICE, SEED_BOB

VECTORS_PATH = Path(__file__).resolve().parent / "vectors_01.json"

ALICE_SEED = SEED_ALICE
BOB_SEED = SEED_BOB

ALICE_PUB = bytes.fromhex(
    "8a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c"
)
BOB_PUB = bytes.fromhex(
    "8139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df60f5b8fc9b394"
)

CONST = bytes.fromhex(
    "890b21e7cd43fc4226938ce0b6eae1d00efa04ef9e6585c352dcf19ccad5ea7e"
)

# Genesis-Objekt aus 00 §3.1 (uint-Keys, kanonisches CBOR)
GENESIS_OBJ = {
    0: 1,
    1: [ALICE_PUB],
    2: 0,
    3: [ALICE_PUB],
    4: CONST,
    5: 2,
    6: 1,
    7: 0,
}

N = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(GENESIS_OBJ)).digest()

N_HEX = N.hex()
P_VOUCH = f"nuc:{N_HEX}/vouch@1"
P_ACCEPT = f"nuc:{N_HEX}/accept-rules@1"
P_REVOKE = "core/revoke@1"

V_VOUCH = bytes.fromhex("a1001864")

# BV1, BV2 — Byte-Vektoren Anhang C.8 (kein Schlüsselmaterial)
BV1_HEX = "a100ff"
BV2_HEX = "bf616100ff"


def _sk(seed: bytes) -> Ed25519PrivateKey:
    return Ed25519PrivateKey.from_private_bytes(seed)


def _finalize(claim: Claim, sk: Ed25519PrivateKey) -> Claim:
    return replace(claim, sigma=sign(sk, claim))


def _signed_wire(core: dict, sk: Ed25519PrivateKey) -> bytes:
    """Core kanonisch kodieren, mit sk über DOM_SIG ‖ core_bytes signieren, Map inkl. σ."""
    core_b = cbor_canon.encode(core)
    sigma = sk.sign(DOM_SIG + core_b)
    signed = dict(core)
    signed[9] = sigma
    return cbor_canon.encode(signed)


def _vec(name: str, claim: Claim, *, expect_reject: str | None = None) -> dict:
    cid = claim_id(claim)
    core = core_bytes(claim)
    wire = signed_bytes(claim)
    entry = {
        "name": name,
        "claim_id": cid.hex(),
        "core_bytes": core.hex(),
        "signed_bytes": wire.hex(),
        "sigma": claim.sigma.hex() if claim.sigma else None,
    }
    if expect_reject:
        entry["expect_reject"] = expect_reject
    return entry


def build_vectors() -> dict:
    alice_sk = _sk(ALICE_SEED)
    bob_sk = _sk(BOB_SEED)

    h_gen_alice = id_genesis_anchor(ALICE_PUB)
    h_gen_bob = id_genesis_anchor(BOB_PUB)

    # TV1 — Genesis-Vouch Alice → Bob
    tv1_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(1, BOB_PUB),
        p=P_VOUCH,
        v=V_VOUCH,
        N=N,
        t=1_700_000_000,
        t_exp=1_735_689_600,
        h_prev=h_gen_alice,
    )
    tv1 = _finalize(tv1_unsigned, alice_sk)
    tv1_cid = claim_id(tv1)

    # BV3 — TV1s signierte Map in indefinite-length-Form (Anhang C.8)
    tv1_signed = signed_map(tv1)
    bv3_wire = (
        b"\xbf"
        + b"".join(
            cbor_canon.encode(k) + cbor_canon.encode(tv1_signed[k])
            for k in sorted(tv1_signed)
        )
        + b"\xff"
    )
    nv2_key_order = [8, 6, 5, 3, 2, 1, 0, 7, 4, 9]
    nv2_wire = bytes([0xA0 + len(nv2_key_order)]) + b"".join(
        cbor_canon.encode(k) + cbor_canon.encode(tv1_signed[k])
        for k in nv2_key_order
    )

    # TV2 — accept-rules Alice, verkettet auf TV1
    tv2_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(3, CONST),
        p=P_ACCEPT,
        N=N,
        t=1_700_000_100,
        h_prev=tv1_cid,
    )
    tv2 = _finalize(tv2_unsigned, alice_sk)
    tv2_cid = claim_id(tv2)

    # TV3 — core/revoke@1 widerruft TV1
    tv3_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(2, tv1_cid),
        p=P_REVOKE,
        t=1_700_000_200,
        h_prev=tv2_cid,
    )
    tv3 = _finalize(tv3_unsigned, alice_sk)
    tv3_cid = claim_id(tv3)

    # TV5 — core/revoke@1 wiederholt TV1, verkettet auf TV3, mit t_exp (01 §C.9)
    tv5_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(2, tv1_cid),
        p=P_REVOKE,
        t=1_700_000_300,
        t_exp=1_700_000_400,
        h_prev=tv3_cid,
    )
    tv5 = _finalize(tv5_unsigned, alice_sk)
    tv5_cid = claim_id(tv5)

    # TV4 — accept-rules Bob, Genesis
    tv4_unsigned = Claim(
        version=1,
        I=BOB_PUB,
        J=(3, CONST),
        p=P_ACCEPT,
        N=N,
        t=1_700_000_050,
        h_prev=h_gen_bob,
    )
    tv4 = _finalize(tv4_unsigned, bob_sk)

    # NV1 — h_prev = 32×0x00
    nv1_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(1, BOB_PUB),
        p=P_VOUCH,
        N=N,
        t=1_700_000_300,
        h_prev=bytes(32),
    )
    nv1 = _finalize(nv1_unsigned, alice_sk)

    # NV3 — Equivocation gegen TV1 (gleiches h_prev, anderes t)
    nv3_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(1, BOB_PUB),
        p=P_VOUCH,
        N=N,
        t=1_700_000_001,
        h_prev=h_gen_alice,
    )
    nv3 = _finalize(nv3_unsigned, alice_sk)

    # NV4 — version 2
    nv4_unsigned = Claim(
        version=2,
        I=ALICE_PUB,
        J=(1, BOB_PUB),
        p=P_VOUCH,
        v=V_VOUCH,
        N=N,
        t=1_700_000_401,
        h_prev=h_gen_alice,
    )
    nv4 = _finalize(nv4_unsigned, alice_sk)

    # NV5 — J.tag 4
    nv5_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(4, BOB_PUB),
        p=P_VOUCH,
        v=V_VOUCH,
        N=N,
        t=1_700_000_402,
        h_prev=h_gen_alice,
    )
    nv5 = _finalize(nv5_unsigned, alice_sk)

    # NV6 — Namensraum foo, N abwesend
    nv6_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(1, BOB_PUB),
        p="foo/vouch@1",
        v=V_VOUCH,
        t=1_700_000_403,
        h_prev=h_gen_alice,
    )
    nv6 = _finalize(nv6_unsigned, alice_sk)

    # NV7 — N ist 32×0x11, p bleibt kanonisch auf N
    nv7_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(1, BOB_PUB),
        p=P_VOUCH,
        v=V_VOUCH,
        N=b"\x11" * 32,
        t=1_700_000_404,
        h_prev=h_gen_alice,
    )
    nv7 = _finalize(nv7_unsigned, alice_sk)

    # NV8 — Alias-Kodierung, N abwesend
    nv8_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(1, BOB_PUB),
        p="nuc:beispiel-alias/vouch@1",
        v=V_VOUCH,
        t=1_700_000_405,
        h_prev=h_gen_alice,
    )
    nv8 = _finalize(nv8_unsigned, alice_sk)

    # NV9 — core/rotate@1, J wie TV3, kein v, kein N
    nv9_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(2, tv1_cid),
        p="core/rotate@1",
        t=1_700_000_406,
        h_prev=h_gen_alice,
    )
    nv9 = _finalize(nv9_unsigned, alice_sk)

    # NV10 — mit BOB signiert, I bleibt ALICE
    nv10_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(1, BOB_PUB),
        p=P_VOUCH,
        v=V_VOUCH,
        N=N,
        t=1_700_000_407,
        h_prev=h_gen_alice,
    )
    nv10 = _finalize(nv10_unsigned, bob_sk)

    # NV11 — t_exp gleich t
    nv11_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(1, BOB_PUB),
        p=P_VOUCH,
        v=V_VOUCH,
        N=N,
        t=1_700_000_408,
        t_exp=1_700_000_408,
        h_prev=h_gen_alice,
    )
    nv11 = _finalize(nv11_unsigned, alice_sk)

    # TV6 — core/revoke@1 mit t >= t_exp, verkettet auf TV5 (01 §C.11, D264)
    tv6_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(2, tv1_cid),
        p=P_REVOKE,
        t=1_700_000_410,
        t_exp=1_700_000_405,
        h_prev=tv5_cid,
    )
    tv6 = _finalize(tv6_unsigned, alice_sk)

    # NV32 — accept-rules Alice, verkettet auf TV6, t kleiner als Vorgänger (D353)
    nv32_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(3, CONST),
        p=P_ACCEPT,
        N=N,
        t=1_700_000_409,
        h_prev=claim_id(tv6),
    )
    nv32 = _finalize(nv32_unsigned, alice_sk)

    # NV12 — core/revoke@1 mit J.tag 1 statt claim-ref (01 §C.11, D263)
    nv12_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(1, ALICE_PUB),
        p=P_REVOKE,
        t=1_700_000_409,
        h_prev=h_gen_alice,
    )
    nv12 = _finalize(nv12_unsigned, alice_sk)

    # NV13 — Großbuchstaben im nuc:-Namen (01 §C.12, D267)
    nv13_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(1, BOB_PUB),
        p="nuc:" + N.hex() + "/VOUCH@1",
        v=V_VOUCH,
        N=N,
        t=1_700_000_411,
        h_prev=h_gen_alice,
    )
    nv13 = _finalize(nv13_unsigned, alice_sk)

    tv1_core = core_map(tv1)

    # NV14 — Key 20 am TV1-Core, neu signiert (01 §C.13, D266)
    nv14_core = dict(tv1_core)
    nv14_core[20] = 1
    nv14_wire = _signed_wire(nv14_core, alice_sk)

    # NV15 — Key 6 trägt CBOR true, neu signiert (01 §C.13, D272)
    nv15_core = dict(tv1_core)
    nv15_core[6] = True
    nv15_wire = _signed_wire(nv15_core, alice_sk)

    # NV16 — Key 6 trägt -5, neu signiert (01 §C.13, D272)
    nv16_core = dict(tv1_core)
    nv16_core[6] = -5
    nv16_wire = _signed_wire(nv16_core, alice_sk)

    # NV17 — Key 6 doppelt im unveränderten signierten TV1 (01 §C.13, D271)
    tv1_wire = signed_bytes(tv1)
    pair_6_a = cbor_canon.encode(6) + cbor_canon.encode(1_700_000_000)
    pair_6_b = cbor_canon.encode(6) + cbor_canon.encode(1_700_000_001)
    assert tv1_wire[0] == 0xAA
    body = tv1_wire[1:]
    assert body.count(pair_6_a) == 1
    idx = body.index(pair_6_a)
    nv17_wire = (
        bytes([0xAB]) + body[: idx + len(pair_6_a)] + pair_6_b + body[idx + len(pair_6_a) :]
    )

    # NV18 — version 2, Key 6 abwesend, neu signiert (01 §C.13, D266)
    nv18_core = dict(tv1_core)
    nv18_core[0] = 2
    del nv18_core[6]
    nv18_wire = _signed_wire(nv18_core, alice_sk)

    # NV19 — signiertes TV1 plus ein Byte 0x00 (01 §C.13, D270)
    nv19_wire = signed_bytes(tv1) + b"\x00"

    # NV20 — Key 0 trägt CBOR true statt 1 (01 §C.14, D280)
    nv20_core = dict(tv1_core)
    nv20_core[0] = True
    nv20_wire = _signed_wire(nv20_core, alice_sk)

    # NV21 — Key 1 trägt die ersten 31 Byte seines bisherigen Wertes (01 §C.14, D280)
    nv21_core = dict(tv1_core)
    nv21_core[1] = nv21_core[1][:31]
    nv21_wire = _signed_wire(nv21_core, alice_sk)

    # NV22 — Key 2 trägt [1, BOB_PUB, BOB_PUB] (01 §C.14, D280)
    nv22_core = dict(tv1_core)
    nv22_core[2] = [1, BOB_PUB, BOB_PUB]
    nv22_wire = _signed_wire(nv22_core, alice_sk)

    # NV23 — Key 2 trägt [true, BOB_PUB] (01 §C.14, D280)
    nv23_core = dict(tv1_core)
    nv23_core[2] = [True, BOB_PUB]
    nv23_wire = _signed_wire(nv23_core, alice_sk)

    # NV24 — Key 3 trägt die Zahl 1 statt einer Zeichenfolge (01 §C.14, D280)
    nv24_core = dict(tv1_core)
    nv24_core[3] = 1
    nv24_wire = _signed_wire(nv24_core, alice_sk)

    # NV25 — Key 4 trägt die Zahl 1 statt einer Bytefolge (01 §C.14, D280)
    nv25_core = dict(tv1_core)
    nv25_core[4] = 1
    nv25_wire = _signed_wire(nv25_core, alice_sk)

    # NV26 — Key 5 trägt die ersten 31 Byte seines bisherigen Wertes (01 §C.14, D280)
    nv26_core = dict(tv1_core)
    nv26_core[5] = nv26_core[5][:31]
    nv26_wire = _signed_wire(nv26_core, alice_sk)

    # NV27 — Key 7 trägt CBOR true (01 §C.14, D280)
    nv27_core = dict(tv1_core)
    nv27_core[7] = True
    nv27_wire = _signed_wire(nv27_core, alice_sk)

    # NV28 — Key 8 trägt die ersten 31 Byte seines bisherigen Wertes (01 §C.14, D280)
    nv28_core = dict(tv1_core)
    nv28_core[8] = nv28_core[8][:31]
    nv28_wire = _signed_wire(nv28_core, alice_sk)

    # NV29 — Core unverändert; Key 9 trägt die ersten 63 Byte der Signatur (01 §C.14, D280)
    nv29_core_b = cbor_canon.encode(tv1_core)
    nv29_sigma = alice_sk.sign(DOM_SIG + nv29_core_b)
    nv29_signed = dict(tv1_core)
    nv29_signed[9] = nv29_sigma[:63]
    nv29_wire = cbor_canon.encode(nv29_signed)

    # NV30 — Key 3 fehlt (01 §C.14, D280)
    nv30_core = dict(tv1_core)
    del nv30_core[3]
    nv30_wire = _signed_wire(nv30_core, alice_sk)

    # NV31 — zehn TV1-Werte als Array statt als Map (01 §C.15, D285)
    nv31_wire = cbor_canon.encode([tv1_signed[k] for k in sorted(tv1_signed)])

    return {
        "params": {
            "ALICE": ALICE_PUB.hex(),
            "BOB": BOB_PUB.hex(),
            "N": N.hex(),
            "CONST": CONST.hex(),
            "id_genesis_anchor_ALICE": h_gen_alice.hex(),
            "id_genesis_anchor_BOB": h_gen_bob.hex(),
        },
        "vectors": [
            _vec("TV1", tv1),
            _vec("TV2", tv2),
            _vec("TV3", tv3),
            _vec("TV4", tv4),
            _vec("NV1", nv1, expect_reject="INVALID_GENESIS_ANCHOR"),
            _vec("NV3", nv3),
            {
                "name": "NV2",
                "wire_bytes": nv2_wire.hex(),
                "expect_reject": "NON_CANONICAL_ENCODING",
            },
            {
                "name": "BV1",
                "wire_bytes": BV1_HEX,
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "BV2",
                "wire_bytes": BV2_HEX,
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "BV3",
                "wire_bytes": bv3_wire.hex(),
                "expect_reject": "NON_CANONICAL_ENCODING",
            },
            _vec("TV5", tv5),
            _vec("NV4", nv4, expect_reject="UNSUPPORTED_VERSION"),
            _vec("NV5", nv5, expect_reject="UNKNOWN_J_TAG"),
            _vec("NV6", nv6, expect_reject="UNKNOWN_NAMESPACE"),
            _vec("NV7", nv7, expect_reject="BAD_SCOPE_BINDING"),
            _vec("NV8", nv8, expect_reject="BAD_SCOPE_BINDING"),
            _vec("NV9", nv9, expect_reject="RESERVED_CORE_PREDICATE"),
            _vec("NV10", nv10, expect_reject="BAD_SIGNATURE"),
            _vec("NV11", nv11, expect_reject="INCOHERENT_EXPIRY"),
            _vec("TV6", tv6),
            _vec("NV12", nv12, expect_reject="MALFORMED_CBOR"),
            _vec("NV13", nv13, expect_reject="INVALID_PREDICATE"),
            {
                "name": "NV14",
                "wire_bytes": nv14_wire.hex(),
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "NV15",
                "wire_bytes": nv15_wire.hex(),
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "NV16",
                "wire_bytes": nv16_wire.hex(),
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "NV17",
                "wire_bytes": nv17_wire.hex(),
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "NV18",
                "wire_bytes": nv18_wire.hex(),
                "expect_reject": "UNSUPPORTED_VERSION",
            },
            {
                "name": "NV19",
                "wire_bytes": nv19_wire.hex(),
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "NV20",
                "wire_bytes": nv20_wire.hex(),
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "NV21",
                "wire_bytes": nv21_wire.hex(),
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "NV22",
                "wire_bytes": nv22_wire.hex(),
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "NV23",
                "wire_bytes": nv23_wire.hex(),
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "NV24",
                "wire_bytes": nv24_wire.hex(),
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "NV25",
                "wire_bytes": nv25_wire.hex(),
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "NV26",
                "wire_bytes": nv26_wire.hex(),
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "NV27",
                "wire_bytes": nv27_wire.hex(),
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "NV28",
                "wire_bytes": nv28_wire.hex(),
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "NV29",
                "wire_bytes": nv29_wire.hex(),
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "NV30",
                "wire_bytes": nv30_wire.hex(),
                "expect_reject": "MALFORMED_CBOR",
            },
            # NV31 — 01 §C.15, D285
            {
                "name": "NV31",
                "wire_bytes": nv31_wire.hex(),
                "expect_reject": "MALFORMED_CBOR",
            },
            _vec("NV32", nv32),
        ],
    }


def main() -> None:
    data = build_vectors()
    VECTORS_PATH.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Wrote {VECTORS_PATH}")


if __name__ == "__main__":
    main()
