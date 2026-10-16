"""Die Aufgabe „Mitmachen“ einer Sparrunde (O109, D704 Beschluss 4, D705 Befund 4, D706)."""

from __future__ import annotations

from tests.node.test_api import _stop
from tests.node.test_gruendung import _drei, _json
from tests.node.test_sparrunde import CENT, _felder, _folge, _handeln, _knoten

MITMACHEN = "ROUND_JOIN"


def _gruenden(server, vorlage="sparrunde"):
    if vorlage == "sparrunde":
        felder = _felder(_folge())
    else:
        felder = {"name": "Laufgruppe", "sitz": "Ort", "zweck": "Gemeinsam laufen"}
    status, antwort = _json(
        server, "POST", "/gruenden", {"vorlage": vorlage, "gruender": _drei(), "felder": felder}
    )
    assert status == 200, antwort
    return antwort["verein"], antwort["vereinsleben"]


def _mitmachen(server, person):
    """Die Zeilen ``ROUND_JOIN`` aus ``GET /tasks`` dieser Person."""
    status, liste = _json(server, "GET", f"/tasks/{person.pub.hex()}")
    assert status == 200
    return [zeile for zeile in liste if zeile["art"] == MITMACHEN]


def _zusagen(server, uhr, zahler, an, leben, betrag=CENT):
    for empfaenger in an:
        _handeln(
            server,
            uhr,
            zahler,
            "obligation",
            scope=leben,
            creditor=empfaenger.pub.hex(),
            amount=betrag,
            unit="EUR-Cent",
        )


def test_mitmachen_bis_jedem_zugesagt(tmp_path) -> None:
    """Nach der Gründung hat jeder ``ROUND_JOIN`` mit dem Scope der Sparrunde unter
    ``sparrunde``; es bleibt, bis er jedem anderen eine Rate zugesagt hat (D704 Beschluss 4)."""
    _path, server, uhr, personen = _knoten(tmp_path)
    anna, bruno, chris, dora = personen
    try:
        verein, leben = _gruenden(server)
        erwartet = [{"scope": verein, "art": MITMACHEN, "sparrunde": verein}]
        for person in (anna, bruno, chris):
            assert _mitmachen(server, person) == erwartet
        assert _mitmachen(server, dora) == []

        _zusagen(server, uhr, anna, (bruno, chris), leben)
        assert _mitmachen(server, anna) == []
        assert _mitmachen(server, bruno) == erwartet

        _zusagen(server, uhr, bruno, (anna,), leben)
        assert _mitmachen(server, bruno) == erwartet
        _zusagen(server, uhr, bruno, (chris,), leben)
        assert _mitmachen(server, bruno) == []
        assert _mitmachen(server, chris) == erwartet
    finally:
        _stop(server)


def test_zusage_in_anderer_hoehe_ist_kein_mitmachen(tmp_path) -> None:
    """Zusagen von 19,99 EUR an beide lassen ``ROUND_JOIN`` stehen (D704 Beschluss 3 und 4)."""
    _path, server, uhr, personen = _knoten(tmp_path)
    anna, bruno, chris, _dora = personen
    try:
        verein, leben = _gruenden(server)
        _zusagen(server, uhr, chris, (anna, bruno), leben, betrag=CENT - 1)
        assert _mitmachen(server, chris) == [
            {"scope": verein, "art": MITMACHEN, "sparrunde": verein}
        ]
    finally:
        _stop(server)


def test_ein_verein_hat_kein_mitmachen(tmp_path) -> None:
    """Ein Verein ist keine Sparrunde: niemand bekommt ``ROUND_JOIN`` (D704 Beschluss 4)."""
    _path, server, _uhr, personen = _knoten(tmp_path)
    try:
        _gruenden(server, "verein")
        for person in personen:
            assert _mitmachen(server, person) == []
    finally:
        _stop(server)
