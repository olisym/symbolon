"""Eine Gründung verwerfen, die Vorlagen für die Seite, gemeinsame Vektoren (D651)."""

from __future__ import annotations

import json
from pathlib import Path

from symbolon.node import gruendung as modul
from symbolon.node.gruendung import wert_gueltig
from tests.node.test_api import _stop
from tests.node.test_gruendung import FELDER, _drei, _json, _knoten

_VEKTOREN = Path(__file__).resolve().parents[2] / "symbolon" / "node" / "static" / "vektoren.json"


def _gruenden(server, felder=FELDER):
    status, antwort = _json(
        server, "POST", "/gruenden", {"vorlage": "verein", "gruender": _drei(), "felder": felder}
    )
    assert status == 200
    return antwort


def _handeln(server, person, art, **mehr):
    status, folge = _json(server, "POST", "/sim/intent", {"I": person.pub.hex(), "art": art, **mehr})
    assert status == 200, folge
    return folge


def test_vorlagen_kommen_aus_dem_knoten(tmp_path, monkeypatch) -> None:
    """``GET /vorlagen`` nennt je Vorlage, was die Seite braucht, bei jedem Aufruf neu gelesen
    (D651 Beschluss 2)."""
    _path, server, _personen = _knoten(tmp_path)
    try:
        erwartet = {}
        for name, muster in modul.VORLAGEN.items():
            erwartet[name] = {
                "fassung": muster["fassung"],
                "mindestens": muster["mindestens"],
                "felder": list(muster["felder"]),
                "pflicht": list(muster["pflicht"]),
                "geschuetzt": list(muster["geschuetzt"]),
                "typen": dict(muster["typen"]),
                "thresholds": {art: list(paar) for art, paar in muster["thresholds"].items()},
            }
        assert _json(server, "GET", "/vorlagen") == (200, erwartet)
        assert sorted(erwartet["verein"]) == sorted(
            ["fassung", "mindestens", "felder", "pflicht", "geschuetzt", "typen", "thresholds"]
        )
        geaendert = dict(modul.VORLAGEN["verein"])
        geaendert["mindestens"] = 5
        monkeypatch.setitem(modul.VORLAGEN, "verein", geaendert)
        assert _json(server, "GET", "/vorlagen")[1]["verein"]["mindestens"] == 5
    finally:
        _stop(server)


def test_verwerfen_blendet_beide_scopes_aus_und_entfernt_nichts(tmp_path) -> None:
    """Nach ``POST /verwerfen`` nennt ``/scopes`` weder Verein noch Vereinsleben, niemand hat eine
    Aufgabe, und der Bestand ist derselbe (D651 Beschluss 6)."""
    _path, server, (anna, bruno, chris, _dora) = _knoten(tmp_path)
    try:
        antwort = _gruenden(server)
        verein, leben = antwort["verein"], antwort["vereinsleben"]
        _handeln(server, anna, "accept-rules", scope=verein)
        stand = _json(server, "GET", "/stand")[1]
        bestand = _json(server, "GET", "/peer/bestand")[1]
        assert _json(server, "POST", "/verwerfen", {"scope": verein}) == (200, {})
        assert _json(server, "GET", "/scopes") == (200, [])
        for person in (anna, bruno, chris):
            assert _json(server, "GET", f"/tasks/{person.pub.hex()}") == (200, [])
        assert _json(server, "GET", "/stand")[1] == stand
        assert _json(server, "GET", "/peer/bestand")[1] == bestand
        assert _json(server, "GET", f"/scopes/{verein}")[0] == 200
        assert _json(server, "GET", f"/scopes/{leben}")[0] == 200
        # Wiederholt: dieselbe Antwort, derselbe Zustand.
        assert _json(server, "POST", "/verwerfen", {"scope": verein}) == (200, {})
        assert _json(server, "GET", "/scopes") == (200, [])
    finally:
        _stop(server)


def test_verworfen_bleibt_ueber_einen_neustart(tmp_path) -> None:
    """Was verworfen ist, steht im Bestand des Knotens, nicht im Speicher des Prozesses
    (D651 Beschluss 6)."""
    from tests.node.test_api import _start

    path, server, _personen = _knoten(tmp_path)
    try:
        verein = _gruenden(server)["verein"]
        assert _json(server, "POST", "/verwerfen", {"scope": verein})[0] == 200
    finally:
        _stop(server)
    server = _start(path, lambda: 1000)
    try:
        assert _json(server, "GET", "/scopes") == (200, [])
    finally:
        _stop(server)


def test_dieselbe_gruendung_noch_einmal_zeigt_sie_wieder(tmp_path) -> None:
    """``POST /gruenden`` mit denselben Angaben nimmt beide Scopes aus den verworfenen; eine frühere
    Bestätigung gilt dann wieder (D651 Beschluss 6, D641 Beschluss 4)."""
    _path, server, (anna, bruno, _chris, _dora) = _knoten(tmp_path)
    try:
        antwort = _gruenden(server)
        verein, leben = antwort["verein"], antwort["vereinsleben"]
        _handeln(server, anna, "accept-rules", scope=verein)
        assert _json(server, "POST", "/verwerfen", {"scope": verein})[0] == 200
        assert _gruenden(server) == antwort
        assert _json(server, "GET", "/scopes") == (200, sorted([verein, leben]))
        assert _json(server, "GET", f"/tasks/{anna.pub.hex()}") == (200, [])
        assert len(_json(server, "GET", f"/tasks/{bruno.pub.hex()}")[1]) == 1
    finally:
        _stop(server)


