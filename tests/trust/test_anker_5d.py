"""Anker 5d — Intervall-now, Profil TP-UHR (D406, 02 §11.1).

Erwartungswerte aus den Tabellen in 02-golden-anchors.md Anker 5d. Keine Zahl
ohne Herkunft; keine Ankerzahl nachgerechnet und ersetzt.
"""

from __future__ import annotations

import pytest

from symbolon.trust import Finding, TrustFinding, trust

from .tpuhr import PARAMS, build

# Punktwerte, Vermerke, disjoint_paths: Tabelle „Punktwerte" in Anker 5d.
NOW_500 = 500
NOW_600 = 600
NOW_601 = 601
NOW_700 = 700
VALUE_BEI_OVERCOMMIT = 8
VALUE_NACH_ABLAUF = 6
DISJOINT_PATHS = 1
PUNKTE = (NOW_500, NOW_600, NOW_601, NOW_700)

# Fenster [500, 700]: Tabelle „Fenster" in Anker 5d.
FENSTER = (NOW_500, NOW_700)
FENSTER_VALUE = 6
FENSTER_VALUE_MAX = 8


def _run(g, now, *, target=None):
    subject = g.DAVE if target is None else target
    return trust(
        g.store(),
        anchors=frozenset({g.ALICE.pub}),
        targets=frozenset({subject.pub}),
        scope=g.scope,
        now=now,
        params=PARAMS,
    )


def _overcommitted_bob(g) -> tuple[Finding, ...]:
    return (
        Finding(kind=TrustFinding.OVERCOMMITTED_AUTHOR, subject=g.BOB.pub),
    )


@pytest.mark.parametrize(
    "now, value, has_overcommit",
    [
        (NOW_500, VALUE_BEI_OVERCOMMIT, True),
        (NOW_600, VALUE_BEI_OVERCOMMIT, True),
        (NOW_601, VALUE_NACH_ABLAUF, False),
        (NOW_700, VALUE_NACH_ABLAUF, False),
    ],
)
def test_punktwerte(now: int, value: int, has_overcommit: bool) -> None:
    g = build()
    result = _run(g, now)
    assert result.value == value
    assert result.value_max == result.value
    assert result.disjoint_paths == DISJOINT_PATHS
    if has_overcommit:
        assert result.findings == _overcommitted_bob(g)
    else:
        assert result.findings == ()


def test_fenster_minimum_ueber_bruchstellen() -> None:
    g = build()
    result = _run(g, FENSTER)
    assert result.value == FENSTER_VALUE
    assert result.value_max == FENSTER_VALUE_MAX
    assert result.disjoint_paths == DISJOINT_PATHS


def test_fenster_vermerke_vom_minimum_punkt() -> None:
    g = build()
    punkt = _run(g, NOW_500)
    fenster = _run(g, FENSTER)
    assert punkt.findings == _overcommitted_bob(g)
    assert fenster.findings == ()


def test_gleichstand_kleinster_zeitpunkt() -> None:
    """Bei mehreren Minimalstellen gilt der kleinste Zeitpunkt (02 §11.1)."""
    g = build()
    an_500 = _run(g, NOW_500, target=g.ERIN)
    an_601 = _run(g, NOW_601, target=g.ERIN)
    fenster = _run(g, FENSTER, target=g.ERIN)
    assert an_500.value == an_601.value
    assert fenster.findings == an_500.findings
    assert fenster.findings != an_601.findings


@pytest.mark.parametrize("now", PUNKTE)
def test_lo_gleich_hi_gegen_int(now: int) -> None:
    g = build()
    als_int = _run(g, now)
    als_paar = _run(g, (now, now))
    assert als_paar == als_int
    assert als_paar.value_max == als_paar.value


def test_lo_groesser_hi_valueerror() -> None:
    g = build()
    with pytest.raises(ValueError):
        _run(g, (NOW_700, NOW_500))


def test_zweimal_derselbe_aufruf() -> None:
    g = build()
    store = g.store()
    kwargs = dict(
        store=store,
        anchors=frozenset({g.ALICE.pub}),
        targets=frozenset({g.DAVE.pub}),
        scope=g.scope,
        now=FENSTER,
        params=PARAMS,
    )
    assert trust(**kwargs) == trust(**kwargs)
