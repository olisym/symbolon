"""Uhrversatz setzt OVERCOMMITTED_AUTHOR gegen einen ehrlichen Autor (D402, D403, 02 §3.1, 02 §7, 02 §10, 02 §11.4).

Der lokale Vermerk liest ``now``, nicht die signierten Zahlen ``t`` (02 §3.1). Zwei
Buergschaften, deren Geltungsintervalle nach den signierten Zahlen disjunkt sind — das
zweite ``t`` liegt nach dem ``t_exp`` des ersten Vouch — liegen bei einer nachlaufenden
Uhr trotzdem gemeinsam im Budget-Set und erzeugen den Vermerk gegen eine Autorin, die
nach ihren eigenen Zahlen nie ueber-committet war (02 §7). Der signaturbasierte Beweis
aus 02 §3.1 ist bewusst nicht gebaut (D403); hier wird nur die Staffelung der Zahlen
behauptet, kein Praedikat nachgerechnet.
"""

from __future__ import annotations

from symbolon.trust import TrustFinding, trust
from symbolon.verifier import InMemoryStore

from tests.helpers import Identity, scope_id, store_with
from .tp02 import PARAMS

_T_ERSTER = 1
_T_EXP_ERSTER = 10
_T_EXP_ZWEITER = 12
_NOW = _T_EXP_ERSTER - 1
_T_ZWEITER_DISJUNKT = _T_EXP_ERSTER + 1
_T_ZWEITER_UEBERLAPPEND = _T_EXP_ERSTER - 5


def _szenario(
    *, zweites_t: int
) -> tuple[InMemoryStore, Identity, Identity, bytes, int, tuple[int, int], tuple[int, int]]:
    """ALICE buergt zuerst fuer BOB, danach fuer CAROL; Ziel ist BOB.

    ``zweites_t`` bestimmt die Staffelung: disjunkt (nach dem ersten ``t_exp``) oder
    ueberlappend (davor). ``now`` liegt innerhalb des ersten Vouch und, im disjunkten
    Fall, vor dem ``t`` des zweiten. ``n`` und der erwartete Kapazitaetswert sind aus
    ``PARAMS`` abgeleitet (02 §3.1).
    """
    n = PARAMS.D // 2 + 1
    scope = scope_id("uhrversatz")
    alice = Identity("UV-ALICE")
    bob = Identity("UV-BOB")
    carol = Identity("UV-CAROL")
    store = store_with(
        alice.vouch(bob, n=n, scope=scope, t=_T_ERSTER, t_exp=_T_EXP_ERSTER),
        alice.vouch(carol, n=n, scope=scope, t=zweites_t, t_exp=_T_EXP_ZWEITER),
    )
    c_alice = (PARAMS.C0 * PARAMS.gamma_num**0) // (PARAMS.gamma_den**0)
    expected = (n * c_alice) // PARAMS.D
    assert n + n > PARAMS.D
    assert expected > 0
    return (
        store,
        alice,
        bob,
        scope,
        expected,
        (_T_ERSTER, zweites_t),
        (_T_EXP_ERSTER, _T_EXP_ZWEITER),
    )


def test_vermerk_faellt_trotz_disjunkter_intervalle() -> None:
    store, alice, bob, scope, _expected, ts, texps = _szenario(
        zweites_t=_T_ZWEITER_DISJUNKT
    )
    assert max(ts) > min(texps)
    result = trust(
        store,
        anchors=frozenset({alice.pub}),
        targets=frozenset({bob.pub}),
        scope=scope,
        now=_NOW,
        params=PARAMS,
    )
    # Subjekt des Vermerks ist der oeffentliche Schluessel der Autorin, keine claim_id (02 §10).
    assert any(
        f.kind == TrustFinding.OVERCOMMITTED_AUTHOR and f.subject == alice.pub
        for f in result.findings
    )
    assert result.value == 0


def test_kontrolle_ueberlappend_gleicher_vermerk() -> None:
    store, alice, bob, scope, expected, ts, texps = _szenario(
        zweites_t=_T_ZWEITER_UEBERLAPPEND
    )
    assert ts[1] < texps[0]
    ungeflaggt = trust(
        store,
        anchors=frozenset({alice.pub}),
        targets=frozenset({bob.pub}),
        scope=scope,
        now=_NOW,
        params=PARAMS,
    )
    assert any(
        f.kind == TrustFinding.OVERCOMMITTED_AUTHOR and f.subject == alice.pub
        for f in ungeflaggt.findings
    )
    assert ungeflaggt.value == 0
    geflaggt = trust(
        store,
        anchors=frozenset({alice.pub}),
        targets=frozenset({bob.pub}),
        scope=scope,
        now=_NOW,
        params=PARAMS,
        include_flagged=True,
    )
    # Der Vermerk haengt nicht an include_flagged (02 §10, 02 §11.4).
    assert any(
        f.kind == TrustFinding.OVERCOMMITTED_AUTHOR and f.subject == alice.pub
        for f in geflaggt.findings
    )
    assert geflaggt.value == expected


def test_wirkung_ist_flagwirkung_nicht_ablauf() -> None:
    store, alice, bob, scope, expected, ts, texps = _szenario(
        zweites_t=_T_ZWEITER_DISJUNKT
    )
    assert max(ts) > min(texps)
    result = trust(
        store,
        anchors=frozenset({alice.pub}),
        targets=frozenset({bob.pub}),
        scope=scope,
        now=_NOW,
        params=PARAMS,
        include_flagged=True,
    )
    # Der Vermerk haengt nicht an include_flagged (02 §10, 02 §11.4).
    assert any(
        f.kind == TrustFinding.OVERCOMMITTED_AUTHOR and f.subject == alice.pub
        for f in result.findings
    )
    assert result.value == expected
    assert result.value > 0
