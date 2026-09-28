"""Der Ausweg nach der Spaltung: die Sperre als Absicht und das Bild (D596)."""

from __future__ import annotations

import json

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_from_map
from tests.node.test_abgleich import _url
from tests.node.test_api import _call, _stop
from tests.node.test_personen import _ausgang
from tests.node.test_spaltung import _lage
from tests.node.test_versehen import _start
from tools.netz import GERAETE_GERAETE, WEST, durchgang, gruppen
from tools.personen import ANTRAG, AUSWEG, SPALTUNG, takt_spaltung
from tools.verein import build
from tools.verein_node import anlegen

_NOW = 1000
_NACHLAUF = 3


def _brunos_geraet(tmp_path):
    """Brunos Gerät aus Bild (c): es hält BRUNOs Schlüssel und kennt sein Zweitgerät."""
    name, datei, personen = GERAETE_GERAETE[1]
    assert name == "Brunos Gerät"
    anlegen(tmp_path / datei, personen, geraete=True)
    return _start(tmp_path / datei, name, lambda: _NOW)


def _namen(server) -> dict[str, str]:
    status, body = _call(server, "GET", "/names")
    assert status == 200, body
    return {eintrag["name"]: eintrag["I"] for eintrag in json.loads(body)}


def _kern(body: bytes) -> Claim:
    """Der vorbereitete Claim aus der Antwort von /intent."""
    return claim_from_map(cbor_canon.decode(bytes.fromhex(json.loads(body)["core"])))


def _sperre(namen: dict[str, str], wer: str, geraet: str, **mehr) -> dict:
    return {
        "I": namen[wer],
        "art": "device-end",
        "scope": build().ex.N_gov.hex(),
        "device": namen[geraet],
        **mehr,
    }


def test_sperre_felder(tmp_path) -> None:
    """Die Wurzel sperrt ihr Gerät: device-end@1, J nennt das Gerät; ohne keep kein v (D596 B. 2)."""
    server = _brunos_geraet(tmp_path)
    try:
        namen = _namen(server)
        scope = build().ex.N_gov.hex()
        status, body = _call(
            server, "POST", "/intent", _sperre(namen, "BRUNO", "BRUNO (Zweitgerät)")
        )
        assert status == 200, body
        antwort = json.loads(body)
        assert antwort["warnings"] == []
        assert antwort["effect"] is None
        claim = _kern(body)
        assert claim.I == bytes.fromhex(namen["BRUNO"])
        assert claim.p == f"nuc:{scope}/device-end@1"
        assert claim.J == (1, bytes.fromhex(namen["BRUNO (Zweitgerät)"]))
        assert claim.N == bytes.fromhex(scope)
        assert claim.v is None
        status, body = _call(server, "GET", f"/tips/{namen['BRUNO (Zweitgerät)']}")
        assert status == 200, body
        (spitze,) = json.loads(body)
        status, body = _call(
            server,
            "POST",
            "/intent",
            _sperre(namen, "BRUNO", "BRUNO (Zweitgerät)", keep=spitze),
        )
        assert status == 200, body
        assert _kern(body).v == cbor_canon.encode({0: bytes.fromhex(spitze)})
    finally:
        _stop(server)


def test_sperre_nur_eigenes_geraet(tmp_path) -> None:
    """Nur die Wurzel sperrt, nur ein wirksam aufgenommenes Gerät (D596 Beschluss 2)."""
    server = _brunos_geraet(tmp_path)
    try:
        namen = _namen(server)
        for wer, geraet in [
            ("ANNA", "BRUNO (Zweitgerät)"),
            ("BRUNO (Zweitgerät)", "BRUNO (Zweitgerät)"),
            ("BRUNO", "DORA (Zweitgerät)"),
            ("BRUNO", "BRUNO"),
        ]:
            status, body = _call(server, "POST", "/intent", _sperre(namen, wer, geraet))
            assert (status, json.loads(body)) == (400, "NOT_OWN_DEVICE"), (wer, geraet)
    finally:
        _stop(server)


def test_sperre_keep_fremd(tmp_path) -> None:
    """keep muss ein bekannter Claim des Geräts sein (D596 Beschluss 2)."""
    server = _brunos_geraet(tmp_path)
    try:
        namen = _namen(server)
        status, body = _call(server, "GET", f"/tips/{namen['BRUNO']}")
        assert status == 200, body
        (fremd,) = json.loads(body)
        for keep in ["00" * 32, fremd]:
            status, body = _call(
                server,
                "POST",
                "/intent",
                _sperre(namen, "BRUNO", "BRUNO (Zweitgerät)", keep=keep),
            )
            assert (status, json.loads(body)) == (400, "UNKNOWN_CLAIM"), keep
        status, body = _call(
            server, "POST", "/intent", _sperre(namen, "BRUNO", "BRUNO (Zweitgerät)", keep="zz")
        )
        assert status == 400, body
    finally:
        _stop(server)


