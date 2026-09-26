#!/usr/bin/env python3
"""Referenzdrucker in der Blockform der Aufträge (D391, rs/AUFTRAG.md Schnittstelle).

Druckt, was die Referenz rechnet. Kein Orakel, keine eigene Rechnung.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from symbolon.trust import TrustParams, classify_all, trust
from symbolon.trust.attribution import attribution
from symbolon.trust.graph import bfs_capacities, infinity
from symbolon.trust.groups import build_groups
from symbolon.verifier import InMemoryStore, State, structural_check

KEYWORDS = (
    "profil",
    "zustand",
    "gruppe",
    "budget",
    "kante",
    "inf",
    "fluss",
    "simultan",
    "disjunkt",
    "schnitt",
    "befund",
)


def _hex(data: bytes) -> str:
    return data.hex()


def _state_name(state: State) -> str:
    """Zustand in der gedruckten Schreibweise aus 01-claim-atom.md Anhang B.1."""
    return state.value.replace("_", "-")


def _num_or_inf(value: int | None) -> str:
    return "inf" if value is None else str(value)


def load_profiles(path: Path) -> list[dict[str, Any]]:
    """Vektordatei lesen. Die Datei ist eine JSON-Liste von Profilen."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise TypeError(f"{path}: expected a JSON list of profiles")
    return payload


def store_from_claims(wires: list[str]) -> InMemoryStore:
    """Claims in Bau-Reihenfolge einlesen und halten (01 §6)."""
    store = InMemoryStore()
    for wire in wires:
        claim = structural_check(bytes.fromhex(wire), store)
        store.add(claim)
    return store


def format_block(profile: dict[str, Any]) -> list[str]:
    """Ein Profil in die Blockform aus rs/AUFTRAG.md, Schnittstelle."""
    params_raw = profile["params"]
    params = TrustParams(
        C0=params_raw["C0"],
        gamma_num=params_raw["gamma_num"],
        gamma_den=params_raw["gamma_den"],
        D=params_raw["D"],
    )
    now = profile["now"]
    scope = bytes.fromhex(profile["scope"])
    anchors = frozenset(bytes.fromhex(item) for item in profile["anchors"])
    targets = frozenset(bytes.fromhex(item) for item in profile["targets"])
    store = store_from_claims(profile["claims"])
    claims = store.all_claims()

    classifications = classify_all(store, now)
    # Mit Zurechnung wie derive (D542 Beschluss 4, D543 Beschluss 5, 02 §2.1).
    groups, _payload_findings = build_groups(
        claims, classifications, scope, params.D, now, attribution(store, classifications, scope)
    )
    # include_flagged=True: dieselben Gruppen, die derive ungefiltert an die BFS reicht.
    bfs = bfs_capacities(anchors, groups, params)
    inf_value = infinity(bfs)
    simultaneous = trust(
        store,
        anchors=anchors,
        targets=targets,
        scope=scope,
        now=now,
        params=params,
        include_flagged=True,
    )

    lines: list[str] = [f"profil {profile['profil']}"]

    for cid in sorted(classifications):
        lines.append(
            f"zustand {_hex(cid)} {_state_name(classifications[cid].state)}"
        )

    for author, subject in sorted(groups):
        group = groups[(author, subject)]
        lines.append(
            f"gruppe {_hex(author)} {_hex(subject)} {group.n_budget} {group.n_kante}"
        )

    budget_by_author: dict[bytes, int] = {}
    for group in groups.values():
        budget_by_author[group.author] = (
            budget_by_author.get(group.author, 0) + group.n_budget
        )
    for author in sorted(budget_by_author):
        total = budget_by_author[author]
        verdikt = "over" if total > params.D else "ok"
        lines.append(f"budget {_hex(author)} {total} {verdikt}")

    for edge in bfs.edges:
        d = bfs.distance.get(edge.author)
        c_author = bfs.node_capacity.get(edge.author)
        lines.append(
            "kante "
            f"{_hex(edge.author)} {_hex(edge.subject)} "
            f"{_num_or_inf(d)} {_num_or_inf(c_author)} {edge.cap}"
        )

    lines.append(f"inf {inf_value}")

    for target in sorted(targets):
        single = trust(
            store,
            anchors=anchors,
            targets=frozenset({target}),
            scope=scope,
            now=now,
            params=params,
            include_flagged=True,
        )
        lines.append(f"fluss {_hex(target)} {single.value}")

    lines.append(f"simultan {simultaneous.value}")
    lines.append(f"disjunkt {simultaneous.disjoint_paths}")

    if simultaneous.cut:
        identities = " ".join(_hex(identity) for identity in simultaneous.cut)
        lines.append(f"schnitt {identities}")
    else:
        lines.append("schnitt")

    for finding in simultaneous.findings:
        lines.append(f"befund {finding.kind.value} {_hex(finding.subject)}")

    return lines


def render(path: Path) -> str:
    """Alle Profile der Datei, in Dateireihenfolge, ohne Leerzeilen dazwischen."""
    lines: list[str] = []
    for profile in load_profiles(path):
        lines.extend(format_block(profile))
    return "\n".join(lines) + ("\n" if lines else "")


def main() -> None:
    if len(sys.argv) != 2:
        sys.stderr.write("usage: ref_block.py <vectors.json>\n")
        raise SystemExit(2)
    sys.stdout.write(render(Path(sys.argv[1])))


if __name__ == "__main__":
    main()
