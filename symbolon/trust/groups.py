"""Gruppenbildung (I, J, N) -> n_budget, n_kante (02a §2.4, D40/K7)."""

from __future__ import annotations

from dataclasses import dataclass

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id
from symbolon.predicates import parse_predicate
from symbolon.verifier import Classification, State

from .findings import Finding, TrustFinding

BUDGET_STATES = frozenset(
    {
        State.ACTIVE,
        State.REVOKED,
        State.SUPERSEDED,
        State.PENDING,
        State.EQUIVOCATION_FLAGGED,
        State.TIME_REGRESSION_FLAGGED,
    }
)


@dataclass(frozen=True, slots=True)
class Group:
    """Ein Kantenkandidat (I, J) im Scope: aggregiertes Budget und Kantengewicht.

    D40 spricht von Gruppen (I, J, N); der Schluessel hier ist nur (author, subject) ohne
    N, weil build_groups() den Scope bereits vorher filtert (_is_scope_vouch) -- pro Aufruf
    von build_groups() gibt es nur einen Scope, N ist also nicht Teil des Schluessels noetig.
    """

    author: bytes
    subject: bytes
    n_budget: int
    n_kante: int
    kante_claim_id: bytes | None  # None gdw. n_kante == 0 (keine Kante)


def _decode_weight(v: bytes | None, D: int) -> tuple[int | None, TrustFinding | None]:
    """n aus v dekodieren (02a §2.3). None-Rückgabe zusammen mit Finding heißt: kein Beitrag."""
    if v is None:
        return D, None
    try:
        obj = cbor_canon.decode(v)
        canonical = cbor_canon.is_canonical(v)
    except Exception:
        return None, TrustFinding.UNPARSABLE_VOUCH_PAYLOAD
    if not canonical:
        return None, TrustFinding.NON_CANONICAL_V
    if not isinstance(obj, dict) or 0 not in obj:
        return None, TrustFinding.UNPARSABLE_VOUCH_PAYLOAD
    n = obj[0]
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        return None, TrustFinding.UNPARSABLE_VOUCH_PAYLOAD
    if n < 1 or n > D:
        return None, TrustFinding.INVALID_VOUCH_WEIGHT
    return n, None


def _is_scope_vouch(claim: Claim, scope: bytes) -> bool:
    if claim.N != scope:
        return False
    parsed = parse_predicate(claim.p)
    return parsed.namespace == "nuc" and parsed.name == "vouch" and parsed.version == "1"


def _in_budget_set(claim: Claim, classification: Classification, now: int) -> bool:
    """state in {ACTIVE,REVOKED,SUPERSEDED,PENDING,EQUIVOCATION_FLAGGED} UND nicht abgelaufen
    (02a §2.6, D135). Equivocation ist kein Lebenszyklus-Akt; der Ueber-Commitment-Beweis
    beruht auf Signaturen, nicht auf Aktivitaet.

    classify() aus Layer 01 prueft REVOKED/SUPERSEDED/PENDING *vor* der Ablauf-Prüfung
    (Prioritaet in der Zustandsmaschine) -- ein einmal widerrufener oder supersedierter
    Claim bleibt daher fuer immer in diesem State und wird nie zu State.EXPIRED, selbst
    wenn t_exp laengst verstrichen ist. Das Budget-Set aus 02a §2.6 verlangt aber genau
    diesen Austritt ueber t_exp (Golden Anchors T-02.2, Schritt S2). Also wird die
    Ablauf-Bedingung hier unabhaengig von Layer 1s State erneut geprueft.
    """
    if classification.state not in BUDGET_STATES:
        return False
    if claim.t_exp is None:
        return True
    return now <= claim.t_exp


def build_groups(
    claims: list[Claim],
    classifications: dict[bytes, Classification],
    scope: bytes,
    D: int,
    now: int,
) -> tuple[dict[tuple[bytes, bytes], Group], tuple[Finding, ...]]:
    """Vouch-Claims des Scopes sammeln, v dekodieren, zu Gruppen aggregieren (02a §2.10 Schritte 2-3)."""
    findings: list[Finding] = []
    members: dict[tuple[bytes, bytes], list[tuple[bytes, int, State]]] = {}

    for c in claims:
        if not _is_scope_vouch(c, scope):
            continue
        cid = claim_id(c)
        classification = classifications[cid]
        if not _in_budget_set(c, classification, now):
            continue
        n, finding_kind = _decode_weight(c.v, D)
        if finding_kind is not None:
            findings.append(Finding(kind=finding_kind, subject=cid))
            continue
        if c.t_exp is None:
            findings.append(
                Finding(kind=TrustFinding.VOUCH_WITHOUT_TEXP, subject=cid)
            )
        key = (c.I, c.J[1])
        members.setdefault(key, []).append((cid, n, classification.state))

    groups: dict[tuple[bytes, bytes], Group] = {}
    for (author, subject), entries in members.items():
        n_budget = max(n for _, n, _ in entries)
        active_entries = [(cid, n) for cid, n, state in entries if state == State.ACTIVE]
        if active_entries:
            n_kante = max(n for _, n in active_entries)
            tied = sorted(cid for cid, n in active_entries if n == n_kante)
            kante_claim_id: bytes | None = tied[0]
        else:
            n_kante = 0
            kante_claim_id = None
        groups[(author, subject)] = Group(
            author=author,
            subject=subject,
            n_budget=n_budget,
            n_kante=n_kante,
            kante_claim_id=kante_claim_id,
        )

    return groups, tuple(sorted(findings))
