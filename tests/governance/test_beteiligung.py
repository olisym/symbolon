"""Beteiligung: Enthaltung, Ruhen, Rückkehr, Kennung (04 §1.1, §2.2, §2.6, §3.1, §3.2, §3.4,
§3.5, §4.1, §4.4, §4.7, §9.3, §9.4; D689 bis D693).

Vektoren ``BV-1`` bis ``BV-43`` aus ``04-golden-anchors.md §14``. Jede Identität frisch (D464).
"""

from __future__ import annotations

import pytest

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id
from symbolon.genesis import genesis_scope
from symbolon.governance import decide, verify_ratification
from symbolon.governance.election import BallotList, Election, ElectionState, tally_election
from symbolon.governance.findings import Finding, GovernanceFinding as GF
from symbolon.governance.objects import Epoch, Proposal
from symbolon.governance.tally import TallyState, current_ballot, reached
from symbolon.policy import constitution_hash
from tests.helpers import Identity, store_with

from .fixtures import (
    C1,
    GENESIS_D,
    N_D,
    NOW,
    _constitution,
    fresh_eve,
    fresh_frank,
    fresh_p1,
    nuc,
    policy_of,
)

PART = "participation@1"
TH_VEREIN = {"ordinary": [1, 2], "membership": [1, 2], "amendment": [2, 3]}
IRR_B = ["obligation@1", "ratify@1", "rest@1", "vote@1"]
WEG = object()


def _verfassung(pubs: list[bytes], thresholds: dict = TH_VEREIN, **aend: object) -> dict:
    """``CB`` aus ``04-golden-anchors.md §14``; ``WEG`` nimmt ein Feld heraus."""
    c = _constitution(participants=sorted(pubs), thresholds=thresholds, irrevocable=IRR_B)
    c["required_features"] = [PART]
    for k, v in aend.items():
        if v is WEG:
            c.pop(k, None)
        else:
            c[k] = v
    return c


class Welt:
    """Epoche 1 eines eigenen Genesis (wie ``§12``), sechs Wurzeln ALICE bis FRANK."""

    def __init__(self, *, extra: int = 0, thresholds: dict = TH_VEREIN, **aend: object) -> None:
        self.alice, self.bob, self.carol, self.dave = fresh_p1()
        self.eve, self.frank = fresh_eve(), fresh_frank()
        self.weitere = [Identity(f"BV-W{i}") for i in range(extra)]
        self.alle = [self.alice, self.bob, self.carol, self.dave, self.eve, self.frank,
                     *self.weitere]
        resolved = {k: (v(self) if callable(v) else v) for k, v in aend.items()}
        self.verfassung = _verfassung([w.pub for w in self.alle], thresholds, **resolved)
        self.genesis = {**GENESIS_D, 4: constitution_hash(self.verfassung), 5: 2}
        self.scope = genesis_scope(self.genesis)
        self.epoch = Epoch(scope=self.scope, index=1,
                           constitution_hash=constitution_hash(self.verfassung))
        self.claims: list[Claim] = []
        self._t = 0

    def t(self) -> int:
        self._t += 1
        return self._t

    def ziel(self, arbitrator: Identity | None = None, **aend: object) -> dict:
        z = dict(self.verfassung)
        if arbitrator is not None:
            z["arbitration"] = {"arbitrators": [arbitrator.pub]}
        z.update(aend)
        return z

    def vorschlag(self, ziel: dict) -> Proposal:
        return Proposal(scope=self.scope, predecessor=self.epoch.epoch_id,
                        constitution_hash=constitution_hash(ziel))

    def stimme(self, who: Identity, h: bytes, choice: int, names: list[bytes] | None = None
               ) -> Claim:
        v: dict[int, object] = {0: choice}
        if names is not None:
            v[1] = names
        c = who.claim(p=nuc(self.scope, "vote"), J=(3, h), t=self.t(), N=self.scope,
                      v=cbor_canon.encode(v))
        self.claims.append(c)
        return c

    def ruhe(self, who: Identity, *, index: int = 1, names: list[bytes] | None = None,
             t_exp: int | None = None) -> Claim:
        v: dict[int, object] = {0: index}
        if names is not None:
            v[1] = names
        c = who.claim(p=nuc(self.scope, "rest"), J=(3, self.epoch.epoch_id), t=self.t(),
                      N=self.scope, v=cbor_canon.encode(v), t_exp=t_exp)
        self.claims.append(c)
        return c

    def vier(self, h: bytes) -> list[Claim]:
        return [self.stimme(w, h, 1) for w in (self.alice, self.bob, self.carol, self.dave)]

    def zaehle(self, p: Proposal, ziel: dict, known: dict | None = None):
        known = known or {p.proposal_hash: p}
        return decide(store_with(*self.claims), epoch=self.epoch, proposal=p,
                      genesis_obj=self.genesis, constitution_obj=self.verfassung,
                      target_constitution_obj=ziel, known_proposals=known, now=NOW,
                      policy=policy_of(self.verfassung, self.scope),
                      known_constitutions={constitution_hash(ziel): ziel})

    def geltend(self, known: dict, ziele: list[dict]) -> int:
        return current_ballot(store_with(*self.claims), epoch=self.epoch,
                              genesis_obj=self.genesis, constitution_obj=self.verfassung,
                              known_proposals=known,
                              known_constitutions={constitution_hash(z): z for z in ziele},
                              now=NOW, policy=policy_of(self.verfassung, self.scope))


