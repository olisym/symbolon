"""Die Sparrunde zu dritt: Vorlage, Reihenfolge, Tafel, Aufgaben (O109, D703, D704)."""

from __future__ import annotations

import pytest

from symbolon import cbor_canon
from symbolon.genesis import genesis_scope
from symbolon.node.gruendung import Abgewiesen, gruenden, reihenfolge_lesen, wert_gueltig
from symbolon.node.store import ObjectKind, SqliteStore
from symbolon.node.view import sparrunde_view, tasks_view
from symbolon.policy import constitution_hash
from tests.node.test_api import _seed, _start, _stop
from tests.node.test_gruendung import _drei, _json
from tools.example_nucleus import people

RATE = "20,00 EUR im Monat"
CENT = 2000


def _felder(folge: list[str]) -> dict[str, str]:
    return {"name": "Sparrunde", "rate": RATE, "reihenfolge": " ".join(folge)}


def _folge() -> list[str]:
    """Anna, Bruno, Chris in dieser Reihenfolge, nicht nach Schlüssel sortiert."""
    anna, bruno, chris, _dora = people()
    return [anna.pub.hex(), bruno.pub.hex(), chris.pub.hex()]


def test_gruendung_einer_sparrunde() -> None:
    """Die Satzung nennt ``sparrunde@1``, Name, Rate und Reihenfolge, alle vier geschützt; die
    Reihenfolge der Gründer in der Anfrage ändert nichts (D704 Beschluss 2)."""
    got = gruenden("sparrunde", _drei(), _felder(_folge()))
    satzung = cbor_canon.decode(got.objekte[0][1])
    assert satzung["vorlage"] == "sparrunde@1"
    assert satzung["rate"] == RATE
    assert satzung["reihenfolge"] == " ".join(_folge())
    assert satzung["protected_fields"] == ["name", "rate", "reihenfolge", "vorlage"]
    assert gruenden("sparrunde", _drei()[::-1], _felder(_folge())) == got


def _falsche_folgen() -> dict[str, str]:
    a, b, c = _folge()
    dora = people()[3].pub.hex()
    return {
        "zwei von drei": f"{a} {b}",
        "einer doppelt": f"{a} {b} {a}",
        "ein Fremder": f"{a} {b} {dora}",
        "vier mit Fremdem": f"{a} {b} {c} {dora}",
        "Grossbuchstaben": f"{a.upper()} {b} {c}",
        "zwei Leerzeichen": f"{a}  {b} {c}",
        "Komma": f"{a},{b},{c}",
        "Leerzeichen am Rand": f" {a} {b} {c}",
    }


@pytest.mark.parametrize("fall", sorted(_falsche_folgen()))
def test_falsche_reihenfolge_wird_abgewiesen(fall: str) -> None:
    """Eine Reihenfolge nennt jeden Gründer genau einmal, sonst ``INVALID_VALUE``
    (D704 Beschluss 2)."""
    felder = {"name": "Sparrunde", "rate": RATE, "reihenfolge": _falsche_folgen()[fall]}
    with pytest.raises(Abgewiesen) as fehler:
        gruenden("sparrunde", _drei(), felder)
    assert fehler.value.name == "INVALID_VALUE"


def test_typ_reihenfolge_prueft_nur_die_form() -> None:
    """``wert_gueltig`` kennt die Gründer nicht: ein Schlüssel gilt, ein doppelter nicht
    (D704 Beschluss 2)."""
    a, b, _c = _folge()
    assert wert_gueltig("reihenfolge", a) is True
    assert wert_gueltig("reihenfolge", f"{b} {a}") is True
    assert wert_gueltig("reihenfolge", f"{a} {a}") is False
    assert wert_gueltig("reihenfolge", "") is False
    assert reihenfolge_lesen(f"{b} {a}") == (bytes.fromhex(b), bytes.fromhex(a))
    assert reihenfolge_lesen(None) is None


