"""Geräte: Aufnahme, Zurechnung, Gruppen und Flags (02 §2.1, 02 §8, 01 §7.3, D529 bis D536).

Welt aus ``tools.verein.build()``, Scope ``N_res``, Anker BRUNO und ANNA wie in
``check_anna_overcommit``. Die Aufnahme entsteht aus echten Claims. „Wie die Wurzel“ heisst:
gleich der Auswertung derselben Welt, in der die Wurzel selbst bürgt (D531).
"""

from __future__ import annotations

import hashlib

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id
from symbolon.index import classify_all
from symbolon.trust.attribution import AttributionStatus, attribution
from symbolon.trust.derive import Derivation, derive
from symbolon.trust.findings import TrustFinding
from symbolon.verifier import State
from tools.example_nucleus import NOW, _Author, _nuc, _store
from tools.verein import Verein, build

T_EXP = NOW + 1000000
# Nächstes t je Wurzel über der Spitze von claim_set (tools/verein.py).
T_ROOT = 10


def _device(k: int) -> _Author:
    return _Author(bytes([0x30 + k] * 32))


def _add(root: _Author, device: _Author, scope: bytes, *, t_exp: int | None = None) -> Claim:
    return root.claim(
        p=_nuc(scope, "device-add"), J=(1, device.pub), t=T_ROOT, N=scope, t_exp=t_exp
    )


def _ack(device: _Author, add: Claim, scope: bytes) -> Claim:
    return device.claim(p=_nuc(scope, "device-ack"), J=(2, claim_id(add)), t=T_ROOT, N=scope)


def _end(root: _Author, device: _Author, scope: bytes, v: bytes | None) -> Claim:
    return root.claim(
        p=_nuc(scope, "device-end"), J=(1, device.pub), t=T_ROOT + 1, N=scope, v=v
    )


def _endpoint(cid: bytes) -> bytes:
    return cbor_canon.encode({0: cid})


def _derive(w: Verein, *extra: Claim) -> Derivation:
    return derive(
        _store(*w.base.values(), *extra),
        anchors=frozenset({w.bruno.pub, w.anna.pub}),
        scope=w.ex.N_res,
        now=NOW,
        params=w.ex.params,
    )


def _overcommitted(d: Derivation) -> set[bytes]:
    return {f.subject for f in d.findings if f.kind is TrustFinding.OVERCOMMITTED_AUTHOR}


def _edges(d: Derivation) -> set[tuple[bytes, bytes, int]]:
    return {(e.author, e.subject, e.cap) for e in d.bfs.edges}


def _dora(w: Verein, d: Derivation) -> tuple[int | None, int | None]:
    return d.bfs.distance.get(w.dora.pub), d.bfs.node_capacity.get(w.dora.pub)


def _status(w: Verein, claims: list[Claim], claim: Claim, scope: bytes | None = None):
    store = _store(*w.base.values(), *claims)
    classifications = classify_all(store, NOW)
    return attribution(store, classifications, scope or w.ex.N_res).status(claim)


def _root_view(root: str, n: int) -> Derivation:
    w = build()
    author = getattr(w, root)
    return _derive(w, author.vouch(w.dora, n=n, scope=w.ex.N_res, t=T_ROOT, t_exp=T_EXP))


def _delegated(root: str, n: int, *, end: str | None = None) -> Derivation:
    """Gerät von ``root`` bürgt mit ``n`` für DORA; ``end``: None, "ack", "vouch", "unknown"."""
    w = build()
    author = getattr(w, root)
    device = _device(1)
    add = _add(author, device, w.ex.N_res)
    ack = _ack(device, add, w.ex.N_res)
    vouch = device.vouch(w.dora, n=n, scope=w.ex.N_res, t=T_ROOT, t_exp=T_EXP)
    claims = [add, ack, vouch]
    if end == "ack":
        claims.append(_end(author, device, w.ex.N_res, _endpoint(claim_id(ack))))
    elif end == "vouch":
        claims.append(_end(author, device, w.ex.N_res, _endpoint(claim_id(vouch))))
    elif end == "unknown":
        missing = hashlib.sha256(b"nicht im Bestand").digest()
        claims.append(_end(author, device, w.ex.N_res, _endpoint(missing)))
    return _derive(w, *claims)


def test_1_delegated_like_root() -> None:
    for root, n in (("anna", 1), ("chris", 50)):
        w = build()
        own = _root_view(root, n)
        via_device = _delegated(root, n)
        assert _overcommitted(via_device) == _overcommitted(own)
        assert _edges(via_device) == _edges(own)
        assert _dora(w, via_device) == _dora(w, own)


