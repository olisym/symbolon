"""Auszählung einer Epoche (04-governance.md §3)."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass, replace
from enum import Enum

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id
from symbolon.genesis import genesis_scope
from symbolon.governance.findings import (
    Finding,
    GovernanceFinding,
    dedupe_sort,
)
from symbolon.governance.objects import (
    Epoch,
    Motion,
    Proposal,
    apply_motions,
    ballot_of,
    motion_list,
    motion_wellformed,
    preconditions,
    protected_fields,
)
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
    """Ergebnis von ``decide`` (04-governance.md §3.3, D106, D109).

    ``current_ballot`` ist der geltende Wahlgang, gerechnet bei einem Vorschlag, dessen Auszählung
    ohne Wahlgang durchkäme; sonst ``None`` (04 §3.2, 04 §4.7, D601 Beschluss 1).

    ``denominator`` ist der Nenner aus 04 §3.2 unter ``participation@1``, sonst ``None``.
    ``abstained`` sind die Wurzeln, deren Stimmen auf den Antrag als Enthaltung zählen (04 §3.2).
    """

    state: TallyState
    yes: tuple[bytes, ...]
    no: tuple[bytes, ...]
    participants: frozenset[bytes] | None
    threshold: tuple[int, int] | None
    findings: tuple[Finding, ...]
    epoch_id: bytes
    proposal_hash: bytes
    current_ballot: int | None = None
    denominator: int | None = None
    abstained: frozenset[bytes] = frozenset()

    @property
    def n(self) -> int | None:
        """Nenner: ``denominator``, wenn gesetzt, sonst ``|participants|`` (04 §3.2)."""
        if self.denominator is not None:
            return self.denominator
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


# Felder, die für die Klasse wie ``participants`` zählen (04 §3.4).
_MEMBERSHIP_FIELDS = frozenset({"participants", "resting", "returned"})


def threshold_class(old_obj: dict, new_obj: dict, genesis_obj: dict) -> str:
    """Klasse aus dem Verfassungsunterschied (04 §3.4, D113).

    ``resting`` und ``returned`` zählen wie ``participants`` (04 §3.4).
    Liest ``genesis_obj[5]`` ungeprüft. Der Aufrufer muss Bindung und Index
    bereits validiert haben — so wie ``decide`` es tut (04 §3.5, D145).
    """
    old_rest = {k: v for k, v in old_obj.items() if k not in _MEMBERSHIP_FIELDS}
    new_rest = {k: v for k, v in new_obj.items() if k not in _MEMBERSHIP_FIELDS}
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


def _is_known_choice(value: object, *, participation: bool = False) -> bool:
    """``0`` und ``1``, unter ``participation@1`` auch ``2`` (04 §2.2, 04 §3.1)."""
    if type(value) is not int:
        return False
    if value in (0, 1):
        return True
    return participation and value == 2


def read_replaces(obj: dict) -> tuple[tuple[bytes, ...], bool]:
    """``v`` Key 1 einer Stimme: die genannten ``claim_id`` und ob der Key formwidrig ist
    (04 §2.2, 04 §3.1, D547 Beschluss 3).

    Ohne Key 1 ``((), False)``; keine Liste oder ein Eintrag kein Bytestring der Länge 32
    ``((), True)``.
    """
    if 1 not in obj:
        return (), False
    names = obj[1]
    if not isinstance(names, list):
        return (), True
    if not all(isinstance(name, bytes) and len(name) == 32 for name in names):
        return (), True
    return tuple(names), False


def maximal_votes(votes: list[Claim]) -> list[Claim]:
    """Die Stimmen ohne die, die eine andere Stimme dieser Liste in ``v`` Key 1 nennt
    (04 §3.1, D547 Beschluss 1 und 2, D548 Beschluss 3).

    Eine Stimme, deren ``v`` nicht lesbar oder deren Key 1 formwidrig ist, nennt nichts.
    """
    named: set[bytes] = set()
    for vote in votes:
        obj, _kind = read_v(vote.v)
        if obj is None:
            continue
        names, _malformed = read_replaces(obj)
        named.update(names)
    return [vote for vote in votes if claim_id(vote) not in named]


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
    *subjects: bytes,
    epoch: Epoch,
    object_hash: bytes,
) -> TallyResult:
    return TallyResult(
        state=TallyState.UNEVALUABLE,
        yes=(),
        no=(),
        participants=None,
        threshold=None,
        findings=dedupe_sort([Finding(kind=kind, subject=subject) for subject in subjects]),
        epoch_id=epoch.epoch_id,
        proposal_hash=object_hash,
    )


def resolve_object(known_proposals: Mapping[bytes, object], h: bytes) -> Proposal | Motion | None:
    """Das Objekt unter ``h``, wenn es unter seinem Domänentrenner auf ``h`` hasht, sonst
    ``None`` (04 §2.5, 04 §4.5)."""
    obj = known_proposals.get(h)
    if isinstance(obj, Proposal) and obj.proposal_hash == h:
        return obj
    if isinstance(obj, Motion) and obj.motion_hash == h:
        return obj
    return None


# Diese Fassung kennt genau diesen Eintrag (04 §1.1, 04 §3.5).
_KNOWN_FEATURES = frozenset({"participation@1"})


def _has_participation(obj: dict) -> bool:
    """Ob die Verfassung ``participation@1`` voraussetzt (04 §1.1)."""
    features = obj.get("required_features")
    return isinstance(features, list) and "participation@1" in features


def _ist_uint(value: object) -> bool:
    """``uint``: ``int`` ab 0, ``bool`` zählt nicht (04 §1.1)."""
    return type(value) is int and value >= 0


def _text_liste_aufsteigend(raw: object) -> bool:
    """Liste von Texten, nicht leer, streng aufsteigend nach UTF-8 (04 §1.1)."""
    if not isinstance(raw, list) or not raw:
        return False
    kodiert: list[bytes] = []
    for eintrag in raw:
        if not isinstance(eintrag, str):
            return False
        try:
            kodiert.append(eintrag.encode("utf-8"))
        except UnicodeEncodeError:
            return False
    return all(links < rechts for links, rechts in zip(kodiert, kodiert[1:]))


def _required_features_finding(obj: dict) -> GovernanceFinding | None:
    """Die beiden Zeilen zu ``required_features`` aus 04 §3.5."""
    if "required_features" not in obj:
        return None
    raw = obj["required_features"]
    if not _text_liste_aufsteigend(raw):
        return GovernanceFinding.MALFORMED_REQUIRED_FEATURES
    if any(eintrag not in _KNOWN_FEATURES for eintrag in raw):
        return GovernanceFinding.UNSUPPORTED_FEATURE
    return None


def _resting_wohlgeformt(raw: object, participants: set[bytes]) -> bool:
    """``resting`` nach 04 §1.1."""
    if not isinstance(raw, list) or not raw:
        return False
    if not all(isinstance(eintrag, bytes) and len(eintrag) == 32 for eintrag in raw):
        return False
    if any(links >= rechts for links, rechts in zip(raw, raw[1:])):
        return False
    return all(eintrag in participants for eintrag in raw)


def _returned_wohlgeformt(raw: object, participants: set[bytes]) -> bool:
    """``returned`` nach 04 §1.1."""
    if not isinstance(raw, dict) or not raw:
        return False
    for key, value in raw.items():
        if not isinstance(key, bytes) or len(key) != 32 or key not in participants:
            return False
        if not _ist_uint(value) or value <= 0:
            return False
    return True


def _resting_returned_finding(obj: dict) -> GovernanceFinding | None:
    """``resting``, ``returned`` und ``rest@1`` aus 04 §3.5."""
    if not _has_participation(obj):
        if "resting" in obj or "returned" in obj:
            return GovernanceFinding.MALFORMED_RESTING
        return None
    participants = set(obj["participants"])
    if "resting" in obj and not _resting_wohlgeformt(obj["resting"], participants):
        return GovernanceFinding.MALFORMED_RESTING
    if "returned" in obj and not _returned_wohlgeformt(obj["returned"], participants):
        return GovernanceFinding.MALFORMED_RESTING
    raw_irr = obj.get("irrevocable_predicates", [])
    if not isinstance(raw_irr, (list, tuple)) or "rest@1" not in raw_irr:
        return GovernanceFinding.REST_REVOCABLE
    return None


def constitution_governable(obj: dict) -> GovernanceFinding | None:
    """Gibt die Vermerksart zurück, wenn ``obj`` keine Auszählung tragen kann (04 §3.5, D200).

    Die Zeilen zu ``required_features`` stehen vor ``participants``. Danach ``resting``,
    ``returned`` und ``rest@1`` (04 §1.1, 04 §3.5). Bekannt ist genau ``participation@1``.
    """
    feature = _required_features_finding(obj)
    if feature is not None:
        return feature
    if "participants" not in obj:
        return GovernanceFinding.PARTICIPANTS_UNDECLARED
    if not participants_wellformed(obj):
        return GovernanceFinding.MALFORMED_PARTICIPANTS
    raw_irr = obj.get("irrevocable_predicates", [])
    if not isinstance(raw_irr, (list, tuple)) or "vote@1" not in raw_irr:
        return GovernanceFinding.VOTE_REVOCABLE
    if "ratify@1" not in raw_irr:
        return GovernanceFinding.RATIFY_REVOCABLE
    return _resting_returned_finding(obj)


def _ruhe_v(claim: Claim) -> tuple[dict | None, tuple[bytes, ...]]:
    """``v`` einer Erklärung, oder ``(None, ())``, wenn Bedingung 3 scheitert (04 §2.6)."""
    obj, kind = read_v(claim.v)
    if kind is not None or obj is None:
        return None, ()
    if not _ist_uint(obj.get(0)):
        return None, ()
    if 1 not in obj:
        return obj, ()
    names, bad = read_replaces(obj)
    if bad:
        return None, ()
    return obj, names


def _ruhe_lage(
    store: ClaimStore,
    *,
    epoch: Epoch,
    participants: frozenset[bytes],
    constitution_obj: dict,
    by_cid: dict[bytes, Classification],
    attr: Attribution,
) -> tuple[frozenset[bytes], dict[bytes, list[Claim]], frozenset[bytes], tuple[Finding, ...]]:
    """``resting``, die wirksamen Erklärungen und wer Unbekanntes nennt (04 §1.1, 04 §2.6)."""
    resting = (
        frozenset(constitution_obj["resting"]) if "resting" in constitution_obj else frozenset()
    )
    returned = constitution_obj.get("returned", {})
    if not isinstance(returned, dict):
        returned = {}
    findings: list[Finding] = []
    rests: dict[bytes, list[Claim]] = defaultdict(list)
    unknown: set[bytes] = set()
    for claim in store.all_claims():
        if not is_nuc_name(claim, "rest") or claim.N != epoch.scope:
            continue
        root = vote_root(attr, claim)
        if root not in participants:
            continue
        cid = claim_id(claim)
        if claim.t_exp is not None:
            findings.append(Finding(kind=GovernanceFinding.REST_WITH_EXPIRY, subject=cid))
            continue
        obj, names = _ruhe_v(claim)
        if obj is None:
            findings.append(Finding(kind=GovernanceFinding.MALFORMED_REST, subject=cid))
            continue
        classification = by_cid.get(cid)
        if classification is None or classification.state is not State.ACTIVE:
            continue
        anfang = returned.get(root, 0)
        if type(anfang) is not int:
            anfang = 0
        if not (anfang <= obj[0] <= epoch.index):
            continue
        rests[root].append(claim)
        if any(store.get(name) is None for name in names):
            unknown.add(root)
    return resting, rests, frozenset(unknown), tuple(findings)


def _nennt_eine(vote: Claim, ids: set[bytes] | frozenset[bytes]) -> bool:
    """Ob Key 1 eine Id aus ``ids`` nennt. Ein formwidriger Key 1 nennt nichts (04 §3.1)."""
    obj, kind = read_v(vote.v)
    if kind is not None or not isinstance(obj, dict):
        return False
    names, bad = read_replaces(obj)
    if bad:
        return False
    return any(name in ids for name in names)


def _genannt(rests: list[Claim]) -> set[bytes]:
    """``claim_id``, die wirksame Erklärungen nennen (04 §2.6, 04 §3.1)."""
    named: set[bytes] = set()
    for rest in rests:
        _obj, names = _ruhe_v(rest)
        named.update(names)
    return named


def _ohne_genannte_enthaltung(votes: list[Claim], abstentions: set[bytes]) -> list[Claim]:
    """Wie ``maximal_votes``; ein Name auf eine Enthaltung bleibt ohne Wirkung (04 §3.1)."""
    named: set[bytes] = set()
    for vote in votes:
        obj, kind = read_v(vote.v)
        if kind is not None or obj is None:
            continue
        names, bad = read_replaces(obj)
        if bad:
            continue
        named.update(name for name in names if name not in abstentions)
    return [vote for vote in votes if claim_id(vote) not in named]


def _zusammenfassen_beteiligung(
    root: bytes,
    group: list[Claim],
    *,
    resting: frozenset[bytes],
    rests: list[Claim],
    findings: list[Finding],
    holding: set[bytes],
    abstained: set[bytes],
    counting: list[Claim],
) -> None:
    """Die drei Regeln unter ``participation@1``, vor der Zusammenfassung (04 §3.1)."""
    rest_ids = {claim_id(rest) for rest in rests}
    offen: list[Claim] = []
    for vote in group:
        if root in resting or _nennt_eine(vote, rest_ids):
            findings.append(Finding(kind=GovernanceFinding.RESTING_VOTE, subject=claim_id(vote)))
        else:
            offen.append(vote)
    if offen:
        holding.add(root)
    if rests and any(claim_id(vote) not in _genannt(rests) for vote in offen):
        for vote in group:
            findings.append(Finding(kind=GovernanceFinding.AMBIGUOUS_REST, subject=claim_id(vote)))
        for rest in rests:
            findings.append(Finding(kind=GovernanceFinding.AMBIGUOUS_REST, subject=claim_id(rest)))
        return
    abstention_ids = {claim_id(vote) for vote in offen if _choice(vote) == 2}
    kept = _ohne_genannte_enthaltung(offen, abstention_ids)
    choices = {_choice(vote) for vote in kept}
    if len(choices) > 1:
        for vote in kept:
            findings.append(Finding(kind=GovernanceFinding.AMBIGUOUS_VOTE, subject=claim_id(vote)))
        return
    if choices == {2}:
        abstained.add(root)
        return
    counting.extend(kept)


def _verlaesst(
    root: bytes,
    *,
    rests: dict[bytes, list[Claim]],
    unknown: frozenset[bytes],
    holding: set[bytes],
    abstained: set[bytes],
    yes_roots: set[bytes],
    no_roots: set[bytes],
) -> bool:
    """Ob die Wurzel den Nenner verlässt, noch ohne die Sperre (04 §3.2)."""
    if root in yes_roots or root in no_roots:
        return False
    if root in abstained:
        return True
    return root in rests and root not in holding and root not in unknown


def _ja_sperrt(
    store: ClaimStore,
    *,
    epoch: Epoch,
    proposal: Proposal | Motion,
    root: bytes,
    by_cid: dict[bytes, Classification],
    attr: Attribution,
    constitution_obj: dict,
    known_proposals: Mapping[bytes, Proposal | Motion],
) -> bool:
    """Aktives Ja auf ein mit dem Antrag unvereinbares oder unbekanntes Objekt (04 §3.2, 04 §4.4)."""
    object_hash = proposal.motion_hash if isinstance(proposal, Motion) else proposal.proposal_hash
    for other in store.all_claims():
        if not is_nuc_name(other, "vote") or other.N != epoch.scope or other.t_exp is not None:
            continue
        if vote_root(attr, other) != root:
            continue
        cid = claim_id(other)
        classification = by_cid.get(cid)
        if classification is None or classification.state is not State.ACTIVE:
            continue
        if attr.status(other) is AttributionStatus.DISPUTED and not _reattributed(
            store,
            by_cid,
            vote_cid=cid,
            scope=epoch.scope,
            constitution_obj=constitution_obj,
        ):
            continue
        obj, kind = read_v(other.v)
        if kind is not None or obj is None or not _is_yes_choice(obj.get(0)):
            continue
        if other.J == (3, object_hash):
            continue
        other_obj = resolve_object(known_proposals, other.J[1]) if other.J[0] == 3 else None
        if other_obj is None or approvals_conflict(proposal, other_obj):
            return True
    return False


def _unbesetzt(epoch: Epoch, ballot: int) -> Proposal:
    """Ein Vorschlag des Wahlgangs, auf den keine Stimme zeigt (04 §4.7)."""
    if ballot > 0:
        return Proposal(
            scope=epoch.scope,
            predecessor=epoch.epoch_id,
            constitution_hash=b"\x00" * 32,
            ballot=ballot,
        )
    return Proposal(
        scope=epoch.scope,
        predecessor=epoch.epoch_id,
        constitution_hash=b"\x00" * 32,
    )


def _ruhe_mehrdeutig(
    store: ClaimStore,
    *,
    epoch: Epoch,
    participants: frozenset[bytes],
    resting: frozenset[bytes],
    rests: dict[bytes, list[Claim]],
    by_cid: dict[bytes, Classification],
    attr: Attribution,
    constitution_obj: dict,
) -> set[tuple[bytes, bytes]]:
    """``(wurzel, hash)``, auf denen Ruhe und Stimme ohne Reihenfolge sind (04 §3.1)."""
    groups: dict[tuple[bytes, bytes], list[Claim]] = defaultdict(list)
    for vote in store.all_claims():
        if not is_nuc_name(vote, "vote") or vote.N != epoch.scope or vote.t_exp is not None:
            continue
        if vote.J[0] != 3:
            continue
        root = vote_root(attr, vote)
        if root not in participants or root in resting or root not in rests:
            continue
        cid = claim_id(vote)
        obj, kind = read_v(vote.v)
        if kind is not None or obj is None or not _is_known_choice(obj.get(0), participation=True):
            continue
        if obj.get(0) == 2 and 1 in obj:
            continue
        classification = by_cid.get(cid)
        if classification is None or classification.state is not State.ACTIVE:
            continue
        if attr.status(vote) is AttributionStatus.DISPUTED and not _reattributed(
            store,
            by_cid,
            vote_cid=cid,
            scope=epoch.scope,
            constitution_obj=constitution_obj,
        ):
            continue
        groups[(root, vote.J[1])].append(vote)
    ambiguous: set[tuple[bytes, bytes]] = set()
    for key, group in groups.items():
        root, _hash = key
        rest_ids = {claim_id(rest) for rest in rests[root]}
        named = _genannt(rests[root])
        offen = [vote for vote in group if not _nennt_eine(vote, rest_ids)]
        if any(claim_id(vote) not in named for vote in offen):
            ambiguous.add(key)
    return ambiguous


def approvals_conflict(own: Proposal | Motion, other: Proposal | Motion) -> bool:
    """Ob zwei Ja derselben Wurzel auf ``own`` und ``other`` unvereinbar sind: die drei Regeln aus
    04 §4.4 (D577 Beschluss 4).

    Ein formwidriger Sachantrag ist mit jedem vereinbar, ebenso ein Objekt mit anderem
    ``predecessor``. Zwei Vorschläge sind unvereinbar, zwei Sachanträge, wenn ihre Vorbedingungen
    sich schneiden, ein Vorschlag und ein Sachantrag, wenn der Sachantrag nicht in ``S`` steht; ein
    formwidriges Feld 3 gilt als leeres ``S``.

    Regel 1 gilt je Wahlgang: zwei Vorschläge sind unvereinbar, wenn ihr Wahlgang gleich ist; ein
    Vorschlag mit formwidrigem Feld 4 ist mit jedem vereinbar (04 §4.4, D600 Beschluss 1 und 4,
    D601 Beschluss 1).
    """
    for obj in (own, other):
        if isinstance(obj, Motion) and not motion_wellformed(obj):
            return False
        if isinstance(obj, Proposal) and ballot_of(obj) is None:
            return False
    if own.predecessor != other.predecessor:
        return False
    if isinstance(own, Proposal) and isinstance(other, Proposal):
        return ballot_of(own) == ballot_of(other)
    if isinstance(own, Motion) and isinstance(other, Motion):
        return bool(preconditions(own) & preconditions(other))
    proposal, motion = (own, other) if isinstance(own, Proposal) else (other, own)
    return motion.motion_hash not in (motion_list(proposal) or ())


def _decide(
    store: ClaimStore,
    *,
    epoch: Epoch,
    proposal: Proposal | Motion,
    genesis_obj: dict,
    constitution_obj: dict | None,
    target_constitution_obj: dict | None,
    known_proposals: Mapping[bytes, Proposal | Motion],
    now: int,
    policy: NucleusPolicy | None = None,
) -> TallyResult:
    """Zählt Stimmen einer Epoche gegen einen Vorschlag oder Sachantrag (04-governance.md §3,
    D112, D145, D274, D275, D276, D567).

    Mitgliedsprüfung, Zusammenfassung, ``CONFLICTING_APPROVAL`` und Zählung laufen je Wurzel
    nach 02 §2.1; eine bestrittene Stimme fällt vor der Zusammenfassung heraus (04 §3.1, 04 §4.4).
    Vor der Zusammenfassung fällt je Wurzel jede Stimme heraus, die eine andere nennt; ein
    formwidriger Key 1 zählt, als fehlte er (04 §3.1, D547, D548 Beschluss 3 und 4).

    Ein Sachantrag hat kein Zielobjekt, seine Form steht vor dem Scope. Berührt er ein Feld aus
    ``protected_fields``, ist seine Klasse die aus ``genesis[5]``, sonst ``ordinary``; eine
    formwidrige Liste endet ``UNEVALUABLE`` nach der Regierbarkeit und vor ``genesis[6]``. Ein
    Vorschlag liest die Liste nicht. Seine Klasse misst den Stand aus der Verfassung der Epoche
    und ``S`` (04 §3.4, 04 §3.5, D646).

    Ohne den Wahlgang aus 04 §3.2; formwidriges Feld 4 ist ``MALFORMED_PROPOSAL`` neben Feld 3
    (04 §2.4, 04 §3.5, D600 Beschluss 1, D601 Beschluss 1).
    """
    is_motion = isinstance(proposal, Motion)
    if is_motion:
        if target_constitution_obj is not None:
            raise ValueError("a motion has no target constitution")
        object_hash = proposal.motion_hash
        if not motion_wellformed(proposal):
            return _unevaluable(
                GovernanceFinding.MALFORMED_MOTION,
                object_hash,
                epoch=epoch,
                object_hash=object_hash,
            )
    else:
        object_hash = proposal.proposal_hash
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
            object_hash,
            epoch=epoch,
            object_hash=object_hash,
        )
    s_hashes: tuple[bytes, ...] = ()
    if not is_motion:
        listed = motion_list(proposal)
        # Feld 3 oder Feld 4 formwidrig (04 §3.5, D600 Beschluss 1).
        if listed is None or ballot_of(proposal) is None:
            return _unevaluable(
                GovernanceFinding.MALFORMED_PROPOSAL,
                object_hash,
                epoch=epoch,
                object_hash=object_hash,
            )
        s_hashes = listed
    if constitution_obj is None or constitution_hash(constitution_obj) != epoch.constitution_hash:
        return _unevaluable(
            GovernanceFinding.CONSTITUTION_UNAVAILABLE,
            epoch.constitution_hash,
            epoch=epoch,
            object_hash=object_hash,
        )
    s_motions: list[Motion] = []
    if not is_motion:
        if (
            target_constitution_obj is None
            or constitution_hash(target_constitution_obj) != proposal.constitution_hash
        ):
            return _unevaluable(
                GovernanceFinding.PROPOSAL_CONSTITUTION_UNAVAILABLE,
                proposal.constitution_hash,
                epoch=epoch,
                object_hash=object_hash,
            )
        s_objects = {h: resolve_object(known_proposals, h) for h in s_hashes}
        unknown = [h for h, obj in s_objects.items() if obj is None]
        if unknown:
            return _unevaluable(
                GovernanceFinding.MOTION_UNAVAILABLE,
                *unknown,
                epoch=epoch,
                object_hash=object_hash,
            )
        if any(isinstance(obj, Proposal) for obj in s_objects.values()):
            return _unevaluable(
                GovernanceFinding.MALFORMED_PROPOSAL,
                object_hash,
                epoch=epoch,
                object_hash=object_hash,
            )
        s_motions = list(s_objects.values())
        malformed = [m.motion_hash for m in s_motions if not motion_wellformed(m)]
        if malformed:
            return _unevaluable(
                GovernanceFinding.MALFORMED_MOTION,
                *malformed,
                epoch=epoch,
                object_hash=object_hash,
            )
        if any(
            m.scope != proposal.scope or m.predecessor != proposal.predecessor
            for m in s_motions
        ):
            return _unevaluable(
                GovernanceFinding.MALFORMED_PROPOSAL,
                object_hash,
                epoch=epoch,
                object_hash=object_hash,
            )
        seen: set[tuple[str, bytes]] = set()
        for m in s_motions:
            pre = preconditions(m)
            if pre & seen:
                return _unevaluable(
                    GovernanceFinding.MALFORMED_PROPOSAL,
                    object_hash,
                    epoch=epoch,
                    object_hash=object_hash,
                )
            seen |= pre
    kind = constitution_governable(constitution_obj)
    if kind is not None:
        return _unevaluable(
            kind,
            epoch.constitution_hash,
            epoch=epoch,
            object_hash=object_hash,
        )
    # Nach der Regierbarkeit, vor genesis[6]; ein Vorschlag liest die Liste nicht
    # (04 §3.5, D646).
    beruehrt = False
    if is_motion:
        geschuetzt = protected_fields(constitution_obj)
        if geschuetzt is None:
            return _unevaluable(
                GovernanceFinding.MALFORMED_PROTECTED_FIELDS,
                epoch.constitution_hash,
                epoch=epoch,
                object_hash=object_hash,
            )
        beruehrt = any(name in geschuetzt for name in proposal.changes)
    weight_mode = genesis_obj.get(6)
    if type(weight_mode) is not int or weight_mode != 0:
        return _unevaluable(
            GovernanceFinding.UNSUPPORTED_WEIGHT_MODE,
            epoch.scope,
            epoch=epoch,
            object_hash=object_hash,
        )
    idx = genesis_obj.get(5)
    if type(idx) is not int or idx not in _CLASS_BY_INDEX:
        return _unevaluable(
            GovernanceFinding.MALFORMED_THRESHOLD,
            epoch.scope,
            epoch=epoch,
            object_hash=object_hash,
        )
    if is_motion:
        klass = _CLASS_BY_INDEX[idx] if beruehrt else "ordinary"
        checked = ((constitution_obj, epoch.constitution_hash),)
        target_obj = constitution_obj
    else:
        stand, _applied = apply_motions(constitution_obj, s_motions)
        klass = threshold_class(stand, target_constitution_obj, genesis_obj)
        checked = (
            (constitution_obj, epoch.constitution_hash),
            (target_constitution_obj, proposal.constitution_hash),
        )
        target_obj = target_constitution_obj
    for obj, obj_hash in checked:
        thresholds = obj.get("thresholds")
        if not isinstance(thresholds, dict) or klass not in thresholds:
            return _unevaluable(
                GovernanceFinding.MALFORMED_THRESHOLD,
                obj_hash,
                epoch=epoch,
                object_hash=object_hash,
            )
        if not _is_ratio(thresholds[klass]):
            return _unevaluable(
                GovernanceFinding.MALFORMED_THRESHOLD,
                obj_hash,
                epoch=epoch,
                object_hash=object_hash,
            )
    threshold = applied_threshold(constitution_obj, target_obj, klass)
    participants = frozenset(constitution_obj["participants"])
    by_cid = classify_all(store, now, policy)
    attr = attribution(store, by_cid, epoch.scope)
    findings: list[Finding] = []
    votes = [c for c in store.all_claims() if is_nuc_name(c, "vote")]
    participation = _has_participation(constitution_obj)
    resting: frozenset[bytes] = frozenset()
    rests: dict[bytes, list[Claim]] = {}
    unknown_rest: frozenset[bytes] = frozenset()
    if participation:
        resting, rests, unknown_rest, rest_findings = _ruhe_lage(
            store,
            epoch=epoch,
            participants=participants,
            constitution_obj=constitution_obj,
            by_cid=by_cid,
            attr=attr,
        )
        findings.extend(rest_findings)
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
        on_this = vote.J == (3, object_hash)
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
        if not _is_known_choice(choice, participation=participation):
            findings.append(
                Finding(kind=GovernanceFinding.UNKNOWN_VOTE_CHOICE, subject=cid)
            )
            continue
        # Enthaltung mit Key 1 zählt nicht (04 §2.2, 04 §3.1 Bedingung 5).
        if participation and choice == 2 and isinstance(obj, dict) and 1 in obj:
            findings.append(
                Finding(kind=GovernanceFinding.ABSTENTION_WITH_REPLACES, subject=cid)
            )
            continue
        _names, malformed = read_replaces(obj)
        if malformed:
            findings.append(Finding(kind=GovernanceFinding.MALFORMED_REPLACES, subject=cid))
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
    abstained_roots: set[bytes] = set()
    holding: set[bytes] = set()
    for root, group in by_root.items():
        if participation:
            _zusammenfassen_beteiligung(
                root,
                group,
                resting=resting,
                rests=rests.get(root, []),
                findings=findings,
                holding=holding,
                abstained=abstained_roots,
                counting=counting,
            )
            continue
        group = maximal_votes(group)
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
            if other.J == (3, object_hash):
                continue
            other_obj = resolve_object(known_proposals, other.J[1]) if other.J[0] == 3 else None
            if other_obj is not None:
                # Die drei Regeln aus 04 §4.4.
                if approvals_conflict(proposal, other_obj):
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
    denominator: int | None = None
    if participation:
        eligible = participants - resting
        leavers: set[bytes] = set()
        for root in eligible:
            if not _verlaesst(
                root,
                rests=rests,
                unknown=unknown_rest,
                holding=holding,
                abstained=abstained_roots,
                yes_roots=yes_roots,
                no_roots=no_roots,
            ):
                continue
            if _ja_sperrt(
                store,
                epoch=epoch,
                proposal=proposal,
                root=root,
                by_cid=by_cid,
                attr=attr,
                constitution_obj=constitution_obj,
                known_proposals=known_proposals,
            ):
                continue
            leavers.add(root)
        denominator = len(eligible - leavers)
        n = denominator
    else:
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
        proposal_hash=object_hash,
        denominator=denominator,
        abstained=frozenset(abstained_roots),
    )


def decide(
    store: ClaimStore,
    *,
    epoch: Epoch,
    proposal: Proposal | Motion,
    genesis_obj: dict,
    constitution_obj: dict | None,
    target_constitution_obj: dict | None,
    known_proposals: Mapping[bytes, Proposal | Motion],
    now: int,
    policy: NucleusPolicy | None = None,
    known_constitutions: Mapping[bytes, dict] | None = None,
) -> TallyResult:
    """Die Auszählung nach ``_decide`` und bei einem Vorschlag der Wahlgang aus 04 §3.2
    (04 §4.7, D600 Beschluss 2, D601 Beschluss 1 und Befund 2).

    Ein Sachantrag zählt mit der Klasse aus ``genesis[5]``, wenn ``changes`` ein Feld aus
    ``protected_fields`` nennt, sonst mit ``ordinary``. Eine formwidrige Liste ist
    ``MALFORMED_PROTECTED_FIELDS`` (04 §3.4, 04 §3.5, D646).

    Kommt ein Vorschlag durch, ist ``current_ballot`` der geltende Wahlgang; ist sein Wahlgang
    ein anderer, bleibt er ``PENDING`` mit ``BALLOT_NOT_CURRENT``. Ohne ``known_constitutions``
    kennt die Rechnung nur das eigene Zielobjekt.
    """
    if known_constitutions is None:
        if isinstance(proposal, Proposal) and target_constitution_obj is not None:
            known_constitutions = {proposal.constitution_hash: target_constitution_obj}
        else:
            known_constitutions = {}
    result = _decide(
        store,
        epoch=epoch,
        proposal=proposal,
        genesis_obj=genesis_obj,
        constitution_obj=constitution_obj,
        target_constitution_obj=target_constitution_obj,
        known_proposals=known_proposals,
        now=now,
        policy=policy,
    )
    if isinstance(proposal, Motion) or result.state is not TallyState.PASSED:
        return result
    current = current_ballot(
        store,
        epoch=epoch,
        genesis_obj=genesis_obj,
        constitution_obj=constitution_obj,
        known_proposals=known_proposals,
        known_constitutions=known_constitutions,
        now=now,
        policy=policy,
    )
    if ballot_of(proposal) == current:
        return replace(result, current_ballot=current)
    return replace(
        result,
        state=TallyState.PENDING,
        findings=dedupe_sort(
            [
                *result.findings,
                Finding(kind=GovernanceFinding.BALLOT_NOT_CURRENT, subject=proposal.proposal_hash),
            ]
        ),
        current_ballot=current,
    )


def _lowest_threshold(constitution_obj: dict) -> tuple[int, int] | None:
    """Die kleinste Schwelle in ``thresholds`` nach Kreuzmultiplikation; ``None``, wenn
    ``thresholds`` keine nicht leere Map ist oder ein Wert formwidrig ist (04 §4.7 Bedingung 3,
    D600 Beschluss 5)."""
    thresholds = constitution_obj.get("thresholds")
    if not isinstance(thresholds, dict) or not thresholds:
        return None
    lowest: tuple[int, int] | None = None
    for value in thresholds.values():
        if not _is_ratio(value):
            return None
        num, den = value
        if lowest is None or num * lowest[1] < lowest[0] * den:
            lowest = (num, den)
    return lowest


def stalemate(
    store: ClaimStore,
    *,
    epoch: Epoch,
    ballot: int,
    genesis_obj: dict,
    constitution_obj: dict | None,
    known_proposals: Mapping[bytes, Proposal | Motion],
    known_constitutions: Mapping[bytes, dict],
    now: int,
    policy: NucleusPolicy | None = None,
) -> bool:
    """Steht der Wahlgang ``ballot`` der Epoche im Patt? Die vier Bedingungen aus 04 §4.7
    (D600 Beschluss 5, D601 Beschluss 1).

    Kann die Auszählung der Epoche selbst nicht laufen, steht kein Wahlgang im Patt. Gebunden
    bindet jede Ja-Stimme, die die Einzelprüfungen aus 04 §3.1 besteht, ohne Zusammenfassung je
    Wurzel und ohne 04 §4.4. Unter ``participation@1`` gilt der Absatz dort (04 §4.7).
    """
    if constitution_obj is None or constitution_hash(constitution_obj) != epoch.constitution_hash:
        return False
    if constitution_governable(constitution_obj) is not None:
        return False
    lowest = _lowest_threshold(constitution_obj)
    if lowest is None:
        return False
    participants = frozenset(constitution_obj["participants"])
    by_cid = classify_all(store, now, policy)
    attr = attribution(store, by_cid, epoch.scope)
    participation = _has_participation(constitution_obj)
    resting: frozenset[bytes] = frozenset()
    rests: dict[bytes, list[Claim]] = {}
    unknown_rest: frozenset[bytes] = frozenset()
    ambiguous: set[tuple[bytes, bytes]] = set()
    rest_ids: dict[bytes, set[bytes]] = {}
    if participation:
        resting, rests, unknown_rest, _rest_findings = _ruhe_lage(
            store,
            epoch=epoch,
            participants=participants,
            constitution_obj=constitution_obj,
            by_cid=by_cid,
            attr=attr,
        )
        ambiguous = _ruhe_mehrdeutig(
            store,
            epoch=epoch,
            participants=participants,
            resting=resting,
            rests=rests,
            by_cid=by_cid,
            attr=attr,
            constitution_obj=constitution_obj,
        )
        rest_ids = {root: {claim_id(rest) for rest in gruppe} for root, gruppe in rests.items()}
    eligible = participants - resting
    bound: dict[bytes, set[bytes]] = {}
    for vote in store.all_claims():
        if not is_nuc_name(vote, "vote") or vote.N != epoch.scope or vote.t_exp is not None:
            continue
        cid = claim_id(vote)
        if by_cid[cid].state is not State.ACTIVE:
            continue
        root = vote_root(attr, vote)
        if root not in participants or root in resting:
            continue
        obj, v_kind = read_v(vote.v)
        if v_kind is not None or obj is None or not _is_yes_choice(obj.get(0)):
            continue
        if attr.status(vote) is AttributionStatus.DISPUTED and not _reattributed(
            store, by_cid, vote_cid=cid, scope=epoch.scope, constitution_obj=constitution_obj
        ):
            continue
        if vote.J[0] != 3:
            continue
        target = resolve_object(known_proposals, vote.J[1])
        if target is None:
            # Bedingung 2: unbekannt heisst möglicherweise zählend (04 §4.7).
            return False
        if (
            isinstance(target, Proposal)
            and target.scope == epoch.scope
            and target.predecessor == epoch.epoch_id
            and ballot_of(target) == ballot
        ):
            # RESTING_VOTE und AMBIGUOUS_REST binden nicht (04 §4.7).
            if participation and (
                (root, target.proposal_hash) in ambiguous
                or _nennt_eine(vote, rest_ids.get(root, frozenset()))
            ):
                continue
            bound.setdefault(root, set()).add(target.proposal_hash)
    # Bedingung 1.
    if not bound:
        return False
    if participation:
        # Wirksame Erklärung: nicht frei, ausser sie nennt Unbekanntes (04 §4.7).
        nicht_frei = {root for root in rests if root in eligible and root not in unknown_rest}
        free_roots = eligible - set(bound) - nicht_frei
        leer = _unbesetzt(epoch, ballot)
        gesperrt = {
            root
            for root in nicht_frei
            if _ja_sperrt(
                store,
                epoch=epoch,
                proposal=leer,
                root=root,
                by_cid=by_cid,
                attr=attr,
                constitution_obj=constitution_obj,
                known_proposals=known_proposals,
            )
        }
        n_neu = len(eligible - (nicht_frei - gesperrt))
    else:
        free_roots = participants - set(bound)
        n_neu = len(participants)
    free = len(free_roots)
    # Bedingung 3: Nenner eines Vorschlags, auf den noch niemand gestimmt hat (04 §4.7).
    num, den = lowest
    if free * den > num * n_neu:
        return False
    # Bedingung 4: jeder Vorschlag des Wahlgangs, der nicht an Feld 3 scheitert.
    for h in sorted(known_proposals):
        proposal = resolve_object(known_proposals, h)
        if not isinstance(proposal, Proposal):
            continue
        if proposal.scope != epoch.scope or proposal.predecessor != epoch.epoch_id:
            continue
        if ballot_of(proposal) != ballot or motion_list(proposal) is None:
            continue
        tally = _decide(
            store,
            epoch=epoch,
            proposal=proposal,
            genesis_obj=genesis_obj,
            constitution_obj=constitution_obj,
            target_constitution_obj=known_constitutions.get(proposal.constitution_hash),
            known_proposals=known_proposals,
            now=now,
            policy=policy,
        )
        num_x, den_x = tally.threshold if tally.threshold is not None else lowest
        only_here = sum(1 for hashes in bound.values() if hashes == {h})
        # Unter participation@1: Nenner von X, F ohne Enthaltungen auf X (04 §4.7).
        if participation and tally.n is not None:
            n_x = tally.n
            free_x = len(free_roots - tally.abstained)
        else:
            n_x = n_neu
            free_x = free
        if (only_here + free_x) * den_x > num_x * n_x:
            return False
    return True


def current_ballot(
    store: ClaimStore,
    *,
    epoch: Epoch,
    genesis_obj: dict,
    constitution_obj: dict | None,
    known_proposals: Mapping[bytes, Proposal | Motion],
    known_constitutions: Mapping[bytes, dict],
    now: int,
    policy: NucleusPolicy | None = None,
) -> int:
    """Der geltende Wahlgang: der kleinste ab ``0``, der nicht im Patt steht (04 §4.7, D600
    Beschluss 5, D601 Beschluss 1)."""
    ballot = 0
    while stalemate(
        store,
        epoch=epoch,
        ballot=ballot,
        genesis_obj=genesis_obj,
        constitution_obj=constitution_obj,
        known_proposals=known_proposals,
        known_constitutions=known_constitutions,
        now=now,
        policy=policy,
    ):
        ballot += 1
    return ballot
