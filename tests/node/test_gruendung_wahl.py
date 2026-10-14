"""Ein Verein aus der Vorlage kann geheim wählen (04 §9.2, D669 Beschluss 1, D673)."""

from __future__ import annotations

from symbolon import cbor_canon
from symbolon.governance import (
    BallotList,
    Election,
    ElectionState,
    Epoch,
    GovernanceFinding,
    tally_election,
)
from symbolon.node.gruendung import gruenden
from symbolon.policy import NucleusPolicy
from tests.helpers import Identity, store_with
from tools.example_nucleus import people

FELDER = {"name": "Laufgruppe", "sitz": "Ort", "zweck": "Gemeinsam laufen"}


def test_verein_aus_der_vorlage_waehlt_geheim() -> None:
    """Drei Gründer, eine Liste mit drei frischen Schlüsseln, zwei Stimmen für ANNA."""
    anna, bruno, chris, _dora = people()
    got = gruenden("verein", [anna.pub.hex(), bruno.pub.hex(), chris.pub.hex()], FELDER)
    satzung = cbor_canon.decode(got.objekte[0][1])
    verein = got.verein
    epoche = Epoch(scope=verein, index=1, constitution_hash=got.constitution)
    wahl = Election(
        {
            0: verein,
            1: epoche.epoch_id,
            2: "vorstand",
            3: sorted([anna.pub, bruno.pub]),
            4: "Vorstand",
        }
    )
    schluessel = [Identity(f"verein-wahl-{i}") for i in range(3)]
    liste = BallotList(
        {
            0: wahl.election_hash,
            1: sorted(p.pub for p in (anna, bruno, chris)),
            2: sorted(k.pub for k in schluessel),
        }
    )
    claims = []
    t = 0
    for wer in (anna, bruno, chris, *schluessel):
        t += 1
        claims.append(
            wer.claim(
                p=f"nuc:{verein.hex()}/ballot-ack@1",
                J=(3, liste.list_hash),
                t=t,
                N=verein,
            )
        )
    for k in schluessel[:2]:
        t += 1
        claims.append(
            k.claim(
                p=f"nuc:{verein.hex()}/ballot@1",
                J=(3, wahl.election_hash),
                t=t,
                N=verein,
                v=cbor_canon.encode({0: anna.pub, 1: 0}),
            )
        )
    ergebnis = tally_election(
        store_with(*claims),
        scope=verein,
        election=wahl,
        epoch=epoche,
        constitution_obj=satzung,
        known_objects={wahl.election_hash: wahl, liste.list_hash: liste},
        now=1000,
        policy=NucleusPolicy(verein, declared=satzung["irrevocable_predicates"]),
    )
    assert GovernanceFinding.BALLOT_REVOCABLE not in {f.kind for f in ergebnis.findings}
    assert ergebnis.lists == (liste.list_hash,)
    assert (ergebnis.state, ergebnis.elected) == (ElectionState.ELECTED, anna.pub)
