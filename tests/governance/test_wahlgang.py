"""Wahlgänge und Patt: GV-92 bis GV-101, INV-04.12 und INV-04.13 (04 §4.7, D600)."""

from __future__ import annotations

import random

import pytest

from symbolon.governance.chain import resolve_epoch
from symbolon.governance.findings import Finding, GovernanceFinding as GF
from symbolon.governance.objects import ABSENT, Epoch, Proposal, ballot_of
from symbolon.governance.tally import (
    TallyState,
    approvals_conflict,
    current_ballot,
    decide,
    stalemate,
)
from symbolon.policy import constitution_hash
from tests.governance.fixtures import (
    C1,
    C1_AMEND,
    C2,
    CONSTITUTION_HASH_2,
    EPOCH_1,
    GENESIS_D,
    N_D,
    NOW,
    P1,
    PROPOSAL_1,
    PROPOSAL_AMEND_E1,
    _constitution,
    fresh_p1,
    policy_of,
    ratify_claim,
    vote,
)
from tests.helpers import store_with

GA = PROPOSAL_1
GB = PROPOSAL_AMEND_E1
GC = Proposal(scope=N_D, predecessor=EPOCH_1.epoch_id, constitution_hash=CONSTITUTION_HASH_2, ballot=1)
GD = Proposal(scope=N_D, predecessor=EPOCH_1.epoch_id, constitution_hash=CONSTITUTION_HASH_2, ballot=2)
KNOWN = {p.proposal_hash: p for p in (GA, GB, GC, GD)}
CONSTITUTIONS = {constitution_hash(c): c for c in (C1, C2, C1_AMEND)}
DAVE_PUB = fresh_p1()[3].pub
_ZIEL_GB2 = _constitution(participants=P1, arbitrators=[DAVE_PUB])
EPOCH_2_HASH = Epoch(scope=N_D, index=2, constitution_hash=CONSTITUTION_HASH_2).epoch_id


def _welt(plan, *extra):
    """Stimmen nach ``plan`` von frischen Identitäten, dazu ``extra`` von denselben."""
    alice, bob, carol, dave = fresh_p1()
    ids = {"ALICE": alice, "BOB": bob, "CAROL": carol, "DAVE": dave}
    t = iter(range(100, 10_000))
    claims = [vote(ids[wer], ziel, choice=1, t=next(t)) for wer, ziel in plan]
    claims += [f(ids, next(t)) for f in extra]
    return store_with(*claims), claims


def _kw(known=None, constitution=C1, epoch=EPOCH_1):
    return {
        "epoch": epoch,
        "genesis_obj": GENESIS_D,
        "constitution_obj": constitution,
        "known_proposals": KNOWN if known is None else known,
        "known_constitutions": CONSTITUTIONS,
        "now": NOW,
        "policy": policy_of(constitution),
    }


def _tally(store, proposal, known=None):
    kw = _kw(known)
    return decide(
        store,
        proposal=proposal,
        target_constitution_obj=CONSTITUTIONS.get(proposal.constitution_hash),
        **kw,
    )


def _patt(store, ballot, known=None):
    return stalemate(store, ballot=ballot, **_kw(known))


def _geltend(store, known=None):
    return current_ballot(store, **_kw(known))


_SPALTUNG = [
    ("ALICE", GA),
    ("CAROL", GB),
    ("BOB", GA),
    ("BOB", GB),
    ("DAVE", GA),
    ("DAVE", GB),
]


def test_feld_4_hash() -> None:
    """Ohne Feld 4 bleibt der Hash, mit Feld 4 = 1 der Anker aus 04-golden-anchors §11."""
    assert GA.ballot is ABSENT
    assert GA.proposal_hash.hex() == (
        "38edfd6b0ba90ade0b96746c21ead9e631c1dac883150a15ed923dd1aaf6db6b"
    )
    assert GC.proposal_hash.hex() == (
        "f3c43bdbbbb33f65babaac05fb79689b79f2f91ac6004a6af235dcfb22b9058f"
    )


