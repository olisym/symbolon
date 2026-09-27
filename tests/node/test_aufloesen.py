"""Das Folgebild: Anna wartet, Bruno löst seinen Widerspruch auf (D551, D552)."""

from __future__ import annotations

import json

from symbolon.atom import claim_id, signed_bytes
from symbolon.node.api import _intent_body
from symbolon.node.view import geraetestimmen
from tests.node.test_abgleich import _url
from tests.node.test_api import _call, _stop
from tests.node.test_ersetzen import _rumpf
from tests.node.test_geraete import _JETZT, _stimme, _welt
from tests.node.test_netz import _stand as _stand_server
from tests.node.test_personen import _ausgang, _epoche, _forks
from tests.node.test_versehen import _GRENZE, _NOW, _start
from tools.example_nucleus import _nuc
from tools.netz import GERAETE_GERAETE, durchgang
from tools.personen import ANTRAG_TAKT, TRENNUNG, aufloesung, takt, wartet
from tools.verein import build
from tools.verein_node import anlegen

_P = "ab" * 32
_Q = "cd" * 32
_BRUNO = "01" * 32
_DORA = "02" * 32


def _gruppe(root: str, proposal: str, werte: list[int]) -> dict:
    stimmen = [[f"{index:02x}" * 32, f"{index + 16:02x}" * 32, wert] for index, wert in enumerate(werte)]
    return {"root": root, "proposal": proposal, "stimmen": stimmen, "ersetzt": []}


def test_wartet() -> None:
    """Nur eine Feststellung, nur bei verschiedener Wahl zu ihrem Antrag (D551 Beschluss 1)."""
    feststellen = {"I": "aa" * 32, "art": "ratify", "proposal": _P}
    widerspruch = _gruppe(_BRUNO, _P, [1, 0])
    assert wartet(feststellen, [widerspruch]) is True
    assert wartet(feststellen, [_gruppe(_DORA, _P, [1, 1])]) is False
    assert wartet(feststellen, [_gruppe(_BRUNO, _Q, [1, 0])]) is False
    assert wartet(feststellen, []) is False
    stimmen = {"I": "aa" * 32, "art": "vote", "proposal": _P, "choice": "yes"}
    assert wartet(stimmen, [widerspruch]) is False


def test_aufloesung() -> None:
    """Ein Ja je eigener Gruppe mit verschiedener Wahl an einem Antrag der Seite (D551 Beschluss 3)."""
    antraege = [{"proposal": _P, "state": "PASSED"}]
    widerspruch = _gruppe(_BRUNO, _P, [1, 0])
    assert aufloesung(_BRUNO, [widerspruch], antraege) == [
        {"I": _BRUNO, "art": "vote", "proposal": _P, "choice": "yes"}
    ]
    assert aufloesung(_BRUNO, [widerspruch], []) == []
    assert aufloesung(_DORA, [widerspruch], antraege) == []
    assert aufloesung(_BRUNO, [_gruppe(_BRUNO, _P, [1, 1])], antraege) == []


def test_gruppe_nach_aufloesung(tmp_path) -> None:
    """Die aufgelöste Gruppe bleibt, mit der neuen Stimme zählend und den alten ersetzt (D551 B. 6)."""
    world, geraete, store = _welt(tmp_path)
    gov = world.ex.N_gov
    ja = _stimme(store, world.bruno, world, 1)
    nein = _stimme(store, geraete["BRUNO"], world, 0)
    felder, _warnungen, _folge = _intent_body(store, _rumpf(world.bruno.pub, world, "yes"), _JETZT)
    neu = world.bruno.claim(
        p=_nuc(gov, "vote"),
        J=(3, world.proposal_3.proposal_hash),
        t=40,
        N=gov,
        v=bytes.fromhex(felder["v"]),
    )
    store.submit_claim(signed_bytes(neu))
    (gruppe,) = geraetestimmen(store, gov, _JETZT)
    assert gruppe.root == world.bruno.pub
    assert gruppe.stimmen == ((claim_id(neu), world.bruno.pub, 1),)
    assert gruppe.ersetzt == tuple(
        sorted([(claim_id(ja), world.bruno.pub, 1), (claim_id(nein), geraete["BRUNO"].pub, 0)])
    )


