"""Schnittstelle des S-Node (D476)."""

from __future__ import annotations

import hashlib
import http.client
import json
import re
import socket
import sqlite3
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
)

from symbolon import cbor_canon
from symbolon.atom import claim_id, id_genesis_anchor, signed_bytes
from symbolon.domains import DOM_CID, DOM_SIG
from symbolon.governance.objects import Epoch
from symbolon.node.api import serve
from symbolon.node.store import SqliteStore
from symbolon.node.__main__ import uhr_ab
from symbolon.policy import constitution_hash
from symbolon.trust.params import resolve_trust_params
from tools.example_nucleus import NOW, _nuc
from tools.verein import (
    BEITRAG,
    DOC_CONSTITUTION_HASH_3,
    DOC_CONSTITUTION_HASH_4,
    DOC_EPOCH_ID_3,
    DOC_PROPOSAL_3,
    DOC_PROPOSAL_4,
    _T_ANNA,
    _T_BRUNO,
    _T_CHRIS,
    _accept,
    _fork_bruno,
    _obligation,
    build,
)
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


def _intent(server, who, art: str, **fields):
    payload = {"I": who.hex(), "art": art, **fields}
    return _call(server, "POST", "/sim/intent", payload)


def _yes(server, world, proposal: bytes) -> None:
    for who in (world.anna, world.chris, world.dora):
        status, body = _intent(server, who.pub, "vote", proposal=proposal.hex(), choice="yes")
        assert status == 200, body
    status, body = _intent(server, world.bruno.pub, "vote", proposal=proposal.hex(), choice="yes")
    assert status == 200, body
    status, body = _intent(server, world.bruno.pub, "vote", proposal=proposal.hex(), choice="no")
    assert status == 200, body


def _epoch_id(view: dict) -> bytes:
    epoch = view["state"]["epoch"]
    return Epoch(
        scope=bytes.fromhex(epoch["scope"]),
        index=epoch["index"],
        constitution_hash=bytes.fromhex(epoch["constitution_hash"]),
    ).epoch_id


def _decision_yes(view: dict, proposal: bytes) -> list[str]:
    for digest, tally in view["verein"]["decisions"]:
        if digest == proposal.hex():
            return tally["yes"]
    raise AssertionError("proposal missing from decide")


def test_weg_zur_epoche_3(tmp_path) -> None:
    """Weg zur Epoche 3 (D479 Beschluss 2, szenario-verein §4, szenario-verein §5.1)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path, lambda: 1000)
    try:
        status, body = _intent(
            server,
            world.anna.pub,
            "propose",
            scope=world.ex.N_gov.hex(),
            change={"set": {"field": "beitrag", "text": BEITRAG}},
        )
        assert status == 200, body
        opened = SqliteStore(path)
        proposed = opened.get(bytes.fromhex(json.loads(body)["claim_id"]))
        assert proposed is not None
        assert proposed.J[1] == DOC_PROPOSAL_3
        opened.close()
        status, body = _call(server, "GET", f"/objects/{DOC_CONSTITUTION_HASH_3.hex()}")
        assert status == 200
        assert json.loads(body)["kind"] == "constitution"
        _yes(server, world, DOC_PROPOSAL_3)
        status, body = _call(server, "GET", f"/scopes/{world.ex.N_gov.hex()}")
        yes = _decision_yes(json.loads(body), DOC_PROPOSAL_3)
        status, body = _intent(server, world.anna.pub, "ratify", proposal=DOC_PROPOSAL_3.hex())
        assert status == 200, body
        opened = SqliteStore(path)
        ratified = opened.get(bytes.fromhex(json.loads(body)["claim_id"]))
        opened.close()
        assert ratified is not None
        assert cbor_canon.decode(ratified.v)[0] == [bytes.fromhex(item) for item in yes]
        status, body = _call(server, "GET", f"/scopes/{world.ex.N_gov.hex()}")
        assert _epoch_id(json.loads(body)) == DOC_EPOCH_ID_3
    finally:
        _stop(server)


def test_ausschluss(tmp_path) -> None:
    """Ausschluss (D479 Beschluss 3, szenario-verein §5.3)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path, lambda: 1000)
    try:
        status, body = _intent(
            server,
            world.anna.pub,
            "propose",
            scope=world.ex.N_gov.hex(),
            change={"set": {"field": "beitrag", "text": BEITRAG}},
        )
        assert status == 200, body
        _yes(server, world, DOC_PROPOSAL_3)
        status, body = _intent(server, world.anna.pub, "ratify", proposal=DOC_PROPOSAL_3.hex())
        assert status == 200, body
        status, body = _intent(
            server,
            world.anna.pub,
            "propose",
            scope=world.ex.N_gov.hex(),
            change={"remove": world.bruno.pub.hex()},
        )
        assert status == 200, body
        opened = SqliteStore(path)
        proposed = opened.get(bytes.fromhex(json.loads(body)["claim_id"]))
        opened.close()
        assert proposed is not None
        assert proposed.J[1] == DOC_PROPOSAL_4
        status, body = _call(server, "GET", f"/objects/{DOC_CONSTITUTION_HASH_4.hex()}")
        assert status == 200
        assert json.loads(body)["kind"] == "constitution"
    finally:
        _stop(server)


