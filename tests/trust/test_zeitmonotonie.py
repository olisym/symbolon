"""Zeitmonotonie des Trust-Werts (D362, 02 §3.1, 02 §7)."""

from __future__ import annotations

from symbolon.trust import TrustFinding, trust
from symbolon.verifier import InMemoryStore

from tests.helpers import Identity, scope_id, store_with
from .tp02 import PARAMS


def _szenario() -> tuple[
    InMemoryStore,
    Identity,
    Identity,
    bytes,
    tuple[int, int, int],
    int,
]:
    """ALICE buergt fuer BOB (spaeteres t_exp) und CAROL (frueheres); Ziel BOB."""
    n = PARAMS.D // 2 + 1
    scope = scope_id("zeitmonotonie")
    alice = Identity("ZM-ALICE")
    bob = Identity("ZM-BOB")
    carol = Identity("ZM-CAROL")
    t_exp_carol = 10
    t_exp_bob = 20
    store = store_with(
        alice.vouch(bob, n=n, scope=scope, t=1, t_exp=t_exp_bob),
        alice.vouch(carol, n=n, scope=scope, t=1, t_exp=t_exp_carol),
    )
    nows = (t_exp_carol - 1, t_exp_carol + 1, t_exp_bob + 1)
    # C(d) nach 02 §3, einmal am Ende gerundet; d(ALICE) = 0.
    c_alice = (PARAMS.C0 * PARAMS.gamma_num**0) // (PARAMS.gamma_den**0)
    # cap(ALICE → BOB) nach 02 §3.1; keine Kurzform (02 §8).
    expected_mid = (n * c_alice) // PARAMS.D
    # 2n > D und n <= D gelten durch die Wahl von n fuer jedes D >= 1 und sind
    # nicht zu pruefen. Die Konstruktion haengt daran, dass die Kante ueberhaupt
    # Kapazitaet traegt: bei expected_mid == 0 waere der mittlere Wert null und
    # der Anstieg unbeobachtbar.
    assert expected_mid > 0
    return store, alice, bob, scope, nows, expected_mid


def test_default_steigt_dann_faellt() -> None:
    store, alice, bob, scope, nows, expected_mid = _szenario()
    values = [
        trust(
            store,
            anchors=frozenset({alice.pub}),
            targets=frozenset({bob.pub}),
            scope=scope,
            now=now,
            params=PARAMS,
        ).value
        for now in nows
    ]
    assert values[0] == 0
    assert values[1] == expected_mid
    assert values[2] == 0
    assert values[0] < values[1]
    assert values[1] > values[2]


def test_include_flagged_nicht_steigend() -> None:
    store, alice, bob, scope, nows, _expected_mid = _szenario()
    values = [
        trust(
            store,
            anchors=frozenset({alice.pub}),
            targets=frozenset({bob.pub}),
            scope=scope,
            now=now,
            params=PARAMS,
            include_flagged=True,
        ).value
        for now in nows
    ]
    assert values[0] >= values[1] >= values[2]


def test_zwischenzustand_overcommitted_author() -> None:
    store, alice, bob, scope, nows, _expected_mid = _szenario()
    first = trust(
        store,
        anchors=frozenset({alice.pub}),
        targets=frozenset({bob.pub}),
        scope=scope,
        now=nows[0],
        params=PARAMS,
    )
    mid = trust(
        store,
        anchors=frozenset({alice.pub}),
        targets=frozenset({bob.pub}),
        scope=scope,
        now=nows[1],
        params=PARAMS,
    )
    assert any(
        f.kind == TrustFinding.OVERCOMMITTED_AUTHOR and f.subject == alice.pub
        for f in first.findings
    )
    assert not any(
        f.kind == TrustFinding.OVERCOMMITTED_AUTHOR and f.subject == alice.pub
        for f in mid.findings
    )
