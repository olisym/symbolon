"""Geräte in der Auszählung und der Feststellung (04 §3.1, 04 §3.2, 04 §4.1, 04 §4.4, 02 §2.1, D529 bis D539).

Welt aus ``tests/governance/fixtures.py``: ``P2``, ``GENESIS_D``, ``N_D``. Eine Verfassung ``CV``
mit ``verdict@1`` in ``irrevocable_predicates`` und Schiedsrichterin ALICE, die Epoche ``EV``
darauf, ein Vorschlag auf ``C3`` und ein zweiter derselben Epoche. Die Aufnahme entsteht aus
echten Claims. „Wie die Wurzel“ heisst: gleich der Auszählung derselben Welt, in der die Wurzel
selbst stimmt (D530).
"""

from __future__ import annotations

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id
from symbolon.governance import verify_ratification
from symbolon.governance.findings import GovernanceFinding
from symbolon.governance.objects import Epoch, Proposal
from symbolon.governance.tally import TallyResult, TallyState, reached
from symbolon.policy import constitution_hash
from tests.helpers import Identity, store_with

from .fixtures import (
    ALICE,
    C2_ALT_A,
    C3,
    CONSTITUTION_HASH_3,
    N_D,
    NOW,
    P2,
    _constitution,
    _tally,
    fresh_p2,
    nuc,
    policy_of,
    ratify_claim,
    vote,
)

CV = _constitution(
    participants=P2,
    irrevocable=["obligation@1", "ratify@1", "verdict@1", "vote@1"],
    arbitrators=[ALICE.pub],
)
EV = Epoch(scope=N_D, index=2, constitution_hash=constitution_hash(CV))
PV = Proposal(scope=N_D, predecessor=EV.epoch_id, constitution_hash=CONSTITUTION_HASH_3)


class _Welt:
    """Frische Ketten für ALICE bis EVE und ihre Geräte; ``claims`` ist der Bestand.

    Epoche 2 auf ``constitution``, ein Vorschlag auf ``C3`` und ein zweiter auf ``C2_ALT_A``.
    """

    def __init__(self, constitution: dict = CV) -> None:
        self.alice, self.bob, self.carol, self.dave, self.eve = fresh_p2()
        self.claims: list[Claim] = []
        self.t = 0
        self.constitution = constitution
        self.epoch = Epoch(scope=N_D, index=2, constitution_hash=constitution_hash(constitution))
        self.proposal = Proposal(
            scope=N_D, predecessor=self.epoch.epoch_id, constitution_hash=CONSTITUTION_HASH_3
        )
        self.alt = Proposal(
            scope=N_D,
            predecessor=self.epoch.epoch_id,
            constitution_hash=constitution_hash(C2_ALT_A),
        )

    def _next_t(self) -> int:
        self.t += 1
        return self.t

    def add(self, *claims: Claim) -> list[Claim]:
        self.claims.extend(claims)
        return list(claims)

    def device(self, root: Identity, label: str) -> tuple[Identity, Claim]:
        """Gerät mit eigenem Namen, von ``root`` aufgenommen und gegengezeichnet (01 §7.3)."""
        device = Identity(label)
        add = root.claim(
            p=nuc(N_D, "device-add"), J=(1, device.pub), t=self._next_t(), N=N_D
        )
        ack = device.claim(
            p=nuc(N_D, "device-ack"), J=(2, claim_id(add)), t=self._next_t(), N=N_D
        )
        self.add(add, ack)
        return device, ack

    def end_at(self, root: Identity, device: Identity, endpoint: Claim) -> Claim:
        (end,) = self.add(
            root.claim(
                p=nuc(N_D, "device-end"),
                J=(1, device.pub),
                t=self._next_t(),
                N=N_D,
                v=cbor_canon.encode({0: claim_id(endpoint)}),
            )
        )
        return end

    def vote(self, who: Identity, choice: int, *, alt: bool = False) -> Claim:
        proposal = self.alt if alt else self.proposal
        (v,) = self.add(vote(who, proposal, choice=choice, t=self._next_t()))
        return v

    def accuse(self, who: Identity, target: Claim, *, tag: int = 2) -> Claim:
        (a,) = self.add(
            who.claim(
                p=nuc(N_D, "accusation"), J=(tag, claim_id(target)), t=self._next_t(), N=N_D
            )
        )
        return a

    def verdict(
        self,
        who: Identity,
        accusation: Claim,
        *,
        v: bytes | None = cbor_canon.encode({0: 1}),
        t_exp: int | None = None,
    ) -> Claim:
        (c,) = self.add(
            who.claim(
                p=nuc(N_D, "verdict"),
                J=(2, claim_id(accusation)),
                t=self._next_t(),
                N=N_D,
                v=v,
                t_exp=t_exp,
            )
        )
        return c

    def tally(self, *, both_known: bool = False) -> TallyResult:
        known = {self.proposal.proposal_hash: self.proposal}
        if both_known:
            known[self.alt.proposal_hash] = self.alt
        return _tally(
            store_with(*self.claims),
            epoch=self.epoch,
            proposal=self.proposal,
            constitution=self.constitution,
            target=C3,
            known=known,
        )


