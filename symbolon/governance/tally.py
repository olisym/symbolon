"""Auszählung einer Epoche (04-governance.md §3)."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id
from symbolon.genesis import genesis_scope
from symbolon.governance.findings import (
    Finding,
    GovernanceFinding,
    dedupe_sort,
)
from symbolon.governance.objects import Epoch, Proposal
from symbolon.index import classify_all
from symbolon.policy import NucleusPolicy, constitution_hash, participants_wellformed
from symbolon.predicates import is_nuc_name
from symbolon.trust.attribution import Attribution, AttributionStatus, attribution
from symbolon.verifier import Classification, ClaimStore, State

_CLASS_BY_INDEX = {0: "ordinary", 1: "membership", 2: "amendment"}


class TallyState(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    PENDING = "PENDING"
    UNEVALUABLE = "UNEVALUABLE"


@dataclass(frozen=True, slots=True)
class TallyResult:
    """Ergebnis von ``decide`` (04-governance.md §3.3, D106, D109)."""

    state: TallyState
    yes: tuple[bytes, ...]
    no: tuple[bytes, ...]
    participants: frozenset[bytes] | None
    threshold: tuple[int, int] | None
    findings: tuple[Finding, ...]
    epoch_id: bytes
    proposal_hash: bytes

    @property
    def n(self) -> int | None:
        if self.participants is None:
            return None
        return len(self.participants)


def ratio_max(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    """Maximum zweier Verhältnisse über Kreuzmultiplikation (04-governance.md §3.4)."""
    return a if a[0] * b[1] >= b[0] * a[1] else b


def reached(yes: int, n: int, num: int, den: int) -> bool:
    """``|Ja| * den > num * n`` — strikt (04-governance.md §3.2)."""
    return yes * den > num * n


def hopeless(no: int, n: int, num: int, den: int) -> bool:
    """``(n - |Nein|) * den <= num * n`` (04-governance.md §3.2)."""
    return (n - no) * den <= num * n


def threshold_class(old_obj: dict, new_obj: dict, genesis_obj: dict) -> str:
    """Klasse aus dem Verfassungsunterschied (04-governance.md §3.4, D113).

    Liest ``genesis_obj[5]`` ungeprüft. Der Aufrufer muss Bindung und Index
    bereits validiert haben — so wie ``decide`` es tut (04-governance.md §3, D145).
    """
    old_rest = {k: v for k, v in old_obj.items() if k != "participants"}
    new_rest = {k: v for k, v in new_obj.items() if k != "participants"}
    if cbor_canon.encode(old_rest) == cbor_canon.encode(new_rest):
        return "membership"
    return _CLASS_BY_INDEX[genesis_obj[5]]


def applied_threshold(old_obj: dict, new_obj: dict, klass: str) -> tuple[int, int]:
    """Angewandte Schwelle: ``ratio_max`` beider Verfassungen (04-governance.md §3.4, D113)."""
    old_th = old_obj["thresholds"][klass]
    new_th = new_obj["thresholds"][klass]
    return ratio_max((old_th[0], old_th[1]), (new_th[0], new_th[1]))


def read_v(v: bytes | None) -> tuple[dict | None, GovernanceFinding | None]:
    """Liest ``v`` in der Form aus 03-profiles.md §1.3 (04-governance.md §2.3, D83, D276).

    Vier Lagen: abwesend; vorhanden und nicht lesbar; lesbar und nicht kanonisch;
    lesbar und kanonisch. ``decode`` und ``is_canonical`` stehen im selben ``try``;
    der ``except``-Zweig führt in die zweite Lage, nicht am ``try`` vorbei.
    """
    if v is None:
        return None, None
    try:
        obj = cbor_canon.decode(v)
        if not cbor_canon.keys_admissible(v):
            return None, GovernanceFinding.UNPARSABLE_V
        canonical = cbor_canon.is_canonical(v)
    except Exception:
        return None, GovernanceFinding.UNPARSABLE_V
    if not canonical:
        return None, GovernanceFinding.NON_CANONICAL_V
    if not isinstance(obj, dict):
        return None, GovernanceFinding.UNPARSABLE_V
    return obj, None


def _choice(vote: Claim) -> object:
    obj, _kind = read_v(vote.v)
    if obj is None:
        return None
    return obj.get(0)


def _is_yes_choice(value: object) -> bool:
    return type(value) is int and value == 1


def _is_known_choice(value: object) -> bool:
    return type(value) is int and value in (0, 1)


def vote_root(attr: Attribution, vote: Claim) -> bytes:
    """Wurzel einer Stimme: bei ``ATTRIBUTED`` und ``DISPUTED`` die Wurzel des aufgenommenen
    Geräts, sonst ``vote.I`` (04 §3.1, 02 §2.1)."""
    if attr.status(vote) in (AttributionStatus.ATTRIBUTED, AttributionStatus.DISPUTED):
        return attr.device_root(vote.I)
    return vote.I


def _arbitrators(constitution_obj: dict) -> frozenset[bytes]:
    """``arbitration.arbitrators`` der Verfassung; nicht wohlgeformt heisst keine (04 §3.1, 00 §5.1)."""
    arbitration = constitution_obj.get("arbitration")
    if not isinstance(arbitration, dict):
        return frozenset()
    arbitrators = arbitration.get("arbitrators")
    if not isinstance(arbitrators, list):
        return frozenset()
    if not all(isinstance(a, bytes) and len(a) == 32 for a in arbitrators):
        return frozenset()
    return frozenset(arbitrators)


def _reattributed(
    store: ClaimStore,
    classifications: dict[bytes, Classification],
    *,
    vote_cid: bytes,
    scope: bytes,
    constitution_obj: dict,
) -> bool:
    """Rechnet ein Verdikt die bestrittene Stimme ``vote_cid`` zu? (04 §3.1, D533, D539)

    Nur Pfad (i): ``verdict.I`` in ``arbitration.arbitrators`` der Verfassung der Epoche, und
    ``verdict@1`` steht in ihren ``irrevocable_predicates``. Ob die Anklage aktiv ist, zählt nicht.
    """
    if "verdict@1" not in constitution_obj.get("irrevocable_predicates", []):
        return False
    arbitrators = _arbitrators(constitution_obj)
    if not arbitrators:
        return False
    accusations = {
        claim_id(c)
        for c in store.all_claims()
        if is_nuc_name(c, "accusation") and c.N == scope and c.J == (2, vote_cid)
    }
    for c in store.all_claims():
        if not is_nuc_name(c, "verdict") or c.N != scope:
            continue
        if c.J[0] != 2 or c.J[1] not in accusations:
            continue
        if c.t_exp is not None or c.I not in arbitrators:
            continue
        classification = classifications.get(claim_id(c))
        if classification is None or classification.state is not State.ACTIVE:
            continue
        obj, _kind = read_v(c.v)
        if obj is not None and _is_yes_choice(obj.get(0)):
            return True
    return False


def _is_ratio(value: object) -> bool:
    """Wohlgeformtheit einer Schwelle (04-governance.md §3.5, D108)."""
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        return False
    num, den = value
    if type(num) is not int or type(den) is not int:
        return False
    if den < 1:
        return False
    if not (0 <= num <= den):
        return False
    if 2 * num < den:
        return False
    return True


def _unevaluable(
    kind: GovernanceFinding,
    subject: bytes,
    *,
    epoch: Epoch,
    proposal: Proposal,
) -> TallyResult:
    return TallyResult(
        state=TallyState.UNEVALUABLE,
        yes=(),
        no=(),
        participants=None,
        threshold=None,
        findings=dedupe_sort([Finding(kind=kind, subject=subject)]),
        epoch_id=epoch.epoch_id,
        proposal_hash=proposal.proposal_hash,
    )


def constitution_governable(obj: dict) -> GovernanceFinding | None:
    """Gibt die Vermerksart zurück, wenn ``obj`` keine Auszählung tragen kann (04-governance.md §3.5, D200)."""
    if "participants" not in obj:
        return GovernanceFinding.PARTICIPANTS_UNDECLARED
    if not participants_wellformed(obj):
        return GovernanceFinding.MALFORMED_PARTICIPANTS
    raw_irr = obj.get("irrevocable_predicates", [])
    if not isinstance(raw_irr, (list, tuple)) or "vote@1" not in raw_irr:
        return GovernanceFinding.VOTE_REVOCABLE
    if "ratify@1" not in raw_irr:
        return GovernanceFinding.RATIFY_REVOCABLE
    return None


def decide(
    store: ClaimStore,
    *,
    epoch: Epoch,
    proposal: Proposal,
    genesis_obj: dict,
    constitution_obj: dict | None,
    target_constitution_obj: dict | None,
    known_proposals: Mapping[bytes, Proposal],
    now: int,
    policy: NucleusPolicy | None = None,
) -> TallyResult:
    """Zählt Stimmen einer Epoche gegen einen Vorschlag (04-governance.md §3, D112, D145, D274, D275, D276).

    Mitgliedsprüfung, Zusammenfassung, ``CONFLICTING_APPROVAL`` und Zählung laufen je Wurzel
    nach 02 §2.1; eine bestrittene Stimme fällt vor der Zusammenfassung heraus (04 §3.1, 04 §4.4).
    """
    if proposal.scope != epoch.scope:
        raise ValueError("proposal scope does not match epoch scope")
    if (
        genesis_scope(genesis_obj)
        != epoch.scope
    ):
        raise ValueError("genesis_obj does not match epoch scope")
    if proposal.predecessor != epoch.epoch_id:
        return _unevaluable(
            GovernanceFinding.STALE_EPOCH_VOTE,
            proposal.proposal_hash,
            epoch=epoch,
            proposal=proposal,
        )
    if constitution_obj is None or constitution_hash(constitution_obj) != epoch.constitution_hash:
        return _unevaluable(
            GovernanceFinding.CONSTITUTION_UNAVAILABLE,
            epoch.constitution_hash,
            epoch=epoch,
            proposal=proposal,
        )
    if (
        target_constitution_obj is None
        or constitution_hash(target_constitution_obj) != proposal.constitution_hash
    ):
        return _unevaluable(
            GovernanceFinding.PROPOSAL_CONSTITUTION_UNAVAILABLE,
            proposal.constitution_hash,
            epoch=epoch,
            proposal=proposal,
        )
    kind = constitution_governable(constitution_obj)
    if kind is not None:
        return _unevaluable(
            kind,
            epoch.constitution_hash,
            epoch=epoch,
            proposal=proposal,
        )
    weight_mode = genesis_obj.get(6)
    if type(weight_mode) is not int or weight_mode != 0:
        return _unevaluable(
            GovernanceFinding.UNSUPPORTED_WEIGHT_MODE,
            epoch.scope,
            epoch=epoch,
            proposal=proposal,
        )
    idx = genesis_obj.get(5)
    if type(idx) is not int or idx not in _CLASS_BY_INDEX:
        return _unevaluable(
            GovernanceFinding.MALFORMED_THRESHOLD,
            epoch.scope,
            epoch=epoch,
            proposal=proposal,
        )
    klass = threshold_class(constitution_obj, target_constitution_obj, genesis_obj)
    for obj, obj_hash in (
        (constitution_obj, epoch.constitution_hash),
        (target_constitution_obj, proposal.constitution_hash),
    ):
        thresholds = obj.get("thresholds")
        if not isinstance(thresholds, dict) or klass not in thresholds:
            return _unevaluable(
                GovernanceFinding.MALFORMED_THRESHOLD,
                obj_hash,
                epoch=epoch,
                proposal=proposal,
            )
        if not _is_ratio(thresholds[klass]):
            return _unevaluable(
                GovernanceFinding.MALFORMED_THRESHOLD,
                obj_hash,
                epoch=epoch,
                proposal=proposal,
            )
    threshold = applied_threshold(constitution_obj, target_constitution_obj, klass)
    participants = frozenset(constitution_obj["participants"])
    by_cid = classify_all(store, now, policy)
    attr = attribution(store, by_cid, epoch.scope)
    findings: list[Finding] = []
    votes = [c for c in store.all_claims() if is_nuc_name(c, "vote")]
    roots: dict[bytes, bytes] = {}
    disputed: set[bytes] = set()

    def counts_disputed(vote: Claim) -> bool:
        """Bestritten und nicht durch ein Verdikt zugerechnet (04 §3.1, D532, D533)."""
        cid = claim_id(vote)
        if cid not in disputed:
            return False
        return not _reattributed(
            store,
            by_cid,
            vote_cid=cid,
            scope=epoch.scope,
            constitution_obj=constitution_obj,
        )

    for vote in votes:
        if vote.N != epoch.scope:
            continue
        cid = claim_id(vote)
        roots[cid] = vote_root(attr, vote)
        if attr.status(vote) is AttributionStatus.DISPUTED:
            disputed.add(cid)
    candidates: list[Claim] = []
    for vote in votes:
        cid = claim_id(vote)
        on_this = vote.J == (3, proposal.proposal_hash)
        if not on_this:
            continue
        if vote.N != epoch.scope:
            findings.append(Finding(kind=GovernanceFinding.SCOPE_MISMATCH, subject=cid))
            continue
        if roots[cid] not in participants:
            findings.append(Finding(kind=GovernanceFinding.NON_MEMBER_VOTE, subject=cid))
            continue
        if vote.t_exp is not None:
            findings.append(Finding(kind=GovernanceFinding.VOTE_WITH_EXPIRY, subject=cid))
            continue
        obj, v_kind = read_v(vote.v)
        if v_kind is GovernanceFinding.UNPARSABLE_V:
            findings.append(Finding(kind=GovernanceFinding.UNPARSABLE_V, subject=cid))
            continue
        if v_kind is GovernanceFinding.NON_CANONICAL_V:
            findings.append(Finding(kind=GovernanceFinding.NON_CANONICAL_V, subject=cid))
            continue
        choice = None if obj is None else obj.get(0)
        if not _is_known_choice(choice):
            findings.append(
                Finding(kind=GovernanceFinding.UNKNOWN_VOTE_CHOICE, subject=cid)
            )
            continue
        if by_cid[cid].state is not State.ACTIVE:
            continue
        if counts_disputed(vote):
            findings.append(Finding(kind=GovernanceFinding.DISPUTED_VOTE, subject=cid))
            continue
        candidates.append(vote)

    by_root: dict[bytes, list[Claim]] = defaultdict(list)
    for vote in candidates:
        by_root[roots[claim_id(vote)]].append(vote)
    counting: list[Claim] = []
    for group in by_root.values():
        if len({_is_yes_choice(_choice(vote)) for vote in group}) > 1:
            for vote in group:
                findings.append(
                    Finding(kind=GovernanceFinding.AMBIGUOUS_VOTE, subject=claim_id(vote))
                )
        else:
            counting.extend(group)

    excluded: set[bytes] = set()
    for vote in counting:
        if not _is_yes_choice(_choice(vote)):
            continue
        author = roots[claim_id(vote)]
        for other in votes:
            if other.N != epoch.scope:
                continue
            other_cid = claim_id(other)
            if roots[other_cid] != author:
                continue
            if other.t_exp is not None:
                continue
            if by_cid[other_cid].state is not State.ACTIVE:
                continue
            if counts_disputed(other):
                continue
            obj, v_kind = read_v(other.v)
            if v_kind is GovernanceFinding.UNPARSABLE_V:
                findings.append(
                    Finding(kind=GovernanceFinding.UNPARSABLE_V, subject=other_cid)
                )
                continue
            if v_kind is GovernanceFinding.NON_CANONICAL_V:
                findings.append(
                    Finding(kind=GovernanceFinding.NON_CANONICAL_V, subject=other_cid)
                )
                continue
            if not _is_yes_choice(None if obj is None else obj.get(0)):
                continue
            if other.J == (3, proposal.proposal_hash):
                continue
            if other.J[0] == 3 and other.J[1] in known_proposals:
                other_prop = known_proposals[other.J[1]]
                if other_prop.proposal_hash == other.J[1]:
                    if other_prop.predecessor == epoch.epoch_id:
                        findings.append(
                            Finding(
                                kind=GovernanceFinding.CONFLICTING_APPROVAL,
                                subject=claim_id(vote),
                            )
                        )
                        findings.append(
                            Finding(
                                kind=GovernanceFinding.CONFLICTING_APPROVAL,
                                subject=other_cid,
                            )
                        )
                        excluded.add(author)
                    continue
            findings.append(
                Finding(kind=GovernanceFinding.UNKNOWN_PROPOSAL, subject=other_cid)
            )
            excluded.add(author)

    yes_ids: list[bytes] = []
    no_ids: list[bytes] = []
    yes_roots: set[bytes] = set()
    no_roots: set[bytes] = set()
    for vote in counting:
        cid = claim_id(vote)
        if roots[cid] in excluded:
            continue
        if _is_yes_choice(_choice(vote)):
            yes_ids.append(cid)
            yes_roots.add(roots[cid])
        else:
            no_ids.append(cid)
            no_roots.add(roots[cid])
    yes = tuple(sorted(yes_ids))
    no = tuple(sorted(no_ids))
    n = len(participants)
    num, den = threshold
    if reached(len(yes_roots), n, num, den):
        state = TallyState.PASSED
    elif hopeless(len(no_roots), n, num, den):
        state = TallyState.FAILED
    else:
        state = TallyState.PENDING
    return TallyResult(
        state=state,
        yes=yes,
        no=no,
        participants=participants,
        threshold=threshold,
        findings=dedupe_sort(findings),
        epoch_id=epoch.epoch_id,
        proposal_hash=proposal.proposal_hash,
    )
