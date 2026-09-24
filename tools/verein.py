#!/usr/bin/env python3
"""Verein als geprüfte Welt (szenario-verein.md)."""

from __future__ import annotations

import sys
from dataclasses import dataclass

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id
from symbolon.governance import (
    Epoch,
    GovernanceFinding,
    Proposal,
    TallyState,
    decide,
)
from symbolon.governance.tally import threshold_class
from symbolon.index import classify_all
from symbolon.keys import resolve_authorized_keys
from symbolon.policy import NucleusPolicy, constitution_hash
from symbolon.profiles import MembershipState, membership, resolve_policy
from symbolon.profiles.credit import SettlementState, settlement
from symbolon.profiles.findings import ProfileFinding
from symbolon.resolve import resolve_state
from symbolon.trust.derive import derive
from symbolon.trust.findings import TrustFinding
from symbolon.verifier import InMemoryStore, State
from tools.example_nucleus import (
    NOW,
    ExampleNucleus,
    _Author,
    _nuc,
    _store,
    build as build_example,
    claim_set,
)

DOC_KASSE = bytes.fromhex(
    "d54207da194977dcf46adbfec2bc2e75b52d5a8a42184fedfdc00024f0e3e8da"
)
DOC_CONSTITUTION_HASH_3 = bytes.fromhex(
    "1675cd589aabf17567cadbf3bf5b5742dfbd9f089aa8e01726908a20755016fb"
)
DOC_PROPOSAL_3 = bytes.fromhex(
    "6747ee5cfa15f66ddecaadc340ea304ea96a171c751505442b70093df0572b14"
)
DOC_EPOCH_ID_3 = bytes.fromhex(
    "c68caa1b9fb24a2958f2ead77a4c85088e5e69d90bddc14f7b22fefd865c4887"
)
DOC_CONSTITUTION_HASH_4 = bytes.fromhex(
    "a3533705454f0fafc65400a4c43b515a2dac659d0345a345f34d18fa7f4b7d47"
)
DOC_PROPOSAL_4 = bytes.fromhex(
    "c22fe60ed5336899b18cef8f9f5fc327b4124fad86431893e3231629ad2be446"
)
BEITRAG = "24 Euro im Jahr, fällig im Januar, an die Kasse"
EUR_CENT = bytes.fromhex("4555522d43656e74")

# Spitzen von claim_set: Anna 6, Bruno 4, Chris 2, Dora 1 (example-nucleus.md §7).
_T_ANNA = 7
_T_BRUNO = 5
_T_CHRIS = 3
_T_DORA = 2


def _policy(
    ex: ExampleNucleus,
    constitution_h: bytes,
    obj: dict,
    *,
    scope: bytes | None = None,
    genesis: dict | None = None,
) -> NucleusPolicy:
    resolved = resolve_policy(
        scope=ex.N_gov if scope is None else scope,
        genesis_obj=ex.genesis_gov if genesis is None else genesis,
        constitution_hash=constitution_h,
        constitution_obj=obj,
    )
    if resolved.findings != ():
        raise AssertionError(f"resolve_policy findings: {resolved.findings!r}")
    return resolved.policy


def _vote(identity: _Author, proposal: Proposal, choice: int, *, t: int, scope: bytes) -> Claim:
    return identity.claim(
        p=_nuc(scope, "vote"),
        J=(3, proposal.proposal_hash),
        t=t,
        N=scope,
        v=cbor_canon.encode({0: choice}),
    )


def _accept(identity: _Author, scope: bytes, constitution_h: bytes, *, t: int) -> Claim:
    return identity.claim(
        p=_nuc(scope, "accept-rules"),
        J=(3, constitution_h),
        t=t,
        N=scope,
    )


@dataclass(frozen=True, slots=True)
class Verein:
    """Beispielnukleus plus Satzung, Vorschläge und Kasse (szenario-verein §2)."""

    ex: ExampleNucleus
    anna: _Author
    bruno: _Author
    chris: _Author
    dora: _Author
    kasse: _Author
    base: dict[str, Claim]
    constitution_3: dict
    constitution_4: dict
    constitution_hash_3: bytes
    constitution_hash_4: bytes
    proposal_3: Proposal
    proposal_4: Proposal
    epoch_3: Epoch