def test_ratify_zu_frueh(tmp_path) -> None:
    """ratify zu früh und Stimme auf eine alte Epoche (D479 Beschluss 4, 04 §2.2, 04 §2.3)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path, lambda: 1000)
    try:
        status, body = _intent(
            server, world.anna.pub, "vote", proposal=DOC_PROPOSAL_3.hex(), choice="yes"
        )
        assert status == 200, body
        status, body = _intent(server, world.anna.pub, "ratify", proposal=DOC_PROPOSAL_3.hex())
        assert status == 400
        assert json.loads(body) == "NOT_PASSED"
        status, body = _intent(
            server,
            world.anna.pub,
            "vote",
            proposal=world.ex.proposal.proposal_hash.hex(),
            choice="yes",
        )
        assert status == 400
        assert json.loads(body) == "NOT_CURRENT"
    finally:
        _stop(server)


def test_add_sortiert(tmp_path) -> None:
    """add sortiert ein (D479 Beschluss 3, 04 §1.1, 04 §3.5)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path, lambda: 1000)
    try:
        status, body = _call(server, "GET", f"/scopes/{world.ex.N_gov.hex()}")
        members = [bytes.fromhex(item[0]) for item in json.loads(body)["verein"]["membership"]]
        fresh = None
        for index in range(1, 64):
            seed = bytes([index]) + bytes(31)
            candidate = Ed25519PrivateKey.from_private_bytes(seed).public_key().public_bytes_raw()
            if all(candidate <= member for member in members):
                fresh = candidate
                break
        assert fresh is not None
        assert all(fresh <= member for member in members)
        status, body = _intent(
            server,
            world.anna.pub,
            "propose",
            scope=world.ex.N_gov.hex(),
            change={"add": fresh.hex()},
        )
        assert status == 200, body
        opened = SqliteStore(path)
        proposed = opened.get(bytes.fromhex(json.loads(body)["claim_id"]))
        opened.close()
        assert proposed is not None
        status, body = _call(server, "GET", f"/objects/{proposed.J[1].hex()}")
        proposal = cbor_canon.decode(bytes.fromhex(json.loads(body)["data"]))
        status, body = _call(server, "GET", f"/objects/{proposal[2].hex()}")
        constitution = cbor_canon.decode(bytes.fromhex(json.loads(body)["data"]))
        assert constitution["participants"] == sorted(constitution["participants"])
        assert fresh in constitution["participants"]
        status, body = _call(server, "GET", f"/scopes/{world.ex.N_gov.hex()}")
        view = json.loads(body)
        tally = next(
            item[1] for item in view["verein"]["decisions"] if item[0] == proposed.J[1].hex()
        )
        assert "MALFORMED_PARTICIPANTS" not in [finding["kind"] for finding in tally["findings"]]
        status, body = _intent(
            server,
            world.anna.pub,
            "propose",
            scope=world.ex.N_gov.hex(),
            change={"add": world.anna.pub.hex()},
        )
        assert status == 400
        assert json.loads(body) == "ALREADY_PARTICIPANT"
    finally:
        _stop(server)


