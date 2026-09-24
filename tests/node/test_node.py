"""Bestand und Sicht (D473)."""

from __future__ import annotations

import pytest

from symbolon import cbor_canon
from symbolon.atom import claim_id, signed_bytes
from symbolon.genesis import genesis_scope
from symbolon.governance.findings import Finding, GovernanceFinding
from symbolon.governance.objects import Proposal
from symbolon.governance.tally import TallyState, decide
from symbolon.policy import constitution_hash
from symbolon.profiles import MembershipState
from symbolon.profiles.credit import SettlementState, settlement
from symbolon.verifier import InMemoryStore, VerifierError
from symbolon.node.store import ObjectKind, SqliteStore
from symbolon.node.view import fork_evidence, scope_view
from tools.example_nucleus import NOW, _nuc
from tools.verein import (
    Verein,
    _T_ANNA,
    _T_BRUNO,
    _T_CHRIS,
    _accept,
    _fork_bruno,
    _obligation,
    _ratify,
    _yes_anna_chris,
    build,
)


def _proposal_bytes(proposal: Proposal) -> bytes:
    return cbor_canon.encode(
        {0: proposal.scope, 1: proposal.predecessor, 2: proposal.constitution_hash}
    )


def _submit_claims(store: SqliteStore, claims: list) -> None:
    for claim in claims:
        store.submit_claim(signed_bytes(claim))


def _submit_constitution(store: SqliteStore, obj: dict) -> None:
    store.submit_object(ObjectKind.CONSTITUTION, cbor_canon.encode(obj))


def _submit_proposal(store: SqliteStore, proposal: Proposal) -> None:
    store.submit_object(ObjectKind.PROPOSAL, _proposal_bytes(proposal))


def _gov_chain(store: SqliteStore, w: Verein, *, extra: tuple[Proposal, dict] = ()) -> None:
    store.submit_object(ObjectKind.GENESIS, w.ex.genesis_gov_cbor)
    _submit_constitution(store, w.ex.constitution_gov)
    _submit_constitution(store, w.ex.constitution_2)
    _submit_proposal(store, w.ex.proposal)
    if extra:
        proposal, constitution = extra
        _submit_constitution(store, constitution)
        _submit_proposal(store, proposal)


def _res_objects(store: SqliteStore, w: Verein) -> None:
    store.submit_object(ObjectKind.GENESIS, w.ex.genesis_res_cbor)
    _submit_constitution(store, w.ex.constitution_res)


def test_roundtrip(tmp_path) -> None:
    """Rundlauf des Bestands (D473, 01 §6)."""
    claims = list(build().base.values())
    memory = InMemoryStore()
    for claim in claims:
        memory.add(claim)
    path = tmp_path / "bestand.sqlite"
    store = SqliteStore(path)
    _submit_claims(store, claims)
    store.close()
    opened = SqliteStore(path)
    got_ids = {claim_id(claim) for claim in opened.all_claims()}
    memory_ids = {claim_id(claim) for claim in memory.all_claims()}
    assert got_ids == memory_ids
    for claim in memory.all_claims():
        got = {claim_id(item) for item in opened.by_author_hprev(claim.I, claim.h_prev)}
        expected = {claim_id(item) for item in memory.by_author_hprev(claim.I, claim.h_prev)}
        assert got == expected
    opened.close()


def test_reject_claim(tmp_path) -> None:
    """Abweisung eines Claims (01 §6, D473 Beschluss 1)."""
    raw = signed_bytes(next(iter(build().base.values())))
    bad_sig = bytearray(raw)
    bad_sig[-1] ^= 0x01
    store = SqliteStore(tmp_path / "bestand.sqlite")
    with pytest.raises(VerifierError):
        store.submit_claim(bytes(bad_sig))
    with pytest.raises(VerifierError):
        store.submit_claim(b"\xff")
    assert store.all_claims() == []
    store.close()


