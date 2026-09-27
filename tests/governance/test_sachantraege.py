"""Sachanträge: Objekt, Auszählung, die drei Regeln, Klasse, Bedingung 7, Fassung
(04 §2.4, 04 §2.5, 04 §3.4, 04 §3.5, 04 §4.1, 04 §4.4, 04 §4.6, D567, D568).

Vektoren ``GV-59`` bis ``GV-89`` aus ``04-golden-anchors.md §10``.
"""

from __future__ import annotations

import itertools

import pytest

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id
from symbolon.governance import decide, verify_ratification
from symbolon.governance.findings import Finding, GovernanceFinding as GF
from symbolon.governance.objects import Epoch, Motion, Proposal, apply_motions
from symbolon.governance.tally import TallyState
from symbolon.policy import constitution_hash
from tests.helpers import Identity, store_with

from .fixtures import (
    C1,
    C2,
    EPOCH_1,
    EPOCH_2,
    GENESIS_D,
    N_D,
    NOW,
    P2,
    PROPOSAL_1,
    fresh_p1,
    nuc,
    policy_of,
)

E1 = EPOCH_1.epoch_id


def _motion(changes: dict, *, scope: bytes = N_D, predecessor: bytes = E1, extra=None) -> Motion:
    obj: dict = {0: scope, 1: predecessor, 2: changes}
    if extra:
        obj.update(extra)
    return Motion(obj)


M1 = _motion({"beitrag": [[], ["30 EUR"]]})
M2 = _motion({"beitrag": [[], ["50 EUR"]]})
M3 = _motion({"beitrag": [["30 EUR"], ["40 EUR"]]})
M4 = _motion({"name": [[], ["Gartenverein"]]})
M5 = _motion({"x": [[1], [2]]})
M6 = _motion({"x": [[True], [3]]})
M7 = _motion({"x": [[], [1]]})
M_RULE = _motion({"participants": [[], [P2]]})  # GV-71
M_NOOP = _motion({"beitrag": [[], []]})  # GV-68: formwidrig, teilte sonst die Vorbedingung von M1

C1S = {**C1, "beitrag": "30 EUR"}
C2S = {**C1S, "participants": C2["participants"]}
G1 = Proposal(N_D, E1, constitution_hash(C2S), (M1.motion_hash,))
G0 = Proposal(N_D, E1, constitution_hash(C2S))
EPOCH_2S = Epoch(scope=N_D, index=2, constitution_hash=constitution_hash(C2S))

DOC = {
    "M1": "731e27631d0580b438a572fb35d2c19f4708f5e471d2f6e1e58e95a45d5c3fd5",
    "M2": "2cdde5b476d3c1973d9c4a7804b3d2cae9abd43ae90069b295d15daaf2210a0e",
    "M3": "00cefced49b449a4896f8740a4d9f5ba6181183ed9d75e2e98f3d4a2958cc1f3",
    "M4": "c739cea70e6de4ef21a3d2c543ed399938bd2321d55f430f1b84072382380d7b",
    "M5": "654f535bd3966fb420e7539345755e9c196ad7929372ae89e75bdd0e27c471c3",
    "M6": "af39623b3367c128b2c2bda23f69e9a206725d6eff66fe23a998af401c616159",
    "M7": "8802b10e30d5d4bfcf8910d43e7a8ce80f3fc9dd826e9fd5d93ea296169b4155",
}
DOC_C2S = "0eebc02acb5619f5769e9a18f28bfdd2f7691408bbcfe1826f0dc5d952e40b49"
DOC_G1 = "6c54b07afa790d67d792dafcd53f5ffd219a565b530a09c209593b0c83cef16d"
DOC_G0 = "bd1621e5170206d5315bc7f9322f09b64b717487d217a7c2e919b6ddbb1785c1"
DOC_E2S = "9804aa920a51ac99302b6407a6622df5eeaa15751c1fcf4a35b33f5f7ee92aae"
DOC_CBOR_M1 = (
    "a3005820a15c70c4829e7a296b5af56656e0a94b9ea9391096515c9cc592e18bd2d9f7ef"
    "01582056915063c07ce1e6b74e10712e8f17b9f381af359a3e12b9719e90a52483d724"
    "02a1676265697472616782808166333020455552"
)

