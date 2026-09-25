"""Die Folge einer Absicht vor der Unterschrift (D490 Beschluss 2).

Jede Vorhersage wird nach dem Einliefern an der Sicht bestätigt.
"""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from symbolon.domains import DOM_SIG
from symbolon.node.api import serve
from symbolon.trust.params import resolve_trust_params
from tools.verein import BEITRAG, build
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


def _call(server: HTTPServer, method: str, path: str, payload: object = None):
    host, port = server.server_address
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(f"http://{host}:{port}{path}", data=data, method=method)
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def _get(server: HTTPServer, path: str):
    status, body = _call(server, "GET", path)
    assert status == 200, body
    return json.loads(body)


def _sim(server: HTTPServer, who: bytes, art: str, **fields) -> dict:
    status, body = _call(server, "POST", "/sim/intent", {"I": who.hex(), "art": art, **fields})
    assert status == 200, body
    return json.loads(body)


def _fresh() -> Ed25519PrivateKey:
    return Ed25519PrivateKey.from_private_bytes(bytes([0x77]) + bytes(31))


def _geraet(server: HTTPServer, key: Ed25519PrivateKey, art: str, **fields) -> dict:
    """POST /intent, unterschreiben, POST /submit; gibt die Antwort von /intent (D479 Beschluss 2)."""
    pub = key.public_key().public_bytes_raw()
    status, body = _call(server, "POST", "/intent", {"I": pub.hex(), "art": art, **fields})
    assert status == 200, body
    prepared = json.loads(body)
    core = bytes.fromhex(prepared["core"])
    sigma = key.sign(DOM_SIG + core)
    status, body = _call(server, "POST", "/submit", {"core": core.hex(), "sigma": sigma.hex()})
    assert status == 200, body
    return prepared


def _antrag(server: HTTPServer, scope: bytes) -> dict:
    rows = _get(server, f"/proposals/{scope.hex()}")
    assert len(rows) == 1
    return rows[0]


def _propose(server: HTTPServer, world) -> dict:
    return _sim(
        server,
        world.anna.pub,
        "propose",
        scope=world.ex.N_gov.hex(),
        change={"set": {"field": "beitrag", "text": BEITRAG}},
    )


def _membership(server: HTTPServer, scope: bytes) -> dict[str, str]:
    view = _get(server, f"/scopes/{scope.hex()}")
    return {subject: result["state"] for subject, result in view["verein"]["membership"]}


def test_antrag(tmp_path) -> None:
    """Kriterium 1: needed 3 und n 4, gleich /proposals danach (szenario-verein §4, D484 Beschluss 2)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        effect = _propose(server, world)["effect"]
        assert effect == {"needed": 3, "n": 4}
        antrag = _antrag(server, world.ex.N_gov)
        assert (antrag["needed"], antrag["n"]) == (effect["needed"], effect["n"])
    finally:
        server.shutdown()


def test_stimmen(tmp_path) -> None:
    """Kriterium 2: yes 1, 2, 3; passes erst bei DORA; /proposals stimmt nach jedem Schritt (04 §3.2)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        _propose(server, world)
        digest = _antrag(server, world.ex.N_gov)["proposal"]
        for person, yes, passes in ((world.anna, 1, False), (world.chris, 2, False), (world.dora, 3, True)):
            effect = _sim(server, person.pub, "vote", proposal=digest, choice="yes")["effect"]
            assert (effect["yes"], effect["passes"], effect["counts"]) == (yes, passes, True)
            antrag = _antrag(server, world.ex.N_gov)
            assert len(antrag["yes"]) == effect["yes"]
            assert len(antrag["no"]) == effect["no"]
            assert antrag["state"] == ("PASSED" if effect["passes"] else "PENDING")
    finally:
        server.shutdown()


def test_zweite_stimme(tmp_path) -> None:
    """Kriterium 3: Brunos Nein nach seinem Ja zählt nicht und nimmt das Ja heraus (04 §3.1)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        _propose(server, world)
        digest = _antrag(server, world.ex.N_gov)["proposal"]
        _sim(server, world.anna.pub, "vote", proposal=digest, choice="yes")
        _sim(server, world.bruno.pub, "vote", proposal=digest, choice="yes")
        vorher = _antrag(server, world.ex.N_gov)
        assert world.bruno.pub.hex() in vorher["yes"]

        answered = _sim(server, world.bruno.pub, "vote", proposal=digest, choice="no")
        effect = answered["effect"]
        assert effect["counts"] is False
        assert effect["yes"] == len(vorher["yes"]) - 1
        assert effect["no"] == len(vorher["no"])

        nachher = _antrag(server, world.ex.N_gov)
        assert len(nachher["yes"]) == effect["yes"]
        assert len(nachher["no"]) == effect["no"]
        assert nachher["state"] == ("PASSED" if effect["passes"] else "PENDING")
    finally:
        server.shutdown()


def test_nicht_auf_der_liste(tmp_path) -> None:
    """Kriterium 4: ein frischer Schlüssel stimmt ab, zählt nicht, die Zahlen bleiben (04 §3.1)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        _propose(server, world)
        digest = _antrag(server, world.ex.N_gov)["proposal"]
        _sim(server, world.anna.pub, "vote", proposal=digest, choice="yes")
        vorher = _antrag(server, world.ex.N_gov)

        effect = _geraet(server, _fresh(), "vote", proposal=digest, choice="yes")["effect"]
        assert effect["counts"] is False
        assert (effect["yes"], effect["no"]) == (len(vorher["yes"]), len(vorher["no"]))

        nachher = _antrag(server, world.ex.N_gov)
        assert (len(nachher["yes"]), len(nachher["no"])) == (effect["yes"], effect["no"])
        assert nachher["state"] == vorher["state"]
    finally:
        server.shutdown()


