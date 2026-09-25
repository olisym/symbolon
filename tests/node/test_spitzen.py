"""Die Spitzen einer Kette und das Ende nach einer Gabelung (D492 Beschluss 4, 01 §4)."""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer

from symbolon.atom import claim_id
from symbolon.node.api import serve
from symbolon.node.store import SqliteStore
from tools.verein import BEITRAG, build
from tools.verein_gabel import gabeln
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
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read())


def test_ende_nach_der_gabelung(tmp_path) -> None:
    """Zwei Spitzen nach der Gabelung; h_prev nur an eine Spitze, sonst NOT_A_TIP (D492 Beschluss 4)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    bruno = world.bruno.pub
    server = _start(path)
    try:
        status, body = _call(
            server,
            "POST",
            "/sim/intent",
            {
                "I": world.anna.pub.hex(),
                "art": "propose",
                "scope": world.ex.N_gov.hex(),
                "change": {"set": {"field": "beitrag", "text": BEITRAG}},
            },
        )
        assert status == 200, body
        ja, nein = gabeln(_base(server))

        status, tips = _call(server, "GET", f"/tips/{bruno.hex()}")
        assert status == 200
        assert tips == sorted([ja.hex(), nein.hex()])

        absicht = {"I": bruno.hex(), "art": "accept-rules", "scope": world.ex.N_gov.hex()}
        status, body = _call(server, "POST", "/sim/intent", absicht)
        assert status == 409, body

        status, body = _call(server, "POST", "/sim/intent", {**absicht, "h_prev": tips[0]})
        assert status == 200, body
        status, forks = _call(server, "GET", "/forks")
        assert len(forks) == 1
        assert sorted(cid for cid, _scope in forks[0]["claims"]) == sorted([ja.hex(), nein.hex()])

        store = SqliteStore(path)
        own = [claim for claim in store.all_claims() if claim.I == bruno]
        store.close()
        pointed = {claim.h_prev for claim in own}
        # Ein Claim mit genau einem Nachfolger, den dieser Test nicht selbst fortgesetzt hat:
        # dieselbe Absicht an denselben Vorgänger ergäbe sonst dieselbe claim_id.
        used = {bytes.fromhex(forks[0]["h_prev"]), bytes.fromhex(tips[0])}
        inner = sorted(
            claim_id(claim)
            for claim in own
            if claim_id(claim) in pointed and claim_id(claim) not in used
        )
        assert inner, "BRUNO hat keinen Claim mit genau einem Nachfolger"

        status, body = _call(server, "POST", "/sim/intent", {**absicht, "h_prev": inner[0].hex()})
        _status, forks = _call(server, "GET", "/forks")
        assert len(forks) == 1
        assert status == 400
        assert body == "NOT_A_TIP"
    finally:
        server.shutdown()


def test_ohne_claim(tmp_path) -> None:
    """Ohne Claim die leere Liste (D492 Beschluss 4)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    server = _start(path)
    try:
        status, tips = _call(server, "GET", f"/tips/{'77' * 32}")
        assert status == 200
        assert tips == []
    finally:
        server.shutdown()
