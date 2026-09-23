"""SUBGRANULAR_VOUCH nur am erreichten Autor (D439, 02 §10, 02 §11.4)."""

from __future__ import annotations

from symbolon.atom import claim_id
from symbolon.trust import Finding, TrustFinding, TrustParams, trust

from tests.helpers import Identity, scope_id, store_with


def test_subgranular_nur_am_erreichten_autor() -> None:
    """Schritt 6 von 02 §11.4: der Vermerk entsteht nur an einer Kante, deren Autor
    die Breitensuche erreicht hat (D439, 02 §10)."""
    params = TrustParams(C0=2, gamma_num=1, gamma_den=2, D=4)
    scope = scope_id("d439-subgranular")
    now = 1000
    t_exp = 5000
    alice = Identity("ALICE")
    bob = Identity("BOB")
    eve = Identity("EVE")
    frank = Identity("FRANK")
    alice_bob = alice.vouch(bob, n=1, scope=scope, t=1, t_exp=t_exp)
    eve_frank = eve.vouch(frank, n=4, scope=scope, t=1, t_exp=t_exp)
    result = trust(
        store_with(alice_bob, eve_frank),
        anchors=frozenset({alice.pub}),
        targets=frozenset({bob.pub, frank.pub}),
        scope=scope,
        now=now,
        params=params,
        include_flagged=True,
    )
    assert result.findings == (
        Finding(kind=TrustFinding.SUBGRANULAR_VOUCH, subject=claim_id(alice_bob)),
    )
