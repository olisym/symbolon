"""INV-04.7 und INV-04.8 über zufällige Claim-Folgen (04-golden-anchors.md §8).

Equivocation bleibt draussen: jede Identität führt eine Kette, keine zwei Claims
eines Autors auf dieselbe Spitze (04-golden-anchors.md §8).

Eine zweite Stimme desselben Autors mit bekanntem ``choice`` und ohne ``t_exp``
wäre ``AMBIGUOUS_VOTE`` (04 §3.1) und nähme die erste aus der zählenden Menge,
ohne Equivocation. Solche Folgen erzeugt der Generator nicht.
"""

from __future__ import annotations

from hypothesis import given, strategies as st

from symbolon.atom import claim_id
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


def _schluessel_index(schritte: tuple, marker: str) -> tuple[int, int]:
    gesehen = [0, 0, 0, 0, 0, 0]
    for step in schritte:
        if step[0] != "vote":
            continue
        autor = step[1]
        if step[4] == marker:
            return autor, gesehen[autor]
        gesehen[autor] += 1
    raise AssertionError(marker)


@st.composite
def _folgen_047(draw: st.DrawFn) -> tuple:
    """Stimmen, Widerruf, Supersede, Vorschläge, Mitglieder und ein Nichtmitglied."""
    ja_autor = draw(st.integers(min_value=0, max_value=4))
    nein_autor = draw(st.integers(min_value=0, max_value=3))
    if nein_autor >= ja_autor:
        nein_autor += 1
    zaehlend = {ja_autor, nein_autor}
    block = [
        ("vote", ja_autor, 1, False, "ja"),
        ("vote", nein_autor, 0, False, "nein"),
        ("vote", draw(st.integers(min_value=0, max_value=4)), 2, False, ""),
        (
            "vote",
            draw(st.integers(min_value=0, max_value=4)),
            draw(st.sampled_from((0, 1, 2))),
            True,
            "",
        ),
        (
            "vote",
            5,
            draw(st.sampled_from((0, 1, 2))),
            draw(st.booleans()),
            "",
        ),
        ("propose", draw(st.integers(min_value=0, max_value=5))),
    ]
    for _ in range(draw(st.integers(min_value=0, max_value=3))):
        autor = draw(st.integers(min_value=0, max_value=5))
        if draw(st.booleans()):
            block.append(("propose", autor))
            continue
        choice = draw(st.sampled_from((0, 1, 2)))
        mit = draw(st.booleans())
        if autor <= 4 and choice in (0, 1) and not mit and autor in zaehlend:
            mit = True
        if autor <= 4 and choice in (0, 1) and not mit:
            zaehlend.add(autor)
        block.append(("vote", autor, choice, mit, ""))
    ordnung = draw(st.permutations(range(len(block))))
    schritte = [block[i] for i in ordnung]
    ja = _schluessel_index(tuple(schritte), "ja")
    nein = _schluessel_index(tuple(schritte), "nein")
    schritte.append(("revoke", ja[0], ja[1]))
    schritte.append(("supersede", nein[0], nein[1]))
    return tuple(schritte)


@st.composite
def _folgen_048(draw: st.DrawFn) -> tuple:
    """Zusätze nach etablierter Epoche, darunter Widerruf und Supersede."""
    block = [
        ("revoke-zeuge", 0),
        ("supersede-zeuge", 1),
        ("revoke-ratify",),
        ("supersede-ratify",),
        ("vote", 3, draw(st.sampled_from((0, 1))), False),
        (
            "vote",
            4,
            draw(st.sampled_from((0, 1, 2))),
            draw(st.booleans()),
        ),
        ("vote", draw(st.sampled_from((0, 1, 2))), 2, False),
        (
            "vote",
            draw(st.integers(min_value=0, max_value=3)),
            draw(st.sampled_from((0, 1))),
            True,
        ),
        ("propose", draw(st.integers(min_value=0, max_value=4))),
    ]
    ordnung = draw(st.permutations(range(len(block))))
    return tuple(block[i] for i in ordnung)


def _leute_047() -> list[Identity]:
    fremd = Identity("fremd-inv047", seed=bytes([0x09] * 32))
    assert fremd.pub not in C2["participants"]
    return [*fresh_p2(), fremd]


