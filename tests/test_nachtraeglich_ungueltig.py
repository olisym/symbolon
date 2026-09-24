"""Nachträglich ungültige Claims: Auswertung, Vorgänger, Equivocation (01 §6, D452)."""

from symbolon.atom import claim_id
from symbolon.index import classify_all
from symbolon.trust import TrustParams, trust
from symbolon.verifier import State, classify
from tests.helpers import Identity, scope_id, store_with

_PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=4)
_NOW = 1000
_T_EXP = 5000


def _welt1():
    """A bürgt für C, B widerruft fremd, B hängt einen Vouch an den Widerruf."""
    scope = scope_id("welt1")
    A = Identity("A")
    B = Identity("B")
    C = Identity("C")
    v = A.vouch(C, n=4, scope=scope, t=1, t_exp=_T_EXP)
    widerruf = B.revoke(v, t=2)
    nach = B.vouch(C, n=4, scope=scope, t=3, t_exp=_T_EXP)
    store = store_with(v, widerruf, nach)
    return scope, A, C, v, widerruf, nach, store


def test_trust_rechnet_trotz_fremdem_widerruf() -> None:
    """trust rechnet die Kante von A, der fremde Widerruf hält nicht an (01 §6, 02 §11.4)."""
    scope, A, C, _v, _widerruf, _nach, store = _welt1()
    result = trust(
        store,
        anchors=frozenset({A.pub}),
        targets=frozenset({C.pub}),
        scope=scope,
        now=_NOW,
        params=_PARAMS,
    )
    assert result.value == 16
    assert result.disjoint_paths == 1
    assert result.findings == ()


def test_classify_all_uebergeht_und_nachfolger_pending() -> None:
    """classify_all ohne Eintrag für den Widerruf; v active, Nachfolger pending (01 §6)."""
    _scope, _A, _C, v, widerruf, nach, store = _welt1()
    result = classify_all(store, _NOW)
    assert claim_id(widerruf) not in result
    assert result[claim_id(v)].state == State.ACTIVE
    assert result[claim_id(nach)].state == State.PENDING


def test_classify_nachfolger_pending() -> None:
    """classify des Nachfolgers ist pending, weil der Vorgänger ungültig ist (01 §6)."""
    _scope, _A, _C, _v, _widerruf, nach, store = _welt1()
    assert classify(nach, store, now=_NOW).state == State.PENDING


def test_ungueltiges_geschwister_flaggt_nicht() -> None:
    """Fremder Genesis-Widerruf ist kein Equivocation-Geschwister (01 §4, 01 §6)."""
    scope = scope_id("welt2")
    A2 = Identity("A2")
    C2 = Identity("C2")
    erste = Identity("B")
    zweite = Identity("B")
    vouch = A2.vouch(C2, n=4, scope=scope, t=1, t_exp=_T_EXP)
    widerruf = erste.revoke(vouch, t=2)
    X = zweite.vouch(C2, n=4, scope=scope, t=2, t_exp=_T_EXP)
    assert (widerruf.I, widerruf.h_prev) == (X.I, X.h_prev)
    store = store_with(vouch, widerruf, X)
    assert classify(X, store, now=_NOW).state == State.ACTIVE
    assert classify_all(store, _NOW)[claim_id(X)].state == State.ACTIVE
