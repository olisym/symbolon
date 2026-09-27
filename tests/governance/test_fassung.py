"""Fassung und Kette mit Sachanträgen; INV-04.9 bis INV-04.11
(04 §4.1, 04 §4.4, 04 §4.5, 04 §4.6, 04-golden-anchors.md §8, 04-golden-anchors.md §10,
D567 bis D572).

Welt und Objekte aus ``tests/governance/test_sachantraege.py``.
"""

from __future__ import annotations

import itertools

from symbolon.atom import claim_id
from symbolon.governance import resolve_epoch, verify_ratification
from symbolon.governance.chain import resolve_fassung
from symbolon.governance.findings import Finding, GovernanceFinding as GF
from symbolon.governance.objects import Proposal, apply_motions, preconditions
from symbolon.governance.tally import TallyState
from symbolon.policy import constitution_hash

from .fixtures import C1, C2, EPOCH_1, GENESIS_D, N_D, NOW, policy_of
from .test_sachantraege import (
    _FORMWIDRIG,
    C2S,
    EPOCH_2S,
    G1,
    KNOWN,
    M1,
    M2,
    M3,
    M4,
    M5,
    M6,
    M7,
    M_RULE,
    E1,
    _decide,
    _motion,
    _Welt,
)

KONST = {constitution_hash(c): c for c in (C1, C2, C2S)}


def _kette(store, known=KNOWN):
    return resolve_epoch(store, scope=N_D, genesis_obj=GENESIS_D, known_constitutions=KONST,
                         known_proposals=known, now=NOW)


def _fassung(store, known=KNOWN):
    return resolve_fassung(store, epoch=EPOCH_1, genesis_obj=GENESIS_D, constitution_obj=C1,
                           known_proposals=known, now=NOW)


def _g1_und_m1(w: _Welt, *, m1_feststellen: bool):
    g_ja = [w.ja(who, G1.proposal_hash) for who in (w.bob, w.alice, w.dave)]
    m_ja = [w.ja(who, M1.motion_hash) for who in (w.alice, w.bob, w.carol)]
    w.ratify(w.alice, G1.proposal_hash, g_ja)
    if m1_feststellen:
        w.ratify(w.bob, M1.motion_hash, m_ja)
    return m_ja


# --- Kette (04 §4.5) --------------------------------------------------------------

def test_kette_erreicht_epoche_2s_mit_festgestelltem_m1() -> None:
    w = _Welt()
    _g1_und_m1(w, m1_feststellen=True)
    r = _kette(w.store())
    assert r.epoch == EPOCH_2S and r.findings == ()


def test_kette_bleibt_ohne_festgestellten_m1() -> None:
    w = _Welt()
    _g1_und_m1(w, m1_feststellen=False)
    r = _kette(w.store())
    assert r.epoch == EPOCH_1
    assert Finding(kind=GF.MOTION_UNRATIFIED, subject=M1.motion_hash) in r.findings


def test_kette_meldet_keine_vermerke_von_sachantraegen() -> None:
    w = _Welt()
    m_ja = [w.ja(who, M1.motion_hash) for who in (w.alice, w.bob, w.carol)]
    w.ratify(w.bob, M1.motion_hash, m_ja[:2])
    r = _kette(w.store())
    assert r.epoch == EPOCH_1 and r.findings == ()


# --- Fassung (04 §4.6) ------------------------------------------------------------

def test_gv90_zwei_feststellungen_eine_traegt() -> None:
    w = _Welt()
    m_ja = [w.ja(who, M1.motion_hash) for who in (w.alice, w.bob, w.carol)]
    w.ratify(w.bob, M1.motion_hash, m_ja)
    w.ratify(w.carol, M1.motion_hash, m_ja[:2])
    r = _fassung(w.store())
    assert r.applied == (M1.motion_hash,) and r.findings == ()
    assert r.fassung_obj["beitrag"] == "30 EUR"


def test_gv91_nur_die_feststellung_mit_zwei_zeugen() -> None:
    w = _Welt()
    m_ja = [w.ja(who, M1.motion_hash) for who in (w.alice, w.bob, w.carol)]
    rc = w.ratify(w.carol, M1.motion_hash, m_ja[:2])
    r = _fassung(w.store())
    assert r.applied == () and "beitrag" not in r.fassung_obj
    assert r.findings == (Finding(kind=GF.UNSUPPORTED_RATIFICATION, subject=claim_id(rc)),)


def test_gv87_gv89_ueber_feststellungen() -> None:
    for motions, felder in (([M1, M3], {"beitrag": "40 EUR"}), ([M3], {}),
                            ([M5, M6, M7], {"x": 2})):
        w = _Welt()
        for m in motions:
            ja = [w.ja(who, m.motion_hash) for who in (w.alice, w.bob, w.carol)]
            w.ratify(w.alice, m.motion_hash, ja)
        r = _fassung(w.store())
        assert {k: v for k, v in r.fassung_obj.items() if k not in C1} == felder
        assert r.fassung_obj is not C1 and "beitrag" not in C1


def test_fassung_ohne_verfassung_ist_leer() -> None:
    r = resolve_fassung(_Welt().store(), epoch=EPOCH_1, genesis_obj=GENESIS_D,
                        constitution_obj=None, known_proposals=KNOWN, now=NOW)
    assert r.fassung_obj is None and r.applied == () and r.findings == ()