def _arten(result) -> set[GF]:
    return {f.kind for f in result.findings}


def _xb(w: Welt) -> tuple[Proposal, dict]:
    z = w.ziel(w.bob)
    return w.vorschlag(z), z


def test_schwellen_liegen_auf_verschiedenen_seiten() -> None:
    """Vier Ja erreichen ``[2,3]`` bei ``n = 6`` nicht, bei ``n = 5`` schon (§14)."""
    assert not reached(4, 6, 2, 3) and reached(4, 5, 2, 3)


# --- 14.1 Enthaltung und Ruhen ----------------------------------------------------

def test_bv_1() -> None:
    w = Welt(); p, z = _xb(w); w.vier(p.proposal_hash)
    r = w.zaehle(p, z)
    assert (r.state, r.n) == (TallyState.PENDING, 6)


def test_bv_2() -> None:
    w = Welt(); p, z = _xb(w); w.vier(p.proposal_hash); w.stimme(w.eve, p.proposal_hash, 2)
    r = w.zaehle(p, z)
    assert (r.state, r.n) == (TallyState.PASSED, 5)


def test_bv_3() -> None:
    w = Welt(required_features=WEG, irrevocable_predicates=["obligation@1", "ratify@1",
                                                            "vote@1"])
    p, z = _xb(w); w.vier(p.proposal_hash); e = w.stimme(w.eve, p.proposal_hash, 2)
    r = w.zaehle(p, z)
    assert (r.state, r.n) == (TallyState.PENDING, 6)
    assert Finding(kind=GF.UNKNOWN_VOTE_CHOICE, subject=claim_id(e)) in r.findings


def test_bv_4() -> None:
    w = Welt(); p, z = _xb(w); w.vier(p.proposal_hash); w.ruhe(w.eve)
    r = w.zaehle(p, z)
    assert (r.state, r.n) == (TallyState.PASSED, 5)


def test_bv_5() -> None:
    w = Welt(resting=lambda w: [w.frank.pub]); p, z = _xb(w); w.vier(p.proposal_hash)
    r = w.zaehle(p, z)
    assert (r.state, r.n) == (TallyState.PASSED, 5)


def test_bv_6() -> None:
    w = Welt(resting=lambda w: [w.frank.pub]); p, z = _xb(w)
    for who in (w.alice, w.bob, w.carol):
        w.stimme(who, p.proposal_hash, 1)
    f = w.stimme(w.frank, p.proposal_hash, 1)
    r = w.zaehle(p, z)
    assert (r.state, r.n, len(r.yes)) == (TallyState.PENDING, 5, 3)
    assert Finding(kind=GF.RESTING_VOTE, subject=claim_id(f)) in r.findings


