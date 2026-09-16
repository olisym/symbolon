"""Geteilte Ableitungsstufe zwischen 02 §4 (trust) und 02 §5 (rank) (02b §2, D49).

Reine Extraktion aus dem, was vorher in flow.py::trust() inline stand (02 §11.4 Schritte
1-6): classify_all -> Gruppen -> Budget/OVERCOMMITTED_AUTHOR -> Flag-Anwendung -> BFS über
E+. trust() baut darauf den Knoten-Split und Dinic; rank() (02b) rechnet direkt auf den
E+-Kanten, ohne Split (D49: kein Knoten-Splitting, das Budget-Set spielt für 02 §5 keine Rolle
mehr, C(x) geht nur als Filter ein).
"""

from __future__ import annotations

from dataclasses import dataclass

from symbolon.atom import claim_id
from symbolon.index import classify_all
from symbolon.verifier import ClaimStore, State

from .findings import Finding, TrustFinding
from .graph import BfsResult, bfs_capacities
from .groups import build_groups
from .params import TrustParams


@dataclass(frozen=True, slots=True)
class Derivation:
    """`bfs` traegt Distanzen, Knotenkapazitaeten und den E+-Kantensatz (mit n_kante);
    `findings` ist bereits die volle, sortierte, deduplizierte Menge (Payload- und
    Budget-Findings aus der Gruppenbildung plus SUBGRANULAR_VOUCH aus der BFS)."""

    bfs: BfsResult
    findings: tuple[Finding, ...]


def derive(
    store: ClaimStore,
    *,
    anchors: frozenset[bytes],
    scope: bytes,
    now: int,
    params: TrustParams,
    include_flagged: bool = False,
) -> Derivation:
    # 1. classify_all
    classifications = classify_all(store, now)
    claims = store.all_claims()

    # 2-3. Vouch-Claims des Scopes sammeln, v dekodieren, Gruppen bilden
    groups, payload_findings = build_groups(claims, classifications, scope, params.D, now)

    # 4. Budget je Autor prüfen -> OVERCOMMITTED_AUTHOR
    budget_by_author: dict[bytes, int] = {}
    for (author, _subject), group in groups.items():
        budget_by_author[author] = budget_by_author.get(author, 0) + group.n_budget
    overcommitted_authors = {
        author for author, total in budget_by_author.items() if total > params.D
    }
    overcommit_findings = tuple(
        Finding(kind=TrustFinding.OVERCOMMITTED_AUTHOR, subject=author)
        for author in overcommitted_authors
    )

    equivocation_flagged_authors = {
        c.I
        for c in claims
        if classifications[claim_id(c)].state == State.EQUIVOCATION_FLAGGED
    }
    flagged_authors = overcommitted_authors | equivocation_flagged_authors

    # 5. Flags anwenden -> Kantenkandidaten
    if include_flagged:
        candidate_groups = groups
    else:
        candidate_groups = {
            key: group for key, group in groups.items() if group.author not in flagged_authors
        }

    # 6. BFS über E+ -> d, C, cap, SUBGRANULAR_VOUCH
    bfs_result = bfs_capacities(anchors, candidate_groups, params)

    all_findings = tuple(
        sorted(set(payload_findings) | set(overcommit_findings) | set(bfs_result.findings))
    )

    return Derivation(bfs=bfs_result, findings=all_findings)