def test_nach_dem_verwerfen_eine_andere_gruendung(tmp_path) -> None:
    """Eine zweite Gründung derselben drei mit anderem Namen steht allein in ``/scopes``
    (D651 Beschluss 6, D640 Befund 8)."""
    _path, server, _personen = _knoten(tmp_path)
    try:
        erste = _gruenden(server)
        assert _json(server, "POST", "/verwerfen", {"scope": erste["verein"]})[0] == 200
        zweite = _gruenden(server, {**FELDER, "name": "Laufgruppe am Hafen"})
        assert zweite["verein"] != erste["verein"]
        assert zweite["vereinsleben"] != erste["vereinsleben"]
        assert _json(server, "GET", "/scopes") == (
            200,
            sorted([zweite["verein"], zweite["vereinsleben"]]),
        )
    finally:
        _stop(server)


def test_verwerfen_nur_in_der_gruendung(tmp_path) -> None:
    """``NOT_FOUNDING``, sobald alle bestätigt haben, auch in einer späteren Fassung mit offenen
    Bestätigungen, und für einen Scope, der kein Verein ist; ein unbekannter Scope ist 404
    (D651 Beschluss 6)."""
    _path, server, (anna, bruno, chris, dora) = _knoten(tmp_path)
    try:
        antwort = _gruenden(server)
        verein, leben = antwort["verein"], antwort["vereinsleben"]
        beide = sorted([verein, leben])
        assert _json(server, "POST", "/verwerfen", {"scope": leben}) == (400, "NOT_FOUNDING")
        assert _json(server, "POST", "/verwerfen", {"scope": "ab" * 32})[0] == 404
        assert _json(server, "POST", "/verwerfen", {})[0] == 400
        for person in (anna, bruno):
            _handeln(server, person, "accept-rules", scope=verein)
        # Zwei von drei haben bestätigt: noch Gründung. Geprüft wird das am dritten Fall unten;
        # hier bestätigt Chris, und der Verein besteht.
        _handeln(server, chris, "accept-rules", scope=verein)
        assert _json(server, "POST", "/verwerfen", {"scope": verein}) == (400, "NOT_FOUNDING")
        assert _json(server, "GET", "/scopes") == (200, beide)
        # Zweite Fassung: Dora ist aufgenommen, alle stehen auf GRANT_ONLY.
        _handeln(server, anna, "propose", scope=verein, change={"add": dora.pub.hex()})
        antrag = _json(server, "GET", f"/proposals/{verein}")[1][0]["proposal"]
        for person in (anna, bruno):
            _handeln(server, person, "vote", proposal=antrag, choice="yes")
        _handeln(server, chris, "ratify", proposal=antrag)
        sicht = _json(server, "GET", f"/scopes/{verein}")[1]
        assert sicht["state"]["epoch"]["index"] == 2
        assert {eintrag[1]["state"] for eintrag in sicht["verein"]["membership"]} == {"GRANT_ONLY"}
        assert _json(server, "POST", "/verwerfen", {"scope": verein}) == (400, "NOT_FOUNDING")
        assert _json(server, "GET", "/scopes") == (200, beide)
    finally:
        _stop(server)


def test_verwerfen_solange_einer_fehlt(tmp_path) -> None:
    """Haben zwei von drei bestätigt, ist es noch eine Gründung (D651 Beschluss 6)."""
    _path, server, (anna, bruno, _chris, _dora) = _knoten(tmp_path)
    try:
        verein = _gruenden(server)["verein"]
        for person in (anna, bruno):
            _handeln(server, person, "accept-rules", scope=verein)
        assert _json(server, "POST", "/verwerfen", {"scope": verein}) == (200, {})
        assert _json(server, "GET", "/scopes") == (200, [])
    finally:
        _stop(server)


def test_gemeinsame_vektoren_fuer_seite_und_knoten() -> None:
    """Jeder Text, den die Seite aus einer Eingabe baut, gilt dem Knoten; ob ein Betrag gilt, sagt
    die Datei wie der Knoten, und die Datei nennt gültige und ungültige (D648 Beschluss 6,
    D651 Beschluss 3). Dass die Datei aus dem Werkzeug stammt, prüft ``test_vektoren_bytegleich``.
    """
    vektoren = json.loads(_VEKTOREN.read_text(encoding="utf-8"))
    betraege, eingaben, texte = vektoren["betrag"], vektoren["betrag_eingabe"], vektoren["text_eingabe"]
    for fall in betraege:
        assert wert_gueltig("betrag", fall["text"]) is fall["gilt"], fall
    assert {"text": "24,00 EUR im Jahr", "gilt": True, "cent": 2400, "faelligkeit": "Jahr"} in betraege
    assert {"text": "0,00 EUR im Jahr", "gilt": False} in betraege
    for fall in eingaben:
        if fall["text"] is not None:
            assert wert_gueltig("betrag", fall["text"]) is True, fall
    for fall in texte:
        if fall["text"] is not None:
            assert wert_gueltig("text", fall["text"]) is True, fall
    assert any(fall["text"] is None for fall in eingaben)
    assert any(fall["text"] is not None for fall in eingaben)
    assert any(fall["text"] is None for fall in texte)
    assert any(fall["text"] is not None for fall in texte)
