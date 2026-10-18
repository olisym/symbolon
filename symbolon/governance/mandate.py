"""Mandat mit Rahmen: Bestellung, Zurechnung eines Akts, Ende (LANDKARTE §11, D710).

PROTOTYP des Supervisors, kein Normtext. Ein Mandat ist ein Sachfeld des Stands, dessen Name mit
``mandat:`` beginnt. Sein Wert ist der Eintrag ``{0: Inhaber, 1: Rahmen, 2: Bezeichnung}``,
optional ``3: letzter gedeckter Akt`` (das Ende). Der Rahmen ist ``{0: [Profilnamen]}``.
Der Inhaber zeichnet gegen mit ``mandate-ack@1``, ``J = [object-hash, mandate_id]``; er tritt
zurück mit ``mandate-end@1``, gleiches ``J``, ``v = {0: claim_id}`` wie ``device-end@1``.
Gelesen wird nur die Kette des Inhabers, keine Uhr (01 §7.3, 02 §2.1).

Die Geschichte (D711 Beschluss 1, 00e5): jeder Wert eines Mandatsfelds, der in einer Epoche der
Kette gestanden hat, aus der Verfassung, mit der sie beginnt, und je angewandtem Sachantrag dem
neuen Wert (04 §4.6). Nach dem Wechsel sind die festgestellten Sachanträge einer Epoche genau die
in ``S`` (04 §4.4 B2, B5), ``resolve_stand`` je Epoche liest also die richtige Menge. Ein Ende
bleibt je ``mandate_id``; verschwindet ein Mandat ohne Ende, ist jeder Akt danach offen.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from enum import Enum
from collections.abc import Iterable, Mapping

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id
from symbolon.errors import VerifierError
from symbolon.governance.chain import resolve_epoch, resolve_stand
from symbolon.governance.objects import Motion, Proposal
from symbolon.policy import constitution_hash
from symbolon.predicates import is_nuc_name, parse_predicate
from symbolon.trust.attribution import _endpoint, _is_ancestor
from symbolon.verifier import Classification, ClaimStore, State

DOM_NUC_MANDATE = b"claim-atom/v1/nucleus-mandate"
PREFIX = "mandat:"
_J_OBJECT = 3
_NAME = re.compile(r"^[a-z0-9_-]+@[1-9][0-9]*$")


class MandateStatus(str, Enum):
    """Lage eines Akts zu den Mandaten seines Autors in einem Scope."""

    COVERED = "covered"  # Akt der Gruppe
    OUTSIDE = "outside"  # Mandat steht, Akt liegt nicht im Rahmen
    BEFORE_ACK = "before-ack"
    AFTER_END = "after-end"
    UNDECIDED = "undecided"  # Lücke in der Kette oder Endpunkt unbekannt
    NONE = "none"  # kein wirksames Mandat dieses Autors


@dataclass(frozen=True, slots=True)
class Mandate:
    field: str
    mandate_id: bytes
    holder: bytes
    predicates: frozenset[str]
    label: str
    end: bytes | None  # Endpunkt aus dem Eintrag (Abruf)


def mandate_id(scope: bytes, core: dict) -> bytes:
    """SHA-256(DOM_NUC_MANDATE || cbor([scope, {0, 1, 2}]))."""
    return hashlib.sha256(DOM_NUC_MANDATE + cbor_canon.encode([scope, core])).digest()


def parse_entry(scope: bytes, field: str, value: object) -> Mandate | None:
    """Ein Eintrag nach der Form oben, sonst ``None`` (formwidrig)."""
    if not isinstance(value, dict) or not all(type(k) is int for k in value):
        return None
    if not {0, 1, 2} <= set(value) <= {0, 1, 2, 3}:
        return None
    holder, frame, label = value[0], value[1], value[2]
    if not isinstance(holder, bytes) or len(holder) != 32 or not isinstance(label, str):
        return None
    if not isinstance(frame, dict) or set(frame) != {0}:
        return None
    names = frame[0]
    if not isinstance(names, list) or not names:
        return None
    if not all(isinstance(n, str) and _NAME.match(n) for n in names):
        return None
    if any(a >= b for a, b in zip(names, names[1:])):
        return None
    end = value.get(3)
    if end is not None and (not isinstance(end, bytes) or len(end) != 32):
        return None
    core = {0: holder, 1: frame, 2: label}
    return Mandate(field, mandate_id(scope, core), holder, frozenset(names), label, end)


def mandates_of(stand_obj: dict | None, scope: bytes) -> tuple[list[Mandate], list[str]]:
    """Die wohlgeformten Mandate des Stands und die Namen formwidriger Mandatsfelder."""
    good: list[Mandate] = []
    bad: list[str] = []
    if not isinstance(stand_obj, dict):
        return good, bad
    for name in sorted(k for k in stand_obj if isinstance(k, str) and k.startswith(PREFIX)):
        m = parse_entry(scope, name, stand_obj[name])
        if m is None:
            bad.append(name)
        else:
            good.append(m)
    return good, bad


def _act_name(claim: Claim) -> str | None:
    try:
        parsed = parse_predicate(claim.p)
    except VerifierError:
        return None
    if parsed.namespace != "nuc":
        return None
    return f"{parsed.name}@{parsed.version}"


@dataclass(frozen=True, slots=True)
class _Effective:
    mandate: Mandate
    ack: bytes
    ends: tuple[bytes, ...]
    open_end: bool  # verschwunden, und keine gestandene Fassung nannte ein Ende


@dataclass(frozen=True, slots=True)
class MandateView:
    store: ClaimStore
    scope: bytes
    effective: tuple[_Effective, ...]
    malformed: tuple[str, ...]

    def _one(self, eff: _Effective, claim: Claim) -> MandateStatus:
        after_ack = _is_ancestor(self.store, eff.ack, claim)
        if after_ack is False:
            return MandateStatus.BEFORE_ACK
        undecided = after_ack is None
        cid = claim_id(claim)
        for endpoint in eff.ends:
            end_claim = self.store.get(endpoint)
            if end_claim is None:
                undecided = True
                continue
            within = _is_ancestor(self.store, cid, end_claim)
            if within is False:
                return MandateStatus.AFTER_END
            if within is None:
                undecided = True
        if undecided or eff.open_end:
            return MandateStatus.UNDECIDED
        if _act_name(claim) not in eff.mandate.predicates:
            return MandateStatus.OUTSIDE
        return MandateStatus.COVERED

    def status(self, claim: Claim) -> MandateStatus:
        if claim.N != self.scope:
            return MandateStatus.NONE
        mine = [e for e in self.effective if e.mandate.holder == claim.I]
        if not mine:
            return MandateStatus.NONE
        results = [self._one(e, claim) for e in mine]
        for wanted in (
            MandateStatus.COVERED,
            MandateStatus.UNDECIDED,
            MandateStatus.OUTSIDE,
            MandateStatus.AFTER_END,
        ):
            if wanted in results:
                return wanted
        return MandateStatus.BEFORE_ACK


def stood_entries(
    constitution_obj: dict | None, applied: Iterable[Motion]
) -> list[tuple[str, object]]:
    """Jeder Wert eines Mandatsfelds, der in einer Epoche gestanden hat, ohne Reihenfolge."""
    out: list[tuple[str, object]] = []
    if isinstance(constitution_obj, dict):
        for name in sorted(k for k in constitution_obj if isinstance(k, str)):
            if name.startswith(PREFIX):
                out.append((name, constitution_obj[name]))
    for motion in applied:
        for name, pair in motion.changes.items():
            if name.startswith(PREFIX) and len(pair[1]) == 1:
                out.append((name, pair[1][0]))
    return out


@dataclass(frozen=True, slots=True)
class MandateHistory:
    constitution_obj: dict | None  # der geltenden Epoche
    stand_obj: dict | None  # der geltenden Epoche
    entries: tuple[tuple[str, object], ...]  # über alle Epochen der Kette


def mandate_history(
    store: ClaimStore,
    *,
    scope: bytes,
    genesis_obj: dict,
    known_constitutions: Mapping[bytes, dict],
    known_proposals: Mapping[bytes, Proposal | Motion],
    now: int,
) -> MandateHistory:
    """Stand der geltenden Epoche und alle gestandenen Mandatswerte der Kette (04 §4.5)."""
    res = resolve_epoch(store, scope=scope, genesis_obj=genesis_obj,
                        known_constitutions=known_constitutions,
                        known_proposals=known_proposals, now=now)
    entries: list[tuple[str, object]] = []
    stand_obj: dict | None = None
    constitution_obj: dict | None = None
    for epoch in res.chain:
        constitution_obj = known_constitutions.get(epoch.constitution_hash)
        if constitution_obj is not None and constitution_hash(constitution_obj) != (
            epoch.constitution_hash
        ):
            constitution_obj = None
        sr = resolve_stand(store, epoch=epoch, genesis_obj=genesis_obj,
                           constitution_obj=constitution_obj,
                           known_proposals=known_proposals, now=now)
        applied = [known_proposals[h] for h in sr.applied]
        entries.extend(stood_entries(constitution_obj, applied))
        stand_obj = sr.stand_obj
    return MandateHistory(constitution_obj, stand_obj, tuple(entries))


def mandate_view(
    store: ClaimStore,
    classifications: dict[bytes, Classification],
    scope: bytes,
    stand_obj: dict | None,
    history: Iterable[tuple[str, object]] = (),
) -> MandateView:
    """Wirksame Mandate: im Stand oder in der Geschichte, gegengezeichnet vom Inhaber, mit ihren
    Endpunkten."""
    current, bad = mandates_of(stand_obj, scope)
    current_ids = {m.mandate_id for m in current}
    variants: dict[bytes, list[Mandate]] = {}
    malformed = set(bad)
    for m in current:
        variants.setdefault(m.mandate_id, []).append(m)
    for name, value in history:
        m = parse_entry(scope, name, value)
        if m is None:
            malformed.add(name)
        else:
            variants.setdefault(m.mandate_id, []).append(m)
    mandates = [vs[0] for vs in variants.values()]
    by_id = {m.mandate_id: m for m in mandates}
    acks: dict[bytes, list[Claim]] = {}
    ends: dict[bytes, list[Claim]] = {}
    for c in store.all_claims():
        if c.N != scope or c.t_exp is not None:
            continue
        cl = classifications.get(claim_id(c))
        if cl is None or cl.state is not State.ACTIVE or c.J[0] != _J_OBJECT:
            continue
        m = by_id.get(c.J[1])
        if m is None or c.I != m.holder:
            continue
        if is_nuc_name(c, "mandate-ack"):
            acks.setdefault(m.mandate_id, []).append(c)
        elif is_nuc_name(c, "mandate-end"):
            ends.setdefault(m.mandate_id, []).append(c)

    effective: list[_Effective] = []
    for m in mandates:
        own = acks.get(m.mandate_id, [])
        binding = next(
            (k for k in own if all(_is_ancestor(store, claim_id(k), o) is True for o in own)),
            None,
        )
        if binding is None:
            continue
        ack_id = claim_id(binding)
        stood_ends = {v.end for v in variants[m.mandate_id] if v.end is not None}
        points: list[bytes] = sorted(stood_ends)
        open_end = m.mandate_id not in current_ids and not stood_ends
        for e in ends.get(m.mandate_id, []):
            ep = _endpoint(e.v)
            points.append(ack_id if ep is None else ep)
        effective.append(_Effective(m, ack_id, tuple(sorted(points)), open_end))
    return MandateView(store, scope, tuple(effective), tuple(sorted(malformed)))


__all__ = [
    "DOM_NUC_MANDATE",
    "Mandate",
    "MandateHistory",
    "MandateStatus",
    "MandateView",
    "mandate_history",
    "mandate_id",
    "mandate_view",
    "mandates_of",
    "parse_entry",
    "stood_entries",
]
