"""Schlüsseltypen in v (02 §3.1, 03 §1.3, 04 §2.3, 04 §3.5, D456)."""

from __future__ import annotations

import hashlib

from symbolon import cbor_canon
from symbolon.domains import DOM_NUC_GEN
from symbolon.governance import Finding, GovernanceFinding, decide
from symbolon.governance.objects import Epoch, Proposal
from symbolon.governance.tally import TallyState
from symbolon.governance.tally import read_v as read_v_04
from symbolon.profiles.findings import ProfileFinding
from symbolon.profiles.payload import read_v as read_v_03
from symbolon.trust.findings import TrustFinding
from symbolon.trust.groups import _decode_weight
from tests.helpers import store_with

from tests.governance.fixtures import (
    C1,
    C2,
    CONSTITUTION_HASH_1,
    CONSTITUTION_HASH_2,
    GENESIS_D,
    policy_of,
)

# Zeilen der Tabelle in D456 Befund 1. Zeilen 1 bis 6 sind unlesbar.
# Zeilen 7 und 8 behalten die gemessene Lage: beide Bytes sind nicht kanonisch.
_ROWS: tuple[tuple[int, str, str], ...] = (
    (1, "a1f401", "unreadable"),
    (2, "a1f9000001", "unreadable"),
    (3, "a2000105a1f400", "unreadable"),
    (4, "a200f5f4f5", "unreadable"),
    (5, "a1810001", "unreadable"),
    (6, "a1c2410001", "unreadable"),
    (7, "a200012000410002616103", "noncanonical"),
    (8, "a200010002", "noncanonical"),
)


def test_schluessel_der_tabelle() -> None:
    """Acht Vektoren: Zeilen 1–6 unlesbar, 7 und 8 nicht kanonisch (02 §3.1, D456)."""
    for row, hex_v, lage in _ROWS:
        data = bytes.fromhex(hex_v)
        if lage == "unreadable":
            assert cbor_canon.keys_admissible(data) is False, row
            assert _decode_weight(data, 8) == (None, TrustFinding.UNPARSABLE_VOUCH_PAYLOAD)
            assert read_v_03(data) == (None, (ProfileFinding.UNPARSABLE_V,))
            assert read_v_04(data) == (None, GovernanceFinding.UNPARSABLE_V)
        else:
            assert cbor_canon.keys_admissible(data) is True, row
            assert _decode_weight(data, 8) == (None, TrustFinding.NON_CANONICAL_V)
            assert read_v_03(data) == (None, (ProfileFinding.NON_CANONICAL_V,))
            assert read_v_04(data) == (None, GovernanceFinding.NON_CANONICAL_V)


def test_zeile_7_schluessel_0_ist_int_eins() -> None:
    """Dekodiert ist Key 0 der int 1; die Bytes sind nicht kanonisch (02 §3.1, D456)."""
    data = bytes.fromhex("a200012000410002616103")
    obj = cbor_canon.decode(data)
    assert type(obj[0]) is int and obj[0] == 1
    assert _decode_weight(data, 8)[0] is None
    assert read_v_04(data)[0] is None


def test_indefinite_map_mit_unzulaessigem_schluessel() -> None:
    """Indefinite Map mit bool-Schlüssel ist unlesbar (02 §3.1, D456)."""
    data = bytes.fromhex("bff400ff")
    assert cbor_canon.keys_admissible(data) is False
    assert _decode_weight(data, 8) == (None, TrustFinding.UNPARSABLE_VOUCH_PAYLOAD)
    assert read_v_03(data) == (None, (ProfileFinding.UNPARSABLE_V,))
    assert read_v_04(data) == (None, GovernanceFinding.UNPARSABLE_V)


def test_genesis_false_ist_unsupported_weight_mode() -> None:
    """genesis[6] = false ist nicht der uint 0 (04 §3.5, D456)."""
    genesis = dict(GENESIS_D)
    genesis[6] = False
    scope = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis)).digest()
    epoch = Epoch(scope=scope, index=1, constitution_hash=CONSTITUTION_HASH_1)
    proposal = Proposal(
        scope=scope,
        predecessor=epoch.epoch_id,
        constitution_hash=CONSTITUTION_HASH_2,
    )
    result = decide(
        store_with(),
        epoch=epoch,
        proposal=proposal,
        genesis_obj=genesis,
        constitution_obj=C1,
        target_constitution_obj=C2,
        known_proposals={proposal.proposal_hash: proposal},
        now=1000,
        policy=policy_of(C1, scope),
    )
    assert result.state is TallyState.UNEVALUABLE
    assert result.findings == (
        Finding(GovernanceFinding.UNSUPPORTED_WEIGHT_MODE, scope),
    )
