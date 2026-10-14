"""Wahlen im Knoten: Objekte, Sicht und Route (04 §9, D675)."""

from __future__ import annotations

import hashlib
import json

import pytest

from symbolon import cbor_canon
from symbolon.atom import claim_id
from symbolon.governance import BallotList, Election, ElectionState, GovernanceFinding
from symbolon.governance.objects import epoch_id
from symbolon.node.gruendung import gruenden
from symbolon.node.store import ObjectKind, SqliteStore
from symbolon.node.view import elections_view, scope_view
from symbolon.policy import constitution_hash
from tests.helpers import Identity
from tests.node.test_api import _call, _start, _stop
from tools.example_nucleus import people

FELDER = {"name": "Laufgruppe", "sitz": "Ort", "zweck": "Gemeinsam laufen"}
NOW = 1000


class Verein:
    """Ein Verein aus der Vorlage im Bestand; ANNA, BRUNO, CHRIS gründen, DORA kommt dazu."""

    def __init__(self, store: SqliteStore) -> None:
        self.store = store
        self.anna, self.bruno, self.chris, self.dora = people()
        gebaut = gruenden(
            "verein", [p.pub.hex() for p in (self.anna, self.bruno, self.chris)], FELDER
        )
        for art, daten in gebaut.objekte:
            store.submit_object(art, daten)
        self.scope = gebaut.verein
        self.satzung = cbor_canon.decode(gebaut.objekte[0][1])
        self.epoch_1 = epoch_id(self.scope, 1, gebaut.constitution)
        self.t = 0

    def nuc(self, name: str) -> str:
        return f"nuc:{self.scope.hex()}/{name}@1"

    def add(self, author, p: str, J, v: bytes | None = None):
        self.t += 1
        claim = author.claim(p=p, J=J, t=self.t, N=self.scope, v=v)
        self.store.add(claim)
        return claim

    def wahl(self, epoch: bytes, label: str = "Vorstand") -> Election:
        wahl = Election(
            {
                0: self.scope,
                1: epoch,
                2: "vorstand",
                3: sorted([self.anna.pub, self.bruno.pub]),
                4: label,
            }
        )
        assert self.store.submit_object(ObjectKind.ELECTION, cbor_canon.encode(wahl.obj)) == (
            wahl.election_hash
        )
        return wahl

    def liste(self, wahl: Election, members, tag: str) -> tuple[BallotList, list[Identity]]:
        keys = [Identity(f"{tag}-{i}") for i in range(len(members))]
        liste = BallotList(
            {
                0: wahl.election_hash,
                1: sorted(m.pub for m in members),
                2: sorted(k.pub for k in keys),
            }
        )
        assert self.store.submit_object(
            ObjectKind.BALLOT_LIST, cbor_canon.encode(liste.obj)
        ) == liste.list_hash
        for wer in [*members, *keys]:
            self.add(wer, self.nuc("ballot-ack"), (3, liste.list_hash))
        return liste, keys

    def stimme(self, key, wahl: Election, kandidat, wahlgang: int = 0):
        return self.add(
            key,
            self.nuc("ballot"),
            (3, wahl.election_hash),
            cbor_canon.encode({0: kandidat.pub, 1: wahlgang}),
        )

    def epoche_2(self, **aenderung) -> bytes:
        """Epoche 2 mit ``aenderung`` an der Satzung, alle drei stimmen zu und ANNA stellt fest."""
        neu = {**self.satzung, **aenderung}
        self.store.submit_object(ObjectKind.CONSTITUTION, cbor_canon.encode(neu))
        vorschlag = {0: self.scope, 1: self.epoch_1, 2: constitution_hash(neu)}
        digest = self.store.submit_object(ObjectKind.PROPOSAL, cbor_canon.encode(vorschlag))
        stimmen = [
            self.add(p, self.nuc("vote"), (3, digest), cbor_canon.encode({0: 1}))
            for p in (self.anna, self.bruno, self.chris)
        ]
        self.add(
            self.anna,
            self.nuc("ratify"),
            (3, digest),
            cbor_canon.encode({0: sorted(claim_id(c) for c in stimmen)}),
        )
        epoche = scope_view(self.store, self.scope, NOW).state.epoch
        assert epoche.index == 2
        return epoche.epoch_id


