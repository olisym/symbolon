"""Geheime Wahl: Golden Anchors WV-1 bis WV-17 (04-golden-anchors.md §13, 04 §9, D669, D671).

Die Hashes der Wahl und der Listen rechnet der Test aus den Objekten; jede Identität frisch (D464).
"""

from __future__ import annotations

import hashlib

from symbolon import cbor_canon
from symbolon.atom import claim_id
from symbolon.governance import GovernanceFinding
from symbolon.governance.election import (
    BallotList,
    Election,
    ElectionState,
    tally_election,
)

from tests.helpers import Identity, store_with

from .fixtures import C1, N_D, NOW, _constitution, fresh_p1, nuc, policy_of

IRR_WAHL = ["ballot-ack@1", "ballot@1", "obligation@1", "ratify@1", "vote@1"]
CV = _constitution(participants=C1["participants"], irrevocable=IRR_WAHL)
CV_OHNE_BALLOT = _constitution(
    participants=C1["participants"],
    irrevocable=["ballot-ack@1", "obligation@1", "ratify@1", "vote@1"],
)


def _epoch(constitution):
    from symbolon.governance import Epoch
    from symbolon.policy import constitution_hash

    return Epoch(scope=N_D, index=1, constitution_hash=constitution_hash(constitution))


class Welt:
    """Profil D, Epoche 1 mit ``CV``; ALICE, BOB, CAROL, DAVE und K1 bis K5 frisch."""

    def __init__(self, constitution=CV):
        self.constitution = constitution
        self.epoch = _epoch(constitution)
        self.alice, self.bob, self.carol, self.dave = fresh_p1()
        self.k = {i: Identity(f"WV-K{i}") for i in range(1, 6)}
        self.wahl = Election(
            {
                0: N_D,
                1: self.epoch.epoch_id,
                2: "vorstand",
                3: sorted([self.alice.pub, self.bob.pub]),
                4: "Vorstand 2026",
            }
        )
        self.claims = []
        self.objekte = {self.wahl.election_hash: self.wahl}
        self.t = 1

    def liste(self, members, keys, *, ohne=()):
        lst = BallotList(
            {
                0: self.wahl.election_hash,
                1: sorted(m.pub for m in members),
                2: sorted(k.pub for k in keys),
            }
        )
        self.objekte[lst.list_hash] = lst
        for ident in [*members, *keys]:
            if ident not in ohne:
                self.ack(ident, lst.list_hash)
        return lst

    def ack(self, ident, h):
        self.t += 1
        self.claims.append(
            ident.claim(p=nuc(N_D, "ballot-ack"), J=(3, h), t=self.t, N=N_D)
        )

    def stimme(self, key, kandidat, wahlgang=0):
        self.t += 1
        c = key.claim(
            p=nuc(N_D, "ballot"),
            J=(3, self.wahl.election_hash),
            t=self.t,
            N=N_D,
            v=cbor_canon.encode({0: kandidat.pub, 1: wahlgang}),
        )
        self.claims.append(c)
        return c

    def zaehlen(self):
        return tally_election(
            store_with(*self.claims),
            scope=N_D,
            election=self.wahl,
            epoch=self.epoch,
            constitution_obj=self.constitution,
            known_objects=self.objekte,
            now=NOW,
            policy=policy_of(self.constitution),
        )

    def lv(self, **kw):
        return self.liste(
            [self.alice, self.bob, self.carol, self.dave],
            [self.k[1], self.k[2], self.k[3], self.k[4]],
            **kw,
        )


def _arten(result):
    return {f.kind for f in result.findings}


def test_wv_1() -> None:
    w = Welt()
    w.lv()
    for i in (1, 2, 3):
        w.stimme(w.k[i], w.alice)
    r = w.zaehlen()
    assert (r.state, r.elected, r.current_round) == (ElectionState.ELECTED, w.alice.pub, 0)


def test_wv_2() -> None:
    w = Welt()
    w.lv()
    w.stimme(w.k[1], w.alice)
    w.stimme(w.k[2], w.alice)
    w.stimme(w.k[3], w.bob)
    w.stimme(w.k[4], w.bob)
    r = w.zaehlen()
    assert (r.state, r.elected, r.current_round) == (ElectionState.OPEN, None, 1)