def _kinds(tally: TallyResult, kind: GovernanceFinding) -> set[bytes]:
    return {f.subject for f in tally.findings if f.kind is kind}


def _world_votes(root_votes_self: bool) -> tuple[_Welt, TallyResult]:
    """BOB, CAROL, DAVE Ja; ALICE Ja selbst oder über ihr Gerät."""
    w = _Welt()
    if root_votes_self:
        w.vote(w.alice, 1)
    else:
        device, _ack = w.device(w.alice, "ALICE_GERAET")
        w.vote(device, 1)
    for who in (w.bob, w.carol, w.dave):
        w.vote(who, 1)
    return w, w.tally()


def test_1_geraet_wie_wurzel() -> None:
    _w, via_root = _world_votes(True)
    _w, via_device = _world_votes(False)
    assert via_device.state is via_root.state
    assert len(via_device.yes) == len(via_root.yes)
    assert _kinds(via_device, GovernanceFinding.NON_MEMBER_VOTE) == set()


def test_2_gleiche_wahl_einmal() -> None:
    once = _Welt()
    for who in (once.alice, once.bob, once.carol, once.dave):
        once.vote(who, 1)
    expected = once.tally()

    w = _Welt()
    device, _ack = w.device(w.alice, "ALICE_GERAET")
    own = w.vote(w.alice, 1)
    via = w.vote(device, 1)
    for who in (w.bob, w.carol, w.dave):
        w.vote(who, 1)
    tally = w.tally()
    assert {claim_id(own), claim_id(via)} <= set(tally.yes)
    assert _kinds(tally, GovernanceFinding.AMBIGUOUS_VOTE) == set()
    assert tally.state is expected.state


def test_3_wurzeln_an_der_schwelle() -> None:
    three = _Welt()
    for who in (three.alice, three.bob, three.carol):
        three.vote(who, 1)
    expected = three.tally()

    w = _Welt()
    device, _ack = w.device(w.alice, "ALICE_GERAET")
    w.vote(w.alice, 1)
    w.vote(device, 1)
    w.vote(w.bob, 1)
    w.vote(w.carol, 1)
    tally = w.tally()
    assert tally.threshold is not None and tally.n is not None
    num, den = tally.threshold
    # Die Welt trennt Wurzeln von Stimmen (D539 Befund 4).
    assert not reached(3, tally.n, num, den)
    assert reached(4, tally.n, num, den)
    assert len(tally.yes) == 4
    assert tally.state is expected.state


def test_4_verschiedene_wahl() -> None:
    w = _Welt()
    device, _ack = w.device(w.alice, "ALICE_GERAET")
    own = w.vote(w.alice, 1)
    via = w.vote(device, 0)
    tally = w.tally()
    assert _kinds(tally, GovernanceFinding.AMBIGUOUS_VOTE) == {claim_id(own), claim_id(via)}
    assert claim_id(own) not in tally.yes
    assert claim_id(via) not in tally.no


def test_5_nicht_delegiert() -> None:
    w = _Welt()
    stray = Identity("ALICE_GERAET_OHNE_AUFNAHME")
    v = w.vote(stray, 1)
    tally = w.tally()
    assert _kinds(tally, GovernanceFinding.NON_MEMBER_VOTE) == {claim_id(v)}
    assert claim_id(v) not in tally.yes


def test_6_bestritten() -> None:
    w = _Welt()
    device, ack = w.device(w.alice, "ALICE_GERAET")
    own = w.vote(w.alice, 1)
    via = w.vote(device, 0)
    w.end_at(w.alice, device, ack)
    tally = w.tally()
    assert _kinds(tally, GovernanceFinding.DISPUTED_VOTE) == {claim_id(via)}
    assert claim_id(own) in tally.yes
    assert _kinds(tally, GovernanceFinding.AMBIGUOUS_VOTE) == set()


def _disputed_dave(w: _Welt) -> tuple[Claim, Claim]:
    """DAVEs Gerät stimmt Ja, DAVE sperrt beim Ack, BOB klagt an."""
    device, ack = w.device(w.dave, "DAVE_GERAET")
    v = w.vote(device, 1)
    w.end_at(w.dave, device, ack)
    return v, w.accuse(w.bob, v)


def test_7_verdikt_rechnet_zu() -> None:
    w = _Welt()
    v, accusation = _disputed_dave(w)
    w.verdict(w.alice, accusation)
    tally = w.tally()
    assert claim_id(v) in tally.yes
    assert _kinds(tally, GovernanceFinding.DISPUTED_VOTE) == set()


