#!/usr/bin/env python3
"""FALL-02 als sprachneutrale Eingabe (02 §3, 02 §4)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from symbolon.atom import signed_bytes
from tests.trust.fall02 import NOW, PARAMS, PROFILES, Graph, build

VECTORS_PATH = ROOT / "tests" / "vectors" / "vectors_02_fall02.json"


def _entry(profil: str, graph: Graph) -> dict[str, object]:
    """Ein Profil: Parameter, Identitäten und Claims in Bau-Reihenfolge."""
    params = PARAMS[profil]
    return {
        "anchors": [graph.identities["ALICE"].pub.hex()],
        "claims": [signed_bytes(claim).hex() for claim in graph.claims],
        "labels": {
            name: ident.pub.hex() for name, ident in graph.identities.items()
        },
        "now": NOW,
        "params": {
            "C0": params.C0,
            "D": params.D,
            "gamma_den": params.gamma_den,
            "gamma_num": params.gamma_num,
        },
        "profil": profil,
        "scope": graph.scope.hex(),
        "targets": [
            graph.identities["g1"].pub.hex(),
            graph.identities["g2"].pub.hex(),
            graph.identities["g3"].pub.hex(),
        ],
    }


def build_profiles() -> list[dict[str, object]]:
    """R1, R2, R3 — Reihenfolge und Werte aus fall02.py."""
    return [_entry(name, build(name)) for name in PROFILES]


def dumps(profiles: list[dict[str, object]]) -> str:
    """JSON mit Einrückung 2, sortierten Schlüsseln, abschliessendem Zeilenumbruch."""
    return json.dumps(profiles, indent=2, sort_keys=True) + "\n"


def main() -> None:
    text = dumps(build_profiles())
    VECTORS_PATH.write_text(text, encoding="utf-8", newline="\n")
    print(f"Wrote {VECTORS_PATH}")


if __name__ == "__main__":
    main()
