"""Vektoren des Geräts (D481 Beschluss 1 und 2, 01 §3, 01 §4)."""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import load_der_private_key

from symbolon import cbor_canon
from symbolon.atom import claim_from_bytes, claim_id, id_genesis_anchor, sign, verify_sig
from symbolon.domains import DOM_SIG
from symbolon.errors import VerifierError
from symbolon.verifier import structural_check
from tools.geraet_vektoren import render

_DATEI = Path("symbolon/node/static/vektoren.json")


def test_vektoren_bytegleich() -> None:
    """Die Datei ist die Ausgabe des Werkzeugs (D481 Beschluss 1)."""
    assert _DATEI.read_bytes() == render()


def _definite_map(data: bytes) -> bool:
    if not data:
        return False
    major = data[0] >> 5
    info = data[0] & 0x1F
    return major == 5 and info < 24


def _mit_signatur(core: bytes, sigma: bytes) -> bytes | None:
    if not _definite_map(core):
        return None
    pair = cbor_canon.encode(9) + cbor_canon.encode(sigma)
    return bytes([core[0] + 1]) + core[1:] + pair


def _weist_ab(core: bytes, sigma: bytes) -> bool:
    signed = _mit_signatur(core, sigma)
    if signed is None:
        try:
            cbor_canon.decode(core)
        except Exception:
            return True
        return not _definite_map(core)
    try:
        structural_check(signed)
    except VerifierError:
        return True
    return False


def test_faelle_mit_symbolon() -> None:
    """Jeder Fall gegen atom und structural_check (D481 Beschluss 1, 01 §2, 01 §4)."""
    data = json.loads(_DATEI.read_text())
    loaded = load_der_private_key(bytes.fromhex(data["key"]["pkcs8"]), password=None)
    assert isinstance(loaded, Ed25519PrivateKey)
    offen: list[str] = []
    for index, fall in enumerate(data["cases"]):
        core = bytes.fromhex(fall["core"])
        if fall["expect"] == "ACCEPT":
            claim = claim_from_bytes(core)
            sigma = sign(loaded, claim)
            assert claim_id(claim).hex() == fall["claim_id"]
            assert id_genesis_anchor(bytes.fromhex(fall["I"])).hex() == fall["anchor"]
            assert sigma.hex() == fall["sigma"]
            assert verify_sig(replace(claim, sigma=sigma))
            continue
        obj = None
        try:
            decoded = cbor_canon.decode(core)
            if isinstance(decoded, dict):
                obj = decoded
        except Exception:
            obj = None
        if fall["expect"] == "WRONG_AUTHOR":
            assert obj is not None
            assert obj[1] != bytes.fromhex(fall["I"])
        if fall["expect"] == "WRONG_PREDECESSOR":
            assert obj is not None
            assert obj[8] != bytes.fromhex(fall["tip"])
            continue
        sigma = loaded.sign(DOM_SIG + core)
        if not _weist_ab(core, sigma):
            offen.append(f"{index}:{fall['expect']}")
    assert offen == []
