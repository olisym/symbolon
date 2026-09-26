"""Abgleich zweier Knoten und der Schalter „getrennt“ (D516, D514 Beschluss 1 und 2)."""

from __future__ import annotations

import json
import sqlite3

import pytest

from symbolon.atom import claim_id, signed_bytes
from symbolon.node.store import SqliteStore
from tests.helpers import Identity, scope_id
from tests.node.test_api import _call, _start, _stop
from tools.abgleich import pruefen, runde
from tools.verein_node import anlegen

_NOW = 1000
_T_EXP = 5000


def _url(server) -> str:
    host, port = server.server_address
    return f"http://{host}:{port}"


def _knoten(path, *claims):
    """Ein Knoten mit eigener Datei, gestartet wie in test_api (D476 Beschluss 5)."""
    store = SqliteStore(path)
    for claim in claims:
        store.submit_claim(signed_bytes(claim))
    store.close()
    return _start(path, lambda: _NOW)


def _bestand(server) -> dict:
    status, body = _call(server, "GET", "/peer/bestand")
    assert status == 200, body
    return json.loads(body)


def _soll(path) -> dict:
    """Bestand aus der Datei, unabhängig von der Route gelesen (D514 Beschluss 2)."""
    db = sqlite3.connect(path)
    try:
        claims = db.execute("SELECT claim_id FROM claims ORDER BY claim_id").fetchall()
        objects = db.execute("SELECT hash FROM objects ORDER BY hash").fetchall()
    finally:
        db.close()
    return {"claims": [row[0].hex() for row in claims], "objects": [row[0].hex() for row in objects]}


def test_fremder_widerruf(tmp_path) -> None:
    """Fremder Widerruf: Abweisung beendet die Runde nicht, danach Ruhe (D516 Golden Numbers)."""
    scope = scope_id("p20-welt")
    A = Identity("p20-A")
    B = Identity("p20-B")
    C = Identity("p20-C")
    v = A.vouch(C, n=4, scope=scope, t=1, t_exp=_T_EXP)
    w = B.revoke(v, t=2)
    n = B.vouch(C, n=4, scope=scope, t=3, t_exp=_T_EXP)
    x = _knoten(tmp_path / "x.sqlite", v)
    y = _knoten(tmp_path / "y.sqlite", w, n)
    try:
        erste = runde(_url(x), _url(y))
        assert erste.eingeliefert == 2
        assert erste.abgewiesen == {"ForeignLifecycle": 1}
        assert erste.getrennt is False
        soll = {"claims": sorted(claim_id(item).hex() for item in (v, n)), "objects": []}
        assert _bestand(x) == soll
        assert _bestand(y) == soll
        zweite = runde(_url(x), _url(y))
        assert zweite.eingeliefert == 0
        assert zweite.abgewiesen == {}
    finally:
        _stop(x)
        _stop(y)


def test_gabelung(tmp_path) -> None:
    """Gabelung: allein sieht kein Knoten etwas, nach der Runde beide (D516 Golden Numbers, 01 §4)."""
    scope = scope_id("p20-welt")
    subject = Identity("p20-C")
    an_p = Identity("p20-bruno").vouch(subject, n=4, scope=scope, t=1, t_exp=_T_EXP)
    an_q = Identity("p20-bruno").vouch(subject, n=3, scope=scope, t=1, t_exp=_T_EXP)
    p = _knoten(tmp_path / "p.sqlite", an_p)
    q = _knoten(tmp_path / "q.sqlite", an_q)
    try:
        for server in (p, q):
            status, body = _call(server, "GET", "/forks")
            assert status == 200, body
            assert json.loads(body) == []
        runde(_url(p), _url(q))
        for server in (p, q):
            status, body = _call(server, "GET", "/forks")
            assert status == 200, body
            assert len(json.loads(body)) == 1
    finally:
        _stop(p)
        _stop(q)