@pytest.mark.parametrize(
    ("wert", "erwartet"),
    [(ABSENT, 0), (1, 1), (7, 7), (0, None), (-1, None), ("1", None), (True, None), (1.0, None)],
)
def test_ballot_of(wert, erwartet) -> None:
    """Feld 4 ist ein int größer 0; bool ist keiner (04 §2.4, D600 Beschluss 1)."""
    proposal = Proposal(
        scope=N_D, predecessor=EPOCH_1.epoch_id, constitution_hash=CONSTITUTION_HASH_2, ballot=wert
    )
    assert ballot_of(proposal) == erwartet


def test_regel_1_je_wahlgang() -> None:
    """Zwei Vorschläge sind nur im selben Wahlgang unvereinbar; formwidriges Feld 4 nie (04 §4.4)."""
    formwidrig = Proposal(
        scope=N_D, predecessor=EPOCH_1.epoch_id, constitution_hash=CONSTITUTION_HASH_2, ballot=0
    )
    assert approvals_conflict(GA, GB) is True
    assert approvals_conflict(GA, GC) is False
    assert approvals_conflict(GC, GD) is False
    formwidrig_2 = Proposal(
        scope=N_D, predecessor=EPOCH_1.epoch_id, constitution_hash=CONSTITUTION_HASH_2, ballot="1"
    )
    assert approvals_conflict(GA, formwidrig) is False
    assert approvals_conflict(formwidrig, GB) is False
    assert approvals_conflict(formwidrig, formwidrig_2) is False


def test_GV_92() -> None:
    """Die Spaltung: Wahlgang 0 im Patt, geltend 1; GA und GB PENDING mit CONFLICTING_APPROVAL."""
    store, _ = _welt(_SPALTUNG)
    assert _patt(store, 0) is True
    assert _geltend(store) == 1
    for proposal in (GA, GB):
        r = _tally(store, proposal)
        assert r.state is TallyState.PENDING
        assert GF.CONFLICTING_APPROVAL in {f.kind for f in r.findings}


def test_GV_93() -> None:
    """Drei Ja auf GC im Wahlgang 1: PASSED, geltend 1, an GC kein CONFLICTING_APPROVAL."""
    store, _ = _welt(_SPALTUNG + [("ALICE", GC), ("BOB", GC), ("CAROL", GC)])
    r = _tally(store, GC)
    assert r.state is TallyState.PASSED
    assert r.current_ballot == 1
    assert GF.CONFLICTING_APPROVAL not in {f.kind for f in r.findings}


def _mit_feststellung(plan, ziel, n_zeugen):
    """Die Stimmen aus ``plan`` und ein ratify@1 von ALICE auf ``ziel`` mit den letzten Ja."""
    from symbolon.atom import claim_id

    alice, bob, carol, dave = fresh_p1()
    ids = {"ALICE": alice, "BOB": bob, "CAROL": carol, "DAVE": dave}
    t = iter(range(100, 10_000))
    claims = [vote(ids[wer], z, choice=1, t=next(t)) for wer, z in plan]
    zeugen = [claim_id(c) for c in claims[-n_zeugen:]]
    claims.append(ratify_claim(ids["ALICE"], ziel, witnesses=zeugen, t=next(t)))
    store = store_with(*claims)
    return resolve_epoch(
        store,
        scope=N_D,
        genesis_obj=GENESIS_D,
        known_constitutions=CONSTITUTIONS,
        known_proposals=KNOWN,
        now=NOW,
    )


def test_GV_93_feststellung() -> None:
    """Das ratify@1 auf GC mit den drei Ja trägt und liefert epoch_id_2 (04 §4.1, 04 §4.2)."""
    plan = _SPALTUNG + [("ALICE", GC), ("BOB", GC), ("CAROL", GC)]
    res = _mit_feststellung(plan, GC, 3)
    assert res.epoch.index == 2
    assert res.epoch.epoch_id == EPOCH_2_HASH


def test_GV_94_und_GV_95() -> None:
    """Das Paar um eine freie Wurzel: CAROL frei, kein Patt; CAROL an GB, Patt."""
    plan = [("ALICE", GA), ("BOB", GA), ("DAVE", GA), ("DAVE", GB)]
    store, _ = _welt(plan)
    assert _patt(store, 0) is False
    assert _geltend(store) == 0
    store, _ = _welt(plan + [("CAROL", GB)])
    assert _patt(store, 0) is True
    assert _geltend(store) == 1


