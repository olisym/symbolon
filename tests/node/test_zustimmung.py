"""Stimmen, die still nicht zählen: ein zweites Ja, ein gesperrtes Gerät (04 §4.4, 04 §3.1, D556)."""

from __future__ import annotations

from symbolon.atom import signed_bytes
from symbolon.governance.findings import GovernanceFinding
from symbolon.governance.tally import TallyState
from symbolon.node.api import _change, _intent_body, _tally_of
from symbolon.node.view import proposals_view, scope_view
from tests.node.test_geraete import _JETZT, _stimme, _welt
from tools.example_nucleus import _nuc


def _rumpf(I: bytes, digest: bytes, wahl: str) -> dict:
    return {"I": I.hex(), "art": "vote", "proposal": digest.hex(), "choice": wahl}


def _einreichen(store, wer, world, digest: bytes, wahl: str, t: int):
    felder, warnungen, folge = _intent_body(store, _rumpf(wer.pub, digest, wahl), _JETZT)
    gov = world.ex.N_gov
    claim = wer.claim(p=_nuc(gov, "vote"), J=(3, digest), t=t, N=gov, v=bytes.fromhex(felder["v"]))
    store.submit_claim(signed_bytes(claim))
    return warnungen, folge


def _zweiter_antrag(tmp_path):
    """Die Welt mit einem zweiten Antrag derselben Epoche; ANNA, CHRIS, DORA stimmen P3 zu."""
    world, geraete, store = _welt(tmp_path)
    gov = world.ex.N_gov
    q = _change(store, gov, {"set": {"field": "ort", "text": "Halle"}}, _JETZT)
    store.submit_claim(signed_bytes(world.chris.claim(p=_nuc(gov, "propose"), J=(3, q), t=21, N=gov)))
    for wer in (world.anna, world.chris, world.dora):
        _stimme(store, wer, world, 1)
    return world, geraete, store, q


def _zeile(store, world, digest):
    (zeile,) = [z for z in proposals_view(store, world.ex.N_gov, _JETZT) if z.proposal == digest]
    return zeile


def _vermerke(store, world, digest):
    tally = _tally_of(scope_view(store, world.ex.N_gov, _JETZT), digest)
    return [f.kind for f in tally.findings]


def test_zweites_ja_warnt_und_kippt(tmp_path) -> None:
    """Die Vorschau nennt den anderen Antrag und dass er fiele; danach zählt keines (D556 B. 2, 4)."""
    world, _geraete, store, q = _zweiter_antrag(tmp_path)
    p3 = world.proposal_3.proposal_hash
    assert _zeile(store, world, p3).state is TallyState.PASSED
    warnungen, folge = _einreichen(store, world.dora, world, q, "yes", 31)
    assert warnungen == ["CONFLICTING_APPROVAL"]
    assert (folge["counts"], folge["yes"], folge["no"]) == (False, 0, 0)
    assert (folge["conflict"], folge["falls"], folge["ended"]) == ([p3.hex()], [p3.hex()], False)
    for digest in (p3, q):
        assert GovernanceFinding.CONFLICTING_APPROVAL in _vermerke(store, world, digest)
        assert _zeile(store, world, digest).conflicting == (world.dora.pub,)
        assert world.dora.pub not in _zeile(store, world, digest).yes
    assert _zeile(store, world, p3).state is TallyState.PENDING


def test_zweites_ja_ohne_folge_fuer_den_anderen(tmp_path) -> None:
    """Hält der andere Antrag ohne das Ja, bleibt ``falls`` leer (D556 Beschluss 2)."""
    world, _geraete, store, q = _zweiter_antrag(tmp_path)
    _stimme(store, world.bruno, world, 1)
    _felder, warnungen, folge = _intent_body(store, _rumpf(world.dora.pub, q, "yes"), _JETZT)
    assert warnungen == ["CONFLICTING_APPROVAL"]
    assert folge["conflict"] == [world.proposal_3.proposal_hash.hex()] and folge["falls"] == []