def build() -> Verein:
    """Baut den Verein auf build() und claim_set() (szenario-verein §1)."""
    ex = build_example()
    cs = claim_set(ex)
    kasse = _Author(bytes([0x15] * 32))
    if kasse.pub != DOC_KASSE:
        raise AssertionError(
            f"KASSE: got {kasse.pub.hex()}, expected {DOC_KASSE.hex()}"
        )
    constitution_3 = dict(ex.constitution_2)
    constitution_3["beitrag"] = BEITRAG
    constitution_4 = dict(constitution_3)
    constitution_4["participants"] = [
        key for key in ex.constitution_2["participants"] if key != ex.bruno.pub
    ]
    hash_3 = constitution_hash(constitution_3)
    if hash_3 != DOC_CONSTITUTION_HASH_3:
        raise AssertionError(
            f"CONSTITUTION_HASH_3: got {hash_3.hex()}, "
            f"expected {DOC_CONSTITUTION_HASH_3.hex()}"
        )
    hash_4 = constitution_hash(constitution_4)
    if hash_4 != DOC_CONSTITUTION_HASH_4:
        raise AssertionError(
            f"CONSTITUTION_HASH_4: got {hash_4.hex()}, "
            f"expected {DOC_CONSTITUTION_HASH_4.hex()}"
        )
    proposal_3 = Proposal(
        scope=ex.N_gov,
        predecessor=ex.epoch_2.epoch_id,
        constitution_hash=hash_3,
    )
    epoch_3 = Epoch(scope=ex.N_gov, index=3, constitution_hash=hash_3)
    if epoch_3.epoch_id != DOC_EPOCH_ID_3:
        raise AssertionError(
            f"EPOCH_ID_3: got {epoch_3.epoch_id.hex()}, expected {DOC_EPOCH_ID_3.hex()}"
        )
    if proposal_3.proposal_hash != DOC_PROPOSAL_3:
        raise AssertionError(
            f"PROPOSAL_3: got {proposal_3.proposal_hash.hex()}, "
            f"expected {DOC_PROPOSAL_3.hex()}"
        )
    proposal_4 = Proposal(
        scope=ex.N_gov,
        predecessor=epoch_3.epoch_id,
        constitution_hash=hash_4,
    )
    if proposal_4.proposal_hash != DOC_PROPOSAL_4:
        raise AssertionError(
            f"PROPOSAL_4: got {proposal_4.proposal_hash.hex()}, "
            f"expected {DOC_PROPOSAL_4.hex()}"
        )
    return Verein(
        ex=ex,
        anna=cs.anna,
        bruno=cs.bruno,
        chris=cs.chris,
        dora=cs.dora,
        kasse=kasse,
        base=cs.claims,
        constitution_3=constitution_3,
        constitution_4=constitution_4,
        constitution_hash_3=hash_3,
        constitution_hash_4=hash_4,
        proposal_3=proposal_3,
        proposal_4=proposal_4,
        epoch_3=epoch_3,
    )


def _known_constitutions(w: Verein) -> dict[bytes, dict]:
    return {
        w.ex.constitution_hash_gov: w.ex.constitution_gov,
        w.ex.constitution_hash_2: w.ex.constitution_2,
        w.constitution_hash_3: w.constitution_3,
        w.constitution_hash_4: w.constitution_4,
    }


def _known_proposals(w: Verein) -> dict[bytes, Proposal]:
    return {
        w.ex.proposal.proposal_hash: w.ex.proposal,
        w.proposal_3.proposal_hash: w.proposal_3,
        w.proposal_4.proposal_hash: w.proposal_4,
    }


def _decide(w: Verein, store: InMemoryStore, epoch: Epoch, proposal: Proposal, current: dict, target: dict):
    return decide(
        store,
        epoch=epoch,
        proposal=proposal,
        genesis_obj=w.ex.genesis_gov,
        constitution_obj=current,
        target_constitution_obj=target,
        known_proposals=_known_proposals(w),
        now=NOW,
        policy=_policy(w.ex, epoch.constitution_hash, current),
    )


def _resolve(w: Verein, store: InMemoryStore):
    return resolve_state(
        store,
        scope=w.ex.N_gov,
        genesis_obj=w.ex.genesis_gov,
        known_constitutions=_known_constitutions(w),
        known_proposals=_known_proposals(w),
        now=NOW,
    )


