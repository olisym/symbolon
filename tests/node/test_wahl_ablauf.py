"""Wahl im Knoten ohne Mischrunde: anlegen, Liste, bestätigen, abstimmen (04 §9, D678)."""

from __future__ import annotations

import json

from symbolon.node.store import SqliteStore
from tests.node.test_api import _call, _seed, _start, _stop
from tools.example_nucleus import people

FELDER = {"name": "Laufgruppe", "sitz": "Ort", "zweck": "Gemeinsam laufen"}
NOW = 1000


class Lauf:
    """Ein Knoten mit ANNA, BRUNO, CHRIS als simulierte Gründer und DORA ohne Mitgliedschaft."""

    def __init__(self, tmp_path, *, vier: bool = False) -> None:
        self.path = tmp_path / "s.sqlite"
        store = SqliteStore(self.path)
        self.anna, self.bruno, self.chris, self.dora = people()
        for person in (self.anna, self.bruno, self.chris, self.dora):
            store.add_sim_key(_seed(person))
        store.close()
        self.server = _start(self.path, lambda: NOW)
        status, body = self.call(
            "/gruenden",
            {
                "vorlage": "verein",
                "gruender": [
                    p.pub.hex()
                    for p in (self.anna, self.bruno, self.chris, self.dora)[: 4 if vier else 3]
                ],
                "felder": FELDER,
            },
        )
        assert status == 200
        self.scope = json.loads(body)["verein"]

    def call(self, path, payload, method="POST"):
        return _call(self.server, method, path, payload)

    def ok(self, path, payload):
        status, body = self.call(path, payload)
        assert status == 200, body
        return json.loads(body)

    def wahl(self) -> str:
        antwort = self.ok(
            "/sim/intent",
            {
                "I": self.anna.pub.hex(),
                "art": "election",
                "scope": self.scope,
                "office": "vorstand",
                "label": "Vorstand",
                "candidates": [self.bruno.pub.hex(), self.anna.pub.hex()],
            },
        )
        return antwort["effect"]["election"]

    def liste(self, wahl: str, person) -> dict:
        antwort = self.ok("/wahl/liste", {"election": wahl, "I": person.pub.hex()})
        self.ok("/sim/intent", {"I": person.pub.hex(), "art": "ballot-ack", "list": antwort["list"]})
        return antwort

    def stimme(self, wahl: str, person, kandidat, **mehr):
        return self.call(
            "/wahl/stimme",
            {"election": wahl, "I": person.pub.hex(), "candidate": kandidat.pub.hex(), **mehr},
        )

    def wahlen(self) -> list:
        status, body = _call(self.server, "GET", f"/wahlen/{self.scope}")
        assert status == 200
        return json.loads(body)


def test_ablauf_bis_gewaehlt(tmp_path) -> None:
    """Drei Listen mit je einem Mitglied, zwei Stimmen für ANNA: ``ELECTED`` (04 §9.4)."""
    lauf = Lauf(tmp_path)
    try:
        wahl = lauf.wahl()
        listen = [lauf.liste(wahl, p)["list"] for p in (lauf.anna, lauf.bruno, lauf.chris)]
        status, body = lauf.stimme(wahl, lauf.anna, lauf.anna)
        assert status == 200
        assert json.loads(body)["round"] == 0
        (zeile,) = lauf.wahlen()
        assert zeile["result"]["state"] == "OPEN"
        assert sorted(zeile["result"]["lists"]) == sorted(listen)
        status, _body = lauf.stimme(wahl, lauf.bruno, lauf.anna)
        assert status == 200
        (zeile,) = lauf.wahlen()
        assert zeile["candidates"] == sorted([lauf.anna.pub.hex(), lauf.bruno.pub.hex()])
        assert (zeile["result"]["state"], zeile["result"]["elected"]) == (
            "ELECTED",
            lauf.anna.pub.hex(),
        )
    finally:
        _stop(lauf.server)


def test_liste_wiederholt(tmp_path) -> None:
    """Zweimal ``/wahl/liste``: dieselbe Liste und derselbe Schlüssel, eine Bestätigung des
    Schlüssels (D678 Beschluss 3)."""
    lauf = Lauf(tmp_path)
    try:
        wahl = lauf.wahl()
        erste = lauf.ok("/wahl/liste", {"election": wahl, "I": lauf.anna.pub.hex()})
        zweite = lauf.ok("/wahl/liste", {"election": wahl, "I": lauf.anna.pub.hex()})
        assert erste == zweite
        store = SqliteStore(lauf.path)
        try:
            acks = [
                c
                for c in store.all_claims()
                if c.I.hex() == erste["key"] and c.p.endswith("/ballot-ack@1")
            ]
        finally:
            store.close()
        assert len(acks) == 1
    finally:
        _stop(lauf.server)


