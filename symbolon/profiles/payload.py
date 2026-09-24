"""v lesen: typ-normativ, bedeutungsblind (03-profiles.md §1.3, D77/D83)."""

from __future__ import annotations

from symbolon import cbor_canon
from symbolon.profiles.findings import ProfileFinding


def read_v(v: bytes | None) -> tuple[dict | None, tuple[ProfileFinding, ...]]:
    """Dekodiert ``v`` und prüft Kanonizität; Subjekt setzt der Aufrufer (03-profiles.md §1.3).

    Reihenfolge ist normativ (D83): ``decode`` und ``is_canonical`` im selben ``try``.
    """
    if v is None:
        return None, ()
    try:
        obj = cbor_canon.decode(v)
        if not cbor_canon.keys_admissible(v):
            return None, (ProfileFinding.UNPARSABLE_V,)
        canonical = cbor_canon.is_canonical(v)
    except Exception:
        return None, (ProfileFinding.UNPARSABLE_V,)
    if not canonical:
        return None, (ProfileFinding.NON_CANONICAL_V,)
    if not isinstance(obj, dict):
        return None, (ProfileFinding.UNPARSABLE_V,)
    return obj, ()
