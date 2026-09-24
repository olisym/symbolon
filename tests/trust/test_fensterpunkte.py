"""disjoint_paths und Schnitt im Fenster (02 §11.1, D450).

Golden Numbers aus D450: Fensterwelt und Schnittwelt, Profil
TrustParams(C0=16, gamma_num=1, gamma_den=2, D=4).
"""

from __future__ import annotations

from symbolon.trust import Finding, TrustFinding, TrustParams, trust

from tests.helpers import Identity, scope_id, store_with

T_1000 = 1000
T_1500 = 1500
T_2000 = 2000
T_EXP = 5000
T_1501 = T_1500 + 1

PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=4)
FENSTER = (T_1000, T_2000)


def test_disjoint_paths_ist_eigenes_minimum() -> None:
    """disjoint_paths ist das Minimum über die Punkte (02 §11.1, D450)."""
    scope = scope_id("o80-fenster")
    A = Identity("o80-fenster-A")
    B = Identity("o80-fenster-B")
    C = Identity("o80-fenster-C")
    E = Identity("o80-fenster-E")
    Z = Identity("o80-fenster-Z")
    T = Identity("o80-fenster-T")
    # A bürgt n=2 für B und n=1 für C und E. B bürgt n=4 für T und n=1 bis 1500
    # für Z. C und E bürgen je n=1 bis 1500 für T (D450, Fenster).
    claims = [
        A.vouch(B, n=2, scope=scope, t=1, t_exp=T_EXP),
        A.vouch(C, n=1, scope=scope, t=2, t_exp=T_EXP),
        A.vouch(E, n=1, scope=scope, t=3, t_exp=T_EXP),
        B.vouch(T, n=4, scope=scope, t=1, t_exp=T_EXP),
        B.vouch(Z, n=1, scope=scope, t=2, t_exp=T_1500),
        C.vouch(T, n=1, scope=scope, t=1, t_exp=T_1500),
        E.vouch(T, n=1, scope=scope, t=1, t_exp=T_1500),
    ]
    store = store_with(*claims)
    common = dict(
        anchors=frozenset({A.pub}),
        targets=frozenset({T.pub}),
        scope=scope,
        params=PARAMS,
    )
    bei_1000 = trust(store, now=T_1000, **common)
    assert bei_1000.value == 4
    assert bei_1000.disjoint_paths == 2
    bei_1501 = trust(store, now=T_1501, **common)
    assert bei_1501.value == 8
    assert bei_1501.disjoint_paths == 1
    fenster = trust(store, now=FENSTER, **common)
    assert fenster.value == 4
    assert fenster.value_max == 8
    assert fenster.disjoint_paths == 1
    assert fenster.findings == (
        Finding(TrustFinding.OVERCOMMITTED_AUTHOR, B.pub),
    )


def test_schnitt_vom_punkt_des_werts() -> None:
    """Schnitt und Wert stammen vom selben Punkt (02 §11.1, D450)."""
    scope = scope_id("o80-schnitt")
    A = Identity("o80-schnitt-A")
    B = Identity("o80-schnitt-B")
    C = Identity("o80-schnitt-C")
    Z = Identity("o80-schnitt-Z")
    T = Identity("o80-schnitt-T")
    # A bürgt n=2 für B und C. B und C bürgen je n=4 für T. C bürgt zusätzlich
    # n=1 bis 1500 für Z (D450, Schnitt).
    claims = [
        A.vouch(B, n=2, scope=scope, t=1, t_exp=T_EXP),
        A.vouch(C, n=2, scope=scope, t=2, t_exp=T_EXP),
        B.vouch(T, n=4, scope=scope, t=1, t_exp=T_EXP),
        C.vouch(T, n=4, scope=scope, t=1, t_exp=T_EXP),
        C.vouch(Z, n=1, scope=scope, t=2, t_exp=T_1500),
    ]
    store = store_with(*claims)
    common = dict(
        anchors=frozenset({A.pub}),
        targets=frozenset({T.pub}),
        scope=scope,
        params=PARAMS,
    )
    bei_1501 = trust(store, now=T_1501, **common)
    assert bei_1501.cut == (A.pub,)
    fenster = trust(store, now=FENSTER, **common)
    assert fenster.value == 8
    assert fenster.cut == ()
    assert fenster.disjoint_paths == 1