def _ergebnis(store, scope, wahl):
    (eintrag,) = [w for w in elections_view(store, scope, NOW) if w.election == wahl.election_hash]
    return eintrag


def test_objekte_wie_sie_kamen(tmp_path) -> None:
    """Wahl und Liste unter ihrem Hash; eine formwidrige Liste bleibt, wie sie kam (04 §9.1)."""
    store = SqliteStore(tmp_path / "s.sqlite")
    v = Verein(store)
    wahl = v.wahl(v.epoch_1)
    formwidrig = {0: wahl.election_hash, 1: [b"\x02" * 32, b"\x01" * 32], 2: [b"\x03" * 32]}
    digest = store.submit_object(ObjectKind.BALLOT_LIST, cbor_canon.encode(formwidrig))
    assert digest == BallotList(formwidrig).list_hash
    assert store.all_ballot_lists()[digest].obj == formwidrig
    assert store.all_elections()[wahl.election_hash].obj == wahl.obj
    with pytest.raises(ValueError):
        store.submit_object(ObjectKind.ELECTION, bytes.fromhex("a1001801"))


def test_wahl_in_der_sicht(tmp_path) -> None:
    """Drei Gründer, eine Liste, zwei Stimmen für ANNA: ``ELECTED``, auch über die Route."""
    path = tmp_path / "s.sqlite"
    store = SqliteStore(path)
    v = Verein(store)
    wahl = v.wahl(v.epoch_1)
    liste, keys = v.liste(wahl, [v.anna, v.bruno, v.chris], "eins")
    v.stimme(keys[0], wahl, v.anna)
    v.stimme(keys[1], wahl, v.anna)
    eintrag = _ergebnis(store, v.scope, wahl)
    assert (eintrag.office, eintrag.label, eintrag.epoch) == ("vorstand", "Vorstand", v.epoch_1)
    assert eintrag.candidates == tuple(sorted([v.anna.pub, v.bruno.pub]))
    assert eintrag.result.lists == (liste.list_hash,)
    assert (eintrag.result.state, eintrag.result.elected) == (ElectionState.ELECTED, v.anna.pub)
    store.close()
    server = _start(path, lambda: NOW)
    try:
        status, body = _call(server, "GET", f"/wahlen/{v.scope.hex()}")
        assert status == 200
        (zeile,) = json.loads(body)
        assert zeile["election"] == wahl.election_hash.hex()
        assert zeile["result"]["state"] == "ELECTED"
        assert zeile["result"]["elected"] == v.anna.pub.hex()
        status, _body = _call(server, "GET", f"/wahlen/{'00' * 32}")
        assert status == 404
    finally:
        _stop(server)


def test_wahl_bleibt_nach_dem_wechsel_der_epoche(tmp_path) -> None:
    """Epoche 2 nimmt DORA auf; die Wahl in Epoche 1 zählt weiter mit drei (04 §9.5)."""
    store = SqliteStore(tmp_path / "s.sqlite")
    v = Verein(store)
    wahl = v.wahl(v.epoch_1)
    _liste, keys = v.liste(wahl, [v.anna, v.bruno, v.chris], "eins")
    v.stimme(keys[0], wahl, v.anna)
    v.stimme(keys[1], wahl, v.anna)
    epoch_2 = v.epoche_2(participants=sorted([*v.satzung["participants"], v.dora.pub]))
    assert _ergebnis(store, v.scope, wahl).result.state is ElectionState.ELECTED
    zweite = v.wahl(epoch_2, "Vorstand neu")
    _liste, keys = v.liste(zweite, [v.anna, v.bruno, v.chris, v.dora], "zwei")
    v.stimme(keys[0], zweite, v.anna)
    v.stimme(keys[1], zweite, v.anna)
    assert _ergebnis(store, v.scope, zweite).result.state is ElectionState.OPEN
    v.stimme(keys[2], zweite, v.anna)
    assert _ergebnis(store, v.scope, zweite).result.state is ElectionState.ELECTED


