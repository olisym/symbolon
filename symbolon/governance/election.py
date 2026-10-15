"""Auszählung einer geheimen Wahl (04 §9, D669, D671)."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id
from symbolon.domains import DOM_NUC_BALLOT_LIST, DOM_NUC_ELECTION
from symbolon.governance.findings import Finding, GovernanceFinding, dedupe_sort
from symbolon.governance.objects import Epoch
from symbolon.governance.tally import (
    _has_participation,
    _reattributed,
    constitution_governable,
    read_v,
    resolve_object,
    vote_root,
)
from symbolon.index import classify_all
from symbolon.policy import NucleusPolicy, constitution_hash
from symbolon.predicates import is_nuc_name
from symbolon.trust.attribution import AttributionStatus, attribution
from symbolon.verifier import ClaimStore, State


def _bstr32(value: object) -> bool:
    return isinstance(value, bytes) and len(value) == 32


def _is_uint(value: object) -> bool:
    """Wahlgang: ``uint``. ``bool`` ist keiner (04 §9.2, 04 §9.4)."""
    return type(value) is int and value >= 0


def _bstr_list(value: object) -> bool:
    """Nicht leere, streng aufsteigende Liste von Bytestrings der Länge 32 (04 §9.1)."""
    if not isinstance(value, list) or not value:
        return False
    if not all(_bstr32(item) for item in value):
        return False
    return all(left < right for left, right in zip(value, value[1:]))


def _int_keys(obj: dict, expected: set[int]) -> bool:
    """Schlüssel sind ``int`` ohne ``bool``; ``{True: …}`` ist formwidrig (04 §9.1)."""
    return all(type(key) is int for key in obj) and set(obj) == expected


@dataclass(frozen=True, slots=True)
class Election:
    """Content-adressiertes Wahlobjekt, wie es kam (04 §9.1, D669)."""

    obj: object

    @property
    def election_hash(self) -> bytes:
        """SHA-256(DOM_NUC_ELECTION || cbor(election)) (04 §9.1)."""
        return hashlib.sha256(DOM_NUC_ELECTION + cbor_canon.encode(self.obj)).digest()


@dataclass(frozen=True, slots=True)
class BallotList:
    """Content-adressierte Wahlliste, wie sie kam (04 §9.1, D669)."""

    obj: object

    @property
    def list_hash(self) -> bytes:
        """SHA-256(DOM_NUC_BALLOT_LIST || cbor(ballot_list)) (04 §9.1)."""
        return hashlib.sha256(DOM_NUC_BALLOT_LIST + cbor_canon.encode(self.obj)).digest()


def election_wellformed(election: Election) -> bool:
    """Form einer Wahl, am Objekt allein entscheidbar (04 §9.1).

    Kein Wert von ``obj`` wirft. Schlüssel ausser ``0`` bis ``4``, ``scope`` oder ``epoch`` kein
    Bytestring der Länge 32, ``office`` oder ``label`` kein Text, ``candidates`` keine nicht leere,
    streng aufsteigende Liste von Bytestrings der Länge 32: formwidrig.
    """
    obj = election.obj
    if not isinstance(obj, dict) or not _int_keys(obj, {0, 1, 2, 3, 4}):
        return False
    if not _bstr32(obj[0]) or not _bstr32(obj[1]):
        return False
    if not isinstance(obj[2], str) or not isinstance(obj[4], str):
        return False
    return _bstr_list(obj[3])


def list_wellformed(ballot_list: BallotList) -> bool:
    """Form einer Liste, am Objekt allein entscheidbar (04 §9.1).

    Kein Wert von ``obj`` wirft. ``members`` und ``keys`` verschieden lang ist formwidrig.
    """
    obj = ballot_list.obj
    if not isinstance(obj, dict) or not _int_keys(obj, {0, 1, 2}):
        return False
    if not _bstr32(obj[0]):
        return False
    members, keys = obj[1], obj[2]
    if not _bstr_list(members) or not _bstr_list(keys):
        return False
    return len(members) == len(keys)


class ElectionState(str, Enum):
    """Zustand einer Wahl (04 §9.4)."""

    ELECTED = "ELECTED"
    OPEN = "OPEN"
    UNEVALUABLE = "UNEVALUABLE"


@dataclass(frozen=True, slots=True)
class RoundCount:
    """Stimmen eines Wahlgangs: ``|Y(c, w)|`` je Kandidat, in der Reihenfolge der Kandidaten
    (04 §9.4, D684 Beschluss 2)."""

    round: int
    counts: tuple[tuple[bytes, int], ...]


@dataclass(frozen=True, slots=True)
class ElectionResult:
    """Ergebnis von ``tally_election`` (04 §9.4, D671 Beschluss 4).

    ``current_round`` ist der geltende Wahlgang; bei ``UNEVALUABLE`` ``None``. ``lists`` sind die
    ``list_hash`` der tragenden Listen, aufsteigend. ``elected`` nennt den Gewählten, sonst
    ``None``. ``rounds`` nennt je Wahlgang von 0 bis zum geltenden die Stimmen je Kandidat; bei
    ``UNEVALUABLE`` ist es leer (D684 Beschluss 2).
    """

    state: ElectionState
    elected: bytes | None
    current_round: int | None
    lists: tuple[bytes, ...]
    findings: tuple[Finding, ...]
    election_hash: bytes
    rounds: tuple[RoundCount, ...] = ()


def _ballot_choice(vote: Claim, *, participation: bool = False) -> tuple[bytes, int] | None:
    """Kandidat und Wahlgang, wenn ``v`` kanonisch ist und beide Felder die Form haben (04 §9.4).

    Unter ``participation@1`` ist ``h''`` eine Enthaltung.
    """
    obj, kind = read_v(vote.v)
    if kind is not None or not isinstance(obj, dict):
        return None
    candidate, rnd = obj.get(0), obj.get(1)
    if not _is_uint(rnd):
        return None
    if _bstr32(candidate):
        return candidate, rnd
    if participation and candidate == b"":
        return candidate, rnd
    return None


def _hashes_under_domain(known: Mapping[bytes, object], h: bytes) -> bool:
    """Liegt unter ``h`` ein Objekt, das unter seinem Domänentrenner auf ``h`` hasht (D671
    Beschluss 4)?"""
    obj = known.get(h)
    if isinstance(obj, Election):
        return obj.election_hash == h
    if isinstance(obj, BallotList):
        return obj.list_hash == h
    return resolve_object(known, h) is not None


def tally_election(
    store: ClaimStore,
    *,
    scope: bytes,
    election: Election,
    epoch: Epoch | None,
    constitution_obj: dict | None,
    known_objects: Mapping[bytes, object],
    now: int,
    policy: NucleusPolicy | None = None,
) -> ElectionResult:
    """Zählt eine geheime Wahl aus (04 §9.3, 04 §9.4, D669, D671).

    Die Tabelle „Wann die Auszählung nicht läuft“ gilt in dieser Reihenfolge. Eine bestrittene
    Bestätigung ist keine, es sei denn, ein Verdikt rechnet sie zu (04 §9.3, D671 Beschluss 1);
    sie fällt dann für die Bedingungen 3, 4 und 5 heraus. Eine Liste für ``E`` ist jede
    ``BallotList`` mit Feld ``0`` gleich ``election_hash``, formwidrig oder nicht (D671
    Beschluss 2). Eine Stimme für einen fremden Kandidaten bindet und zählt nicht (D669
    Beschluss 3). Vermerke zu Stimmen stehen für jeden Wahlgang mit Stimmen.
    Unter ``participation@1`` ist ``h''`` eine Enthaltung, ``n`` ist ``|P|`` ohne ``resting``,
    und eine Erklärung nach 04 §2.6 wird nicht gelesen (04 §9.3, 04 §9.4).
    """
    e_hash = election.election_hash

    def stop(kind: GovernanceFinding, subject: bytes) -> ElectionResult:
        return ElectionResult(
            state=ElectionState.UNEVALUABLE,
            elected=None,
            current_round=None,
            lists=(),
            findings=dedupe_sort((Finding(kind=kind, subject=subject),)),
            election_hash=e_hash,
        )

    if not election_wellformed(election):
        return stop(GovernanceFinding.MALFORMED_ELECTION, e_hash)
    raw = election.obj
    if raw[0] != scope:
        raise ValueError("election scope does not match scope")
    if epoch is None or epoch.epoch_id != raw[1]:
        return stop(GovernanceFinding.CONSTITUTION_UNAVAILABLE, raw[1])
    if constitution_obj is None or constitution_hash(constitution_obj) != epoch.constitution_hash:
        return stop(GovernanceFinding.CONSTITUTION_UNAVAILABLE, epoch.constitution_hash)
    kind = constitution_governable(constitution_obj)
    if kind is not None:
        return stop(kind, epoch.constitution_hash)
    irrevocable = constitution_obj.get("irrevocable_predicates", [])
    if "ballot-ack@1" not in irrevocable or "ballot@1" not in irrevocable:
        return stop(GovernanceFinding.BALLOT_REVOCABLE, epoch.constitution_hash)

    participants = frozenset(constitution_obj["participants"])
    participation = _has_participation(constitution_obj)
    resting = (
        frozenset(constitution_obj["resting"])
        if participation and "resting" in constitution_obj
        else frozenset()
    )
    # Unter participation@1 liegt die Liste in ``P \\ resting`` (04 §9.3, 04 §9.4).
    eligible = participants - resting
    candidates = tuple(raw[3])
    candidate_set = set(candidates)
    by_cid = classify_all(store, now, policy)
    attr = attribution(store, by_cid, scope)
    findings: list[Finding] = []

    def counts(claim: Claim) -> bool:
        """Bestätigung: ``N == scope``, ``ACTIVE``, ohne ``t_exp`` (04 §9.3).

        Eine bestrittene Bestätigung zählt nicht, es sei denn, ``_reattributed`` rechnet sie zu
        (D671 Beschluss 1). Sie fällt dann für die Bedingungen 3, 4 und 5 heraus.
        """
        if claim.N != scope or claim.t_exp is not None:
            return False
        classification = by_cid.get(claim_id(claim))
        if classification is None or classification.state is not State.ACTIVE:
            return False
        if attr.status(claim) is AttributionStatus.DISPUTED and not _reattributed(
            store,
            by_cid,
            vote_cid=claim_id(claim),
            scope=scope,
            constitution_obj=constitution_obj,
        ):
            return False
        return True

    def root_of(claim: Claim) -> bytes:
        """Wurzel nach 02 §2.1, bei ``DISPUTED`` die des Geräts (04 §9.3, 04 §3.1)."""
        return vote_root(attr, claim)

    confirmations = [c for c in store.all_claims() if is_nuc_name(c, "ballot-ack") and counts(c)]
    lists_for_e: list[BallotList] = []
    list_hashes: set[bytes] = set()
    for h, obj in known_objects.items():
        if not isinstance(obj, BallotList) or obj.list_hash != h:
            continue
        body = obj.obj
        if isinstance(body, dict) and body.get(0) == e_hash:
            lists_for_e.append(obj)
            list_hashes.add(h)

    def carries(lst: BallotList) -> bool:
        """Die fünf Bedingungen aus 04 §9.3."""
        if not list_wellformed(lst) or lst.obj[0] != e_hash:
            return False
        members, keys = lst.obj[1], lst.obj[2]
        if any(member not in eligible for member in members):
            return False
        acks = [c for c in confirmations if c.J == (3, lst.list_hash)]
        roots = {root_of(c) for c in acks}
        authors = {c.I for c in acks}
        if any(member not in roots for member in members):
            return False
        if any(key not in authors for key in keys):
            return False
        member_set, key_set = set(members), set(keys)
        for ack in confirmations:
            if ack.J[0] != 3 or ack.J[1] == lst.list_hash:
                continue
            target = ack.J[1]
            if target not in list_hashes and _hashes_under_domain(known_objects, target):
                continue
            if root_of(ack) in member_set or ack.I in key_set:
                return False
        return True

    carrying = [lst for lst in lists_for_e if carries(lst)]
    keys_k = {key for lst in carrying for key in lst.obj[2]}
    members_t = {member for lst in carrying for member in lst.obj[1]}

    by_root: dict[bytes, list[Claim]] = defaultdict(list)
    by_author: dict[bytes, list[Claim]] = defaultdict(list)
    for ack in confirmations:
        if ack.J[0] != 3 or ack.J[1] not in list_hashes:
            continue
        by_root[root_of(ack)].append(ack)
        by_author[ack.I].append(ack)
    for group in (*by_root.values(), *by_author.values()):
        if len({ack.J[1] for ack in group}) < 2:
            continue
        for ack in group:
            findings.append(
                Finding(kind=GovernanceFinding.CONFLICTING_LIST_ACK, subject=claim_id(ack))
            )
    for ack in confirmations:
        if ack.J[0] != 3 or ack.J[1] in list_hashes:
            continue
        if not _hashes_under_domain(known_objects, ack.J[1]):
            findings.append(Finding(kind=GovernanceFinding.UNKNOWN_LIST, subject=claim_id(ack)))

    by_key_round: dict[tuple[bytes, int], list[tuple[Claim, bytes]]] = defaultdict(list)
    for vote in store.all_claims():
        if not is_nuc_name(vote, "ballot"):
            continue
        if vote.N != scope or vote.t_exp is not None or vote.J != (3, e_hash):
            continue
        if vote.I not in keys_k:
            continue
        classification = by_cid.get(claim_id(vote))
        if classification is None or classification.state is not State.ACTIVE:
            continue
        parsed = _ballot_choice(vote, participation=participation)
        if parsed is None:
            findings.append(
                Finding(kind=GovernanceFinding.MALFORMED_BALLOT, subject=claim_id(vote))
            )
            continue
        candidate, rnd = parsed
        by_key_round[(vote.I, rnd)].append((vote, candidate))

    gebunden_rounds: dict[int, set[bytes]] = defaultdict(set)
    counted: dict[tuple[int, bytes], set[bytes]] = defaultdict(set)
    abstained: dict[int, set[bytes]] = defaultdict(set)
    for (key, rnd), group in by_key_round.items():
        # Bindet auch für einen fremden Kandidaten; der Schlüssel ist dann nicht frei
        # (04 §9.4, D669 Beschluss 3).
        gebunden_rounds[rnd].add(key)
        named = {cand for _vote, cand in group}
        if len(named) > 1:
            for vote, _cand in group:
                findings.append(
                    Finding(kind=GovernanceFinding.AMBIGUOUS_BALLOT, subject=claim_id(vote))
                )
            continue
        cand = next(iter(named))
        # ``h''`` enthält sich: gebunden, kein Kandidat, verlässt den Nenner (04 §9.4).
        if participation and cand == b"":
            abstained[rnd].add(key)
            continue
        if cand not in candidate_set:
            for vote, _cand in group:
                findings.append(
                    Finding(kind=GovernanceFinding.UNKNOWN_CANDIDATE, subject=claim_id(vote))
                )
            continue
        counted[(rnd, cand)].add(key)

    def patt(rnd: int) -> bool:
        """Wahlgang ``rnd`` steht im Patt (04 §9.4, D668)."""
        gebunden = gebunden_rounds.get(rnd, set())
        if not gebunden:
            return False
        # Wurzeln aus ``P`` ohne Liste bleiben frei, sonst höbe eine neue Liste ein Patt auf
        # (04 §9.4, 04 §9.5, D668 Befund 2).
        frei = len(keys_k - gebunden) + len(eligible - members_t)
        # Unter participation@1 rechnet Patt und „gewählt“ mit ``n(w)`` (04 §9.4).
        n_w = len(eligible) - len(abstained.get(rnd, ()))
        return all(
            2 * (len(counted.get((rnd, cand), ())) + frei) <= n_w
            for cand in candidates
        )

    current = 0
    while current in gebunden_rounds and patt(current):
        current += 1
    n_aktuell = len(eligible) - len(abstained.get(current, ()))
    winners = [
        cand
        for cand in candidates
        if 2 * len(counted.get((current, cand), ())) > n_aktuell
    ]
    elected = winners[0] if len(winners) == 1 else None
    state = ElectionState.ELECTED if elected is not None else ElectionState.OPEN
    # Je Wahlgang bis zum geltenden die Stimmen je Kandidat, in dessen Reihenfolge
    # (04 §9.4, D684 Beschluss 2).
    rounds = tuple(
        RoundCount(
            round=rnd,
            counts=tuple((cand, len(counted.get((rnd, cand), ()))) for cand in candidates),
        )
        for rnd in range(current + 1)
    )
    return ElectionResult(
        state=state,
        elected=elected,
        current_round=current,
        lists=tuple(sorted(lst.list_hash for lst in carrying)),
        findings=dedupe_sort(findings),
        election_hash=e_hash,
        rounds=rounds,
    )
