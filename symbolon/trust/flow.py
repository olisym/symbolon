"""Öffentliche API: trust() (02 §4, 02 §8, 02 §11)."""

from __future__ import annotations

from dataclasses import dataclass

from symbolon.verifier import ClaimStore

from .derive import derive
from .dinic import Dinic
from .findings import Finding
from .graph import SINK, SOURCE, build_flow_graph, infinity, source_side_cut
from .groups import _is_scope_vouch
from .params import TrustParams


@dataclass(frozen=True, slots=True)
class TrustResult:
    value: int
    disjoint_paths: int
    cut: tuple[bytes, ...]
    findings: tuple[Finding, ...]
    value_max: int


def _as_interval(now: int | tuple[int, int]) -> tuple[int, int]:
    """now als [lo, hi]; Zeitpunkt ist der Fall lo = hi (02 §11.1, D406)."""
    if type(now) is int:
        return now, now
    if (
        type(now) is tuple
        and len(now) == 2
        and type(now[0]) is int
        and type(now[1]) is int
        and now[0] <= now[1]
    ):
        return now[0], now[1]
    raise ValueError("now must be int or (lo, hi) with lo <= hi")


def _break_points(
    store: ClaimStore, scope: bytes, lo: int, hi: int
) -> tuple[int, ...]:
    """Auswertungspunkte eines Fensters [lo, hi] (02 §11.1, D406)."""
    points = {lo}
    for claim in store.all_claims():
        if claim.t_exp is None:
            continue
        if not _is_scope_vouch(claim, scope):
            continue
        if lo <= claim.t_exp < hi:
            points.add(claim.t_exp + 1)
    return tuple(sorted(points))


def _trust_at_point(
    store: ClaimStore,
    *,
    anchors: frozenset[bytes],
    targets: frozenset[bytes],
    scope: bytes,
    now: int,
    params: TrustParams,
    include_flagged: bool,
) -> TrustResult:
    """Punktauswertung, unverändert in ihrer Punktform (02 §11.1, 02 §11.4, D406)."""
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
        value_max=value,
    )


def trust(
    store: ClaimStore,
    *,
    anchors: frozenset[bytes],
    targets: frozenset[bytes],
    scope: bytes,
    now: int | tuple[int, int],
    params: TrustParams,
    include_flagged: bool = False,
) -> TrustResult:
    if anchors & targets:
        raise ValueError("anchors and targets must be disjoint")

    lo, hi = _as_interval(now)
    points = _break_points(store, scope, lo, hi)
    point_results = [
        _trust_at_point(
            store,
            anchors=anchors,
            targets=targets,
            scope=scope,
            now=t,
            params=params,
            include_flagged=include_flagged,
        )
        for t in points
    ]
    # Kleinster value, bei Gleichstand der kleinste Zeitpunkt (02 §11.1, D406).
    best = min(point_results, key=lambda r: r.value)
    value_max = max(r.value for r in point_results)
    return TrustResult(
        value=best.value,
        disjoint_paths=best.disjoint_paths,
        cut=best.cut,
        findings=best.findings,
        value_max=value_max,
    )