def test_ersetztes_ja_zaehlt_fuer_die_regel(tmp_path) -> None:
    """Ein durch Nein ersetztes Ja warnt weiter und wirkt weiter (04 §4.4, D547 B. 4, D556 B. 2)."""
    world, _geraete, store, q = _zweiter_antrag(tmp_path)
    p3 = world.proposal_3.proposal_hash
    _einreichen(store, world.dora, world, p3, "no", 40)
    warnungen, folge = _einreichen(store, world.dora, world, q, "yes", 41)
    assert warnungen == ["CONFLICTING_APPROVAL"]
    assert folge["conflict"] == [p3.hex()] and folge["falls"] == []
    assert GovernanceFinding.CONFLICTING_APPROVAL in _vermerke(store, world, q)
    assert _zeile(store, world, q).conflicting == (world.dora.pub,)


def test_nein_warnt_nicht(tmp_path) -> None:
    """Nein-Stimmen sind unbeschränkt (04 §4.4)."""
    world, _geraete, store, q = _zweiter_antrag(tmp_path)
    _felder, warnungen, folge = _intent_body(store, _rumpf(world.dora.pub, q, "no"), _JETZT)
    assert warnungen == [] and folge["conflict"] == [] and folge["counts"] is True


def test_zweites_ja_ueber_ein_geraet(tmp_path) -> None:
    """Die Regel gilt je Wurzel; das Zweitgerät sieht das Ja des Erstgeräts (02 §2.1, D556 B. 2)."""
    world, geraete, store, q = _zweiter_antrag(tmp_path)
    _felder, warnungen, folge = _intent_body(store, _rumpf(geraete["DORA"].pub, q, "yes"), _JETZT)
    assert warnungen == ["CONFLICTING_APPROVAL"]
    assert folge["falls"] == [world.proposal_3.proposal_hash.hex()]


def test_gesperrtes_geraet(tmp_path) -> None:
    """Die Vorschau sagt, dass die Stimme nicht zählt; danach nennt die Sicht den Schlüssel
    (04 §3.1, D532, D556 Beschluss 3 und 5)."""
    world, geraete, store = _welt(tmp_path)
    gov = world.ex.N_gov
    p3 = world.proposal_3.proposal_hash
    ende = world.bruno.claim(p=_nuc(gov, "device-end"), J=(1, geraete["BRUNO"].pub), t=60, N=gov)
    store.submit_claim(signed_bytes(ende))
    _felder, warnungen, _folge = _intent_body(store, _rumpf(world.bruno.pub, p3, "yes"), _JETZT)
    assert warnungen == []
    warnungen, folge = _einreichen(store, geraete["BRUNO"], world, p3, "yes", 61)
    assert warnungen == ["DEVICE_ENDED"]
    assert (folge["counts"], folge["yes"], folge["ended"]) == (False, 0, True)
    assert _zeile(store, world, p3).disputed == (geraete["BRUNO"].pub,)
    assert _zeile(store, world, p3).yes == ()
    assert GovernanceFinding.DISPUTED_VOTE in _vermerke(store, world, p3)


def test_gesperrtes_ja_zaehlt_nicht_fuer_die_regel(tmp_path) -> None:
    """Ein Ja eines gesperrten Geräts löst keine Warnung vor einem zweiten Ja aus (04 §4.4, D556)."""
    world, geraete, store, q = _zweiter_antrag(tmp_path)
    gov = world.ex.N_gov
    ende = world.bruno.claim(p=_nuc(gov, "device-end"), J=(1, geraete["BRUNO"].pub), t=60, N=gov)
    store.submit_claim(signed_bytes(ende))
    _einreichen(store, geraete["BRUNO"], world, world.proposal_3.proposal_hash, "yes", 61)
    _felder, warnungen, folge = _intent_body(store, _rumpf(world.bruno.pub, q, "yes"), _JETZT)
    assert warnungen == [] and folge["conflict"] == [] and folge["counts"] is True
