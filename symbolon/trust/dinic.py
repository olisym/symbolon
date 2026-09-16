"""Dinic Max-Flow-Solver, generisch über hashbare Knoten (02 §4, 02 §8)."""

from __future__ import annotations

from collections import deque
from typing import Hashable


class Dinic:
    """Eine Implementierung, zwei Kapazitätsbelegungen (Fluss- und Disjunktheitslauf)."""

    def __init__(self) -> None:
        self._graph: dict[Hashable, list[int]] = {}
        self._edges: list[list] = []  # [to, cap] je Index; gepaart via i ^ 1

    def _ensure_node(self, node: Hashable) -> None:
        if node not in self._graph:
            self._graph[node] = []

    def add_edge(self, u: Hashable, v: Hashable, cap: int) -> None:
        self._ensure_node(u)
        self._ensure_node(v)
        self._graph[u].append(len(self._edges))
        self._edges.append([v, cap])
        self._graph[v].append(len(self._edges))
        self._edges.append([u, 0])

    def _bfs_levels(self, s: Hashable, t: Hashable) -> dict[Hashable, int] | None:
        level: dict[Hashable, int] = {s: 0}
        q: deque[Hashable] = deque([s])
        while q:
            u = q.popleft()
            for ei in self._graph.get(u, []):
                v, cap = self._edges[ei]
                if cap > 0 and v not in level:
                    level[v] = level[u] + 1
                    q.append(v)
        return level if t in level else None

    def _dfs_push(
        self,
        u: Hashable,
        t: Hashable,
        pushed: int,
        level: dict[Hashable, int],
        it: dict[Hashable, int],
    ) -> int:
        if u == t:
            return pushed
        adj = self._graph.get(u, [])
        while it[u] < len(adj):
            ei = adj[it[u]]
            v, cap = self._edges[ei]
            if cap > 0 and level.get(v, -1) == level[u] + 1:
                d = self._dfs_push(v, t, min(pushed, cap), level, it)
                if d > 0:
                    self._edges[ei][1] -= d
                    self._edges[ei ^ 1][1] += d
                    return d
            it[u] += 1
        return 0

    def max_flow(self, s: Hashable, t: Hashable) -> int:
        self._ensure_node(s)
        self._ensure_node(t)
        bound = sum(cap for _, cap in self._edges) + 1
        flow = 0
        while True:
            level = self._bfs_levels(s, t)
            if level is None:
                break
            it = {node: 0 for node in self._graph}
            while True:
                pushed = self._dfs_push(s, t, bound, level, it)
                if pushed == 0:
                    break
                flow += pushed
        return flow

    def reachable_from(self, s: Hashable) -> frozenset[Hashable]:
        """Knoten, die im aktuellen Residualgraphen von s aus erreichbar sind."""
        self._ensure_node(s)
        seen = {s}
        q: deque[Hashable] = deque([s])
        while q:
            u = q.popleft()
            for ei in self._graph.get(u, []):
                v, cap = self._edges[ei]
                if cap > 0 and v not in seen:
                    seen.add(v)
                    q.append(v)
        return frozenset(seen)
