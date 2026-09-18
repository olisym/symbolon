"""Testprofil TP-UHR (02-golden-anchors.md Anker 5d): gamma=1/2, C0=16, D=4."""

from __future__ import annotations

from symbolon.atom import Claim
from symbolon.trust import TrustParams
from symbolon.verifier import InMemoryStore

from tests.helpers import Identity, scope_id, store_with

# Parameter wie TP-02 (Anker 5d).
PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=4)
SCOPE = scope_id("TP-UHR")
FOREIGN_SCOPE = scope_id("TP-UHR-fremd")

# Bestand: alle t = 100 (Anker 5d).
T = 100
# t_exp aus der Bestandstabelle in Anker 5d.
T_EXP_LANG = 10000
T_EXP_KURZ = 600
T_EXP_FREMD = 650

# n aus der Bestandstabelle in Anker 5d.
N_ALICE_BOB = 2
N_ALICE_CAROL = 2
N_BOB_DAVE = 3
N_BOB_ERIN = 3
N_CAROL_DAVE = 4
N_ALICE_ERIN_FREMD = 1


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


def build() -> Graph:
    """Frische Identitäten je Aufruf; Bestand und Fremdscope-Vouch nach Anker 5d."""
    ALICE = Identity("ALICE-UHR")
    BOB = Identity("BOB-UHR")
    CAROL = Identity("CAROL-UHR")
    DAVE = Identity("DAVE-UHR")
    ERIN = Identity("ERIN-UHR")

    claims = [
        ALICE.vouch(BOB, n=N_ALICE_BOB, scope=SCOPE, t=T, t_exp=T_EXP_LANG),
        ALICE.vouch(CAROL, n=N_ALICE_CAROL, scope=SCOPE, t=T, t_exp=T_EXP_LANG),
        BOB.vouch(DAVE, n=N_BOB_DAVE, scope=SCOPE, t=T, t_exp=T_EXP_LANG),
        BOB.vouch(ERIN, n=N_BOB_ERIN, scope=SCOPE, t=T, t_exp=T_EXP_KURZ),
        CAROL.vouch(DAVE, n=N_CAROL_DAVE, scope=SCOPE, t=T, t_exp=T_EXP_KURZ),
        ALICE.vouch(
            ERIN, n=N_ALICE_ERIN_FREMD, scope=FOREIGN_SCOPE, t=T, t_exp=T_EXP_FREMD
        ),
    ]
    identities = {
        "ALICE": ALICE,
        "BOB": BOB,
        "CAROL": CAROL,
        "DAVE": DAVE,
        "ERIN": ERIN,
    }
    return Graph(identities, claims, SCOPE)
