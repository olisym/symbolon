"""Der Knoten im neuen Wahlgang: Vorschläge, Aufgaben, Zeugen je Wurzel und das Bild (D603)."""

from __future__ import annotations

import json

from symbolon.governance.objects import ABSENT, Proposal, ballot_of
from symbolon.node import view as view_modul
from symbolon.node.store import SqliteStore
from symbolon.node.view import _decide_proposal, _known, scope_view
from tests.node.test_abgleich import _url
from tests.node.test_api import _call, _stop
from tests.node.test_personen import _ausgang
from tests.node.test_spaltung import _arten, _lage
from tests.node.test_versehen import _start
from tools.netz import GERAETE_GERAETE, durchgang, gruppen
from tools.personen import ANTRAG_WAHLGANG, SPALTUNG, WAHLGANG, takt_spaltung
from tools.verein import build
from tools.verein_node import anlegen

_NOW = 1000
_NACHLAUF = 2


def test_view_reicht_die_verfassungen(tmp_path, monkeypatch) -> None:
    """Die Auszählung im Knoten kennt jede Verfassung des Bestands (04 §4.7, D601 Befund 2)."""
    datei = tmp_path / "verein.sqlite"
    anlegen(datei)
    store = SqliteStore(datei)
    scope = build().ex.N_gov
    sicht = scope_view(store, scope, _NOW)
    gesehen: list[dict] = []
    echt = view_modul.decide

    def decide(*args, **kwargs):
        gesehen.append(kwargs)
        return echt(*args, **kwargs)

    monkeypatch.setattr(view_modul, "decide", decide)
    vorschlaege = _known(store)
    vorschlag = next(p for p in vorschlaege.values() if isinstance(p, Proposal))
    _decide_proposal(
        store,
        sicht.state,
        store.all_genesis()[scope],
        vorschlag,
        store.all_constitutions(),
        vorschlaege,
        _NOW,
    )
    assert gesehen[-1]["known_constitutions"] == store.all_constitutions()


def test_bild_wahlgang(tmp_path) -> None:
    """Nach der Vereinigung gilt Wahlgang 1; Annas neuer Antrag steht darin und gilt überall."""
    ausgang = _ausgang(tmp_path)
    jetzt = {"t": _NOW}
    knoten = []
    for name, datei, personen in GERAETE_GERAETE:
        anlegen(tmp_path / datei, personen, geraete=True)
        knoten.append(_start(tmp_path / datei, name, lambda: jetzt["t"]))
    try:
        urls = [_url(server) for server in knoten]
        namen = [name for name, _datei, _personen in GERAETE_GERAETE]
        anna = knoten[namen.index("Annas Gerät")]
        zeilen: dict[int, list[str]] = {}
        teile = gruppen(GERAETE_GERAETE, False)
        for nummer in range(WAHLGANG):
            jetzt["t"] = _NOW + nummer
            if nummer in SPALTUNG:
                teile = gruppen(GERAETE_GERAETE, nummer == SPALTUNG[0])
            zeilen[nummer] = takt_spaltung(urls, nummer, GERAETE_GERAETE, wahlgang=True)
            durchgang(urls, teile)
        assert {_lage(server)[:2] for server in knoten} == {(ausgang, None)}
        # Wahlgang 0 im Patt: kein Vorschlag aus ihm ist eine Aufgabe.
        for person in ("ANNA", "CHRIS"):
            assert "VOTE" not in _arten(anna, person)
        for nummer in range(WAHLGANG, WAHLGANG + 3 + _NACHLAUF):
            jetzt["t"] = _NOW + nummer
            zeilen[nummer] = takt_spaltung(urls, nummer, GERAETE_GERAETE, wahlgang=True)
            durchgang(urls, teile)
        alle = [z for nummer in sorted(zeilen) for z in zeilen[nummer]]
        assert not [z for z in alle if "abgewiesen" in z], alle
        assert [z for z in zeilen[WAHLGANG] if "beantragt" in z] == [
            f"Takt {WAHLGANG}, Annas Gerät: ANNA beantragt den Beitrag"
        ], zeilen[WAHLGANG]
        assert [z for z in zeilen[SPALTUNG[1]]] == []
        fest = [z for z in alle if z.endswith("stellt den Beschluss fest")]
        assert fest[-1] == f"Takt {WAHLGANG + 2}, Annas Gerät: ANNA stellt den Beschluss fest"
        text = ANTRAG_WAHLGANG["set"]["text"]
        assert [_lage(server) for server in knoten] == [(ausgang + 1, text, set())] * len(knoten)
        store = SqliteStore(tmp_path / "anna.sqlite")
        vorschlaege = [p for p in _known(store).values() if isinstance(p, Proposal)]
        (neu,) = [p for p in vorschlaege if ballot_of(p) != 0]
        assert neu.ballot == 1
        dieselbe = [p for p in vorschlaege if p.predecessor == neu.predecessor]
        alte = [p for p in dieselbe if p is not neu]
        # Die Anträge aus Takt 2 und was der Verein vorher kannte: alle ohne Feld 4.
        assert len(alte) >= 2 and all(p.ballot is ABSENT for p in alte), alte
    finally:
        for server in knoten:
            _stop(server)


def _antraege(server) -> list[dict]:
    status, body = _call(server, "GET", f"/proposals/{build().ex.N_gov.hex()}")
    assert status == 200, body
    return json.loads(body)


def test_antraege_laufend(tmp_path) -> None:
    """Vereint stehen die Anträge der Spaltung ausserhalb des geltenden Wahlgangs; Annas neuer
    Antrag steht darin (04 §4.7, D605 Beschluss 1)."""
    jetzt = {"t": _NOW}
    knoten = []
    for name, datei, personen in GERAETE_GERAETE:
        anlegen(tmp_path / datei, personen, geraete=True)
        knoten.append(_start(tmp_path / datei, name, lambda: jetzt["t"]))
    try:
        urls = [_url(server) for server in knoten]
        anna = knoten[[name for name, _d, _p in GERAETE_GERAETE].index("Annas Gerät")]
        teile = gruppen(GERAETE_GERAETE, False)
        for nummer in range(WAHLGANG + 1):
            jetzt["t"] = _NOW + nummer
            if nummer in SPALTUNG:
                teile = gruppen(GERAETE_GERAETE, nummer == SPALTUNG[0])
            if nummer == WAHLGANG:
                alt = _antraege(anna)
                assert len(alt) == 2, alt
                assert {(a["kind"], a["ballot"], a["current"]) for a in alt} == {("proposal", 0, False)}
            takt_spaltung(urls, nummer, GERAETE_GERAETE, wahlgang=True)
            durchgang(urls, teile)
        neu = [a for a in _antraege(anna) if a["proposal"] not in {b["proposal"] for b in alt}]
        assert [(a["ballot"], a["current"]) for a in neu] == [(1, True)], neu
    finally:
        for server in knoten:
            _stop(server)
