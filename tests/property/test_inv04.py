"""INV-04.7 und INV-04.8 (04-golden-anchors.md §8, D433).

Equivocation ist ausgeschlossen: jede Identität führt eine Kette, keine zwei
Claims eines Autors auf dieselbe Spitze. Die beiden anderen Ausgänge werden
erzeugt: eine zweite gültige Stimme auf denselben Vorschlag (``AMBIGUOUS_VOTE``,
04 §3.1) und ein Ja auf einen anderen Vorschlag derselben Epoche
(``CONFLICTING_APPROVAL``, 04 §4.4).
"""

from __future__ import annotations

from hypothesis import given, strategies as st

from symbolon.atom import Claim, claim_id
from symbolon.governance import verify_ratification
from tests.governance.fixtures import (
    C1,
    C2,
    C3,
    EPOCH_1,
    EPOCH_2,
    NOW,
    PROPOSAL_1,
    PROPOSAL_2,
    PROPOSAL_ALT_A,
    PROPOSAL_AMEND_E1,
    _tally,
    fresh_p1,
    fresh_p2,
    policy_of,
    propose_claim,
    ratify_claim,
    vote,
)
from tests.helpers import Identity, store_with

_T_EXP = 10**9


def _vorschlaege_047() -> dict:
    return {
        PROPOSAL_2.proposal_hash: PROPOSAL_2,
        PROPOSAL_ALT_A.proposal_hash: PROPOSAL_ALT_A,
    }


def _vorschlaege_048() -> dict:
    return {
        PROPOSAL_1.proposal_hash: PROPOSAL_1,
        PROPOSAL_AMEND_E1.proposal_hash: PROPOSAL_AMEND_E1,
    }


def _ziel_047(name: str):
    if name == "alt":
        return PROPOSAL_ALT_A
    return PROPOSAL_2


def _ziel_048(name: str):
    if name == "alt":
        return PROPOSAL_AMEND_E1
    return PROPOSAL_1


@st.composite
def _folgen_047(draw: st.DrawFn) -> tuple:
    """Stimmen, darunter eine zweite gültige und ein Ja auf den anderen Vorschlag."""
    doppel = draw(st.integers(min_value=0, max_value=4))
    dritter = draw(st.integers(min_value=0, max_value=3))
    if dritter >= doppel:
        dritter += 1
    block: list[tuple] = [
        ("vote", doppel, draw(st.sampled_from((0, 1))), False, "haupt"),
        ("vote", dritter, draw(st.sampled_from((0, 1))), False, "haupt"),
        ("vote", dritter, 1, False, "alt"),
        ("vote", draw(st.integers(min_value=0, max_value=4)), 2, False, "haupt"),
        (
            "vote",
            draw(st.integers(min_value=0, max_value=4)),
            draw(st.sampled_from((0, 1, 2))),
            True,
            "haupt",
        ),
        (
            "vote",
            5,
            draw(st.sampled_from((0, 1, 2))),
            draw(st.booleans()),
            "haupt",
        ),
        ("propose", draw(st.integers(min_value=0, max_value=5))),
    ]
    for _ in range(draw(st.integers(min_value=0, max_value=3))):
        autor = draw(st.integers(min_value=0, max_value=5))
        if draw(st.booleans()):
            block.append(("propose", autor))
            continue
        block.append(
            (
                "vote",
                autor,
                draw(st.sampled_from((0, 1, 2))),
                draw(st.booleans()),
                "haupt",
            )
        )
    ordnung = draw(st.permutations(range(len(block))))
    schritte = [block[i] for i in ordnung]
    vorher = sum(1 for step in schritte if step[0] == "vote" and step[1] == doppel)
    schritte.append(("vote", doppel, 1, False, "haupt"))
    schritte.append(("revoke", doppel, vorher))
    return tuple(schritte)


@st.composite
def _folgen_048(draw: st.DrawFn) -> tuple:
    """Zusätze, darunter gültige Zweitstimmen der Zeugen auf beide Vorschläge."""
    block: list[tuple] = [
        ("revoke-ratify",),
        ("supersede-ratify",),
        (
            "vote",
            4,
            draw(st.sampled_from((0, 1, 2))),
            draw(st.booleans()),
            "haupt",
        ),
        ("vote", draw(st.sampled_from((0, 1, 2))), 2, False, "haupt"),
        (
            "vote",
            draw(st.sampled_from((0, 1, 2))),
            draw(st.sampled_from((0, 1))),
            True,
            "haupt",
        ),
        ("vote", 3, draw(st.sampled_from((0, 1, 2))), draw(st.booleans()), "haupt"),
        ("propose", draw(st.integers(min_value=0, max_value=4))),
    ]
    ordnung = draw(st.permutations(range(len(block))))
    schritte = [block[i] for i in ordnung]
    alice_vorher = sum(1 for step in schritte if step[0] == "vote" and step[1] == 0)
    schritte.append(("vote", 0, 1, False, "haupt"))
    bob_vorher = sum(1 for step in schritte if step[0] == "vote" and step[1] == 1)
    schritte.append(("vote", 1, 1, False, "alt"))
    schritte.append(("revoke", 0, alice_vorher))
    schritte.append(("revoke", 1, bob_vorher))
    return tuple(schritte)


def _leute_047() -> list[Identity]:
    fremd = Identity("fremd-inv047", seed=bytes([0x09] * 32))
    assert fremd.pub not in C2["participants"]
    return [*fresh_p2(), fremd]


