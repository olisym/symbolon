"""Holen ohne Transport: ein Knoten holt, der Nachbar wird nie beliefert (D584 Beschluss 2)."""

from __future__ import annotations

import pytest

from symbolon import buendel
from symbolon.atom import claim_id, signed_bytes
from symbolon.bote import rbsr
from symbolon.bote.kern import Ergebnis, Formwidrig, Getrennt, HttpKnoten, holen
from tests.helpers import Identity, scope_id
from tests.node.test_abgleich import _bestand, _knoten, _soll, _url
from tests.node.test_api import _call, _start, _stop
from tools.verein_node import anlegen

_NOW = 1000
_T_EXP = 5000


class _Fremd:
    """Ein Nachbar im Speicher; zählt jede Anfrage."""

    def __init__(
        self,
        claims: dict[bytes, object],
        abgleich_wirft: type[Exception] | None = None,
        objekte: dict[bytes, object] | None = None,
    ):
        self.claims = claims
        self.objekte = objekte or {}
        self.abgleich_wirft = abgleich_wirft
        self.paket_wirft: type[Exception] | None = None
        self.paket_roh: bytes | None = None
        self.aufrufe = 0

    def abgleich(self, roh: bytes):
        """Wie ein Nachbar über den Draht: die Anfrage gelesen, die Antwort aus dem Bestand."""
        self.aufrufe += 1
        if self.abgleich_wirft is not None:
            raise self.abgleich_wirft()
        s = rbsr.schluessel(list(self.claims), list(self.objekte))
        return rbsr.kodieren(rbsr.antworten(s, rbsr.lesen(roh, vom_boten=True)))

    def paket(self, claims: list[bytes], objekte: list[bytes]):
        """Ein Bündel aus dem, was da ist; ``bytes`` unter einer Kennung sind das ganze Paket."""
        self.aufrufe += 1
        self.gefragt = (claims, objekte)
        if self.paket_wirft is not None:
            raise self.paket_wirft()
        if self.paket_roh is not None:
            return self.paket_roh
        return buendel.schreiben(
            [self.claims[c] for c in claims if self.claims[c] is not None],
            [self.objekte[o] for o in objekte if self.objekte[o] is not None],
        )


def _vouches():
    scope = scope_id("p36-welt")
    C = Identity("p36-C")
    return [Identity(f"p36-{i}").vouch(C, n=4, scope=scope, t=1, t_exp=_T_EXP) for i in "ABD"]


def test_verein(tmp_path) -> None:
    """Der Verein geht ganz mit; ein zweites Holen bringt nichts (D584 Beschluss 2)."""
    path_a = tmp_path / "a.sqlite"
    anlegen(path_a)
    soll = _soll(path_a)
    a = _start(path_a, lambda: _NOW)
    b = _knoten(tmp_path / "b.sqlite")
    try:
        erste = holen(HttpKnoten(_url(b)), HttpKnoten(_url(a)))
        assert erste == Ergebnis(len(soll["claims"]) + len(soll["objects"]), {}, False, 0, 0)
        assert _bestand(b) == soll
        assert _bestand(a) == soll
        assert holen(HttpKnoten(_url(b)), HttpKnoten(_url(a))) == Ergebnis(0, {}, False, 0, 0)
    finally:
        _stop(a)
        _stop(b)


def test_fremder_widerruf(tmp_path) -> None:
    """Abweisung zählt, der Nachbar bleibt unberührt; beide Richtungen enden gleich (D514, D516)."""
    scope = scope_id("p20-welt")
    A = Identity("p20-A")
    B = Identity("p20-B")
    C = Identity("p20-C")
    v = A.vouch(C, n=4, scope=scope, t=1, t_exp=_T_EXP)
    w = B.revoke(v, t=2)
    n = B.vouch(C, n=4, scope=scope, t=3, t_exp=_T_EXP)
    x = _knoten(tmp_path / "x.sqlite", v)
    y = _knoten(tmp_path / "y.sqlite", w, n)
    try:
        vorher_y = _bestand(y)
        e = holen(HttpKnoten(_url(x)), HttpKnoten(_url(y)))
        assert e == Ergebnis(1, {"ForeignLifecycle": 1}, False, 0, 0)
        soll = {"claims": sorted(claim_id(item).hex() for item in (v, n)), "objects": []}
        assert _bestand(x) == soll
        assert _bestand(y) == vorher_y
        assert holen(HttpKnoten(_url(y)), HttpKnoten(_url(x))) == Ergebnis(1, {}, False, 0, 0)
        assert _bestand(y) == soll
    finally:
        _stop(x)
        _stop(y)