def test_wv_3() -> None:
    w = Welt()
    w.lv()
    w.stimme(w.k[1], w.alice)
    w.stimme(w.k[2], w.alice)
    w.stimme(w.k[3], w.bob)
    r = w.zaehlen()
    assert (r.state, r.current_round) == (ElectionState.OPEN, 0)


def test_wv_4() -> None:
    w = Welt()
    lst = w.liste([w.alice, w.bob, w.carol], [w.k[1], w.k[2], w.k[3]])
    w.stimme(w.k[1], w.alice)
    w.stimme(w.k[2], w.alice)
    w.stimme(w.k[3], w.bob)
    r = w.zaehlen()
    assert r.lists == (lst.list_hash,)
    assert (r.state, r.current_round) == (ElectionState.OPEN, 0)


def test_wv_5() -> None:
    w = Welt()
    w.lv()
    a = w.stimme(w.k[1], w.alice)
    b = w.stimme(w.k[1], w.bob)
    w.stimme(w.k[2], w.alice)
    w.stimme(w.k[3], w.alice)
    r = w.zaehlen()
    assert (r.state, r.current_round) == (ElectionState.OPEN, 0)
    amb = {f.subject for f in r.findings if f.kind is GovernanceFinding.AMBIGUOUS_BALLOT}
    assert amb == {claim_id(a), claim_id(b)}


def test_wv_6() -> None:
    w = Welt()
    w.lv(ohne=(w.k[4],))
    for i in (1, 2, 3):
        w.stimme(w.k[i], w.alice)
    r = w.zaehlen()
    assert r.lists == ()
    assert (r.state, r.current_round) == (ElectionState.OPEN, 0)


def _wv_7(w):
    lv1 = w.liste([w.alice, w.bob], [w.k[1], w.k[2]])
    lv2 = w.liste([w.carol, w.dave], [w.k[3], w.k[4]])
    for i in (1, 2, 3):
        w.stimme(w.k[i], w.alice)
    return lv1, lv2


def test_wv_7() -> None:
    w = Welt()
    lv1, lv2 = _wv_7(w)
    r = w.zaehlen()
    assert r.lists == tuple(sorted([lv1.list_hash, lv2.list_hash]))
    assert (r.state, r.elected) == (ElectionState.ELECTED, w.alice.pub)


def test_wv_8() -> None:
    w = Welt()
    lv1, lv2 = _wv_7(w)
    lv3 = w.liste([w.bob], [w.k[5]])
    r = w.zaehlen()
    assert r.lists == (lv2.list_hash,)
    assert (r.state, r.current_round) == (ElectionState.OPEN, 0)
    bob_acks = {
        claim_id(c)
        for c in w.claims
        if c.I == w.bob.pub and c.J[1] in (lv1.list_hash, lv3.list_hash)
    }
    konflikt = {f.subject for f in r.findings if f.kind is GovernanceFinding.CONFLICTING_LIST_ACK}
    assert konflikt == bob_acks


def test_wv_9() -> None:
    w = Welt()
    _lv1, lv2 = _wv_7(w)
    w.ack(w.bob, hashlib.sha256(b"WV-9 unbekannt").digest())
    fremd = w.claims[-1]
    r = w.zaehlen()
    assert r.lists == (lv2.list_hash,)
    assert (r.state, r.current_round) == (ElectionState.OPEN, 0)
    assert {f.subject for f in r.findings if f.kind is GovernanceFinding.UNKNOWN_LIST} == {
        claim_id(fremd)
    }


def test_wv_10() -> None:
    w = Welt(CV_OHNE_BALLOT)
    w.lv()
    for i in (1, 2, 3):
        w.stimme(w.k[i], w.alice)
    r = w.zaehlen()
    assert r.state is ElectionState.UNEVALUABLE
    assert _arten(r) == {GovernanceFinding.BALLOT_REVOCABLE}


