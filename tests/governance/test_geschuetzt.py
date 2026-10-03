"""Geschützte Sachfelder: Liste, Klasse eines Sachantrags, Formwidrigkeit
(04 §1.1, 04 §3.4, 04 §3.5, 04 §4.1, D646).

Vektoren ``GV-104`` bis ``GV-121`` aus ``04-golden-anchors.md §12``.
"""

from __future__ import annotations

import pytest

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id
from symbolon.genesis import genesis_scope
from symbolon.governance import decide, verify_ratification
from symbolon.governance.findings import Finding, GovernanceFinding as GF
from symbolon.governance.objects import Epoch, Motion, Proposal, protected_fields
from symbolon.governance.tally import TallyState, reached
from symbolon.policy import constitution_hash
from tests.helpers import store_with

from .fixtures import C1, GENESIS_D, NOW, P2, fresh_p1, nuc, policy_of

CP = {**C1, "name": "Gartenverein", "protected_fields": ["name", "zweck"]}


class _Welt:
    """Epoche 1 eines eigenen Genesis, dessen Verfassung ``verfassung`` ist."""

    def __init__(self, verfassung: dict = CP, *, regel: int = 2) -> None:
        self.verfassung = verfassung
        self.genesis = {**GENESIS_D, 4: constitution_hash(verfassung), 5: regel}
        self.scope = genesis_scope(self.genesis)
        self.epoch = Epoch(scope=self.scope, index=1, constitution_hash=constitution_hash(verfassung))
        self.alice, self.bob, self.carol, self.dave = fresh_p1()
        self.claims: list[Claim] = []
        self._t = 0

    def t(self) -> int:
        self._t += 1
        return self._t

    def motion(self, changes: dict) -> Motion:
        return Motion({0: self.scope, 1: self.epoch.epoch_id, 2: changes})

    def ja(self, who, obj_hash: bytes) -> Claim:
        c = who.claim(p=nuc(self.scope, "vote"), J=(3, obj_hash), t=self.t(), N=self.scope,
                      v=cbor_canon.encode({0: 1}))
        self.claims.append(c)
        return c

    def ratify(self, who, obj_hash: bytes, witnesses: list[Claim]) -> Claim:
        c = who.claim(p=nuc(self.scope, "ratify"), J=(3, obj_hash), t=self.t(), N=self.scope,
                      v=cbor_canon.encode({0: [claim_id(w) for w in witnesses]}))
        self.claims.append(c)
        return c

    def decide(self, obj, *, target=None, known=None):
        return decide(store_with(*self.claims), epoch=self.epoch, proposal=obj,
                      genesis_obj=self.genesis, constitution_obj=self.verfassung,
                      target_constitution_obj=target, known_proposals=known or {}, now=NOW,
                      policy=policy_of(self.verfassung))

    def drei(self, obj_hash: bytes) -> list[Claim]:
        return [self.ja(who, obj_hash) for who in (self.alice, self.bob, self.carol)]


def test_schwellen_liegen_auf_verschiedenen_seiten() -> None:
    """Drei Ja von vier erreichen ``[1,2]`` und ``[2,3]``, nicht ``[3,4]`` (D539)."""
    th = CP["thresholds"]
    assert reached(3, 4, *th["ordinary"]) and reached(3, 4, *th["membership"])
    assert not reached(3, 4, *th["amendment"]) and reached(4, 4, *th["amendment"])


# --- 12.1 Die Klasse eines Sachantrags ------------------------------------------

@pytest.mark.parametrize(
    ("vektor", "changes"),
    [
        ("GV-104", {"name": [["Gartenverein"], ["Laufgruppe"]]}),
        ("GV-106", {"name": [["Gartenverein"], []]}),
        ("GV-107", {"zweck": [[], ["Gemeinsam laufen"]]}),
        ("GV-108", {"beitrag": [[], ["30 EUR"]], "name": [["Gartenverein"], ["Laufgruppe"]]}),
    ],
)
def test_gv104_bis_gv108_geschuetztes_feld(vektor, changes) -> None:
    w = _Welt()
    m = w.motion(changes)
    w.drei(m.motion_hash)
    r = w.decide(m)
    assert r.state is TallyState.PENDING and r.threshold == (3, 4), vektor
    assert r.findings == (), vektor
    if vektor == "GV-104":
        w.ja(w.dave, m.motion_hash)
        r = w.decide(m)
        assert r.state is TallyState.PASSED and r.findings == (), "GV-105"


def test_gv109_ungeschuetztes_feld_neben_der_liste() -> None:
    w = _Welt()
    m = w.motion({"beitrag": [[], ["30 EUR"]]})
    w.drei(m.motion_hash)
    r = w.decide(m)
    assert r.state is TallyState.PASSED and r.threshold == (1, 2) and r.findings == ()


def test_gv110_ohne_liste_ist_nichts_geschuetzt() -> None:
    ohne = {k: v for k, v in CP.items() if k != "protected_fields"}
    assert protected_fields(ohne) == frozenset()
    w = _Welt(ohne)
    m = w.motion({"name": [["Gartenverein"], ["Laufgruppe"]]})
    w.drei(m.motion_hash)
    r = w.decide(m)
    assert r.state is TallyState.PASSED and r.threshold == (1, 2) and r.findings == ()


