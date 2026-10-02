"""Die Bindung an Reticulum: zwei Boten, zwei Knoten, eine Maschine (D584 Beschluss 1 und 4).

Fehlt ``rns``, ist das ein Fehler, kein übersprungener Test (D584 Beschluss 4).
"""

from __future__ import annotations

import re
import socket
import subprocess
import sys
import time

import pytest
import RNS

from symbolon.atom import signed_bytes
from symbolon.bote.draht import FORMWIDRIG, PFADE
from symbolon.bote import reticulum
from symbolon.bote.trickle import Zeiten
from symbolon.bote.kern import Getrennt, HttpKnoten
from symbolon.bote.reticulum import adresse, anbieten, identitaet
from symbolon import cbor_canon
from tests.helpers import Identity, scope_id
from tests.node.test_abgleich import _bestand, _knoten, _soll, _url
from tests.node.test_api import _call, _start, _stop
from tools.verein_node import anlegen

_NOW = 1000
_EIGENER_RAHMEN = r'File "[^"]*[/\\]symbolon[/\\]bote[/\\]'
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
        if pfad == "paket":
            assert antwort("paket", [[b"\x00" * 31], []], b"", b"", None, 0.0) == cbor_canon.encode(
                [FORMWIDRIG]
            )
        if pfad == "abgleich":
            assert antwort("abgleich", b"\xff", b"", b"", None, 0.0) == cbor_canon.encode(
                [FORMWIDRIG]
            )


def test_anbieten_nur_lesen(tmp_path) -> None:
    """Genau die lesenden Pfade, keiner zum Einliefern (D584 Beschluss 2)."""
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
    """B holt den Verein über Reticulum; A getrennt hält B an, verbunden holt B nach.

    Was in A entsteht, hört B als Rundruf, sobald A verbunden ist (D636 Beschluss 1 und 2).
    """
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
        vorher = _bestand(a)
        eigener = Identity("p36-B").vouch(
            Identity("p36-C"), n=4, scope=scope_id("p36-welt"), t=1, t_exp=5000
        )
        status, body = _call(a, "POST", "/claims", {"data": signed_bytes(eigener).hex()})
        assert status == 200, body
        assert _warten(lambda: _bestand(b) == _bestand(a) != vorher)
    finally:
        for bote in boten:
            bote.terminate()
        ausgaben = [bote.communicate(timeout=10)[0] for bote in boten]
        _stop(a)
        _stop(b)
    assert re.search(_EIGENER_RAHMEN, ausgaben[0] + ausgaben[1]) is None
    geholt = sum(int(m) for m in re.findall(r"geholt=(\d+)", ausgaben[1]))
    assert geholt == len(soll["claims"]) + len(soll["objects"]) + 2
    # Beide Einträge, die in A entstanden, kamen als Rundruf, der erste nach der Trennung
    # (D636 Beschluss 1 und 2).
    assert re.findall(r"rundruf geholt=(\d+)", ausgaben[1]) == ["1", "1"]
    assert re.findall(r"geholt=(\d+)", ausgaben[0]) == []


def test_nachbar_mehrfach(tmp_path, monkeypatch) -> None:
    """``--nachbar`` nimmt mehrere Werte und lässt sich wiederholen; keiner geht verloren (D586)."""
    from symbolon.bote import __main__ as start
    from symbolon.bote import reticulum

    gerufen = []
    monkeypatch.setattr(reticulum, "laufen", lambda *args: gerufen.append(args))
    start.main(
        [
            "http://127.0.0.1:1",
            "--identitaet", str(tmp_path / "x.id"),
            "--rns", str(tmp_path),
            "--nachbar", "aa", "bb",
            "--nachbar", "cc",
        ]
    )
    assert [args[3] for args in gerufen] == [[b"\xaa", b"\xbb", b"\xcc"]]


class _Quittung:
    """Eine Anfrage, die nach ``dauer`` Sekunden mit ``status`` endet; ``steigt`` meldet Fortschritt."""

    def __init__(self, dauer: float, status: int, antwort: bytes, steigt: bool) -> None:
        self.ende = time.monotonic() + dauer
        self.status = status
        self.antwort = antwort
        self.steigt = steigt

    def get_progress(self) -> float:
        return time.monotonic() if self.steigt else 0.0

    def concluded(self) -> bool:
        return time.monotonic() >= self.ende

    def get_status(self) -> int:
        return self.status

    def get_response(self) -> bytes:
        return self.antwort