class _Uhr:
    def __init__(self) -> None:
        self.t = 1000

    def __call__(self) -> int:
        return self.t


def _knoten(tmp_path):
    path = tmp_path / "bestand.sqlite"
    store = SqliteStore(path)
    personen = people()
    for person in personen:
        store.add_sim_key(_seed(person))
    store.close()
    uhr = _Uhr()
    return path, _start(path, uhr), uhr, personen


def _handeln(server, uhr, person, art, **mehr):
    uhr.t += 10
    status, folge = _json(
        server, "POST", "/sim/intent", {"I": person.pub.hex(), "art": art, **mehr}
    )
    assert status == 200, folge
    return folge


def _runde(server, uhr, personen, betrag=CENT):
    """Gründet, und jeder sagt jedem anderen eine Rate zu; die sechs Zusagen nach Paar."""
    anna, bruno, chris, _dora = personen
    status, antwort = _json(
        server,
        "POST",
        "/gruenden",
        {"vorlage": "sparrunde", "gruender": _drei(), "felder": _felder(_folge())},
    )
    assert status == 200, antwort
    verein, leben = antwort["verein"], antwort["vereinsleben"]
    zusagen = {}
    for x in (anna, bruno, chris):
        for y in (anna, bruno, chris):
            if x is y:
                continue
            folge = _handeln(
                server,
                uhr,
                x,
                "obligation",
                scope=leben,
                creditor=y.pub.hex(),
                amount=betrag,
                unit="EUR-Cent",
            )
            zusagen[(x.pub, y.pub)] = folge["claim_id"]
    return verein, leben, zusagen


def _tafel(server, verein):
    status, tafel = _json(server, "GET", f"/sparrunde/{verein}")
    assert status == 200
    return tafel


def _zustaende(tafel):
    """Je Monat die Zustände der Zahler in der Reihenfolge der Tafel."""
    return [[zeile["zustand"] for zeile in monat["zeilen"]] for monat in tafel["monate"]]


def _aufgaben(server, person, leben):
    status, liste = _json(server, "GET", f"/tasks/{person.pub.hex()}")
    assert status == 200
    return sorted((z["art"], z["obligation"]) for z in liste if z["scope"] == leben)


def test_tafel_weiter_wenn_bezahlt(tmp_path) -> None:
    """Monat 2 ist dran, sobald Anna von beiden ihr Geld hat; ``seit`` ist der Zeitstempel der
    späteren Quittung von Monat 1; zahlt Anna nicht, bleibt Monat 2 dran (D704 Beschluss 1
    und 3)."""
    _path, server, uhr, personen = _knoten(tmp_path)
    anna, bruno, chris, _dora = personen
    try:
        verein, leben, zusagen = _runde(server, uhr, personen)
        tafel = _tafel(server, verein)
        assert tafel["verein"] == verein
        assert tafel["vereinsleben"] == leben
        assert tafel["rate"] == CENT
        assert [m["empfaenger"] for m in tafel["monate"]] == _folge()
        assert [[z["zahler"] for z in m["zeilen"]] for m in tafel["monate"]] == [
            [bruno.pub.hex(), chris.pub.hex()],
            [anna.pub.hex(), chris.pub.hex()],
            [anna.pub.hex(), bruno.pub.hex()],
        ]
        assert (tafel["laufend"], tafel["seit"]) == (1, None)
        assert _zustaende(tafel) == [["offen", "offen"]] * 3

        _handeln(server, uhr, anna, "receipt", obligation=zusagen[(bruno.pub, anna.pub)])
        tafel = _tafel(server, verein)
        assert (tafel["laufend"], tafel["seit"]) == (1, None)
        assert _zustaende(tafel)[0] == ["bezahlt", "offen"]

        _handeln(server, uhr, anna, "receipt", obligation=zusagen[(chris.pub, anna.pub)])
        spaeter = uhr.t
        tafel = _tafel(server, verein)
        assert (tafel["laufend"], tafel["seit"]) == (2, spaeter)
        assert tafel["monate"][0]["fertig"] is True

        _handeln(server, uhr, bruno, "receipt", obligation=zusagen[(chris.pub, bruno.pub)])
        tafel = _tafel(server, verein)
        assert (tafel["laufend"], tafel["seit"]) == (2, spaeter)
        assert _zustaende(tafel) == [
            ["bezahlt", "bezahlt"],
            ["offen", "bezahlt"],
            ["offen", "offen"],
        ]

        for x, y in ((anna, bruno), (anna, chris), (bruno, chris)):
            _handeln(server, uhr, y, "receipt", obligation=zusagen[(x.pub, y.pub)])
        tafel = _tafel(server, verein)
        assert (tafel["laufend"], tafel["seit"]) == (None, None)
    finally:
        _stop(server)