def _zaehlende(store, *, epoch, proposal, constitution, target) -> set[bytes]:
    result = _tally(
        store,
        epoch=epoch,
        proposal=proposal,
        constitution=constitution,
        target=target,
    )
    return set(result.yes) | set(result.no)


@given(_folgen_047())
def test_INV_04_7_counting_set_monotonic_random(folge: tuple) -> None:
    """04 §3.1: die zählende Menge schrumpft nicht, Equivocation ausgenommen."""
    autoren = _leute_047()
    zuletzt = [0, 0, 0, 0, 0, 0]
    stimmen: list[list] = [[], [], [], [], [], []]
    store = store_with()
    gesehen: set[bytes] = set()

    def naechstes(autor: int) -> int:
        zuletzt[autor] += 1
        return zuletzt[autor]

    for step in folge:
        art = step[0]
        if art == "vote":
            _art, autor, choice, mit, _marker = step
            stimmen[autor].append(
                vote(
                    autoren[autor],
                    PROPOSAL_2,
                    choice=choice,
                    t=naechstes(autor),
                    t_exp=_T_EXP if mit else None,
                )
            )
            store.add(stimmen[autor][-1])
        elif art == "propose":
            autor = step[1]
            store.add(
                propose_claim(autoren[autor], PROPOSAL_2, t=naechstes(autor))
            )
        elif art == "revoke":
            _art, autor, ziel = step
            store.add(
                autoren[autor].revoke(stimmen[autor][ziel], t=naechstes(autor))
            )
        else:
            _art, autor, ziel = step
            store.add(
                autoren[autor].supersede(stimmen[autor][ziel], t=naechstes(autor))
            )
        aktuell = _zaehlende(
            store,
            epoch=EPOCH_2,
            proposal=PROPOSAL_2,
            constitution=C2,
            target=C3,
        )
        assert gesehen <= aktuell
        gesehen = aktuell


def _leute_048() -> tuple[list[Identity], list]:
    mitglieder = list(fresh_p1())
    fremd = Identity("fremd-inv048", seed=bytes([0x0A] * 32))
    assert fremd.pub not in C1["participants"]
    stimmen = [
        vote(mitglied, PROPOSAL_1, choice=1, t=1) for mitglied in mitglieder[:3]
    ]
    return [*mitglieder, fremd], stimmen


@given(_folgen_048())
def test_INV_04_8_established_epoch_persists_random(folge: tuple) -> None:
    """04 §4.1: die Epoche bleibt, die Auszählung jedes Mal neu aus dem Speicher."""
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
    etabliert = verify_ratification(
        store,
        ratify=ratify,
        epoch=EPOCH_1,
        proposal=PROPOSAL_1,
        tally=_tally(store),
        target_constitution_obj=C2,
        now=NOW,
        policy=policy,
    )
    assert etabliert.next_epoch is not None
    epoch_id = etabliert.next_epoch.epoch_id
    zuletzt = [10, 1, 1, 0, 0]

    def naechstes(autor: int) -> int:
        zuletzt[autor] += 1
        return zuletzt[autor]

    for step in folge:
        art = step[0]
        if art == "revoke-zeuge":
            autor = step[1]
            store.add(autoren[autor].revoke(stimmen[autor], t=naechstes(autor)))
        elif art == "supersede-zeuge":
            autor = step[1]
            store.add(autoren[autor].supersede(stimmen[autor], t=naechstes(autor)))
        elif art == "revoke-ratify":
            store.add(autoren[0].revoke(ratify, t=naechstes(0)))
        elif art == "supersede-ratify":
            store.add(autoren[0].supersede(ratify, t=naechstes(0)))
        elif art == "vote":
            _art, autor, choice, mit = step
            store.add(
                vote(
                    autoren[autor],
                    PROPOSAL_1,
                    choice=choice,
                    t=naechstes(autor),
                    t_exp=_T_EXP if mit else None,
                )
            )
        else:
            store.add(propose_claim(autoren[step[1]], PROPOSAL_1, t=naechstes(step[1])))
        erneut = verify_ratification(
            store,
            ratify=ratify,
            epoch=EPOCH_1,
            proposal=PROPOSAL_1,
            tally=_tally(store),
            target_constitution_obj=C2,
            now=NOW,
            policy=policy,
        )
        assert erneut.next_epoch is not None
        assert erneut.next_epoch.epoch_id == epoch_id
