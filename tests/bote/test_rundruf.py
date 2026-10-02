"""Der Rundruf ohne Transport: eigene neue Einträge einmal, Annahme nur von Nachbarn (D636)."""

from __future__ import annotations

import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from symbolon import buendel
from symbolon.atom import claim_id, signed_bytes
from symbolon.bote.kern import (
    RUNDRUF_ANZAHL,
    RUNDRUF_GEHALTEN,
    RUNDRUF_KOPF,
    RUNDRUF_MARKE,
    Grenze,
    HttpKnoten,
    Rundruf,
    einliefern,
    holen,
    rundruf_stuecke,
)
from tests.helpers import Identity, scope_id
from tests.node.test_abgleich import _bestand, _knoten, _url
from tests.node.test_api import _call, _stop
from tools.verein_node import anlegen

_PLATZ = 384
_FENSTER = 600.0
_ICH = b"\x01" * 16
_ANNA = b"\x0a" * 16
_BRUNO = b"\x0b" * 16


def _claim(nummer: int):
    """Je Nummer ein eigener Aussteller; der Knoten nimmt jeden an (D622 Befund 1)."""
    return Identity(f"p51-{nummer}").vouch(
        Identity("p51-Z"), n=4, scope=scope_id("p51-welt"), t=1, t_exp=5000
    )


def _pruefer(schluessel: dict[bytes, Ed25519PrivateKey]):
    def pruefen(von: bytes, signatur: bytes, nachricht: bytes) -> bool | None:
        if von not in schluessel:
            return None
        try:
            schluessel[von].public_key().verify(signatur, nachricht)
        except InvalidSignature:
            return False
        return True

    return pruefen


def _rundruf(knoten, schluessel, quellen=(_ANNA, _BRUNO), platz=_PLATZ):
    """Ein Rundruf über ``knoten`` mit eigenem Schlüssel; dazu die gemeldeten Zeilen."""
    eigener = Ed25519PrivateKey.generate()
    zeilen: list[str] = []
    rundruf = Rundruf(
        HttpKnoten(_url(knoten)),
        _ICH,
        eigener.sign,
        _pruefer(schluessel),
        quellen,
        platz,
        _FENSTER,
        zeilen.append,
    )
    return rundruf, zeilen, eigener


def _paket(schluessel, von: bytes, *claims, marke: bytes = RUNDRUF_MARKE) -> bytes:
    stueck = buendel.schreiben([signed_bytes(claim) for claim in claims], [])
    return von + schluessel.sign(marke + stueck) + stueck


def _ids(knoten) -> tuple[list[bytes], list[bytes]]:
    bestand = _bestand(knoten)
    return (
        [bytes.fromhex(item) for item in bestand["claims"]],
        [bytes.fromhex(item) for item in bestand["objects"]],
    )


def _lokal(knoten, claim) -> None:
    """Ein Eintrag entsteht im eigenen Knoten, nicht über ``/peer/``."""
    status, body = _call(knoten, "POST", "/claims", {"data": signed_bytes(claim).hex()})
    assert status == 200, body


def test_stuecke() -> None:
    """Alles in einem, sonst je Eintrag eines, Objekte zuerst; zu Grosses fehlt
    (D636 Beschluss 3)."""
    claims = [signed_bytes(_claim(nummer)) for nummer in range(3)]
    gross = b"".join(hashlib.sha256(bytes([nummer])).digest() for nummer in range(13))
    objekte = [("motion", b"\x01" * 20), ("motion", gross)]
    assert rundruf_stuecke([], [], _PLATZ) == []
    eines = rundruf_stuecke(claims[:1], objekte[:1], _PLATZ)
    assert eines == [buendel.schreiben(claims[:1], objekte[:1])]
    assert len(eines[0]) <= _PLATZ
    assert len(buendel.schreiben(claims, objekte[:1])) > _PLATZ
    einzeln = rundruf_stuecke(claims, objekte, _PLATZ)
    assert len(buendel.schreiben([], objekte[1:])) > _PLATZ
    assert einzeln == [buendel.schreiben([], objekte[:1])] + [
        buendel.schreiben([claim], []) for claim in claims
    ]
    assert all(len(stueck) <= _PLATZ for stueck in einzeln)


def test_grenze() -> None:
    """Je Absender ``anzahl`` im Fenster, danach wieder (D636 Beschluss 5)."""
    grenze = Grenze(3, 10.0)
    assert [grenze.erlaubt(_ANNA, zeit) for zeit in (0.0, 1.0, 2.0, 3.0)] == [True] * 3 + [False]
    assert grenze.erlaubt(_BRUNO, 3.0)
    assert not grenze.erlaubt(_ANNA, 9.9)
    assert grenze.erlaubt(_ANNA, 10.0)
    assert not grenze.erlaubt(_ANNA, 10.5)
    assert grenze.erlaubt(_ANNA, 11.0)


