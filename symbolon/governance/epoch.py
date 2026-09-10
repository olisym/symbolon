"""Materialisierung einer gesättigten Entscheidung (04-governance.md §4)."""

from __future__ import annotations

from dataclasses import dataclass

from symbolon.atom import Claim, claim_id
from symbolon.governance.findings import (
    Finding,
    GovernanceFinding,
    dedupe_sort,
)
from symbolon.governance.objects import Epoch, Proposal
from symbolon.governance.tally import (
    TallyResult,
    TallyState,
    constitution_governable,
    reached,
    read_v,
)
from symbolon.index import classify_all
from symbolon.policy import NucleusPolicy, constitution_hash
from symbolon.predicates import is_nuc_name
from symbolon.verifier import ClaimStore, State


@dataclass(frozen=True, slots=True)
class RatificationResult:
    """Ergebnis von ``verify_ratification`` (04-governance.md §4.1, D99)."""

    next_epoch: Epoch | None
    findings: tuple[Finding, ...]


def _cited(ratify: Claim) -> tuple[list[object] | None, GovernanceFinding | None]:
    """Zeugenliste aus ``ratify.v`` (04-governance.md §4.1, 04-governance.md §2.3, D83, D275, D276).

    Nur Lage 3 verdrängt ``UNSUPPORTED_RATIFICATION`` durch ``NON_CANONICAL_V``.
    Lage 1 und Lage 2 behalten das heutige Ergebnis.
    """
    obj, kind = read_v(ratify.v)
    if kind is GovernanceFinding.NON_CANONICAL_V:
        return None, kind
    if obj is None:
        return None, None
    cited = obj.get(0)
    if not isinstance(cited, list):
        return None, None
    return cited, None


def _unsupported(ratify: Claim, tally: TallyResult) -> RatificationResult:
    return RatificationResult(
        next_epoch=None,
        findings=dedupe_sort(
            [
                Finding(kind=GovernanceFinding.UNSUPPORTED_RATIFICATION, subject=claim_id(ratify)),
                *tally.findings,
            ]
        ),
    )


def verify_ratification(
    store: ClaimStore,
    *,
    ratify: Claim,
    epoch: Epoch,
    proposal: Proposal,
    tally: TallyResult,
    target_constitution_obj: dict | None,
    now: int,
    policy: NucleusPolicy | None = None,
) -> RatificationResult:
    """Prüft ein ``ratify@1`` gegen eine Auszählung (04-governance.md §4.1, D106, D109, D112, D200, D203, D275, D276)."""
    if (
        proposal.scope != epoch.scope
        or tally.epoch_id != epoch.epoch_id
        or tally.proposal_hash != proposal.proposal_hash
    ):
        raise ValueError("tally does not match epoch and proposal")
    if tally.state is TallyState.UNEVALUABLE:
        return RatificationResult(
            next_epoch=None,
            findings=dedupe_sort(
                [
                    Finding(
                        kind=GovernanceFinding.TALLY_UNEVALUABLE,
                        subject=claim_id(ratify),
                    ),
                    *tally.findings,
                ]
            ),
        )
    if tally.participants is None:
        return RatificationResult(
            next_epoch=None,
            findings=dedupe_sort(
                [
                    Finding(
                        kind=GovernanceFinding.TALLY_UNEVALUABLE,
                        subject=claim_id(ratify),
                    ),
                    *tally.findings,
                ]
            ),
        )
    if (
        target_constitution_obj is None
        or constitution_hash(target_constitution_obj) != proposal.constitution_hash
    ):
        raise ValueError("target_constitution_obj does not match proposal")
    participants = tally.participants
    if ratify.N != epoch.scope or ratify.J != (3, proposal.proposal_hash):
        return _unsupported(ratify, tally)
    if not is_nuc_name(ratify, "ratify"):
        return _unsupported(ratify, tally)
    if ratify.I not in participants:
        return _unsupported(ratify, tally)
    if ratify.t_exp is not None:
        return RatificationResult(
            next_epoch=None,
            findings=dedupe_sort(
                [
                    Finding(kind=GovernanceFinding.RATIFY_WITH_EXPIRY, subject=claim_id(ratify)),
                    *tally.findings,
                ]
            ),
        )
    by_cid = classify_all(store, now, policy)
    rid = claim_id(ratify)
    if rid not in by_cid or by_cid[rid].state is not State.ACTIVE:
        return _unsupported(ratify, tally)
    cited, v_kind = _cited(ratify)
    if v_kind is GovernanceFinding.NON_CANONICAL_V:
        return RatificationResult(
            next_epoch=None,
            findings=dedupe_sort(
                [
                    Finding(
                        kind=GovernanceFinding.NON_CANONICAL_V,
                        subject=claim_id(ratify),
                    ),
                    *tally.findings,
                ]
            ),
        )
    if cited is None:
        return _unsupported(ratify, tally)
    witness_findings: list[Finding] = []
    authors: list[bytes] = []
    for cid in cited:
        if not isinstance(cid, bytes):
            witness_findings.append(
                Finding(kind=GovernanceFinding.UNSUPPORTED_RATIFICATION, subject=rid)
            )
            continue
        present = store.get(cid)
        if present is None:
            witness_findings.append(
                Finding(kind=GovernanceFinding.UNKNOWN_WITNESS_VOTE, subject=cid)
            )
        elif cid not in tally.yes:
            witness_findings.append(
                Finding(kind=GovernanceFinding.UNSUPPORTED_RATIFICATION, subject=rid)
            )
        else:
            authors.append(present.I)
    if witness_findings:
        return RatificationResult(
            next_epoch=None, findings=dedupe_sort([*witness_findings, *tally.findings])
        )
    if len(authors) != len(set(authors)):
        return _unsupported(ratify, tally)
    if tally.threshold is None or tally.n is None:
        return _unsupported(ratify, tally)
    num, den = tally.threshold
    if not reached(len(cited), tally.n, num, den):
        return _unsupported(ratify, tally)
    kind = constitution_governable(target_constitution_obj)
    if kind is not None:
        return RatificationResult(
            next_epoch=None,
            findings=dedupe_sort(
                [
                    Finding(kind=kind, subject=proposal.constitution_hash),
                    *tally.findings,
                ]
            ),
        )
    return RatificationResult(
        next_epoch=Epoch(
            scope=epoch.scope,
            index=epoch.index + 1,
            constitution_hash=proposal.constitution_hash,
        ),
        findings=(),
    )
