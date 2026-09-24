"""Genesis-Scope: Hash nach der Schlüsselprüfung (00 §4, D462)."""

from __future__ import annotations

import hashlib

from symbolon import cbor_canon
from symbolon.domains import DOM_NUC_GEN


def genesis_scope(genesis_obj: dict) -> bytes:
    """Hash des Genesis; jeder Map-Schlüssel ist ein uint (00 §4, D462)."""
    pending: list[object] = [genesis_obj]
    while pending:
        node = pending.pop()
        if isinstance(node, dict):
            for key, value in node.items():
                if type(key) is not int or key < 0:
                    raise ValueError("genesis_obj has a non-uint map key")
                pending.append(value)
        elif isinstance(node, (list, tuple)):
            pending.extend(node)
    return hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis_obj)).digest()