def test_erster_aufruf_sendet_nichts(tmp_path) -> None:
    """Der Bestand beim Start ist nicht neu (D636 Beschluss 2)."""
    pfad = tmp_path / "x.sqlite"
    anlegen(pfad)
    x = _knoten(pfad)
    try:
        rundruf, _zeilen, _eigener = _rundruf(x, {})
        claims, objekte = _ids(x)
        assert claims and objekte
        assert rundruf.senden(claims, objekte, 0.0) == []
        assert rundruf.senden(claims, objekte, 1.0) == []
    finally:
        _stop(x)


def test_eigener_eintrag_geht_einmal(tmp_path) -> None:
    """Was im eigenen Knoten entsteht, geht einmal hinaus: Adresse, Signatur, Bündel
    (D636 Beschluss 2 und 3)."""
    x = _knoten(tmp_path / "x.sqlite", _claim(0))
    try:
        rundruf, _zeilen, eigener = _rundruf(x, {})
        assert rundruf.senden(*_ids(x), 0.0) == []
        _lokal(x, _claim(1))
        (paket,) = rundruf.senden(*_ids(x), 1.0)
        stueck = paket[RUNDRUF_KOPF:]
        assert paket[:16] == _ICH
        eigener.public_key().verify(paket[16:RUNDRUF_KOPF], RUNDRUF_MARKE + stueck)
        assert buendel.lesen(stueck) == ([signed_bytes(_claim(1))], [])
        assert rundruf.senden(*_ids(x), 2.0) == []
    finally:
        _stop(x)


def test_geholtes_und_gehoertes_geht_nicht_weiter(tmp_path) -> None:
    """Was über den Boten kam, sendet er nicht; Eigenes daneben schon (D636 Beschluss 2)."""
    x = _knoten(tmp_path / "x.sqlite")
    anna = Ed25519PrivateKey.generate()
    try:
        rundruf, zeilen, _eigener = _rundruf(x, {_ANNA: anna})
        assert rundruf.senden(*_ids(x), 0.0) == []
        assert einliefern(rundruf.mein, [signed_bytes(_claim(1))], []) == (1, {}, False)
        rundruf.empfangen(_paket(anna, _ANNA, _claim(2)), 1.0, frozenset())
        assert zeilen == [f"{_ANNA.hex()}: rundruf geholt=1 abgewiesen={{}}"]
        _lokal(x, _claim(3))
        assert len(_ids(x)[0]) == 3
        (paket,) = rundruf.senden(*_ids(x), 2.0)
        assert buendel.lesen(paket[RUNDRUF_KOPF:]) == ([signed_bytes(_claim(3))], [])
        assert rundruf.mein.eingeliefert == set()
    finally:
        _stop(x)


def test_geholter_verein_geht_nicht_weiter(tmp_path) -> None:
    """Auch geholte Objekte sind nicht neu (D636 Beschluss 2)."""
    pfad = tmp_path / "y.sqlite"
    anlegen(pfad)
    y = _knoten(pfad)
    x = _knoten(tmp_path / "x.sqlite")
    try:
        rundruf, _zeilen, _eigener = _rundruf(x, {})
        assert rundruf.senden(*_ids(x), 0.0) == []
        geholt = holen(rundruf.mein, HttpKnoten(_url(y))).geholt
        claims, objekte = _ids(x)
        assert geholt == len(claims) + len(objekte) and objekte
        assert rundruf.senden(claims, objekte, 1.0) == []
    finally:
        _stop(x)
        _stop(y)


def test_annahme_nur_vom_nachbarn(tmp_path) -> None:
    """Fremd, gesperrt, formwidrige Sperrliste, falsche Signatur, fehlende Marke: nichts
    (D636 Beschluss 4)."""
    x = _knoten(tmp_path / "x.sqlite")
    anna = Ed25519PrivateKey.generate()
    fremd = Ed25519PrivateKey.generate()
    fremder = b"\x0f" * 16
    try:
        rundruf, zeilen, _eigener = _rundruf(x, {_ANNA: anna, fremder: fremd})
        gut = _paket(anna, _ANNA, _claim(1))
        rundruf.empfangen(_paket(fremd, fremder, _claim(1)), 0.0, frozenset())
        rundruf.empfangen(gut, 0.0, frozenset({_ANNA}))
        rundruf.empfangen(gut, 0.0, None)
        rundruf.empfangen(_paket(fremd, _ANNA, _claim(1)), 0.0, frozenset())
        rundruf.empfangen(_paket(anna, _ANNA, _claim(1), marke=b""), 0.0, frozenset())
        rundruf.empfangen(gut[:RUNDRUF_KOPF], 0.0, frozenset())
        rundruf.empfangen(bytearray(gut), 0.0, frozenset())
        assert _ids(x) == ([], [])
        assert zeilen == []
        rundruf.empfangen(gut, 0.0, frozenset({_BRUNO}))
        assert _ids(x) == ([claim_id(_claim(1))], [])
    finally:
        _stop(x)


