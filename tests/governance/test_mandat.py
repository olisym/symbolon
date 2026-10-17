"""Mandat mit Rahmen, Prototyp (LANDKARTE §11, D710).

Bruno (BOB) wird für den Privatweg bestellt; Rahmen: ``auftrag@1``. Die Welt ist die aus
``test_sachantraege``: vier Mitglieder, ein Sachantrag trägt mit drei Ja.
"""

from __future__ import annotations

from symbolon import cbor_canon
from symbolon.atom import claim_id
from symbolon.governance.chain import resolve_stand
from symbolon.governance.mandate import (
    MandateStatus as S,
    mandate_id,
    mandate_view,
)
from symbolon.governance.objects import Motion
from symbolon.index import classify_all

from .fixtures import C1, EPOCH_1, GENESIS_D, N_D, NOW, nuc, policy_of
from .test_sachantraege import E1, _Welt

RAHMEN = {0: ["auftrag@1"]}


def _eintrag(w: _Welt, *, rahmen=None, label="Verwalter Weg", holder=None, end=None) -> dict:
    e = {0: (holder or w.bob).pub, 1: rahmen or RAHMEN, 2: label}
    if end is not None:
        e[3] = end
    return e


def _mid(e: dict) -> bytes:
    return mandate_id(N_D, {k: e[k] for k in (0, 1, 2)})


def _antrag(changes: dict) -> Motion:
    return Motion({0: N_D, 1: E1, 2: changes})


class _Fall:
    """Eine Welt mit bekannten Sachanträgen und Hilfen für Bestellung, Akt, Ende."""

    def __init__(self) -> None:
        self.w = _Welt()
        self.known: dict[bytes, Motion] = {}

    def beschliessen(self, changes: dict, *, ja: int = 3) -> Motion:
        m = _antrag(changes)
        self.known[m.motion_hash] = m
        w = self.w
        stimmen = [w.ja(who, m.motion_hash) for who in (w.alice, w.carol, w.dave, w.bob)[:ja]]
        w.ratify(w.alice, m.motion_hash, stimmen)
        return m

    def bestellen(self, e: dict, *, feld="mandat:weg", ja: int = 3) -> Motion:
        return self.beschliessen({feld: [[], [e]]}, ja=ja)

    def ack(self, who, e: dict, *, scope=N_D):
        c = who.claim(p=nuc(scope, "mandate-ack"), J=(3, _mid(e)), t=self.w.t(), N=scope)
        self.w.claims.append(c)
        return c

    def ende(self, who, e: dict, v=None):
        c = who.claim(p=nuc(N_D, "mandate-end"), J=(3, _mid(e)), t=self.w.t(), N=N_D, v=v)
        self.w.claims.append(c)
        return c

    def akt(self, who, name="auftrag"):
        c = who.claim(p=nuc(N_D, name), J=(1, who.pub), t=self.w.t(), N=N_D)
        self.w.claims.append(c)
        return c

    def sicht(self):
        store = self.w.store()
        stand = resolve_stand(store, epoch=EPOCH_1, genesis_obj=GENESIS_D, constitution_obj=C1,
                              known_proposals=self.known, now=NOW).stand_obj
        cls = classify_all(store, NOW, policy_of(C1))
        return mandate_view(store, cls, N_D, stand)


def _v_ende(cid: bytes) -> bytes:
    return cbor_canon.encode({0: cid})


# MV-1: bestellt, gegengezeichnet, Akt im Rahmen.
def test_mv1_akt_im_rahmen_ist_akt_der_gruppe() -> None:
    f = _Fall()
    e = _eintrag(f.w)
    f.bestellen(e)
    f.ack(f.w.bob, e)
    a = f.akt(f.w.bob)
    assert f.sicht().status(a) is S.COVERED


# MV-2: ausserhalb des Rahmens bleibt eigene Aussage.
def test_mv2_akt_ausserhalb_des_rahmens() -> None:
    f = _Fall()
    e = _eintrag(f.w)
    f.bestellen(e)
    f.ack(f.w.bob, e)
    a = f.akt(f.w.bob, "verkauf")
    assert f.sicht().status(a) is S.OUTSIDE


# MV-3: ein Akt vor der Gegenzeichnung ist nicht gedeckt.
def test_mv3_vor_der_gegenzeichnung() -> None:
    f = _Fall()
    e = _eintrag(f.w)
    f.bestellen(e)
    a = f.akt(f.w.bob)
    f.ack(f.w.bob, e)
    assert f.sicht().status(a) is S.BEFORE_ACK


# MV-4: ohne Gegenzeichnung kein Mandat.
def test_mv4_ohne_gegenzeichnung() -> None:
    f = _Fall()
    e = _eintrag(f.w)
    f.bestellen(e)
    a = f.akt(f.w.bob)
    assert f.sicht().status(a) is S.NONE


# MV-5: nicht festgestellt (zwei Ja reichen nicht) heisst nicht bestellt.
def test_mv5_bestellung_nicht_festgestellt() -> None:
    f = _Fall()
    e = _eintrag(f.w)
    f.bestellen(e, ja=2)
    f.ack(f.w.bob, e)
    a = f.akt(f.w.bob)
    assert f.sicht().status(a) is S.NONE


