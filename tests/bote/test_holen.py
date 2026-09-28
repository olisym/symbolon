"""Holen ohne Transport: ein Knoten holt, der Nachbar wird nie beliefert (D584 Beschluss 2)."""

from __future__ import annotations

from symbolon.atom import claim_id, signed_bytes
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
        bestand_wirft: type[Exception] | None = None,
        objekte: dict[bytes, object] | None = None,
    ):
        self.claims = claims
        self.objekte = objekte or {}
        self.bestand_wirft = bestand_wirft
        self.aufrufe = 0

    def bestand(self):
        self.aufrufe += 1
        if self.bestand_wirft is not None:
            raise self.bestand_wirft()
        return sorted(self.claims), sorted(self.objekte)

    def claim(self, cid: bytes):
        self.aufrufe += 1
        found = self.claims[cid]
        if isinstance(found, type) and issubclass(found, Exception):
            raise found()
        return found

    def objekt(self, digest: bytes):
        self.aufrufe += 1
        return self.objekte[digest]


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


def test_fehlend_und_formwidrig(tmp_path) -> None:
    """Ein fehlender und ein formwidriger Eintrag zählen je einzeln, der dritte kommt an."""
    eins, zwei, drei = _vouches()
    fremd = _Fremd(
        {claim_id(eins): signed_bytes(eins), claim_id(zwei): None, claim_id(drei): Formwidrig}
    )
    x = _knoten(tmp_path / "x.sqlite")
    try:
        assert holen(HttpKnoten(_url(x)), fremd) == Ergebnis(1, {}, False, 1, 1)
        assert _bestand(x) == {"claims": [claim_id(eins).hex()], "objects": []}
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


def test_formwidriger_bestand(tmp_path) -> None:
    """Ein formwidriger Bestand beendet das Holen ohne weitere Anfrage."""
    fremd = _Fremd({}, bestand_wirft=Formwidrig)
    x = _knoten(tmp_path / "x.sqlite")
    try:
        assert holen(HttpKnoten(_url(x)), fremd) == Ergebnis(0, {}, False, 0, 1)
        assert fremd.aufrufe == 1
        fremd.bestand_wirft = Getrennt
        assert holen(HttpKnoten(_url(x)), fremd) == Ergebnis(0, {}, True, 0, 0)
    finally:
        _stop(x)
