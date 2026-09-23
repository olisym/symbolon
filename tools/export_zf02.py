#!/usr/bin/env python3
"""ZF-02 als sprachneutrale Eingabe (D438, 01 §6, 02 §3.1)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from symbolon.atom import signed_bytes
from tests.trust.zf02 import PARAMS, Graph, iter_profiles

VECTORS_PATH = ROOT / "tests" / "vectors" / "vectors_02_zf02.json"


def _entry(profil: str, graph: Graph, now: int) -> dict[str, object]:
    """Ein Profil: Parameter, Identitäten und Claims in Bau-Reihenfolge."""
    return {
        "anchors": [graph.identities["ALICE"].pub.hex()],
        "claims": [signed_bytes(claim).hex() for claim in graph.claims],
        "labels": {
            name: ident.pub.hex() for name, ident in graph.identities.items()
        },
        "now": now,
        "params": {
            "C0": PARAMS.C0,
            "D": PARAMS.D,
            "gamma_den": PARAMS.gamma_den,
            "gamma_num": PARAMS.gamma_num,
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
    """F1–F3 — Reihenfolge und Werte aus zf02.py (D438)."""
    return [_entry(name, graph, now) for name, graph, now in iter_profiles()]


def dumps(profiles: list[dict[str, object]]) -> str:
    """JSON mit Einrückung 2, sortierten Schlüsseln, abschliessendem Zeilenumbruch."""
    return json.dumps(profiles, indent=2, sort_keys=True) + "\n"


def main() -> None:
    text = dumps(build_profiles())
    VECTORS_PATH.write_text(text, encoding="utf-8", newline="\n")
    print(f"Wrote {VECTORS_PATH}")


if __name__ == "__main__":
    main()