KNOWN = {o.motion_hash: o for o in (M1, M2, M3, M4, M5, M6, M7, M_RULE, M_NOOP)}
KNOWN.update({G1.proposal_hash: G1, G0.proposal_hash: G0, PROPOSAL_1.proposal_hash: PROPOSAL_1})


def _h(obj) -> bytes:
    return obj.motion_hash if isinstance(obj, Motion) else obj.proposal_hash


class _Welt:
    def __init__(self) -> None:
        self.alice, self.bob, self.carol, self.dave = fresh_p1()
        self.claims: list[Claim] = []
        self._t = 0

    def t(self) -> int:
        self._t += 1
        return self._t

    def ja(self, who: Identity, obj_hash: bytes, choice: int = 1) -> Claim:
        c = who.claim(p=nuc(N_D, "vote"), J=(3, obj_hash), t=self.t(), N=N_D,
                      v=cbor_canon.encode({0: choice}))
        self.claims.append(c)
        return c

    def ratify(self, who: Identity, obj_hash: bytes, witnesses: list[Claim]) -> Claim:
        c = who.claim(p=nuc(N_D, "ratify"), J=(3, obj_hash), t=self.t(), N=N_D,
                      v=cbor_canon.encode({0: [claim_id(w) for w in witnesses]}))
        self.claims.append(c)
        return c

    def store(self):
        return store_with(*self.claims)


def _decide(store, obj, *, known=KNOWN, epoch=EPOCH_1, target="auto"):
    if target == "auto":
        target = None if isinstance(obj, Motion) else {
            constitution_hash(C2S): C2S, constitution_hash(C2): C2}.get(obj.constitution_hash)
    return decide(store, epoch=epoch, proposal=obj, genesis_obj=GENESIS_D,
                  constitution_obj=C1, target_constitution_obj=target,
                  known_proposals=known, now=NOW, policy=policy_of(C1))


def _kinds(result) -> set[GF]:
    return {f.kind for f in result.findings}


# --- 10.1 Objekte -------------------------------------------------------------

def test_anker_objekte() -> None:
    for name, hexed in DOC.items():
        assert globals()[name].motion_hash.hex() == hexed, name
    assert cbor_canon.encode(M1.obj).hex() == DOC_CBOR_M1
    assert constitution_hash(C2S).hex() == DOC_C2S
    assert G1.proposal_hash.hex() == DOC_G1
    assert G0.proposal_hash.hex() == DOC_G0
    assert EPOCH_2S.epoch_id.hex() == DOC_E2S
    assert PROPOSAL_1.proposal_hash.hex().startswith("38edfd6b")


def test_1_und_true_kodieren_verschieden() -> None:
    assert cbor_canon.encode([1]).hex() == "8101"
    assert cbor_canon.encode([True]).hex() == "81f5"


# --- 10.2 Auszählung und Klasse ------------------------------------------------

def test_gv59_gv60_ordinary() -> None:
    w = _Welt()
    w.ja(w.alice, M1.motion_hash)
    w.ja(w.bob, M1.motion_hash)
    r = _decide(w.store(), M1)
    assert r.state is TallyState.PENDING and r.threshold == (1, 2)
    w.ja(w.carol, M1.motion_hash)
    r = _decide(w.store(), M1)
    assert r.state is TallyState.PASSED and r.findings == ()
    assert r.proposal_hash == M1.motion_hash


def test_gv61_gv62_klasse_gegen_fassung_aus_s() -> None:
    w1 = _Welt()
    for who in (w1.bob, w1.alice, w1.dave):
        w1.ja(who, G1.proposal_hash)
    r1 = _decide(w1.store(), G1)
    assert r1.threshold == (2, 3) and r1.state is TallyState.PASSED
    w0 = _Welt()
    for who in (w0.bob, w0.alice, w0.dave):
        w0.ja(who, G0.proposal_hash)
    r0 = _decide(w0.store(), G0)
    assert r0.threshold == (3, 4) and r0.state is TallyState.PENDING