def test_epoche_ausserhalb_der_kette_ist_nicht_aufgeloest(tmp_path) -> None:
    """Eine Wahl auf eine Epoche, die nur ihr Hash nennt: eine Verfassung des Bestands mit ANNA
    allein, nie festgestellt. ``CONSTITUTION_UNAVAILABLE`` (04 §9.4)."""
    store = SqliteStore(tmp_path / "s.sqlite")
    v = Verein(store)
    allein = {**v.satzung, "participants": [v.anna.pub]}
    digest = store.submit_object(ObjectKind.CONSTITUTION, cbor_canon.encode(allein))
    erfunden = epoch_id(v.scope, 2, digest)
    wahl = v.wahl(erfunden)
    _liste, keys = v.liste(wahl, [v.anna], "allein")
    v.stimme(keys[0], wahl, v.anna)
    ergebnis = _ergebnis(store, v.scope, wahl).result
    assert ergebnis.state is ElectionState.UNEVALUABLE
    assert {f.kind for f in ergebnis.findings} == {GovernanceFinding.CONSTITUTION_UNAVAILABLE}


def test_policy_der_epoche_der_wahl(tmp_path) -> None:
    """Epoche 2 führt ``ballot@1`` nicht mehr als unwiderruflich; ein Widerruf einer Stimme der
    Wahl in Epoche 1 wirkt trotzdem nicht (04 §9.2, D675)."""
    store = SqliteStore(tmp_path / "s.sqlite")
    v = Verein(store)
    wahl = v.wahl(v.epoch_1)
    _liste, keys = v.liste(wahl, [v.anna, v.bruno, v.chris], "eins")
    erste = v.stimme(keys[0], wahl, v.anna)
    v.stimme(keys[1], wahl, v.anna)
    ohne = [p for p in v.satzung["irrevocable_predicates"] if p != "ballot@1"]
    v.epoche_2(irrevocable_predicates=ohne)
    v.t += 1
    store.add(keys[0].revoke(erste, t=v.t))
    ergebnis = _ergebnis(store, v.scope, wahl).result
    assert (ergebnis.state, ergebnis.elected) == (ElectionState.ELECTED, v.anna.pub)


def test_formwidrige_und_fremde_wahlen(tmp_path) -> None:
    """Formwidrig mit dem Scope: in der Sicht mit ``MALFORMED_ELECTION`` und ohne Felder. Ein
    fremder Scope oder kein Map: nicht in der Sicht."""
    store = SqliteStore(tmp_path / "s.sqlite")
    v = Verein(store)
    formwidrig = Election({0: v.scope, 1: v.epoch_1, 2: "vorstand", 3: [], 4: "leer"})
    store.submit_object(ObjectKind.ELECTION, cbor_canon.encode(formwidrig.obj))
    fremd = Election({**v.wahl(v.epoch_1).obj, 0: hashlib.sha256(b"fremd").digest()})
    store.submit_object(ObjectKind.ELECTION, cbor_canon.encode(fremd.obj))
    store.submit_object(ObjectKind.ELECTION, cbor_canon.encode([v.scope]))
    eintraege = {w.election: w for w in elections_view(store, v.scope, NOW)}
    assert fremd.election_hash not in eintraege
    assert len(eintraege) == 2
    eintrag = eintraege[formwidrig.election_hash]
    assert (eintrag.office, eintrag.label, eintrag.candidates, eintrag.epoch) == (
        None,
        None,
        (),
        None,
    )
    assert {f.kind for f in eintrag.result.findings} == {GovernanceFinding.MALFORMED_ELECTION}