def test_wv_11() -> None:
    w = Welt()
    w.lv()
    fremd = w.stimme(w.k[1], w.carol)
    w.stimme(w.k[2], w.alice)
    w.stimme(w.k[3], w.alice)
    w.stimme(w.k[4], w.bob)
    r = w.zaehlen()
    assert (r.state, r.current_round) == (ElectionState.OPEN, 1)
    unbekannt = {f.subject for f in r.findings if f.kind is GovernanceFinding.UNKNOWN_CANDIDATE}
    assert unbekannt == {claim_id(fremd)}


def test_wv_12() -> None:
    w = Welt()
    w.lv()
    w.stimme(w.k[1], w.alice)
    w.stimme(w.k[2], w.alice)
    w.stimme(w.k[3], w.bob)
    w.stimme(w.k[4], w.bob)
    for i in (1, 2, 3):
        w.stimme(w.k[i], w.alice, 1)
    r = w.zaehlen()
    assert (r.state, r.elected, r.current_round) == (ElectionState.ELECTED, w.alice.pub, 1)


def test_wv_13() -> None:
    w = Welt()
    w.lv()
    w.stimme(w.k[1], w.alice)
    w.stimme(w.k[2], w.alice)
    w.stimme(w.k[3], w.bob)
    for i in (1, 2, 3):
        w.stimme(w.k[i], w.alice, 1)
    r = w.zaehlen()
    assert (r.state, r.elected, r.current_round) == (ElectionState.OPEN, None, 0)


def _geraet(w, root, label):
    """Gerät von ``root`` aufgenommen und gegengezeichnet (01 §7.3, 02 §2.1)."""
    device = Identity(label)
    w.t += 1
    add = root.claim(p=nuc(N_D, "device-add"), J=(1, device.pub), t=w.t, N=N_D)
    w.t += 1
    ack = device.claim(p=nuc(N_D, "device-ack"), J=(2, claim_id(add)), t=w.t, N=N_D)
    w.claims.extend([add, ack])
    return device, ack


def _beenden(w, root, device, endpunkt):
    w.t += 1
    w.claims.append(
        root.claim(
            p=nuc(N_D, "device-end"),
            J=(1, device.pub),
            t=w.t,
            N=N_D,
            v=cbor_canon.encode({0: claim_id(endpunkt)}),
        )
    )


def test_wv_14() -> None:
    """Wie WV-1, DAVE bestätigt über sein Gerät (04 §9.3 Bedingung 3, 02 §2.1)."""
    w = Welt()
    geraet, _ack = _geraet(w, w.dave, "WV-DAVE-GERAET")
    lst = w.lv(ohne=(w.dave,))
    w.ack(geraet, lst.list_hash)
    for i in (1, 2, 3):
        w.stimme(w.k[i], w.alice)
    r = w.zaehlen()
    assert (r.state, r.elected) == (ElectionState.ELECTED, w.alice.pub)


def test_wv_15() -> None:
    """Wie oben, aber DAVE beendet das Gerät beim Endpunkt vor der Bestätigung."""
    w = Welt()
    geraet, ack = _geraet(w, w.dave, "WV-DAVE-GERAET")
    lst = w.lv(ohne=(w.dave,))
    w.ack(geraet, lst.list_hash)
    _beenden(w, w.dave, geraet, ack)
    for i in (1, 2, 3):
        w.stimme(w.k[i], w.alice)
    r = w.zaehlen()
    assert r.lists == ()
    assert (r.state, r.current_round) == (ElectionState.OPEN, 0)


def test_wv_17() -> None:
    """WV-7; ein beendetes Gerät von BOB bestätigt LV3 und entwertet LV1 nicht (04 §9.3
    Bedingung 5)."""
    w = Welt()
    geraet, ack = _geraet(w, w.bob, "WV-BOB-GERAET")
    lv1, lv2 = _wv_7(w)
    lv3 = w.liste([w.bob], [w.k[5]], ohne=(w.bob,))
    w.ack(geraet, lv3.list_hash)
    _beenden(w, w.bob, geraet, ack)
    r = w.zaehlen()
    assert r.lists == tuple(sorted([lv1.list_hash, lv2.list_hash]))
    assert (r.state, r.elected) == (ElectionState.ELECTED, w.alice.pub)


CV_VERDIKT = _constitution(
    participants=C1["participants"],
    irrevocable=["ballot-ack@1", "ballot@1", "obligation@1", "ratify@1", "verdict@1", "vote@1"],
)


