"""Schnittstelle des S-Node (D476)."""

from __future__ import annotations

import hashlib
import json
import socket
import sqlite3
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
)

from symbolon import cbor_canon
from symbolon.atom import claim_id, id_genesis_anchor, signed_bytes
from symbolon.domains import DOM_CID, DOM_SIG
from symbolon.node.api import serve
from symbolon.node.store import SqliteStore
from symbolon.policy import constitution_hash
from tools.example_nucleus import NOW, _nuc
from tools.verein import _T_ANNA, _T_BRUNO, _T_CHRIS, _accept, _fork_bruno, build
from tools.verein_node import anlegen


def _seed(author) -> bytes:
    return author._autor._sk.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())


def _start(path, clock) -> HTTPServer:
    ready = threading.Event()
    holder: dict[str, HTTPServer] = {}

    def bound(server: HTTPServer) -> None:
        holder["server"] = server
        ready.set()

    thread = threading.Thread(
        target=serve, args=(path,), kwargs={"port": 0, "clock": clock, "bound": bound}, daemon=True
    )
    thread.start()
    ready.wait()
    return holder["server"]


def _stop(server: HTTPServer) -> None:
    server.shutdown()


def _call(server: HTTPServer, method: str, path: str, payload: object = None, raw: bytes | None = None):
    host, port = server.server_address
    url = f"http://{host}:{port}{path}"
    data = raw if raw is not None else None
    if payload is not None:
        data = json.dumps(payload).encode()
    request = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(request) as response:
            body = response.read()
            status = response.status
    except urllib.error.HTTPError as exc:
        body = exc.read()
        status = exc.code
    return status, body


def _proposal_bytes(proposal) -> str:
    return cbor_canon.encode(
        {0: proposal.scope, 1: proposal.predecessor, 2: proposal.constitution_hash}
    ).hex()


def test_einliefern_und_lesen(tmp_path) -> None:
    """Einliefern und Lesen (D476, Abschnitt 3.6 Punkt 1)."""
    world = build()
    path = tmp_path / "bestand.sqlite"
    SqliteStore(path).close()
    server = _start(path, lambda: NOW)
    try:
        status, body = _call(
            server,
            "POST",
            "/objects",
            {"kind": "genesis", "data": world.ex.genesis_gov_cbor.hex()},
        )
        assert status == 200
        assert json.loads(body)["hash"] == world.ex.N_gov.hex()
        for constitution in (world.ex.constitution_gov, world.ex.constitution_2):
            status, _body = _call(
                server,
                "POST",
                "/objects",
                {"kind": "constitution", "data": cbor_canon.encode(constitution).hex()},
            )
            assert status == 200
        status, _body = _call(
            server,
            "POST",
            "/objects",
            {"kind": "proposal", "data": _proposal_bytes(world.ex.proposal)},
        )
        assert status == 200
        status, body = _call(
            server,
            "POST",
            "/objects",
            {"kind": "genesis", "data": world.ex.genesis_res_cbor.hex()},
        )
        assert status == 200
        assert json.loads(body)["hash"] == world.ex.N_res.hex()
        status, _body = _call(
            server,
            "POST",
            "/objects",
            {"kind": "constitution", "data": cbor_canon.encode(world.ex.constitution_res).hex()},
        )
        assert status == 200
        vouch = world.chris.vouch(
            world.dora, n=50, scope=world.ex.N_res, t=_T_CHRIS, t_exp=NOW + 1000000
        )
        accepts = [
            _accept(world.anna, world.ex.N_gov, world.ex.constitution_hash_2, t=_T_ANNA),
            _accept(world.bruno, world.ex.N_gov, world.ex.constitution_hash_2, t=_T_BRUNO),
            _accept(world.chris, world.ex.N_gov, world.ex.constitution_hash_2, t=_T_CHRIS),
        ]
        for claim in (*world.base.values(), vouch, *accepts):
            status, _body = _call(
                server, "POST", "/claims", {"data": signed_bytes(claim).hex()}
            )
            assert status == 200
        status, body = _call(server, "GET", "/scopes")
        assert status == 200
        assert json.loads(body) == sorted([world.ex.N_gov.hex(), world.ex.N_res.hex()])
        status, body = _call(server, "GET", f"/scopes/{world.ex.N_gov.hex()}")
        assert status == 200
        view = json.loads(body)
        assert view["state"]["epoch"]["index"] == 2
        members = view["verein"]["membership"]
        assert len(members) == 4
        assert {item[1]["state"] for item in members} == {"MEMBER"}
    finally:
        _stop(server)


