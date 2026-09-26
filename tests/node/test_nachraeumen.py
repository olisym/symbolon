"""Der Bestand räumt fremde Lebenszyklus-Claims nach (01 §6, D514 Beschluss 1)."""

from __future__ import annotations

from itertools import permutations

from symbolon.atom import claim_id, signed_bytes
from symbolon.node.store import SqliteStore
from symbolon.verifier import State, VerifierError, classify
from tests.helpers import Identity, scope_id

_NOW = 1000
_T_EXP = 5000


def _welt() -> dict:
    """Welt aus D514 Golden Numbers, mit eigenen Identitäten (D514)."""
    scope = scope_id("p19-welt")
    A = Identity("p19-A")
    B = Identity("p19-B")
    C = Identity("p19-C")
    D = Identity("p19-D")
    v = A.vouch(C, n=4, scope=scope, t=1, t_exp=_T_EXP)
    w = B.revoke(v, t=2)
    n = B.vouch(C, n=4, scope=scope, t=3, t_exp=_T_EXP)
    su = D.supersede(v, t=2)
    w2 = C.revoke(v, t=2)
    eigen = A.revoke(v, t=2)
    return {"v": v, "w": w, "n": n, "su": su, "w2": w2, "eigen": eigen}


def _submit(store: SqliteStore, claim) -> None:
    try:
        store.submit_claim(signed_bytes(claim))
    except VerifierError:
        pass


def test_jede_reihenfolge_ein_bestand() -> None:
    """Jede der 720 Reihenfolgen hält genau v, n und eigen (01 §6, D514 Golden Numbers)."""
    welt = _welt()
    soll = {claim_id(welt[name]) for name in ("v", "n", "eigen")}
    for order in permutations(welt.values()):
        store = SqliteStore(":memory:")
        for claim in order:
            _submit(store, claim)
        assert {claim_id(claim) for claim in store.all_claims()} == soll
        store.close()


def test_ziel_kommt_zuletzt() -> None:
    """Ziel nach dem fremden Widerruf: der Widerruf geht, sein Nachfolger bleibt pending (01 §6, D514)."""
    welt = _welt()
    store = SqliteStore(":memory:")
    _submit(store, welt["w"])
    _submit(store, welt["n"])
    assert store.get(claim_id(welt["w"])) is not None
    _submit(store, welt["v"])
    assert store.get(claim_id(welt["w"])) is None
    assert store.get(claim_id(welt["n"])) is not None
    assert classify(welt["n"], store, now=_NOW).state == State.PENDING
    store.close()


def test_ziel_kommt_nie() -> None:
    """Ohne Ziel bleiben der fremde Widerruf und sein Nachfolger gehalten (01 §6, D514)."""
    welt = _welt()
    store = SqliteStore(":memory:")
    _submit(store, welt["w"])
    _submit(store, welt["n"])
    assert {claim_id(claim) for claim in store.all_claims()} == {
        claim_id(welt["w"]),
        claim_id(welt["n"]),
    }
    store.close()
