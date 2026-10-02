"""Gründung aus einer Vorlage (D641)."""

from __future__ import annotations

import copy
import json

import pytest

from symbolon import cbor_canon
from symbolon.genesis import genesis_scope
from symbolon.node import gruendung as modul
from symbolon.node.gruendung import Abgewiesen, gruenden
from symbolon.node.store import ObjectKind, SqliteStore
from symbolon.policy import constitution_hash
from tests.node.test_api import _call, _seed, _start, _stop
from tools.example_nucleus import people

FELDER = {"name": "Laufgruppe", "sitz": "Ort", "zweck": "Gemeinsam laufen"}


def _drei() -> list[str]:
    anna, bruno, chris, _dora = people()
    return [anna.pub.hex(), bruno.pub.hex(), chris.pub.hex()]


def test_gruendung_ist_bestimmt() -> None:
    """Die vier Objekte, hier von Hand gebaut (D641 Beschluss 3, 00 §4, 00 §4.1, 00 §5)."""
    keys = sorted(bytes.fromhex(item) for item in _drei())
    thresholds = {"ordinary": [1, 2], "membership": [1, 2], "amendment": [2, 3]}
    satzung = {
        "name": "Laufgruppe",
        "sitz": "Ort",
        "zweck": "Gemeinsam laufen",
        "beitrag": "24 Euro im Jahr",
        "irrevocable_predicates": ["obligation@1", "ratify@1", "vote@1"],
        "thresholds": thresholds,
        "arbitration": {"arbitrators": keys},
        "participants": keys,
    }
    leben = {
        "irrevocable_predicates": ["obligation@1"],
        "thresholds": thresholds,
        "arbitration": {"arbitrators": keys},
    }
    genesis = {0: 1, 1: keys, 2: 0, 3: keys, 4: constitution_hash(satzung), 5: 2, 6: 0, 7: 0}
    verein = genesis_scope(genesis)
    genesis_leben = {
        0: 1,
        1: keys,
        2: 0,
        3: keys,
        4: constitution_hash(leben),
        5: 2,
        6: 0,
        7: 0,
        8: verein,
        9: {0: 100, 1: 1, 2: 2, 3: 100},
    }
    got = gruenden("verein", _drei(), {**FELDER, "beitrag": "24 Euro im Jahr"})
    assert got.verein == verein
    assert got.vereinsleben == genesis_scope(genesis_leben)
    assert got.constitution == constitution_hash(satzung)
    assert got.objekte == (
        (ObjectKind.CONSTITUTION, cbor_canon.encode(satzung)),
        (ObjectKind.GENESIS, cbor_canon.encode(genesis)),
        (ObjectKind.CONSTITUTION, cbor_canon.encode(leben)),
        (ObjectKind.GENESIS, cbor_canon.encode(genesis_leben)),
    )
    # Die Reihenfolge der Gründer in der Eingabe ändert nichts.
    assert gruenden("verein", _drei()[::-1], {**FELDER, "beitrag": "24 Euro im Jahr"}) == got


def test_vereinsleben_gehoert_zu_seinem_verein() -> None:
    """Dieselben drei gründen zwei Vereine: zwei Vereinsleben (D641 Befund 1, 00 §4.1)."""
    eins = gruenden("verein", _drei(), FELDER)
    zwei = gruenden("verein", _drei(), {**FELDER, "name": "Chor"})
    assert eins.verein != zwei.verein
    assert eins.vereinsleben != zwei.vereinsleben
    assert cbor_canon.decode(eins.objekte[3][1])[8] == eins.verein