def test_geraet_unterschreibt(tmp_path) -> None:
    """Das Gerät unterschreibt (D476, Abschnitt 3.6 Punkt 2, 01 §4)."""
    world = build()
    path = tmp_path / "bestand.sqlite"
    store = SqliteStore(path)
    for claim in world.base.values():
        store.submit_claim(signed_bytes(claim))
    store.close()
    server = _start(path, lambda: NOW)
    try:
        last = claim_id(world.base["accept_dora"])
        status, body = _call(
            server,
            "POST",
            "/prepare",
            {
                "I": world.dora.pub.hex(),
                "p": _nuc(world.ex.N_gov, "accept-rules"),
                "J": [3, world.constitution_hash_3.hex()],
                "N": world.ex.N_gov.hex(),
            },
        )
        assert status == 200
        prepared = json.loads(body)
        core = bytes.fromhex(prepared["core"])
        decoded = cbor_canon.decode(core)
        assert decoded[1] == world.dora.pub
        assert decoded[8] == last
        cid = hashlib.sha256(DOM_CID + core).digest()
        assert bytes.fromhex(prepared["claim_id"]) == cid
        sigma = Ed25519PrivateKey.from_private_bytes(_seed(world.dora)).sign(DOM_SIG + core)
        status, body = _call(
            server, "POST", "/submit", {"core": core.hex(), "sigma": sigma.hex()}
        )
        assert status == 200
        assert bytes.fromhex(json.loads(body)["claim_id"]) == cid
        opened = SqliteStore(path)
        assert opened.get(cid) is not None
        opened.close()
    finally:
        _stop(server)


def test_vorgaenger_vom_geraet(tmp_path) -> None:
    """Der Vorgänger vom Gerät (D476, Abschnitt 3.6 Punkt 3, D476 Beschluss 3)."""
    world = build()
    path = tmp_path / "bestand.sqlite"
    store = SqliteStore(path)
    for claim in world.base.values():
        store.submit_claim(signed_bytes(claim))
    store.close()
    given = id_genesis_anchor(world.dora.pub)
    assert given != claim_id(world.base["accept_dora"])
    server = _start(path, lambda: NOW)
    try:
        status, body = _call(
            server,
            "POST",
            "/prepare",
            {
                "I": world.dora.pub.hex(),
                "p": _nuc(world.ex.N_gov, "accept-rules"),
                "J": [3, world.constitution_hash_3.hex()],
                "N": world.ex.N_gov.hex(),
                "h_prev": given.hex(),
            },
        )
        assert status == 200
        core = bytes.fromhex(json.loads(body)["core"])
        assert cbor_canon.decode(core)[8] == given
    finally:
        _stop(server)


def test_gegabelte_kette(tmp_path) -> None:
    """Gegabelte Kette (D476, Abschnitt 3.6 Punkt 4, szenario-verein §5.2)."""
    world = build()
    nein, ja = _fork_bruno(world)
    path = tmp_path / "bestand.sqlite"
    store = SqliteStore(path)
    for claim in (*world.base.values(), nein, ja):
        store.submit_claim(signed_bytes(claim))
    store.close()
    server = _start(path, lambda: NOW)
    try:
        status, body = _call(
            server,
            "POST",
            "/prepare",
            {
                "I": world.bruno.pub.hex(),
                "p": _nuc(world.ex.N_gov, "vote"),
                "J": [3, world.proposal_3.proposal_hash.hex()],
                "N": world.ex.N_gov.hex(),
            },
        )
        assert status == 409
        assert b"Traceback" not in body
        status, body = _call(server, "GET", "/forks")
        assert status == 200
        groups = json.loads(body)
        assert any(group["I"] == world.bruno.pub.hex() for group in groups)
    finally:
        _stop(server)