def test_ein_schluessel_ist_keine_gruppe(tmp_path) -> None:
    """Ersetzt eine Wurzel nur Stimmen desselben Schlüssels, entsteht keine Gruppe (D551 B. 6)."""
    world, _geraete, store = _welt(tmp_path)
    gov = world.ex.N_gov
    _stimme(store, world.dora, world, 1)
    felder, _warnungen, _folge = _intent_body(store, _rumpf(world.dora.pub, world, "no"), _JETZT)
    neu = world.dora.claim(
        p=_nuc(gov, "vote"),
        J=(3, world.proposal_3.proposal_hash),
        t=40,
        N=gov,
        v=bytes.fromhex(felder["v"]),
    )
    store.submit_claim(signed_bytes(neu))
    assert geraetestimmen(store, gov, _JETZT) == ()


def _knoten(tmp_path, jetzt):
    knoten = []
    for name, datei, personen in GERAETE_GERAETE:
        anlegen(tmp_path / datei, personen, geraete=True)
        knoten.append(_start(tmp_path / datei, name, lambda: jetzt["t"]))
    return knoten


def _lauf(urls, jetzt):
    zeilen, gemeldet, gesehen = [], set(), {}
    for nummer in range(_GRENZE):
        jetzt["t"] = _NOW + nummer
        neu = takt(urls, nummer, gemeldet, GERAETE_GERAETE, gesehen, aufloesen=True)
        zeilen += neu
        verteilt = durchgang(urls)
        if nummer > max(ANTRAG_TAKT, *TRENNUNG) and not neu and not verteilt:
            return zeilen
    raise AssertionError(f"nach {_GRENZE} Takten nicht still: {zeilen}")


def test_bild_aufloesen(tmp_path) -> None:
    """Uhr +1 je Takt: Anna wartet, Bruno löst auf, Anna stellt fest, der Beschluss hält (D551)."""
    ausgang = _ausgang(tmp_path)
    world = build()
    jetzt = {"t": _NOW}
    knoten = _knoten(tmp_path, jetzt)
    try:
        urls = [_url(server) for server in knoten]
        zeilen = _lauf(urls, jetzt)
        assert [z for z in zeilen if "wartet" in z or "neu Ja" in z or "fest" in z] == [
            "Takt 4, Annas Gerät: ANNA wartet mit der Feststellung, bis BRUNO den Widerspruch auflöst.",
            "Takt 4, Brunos Gerät: BRUNO stimmt neu Ja; die Stimme ersetzt die früheren",
            "Takt 5, Annas Gerät: ANNA stellt den Beschluss fest",
        ], zeilen
        assert not [z for z in zeilen if "abgewiesen" in z or "widersprochen" in z], zeilen
        assert len({_stand_server(server) for server in knoten}) == 1
        for server in knoten:
            assert _forks(server) == []
            assert _epoche(server, world.ex.N_gov) == ausgang + 1
            status, body = _call(server, "GET", f"/geraetestimmen/{world.ex.N_gov.hex()}")
            assert status == 200, body
            gruppen = {
                g["root"]: (sorted(s[2] for s in g["stimmen"]), sorted(s[2] for s in g["ersetzt"]))
                for g in json.loads(body)
            }
            assert gruppen == {
                world.bruno.pub.hex(): ([1], [0, 1]),
                world.dora.pub.hex(): ([1, 1], []),
            }
    finally:
        for server in knoten:
            _stop(server)


def test_anna_wartet_einmal(tmp_path) -> None:
    """Annas Warten steht je Antrag einmal im Terminal (D551 Beschluss 7)."""
    jetzt = {"t": _NOW}
    knoten = _knoten(tmp_path, jetzt)
    try:
        urls = [_url(server) for server in knoten]
        gemeldet, gesehen = set(), {}
        for nummer in range(4):
            jetzt["t"] = _NOW + nummer
            takt(urls, nummer, gemeldet, GERAETE_GERAETE, gesehen, aufloesen=True)
            durchgang(urls)
        nur_anna = GERAETE_GERAETE[:1]
        assert nur_anna[0][0] == "Annas Gerät"
        erste = takt(urls[:1], 4, gemeldet, nur_anna, gesehen, aufloesen=True)
        zweite = takt(urls[:1], 5, gemeldet, nur_anna, gesehen, aufloesen=True)
        assert [z for z in erste if "wartet" in z] == [
            "Takt 4, Annas Gerät: ANNA wartet mit der Feststellung, bis BRUNO den Widerspruch auflöst."
        ], erste
        assert zweite == [], zweite
    finally:
        for server in knoten:
            _stop(server)
