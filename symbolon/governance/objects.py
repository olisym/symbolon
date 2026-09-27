"""Epochen-, Vorschlags- und Sachantragsidentität (04 §1.1, 04 §2.4, 04 §2.5, 04 §4.6)."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from symbolon import cbor_canon
from symbolon.domains import DOM_NUC_EPOCH, DOM_NUC_MOTION, DOM_NUC_PROPOSAL

# Die Regelfelder einer Verfassung; jedes andere Feld ist ein Sachfeld (04 §1.1, D565).
RULE_FIELDS = frozenset(
    {
        "participants",
        "thresholds",
        "irrevocable_predicates",
        "arbitration",
        "enforcement_policy",
        "nucleus_keys",
    }
)


def epoch_id(scope: bytes, index: int, constitution_hash: bytes) -> bytes:
    """SHA-256(DOM_NUC_EPOCH || cbor([scope, index, constitution_hash]))."""
    return hashlib.sha256(
        DOM_NUC_EPOCH + cbor_canon.encode([scope, index, constitution_hash])
    ).digest()


def proposal_hash(
    scope: bytes, predecessor: bytes, constitution_hash: bytes, motions: object = None
) -> bytes:
    """SHA-256(DOM_NUC_PROPOSAL || cbor({0: scope, 1: predecessor, 2: constitution_hash}));
    Key 3 nur, wenn ``motions`` nicht ``None`` ist (04 §2.4)."""
    obj: dict = {0: scope, 1: predecessor, 2: constitution_hash}
    if motions is not None:
        obj[3] = motions
    return hashlib.sha256(DOM_NUC_PROPOSAL + cbor_canon.encode(obj)).digest()


@dataclass(frozen=True, slots=True)
class Epoch:
    """Abgeleitete Epochenidentität (04-governance.md §1.1)."""

    scope: bytes
    index: int
    constitution_hash: bytes

    @property
    def epoch_id(self) -> bytes:
        return epoch_id(self.scope, self.index, self.constitution_hash)


@dataclass(frozen=True, slots=True)
class Proposal:
    """Content-adressiertes Vorschlagsobjekt (04-governance.md §2.4).

    ``motions`` ist Feld 3, wie es kam; ``None`` heisst, das Feld fehlt (D569 Beschluss 2).
    """

    scope: bytes
    predecessor: bytes
    constitution_hash: bytes
    motions: object = None

    @property
    def proposal_hash(self) -> bytes:
        return proposal_hash(self.scope, self.predecessor, self.constitution_hash, self.motions)


def motion_list(proposal: Proposal) -> tuple[bytes, ...] | None:
    """Die Liste ``S`` aus Feld 3: ``()`` ohne Feld 3, ``None`` wenn es formwidrig ist
    (04 §2.4)."""
    motions = proposal.motions
    if motions is None:
        return ()
    if not isinstance(motions, (list, tuple)) or not motions:
        return None
    if not all(isinstance(h, bytes) and len(h) == 32 for h in motions):
        return None
    if any(a >= b for a, b in zip(motions, motions[1:])):
        return None
    return tuple(motions)


@dataclass(frozen=True, slots=True)
class Motion:
    """Content-adressiertes Sachantragsobjekt, wie es kam (04 §2.5, D569 Beschluss 2)."""

    obj: object

    @property
    def motion_hash(self) -> bytes:
        """SHA-256(DOM_NUC_MOTION || cbor(motion)) (04 §2.5)."""
        return hashlib.sha256(DOM_NUC_MOTION + cbor_canon.encode(self.obj)).digest()

    @property
    def scope(self) -> object:
        return self.obj.get(0) if isinstance(self.obj, dict) else None

    @property
    def predecessor(self) -> object:
        return self.obj.get(1) if isinstance(self.obj, dict) else None

    @property
    def changes(self) -> object:
        return self.obj.get(2) if isinstance(self.obj, dict) else None


def value_key(v: object) -> bytes:
    """Die deterministische Kodierung eines Werts ``[]`` oder ``[w]`` (04 §2.5, D567
    Beschluss 4)."""
    return cbor_canon.encode(v)


def same_value(a: object, b: object) -> bool:
    """Gleichheit zweier Werte als Byte-Gleichheit ihrer Kodierung (04 §2.5)."""
    return value_key(a) == value_key(b)


def _is_hash(value: object) -> bool:
    return isinstance(value, bytes) and len(value) == 32


def _is_value(value: object) -> bool:
    return isinstance(value, (list, tuple)) and len(value) in (0, 1)


def motion_wellformed(motion: Motion) -> bool:
    """Form eines Sachantrags, am Objekt allein entscheidbar (04 §2.5)."""
    obj = motion.obj
    if not isinstance(obj, dict):
        return False
    if not all(type(k) is int for k in obj) or set(obj) != {0, 1, 2}:
        return False
    if not _is_hash(obj[0]) or not _is_hash(obj[1]):
        return False
    changes = obj[2]
    if not isinstance(changes, dict) or not changes:
        return False
    for name, pair in changes.items():
        if not isinstance(name, str) or name in RULE_FIELDS:
            return False
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            return False
        alt, neu = pair
        if not _is_value(alt) or not _is_value(neu):
            return False
        if same_value(alt, neu):
            return False
    return True


def preconditions(motion: Motion) -> frozenset[tuple[str, bytes]]:
    """Die Vorbedingungen, je Feld das Paar aus Feldname und ``value_key(alt)`` (04 §2.5,
    04 §4.4)."""
    return frozenset((name, value_key(pair[0])) for name, pair in motion.changes.items())


def apply_motions(
    constitution_obj: dict, motions: list[Motion] | tuple[Motion, ...]
) -> tuple[dict, tuple[bytes, ...]]:
    """Der Stand aus ``constitution_obj`` und ``motions`` und die aufsteigend sortierten
    ``motion_hash`` der angewandten (04 §4.6).

    Wendet in der gereichten Reihenfolge den ersten anwendbaren an, bis keiner mehr anwendbar
    ist, jeden höchstens einmal (D569 Beschluss 2). ``constitution_obj`` bleibt unverändert.
    """
    stand = dict(constitution_obj)
    applied: list[bytes] = []
    while True:
        for motion in motions:
            if motion.motion_hash in applied:
                continue
            if all(
                same_value([stand[name]] if name in stand else [], pair[0])
                for name, pair in motion.changes.items()
            ):
                break
        else:
            return stand, tuple(sorted(applied))
        for name, pair in motion.changes.items():
            neu = pair[1]
            if len(neu) == 1:
                stand[name] = neu[0]
            else:
                stand.pop(name, None)
        applied.append(motion.motion_hash)