# MV-6: Abruf durch Sachantrag mit dem letzten gedeckten Akt im Eintrag.
def test_mv6_abruf_mit_letztem_akt() -> None:
    f = _Fall()
    e = _eintrag(f.w)
    f.bestellen(e)
    f.ack(f.w.bob, e)
    a1 = f.akt(f.w.bob)
    a2 = f.akt(f.w.bob)
    f.beschliessen({"mandat:weg": [[e], [_eintrag(f.w, end=claim_id(a1))]]})
    s = f.sicht()
    assert s.status(a1) is S.COVERED
    assert s.status(a2) is S.AFTER_END


# MV-7: Rücktritt durch den Inhaber, wie device-end.
def test_mv7_ruecktritt() -> None:
    f = _Fall()
    e = _eintrag(f.w)
    f.bestellen(e)
    f.ack(f.w.bob, e)
    a1 = f.akt(f.w.bob)
    f.ende(f.w.bob, e, _v_ende(claim_id(a1)))
    a2 = f.akt(f.w.bob)
    s = f.sicht()
    assert s.status(a1) is S.COVERED
    assert s.status(a2) is S.AFTER_END


# MV-8: ein Endpunkt, der lokal fehlt, lässt offen.
def test_mv8_endpunkt_unbekannt() -> None:
    f = _Fall()
    e = _eintrag(f.w)
    f.bestellen(e)
    f.ack(f.w.bob, e)
    a1 = f.akt(f.w.bob)
    f.ende(f.w.bob, e, _v_ende(b"\x11" * 32))
    assert f.sicht().status(a1) is S.UNDECIDED


# MV-9: ein defektes v beim Rücktritt endet bei der Gegenzeichnung (sichere Richtung).
def test_mv9_ruecktritt_defektes_v() -> None:
    f = _Fall()
    e = _eintrag(f.w)
    f.bestellen(e)
    f.ack(f.w.bob, e)
    a1 = f.akt(f.w.bob)
    f.ende(f.w.bob, e, b"\xff")
    assert f.sicht().status(a1) is S.AFTER_END


# MV-10: ein anderer Autor hat kein Mandat.
def test_mv10_fremder_autor() -> None:
    f = _Fall()
    e = _eintrag(f.w)
    f.bestellen(e)
    f.ack(f.w.bob, e)
    a = f.akt(f.w.carol)
    assert f.sicht().status(a) is S.NONE


# MV-11: zeichnet ein anderer gegen, wird niemand Inhaber.
def test_mv11_gegenzeichnung_durch_andere() -> None:
    f = _Fall()
    e = _eintrag(f.w)
    f.bestellen(e)
    f.ack(f.w.carol, e)
    a = f.akt(f.w.bob)
    assert f.sicht().status(a) is S.NONE


# MV-12: eine Gegenzeichnung in einem anderen Scope zählt nicht.
def test_mv12_gegenzeichnung_fremder_scope() -> None:
    f = _Fall()
    e = _eintrag(f.w)
    f.bestellen(e)
    f.ack(f.w.bob, e, scope=b"\x22" * 32)
    a = f.akt(f.w.bob)
    assert f.sicht().status(a) is S.NONE


# MV-13: ein formwidriger Eintrag ist kein Mandat und wird benannt.
def test_mv13_formwidriger_eintrag() -> None:
    f = _Fall()
    e = _eintrag(f.w, rahmen={0: ["b@1", "a@1"]})
    f.bestellen(e)
    f.ack(f.w.bob, e)
    a = f.akt(f.w.bob)
    s = f.sicht()
    assert s.status(a) is S.NONE
    assert s.malformed == ("mandat:weg",)


# MV-14: zwei Mandate, eins deckt.
def test_mv14_zwei_mandate_eins_deckt() -> None:
    f = _Fall()
    e1 = _eintrag(f.w)
    e2 = _eintrag(f.w, rahmen={0: ["abnahme@1"]}, label="Abnahme")
    f.bestellen(e1)
    f.bestellen(e2, feld="mandat:abnahme")
    f.ack(f.w.bob, e1)
    f.ack(f.w.bob, e2)
    assert f.sicht().status(f.akt(f.w.bob, "abnahme")) is S.COVERED


# MV-15: ein Abruf, der das Feld nur entfernt, nimmt jede Deckung (Fork E aus §11).
def test_mv15_abruf_ohne_ende_entfernt_das_mandat() -> None:
    f = _Fall()
    e = _eintrag(f.w)
    f.bestellen(e)
    f.ack(f.w.bob, e)
    a1 = f.akt(f.w.bob)
    f.beschliessen({"mandat:weg": [[e], []]})
    assert f.sicht().status(a1) is S.NONE


# MV-16: derselbe Inhaber in einem anderen Scope handelt nicht für diese Gruppe.
def test_mv16_akt_in_fremdem_scope() -> None:
    f = _Fall()
    e = _eintrag(f.w)
    f.bestellen(e)
    f.ack(f.w.bob, e)
    fremd = b"\x33" * 32
    a = f.w.bob.claim(p=nuc(fremd, "auftrag"), J=(1, f.w.bob.pub), t=f.w.t(), N=fremd)
    f.w.claims.append(a)
    assert f.sicht().status(a) is S.NONE