def test_bv_7() -> None:
    w = Welt(); p, z = _xb(w); w.vier(p.proposal_hash)
    e = w.stimme(w.eve, p.proposal_hash, 1); w.ruhe(w.eve, names=[claim_id(e)])
    r = w.zaehle(p, z)
    assert (r.state, r.n, len(r.yes)) == (TallyState.PASSED, 6, 5)


def test_bv_8() -> None:
    w = Welt(); p, z = _xb(w); w.vier(p.proposal_hash)
    e = w.stimme(w.eve, p.proposal_hash, 1); rest = w.ruhe(w.eve)
    r = w.zaehle(p, z)
    assert (r.state, r.n, len(r.yes)) == (TallyState.PENDING, 6, 4)
    for c in (e, rest):
        assert Finding(kind=GF.AMBIGUOUS_REST, subject=claim_id(c)) in r.findings


def test_bv_9() -> None:
    w = Welt(); p, z = _xb(w); w.vier(p.proposal_hash)
    rest = w.ruhe(w.eve); e = w.stimme(w.eve, p.proposal_hash, 1, [claim_id(rest)])
    r = w.zaehle(p, z)
    assert (r.state, r.n) == (TallyState.PASSED, 5)
    assert Finding(kind=GF.RESTING_VOTE, subject=claim_id(e)) in r.findings


def test_bv_10() -> None:
    w = Welt(); p, z = _xb(w); w.vier(p.proposal_hash)
    e = w.stimme(w.eve, p.proposal_hash, 2, [bytes(32)])
    r = w.zaehle(p, z)
    assert (r.state, r.n) == (TallyState.PENDING, 6)
    assert Finding(kind=GF.ABSTENTION_WITH_REPLACES, subject=claim_id(e)) in r.findings


def test_bv_11() -> None:
    w = Welt(); p, z = _xb(w); w.vier(p.proposal_hash)
    a = w.stimme(w.eve, p.proposal_hash, 1); b = w.stimme(w.eve, p.proposal_hash, 2)
    r = w.zaehle(p, z)
    assert (r.state, r.n) == (TallyState.PENDING, 6)
    for c in (a, b):
        assert Finding(kind=GF.AMBIGUOUS_VOTE, subject=claim_id(c)) in r.findings


def test_bv_12() -> None:
    w = Welt(); p, z = _xb(w); w.vier(p.proposal_hash)
    a = w.stimme(w.eve, p.proposal_hash, 2); b = w.stimme(w.eve, p.proposal_hash, 0, [claim_id(a)])
    r = w.zaehle(p, z)
    assert (r.state, r.n) == (TallyState.PENDING, 6)
    for c in (a, b):
        assert Finding(kind=GF.AMBIGUOUS_VOTE, subject=claim_id(c)) in r.findings


def test_bv_13() -> None:
    w = Welt(); p, z = _xb(w); w.vier(p.proposal_hash); w.ruhe(w.eve, names=[bytes([7]) * 32])
    r = w.zaehle(p, z)
    assert (r.state, r.n) == (TallyState.PENDING, 6)


def test_bv_14() -> None:
    w = Welt(); p, z = _xb(w); w.vier(p.proposal_hash)
    rest = w.ruhe(w.eve, t_exp=NOW + 10**6)
    r = w.zaehle(p, z)
    assert (r.state, r.n) == (TallyState.PENDING, 6)
    assert Finding(kind=GF.REST_WITH_EXPIRY, subject=claim_id(rest)) in r.findings


def test_bv_15() -> None:
    w = Welt(); p, z = _xb(w); w.vier(p.proposal_hash); w.ruhe(w.eve, index=2)
    r = w.zaehle(p, z)
    assert (r.state, r.n) == (TallyState.PENDING, 6)


def test_bv_16() -> None:
    w = Welt(returned=lambda w: {w.eve.pub: 2}); p, z = _xb(w); w.vier(p.proposal_hash)
    w.ruhe(w.eve)
    r = w.zaehle(p, z)
    assert (r.state, r.n) == (TallyState.PENDING, 6)


# --- 14.2 Rivalen -----------------------------------------------------------------

def _rivalen(w: Welt) -> tuple[Proposal, dict, Proposal, dict, dict]:
    zx, zy = w.ziel(w.bob), w.ziel(w.carol)
    px, py = w.vorschlag(zx), w.vorschlag(zy)
    return px, zx, py, zy, {px.proposal_hash: px, py.proposal_hash: py}


