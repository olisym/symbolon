"""Die Seite nennt frühere Stimmen derselben Wurzel und ersetzt sie (04 §3.1, D547, D548)."""

from __future__ import annotations

from symbolon import cbor_canon
from symbolon.atom import claim_id, signed_bytes
from symbolon.node.api import _intent_body
from symbolon.node.view import geraetestimmen, proposals_view
from tests.node.test_geraete import _JETZT, _stimme, _welt
from tools.example_nucleus import _nuc


def _v(felder: dict) -> dict:
    return cbor_canon.decode(bytes.fromhex(felder["v"]))


def _rumpf(I: bytes, world, wahl: str) -> dict:
    return {
        "I": I.hex(),
        "art": "vote",
        "proposal": world.proposal_3.proposal_hash.hex(),
        "choice": wahl,
    }


def test_absicht_nennt_fruehere(tmp_path) -> None:
    """Ohne frühere Stimme kein Key 1; danach jede frühere Stimme der Wurzel, sortiert (D548)."""
    world, geraete, store = _welt(tmp_path)
    felder, warnungen, _folge = _intent_body(store, _rumpf(world.dora.pub, world, "yes"), _JETZT)
    assert _v(felder) == {0: 1} and warnungen == []
    eigen = _stimme(store, world.dora, world, 1)
    fremd = _stimme(store, world.anna, world, 1)
    zweit = _stimme(store, geraete["DORA"], world, 0, t=31)
    felder, warnungen, folge = _intent_body(store, _rumpf(world.dora.pub, world, "yes"), _JETZT)
    assert _v(felder) == {0: 1, 1: sorted([claim_id(eigen), claim_id(zweit)])}
    assert claim_id(fremd) not in _v(felder)[1]
    assert warnungen == ["CHANGE_VOTE"]
    assert (folge["counts"], folge["replaces"]) == (True, True)


def test_gleiche_wahl_nennt_auch(tmp_path) -> None:
    """Gleiche Wahl: SAME_VOTE, die Stimme nennt trotzdem, Ja bleibt (D543 Beschluss 4, D548)."""
    world, geraete, store = _welt(tmp_path)
    eigen = _stimme(store, world.dora, world, 1)
    felder, warnungen, folge = _intent_body(
        store, _rumpf(geraete["DORA"].pub, world, "yes"), _JETZT
    )
    assert _v(felder) == {0: 1, 1: [claim_id(eigen)]}
    assert warnungen == ["SAME_VOTE"]
    assert (folge["counts"], folge["replaces"], folge["yes"]) == (False, False, 1)


def test_aufloesung_auf_dem_zweitgeraet(tmp_path) -> None:
    """Bruno löst seinen Widerspruch auf: nur die neue Stimme zählt, er zählt Ja (D548, D551)."""
    world, geraete, store = _welt(tmp_path)
    ja = _stimme(store, world.bruno, world, 1)
    nein = _stimme(store, geraete["BRUNO"], world, 0)
    gov = world.ex.N_gov
    assert [g.root for g in geraetestimmen(store, gov, _JETZT)] == [world.bruno.pub]
    felder, warnungen, _folge = _intent_body(
        store, _rumpf(geraete["BRUNO"].pub, world, "yes"), _JETZT
    )
    assert _v(felder)[1] == sorted([claim_id(ja), claim_id(nein)])
    assert warnungen == ["CHANGE_VOTE"]
    neu = geraete["BRUNO"].claim(
        p=_nuc(gov, "vote"),
        J=(3, world.proposal_3.proposal_hash),
        t=40,
        N=gov,
        v=bytes.fromhex(felder["v"]),
    )
    store.submit_claim(signed_bytes(neu))
    (gruppe,) = geraetestimmen(store, gov, _JETZT)
    assert gruppe.stimmen == ((claim_id(neu), geraete["BRUNO"].pub, 1),)
    (zeile,) = [z for z in proposals_view(store, gov, _JETZT) if z.proposal == world.proposal_3.proposal_hash]
    assert zeile.yes == (world.bruno.pub,) and zeile.ambiguous == ()