def test_set_protokollfeld(tmp_path) -> None:
    """set auf ein Protokollfeld (D479 Beschluss 3, 00 §5, 04 §1.1)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path, lambda: 1000)
    try:
        for field in ("participants", "thresholds"):
            status, body = _intent(
                server,
                world.anna.pub,
                "propose",
                scope=world.ex.N_gov.hex(),
                change={"set": {"field": field, "text": "x"}},
            )
            assert status == 400
            assert json.loads(body) == "RESERVED_FIELD"
    finally:
        _stop(server)


def test_budget(tmp_path) -> None:
    """Budget (D479 Beschluss 4, 02 §3.1)."""
    world = build()
    limit = resolve_trust_params(
        scope=world.ex.N_res, genesis_obj=world.ex.genesis_res
    ).D
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    server = _start(path, lambda: 1000)
    try:
        status, body = _intent(
            server,
            world.anna.pub,
            "vouch",
            scope=world.ex.N_res.hex(),
            subject=world.dora.pub.hex(),
            n=1,
            t_exp=1001000,
        )
        assert status == 200, body
        assert "BUDGET_FULL" in json.loads(body)["warnings"]
        status, body = _intent(
            server,
            world.chris.pub,
            "vouch",
            scope=world.ex.N_res.hex(),
            subject=world.dora.pub.hex(),
            n=50,
            t_exp=1001000,
        )
        assert status == 200, body
        assert json.loads(body)["warnings"] == []
        for weight in (0, limit + 1):
            status, body = _intent(
                server,
                world.chris.pub,
                "vouch",
                scope=world.ex.N_res.hex(),
                subject=world.dora.pub.hex(),
                n=weight,
                t_exp=1001000,
            )
            assert status == 400
            assert json.loads(body) == "INVALID_WEIGHT"
    finally:
        _stop(server)
    later = tmp_path / "spaeter.sqlite"
    anlegen(later)
    server = _start(later, lambda: 1001001)
    try:
        status, body = _intent(
            server,
            world.anna.pub,
            "vouch",
            scope=world.ex.N_res.hex(),
            subject=world.dora.pub.hex(),
            n=1,
            t_exp=2001001,
        )
        assert status == 200, body
        assert json.loads(body)["warnings"] == []
    finally:
        _stop(server)


def test_zweite_stimme(tmp_path) -> None:
    """Zweite Stimme (D479 Beschluss 4, 04 §3.1)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path, lambda: 1000)
    try:
        status, body = _intent(
            server, world.bruno.pub, "vote", proposal=DOC_PROPOSAL_3.hex(), choice="yes"
        )
        assert status == 200, body
        assert json.loads(body)["warnings"] == []
        status, body = _intent(
            server, world.bruno.pub, "vote", proposal=DOC_PROPOSAL_3.hex(), choice="no"
        )
        assert status == 200, body
        assert "ALREADY_VOTED" in json.loads(body)["warnings"]
        status, body = _intent(
            server, world.chris.pub, "vote", proposal=DOC_PROPOSAL_3.hex(), choice="yes"
        )
        assert status == 200, body
        assert json.loads(body)["warnings"] == []
    finally:
        _stop(server)


def test_beitrag(tmp_path) -> None:
    """Beitrag (D479 Beschluss 2, szenario-verein §6, 03 §3.3.2)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    expected = _obligation(world).v
    server = _start(path, lambda: 1000)
    try:
        status, body = _intent(
            server,
            world.dora.pub,
            "obligation",
            scope=world.ex.N_res.hex(),
            creditor=world.kasse.pub.hex(),
            amount=2400,
            unit="EUR-Cent",
        )
        assert status == 200, body
        opened = SqliteStore(path)
        obligation = opened.get(bytes.fromhex(json.loads(body)["claim_id"]))
        opened.close()
        assert obligation is not None
        assert obligation.v == expected
        status, body = _intent(
            server, world.kasse.pub, "receipt", obligation=claim_id(obligation).hex()
        )
        assert status == 200, body
        status, body = _call(server, "GET", f"/scopes/{world.ex.N_res.hex()}")
        view = json.loads(body)
        settled = {
            item[0]: item[1]["state"] for item in view["vereinsleben"]["settlements"]
        }
        assert settled[claim_id(obligation).hex()] == "SETTLED"
        status, body = _intent(
            server, world.chris.pub, "receipt", obligation=claim_id(obligation).hex()
        )
        assert status == 400
        assert json.loads(body) == "NOT_CREDITOR"
    finally:
        _stop(server)


def test_intent_geraet(tmp_path) -> None:
    """intent für ein Gerät (D479 Beschluss 2, D476 Beschluss 3)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    given = id_genesis_anchor(world.dora.pub)
    server = _start(path, lambda: 1000)
    try:
        status, body = _call(
            server,
            "POST",
            "/intent",
            {
                "I": world.dora.pub.hex(),
                "art": "accept-rules",
                "scope": world.ex.N_gov.hex(),
                "h_prev": given.hex(),
            },
        )
        assert status == 200, body
        prepared = json.loads(body)
        core = bytes.fromhex(prepared["core"])
        assert cbor_canon.decode(core)[8] == given
        sigma = Ed25519PrivateKey.from_private_bytes(_seed(world.dora)).sign(DOM_SIG + core)
        status, body = _call(
            server, "POST", "/submit", {"core": core.hex(), "sigma": sigma.hex()}
        )
        assert status == 200, body
        assert json.loads(body)["claim_id"] == prepared["claim_id"]
    finally:
        _stop(server)