class _Link:
    status = RNS.Link.ACTIVE

    def __init__(self, quittung: _Quittung) -> None:
        self.quittung = quittung
        self.abgebaut = False

    def request(self, _pfad, _data):
        return self.quittung

    def teardown(self) -> None:
        self.abgebaut = True


def test_antwort_frist() -> None:
    """Ohne Fortschritt ist eine Anfrage nach der Frist getrennt, der Link abgebaut (D586)."""
    link = _Link(_Quittung(2.0, RNS.RequestReceipt.FAILED, b"", steigt=False))
    nachbar = reticulum.RnsNachbar(bytes(16), Zeiten(10.0, 0.2, 10.0))
    nachbar._link = link
    begun = time.monotonic()
    with pytest.raises(Getrennt):
        nachbar.bestand()
    assert time.monotonic() - begun < 1.0
    assert link.abgebaut
    assert nachbar._link is None


def test_antwort_mit_fortschritt() -> None:
    """Solange die Antwort fortschreitet, läuft die Frist neu; die Antwort kommt an (D586)."""
    gut = cbor_canon.encode([0, [[], []]])
    link = _Link(_Quittung(0.6, RNS.RequestReceipt.READY, gut, steigt=True))
    nachbar = reticulum.RnsNachbar(bytes(16), Zeiten(10.0, 0.2, 10.0))
    nachbar._link = link
    assert nachbar.bestand() == ([], [])
    assert not link.abgebaut


