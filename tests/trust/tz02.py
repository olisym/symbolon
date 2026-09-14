"""Testprofil TZ-02 (02-golden-anchors.md §5): Anker 5, 5b, 5c."""

from __future__ import annotations

from symbolon.atom import Claim
from symbolon.trust import TrustParams
from symbolon.verifier import InMemoryStore

from tests.helpers import Identity, scope_id, store_with

PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=4)
T_EXP = 5000
T_EXP_G1 = 2000
T_EXP_HELD = 10**9
REVOKE_AT = 900
NOW_S1 = 1000
NOW_S2 = 2001
NOW_FAR = 10**6
SCOPE = scope_id("TZ-02")

# Anker 5b, Tabellenreihenfolge in 02-golden-anchors.md §5:
# Erneuerung, Herabstufung, Heraufstufung, beide aktiv.
# (n(V1), Zustand V1, n(V2))
ANKER_5B_CASES: dict[str, tuple[int, str, int]] = {
    "renewal": (2, "superseded", 2),
    "downgrade": (2, "superseded", 1),
    "upgrade": (1, "superseded", 3),
    "both_active": (2, "active", 2),
}

PROFILES = ("Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "Z7", "Z8", "Z9")


def mesh(
    g1: Identity, g2: Identity, g3: Identity, n: int, scope: bytes, t_exp: int
) -> list[Claim]:
    pairs = [(g1, g2), (g2, g1), (g1, g3), (g3, g1), (g2, g3), (g3, g2)]
    return [a.vouch(b, n=n, scope=scope, t=1, t_exp=t_exp) for a, b in pairs]


def rump(
    alice: Identity, bob: Identity, carol: Identity, scope: bytes, t_exp: int
) -> list[Claim]:
    return [
        alice.vouch(bob, n=4, scope=scope, t=1, t_exp=t_exp),
        bob.vouch(carol, n=4, scope=scope, t=1, t_exp=t_exp),
    ]


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


def _identities(suffix: str) -> dict[str, Identity]:
    return {
        "ALICE": Identity(f"ALICE-{suffix}"),
        "BOB": Identity(f"BOB-{suffix}"),
        "CAROL": Identity(f"CAROL-{suffix}"),
        "g1": Identity(f"g1-{suffix}"),
        "g2": Identity(f"g2-{suffix}"),
        "g3": Identity(f"g3-{suffix}"),
    }


def build_anker5(
    *,
    suffix: str,
    scope: bytes | None = None,
    via_supersede: bool = False,
    neighbor_t_exp: int = T_EXP,
    g1_t_exp: int | None = T_EXP_G1,
    with_revoke: bool = True,
) -> Graph:
    """Variante C: CAROL→g1 abweichendes t_exp, optional Widerruf/Supersede bei 900.

    Rumpf und CAROLs übrige Vouches tragen neighbor_t_exp. Das Mesh bleibt auf
    T_EXP (Anker 5c ändert nur Rumpf und CAROL, 02-golden-anchors.md §5).
    """
    scope = scope if scope is not None else SCOPE
    ids = _identities(suffix)
    ALICE, BOB, CAROL = ids["ALICE"], ids["BOB"], ids["CAROL"]
    g1, g2, g3 = ids["g1"], ids["g2"], ids["g3"]
    rump_t_exp = neighbor_t_exp
    claims = rump(ALICE, BOB, CAROL, scope, rump_t_exp)
    g1v = CAROL.vouch(g1, n=1, scope=scope, t=1, t_exp=g1_t_exp)
    g2v = CAROL.vouch(g2, n=1, scope=scope, t=1, t_exp=neighbor_t_exp)
    g3v = CAROL.vouch(g3, n=1, scope=scope, t=1, t_exp=neighbor_t_exp)
    claims += [g1v, g2v, g3v]
    if with_revoke:
        if via_supersede:
            claims.append(CAROL.supersede(g1v, t=REVOKE_AT))
        else:
            claims.append(CAROL.revoke(g1v, t=REVOKE_AT))
    claims += mesh(g1, g2, g3, 2, scope, T_EXP)
    return Graph(ids, claims, scope)


def build_anker5b(
    case: str,
    *,
    suffix: str | None = None,
    scope: bytes | None = None,
) -> Graph:
    """Variante B, S isoliert: zwei Claims derselben Gruppe auf g1 (Anker 5b)."""
    if case not in ANKER_5B_CASES:
        raise ValueError(f"unknown 5b case {case!r}")
    n_v1, v1_state, n_v2 = ANKER_5B_CASES[case]
    suffix = suffix if suffix is not None else case
    scope = scope if scope is not None else SCOPE
    ids = _identities(suffix)
    ALICE, BOB, CAROL = ids["ALICE"], ids["BOB"], ids["CAROL"]
    g1, g2, g3 = ids["g1"], ids["g2"], ids["g3"]
    claims = rump(ALICE, BOB, CAROL, scope, T_EXP)
    claims += [
        CAROL.vouch(g2, n=1, scope=scope, t=1, t_exp=T_EXP),
        CAROL.vouch(g3, n=1, scope=scope, t=1, t_exp=T_EXP),
    ]
    v1 = CAROL.vouch(g1, n=n_v1, scope=scope, t=1, t_exp=T_EXP)
    v2 = CAROL.vouch(g1, n=n_v2, scope=scope, t=2, t_exp=T_EXP)
    claims += [v1, v2]
    if v1_state == "superseded":
        claims.append(CAROL.supersede(v1, t=3))
    return Graph(ids, claims, scope)


def build_anker5c(
    *,
    suffix: str,
    with_revoke: bool,
    g1_t_exp: int | None,
    scope: bytes | None = None,
) -> Graph:
    """Anker 5c: Rumpf und übrige CAROL-Vouches T_EXP_HELD; Mesh bleibt T_EXP."""
    return build_anker5(
        suffix=suffix,
        scope=scope,
        neighbor_t_exp=T_EXP_HELD,
        g1_t_exp=g1_t_exp,
        with_revoke=with_revoke,
    )


def iter_profiles() -> list[tuple[str, Graph, int]]:
    """Z1–Z9 in Auftragsreihenfolge, je (Name, Graph, now)."""
    z12 = build_anker5(suffix="Z1")
    z7 = build_anker5c(suffix="Z7", with_revoke=True, g1_t_exp=None)
    z8 = build_anker5c(suffix="Z8", with_revoke=False, g1_t_exp=None)
    z9 = build_anker5c(suffix="Z9", with_revoke=True, g1_t_exp=T_EXP_G1)
    rows = [
        ("Z1", z12, NOW_S1),
        ("Z2", z12, NOW_S2),
        ("Z3", build_anker5b("renewal", suffix="Z3"), NOW_S1),
        ("Z4", build_anker5b("downgrade", suffix="Z4"), NOW_S1),
        ("Z5", build_anker5b("upgrade", suffix="Z5"), NOW_S1),
        ("Z6", build_anker5b("both_active", suffix="Z6"), NOW_S1),
        ("Z7", z7, NOW_FAR),
        ("Z8", z8, NOW_FAR),
        ("Z9", z9, NOW_FAR),
    ]
    if tuple(name for name, _, _ in rows) != PROFILES:
        raise RuntimeError("TZ-02 profile order drifted")
    return rows