def test_eigener_knoten_getrennt(tmp_path) -> None:
    """Ist der eigene Knoten getrennt, wird der Nachbar nicht gefragt (D516 Beschluss 3)."""
    x = _knoten(tmp_path / "x.sqlite")
    fremd = _Fremd({claim_id(c): signed_bytes(c) for c in _vouches()})
    try:
        status, _body = _call(x, "POST", "/getrennt", {"getrennt": True})
        assert status == 200
        assert holen(HttpKnoten(_url(x)), fremd) == Ergebnis(0, {}, True, 0, 0)
        assert fremd.aufrufe == 0
    finally:
        _stop(x)


def test_nachbar_getrennt(tmp_path) -> None:
    """Ist der Nachbar getrennt, bleibt der eigene Bestand, wie er war (D516 Beschluss 3)."""
    x = _knoten(tmp_path / "x.sqlite")
    y = _knoten(tmp_path / "y.sqlite", *_vouches())
    try:
        status, _body = _call(y, "POST", "/getrennt", {"getrennt": True})
        assert status == 200
        assert holen(HttpKnoten(_url(x)), HttpKnoten(_url(y))) == Ergebnis(0, {}, True, 0, 0)
        assert _bestand(x) == {"claims": [], "objects": []}
    finally:
        _stop(x)
        _stop(y)


def test_fehlend_und_abgewiesen(tmp_path) -> None:
    """Ein fehlender Eintrag zählt als fehlend, formwidrige Claim-Bytes weist der Knoten ab.

    Seit D614 urteilt über den einzelnen Eintrag der Knoten; formwidrig ist nur das Bündel.
    """
    eins, zwei, drei = _vouches()
    fremd = _Fremd(
        {claim_id(eins): signed_bytes(eins), claim_id(zwei): None, claim_id(drei): b"\xff"}
    )
    x = _knoten(tmp_path / "x.sqlite")
    try:
        e = holen(HttpKnoten(_url(x)), fremd)
        assert (e.geholt, e.getrennt, e.fehlend, e.formwidrig) == (1, False, 1, 0)
        assert sum(e.abgewiesen.values()) == 1
        assert _bestand(x) == {"claims": [claim_id(eins).hex()], "objects": []}
    finally:
        _stop(x)


def test_eine_anfrage_fuer_alles(tmp_path) -> None:
    """Nach dem Bestand genau eine Anfrage, mit allem Fehlenden, sortiert (D614 Beschluss 4)."""
    vouches = _vouches()
    fremd = _Fremd({claim_id(c): signed_bytes(c) for c in vouches})
    x = _knoten(tmp_path / "x.sqlite", vouches[0])
    try:
        assert holen(HttpKnoten(_url(x)), fremd) == Ergebnis(2, {}, False, 0, 0)
        assert fremd.aufrufe == 2
        assert fremd.gefragt == (sorted(claim_id(c) for c in vouches[1:]), [])
    finally:
        _stop(x)


def test_nichts_fehlt_keine_anfrage(tmp_path) -> None:
    """Fehlt nichts, wird kein Paket angefragt (D614 Beschluss 4)."""
    vouches = _vouches()
    fremd = _Fremd({claim_id(c): signed_bytes(c) for c in vouches[:1]})
    x = _knoten(tmp_path / "x.sqlite", *vouches)
    try:
        assert holen(HttpKnoten(_url(x)), fremd) == Ergebnis(0, {}, False, 0, 0)
        assert fremd.aufrufe == 1
    finally:
        _stop(x)


def test_formwidriges_buendel(tmp_path) -> None:
    """Ein formwidriges Bündel zählt einmal und liefert nichts ein (D614 Beschluss 4)."""
    vouches = _vouches()
    fremd = _Fremd({claim_id(c): signed_bytes(c) for c in vouches})
    gut = buendel.schreiben([signed_bytes(c) for c in vouches], [])
    x = _knoten(tmp_path / "x.sqlite")
    try:
        for roh in (b"\xff", gut + b"\x00", gut[:-1]):
            fremd.paket_roh = roh
            assert holen(HttpKnoten(_url(x)), fremd) == Ergebnis(0, {}, False, 0, 1)
        fremd.paket_roh = None
        fremd.paket_wirft = Formwidrig
        assert holen(HttpKnoten(_url(x)), fremd) == Ergebnis(0, {}, False, 0, 1)
        fremd.paket_wirft = Getrennt
        assert holen(HttpKnoten(_url(x)), fremd) == Ergebnis(0, {}, True, 0, 0)
        assert _bestand(x) == {"claims": [], "objects": []}
    finally:
        _stop(x)


