"""Die Titel der Anträge des Bestands, auch nach dem Beschluss (D559 Beschluss 5, D507 Befund 2)."""

from __future__ import annotations

import json

from symbolon.node.api import json_value
from symbolon.node.view import antragstitel, proposals_view
from tests.node.test_api import _call, _start, _stop
from tests.node.test_geraete import _JETZT, _welt


def test_titel_auch_nach_dem_beschluss(tmp_path) -> None:
    """Der offene Antrag mit denselben Änderungen wie in der Sicht, der festgestellte mit seinen,
    der Antrag einer noch unbekannten Epoche nicht (D559 Beschluss 5)."""
    world, _geraete, store = _welt(tmp_path)
    gov = world.ex.N_gov
    titel = {eintrag.proposal: eintrag.changes for eintrag in antragstitel(store, gov, _JETZT)}
    sicht = {antrag.proposal: antrag.changes for antrag in proposals_view(store, gov, _JETZT)}
    assert list(sicht) == [world.proposal_3.proposal_hash]
    assert titel[world.proposal_3.proposal_hash] == sicht[world.proposal_3.proposal_hash]
    assert world.ex.proposal.proposal_hash in titel
    assert world.ex.proposal.proposal_hash not in sicht
    assert world.proposal_4.proposal_hash not in titel
    assert list(titel) == sorted(titel)


def test_antragstitel_ueber_die_schnittstelle(tmp_path) -> None:
    """GET /antragstitel/<scope> gibt dieselbe Liste; ein unbekannter Scope ist 404 (D559)."""
    world, _geraete, store = _welt(tmp_path)
    gov = world.ex.N_gov
    erwartet = json_value(antragstitel(store, gov, _JETZT))
    server = _start(tmp_path / "w.sqlite", lambda: _JETZT)
    try:
        status, body = _call(server, "GET", f"/antragstitel/{gov.hex()}")
        assert status == 200, body
        assert json.loads(body) == erwartet
        status, _body = _call(server, "GET", f"/antragstitel/{'00' * 32}")
        assert status == 404
    finally:
        _stop(server)
