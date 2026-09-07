#!/usr/bin/env python3
"""Szenario G: zweistufige Epochenkette unter Teilwissen (04 §3.2, 04 §4.1, 04 §4.4, 04 §4.5, D174, D178, D179, D342).

Wegwerf-Treiber. Drei unabhängige Läufe, kein geteilter Kontext.
Stimmen und ratify@1 über Welt.zustellen; Verfassungs- und Vorschlagsobjekte
über pro Beobachter geführte Dicts. Keine neuen Primitive.
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
from symbolon.governance.findings import Finding
from symbolon.policy import constitution_hash
from tools.sim.welt import Welt

A, B, C, Z = "anna", "bruno", "chris", "dora"
NAMEN = (A, B, C, Z)
NAMEN_SEED = {A: 0x11, B: 0x12, C: 0x13, Z: 0x14}
NOW = 1000


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


def _aufbau(welt: Welt, *, konflikte: bool) -> dict[str, Any]:
    """Genesis, Kette 1→2→3, optional Konfliktstimmen (04 §1.1, 04 §2, 04 §4.4)."""
    pubs = {name: welt.teilnehmer[name].pub for name in NAMEN}
    participants = sorted(pubs.values())
    constitution_1 = _verfassung(participants, arbitrators=[pubs[A]])
    constitution_a = _verfassung(participants, arbitrators=[pubs[B]])
    constitution_c = _verfassung(participants, arbitrators=[pubs[C]])
    constitution_b = _verfassung(participants, arbitrators=[pubs[Z]])
    constitution_d = _verfassung(participants, arbitrators=[pubs[A], pubs[B]])
    constitution_x = _verfassung(participants, arbitrators=[pubs[A], pubs[C]])
    hash_1 = constitution_hash(constitution_1)
    hash_a = constitution_hash(constitution_a)
    hash_c = constitution_hash(constitution_c)
    hash_b = constitution_hash(constitution_b)
    hash_d = constitution_hash(constitution_d)
    hash_x = constitution_hash(constitution_x)
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
    epoch_2 = Epoch(scope=n, index=2, constitution_hash=hash_a)
    proposal_a = Proposal(
        scope=n, predecessor=epoch_1.epoch_id, constitution_hash=hash_a
    )
    proposal_c = Proposal(
        scope=n, predecessor=epoch_2.epoch_id, constitution_hash=hash_c
    )
    proposal_b = Proposal(
        scope=n, predecessor=epoch_1.epoch_id, constitution_hash=hash_b
    )
    proposal_d = Proposal(
        scope=n, predecessor=epoch_2.epoch_id, constitution_hash=hash_d
    )
    proposal_x = Proposal(
        scope=n, predecessor=epoch_2.epoch_id, constitution_hash=hash_x
    )

    def _ja(autor: str, proposal: Proposal, t: int) -> Claim:
        return welt.teilnehmer[autor].claim_signieren(
            p=_nuc(n, "vote"),
            J=(3, proposal.proposal_hash),
            t=t,
            v=cbor_canon.encode({0: 1}),
            N=n,
        )

    def _ja_gabel(autor: str, proposal: Proposal, t: int) -> Claim:
        # Drei unabhängige Fortsetzungen derselben Spitze, damit je Beobachter
        # eine Konfliktstimme ACTIVE ist, ohne die anderen beiden (D129).
        return welt.teilnehmer[autor].claim_gabeln(
            p=_nuc(n, "vote"),
            J=(3, proposal.proposal_hash),
            t=t,
            v=cbor_canon.encode({0: 1}),
            N=n,
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
    anna_c = _ja(A, proposal_c, 3)
    bruno_c = _ja(B, proposal_c, 3)
    chris_c = _ja(C, proposal_c, 3)
    ratify_c = welt.teilnehmer[A].claim_signieren(
        p=_nuc(n, "ratify"),
        J=(3, proposal_c.proposal_hash),
        t=4,
        v=cbor_canon.encode(
            {0: [claim_id(anna_c), claim_id(bruno_c), claim_id(chris_c)]}
        ),
        N=n,
    )
    chris_b = _ja_gabel(C, proposal_b, 5) if konflikte else None
    chris_d = _ja_gabel(C, proposal_d, 5) if konflikte else None
    chris_x = _ja_gabel(C, proposal_x, 5) if konflikte else None
    return {
        "N": n,
        "genesis": genesis,
        "epoch_1": epoch_1,
        "epoch_2": epoch_2,
        "constitution_1": constitution_1,
        "constitution_a": constitution_a,
        "constitution_c": constitution_c,
        "constitution_b": constitution_b,
        "constitution_d": constitution_d,
        "constitution_x": constitution_x,
        "hash_1": hash_1,
        "hash_a": hash_a,
        "hash_c": hash_c,
        "hash_b": hash_b,
        "hash_d": hash_d,
        "hash_x": hash_x,
        "proposal_a": proposal_a,
        "proposal_c": proposal_c,
        "proposal_b": proposal_b,
        "proposal_d": proposal_d,
        "proposal_x": proposal_x,
        "anna_a": anna_a,
        "bruno_a": bruno_a,
        "chris_a": chris_a,
        "ratify_a": ratify_a,
        "anna_c": anna_c,
        "bruno_c": bruno_c,
        "chris_c": chris_c,
        "ratify_c": ratify_c,
        "chris_b": chris_b,
        "chris_d": chris_d,
        "chris_x": chris_x,
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
    _kennt_verfassung(ex, name, ex["constitution_c"])
    _kennt_vorschlag(ex, name, ex["proposal_a"])
    _kennt_vorschlag(ex, name, ex["proposal_c"])


def _basis_cids(ex: dict[str, Any]) -> list[bytes]:
    return [
        claim_id(ex["anna_a"]),
        claim_id(ex["bruno_a"]),
        claim_id(ex["chris_a"]),
        claim_id(ex["ratify_a"]),
        claim_id(ex["anna_c"]),
        claim_id(ex["bruno_c"]),
        claim_id(ex["chris_c"]),
        claim_id(ex["ratify_c"]),
    ]


def _zustellen_cids(welt: Welt, an: list[str], cids: list[bytes]) -> None:
    for von in (A, B, C):
        welt.zustellen(von, an, nur=cids)


def _vermerke(findings: tuple[Finding, ...]) -> list[str]:
    return [f"{f.kind.value} subject={_kurz(f.subject)}" for f in findings]


def _beobachte(welt: Welt, ex: dict[str, Any], name: str) -> dict[str, Any]:
    """resolve_epoch gegen die lokale Sicht (04 §3, 04 §4.5)."""
    tp = welt.teilnehmer[name]
    store = tp.store_laden()
    now = tp.read_now()
    resolution = resolve_epoch(
        store,
        scope=ex["N"],
        genesis_obj=ex["genesis"],
        known_constitutions=ex["known_constitutions"][name],
        known_proposals=ex["known_proposals"][name],
        now=now,
    )
    return {
        "name": name,
        "index": resolution.epoch.index,
        "constitution_hash": resolution.epoch.constitution_hash,
        "chain_findings": _vermerke(resolution.findings),
        "findings": resolution.findings,
    }


def _drucke_beobachter(row: dict[str, Any]) -> None:
    print(
        f"  {row['name']}: Epoche {row['index']}  "
        f"constitution_hash={_kurz(row['constitution_hash'])}"
    )
    print("    Vermerke resolve_epoch:")
    if row["chain_findings"]:
        for line in row["chain_findings"]:
            print(f"      {line}")
    else:
        print("      (keine)")
    print()


def _lauf1(pfad: str) -> dict[str, Any]:
    print("=== Lauf 1 — Grundlage und stille Divergenz ===")
    print()
    welt = _welt(pfad)
    ex = _aufbau(welt, konflikte=False)
    for name in NAMEN:
        _kette_bekannt(ex, name)
    basis = _basis_cids(ex)
    _zustellen_cids(welt, [A, B, C], basis)
    ohne_c = [cid for cid in basis if cid != claim_id(ex["ratify_c"])]
    _zustellen_cids(welt, [Z], ohne_c)

    print("--- Stufe 1 — ratify_c nicht bei dora ---")
    stufe1 = {name: _beobachte(welt, ex, name) for name in NAMEN}
    for name in NAMEN:
        _drucke_beobachter(stufe1[name])

    print("--- Stufe 2 — ratify_c an dora nachgereicht ---")
    welt.zustellen(A, [Z], nur=[claim_id(ex["ratify_c"])])
    stufe2_dora = _beobachte(welt, ex, Z)
    _drucke_beobachter(stufe2_dora)

    return {"stufe1": stufe1, "stufe2_dora": stufe2_dora}


def _lauf2(pfad: str) -> dict[str, Any]:
    print("=== Lauf 2 — Rückfall ===")
    print()
    welt = _welt(pfad)
    ex = _aufbau(welt, konflikte=True)
    for name in NAMEN:
        _kette_bekannt(ex, name)
    _zustellen_cids(welt, list(NAMEN), _basis_cids(ex))

    welt.zustellen(C, [B], nur=[claim_id(ex["chris_b"])])
    _kennt_vorschlag(ex, B, ex["proposal_b"])
    welt.zustellen(C, [Z], nur=[claim_id(ex["chris_d"])])
    _kennt_vorschlag(ex, Z, ex["proposal_d"])
    welt.zustellen(C, [A], nur=[claim_id(ex["chris_x"])])

    print("--- G1 — bruno, Konfliktstimme auf P_b ---")
    g1 = _beobachte(welt, ex, B)
    _drucke_beobachter(g1)

    print("--- G2 — dora, Konfliktstimme auf P_d ---")
    g2 = _beobachte(welt, ex, Z)
    _drucke_beobachter(g2)

    print("--- G3 — anna, Konfliktstimme auf P_x ohne Objekt ---")
    g3 = _beobachte(welt, ex, A)
    _drucke_beobachter(g3)

    print("--- G3' — anna, Objekt P_x nachgereicht ---")
    _kennt_vorschlag(ex, A, ex["proposal_x"])
    g3p = _beobachte(welt, ex, A)
    _drucke_beobachter(g3p)

    return {
        "g1": g1,
        "g2": g2,
        "g3": g3,
        "g3p": g3p,
        "cid_ratify_c": claim_id(ex["ratify_c"]),
        "hash_p_c": ex["proposal_c"].proposal_hash,
    }


def _ja_signieren(
    welt: Welt, ex: dict[str, Any], autor: str, proposal: Proposal, t: int
) -> Claim:
    n = ex["N"]
    return welt.teilnehmer[autor].claim_signieren(
        p=_nuc(n, "vote"),
        J=(3, proposal.proposal_hash),
        t=t,
        v=cbor_canon.encode({0: 1}),
        N=n,
    )


def _lauf3_fall(
    pfad: str,
    *,
    titel: str,
    rivale: str | None,
    objekt_bekannt: bool,
) -> dict[str, dict[str, Any]]:
    """Eine Welt, höchstens eine Konfliktstimme per claim_signieren (04 §4.4, 04 §4.5)."""
    print(f"--- {titel} ---")
    welt = _welt(pfad)
    ex = _aufbau(welt, konflikte=False)
    for name in NAMEN:
        _kette_bekannt(ex, name)
    if rivale == "b":
        _ja_signieren(welt, ex, C, ex["proposal_b"], 5)
        if objekt_bekannt:
            for name in NAMEN:
                _kennt_vorschlag(ex, name, ex["proposal_b"])
    elif rivale == "d":
        _ja_signieren(welt, ex, C, ex["proposal_d"], 5)
        if objekt_bekannt:
            for name in NAMEN:
                _kennt_vorschlag(ex, name, ex["proposal_d"])
    elif rivale == "x":
        _ja_signieren(welt, ex, C, ex["proposal_x"], 5)
        if objekt_bekannt:
            for name in NAMEN:
                _kennt_vorschlag(ex, name, ex["proposal_x"])
    welt.zustellen(A, "alle")
    welt.zustellen(B, "alle")
    welt.zustellen(C, "alle")
    rows = {name: _beobachte(welt, ex, name) for name in NAMEN}
    for name in NAMEN:
        _drucke_beobachter(rows[name])
    return rows


def _lauf3(pfad: str) -> dict[str, dict[str, dict[str, Any]]]:
    print("=== Lauf 3 — ohne Gabelung, Vollzustellung ===")
    print()
    root = Path(pfad)
    return {
        "l3_0": _lauf3_fall(
            str(root / "l3-0"),
            titel="L3-0 — keine Konfliktstimme",
            rivale=None,
            objekt_bekannt=False,
        ),
        "l3_1": _lauf3_fall(
            str(root / "l3-1"),
            titel="L3-1 — Rivale epoch_1, Objekt bekannt",
            rivale="b",
            objekt_bekannt=True,
        ),
        "l3_2": _lauf3_fall(
            str(root / "l3-2"),
            titel="L3-2 — Rivale epoch_2, Objekt bekannt",
            rivale="d",
            objekt_bekannt=True,
        ),
        "l3_3": _lauf3_fall(
            str(root / "l3-3"),
            titel="L3-3 — Rivale epoch_2, Objekt unbekannt",
            rivale="x",
            objekt_bekannt=False,
        ),
    }


def _hat(rows: list[str], kind: str) -> bool:
    return any(line.startswith(kind + " ") for line in rows)


def _arten(rows: list[str]) -> list[str]:
    return [line.split(" ", 1)[0] for line in rows]


def _arten_menge(row: dict[str, Any]) -> frozenset[str]:
    return frozenset(_arten(row["chain_findings"]))


def _identisch_beobachter(rows: dict[str, dict[str, Any]]) -> bool:
    indices = {rows[name]["index"] for name in NAMEN}
    karten = {_arten_menge(rows[name]) for name in NAMEN}
    return len(indices) == 1 and len(karten) == 1


def _hat_subjekt(findings: tuple[Finding, ...], subject: bytes) -> bool:
    return any(f.subject == subject for f in findings)


def _befunde(
    lauf1: dict[str, Any],
    lauf2: dict[str, Any],
    lauf3: dict[str, dict[str, dict[str, Any]]],
) -> None:
    print("=== Befunde ===")
    print()

    s1 = lauf1["stufe1"]
    abc = (s1[A], s1[B], s1[C])
    epochen_abc = {row["name"]: row["index"] for row in abc}
    vermerke_abc = {row["name"]: row["chain_findings"] for row in abc}
    leer_abc = all(not row["chain_findings"] for row in abc)
    epoche3_abc = all(row["index"] == 3 for row in abc)
    print(
        f"(Lauf 1 Stufe 1, anna/bruno/chris) Epochen={epochen_abc} "
        f"Vermerke={vermerke_abc}"
    )
    if epoche3_abc and leer_abc:
        print(
            "(Lauf 1 Stufe 1, anna/bruno/chris) bestätigt — Epoche 3, "
            "Vermerkliste leer."
        )
    else:
        print(
            "(Lauf 1 Stufe 1, anna/bruno/chris) widerlegt — "
            f"Epochen={epochen_abc}, Vermerke={vermerke_abc}."
        )
    print()

    dora1 = s1[Z]
    print(
        f"(Lauf 1 Stufe 1, dora) Epoche {dora1['index']} "
        f"hash={_kurz(dora1['constitution_hash'])} "
        f"Vermerke={dora1['chain_findings']}"
    )
    if dora1["index"] == 2 and not dora1["chain_findings"]:
        print(
            "(Lauf 1 Stufe 1, dora) bestätigt — Epoche 2, Vermerkliste leer "
            "(dauerhafte Divergenz ohne Vermerk)."
        )
    else:
        print(
            f"(Lauf 1 Stufe 1, dora) widerlegt — Epoche {dora1['index']}, "
            f"Vermerke={dora1['chain_findings']}."
        )
    print()

    dora2 = lauf1["stufe2_dora"]
    print(
        f"(Lauf 1 Stufe 2, dora) Epoche {dora2['index']} "
        f"hash={_kurz(dora2['constitution_hash'])} "
        f"Vermerke={dora2['chain_findings']}"
    )
    if dora2["index"] == 3:
        print("(Lauf 1 Stufe 2, dora) bestätigt — Epoche 3.")
    else:
        print(
            f"(Lauf 1 Stufe 2, dora) widerlegt — Epoche {dora2['index']}, "
            f"Vermerke={dora2['chain_findings']}."
        )
    print()

    g1 = lauf2["g1"]
    g1_conflict = _hat(g1["chain_findings"], "CONFLICTING_APPROVAL")
    g1_unsupported = _hat(g1["chain_findings"], "UNSUPPORTED_RATIFICATION")
    g1_ratify_c = _hat_subjekt(g1["findings"], lauf2["cid_ratify_c"])
    g1_pc = _hat_subjekt(g1["findings"], lauf2["hash_p_c"])
    print(
        f"(G1, bruno) Epoche {g1['index']} hash={_kurz(g1['constitution_hash'])} "
        f"Arten={_arten(g1['chain_findings'])} "
        f"subjekt_ratify_c={g1_ratify_c} subjekt_P_c={g1_pc} "
        f"Vermerke={g1['chain_findings']}"
    )
    if (
        g1["index"] == 1
        and g1_conflict
        and g1_unsupported
        and not g1_ratify_c
        and not g1_pc
    ):
        print(
            "(G1, bruno) bestätigt — Epoche 1, CONFLICTING_APPROVAL und "
            "UNSUPPORTED_RATIFICATION; kein Vermerk trägt cid(ratify_c) oder "
            "den Hash von P_c als Subjekt."
        )
    else:
        print(
            f"(G1, bruno) widerlegt — Epoche {g1['index']}, "
            f"CONFLICTING_APPROVAL={g1_conflict}, "
            f"UNSUPPORTED_RATIFICATION={g1_unsupported}, "
            f"subjekt_ratify_c={g1_ratify_c}, subjekt_P_c={g1_pc}, "
            f"Vermerke={g1['chain_findings']}."
        )
    print()

    g2 = lauf2["g2"]
    g2_conflict = _hat(g2["chain_findings"], "CONFLICTING_APPROVAL")
    g2_unsupported = _hat(g2["chain_findings"], "UNSUPPORTED_RATIFICATION")
    print(
        f"(G2, dora) Epoche {g2['index']} hash={_kurz(g2['constitution_hash'])} "
        f"Arten={_arten(g2['chain_findings'])} Vermerke={g2['chain_findings']}"
    )
    if g2["index"] == 2 and g2_conflict and g2_unsupported:
        print(
            "(G2, dora) bestätigt — Epoche 2, CONFLICTING_APPROVAL und "
            "UNSUPPORTED_RATIFICATION."
        )
    else:
        print(
            f"(G2, dora) widerlegt — Epoche {g2['index']}, "
            f"CONFLICTING_APPROVAL={g2_conflict}, "
            f"UNSUPPORTED_RATIFICATION={g2_unsupported}, "
            f"Vermerke={g2['chain_findings']}."
        )
    print()

    g3 = lauf2["g3"]
    g3_unknown = _hat(g3["chain_findings"], "UNKNOWN_PROPOSAL")
    g3_unsupported = _hat(g3["chain_findings"], "UNSUPPORTED_RATIFICATION")
    g3_unavailable = _hat(g3["chain_findings"], "EPOCH_PROPOSAL_UNAVAILABLE")
    print(
        f"(G3, anna) Epoche {g3['index']} hash={_kurz(g3['constitution_hash'])} "
        f"Arten={_arten(g3['chain_findings'])} Vermerke={g3['chain_findings']}"
    )
    if (
        g3["index"] == 1
        and g3_unknown
        and g3_unsupported
        and not g3_unavailable
    ):
        print(
            "(G3, anna) bestätigt — Epoche 1, UNKNOWN_PROPOSAL und "
            "UNSUPPORTED_RATIFICATION, kein EPOCH_PROPOSAL_UNAVAILABLE."
        )
    else:
        print(
            f"(G3, anna) widerlegt — Epoche {g3['index']}, "
            f"UNKNOWN_PROPOSAL={g3_unknown}, "
            f"UNSUPPORTED_RATIFICATION={g3_unsupported}, "
            f"EPOCH_PROPOSAL_UNAVAILABLE={g3_unavailable}, "
            f"Vermerke={g3['chain_findings']}."
        )
    print()

    g3p = lauf2["g3p"]
    g3p_unknown = _hat(g3p["chain_findings"], "UNKNOWN_PROPOSAL")
    g3p_conflict = _hat(g3p["chain_findings"], "CONFLICTING_APPROVAL")
    print(
        f"(G3', anna) Epoche {g3p['index']} hash={_kurz(g3p['constitution_hash'])} "
        f"Arten={_arten(g3p['chain_findings'])} "
        f"index_gleich_G2={g3p['index'] == g2['index']} "
        f"Vermerke={g3p['chain_findings']}"
    )
    if (
        g3p["index"] == g2["index"]
        and not g3p_unknown
        and g3p_conflict
    ):
        print(
            "(G3', anna) bestätigt — UNKNOWN_PROPOSAL verschwunden, "
            "CONFLICTING_APPROVAL vorhanden; index gleich dem von G2 "
            f"({g2['index']})."
        )
    else:
        print(
            f"(G3', anna) widerlegt — Epoche {g3p['index']} (G2={g2['index']}), "
            f"UNKNOWN_PROPOSAL={g3p_unknown}, "
            f"CONFLICTING_APPROVAL={g3p_conflict}, "
            f"Vermerke={g3p['chain_findings']}."
        )
    print()

    l30 = lauf3["l3_0"]
    l30_epochen = {name: l30[name]["index"] for name in NAMEN}
    l30_karten = {name: sorted(_arten_menge(l30[name])) for name in NAMEN}
    l30_leer = all(not l30[name]["chain_findings"] for name in NAMEN)
    l30_ep3 = all(l30[name]["index"] == 3 for name in NAMEN)
    print(f"(L3-0) Epochen={l30_epochen} Vermerkarten={l30_karten}")
    if l30_ep3 and l30_leer:
        print("(L3-0) bestätigt — alle vier Epoche 3, Vermerkliste leer.")
    else:
        print(
            f"(L3-0) widerlegt — Epochen={l30_epochen}, "
            f"Vermerkarten={l30_karten}."
        )
    print()
    print(
        f"(L3-0 Identität) identisch={_identisch_beobachter(l30)} "
        f"Epochen={l30_epochen} Vermerkarten={l30_karten}"
    )
    if _identisch_beobachter(l30):
        print(
            "(L3-0 Identität) bestätigt — alle vier Beobachter gleicher "
            "Index und gleiche Vermerkarten."
        )
    else:
        print(
            "(L3-0 Identität) widerlegt — ein Beobachter weicht ab: "
            f"Epochen={l30_epochen}, Vermerkarten={l30_karten}."
        )
    print()

    l31 = lauf3["l3_1"]
    l31_epochen = {name: l31[name]["index"] for name in NAMEN}
    l31_karten = {name: sorted(_arten_menge(l31[name])) for name in NAMEN}
    l31_ok = all(
        l31[name]["index"] == 1
        and _hat(l31[name]["chain_findings"], "CONFLICTING_APPROVAL")
        and _hat(l31[name]["chain_findings"], "UNSUPPORTED_RATIFICATION")
        for name in NAMEN
    )
    print(f"(L3-1) Epochen={l31_epochen} Vermerkarten={l31_karten}")
    if l31_ok:
        print(
            "(L3-1) bestätigt — alle vier Epoche 1, CONFLICTING_APPROVAL "
            "und UNSUPPORTED_RATIFICATION."
        )
    else:
        print(
            f"(L3-1) widerlegt — Epochen={l31_epochen}, "
            f"Vermerkarten={l31_karten}."
        )
    print()
    print(
        f"(L3-1 Identität) identisch={_identisch_beobachter(l31)} "
        f"Epochen={l31_epochen} Vermerkarten={l31_karten}"
    )
    if _identisch_beobachter(l31):
        print(
            "(L3-1 Identität) bestätigt — alle vier Beobachter gleicher "
            "Index und gleiche Vermerkarten."
        )
    else:
        print(
            "(L3-1 Identität) widerlegt — ein Beobachter weicht ab: "
            f"Epochen={l31_epochen}, Vermerkarten={l31_karten}."
        )
    print()

    l32 = lauf3["l3_2"]
    l32_epochen = {name: l32[name]["index"] for name in NAMEN}
    l32_karten = {name: sorted(_arten_menge(l32[name])) for name in NAMEN}
    l32_ok = all(
        l32[name]["index"] == 2
        and _hat(l32[name]["chain_findings"], "CONFLICTING_APPROVAL")
        and _hat(l32[name]["chain_findings"], "UNSUPPORTED_RATIFICATION")
        for name in NAMEN
    )
    print(f"(L3-2) Epochen={l32_epochen} Vermerkarten={l32_karten}")
    if l32_ok:
        print(
            "(L3-2) bestätigt — alle vier Epoche 2, CONFLICTING_APPROVAL "
            "und UNSUPPORTED_RATIFICATION."
        )
    else:
        print(
            f"(L3-2) widerlegt — Epochen={l32_epochen}, "
            f"Vermerkarten={l32_karten}."
        )
    print()
    print(
        f"(L3-2 Identität) identisch={_identisch_beobachter(l32)} "
        f"Epochen={l32_epochen} Vermerkarten={l32_karten}"
    )
    if _identisch_beobachter(l32):
        print(
            "(L3-2 Identität) bestätigt — alle vier Beobachter gleicher "
            "Index und gleiche Vermerkarten."
        )
    else:
        print(
            "(L3-2 Identität) widerlegt — ein Beobachter weicht ab: "
            f"Epochen={l32_epochen}, Vermerkarten={l32_karten}."
        )
    print()

    l33 = lauf3["l3_3"]
    l33_epochen = {name: l33[name]["index"] for name in NAMEN}
    l33_karten = {name: sorted(_arten_menge(l33[name])) for name in NAMEN}
    l33_ok = all(
        l33[name]["index"] == 1
        and _hat(l33[name]["chain_findings"], "UNKNOWN_PROPOSAL")
        and _hat(l33[name]["chain_findings"], "UNSUPPORTED_RATIFICATION")
        and not _hat(l33[name]["chain_findings"], "EPOCH_PROPOSAL_UNAVAILABLE")
        for name in NAMEN
    )
    print(f"(L3-3) Epochen={l33_epochen} Vermerkarten={l33_karten}")
    if l33_ok:
        print(
            "(L3-3) bestätigt — alle vier Epoche 1, UNKNOWN_PROPOSAL und "
            "UNSUPPORTED_RATIFICATION, kein EPOCH_PROPOSAL_UNAVAILABLE."
        )
    else:
        print(
            f"(L3-3) widerlegt — Epochen={l33_epochen}, "
            f"Vermerkarten={l33_karten}."
        )
    print()
    print(
        f"(L3-3 Identität) identisch={_identisch_beobachter(l33)} "
        f"Epochen={l33_epochen} Vermerkarten={l33_karten}"
    )
    if _identisch_beobachter(l33):
        print(
            "(L3-3 Identität) bestätigt — alle vier Beobachter gleicher "
            "Index und gleiche Vermerkarten."
        )
    else:
        print(
            "(L3-3 Identität) widerlegt — ein Beobachter weicht ab: "
            f"Epochen={l33_epochen}, Vermerkarten={l33_karten}."
        )


def main() -> None:
    print("Szenario G — zweistufige Epochenkette unter Teilwissen (00ax)")
    print("A=anna  B=bruno  C=chris  Z=dora")
    print()
    with tempfile.TemporaryDirectory() as tmp:
        lauf1 = _lauf1(str(Path(tmp) / "lauf1"))
        lauf2 = _lauf2(str(Path(tmp) / "lauf2"))
        lauf3 = _lauf3(str(Path(tmp) / "lauf3"))
    _befunde(lauf1, lauf2, lauf3)


if __name__ == "__main__":
    main()
