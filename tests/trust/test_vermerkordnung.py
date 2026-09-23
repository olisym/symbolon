"""Ordnung der Trust-Vermerke gegen den Schlüssel aus 00 §10 (02 §10, D429)."""

from __future__ import annotations

from symbolon.trust.derive import derive
from symbolon.trust.findings import TrustFinding

from tests.helpers import Identity, scope_id, store_with
from .tp02 import NOW, PARAMS


def schluessel(vermerk):
    """00 §10: aufsteigend nach kind als ASCII-Zeichenfolge, dann subject byteweise."""
    return (vermerk.kind.value.encode("ascii"), vermerk.subject)


def test_derive_ordnet_vermerke_nach_00_10() -> None:
    """Zwei Vermerke einer Ableitung, verglichen mit dem ausgeschriebenen Schlüssel."""
    scope = scope_id("vermerkordnung-02")
    alice = Identity("ord-02-alice")
    bob = Identity("ord-02-bob")
    carol = Identity("ord-02-carol")
    dave = Identity("ord-02-dave")
    store = store_with(
        alice.vouch(bob, n=1, scope=scope, t=1),
        carol.vouch(dave, n=1, scope=scope, t=1),
    )
    result = derive(
        store,
        anchors=frozenset({alice.pub}),
        scope=scope,
        now=NOW,
        params=PARAMS,
    )
    paare = {(f.kind, f.subject) for f in result.findings}
    assert len(paare) >= 2
    assert TrustFinding.VOUCH_WITHOUT_TEXP in {f.kind for f in result.findings}
    assert result.findings == tuple(sorted(result.findings, key=schluessel))
