"""Die Bindung an Reticulum: zwei Boten, zwei Knoten, eine Maschine (D584 Beschluss 1 und 4).

Fehlt ``rns``, ist das ein Fehler, kein übersprungener Test (D584 Beschluss 4).
"""

from __future__ import annotations

import re
import socket
import subprocess
import sys
import time

from symbolon.atom import signed_bytes
from symbolon.bote.draht import FORMWIDRIG, PFADE
from symbolon.bote.kern import HttpKnoten
from symbolon.bote.reticulum import adresse, anbieten, identitaet
from symbolon import cbor_canon
from tests.helpers import Identity, scope_id
from tests.node.test_abgleich import _bestand, _knoten, _soll, _url
from tests.node.test_api import _call, _start, _stop
from tools.verein_node import anlegen

_NOW = 1000
_FRIST = 40.0

_KOPF = "[reticulum]\n  enable_transport = No\n  share_instance = No\n[logging]\n  loglevel = 2\n"
_SERVER = (
    "[interfaces]\n  [[lab]]\n    type = TCPServerInterface\n    enabled = yes\n"
    "    listen_ip = 127.0.0.1\n    listen_port = {port}\n"
)
_CLIENT = (
    "[interfaces]\n  [[lab]]\n    type = TCPClientInterface\n    enabled = yes\n"
    "    target_host = 127.0.0.1\n    target_port = {port}\n"
)


class _Ziel:
    def __init__(self) -> None:
        self.pfade: list[str] = []

    def register_request_handler(self, pfad, antwort, _allow) -> None:
        self.pfade.append(pfad)
        if pfad == "claim":
            assert antwort("claim", b"\x00" * 31, b"", b"", None, 0.0) == cbor_canon.encode(
                [FORMWIDRIG]
            )


def test_anbieten_nur_lesen(tmp_path) -> None:
    """Genau die drei lesenden Pfade, keiner zum Einliefern (D584 Beschluss 2)."""
    x = _knoten(tmp_path / "x.sqlite")
    ziel = _Ziel()
    try:
        anbieten(ziel, HttpKnoten(_url(x)))
    finally:
        _stop(x)
    assert ziel.pfade == list(PFADE)


def test_adresse_bleibt(tmp_path) -> None:
    """Die Identität liegt in einer Datei; die Adresse bleibt über Starts gleich."""
    pfad = tmp_path / "bote.id"
    erste = adresse(identitaet(pfad))
    assert pfad.exists()
    assert adresse(identitaet(pfad)) == erste
    assert len(erste) == 16


def _frei() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _bote(tmp_path, name, knoten, konfig, nachbar: bytes) -> subprocess.Popen:
    rns = tmp_path / f"rns-{name}"
    rns.mkdir()
    (rns / "config").write_text(konfig)
    return subprocess.Popen(
        [
            sys.executable, "-m", "symbolon.bote", _url(knoten),
            "--rns", str(rns), "--identitaet", str(tmp_path / f"{name}.id"),
            "--nachbar", nachbar.hex(), "--takt", "0.5",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def _warten(bedingung) -> bool:
    begun = time.monotonic()
    while time.monotonic() - begun < _FRIST:
        if bedingung():
            return True
        time.sleep(0.25)
    return False


def test_zwei_boten(tmp_path) -> None:
    """B holt den Verein über Reticulum; A getrennt hält B an, verbunden holt B nach."""
    path_a = tmp_path / "a.sqlite"
    anlegen(path_a)
    soll = _soll(path_a)
    a = _start(path_a, lambda: _NOW)
    b = _knoten(tmp_path / "b.sqlite")
    port = _frei()
    adr_a = adresse(identitaet(tmp_path / "a.id"))
    adr_b = adresse(identitaet(tmp_path / "b.id"))
    boten = [
        _bote(tmp_path, "a", a, _KOPF + _SERVER.format(port=port), adr_b),
        _bote(tmp_path, "b", b, _KOPF + _CLIENT.format(port=port), adr_a),
    ]
    try:
        assert _warten(lambda: _bestand(b) == soll)
        assert _bestand(a) == soll
        status, _body = _call(a, "POST", "/getrennt", {"getrennt": True})
        assert status == 200
        neu = Identity("p36-A").vouch(
            Identity("p36-C"), n=4, scope=scope_id("p36-welt"), t=1, t_exp=5000
        )
        status, body = _call(a, "POST", "/claims", {"data": signed_bytes(neu).hex()})
        assert status == 200, body
        time.sleep(3)
        assert _bestand(b) == soll
        status, _body = _call(a, "POST", "/getrennt", {"getrennt": False})
        assert status == 200
        assert _warten(lambda: _bestand(b) == _bestand(a) != soll)
    finally:
        for bote in boten:
            bote.terminate()
        ausgaben = [bote.communicate(timeout=10)[0] for bote in boten]
        _stop(a)
        _stop(b)
    assert "Traceback" not in ausgaben[0] + ausgaben[1]
    geholt = sum(int(m) for m in re.findall(r"geholt=(\d+)", ausgaben[1]))
    assert geholt == len(soll["claims"]) + len(soll["objects"]) + 1
    assert re.findall(r"geholt=(\d+)", ausgaben[0]) == []
