"""Aufgaben, Anträge und Lesepfade für die Bildschirme.

D484 Beschluss 1 und 2, D482 Befund 2, D486 Beschluss 1, D487 Beschluss 3.
"""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer

from symbolon import cbor_canon
from symbolon.atom import claim_id
from symbolon.node.api import serve
from tools.verein import (
    BEITRAG,
    DOC_PROPOSAL_3,
    DOC_PROPOSAL_4,
    build,
)
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


def _stop(server: HTTPServer) -> None:
    server.shutdown()


def _call(server: HTTPServer, method: str, path: str, payload: object = None):
    host, port = server.server_address
    url = f"http://{host}:{port}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def _get(server: HTTPServer, path: str):
    status, body = _call(server, "GET", path)
    assert status == 200, body
    return json.loads(body)


def _intent(server: HTTPServer, who: bytes, art: str, **fields):
    status, body = _call(server, "POST", "/sim/intent", {"I": who.hex(), "art": art, **fields})
    assert status == 200, body
    return json.loads(body)


def _tasks(server: HTTPServer, who: bytes) -> list[dict]:
    return _get(server, f"/tasks/{who.hex()}")


def _arts(tasks: list[dict], scope: bytes) -> set[str]:
    return {row["art"] for row in tasks if row["scope"] == scope.hex()}


def test_grundbestand(tmp_path) -> None:
    """CONFIRM_RULES für A/B/C, nicht DORA; /proposals leer trotz decisions (D484 Befund 2, Beschluss 1)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        for person in (world.anna, world.bruno, world.chris):
            assert "CONFIRM_RULES" in _arts(_tasks(server, person.pub), world.ex.N_gov)
        assert "CONFIRM_RULES" not in _arts(_tasks(server, world.dora.pub), world.ex.N_gov)

        view = _get(server, f"/scopes/{world.ex.N_gov.hex()}")
        digests = [digest for digest, _tally in view["verein"]["decisions"]]
        assert DOC_PROPOSAL_3.hex() in digests

        assert _get(server, f"/proposals/{world.ex.N_gov.hex()}") == []
    finally:
        _stop(server)


def test_antrag(tmp_path) -> None:
    """propose mit set beitrag: ein Antrag, VOTE für alle vier (D484 Beschluss 1 und 2, szenario-verein §4)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        _intent(
            server,
            world.anna.pub,
            "propose",
            scope=world.ex.N_gov.hex(),
            change={"set": {"field": "beitrag", "text": BEITRAG}},
        )
        proposals = _get(server, f"/proposals/{world.ex.N_gov.hex()}")
        assert len(proposals) == 1
        antrag = proposals[0]
        assert antrag["proposal"] == DOC_PROPOSAL_3.hex()
        assert antrag["proposers"] == [world.anna.pub.hex()]
        assert antrag["state"] == "PENDING"
        assert antrag["n"] == 4
        assert antrag["needed"] == 3
        assert antrag["changes"]["added"] == []
        assert antrag["changes"]["removed"] == []
        assert antrag["changes"]["fields"] == [{"field": "beitrag", "old": None, "new": BEITRAG}]

        for person in (world.anna, world.bruno, world.chris, world.dora):
            assert "VOTE" in _arts(_tasks(server, person.pub), world.ex.N_gov)
    finally:
        _stop(server)


def test_stimmen(tmp_path) -> None:
    """Ja-Stimmen bis PASSED, RATIFY für alle vier, VOTE für niemanden (D484 Beschluss 1 und 2)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        _intent(
            server,
            world.anna.pub,
            "propose",
            scope=world.ex.N_gov.hex(),
            change={"set": {"field": "beitrag", "text": BEITRAG}},
        )
        _intent(server, world.anna.pub, "vote", proposal=DOC_PROPOSAL_3.hex(), choice="yes")
        _intent(server, world.chris.pub, "vote", proposal=DOC_PROPOSAL_3.hex(), choice="yes")

        antrag = _get(server, f"/proposals/{world.ex.N_gov.hex()}")[0]
        assert sorted(antrag["yes"]) == sorted([world.anna.pub.hex(), world.chris.pub.hex()])
        assert antrag["no"] == []
        assert antrag["state"] == "PENDING"
        assert "VOTE" not in _arts(_tasks(server, world.anna.pub), world.ex.N_gov)
        assert "VOTE" not in _arts(_tasks(server, world.chris.pub), world.ex.N_gov)
        assert "VOTE" in _arts(_tasks(server, world.bruno.pub), world.ex.N_gov)
        assert "VOTE" in _arts(_tasks(server, world.dora.pub), world.ex.N_gov)

        _intent(server, world.dora.pub, "vote", proposal=DOC_PROPOSAL_3.hex(), choice="yes")
        antrag = _get(server, f"/proposals/{world.ex.N_gov.hex()}")[0]
        assert antrag["state"] == "PASSED"
        for person in (world.anna, world.bruno, world.chris, world.dora):
            tasks = _arts(_tasks(server, person.pub), world.ex.N_gov)
            assert "RATIFY" in tasks
            assert "VOTE" not in tasks
    finally:
        _stop(server)


def test_nach_ratifizierung_und_ausschluss(tmp_path) -> None:
    """Ratifizierung leert /proposals, CONFIRM_RULES für alle vier; Ausschlussantrag (D484 Beschluss 1 und 2)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        _intent(
            server,
            world.anna.pub,
            "propose",
            scope=world.ex.N_gov.hex(),
            change={"set": {"field": "beitrag", "text": BEITRAG}},
        )
        for person in (world.anna, world.chris, world.dora):
            _intent(server, person.pub, "vote", proposal=DOC_PROPOSAL_3.hex(), choice="yes")
        _intent(server, world.anna.pub, "ratify", proposal=DOC_PROPOSAL_3.hex())

        assert _get(server, f"/proposals/{world.ex.N_gov.hex()}") == []
        for person in (world.anna, world.bruno, world.chris, world.dora):
            assert "CONFIRM_RULES" in _arts(_tasks(server, person.pub), world.ex.N_gov)

        _intent(
            server,
            world.anna.pub,
            "propose",
            scope=world.ex.N_gov.hex(),
            change={"remove": world.bruno.pub.hex()},
        )
        antrag = _get(server, f"/proposals/{world.ex.N_gov.hex()}")[0]
        assert antrag["proposal"] == DOC_PROPOSAL_4.hex()
        assert antrag["changes"]["removed"] == [world.bruno.pub.hex()]
        assert antrag["changes"]["fields"] == []
        assert antrag["needed"] == 3
    finally:
        _stop(server)


