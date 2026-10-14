"""Was die Seite über eine Wahl wissen muss: angekündigt, wahlberechtigt, Teilnehmer, und die
Schritte einer Wurzel als Aufgaben (04 §9.3, 04 §9.4, D681)."""

from __future__ import annotations

import json

from tests.node.test_api import _call, _stop
from tests.node.test_wahl_ablauf import Lauf


def _aufgaben(lauf: Lauf, person) -> list[tuple[str, str]]:
    status, body = _call(lauf.server, "GET", f"/tasks/{person.pub.hex()}")
    assert status == 200
    return [
        (eintrag["art"], eintrag["election"])
        for eintrag in json.loads(body)
        if eintrag["art"] in {"ELECTION_JOIN", "ELECTION_VOTE"}
    ]


def _angelegt(lauf: Lauf, person) -> str:
    """Die Wahl über ``/intent``: das Objekt liegt im Bestand, ``election@1`` nicht."""
    status, body = lauf.call(
        "/intent",
        {
            "I": person.pub.hex(),
            "art": "election",
            "scope": lauf.scope,
            "office": "vorstand",
            "label": "Vorstand",
            "candidates": [lauf.bruno.pub.hex(), lauf.anna.pub.hex()],
        },
    )
    assert status == 200, body
    return json.loads(body)["effect"]["election"]


def test_angekuendigt(tmp_path) -> None:
    """Ohne ``election@1`` nicht angekündigt und ohne Aufgaben; eines von DORA, die nicht in ``P``
    steht, kündigt nicht an; eines von ANNA schon. ``participants`` ist ``P`` der Epoche der Wahl,
    ``members`` leer (D681)."""
    lauf = Lauf(tmp_path)
    try:
        wahl = _angelegt(lauf, lauf.anna)
        (zeile,) = lauf.wahlen()
        assert zeile["election"] == wahl
        assert zeile["announced"] is False
        assert _aufgaben(lauf, lauf.anna) == []
        lauf.ok(
            "/sim/intent",
            {
                "I": lauf.dora.pub.hex(),
                "art": "election",
                "scope": lauf.scope,
                "office": "vorstand",
                "label": "Vorstand",
                "candidates": [lauf.bruno.pub.hex(), lauf.anna.pub.hex()],
            },
        )
        (zeile,) = lauf.wahlen()
        assert zeile["announced"] is False
        assert lauf.wahl() == wahl
        (zeile,) = lauf.wahlen()
        assert zeile["announced"] is True
        assert zeile["participants"] == sorted(p.pub.hex() for p in (lauf.anna, lauf.bruno, lauf.chris))
        assert zeile["members"] == []
    finally:
        _stop(lauf.server)


def test_schritte_bis_gewaehlt(tmp_path) -> None:
    """Je Wurzel aus ``P`` erst ``ELECTION_JOIN``, nach Liste und Bestätigung ``ELECTION_VOTE``,
    nach der Stimme nichts; DORA nie; nach der Wahl niemand mehr (04 §9.4, D681)."""
    lauf = Lauf(tmp_path)
    try:
        wahl = lauf.wahl()
        for person in (lauf.anna, lauf.bruno, lauf.chris):
            assert _aufgaben(lauf, person) == [("ELECTION_JOIN", wahl)]
        assert _aufgaben(lauf, lauf.dora) == []
        lauf.liste(wahl, lauf.anna)
        assert _aufgaben(lauf, lauf.anna) == [("ELECTION_VOTE", wahl)]
        (zeile,) = lauf.wahlen()
        assert zeile["members"] == [lauf.anna.pub.hex()]
        status, _body = lauf.stimme(wahl, lauf.anna, lauf.bruno)
        assert status == 200
        assert _aufgaben(lauf, lauf.anna) == []
        assert _aufgaben(lauf, lauf.bruno) == [("ELECTION_JOIN", wahl)]
        lauf.liste(wahl, lauf.bruno)
        status, _body = lauf.stimme(wahl, lauf.bruno, lauf.bruno)
        assert status == 200
        (zeile,) = lauf.wahlen()
        assert zeile["result"]["state"] == "ELECTED"
        for person in (lauf.anna, lauf.bruno, lauf.chris, lauf.dora):
            assert _aufgaben(lauf, person) == []
    finally:
        _stop(lauf.server)


def test_liste_ohne_bestaetigung_des_mitglieds(tmp_path) -> None:
    """Nur ``/wahl/liste``, ohne die Bestätigung als Mitglied: die Liste trägt nicht, ANNA steht
    nicht unter ``members`` und hat weiter ``ELECTION_JOIN``, obwohl ihr Wahlschlüssel besteht
    (04 §9.3 Bedingung 3, D681)."""
    lauf = Lauf(tmp_path)
    try:
        wahl = lauf.wahl()
        lauf.ok("/wahl/liste", {"election": wahl, "I": lauf.anna.pub.hex()})
        (zeile,) = lauf.wahlen()
        assert zeile["members"] == []
        assert _aufgaben(lauf, lauf.anna) == [("ELECTION_JOIN", wahl)]
    finally:
        _stop(lauf.server)


def test_neuer_wahlgang(tmp_path) -> None:
    """Zu viert, Wahlgang 0 im Patt: jede Wurzel hat wieder ``ELECTION_VOTE``; nach einer Stimme
    in Wahlgang 1 hat CHRIS keine mehr (04 §9.4, D681)."""
    lauf = Lauf(tmp_path, vier=True)
    try:
        wahl = lauf.wahl()
        alle = (lauf.anna, lauf.bruno, lauf.chris, lauf.dora)
        for person in alle:
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
        assert zeile["result"]["current_round"] == 1
        for person in alle:
            assert _aufgaben(lauf, person) == [("ELECTION_VOTE", wahl)]
        status, _body = lauf.stimme(wahl, lauf.chris, lauf.anna)
        assert status == 200
        assert _aufgaben(lauf, lauf.chris) == []
    finally:
        _stop(lauf.server)
