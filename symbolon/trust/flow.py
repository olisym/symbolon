"""Öffentliche API: trust() (02 §4, 02 §8, 02 §11)."""

from __future__ import annotations

from dataclasses import dataclass

from symbolon.verifier import ClaimStore

from .derive import derive
from .dinic import Dinic
from .findings import Finding
from .graph import SINK, SOURCE, build_flow_graph, infinity, source_side_cut
from .params import TrustParams


@dataclass(frozen=True, slots=True)
class TrustResult:
    value: int
    disjoint_paths: int
    cut: tuple[bytes, ...]
    findings: tuple[Finding, ...]


def trust(
    store: ClaimStore,
    *,
    anchors: frozenset[bytes],
    targets: frozenset[bytes],
    scope: bytes,
    now: int,
    params: TrustParams,
    include_flagged: bool = False,
) -> TrustResult:
    if anchors & targets:
        raise ValueError("anchors and targets must be disjoint")

    # 1-6. geteilte Ableitung (D49): classify_all -> Gruppen -> Budget -> Flags -> BFS über E+
    derivation = derive(
        store, anchors=anchors, scope=scope, now=now, params=params,
        include_flagged=include_flagged,
    )
    bfs_result = derivation.bfs

    identities = frozenset(bfs_result.node_capacity) | anchors | targets
    inf = infinity(bfs_result)

    # 7-8a. Graph bauen (Split, S*, T*), Dinic (Fluss-Belegung) -> value, cut
    flow_solver = build_flow_graph(
        Dinic, bfs_result, anchors, targets, inf, unit_capacities=False
    )
    value = flow_solver.max_flow(SOURCE, SINK)
    cut = source_side_cut(flow_solver, identities)

    # 8b. Dinic (Einheitskapazitäts-Belegung) -> disjoint_paths
    disjoint_solver = build_flow_graph(
        Dinic, bfs_result, anchors, targets, inf, unit_capacities=True
    )
    disjoint_paths = disjoint_solver.max_flow(SOURCE, SINK)

    return TrustResult(
        value=value,
        disjoint_paths=disjoint_paths,
        cut=cut,
        findings=derivation.findings,
    )
