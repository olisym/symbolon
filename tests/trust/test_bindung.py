"""Bindung von zehn Normen aus 02 §3.1, 02 §8 und 02 §10, D448, D450."""

from __future__ import annotations

import pytest

from symbolon import cbor_canon
from symbolon.atom import claim_id
from symbolon.trust import Finding, TrustFinding, TrustParams, trust

from tests.helpers import Identity, scope_id, store_with
from tests.trust.tp02 import NOW, T_EXP
from tests.trust.zf02 import FLOW_PER_TARGET, build_f3
from tests.trust.zf02 import NOW as ZF02_NOW
from tests.trust.zf02 import PARAMS as ZF02_PARAMS

PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=4)


def test_knotendisjunkt() -> None:
    """Interne Kante eines Nicht-Ankers im Einheitslauf ist 1 (02 §8, D448)."""
    scope = scope_id("o79-knotendisjunkt")
    A1, A2 = Identity("o79-A1"), Identity("o79-A2")
    B = Identity("o79-B")
    X1, X2 = Identity("o79-X1"), Identity("o79-X2")
    T = Identity("o79-T")
    # C(B) = 8, cap(B→X) = floor(2·8/4) = 4, C(X) = 4, cap(X→T) = floor(4·4/4) = 4.
    # Daraus value = 8. Beide Pfade teilen B, der Einheitslauf zählt 1.
    claims = [
        A1.vouch(B, n=4, scope=scope, t=1, t_exp=T_EXP),
        A2.vouch(B, n=4, scope=scope, t=1, t_exp=T_EXP),
        B.vouch(X1, n=2, scope=scope, t=1, t_exp=T_EXP),
        B.vouch(X2, n=2, scope=scope, t=2, t_exp=T_EXP),
        X1.vouch(T, n=4, scope=scope, t=1, t_exp=T_EXP),
        X2.vouch(T, n=4, scope=scope, t=1, t_exp=T_EXP),
    ]
    r = trust(
        store_with(*claims),
        anchors=frozenset({A1.pub, A2.pub}),
        targets=frozenset({T.pub}),
        scope=scope,
        now=NOW,
        params=PARAMS,
    )
    assert r.value == 8
    assert r.disjoint_paths == 1
    assert r.findings == ()


def test_true_ist_kein_uint() -> None:
    """CBOR-true ist kein uint (02 §10, D448)."""
    scope = scope_id("o79-true")
    autor, subjekt = Identity("o79-true-A"), Identity("o79-true-S")
    claim = autor.vouch_raw(
        subjekt, v=bytes.fromhex("a100f5"), scope=scope, t=1, t_exp=T_EXP,
    )
    r = trust(
        store_with(claim),
        anchors=frozenset({autor.pub}),
        targets=frozenset({subjekt.pub}),
        scope=scope,
        now=NOW,
        params=PARAMS,
    )
    assert r.value == 0
    assert r.findings == (
        Finding(TrustFinding.UNPARSABLE_VOUCH_PAYLOAD, claim_id(claim)),
    )


def test_negatives_n_ist_kein_uint() -> None:
    """Negatives n ist kein uint (02 §10, D448)."""
    scope = scope_id("o79-negativ")
    autor, subjekt = Identity("o79-neg-A"), Identity("o79-neg-S")
    claim = autor.vouch_raw(
        subjekt, v=bytes.fromhex("a10020"), scope=scope, t=1, t_exp=T_EXP,
    )
    r = trust(
        store_with(claim),
        anchors=frozenset({autor.pub}),
        targets=frozenset({subjekt.pub}),
        scope=scope,
        now=NOW,
        params=PARAMS,
    )
    assert r.value == 0
    assert r.findings == (
        Finding(TrustFinding.UNPARSABLE_VOUCH_PAYLOAD, claim_id(claim)),
    )


def test_kanonizitaet_vor_form() -> None:
    """Kanonizität geht der Form voraus (02 §10, D448)."""
    scope = scope_id("o79-kanon")
    autor, subjekt = Identity("o79-kanon-A"), Identity("o79-kanon-S")
    claim = autor.vouch_raw(
        subjekt, v=bytes.fromhex("1800"), scope=scope, t=1, t_exp=T_EXP,
    )
    r = trust(
        store_with(claim),
        anchors=frozenset({autor.pub}),
        targets=frozenset({subjekt.pub}),
        scope=scope,
        now=NOW,
        params=PARAMS,
    )
    assert r.findings == (
        Finding(TrustFinding.NON_CANONICAL_V, claim_id(claim)),
    )


