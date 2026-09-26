"""Personen mit eigenem Verhalten, Stufe (b): Doras Versehen neben Brunos Lüge (D523)."""

from __future__ import annotations

import json
import threading
from collections.abc import Callable
from http.server import HTTPServer

from symbolon import cbor_canon
from symbolon.node.api import serve
from tests.node.test_abgleich import _url
from tests.node.test_api import _call, _stop
from tests.node.test_netz import _stand
from tests.node.test_personen import _ausgang, _epoche, _forks
from tools.netz import GERAETE_VERSEHEN, durchgang
from tools.personen import ANTRAG_TAKT, TRENNUNG, verzoegert, takt
from tools.verein import build
from tools.verein_node import anlegen

_GRENZE = 20
_NOW = 1000


def _start(path, geraet: str, uhr: Callable[[], int]) -> HTTPServer:
    """Wie _start in test_netz, mit der Uhr als Argument (D523 Befunde)."""
    ready = threading.Event()
    holder: dict[str, HTTPServer] = {}

    def bound(server: HTTPServer) -> None:
        holder["server"] = server
        ready.set()

    thread = threading.Thread(
        target=serve,
        args=(path,),
        kwargs={"port": 0, "clock": uhr, "bound": bound, "geraet": geraet},
        daemon=True,
    )
    thread.start()
    ready.wait()
    return holder["server"]


def _geraete(tmp_path, uhr: Callable[[], int]) -> list:
    """Jedes Gerät aus GERAETE_VERSEHEN im Prozess, mit der Uhr des Tests (D523 Beschluss 1)."""
    knoten = []
    for name, datei, personen in GERAETE_VERSEHEN:
        anlegen(tmp_path / datei, personen)
        knoten.append(_start(tmp_path / datei, name, uhr))
    return knoten


def _lauf(urls: list[str], jetzt: dict[str, int], schritt: int) -> list[str]:
    """Takte ab 0 bis zum ersten stillen nach Antrag und Trennung (D523 Beschluss 2 und 3).

    Die Uhr steht je Takt auf ``1000 + schritt * nummer``.
    """
    zeilen: list[str] = []
    gemeldet: set[tuple[str, str]] = set()
    gesehen: dict[tuple[str, str], list[dict]] = {}
    for nummer in range(_GRENZE):
        jetzt["t"] = _NOW + schritt * nummer
        neu = takt(urls, nummer, gemeldet, GERAETE_VERSEHEN, gesehen)
        zeilen += neu
        verteilt = durchgang(urls)
        if nummer > max(ANTRAG_TAKT, *TRENNUNG) and not neu and not verteilt:
            return zeilen
    raise AssertionError(f"nach {_GRENZE} Takten nicht still: {zeilen}")


def _stimmen(server, gruppe: dict) -> list[int]:
    """Die Werte aus v der Claims einer Gabelgruppe, sortiert (D523 Golden Numbers)."""
    werte = []
    for cid, _scope in gruppe["claims"]:
        status, body = _call(server, "GET", f"/claims/{cid}")
        assert status == 200, body
        werte.append(cbor_canon.decode(bytes.fromhex(json.loads(body)["v"]))[0])
    return sorted(werte)


def test_verzoegert() -> None:
    """Nur was schon im vorigen Takt anstand, gleich Rumpf für Rumpf (D523 Beschluss 2)."""
    I = "aa" * 32
    quittung = {"I": I, "art": "receipt", "obligation": "bb" * 32}
    alt = {"I": I, "art": "vote", "proposal": "cc" * 32, "choice": "yes"}
    neu = {"I": I, "art": "vote", "proposal": "dd" * 32, "choice": "yes"}
    assert verzoegert([neu, quittung], [alt, quittung]) == [quittung]
    assert verzoegert([neu, quittung], []) == []
    assert verzoegert([], [alt, quittung]) == []


def test_versehen(tmp_path) -> None:
    """Uhr +1 je Takt: Gabeln BRUNO und DORA, der Beschluss fällt (D523 Golden Numbers)."""
    ausgang = _ausgang(tmp_path)
    world = build()
    jetzt = {"t": _NOW}
    knoten = _geraete(tmp_path, lambda: jetzt["t"])
    try:
        urls = [_url(server) for server in knoten]
        zeilen = _lauf(urls, jetzt, 1)
        assert len({_stand(server) for server in knoten}) == 1
        soll = {world.bruno.pub.hex(): [0, 1], world.dora.pub.hex(): [1, 1]}
        for server in knoten:
            forks = _forks(server)
            assert len(forks) == 2, forks
            assert {gruppe["I"]: _stimmen(server, gruppe) for gruppe in forks} == soll
            assert _epoche(server, world.ex.N_gov) == ausgang
        assert len([zeile for zeile in zeilen if "stellt den Beschluss fest" in zeile]) == 1, zeilen
        assert not [zeile for zeile in zeilen if "abgewiesen" in zeile], zeilen
    finally:
        for server in knoten:
            _stop(server)


def test_versehen_feste_uhr(tmp_path) -> None:
    """Feste Uhr: Doras Claims gleich, nur Brunos Gabel, Epoche höher (D523 Befund 1)."""
    ausgang = _ausgang(tmp_path)
    world = build()
    jetzt = {"t": _NOW}
    knoten = _geraete(tmp_path, lambda: jetzt["t"])
    try:
        urls = [_url(server) for server in knoten]
        _lauf(urls, jetzt, 0)
        assert len({_stand(server) for server in knoten}) == 1
        for server in knoten:
            forks = _forks(server)
            assert len(forks) == 1, forks
            assert forks[0]["I"] == world.bruno.pub.hex()
            assert _epoche(server, world.ex.N_gov) == ausgang + 1
    finally:
        for server in knoten:
            _stop(server)