def _member(w: Verein, store: InMemoryStore, subject: bytes, constitution_h: bytes, obj: dict):
    policy = _policy(w.ex, constitution_h, obj)
    resolved = resolve_authorized_keys(
        store,
        scope=w.ex.N_gov,
        genesis_obj=w.ex.genesis_gov,
        constitution_hash=constitution_h,
        constitution_obj=obj,
        now=NOW,
        policy=policy,
    )
    return membership(
        store,
        subject=subject,
        scope=w.ex.N_gov,
        constitution_hash=constitution_h,
        now=NOW,
        authorized_keys=resolved.keys,
        constitution_obj=obj,
        policy=policy,
    )


def _fork_bruno(w: Verein) -> tuple[Claim, Claim]:
    """Nein per gabeln, Ja per signieren, dasselbe h_prev (szenario-verein §5.2, D129)."""
    nein = w.bruno._autor.gabeln(
        p=_nuc(w.ex.N_gov, "vote"),
        J=(3, w.proposal_3.proposal_hash),
        t=_T_BRUNO,
        v=cbor_canon.encode({0: 0}),
        N=w.ex.N_gov,
    )
    ja = w.bruno.claim(
        p=_nuc(w.ex.N_gov, "vote"),
        J=(3, w.proposal_3.proposal_hash),
        t=_T_BRUNO,
        N=w.ex.N_gov,
        v=cbor_canon.encode({0: 1}),
    )
    if nein.h_prev != ja.h_prev:
        raise AssertionError("fork branches do not share h_prev")
    return nein, ja


def _yes_anna_chris(w: Verein) -> tuple[Claim, Claim]:
    anna = _vote(w.anna, w.proposal_3, 1, t=_T_ANNA, scope=w.ex.N_gov)
    chris = _vote(w.chris, w.proposal_3, 1, t=_T_CHRIS, scope=w.ex.N_gov)
    return anna, chris


def _ratify(identity: _Author, proposal: Proposal, witnesses: list[Claim], *, t: int, scope: bytes) -> Claim:
    return identity.claim(
        p=_nuc(scope, "ratify"),
        J=(3, proposal.proposal_hash),
        t=t,
        N=scope,
        v=cbor_canon.encode({0: [claim_id(c) for c in witnesses]}),
    )


def check_anna_overcommit(w: Verein) -> None:
    """Bürgschaft n=1 von ANNA: OVERCOMMITTED_AUTHOR, keine Kante (szenario-verein §3)."""
    extra = w.anna.vouch(w.dora, n=1, scope=w.ex.N_res, t=_T_ANNA, t_exp=NOW + 1000000)
    derivation = derive(
        _store(*w.base.values(), extra),
        anchors=frozenset({w.ex.bruno.pub, w.ex.anna.pub}),
        scope=w.ex.N_res,
        now=NOW,
        params=w.ex.params,
    )
    subjects = {
        f.subject
        for f in derivation.findings
        if f.kind is TrustFinding.OVERCOMMITTED_AUTHOR
    }
    if w.anna.pub not in subjects:
        raise AssertionError(f"OVERCOMMITTED_AUTHOR subjects: {subjects!r}")
    if any(edge.author == w.anna.pub for edge in derivation.bfs.edges):
        raise AssertionError("an edge with author ANNA remained")


def check_chris_vouch_dora(w: Verein) -> None:
    """V1: DORA Distanz 2 Kapazität 25, Kante CHRIS→DORA Kapazität 25 (szenario-verein §3)."""
    vouch = w.chris.vouch(w.dora, n=50, scope=w.ex.N_res, t=_T_CHRIS, t_exp=NOW + 1000000)
    derivation = derive(
        _store(*w.base.values(), vouch),
        anchors=frozenset({w.ex.bruno.pub, w.ex.anna.pub}),
        scope=w.ex.N_res,
        now=NOW,
        params=w.ex.params,
    )
    distance = derivation.bfs.distance.get(w.dora.pub)
    capacity = derivation.bfs.node_capacity.get(w.dora.pub)
    if distance != 2 or capacity != 25:
        raise AssertionError(f"DORA d={distance} C={capacity}, expected d=2 C=25")
    onward = next(
        (edge for edge in derivation.bfs.edges if edge.author == w.chris.pub and edge.subject == w.dora.pub),
        None,
    )
    if onward is None or onward.cap != 25:
        raise AssertionError(f"CHRIS→DORA cap: {onward}")