def test_simulierte_person(tmp_path) -> None:
    """Simulierte Person (D476, Abschnitt 3.6 Punkt 5, szenario-verein §3)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    opened = SqliteStore(path)
    own = [claim for claim in opened.all_claims() if claim.I == world.chris.pub]
    pointed = {claim.h_prev for claim in own}
    tip = next(claim_id(claim) for claim in own if claim_id(claim) not in pointed)
    opened.close()
    server = _start(path, lambda: NOW)
    try:
        status, body = _call(
            server,
            "POST",
            "/sim/sign",
            {
                "I": world.chris.pub.hex(),
                "p": _nuc(world.ex.N_res, "vouch"),
                "J": [1, world.dora.pub.hex()],
                "v": cbor_canon.encode({0: 50}).hex(),
                "N": world.ex.N_res.hex(),
                "t_exp": NOW + 1000000,
            },
        )
        assert status == 200
        cid = bytes.fromhex(json.loads(body)["claim_id"])
        opened = SqliteStore(path)
        stored = opened.get(cid)
        assert stored is not None
        assert stored.h_prev == tip
        opened.close()
        status, body = _call(server, "GET", f"/scopes/{world.ex.N_res.hex()}")
        assert status == 200
        view = json.loads(body)
        assert view["vereinsleben"]["derivation"]["bfs"]["distance"][world.dora.pub.hex()] == 2
        status, body = _call(
            server,
            "POST",
            "/sim/sign",
            {
                "I": bytes(32).hex(),
                "p": _nuc(world.ex.N_res, "vouch"),
                "J": [1, world.dora.pub.hex()],
            },
        )
        assert status == 404
        assert b"Traceback" not in body
    finally:
        _stop(server)


def test_zeit(tmp_path) -> None:
    """Zeit (D476, Abschnitt 3.6 Punkt 6, 01 §6)."""
    world = build()
    previous = world.base["accept_dora"]
    path = tmp_path / "bestand.sqlite"
    store = SqliteStore(path)
    store.submit_claim(signed_bytes(previous))
    store.close()
    assert 0 < previous.t
    server = _start(path, lambda: 0)
    try:
        status, body = _call(
            server,
            "POST",
            "/prepare",
            {
                "I": world.dora.pub.hex(),
                "p": _nuc(world.ex.N_gov, "accept-rules"),
                "J": [3, world.constitution_hash_3.hex()],
                "N": world.ex.N_gov.hex(),
            },
        )
        assert status == 200
        core = bytes.fromhex(json.loads(body)["core"])
        assert cbor_canon.decode(core)[6] == previous.t
    finally:
        _stop(server)


def test_fehler(tmp_path) -> None:
    """Fehler (D476, Abschnitt 3.6 Punkt 7, 01 §6)."""
    world = build()
    path = tmp_path / "bestand.sqlite"
    SqliteStore(path).close()
    server = _start(path, lambda: NOW)
    try:
        raw = bytearray(signed_bytes(next(iter(world.base.values()))))
        raw[-1] ^= 0x01
        status, body = _call(server, "POST", "/claims", {"data": bytes(raw).hex()})
        assert status == 400
        assert b"BadSignature" in body
        assert b"Traceback" not in body
        status, body = _call(server, "GET", f"/scopes/{bytes(32).hex()}")
        assert status == 404
        assert b"Traceback" not in body
        status, body = _call(server, "POST", "/claims", raw=b"x" * (1048576 + 1))
        assert status == 413
        assert b"Traceback" not in body
        status, body = _call(server, "POST", "/claims", raw=b"not-json")
        assert status == 400
        assert b"Traceback" not in body
    finally:
        _stop(server)


def test_fremder_inhalt(tmp_path) -> None:
    """Fremder Inhalt (D476, Abschnitt 3.6 Punkt 8, D474 Beschluss 2)."""
    world = build()
    constitution = dict(world.ex.constitution_gov)
    constitution["participants"] = 5
    digest = constitution_hash(constitution)
    genesis = dict(world.ex.genesis_gov)
    genesis[4] = digest
    path = tmp_path / "bestand.sqlite"
    SqliteStore(path).close()
    server = _start(path, lambda: NOW)
    try:
        status, body = _call(
            server,
            "POST",
            "/objects",
            {"kind": "genesis", "data": cbor_canon.encode(genesis).hex()},
        )
        assert status == 200
        scope = json.loads(body)["hash"]
        status, _body = _call(
            server,
            "POST",
            "/objects",
            {"kind": "constitution", "data": cbor_canon.encode(constitution).hex()},
        )
        assert status == 200
        status, body = _call(server, "GET", f"/scopes/{scope}")
        assert status == 200
        assert b"Traceback" not in body
        assert "MALFORMED_PARTICIPANTS" in body.decode()
    finally:
        _stop(server)


def _read_response(sock: socket.socket) -> bytes:
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    head, _, rest = data.partition(b"\r\n\r\n")
    length = 0
    for line in head.split(b"\r\n")[1:]:
        name, _, value = line.partition(b":")
        if name.lower() == b"content-length":
            length = int(value.strip())
    while len(rest) < length:
        chunk = sock.recv(4096)
        if not chunk:
            break
        rest += chunk
    return head


def _bestand(path) -> tuple:
    db = sqlite3.connect(path)
    try:
        claims = db.execute(
            "SELECT claim_id, data, I, h_prev FROM claims ORDER BY claim_id"
        ).fetchall()
        objects = db.execute(
            "SELECT hash, kind, data FROM objects ORDER BY hash"
        ).fetchall()
        keys = db.execute(
            "SELECT pub, seed FROM sim_keys ORDER BY pub"
        ).fetchall()
    finally:
        db.close()
    return claims, objects, keys


def test_verbindung(tmp_path) -> None:
    """Verbindung (D477)."""
    path = tmp_path / "bestand.sqlite"
    SqliteStore(path).close()
    server = _start(path, lambda: NOW)
    try:
        host, port = server.server_address
        sock = socket.create_connection((host, port))
        sock.settimeout(3)
        try:
            sock.sendall(
                f"GET /scopes HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n".encode()
            )
            head = _read_response(sock)
            assert b"connection: close" in head.lower()
            request = urllib.request.Request(
                f"http://{host}:{port}/scopes", method="GET"
            )
            with urllib.request.urlopen(request, timeout=3) as response:
                assert response.status == 200
                response.read()
        finally:
            sock.close()
    finally:
        _stop(server)


def test_zweiter_lauf(tmp_path) -> None:
    """Zweiter Lauf (D477)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    before = _bestand(path)
    anlegen(path)
    assert _bestand(path) == before


def test_verfassung_des_vereinslebens(tmp_path) -> None:
    """Verfassung des Vereinslebens (D477)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path, lambda: NOW)
    try:
        status, body = _call(server, "GET", f"/scopes/{world.ex.N_res.hex()}")
        assert status == 200
        view = json.loads(body)
        kinds = [item["kind"] for item in view["state"]["policy_findings"]]
        assert "CONSTITUTION_UNAVAILABLE" not in kinds
    finally:
        _stop(server)


def test_nur_lokal(tmp_path) -> None:
    """Nur lokal (D476, Abschnitt 3.6 Punkt 9, D476 Beschluss 5)."""
    path = tmp_path / "bestand.sqlite"
    SqliteStore(path).close()
    server = _start(path, lambda: NOW)
    try:
        assert server.server_address[0] == "127.0.0.1"
    finally:
        _stop(server)