def test_ungefragtes_urteilt_der_knoten(tmp_path) -> None:
    """Was ungefragt im Bündel steht, wird eingeliefert; der Knoten urteilt (D614 Beschluss 4)."""
    eins, zwei, _drei = _vouches()
    fremd = _Fremd({claim_id(eins): signed_bytes(eins)})
    fremd.paket_roh = buendel.schreiben([signed_bytes(eins), signed_bytes(zwei)], [])
    x = _knoten(tmp_path / "x.sqlite")
    try:
        assert holen(HttpKnoten(_url(x)), fremd) == Ergebnis(2, {}, False, 0, 0)
    finally:
        _stop(x)


def test_fehlendes_objekt(tmp_path) -> None:
    """Ein Objekt, das der Nachbar nennt und nicht liefert, zählt als fehlend."""
    fremd = _Fremd({}, objekte={bytes(32): None})
    x = _knoten(tmp_path / "x.sqlite")
    try:
        assert holen(HttpKnoten(_url(x)), fremd) == Ergebnis(0, {}, False, 1, 0)
        assert fremd.aufrufe == 2
    finally:
        _stop(x)


def test_formwidriger_abgleich(tmp_path) -> None:
    """Eine formwidrige Antwort im Abgleich beendet das Holen ohne weitere Anfrage (D617)."""
    fremd = _Fremd({}, abgleich_wirft=Formwidrig)
    x = _knoten(tmp_path / "x.sqlite")
    try:
        assert holen(HttpKnoten(_url(x)), fremd) == Ergebnis(0, {}, False, 0, 1)
        assert fremd.aufrufe == 1
        fremd.abgleich_wirft = Getrennt
        assert holen(HttpKnoten(_url(x)), fremd) == Ergebnis(0, {}, True, 0, 0)
    finally:
        _stop(x)


def test_nur_formwidrig_zaehlt(tmp_path, monkeypatch) -> None:
    """Nur ``buendel.Formwidrig`` zählt als formwidrig; ein anderer Fehler bleibt einer (D615)."""
    vouches = _vouches()
    fremd = _Fremd({claim_id(c): signed_bytes(c) for c in vouches})

    def kaputt(_roh):
        raise ValueError("kein Formfehler")

    monkeypatch.setattr(buendel, "lesen", kaputt)
    x = _knoten(tmp_path / "x.sqlite")
    try:
        with pytest.raises(ValueError, match="kein Formfehler"):
            holen(HttpKnoten(_url(x)), fremd)
    finally:
        _stop(x)


class _Luegner(_Fremd):
    """Ein Nachbar, dessen Antwort nicht in der Form aus D617 ist."""

    def abgleich(self, _roh: bytes):
        self.aufrufe += 1
        return rbsr.kodieren([(None, rbsr.FEHLT, [bytes([2]) + bytes(32)])])


def test_formwidrige_antwort_im_abgleich(tmp_path) -> None:
    """Eine Antwort ausserhalb der Form zählt einmal und fragt kein Paket (D617 Beschluss 2)."""
    fremd = _Luegner({})
    x = _knoten(tmp_path / "x.sqlite")
    try:
        assert holen(HttpKnoten(_url(x)), fremd) == Ergebnis(0, {}, False, 0, 1)
        assert fremd.aufrufe == 1
    finally:
        _stop(x)


def test_viele_eintraege(tmp_path) -> None:
    """Ein ganzer Verein über HTTP geholt, der Nachbar ein ``HttpKnoten`` (D617)."""
    path_a = tmp_path / "a.sqlite"
    anlegen(path_a)
    soll = _soll(path_a)
    a = _start(path_a, lambda: _NOW)
    b = _knoten(tmp_path / "b.sqlite")
    try:
        e = holen(HttpKnoten(_url(b)), HttpKnoten(_url(a)))
        assert e.geholt == len(soll["claims"]) + len(soll["objects"])
        assert (e.fehlend, e.formwidrig) == (0, 0)
        assert _bestand(b) == soll
    finally:
        _stop(a)
        _stop(b)