def test_aufgaben_nur_im_laufenden_monat(tmp_path) -> None:
    """Am ersten Tag zahlt man nur Anna, und nur Anna quittiert; nach Monat 1 nur Bruno
    (D704 Beschluss 4)."""
    _path, server, uhr, personen = _knoten(tmp_path)
    anna, bruno, chris, _dora = personen
    try:
        _verein, leben, zusagen = _runde(server, uhr, personen)
        assert _aufgaben(server, chris, leben) == [
            ("CONTRIBUTION_OPEN", zusagen[(chris.pub, anna.pub)])
        ]
        assert _aufgaben(server, bruno, leben) == [
            ("CONTRIBUTION_OPEN", zusagen[(bruno.pub, anna.pub)])
        ]
        assert _aufgaben(server, anna, leben) == sorted(
            [
                ("RECEIPT", zusagen[(bruno.pub, anna.pub)]),
                ("RECEIPT", zusagen[(chris.pub, anna.pub)]),
            ]
        )
        for x in (bruno, chris):
            _handeln(server, uhr, anna, "receipt", obligation=zusagen[(x.pub, anna.pub)])
        assert _aufgaben(server, chris, leben) == [
            ("CONTRIBUTION_OPEN", zusagen[(chris.pub, bruno.pub)])
        ]
        assert _aufgaben(server, anna, leben) == [
            ("CONTRIBUTION_OPEN", zusagen[(anna.pub, bruno.pub)])
        ]
        assert _aufgaben(server, bruno, leben) == sorted(
            [
                ("RECEIPT", zusagen[(anna.pub, bruno.pub)]),
                ("RECEIPT", zusagen[(chris.pub, bruno.pub)]),
            ]
        )
    finally:
        _stop(server)


def test_zusage_in_anderer_hoehe_zaehlt_nicht(tmp_path) -> None:
    """Eine Zusage von 19,99 EUR steht nicht auf der Tafel und bleibt sofort eine Aufgabe wie
    bisher (D704 Beschluss 3 und 4)."""
    _path, server, uhr, personen = _knoten(tmp_path)
    anna, bruno, chris, _dora = personen
    try:
        status, antwort = _json(
            server,
            "POST",
            "/gruenden",
            {"vorlage": "sparrunde", "gruender": _drei(), "felder": _felder(_folge())},
        )
        assert status == 200
        verein, leben = antwort["verein"], antwort["vereinsleben"]
        klein = _handeln(
            server,
            uhr,
            chris,
            "obligation",
            scope=leben,
            creditor=bruno.pub.hex(),
            amount=CENT - 1,
            unit="EUR-Cent",
        )["claim_id"]
        euro = _handeln(
            server,
            uhr,
            chris,
            "obligation",
            scope=leben,
            creditor=anna.pub.hex(),
            amount=20,
            unit="EUR",
        )["claim_id"]
        tafel = _tafel(server, verein)
        assert _zustaende(tafel) == [["fehlt", "fehlt"]] * 3
        assert _aufgaben(server, chris, leben) == sorted(
            [("CONTRIBUTION_OPEN", klein), ("CONTRIBUTION_OPEN", euro)]
        )
    finally:
        _stop(server)


