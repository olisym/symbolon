"""Tilgung: Obligation und passende Quittung (03-profiles.md §3.3.2)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from symbolon.atom import Claim, claim_id
from symbolon.policy import NucleusPolicy
from symbolon.predicates import is_nuc_name
from symbolon.profiles.findings import Finding, ProfileFinding, dedupe_sort
from symbolon.index import classify_all
from symbolon.profiles.payload import read_v
from symbolon.verifier import ClaimStore, State


class SettlementState(str, Enum):
    SETTLED = "SETTLED"
    OPEN = "OPEN"
    EXPIRED = "EXPIRED"
    INDETERMINATE = "INDETERMINATE"


@dataclass(frozen=True, slots=True)
class SettlementResult:
    """Ergebnis von ``settlement`` (03-profiles.md §3.3.2, D79)."""

    state: SettlementState
    receipt_claim_id: bytes | None
    findings: tuple[Finding, ...]


def _is_valid_uint(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _obligation_v_findings(obligation: Claim) -> list[Finding]:
    """Typprüfung und EXPIRING_OBLIGATION (03 §1.3, 03 §3.3.1; B2)."""
    cid = claim_id(obligation)
    findings: list[Finding] = []
    if obligation.t_exp is not None:
        findings.append(
            Finding(kind=ProfileFinding.EXPIRING_OBLIGATION, subject=cid)
        )
    obj, kinds = read_v(obligation.v)
    for kind in kinds:
        findings.append(Finding(kind=kind, subject=cid))
    if obj is None:
        return findings
    if 0 in obj and not _is_valid_uint(obj[0]):
        findings.append(Finding(kind=ProfileFinding.INVALID_V_TYPE, subject=cid))
    if 1 in obj and not isinstance(obj[1], bytes):
        findings.append(Finding(kind=ProfileFinding.INVALID_V_TYPE, subject=cid))
    return findings


def settlement(
    store: ClaimStore,
    *,
    obligation: Claim,
    scope: bytes,
    now: int,
    policy: NucleusPolicy,
) -> SettlementResult:
    """Bestimmt den Tilgungszustand einer Obligation (03-profiles.md §3.3.2, 03-prompt.md §6).

    ``policy`` ist Pflicht-Keyword ohne Default (D80).
    """
    if not is_nuc_name(obligation, "obligation") or obligation.N != scope:
        raise ValueError("obligation must be obligation@1 in scope")
    if policy.scope != scope:
        raise ValueError("policy scope does not match scope")

    o_cid = claim_id(obligation)
    if store.get(o_cid) is None:
        raise ValueError("obligation not in store")

    by_cid = classify_all(store, now, policy)
    findings: list[Finding] = _obligation_v_findings(obligation)
    o_state = by_cid[o_cid].state

    if o_state == State.EXPIRED:
        return SettlementResult(
            state=SettlementState.EXPIRED,
            receipt_claim_id=None,
            findings=dedupe_sort(findings),
        )

    if o_state == State.PENDING:
        findings.append(
            Finding(kind=ProfileFinding.OBLIGATION_PENDING, subject=o_cid)
        )
        return SettlementResult(
            state=SettlementState.INDETERMINATE,
            receipt_claim_id=None,
            findings=dedupe_sort(findings),
        )

    if o_state == State.EQUIVOCATION_FLAGGED:
        findings.append(
            Finding(kind=ProfileFinding.OBLIGATION_AUTHOR_FLAGGED, subject=o_cid)
        )
        return SettlementResult(
            state=SettlementState.INDETERMINATE,
            receipt_claim_id=None,
            findings=dedupe_sort(findings),
        )

    if o_state == State.TIME_REGRESSION_FLAGGED:
        findings.append(
            Finding(kind=ProfileFinding.OBLIGATION_TIME_REGRESSION, subject=o_cid)
        )
        return SettlementResult(
            state=SettlementState.INDETERMINATE,
            receipt_claim_id=None,
            findings=dedupe_sort(findings),
        )

    assert o_state not in (
        State.REVOKED,
        State.SUPERSEDED,
        State.LINKED,
    ), f"unreachable obligation state under policy: {o_state}"
    assert o_state == State.ACTIVE, f"unexpected obligation state: {o_state}"

    matching: list[Claim] = []
    for c in store.all_claims():
        if not is_nuc_name(c, "receipt"):
            continue
        if c.J != (2, o_cid):
            continue
        if c.N != scope:
            findings.append(
                Finding(kind=ProfileFinding.SCOPE_MISMATCH, subject=claim_id(c))
            )
            continue
        if obligation.J[0] != 1 or c.I != obligation.J[1]:
            continue
        if by_cid[claim_id(c)].state != State.ACTIVE:
            continue
        matching.append(c)

    matching.sort(key=claim_id)
    receipt_claim_id: bytes | None = None
    settled = False

    for r in matching:
        rid = claim_id(r)
        if receipt_claim_id is None:
            receipt_claim_id = rid

        if r.v is None:
            settled = True
            receipt_claim_id = rid
            break

        obj, kinds = read_v(r.v)
        if obj is None:
            findings.append(
                Finding(kind=ProfileFinding.PARTIAL_RECEIPT_UNSUPPORTED, subject=rid)
            )
            for kind in kinds:
                findings.append(Finding(kind=kind, subject=rid))
            continue

        if 0 in obj:
            findings.append(
                Finding(kind=ProfileFinding.PARTIAL_RECEIPT_UNSUPPORTED, subject=rid)
            )
            if not _is_valid_uint(obj[0]):
                findings.append(
                    Finding(kind=ProfileFinding.INVALID_V_TYPE, subject=rid)
                )
            continue

        settled = True
        receipt_claim_id = rid
        break

    if settled:
        return SettlementResult(
            state=SettlementState.SETTLED,
            receipt_claim_id=receipt_claim_id,
            findings=dedupe_sort(findings),
        )

    return SettlementResult(
        state=SettlementState.OPEN,
        receipt_claim_id=receipt_claim_id,
        findings=dedupe_sort(findings),
    )