# --- 10.3 Vereinbare und unvereinbare Ja ----------------------------------------

def _m1_abc(w: _Welt) -> None:
    for who in (w.alice, w.bob, w.carol):
        w.ja(who, M1.motion_hash)


def _g1_bad(w: _Welt) -> None:
    for who in (w.bob, w.alice, w.dave):
        w.ja(who, G1.proposal_hash)


@pytest.mark.parametrize(
    ("vektor", "basis", "zusatz", "zustand", "konflikt"),
    [
        ("GV-63", "M1", [M2.motion_hash], TallyState.PENDING, True),
        ("GV-64", "M1", [M3.motion_hash, M4.motion_hash], TallyState.PASSED, False),
        ("GV-65", "G1", [M4.motion_hash], TallyState.PENDING, True),
        ("GV-66", "G1", [M1.motion_hash], TallyState.PASSED, False),
        ("GV-67", "M1", [PROPOSAL_1.proposal_hash], TallyState.PENDING, True),
        ("GV-68", "M1", [M_NOOP.motion_hash], TallyState.PASSED, False),
    ],
)
def test_gv63_bis_gv68(vektor, basis, zusatz, zustand, konflikt) -> None:
    w = _Welt()
    (_m1_abc if basis == "M1" else _g1_bad)(w)
    extra = [w.ja(w.alice, h) for h in zusatz]
    obj = M1 if basis == "M1" else G1
    r = _decide(w.store(), obj)
    assert r.state is zustand, vektor
    subjects = {f.subject for f in r.findings if f.kind is GF.CONFLICTING_APPROVAL}
    if konflikt:
        assert {claim_id(c) for c in extra} <= subjects, vektor
    else:
        assert r.findings == (), vektor


def test_gv69_unbekanntes_objekt_blockiert() -> None:
    w = _Welt()
    _m1_abc(w)
    fremd = w.ja(w.alice, bytes(range(32)))
    r = _decide(w.store(), M1)
    assert r.state is TallyState.PENDING
    assert Finding(kind=GF.UNKNOWN_PROPOSAL, subject=claim_id(fremd)) in r.findings


def test_gv70_vorbedingung_nach_kodierung() -> None:
    w = _Welt()
    for m in (M5, M6, M7):
        for who in (w.alice, w.bob, w.carol, w.dave):
            w.ja(who, m.motion_hash)
    store = w.store()
    for m in (M5, M6, M7):
        r = _decide(store, m)
        assert r.state is TallyState.PASSED and r.findings == (), m.obj


# --- 10.4 Formwidrigkeit ------------------------------------------------------

_FORMWIDRIG = [
    ("GV-71", M_RULE),
    ("GV-72", _motion({"beitrag": [["30 EUR"], ["30 EUR"]]})),
    ("GV-73", _motion({"beitrag": [[], ["30 EUR"]]}, extra={3: 0})),
    ("GV-74", _motion({})),
    ("GV-75", _motion({"beitrag": [[[], []], ["30 EUR"]]})),
    ("GV-76", _motion({7: [[], ["30 EUR"]]})),
    ("GV-77", _motion({"participants": [[], [P2]]}, scope=bytes(32))),
]


@pytest.mark.parametrize(("vektor", "motion"), _FORMWIDRIG)
def test_gv71_bis_gv77_formwidriger_sachantrag(vektor, motion) -> None:
    r = _decide(store_with(), motion, known={motion.motion_hash: motion})
    assert r.state is TallyState.UNEVALUABLE, vektor
    assert r.findings == (Finding(kind=GF.MALFORMED_MOTION, subject=motion.motion_hash),), vektor


def _g(motions) -> Proposal:
    return Proposal(N_D, E1, constitution_hash(C2S), motions)


