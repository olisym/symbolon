#!/usr/bin/env python3
"""Szenario H: zwei Zeitregime unter divergenten Uhren (01 §2 Feld 6, 04 §3.1, 02a §2.6, D350).

Wegwerf-Treiber. Drei unabhängige Läufe, kein geteilter Kontext.
now wird in _beobachte durchgereicht; die Lage ohne setzt now=None, ohne welt.py
anzutasten. Keine neuen Primitive.
"""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path
from typing import Any

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id
from symbolon.domains import DOM_NUC_GEN
from symbolon.governance import Epoch, Proposal, resolve_epoch
from symbolon.governance.findings import Finding, GovernanceFinding
from symbolon.index import classify_all
from symbolon.policy import constitution_hash
from symbolon.verifier import State, classify
from tools.sim.welt import Welt

A, B, C, Z = "anna", "bruno", "chris", "dora"
NAMEN = (A, B, C, Z)
NAMEN_SEED = {A: 0x11, B: 0x12, C: 0x13, Z: 0x14}
NOW = 1000
T_EXP = 10_000
VOR = 1_000_000
ZURUECK = 100
UHRLAGEN: tuple[tuple[str, int | None], ...] = (
    ("vor", VOR),
    ("zurueck", ZURUECK),
    ("ohne", None),
)


def _nuc(scope: bytes, name: str) -> str:
    return f"nuc:{scope.hex()}/{name}@1"


def _kurz(value: bytes) -> str:
    return value.hex()[:16]


def _verfassung(
    participants: list[bytes],
    *,
    arbitrators: list[bytes],
) -> dict[str, Any]:
    return {
        "irrevocable_predicates": ["obligation@1", "ratify@1", "vote@1"],
        "thresholds": {
            "ordinary": [1, 2],
            "membership": [1, 2],
            "amendment": [1, 2],
        },
        "arbitration": {"arbitrators": arbitrators},
        "participants": participants,
    }


def _welt(pfad: str) -> Welt:
    welt = Welt.anlegen(Path(pfad))
    for name in NAMEN:
        welt.teilnehmer_anlegen(name, bytes([NAMEN_SEED[name]] * 32), NOW)
    return welt


def _aufbau(welt: Welt, *, vote_t_exp: int | None = None) -> dict[str, Any]:
    """Genesis und gerade Epochenkette ohne Konflikt (04 §1.1, 04 §2, 04 §3.1)."""
    pubs = {name: welt.teilnehmer[name].pub for name in NAMEN}
    participants = sorted(pubs.values())
    constitution_1 = _verfassung(participants, arbitrators=[pubs[A]])
    constitution_a = _verfassung(participants, arbitrators=[pubs[B]])
    hash_1 = constitution_hash(constitution_1)
    hash_a = constitution_hash(constitution_a)
    genesis = {
        0: 1,
        1: [pubs[A]],
        2: 0,
        3: [pubs[A]],
        4: hash_1,
        5: 2,
        6: 0,
        7: 0,
    }
    n = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis)).digest()
    epoch_1 = Epoch(scope=n, index=1, constitution_hash=hash_1)
    proposal_a = Proposal(
        scope=n, predecessor=epoch_1.epoch_id, constitution_hash=hash_a
    )

    def _ja(autor: str, proposal: Proposal, t: int) -> Claim:
        return welt.teilnehmer[autor].claim_signieren(
            p=_nuc(n, "vote"),
            J=(3, proposal.proposal_hash),
            t=t,
            v=cbor_canon.encode({0: 1}),
            N=n,
            t_exp=vote_t_exp,
        )

    anna_a = _ja(A, proposal_a, 1)
    bruno_a = _ja(B, proposal_a, 1)
    chris_a = _ja(C, proposal_a, 1)
    ratify_a = welt.teilnehmer[A].claim_signieren(
        p=_nuc(n, "ratify"),
        J=(3, proposal_a.proposal_hash),
        t=2,
        v=cbor_canon.encode(
            {0: [claim_id(anna_a), claim_id(bruno_a), claim_id(chris_a)]}
        ),
        N=n,
    )
    votes = (anna_a, bruno_a, chris_a)
    return {
        "N": n,
        "genesis": genesis,
        "epoch_1": epoch_1,
        "constitution_1": constitution_1,
        "constitution_a": constitution_a,
        "hash_1": hash_1,
        "hash_a": hash_a,
        "proposal_a": proposal_a,
        "anna_a": anna_a,
        "bruno_a": bruno_a,
        "chris_a": chris_a,
        "ratify_a": ratify_a,
        "votes": votes,
        "vote_cids": tuple(claim_id(v) for v in votes),
        "known_constitutions": {name: {} for name in NAMEN},
        "known_proposals": {name: {} for name in NAMEN},
    }


