"""Geräte im Knoten, in der Simulation und auf der Karte (D542, D543)."""

from __future__ import annotations

import json

from symbolon.atom import claim_id, signed_bytes
from symbolon.index import classify_all
from symbolon.node.api import _budget_of, _intent_body, _stand
from symbolon.node.store import SqliteStore
from symbolon.node.view import _changes, geraetestimmen, proposals_view, scope_view, tasks_view
from symbolon.trust.attribution import attribution
from tests.node.test_abgleich import _url
from tests.node.test_api import _call, _stop
from tests.node.test_netz import _stand as _stand_server
from tests.node.test_personen import _ausgang, _epoche, _forks
from tests.node.test_versehen import _GRENZE, _NOW, _start
from tools.example_nucleus import _Author, _nuc
from tools.netz import GERAETE_GERAETE, durchgang
from tools.personen import ANTRAG_TAKT, TRENNUNG, takt
from tools.verein import _ratify, _vote, build
from tools.verein_node import aufnahmen, anlegen

_JETZT = 2000


def _welt(tmp_path, datei="w.sqlite", schluessel=None):
    """Frischer Bestand mit Aufnahmen und eine Welt, deren Ketten dort weitergehen."""
    anlegen(tmp_path / datei, schluessel, geraete=True)
    world = build()
    geraete = {name: dev for name, dev, _add, _ack in aufnahmen(world)}
    store = SqliteStore(tmp_path / datei)
    antrag = world.anna.claim(
        p=_nuc(world.ex.N_gov, "propose"),
        J=(3, world.proposal_3.proposal_hash),
        t=20,
        N=world.ex.N_gov,
    )
    store.submit_claim(signed_bytes(antrag))
    return world, geraete, store


def _stimme(store, wer, world, wahl, t=30):
    claim = _vote(wer, world.proposal_3, wahl, t=t, scope=world.ex.N_gov)
    store.submit_claim(signed_bytes(claim))
    return claim


def test_aufnahme_im_bestand(tmp_path) -> None:
    """Gleiche Bytes in jedem Bestand, zugerechnet in N_gov, Seed nur, wo genannt (D542 Beschluss 3)."""
    anlegen(tmp_path / "a.sqlite", frozenset({"ANNA"}), geraete=True)
    anlegen(tmp_path / "b.sqlite", frozenset({"BRUNO (Zweitgerät)"}), geraete=True)
    world = build()
    geraete = {name: dev for name, dev, _add, _ack in aufnahmen(world)}
    a, b = SqliteStore(tmp_path / "a.sqlite"), SqliteStore(tmp_path / "b.sqlite")
    assert _stand(a) == _stand(b)
    for store in (a, b):
        attr = attribution(store, classify_all(store, _JETZT), world.ex.N_gov)
        assert attr.device_root(geraete["BRUNO"].pub) == world.bruno.pub
        assert attr.device_root(geraete["DORA"].pub) == world.dora.pub
        namen = store.all_names()
        assert namen[geraete["BRUNO"].pub] == "BRUNO (Zweitgerät)"
        assert namen[geraete["DORA"].pub] == "DORA (Zweitgerät)"
    assert b.sim_pubs() == {geraete["BRUNO"].pub}
    assert geraete["BRUNO"].pub not in a.sim_pubs()


def test_sicht_je_wurzel(tmp_path) -> None:
    """Ja, Nein und mehrdeutig nennen Wurzeln (D542 Beschluss 4)."""
    world, geraete, store = _welt(tmp_path)
    for wer in (world.anna, world.chris, world.dora, geraete["DORA"], world.bruno):
        _stimme(store, wer, world, 1)
    _stimme(store, geraete["BRUNO"], world, 0)
    (zeile,) = [
        z for z in proposals_view(store, world.ex.N_gov, _JETZT)
        if z.proposal == world.proposal_3.proposal_hash
    ]
    assert zeile.yes == tuple(sorted((world.anna.pub, world.chris.pub, world.dora.pub)))
    assert zeile.no == ()
    assert zeile.ambiguous == (world.bruno.pub,)


def _arten(store, wer):
    return {(t.art, t.detail) for t in tasks_view(store, wer, _JETZT)}


