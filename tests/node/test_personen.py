"""Personen mit eigenem Verhalten, Stufe (a): Regeln und Lauf (D521 Beschluss 2 und 3)."""

from __future__ import annotations

import json

from symbolon import cbor_canon
from symbolon.node.api import _TASK_DETAIL_FIELD
from tests.node.test_abgleich import _url
from tests.node.test_api import _call, _stop
from tests.node.test_netz import _start, _stand
from tools.netz import GERAETE, durchgang
from tools.personen import ANTRAG_TAKT, absichten, takt
from tools.verein import build
from tools.verein_node import anlegen

_GRENZE = 20
_ZWEITGERAET = "Brunos Zweitgerät"


def _geraete(tmp_path) -> list:
    """Jedes Gerät aus GERAETE im Prozess, mit fester Uhr (D518 Beschluss 1)."""
    knoten = []
    for name, datei, personen in GERAETE:
        anlegen(tmp_path / datei, personen)
        knoten.append(_start(tmp_path / datei, name))
    return knoten


def _lauf(urls: list[str]) -> list[str]:
    """Takte ab 0, je takt und durchgang, bis zum ersten stillen Takt nach ANTRAG_TAKT (D521 Beschluss 3)."""
    zeilen: list[str] = []
    gemeldet: set[tuple[str, str]] = set()
    for nummer in range(_GRENZE):
        neu = takt(urls, nummer, gemeldet)
        zeilen += neu
        verteilt = durchgang(urls)
        if nummer > ANTRAG_TAKT and not neu and not verteilt:
            return zeilen
    raise AssertionError(f"nach {_GRENZE} Takten nicht still: {zeilen}")


def _epoche(server, scope: bytes) -> int:
    status, body = _call(server, "GET", f"/scopes/{scope.hex()}")
    assert status == 200, body
    return json.loads(body)["state"]["epoch"]["index"]


def _forks(server) -> list:
    status, body = _call(server, "GET", "/forks")
    assert status == 200, body
    return json.loads(body)


def _ausgang(tmp_path) -> int:
    """Die Epoche des Vereins-Scopes in einem frisch angelegten Bestand, gelesen."""
    pfad = tmp_path / "frisch.sqlite"
    anlegen(pfad)
    server = _start(pfad)
    try:
        return _epoche(server, build().ex.N_gov)
    finally:
        _stop(server)


def test_regeln() -> None:
    """Jede Art auf jedem Gerät für jede seiner Personen, Rumpf für Rumpf (D521 Beschluss 2)."""
    world = build()
    scope = "aa" * 32
    for geraet, _datei, personen in GERAETE:
        for person in sorted(personen):
            I = getattr(world, person.lower()).pub.hex()
            for art, feld in _TASK_DETAIL_FIELD.items():
                detail = "bb" * 32
                aufgabe = {"scope": scope, "art": art, feld: detail}
                erhalten = absichten(geraet, person, I, [aufgabe])
                zweit = geraet == _ZWEITGERAET
                if art == "CONFIRM_RULES":
                    soll = (
                        []
                        if zweit
                        else [
                            {
                                "I": I,
                                "art": "accept-rules",
                                "scope": scope,
                                "constitution": detail,
                            }
                        ]
                    )
                elif art == "VOTE":
                    choice = "no" if zweit else "yes"
                    soll = [{"I": I, "art": "vote", "proposal": detail, "choice": choice}]
                elif art == "RATIFY":
                    soll = (
                        [{"I": I, "art": "ratify", "proposal": detail}]
                        if not zweit and person == "ANNA"
                        else []
                    )
                elif art == "RECEIPT":
                    soll = [] if zweit else [{"I": I, "art": "receipt", "obligation": detail}]
                elif art == "CONTRIBUTION_OPEN":
                    soll = []
                else:
                    raise AssertionError(f"Art ohne Regel: {art}")
                assert erhalten == soll, (geraet, person, art)


def test_lauf(tmp_path) -> None:
    """Ohne Trennung: Brunos Gabel auf jedem Gerät, Epoche um eins höher (D521 Golden Numbers)."""
    ausgang = _ausgang(tmp_path)
    world = build()
    knoten = _geraete(tmp_path)
    try:
        urls = [_url(server) for server in knoten]
        zeilen = _lauf(urls)
        staende = {_stand(server) for server in knoten}
        assert len(staende) == 1
        for server in knoten:
            forks = _forks(server)
            assert len(forks) == 1, forks
            assert forks[0]["I"] == world.bruno.pub.hex()
            werte = set()
            for cid, _scope in forks[0]["claims"]:
                status, body = _call(server, "GET", f"/claims/{cid}")
                assert status == 200, body
                werte.add(cbor_canon.decode(bytes.fromhex(json.loads(body)["v"]))[0])
            assert werte == {0, 1}
            assert _epoche(server, world.ex.N_gov) == ausgang + 1
        meldungen = [zeile for zeile in zeilen if "hat sich widersprochen" in zeile]
        assert len(meldungen) == 1, zeilen
        assert meldungen[0].split(":")[0].endswith(", Brunos Gerät"), zeilen
        assert not [zeile for zeile in zeilen if "abgewiesen" in zeile], zeilen
    finally:
        for server in knoten:
            _stop(server)


def test_zweitgeraet_getrennt(tmp_path) -> None:
    """Brunos Zweitgerät vor dem ersten Takt getrennt: keine Gabel (D521 Golden Numbers)."""
    ausgang = _ausgang(tmp_path)
    world = build()
    knoten = _geraete(tmp_path)
    try:
        urls = [_url(server) for server in knoten]
        index = [name for name, _datei, _personen in GERAETE].index(_ZWEITGERAET)
        status, _body = _call(knoten[index], "POST", "/getrennt", {"getrennt": True})
        assert status == 200
        zeilen = _lauf(urls)
        verbunden = [server for position, server in enumerate(knoten) if position != index]
        assert len({_stand(server) for server in verbunden}) == 1
        for server in verbunden:
            assert _forks(server) == []
            assert _epoche(server, world.ex.N_gov) == ausgang + 1
        assert not [zeile for zeile in zeilen if "hat sich widersprochen" in zeile], zeilen
        assert not [zeile for zeile in zeilen if "abgewiesen" in zeile], zeilen
    finally:
        for server in knoten:
            _stop(server)