def test_wv_16() -> None:
    """Wie ``test_wv_15``, mit ``verdict@1`` geschützt und einem
    Verdikt der Schiedsrichterin ALICE (04 §3.1, D533)."""
    w = Welt(CV_VERDIKT)
    geraet, ack = _geraet(w, w.dave, "WV-DAVE-GERAET")
    lst = w.lv(ohne=(w.dave,))
    w.ack(geraet, lst.list_hash)
    bestritten = w.claims[-1]
    _beenden(w, w.dave, geraet, ack)
    w.t += 1
    anklage = w.carol.claim(
        p=nuc(N_D, "accusation"), J=(2, claim_id(bestritten)), t=w.t, N=N_D
    )
    w.t += 1
    verdikt = w.alice.claim(
        p=nuc(N_D, "verdict"),
        J=(2, claim_id(anklage)),
        t=w.t,
        N=N_D,
        v=cbor_canon.encode({0: 1}),
    )
    w.claims.extend([anklage, verdikt])
    for i in (1, 2, 3):
        w.stimme(w.k[i], w.alice)
    r = w.zaehlen()
    assert r.lists == (lst.list_hash,)
    assert (r.state, r.elected) == (ElectionState.ELECTED, w.alice.pub)


def test_formwidrige_stimme_bindet_nicht() -> None:
    """Wie WV-1, aber ``K3`` nennt den Wahlgang als ``true`` (04 §9.4)."""
    w = Welt()
    w.lv()
    w.stimme(w.k[1], w.alice)
    w.stimme(w.k[2], w.alice)
    w.t += 1
    formwidrig = w.k[3].claim(
        p=nuc(N_D, "ballot"),
        J=(3, w.wahl.election_hash),
        t=w.t,
        N=N_D,
        v=cbor_canon.encode({0: w.alice.pub, 1: True}),
    )
    w.claims.append(formwidrig)
    r = w.zaehlen()
    assert (r.state, r.current_round) == (ElectionState.OPEN, 0)
    assert {f.subject for f in r.findings if f.kind is GovernanceFinding.MALFORMED_BALLOT} == {
        claim_id(formwidrig)
    }


def test_formwidrige_liste_traegt_nicht() -> None:
    """``LV`` mit einem Schlüssel weniger als Teilnehmer (04 §9.1); alle haben bestätigt."""
    w = Welt()
    w.liste([w.alice, w.bob, w.carol, w.dave], [w.k[1], w.k[2], w.k[3]])
    for i in (1, 2, 3):
        w.stimme(w.k[i], w.alice)
    r = w.zaehlen()
    assert r.lists == ()
    assert r.state is ElectionState.OPEN


def test_unauswertbar_der_reihe_nach() -> None:
    """Die Tabelle aus 04 §9.4 Zeile für Zeile."""
    import pytest

    from symbolon.governance.election import election_wellformed

    w = Welt()
    obj = dict(w.wahl.obj)
    obj[3] = list(reversed(obj[3]))
    w.wahl = Election(obj)
    assert not election_wellformed(w.wahl)
    r = w.zaehlen()
    assert r.state is ElectionState.UNEVALUABLE
    assert r.findings[0].kind is GovernanceFinding.MALFORMED_ELECTION

    w = Welt()
    obj = dict(w.wahl.obj)
    obj[0] = hashlib.sha256(b"anderer Scope").digest()
    w.wahl = Election(obj)
    with pytest.raises(ValueError):
        w.zaehlen()

    w = Welt()
    w.epoch = None
    assert _arten(w.zaehlen()) == {GovernanceFinding.CONSTITUTION_UNAVAILABLE}

    w = Welt()
    w.constitution = CV_OHNE_BALLOT
    assert _arten(w.zaehlen()) == {GovernanceFinding.CONSTITUTION_UNAVAILABLE}

    ohne_vote = _constitution(
        participants=C1["participants"],
        irrevocable=["ballot-ack@1", "ballot@1", "obligation@1", "ratify@1"],
    )
    w = Welt(ohne_vote)
    assert _arten(w.zaehlen()) == {GovernanceFinding.VOTE_REVOCABLE}
