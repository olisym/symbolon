"""Sachanträge im Knoten: Speicher, Sicht, Absichten, Stand (04 §2.4, 04 §2.5, 04 §4.4, 04 §4.5,
04 §4.6, D577).

Welt aus ``tests/node/test_geraete.py``: Epoche 2, vier Teilnehmer, drei Ja kommen durch.
"""

from __future__ import annotations

import hashlib

import pytest

from symbolon import cbor_canon
from symbolon.atom import signed_bytes
from symbolon.domains import DOM_NUC_PROPOSAL
from symbolon.governance.findings import GovernanceFinding
from symbolon.governance.objects import Motion
from symbolon.node.api import _Named, _intent_body, _tally_of
from symbolon.node.store import ObjectKind
from symbolon.node.view import FieldChange, proposals_view, scope_view
from tests.node.test_geraete import _JETZT, _welt
from tools.example_nucleus import _nuc

_T = iter(range(100, 10_000))


def _absicht(store, wer, rumpf: dict):
    return _intent_body(store, {"I": wer.pub.hex(), **rumpf}, _JETZT)


def _claim(store, wer, world, art: str, felder: dict) -> None:
    gov = world.ex.N_gov
    v = bytes.fromhex(felder["v"]) if "v" in felder else None
    digest = bytes.fromhex(felder["J"][1])
    claim = wer.claim(p=_nuc(gov, art), J=(3, digest), t=next(_T), N=gov, v=v)
    store.submit_claim(signed_bytes(claim))


def _antrag(store, world, wer, rumpf: dict) -> bytes:
    """Absicht ``propose``, eingereicht; gibt den Hash des Objekts zurück."""
    felder, _warnungen, _folge = _absicht(
        store, wer, {"art": "propose", "scope": world.ex.N_gov.hex(), **rumpf}
    )
    _claim(store, wer, world, "propose", felder)
    return bytes.fromhex(felder["J"][1])


def _ja(store, world, wer, digest: bytes):
    felder, warnungen, folge = _absicht(
        store, wer, {"art": "vote", "proposal": digest.hex(), "choice": "yes"}
    )
    _claim(store, wer, world, "vote", felder)
    return warnungen, folge


def _feststellen(store, world, digest: bytes):
    for wer in (world.anna, world.chris, world.dora):
        _ja(store, world, wer, digest)
    felder, _warnungen, folge = _absicht(
        store, world.anna, {"art": "ratify", "proposal": digest.hex()}
    )
    _claim(store, world.anna, world, "ratify", felder)
    return folge


def _sicht(store, world):
    return scope_view(store, world.ex.N_gov, _JETZT)


def _zeile(store, world, digest):
    (zeile,) = [z for z in proposals_view(store, world.ex.N_gov, _JETZT) if z.proposal == digest]
    return zeile


def _vermerke(store, world, digest):
    return [f.kind for f in _tally_of(_sicht(store, world), digest).findings]


def test_sachantrag_anlegen(tmp_path) -> None:
    """Das Objekt aus dem Stand, als Sachantrag gespeichert, als Zeile der Sicht (D577)."""
    world, _geraete, store = _welt(tmp_path)
    m = _antrag(store, world, world.bruno, {"motion": {"ort": "Halle"}})
    epoche = _sicht(store, world).state.epoch.epoch_id
    kind, data = store.object_at(m)
    assert kind == ObjectKind.MOTION.value
    assert data == cbor_canon.encode({0: world.ex.N_gov, 1: epoche, 2: {"ort": [[], ["Halle"]]}})
    assert Motion(cbor_canon.decode(data)).motion_hash == m
    zeile = _zeile(store, world, m)
    assert (zeile.kind, zeile.motions, zeile.n, zeile.needed) == ("motion", (), 4, 3)
    assert zeile.changes.fields == (FieldChange(field="ort", old=None, new="Halle"),)


def test_sachantrag_feststellen_setzt_den_stand(tmp_path) -> None:
    """Festgestellt ändert den Stand, nicht die Epoche und nicht ihre Verfassung (04 §4.6)."""
    world, _geraete, store = _welt(tmp_path)
    m = _antrag(store, world, world.bruno, {"motion": {"ort": "Halle"}})
    assert _feststellen(store, world, m) == {"epoch": 2}
    sicht = _sicht(store, world)
    assert sicht.state.epoch.index == 2 and "ort" not in sicht.state.constitution_obj
    assert sicht.stand.stand_obj["ort"] == "Halle"
    assert sicht.stand.ratified == sicht.stand.applied == (m,)


