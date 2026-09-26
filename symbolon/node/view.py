"""Sicht als reine Funktion des Bestands und der Uhr (D473 Beschluss 2)."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from symbolon.atom import Claim, claim_id
from symbolon.governance.findings import Finding, GovernanceFinding, dedupe_sort
from symbolon.governance.objects import Proposal, epoch_id
from symbolon.governance.tally import TallyResult, TallyState, decide, reached, vote_root
from symbolon.governance.tally import read_v as read_vote_v
from symbolon.index import classify_all
from symbolon.policy import constitution_hash, participants_wellformed
from symbolon.predicates import is_nuc_name
from symbolon.profiles.credit import SettlementResult, SettlementState, settlement
from symbolon.profiles.membership import MembershipResult, MembershipState, membership
from symbolon.profiles.payload import read_v
from symbolon.resolve import NucleusState, resolve_state
from symbolon.trust.attribution import AttributionStatus, attribution
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


@dataclass(frozen=True, slots=True)
class FieldChange:
    """Unterschied eines Verfassungsfelds außer ``participants`` (D484 Beschluss 2)."""

    field: str
    old: object
    new: object


@dataclass(frozen=True, slots=True)
class ProposalChanges:
    """Unterschiede zwischen geltender und vorgeschlagener Verfassung (D484 Beschluss 2)."""

    added: tuple[bytes, ...]
    removed: tuple[bytes, ...]
    fields: tuple[FieldChange, ...]


@dataclass(frozen=True, slots=True)
class ProposalView:
    """Ein Antrag: propose@1 eines Teilnehmers auf ein Vorschlagsobjekt

    (D482 Befund 2, D484 Beschluss 2, D487 Beschluss 3).
    """

    proposal: bytes
    proposers: tuple[bytes, ...]
    state: TallyState
    yes: tuple[bytes, ...]
    no: tuple[bytes, ...]
    ambiguous: tuple[bytes, ...]
    n: int | None
    needed: int | None
    changes: ProposalChanges


@dataclass(frozen=True, slots=True)
class TaskView:
    """Eine Aufgabe einer Identität in einem Scope (D484 Beschluss 1). ``detail`` ist,

    je nach ``art``, ein Verfassungs-, Vorschlags- oder Obligationshash.
    """

    scope: bytes
    art: str
    detail: bytes


def _antraege(
    store: SqliteStore, scope: bytes, participants: frozenset[bytes]
) -> dict[bytes, tuple[bytes, ...]]:
    """propose@1 eines Teilnehmers der geltenden Epoche, nach Ziel-Hash (D482 Befund 2, 04 §2.1).

    Ein Vorschlagsobjekt gilt der Oberfläche nur als Antrag, wenn ein solcher Claim im
    Bestand liegt; die Auszählung selbst bleibt unberührt (D484 Befund 2).
    """
    grouped: dict[bytes, set[bytes]] = defaultdict(set)
    for claim in store.all_claims():
        if not is_nuc_name(claim, "propose") or claim.N != scope:
            continue
        if claim.I not in participants:
            continue
        if claim.J[0] != 3:
            continue
        grouped[claim.J[1]].add(claim.I)
    return {digest: tuple(sorted(authors)) for digest, authors in grouped.items()}


def _needed(threshold: tuple[int, int] | None, n: int | None) -> int | None:
    """Kleinstes ``y`` mit ``reached(y, n, num, den)``, keine zweite Formel (D484 Beschluss 2, 04 §3.2)."""
    if threshold is None or n is None:
        return None
    num, den = threshold
    for y in range(n + 1):
        if reached(y, n, num, den):
            return y
    return None


def _changes(current: dict, target: dict | None) -> ProposalChanges:
    """``participants`` getrennt, jedes andere Feld mit altem und neuem Wert (D484 Beschluss 2)."""
    if target is None:
        return ProposalChanges(added=(), removed=(), fields=())
    old_participants = set(current.get("participants", ()))
    new_participants = set(target.get("participants", ()))
    added = tuple(sorted(new_participants - old_participants))
    removed = tuple(sorted(old_participants - new_participants))
    keys = sorted((set(current) | set(target)) - {"participants"})
    fields = tuple(
        FieldChange(field=key, old=current.get(key), new=target.get(key))
        for key in keys
        if current.get(key) != target.get(key)
    )
    return ProposalChanges(added=added, removed=removed, fields=fields)


def proposals_view(store: SqliteStore, scope: bytes, now: int) -> tuple[ProposalView, ...]:
    """Anträge auf der geltenden Epoche, sortiert nach ``proposal`` (D484 Beschluss 2, D487 Beschluss 3).

    ``yes``, ``no`` und ``ambiguous`` nennen die Wurzeln der Stimmen (D542 Beschluss 4, 04 §3.1).
    """
    if scope not in store.all_genesis():
        raise ValueError("genesis of scope is not in the store")
    view = scope_view(store, scope, now)
    if view.verein is None:
        return ()
    participants = frozenset(view.state.constitution_obj["participants"])
    grouped = _antraege(store, scope, participants)
    proposals = store.all_proposals()
    constitutions = store.all_constitutions()
    current = view.state.constitution_obj
    attr = attribution(store, classify_all(store, now, view.state.policy), scope)
    result: list[ProposalView] = []
    for digest, tally in view.verein.decisions:
        proposers = grouped.get(digest)
        if not proposers:
            continue
        yes_authors = tuple(sorted({vote_root(attr, store.get(cid)) for cid in tally.yes}))
        no_authors = tuple(sorted({vote_root(attr, store.get(cid)) for cid in tally.no}))
        ambiguous_authors = tuple(
            sorted(
                {
                    vote_root(attr, store.get(finding.subject))
                    for finding in tally.findings
                    if finding.kind is GovernanceFinding.AMBIGUOUS_VOTE
                    and store.get(finding.subject) is not None
                }
            )
        )
        proposal_obj = proposals.get(digest)
        target = constitutions.get(proposal_obj.constitution_hash) if proposal_obj else None
        result.append(
            ProposalView(
                proposal=digest,
                proposers=proposers,
                state=tally.state,
                yes=yes_authors,
                no=no_authors,
                ambiguous=ambiguous_authors,
                n=tally.n,
                needed=_needed(tally.threshold, tally.n),
                changes=_changes(current, target),
            )
        )
    return tuple(sorted(result, key=lambda item: item.proposal))


def tasks_view(store: SqliteStore, I: bytes, now: int) -> tuple[TaskView, ...]:
    """Aufgaben einer Identität über alle Scopes, sortiert (D484 Beschluss 1).

    Ist ``I`` in einem Scope als Gerät aufgenommen, gelten dort die Aufgaben ``VOTE`` und
    ``RATIFY`` seiner Wurzel und keine andere; „abgestimmt“ heisst eine Stimme zum Antrag mit
    derselben Wurzel (D542 Beschluss 4, D534 Beschluss 2, 04 §3.1, 02 §2.1).
    """
    tasks: list[TaskView] = []
    for scope in store.all_genesis():
        view = scope_view(store, scope, now)
        attr = attribution(store, classify_all(store, now, view.state.policy), scope)
        root = attr.device_root(I)
        geraet = root is not None
        wer = root if geraet else I
        if view.verein is not None:
            participants = frozenset(view.state.constitution_obj["participants"])
            if wer in participants:
                member = next(
                    (result for subject, result in view.verein.membership if subject == wer),
                    None,
                )
                if (
                    not geraet
                    and member is not None
                    and member.state is not MembershipState.MEMBER
                ):
                    tasks.append(
                        TaskView(
                            scope=scope,
                            art="CONFIRM_RULES",
                            detail=view.state.epoch.constitution_hash,
                        )
                    )
                grouped = _antraege(store, scope, participants)
                for digest, tally in view.verein.decisions:
                    if not grouped.get(digest):
                        continue
                    if tally.state is TallyState.PENDING:
                        voted = any(
                            is_nuc_name(claim, "vote")
                            and claim.N == scope
                            and claim.J == (3, digest)
                            and vote_root(attr, claim) == wer
                            for claim in store.all_claims()
                        )
                        if not voted:
                            tasks.append(TaskView(scope=scope, art="VOTE", detail=digest))
                    elif tally.state is TallyState.PASSED:
                        tasks.append(TaskView(scope=scope, art="RATIFY", detail=digest))
        if view.vereinsleben is not None and not geraet:
            for cid, result in view.vereinsleben.settlements:
                if result.state is not SettlementState.OPEN:
                    continue
                claim = store.get(cid)
                if claim is None:
                    continue
                if claim.I == I:
                    tasks.append(TaskView(scope=scope, art="CONTRIBUTION_OPEN", detail=cid))
                if claim.J[0] == 1 and claim.J[1] == I:
                    tasks.append(TaskView(scope=scope, art="RECEIPT", detail=cid))
    return tuple(sorted(tasks, key=lambda item: (item.scope, item.art, item.detail)))


@dataclass(frozen=True, slots=True)
class ObligationView:
    """Eine Zeile der Kassenliste: Schuldner, Gläubiger, Betrag, Zustand (D486 Beschluss 1)."""

    claim_id: bytes
    debtor: bytes
    creditor: bytes | None
    amount: int | None
    unit: str | None
    state: SettlementState


def _is_amount(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _obligation_amount_unit(v: bytes | None) -> tuple[int | None, str | None]:
    """Betrag und Einheit aus ``v``, oder beide ``null`` bei fremdem Inhalt (D486 Beschluss 1, 03 §3.3.1).

    ``v`` bleibt Anzeige: das Protokoll liest es nie (01 §2). Ist ``v`` nicht die Form aus
    03 §1.3 oder ist die Einheit kein UTF-8, erscheint die Obligation trotzdem, nur ohne Zahl.
    """
    obj, _kinds = read_v(v)
    if obj is None:
        return None, None
    amount = obj.get(0)
    if amount is not None and not _is_amount(amount):
        return None, None
    unit_raw = obj.get(1)
    if unit_raw is None:
        return amount, None
    if not isinstance(unit_raw, bytes):
        return None, None
    try:
        unit = unit_raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, None
    return amount, unit


def obligations_view(store: SqliteStore, scope: bytes, now: int) -> tuple[ObligationView, ...]:
    """Obligationen eines Scopes aus dem Zustand der Sicht, sortiert nach ``claim_id`` (D486 Beschluss 1).

    Nutzt ``view.vereinsleben.settlements``, keine zweite Rechnung mit ``settlement``.
    """
    if scope not in store.all_genesis():
        raise ValueError("genesis of scope is not in the store")
    view = scope_view(store, scope, now)
    if view.vereinsleben is None:
        return ()
    result: list[ObligationView] = []
    for cid, settlement_result in view.vereinsleben.settlements:
        claim = store.get(cid)
        if claim is None:
            continue
        creditor = claim.J[1] if claim.J[0] == 1 else None
        amount, unit = _obligation_amount_unit(claim.v)
        result.append(
            ObligationView(
                claim_id=cid,
                debtor=claim.I,
                creditor=creditor,
                amount=amount,
                unit=unit,
                state=settlement_result.state,
            )
        )
    return tuple(result)


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


@dataclass(frozen=True, slots=True)
class GeraeteStimmen:
    """Stimmen einer Wurzel zu einem Antrag von mehreren Schlüsseln (D542 Beschluss 5, D543).

    ``stimmen`` sind ``(claim_id, I, wahl)``, sortiert; ``changes`` gegen die Verfassung der
    Vorgängerepoche des Antrags.
    """

    root: bytes
    proposal: bytes
    changes: ProposalChanges
    stimmen: tuple[tuple[bytes, bytes, int], ...]


def geraetestimmen(store: SqliteStore, scope: bytes, now: int) -> tuple[GeraeteStimmen, ...]:
    """Aktive ``vote@1`` eines Scopes je Wurzel und Antrag, über alle Epochen, nur wo Stimmen von
    mindestens zwei Schlüsseln stammen (D542 Beschluss 5, D543 Beschluss 1 und 3, 04 §3.1, 02 §2.1).

    Gelesen werden nur Stimmen mit ``J``-Tag 3, ohne ``t_exp``, ``ACTIVE``, nicht bestritten, mit
    lesbarem, kanonischem ``v`` und Wahl ``0`` oder ``1``. Eine Gruppe erscheint nur, wenn ihr
    Antrag im Bestand liegt, die Verfassung seiner Vorgängerepoche bekannt ist und die Wurzel unter
    deren ``participants`` steht. Sortiert nach ``(root, proposal)``.
    """
    view = scope_view(store, scope, now)
    if view.verein is None:
        return ()
    classified = classify_all(store, now, view.state.policy)
    attr = attribution(store, classified, scope)
    grouped: dict[tuple[bytes, bytes], list[tuple[bytes, bytes, int]]] = defaultdict(list)
    for claim in store.all_claims():
        if not is_nuc_name(claim, "vote") or claim.N != scope:
            continue
        if claim.J[0] != 3 or claim.t_exp is not None:
            continue
        cid = claim_id(claim)
        classification = classified.get(cid)
        if classification is None or classification.state is not State.ACTIVE:
            continue
        if attr.status(claim) is AttributionStatus.DISPUTED:
            continue
        obj, kind = read_vote_v(claim.v)
        if obj is None or kind is not None:
            continue
        wahl = obj.get(0)
        if type(wahl) is not int or wahl not in (0, 1):
            continue
        grouped[(vote_root(attr, claim), claim.J[1])].append((cid, claim.I, wahl))
    proposals = store.all_proposals()
    constitutions = store.all_constitutions()
    result: list[GeraeteStimmen] = []
    for (root, digest), stimmen in grouped.items():
        if len({key for _cid, key, _wahl in stimmen}) < 2:
            continue
        proposal = proposals.get(digest)
        if proposal is None:
            continue
        # Die Vorgängerverfassung: die bekannte, deren Epoche 0 bis zur geltenden die
        # Vorgängerepoche des Antrags ist (04 §1.1, 04 §2.4).
        vorgaenger = next(
            (
                constitution
                for index in range(view.state.epoch.index + 1)
                for key, constitution in constitutions.items()
                if epoch_id(scope, index, key) == proposal.predecessor
            ),
            None,
        )
        if vorgaenger is None:
            continue
        participants = vorgaenger.get("participants")
        if not isinstance(participants, list) or root not in participants:
            continue
        result.append(
            GeraeteStimmen(
                root=root,
                proposal=digest,
                changes=_changes(vorgaenger, constitutions.get(proposal.constitution_hash)),
                stimmen=tuple(sorted(stimmen)),
            )
        )
    return tuple(sorted(result, key=lambda item: (item.root, item.proposal)))
