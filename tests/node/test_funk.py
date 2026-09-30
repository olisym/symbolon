"""Der Funkkanal und das Lab über Funk (D611 Beschluss 4)."""

from __future__ import annotations

import json
import random
import re
import time

import pytest

from symbolon.bote.kern import HttpKnoten
from tests.node.test_abgleich import _bestand, _knoten, _soll, _url
from tests.node.test_api import _call, _start, _stop
from tools.funk import Kanal
from tools.netz import boten, ruhe
from tools.verein_node import anlegen

_NOW = 1000


def test_senden_nacheinander() -> None:
    """Einer sendet zur Zeit; die Sendezeit ist Bytes mal 8 durch die Bitrate."""
    kanal = Kanal(8000, 0.0, 0)
    assert kanal.senden(0.0, bytes(1000)) == 1.0
    assert kanal.senden(0.5, bytes(1000)) == 2.0
    assert kanal.senden(5.0, bytes(100)) == 5.1
    assert (kanal.pakete, kanal.bytes, kanal.ankuendigungen) == (3, 2100, 0)
    kanal.senden(6.0, bytes([0x01]) + bytes(99))
    assert kanal.ankuendigungen == 1


def test_nie_an_den_sender() -> None:
    """Ohne Verlust hört jeder andere, nie der Sender (D610 Befund 1)."""
    assert Kanal(1000, 0.0, 0).empfaenger(1, 4) == [0, 2, 3]


def test_verlust_mit_samen() -> None:
    """Der Verlust folgt dem Zufall mit festem Samen, je Empfänger gezogen."""
    kanal = Kanal(1000, 0.3, 7)
    zufall = random.Random(7)
    erwartet_verloren = 0
    for _ in range(200):
        hoeren = kanal.empfaenger(0, 3)
        soll = [ziel for ziel in (1, 2) if not zufall.random() < 0.3]
        erwartet_verloren += 2 - len(soll)
        assert hoeren == soll
    assert kanal.verloren == erwartet_verloren > 0


@pytest.mark.parametrize(("bitrate", "verlust"), [(0, 0.0), (-1, 0.0), (1000, 1.0), (1000, -0.1)])
def test_werte(bitrate, verlust) -> None:
    with pytest.raises(ValueError):
        Kanal(bitrate, verlust, 0)


def test_bericht() -> None:
    kanal = Kanal(1000, 0.0, 0)
    kanal.senden(0.0, bytes([0x01, 0]))
    assert kanal.bericht() == "funk pakete=1 bytes=2 verloren=0 ankuendigungen=1"


def test_stand(tmp_path) -> None:
    """``HttpKnoten.stand`` ist der Stand aus ``/stand`` (D611 Beschluss 1)."""
    datei = tmp_path / "a.sqlite"
    anlegen(datei)
    server = _start(datei, lambda: _NOW)
    try:
        status, body = _call(server, "GET", "/stand")
        assert status == 200
        assert HttpKnoten(_url(server)).stand() == bytes.fromhex(json.loads(body))
    finally:
        _stop(server)


def _ankuendigungen(zeilen: list[str]) -> list[int]:
    return [int(m) for z in zeilen for m in re.findall(r"^funk .*ankuendigungen=(\d+)$", z)]


def test_drei_ueber_funk(tmp_path) -> None:
    """Drei Geräte über den Kanal: B und C holen den Verein von A; danach kündigen die Boten
    nach Trickle selten an, statt in jedem Takt (D611 Beschluss 1 und 4)."""
    path_a = tmp_path / "a.sqlite"
    anlegen(path_a)
    soll = _soll(path_a)
    a = _start(path_a, lambda: _NOW)
    b = _knoten(tmp_path / "b.sqlite")
    c = _knoten(tmp_path / "c.sqlite")
    urls = [_url(a), _url(b), _url(c)]
    geraete = [
        ("Gerät A", "a.sqlite", frozenset()),
        ("Gerät B", "b.sqlite", frozenset()),
        ("Gerät C", "c.sqlite", frozenset()),
    ]
    zeilen: list[str] = []
    prozesse = boten(tmp_path, geraete, urls, zeilen.append, funk=(50000, 0.05))
    try:
        assert ruhe(urls, frist=120.0) is not None, zeilen
        assert _bestand(b) == soll and _bestand(c) == soll
        # Ruhe: zwischen zwei Berichten des Kanals, 20 s auseinander, höchstens zehn
        # Ankündigungen; wer in jedem Takt von 1 s ankündigte, käme auf sechzig.
        ende = time.monotonic() + 15
        while len(_ankuendigungen(zeilen)) < 1:
            assert time.monotonic() < ende, zeilen
            time.sleep(0.2)
        erste = len(_ankuendigungen(zeilen))
        time.sleep(20.5)
        zaehler = _ankuendigungen(zeilen)
        assert len(zaehler) >= erste + 2, zeilen
        assert zaehler[erste + 1] - zaehler[erste - 1] <= 10, zaehler
    finally:
        for prozess in prozesse:
            prozess.terminate()
        for prozess in prozesse:
            prozess.wait(timeout=10)
        _stop(a)
        _stop(b)
        _stop(c)
