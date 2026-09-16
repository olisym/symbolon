"""Aktiv-Set/Budget-Kanten -> BFS mit Kapazitätsfilter -> Knoten-Split-Graph (02 §3, 02 §4)."""

from __future__ import annotations

from dataclasses import dataclass

from .findings import Finding, TrustFinding
from .groups import Group
from .params import TrustParams

SOURCE = "S*"
SINK = "T*"


def node_in(identity: bytes) -> tuple[str, bytes]:
    return ("in", identity)


def node_out(identity: bytes) -> tuple[str, bytes]:
    return ("out", identity)


def capacity(params: TrustParams, d: int | None) -> int:
    """C(d) = ⌊C0 · γ^d⌋; C(∞) = 0 (02 §3). Einmal am Ende gerundet."""
    if d is None:
        return 0
    return (params.C0 * params.gamma_num**d) // (params.gamma_den**d)


@dataclass(frozen=True, slots=True)
class Edge:
    author: bytes
    subject: bytes
    cap: int
    claim_id: bytes
    n_kante: int  # Gruppengewicht vor der C(I)-Gewichtung; von rank() gelesen (02b §2/D49)


@dataclass(frozen=True, slots=True)
class BfsResult:
    distance: dict[bytes, int]
    node_capacity: dict[bytes, int]
    edges: tuple[Edge, ...]
    findings: tuple[Finding, ...]


def bfs_capacities(
    anchors: frozenset[bytes],
    groups: dict[tuple[bytes, bytes], Group],
    params: TrustParams,
) -> BfsResult:
    """02 §3/K8: E+ = {e in Aktiv-Set : cap(e) >= 1}, ein Durchlauf, schichtweise."""
    adjacency: dict[bytes, list[bytes]] = {}
    for author, subject in groups:
        if groups[(author, subject)].n_kante <= 0:
            continue
        adjacency.setdefault(author, []).append(subject)
    for subjects in adjacency.values():
        subjects.sort()

    distance: dict[bytes, int] = {a: 0 for a in anchors}
    node_cap: dict[bytes, int] = {a: capacity(params, 0) for a in anchors}
    edges: list[Edge] = []
    findings: list[Finding] = []

    frontier = sorted(anchors)
    seen = set(anchors)
    while frontier:
        next_frontier: set[bytes] = set()
        for author in frontier:
            d_author = distance[author]
            C_author = node_cap[author]
            for subject in adjacency.get(author, []):
                group = groups[(author, subject)]
                cap = (group.n_kante * C_author) // params.D
                if cap == 0:
                    findings.append(
                        Finding(kind=TrustFinding.SUBGRANULAR_VOUCH, subject=group.kante_claim_id)
                    )
                    continue
                edges.append(
                    Edge(
                        author=author,
                        subject=subject,
                        cap=cap,
                        claim_id=group.kante_claim_id,
                        n_kante=group.n_kante,
                    )
                )
                if subject not in seen:
                    seen.add(subject)
                    distance[subject] = d_author + 1
                    node_cap[subject] = capacity(params, d_author + 1)
                    next_frontier.add(subject)
        frontier = sorted(next_frontier)

    edges.sort(key=lambda e: (e.author, e.subject))
    return BfsResult(
        distance=distance,
        node_capacity=node_cap,
        edges=tuple(edges),
        findings=tuple(sorted(findings)),
    )


def infinity(bfs_result: BfsResult) -> int:
    """INF = Summe aller endlichen Kapazitäten + 1 (02 §4), nie float('inf').

    Wird aus dem Flusslauf berechnet und fuer beide Laeufe (Fluss und Einheitskapazitaet)
    verwendet. Das traegt auch im Einheitslauf: jede Kante in bfs_result.edges hat per
    Filter (E+, 02 §3/K8) cap >= 1, also gilt |edges| <= Summe der cap-Werte < INF, und
    maxflow im Einheitslauf ist durch die Anzahl der Kanten beschraenkt -- also INF >
    |edges| >= maxflow. Diese Kette bricht still, falls der cap>=1-Filter je gelockert
    wird (dann koennte eine Kante mit cap==0 in bfs_result.edges landen).
    """
    finite = list(bfs_result.node_capacity.values()) + [e.cap for e in bfs_result.edges]
    return sum(finite) + 1


def build_flow_graph(
    solver_cls,
    bfs_result: BfsResult,
    anchors: frozenset[bytes],
    targets: frozenset[bytes],
    inf: int,
    *,
    unit_capacities: bool,
):
    """Split-Graph mit S*/T* (K3, K4); zwei Belegungen je nach unit_capacities (02 §8)."""
    solver = solver_cls()
    identities = set(bfs_result.node_capacity) | anchors | targets

    for identity in sorted(identities):
        if unit_capacities:
            cap = inf if identity in anchors else 1
        else:
            cap = bfs_result.node_capacity.get(identity, 0)
        solver.add_edge(node_in(identity), node_out(identity), cap)

    for anchor in sorted(anchors):
        solver.add_edge(SOURCE, node_in(anchor), inf)

    for target in sorted(targets):
        solver.add_edge(node_in(target), SINK, inf)

    for edge in bfs_result.edges:
        # Vouch-Kanten tragen im Disjunktheitslauf 1, nicht INF (D42, K5, 02 Paragraph 8).
        # Bei einer direkten Anker->Ziel-Kante ohne Zwischenknoten laege sonst gar keine
        # Kapazitaets-1-Kante auf dem Pfad (das Ziel ist wegen K3 ungespalten, der Anker
        # intern ist wegen K4 INF) -- der Fluss waere dann nur durch den INF-Sentinel
        # begrenzt statt durch die tatsaechliche Pfadzahl (TP-BOOT m=1/m=2: disjoint_paths
        # muesste 1 bzw. 2 sein, nicht der Sentinel-Wert).
        cap = 1 if unit_capacities else edge.cap
        solver.add_edge(node_out(edge.author), node_in(edge.subject), cap)

    return solver


def source_side_cut(solver, identities: frozenset[bytes]) -> tuple[bytes, ...]:
    """Quellseitiger Schnitt: Identitäten, deren interne Kante im Schnitt liegt (02-golden-anchors.md §0, K9)."""
    reachable = solver.reachable_from(SOURCE)
    return tuple(
        sorted(
            identity
            for identity in identities
            if node_in(identity) in reachable and node_out(identity) not in reachable
        )
    )