def test_bv_17() -> None:
    w = Welt(); px, zx, py, _zy, known = _rivalen(w)
    w.vier(px.proposal_hash); w.stimme(w.eve, py.proposal_hash, 1)
    w.stimme(w.eve, px.proposal_hash, 2)
    r = w.zaehle(px, zx, known)
    assert (r.state, r.n) == (TallyState.PENDING, 6)


def test_bv_18() -> None:
    w = Welt(); p, z = _xb(w); w.vier(p.proposal_hash)
    w.stimme(w.eve, bytes([9]) * 32, 1); w.stimme(w.eve, p.proposal_hash, 2)
    r = w.zaehle(p, z)
    assert (r.state, r.n) == (TallyState.PENDING, 6)


def test_bv_19() -> None:
    w = Welt(); px, zx, py, _zy, known = _rivalen(w)
    w.vier(px.proposal_hash); e = w.stimme(w.eve, py.proposal_hash, 1)
    w.ruhe(w.eve, names=[claim_id(e)])
    r = w.zaehle(px, zx, known)
    assert (r.state, r.n) == (TallyState.PENDING, 6)


def test_bv_20() -> None:
    """D692 Befund 1: ohne die Sperre kommen beide durch."""
    halb = {"ordinary": [1, 2], "membership": [1, 2], "amendment": [1, 2]}
    w = Welt(extra=4, thresholds=halb); px, zx, py, zy, known = _rivalen(w)
    a, b = w.alle[:4], w.alle[4:9]
    for who in a:
        w.stimme(who, px.proposal_hash, 1); w.stimme(who, py.proposal_hash, 2)
    for i, who in enumerate(b):
        w.stimme(who, py.proposal_hash, 1)
        if i < 3:
            w.stimme(who, px.proposal_hash, 2)
    rx, ry = w.zaehle(px, zx, known), w.zaehle(py, zy, known)
    assert (rx.state, rx.n) == (TallyState.PENDING, 10)
    assert (ry.state, ry.n) == (TallyState.PENDING, 10)


# --- 14.3 Klasse und Form -----------------------------------------------------------

def test_bv_21() -> None:
    w = Welt(); z = w.ziel(resting=sorted([w.eve.pub, w.frank.pub])); p = w.vorschlag(z)
    w.vier(p.proposal_hash)
    r = w.zaehle(p, z)
    assert (r.state, r.threshold) == (TallyState.PASSED, (1, 2))


def test_bv_22() -> None:
    w = Welt(); z = w.ziel(w.bob, resting=sorted([w.eve.pub, w.frank.pub])); p = w.vorschlag(z)
    w.vier(p.proposal_hash)
    r = w.zaehle(p, z)
    assert (r.state, r.threshold) == (TallyState.PENDING, (2, 3))


def test_bv_23() -> None:
    w = Welt(); z = w.ziel(returned={w.eve.pub: 2}); p = w.vorschlag(z)
    w.vier(p.proposal_hash)
    r = w.zaehle(p, z)
    assert (r.state, r.threshold) == (TallyState.PASSED, (1, 2))


@pytest.mark.parametrize(
    ("vektor", "aend", "art"),
    [
        ("BV-24", {"required_features": [PART, "x-unbekannt@1"]}, GF.UNSUPPORTED_FEATURE),
        ("BV-25", {"required_features": []}, GF.MALFORMED_REQUIRED_FEATURES),
        ("BV-26", {"required_features": ["x-unbekannt@1"], "participants": []},
         GF.UNSUPPORTED_FEATURE),
        ("BV-27", {"required_features": WEG, "resting": lambda w: [w.frank.pub]},
         GF.MALFORMED_RESTING),
        ("BV-28", {"resting": lambda _w: [bytes([3]) * 32]}, GF.MALFORMED_RESTING),
        ("BV-29", {"resting": lambda w: sorted([w.eve.pub, w.frank.pub], reverse=True)},
         GF.MALFORMED_RESTING),
        ("BV-30", {"returned": lambda w: {w.eve.pub: 0}}, GF.MALFORMED_RESTING),
        ("BV-31", {"irrevocable_predicates": ["obligation@1", "ratify@1", "vote@1"]},
         GF.REST_REVOCABLE),
    ],
)
def test_bv_24_bis_31(vektor: str, aend: dict, art: GF) -> None:
    w = Welt(**aend); p, z = _xb(w); w.vier(p.proposal_hash)
    r = w.zaehle(p, z)
    assert r.state is TallyState.UNEVALUABLE, vektor
    assert r.findings == (Finding(kind=art, subject=w.epoch.constitution_hash),), vektor


