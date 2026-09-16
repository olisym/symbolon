"""Falltest FALL-02 (02 §3, 02 §4, 02-golden-anchors.md §0 K9): ein Graph, drei C0."""

from __future__ import annotations

from symbolon.atom import Claim
from symbolon.trust import TrustParams
from symbolon.verifier import InMemoryStore

from tests.helpers import Identity, scope_id, store_with

NOW = 1000
T_EXP = 5000
SCOPE = scope_id("FALL-02")
PROFILES = ("R1", "R2", "R3")

PARAMS: dict[str, TrustParams] = {
    "R1": TrustParams(C0=1152921504606846976, gamma_num=1, gamma_den=2, D=4),
    "R2": TrustParams(C0=3458764513820540928, gamma_num=1, gamma_den=2, D=4),
    "R3": TrustParams(C0=4611686018427387904, gamma_num=1, gamma_den=2, D=4),
}


class Graph:
    def __init__(self, identities: dict[str, Identity], claims: list[Claim], scope: bytes) -> None:
        self.identities = identities
        self.claims = claims
        self.scope = scope

    def __getattr__(self, name: str) -> Identity:
        try:
            return self.identities[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def store(self, *extra: Claim) -> InMemoryStore:
        return store_with(*self.claims, *extra)


def build(profil: str, *, label_suffix: str = "", scope: bytes = SCOPE, t_exp: int = T_EXP) -> Graph:
    """Frische Identitäten je Aufruf; label_suffix hält Schlüssel über Profile hinweg getrennt."""
    if profil not in PARAMS:
        raise ValueError(f"unknown profil {profil!r}")
    suf = label_suffix or profil
    ALICE = Identity(f"ALICE-{suf}")
    BOB = Identity(f"BOB-{suf}")
    CAROL = Identity(f"CAROL-{suf}")
    g1 = Identity(f"g1-{suf}")
    g2 = Identity(f"g2-{suf}")
    g3 = Identity(f"g3-{suf}")

    claims = [
        ALICE.vouch(BOB, n=4, scope=scope, t=1, t_exp=t_exp),
        BOB.vouch(CAROL, n=4, scope=scope, t=1, t_exp=t_exp),
        CAROL.vouch(g1, n=2, scope=scope, t=1, t_exp=t_exp),
        CAROL.vouch(g2, n=1, scope=scope, t=1, t_exp=t_exp),
        CAROL.vouch(g3, n=1, scope=scope, t=1, t_exp=t_exp),
    ]
    identities = {
        "ALICE": ALICE,
        "BOB": BOB,
        "CAROL": CAROL,
        "g1": g1,
        "g2": g2,
        "g3": g3,
    }
    return Graph(identities, claims, scope)
