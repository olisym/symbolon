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
from symbolon.atom import Claim, claim_id, signed_bytes
from symbolon.governance.objects import Proposal
from symbolon.node.store import ObjectKind, SqliteStore
from tools.example_nucleus import _Author, _nuc
from tools.verein import Verein, build

# Seeds der Zweitgeräte, je 32 Byte (D542 Beschluss 3).
GERAETE_SEEDS: dict[str, bytes] = {
    "BRUNO": bytes([0x21] * 32),
    "DORA": bytes([0x22] * 32),
}


def _seed(author: _Author) -> bytes:
    return author._autor._sk.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())


def _proposal_bytes(proposal: Proposal) -> bytes:
    return cbor_canon.encode(
        {0: proposal.scope, 1: proposal.predecessor, 2: proposal.constitution_hash}
    )


def aufnahmen(world: Verein) -> list[tuple[str, _Author, Claim, Claim]]:
    """Aufnahme der Zweitgeräte in ``N_gov``, BRUNO vor DORA (D542 Beschluss 3, D543 Beschluss 5,
    02 §2.1, 01 §7.3).

    Je Gerät ein ``device-add@1`` der Wurzel mit ``J = (1, Gerät)`` und ein ``device-ack@1`` des
    Geräts mit ``J = (2, claim_id(add))``, ohne ``t_exp``, ``t = 10``; die Ketten in ``world``
    gehen weiter.
    """
    gov = world.ex.N_gov
    wurzeln = {"BRUNO": world.bruno, "DORA": world.dora}
    result: list[tuple[str, _Author, Claim, Claim]] = []
    for name, seed in GERAETE_SEEDS.items():
        geraet = _Author(seed)
        add = wurzeln[name].claim(p=_nuc(gov, "device-add"), J=(1, geraet.pub), t=10, N=gov)
        ack = geraet.claim(p=_nuc(gov, "device-ack"), J=(2, claim_id(add)), t=10, N=gov)
        result.append((name, geraet, add, ack))
    return result


def anlegen(
    path: str | Path,
    schluessel: set[str] | frozenset[str] | None = None,
    geraete: bool = False,
) -> None:
    """Legt den Bestand des Vereins an (D476, szenario-verein §9, example-nucleus §5).

    Ist ``schluessel`` gesetzt, trägt es nur die simulierten Schlüssel dieser Namen ein; die
    Namen immer für alle fünf (D518 Beschluss 1). Mit ``geraete`` dazu die Aufnahmen aus
    :func:`aufnahmen` und die Namen beider Zweitgeräte, deren Seed nur, wo ihr Name in
    ``schluessel`` steht (D542 Beschluss 3).
    """
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
        if schluessel is None or name in schluessel:
            store.add_sim_key(_seed(author))
        store.add_name(author.pub, name)
    if geraete:
        for name, geraet, add, ack in aufnahmen(world):
            for claim in (add, ack):
                store.submit_claim(signed_bytes(claim))
            geraet_name = f"{name} (Zweitgerät)"
            if schluessel is None or geraet_name in schluessel:
                store.add_sim_key(_seed(geraet))
            store.add_name(geraet.pub, geraet_name)
    store.close()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m tools.verein_node <datei>")
    anlegen(sys.argv[1])


if __name__ == "__main__":
    main()