def check_membership_constitution_2(w: Verein) -> None:
    """Vor V8–V10 GRANT_ONLY, nach V7–V10 alle vier MEMBER (szenario-verein §3)."""
    store = _store(*w.base.values())
    for subject in (w.anna.pub, w.bruno.pub, w.chris.pub):
        result = _member(w, store, subject, w.ex.constitution_hash_2, w.ex.constitution_2)
        if result.state is not MembershipState.GRANT_ONLY:
            raise AssertionError(f"before V8–V10 {subject.hex()[:8]}: {result.state}")
    store.add(_accept(w.anna, w.ex.N_gov, w.ex.constitution_hash_2, t=_T_ANNA))
    store.add(_accept(w.bruno, w.ex.N_gov, w.ex.constitution_hash_2, t=_T_BRUNO))
    store.add(_accept(w.chris, w.ex.N_gov, w.ex.constitution_hash_2, t=_T_CHRIS))
    for subject in (w.anna.pub, w.bruno.pub, w.chris.pub, w.dora.pub):
        result = _member(w, store, subject, w.ex.constitution_hash_2, w.ex.constitution_2)
        if result.state is not MembershipState.MEMBER:
            raise AssertionError(f"after V7–V10 {subject.hex()[:8]}: {result.state}")


def check_amendment_class(w: Verein) -> None:
    """threshold_class von constitution_2 nach constitution_3 ist amendment (szenario-verein §4)."""
    klass = threshold_class(w.ex.constitution_2, w.constitution_3, w.ex.genesis_gov)
    if klass != "amendment":
        raise AssertionError(f"threshold_class: {klass!r}")


def _tally_row(w: Verein, choices: list[tuple[_Author, int, int]]) -> TallyState:
    votes = [
        _vote(identity, w.proposal_3, choice, t=t, scope=w.ex.N_gov)
        for identity, choice, t in choices
    ]
    return _decide(
        w,
        _store(*w.base.values(), *votes),
        w.ex.epoch_2,
        w.proposal_3,
        w.ex.constitution_2,
        w.constitution_3,
    ).state


def check_amendment_table(w: Verein) -> None:
    """Fünf Zeilen der Auszählung gegen Epoche 2 (szenario-verein §4)."""
    rows: list[tuple[Verein, list[tuple[_Author, int, int]], TallyState]] = [
        (w, [(w.anna, 1, _T_ANNA), (w.chris, 1, _T_CHRIS)], TallyState.PENDING),
    ]
    fresh = [build() for _ in range(4)]
    specs: list[tuple[list[tuple[str, int]], TallyState]] = [
        ([("anna", 1), ("chris", 1), ("bruno", 0)], TallyState.PENDING),
        ([("anna", 1), ("chris", 1), ("bruno", 0), ("dora", 0)], TallyState.FAILED),
        ([("anna", 1), ("chris", 1), ("dora", 1)], TallyState.PASSED),
        ([("anna", 1), ("chris", 1), ("dora", 1), ("bruno", 0)], TallyState.PASSED),
    ]
    times = {"anna": _T_ANNA, "bruno": _T_BRUNO, "chris": _T_CHRIS, "dora": _T_DORA}
    for world, (named, expected) in zip(fresh, specs, strict=True):
        authors = {
            "anna": world.anna,
            "bruno": world.bruno,
            "chris": world.chris,
            "dora": world.dora,
        }
        choices = [(authors[name], choice, times[name]) for name, choice in named]
        rows.append((world, choices, expected))
    for world, choices, expected in rows:
        state = _tally_row(world, choices)
        if state is not expected:
            raise AssertionError(f"tally {choices}: {state}, expected {expected}")