def test_GV_96() -> None:
    """Ohne Stimme kein Patt, geltend 0."""
    store, _ = _welt([])
    assert _patt(store, 0) is False
    assert _geltend(store) == 0


def test_GV_97() -> None:
    """GD im Wahlgang 2 bei geltendem 1: PENDING mit BALLOT_NOT_CURRENT; sein ratify@1 trägt nicht."""
    plan = _SPALTUNG + [("ALICE", GD), ("BOB", GD), ("CAROL", GD)]
    store, _ = _welt(plan)
    assert _geltend(store) == 1
    r = _tally(store, GD)
    assert r.state is TallyState.PENDING
    assert Finding(kind=GF.BALLOT_NOT_CURRENT, subject=GD.proposal_hash) in r.findings
    res = _mit_feststellung(plan, GD, 3)
    assert res.epoch.index == 1
    assert Finding(kind=GF.BALLOT_NOT_CURRENT, subject=GD.proposal_hash) in res.findings


def test_GV_98() -> None:
    """Ein Ja auf ein unbekanntes Objekt verhindert das Patt (Bedingung 2)."""
    unbekannt = Proposal(
        scope=N_D, predecessor=EPOCH_1.epoch_id, constitution_hash=bytes(32), ballot=5
    )
    store, _ = _welt(_SPALTUNG + [("ALICE", unbekannt)])
    assert _patt(store, 0) is False
    assert _geltend(store) == 0


@pytest.mark.parametrize("feld_4", [0, "1"])
def test_GV_99_und_GV_100(feld_4) -> None:
    """Formwidriges Feld 4: UNEVALUABLE, MALFORMED_PROPOSAL mit dem proposal_hash."""
    formwidrig = Proposal(
        scope=N_D, predecessor=EPOCH_1.epoch_id, constitution_hash=CONSTITUTION_HASH_2, ballot=feld_4
    )
    known = {**KNOWN, formwidrig.proposal_hash: formwidrig}
    store, _ = _welt([("ALICE", formwidrig), ("BOB", formwidrig), ("CAROL", formwidrig)])
    r = _tally(store, formwidrig, known)
    assert r.state is TallyState.UNEVALUABLE
    assert Finding(kind=GF.MALFORMED_PROPOSAL, subject=formwidrig.proposal_hash) in r.findings


GB2 = Proposal(
    scope=N_D,
    predecessor=EPOCH_1.epoch_id,
    constitution_hash=constitution_hash(_constitution(participants=P1, arbitrators=[DAVE_PUB])),
)


def test_GV_102() -> None:
    """Bedingung 3: DAVE an GB und GB2, beide [3,4]; drei freie Wurzeln könnten einen neuen
    Vorschlag der Klasse membership tragen, also kein Patt, geltend 0."""
    known = {GB.proposal_hash: GB, GB2.proposal_hash: GB2}
    store, _ = _welt([("DAVE", GB), ("DAVE", GB2)])
    kw = {**_kw(known), "known_constitutions": {**CONSTITUTIONS, GB2.constitution_hash: _ZIEL_GB2}}
    assert stalemate(store, ballot=0, **kw) is False
    assert current_ballot(store, **kw) == 0


def test_GV_103() -> None:
    """Die angewandte Schwelle zählt: mit [3,4] für GB Patt, das ratify@1 auf GC trägt; wer nur
    die kleinste Schwelle kennt, sieht kein Patt (04 §4.7, Bedingung 4)."""
    plan = [("ALICE", GB), ("BOB", GB), ("DAVE", GB), ("CAROL", GA)]
    store, _ = _welt(plan)
    assert _patt(store, 0) is True
    kw = {**_kw(), "known_constitutions": {constitution_hash(C1): C1}}
    assert stalemate(store, ballot=0, **kw) is False
    res = _mit_feststellung(plan + [("ALICE", GC), ("BOB", GC), ("CAROL", GC)], GC, 3)
    assert res.epoch.epoch_id == EPOCH_2_HASH