def test_abweisungen(tmp_path) -> None:
    """Was der Knoten abweist, und dass danach nichts geschrieben ist (D678 Beschluss 3 und 4)."""
    lauf = Lauf(tmp_path)
    try:
        wahl = lauf.wahl()
        status, body = lauf.call("/wahl/liste", {"election": wahl, "I": lauf.dora.pub.hex()})
        assert (status, json.loads(body)) == (400, "NOT_ELIGIBLE")
        status, body = lauf.stimme(wahl, lauf.anna, lauf.anna)
        assert (status, json.loads(body)) == (400, "NO_BALLOT_KEY")
        status, body = lauf.call("/wahl/liste", {"election": "00" * 32, "I": lauf.anna.pub.hex()})
        assert (status, json.loads(body)) == (400, "UNKNOWN_ELECTION")
        lauf.liste(wahl, lauf.anna)
        status, body = lauf.stimme(wahl, lauf.anna, lauf.chris)
        assert (status, json.loads(body)) == (400, "UNKNOWN_CANDIDATE")
        status, _body = lauf.stimme(wahl, lauf.anna, lauf.bruno)
        assert status == 200
        status, body = lauf.stimme(wahl, lauf.anna, lauf.anna)
        assert (status, json.loads(body)) == (400, "ALREADY_VOTED")
        status, body = lauf.stimme(wahl, lauf.anna, lauf.anna, round=1)
        assert status == 200
        assert json.loads(body)["round"] == 1
        status, body = lauf.call(
            "/sim/intent",
            {
                "I": lauf.anna.pub.hex(),
                "art": "election",
                "scope": lauf.scope,
                "office": "vorstand",
                "label": "doppelt",
                "candidates": [lauf.anna.pub.hex(), lauf.anna.pub.hex()],
            },
        )
        assert (status, json.loads(body)) == (400, "INVALID_ELECTION")
        status, body = lauf.call(
            "/sim/intent",
            {"I": lauf.anna.pub.hex(), "art": "ballot-ack", "list": "00" * 32},
        )
        assert (status, json.loads(body)) == (400, "UNKNOWN_LIST")
        (zeile,) = lauf.wahlen()
        assert zeile["result"]["state"] == "OPEN"
        assert not any(f["kind"] == "AMBIGUOUS_BALLOT" for f in zeile["result"]["findings"])
    finally:
        _stop(lauf.server)


def test_schluessel_bleibt_im_knoten(tmp_path) -> None:
    """Der Wahlschlüssel ist nach einem Neustart des Knotens derselbe (D678 Beschluss 2)."""
    lauf = Lauf(tmp_path)
    try:
        wahl = lauf.wahl()
        erste = lauf.liste(wahl, lauf.anna)
    finally:
        _stop(lauf.server)
    lauf.server = _start(lauf.path, lambda: NOW)
    try:
        zweite = lauf.ok("/wahl/liste", {"election": wahl, "I": lauf.anna.pub.hex()})
        assert zweite == erste
        status, _body = lauf.stimme(wahl, lauf.anna, lauf.anna)
        assert status == 200
    finally:
        _stop(lauf.server)


def test_ohne_wahlgang_der_geltende(tmp_path) -> None:
    """Zu viert, je zwei für ANNA und BRUNO: Wahlgang 0 steht im Patt, die nächste Stimme ohne
    ``round`` geht in Wahlgang 1 (04 §9.4, D678 Beschluss 4)."""
    lauf = Lauf(tmp_path, vier=True)
    try:
        wahl = lauf.wahl()
        for person in (lauf.anna, lauf.bruno, lauf.chris, lauf.dora):
            lauf.liste(wahl, person)
        for person, kandidat in (
            (lauf.anna, lauf.anna),
            (lauf.bruno, lauf.anna),
            (lauf.chris, lauf.bruno),
            (lauf.dora, lauf.bruno),
        ):
            status, _body = lauf.stimme(wahl, person, kandidat)
            assert status == 200
        (zeile,) = lauf.wahlen()
        assert (zeile["result"]["state"], zeile["result"]["current_round"]) == ("OPEN", 1)
        status, body = lauf.stimme(wahl, lauf.chris, lauf.anna)
        assert status == 200
        assert json.loads(body)["round"] == 1
    finally:
        _stop(lauf.server)