def _zaehlende_047(store) -> set[bytes]:
    result = _tally(
        store,
        epoch=EPOCH_2,
        proposal=PROPOSAL_2,
        constitution=C2,
        target=C3,
        known=_vorschlaege_047(),
    )
    return set(result.yes) | set(result.no)


def _pruefe_047(folge: tuple) -> bool:
    """True, wenn die zählende Menge in mindestens einem Schritt schrumpft."""
    autoren = _leute_047()
    zuletzt = [0, 0, 0, 0, 0, 0]
    stimmen: list[list[Claim]] = [[], [], [], [], [], []]
    von_claim: dict[bytes, bytes] = {}
    store = store_with()
    gesehen: set[bytes] = set()
    entfallen: set[bytes] = set()
    schrumpfte = False

    def naechstes(autor: int) -> int:
        zuletzt[autor] += 1
        return zuletzt[autor]

    for step in folge:
        art = step[0]
        if art == "vote":
            _art, autor, choice, mit, vorschlag = step
            claim = vote(
                autoren[autor],
                _ziel_047(vorschlag),
                choice=choice,
                t=naechstes(autor),
                t_exp=_T_EXP if mit else None,
            )
            stimmen[autor].append(claim)
            von_claim[claim_id(claim)] = claim.I
            store.add(claim)
        elif art == "propose":
            claim = propose_claim(autoren[step[1]], PROPOSAL_2, t=naechstes(step[1]))
            store.add(claim)
        elif art == "revoke":
            _art, autor, ziel = step
            claim = autoren[autor].revoke(stimmen[autor][ziel], t=naechstes(autor))
            store.add(claim)
        else:
            raise AssertionError(art)
        aktuell = _zaehlende_047(store)
        for cid in gesehen - aktuell:
            assert von_claim[cid] == claim.I
            schrumpfte = True
        entfallen |= gesehen - aktuell
        assert entfallen.isdisjoint(aktuell)
        gesehen = aktuell
    return schrumpfte


def _leute_048() -> tuple[list[Identity], list[Claim]]:
    mitglieder = list(fresh_p1())
    fremd = Identity("fremd-inv048", seed=bytes([0x0A] * 32))
    assert fremd.pub not in C1["participants"]
    stimmen = [
        vote(mitglied, PROPOSAL_1, choice=1, t=1) for mitglied in mitglieder[:3]
    ]
    return [*mitglieder, fremd], stimmen


def _pruefe_048(folge: tuple) -> bool:
    """True, wenn die Epoche in mindestens einem Schritt fällt."""
    autoren, stimmen = _leute_048()
    store = store_with(*stimmen)
    ratify = ratify_claim(
        autoren[0],
        PROPOSAL_1,
        witnesses=[claim_id(stimme) for stimme in stimmen],
        t=10,
    )
    store.add(ratify)
    policy = policy_of(C1)
    zeugen = {stimme.I for stimme in stimmen}
    etabliert = verify_ratification(
        store,
        ratify=ratify,
        epoch=EPOCH_1,
        proposal=PROPOSAL_1,
        tally=_tally(store, known=_vorschlaege_048()),
        target_constitution_obj=C2,
        now=NOW,
        policy=policy,
    )
    assert etabliert.next_epoch is not None
    epoch_id = etabliert.next_epoch.epoch_id
    zuletzt = [10, 1, 1, 0, 0]
    hinzugefuegt: list[list[Claim]] = [[], [], [], [], []]
    steht = True
    gefallen = False

    def naechstes(autor: int) -> int:
        zuletzt[autor] += 1
        return zuletzt[autor]

    for step in folge:
        art = step[0]
        if art == "vote":
            _art, autor, choice, mit, vorschlag = step
            claim = vote(
                autoren[autor],
                _ziel_048(vorschlag),
                choice=choice,
                t=naechstes(autor),
                t_exp=_T_EXP if mit else None,
            )
            hinzugefuegt[autor].append(claim)
        elif art == "propose":
            claim = propose_claim(autoren[step[1]], PROPOSAL_1, t=naechstes(step[1]))
        elif art == "revoke-ratify":
            claim = autoren[0].revoke(ratify, t=naechstes(0))
        elif art == "supersede-ratify":
            claim = autoren[0].supersede(ratify, t=naechstes(0))
        elif art == "revoke":
            _art, autor, ziel = step
            claim = autoren[autor].revoke(hinzugefuegt[autor][ziel], t=naechstes(autor))
        else:
            raise AssertionError(art)
        store.add(claim)
        erneut = verify_ratification(
            store,
            ratify=ratify,
            epoch=EPOCH_1,
            proposal=PROPOSAL_1,
            tally=_tally(store, known=_vorschlaege_048()),
            target_constitution_obj=C2,
            now=NOW,
            policy=policy,
        )
        jetzt = (
            erneut.next_epoch is not None and erneut.next_epoch.epoch_id == epoch_id
        )
        if steht and not jetzt:
            assert claim.I in zeugen
            gefallen = True
        if gefallen:
            assert not jetzt
        steht = jetzt
    return gefallen


@given(_folgen_047())
def test_INV_04_7_counting_set_monotonic_random(folge: tuple) -> None:
    """04 §3.1, 04 §4.4, D433: entwertet wird nur durch den Autor der Stimme."""
    _pruefe_047(folge)


@given(_folgen_048())
def test_INV_04_8_established_epoch_persists_random(folge: tuple) -> None:
    """04 §4.1, 04 §4.4, D433: fällt nur durch einen Zeugen und nicht wieder auf."""
    _pruefe_048(folge)
