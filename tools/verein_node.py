"""Bestand des Vereins für den S-Node (D476, szenario-verein §9)."""

from __future__ import annotations

import sys
from pathlib import Path

from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
)

from symbolon import cbor_canon
from symbolon.atom import signed_bytes
from symbolon.governance.objects import Proposal
from symbolon.node.store import ObjectKind, SqliteStore
from tools.example_nucleus import _Author
from tools.verein import build


def _seed(author: _Author) -> bytes:
    return author._autor._sk.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())


def _proposal_bytes(proposal: Proposal) -> bytes:
    return cbor_canon.encode(
        {0: proposal.scope, 1: proposal.predecessor, 2: proposal.constitution_hash}
    )


def anlegen(path: str | Path) -> None:
    """Legt den Bestand des Vereins an (D476, szenario-verein §9, example-nucleus §5)."""
    world = build()
    store = SqliteStore(path)
    store.submit_object(ObjectKind.GENESIS, world.ex.genesis_gov_cbor)
    store.submit_object(ObjectKind.GENESIS, world.ex.genesis_res_cbor)
    for constitution in (
        world.ex.constitution_gov,
        world.ex.constitution_2,
        world.ex.constitution_res,
        world.constitution_3,
        world.constitution_4,
    ):
        store.submit_object(ObjectKind.CONSTITUTION, cbor_canon.encode(constitution))
    for proposal in (world.ex.proposal, world.proposal_3, world.proposal_4):
        store.submit_object(ObjectKind.PROPOSAL, _proposal_bytes(proposal))
    for claim in world.base.values():
        store.submit_claim(signed_bytes(claim))
    named = (
        (world.anna, "ANNA"),
        (world.bruno, "BRUNO"),
        (world.chris, "CHRIS"),
        (world.dora, "DORA"),
        (world.kasse, "KASSE"),
    )
    for author, name in named:
        store.add_sim_key(_seed(author))
        store.add_name(author.pub, name)
    store.close()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m tools.verein_node <datei>")
    anlegen(sys.argv[1])


if __name__ == "__main__":
    main()
