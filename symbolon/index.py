"""classify_all: schneller Zwilling von verifier.classify (02a §3, classify_all; D86/D87).

structural_check läuft genau einmal pro core/revoke@1- bzw. core/supersede@1-Claim
(Index-Aufbau), statt einmal pro Kandidat-Suche innerhalb jedes classify()-Aufrufs.
classify() aus Layer 01 bleibt die normative Wahrheit; dieses Modul dupliziert ihre
Logik absichtlich 1:1, mit den beiden linearen Kandidatensuchen durch Index-Lookups
ersetzt. Der Kopplungstest (T-02.4 / PR-INV-11) stellt sicher, dass beide nie
auseinanderlaufen.
"""

from __future__ import annotations

from symbolon.atom import Claim, claim_id, signed_bytes
from symbolon.errors import ForeignLifecycle, VerifierError
from symbolon.policy import NucleusPolicy, is_irrevocable
from symbolon.predicates import is_core_predicate, parse_predicate
from symbolon.verifier import (
    Classification,
    ClaimStore,
    State,
    _is_in_equivocation_pair,
    _is_temporally_valid,
    _predecessor_known_and_valid,
    structural_check,
)

_J_TAG_CLAIM_REF = 2


def _build_lifecycle_index(
    claims: list[Claim],
) -> tuple[dict[bytes, list[Claim]], dict[bytes, list[Claim]]]:
    """revokes_by_target, supersedes_by_target: nur strukturell gültige Kandidaten."""
    revokes_by_target: dict[bytes, list[Claim]] = {}
    supersedes_by_target: dict[bytes, list[Claim]] = {}

    for c in claims:
        if not is_core_predicate(c):
            continue
        parsed = parse_predicate(c.p)
        if parsed.name not in ("revoke", "supersede"):
            continue
        if c.J[0] != _J_TAG_CLAIM_REF:
            continue
        try:
            structural_check(signed_bytes(c))
        except VerifierError:
            continue
        index = revokes_by_target if parsed.name == "revoke" else supersedes_by_target
        index.setdefault(c.J[1], []).append(c)

    return revokes_by_target, supersedes_by_target


def _classify_one(
    claim: Claim,
    store: ClaimStore,
    now: int | None,
    revokes_by_target: dict[bytes, list[Claim]],
    supersedes_by_target: dict[bytes, list[Claim]],
    policy: NucleusPolicy | None,
) -> Classification:
    # D73 gilt nur für classify() auf einen einzelnen Claim. classify_all wendet policy
    # scope-lokal an (D91) und reicht hier bereits die passende Policy (oder None) herein.
    if is_core_predicate(claim):
        target = store.get(claim.J[1])
        if target is not None and target.I != claim.I:
            raise ForeignLifecycle()

    if _is_in_equivocation_pair(claim, store):
        return Classification(state=State.EQUIVOCATION_FLAGGED, trust_usable=False)

    pred_ok, pred = _predecessor_known_and_valid(claim, store)
    if not pred_ok:
        return Classification(state=State.PENDING, trust_usable=False)

    if pred is not None and claim.t < pred.t:
        return Classification(state=State.TIME_REGRESSION_FLAGGED, trust_usable=False)

    temporal = _is_temporally_valid(claim, now)

    protected = is_irrevocable(claim.p, policy)

    cid = claim_id(claim)

    superseding = [c for c in supersedes_by_target.get(cid, []) if c.I == claim.I]
    if not protected and superseding:
        return Classification(state=State.SUPERSEDED, trust_usable=False)

    revoking = [c for c in revokes_by_target.get(cid, []) if c.I == claim.I]
    if not protected and revoking:
        return Classification(state=State.REVOKED, trust_usable=False)

    if temporal is None:
        return Classification(state=State.LINKED, trust_usable=False)

    if temporal is False:
        return Classification(state=State.EXPIRED, trust_usable=False)

    return Classification(state=State.ACTIVE, trust_usable=True)


def _policy_for_claim(
    claim: Claim, policy: NucleusPolicy | None
) -> NucleusPolicy | None:
    """Policy nur für nuc:-Claims mit N == policy.scope (03-profiles.md §6, D91)."""
    if policy is None:
        return None
    if claim.p.startswith("nuc:") and claim.N == policy.scope:
        return policy
    return None


def classify_all(
    store: ClaimStore,
    now: int,
    policy: NucleusPolicy | None = None,
) -> dict[bytes, Classification]:
    """Ein Durchlauf über den Store; klassifiziert jeden Claim (02a §3, D87/D91).

    ``policy`` gilt nur für ``nuc:``-Claims mit ``N == policy.scope``; alle übrigen
    werden mit ``policy=None`` klassifiziert. Wirft nie wegen fremdem Scope (PR-INV-12).
    """
    claims = store.all_claims()
    revokes_by_target, supersedes_by_target = _build_lifecycle_index(claims)

    result: dict[bytes, Classification] = {}
    for claim in claims:
        effective = _policy_for_claim(claim, policy)
        result[claim_id(claim)] = _classify_one(
            claim, store, now, revokes_by_target, supersedes_by_target, effective
        )
    return result