def check_epoch_3(w: Verein) -> None:
    """Drei Ja und ein ratify@1 erreichen Epoche 3; danach alle MEMBER (szenario-verein §4)."""
    anna = _vote(w.anna, w.proposal_3, 1, t=_T_ANNA, scope=w.ex.N_gov)
    chris = _vote(w.chris, w.proposal_3, 1, t=_T_CHRIS, scope=w.ex.N_gov)
    dora = _vote(w.dora, w.proposal_3, 1, t=_T_DORA, scope=w.ex.N_gov)
    ratify = _ratify(w.anna, w.proposal_3, [anna, chris, dora], t=_T_ANNA + 1, scope=w.ex.N_gov)
    store = _store(*w.base.values(), anna, chris, dora, ratify)
    state = _resolve(w, store)
    if state.epoch != w.epoch_3:
        raise AssertionError(f"resolved epoch: {state.epoch!r}")
    store.add(_accept(w.anna, w.ex.N_gov, w.constitution_hash_3, t=_T_ANNA + 2))
    store.add(_accept(w.bruno, w.ex.N_gov, w.constitution_hash_3, t=_T_BRUNO))
    store.add(_accept(w.chris, w.ex.N_gov, w.constitution_hash_3, t=_T_CHRIS + 1))
    store.add(_accept(w.dora, w.ex.N_gov, w.constitution_hash_3, t=_T_DORA + 1))
    for subject in (w.anna.pub, w.bruno.pub, w.chris.pub, w.dora.pub):
        result = _member(w, store, subject, w.constitution_hash_3, w.constitution_3)
        if result.state is not MembershipState.MEMBER:
            raise AssertionError(f"constitution_3 {subject.hex()[:8]}: {result.state}")


def check_ambiguous_sequence(w: Verein) -> None:
    """Bruno Ja dann Nein: beide AMBIGUOUS_VOTE, Auszählung PENDING (szenario-verein §5.1)."""
    anna, chris = _yes_anna_chris(w)
    ja = _vote(w.bruno, w.proposal_3, 1, t=_T_BRUNO, scope=w.ex.N_gov)
    nein = _vote(w.bruno, w.proposal_3, 0, t=_T_BRUNO + 1, scope=w.ex.N_gov)
    tally = _decide(
        w,
        _store(*w.base.values(), anna, chris, ja, nein),
        w.ex.epoch_2,
        w.proposal_3,
        w.ex.constitution_2,
        w.constitution_3,
    )
    flagged = {
        f.subject for f in tally.findings if f.kind is GovernanceFinding.AMBIGUOUS_VOTE
    }
    if flagged != {claim_id(ja), claim_id(nein)}:
        raise AssertionError(f"AMBIGUOUS_VOTE subjects: {flagged!r}")
    if tally.state is not TallyState.PENDING:
        raise AssertionError(f"sequential tally: {tally.state}")


def check_anna_view(w: Verein) -> None:
    """Annas Rechner: drei Ja PASSED, ratify@1 erreicht Epoche 3 (szenario-verein §5.2)."""
    anna, chris = _yes_anna_chris(w)
    _nein, ja = _fork_bruno(w)
    ratify = _ratify(w.anna, w.proposal_3, [anna, chris, ja], t=_T_ANNA + 1, scope=w.ex.N_gov)
    store = _store(*w.base.values(), anna, chris, ja, ratify)
    tally = _decide(w, store, w.ex.epoch_2, w.proposal_3, w.ex.constitution_2, w.constitution_3)
    if tally.state is not TallyState.PASSED:
        raise AssertionError(f"Anna tally: {tally.state}")
    state = _resolve(w, store)
    if state.epoch != w.epoch_3:
        raise AssertionError(f"Anna epoch: {state.epoch!r}")


def check_chris_view(w: Verein) -> None:
    """Chris ohne Ja-Zweig: PENDING, Epoche 2, UNKNOWN_WITNESS_VOTE (szenario-verein §5.2)."""
    anna, chris = _yes_anna_chris(w)
    nein, ja = _fork_bruno(w)
    ratify = _ratify(w.anna, w.proposal_3, [anna, chris, ja], t=_T_ANNA + 1, scope=w.ex.N_gov)
    store = _store(*w.base.values(), anna, chris, nein, ratify)
    tally = _decide(w, store, w.ex.epoch_2, w.proposal_3, w.ex.constitution_2, w.constitution_3)
    if tally.state is not TallyState.PENDING:
        raise AssertionError(f"Chris tally: {tally.state}")
    state = _resolve(w, store)
    if state.epoch != w.ex.epoch_2:
        raise AssertionError(f"Chris epoch: {state.epoch!r}")
    expected = (GovernanceFinding.UNKNOWN_WITNESS_VOTE, claim_id(ja))
    if not any((f.kind, f.subject) == expected for f in state.epoch_findings):
        raise AssertionError(f"Chris findings: {state.epoch_findings!r}")