def test_formwidriges_buendel_wirft_nicht(tmp_path) -> None:
    """Gültig signiert, aber kein Bündel: still verworfen, und es zählt (D636 Beschluss 4)."""
    x = _knoten(tmp_path / "x.sqlite")
    anna = Ed25519PrivateKey.generate()
    try:
        rundruf, zeilen, _eigener = _rundruf(x, {_ANNA: anna})
        muell = b"\xff" * 40
        for nummer in range(RUNDRUF_ANZAHL):
            rundruf.empfangen(_ANNA + anna.sign(RUNDRUF_MARKE + muell) + muell, nummer, frozenset())
        rundruf.empfangen(_paket(anna, _ANNA, _claim(1)), RUNDRUF_ANZAHL, frozenset())
        assert _ids(x) == ([], [])
        assert zeilen == []
    finally:
        _stop(x)


def test_grenze_je_absender(tmp_path) -> None:
    """Der siebzehnte Rundruf eines Absenders im Fenster wird verworfen, ein anderer Absender
    nicht (D636 Beschluss 5)."""
    x = _knoten(tmp_path / "x.sqlite")
    anna = Ed25519PrivateKey.generate()
    bruno = Ed25519PrivateKey.generate()
    try:
        rundruf, _zeilen, _eigener = _rundruf(x, {_ANNA: anna, _BRUNO: bruno})
        for nummer in range(RUNDRUF_ANZAHL + 1):
            rundruf.empfangen(_paket(anna, _ANNA, _claim(nummer)), float(nummer), frozenset())
        assert len(_ids(x)[0]) == RUNDRUF_ANZAHL
        assert claim_id(_claim(RUNDRUF_ANZAHL)) not in _ids(x)[0]
        rundruf.empfangen(_paket(bruno, _BRUNO, _claim(100)), 20.0, frozenset())
        assert len(_ids(x)[0]) == RUNDRUF_ANZAHL + 1
        rundruf.empfangen(_paket(anna, _ANNA, _claim(RUNDRUF_ANZAHL)), _FENSTER, frozenset())
        assert claim_id(_claim(RUNDRUF_ANZAHL)) in _ids(x)[0]
    finally:
        _stop(x)


def test_eigene_grenze(tmp_path) -> None:
    """Auch der Sender hält die Grenze; der Rest bleibt dem Holen (D636 Beschluss 5)."""
    x = _knoten(tmp_path / "x.sqlite")
    try:
        rundruf, _zeilen, _eigener = _rundruf(x, {})
        assert rundruf.senden(*_ids(x), 0.0) == []
        for nummer in range(RUNDRUF_ANZAHL + 1):
            _lokal(x, _claim(nummer))
        pakete = rundruf.senden(*_ids(x), 1.0)
        assert len(pakete) == RUNDRUF_ANZAHL
        assert all(len(paket) <= RUNDRUF_KOPF + _PLATZ for paket in pakete)
        assert rundruf.senden(*_ids(x), 2.0) == []
    finally:
        _stop(x)


def test_zu_grosser_eintrag_bleibt(tmp_path) -> None:
    """Ein Eintrag, der allein nicht passt, wird nicht gesendet (D636 Beschluss 3)."""
    x = _knoten(tmp_path / "x.sqlite")
    try:
        klein = len(buendel.schreiben([signed_bytes(_claim(1))], [])) - 1
        rundruf, _zeilen, _eigener = _rundruf(x, {}, platz=klein)
        assert rundruf.senden(*_ids(x), 0.0) == []
        _lokal(x, _claim(1))
        assert rundruf.senden(*_ids(x), 1.0) == []
    finally:
        _stop(x)


def test_gehalten_bis_der_schluessel_bekannt_ist(tmp_path) -> None:
    """Ohne Schlüssel gehalten, höchstens ``RUNDRUF_GEHALTEN``; mit Schlüssel nachgeholt
    (D636 Beschluss 4)."""
    x = _knoten(tmp_path / "x.sqlite")
    anna = Ed25519PrivateKey.generate()
    bruno = Ed25519PrivateKey.generate()
    schluessel: dict[bytes, Ed25519PrivateKey] = {}
    je = RUNDRUF_GEHALTEN // 2 + 2
    assert je <= RUNDRUF_ANZAHL
    try:
        rundruf, _zeilen, _eigener = _rundruf(x, schluessel)
        for nummer in range(je):
            rundruf.empfangen(_paket(anna, _ANNA, _claim(nummer)), 0.0, frozenset())
        for nummer in range(je):
            rundruf.empfangen(_paket(bruno, _BRUNO, _claim(100 + nummer)), 0.0, frozenset())
        assert _ids(x) == ([], [])
        schluessel[_ANNA] = anna
        rundruf.nachholen(_ANNA, 1.0, frozenset())
        assert len(_ids(x)[0]) == je
        schluessel[_BRUNO] = bruno
        rundruf.nachholen(_BRUNO, 2.0, frozenset())
        assert len(_ids(x)[0]) == RUNDRUF_GEHALTEN < 2 * je
        rundruf.empfangen(_paket(bruno, _BRUNO, _claim(200)), 3.0, frozenset())
        assert len(_ids(x)[0]) == RUNDRUF_GEHALTEN + 1
    finally:
        _stop(x)
