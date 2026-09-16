"""t_exp-lose Buergschaften im Budget-Set (D364, 02 §3.1, 02 §6.2, D135, D119)."""

from __future__ import annotations

from symbolon.trust import TrustFinding, trust
from symbolon.verifier import InMemoryStore

from tests.helpers import Identity, scope_id, store_with
from .tp02 import PARAMS


def _szenario(
    *,
    carol_hat_texp: bool = False,
    carol_widerrufen: bool = False,
) -> tuple[
    InMemoryStore,
    Identity,
    Identity,
    bytes,
    tuple[int, ...],
    int,
]:
    """ALICE buergt fuer BOB (Ziel) und CAROL, gleiches n, gemeinsamer Scope."""
    n = PARAMS.D // 2 + 1
    t_exp_carol = 7
    t_revoke = 2
    now_near = 4
    now_mid = 400
    now_far = 40000
    now_before_exp = t_exp_carol - 1
    now_after_exp = t_exp_carol + 1
    # C(d) nach 02 §3, einmal am Ende gerundet; d(ALICE) = 0.
    c_alice = (PARAMS.C0 * PARAMS.gamma_num**0) // (PARAMS.gamma_den**0)
    # cap(ALICE → BOB) nach 02 §3.1; keine Kurzform (02 §8).
    expected = (n * c_alice) // PARAMS.D
    assert n + n > PARAMS.D
    assert expected > 0

    scope = scope_id("texp-los")
    alice = Identity("TL-ALICE")
    bob = Identity("TL-BOB")
    carol = Identity("TL-CAROL")
    carol_texp = t_exp_carol if carol_hat_texp else None
    vouch_bob = alice.vouch(bob, n=n, scope=scope, t=1)
    vouch_carol = alice.vouch(carol, n=n, scope=scope, t=1, t_exp=carol_texp)
    claims = [vouch_bob, vouch_carol]
    if carol_widerrufen:
        claims.append(alice.revoke(vouch_carol, t=t_revoke))
    store = store_with(*claims)
    if carol_hat_texp:
        nows: tuple[int, ...] = (now_before_exp, now_after_exp)
    else:
        nows = (now_near, now_mid, now_far)
    return store, alice, bob, scope, nows, expected


def test_dauerhaft_ueberbunden() -> None:
    store, alice, bob, scope, nows, _expected = _szenario()
    for now in nows:
        result = trust(
            store,
            anchors=frozenset({alice.pub}),
            targets=frozenset({bob.pub}),
            scope=scope,
            now=now,
            params=PARAMS,
        )
        assert result.value == 0
        assert any(
            f.kind == TrustFinding.OVERCOMMITTED_AUTHOR and f.subject == alice.pub
            for f in result.findings
        )


def test_widerruf_befreit_nicht() -> None:
    store_a, alice_a, bob_a, scope_a, nows_a, _e_a = _szenario()
    store_b, alice_b, bob_b, scope_b, nows_b, _e_b = _szenario(
        carol_widerrufen=True
    )
    assert nows_a == nows_b
    for now in nows_a:
        ohne = trust(
            store_a,
            anchors=frozenset({alice_a.pub}),
            targets=frozenset({bob_a.pub}),
            scope=scope_a,
            now=now,
            params=PARAMS,
        )
        mit = trust(
            store_b,
            anchors=frozenset({alice_b.pub}),
            targets=frozenset({bob_b.pub}),
            scope=scope_b,
            now=now,
            params=PARAMS,
        )
        assert ohne.value == mit.value
        flag_ohne = any(
            f.kind == TrustFinding.OVERCOMMITTED_AUTHOR and f.subject == alice_a.pub
            for f in ohne.findings
        )
        flag_mit = any(
            f.kind == TrustFinding.OVERCOMMITTED_AUTHOR and f.subject == alice_b.pub
            for f in mit.findings
        )
        assert flag_ohne is flag_mit


def test_ablauf_befreit() -> None:
    store_widerruf, alice_w, bob_w, scope_w, nows_w, _e_w = _szenario(
        carol_widerrufen=True
    )
    store, alice, bob, scope, nows, expected = _szenario(
        carol_hat_texp=True, carol_widerrufen=True
    )
    now_before, now_after = nows
    before = trust(
        store,
        anchors=frozenset({alice.pub}),
        targets=frozenset({bob.pub}),
        scope=scope,
        now=now_before,
        params=PARAMS,
    )
    after = trust(
        store,
        anchors=frozenset({alice.pub}),
        targets=frozenset({bob.pub}),
        scope=scope,
        now=now_after,
        params=PARAMS,
    )
    assert before.value == 0
    assert after.value == expected
    widerruf_werte = [
        trust(
            store_widerruf,
            anchors=frozenset({alice_w.pub}),
            targets=frozenset({bob_w.pub}),
            scope=scope_w,
            now=now,
            params=PARAMS,
        ).value
        for now in nows_w
    ]
    assert after.value not in widerruf_werte