def test_gv111_klasse_aus_dem_genesis() -> None:
    w = _Welt(regel=1)
    m = w.motion({"name": [["Gartenverein"], ["Laufgruppe"]]})
    w.drei(m.motion_hash)
    r = w.decide(m)
    assert r.state is TallyState.PASSED and r.threshold == (2, 3) and r.findings == ()


def test_gv112_gv113_feststellung() -> None:
    w = _Welt()
    m = w.motion({"name": [["Gartenverein"], ["Laufgruppe"]]})
    drei = w.drei(m.motion_hash)
    zu_frueh = w.ratify(w.alice, m.motion_hash, drei)
    t = w.decide(m)
    r = verify_ratification(store_with(*w.claims), ratify=zu_frueh, epoch=w.epoch, proposal=m,
                            tally=t, target_constitution_obj=None, now=NOW,
                            policy=policy_of(w.verfassung))
    assert r.ratified_motion is None
    assert Finding(kind=GF.UNSUPPORTED_RATIFICATION, subject=claim_id(zu_frueh)) in r.findings
    vier = [*drei, w.ja(w.dave, m.motion_hash)]
    fest = w.ratify(w.bob, m.motion_hash, vier)
    t = w.decide(m)
    r = verify_ratification(store_with(*w.claims), ratify=fest, epoch=w.epoch, proposal=m,
                            tally=t, target_constitution_obj=None, now=NOW,
                            policy=policy_of(w.verfassung))
    assert r.ratified_motion == m.motion_hash and r.findings == ()


# --- 12.2 Formwidrigkeit -------------------------------------------------------

@pytest.mark.parametrize(
    ("vektor", "liste"),
    [
        ("GV-114", []),
        ("GV-115", ["zweck", "name"]),
        ("GV-116", ["name", "name"]),
        ("GV-117", ["name", 7]),
        ("GV-118", ["participants"]),
        ("GV-119", "name"),
    ],
)
def test_gv114_bis_gv119_formwidrige_liste(vektor, liste) -> None:
    kaputt = {**CP, "protected_fields": liste}
    assert protected_fields(kaputt) is None, vektor
    w = _Welt(kaputt)
    # Ein Feld, das in keiner Lesart der Liste geschützt wäre.
    m = w.motion({"beitrag": [[], ["30 EUR"]]})
    w.drei(m.motion_hash)
    r = w.decide(m)
    assert r.state is TallyState.UNEVALUABLE, vektor
    assert r.findings == (
        Finding(kind=GF.MALFORMED_PROTECTED_FIELDS, subject=constitution_hash(kaputt)),
    ), vektor


def test_gv120_vorschlag_bleibt_auszaehlbar() -> None:
    """Der Weg der Reparatur: ein Vorschlag liest die Liste nicht."""
    kaputt = {**CP, "protected_fields": []}
    w = _Welt(kaputt)
    ziel = {k: v for k, v in kaputt.items() if k != "protected_fields"}
    g = Proposal(w.scope, w.epoch.epoch_id, constitution_hash(ziel))
    w.drei(g.proposal_hash)
    r = w.decide(g, target=ziel, known={g.proposal_hash: g})
    assert r.state is TallyState.PENDING and r.threshold == (3, 4) and r.findings == ()
    aufnahme = {**kaputt, "participants": P2}
    g2 = Proposal(w.scope, w.epoch.epoch_id, constitution_hash(aufnahme))
    r = w.decide(g2, target=aufnahme, known={g2.proposal_hash: g2})
    assert r.state is not TallyState.UNEVALUABLE and r.threshold == (2, 3)


def test_gv121_die_liste_ist_ein_regelfeld() -> None:
    w = _Welt()
    m = w.motion({"protected_fields": [[["name", "zweck"]], [["name"]]]})
    r = w.decide(m)
    assert r.state is TallyState.UNEVALUABLE
    assert r.findings == (Finding(kind=GF.MALFORMED_MOTION, subject=m.motion_hash),)


def test_regierbarkeit_steht_vor_der_liste() -> None:
    """Die Reihenfolge aus 04 §3.5: erst die vier Lagen der Regierbarkeit, dann die Liste."""
    kaputt = {**CP, "protected_fields": [], "irrevocable_predicates": ["ratify@1"]}
    w = _Welt(kaputt)
    m = w.motion({"beitrag": [[], ["30 EUR"]]})
    r = decide(store_with(), epoch=w.epoch, proposal=m, genesis_obj=w.genesis,
               constitution_obj=kaputt, target_constitution_obj=None, known_proposals={},
               now=NOW, policy=None)
    assert [f.kind for f in r.findings] == [GF.VOTE_REVOCABLE]


def test_sortiert_nach_bytes() -> None:
    assert protected_fields({"protected_fields": ["Zweck", "name"]}) == frozenset({"Zweck", "name"})
    assert protected_fields({"protected_fields": ["name", "Zweck"]}) is None
    assert protected_fields({"protected_fields": ["z", "ä"]}) == frozenset({"z", "ä"})


@pytest.mark.parametrize(
    "liste",
    [[["name"]], [{"name": 1}], [b"name"], [None], {"name": 1}, 7, None, b"name", [1.5], ["name", []]],
)
def test_fremder_inhalt_wirft_nicht(liste) -> None:
    """Die Verfassung ist fremder Inhalt: jede Form ohne Ausnahme (D474)."""
    assert protected_fields({"protected_fields": liste}) is None
