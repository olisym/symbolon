"""Eine Stimme ersetzt frühere Stimmen derselben Wurzel, die sie nennt (04 §2.2, 04 §3.1, D547, D548).

Welt aus ``tests/governance/test_geraete.py``. ``GV-55`` bis ``GV-58`` aus ``04-golden-anchors.md``.
"""

from __future__ import annotations

import random

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id
from symbolon.governance import verify_ratification
from symbolon.governance.findings import GovernanceFinding
from symbolon.governance.tally import TallyResult
from tests.helpers import Identity, store_with

from .fixtures import C3, NOW, policy_of, ratify_claim
from .test_geraete import CV, EV, PV, _kinds, _Welt


def _stimme(w: _Welt, who: Identity, choice: int, names: object = None) -> Claim:
    """Eine Stimme auf ``w.proposal``; ``names`` wird wörtlich als ``v`` Key 1 gesetzt."""
    v: dict[int, object] = {0: choice}
    if names is not None:
        v[1] = names
    (c,) = w.add(
        who.claim(
            p=f"nuc:{w.proposal.scope.hex()}/vote@1",
            J=(3, w.proposal.proposal_hash),
            t=w._next_t(),
            N=w.proposal.scope,
            v=cbor_canon.encode(v),
        )
    )
    return c


def _ids(*claims: Claim) -> list[bytes]:
    return [claim_id(c) for c in claims]


def _zaehlt(tally: TallyResult) -> tuple[set[bytes], set[bytes]]:
    return set(tally.yes), set(tally.no)


def test_gv55_wechsel() -> None:
    """Ja, danach Nein mit Nennung des Ja: das Nein zählt, nichts ist mehrdeutig (GV-55)."""
    w = _Welt()
    ja = _stimme(w, w.bob, 1)
    nein = _stimme(w, w.bob, 0, _ids(ja))
    tally = w.tally()
    assert _zaehlt(tally) == (set(), {claim_id(nein)})
    assert _kinds(tally, GovernanceFinding.AMBIGUOUS_VOTE) == set()


def test_gv56_aufloesung_und_feststellung() -> None:
    """Ja und Nein zweier Geräte, danach ein Ja der Wurzel, das beide nennt (GV-56)."""
    w = _Welt()
    zweit, _ack = w.device(w.alice, "ALICE_ZWEIT")
    ja = _stimme(w, w.alice, 1)
    nein = _stimme(w, zweit, 0)
    assert _kinds(w.tally(), GovernanceFinding.AMBIGUOUS_VOTE) == set(_ids(ja, nein))
    neu = _stimme(w, w.alice, 1, _ids(ja, nein))
    andere = [w.vote(who, 1) for who in (w.bob, w.carol, w.dave)]
    tally = w.tally()
    assert claim_id(neu) in tally.yes and claim_id(ja) not in tally.yes
    assert _kinds(tally, GovernanceFinding.AMBIGUOUS_VOTE) == set()
    alt = ratify_claim(w.alice, PV, witnesses=_ids(ja, *andere), t=100)
    gut = ratify_claim(w.alice, PV, witnesses=_ids(neu, *andere), t=101)
    w.add(alt, gut)
    store = store_with(*w.claims)
    tally = w.tally()

    def ergebnis(r: Claim):
        return verify_ratification(
            store,
            ratify=r,
            epoch=EV,
            proposal=PV,
            tally=tally,
            target_constitution_obj=C3,
            now=NOW,
            policy=policy_of(CV),
        )

    assert ergebnis(gut).next_epoch is not None
    schlecht = ergebnis(alt)
    assert schlecht.next_epoch is None
    assert GovernanceFinding.UNSUPPORTED_RATIFICATION in {f.kind for f in schlecht.findings}


def test_gv57_fremder_name() -> None:
    """Ein Name auf die Stimme eines anderen Autors bleibt ohne Wirkung und Vermerk (GV-57)."""
    w = _Welt()
    fremd = _stimme(w, w.carol, 1)
    eigen = _stimme(w, w.bob, 0, _ids(fremd))
    tally = w.tally()
    assert _zaehlt(tally) == ({claim_id(fremd)}, {claim_id(eigen)})
    assert not tally.findings


