"""T-02.6 — Bootstrap, Profil TP-BOOT (gamma=1/2, C0=16, D=24, f=3, M=17)."""

from __future__ import annotations

import pytest

from symbolon.index import classify_all
from symbolon.trust import TrustFinding, TrustParams, trust
from symbolon.trust.groups import build_groups

from tests.helpers import Identity, scope_id, store_with
from .tp02 import NOW, T_EXP

PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=24)


def _build(m: int, scope: bytes) -> tuple[list[Identity], list[Identity], list]:
    founders = [Identity(f"F{i}-m{m}") for i in range(3)]
    newcomers = [Identity(f"N{i}-m{m}") for i in range(17)]

    if m == 1:
        voucher_sets = [[i % 3] for i in range(17)]
    elif m == 2:
        pairs = [(0, 1), (0, 2), (1, 2)]
        voucher_sets = [list(pairs[i % 3]) for i in range(17)]
    elif m == 3:
        voucher_sets = [[0, 1, 2] for i in range(17)]
    else:
        raise ValueError(m)

    max_edges = max(
        sum(1 for vs in voucher_sets if idx in vs) for idx in range(3)
    )
    n = PARAMS.D // max_edges

    claims = []
    for newcomer, vouchers in zip(newcomers, voucher_sets):
        for idx in vouchers:
            claims.append(
                founders[idx].vouch(newcomer, n=n, scope=scope, t=1, t_exp=T_EXP)
            )
    return founders, newcomers, claims


@pytest.mark.parametrize(
    "m,expected_n,expected_cap,expected_trust,expected_disjoint",
    [
        (1, 4, 2, 2, 1),
        (2, 2, 1, 2, 2),
        (3, 1, 0, 0, 0),
    ],
)
def test_bootstrap_rows(
    m: int, expected_n: int, expected_cap: int, expected_trust: int, expected_disjoint: int
) -> None:
    scope = scope_id(f"TP-BOOT-m{m}")
    founders, newcomers, claims = _build(m, scope)
    store = store_with(*claims)
    anchors = frozenset(f.pub for f in founders)
    classifications = classify_all(store, NOW, None)
    groups, _ = build_groups(store.all_claims(), classifications, scope, PARAMS.D, NOW)
    assert {g.n_kante for g in groups.values()} == {expected_n}
    assert expected_trust == m * expected_cap

    for newcomer in newcomers:
        r = trust(
            store, anchors=anchors, targets=frozenset({newcomer.pub}), scope=scope,
            now=NOW, params=PARAMS, include_flagged=True,
        )
        assert r.value == expected_trust, newcomer.label
        assert r.disjoint_paths == expected_disjoint, newcomer.label

    if m == 3:
        r = trust(
            store, anchors=anchors, targets=frozenset({newcomers[0].pub}), scope=scope,
            now=NOW, params=PARAMS, include_flagged=True,
        )
        assert any(f.kind == TrustFinding.SUBGRANULAR_VOUCH for f in r.findings)


def test_bootstrap_m3_all_subgranular() -> None:
    scope = scope_id("TP-BOOT-m3-all")
    founders, newcomers, claims = _build(3, scope)
    store = store_with(*claims)
    anchors = frozenset(f.pub for f in founders)
    r = trust(
        store, anchors=anchors, targets=frozenset(n.pub for n in newcomers), scope=scope,
        now=NOW, params=PARAMS, include_flagged=True,
    )
    subgranular = [f for f in r.findings if f.kind == TrustFinding.SUBGRANULAR_VOUCH]
    # 02a-maxflow-prompt.md sagt "17 x SUBGRANULAR_VOUCH" (eines je betroffenem Neuling).
    # SUBGRANULAR_VOUCH ist aber pro Gruppe (I, J, N) definiert (02 §10), und bei m=3 vouchen
    # alle 3 Gruender fuer jeden Neuling separat -> 3 Gruppen je Neuling, 3*17=51 Findings.
    # Wir folgen der Gruppen-Definition aus 02 §10, nicht der Ueberschlagszahl im Fliesstext.
    affected_newcomers = {f.subject for f in subgranular}
    assert len(subgranular) == 51
    assert len(affected_newcomers) == 51  # je Gruppe eine eigene claim_id
    assert r.value == 0


def test_bootstrap_m2_simultaneous_over_all_newcomers_is_34() -> None:
    scope = scope_id("TP-BOOT-m2-sim")
    founders, newcomers, claims = _build(2, scope)
    store = store_with(*claims)
    anchors = frozenset(f.pub for f in founders)
    r = trust(
        store, anchors=anchors, targets=frozenset(n.pub for n in newcomers), scope=scope,
        now=NOW, params=PARAMS, include_flagged=True,
    )
    assert r.value == 34
    for founder in founders:
        assert not any(
            f.kind == TrustFinding.OVERCOMMITTED_AUTHOR and f.subject == founder.pub
            for f in r.findings
        )
