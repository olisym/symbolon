"""Nukleus-Policy: Override der Widerrufbarkeit für Nukleus-Prädikate (01 §5.4, 00 §5.2)."""

from __future__ import annotations

import hashlib
from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import Enum

from symbolon import cbor_canon

PROTOCOL_IRREVOCABLE = frozenset(
    {
        "obligation@1",
        "rotate-key@1",
        "rotate-ack@1",
        "device-add@1",
        "device-ack@1",
        "device-end@1",
    }
)  # Boden, D70 / D153 / D535 / 00 §5.2
TRUST_GRANTING = frozenset({"vouch@1"})  # Negativliste, D58 / 01 §5.4.3 b
_CORE_ENTRIES = frozenset({"revoke@1", "supersede@1"})  # D71

assert not (PROTOCOL_IRREVOCABLE & TRUST_GRANTING), (
    "D70/D58: der Boden darf nie in der Negativliste stehen"
)
assert not (PROTOCOL_IRREVOCABLE & _CORE_ENTRIES), (
    "D70/D71: der Boden darf nie ein core-Prädikat sein"
)


class PolicyWarning(str, Enum):
    UNSAFE_IRREVOCABLE_PREDICATE = "UNSAFE_IRREVOCABLE_PREDICATE"
    MALFORMED_IRREVOCABLE_ENTRY = "MALFORMED_IRREVOCABLE_ENTRY"


@dataclass(frozen=True, slots=True, order=True)
class PolicyNote:
    code: PolicyWarning
    predicate: str


def dedupe_sort(notes: list[PolicyNote] | tuple[PolicyNote, ...]) -> tuple[PolicyNote, ...]:
    """Warnings sortiert und dedupliziert (04a, D95-Nachzug)."""
    return tuple(sorted(set(notes)))


def constitution_hash(constitution_obj: dict) -> bytes:
    """SHA-256 der kanonischen Kodierung (00 §3, 04-prompt.md §0.2)."""
    return hashlib.sha256(cbor_canon.encode(constitution_obj)).digest()


def participants_wellformed(obj: dict) -> bool:
    """``participants`` deklariert, nicht leer, je 32 Byte, ohne Duplikat, aufsteigend (04 §3.5)."""
    if "participants" not in obj:
        return False
    raw = obj["participants"]
    if not isinstance(raw, (list, tuple)):
        return False
    if len(raw) == 0:
        return False
    seen: set[bytes] = set()
    ordered: list[bytes] = []
    for entry in raw:
        if not isinstance(entry, bytes) or len(entry) != 32:
            return False
        if entry in seen:
            return False
        seen.add(entry)
        ordered.append(entry)
    if ordered != sorted(ordered):
        return False
    return True


def _well_formed_irrevocable_entry(entry: object) -> bool:
    """Formkriterium aus D95: Profilname, bedeutungsblind."""
    if not isinstance(entry, str):
        return False
    if entry.count("@") != 1:
        return False
    left, right = entry.split("@")
    if not left or not right:
        return False
    if "/" in entry or ":" in entry:
        return False
    return True


@dataclass(frozen=True, slots=True)
class NucleusPolicy:
    """Policy eines Nukleus: welche Prädikate in ihrem Scope irrevocable sind."""

    scope: bytes
    declared: Iterable[object] = frozenset()
    irrevocable: frozenset[str] = field(init=False, default=frozenset())
    warnings: tuple[PolicyNote, ...] = field(init=False, default=())

    def __post_init__(self) -> None:
        raw = self.declared
        notes: list[PolicyNote] = []
        kept: list[str] = []
        if isinstance(raw, str):
            notes.append(
                PolicyNote(PolicyWarning.MALFORMED_IRREVOCABLE_ENTRY, repr(raw))
            )
        else:
            try:
                entries = list(raw)
            except TypeError:
                notes.append(
                    PolicyNote(PolicyWarning.MALFORMED_IRREVOCABLE_ENTRY, repr(raw))
                )
            else:
                for entry in entries:
                    if _well_formed_irrevocable_entry(entry):
                        kept.append(entry)
                    else:
                        subject = entry if isinstance(entry, str) else repr(entry)
                        notes.append(
                            PolicyNote(
                                PolicyWarning.MALFORMED_IRREVOCABLE_ENTRY, subject
                            )
                        )
        well_formed = frozenset(kept)
        irrevocable = (PROTOCOL_IRREVOCABLE | well_formed) - TRUST_GRANTING - _CORE_ENTRIES
        unsafe = well_formed & TRUST_GRANTING
        notes.extend(
            PolicyNote(PolicyWarning.UNSAFE_IRREVOCABLE_PREDICATE, predicate)
            for predicate in sorted(unsafe)
        )
        object.__setattr__(self, "irrevocable", frozenset(irrevocable))
        object.__setattr__(self, "warnings", dedupe_sort(notes))


def is_irrevocable(predicate: str, policy: NucleusPolicy | None) -> bool:
    """Wahr gdw. predicate ein nuc:-Prädikat ist und dessen Profilname
    (Teil nach dem letzten "/") in der wirksamen Menge liegt (01 §5.4.2).

    Die wirksame Menge ist ``policy.irrevocable``, falls ``policy`` gesetzt ist,
    sonst ``PROTOCOL_IRREVOCABLE`` (00 §5.2, D156, D159).
    """
    if not predicate.startswith("nuc:"):
        return False
    name = predicate.rsplit("/", 1)[-1]
    if policy is None:
        return name in PROTOCOL_IRREVOCABLE
    return name in policy.irrevocable


__all__ = [
    "PROTOCOL_IRREVOCABLE",
    "TRUST_GRANTING",
    "NucleusPolicy",
    "PolicyNote",
    "PolicyWarning",
    "constitution_hash",
    "dedupe_sort",
    "is_irrevocable",
    "participants_wellformed",
]