@pytest.mark.parametrize(
    ("vorlage", "gruender", "felder", "name"),
    [
        ("firma", "drei", FELDER, "UNKNOWN_TEMPLATE"),
        (7, "drei", FELDER, "UNKNOWN_TEMPLATE"),
        (["verein"], "drei", FELDER, "UNKNOWN_TEMPLATE"),
        ("verein", "kein-feld", FELDER, "INVALID_FOUNDERS"),
        ("verein", {"a": 1}, FELDER, "INVALID_FOUNDERS"),
        ("verein", ["zz", "zz", "zz"], FELDER, "INVALID_FOUNDERS"),
        ("verein", [1, 2, 3], FELDER, "INVALID_FOUNDERS"),
        ("verein", ["00" * 31, "11" * 32, "22" * 32], FELDER, "INVALID_FOUNDERS"),
        ("verein", "doppelt", FELDER, "INVALID_FOUNDERS"),
        ("verein", "zwei", FELDER, "TOO_FEW_FOUNDERS"),
        ("verein", [], FELDER, "TOO_FEW_FOUNDERS"),
        ("verein", "drei", ["name"], "INVALID_FIELDS"),
        ("verein", "drei", {**FELDER, "zweck": 5}, "INVALID_FIELDS"),
        ("verein", "drei", {**FELDER, "beitrag": None}, "INVALID_FIELDS"),
        ("verein", "drei", {**FELDER, "participants": "x"}, "UNKNOWN_FIELD"),
        ("verein", "drei", {**FELDER, "thresholds": "x"}, "UNKNOWN_FIELD"),
        ("verein", "drei", {"name": "Laufgruppe", "sitz": "Ort"}, "MISSING_FIELD"),
        ("verein", "drei", {**FELDER, "name": ""}, "MISSING_FIELD"),
    ],
)
def test_abweisungen(vorlage, gruender, felder, name) -> None:
    """Formwidrige Eingaben, jede mit ihrem Namen (D641 Beschluss 4, D474)."""
    drei = _drei()
    eingaben = {"drei": drei, "zwei": drei[:2], "doppelt": [drei[0], drei[1], drei[0]]}
    if isinstance(gruender, str) and gruender in eingaben:
        gruender = eingaben[gruender]
    with pytest.raises(Abgewiesen) as caught:
        gruenden(vorlage, gruender, felder)
    assert caught.value.name == name


@pytest.mark.parametrize(
    ("schluessel", "wert"),
    [
        ("irrevocable_verein", ["obligation@1", "vote@1"]),
        ("irrevocable_verein", ["obligation@1", "ratify@1"]),
        ("thresholds", {"ordinary": [1, 2], "membership": [1, 2]}),
        ("thresholds", {"ordinary": [1, 2], "amendment": [2, 3]}),
        ("trust_params", {0: 100, 1: 3, 2: 2, 3: 100}),
    ],
)
def test_probelauf_weist_eine_vorlage_ab_die_nicht_handeln_kann(
    monkeypatch, schluessel, wert
) -> None:
    """Eine Vorlage, deren Verein nie beschliessen könnte (D641 Beschluss 5, D640 Befund 4)."""
    assert gruenden("verein", _drei(), FELDER).verein
    kaputt = copy.deepcopy(modul.VORLAGEN["verein"])
    kaputt[schluessel] = wert
    monkeypatch.setitem(modul.VORLAGEN, "verein", kaputt)
    with pytest.raises(Abgewiesen) as caught:
        gruenden("verein", _drei(), FELDER)
    assert caught.value.name == "UNSOUND_TEMPLATE"


def _knoten(tmp_path):
    path = tmp_path / "bestand.sqlite"
    store = SqliteStore(path)
    personen = people()
    for person in personen:
        store.add_sim_key(_seed(person))
    store.close()
    return path, _start(path, lambda: 1000), personen


def _json(server, method, path, payload=None):
    status, body = _call(server, method, path, payload)
    return status, json.loads(body)