def test_doppelstimme(tmp_path) -> None:
    """Ja dann Nein: kein VOTE mehr, weder yes noch no (D484 Beschluss 1 und 2, szenario-verein §5.1)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        _intent(
            server,
            world.anna.pub,
            "propose",
            scope=world.ex.N_gov.hex(),
            change={"set": {"field": "beitrag", "text": BEITRAG}},
        )
        _intent(server, world.bruno.pub, "vote", proposal=DOC_PROPOSAL_3.hex(), choice="yes")
        _intent(server, world.bruno.pub, "vote", proposal=DOC_PROPOSAL_3.hex(), choice="no")

        antrag = _get(server, f"/proposals/{world.ex.N_gov.hex()}")[0]
        assert world.bruno.pub.hex() not in antrag["yes"]
        assert world.bruno.pub.hex() not in antrag["no"]
        assert "VOTE" not in _arts(_tasks(server, world.bruno.pub), world.ex.N_gov)
        for person in (world.anna, world.chris, world.dora):
            assert "VOTE" in _arts(_tasks(server, person.pub), world.ex.N_gov)
    finally:
        _stop(server)


def test_beitrag(tmp_path) -> None:
    """Obligation und Quittung: CONTRIBUTION_OPEN und RECEIPT, danach keins mehr (D484 Beschluss 1, 03 §3.3.2)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        answered = _intent(
            server,
            world.dora.pub,
            "obligation",
            scope=world.ex.N_res.hex(),
            creditor=world.kasse.pub.hex(),
            amount=2400,
            unit="EUR-Cent",
        )
        cid = answered["claim_id"]

        dora_tasks = [row for row in _tasks(server, world.dora.pub) if row["scope"] == world.ex.N_res.hex()]
        assert {"scope": world.ex.N_res.hex(), "art": "CONTRIBUTION_OPEN", "obligation": cid} in dora_tasks
        kasse_tasks = [
            row for row in _tasks(server, world.kasse.pub) if row["scope"] == world.ex.N_res.hex()
        ]
        assert {"scope": world.ex.N_res.hex(), "art": "RECEIPT", "obligation": cid} in kasse_tasks

        _intent(server, world.kasse.pub, "receipt", obligation=cid)

        dora_tasks = _tasks(server, world.dora.pub)
        kasse_tasks = _tasks(server, world.kasse.pub)
        assert not any(row["art"] == "CONTRIBUTION_OPEN" for row in dora_tasks)
        assert not any(row["art"] == "RECEIPT" for row in kasse_tasks)
    finally:
        _stop(server)


def test_unbekannter_scope(tmp_path) -> None:
    """GET /proposals/<scope> auf einen unbekannten Scope ist 404 (D484 Beschluss 2)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    server = _start(path)
    try:
        status, _body = _call(server, "GET", f"/proposals/{'00' * 32}")
        assert status == 404
    finally:
        _stop(server)


def test_scope_ohne_verein(tmp_path) -> None:
    """Scope ohne Teil verein: leere Liste (D484 Beschluss 2)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        assert _get(server, f"/proposals/{world.ex.N_res.hex()}") == []
    finally:
        _stop(server)


