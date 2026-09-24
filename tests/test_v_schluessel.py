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
# Zeile 7 ist die kanonische Map und lesbar, Zeile 8 nicht kanonisch.
_ROWS: tuple[tuple[int, str, str], ...] = (
    (1, "a1f401", "unreadable"),
    (2, "a1f9000001", "unreadable"),
    (3, "a2000105a1f400", "unreadable"),
    (4, "a200f5f4f5", "unreadable"),
    (5, "a1810001", "unreadable"),
    (6, "a1c2410001", "unreadable"),
    (7, "a400012000410002616103", "lesbar"),
    (8, "a200010002", "noncanonical"),
)


def test_schluessel_der_tabelle() -> None:
    """Zeilen 1–6 unlesbar, 7 lesbar, 8 nicht kanonisch (02 §3.1, D456)."""
    for row, hex_v, lage in _ROWS:
        data = bytes.fromhex(hex_v)
        if lage == "unreadable":
            assert cbor_canon.keys_admissible(data) is False, row
            assert _decode_weight(data, 8) == (None, TrustFinding.UNPARSABLE_VOUCH_PAYLOAD)
            assert read_v_03(data) == (None, (ProfileFinding.UNPARSABLE_V,))
            assert read_v_04(data) == (None, GovernanceFinding.UNPARSABLE_V)
        elif lage == "lesbar":
            assert cbor_canon.keys_admissible(data) is True, row
            assert _decode_weight(data, 8) == (1, None)
            obj_03, vermerke_03 = read_v_03(data)
            assert vermerke_03 == ()
            assert obj_03 is not None
            assert type(obj_03[0]) is int and obj_03[0] == 1
            obj_04, vermerk_04 = read_v_04(data)
            assert vermerk_04 is None
            assert obj_04 is not None
            assert type(obj_04[0]) is int and obj_04[0] == 1
        else:
            assert cbor_canon.keys_admissible(data) is True, row
            assert _decode_weight(data, 8) == (None, TrustFinding.NON_CANONICAL_V)
            assert read_v_03(data) == (None, (ProfileFinding.NON_CANONICAL_V,))
            assert read_v_04(data) == (None, GovernanceFinding.NON_CANONICAL_V)


def test_zeile_7_schluessel_0_ist_int_eins() -> None:
    """Lesbare Map: Key 0 ist der int 1, Gewicht 1, ohne Vermerk (02 §3.1, D456)."""
    data = bytes.fromhex("a400012000410002616103")
    assert cbor_canon.keys_admissible(data) is True
    assert _decode_weight(data, 8) == (1, None)
    obj_03, vermerke_03 = read_v_03(data)
    assert vermerke_03 == ()
    assert obj_03 is not None
    assert type(obj_03[0]) is int and obj_03[0] == 1
    obj_04, vermerk_04 = read_v_04(data)
    assert vermerk_04 is None
    assert obj_04 is not None
    assert type(obj_04[0]) is int and obj_04[0] == 1


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
