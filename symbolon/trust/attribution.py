"""Zurechnung an die Wurzel (02 §2.1, 01 §7.3, D529 bis D536).

Liest die Zustände aus ``classify_all`` derselben Auswertung und klassifiziert nicht selbst
(02 §11.4 Schritt 1). Alles gilt je Scope ``N``; die Bestimmung liest nur Ketten, keine Uhr.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id
from symbolon.predicates import is_nuc_name
from symbolon.verifier import (
    Classification,
    ClaimStore,
    State,
    _predecessor_known_and_valid,
)

_J_TAG_IDENTITY = 1
_J_TAG_CLAIM_REF = 2


class AttributionStatus(str, Enum):
    """Lage eines Claims zur Zurechnung (02 §2.1)."""

    OWN = "own"
    ATTRIBUTED = "attributed"
    BEFORE_ACK = "before-ack"
    DISPUTED = "disputed"
    UNDECIDED = "undecided"


@dataclass(frozen=True, slots=True)
class _Device:
    """Ein wirksam aufgenommenes Gerät: Wurzel, bindendes Ack, Endpunkte (02 §2.1)."""

    root: bytes
    ack: bytes
    ends: tuple[bytes, ...]


def _is_ancestor(store: ClaimStore, ancestor: bytes, claim: Claim) -> bool | None:
    """Ist ``ancestor`` Vorfahr von ``claim`` über ``h_prev``? ``None``: eine Lücke (02 §2.1).

    Ein Claim ist sein eigener Vorfahr. Ein Glied gilt als vorhanden wie in der
    Vorgängerprüfung der Zustandsmaschine (01 §6).
    """
    current = claim
    while True:
        if claim_id(current) == ancestor:
            return True
        known, pred = _predecessor_known_and_valid(current, store)
        if not known:
            return None
        if pred is None:
            return False
        current = pred


def _endpoint(v: bytes | None) -> bytes | None:
    """Endpunkt aus ``v`` eines ``device-end@1`` (01 §7.3); ``None`` heisst Ende beim Ack.

    Gelesen wie ``v`` einer Bürgschaft (02 §3.1): zulässige Schlüssel, kanonisch, eine Map,
    Key ``0`` eine ``bstr`` der Länge 32.
    """
    if v is None:
        return None
    try:
        obj = cbor_canon.decode(v)
        if not cbor_canon.keys_admissible(v):
            return None
        canonical = cbor_canon.is_canonical(v)
    except Exception:
        return None
    if not canonical or not isinstance(obj, dict):
        return None
    value = obj.get(0)
    if not isinstance(value, bytes) or len(value) != 32:
        return None
    return value


@dataclass(frozen=True, slots=True)
class Attribution:
    """Ergebnis von :func:`attribution` für einen Scope (02 §2.1)."""

    store: ClaimStore
    scope: bytes
    devices: dict[bytes, _Device]

    def status(self, claim: Claim) -> AttributionStatus:
        """Lage von ``claim`` in diesem Scope (02 §2.1, „Zurechnung“, „Ohne Uhr“)."""
        if claim.N != self.scope:
            return AttributionStatus.OWN
        device = self.devices.get(claim.I)
        if device is None:
            return AttributionStatus.OWN
        after_ack = _is_ancestor(self.store, device.ack, claim)
        if after_ack is False:
            return AttributionStatus.BEFORE_ACK
        undecided = after_ack is None
        cid = claim_id(claim)
        for endpoint in device.ends:
            end_claim = self.store.get(endpoint)
            if end_claim is None:
                undecided = True
                continue
            within = _is_ancestor(self.store, cid, end_claim)
            if within is False:
                return AttributionStatus.DISPUTED
            if within is None:
                undecided = True
        if undecided:
            return AttributionStatus.UNDECIDED
        return AttributionStatus.ATTRIBUTED

    def device_root(self, key: bytes) -> bytes | None:
        """Wurzel des in diesem Scope wirksam aufgenommenen Geräts ``key``, sonst ``None``
        (02 §2.1, „Wirksame Aufnahme“)."""
        device = self.devices.get(key)
        if device is None:
            return None
        return device.root

    def root(self, claim: Claim) -> bytes:
        """Wurzel für Kanten: die Wurzel bei ``ATTRIBUTED``, sonst ``claim.I`` (02 §2.1)."""
        if self.status(claim) is AttributionStatus.ATTRIBUTED:
            return self.devices[claim.I].root
        return claim.I

    def budget_root(self, claim: Claim) -> bytes:
        """Wurzel für das Budget-Set: die Wurzel, solange nicht erwiesen ist, dass
        ``claim`` vor dem Ack liegt oder bestritten ist (02 §2.1, „Budget-Set“)."""
        status = self.status(claim)
        if status in (AttributionStatus.ATTRIBUTED, AttributionStatus.UNDECIDED):
            return self.devices[claim.I].root
        return claim.I


def attribution(
    store: ClaimStore,
    classifications: dict[bytes, Classification],
    scope: bytes,
) -> Attribution:
    """Wirksame Aufnahmen und Enden im Scope ``scope`` bestimmen (02 §2.1).

    ``classifications`` ist das Ergebnis von ``classify_all`` derselben Auswertung
    (02 §11.4 Schritt 1).
    """
    adds: dict[bytes, Claim] = {}
    acks: list[Claim] = []
    ends: list[Claim] = []
    for c in store.all_claims():
        if c.N != scope or c.t_exp is not None:
            continue
        cid = claim_id(c)
        classification = classifications.get(cid)
        if classification is None or classification.state is not State.ACTIVE:
            continue
        if is_nuc_name(c, "device-add"):
            adds[cid] = c
        elif is_nuc_name(c, "device-ack"):
            acks.append(c)
        elif is_nuc_name(c, "device-end"):
            ends.append(c)

    # Geräte nehmen keine Geräte auf: gelesen wird nur, ob die Wurzel ein Ack mit J-Tag
    # claim-ref gezeichnet hat; ein formwidriges Ack nimmt nichts (D537).
    acting_as_device = {k.I for k in acks if k.J[0] == _J_TAG_CLAIM_REF}
    valid_adds = {
        cid: a
        for cid, a in adds.items()
        if a.J[0] == _J_TAG_IDENTITY and a.J[1] != a.I and a.I not in acting_as_device
    }

    candidates: dict[bytes, list[Claim]] = {}
    for k in acks:
        if k.J[0] != _J_TAG_CLAIM_REF:
            continue
        add = valid_adds.get(k.J[1])
        if add is None or add.J[1] != k.I:
            continue
        candidates.setdefault(k.I, []).append(k)

    devices: dict[bytes, _Device] = {}
    for device_key, device_acks in candidates.items():
        binding = next(
            (
                k
                for k in device_acks
                if all(_is_ancestor(store, claim_id(k), other) is True for other in device_acks)
            ),
            None,
        )
        if binding is None:
            continue
        root = valid_adds[binding.J[1]].I
        ack_id = claim_id(binding)
        endpoints: list[bytes] = []
        for e in ends:
            if e.I != root or e.J[0] != _J_TAG_IDENTITY or e.J[1] != device_key:
                continue
            endpoint = _endpoint(e.v)
            endpoints.append(ack_id if endpoint is None else endpoint)
        devices[device_key] = _Device(root=root, ack=ack_id, ends=tuple(sorted(endpoints)))

    return Attribution(store=store, scope=scope, devices=devices)


__all__ = ["Attribution", "AttributionStatus", "attribution"]