def test_now(tmp_path) -> None:
    """/now gibt die eingespeiste Uhr (D486 Beschluss 1, Abnahmekriterium 1)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    server = _start(path)
    try:
        assert _get(server, "/now") == NOW
    finally:
        _stop(server)


def test_obligationen(tmp_path) -> None:
    """Doras Obligation an KASSE: OPEN, nach der Quittung SETTLED; N_gov leer (D486 Beschluss 1,

    szenario-verein §6).
    """
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        assert _get(server, f"/obligations/{world.ex.N_gov.hex()}") == []

        answered = _intent(
            server,
            world.dora.pub,
            "obligation",
            scope=world.ex.N_res.hex(),
            creditor=world.kasse.pub.hex(),
            amount=2400,
            unit="EUR-Cent",
        )
        cid = answered["claim_id"]

        rows = _get(server, f"/obligations/{world.ex.N_res.hex()}")
        assert len(rows) == 1
        row = rows[0]
        assert row["claim_id"] == cid
        assert row["debtor"] == world.dora.pub.hex()
        assert row["creditor"] == world.kasse.pub.hex()
        assert row["amount"] == 2400
        assert row["unit"] == "EUR-Cent"
        assert row["state"] == "OPEN"

        _intent(server, world.kasse.pub, "receipt", obligation=cid)
        row = _get(server, f"/obligations/{world.ex.N_res.hex()}")[0]
        assert row["state"] == "SETTLED"

        status, _body = _call(server, "GET", f"/obligations/{'00' * 32}")
        assert status == 404
    finally:
        _stop(server)


def test_obligationen_fremder_inhalt(tmp_path) -> None:
    """v kein Map, Einheit kein UTF-8: beide erscheinen, amount und unit null, 200 (D486 Beschluss 1)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        predicate = f"nuc:{world.ex.N_res.hex()}/obligation@1"
        status, body = _call(
            server,
            "POST",
            "/sim/sign",
            {
                "I": world.dora.pub.hex(),
                "p": predicate,
                "J": [1, world.kasse.pub.hex()],
                "v": cbor_canon.encode(42).hex(),
                "N": world.ex.N_res.hex(),
            },
        )
        assert status == 200, body
        non_map_cid = json.loads(body)["claim_id"]

        status, body = _call(
            server,
            "POST",
            "/sim/sign",
            {
                "I": world.dora.pub.hex(),
                "p": predicate,
                "J": [1, world.kasse.pub.hex()],
                "v": cbor_canon.encode({0: 500, 1: b"\xff\xfe"}).hex(),
                "N": world.ex.N_res.hex(),
            },
        )
        assert status == 200, body
        bad_unit_cid = json.loads(body)["claim_id"]

        rows = {row["claim_id"]: row for row in _get(server, f"/obligations/{world.ex.N_res.hex()}")}
        for cid in (non_map_cid, bad_unit_cid):
            assert rows[cid]["amount"] is None
            assert rows[cid]["unit"] is None
    finally:
        _stop(server)


def test_claims(tmp_path) -> None:
    """p, t, I und der dekodierte Wert; kein kanonisches v ist null; unbekannt ist 404 (D486 Beschluss 1)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        vote_id = claim_id(world.base["vote_anna"]).hex()
        row = _get(server, f"/claims/{vote_id}")
        assert row["p"] == f"nuc:{world.ex.N_gov.hex()}/vote@1"
        assert row["t"] == world.base["vote_anna"].t
        assert row["I"] == world.anna.pub.hex()
        assert row["value"] == {"0": 1}

        predicate = f"nuc:{world.ex.N_res.hex()}/obligation@1"
        status, body = _call(
            server,
            "POST",
            "/sim/sign",
            {
                "I": world.dora.pub.hex(),
                "p": predicate,
                "J": [1, world.kasse.pub.hex()],
                "v": bytes.fromhex("1801").hex(),
                "N": world.ex.N_res.hex(),
            },
        )
        assert status == 200, body
        non_canon_cid = json.loads(body)["claim_id"]
        assert _get(server, f"/claims/{non_canon_cid}")["value"] is None

        status, _body = _call(server, "GET", f"/claims/{'11' * 32}")
        assert status == 404
    finally:
        _stop(server)


def test_ambiguous(tmp_path) -> None:
    """Bruno stimmt Nein und dann Ja: ambiguous, nicht yes oder no; Anna bleibt draußen

    (D487 Beschluss 3, szenario-verein §5.1).
    """
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        _intent(
            server,
            world.anna.pub,
            "propose",
            scope=world.ex.N_gov.hex(),
            change={"set": {"field": "beitrag", "text": BEITRAG}},
        )
        _intent(server, world.bruno.pub, "vote", proposal=DOC_PROPOSAL_3.hex(), choice="no")
        _intent(server, world.bruno.pub, "vote", proposal=DOC_PROPOSAL_3.hex(), choice="yes")
        _intent(server, world.anna.pub, "vote", proposal=DOC_PROPOSAL_3.hex(), choice="yes")

        antrag = _get(server, f"/proposals/{world.ex.N_gov.hex()}")[0]
        assert antrag["ambiguous"] == [world.bruno.pub.hex()]
        assert world.bruno.pub.hex() not in antrag["yes"]
        assert world.bruno.pub.hex() not in antrag["no"]
        assert world.anna.pub.hex() not in antrag["ambiguous"]
        assert antrag["yes"] == [world.anna.pub.hex()]
    finally:
        _stop(server)