def test_objects(tmp_path) -> None:
    """Objekte je Art (D473 Beschluss 1, 00 §3, 00 §5, 04 §2.4)."""
    w = build()
    store = SqliteStore(tmp_path / "bestand.sqlite")
    genesis_hash = store.submit_object(ObjectKind.GENESIS, w.ex.genesis_gov_cbor)
    assert genesis_hash == genesis_scope(w.ex.genesis_gov)
    assert store.all_genesis()[genesis_hash] == w.ex.genesis_gov
    constitution_data = cbor_canon.encode(w.constitution_3)
    constitution_h = store.submit_object(ObjectKind.CONSTITUTION, constitution_data)
    assert constitution_h == constitution_hash(w.constitution_3)
    assert store.all_constitutions()[constitution_h] == w.constitution_3
    proposal_h = store.submit_object(ObjectKind.PROPOSAL, _proposal_bytes(w.proposal_3))
    assert proposal_h == w.proposal_3.proposal_hash
    assert store.all_proposals()[proposal_h] == w.proposal_3
    with pytest.raises(ValueError):
        store.submit_object(ObjectKind.PROPOSAL, cbor_canon.encode(w.constitution_3))
    with pytest.raises(ValueError):
        store.submit_object(ObjectKind.GENESIS, w.ex.genesis_gov_cbor + b"\x00")
    assert set(store.all_genesis()) == {genesis_hash}
    assert set(store.all_constitutions()) == {constitution_h}
    assert set(store.all_proposals()) == {proposal_h}
    store.close()


def test_aufnahme(tmp_path) -> None:
    """Aufnahme (szenario-verein §3)."""
    w = build()
    v1 = w.chris.vouch(w.dora, n=50, scope=w.ex.N_res, t=_T_CHRIS, t_exp=NOW + 1000000)
    accepts = [
        _accept(w.anna, w.ex.N_gov, w.ex.constitution_hash_2, t=_T_ANNA),
        _accept(w.bruno, w.ex.N_gov, w.ex.constitution_hash_2, t=_T_BRUNO),
        _accept(w.chris, w.ex.N_gov, w.ex.constitution_hash_2, t=_T_CHRIS),
    ]
    store = SqliteStore(tmp_path / "bestand.sqlite")
    _gov_chain(store, w)
    _res_objects(store, w)
    _submit_claims(store, [*w.base.values(), v1, *accepts])
    gov = scope_view(store, w.ex.N_gov, NOW)
    assert gov.findings == ()
    assert gov.state.epoch == w.ex.epoch_2
    assert gov.vereinsleben is None
    assert gov.verein is not None
    members = dict(gov.verein.membership)
    assert set(members) == set(w.ex.constitution_2["participants"])
    for result in members.values():
        assert result.state is MembershipState.MEMBER
    res = scope_view(store, w.ex.N_res, NOW)
    assert res.findings == ()
    assert res.verein is None
    assert res.vereinsleben is not None
    assert res.vereinsleben.derivation.bfs.distance[w.dora.pub] == 2
    store.close()


def test_austausch(tmp_path) -> None:
    """Austausch (szenario-verein §5.2)."""
    w = build()
    anna, chris = _yes_anna_chris(w)
    nein, ja = _fork_bruno(w)
    ratify = _ratify(
        w.anna, w.proposal_3, [anna, chris, ja], t=_T_ANNA + 1, scope=w.ex.N_gov
    )
    store = SqliteStore(tmp_path / "bestand.sqlite")
    _gov_chain(store, w, extra=(w.proposal_3, w.constitution_3))
    _submit_claims(store, [*w.base.values(), anna, chris, nein, ja, ratify])
    gov = scope_view(store, w.ex.N_gov, NOW)
    assert gov.findings == ()
    assert gov.state.epoch == w.ex.epoch_2
    assert gov.verein is not None
    decisions = dict(gov.verein.decisions)
    assert w.proposal_3.proposal_hash in decisions
    direct = decide(
        store,
        epoch=gov.state.epoch,
        proposal=w.proposal_3,
        genesis_obj=w.ex.genesis_gov,
        constitution_obj=gov.state.constitution_obj,
        target_constitution_obj=store.all_constitutions().get(w.proposal_3.constitution_hash),
        known_proposals=store.all_proposals(),
        now=NOW,
        policy=gov.state.policy,
    )
    assert decisions[w.proposal_3.proposal_hash] == direct
    assert direct.state is TallyState.PENDING
    evidence = fork_evidence(store, NOW)
    assert len(evidence) == 1
    group = evidence[0]
    assert group.I == w.bruno.pub
    assert [cid for cid, _scope in group.claims] == sorted(
        (claim_id(nein), claim_id(ja))
    )
    assert {scope for _cid, scope in group.claims} == {w.ex.N_gov}
    store.close()


