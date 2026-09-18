"""INV-9 und INV-10 — Zeitinvarianten (02-golden-anchors.md §8, D410, D406, D362)."""

from __future__ import annotations

import pytest

from symbolon.trust import TrustParams, trust
from symbolon.verifier import InMemoryStore

from .test_zeitmonotonie import _szenario
from .tp02 import PARAMS as PARAMS_TP02
from .tpuhr import PARAMS as PARAMS_TPUHR
from .tpuhr import build

_FAELLE = ("TP-UHR-DAVE", "TP-UHR-ERIN", "D362")


def _fall(
    name: str,
) -> tuple[InMemoryStore, frozenset[bytes], bytes, bytes, TrustParams]:
    """Fall als (store, anchors, target, scope, params) (D410)."""
    if name == "TP-UHR-DAVE":
        g = build()
        return (
            g.store(),
            frozenset({g.ALICE.pub}),
            g.DAVE.pub,
            g.scope,
            PARAMS_TPUHR,
        )
    if name == "TP-UHR-ERIN":
        g = build()
        return (
            g.store(),
            frozenset({g.ALICE.pub}),
            g.ERIN.pub,
            g.scope,
            PARAMS_TPUHR,
        )
    if name == "D362":
        store, alice, bob, scope, _nows, _expected_mid = _szenario()
        return store, frozenset({alice.pub}), bob.pub, scope, PARAMS_TP02
    raise ValueError(name)


def _raster(store: InMemoryStore) -> tuple[int, ...]:
    """Kleinstes t, jedes t_exp und t_exp+1, ueber alle Scopes, ohne Doppel (D410)."""
    claims = store.all_claims()
    punkte = {min(claim.t for claim in claims)}
    for claim in claims:
        if claim.t_exp is not None:
            punkte.add(claim.t_exp)
            punkte.add(claim.t_exp + 1)
    return tuple(sorted(punkte))


def _fenster(raster: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    """Alle Paare (a, b) aus dem Raster mit a <= b (D410)."""
    return tuple((a, b) for a in raster for b in raster if a <= b)


def _anstiege(werte: list[int]) -> list[tuple[int, int]]:
    """Indexpaare aufeinanderfolgender Anstiege (INV-9, 02-golden-anchors.md §8)."""
    return [(i, i + 1) for i in range(len(werte) - 1) if werte[i + 1] > werte[i]]


@pytest.mark.parametrize("fall", _FAELLE)
def test_inv9_nicht_steigend(fall: str) -> None:
    store, anchors, target, scope, params = _fall(fall)
    raster = _raster(store)
    werte = [
        trust(
            store,
            anchors=anchors,
            targets=frozenset({target}),
            scope=scope,
            now=t,
            params=params,
            include_flagged=True,
        ).value
        for t in raster
    ]
    anstiege = _anstiege(werte)
    assert anstiege == [], f"{fall}: Anstiege " + ", ".join(
        f"now={raster[i]}->{raster[j]} value={werte[i]}->{werte[j]}"
        for i, j in anstiege
    )


@pytest.mark.parametrize("fall", ["D362"])
def test_inv9_befund_bei_false(fall: str) -> None:
    store, anchors, target, scope, params = _fall(fall)
    raster = _raster(store)
    werte = [
        trust(
            store,
            anchors=anchors,
            targets=frozenset({target}),
            scope=scope,
            now=t,
            params=params,
            include_flagged=False,
        ).value
        for t in raster
    ]
    anstiege = _anstiege(werte)
    assert anstiege, (
        f"{fall}: kein Anstieg bei include_flagged=False, Werte {werte} Raster {raster}"
    )


@pytest.mark.parametrize("fall", _FAELLE)
@pytest.mark.parametrize("include_flagged", [True, False])
def test_inv10_fensterinklusion(fall: str, include_flagged: bool) -> None:
    store, anchors, target, scope, params = _fall(fall)
    fenster = _fenster(_raster(store))
    ergebnisse = {
        w: trust(
            store,
            anchors=anchors,
            targets=frozenset({target}),
            scope=scope,
            now=w,
            params=params,
            include_flagged=include_flagged,
        )
        for w in fenster
    }
    for w, r in ergebnisse.items():
        assert r.value <= r.value_max, (
            f"{fall} include_flagged={include_flagged}: "
            f"Fenster {w}: value={r.value} > value_max={r.value_max}"
        )
    for w in fenster:
        for w_prime in fenster:
            if not (w_prime[0] <= w[0] and w[1] <= w_prime[1]):
                continue
            r = ergebnisse[w]
            r_prime = ergebnisse[w_prime]
            assert r_prime.value <= r.value, (
                f"{fall} include_flagged={include_flagged}: "
                f"Fenster {w} in {w_prime}: "
                f"value({w_prime})={r_prime.value} > value({w})={r.value}"
            )
            assert r_prime.value_max >= r.value_max, (
                f"{fall} include_flagged={include_flagged}: "
                f"Fenster {w} in {w_prime}: "
                f"value_max({w_prime})={r_prime.value_max}"
                f" < value_max({w})={r.value_max}"
            )


@pytest.mark.parametrize("fall", _FAELLE)
def test_inv10_raender_bei_true(fall: str) -> None:
    store, anchors, target, scope, params = _fall(fall)
    common = dict(
        store=store,
        anchors=anchors,
        targets=frozenset({target}),
        scope=scope,
        params=params,
        include_flagged=True,
    )
    for lo, hi in _fenster(_raster(store)):
        fenster = trust(**common, now=(lo, hi))
        am_hi = trust(**common, now=hi)
        am_lo = trust(**common, now=lo)
        assert fenster.value == am_hi.value, (
            f"{fall}: Fenster ({lo}, {hi}): "
            f"value={fenster.value} != value(hi)={am_hi.value}"
        )
        assert fenster.value_max == am_lo.value, (
            f"{fall}: Fenster ({lo}, {hi}): "
            f"value_max={fenster.value_max} != value(lo)={am_lo.value}"
        )