def test_2_undelegated_weighs_nothing() -> None:
    w = build()
    base = _derive(w)
    device = _device(1)
    alone = device.vouch(w.dora, n=1, scope=w.ex.N_res, t=T_ROOT, t_exp=T_EXP)
    assert _derive(w, alone).findings == base.findings

    w = build()
    device = _device(1)
    add = _add(w.anna, device, w.ex.N_res)
    unacked = device.vouch(w.dora, n=1, scope=w.ex.N_res, t=T_ROOT, t_exp=T_EXP)
    assert _derive(w, add, unacked).findings == base.findings


def test_3_end_cuts() -> None:
    w = build()
    reached = _dora(w, _root_view("chris", 50))
    assert reached[0] is not None
    assert _dora(w, _delegated("chris", 50)) == reached
    assert _dora(w, _delegated("chris", 50, end="ack")) == (None, None)
    assert _dora(w, _delegated("chris", 50, end="vouch")) == reached


def test_4_endpoint_unknown_or_defective() -> None:
    w = build()
    assert _dora(w, _delegated("chris", 50, end="unknown")) == (None, None)

    w = build()
    device = _device(1)
    add = _add(w.chris, device, w.ex.N_res)
    ack = _ack(device, add, w.ex.N_res)
    vouch = device.vouch(w.dora, n=50, scope=w.ex.N_res, t=T_ROOT, t_exp=T_EXP)
    end = _end(w.chris, device, w.ex.N_res, bytes.fromhex("a1001801"))
    assert _dora(w, _derive(w, add, ack, vouch, end)) == (None, None)


def test_5_withheld_predecessor() -> None:
    w = build()
    device = _device(1)
    add = _add(w.anna, device, w.ex.N_res)
    ack = _ack(device, add, w.ex.N_res)
    device.vouch(w.bruno, n=1, scope=w.ex.N_res, t=T_ROOT, t_exp=T_EXP)  # zurückgehalten
    vouch = device.vouch(w.dora, n=1, scope=w.ex.N_res, t=T_ROOT, t_exp=T_EXP)
    assert w.anna.pub in _overcommitted(_derive(w, add, ack, vouch))


def test_6_disputed_versus_unknown_in_budget() -> None:
    assert build().anna.pub not in _overcommitted(_delegated("anna", 1, end="ack"))
    assert build().anna.pub in _overcommitted(_delegated("anna", 1, end="unknown"))


def test_7_earliest_ack_binds() -> None:
    w = build()
    device = _device(1)
    add_chris = _add(w.chris, device, w.ex.N_res)
    add_anna = _add(w.anna, device, w.ex.N_res)
    ack_chris = _ack(device, add_chris, w.ex.N_res)
    ack_anna = _ack(device, add_anna, w.ex.N_res)
    vouch = device.vouch(w.dora, n=50, scope=w.ex.N_res, t=T_ROOT, t_exp=T_EXP)
    store = _store(*w.base.values(), add_chris, add_anna, ack_chris, ack_anna, vouch)
    result = attribution(store, classify_all(store, NOW), w.ex.N_res)
    assert result.status(vouch) is AttributionStatus.ATTRIBUTED
    assert result.root(vouch) == w.chris.pub


def test_8_devices_do_not_add_devices() -> None:
    w = build()
    first = _device(1)
    second = _device(2)
    add_first = _add(w.chris, first, w.ex.N_res)
    ack_first = _ack(first, add_first, w.ex.N_res)
    add_second = _add(first, second, w.ex.N_res)
    ack_second = _ack(second, add_second, w.ex.N_res)
    vouch = second.vouch(w.dora, n=50, scope=w.ex.N_res, t=T_ROOT, t_exp=T_EXP)
    claims = [add_first, ack_first, add_second, ack_second, vouch]
    assert _status(w, claims, vouch) is AttributionStatus.OWN


def test_9_texp_on_add() -> None:
    w = build()
    device = _device(1)
    add = _add(w.chris, device, w.ex.N_res, t_exp=T_EXP)
    ack = _ack(device, add, w.ex.N_res)
    vouch = device.vouch(w.dora, n=50, scope=w.ex.N_res, t=T_ROOT, t_exp=T_EXP)
    assert _status(w, [add, ack, vouch], vouch) is AttributionStatus.OWN


def _fork(w: Verein, *, heal: bool) -> Derivation:
    device = _device(1)
    add = _add(w.bruno, device, w.ex.N_gov)
    ack = _ack(device, add, w.ex.N_gov)
    claims = [add, ack]
    if heal:
        claims.append(_end(w.bruno, device, w.ex.N_gov, _endpoint(claim_id(ack))))
    in_res = device._autor.gabeln(
        p=_nuc(w.ex.N_res, "vote"),
        J=(3, w.proposal_3.proposal_hash),
        t=T_ROOT,
        v=cbor_canon.encode({0: 0}),
        N=w.ex.N_res,
    )
    in_gov = device.claim(
        p=_nuc(w.ex.N_gov, "vote"),
        J=(3, w.proposal_3.proposal_hash),
        t=T_ROOT,
        v=cbor_canon.encode({0: 1}),
        N=w.ex.N_gov,
    )
    assert in_res.h_prev == in_gov.h_prev == claim_id(ack)
    return _derive(w, *claims, in_res, in_gov)