def test_bv_32() -> None:
    w = Welt(); z = w.ziel(required_features=[PART, "x-unbekannt@1"]); p = w.vorschlag(z)
    ja = [w.stimme(who, p.proposal_hash, 1) for who in w.alle[:5]]
    t = w.zaehle(p, z)
    assert t.state is TallyState.PASSED
    rat = w.alice.claim(p=nuc(w.scope, "ratify"), J=(3, p.proposal_hash), t=w.t(), N=w.scope,
                        v=cbor_canon.encode({0: [claim_id(c) for c in ja]}))
    w.claims.append(rat)
    r = verify_ratification(store_with(*w.claims), ratify=rat, epoch=w.epoch, proposal=p,
                            tally=w.zaehle(p, z), target_constitution_obj=z, now=NOW,
                            policy=policy_of(w.verfassung, w.scope))
    assert r.next_epoch is None
    assert Finding(kind=GF.UNSUPPORTED_FEATURE, subject=p.constitution_hash) in r.findings


# --- 14.4 Patt ----------------------------------------------------------------------

def _patt(w: Welt) -> tuple[dict, list[dict], Proposal, Proposal]:
    px, zx, py, zy, known = _rivalen(w)
    w.stimme(w.alice, px.proposal_hash, 1); w.stimme(w.bob, px.proposal_hash, 1)
    w.stimme(w.carol, py.proposal_hash, 1)
    return known, [zx, zy], px, py


def test_bv_33() -> None:
    w = Welt(); known, ziele, _px, _py = _patt(w)
    assert w.geltend(known, ziele) == 0


def test_bv_34() -> None:
    w = Welt(); known, ziele, _px, _py = _patt(w)
    for who in (w.dave, w.eve, w.frank):
        w.ruhe(who)
    assert w.geltend(known, ziele) == 1


def test_bv_35() -> None:
    w = Welt(resting=lambda w: sorted([w.dave.pub, w.eve.pub, w.frank.pub]))
    known, ziele, _px, _py = _patt(w)
    assert w.geltend(known, ziele) == 1


def test_bv_36() -> None:
    w = Welt(); known, ziele, px, py = _patt(w)
    for who in (w.dave, w.eve, w.frank):
        w.stimme(who, px.proposal_hash, 2); w.stimme(who, py.proposal_hash, 2)
    assert w.geltend(known, ziele) == 1


# --- 14.5 Geheime Wahl --------------------------------------------------------------

IRR_WAHL_B = ["ballot-ack@1", "ballot@1", "obligation@1", "ratify@1", "rest@1", "vote@1"]


