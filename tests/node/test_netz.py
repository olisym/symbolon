"""Fünf Geräte, ein Durchgang über alle Paare, Gerätename und Stand (D518)."""

from __future__ import annotations

import hashlib
import json
import threading
from http.server import HTTPServer

from symbolon.atom import claim_id, signed_bytes
from symbolon.node.api import serve
from symbolon.node.store import SqliteStore
from tests.helpers import Identity, scope_id
from tests.node.test_abgleich import _bestand, _knoten, _url
from tests.node.test_api import _call, _stop
from tools.netz import GERAETE, durchgang
from tools.verein import build
from tools.verein_node import anlegen

_NOW = 1000
_T_EXP = 5000


def _start(path, geraet: str | None = None) -> HTTPServer:
    """Wie _start in test_api, mit dem Gerätenamen (D518 Beschluss 4)."""
    ready = threading.Event()
    holder: dict[str, HTTPServer] = {}

    def bound(server: HTTPServer) -> None:
        holder["server"] = server
        ready.set()

    thread = threading.Thread(
        target=serve,
        args=(path,),
        kwargs={"port": 0, "clock": lambda: _NOW, "bound": bound, "geraet": geraet},
        daemon=True,
    )
    thread.start()
    ready.wait()
    return holder["server"]


def _stand(server) -> str:
    status, body = _call(server, "GET", "/stand")
    assert status == 200, body
    return json.loads(body)


def test_schluessel_je_geraet(tmp_path) -> None:
    """Jedes Gerät hält die Schlüssel seiner Spalte und alle fünf Namen (D518 Beschluss 1)."""
    world = build()
    alle = frozenset().union(*(personen for _name, _datei, personen in GERAETE))
    namen = {getattr(world, name.lower()).pub: name for name in alle}
    assert len(namen) == 5
    for _name, datei, personen in GERAETE:
        anlegen(tmp_path / datei, personen)
        store = SqliteStore(tmp_path / datei)
        try:
            assert store.sim_pubs() == {getattr(world, name.lower()).pub for name in personen}
            assert store.all_names() == namen
        finally:
            store.close()


def test_durchgang_ueber_vier(tmp_path) -> None:
    """Vier Knoten, je ein Claim: 12 eingeliefert, dann jeder alle vier, dann 0 (D518 Beschluss 2)."""
    scope = scope_id("p21-welt")
    subject = Identity("p21-C")
    claims = [
        Identity(f"p21-{index}").vouch(subject, n=4, scope=scope, t=1, t_exp=_T_EXP)
        for index in range(4)
    ]
    knoten = [_knoten(tmp_path / f"k{index}.sqlite", claim) for index, claim in enumerate(claims)]
    try:
        urls = [_url(server) for server in knoten]
        assert durchgang(urls) == 12
        soll = {claim_id(claim).hex() for claim in claims}
        for server in knoten:
            assert set(_bestand(server)["claims"]) == soll
        assert durchgang(urls) == 0
    finally:
        for server in knoten:
            _stop(server)


def test_geraet_und_stand(tmp_path) -> None:
    """Gerätename und Stand, auch bei gesetztem Schalter (D518 Beschluss 4)."""
    a = _start(tmp_path / "a.sqlite", "Annas Gerät")
    b = _start(tmp_path / "b.sqlite")
    try:
        status, body = _call(a, "GET", "/geraet")
        assert (status, json.loads(body)) == (200, {"name": "Annas Gerät"})
        status, body = _call(b, "GET", "/geraet")
        assert (status, json.loads(body)) == (200, {"name": None})

        leer = _stand(a)
        assert leer == _stand(b)
        assert leer == hashlib.sha256((0).to_bytes(8, "big")).hexdigest()

        claim = Identity("p21-A").vouch(
            Identity("p21-C"), n=4, scope=scope_id("p21-welt"), t=1, t_exp=_T_EXP
        )
        status, body = _call(a, "POST", "/peer/claims", {"data": signed_bytes(claim).hex()})
        assert status == 200, body
        mit_claim = _stand(a)
        assert mit_claim != leer
        genesis = build().ex.genesis_gov_cbor
        status, body = _call(a, "POST", "/peer/objects", {"kind": "genesis", "data": genesis.hex()})
        assert status == 200, body
        mit_objekt = _stand(a)
        assert mit_objekt != mit_claim

        status, _body = _call(a, "POST", "/getrennt", {"getrennt": True})
        assert status == 200
        status, body = _call(a, "GET", "/stand")
        assert (status, json.loads(body)) == (200, mit_objekt)

        status, _body = _call(a, "POST", "/getrennt", {"getrennt": False})
        assert status == 200
        durchgang([_url(a), _url(b)])
        assert _stand(b) == mit_objekt
    finally:
        _stop(a)
        _stop(b)