def test_aufgaben_eines_geraets(tmp_path) -> None:
    """Aufgaben der Wurzel für VOTE und RATIFY, nichts nach I (D542 Beschluss 4)."""
    world, geraete, store = _welt(tmp_path)
    abstimmen = ("VOTE", world.proposal_3.proposal_hash)
    assert abstimmen in _arten(store, geraete["BRUNO"].pub)
    assert any(art == "CONFIRM_RULES" for art, _d in _arten(store, world.bruno.pub))
    assert not any(art != "VOTE" for art, _d in _arten(store, geraete["BRUNO"].pub))
    _stimme(store, geraete["BRUNO"], world, 0)
    assert abstimmen not in _arten(store, world.bruno.pub)
    _stimme(store, world.dora, world, 1)
    assert abstimmen not in _arten(store, geraete["DORA"].pub)
    for wer in (world.anna, world.chris):
        _stimme(store, wer, world, 1)
    assert ("RATIFY", world.proposal_3.proposal_hash) in _arten(store, geraete["DORA"].pub)


def test_stimme_ueber_geraet(tmp_path) -> None:
    """ALREADY_VOTED und die Folge nach der Wurzel (D542 Beschluss 4)."""
    world, geraete, store = _welt(tmp_path)
    rumpf = {
        "I": geraete["DORA"].pub.hex(),
        "art": "vote",
        "proposal": world.proposal_3.proposal_hash.hex(),
        "choice": "yes",
    }
    _felder, warnungen, folge = _intent_body(store, rumpf, _JETZT)
    assert warnungen == [] and folge["counts"] is True and folge["yes"] == 1
    _stimme(store, world.dora, world, 1)
    _felder, warnungen, folge = _intent_body(store, rumpf, _JETZT)
    assert warnungen == ["SAME_VOTE"] and folge["counts"] is False and folge["yes"] == 1
    rumpf["choice"] = "no"
    _felder, warnungen, folge = _intent_body(store, rumpf, _JETZT)
    assert warnungen == ["ALREADY_VOTED"] and folge["counts"] is False and folge["yes"] == 0


def test_budget_je_wurzel(tmp_path) -> None:
    """Eine Bürgschaft des Geräts zählt zum Budget der Wurzel (D542 Beschluss 4, 02 §2.1)."""
    world, geraete, store = _welt(tmp_path)
    res = world.ex.N_res
    dev = geraete["BRUNO"]
    add = world.bruno.claim(p=_nuc(res, "device-add"), J=(1, dev.pub), t=40, N=res)
    ack = dev.claim(p=_nuc(res, "device-ack"), J=(2, claim_id(add)), t=40, N=res)
    for claim in (add, ack):
        store.submit_claim(signed_bytes(claim))
    vorher, _D = _budget_of(store, res, world.bruno.pub, _JETZT)
    store.submit_claim(
        signed_bytes(dev.vouch(world.dora, n=3, scope=res, t=41, t_exp=_JETZT + 100000))
    )
    nachher, _D = _budget_of(store, res, world.bruno.pub, _JETZT)
    assert nachher == vorher + 3


def _gruppen(store, world):
    return {
        g.root: (sorted(w for _c, _k, w in g.stimmen), g.changes)
        for g in geraetestimmen(store, world.ex.N_gov, _JETZT)
    }


def test_geraetestimmen(tmp_path) -> None:
    """Je Wurzel und Antrag, nur mit zwei Schlüsseln, über die Epoche hinaus (D542 Beschluss 5)."""
    world, geraete, store = _welt(tmp_path)
    anna = _stimme(store, world.anna, world, 1)
    chris = _stimme(store, world.chris, world, 1)
    _stimme(store, world.chris, world, 1, t=31)
    dora = _stimme(store, world.dora, world, 1)
    _stimme(store, geraete["DORA"], world, 1)
    _stimme(store, world.bruno, world, 1)
    _stimme(store, geraete["BRUNO"], world, 0)
    erwartet = _changes(world.ex.constitution_2, world.constitution_3)
    soll = {world.bruno.pub: ([0, 1], erwartet), world.dora.pub: ([1, 1], erwartet)}
    assert _gruppen(store, world) == soll
    ratify = _ratify(world.anna, world.proposal_3, [anna, chris, dora], t=50, scope=world.ex.N_gov)
    store.submit_claim(signed_bytes(ratify))
    assert scope_view(store, world.ex.N_gov, _JETZT).state.epoch.index == 3
    assert _gruppen(store, world) == soll


