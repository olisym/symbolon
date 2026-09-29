"""Die Spaltung: zwei Gruppen entscheiden getrennt und kommen wieder zusammen (D594)."""

from __future__ import annotations

import itertools
import json
import threading
import time
from types import SimpleNamespace

from symbolon.bote.kern import sperren_lesen
from tests.node.test_abgleich import _knoten as _leer, _url
from tests.node.test_api import _call, _start as _start_api, _stop
from tests.node.test_personen import _ausgang
from tests.node.test_versehen import _start
from tools import netz
from tools.netz import (
    GERAETE_GERAETE,
    OST,
    WEST,
    durchgang,
    gesperrt_gemeldet,
    gruppen,
    ruhe,
    sperrdateien,
)
from tools.personen import ANTRAG, ANTRAG_OST, SPALTUNG, takt_spaltung
from tools.verein import build
from tools.verein_node import anlegen

_NOW = 1000
_NACHLAUF = 3


def test_gruppen() -> None:
    """West und Ost als Stellen in GERAETE_GERAETE, zusammen jedes Gerät einmal (D594 B. 1)."""
    namen = [name for name, _datei, _personen in GERAETE_GERAETE]
    west, ost = gruppen(GERAETE_GERAETE, True)
    assert [namen[i] for i in west] == list(WEST)
    assert [namen[i] for i in ost] == list(OST)
    assert sorted(west + ost) == list(range(len(namen)))
    assert gruppen(GERAETE_GERAETE, False) == [list(range(len(namen)))]


def test_durchgang_gruppen(monkeypatch) -> None:
    """Nur Paare innerhalb einer Gruppe; ohne Gruppen jedes Paar (D594 Beschluss 3)."""
    paare: list[tuple[str, str]] = []

    def runde(url_a, url_b):
        paare.append((url_a, url_b))
        return SimpleNamespace(eingeliefert=1)

    monkeypatch.setattr(netz, "runde", runde)
    urls = [f"u{i}" for i in range(len(GERAETE_GERAETE))]
    teile = gruppen(GERAETE_GERAETE, True)
    soll = [(urls[a], urls[b]) for teil in teile for a, b in itertools.combinations(teil, 2)]
    assert durchgang(urls, teile) == len(soll)
    assert paare == soll
    paare.clear()
    assert durchgang(urls) == len(list(itertools.combinations(urls, 2)))
    assert paare == list(itertools.combinations(urls, 2))


def test_sperrdateien(tmp_path) -> None:
    """Je Gerät die Adressen ausserhalb seiner Gruppe; vereint keine (D594 Beschluss 3)."""
    adressen = [f"{i:02x}" * 16 for i in range(len(GERAETE_GERAETE))]
    teile = gruppen(GERAETE_GERAETE, True)
    sperrdateien(tmp_path, GERAETE_GERAETE, adressen, teile)
    for teil in teile:
        for index in teil:
            datei = tmp_path / "sperren" / f"{GERAETE_GERAETE[index][1]}.txt"
            fremde = {bytes.fromhex(adressen[j]) for j in range(len(adressen)) if j not in teil}
            assert sperren_lesen(datei) == fremde
    sperrdateien(tmp_path, GERAETE_GERAETE, adressen, gruppen(GERAETE_GERAETE, False))
    for _name, datei, _personen in GERAETE_GERAETE:
        assert sperren_lesen(tmp_path / "sperren" / f"{datei}.txt") == frozenset()


def test_gesperrt_gemeldet() -> None:
    """Wahr, sobald jeder Bote die erwartete Zahl meldet; nach der Frist falsch (D594 B. 3)."""
    stand: dict[str, int | None] = {"A": 0, "B": 0}
    erwartet = {"A": 1, "B": 1}

    def melden():
        time.sleep(0.2)
        stand["A"] = 1
        time.sleep(0.2)
        stand["B"] = 1

    faden = threading.Thread(target=melden)
    faden.start()
    assert gesperrt_gemeldet(stand, erwartet, frist=5.0) is True
    faden.join()
    stand["B"] = None
    assert gesperrt_gemeldet(stand, erwartet, frist=0.3) is False


def test_ruhe_gruppen(tmp_path) -> None:
    """Gleicher Stand je Gruppe genügt; über die Grenze zählt kein Unterschied (D594 B. 3)."""
    path_a = tmp_path / "a.sqlite"
    anlegen(path_a)
    a = _start_api(path_a, lambda: _NOW)
    b = _leer(tmp_path / "b.sqlite")
    c = _leer(tmp_path / "c.sqlite")
    try:
        urls = [_url(a), _url(b), _url(c)]
        assert ruhe(urls, frist=0.5) is None
        assert ruhe(urls, frist=0.5, gruppen=[[0], [1, 2]]) is not None
        assert ruhe(urls, frist=0.5, gruppen=[[0, 1], [2]]) is None
    finally:
        _stop(a)
        _stop(b)
        _stop(c)