def test_GV_101() -> None:
    """[1,1] in jeder Klasse, keine Stimme: kein Patt (Bedingung 1), geltend 0; endet."""
    einstimmig = _constitution(
        participants=P1,
        thresholds={"ordinary": [1, 1], "membership": [1, 1], "amendment": [1, 1]},
    )
    epoch = Epoch(scope=N_D, index=1, constitution_hash=constitution_hash(einstimmig))
    store, _ = _welt([])
    kw = _kw(constitution=einstimmig, epoch=epoch)
    assert stalemate(store, ballot=0, **kw) is False
    assert current_ballot(store, **kw) == 0


# --- INV-04.12 und INV-04.13 über zufällige Welten (04-golden-anchors §8, D600 Beschluss 6).

_HALB = _constitution(
    participants=P1, thresholds={"ordinary": [1, 2], "membership": [1, 2], "amendment": [1, 2]}
)
_EPOCH_HALB = Epoch(scope=N_D, index=1, constitution_hash=constitution_hash(_HALB))
_WELTEN = 300


def _zufallswelt(seed: int):
    rng = random.Random(seed)
    ziele = {}
    vorschlaege = []
    for i in range(rng.randint(2, 5)):
        ziel = _constitution(participants=P1, arbitrators=[bytes([i + 10]) * 32])
        ziele[constitution_hash(ziel)] = ziel
        wahlgang = rng.choice([0, 0, 1, 1, 2])
        vorschlaege.append(
            Proposal(
                scope=N_D,
                predecessor=_EPOCH_HALB.epoch_id,
                constitution_hash=constitution_hash(ziel),
                ballot=ABSENT if wahlgang == 0 else wahlgang,
            )
        )
    known = {p.proposal_hash: p for p in vorschlaege}
    kw = {
        "epoch": _EPOCH_HALB,
        "genesis_obj": GENESIS_D,
        "constitution_obj": _HALB,
        "known_proposals": known,
        "known_constitutions": {**ziele, constitution_hash(_HALB): _HALB},
        "now": NOW,
        "policy": policy_of(_HALB),
    }
    ids = dict(zip("abcd", fresh_p1()))
    t = iter(range(100, 10_000))
    ketten = {w: [] for w in ids}
    for _ in range(rng.randint(4, 14)):
        wer = rng.choice("abcd")
        ketten[wer].append(vote(ids[wer], rng.choice(vorschlaege), choice=1, t=next(t)))
    return rng, vorschlaege, ziele, kw, ketten


def _durch(store, vorschlaege, ziele, kw):
    return [
        p
        for p in vorschlaege
        if decide(
            store, proposal=p, target_constitution_obj=ziele[p.constitution_hash], **kw
        ).state
        is TallyState.PASSED
    ]


def test_INV_04_12_und_04_13() -> None:
    """Höchstens ein Beschluss, im geltenden Wahlgang, keiner im Patt; Patt monoton im Wissen."""
    beschluss = spaeter = patt = 0
    for seed in range(_WELTEN):
        rng, vorschlaege, ziele, kw, ketten = _zufallswelt(seed)
        ganz = store_with(*[c for k in ketten.values() for c in k])
        durch = _durch(ganz, vorschlaege, ziele, kw)
        assert len(durch) <= 1, seed
        geltend = current_ballot(ganz, **kw)
        for p in durch:
            assert ballot_of(p) == geltend, seed
            assert not stalemate(ganz, ballot=ballot_of(p), **kw), seed
        beschluss += bool(durch)
        spaeter += any(ballot_of(p) > 0 for p in durch)
        im_patt = {b for b in range(3) if stalemate(ganz, ballot=b, **kw)}
        patt += bool(im_patt)
        for _ in range(3):
            teil = store_with(
                *[c for k in ketten.values() for c in k[: rng.randint(0, len(k))]]
            )
            for b in range(3):
                if stalemate(teil, ballot=b, **kw):
                    assert b in im_patt, (seed, b)
    # Die Abdeckung als Golden Number: fällt eine Gruppe weg, wird der Test rot (D555).
    assert (beschluss, spaeter, patt) == (21, 2, 221)