class Wahl:
    """Die Welt aus ``§13`` mit ``participation@1``."""

    def __init__(self, *, kennung: bool = True, resting: bool = False) -> None:
        self.alice, self.bob, self.carol, self.dave = fresh_p1()
        c = _constitution(participants=C1["participants"], irrevocable=IRR_WAHL_B)
        if kennung:
            c["required_features"] = [PART]
        if resting:
            c["resting"] = [self.dave.pub]
        self.constitution = c
        self.epoch = Epoch(scope=N_D, index=1, constitution_hash=constitution_hash(c))
        self.k = {i: Identity(f"BV-K{i}") for i in range(1, 6)}
        self.wahl = Election({0: N_D, 1: self.epoch.epoch_id, 2: "vorstand",
                              3: sorted([self.alice.pub, self.bob.pub]), 4: "Vorstand 2026"})
        self.claims: list[Claim] = []
        self.objekte = {self.wahl.election_hash: self.wahl}
        self.t = 1

    def liste(self, members: list[Identity], keys: list[Identity]) -> BallotList:
        lst = BallotList({0: self.wahl.election_hash, 1: sorted(m.pub for m in members),
                          2: sorted(k.pub for k in keys)})
        self.objekte[lst.list_hash] = lst
        for ident in [*members, *keys]:
            self.t += 1
            self.claims.append(ident.claim(p=nuc(N_D, "ballot-ack"), J=(3, lst.list_hash),
                                           t=self.t, N=N_D))
        return lst

    def lv(self, ohne_dave: bool = False) -> BallotList:
        m = [self.alice, self.bob, self.carol] + ([] if ohne_dave else [self.dave])
        k = [self.k[1], self.k[2], self.k[3]] + ([] if ohne_dave else [self.k[4]])
        return self.liste(m, k)

    def stimme(self, key: Identity, kandidat: bytes, wahlgang: int = 0) -> Claim:
        self.t += 1
        c = key.claim(p=nuc(N_D, "ballot"), J=(3, self.wahl.election_hash), t=self.t, N=N_D,
                      v=cbor_canon.encode({0: kandidat, 1: wahlgang}))
        self.claims.append(c)
        return c

    def zaehlen(self):
        return tally_election(store_with(*self.claims), scope=N_D, election=self.wahl,
                              epoch=self.epoch, constitution_obj=self.constitution,
                              known_objects=self.objekte, now=NOW,
                              policy=policy_of(self.constitution))


E = b""


def test_bv_37() -> None:
    w = Wahl(); w.lv()
    w.stimme(w.k[1], w.alice.pub); w.stimme(w.k[2], w.alice.pub); w.stimme(w.k[3], E)
    r = w.zaehlen()
    assert (r.state, r.elected) == (ElectionState.ELECTED, w.alice.pub)


def test_bv_38() -> None:
    w = Wahl(kennung=False); w.lv()
    w.stimme(w.k[1], w.alice.pub); w.stimme(w.k[2], w.alice.pub); w.stimme(w.k[3], E)
    r = w.zaehlen()
    assert (r.state, r.current_round) == (ElectionState.OPEN, 0)


def test_bv_39() -> None:
    w = Wahl(); w.lv()
    w.stimme(w.k[1], w.alice.pub); w.stimme(w.k[2], w.alice.pub)
    a = w.stimme(w.k[3], E); b = w.stimme(w.k[3], w.alice.pub)
    r = w.zaehlen()
    assert (r.state, r.current_round) == (ElectionState.OPEN, 0)
    for c in (a, b):
        assert Finding(kind=GF.AMBIGUOUS_BALLOT, subject=claim_id(c)) in r.findings


def test_bv_40() -> None:
    w = Wahl(resting=True); w.lv(ohne_dave=True)
    w.stimme(w.k[1], w.alice.pub); w.stimme(w.k[2], w.alice.pub)
    r = w.zaehlen()
    assert (r.state, r.elected) == (ElectionState.ELECTED, w.alice.pub)


def test_bv_41() -> None:
    w = Wahl(resting=True); w.lv()
    w.stimme(w.k[1], w.alice.pub); w.stimme(w.k[2], w.alice.pub)
    r = w.zaehlen()
    assert (r.state, r.current_round, r.lists) == (ElectionState.OPEN, 0, ())


def test_bv_42() -> None:
    w = Wahl(); w.lv()
    w.stimme(w.k[1], w.alice.pub); w.stimme(w.k[2], w.alice.pub)
    w.t += 1
    w.claims.append(w.dave.claim(p=nuc(N_D, "rest"), J=(3, w.epoch.epoch_id), t=w.t, N=N_D,
                                 v=cbor_canon.encode({0: 1})))
    r = w.zaehlen()
    assert (r.state, r.current_round) == (ElectionState.OPEN, 0)


def test_bv_43() -> None:
    w = Wahl(); w.lv()
    w.stimme(w.k[1], w.alice.pub); w.stimme(w.k[2], w.bob.pub)
    w.stimme(w.k[3], E); w.stimme(w.k[4], E)
    r = w.zaehlen()
    assert (r.state, r.current_round) == (ElectionState.OPEN, 1)