def test_satzungsantrag_baut_auf_dem_stand(tmp_path) -> None:
    """Feld 3 nennt die festgestellten Sachanträge, die Verfassung trägt ihre Werte, die Zeile
    zeigt nur die eigene Änderung (04 §2.4, 04 §3.4, D577)."""
    world, _geraete, store = _welt(tmp_path)
    ohne = _antrag(store, world, world.bruno, {"change": {"set": {"field": "farbe", "text": "grün"}}})
    assert set(cbor_canon.decode(store.object_at(ohne)[1])) == {0, 1, 2}
    m = _antrag(store, world, world.bruno, {"motion": {"ort": "Halle"}})
    _feststellen(store, world, m)
    g = _antrag(store, world, world.bruno, {"change": {"set": {"field": "farbe", "text": "rot"}}})
    obj = cbor_canon.decode(store.object_at(g)[1])
    assert obj[3] == [m]
    ziel = store.all_constitutions()[obj[2]]
    assert (ziel["ort"], ziel["farbe"]) == ("Halle", "rot")
    zeile = _zeile(store, world, g)
    assert (zeile.kind, zeile.motions) == ("proposal", (m,))
    assert zeile.changes.fields == (FieldChange(field="farbe", old=None, new="rot"),)


def test_satzungsantrag_mit_s_traegt(tmp_path) -> None:
    """Die Kette sieht die Sachanträge: Bedingung 7 trägt, die neue Epoche hat den Wert (04 §4.1,
    04 §4.5)."""
    world, _geraete, store = _welt(tmp_path)
    m = _antrag(store, world, world.bruno, {"motion": {"ort": "Halle"}})
    _feststellen(store, world, m)
    g = _antrag(store, world, world.bruno, {"change": {"set": {"field": "farbe", "text": "rot"}}})
    assert _feststellen(store, world, g) == {"epoch": 3}
    sicht = _sicht(store, world)
    assert sicht.state.epoch.index == 3
    assert (sicht.state.constitution_obj["ort"], sicht.state.constitution_obj["farbe"]) == (
        "Halle",
        "rot",
    )


def test_regel_2_warnt(tmp_path) -> None:
    """Zwei Ja auf dieselbe Vorbedingung: Warnung und Vermerk; verschiedene Felder: keine (04 §4.4)."""
    world, _geraete, store = _welt(tmp_path)
    halle = _antrag(store, world, world.bruno, {"motion": {"ort": "Halle"}})
    essen = _antrag(store, world, world.chris, {"motion": {"ort": "Essen"}})
    farbe = _antrag(store, world, world.chris, {"motion": {"farbe": "rot"}})
    assert _ja(store, world, world.dora, halle)[0] == []
    assert _ja(store, world, world.dora, farbe)[0] == []
    warnungen, folge = _ja(store, world, world.dora, essen)
    assert warnungen == ["CONFLICTING_APPROVAL"] and folge["conflict"] == [halle.hex()]
    assert GovernanceFinding.CONFLICTING_APPROVAL in _vermerke(store, world, essen)
    assert GovernanceFinding.CONFLICTING_APPROVAL not in _vermerke(store, world, farbe)


def test_regel_3_warnt(tmp_path) -> None:
    """Ein Ja auf einen Satzungsantrag neben einem Ja auf einen Sachantrag außerhalb von ``S``
    warnt; innerhalb von ``S`` nicht (04 §4.4)."""
    world, _geraete, store = _welt(tmp_path)
    m = _antrag(store, world, world.bruno, {"motion": {"ort": "Halle"}})
    g = _antrag(store, world, world.bruno, {"change": {"set": {"field": "farbe", "text": "rot"}}})
    _ja(store, world, world.dora, m)
    warnungen, folge = _ja(store, world, world.dora, g)
    assert warnungen == ["CONFLICTING_APPROVAL"] and folge["conflict"] == [m.hex()]


def test_regel_3_schweigt_bei_s(tmp_path) -> None:
    """Ein Ja auf einen Sachantrag in ``S`` ist mit dem Ja auf den Satzungsantrag vereinbar."""
    world, _geraete, store = _welt(tmp_path)
    m = _antrag(store, world, world.bruno, {"motion": {"ort": "Halle"}})
    _feststellen(store, world, m)
    g = _antrag(store, world, world.bruno, {"change": {"set": {"field": "farbe", "text": "rot"}}})
    assert _ja(store, world, world.dora, g)[0] == []


def test_alter_wert_aus_dem_stand(tmp_path) -> None:
    """``alt`` kommt aus dem Stand, nicht aus der Verfassung der Epoche (04 §2.5, 04 §4.6)."""
    world, _geraete, store = _welt(tmp_path)
    _feststellen(store, world, _antrag(store, world, world.bruno, {"motion": {"ort": "Halle"}}))
    with pytest.raises(_Named, match="UNCHANGED_FIELD"):
        _absicht(store, world.bruno, {"art": "propose", "scope": world.ex.N_gov.hex(),
                                      "motion": {"ort": "Halle"}})
    essen = _antrag(store, world, world.bruno, {"motion": {"ort": "Essen"}})
    assert cbor_canon.decode(store.object_at(essen)[1])[2] == {"ort": [["Halle"], ["Essen"]]}