M_E2 = _motion({"beitrag": [[], ["30 EUR"]]}, predecessor=EPOCH_2.epoch_id)


@pytest.mark.parametrize(
    ("vektor", "motions"),
    [
        ("GV-78", []),
        ("GV-79", [M1.motion_hash, M3.motion_hash]),
        ("GV-80", [M2.motion_hash, M1.motion_hash]),
        ("GV-81", [PROPOSAL_1.proposal_hash]),
        ("GV-82", [M_E2.motion_hash]),
    ],
)
def test_gv78_bis_gv82_formwidriger_vorschlag(vektor, motions) -> None:
    g = _g(motions)
    known = {**KNOWN, M_E2.motion_hash: M_E2, g.proposal_hash: g}
    r = _decide(store_with(), g, known=known)
    assert r.state is TallyState.UNEVALUABLE, vektor
    assert r.findings == (Finding(kind=GF.MALFORMED_PROPOSAL, subject=g.proposal_hash),), vektor


def test_gv83_formwidriger_sachantrag_in_s() -> None:
    g = _g([M_RULE.motion_hash])
    r = _decide(store_with(), g, known={**KNOWN, g.proposal_hash: g})
    assert r.findings == (Finding(kind=GF.MALFORMED_MOTION, subject=M_RULE.motion_hash),)


def test_gv84_sachantrag_in_s_unbekannt() -> None:
    known = {h: o for h, o in KNOWN.items() if h != M1.motion_hash}
    r = _decide(store_with(), G1, known=known)
    assert r.state is TallyState.UNEVALUABLE
    assert r.findings == (Finding(kind=GF.MOTION_UNAVAILABLE, subject=M1.motion_hash),)


# --- 10.5 Feststellung und Fassung --------------------------------------------

def test_gv85_gv86_bedingung_7() -> None:
    w = _Welt()
    g_ja = [w.ja(who, G1.proposal_hash) for who in (w.bob, w.alice, w.dave)]
    m_ja = [w.ja(who, M1.motion_hash) for who in (w.alice, w.bob, w.carol)]
    rg = w.ratify(w.alice, G1.proposal_hash, g_ja)
    rm = w.ratify(w.bob, M1.motion_hash, m_ja)
    store = w.store()
    tg = _decide(store, G1)
    assert tg.state is TallyState.PASSED
    ohne = verify_ratification(store, ratify=rg, epoch=EPOCH_1, proposal=G1, tally=tg,
                               target_constitution_obj=C2S, now=NOW, policy=policy_of(C1))
    assert ohne.next_epoch is None
    assert Finding(kind=GF.MOTION_UNRATIFIED, subject=M1.motion_hash) in ohne.findings
    tm = _decide(store, M1)
    fest = verify_ratification(store, ratify=rm, epoch=EPOCH_1, proposal=M1, tally=tm,
                               target_constitution_obj=None, now=NOW, policy=policy_of(C1))
    assert fest.next_epoch is None and fest.findings == ()
    assert fest.ratified_motion == M1.motion_hash
    mit = verify_ratification(store, ratify=rg, epoch=EPOCH_1, proposal=G1, tally=tg,
                              target_constitution_obj=C2S, now=NOW, policy=policy_of(C1),
                              ratified_motions=frozenset({M1.motion_hash}))
    assert mit.next_epoch == EPOCH_2S


@pytest.mark.parametrize(
    ("vektor", "motions", "felder", "applied"),
    [
        ("GV-87", [M1, M3], {"beitrag": "40 EUR"}, [M3, M1]),
        ("GV-88", [M3], {}, []),
        ("GV-89", [M5, M6, M7], {"x": 2}, [M5, M7]),
    ],
)
def test_gv87_bis_gv89_fassung_in_jeder_reihenfolge(vektor, motions, felder, applied) -> None:
    for order in itertools.permutations(motions):
        fassung, done = apply_motions(C1, list(order))
        assert {k: v for k, v in fassung.items() if k not in C1} == felder, vektor
        assert list(done) == [m.motion_hash for m in applied], vektor