# --- Formwidriger Sachantrag bei der Feststellung (04 §4.1, D570) ---------------------

def test_formwidriger_sachantrag_endet_mit_tally_unevaluable() -> None:
    fremd = dict(_FORMWIDRIG)["GV-77"]
    w = _Welt()
    ja = [w.ja(who, fremd.motion_hash) for who in (w.alice, w.bob, w.carol)]
    rc = w.ratify(w.alice, fremd.motion_hash, ja)
    store = w.store()
    tally = _decide(store, fremd, known={fremd.motion_hash: fremd})
    r = verify_ratification(store, ratify=rc, epoch=EPOCH_1, proposal=fremd, tally=tally,
                            target_constitution_obj=None, now=NOW, policy=policy_of(C1))
    assert r.ratified_motion is None and r.next_epoch is None
    assert Finding(kind=GF.TALLY_UNEVALUABLE, subject=claim_id(rc)) in r.findings
    assert Finding(kind=GF.MALFORMED_MOTION, subject=fremd.motion_hash) in r.findings


def test_formwidriger_sachantrag_der_epoche_in_der_fassung() -> None:
    w = _Welt()
    ja = [w.ja(who, M_RULE.motion_hash) for who in (w.alice, w.bob, w.carol)]
    rc = w.ratify(w.alice, M_RULE.motion_hash, ja)
    r = _fassung(w.store())
    assert r.applied == ()
    assert set(r.findings) == {
        Finding(kind=GF.TALLY_UNEVALUABLE, subject=claim_id(rc)),
        Finding(kind=GF.MALFORMED_MOTION, subject=M_RULE.motion_hash),
    }


# --- INV-04.9 (04 §4.4, B2 und B3) -------------------------------------------------

def _inv_049(objekte, menue, verboten) -> None:
    """Jede Belegung der vier Mitglieder aus ``menue``; kein Paar aus ``verboten`` zugleich
    ``PASSED``. Objekte werden über ihren Namen in ``objekte`` angesprochen."""
    for belegung in itertools.product(menue, repeat=4):
        w = _Welt()
        for who, auswahl in zip((w.alice, w.bob, w.carol, w.dave), belegung):
            for name in auswahl:
                obj = objekte[name]
                w.ja(who, obj.proposal_hash if name.startswith("G") else obj.motion_hash)
        store = w.store()
        passed = {name for name, obj in objekte.items()
                  if _decide(store, obj).state is TallyState.PASSED}
        for a, b in verboten:
            assert not {a, b} <= passed, belegung


def test_INV_04_9_vorschlag_und_sachantrag_ausserhalb_s() -> None:
    _inv_049({"G1": G1, "M4": M4}, ((), ("G1",), ("M4",), ("G1", "M4")), (("G1", "M4"),))


def test_INV_04_9_gemeinsame_vorbedingung() -> None:
    _inv_049({"M1": M1, "M2": M2}, ((), ("M1",), ("M2",), ("M1", "M2")), (("M1", "M2"),))


# --- INV-04.10 und INV-04.11 (04 §4.6, B4) ------------------------------------------

_ALLE = (M1, M2, M3, M4, M5, M6, M7)


def _vertraeglich(menge) -> bool:
    return all(not (preconditions(a) & preconditions(b)) for a, b in itertools.combinations(menge, 2))


def _mengen():
    for k in range(len(_ALLE) + 1):
        for menge in itertools.combinations(_ALLE, k):
            if _vertraeglich(menge):
                yield menge


def test_INV_04_10_fassung_unabhaengig_von_der_reihenfolge() -> None:
    for menge in _mengen():
        ergebnisse = {
            (repr(sorted(apply_motions(C1, list(p))[0].items())), apply_motions(C1, list(p))[1])
            for p in itertools.permutations(menge)
        }
        assert len(ergebnisse) == 1, [m.obj[2] for m in menge]


def test_INV_04_11_fassung_waechst() -> None:
    for menge in _mengen():
        vorher = set(apply_motions(C1, list(menge))[1])
        for m in _ALLE:
            if m in menge or not _vertraeglich((*menge, m)):
                continue
            nachher = set(apply_motions(C1, [*menge, m])[1])
            assert vorher <= nachher, ([x.obj[2] for x in menge], m.obj[2])


def test_mengen_decken_die_faelle() -> None:
    """Golden Number: 7 Sachanträge, M1 und M2 unverträglich, M5 und M7 verträglich."""
    assert sum(1 for _ in _mengen()) == 96


# --- Fremder scope (04 §4.5, D572) --------------------------------------------------

def test_objekt_mit_fremdem_scope_wird_uebergangen() -> None:
    fremd_m = _motion({"beitrag": [[], ["30 EUR"]]}, scope=bytes(32))
    fremd_g = Proposal(bytes(32), E1, constitution_hash(C2S))
    w = _Welt()
    for h in (fremd_m.motion_hash, fremd_g.proposal_hash):
        ja = [w.ja(who, h) for who in (w.alice, w.bob, w.carol)]
        w.ratify(w.alice, h, ja)
    known = {**KNOWN, fremd_m.motion_hash: fremd_m, fremd_g.proposal_hash: fremd_g}
    store = w.store()
    kette = _kette(store, known)
    assert kette.epoch == EPOCH_1 and kette.findings == ()
    fassung = _fassung(store, known)
    assert fassung.applied == () and fassung.findings == ()
