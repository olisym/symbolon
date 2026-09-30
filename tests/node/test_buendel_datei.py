"""Ein Bündel als Datei über die HTTP-Schnittstelle (D614 Beschluss 5)."""

from __future__ import annotations

from tests.node.test_abgleich import _bestand, _knoten, _soll, _url
from tests.node.test_api import _call, _start, _stop
from symbolon import buendel
from symbolon.bote.kern import HttpKnoten
from symbolon.buendel import GRENZE
from tools import buendel as werkzeug
from tools.verein_node import anlegen

_NOW = 1000


def test_datei_hin_und_zurueck(tmp_path, capsys) -> None:
    """Der Verein geht über eine Datei ganz mit; ein zweites Lesen bringt nichts Neues."""
    path_a = tmp_path / "a.sqlite"
    anlegen(path_a)
    soll = _soll(path_a)
    a = _start(path_a, lambda: _NOW)
    b = _knoten(tmp_path / "b.sqlite")
    datei = tmp_path / "verein.buendel"
    n = len(soll["claims"]) + len(soll["objects"])
    try:
        assert werkzeug.main(["x", "schreiben", _url(a), str(datei)]) == 0
        zeile = capsys.readouterr().out.strip()
        assert zeile == (
            f"claims={len(soll['claims'])} objekte={len(soll['objects'])} "
            f"bytes={datei.stat().st_size}"
        )
        assert werkzeug.main(["x", "lesen", _url(b), str(datei)]) == 0
        assert capsys.readouterr().out.strip() == f"eingeliefert={n} neu={n} abgewiesen={{}}"
        assert _bestand(b) == soll
        assert werkzeug.main(["x", "lesen", _url(b), str(datei)]) == 0
        assert capsys.readouterr().out.strip() == f"eingeliefert={n} neu=0 abgewiesen={{}}"
    finally:
        _stop(a)
        _stop(b)


def test_datei_formwidrig_und_getrennt(tmp_path, capsys) -> None:
    """Eine formwidrige Datei und ein getrennter Knoten enden mit 1 und einer Zeile."""
    b = _knoten(tmp_path / "b.sqlite")
    datei = tmp_path / "kaputt.buendel"
    datei.write_bytes(b"\xff")
    try:
        assert werkzeug.main(["x", "lesen", _url(b), str(datei)]) == 1
        assert capsys.readouterr().out.strip() == "formwidrig"
        assert werkzeug.main(["x", "lesen", _url(b), str(tmp_path / "fehlt")]) == 1
        assert capsys.readouterr().out.strip().startswith("datei: ")
        status, _body = _call(b, "POST", "/getrennt", {"getrennt": True})
        assert status == 200
        assert werkzeug.main(["x", "schreiben", _url(b), str(datei)]) == 1
        assert capsys.readouterr().out.strip() == "getrennt"
        assert datei.read_bytes() == b"\xff"
    finally:
        _stop(b)


def test_aufruf_falsch(capsys) -> None:
    """Ein falscher Aufruf endet mit 2."""
    assert werkzeug.main(["x", "senden", "http://127.0.0.1:1", "d"]) == 2
    assert capsys.readouterr().out.startswith("aufruf: ")


class _Gross(HttpKnoten):
    """Ein Knoten-Ersatz, dessen Bestand über ``GRENZE`` liegt; ein Claim ist verschwunden."""

    def bestand(self):
        return [bytes([1]) * 32, bytes([2]) * 32, bytes([3]) * 32], [bytes([4]) * 32]

    def claim(self, cid: bytes):
        return None if cid[0] == 3 else bytes([cid[0]]) * (GRENZE // 3)

    def objekt(self, _digest: bytes):
        return "proposal", b"o" * (GRENZE // 3)


def test_datei_zaehlt_was_darin_steht(tmp_path, monkeypatch, capsys) -> None:
    """Die Zeile zählt den Inhalt der Datei; was fehlt, steht als ``weggelassen`` (D615)."""
    monkeypatch.setattr(werkzeug, "HttpKnoten", _Gross)
    datei = tmp_path / "gross.buendel"
    assert werkzeug.main(["x", "schreiben", "http://gross", str(datei)]) == 0
    assert capsys.readouterr().out.strip() == (
        f"claims=1 objekte=1 bytes={datei.stat().st_size} weggelassen=2"
    )
    claims, objekte = buendel.lesen(datei.read_bytes())
    assert (len(claims), len(objekte)) == (1, 1)
