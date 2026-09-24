"""Mitgliedschaft als Konjunktion zweier aktiver Claims (03-profiles.md §4)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from symbolon.atom import claim_id
from symbolon.policy import (
    NucleusPolicy,
    constitution_hash as hash_constitution,
    participants_wellformed,
)
from symbolon.predicates import is_nuc_name
from symbolon.profiles.findings import Finding, ProfileFinding, dedupe_sort
from symbolon.index import classify_all
from symbolon.verifier import ClaimStore, State


class MembershipState(str, Enum):
    MEMBER = "MEMBER"
    APPLICANT = "APPLICANT"
    GRANT_ONLY = "GRANT_ONLY"
    NONE = "NONE"


@dataclass(frozen=True, slots=True)
class MembershipResult:
    """Zustand der Mitgliedschaft plus zählende claim_ids (03-profiles.md §4)."""

    state: MembershipState
    accept_claim_id: bytes | None
    grant_claim_id: bytes | None
    findings: tuple[Finding, ...]


def membership(
    store: ClaimStore,
    *,
    subject: bytes,
    scope: bytes,
    constitution_hash: bytes,
    now: int,
    authorized_keys: frozenset[bytes],
    policy: NucleusPolicy | None = None,
    constitution_obj: dict | None = None,
) -> MembershipResult:
    """Wertet accept-rules ∧ grant-membership aus (03-profiles.md §4, 04 §6.2, D111)."""
    if policy is not None and policy.scope != scope:
        raise ValueError("policy scope does not match scope")
    if constitution_obj is not None:
        if hash_constitution(constitution_obj) != constitution_hash:
            raise ValueError("constitution_obj does not match constitution_hash")

    by_cid = classify_all(store, now, policy)
    findings: list[Finding] = []
    accept_ids: list[bytes] = []
    grant_ids: list[bytes] = []

    for c in store.all_claims():
        cid = claim_id(c)

        if is_nuc_name(c, "accept-rules") and c.I == subject:
            if c.N != scope:
                findings.append(
                    Finding(kind=ProfileFinding.SCOPE_MISMATCH, subject=cid)
                )
                continue
            if c.J != (3, constitution_hash):
                if c.J[0] == 3:
                    findings.append(
                        Finding(
                            kind=ProfileFinding.CONSTITUTION_VERSION_MISMATCH,
                            subject=cid,
                        )
                    )
                continue
            if by_cid[cid].state != State.ACTIVE:
                continue
            accept_ids.append(cid)
            continue

        if is_nuc_name(c, "grant-membership") and c.J == (1, subject):
            if c.N != scope:
                findings.append(
                    Finding(kind=ProfileFinding.SCOPE_MISMATCH, subject=cid)
                )
                continue
            if c.I not in authorized_keys:
                findings.append(
                    Finding(
                        kind=ProfileFinding.UNAUTHORIZED_GRANT_AUTHOR,
                        subject=cid,
                    )
                )
                continue
            if by_cid[cid].state != State.ACTIVE:
                continue
            grant_ids.append(cid)

    accept_claim_id = min(accept_ids) if accept_ids else None
    grant_claim_id = min(grant_ids) if grant_ids else None
    listed = False
    if constitution_obj is not None and participants_wellformed(constitution_obj):
        listed = subject in constitution_obj["participants"]
    has_accept = accept_claim_id is not None
    has_grant = grant_claim_id is not None or listed

    if has_accept and has_grant:
        state = MembershipState.MEMBER
    elif has_accept:
        state = MembershipState.APPLICANT
    elif has_grant:
        state = MembershipState.GRANT_ONLY
    else:
        state = MembershipState.NONE

    return MembershipResult(
        state=state,
        accept_claim_id=accept_claim_id,
        grant_claim_id=grant_claim_id,
        findings=dedupe_sort(findings),
    )