def test_10_fork_flags_globally_end_heals() -> None:
    w = build()
    bruno_edges = {e for e in _edges(_derive(w)) if e[0] == w.bruno.pub}
    assert bruno_edges

    w = build()
    assert not any(e[0] == w.bruno.pub for e in _edges(_fork(w, heal=False)))

    w = build()
    assert {e for e in _edges(_fork(w, heal=True)) if e[0] == w.bruno.pub} == bruno_edges


def test_11_add_irrevocable() -> None:
    w = build()
    device = _device(1)
    add = _add(w.chris, device, w.ex.N_res)
    revoke = w.chris.claim(p="core/revoke@1", J=(2, claim_id(add)), t=T_ROOT + 1)
    store = _store(*w.base.values(), add, revoke)
    assert classify_all(store, NOW)[claim_id(add)].state is State.ACTIVE


def test_12_malformed() -> None:
    # device-add@1 mit J-Tag nicht identity
    w = build()
    device = _device(1)
    add = w.chris.claim(p=_nuc(w.ex.N_res, "device-add"), J=(3, device.pub), t=T_ROOT, N=w.ex.N_res)
    ack = _ack(device, add, w.ex.N_res)
    vouch = device.vouch(w.dora, n=50, scope=w.ex.N_res, t=T_ROOT, t_exp=T_EXP)
    assert _status(w, [add, ack, vouch], vouch) is AttributionStatus.OWN
    _derive(w, add, ack, vouch)

    # device-add@1 auf den eigenen Schlüssel
    w = build()
    add = _add(w.chris, w.chris, w.ex.N_res)
    ack = _ack(w.chris, add, w.ex.N_res)
    vouch = w.chris.vouch(w.dora, n=50, scope=w.ex.N_res, t=T_ROOT, t_exp=T_EXP)
    assert _status(w, [add, ack, vouch], vouch) is AttributionStatus.OWN
    _derive(w, add, ack, vouch)

    # device-ack@1 mit J-Tag nicht claim-ref
    w = build()
    device = _device(1)
    add = _add(w.chris, device, w.ex.N_res)
    ack = device.claim(p=_nuc(w.ex.N_res, "device-ack"), J=(3, claim_id(add)), t=T_ROOT, N=w.ex.N_res)
    vouch = device.vouch(w.dora, n=50, scope=w.ex.N_res, t=T_ROOT, t_exp=T_EXP)
    assert _status(w, [add, ack, vouch], vouch) is AttributionStatus.OWN
    _derive(w, add, ack, vouch)

    # formwidriges device-ack@1 der Wurzel nimmt ihren Aufnahmen nicht die Wirkung (D537)
    w = build()
    device = _device(1)
    stray = w.chris.claim(
        p=_nuc(w.ex.N_res, "device-ack"),
        J=(3, hashlib.sha256(b"kein claim-ref").digest()),
        t=T_ROOT,
        N=w.ex.N_res,
    )
    add = _add(w.chris, device, w.ex.N_res)
    ack = _ack(device, add, w.ex.N_res)
    vouch = device.vouch(w.dora, n=50, scope=w.ex.N_res, t=T_ROOT, t_exp=T_EXP)
    assert _status(w, [stray, add, ack, vouch], vouch) is AttributionStatus.ATTRIBUTED
    _derive(w, stray, add, ack, vouch)

    # device-ack@1 auf ein device-add@1 für einen anderen Schlüssel
    w = build()
    named = _device(1)
    other = _device(2)
    add = _add(w.chris, named, w.ex.N_res)
    ack = _ack(other, add, w.ex.N_res)
    vouch = other.vouch(w.dora, n=50, scope=w.ex.N_res, t=T_ROOT, t_exp=T_EXP)
    assert _status(w, [add, ack, vouch], vouch) is AttributionStatus.OWN
    _derive(w, add, ack, vouch)

    # device-end@1 einer anderen Identität als der Wurzel
    w = build()
    device = _device(1)
    add = _add(w.chris, device, w.ex.N_res)
    ack = _ack(device, add, w.ex.N_res)
    vouch = device.vouch(w.dora, n=50, scope=w.ex.N_res, t=T_ROOT, t_exp=T_EXP)
    end = _end(w.anna, device, w.ex.N_res, _endpoint(claim_id(ack)))
    assert _status(w, [add, ack, vouch, end], vouch) is AttributionStatus.ATTRIBUTED
    _derive(w, add, ack, vouch, end)