def check_exchange(w: Verein) -> None:
    """Nach dem Austausch: geflaggt, PENDING, Epoche 2, UNSUPPORTED_RATIFICATION (szenario-verein §5.2, D469)."""
    anna, chris = _yes_anna_chris(w)
    nein, ja = _fork_bruno(w)
    ratify = _ratify(w.anna, w.proposal_3, [anna, chris, ja], t=_T_ANNA + 1, scope=w.ex.N_gov)
    store = _store(*w.base.values(), anna, chris, nein, ja, ratify)
    policy = _policy(w.ex, w.ex.constitution_hash_2, w.ex.constitution_2)
    classified = classify_all(store, NOW, policy)
    for claim in (nein, ja):
        if classified[claim_id(claim)].state is not State.EQUIVOCATION_FLAGGED:
            raise AssertionError(f"{claim_id(claim).hex()} is not EQUIVOCATION_FLAGGED")
    tally = _decide(w, store, w.ex.epoch_2, w.proposal_3, w.ex.constitution_2, w.constitution_3)
    if tally.state is not TallyState.PENDING:
        raise AssertionError(f"exchange tally: {tally.state}")
    fork_ids = {claim_id(nein), claim_id(ja)}
    leaked = [f for f in tally.findings if f.subject in fork_ids]
    if leaked:
        raise AssertionError(f"tally names a fork claim: {leaked!r}")
    state = _resolve(w, store)
    if state.epoch != w.ex.epoch_2:
        raise AssertionError(f"exchange epoch: {state.epoch!r}")
    expected = (GovernanceFinding.UNSUPPORTED_RATIFICATION, claim_id(ratify))
    if not any((f.kind, f.subject) == expected for f in state.epoch_findings):
        raise AssertionError(f"exchange findings: {state.epoch_findings!r}")


def check_dora_returns(w: Verein) -> None:
    """Doras Ja und ein zweites ratify@1 erreichen Epoche 3 (szenario-verein §5.2)."""
    anna, chris = _yes_anna_chris(w)
    nein, ja = _fork_bruno(w)
    first = _ratify(w.anna, w.proposal_3, [anna, chris, ja], t=_T_ANNA + 1, scope=w.ex.N_gov)
    dora = _vote(w.dora, w.proposal_3, 1, t=_T_DORA, scope=w.ex.N_gov)
    second = _ratify(w.anna, w.proposal_3, [anna, chris, dora], t=_T_ANNA + 2, scope=w.ex.N_gov)
    store = _store(*w.base.values(), anna, chris, nein, ja, first, dora, second)
    state = _resolve(w, store)
    if state.epoch != w.epoch_3:
        raise AssertionError(f"Dora return epoch: {state.epoch!r}")


def check_flagged_trust(w: Verein) -> None:
    """Keine Kante von BRUNO; CHRIS d=1, DORA d=2, BRUNO d=0 (szenario-verein §5.3, 02 §8)."""
    anna, chris = _yes_anna_chris(w)
    nein, ja = _fork_bruno(w)
    vouch = w.chris.vouch(
        w.dora, n=50, scope=w.ex.N_res, t=_T_CHRIS + 1, t_exp=NOW + 1000000
    )
    derivation = derive(
        _store(*w.base.values(), anna, chris, nein, ja, vouch),
        anchors=frozenset({w.ex.bruno.pub, w.ex.anna.pub}),
        scope=w.ex.N_res,
        now=NOW,
        params=w.ex.params,
    )
    if any(edge.author == w.bruno.pub for edge in derivation.bfs.edges):
        raise AssertionError("an edge with author BRUNO remained")
    distance = derivation.bfs.distance
    if distance.get(w.chris.pub) != 1 or distance.get(w.dora.pub) != 2 or distance.get(w.bruno.pub) != 0:
        raise AssertionError(
            f"distances CHRIS={distance.get(w.chris.pub)} "
            f"DORA={distance.get(w.dora.pub)} BRUNO={distance.get(w.bruno.pub)}"
        )