def _assert_disputed(w: _Welt, v: Claim) -> None:
    tally = w.tally()
    assert _kinds(tally, GovernanceFinding.DISPUTED_VOTE) == {claim_id(v)}
    assert claim_id(v) not in tally.yes


def test_8_verdikt_ohne_unwiderruflichkeit() -> None:
    revocable = _constitution(
        participants=P2,
        irrevocable=["obligation@1", "ratify@1", "vote@1"],
        arbitrators=[ALICE.pub],
    )
    w = _Welt(revocable)
    v, accusation = _disputed_dave(w)
    w.verdict(w.alice, accusation)
    _assert_disputed(w, v)


def test_8_verdikt_keine_schiedsrichterin() -> None:
    w = _Welt()
    v, accusation = _disputed_dave(w)
    w.verdict(w.carol, accusation)
    _assert_disputed(w, v)


def test_8_verdikt_ausgang_2() -> None:
    w = _Welt()
    v, accusation = _disputed_dave(w)
    w.verdict(w.alice, accusation, v=cbor_canon.encode({0: 2}))
    _assert_disputed(w, v)


def test_8_verdikt_mit_t_exp() -> None:
    w = _Welt()
    v, accusation = _disputed_dave(w)
    w.verdict(w.alice, accusation, t_exp=NOW + 1000)
    _assert_disputed(w, v)


def test_9_konflikt_ueber_geraete() -> None:
    w = _Welt()
    device, _ack = w.device(w.alice, "ALICE_GERAET")
    own = w.vote(w.alice, 1)
    w.vote(device, 1, alt=True)
    tally = w.tally(both_known=True)
    assert claim_id(own) in _kinds(tally, GovernanceFinding.CONFLICTING_APPROVAL)
    assert claim_id(own) not in tally.yes


def test_10_konflikt_ohne_bestrittene() -> None:
    w = _Welt()
    device, ack = w.device(w.alice, "ALICE_GERAET")
    own = w.vote(w.alice, 1)
    w.vote(device, 1, alt=True)
    w.end_at(w.alice, device, ack)
    tally = w.tally(both_known=True)
    assert _kinds(tally, GovernanceFinding.CONFLICTING_APPROVAL) == set()
    assert claim_id(own) in tally.yes


def test_11_feststellung_je_wurzel() -> None:
    w = _Welt()
    device, _ack = w.device(w.alice, "ALICE_GERAET")
    stray = Identity("FREMDES_GERAET")
    own = w.vote(w.alice, 1)
    via = w.vote(device, 1)
    others = [w.vote(who, 1) for who in (w.bob, w.carol, w.dave)]
    four = [claim_id(own), *(claim_id(o) for o in others)]
    both = [claim_id(own), claim_id(via), *(claim_id(o) for o in others)]
    ratifies = {
        "alice": ratify_claim(w.alice, PV, witnesses=four, t=100),
        "geraet": ratify_claim(device, PV, witnesses=four, t=100),
        "beide": ratify_claim(w.alice, PV, witnesses=both, t=101),
        "fremd": ratify_claim(stray, PV, witnesses=four, t=100),
    }
    w.add(*ratifies.values())
    tally = w.tally()
    assert tally.state is TallyState.PASSED
    store = store_with(*w.claims)

    def established(r: Claim) -> bool:
        result = verify_ratification(
            store,
            ratify=r,
            epoch=EV,
            proposal=PV,
            tally=tally,
            target_constitution_obj=C3,
            now=NOW,
            policy=policy_of(CV),
        )
        return result.next_epoch is not None

    assert established(ratifies["alice"])
    assert established(ratifies["geraet"])
    assert not established(ratifies["beide"])
    assert not established(ratifies["fremd"])


def test_12_formwidrig() -> None:
    # accusation@1 mit J-Tag nicht claim-ref
    w = _Welt()
    device, ack = w.device(w.dave, "DAVE_GERAET")
    v = w.vote(device, 1)
    w.end_at(w.dave, device, ack)
    w.verdict(w.alice, w.accuse(w.bob, v, tag=3))
    _assert_disputed(w, v)

    # verdict@1 ohne v, mit nicht kanonischem v, mit v ohne Key 0
    for raw in (None, bytes.fromhex("a1001801"), cbor_canon.encode({1: bytes(32)})):
        w = _Welt()
        v, accusation = _disputed_dave(w)
        w.verdict(w.alice, accusation, v=raw)
        _assert_disputed(w, v)

    # arbitration ist keine Map
    broken = dict(CV)
    broken["arbitration"] = [ALICE.pub]
    w = _Welt(broken)
    v, accusation = _disputed_dave(w)
    w.verdict(w.alice, accusation)
    _assert_disputed(w, v)