def test_sperre_wirkt(tmp_path) -> None:
    """Nach der Sperre warnt eine Stimme des Geräts mit DEVICE_ENDED (D596 B. 2, D556 B. 3)."""
    server = _brunos_geraet(tmp_path)
    try:
        namen = _namen(server)
        scope = build().ex.N_gov.hex()
        status, body = _call(
            server,
            "POST",
            "/sim/intent",
            {"I": namen["BRUNO"], "art": "propose", "scope": scope, "change": ANTRAG},
        )
        assert status == 200, body
        status, body = _call(server, "GET", f"/tasks/{namen['BRUNO']}")
        assert status == 200, body
        (vorschlag,) = [a["proposal"] for a in json.loads(body) if a["art"] == "VOTE"]
        stimme = {
            "I": namen["BRUNO (Zweitgerät)"],
            "art": "vote",
            "proposal": vorschlag,
            "choice": "yes",
        }
        status, body = _call(server, "POST", "/intent", stimme)
        assert status == 200, body
        assert "DEVICE_ENDED" not in json.loads(body)["warnings"]
        status, body = _call(
            server, "POST", "/sim/intent", _sperre(namen, "BRUNO", "BRUNO (Zweitgerät)")
        )
        assert status == 200, body
        status, body = _call(server, "POST", "/intent", stimme)
        assert status == 200, body
        assert "DEVICE_ENDED" in json.loads(body)["warnings"]
    finally:
        _stop(server)


def test_bild_ausweg(tmp_path) -> None:
    """Bruno sperrt: es gilt nichts; Dora sperrt: Annas Beschluss gilt überall (D596 B. 3)."""
    ausgang = _ausgang(tmp_path)
    jetzt = {"t": _NOW}
    knoten = []
    for name, datei, personen in GERAETE_GERAETE:
        anlegen(tmp_path / datei, personen, geraete=True)
        knoten.append(_start(tmp_path / datei, name, lambda: jetzt["t"]))
    try:
        urls = [_url(server) for server in knoten]
        zeilen: list[str] = []
        teile = gruppen(GERAETE_GERAETE, False)
        for nummer in range(SPALTUNG[1] + 1):
            jetzt["t"] = _NOW + nummer
            if nummer in SPALTUNG:
                teile = gruppen(GERAETE_GERAETE, nummer == SPALTUNG[0])
            zeilen += takt_spaltung(urls, nummer, GERAETE_GERAETE, ausweg=True)
            durchgang(urls, teile)
        assert {_lage(server)[:2] for server in knoten} == {(ausgang, None)}
        (erste, zweite) = AUSWEG
        assert SPALTUNG[1] < erste[0] < zweite[0]
        for nummer in range(SPALTUNG[1] + 1, erste[0] + 1):
            jetzt["t"] = _NOW + nummer
            zeilen += takt_spaltung(urls, nummer, GERAETE_GERAETE, ausweg=True)
            durchgang(urls, teile)
        assert {_lage(server)[:2] for server in knoten} == {(ausgang, None)}
        for nummer in range(erste[0] + 1, zweite[0] + 1):
            jetzt["t"] = _NOW + nummer
            zeilen += takt_spaltung(urls, nummer, GERAETE_GERAETE, ausweg=True)
            durchgang(urls, teile)
        text = ANTRAG["set"]["text"]
        assert {_lage(server)[:2] for server in knoten} == {(ausgang + 1, text)}
        sperren = [z for z in zeilen if z.endswith("sperrt das Zweitgerät")]
        assert sperren == [
            f"Takt {erste[0]}, Brunos Gerät: BRUNO sperrt das Zweitgerät",
            f"Takt {zweite[0]}, Doras Gerät: DORA sperrt das Zweitgerät",
        ], zeilen
        assert erste[1] in WEST and zweite[1] in WEST
        assert not [z for z in zeilen if "abgewiesen" in z], zeilen
        for nummer in range(zweite[0] + 1, zweite[0] + 1 + _NACHLAUF):
            jetzt["t"] = _NOW + nummer
            assert takt_spaltung(urls, nummer, GERAETE_GERAETE, ausweg=True) == []
            assert durchgang(urls, teile) == 0
    finally:
        for server in knoten:
            _stop(server)