def check_exclusion(w: Verein) -> None:
    """Klasse membership; drei Ja und Brunos Nein sind PASSED (szenario-verein §5.3)."""
    klass = threshold_class(w.constitution_3, w.constitution_4, w.ex.genesis_gov)
    if klass != "membership":
        raise AssertionError(f"exclusion class: {klass!r}")
    votes = [
        _vote(w.anna, w.proposal_4, 1, t=_T_ANNA, scope=w.ex.N_gov),
        _vote(w.chris, w.proposal_4, 1, t=_T_CHRIS, scope=w.ex.N_gov),
        _vote(w.dora, w.proposal_4, 1, t=_T_DORA, scope=w.ex.N_gov),
        _vote(w.bruno, w.proposal_4, 0, t=_T_BRUNO, scope=w.ex.N_gov),
    ]
    tally = _decide(
        w,
        _store(*w.base.values(), *votes),
        w.epoch_3,
        w.proposal_4,
        w.constitution_3,
        w.constitution_4,
    )
    if tally.state is not TallyState.PASSED:
        raise AssertionError(f"exclusion tally: {tally.state}")


def _res_policy(w: Verein) -> NucleusPolicy:
    return _policy(
        w.ex,
        w.ex.constitution_hash_res,
        w.ex.constitution_res,
        scope=w.ex.N_res,
        genesis=w.ex.genesis_res,
    )


def _obligation(w: Verein) -> Claim:
    return w.dora.claim(
        p=_nuc(w.ex.N_res, "obligation"),
        J=(1, w.kasse.pub),
        t=_T_DORA,
        N=w.ex.N_res,
        v=cbor_canon.encode({0: 2400, 1: EUR_CENT}),
    )


def check_settlement(w: Verein) -> None:
    """V20 OPEN, nach V21 SETTLED (szenario-verein §6, 03 §3.3.2)."""
    obligation = _obligation(w)
    policy = _res_policy(w)
    before = _store(*w.base.values(), obligation)
    open_result = settlement(before, obligation=obligation, scope=w.ex.N_res, now=NOW, policy=policy)
    if open_result.state is not SettlementState.OPEN:
        raise AssertionError(f"before V21: {open_result.state}")
    receipt = w.kasse.claim(
        p=_nuc(w.ex.N_res, "receipt"),
        J=(2, claim_id(obligation)),
        t=1,
        N=w.ex.N_res,
    )
    before.add(receipt)
    settled = settlement(before, obligation=obligation, scope=w.ex.N_res, now=NOW, policy=policy)
    if settled.state is not SettlementState.SETTLED:
        raise AssertionError(f"after V21: {settled.state}")


def check_partial_receipt(w: Verein) -> None:
    """Quittung v={0: 1200}: OPEN und PARTIAL_RECEIPT_UNSUPPORTED (szenario-verein §6)."""
    obligation = _obligation(w)
    receipt = w.kasse.claim(
        p=_nuc(w.ex.N_res, "receipt"),
        J=(2, claim_id(obligation)),
        t=1,
        N=w.ex.N_res,
        v=cbor_canon.encode({0: 1200}),
    )
    result = settlement(
        _store(*w.base.values(), obligation, receipt),
        obligation=obligation,
        scope=w.ex.N_res,
        now=NOW,
        policy=_res_policy(w),
    )
    if result.state is not SettlementState.OPEN:
        raise AssertionError(f"partial receipt state: {result.state}")
    if not any(f.kind is ProfileFinding.PARTIAL_RECEIPT_UNSUPPORTED for f in result.findings):
        raise AssertionError(f"partial receipt findings: {result.findings!r}")


def verify_all() -> None:
    """Ruft die fünfzehn Prüfungen aus szenario-verein.md."""
    check_anna_overcommit(build())
    check_chris_vouch_dora(build())
    check_membership_constitution_2(build())
    check_amendment_class(build())
    check_amendment_table(build())
    check_epoch_3(build())
    check_ambiguous_sequence(build())
    check_anna_view(build())
    check_chris_view(build())
    check_exchange(build())
    check_dora_returns(build())
    check_flagged_trust(build())
    check_exclusion(build())
    check_settlement(build())
    check_partial_receipt(build())


def _print_table(w: Verein) -> None:
    rows = [
        ("constitution_3", w.constitution_hash_3),
        ("proposal_3", w.proposal_3.proposal_hash),
        ("epoch_3", w.epoch_3.epoch_id),
        ("constitution_4", w.constitution_hash_4),
        ("proposal_4", w.proposal_4.proposal_hash),
        ("KASSE", w.kasse.pub),
    ]
    width = max(len(name) for name, _ in rows)
    for name, value in rows:
        print(f"{name:<{width}}  {value.hex()}")


def main() -> int:
    try:
        verify_all()
        _print_table(build())
    except AssertionError as exc:
        print(f"verein: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
