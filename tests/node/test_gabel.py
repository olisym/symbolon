"""Brunos Gabelung über die Schnittstelle (D488 Befund und Beschluss 2, szenario-verein §5.2)."""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer

import pytest

from symbolon.node.api import serve
from tools.verein import BEITRAG, build
from tools.verein_gabel import GabelFehler, gabeln
from tools.verein_node import anlegen

NOW = 1000


def _start(path) -> HTTPServer:
    ready = threading.Event()
    holder: dict[str, HTTPServer] = {}

    def bound(server: HTTPServer) -> None:
        holder["server"] = server
        ready.set()

    thread = threading.Thread(
        target=serve,
        args=(path,),
        kwargs={"port": 0, "clock": lambda: NOW, "bound": bound},
        daemon=True,
    )
    thread.start()
    ready.wait()
    return holder["server"]


def _base(server: HTTPServer) -> str:
    host, port = server.server_address
    return f"http://{host}:{port}"


def _call(server: HTTPServer, method: str, path: str, payload: object = None):
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(_base(server) + path, data=data, method=method)
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def _get(server: HTTPServer, path: str):
    status, body = _call(server, "GET", path)
    assert status == 200, body
    return json.loads(body)


def _propose(server: HTTPServer, who: bytes, scope: bytes, text: str) -> str:
    status, body = _call(
        server,
        "POST",
        "/sim/intent",
        {
            "I": who.hex(),
            "art": "propose",
            "scope": scope.hex(),
            "change": {"set": {"field": "beitrag", "text": text}},
        },
    )
    assert status == 200, body
    return json.loads(body)["claim_id"]


def _spitze(server: HTTPServer, who: bytes) -> str:
    """Vorgeschlagenes h_prev für who, ohne etwas einzuliefern (D476 Beschluss 3)."""
    status, body = _call(server, "POST", "/prepare", {"I": who.hex(), "p": "x", "J": [1, who.hex()]})
    assert status == 200, body
    return json.loads(body)["h_prev"]


def _kanten(server: HTTPServer, scope: bytes) -> int:
    view = _get(server, f"/scopes/{scope.hex()}")
    return len(view["vereinsleben"]["derivation"]["bfs"]["edges"])


def test_gabelung(tmp_path) -> None:
    """Eine Gruppe mit BRUNO und den zwei claim_id; keine Stimme gezählt; weniger Kanten

    (D488 Befund, szenario-verein §5.2, szenario-verein §5.3, D469).
    """
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        _propose(server, world.anna.pub, world.ex.N_gov, BEITRAG)
        vorher = _kanten(server, world.ex.N_res)

        ja, nein = gabeln(_base(server))

        forks = _get(server, "/forks")
        assert len(forks) == 1
        assert forks[0]["I"] == world.bruno.pub.hex()
        assert sorted(cid for cid, _scope in forks[0]["claims"]) == sorted([ja.hex(), nein.hex()])

        antrag = _get(server, f"/proposals/{world.ex.N_gov.hex()}")[0]
        for key in ("yes", "no", "ambiguous"):
            assert world.bruno.pub.hex() not in antrag[key]

        assert _kanten(server, world.ex.N_res) < vorher
    finally:
        server.shutdown()


def test_ohne_antrag(tmp_path) -> None:
    """Kein Antrag auf PENDING: benannter Fehler, nichts eingeliefert (D488 Beschluss 2)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        spitze = _spitze(server, world.bruno.pub)
        with pytest.raises(GabelFehler, match="Kein Antrag"):
            gabeln(_base(server))
        assert _get(server, "/forks") == []
        assert _spitze(server, world.bruno.pub) == spitze
    finally:
        server.shutdown()


def test_zwei_antraege(tmp_path) -> None:
    """Zwei Anträge ohne --antrag: benannter Fehler mit beiden, nichts eingeliefert (D488 Beschluss 2)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        _propose(server, world.anna.pub, world.ex.N_gov, BEITRAG)
        _propose(server, world.chris.pub, world.ex.N_gov, BEITRAG + ", ab 2027")
        antraege = [row["proposal"] for row in _get(server, f"/proposals/{world.ex.N_gov.hex()}")]
        assert len(antraege) == 2
        spitze = _spitze(server, world.bruno.pub)
        with pytest.raises(GabelFehler, match="Mehrere") as info:
            gabeln(_base(server))
        for digest in antraege:
            assert digest in str(info.value)
        assert _get(server, "/forks") == []
        assert _spitze(server, world.bruno.pub) == spitze

        ja, nein = gabeln(_base(server), bytes.fromhex(antraege[0]))
        forks = _get(server, "/forks")
        assert sorted(cid for cid, _scope in forks[0]["claims"]) == sorted([ja.hex(), nein.hex()])
    finally:
        server.shutdown()


def test_antrag_nicht_pending(tmp_path) -> None:
    """--antrag, der nicht auf PENDING steht: benannter Fehler (D488 Beschluss 2)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    server = _start(path)
    try:
        with pytest.raises(GabelFehler, match="nicht auf PENDING"):
            gabeln(_base(server), bytes(32))
        assert _get(server, "/forks") == []
    finally:
        server.shutdown()


def test_nicht_erreichbar(tmp_path) -> None:
    """S-Node nicht erreichbar: benannter Fehler (D488 Beschluss 2)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    server = _start(path)
    base = _base(server)
    server.shutdown()
    server.server_close()
    with pytest.raises(GabelFehler, match="nicht erreichbar"):
        gabeln(base)
