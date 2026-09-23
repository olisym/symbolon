"""Vektorsatz ZF-02 (D438, 01 §6, 02 §3.1).

Profile F1 bis F3 auf einem Gerüst. Zustände nach 01 Anhang B.1.
"""

from __future__ import annotations

from symbolon.atom import Claim
from symbolon.trust import TrustParams
from symbolon.verifier import InMemoryStore, State

from tests.helpers import Identity, scope_id, store_with

# D438 Beschluss 1.
PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=4)
NOW = 1000
T_EXP = 5000
SCOPE = scope_id("ZF-02")
PROFILES = ("F1", "F2", "F3")

# D438 Beschluss 1, Zustände aus 01 Anhang B.1. b1 in F1 ist signiert und
# nicht gehalten, deshalb ohne Zeile. Jeder andere Claim ist active.
NAMED_STATES: dict[str, dict[str, State]] = {
    "F1": {
        "b0": State.ACTIVE,
        "b2": State.PENDING,
        "b3": State.ACTIVE,
    },
    "F2": {
        "f1": State.EQUIVOCATION_FLAGGED,
        "f2": State.EQUIVOCATION_FLAGGED,
        "b": State.ACTIVE,
    },
    "F3": {
        "b0": State.ACTIVE,
        "b1": State.TIME_REGRESSION_FLAGGED,
        "b2": State.ACTIVE,
    },
}
OTHER_STATE = State.ACTIVE

# D438, Golden Numbers. Fluss in allen drei Profilen gleich (02 §3.1, 02 §4).
FLOW_PER_TARGET = 3
SIMULTANEOUS = 3
DISJOINT = 1
BOB_BUDGET = {"F1": 4, "F2": 4, "F3": 3}


def mesh(
    g1: Identity, g2: Identity, g3: Identity, n: int, scope: bytes, t_exp: int
) -> list[Claim]:
    """Mesh unter g1 bis g3, n in beide Richtungen (D438 Beschluss 1)."""
    pairs = [(g1, g2), (g2, g1), (g1, g3), (g3, g1), (g2, g3), (g3, g2)]
    return [a.vouch(b, n=n, scope=scope, t=1, t_exp=t_exp) for a, b in pairs]


class Graph:
    def __init__(
        self,
        identities: dict[str, Identity],
        claims: list[Claim],
        scope: bytes,
        named: dict[str, Claim],
    ) -> None:
        self.identities = identities
        self.claims = claims
        self.scope = scope
        self.named = named

    def __getattr__(self, name: str) -> Identity:
        try:
            return self.identities[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def store(self, *extra: Claim) -> InMemoryStore:
        return store_with(*self.claims, *extra)


def _identities(suffix: str) -> dict[str, Identity]:
    names = ("ALICE", "BOB", "CAROL", "g1", "g2", "g3", "X", "Y", "Z")
    return {name: Identity(f"{name}-{suffix}") for name in names}


def _finish(ids: dict[str, Identity], claims: list[Claim], named: dict[str, Claim]) -> Graph:
    """CAROL und das Mesh hinter der schon gebauten Kette (D438 Beschluss 1)."""
    carol = ids["CAROL"]
    claims = list(claims)
    claims += [
        carol.vouch(ids["g1"], n=1, scope=SCOPE, t=1, t_exp=T_EXP),
        carol.vouch(ids["g2"], n=1, scope=SCOPE, t=1, t_exp=T_EXP),
        carol.vouch(ids["g3"], n=1, scope=SCOPE, t=1, t_exp=T_EXP),
    ]
    claims += mesh(ids["g1"], ids["g2"], ids["g3"], 2, SCOPE, T_EXP)
    return Graph(ids, claims, SCOPE, named)


def _open(suffix: str) -> tuple[dict[str, Identity], list[Claim]]:
    """ALICE → BOB, danach hängt das Profil BOBs Kette an (D438 Beschluss 1)."""
    ids = _identities(suffix)
    head = [ids["ALICE"].vouch(ids["BOB"], n=4, scope=SCOPE, t=1, t_exp=T_EXP)]
    return ids, head


def build_f1() -> Graph:
    """F1, Lücke: b1 signiert, nicht in der Claim-Liste (D438, 01 §6)."""
    ids, claims = _open("F1")
    bob = ids["BOB"]
    b0 = bob.vouch(ids["X"], n=1, scope=SCOPE, t=1, t_exp=T_EXP)
    b1 = bob.vouch(ids["Y"], n=1, scope=SCOPE, t=2, t_exp=T_EXP)
    b2 = bob.vouch(ids["Z"], n=1, scope=SCOPE, t=3, t_exp=T_EXP)
    b3 = bob.vouch(ids["CAROL"], n=2, scope=SCOPE, t=4, t_exp=T_EXP)
    claims += [b0, b2, b3]
    return _finish(ids, claims, {"b0": b0, "b1": b1, "b2": b2, "b3": b3})


def build_f2() -> Graph:
    """F2, Gabel: zwei Identity mit gleichem Label, b hängt an f1 (D438, 01 §6)."""
    ids, claims = _open("F2")
    bob = ids["BOB"]
    fork = Identity("BOB-F2")
    f1 = bob.vouch(ids["X"], n=1, scope=SCOPE, t=1, t_exp=T_EXP)
    f2 = fork.vouch(ids["Y"], n=1, scope=SCOPE, t=1, t_exp=T_EXP)
    b = bob.vouch(ids["CAROL"], n=2, scope=SCOPE, t=2, t_exp=T_EXP)
    claims += [f1, f2, b]
    return _finish(ids, claims, {"f1": f1, "f2": f2, "b": b})


def build_f3() -> Graph:
    """F3, Rückdatierung: b1.t liegt vor b0.t (D438, 01 §6)."""
    ids, claims = _open("F3")
    bob = ids["BOB"]
    b0 = bob.vouch(ids["X"], n=1, scope=SCOPE, t=10, t_exp=T_EXP)
    b1 = bob.vouch(ids["CAROL"], n=1, scope=SCOPE, t=5, t_exp=T_EXP)
    b2 = bob.vouch(ids["CAROL"], n=2, scope=SCOPE, t=20, t_exp=T_EXP)
    claims += [b0, b1, b2]
    return _finish(ids, claims, {"b0": b0, "b1": b1, "b2": b2})


def iter_profiles() -> list[tuple[str, Graph, int]]:
    """F1, F2, F3, je (Name, Graph, now) (D438 Beschluss 1)."""
    rows = [
        ("F1", build_f1(), NOW),
        ("F2", build_f2(), NOW),
        ("F3", build_f3(), NOW),
    ]
    if tuple(name for name, _, _ in rows) != PROFILES:
        raise RuntimeError("ZF-02 profile order drifted")
    return rows