def test_geraetestimmen_ohne_fremde_werte(tmp_path) -> None:
    """Ein Wert, der weder Ja noch Nein ist, ist keine Stimme dieser Gruppe (D543)."""
    world, geraete, store = _welt(tmp_path)
    _stimme(store, world.dora, world, 1)
    _stimme(store, geraete["DORA"], world, 2)
    assert _gruppen(store, world) == {}


def test_geraetestimmen_ohne_bestrittene(tmp_path) -> None:
    """Eine gesperrte Stimme steht nicht in der Gruppe (D542 Beschluss 5, D532)."""
    world, geraete, store = _welt(tmp_path)
    _stimme(store, world.dora, world, 1)
    _stimme(store, geraete["DORA"], world, 1)
    ende = world.dora.claim(
        p=_nuc(world.ex.N_gov, "device-end"), J=(1, geraete["DORA"].pub), t=60, N=world.ex.N_gov
    )
    store.submit_claim(signed_bytes(ende))
    assert _gruppen(store, world) == {}


def _lauf(urls, jetzt):
    zeilen, gemeldet, gesehen = [], set(), {}
    for nummer in range(_GRENZE):
        jetzt["t"] = _NOW + nummer
        neu = takt(urls, nummer, gemeldet, GERAETE_GERAETE, gesehen)
        zeilen += neu
        verteilt = durchgang(urls)
        if nummer > max(ANTRAG_TAKT, *TRENNUNG) and not neu and not verteilt:
            return zeilen
    raise AssertionError(f"nach {_GRENZE} Takten nicht still: {zeilen}")


def test_bild_c(tmp_path) -> None:
    """Uhr +1 je Takt: keine Gabel, der Beschluss hält, beide Gruppen auf jedem Gerät (D542)."""
    ausgang = _ausgang(tmp_path)
    world = build()
    jetzt = {"t": _NOW}
    knoten = []
    for name, datei, personen in GERAETE_GERAETE:
        anlegen(tmp_path / datei, personen, geraete=True)
        knoten.append(_start(tmp_path / datei, name, lambda: jetzt["t"]))
    try:
        urls = [_url(server) for server in knoten]
        zeilen = _lauf(urls, jetzt)
        assert len({_stand_server(server) for server in knoten}) == 1
        for server in knoten:
            assert _forks(server) == []
            assert _epoche(server, world.ex.N_gov) == ausgang + 1
            status, body = _call(server, "GET", f"/geraetestimmen/{world.ex.N_gov.hex()}")
            assert status == 200, body
            gruppen = {g["root"]: sorted(s[2] for s in g["stimmen"]) for g in json.loads(body)}
            assert gruppen == {world.bruno.pub.hex(): [0, 1], world.dora.pub.hex(): [1, 1]}
        assert len([z for z in zeilen if "stellt den Beschluss fest" in z]) == 1, zeilen
        assert not [z for z in zeilen if "abgewiesen" in z or "widersprochen" in z], zeilen
    finally:
        for server in knoten:
            _stop(server)


def test_geraetestimmen_nur_teilnehmer(tmp_path) -> None:
    """Eine Wurzel, die im Antrag nicht Teilnehmerin ist, erscheint nicht (D542 Beschluss 5)."""
    world, _geraete, store = _welt(tmp_path)
    gov = world.ex.N_gov
    dev = _Author(bytes([0x23] * 32))
    add = world.kasse.claim(p=_nuc(gov, "device-add"), J=(1, dev.pub), t=40, N=gov)
    ack = dev.claim(p=_nuc(gov, "device-ack"), J=(2, claim_id(add)), t=40, N=gov)
    for claim in (add, ack):
        store.submit_claim(signed_bytes(claim))
    _stimme(store, world.kasse, world, 1, t=41)
    _stimme(store, dev, world, 0, t=41)
    assert world.kasse.pub not in world.ex.constitution_2["participants"]
    assert _gruppen(store, world) == {}