def _scope(server) -> dict:
    status, body = _call(server, "GET", f"/scopes/{build().ex.N_gov.hex()}")
    assert status == 200, body
    return json.loads(body)


def _lage(server) -> tuple[int, str | None, set[str]]:
    """Fassung, Beitrag und die Arten der Vermerke der Kette auf einem Gerät."""
    ansicht = _scope(server)
    zustand = ansicht["state"]
    return (
        zustand["epoch"]["index"],
        ansicht["stand"]["stand_obj"].get("beitrag"),
        {vermerk["kind"] for vermerk in zustand["epoch_findings"]},
    )


def _bestand(server) -> tuple[int, int]:
    status, body = _call(server, "GET", "/peer/bestand")
    assert status == 200, body
    bestand = json.loads(body)
    return len(bestand["claims"]), len(bestand["objects"])


def _arten(server, person: str) -> list[str]:
    """Die Arten der Aufgaben einer Person auf einem Gerät."""
    status, body = _call(server, "GET", "/names")
    assert status == 200, body
    schluessel = {eintrag["name"]: eintrag["I"] for eintrag in json.loads(body)}[person]
    status, body = _call(server, "GET", f"/tasks/{schluessel}")
    assert status == 200, body
    return [aufgabe["art"] for aufgabe in json.loads(body)]


def test_bild_spaltung(tmp_path) -> None:
    """Jede Seite stellt ihren Beitrag fest; vereint fallen beide, und niemand handelt mehr (D594)."""
    ausgang = _ausgang(tmp_path)
    jetzt = {"t": _NOW}
    knoten = []
    for name, datei, personen in GERAETE_GERAETE:
        anlegen(tmp_path / datei, personen, geraete=True)
        knoten.append(_start(tmp_path / datei, name, lambda: jetzt["t"]))
    try:
        urls = [_url(server) for server in knoten]
        namen = [name for name, _datei, _personen in GERAETE_GERAETE]
        zeilen: list[str] = []
        teile = gruppen(GERAETE_GERAETE, False)
        for nummer in range(SPALTUNG[1]):
            jetzt["t"] = _NOW + nummer
            if nummer == SPALTUNG[0]:
                teile = gruppen(GERAETE_GERAETE, True)
            zeilen += takt_spaltung(urls, nummer, GERAETE_GERAETE)
            durchgang(urls, teile)
        assert not [z for z in zeilen if "abgewiesen" in z], zeilen
        feststellungen = sorted(
            z.split(", ", 1)[1] for z in zeilen if z.endswith("stellt den Beschluss fest")
        )
        assert feststellungen == [
            "Annas Gerät: ANNA stellt den Beschluss fest",
            "Chris' Gerät: CHRIS stellt den Beschluss fest",
        ], zeilen
        for name, server in zip(namen, knoten):
            text = (ANTRAG if name in WEST else ANTRAG_OST)["set"]["text"]
            assert _lage(server) == (ausgang + 1, text, set()), name
        teile = gruppen(GERAETE_GERAETE, False)
        jetzt["t"] = _NOW + SPALTUNG[1]
        durchgang(urls, teile)
        # Vereint steht Wahlgang 0 im Patt; Chris' Antrag ist keine Aufgabe mehr (04 §4.7, D603
        # Beschluss 3). Niemand handelt.
        assert "VOTE" not in _arten(knoten[namen.index("Annas Gerät")], "ANNA")
        assert takt_spaltung(urls, SPALTUNG[1], GERAETE_GERAETE) == []
        staende = set()
        for name, server in zip(namen, knoten):
            fassung, beitrag, vermerke = _lage(server)
            assert (fassung, beitrag) == (ausgang, None), name
            assert "CONFLICTING_APPROVAL" in vermerke, (name, vermerke)
            staende.add(_bestand(server))
        assert len(staende) == 1
        for nummer in range(SPALTUNG[1] + 1, SPALTUNG[1] + 1 + _NACHLAUF):
            jetzt["t"] = _NOW + nummer
            assert takt_spaltung(urls, nummer, GERAETE_GERAETE) == []
            assert durchgang(urls, teile) == 0
        assert {_bestand(server) for server in knoten} == staende
    finally:
        for server in knoten:
            _stop(server)
