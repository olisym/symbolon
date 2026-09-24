"""Sicht als reine Funktion des Bestands und der Uhr (D473 Beschluss 2)."""

from __future__ import annotations

from dataclasses import dataclass

from symbolon.atom import Claim, claim_id
from symbolon.governance.findings import Finding, GovernanceFinding, dedupe_sort
from symbolon.governance.objects import Proposal
from symbolon.governance.tally import TallyResult, decide
from symbolon.index import classify_all
from symbolon.policy import constitution_hash, participants_wellformed
from symbolon.predicates import is_nuc_name
from symbolon.profiles.credit import SettlementResult, settlement
from symbolon.profiles.membership import MembershipResult, membership
from symbolon.resolve import NucleusState, resolve_state
from symbolon.trust.derive import Derivation, derive
from symbolon.trust.params import resolve_trust_params
from symbolon.verifier import State

from symbolon.node.store import SqliteStore


@dataclass(frozen=True, slots=True)
class VereinView:
    """Teil Verein: Mitgliedschaft und Auszählung (D473 Beschluss 3, 04 §6.2)."""

    membership: tuple[tuple[bytes, MembershipResult], ...]
    decisions: tuple[tuple[bytes, TallyResult], ...]


@dataclass(frozen=True, slots=True)
class VereinslebenView:
    """Teil Vereinsleben: Ableitung und Tilgung (D473 Beschluss 3, 03 §3.3.2)."""

    derivation: Derivation
    settlements: tuple[tuple[bytes, SettlementResult], ...]


@dataclass(frozen=True, slots=True)
class ScopeView:
    """Sicht eines Scopes (D473 Beschluss 3, D474 Beschluss 2)."""

    state: NucleusState
    verein: VereinView | None
    vereinsleben: VereinslebenView | None
    findings: tuple[Finding, ...]


@dataclass(frozen=True, slots=True)
class ForkGroup:
    """Eine Gabelung: Autor, Vorgänger, claim_id und Scope (D473 Beschluss 4, 02 §8)."""

    I: bytes
    h_prev: bytes
    claims: tuple[tuple[bytes, bytes | None], ...]


def scope_view(store: SqliteStore, scope: bytes, now: int) -> ScopeView:
    """Sicht eines Scopes (D473 Beschluss 3, D474 Beschluss 2, 04 §3.5, 04 §4.5, 04 §6.2)."""
    genesis = store.all_genesis().get(scope)
    if genesis is None:
        raise ValueError("genesis of scope is not in the store")
    constitutions = store.all_constitutions()
    proposals = store.all_proposals()
    state = resolve_state(
        store,
        scope=scope,
        genesis_obj=genesis,
        known_constitutions=constitutions,
        known_proposals=proposals,
        now=now,
    )
    verein: VereinView | None = None
    findings: list[Finding] = []
    constitution = state.constitution_obj
    if constitution is not None and "participants" in constitution:
        if not participants_wellformed(constitution):
            findings.append(
                Finding(
                    GovernanceFinding.MALFORMED_PARTICIPANTS,
                    constitution_hash(constitution),
                )
            )
        else:
            members = tuple(
                sorted(
                    (
                        (
                            subject,
                            membership(
                                store,
                                subject=subject,
                                scope=scope,
                                constitution_hash=state.epoch.constitution_hash,
                                now=now,
                                authorized_keys=state.authorized_keys,
                                policy=state.policy,
                                constitution_obj=constitution,
                            ),
                        )
                        for subject in constitution["participants"]
                    ),
                    key=lambda item: item[0],
                )
            )
            listed: list[tuple[bytes, TallyResult]] = []
            for digest, proposal in proposals.items():
                if proposal.predecessor != state.epoch.epoch_id:
                    continue
                listed.append(
                    (
                        digest,
                        _decide_proposal(
                            store,
                            state,
                            genesis,
                            proposal,
                            constitutions,
                            proposals,
                            now,
                        ),
                    )
                )
            verein = VereinView(
                membership=members,
                decisions=tuple(sorted(listed, key=lambda item: item[0])),
            )
    vereinsleben: VereinslebenView | None = None
    if 9 in genesis:
        derivation = derive(
            store,
            anchors=frozenset(genesis[3]),
            scope=scope,
            now=now,
            params=resolve_trust_params(scope=scope, genesis_obj=genesis),
        )
        settled: list[tuple[bytes, SettlementResult]] = []
        for claim in store.all_claims():
            if not is_nuc_name(claim, "obligation") or claim.N != scope:
                continue
            settled.append(
                (
                    claim_id(claim),
                    settlement(
                        store,
                        obligation=claim,
                        scope=scope,
                        now=now,
                        policy=state.policy,
                    ),
                )
            )
        vereinsleben = VereinslebenView(
            derivation=derivation,
            settlements=tuple(sorted(settled, key=lambda item: item[0])),
        )
    return ScopeView(
        state=state,
        verein=verein,
        vereinsleben=vereinsleben,
        findings=dedupe_sort(findings),
    )


def _decide_proposal(
    store: SqliteStore,
    state: NucleusState,
    genesis: dict,
    proposal: Proposal,
    constitutions: dict[bytes, dict],
    proposals: dict[bytes, Proposal],
    now: int,
) -> TallyResult:
    return decide(
        store,
        epoch=state.epoch,
        proposal=proposal,
        genesis_obj=genesis,
        constitution_obj=state.constitution_obj,
        target_constitution_obj=constitutions.get(proposal.constitution_hash),
        known_proposals=proposals,
        now=now,
        policy=state.policy,
    )


def fork_evidence(store: SqliteStore, now: int) -> tuple[ForkGroup, ...]:
    """Gabelungsbeweise über alle Scopes (D473 Beschluss 4, 02 §8)."""
    classified = classify_all(store, now)
    grouped: dict[tuple[bytes, bytes], list[Claim]] = {}
    for claim in store.all_claims():
        cid = claim_id(claim)
        classification = classified.get(cid)
        if classification is None or classification.state is not State.EQUIVOCATION_FLAGGED:
            continue
        grouped.setdefault((claim.I, claim.h_prev), []).append(claim)
    groups: list[ForkGroup] = []
    for author, prev in sorted(grouped):
        entries = tuple(
            sorted(
                ((claim_id(claim), claim.N) for claim in grouped[(author, prev)]),
                key=lambda item: item[0],
            )
        )
        groups.append(ForkGroup(I=author, h_prev=prev, claims=entries))
    return tuple(groups)