def _kennt_verfassung(ex: dict[str, Any], name: str, obj: dict[str, Any]) -> None:
    ex["known_constitutions"][name][constitution_hash(obj)] = obj


def _kennt_vorschlag(ex: dict[str, Any], name: str, proposal: Proposal) -> None:
    ex["known_proposals"][name][proposal.proposal_hash] = proposal


def _kette_bekannt(ex: dict[str, Any], name: str) -> None:
    _kennt_verfassung(ex, name, ex["constitution_1"])
    _kennt_verfassung(ex, name, ex["constitution_a"])
    _kennt_vorschlag(ex, name, ex["proposal_a"])


def _vermerke(findings: tuple[Finding, ...]) -> list[str]:
    return [f"{f.kind.value} subject={_kurz(f.subject)}" for f in findings]


def _beobachte(
    welt: Welt, ex: dict[str, Any], name: str, now: int | None
) -> dict[str, Any]:
    """resolve_epoch und classify_all gegen die lokale Sicht; now durchgereicht (D350)."""
    tp = welt.teilnehmer[name]
    store = tp.store_laden()
    by_cid = classify_all(store, now)
    row: dict[str, Any] = {
        "name": name,
        "now": now,
        "read_now": tp.read_now(),
        "classify": {cid: cls.state for cid, cls in by_cid.items()},
        "store_cids": frozenset(by_cid),
    }
    if "genesis" in ex:
        resolution = resolve_epoch(
            store,
            scope=ex["N"],
            genesis_obj=ex["genesis"],
            known_constitutions=ex["known_constitutions"][name],
            known_proposals=ex["known_proposals"][name],
            now=now,
        )
        row["index"] = resolution.epoch.index
        row["constitution_hash"] = resolution.epoch.constitution_hash
        row["chain_findings"] = _vermerke(resolution.findings)
        row["findings"] = resolution.findings
    return row


def _alle(welt: Welt, ex: dict[str, Any]) -> dict[str, dict[str, dict[str, Any]]]:
    return {
        lage: {name: _beobachte(welt, ex, name, now) for name in NAMEN}
        for lage, now in UHRLAGEN
    }


def _drucke_governance(lage: str, rows: dict[str, dict[str, Any]]) -> None:
    print(f"--- Uhrlage {lage} ---")
    for name in NAMEN:
        row = rows[name]
        print(
            f"  {row['name']}: Epoche {row['index']}  "
            f"constitution_hash={_kurz(row['constitution_hash'])}  "
            f"now={row['now']!r}  read_now={row['read_now']}"
        )
        print("    Vermerke resolve_epoch:")
        if row["chain_findings"]:
            for line in row["chain_findings"]:
                print(f"      {line}")
        else:
            print("      (keine)")
    print()


def _drucke_trust(
    lage: str, rows: dict[str, dict[str, Any]], cid: bytes
) -> None:
    print(f"--- Uhrlage {lage} ---")
    for name in NAMEN:
        row = rows[name]
        state = row["classify"].get(cid)
        state_name = state.name if state is not None else "abwesend"
        print(
            f"  {row['name']}: State={state_name}  "
            f"hat={cid in row['store_cids']}  "
            f"now={row['now']!r}  read_now={row['read_now']}"
        )
    print()


def _lauf1(pfad: str) -> dict[str, Any]:
    print("=== Lauf 1 — Governance bei identischem Wissen und drei Uhren ===")
    print()
    welt = _welt(pfad)
    ex = _aufbau(welt, vote_t_exp=None)
    for name in NAMEN:
        _kette_bekannt(ex, name)
    welt.zustellen(A, "alle")
    welt.zustellen(B, "alle")
    welt.zustellen(C, "alle")
    beobachtung = _alle(welt, ex)
    for lage, _now in UHRLAGEN:
        _drucke_governance(lage, beobachtung[lage])
    return {"beobachtung": beobachtung, "epoch_1": ex["epoch_1"]}