def test_keine_tafel_fuer_einen_verein_und_404_fuer_unbekannt(tmp_path) -> None:
    """Ein Verein ist keine Sparrunde: ``null``; ein unbekannter Scope: 404 (D704 Beschluss 3)."""
    _path, server, _uhr, _personen = _knoten(tmp_path)
    try:
        felder = {"name": "Laufgruppe", "sitz": "Ort", "zweck": "Gemeinsam laufen"}
        status, antwort = _json(
            server,
            "POST",
            "/gruenden",
            {"vorlage": "verein", "gruender": _drei(), "felder": felder},
        )
        assert status == 200
        assert _json(server, "GET", f"/sparrunde/{antwort['verein']}") == (200, None)
        assert _json(server, "GET", f"/sparrunde/{antwort['vereinsleben']}") == (200, None)
        assert _json(server, "GET", f"/sparrunde/{'ab' * 32}")[0] == 404
    finally:
        _stop(server)


def _formwidrig(satzung_aendern, zweites_leben=False):
    """Ein Bestand mit einer Sparrunde, deren Satzung nach der Gründung geändert und neu
    eingeliefert ist, wie über ``POST /objects`` (D652 Befund 2)."""
    got = gruenden("sparrunde", _drei(), _felder(_folge()))
    satzung = cbor_canon.decode(got.objekte[0][1])
    genesis = cbor_canon.decode(got.objekte[1][1])
    leben_satzung = got.objekte[2][1]
    leben_genesis = cbor_canon.decode(got.objekte[3][1])
    satzung_aendern(satzung)
    genesis[4] = constitution_hash(satzung)
    verein = genesis_scope(genesis)
    leben_genesis[8] = verein
    store = SqliteStore(":memory:")
    store.submit_object(ObjectKind.CONSTITUTION, cbor_canon.encode(satzung))
    store.submit_object(ObjectKind.GENESIS, cbor_canon.encode(genesis))
    store.submit_object(ObjectKind.CONSTITUTION, leben_satzung)
    store.submit_object(ObjectKind.GENESIS, cbor_canon.encode(leben_genesis))
    if zweites_leben:
        noch = dict(leben_genesis)
        noch[6] = 1
        store.submit_object(ObjectKind.GENESIS, cbor_canon.encode(noch))
    return store, verein, genesis_scope(leben_genesis)


@pytest.mark.parametrize(
    ("fall", "aendern", "zweites"),
    [
        ("Reihenfolge kaputt", lambda s: s.__setitem__("reihenfolge", "kaputt"), False),
        ("Reihenfolge keine Zeichenkette", lambda s: s.__setitem__("reihenfolge", 7), False),
        ("Rate kaputt", lambda s: s.__setitem__("rate", "zwanzig"), False),
        ("Rate fehlt", lambda s: s.pop("rate"), False),
        ("zwei Vereinsleben", lambda _s: None, True),
    ],
)
def test_formwidrige_sparrunde_hat_keine_tafel(fall, aendern, zweites) -> None:
    """Keine Tafel und kein Fehler; die Aufgaben gelten wie bisher (D704 Beschluss 3, D652
    Beschluss 5)."""
    store, verein, leben = _formwidrig(aendern, zweites)
    try:
        anna, bruno, _chris, _dora = people()
        zusage = anna.claim(
            p=f"nuc:{leben.hex()}/obligation@1",
            J=(1, bruno.pub),
            t=1001,
            v=cbor_canon.encode({0: CENT, 1: b"EUR-Cent"}),
            N=leben,
        )
        store.add(zusage)
        assert sparrunde_view(store, verein, 1002) is None, fall
        arten = [(a.scope, a.art) for a in tasks_view(store, anna.pub, 1002)]
        assert (leben, "CONTRIBUTION_OPEN") in arten
    finally:
        store.close()