def test_beitrag(tmp_path) -> None:
    """Beitrag (szenario-verein §6)."""
    w = build()
    obligation = _obligation(w)
    receipt = w.kasse.claim(
        p=_nuc(w.ex.N_res, "receipt"),
        J=(2, claim_id(obligation)),
        t=1,
        N=w.ex.N_res,
    )
    store = SqliteStore(tmp_path / "bestand.sqlite")
    _res_objects(store, w)
    _submit_claims(store, [*w.base.values(), obligation, receipt])
    res = scope_view(store, w.ex.N_res, NOW)
    assert res.findings == ()
    assert res.vereinsleben is not None
    settled = dict(res.vereinsleben.settlements)[claim_id(obligation)]
    direct = settlement(
        store,
        obligation=obligation,
        scope=w.ex.N_res,
        now=NOW,
        policy=res.state.policy,
    )
    assert settled == direct
    assert direct.state is SettlementState.SETTLED
    store.close()

    partial = build()
    obligation_partial = _obligation(partial)
    partial_receipt = partial.kasse.claim(
        p=_nuc(partial.ex.N_res, "receipt"),
        J=(2, claim_id(obligation_partial)),
        t=1,
        N=partial.ex.N_res,
        v=cbor_canon.encode({0: 1200}),
    )
    other = SqliteStore(tmp_path / "teil.sqlite")
    _res_objects(other, partial)
    _submit_claims(other, [*partial.base.values(), obligation_partial, partial_receipt])
    view = scope_view(other, partial.ex.N_res, NOW)
    assert view.findings == ()
    assert view.vereinsleben is not None
    opened = dict(view.vereinsleben.settlements)[claim_id(obligation_partial)]
    direct_open = settlement(
        other,
        obligation=obligation_partial,
        scope=partial.ex.N_res,
        now=NOW,
        policy=view.state.policy,
    )
    assert opened == direct_open
    assert direct_open.state is SettlementState.OPEN
    other.close()


def test_participants_not_a_list(tmp_path) -> None:
    """participants = 5 (D474 Beschluss 2, 04 §3.5)."""
    w = build()
    constitution = dict(w.ex.constitution_gov)
    constitution["participants"] = 5
    digest = constitution_hash(constitution)
    genesis = dict(w.ex.genesis_gov)
    genesis[4] = digest
    store = SqliteStore(tmp_path / "bestand.sqlite")
    scope = store.submit_object(ObjectKind.GENESIS, cbor_canon.encode(genesis))
    store.submit_object(ObjectKind.CONSTITUTION, cbor_canon.encode(constitution))
    view = scope_view(store, scope, NOW)
    assert view.verein is None
    assert view.findings == (
        Finding(GovernanceFinding.MALFORMED_PARTICIPANTS, digest),
    )
    store.close()


def test_participants_short_entry(tmp_path) -> None:
    """participants mit einem Byte (D474 Beschluss 2, 04 §3.5)."""
    w = build()
    constitution = dict(w.ex.constitution_gov)
    constitution["participants"] = [bytes([0x78])]
    digest = constitution_hash(constitution)
    genesis = dict(w.ex.genesis_gov)
    genesis[4] = digest
    store = SqliteStore(tmp_path / "bestand.sqlite")
    scope = store.submit_object(ObjectKind.GENESIS, cbor_canon.encode(genesis))
    store.submit_object(ObjectKind.CONSTITUTION, cbor_canon.encode(constitution))
    view = scope_view(store, scope, NOW)
    assert view.verein is None
    assert view.findings == (
        Finding(GovernanceFinding.MALFORMED_PARTICIPANTS, digest),
    )
    store.close()


def test_root_keys_not_a_list(tmp_path) -> None:
    """root_keys = 5 (D474 Beschluss 1, 03 §1.2)."""
    w = build()
    genesis = dict(w.ex.genesis_gov)
    genesis[1] = 5
    store = SqliteStore(tmp_path / "bestand.sqlite")
    with pytest.raises(ValueError):
        store.submit_object(ObjectKind.GENESIS, cbor_canon.encode(genesis))
    assert store.all_genesis() == {}
    store.close()


def test_trust_params_text(tmp_path) -> None:
    """Key 9, Wert unter 0 ein Text (D474 Beschluss 1, 00 §4.0)."""
    w = build()
    genesis = dict(w.ex.genesis_res)
    trust = dict(w.ex.genesis_res[9])
    trust[0] = "text"
    genesis[9] = trust
    store = SqliteStore(tmp_path / "bestand.sqlite")
    with pytest.raises(ValueError):
        store.submit_object(ObjectKind.GENESIS, cbor_canon.encode(genesis))
    assert store.all_genesis() == {}
    store.close()