def test_adressbuch(tmp_path) -> None:
    """Adressbuch (D479 Beschluss 5, szenario-verein §2)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    anlegen(path)
    world = build()
    server = _start(path, lambda: 1000)
    try:
        status, body = _call(server, "GET", "/names")
        assert status == 200, body
        rows = json.loads(body)
        named = {row["name"]: row for row in rows}
        assert set(named) == {"ANNA", "BRUNO", "CHRIS", "DORA", "KASSE"}
        assert all(row["simulated"] for row in rows)
        fresh = Ed25519PrivateKey.from_private_bytes(bytes([9]) + bytes(31)).public_key().public_bytes_raw()
        status, body = _call(
            server, "POST", "/names", {"I": fresh.hex(), "name": "OLI"}
        )
        assert status == 200, body
        status, body = _call(server, "GET", "/names")
        rows = json.loads(body)
        added = next(row for row in rows if row["I"] == fresh.hex())
        assert added["name"] == "OLI"
        assert added["simulated"] is False
    finally:
        _stop(server)


def test_weltuhr() -> None:
    """Weltuhr (D479 Beschluss 1)."""
    clock = uhr_ab(1000)
    assert clock() == 1000
    assert clock() >= 1000


def test_nur_lokal(tmp_path) -> None:
    """Nur lokal (D476, Abschnitt 3.6 Punkt 9, D476 Beschluss 5)."""
    path = tmp_path / "bestand.sqlite"
    SqliteStore(path).close()
    server = _start(path, lambda: NOW)
    try:
        assert server.server_address[0] == "127.0.0.1"
    finally:
        _stop(server)


_APP_HEADERS = {
    "content-security-policy": "default-src 'self'; frame-ancestors 'none'",
    "x-content-type-options": "nosniff",
    "cache-control": "no-store",
}


def _raw(server: HTTPServer, path: str):
    host, port = server.server_address
    connection = http.client.HTTPConnection(host, port)
    connection.request("GET", path)
    response = connection.getresponse()
    body = response.read()
    headers = {key.lower(): value for key, value in response.getheaders()}
    status = response.status
    connection.close()
    return status, body, headers


def _content_type(name: str) -> str:
    if name.endswith(".html"):
        return "text/html; charset=utf-8"
    if name.endswith(".js"):
        return "text/javascript; charset=utf-8"
    if name.endswith(".json"):
        return "application/json"
    if name.endswith(".css"):
        return "text/css; charset=utf-8"
    raise AssertionError(name)


def test_statische_dateien(tmp_path) -> None:
    """Startseite und /app/ nur mit den Namen aus static/ (D481 Beschluss 5)."""
    path = tmp_path / "bestand.sqlite"
    SqliteStore(path).close()
    root = Path("symbolon/node/static")
    server = _start(path, lambda: NOW)
    try:
        status, body, headers = _raw(server, "/")
        assert status == 200
        assert body == (root / "index.html").read_bytes()
        assert headers["content-type"] == "text/html; charset=utf-8"
        for key, value in _APP_HEADERS.items():
            assert headers[key] == value
        for file in sorted(item for item in root.iterdir() if item.is_file()):
            status, body, headers = _raw(server, f"/app/{file.name}")
            assert status == 200, file.name
            assert body == file.read_bytes()
            assert headers["content-type"] == _content_type(file.name)
            for key, value in _APP_HEADERS.items():
                assert headers[key] == value
        for blocked in ("/app/../api.py", "/app/%2e%2e/api.py", "/app/unbekannt.js", "/app/unter/datei.js"):
            status, _body, _headers = _raw(server, blocked)
            assert status == 404, blocked
        status, _body, headers = _raw(server, "/scopes")
        assert status == 200
        assert headers["content-type"] == "application/json"
        assert "content-security-policy" not in headers
    finally:
        _stop(server)


def _css_regeln(text: str) -> list[tuple[list[str], dict[str, str]]]:
    """Regeln einer Stildatei als Selektoren und Deklarationen, ohne Kommentare und @media."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    regeln = []
    for selektoren, rumpf in re.findall(r"([^{}]+)\{([^{}]*)\}", text):
        deklarationen = {}
        for teil in rumpf.split(";"):
            if ":" in teil:
                name, wert = teil.split(":", 1)
                deklarationen[name.strip()] = " ".join(wert.split())
        regeln.append(([s.strip() for s in selektoren.split(",")], deklarationen))
    return regeln


def test_hidden_gilt() -> None:
    """[hidden] wird nie angezeigt, gleich welche Klasse das Element trägt (D494 Beschluss 4).

    Ein Attributselektor wiegt so viel wie eine Klasse; gegen .karte { display: flex } setzt sich
    die Regel nur mit !important durch, und keine andere Regel darf display ebenso erzwingen.
    """
    regeln = _css_regeln(Path("symbolon/node/static/style.css").read_text(encoding="utf-8"))
    hidden = [d for selektoren, d in regeln if "[hidden]" in selektoren]
    assert any(d.get("display") == "none !important" for d in hidden)
    erzwungen = [
        selektoren
        for selektoren, d in regeln
        if "[hidden]" not in selektoren and d.get("display", "").endswith("!important")
    ]
    assert erzwungen == []