def _lauf2(pfad: str) -> dict[str, Any]:
    print("=== Lauf 2 — dieselbe Kette, aber mit t_exp auf den Stimmen ===")
    print()
    welt = _welt(pfad)
    ex = _aufbau(welt, vote_t_exp=T_EXP)
    for name in NAMEN:
        _kette_bekannt(ex, name)
    welt.zustellen(A, "alle")
    welt.zustellen(B, "alle")
    welt.zustellen(C, "alle")
    beobachtung = _alle(welt, ex)
    for lage, _now in UHRLAGEN:
        _drucke_governance(lage, beobachtung[lage])
    return {
        "beobachtung": beobachtung,
        "epoch_1": ex["epoch_1"],
        "vote_cids": ex["vote_cids"],
    }


def _vouch(welt: Welt) -> tuple[dict[str, Any], Claim]:
    pubs = {name: welt.teilnehmer[name].pub for name in NAMEN}
    n = bytes([0x22] * 32)
    claim = welt.teilnehmer[A].claim_signieren(
        p=_nuc(n, "vouch"),
        J=(1, pubs[B]),
        t=1,
        v=cbor_canon.encode({0: 50}),
        N=n,
        t_exp=T_EXP,
    )
    ex: dict[str, Any] = {"vouch": claim, "vouch_cid": claim_id(claim)}
    return ex, claim


def _lauf3(pfad: str) -> dict[str, Any]:
    print("=== Lauf 3 — Trust unter denselben drei Uhren ===")
    print()
    root = Path(pfad)
    welt = _welt(str(root / "stufe1"))
    ex, _claim = _vouch(welt)
    cid = ex["vouch_cid"]
    welt.zustellen(A, "alle")
    beobachtung = _alle(welt, ex)
    for lage, _now in UHRLAGEN:
        _drucke_trust(lage, beobachtung[lage], cid)

    print("--- Stufe 2 — Nachlieferung nach t_exp ---")
    welt2 = _welt(str(root / "stufe2"))
    ex2, claim2 = _vouch(welt2)
    cid2 = ex2["vouch_cid"]
    welt2.zustellen(A, [B, C])
    welt2.teilnehmer[Z].write_now(VOR)
    hat_vor = welt2.teilnehmer[Z].hat_claim(cid2)
    vor_zustellung = _beobachte(welt2, ex2, Z, VOR)
    classify_obj_vor = classify(claim2, welt2.teilnehmer[Z].store_laden(), now=VOR)
    print(
        f"  dora vor Zustellung: hat_claim={hat_vor}  "
        f"in_classify_all={cid2 in vor_zustellung['store_cids']}  "
        f"classify(claim)={classify_obj_vor.state.name}  "
        f"now={VOR}  read_now={welt2.teilnehmer[Z].read_now()}"
    )
    welt2.zustellen(A, [Z], nur=[cid2])
    hat_nach = welt2.teilnehmer[Z].hat_claim(cid2)
    nach_zustellung = _beobachte(welt2, ex2, Z, VOR)
    classify_obj_nach = classify(claim2, welt2.teilnehmer[Z].store_laden(), now=VOR)
    state_nach = nach_zustellung["classify"].get(cid2)
    state_nach_name = state_nach.name if state_nach is not None else "abwesend"
    print(
        f"  dora nach Zustellung: hat_claim={hat_nach}  "
        f"in_classify_all={cid2 in nach_zustellung['store_cids']}  "
        f"State={state_nach_name}  "
        f"classify(claim)={classify_obj_nach.state.name}  "
        f"now={VOR}  read_now={welt2.teilnehmer[Z].read_now()}"
    )
    vermerke_vor = vor_zustellung.get("chain_findings", [])
    vermerke_nach = nach_zustellung.get("chain_findings", [])
    print(f"  Vermerke vor={vermerke_vor} nach={vermerke_nach}")
    print()
    return {
        "beobachtung": beobachtung,
        "vouch_cid": cid,
        "vor_zustellung": vor_zustellung,
        "nach_zustellung": nach_zustellung,
        "hat_vor": hat_vor,
        "hat_nach": hat_nach,
        "in_all_vor": cid2 in vor_zustellung["store_cids"],
        "in_all_nach": cid2 in nach_zustellung["store_cids"],
        "classify_obj_vor": classify_obj_vor.state,
        "classify_obj_nach": classify_obj_nach.state,
        "state_nach": state_nach,
        "vermerke_vor": vermerke_vor,
        "vermerke_nach": vermerke_nach,
        "cid2": cid2,
    }