@pytest.mark.parametrize(
    ("rumpf", "name"),
    [
        ({"motion": {"participants": "x"}}, "RESERVED_FIELD"),
        ({"motion": {"ort": None}}, "UNCHANGED_FIELD"),
        ({"motion": {"ort": 5}}, "INVALID_CHANGE"),
        ({"motion": {}}, "INVALID_CHANGE"),
        ({"motion": {"ort": "Halle"}, "change": {"set": {"field": "ort", "text": "x"}}},
         "INVALID_CHANGE"),
        ({}, "INVALID_CHANGE"),
    ],
)
def test_sachantrag_abgewiesen(tmp_path, rumpf, name) -> None:
    """Absichten, aus denen kein wohlgeformter Sachantrag wird (04 §2.5, D577)."""
    world, _geraete, store = _welt(tmp_path)
    with pytest.raises(_Named, match=name):
        _absicht(store, world.bruno, {"art": "propose", "scope": world.ex.N_gov.hex(), **rumpf})


def test_formwidriger_sachantrag_wird_gespeichert(tmp_path) -> None:
    """Kanonisch und formwidrig: gespeichert, ausgezählt als formwidrig, keine Absicht darauf;
    nicht kanonisch: abgewiesen (04 §2.5, 04 §3.5, D577)."""
    world, _geraete, store = _welt(tmp_path)
    gov = world.ex.N_gov
    epoche = _sicht(store, world).state.epoch.epoch_id
    regelfeld = {0: gov, 1: epoche, 2: {"participants": [[], ["x"]]}}
    for obj in ([1, 2], regelfeld, {0: gov, 1: epoche, 2: {"ort": [[], []]}}):
        digest = store.submit_object(ObjectKind.MOTION, cbor_canon.encode(obj))
        assert store.all_motions()[digest] == Motion(obj)
        with pytest.raises(_Named, match="MALFORMED_MOTION"):
            _absicht(store, world.dora, {"art": "vote", "proposal": digest.hex(), "choice": "yes"})
    r = Motion(regelfeld).motion_hash
    assert GovernanceFinding.MALFORMED_MOTION in _vermerke(store, world, r)
    with pytest.raises(ValueError, match="not canonical"):
        store.submit_object(ObjectKind.MOTION, bytes.fromhex("a2616201616102"))
    with pytest.raises(ValueError, match="not canonical"):
        store.submit_object(ObjectKind.MOTION, bytes.fromhex("1817"))


def test_formwidriges_feld_3_wird_gespeichert(tmp_path) -> None:
    """Feld 3 wie es kam; ausgezählt als formwidrig. Key 4 ist abgewiesen (04 §2.4, D577)."""
    world, _geraete, store = _welt(tmp_path)
    gov = world.ex.N_gov
    epoche = _sicht(store, world).state.epoch.epoch_id
    ziel = world.constitution_hash_3
    digest = store.submit_object(
        ObjectKind.PROPOSAL, cbor_canon.encode({0: gov, 1: epoche, 2: ziel, 3: []})
    )
    assert store.all_proposals()[digest].motions == []
    assert GovernanceFinding.MALFORMED_PROPOSAL in _vermerke(store, world, digest)
    with pytest.raises(ValueError, match="keys"):
        store.submit_object(
            ObjectKind.PROPOSAL, cbor_canon.encode({0: gov, 1: epoche, 2: ziel, 4: 1})
        )


def test_fremder_scope_bricht_die_sicht_nicht(tmp_path) -> None:
    """Ein Objekt mit fremdem ``scope`` und dem ``epoch_id`` der Epoche gehört nicht zu ihr
    (04 §4.5, D572, D577)."""
    world, _geraete, store = _welt(tmp_path)
    epoche = _sicht(store, world).state.epoch.epoch_id
    fremd = bytes(32)
    p = store.submit_object(
        ObjectKind.PROPOSAL,
        cbor_canon.encode({0: fremd, 1: epoche, 2: world.constitution_hash_3}),
    )
    m = store.submit_object(
        ObjectKind.MOTION, cbor_canon.encode({0: fremd, 1: epoche, 2: {"ort": [[], ["x"]]}})
    )
    decisions = dict(_sicht(store, world).verein.decisions)
    assert p not in decisions and m not in decisions


def test_feld_3_null_wird_unter_seinen_bytes_gespeichert(tmp_path) -> None:
    """``3: null`` ist ein formwidriges Feld 3, kein fehlendes; der Hash ist der seiner Bytes
    (04 §2.4, D578)."""
    world, _geraete, store = _welt(tmp_path)
    epoche = _sicht(store, world).state.epoch.epoch_id
    data = cbor_canon.encode(
        {0: world.ex.N_gov, 1: epoche, 2: world.constitution_hash_3, 3: None}
    )
    digest = store.submit_object(ObjectKind.PROPOSAL, data)
    assert digest == hashlib.sha256(DOM_NUC_PROPOSAL + data).digest()
    assert store.object_at(digest) == (ObjectKind.PROPOSAL.value, data)
    assert store.all_proposals()[digest].motions is None
    assert GovernanceFinding.MALFORMED_PROPOSAL in _vermerke(store, world, digest)