def test_ratifizierung(tmp_path) -> None:
    """Kriterium 5: epoch ist die geltende plus eins; danach steht die Sicht dort (04 §4.2)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        _propose(server, world)
        digest = _antrag(server, world.ex.N_gov)["proposal"]
        for person in (world.anna, world.chris, world.dora):
            _sim(server, person.pub, "vote", proposal=digest, choice="yes")
        vorher = _get(server, f"/scopes/{world.ex.N_gov.hex()}")["state"]["epoch"]["index"]

        effect = _sim(server, world.anna.pub, "ratify", proposal=digest)["effect"]
        assert effect == {"epoch": vorher + 1}
        nachher = _get(server, f"/scopes/{world.ex.N_gov.hex()}")["state"]["epoch"]["index"]
        assert nachher == effect["epoch"]
    finally:
        server.shutdown()


def test_satzung_annehmen(tmp_path) -> None:
    """Kriterium 6: frühere Fassung, geltende Fassung, frischer Schlüssel (04 §6.1)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        view = _get(server, f"/scopes/{world.ex.N_gov.hex()}")
        assert view["state"]["epoch"]["index"] == 2
        anna = world.anna.pub.hex()
        vorher = _membership(server, world.ex.N_gov)[anna]

        effect = _sim(
            server,
            world.anna.pub,
            "accept-rules",
            scope=world.ex.N_gov.hex(),
            constitution=world.ex.constitution_hash_gov.hex(),
        )["effect"]
        assert effect == {"membership": vorher}
        assert _membership(server, world.ex.N_gov)[anna] == effect["membership"]

        effect = _sim(server, world.anna.pub, "accept-rules", scope=world.ex.N_gov.hex())["effect"]
        assert effect == {"membership": "MEMBER"}
        assert _membership(server, world.ex.N_gov)[anna] == effect["membership"]

        fresh = _fresh()
        effect = _geraet(server, fresh, "accept-rules", scope=world.ex.N_gov.hex())["effect"]
        assert effect == {"membership": "APPLICANT"}
        # Die Sicht führt nur Teilnehmer; wer dort fehlt, ist nach 04 §6.1 nicht MEMBER.
        pub = fresh.public_key().public_bytes_raw().hex()
        assert pub not in _membership(server, world.ex.N_gov)
    finally:
        server.shutdown()


def test_buergschaft(tmp_path) -> None:
    """Kriterium 7: ANNA n = 1 sagt used 101, CHRIS n = 50 sagt used 50; D aus der Policy (02 §3.1)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    limit = resolve_trust_params(scope=world.ex.N_res, genesis_obj=world.ex.genesis_res).D
    server = _start(path)
    try:
        effect = _sim(
            server,
            world.anna.pub,
            "vouch",
            scope=world.ex.N_res.hex(),
            subject=world.dora.pub.hex(),
            n=1,
            t_exp=1001000,
        )["effect"]
        assert effect == {"used": 101, "D": limit}
        assert limit == 100
        view = _get(server, f"/scopes/{world.ex.N_res.hex()}")
        over = {
            finding["subject"]
            for finding in view["vereinsleben"]["derivation"]["findings"]
            if finding["kind"] == "OVERCOMMITTED_AUTHOR"
        }
        assert (world.anna.pub.hex() in over) == (effect["used"] > effect["D"])

        effect = _sim(
            server,
            world.chris.pub,
            "vouch",
            scope=world.ex.N_res.hex(),
            subject=world.dora.pub.hex(),
            n=50,
            t_exp=1001000,
        )["effect"]
        assert effect == {"used": 50, "D": limit}
        view = _get(server, f"/scopes/{world.ex.N_res.hex()}")
        over = {
            finding["subject"]
            for finding in view["vereinsleben"]["derivation"]["findings"]
            if finding["kind"] == "OVERCOMMITTED_AUTHOR"
        }
        assert (world.chris.pub.hex() in over) == (effect["used"] > effect["D"])
    finally:
        server.shutdown()


def test_beitrag(tmp_path) -> None:
    """Kriterium 8: obligation sagt OPEN, die Quittung SETTLED; /obligations stimmt (03 §3.3.2)."""
    path = tmp_path / "bestand.sqlite"
    anlegen(path)
    world = build()
    server = _start(path)
    try:
        answered = _sim(
            server,
            world.dora.pub,
            "obligation",
            scope=world.ex.N_res.hex(),
            creditor=world.kasse.pub.hex(),
            amount=2400,
            unit="EUR-Cent",
        )
        assert answered["effect"] == {"settlement": "OPEN"}
        cid = answered["claim_id"]
        rows = {row["claim_id"]: row["state"] for row in _get(server, f"/obligations/{world.ex.N_res.hex()}")}
        assert rows[cid] == answered["effect"]["settlement"]

        effect = _sim(server, world.kasse.pub, "receipt", obligation=cid)["effect"]
        assert effect == {"settlement": "SETTLED"}
        rows = {row["claim_id"]: row["state"] for row in _get(server, f"/obligations/{world.ex.N_res.hex()}")}
        assert rows[cid] == effect["settlement"]
    finally:
        server.shutdown()