class _Stockend(_Quittung):
    """Fortschritt bis ``stockt_ab``, danach keiner mehr."""

    def __init__(self, stockt_ab: float, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.stockt_ab = stockt_ab

    def get_progress(self) -> float:
        return min(time.monotonic(), self.stockt_ab)


def test_antwort_stockt_nach_fortschritt() -> None:
    """Stockt die Antwort nach Fortschritt kürzer als die Frist, kommt sie an (D587)."""
    gut = cbor_canon.encode([0, [[], []]])
    begun = time.monotonic()
    quittung = _Stockend(begun + 1.0, 1.2, RNS.RequestReceipt.READY, gut, steigt=True)
    link = _Link(quittung)
    nachbar = reticulum.RnsNachbar(bytes(16), Zeiten(10.0, 0.5, 10.0))
    nachbar._link = link
    assert nachbar.bestand() == ([], [])
    assert time.monotonic() - begun >= 1.0
    assert not link.abgebaut


class _Folge:
    """Ein Link, dessen Anfragen der Reihe nach die gegebenen Quittungen liefern."""

    status = RNS.Link.ACTIVE

    def __init__(self, quittungen: list[_Quittung], rtt: float = 0.001) -> None:
        self.quittungen = quittungen
        self.rtt = rtt
        self.anfragen = 0
        self.abgebaut = False

    def request(self, _pfad, _data):
        self.anfragen += 1
        return self.quittungen.pop(0)

    def teardown(self) -> None:
        self.abgebaut = True


def _verloren() -> _Quittung:
    return _Quittung(1000.0, RNS.RequestReceipt.SENT, b"", steigt=False)


def _gut(dauer: float = 0.05) -> _Quittung:
    gut = cbor_canon.encode([0, [[], []]])
    return _Quittung(dauer, RNS.RequestReceipt.READY, gut, steigt=False)


def _nachbar(link: _Folge, zeit: Zeiten | None = None) -> reticulum.RnsNachbar:
    """Ein Nachbar, dessen Link schon einmal geantwortet hat (D631 Beschluss 1)."""
    nachbar = reticulum.RnsNachbar(bytes(16), zeit)
    nachbar._link = link
    nachbar._beantwortet = link
    return nachbar


def test_erneut_nach_verlust(monkeypatch) -> None:
    """Bleibt eine Anfrage unzugestellt, geht sie erneut; auf einem Link, der schon geantwortet
    hat, auf demselben (D591, D631)."""
    monkeypatch.setattr(reticulum, "_ZUSTELL_MIN", 0.1)
    link = _Folge([_verloren(), _gut()])
    begun = time.monotonic()
    assert _nachbar(link).bestand() == ([], [])
    assert time.monotonic() - begun < 1.0
    assert link.anfragen == 2
    assert not link.abgebaut


def test_versuche_begrenzt(monkeypatch) -> None:
    """Höchstens ``_VERSUCHE`` Anfragen; die Frist läuft ab der ersten, dann getrennt (D591, D625).

    Ein erneutes Senden startet die Antwortfrist nicht neu: getrennt nach rund 0,3 s, nicht nach
    0,5 s.
    """
    monkeypatch.setattr(reticulum, "_ZUSTELL_MIN", 0.1)
    link = _Folge([_verloren() for _ in range(5)])
    begun = time.monotonic()
    with pytest.raises(Getrennt):
        _nachbar(link, Zeiten(10.0, 0.3, 10.0)).bestand()
    dauer = time.monotonic() - begun
    assert 0.3 <= dauer < 0.45
    assert link.anfragen == reticulum._VERSUCHE == 3
    assert link.abgebaut


def test_zugestellt_nicht_erneut(monkeypatch) -> None:
    """Eine zugestellte Anfrage ohne Fortschritt geht nicht erneut (D591)."""
    monkeypatch.setattr(reticulum, "_ZUSTELL_MIN", 0.05)

    class _Spaet(_Quittung):
        def get_status(self) -> int:
            return RNS.RequestReceipt.READY if self.concluded() else RNS.RequestReceipt.DELIVERED

    gut = cbor_canon.encode([0, [[], []]])
    link = _Folge([_Spaet(0.4, RNS.RequestReceipt.READY, gut, steigt=False)])
    assert _nachbar(link).bestand() == ([], [])
    assert link.anfragen == 1


def test_zustellfrist_waechst_mit_rtt(monkeypatch) -> None:
    """Die Frist bis zum erneuten Senden folgt der gemessenen Laufzeit des Links (D591)."""
    monkeypatch.setattr(reticulum, "_ZUSTELL_MIN", 0.1)
    link = _Folge([_verloren(), _gut()], rtt=0.05)
    begun = time.monotonic()
    assert _nachbar(link).bestand() == ([], [])
    assert time.monotonic() - begun >= 1.0
    assert link.anfragen == 2


def test_zustellfrist_gedeckelt(monkeypatch) -> None:
    """Eine lange Laufzeit schiebt das erneute Senden nicht hinter die Antwortfrist (D625)."""
    monkeypatch.setattr(reticulum, "_ZUSTELL_MIN", 0.1)
    link = _Folge([_verloren(), _gut()], rtt=10.0)
    begun = time.monotonic()
    assert _nachbar(link, Zeiten(10.0, 0.6, 10.0)).bestand() == ([], [])
    assert time.monotonic() - begun < 0.6
    assert link.anfragen == 2


class _Ausgang:
    """Ein Ziel ohne RNS; trägt nur die Konstanten, die ``_verbinden`` liest."""

    OUT = RNS.Destination.OUT
    SINGLE = RNS.Destination.SINGLE

    def __init__(self, *_args) -> None:
        pass


class _Geschlossen:
    """Ein Link, den RNS beim Aufbau schliesst."""

    ACTIVE = RNS.Link.ACTIVE
    CLOSED = RNS.Link.CLOSED

    def __init__(self, _ziel) -> None:
        self.status = RNS.Link.CLOSED


def test_geschlossener_link_sofort_getrennt(monkeypatch) -> None:
    """Schliesst RNS den Link beim Aufbau, ist der Nachbar sofort getrennt, nicht erst nach der
    Frist für den Link (D625)."""
    monkeypatch.setattr(reticulum.RNS.Transport, "has_path", lambda _ziel: True)
    monkeypatch.setattr(reticulum.RNS.Identity, "recall", lambda _ziel: object())
    monkeypatch.setattr(reticulum.RNS, "Destination", _Ausgang)
    monkeypatch.setattr(reticulum.RNS, "Link", _Geschlossen)
    nachbar = reticulum.RnsNachbar(bytes(16), Zeiten(5.0, 15.0, 10.0))
    begun = time.monotonic()
    with pytest.raises(Getrennt):
        nachbar.bestand()
    assert time.monotonic() - begun < 1.0


def _frisch(link: _Folge, zeit: Zeiten | None = None) -> reticulum.RnsNachbar:
    """Ein Nachbar, dessen Link noch nie geantwortet hat (D631 Beschluss 1)."""
    nachbar = reticulum.RnsNachbar(bytes(16), zeit)
    nachbar._link = link
    return nachbar


def _aufbau(monkeypatch, links: list) -> None:
    """``RNS.Link(ziel)`` liefert der Reihe nach die gegebenen Links, ohne RNS."""

    class _Fabrik:
        ACTIVE = RNS.Link.ACTIVE
        CLOSED = RNS.Link.CLOSED

        def __new__(cls, _ziel):
            return links.pop(0)

    monkeypatch.setattr(reticulum.RNS.Transport, "has_path", lambda _ziel: True)
    monkeypatch.setattr(reticulum.RNS.Identity, "recall", lambda _ziel: object())
    monkeypatch.setattr(reticulum.RNS, "Destination", _Ausgang)
    monkeypatch.setattr(reticulum.RNS, "Link", _Fabrik)


def test_frischer_link_ohne_antwort_neu(monkeypatch) -> None:
    """Bleibt die Anfrage auf einem Link ohne Antwort, der noch nie geantwortet hat, wird er
    abgebaut, und sie geht über einen neuen (D631 Beschluss 1)."""
    monkeypatch.setattr(reticulum, "_ZUSTELL_MIN", 0.1)
    erster = _Folge([_verloren(), _verloren(), _verloren()])
    zweiter = _Folge([_gut()])
    uebrig = [zweiter]
    _aufbau(monkeypatch, uebrig)
    nachbar = _frisch(erster)
    begun = time.monotonic()
    assert nachbar.bestand() == ([], [])
    assert time.monotonic() - begun < 1.0
    assert erster.anfragen == 1
    assert erster.abgebaut
    assert zweiter.anfragen == 1
    assert not zweiter.abgebaut
    assert nachbar._link is zweiter
    assert uebrig == []


def test_link_mit_antwort_wiederholt_auf_demselben(monkeypatch) -> None:
    """Hat ein Link einmal geantwortet, geht eine unzugestellte Anfrage auf ihm erneut; kein
    neuer Link wird aufgebaut (D591, D631 Beschluss 1)."""
    monkeypatch.setattr(reticulum, "_ZUSTELL_MIN", 0.1)
    link = _Folge([_gut(), _verloren(), _gut()])
    ersatz = _Folge([_gut()])
    uebrig = [ersatz]
    _aufbau(monkeypatch, uebrig)
    nachbar = _frisch(link)
    assert nachbar.bestand() == ([], [])
    assert nachbar.bestand() == ([], [])
    assert link.anfragen == 3
    assert not link.abgebaut
    assert ersatz.anfragen == 0
    assert uebrig == [ersatz]


def test_neuer_link_ist_wieder_frisch(monkeypatch) -> None:
    """Auch der neue Link hat noch nie geantwortet: bleibt er ohne Antwort, folgt ein dritter
    (D631 Beschluss 1)."""
    monkeypatch.setattr(reticulum, "_ZUSTELL_MIN", 0.1)
    erster = _Folge([_verloren(), _verloren(), _verloren()])
    zweiter = _Folge([_verloren(), _verloren()])
    dritter = _Folge([_gut()])
    _aufbau(monkeypatch, [zweiter, dritter])
    nachbar = _frisch(erster)
    assert nachbar.bestand() == ([], [])
    assert (erster.anfragen, zweiter.anfragen, dritter.anfragen) == (1, 1, 1)
    assert erster.abgebaut and zweiter.abgebaut and not dritter.abgebaut
    assert nachbar._link is dritter


def test_frist_ab_erster_anfrage_ueber_neue_links(monkeypatch) -> None:
    """Die Antwortfrist läuft ab der ersten Anfrage, auch wenn die späteren über neue Links
    gehen; höchstens ``_VERSUCHE`` Anfragen, dann getrennt (D625, D631 Beschluss 2)."""
    monkeypatch.setattr(reticulum, "_ZUSTELL_MIN", 0.1)
    links = [_Folge([_verloren() for _ in range(5)]) for _ in range(5)]
    erster = links.pop(0)
    spaetere = list(links)
    _aufbau(monkeypatch, links)
    nachbar = _frisch(erster, Zeiten(10.0, 0.3, 10.0))
    begun = time.monotonic()
    with pytest.raises(Getrennt):
        nachbar.bestand()
    dauer = time.monotonic() - begun
    assert 0.3 <= dauer < 0.45
    assert [link.anfragen for link in [erster] + spaetere] == [1, 1, 1, 0, 0]
    assert spaetere[1].abgebaut
    assert nachbar._link is None


def test_neuer_link_scheitert_getrennt(monkeypatch) -> None:
    """Scheitert der Aufbau des neuen Links, ist der Nachbar getrennt und hält keinen Link
    (D625 Beschluss 1, D631 Beschluss 2)."""
    monkeypatch.setattr(reticulum, "_ZUSTELL_MIN", 0.1)
    erster = _Folge([_verloren(), _verloren(), _verloren()])

    class _Zu:
        status = RNS.Link.CLOSED

    _aufbau(monkeypatch, [_Zu()])
    nachbar = _frisch(erster, Zeiten(5.0, 1.5, 10.0))
    begun = time.monotonic()
    with pytest.raises(Getrennt):
        nachbar.bestand()
    assert time.monotonic() - begun < 1.0
    assert erster.anfragen == 1
    assert erster.abgebaut
    assert nachbar._link is None
