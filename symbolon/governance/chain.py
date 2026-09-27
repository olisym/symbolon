"""Epochenkette aus aufeinanderfolgenden Übergängen und Fassung einer Epoche
(04-governance.md §4.5, 04-governance.md §4.6, D174, D571)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from symbolon.atom import Claim, claim_id
from symbolon.genesis import genesis_scope
from symbolon.governance.epoch import verify_ratification
from symbolon.governance.findings import (
    Finding,
    GovernanceFinding,
    dedupe_sort,
)
from symbolon.governance.objects import Epoch, Motion, Proposal, apply_motions
from symbolon.governance.tally import constitution_governable, decide, resolve_object
from symbolon.index import classify_all
from symbolon.policy import NucleusPolicy, constitution_hash
from symbolon.predicates import is_nuc_name
from symbolon.profiles.policy import resolve_policy
from symbolon.verifier import ClaimStore, State


@dataclass(frozen=True, slots=True)
class EpochResolution:
    """Ergebnis von ``resolve_epoch`` (04-governance.md §4.5, D174)."""

    epoch: Epoch
    constitution_obj: dict | None
    findings: tuple[Finding, ...]


def _known_constitution(known: Mapping[bytes, dict], h: bytes) -> dict | None:
    obj = known.get(h)
    if obj is None or constitution_hash(obj) != h:
        return None
    return obj


@dataclass(frozen=True, slots=True)
class FassungResolution:
    """Ergebnis von ``resolve_fassung`` (04-governance.md §4.6, D571)."""

    fassung_obj: dict | None
    applied: tuple[bytes, ...]
    findings: tuple[Finding, ...]


def _ratified_motions(
    store: ClaimStore,
    *,
    epoch: Epoch,
    genesis_obj: dict,
    constitution_obj: dict | None,
    known_proposals: Mapping[bytes, Proposal | Motion],
    now: int,
    policy: NucleusPolicy | None,
) -> tuple[frozenset[bytes], list[Finding]]:
    """Die festgestellten Sachanträge der Epoche und die Vermerke der nicht tragenden
    Feststellungen (04 §4.1, 04 §4.6, D571 Beschluss 2).

    Zur Epoche gehören die aktiven ``ratify@1`` mit Tag 3 auf einen Sachantrag, dessen Objekt eine
    Map mit ``predecessor == epoch_id`` ist. Trägt eine Feststellung eines Sachantrags, fallen die
    Vermerke seiner übrigen weg. Ohne Verfassung der Epoche ist nichts festgestellt.
    """
    if constitution_obj is None:
        return frozenset(), []
    by_cid = classify_all(store, now, policy)
    by_motion: dict[bytes, tuple[Motion, list[Claim]]] = {}
    for claim in store.all_claims():
        if not is_nuc_name(claim, "ratify") or claim.N != epoch.scope:
            continue
        if by_cid[claim_id(claim)].state is not State.ACTIVE or claim.J[0] != 3:
            continue
        motion = resolve_object(known_proposals, claim.J[1])
        if not isinstance(motion, Motion) or not isinstance(motion.obj, dict):
            continue
        if motion.scope != epoch.scope or motion.predecessor != epoch.epoch_id:
            continue
        by_motion.setdefault(motion.motion_hash, (motion, []))[1].append(claim)

    ratified: set[bytes] = set()
    findings: list[Finding] = []
    for motion, claims in by_motion.values():
        tally = decide(
            store,
            epoch=epoch,
            proposal=motion,
            genesis_obj=genesis_obj,
            constitution_obj=constitution_obj,
            target_constitution_obj=None,
            known_proposals=known_proposals,
            now=now,
            policy=policy,
        )
        pending: list[Finding] = []
        for claim in claims:
            result = verify_ratification(
                store,
                ratify=claim,
                epoch=epoch,
                proposal=motion,
                tally=tally,
                target_constitution_obj=None,
                now=now,
                policy=policy,
            )
            if result.ratified_motion is not None:
                ratified.add(result.ratified_motion)
            pending.extend(result.findings)
        if motion.motion_hash not in ratified:
            findings.extend(pending)
    return frozenset(ratified), findings


def resolve_epoch(
    store: ClaimStore,
    *,
    scope: bytes,
    genesis_obj: dict,
    known_constitutions: Mapping[bytes, dict],
    known_proposals: Mapping[bytes, Proposal | Motion],
    now: int,
) -> EpochResolution:
    """Leitet die geltende Epoche aus der Kette der Übergänge her (04-governance.md §4.5)."""
    computed = genesis_scope(genesis_obj)
    if scope != computed:
        raise ValueError("genesis_obj does not match scope")

    epoch = Epoch(scope=scope, index=1, constitution_hash=genesis_obj[4])

    while True:
        constitution_obj = _known_constitution(
            known_constitutions, epoch.constitution_hash
        )
        policy = resolve_policy(
            scope=scope,
            genesis_obj=genesis_obj,
            constitution_hash=epoch.constitution_hash,
            constitution_obj=constitution_obj,
        ).policy
        by_cid = classify_all(store, now, policy)

        # Die festgestellten Sachanträge vor den Vorschlägen; ihre Vermerke gehören zu
        # resolve_fassung, nicht zur Kette (04 §4.5, D570).
        ratified_motions, _motion_findings = _ratified_motions(
            store,
            epoch=epoch,
            genesis_obj=genesis_obj,
            constitution_obj=constitution_obj,
            known_proposals=known_proposals,
            now=now,
            policy=policy,
        )

        # Nur Vermerke der erreichten Epoche: die Liste entsteht je Schritt neu,
        # überholte Epochen fallen durch Verwerfen weg (04-governance.md §4.5).
        findings: list[Finding] = []
        by_proposal: dict[bytes, tuple[Proposal, list[Claim]]] = {}
        for claim in store.all_claims():
            if not is_nuc_name(claim, "ratify") or claim.N != scope:
                continue
            if by_cid[claim_id(claim)].state is not State.ACTIVE:
                continue
            proposal = resolve_object(known_proposals, claim.J[1])
            if isinstance(proposal, Motion):
                # Eine Feststellung eines Sachantrags führt zu keiner Epoche (04 §4.5).
                continue
            if proposal is None:
                # 04 §4.5: Vermerk nur bei Tag 3 und, wenn participants wohlgeformt
                # ist, bei I in P. Wohlgeformtheit kommt aus constitution_governable.
                emit = claim.J[0] == 3
                if constitution_obj is not None:
                    kind = constitution_governable(constitution_obj)
                    if kind not in (
                        GovernanceFinding.PARTICIPANTS_UNDECLARED,
                        GovernanceFinding.MALFORMED_PARTICIPANTS,
                    ):
                        emit = emit and claim.I in constitution_obj["participants"]
                if emit:
                    findings.append(
                        Finding(
                            kind=GovernanceFinding.EPOCH_PROPOSAL_UNAVAILABLE,
                            subject=claim.J[1],
                        )
                    )
                continue
            if proposal.scope != scope or proposal.predecessor != epoch.epoch_id:
                continue
            group = by_proposal.get(proposal.proposal_hash)
            if group is None:
                by_proposal[proposal.proposal_hash] = (proposal, [claim])
            else:
                group[1].append(claim)

        carrying: dict[bytes, Epoch] = {}
        for proposal, claims in by_proposal.values():
            target = _known_constitution(
                known_constitutions, proposal.constitution_hash
            )
            tally = decide(
                store,
                epoch=epoch,
                proposal=proposal,
                genesis_obj=genesis_obj,
                constitution_obj=constitution_obj,
                target_constitution_obj=target,
                known_proposals=known_proposals,
                now=now,
                policy=policy,
            )
            for claim in claims:
                result = verify_ratification(
                    store,
                    ratify=claim,
                    epoch=epoch,
                    proposal=proposal,
                    tally=tally,
                    target_constitution_obj=target,
                    now=now,
                    policy=policy,
                    ratified_motions=ratified_motions,
                )
                if result.next_epoch is None:
                    findings.extend(result.findings)
                else:
                    carrying[result.next_epoch.epoch_id] = result.next_epoch

        if len(carrying) == 1:
            epoch = next(iter(carrying.values()))
            continue
        if len(carrying) > 1:
            for successor_id in carrying:
                findings.append(
                    Finding(kind=GovernanceFinding.EPOCH_FORK, subject=successor_id)
                )
        return EpochResolution(
            epoch=epoch,
            constitution_obj=constitution_obj,
            findings=dedupe_sort(findings),
        )


def resolve_fassung(
    store: ClaimStore,
    *,
    epoch: Epoch,
    genesis_obj: dict,
    constitution_obj: dict | None,
    known_proposals: Mapping[bytes, Proposal | Motion],
    now: int,
) -> FassungResolution:
    """Die Fassung der Epoche, die angewandten Sachanträge und die Vermerke der nicht tragenden
    Feststellungen (04-governance.md §4.6, D570 Beschluss 4, D571).

    ``epoch`` und ``constitution_obj`` sind das Ergebnis von ``resolve_epoch`` (04 §4.5). Ohne
    ``constitution_obj`` ist alles leer.
    """
    if constitution_obj is None:
        return FassungResolution(fassung_obj=None, applied=(), findings=())
    policy = resolve_policy(
        scope=epoch.scope,
        genesis_obj=genesis_obj,
        constitution_hash=epoch.constitution_hash,
        constitution_obj=constitution_obj,
    ).policy
    ratified, findings = _ratified_motions(
        store,
        epoch=epoch,
        genesis_obj=genesis_obj,
        constitution_obj=constitution_obj,
        known_proposals=known_proposals,
        now=now,
        policy=policy,
    )
    motions = [resolve_object(known_proposals, h) for h in sorted(ratified)]
    fassung_obj, applied = apply_motions(constitution_obj, motions)
    return FassungResolution(
        fassung_obj=fassung_obj,
        applied=applied,
        findings=dedupe_sort(findings),
    )
