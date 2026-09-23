"""Ordnung der Governance-Vermerke gegen den Schlüssel aus 00 §10 (04 §3.5, D429)."""

from __future__ import annotations

from symbolon.governance import GovernanceFinding

from tests.helpers import Identity, store_with

from .fixtures import C1, PROPOSAL_1, _tally, fresh_p1, vote


def schluessel(vermerk):
    """00 §10: aufsteigend nach kind als ASCII-Zeichenfolge, dann subject byteweise."""
    return (vermerk.kind.value.encode("ascii"), vermerk.subject)


def test_auszaehlung_ordnet_vermerke_nach_00_10() -> None:
    """Zwei Vermerke einer Auszählung, verglichen mit dem ausgeschriebenen Schlüssel."""
    alice, _bob, _carol, _dave = fresh_p1()
    fremd = Identity("fremd-ordnung")
    assert fremd.pub not in C1["participants"]
    ablauf = vote(alice, PROPOSAL_1, choice=1, t=1, t_exp=10**9)
    fremdstimme = vote(fremd, PROPOSAL_1, choice=1, t=1)
    result = _tally(store_with(ablauf, fremdstimme))
    paare = {(f.kind, f.subject) for f in result.findings}
    assert len(paare) >= 2
    assert GovernanceFinding.VOTE_WITH_EXPIRY in {f.kind for f in result.findings}
    assert GovernanceFinding.NON_MEMBER_VOTE in {f.kind for f in result.findings}
    assert result.findings == tuple(sorted(result.findings, key=schluessel))