@pytest.mark.parametrize("n_frueher,n_spaeter", [(1, 4), (4, 1)])
def test_n_kante_ist_max(n_frueher: int, n_spaeter: int) -> None:
    """n_kante ist das Maximum der aktiven Mitglieder (02 §3.1, D448)."""
    scope = scope_id(f"o79-max-{n_frueher}-{n_spaeter}")
    autor, subjekt = Identity(f"o79-max-A-{n_frueher}"), Identity(f"o79-max-S-{n_frueher}")
    claims = [
        autor.vouch(subjekt, n=n_frueher, scope=scope, t=1, t_exp=T_EXP),
        autor.vouch(subjekt, n=n_spaeter, scope=scope, t=2, t_exp=T_EXP),
    ]
    r = trust(
        store_with(*claims),
        anchors=frozenset({autor.pub}),
        targets=frozenset({subjekt.pub}),
        scope=scope,
        now=NOW,
        params=PARAMS,
    )
    assert r.value == 16
    assert r.findings == ()


def test_zeitregression_flaggt_den_autor_nicht() -> None:
    """time-regression-flagged flaggt den Claim, nicht den Autor (02 §8, D448)."""
    graph = build_f3()
    r = trust(
        graph.store(),
        anchors=frozenset({graph.ALICE.pub}),
        targets=frozenset({graph.g1.pub}),
        scope=graph.scope,
        now=ZF02_NOW,
        params=ZF02_PARAMS,
        include_flagged=False,
    )
    assert r.value == FLOW_PER_TARGET
    assert not any(f.kind == TrustFinding.OVERCOMMITTED_AUTHOR for f in r.findings)


def test_uebrige_gruppenmitglieder_unberuehrt() -> None:
    """Ein Lesefehler lässt die übrigen Gruppenmitglieder unberührt (02 §10, D448)."""
    scope = scope_id("o79-gruppe")
    autor, subjekt = Identity("o79-gruppe-A"), Identity("o79-gruppe-S")
    gueltig = autor.vouch(subjekt, n=4, scope=scope, t=1, t_exp=T_EXP)
    unlesbar = autor.vouch_raw(
        subjekt, v=bytes.fromhex("ff"), scope=scope, t=2, t_exp=T_EXP,
    )
    r = trust(
        store_with(gueltig, unlesbar),
        anchors=frozenset({autor.pub}),
        targets=frozenset({subjekt.pub}),
        scope=scope,
        now=NOW,
        params=PARAMS,
    )
    assert r.value == 16
    assert r.findings == (
        Finding(TrustFinding.UNPARSABLE_VOUCH_PAYLOAD, claim_id(unlesbar)),
    )


def test_c_einmal_am_ende_gerundet() -> None:
    """C(d) wird einmal am Ende gerundet (02 §3, D450)."""
    params = TrustParams(C0=2, gamma_num=3, gamma_den=4, D=4)
    scope = scope_id("o80-c-ende")
    A, B = Identity("o80-c-A"), Identity("o80-c-B")
    X, T = Identity("o80-c-X"), Identity("o80-c-T")
    claims = [
        A.vouch(B, n=4, scope=scope, t=1, t_exp=T_EXP),
        B.vouch(X, n=4, scope=scope, t=1, t_exp=T_EXP),
        X.vouch(T, n=4, scope=scope, t=1, t_exp=T_EXP),
    ]
    r = trust(
        store_with(*claims),
        anchors=frozenset({A.pub}),
        targets=frozenset({T.pub}),
        scope=scope,
        now=NOW,
        params=params,
    )
    assert r.value == 1
    assert r.findings == ()


def test_nur_vouch_at_1() -> None:
    """Eine Kante trägt nur nuc:N/vouch@1 (02 §2, D450)."""
    scope = scope_id("o80-vouch-at-2")
    autor, subjekt = Identity("o80-v2-A"), Identity("o80-v2-S")
    claim = autor.claim(
        p=f"nuc:{scope.hex()}/vouch@2",
        J=(1, subjekt.pub),
        t=1,
        v=cbor_canon.encode({0: 4}),
        N=scope,
        t_exp=T_EXP,
    )
    r = trust(
        store_with(claim),
        anchors=frozenset({autor.pub}),
        targets=frozenset({subjekt.pub}),
        scope=scope,
        now=NOW,
        params=PARAMS,
    )
    assert r.value == 0
    assert r.findings == ()


def test_now_ist_kein_bool() -> None:
    """now ist ein Zeitpunkt oder ein Intervall, kein bool (02 §11.1, 02 §11.2, D450)."""
    scope = scope_id("o80-now-bool")
    autor, subjekt = Identity("o80-now-A"), Identity("o80-now-S")
    claim = autor.vouch(subjekt, n=4, scope=scope, t=1, t_exp=T_EXP)
    with pytest.raises(ValueError):
        trust(
            store_with(claim),
            anchors=frozenset({autor.pub}),
            targets=frozenset({subjekt.pub}),
            scope=scope,
            now=True,
            params=PARAMS,
        )
