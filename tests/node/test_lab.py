"""Das Lab über Reticulum: Schalter, Konfiguration, Warten, Verlauf, Boten (D588)."""

from __future__ import annotations

import re
import threading
import time

import pytest

from tests.node.test_abgleich import _bestand, _knoten, _soll, _url
from tests.node.test_api import _call, _start, _stop
from tools.netz import (
    Ausgabe,
    adressen_der,
    boten,
    gesperrt_gemeldet,
    instanz_bereit,
    instanz_name,
    rns_konfiguration,
    ruhe,
    schalter,
)
from tools.verein_node import anlegen

_NOW = 1000
_EIGENER_RAHMEN = r'File "[^"]*[/\\](symbolon|tools)[/\\]'


@pytest.mark.parametrize(
    ("argv", "erwartet"),
    [
        ([], (None, False)),
        (["--reticulum"], (None, True)),
        (["--personen"], ("--personen", False)),
        (["--versehen", "--reticulum"], ("--versehen", True)),
        (["--geraete", "--reticulum"], ("--geraete", True)),
        (["--aufloesen", "--reticulum"], ("--aufloesen", True)),
        (["--spaltung"], ("--spaltung", False)),
        (["--spaltung", "--reticulum"], ("--spaltung", True)),
        (["--ausweg", "--reticulum"], ("--ausweg", True)),
    ],
)
def test_schalter(argv, erwartet) -> None:
    """Eine Geschichte oder keine, ``--reticulum`` nur am Ende (D588)."""
    assert schalter(argv) == erwartet


@pytest.mark.parametrize(
    "argv",
    [
        ["--reticulum", "--personen"],
        ["--reticulum", "--reticulum"],
        ["--personen", "--geraete"],
        ["--http"],
        [""],
    ],
)
def test_schalter_abgelehnt(argv) -> None:
    with pytest.raises(SystemExit):
        schalter(argv)


def test_rns_konfiguration(tmp_path) -> None:
    """Gemeinsame Instanz ohne Schnittstelle, Name je Verzeichnis (D588)."""
    a = rns_konfiguration(tmp_path / "a")
    b = rns_konfiguration(tmp_path / "b")
    text_a = (a / "config").read_text(encoding="utf-8")
    text_b = (b / "config").read_text(encoding="utf-8")
    assert a == tmp_path / "a" / "rns"
    assert "share_instance = Yes" in text_a
    assert "enable_transport = No" in text_a
    assert text_a.rstrip().endswith("[interfaces]")
    name_a = re.search(r"instance_name = (symbolon-[0-9a-f]{12})\n", text_a).group(1)
    name_b = re.search(r"instance_name = (symbolon-[0-9a-f]{12})\n", text_b).group(1)
    assert name_a != name_b
    assert (rns_konfiguration(tmp_path / "a") / "config").read_text(encoding="utf-8") == text_a


def test_instanz_bereit(tmp_path) -> None:
    """Nur ein lauschender Socket mit genau diesem Namen zählt (D589)."""
    name = instanz_name(tmp_path)
    assert re.fullmatch(r"symbolon-[0-9a-f]{12}", name)
    tabelle = tmp_path / "unix"
    kopf = "Num       RefCount Protocol Flags    Type St Inode Path\n"
    tabelle.write_text(kopf + f"0000: 00000002 00000000 00010000 0001 01  5409 @rns/{name}/rpc\n")
    assert not instanz_bereit(name, tabelle)
    tabelle.write_text(kopf + f"0000: 00000002 00000000 00010000 0001 01  5408 @rns/{name}x\n")
    assert not instanz_bereit(name, tabelle)
    tabelle.write_text(kopf + f"0000: 00000002 00000000 00010000 0001 01  5408 @rns/{name}\n")
    assert instanz_bereit(name, tabelle)


def test_ruhe(tmp_path) -> None:
    """Gleicher Stand sofort; verschiedener nach der Frist None; getrennt zählt nicht (D588)."""
    path_a = tmp_path / "a.sqlite"
    anlegen(path_a)
    a = _start(path_a, lambda: _NOW)
    b = _knoten(tmp_path / "b.sqlite")
    c = _knoten(tmp_path / "c.sqlite")
    try:
        urls = [_url(b), _url(c)]
        dauer = ruhe(urls, frist=0.5)
        assert dauer is not None and dauer < 0.5
        urls = [_url(a), _url(b)]
        assert ruhe(urls, frist=0.5) is None
        status, _body = _call(b, "POST", "/getrennt", {"getrennt": True})
        assert status == 200
        assert ruhe(urls, frist=0.5) is not None
    finally:
        _stop(a)
        _stop(b)
        _stop(c)