def test_gv58_formwidrig() -> None:
    """Ein Eintrag mit 31 Byte: MALFORMED_REPLACES, die Stimme zählt, als fehlte Key 1 (GV-58)."""
    w = _Welt()
    ja = _stimme(w, w.bob, 1)
    nein = _stimme(w, w.bob, 0, [claim_id(ja)[:31]])
    tally = w.tally()
    assert _kinds(tally, GovernanceFinding.MALFORMED_REPLACES) == {claim_id(nein)}
    assert _kinds(tally, GovernanceFinding.AMBIGUOUS_VOTE) == set(_ids(ja, nein))
    assert _zaehlt(tally) == (set(), set())


def test_formwidrig_keine_liste() -> None:
    """Key 1 ist ein Bytestring statt einer Liste: MALFORMED_REPLACES, zählt wie ohne (04 §3.1)."""
    w = _Welt()
    ja = _stimme(w, w.bob, 1, claim_id(w.vote(w.carol, 1)))
    tally = w.tally()
    assert _kinds(tally, GovernanceFinding.MALFORMED_REPLACES) == {claim_id(ja)}
    assert claim_id(ja) in tally.yes


def test_nachzuegler() -> None:
    """Die genannte Stimme trifft später ein: sie ist dann schon ersetzt (D547 Beschluss 2)."""
    w = _Welt()
    zweit, _ack = w.device(w.bob, "BOB_ZWEIT")
    frueh = zweit.claim(
        p=f"nuc:{w.proposal.scope.hex()}/vote@1",
        J=(3, w.proposal.proposal_hash),
        t=w._next_t(),
        N=w.proposal.scope,
        v=cbor_canon.encode({0: 1}),
    )
    neu = _stimme(w, w.bob, 0, _ids(frueh))
    assert _zaehlt(w.tally()) == (set(), {claim_id(neu)})
    w.add(frueh)
    tally = w.tally()
    assert _zaehlt(tally) == (set(), {claim_id(neu)})
    assert _kinds(tally, GovernanceFinding.AMBIGUOUS_VOTE) == set()


def test_zwei_aufloesungen_verschieden() -> None:
    """Zwei ersetzende Stimmen zweier Geräte, verschieden, einander nicht nennend (04 §3.1)."""
    w = _Welt()
    zweit, _ack = w.device(w.bob, "BOB_ZWEIT")
    ja = _stimme(w, w.bob, 1)
    nein = _stimme(w, zweit, 0)
    a = _stimme(w, w.bob, 1, _ids(ja, nein))
    b = _stimme(w, zweit, 0, _ids(ja, nein))
    tally = w.tally()
    assert _kinds(tally, GovernanceFinding.AMBIGUOUS_VOTE) == set(_ids(a, b))
    assert _zaehlt(tally) == (set(), set())


def _beitrag(tally: TallyResult) -> str:
    return ("ja" if tally.yes else "") + ("nein" if tally.no else "") or "-"


def test_nie_weniger_als_ohne_nennung() -> None:
    """Zählt die Wurzel ohne Nennung eine Wahl, zählt sie mit Nennung dieselbe (D547 Befund 1).

    400 Folgen von bis zu fünf Stimmen über die Wurzel und zwei Geräte, fester Seed.
    """
    rng = random.Random(547)
    geprueft = 0
    for _ in range(400):
        plan = []
        for i in range(rng.randint(1, 5)):
            plan.append((rng.randrange(3), rng.randrange(2), [j for j in range(i) if rng.random() < 0.4]))

        def lauf(mit_namen: bool) -> list[str]:
            w = _Welt()
            b2, _a2 = w.device(w.bob, "BOB_2")
            b3, _a3 = w.device(w.bob, "BOB_3")
            schluessel = [w.bob, b2, b3]
            gemacht: list[Claim] = []
            stand = []
            for wer, wahl, namen in plan:
                genannt = _ids(*(gemacht[j] for j in namen)) if mit_namen and namen else None
                gemacht.append(_stimme(w, schluessel[wer], wahl, genannt))
                stand.append(_beitrag(w.tally()))
            return stand

        for ohne, mit in zip(lauf(False), lauf(True), strict=True):
            geprueft += 1
            if ohne != "-":
                assert mit == ohne, (plan, ohne, mit)
    assert geprueft > 1000