def test_verein(tmp_path) -> None:
    """Verein: alle Claims und Objekte gehen mit, kein Name (D516 Golden Numbers, D514 Beschluss 2)."""
    path_a = tmp_path / "a.sqlite"
    anlegen(path_a)
    soll = _soll(path_a)
    a = _start(path_a, lambda: _NOW)
    b = _knoten(tmp_path / "b.sqlite")
    try:
        assert _bestand(a) == soll
        result = runde(_url(a), _url(b))
        assert _bestand(a) == soll
        assert _bestand(b) == soll
        status, body = _call(b, "GET", "/names")
        assert status == 200, body
        assert json.loads(body) == []
        assert result.eingeliefert == len(soll["claims"]) + len(soll["objects"])
    finally:
        _stop(a)
        _stop(b)


def test_getrennt(tmp_path) -> None:
    """Getrennt: jede Route unter /peer/ ist 503, alle anderen arbeiten weiter (D516 Beschluss 3)."""
    scope = scope_id("p20-welt")
    C = Identity("p20-C")
    an_a = Identity("p20-A").vouch(C, n=4, scope=scope, t=1, t_exp=_T_EXP)
    an_b = Identity("p20-B").vouch(C, n=4, scope=scope, t=1, t_exp=_T_EXP)
    a = _knoten(tmp_path / "a.sqlite", an_a)
    b = _knoten(tmp_path / "b.sqlite", an_b)
    try:
        status, body = _call(a, "GET", "/getrennt")
        assert (status, json.loads(body)) == (200, False)
        status, body = _call(a, "POST", "/getrennt", {"getrennt": True})
        assert (status, json.loads(body)) == (200, {})
        status, body = _call(a, "GET", "/getrennt")
        assert (status, json.loads(body)) == (200, True)
        status, body = _call(a, "GET", "/peer/bestand")
        assert (status, json.loads(body)) == (503, "getrennt")
        status, body = _call(a, "GET", f"/peer/claims/{claim_id(an_a).hex()}")
        assert (status, json.loads(body)) == (503, "getrennt")
        status, body = _call(a, "POST", "/peer/claims", {"data": signed_bytes(an_b).hex()})
        assert (status, json.loads(body)) == (503, "getrennt")
        status, _body = _call(a, "GET", "/scopes")
        assert status == 200
        vorher = _bestand(b)
        result = runde(_url(a), _url(b))
        assert result.getrennt is True
        assert result.eingeliefert == 0
        assert _bestand(b) == vorher
        status, _body = _call(a, "POST", "/getrennt", {"getrennt": False})
        assert status == 200
        result = runde(_url(a), _url(b))
        assert result.getrennt is False
        assert _bestand(a) == _bestand(b)
        assert set(_bestand(a)["claims"]) == {claim_id(an_a).hex(), claim_id(an_b).hex()}
    finally:
        _stop(a)
        _stop(b)


def test_formwidrig(tmp_path) -> None:
    """Formwidrige Einlieferung unter /peer/ ist 400 und speichert nichts (D516 Beschluss 2)."""
    a = _knoten(tmp_path / "a.sqlite")
    try:
        vorher = _bestand(a)
        status, _body = _call(a, "POST", "/peer/claims", {"data": b"kein claim".hex()})
        assert status == 400
        # Die Zahl 1, nicht minimal kodiert: kein kanonisches CBOR.
        status, _body = _call(a, "POST", "/peer/objects", {"kind": "genesis", "data": "1801"})
        assert status == 400
        assert _bestand(a) == vorher
        status, _body = _call(a, "POST", "/getrennt", {"getrennt": 1})
        assert status == 400
    finally:
        _stop(a)


@pytest.mark.parametrize(
    "bestand",
    [
        ["claims", "objects"],
        {"claims": ["zz" * 32], "objects": []},
        {"claims": ["ab" * 31], "objects": []},
    ],
)
def test_formwidrige_bestandsliste(bestand) -> None:
    """Eine Bestandsliste ohne Form ist ein Fehler (D516 Beschluss 4)."""
    with pytest.raises(ValueError):
        pruefen(bestand)