def _zeile(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        row["index"],
        row["constitution_hash"],
        tuple(row["chain_findings"]),
    )


def _beobachter_gleich(rows: dict[str, dict[str, Any]]) -> bool:
    zeilen = {_zeile(rows[name]) for name in NAMEN}
    return len(zeilen) == 1


def _uhren_gleich(
    beobachtung: dict[str, dict[str, dict[str, Any]]],
) -> bool:
    zeilen = set()
    for lage, _now in UHRLAGEN:
        for name in NAMEN:
            zeilen.add(_zeile(beobachtung[lage][name]))
    return len(zeilen) == 1


def _vote_expiry(
    row: dict[str, Any], vote_cids: tuple[bytes, ...]
) -> bool:
    subjects = {
        f.subject
        for f in row["findings"]
        if f.kind is GovernanceFinding.VOTE_WITH_EXPIRY
    }
    return subjects == set(vote_cids)


def _befunde(
    lauf1: dict[str, Any],
    lauf2: dict[str, Any],
    lauf3: dict[str, Any],
) -> None:
    print("=== Befunde ===")
    print()

    b1 = lauf1["beobachtung"]
    for lage, _now in UHRLAGEN:
        rows = b1[lage]
        epochen = {name: rows[name]["index"] for name in NAMEN}
        hashes = {name: _kurz(rows[name]["constitution_hash"]) for name in NAMEN}
        vermerke = {name: rows[name]["chain_findings"] for name in NAMEN}
        print(
            f"(Lauf 1, {lage}) Epochen={epochen} hashes={hashes} "
            f"Vermerke={vermerke}"
        )
    print()
    gleich_beobachter = all(_beobachter_gleich(b1[lage]) for lage, _now in UHRLAGEN)
    gleich_uhren = _uhren_gleich(b1)
    if gleich_beobachter and gleich_uhren:
        eine = _zeile(b1["vor"][A])
        print(
            "(Lauf 1) bestätigt — alle vier Beobachter und alle drei Uhrlagen "
            f"identisch: Epoche {eine[0]}, hash={_kurz(eine[1])}, "
            f"Vermerke={list(eine[2])}."
        )
    else:
        print(
            "(Lauf 1) widerlegt — "
            f"beobachter_gleich={gleich_beobachter}, uhren_gleich={gleich_uhren}."
        )
    print()

    b2 = lauf2["beobachtung"]
    vote_cids = lauf2["vote_cids"]
    genesis_index = lauf2["epoch_1"].index
    for lage, _now in UHRLAGEN:
        rows = b2[lage]
        epochen = {name: rows[name]["index"] for name in NAMEN}
        hashes = {name: _kurz(rows[name]["constitution_hash"]) for name in NAMEN}
        vermerke = {name: rows[name]["chain_findings"] for name in NAMEN}
        expiry = {name: _vote_expiry(rows[name], vote_cids) for name in NAMEN}
        print(
            f"(Lauf 2, {lage}) Epochen={epochen} hashes={hashes} "
            f"VOTE_WITH_EXPIRY_je_Stimme={expiry} Vermerke={vermerke}"
        )
    print()
    alle_expiry = all(
        _vote_expiry(b2[lage][name], vote_cids)
        for lage, _now in UHRLAGEN
        for name in NAMEN
    )
    alle_genesis = all(
        b2[lage][name]["index"] == genesis_index
        for lage, _now in UHRLAGEN
        for name in NAMEN
    )
    gleich_uhren2 = _uhren_gleich(b2)
    if alle_expiry and alle_genesis and gleich_uhren2:
        print(
            "(Lauf 2) bestätigt — VOTE_WITH_EXPIRY je Stimme, Epoche bleibt die "
            f"Genesis (index {genesis_index}), drei Uhrlagen identisch."
        )
    else:
        print(
            "(Lauf 2) widerlegt — "
            f"VOTE_WITH_EXPIRY_je_Stimme={alle_expiry}, "
            f"genesis={alle_genesis}, uhren_gleich={gleich_uhren2}."
        )
    print()

    b3 = lauf3["beobachtung"]
    cid = lauf3["vouch_cid"]
    erwartet = {"vor": State.EXPIRED, "zurueck": State.ACTIVE, "ohne": State.LINKED}
    for lage, _now in UHRLAGEN:
        rows = b3[lage]
        zustaende = {
            name: (
                rows[name]["classify"][cid].name
                if cid in rows[name]["classify"]
                else "abwesend"
            )
            for name in NAMEN
        }
        print(f"(Lauf 3, {lage}) State={zustaende}")
    print()
    divergiert = True
    for lage, soll in erwartet.items():
        for name in NAMEN:
            ist = b3[lage][name]["classify"].get(cid)
            if ist is not soll:
                divergiert = False
    if divergiert:
        print(
            "(Lauf 3 Klassifikation) bestätigt — ACTIVE bei zurueck, EXPIRED bei "
            "vor, LINKED bei ohne, auf identischem Claim-Satz."
        )
    else:
        print(
            "(Lauf 3 Klassifikation) widerlegt — Klassifikation divergiert nicht "
            "wie erwartet."
        )
    print()

    state_nach = lauf3["state_nach"]
    print(
        f"(Lauf 3 Stufe 2) hat_nach={lauf3['hat_nach']} "
        f"in_classify_all_vor={lauf3['in_all_vor']} "
        f"in_classify_all_nach={lauf3['in_all_nach']} "
        f"State_nach={state_nach.name if state_nach is not None else 'abwesend'} "
        f"classify_obj_vor={lauf3['classify_obj_vor'].name} "
        f"classify_obj_nach={lauf3['classify_obj_nach'].name} "
        f"Vermerke_vor={lauf3['vermerke_vor']} "
        f"Vermerke_nach={lauf3['vermerke_nach']}"
    )
    heilt_nicht = (
        lauf3["hat_nach"]
        and lauf3["in_all_nach"]
        and state_nach is State.EXPIRED
    )
    vermerk_unterscheidet = lauf3["vermerke_vor"] != lauf3["vermerke_nach"]
    store_unterscheidet = (not lauf3["in_all_vor"]) and lauf3["in_all_nach"]
    classify_obj_gleich = (
        lauf3["classify_obj_vor"] is lauf3["classify_obj_nach"]
    )
    print(
        f"(Lauf 3 Stufe 2 Unterscheidung) "
        f"store_unterscheidet={store_unterscheidet} "
        f"vermerk_unterscheidet={vermerk_unterscheidet} "
        f"classify(claim)_gleich={classify_obj_gleich}"
    )
    if heilt_nicht:
        print(
            "(Lauf 3 Stufe 2) bestätigt — Nachlieferung heilt nicht, Claim kommt "
            "an und ist EXPIRED."
        )
    else:
        print(
            "(Lauf 3 Stufe 2) widerlegt — "
            f"hat_nach={lauf3['hat_nach']}, in_all_nach={lauf3['in_all_nach']}, "
            f"State={state_nach.name if state_nach is not None else 'abwesend'}."
        )
    if vermerk_unterscheidet:
        print(
            "(Lauf 3 Stufe 2 Vermerk) bestätigt — ein Vermerk unterscheidet "
            '"nie erhalten" und "zu spaet erhalten".'
        )
    else:
        print(
            "(Lauf 3 Stufe 2 Vermerk) widerlegt — kein Vermerk unterscheidet "
            '"nie erhalten" und "zu spaet erhalten"; die Lagen trennt die '
            "Anwesenheit in classify_all, nicht ein Finding."
        )


def main() -> None:
    print("Szenario H — zwei Zeitregime unter divergenten Uhren (00ba)")
    print("A=anna  B=bruno  C=chris  Z=dora")
    print(
        f"Uhrlagen: vor={VOR}  zurueck={ZURUECK}  ohne=None  t_exp={T_EXP}  "
        f"Teilnehmer.read_now()={NOW}"
    )
    print()
    with tempfile.TemporaryDirectory() as tmp:
        lauf1 = _lauf1(str(Path(tmp) / "lauf1"))
        lauf2 = _lauf2(str(Path(tmp) / "lauf2"))
        lauf3 = _lauf3(str(Path(tmp) / "lauf3"))
    _befunde(lauf1, lauf2, lauf3)


if __name__ == "__main__":
    main()