def test_route_gruendet_und_der_verein_traegt(tmp_path) -> None:
    """Gründen, bestätigen, aufnehmen, bürgen: alles über die Schnittstelle (D641 Beschluss 4)."""
    _path, server, (anna, bruno, chris, dora) = _knoten(tmp_path)
    try:
        status, antwort = _json(
            server, "POST", "/gruenden", {"vorlage": "verein", "gruender": _drei(), "felder": FELDER}
        )
        assert status == 200
        erwartet = gruenden("verein", _drei(), FELDER)
        assert antwort == {
            "verein": erwartet.verein.hex(),
            "vereinsleben": erwartet.vereinsleben.hex(),
            "constitution": erwartet.constitution.hex(),
        }
        verein, leben = antwort["verein"], antwort["vereinsleben"]
        assert _json(server, "GET", "/scopes")[1] == sorted([verein, leben])
        # Der Probelauf hinterlässt nichts: vier Objekte, kein Antrag.
        assert len(_json(server, "GET", "/peer/bestand")[1]["objects"]) == 4
        assert _json(server, "GET", f"/proposals/{verein}")[1] == []
        for person in (anna, bruno, chris):
            aufgaben = _json(server, "GET", f"/tasks/{person.pub.hex()}")[1]
            assert aufgaben == [
                {"scope": verein, "art": "CONFIRM_RULES", "constitution": antwort["constitution"]}
            ]
            status, folge = _json(
                server,
                "POST",
                "/sim/intent",
                {"I": person.pub.hex(), "art": "accept-rules", "scope": verein},
            )
            assert status == 200
            assert folge["effect"] == {"membership": "MEMBER"}
        status, _folge = _json(
            server,
            "POST",
            "/sim/intent",
            {"I": anna.pub.hex(), "art": "propose", "scope": verein, "change": {"add": dora.pub.hex()}},
        )
        assert status == 200
        antrag = _json(server, "GET", f"/proposals/{verein}")[1][0]["proposal"]
        for person in (anna, bruno):
            status, folge = _json(
                server,
                "POST",
                "/sim/intent",
                {"I": person.pub.hex(), "art": "vote", "proposal": antrag, "choice": "yes"},
            )
            assert status == 200
        assert folge["effect"]["passes"] is True
        status, folge = _json(
            server, "POST", "/sim/intent", {"I": chris.pub.hex(), "art": "ratify", "proposal": antrag}
        )
        assert status == 200
        assert _json(server, "GET", f"/scopes/{verein}")[1]["state"]["epoch"]["index"] == 2
        status, folge = _json(
            server,
            "POST",
            "/sim/intent",
            {
                "I": chris.pub.hex(),
                "art": "vouch",
                "scope": leben,
                "subject": dora.pub.hex(),
                "n": 50,
                "t_exp": 5000,
            },
        )
        assert status == 200
        assert folge["effect"] == {"used": 50, "D": 100}
    finally:
        _stop(server)


def test_route_weist_ab_und_schreibt_nichts(tmp_path, monkeypatch) -> None:
    """Eine Abweisung lässt den Bestand, wie er war (D641 Beschluss 4 und 5)."""
    path, server, _personen = _knoten(tmp_path)
    try:
        vorher = _json(server, "GET", "/stand")[1]
        status, antwort = _json(
            server,
            "POST",
            "/gruenden",
            {"vorlage": "verein", "gruender": _drei()[:2], "felder": FELDER},
        )
        assert (status, antwort) == (400, "TOO_FEW_FOUNDERS")
        status, antwort = _json(
            server, "POST", "/gruenden", {"vorlage": "verein", "gruender": _drei()}
        )
        assert (status, antwort) == (400, "missing field felder")
        kaputt = copy.deepcopy(modul.VORLAGEN["verein"])
        kaputt["irrevocable_verein"] = ["obligation@1", "vote@1"]
        monkeypatch.setitem(modul.VORLAGEN, "verein", kaputt)
        status, antwort = _json(
            server, "POST", "/gruenden", {"vorlage": "verein", "gruender": _drei(), "felder": FELDER}
        )
        assert (status, antwort) == (400, "UNSOUND_TEMPLATE")
        assert _json(server, "GET", "/scopes")[1] == []
        assert _json(server, "GET", "/stand")[1] == vorher
    finally:
        _stop(server)
    store = SqliteStore(path)
    try:
        assert store.object_hashes() == []
    finally:
        store.close()


def test_route_ist_wiederholbar(tmp_path) -> None:
    """Dieselbe Gründung zweimal: dieselbe Antwort, derselbe Bestand (D641 Beschluss 4)."""
    _path, server, _personen = _knoten(tmp_path)
    try:
        rumpf = {"vorlage": "verein", "gruender": _drei(), "felder": FELDER}
        erste = _json(server, "POST", "/gruenden", rumpf)
        stand = _json(server, "GET", "/stand")[1]
        assert erste[0] == 200
        assert _json(server, "POST", "/gruenden", rumpf) == erste
        assert _json(server, "GET", "/stand")[1] == stand
    finally:
        _stop(server)
