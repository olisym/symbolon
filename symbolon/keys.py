"""Schlüsselkette: resolve_current_key, resolve_authorized_keys (00 §6.4, D151–D164)."""

from __future__ import annotations

from dataclasses import dataclass

from symbolon.atom import Claim, claim_id
from symbolon.findings import Finding, NucleusFinding, dedupe_sort
from symbolon.genesis import genesis_scope
from symbolon.index import classify_all
from symbolon.policy import NucleusPolicy, constitution_hash as hash_constitution
from symbolon.predicates import is_nuc_name
from symbolon.verifier import ClaimStore, State, _predecessor_known_and_valid

_J_TAG_IDENTITY = 1
_J_TAG_CLAIM_REF = 2
_COUNTING = frozenset({State.ACTIVE, State.EXPIRED})


@dataclass(frozen=True, slots=True)
class KeyResolution:
    """Aufgelöste Schlüssel plus Vermerke (00 §6.4 Schritt 1, D161)."""

    keys: frozenset[bytes]
    findings: tuple[Finding, ...]


def _on_author_chain(earlier: Claim, later: Claim, store: ClaimStore) -> bool:
    """True gdw. ``earlier`` über gültige Vorgänger von ``later`` liegt (01 §6, D462)."""
    target = claim_id(earlier)
    seen: set[bytes] = set()
    current = later
    while True:
        cid = claim_id(current)
        if cid in seen:
            return False
        seen.add(cid)
        ok, pred = _predecessor_known_and_valid(current, store)
        if not ok or pred is None:
            return False
        if claim_id(pred) == target:
            return True
        current = pred


def _earliest_on_chain(
    rotates: list[Claim], store: ClaimStore
) -> Claim | None:
    for candidate in rotates:
        if all(
            other is candidate or _on_author_chain(candidate, other, store)
            for other in rotates
        ):
            return candidate
    return None


def resolve_current_key(
    store: ClaimStore,
    *,
    scope: bytes,
    anchor_keys: frozenset[bytes],
    now: int,
    policy: NucleusPolicy | None = None,
) -> frozenset[bytes]:
    """Köpfe der vollständigen Rotationsketten ab ``anchor_keys`` (00 §6.4 Schritt 2–4).

    ``policy`` wird unverändert an ``classify_all`` gereicht (03 §4, D156).
    """
    by_cid = classify_all(store, now, policy)
    claims = store.all_claims()

    def _head_from(k: bytes) -> bytes | None:
        visited: set[bytes] = set()
        k_cur = k
        while True:
            if k_cur in visited:
                return None
            visited.add(k_cur)
            if any(
                claim.I == k_cur
                and claim_id(claim) in by_cid
                and by_cid[claim_id(claim)].state is State.EQUIVOCATION_FLAGGED
                for claim in claims
            ):
                return None
            complete: list[Claim] = []
            for claim in claims:
                if not is_nuc_name(claim, "rotate-key"):
                    continue
                if claim.I != k_cur or claim.N != scope:
                    continue
                if claim.J[0] != _J_TAG_IDENTITY:
                    continue
                if by_cid[claim_id(claim)].state not in _COUNTING:
                    continue
                rid = claim_id(claim)
                ack_ok = False
                for ack in claims:
                    if not is_nuc_name(ack, "rotate-ack"):
                        continue
                    if ack.J != (_J_TAG_CLAIM_REF, rid):
                        continue
                    if ack.I != claim.J[1]:
                        continue
                    if ack.N != claim.N:
                        continue
                    if by_cid[claim_id(ack)].state not in _COUNTING:
                        continue
                    ack_ok = True
                    break
                if ack_ok:
                    complete.append(claim)
            if not complete:
                return k_cur
            if len(complete) == 1:
                k_cur = complete[0].J[1]
                continue
            earliest = _earliest_on_chain(complete, store)
            if earliest is None:
                return None
            k_cur = earliest.J[1]

    heads: set[bytes] = set()
    for k in anchor_keys:
        head = _head_from(k)
        if head is not None:
            heads.add(head)
    return frozenset(heads)


def resolve_authorized_keys(
    store: ClaimStore,
    *,
    scope: bytes,
    genesis_obj: dict,
    constitution_hash: bytes,
    constitution_obj: dict | None = None,
    now: int,
    policy: NucleusPolicy | None = None,
) -> KeyResolution:
    """Anker aus Genesis und Verfassung, dann Köpfe der Ketten (00 §6.4 Schritt 1, D161)."""
    computed_scope = genesis_scope(genesis_obj)
    if scope != computed_scope:
        raise ValueError("genesis_obj does not match scope")

    if 1 not in genesis_obj:
        raise ValueError("genesis_obj missing or invalid root_keys (key 1)")
    raw_roots = genesis_obj[1]
    if not isinstance(raw_roots, list):
        raise ValueError("genesis_obj missing or invalid root_keys (key 1)")
    for entry in raw_roots:
        if not isinstance(entry, bytes) or len(entry) != 32:
            raise ValueError("genesis_obj missing or invalid root_keys (key 1)")
    root_keys = frozenset(raw_roots)

    if constitution_obj is None:
        keys = resolve_current_key(
            store, scope=scope, anchor_keys=root_keys, now=now, policy=policy
        )
        return KeyResolution(
            keys=keys,
            findings=dedupe_sort(
                [Finding(NucleusFinding.CONSTITUTION_UNAVAILABLE, constitution_hash)]
            ),
        )

    if hash_constitution(constitution_obj) != constitution_hash:
        raise ValueError("constitution_obj does not match constitution_hash")

    if "nucleus_keys" not in constitution_obj:
        keys = resolve_current_key(
            store, scope=scope, anchor_keys=root_keys, now=now, policy=policy
        )
        return KeyResolution(keys=keys, findings=())

    raw = constitution_obj["nucleus_keys"]
    notes: list[Finding] = []
    kept: list[bytes] = []
    if not isinstance(raw, (list, tuple)):
        notes.append(
            Finding(NucleusFinding.MALFORMED_NUCLEUS_KEY, constitution_hash)
        )
    else:
        for entry in raw:
            if isinstance(entry, bytes) and len(entry) == 32:
                kept.append(entry)
            else:
                notes.append(
                    Finding(NucleusFinding.MALFORMED_NUCLEUS_KEY, constitution_hash)
                )
    keys = resolve_current_key(
        store, scope=scope, anchor_keys=frozenset(kept), now=now, policy=policy
    )
    return KeyResolution(keys=keys, findings=dedupe_sort(notes))