def test_ausgabe(tmp_path) -> None:
    """Jede Zeile auf den Schirm und in den Verlauf, auch aus mehreren Fäden (D588 Beschluss 3)."""
    ausgeben = Ausgabe(tmp_path / "verlauf.txt")
    faeden = [
        threading.Thread(target=lambda n=n: [ausgeben(f"{n}-{i}") for i in range(50)])
        for n in range(4)
    ]
    for faden in faeden:
        faden.start()
    for faden in faeden:
        faden.join()
    zeilen = (tmp_path / "verlauf.txt").read_text(encoding="utf-8").splitlines()
    assert sorted(zeilen) == sorted(f"{n}-{i}" for n in range(4) for i in range(50))


def test_boten(tmp_path) -> None:
    """Zwei Geräte, eine gemeinsame Instanz: B kommt auf den Stand von A (D588 Beschluss 4)."""
    path_a = tmp_path / "a.sqlite"
    anlegen(path_a)
    soll = _soll(path_a)
    a = _start(path_a, lambda: _NOW)
    b = _knoten(tmp_path / "b.sqlite")
    geraete = [("Gerät A", "a.sqlite", frozenset()), ("Gerät B", "b.sqlite", frozenset())]
    zeilen: list[str] = []
    prozesse = boten(tmp_path, geraete, [_url(a), _url(b)], zeilen.append)
    try:
        assert ruhe([_url(a), _url(b)], frist=40.0) is not None
        assert _bestand(b) == soll
        assert _bestand(a) == soll
        ende = time.monotonic() + 10
        while not any(z.startswith("Gerät B ← Gerät A: geholt=") for z in zeilen):
            assert time.monotonic() < ende, zeilen
            time.sleep(0.1)
    finally:
        for prozess in prozesse:
            prozess.terminate()
        for prozess in prozesse:
            prozess.wait(timeout=10)
        _stop(a)
        _stop(b)
    assert any(zeile.startswith("Gerät B ← Gerät A: geholt=") for zeile in zeilen), zeilen
    assert not any(zeile.startswith("Gerät A ← ") and "geholt=0" not in zeile for zeile in zeilen)
    assert re.search(_EIGENER_RAHMEN, "\n".join(zeilen)) is None
    assert (tmp_path / "rns" / "config").exists()
    assert (tmp_path / "a.sqlite.id").exists() and (tmp_path / "b.sqlite.id").exists()


def test_boten_sperren(tmp_path) -> None:
    """B sperrt A: B bleibt ohne den Verein und meldet es; entsperrt holt B nach (D594 B. 3)."""
    path_a = tmp_path / "a.sqlite"
    anlegen(path_a)
    soll = _soll(path_a)
    a = _start(path_a, lambda: _NOW)
    b = _knoten(tmp_path / "b.sqlite")
    leer = _bestand(b)
    geraete = [("Gerät A", "a.sqlite", frozenset()), ("Gerät B", "b.sqlite", frozenset())]
    adr_a, _adr_b = adressen_der(tmp_path, geraete)
    (tmp_path / "sperren").mkdir()
    (tmp_path / "sperren" / "b.sqlite.txt").write_text(adr_a + "\n", encoding="utf-8")
    zeilen: list[str] = []
    stand: dict[str, int | None] = {}
    prozesse = boten(tmp_path, geraete, [_url(a), _url(b)], zeilen.append, stand)
    try:
        assert gesperrt_gemeldet(stand, {"Gerät B": 1}, frist=40.0), zeilen
        assert ruhe([_url(a), _url(b)], frist=5.0) is None
        assert _bestand(b) == leer
        (tmp_path / "sperren" / "b.sqlite.txt").write_text("", encoding="utf-8")
        assert gesperrt_gemeldet(stand, {"Gerät B": 0}, frist=40.0), zeilen
        assert ruhe([_url(a), _url(b)], frist=40.0) is not None
        assert _bestand(b) == soll
    finally:
        for prozess in prozesse:
            prozess.terminate()
        for prozess in prozesse:
            prozess.wait(timeout=10)
        _stop(a)
        _stop(b)
    assert "Gerät B: gesperrt=1" in zeilen and "Gerät B: gesperrt=0" in zeilen, zeilen
    assert "Gerät A: gesperrt=1" not in zeilen, zeilen
    gesperrt_ab = zeilen.index("Gerät B: gesperrt=1")
    frei_ab = zeilen.index("Gerät B: gesperrt=0")
    assert not [z for z in zeilen[gesperrt_ab:frei_ab] if z.startswith("Gerät B ← Gerät A")], zeilen
