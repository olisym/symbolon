"""Gründung aus einer Vorlage (D641 Beschluss 2, 00 §4, 00 §4.1, 00 §4.2, 00 §5)."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass

from symbolon import cbor_canon
from symbolon.genesis import genesis_scope
from symbolon.governance.objects import epoch_id
from symbolon.governance.tally import TallyState
from symbolon.node.store import ObjectKind, SqliteStore
from symbolon.node.view import scope_view
from symbolon.policy import constitution_hash
from symbolon.profiles.membership import MembershipState

# Heute nur verein. Gelesen wird bei jedem Aufruf, die Tests tauschen den Eintrag aus
# (D641 Beschluss 2).
VORLAGEN: dict[str, dict[str, object]] = {
    "verein": {
        "mindestens": 3,
        "felder": ("name", "sitz", "zweck", "beitrag"),
        "pflicht": ("name", "sitz", "zweck"),
        "geschuetzt": ("name", "vorlage", "zweck"),
        "fassung": 1,
        "typen": {"name": "text", "sitz": "text", "zweck": "text", "beitrag": "betrag"},
        "thresholds": {
            "ordinary": [1, 2],
            "membership": [1, 2],
            "amendment": [2, 3],
        },
        "irrevocable_verein": ["obligation@1", "ratify@1", "vote@1"],
        "irrevocable_vereinsleben": ["obligation@1"],
        "amendment_rule": 2,
        "trust_params": {0: 100, 1: 1, 2: 2, 3: 100},
    },
}


# Ziffern 0 bis 9, nicht die Unicode-Klasse \d (D648 Beschluss 2, D648 Befund 4).
_BETRAG = re.compile(r"(0|[1-9][0-9]{0,6}),[0-9]{2} EUR im (Monat|Jahr)")


def wert_gueltig(typ: object, wert: object) -> bool:
    """Ob ``wert`` zum Typ der Vorlage passt (D648 Beschluss 2, D496).

    Falsch, wenn ``wert`` kein Text ist, leer ist, Leerraum am Rand oder einen Zeilenumbruch
    trägt oder nicht in NFC steht. ``text`` ist sonst wahr, ``betrag`` nur in der Form
    ``(0|[1-9][0-9]{0,6}),[0-9]{2} EUR im (Monat|Jahr)`` und nicht ``0,00``. Jeder andere Typ
    ist falsch. Kein Wert und kein Typ wirft.
    """
    if not isinstance(wert, str) or wert == "" or wert != wert.strip():
        return False
    if "\n" in wert or "\r" in wert:
        return False
    if not unicodedata.is_normalized("NFC", wert):
        return False
    if typ == "text":
        return True
    if typ != "betrag":
        return False
    if _BETRAG.fullmatch(wert) is None or wert.startswith("0,00"):
        return False
    return True


def vorlage_der_satzung(stand: object) -> dict[str, object] | None:
    """Der Eintrag von ``VORLAGEN``, den ``stand`` als ``<name>@<fassung>`` nennt, sonst
    ``None`` (D648 Beschluss 3).

    ``VORLAGEN`` wird bei jedem Aufruf gelesen. Kein Wert wirft.
    """
    if not isinstance(stand, Mapping):
        return None
    try:
        genannt = stand.get("vorlage")
    except Exception:
        return None
    if not isinstance(genannt, str):
        return None
    for name, eintrag in VORLAGEN.items():
        if genannt == f"{name}@{eintrag['fassung']}":
            return eintrag
    return None


def feld_abweisung(muster: Mapping[str, object], feld: str, wert: str | None) -> str | None:
    """Abweisung eines Sachfelds gegen die Vorlage, sonst ``None`` (D648 Beschluss 4).

    ``wert`` ``None`` heisst entfernen. ``vorlage`` ist bei jedem Wert ``RESERVED_FIELD``.
    Ein Feld ohne Eintrag in ``typen`` bleibt ungeprüft.
    """
    if feld == "vorlage":
        return "RESERVED_FIELD"
    typen = muster["typen"]
    if feld not in typen:
        return None
    if wert is None:
        if feld in muster["pflicht"]:
            return "MISSING_FIELD"
        return None
    if not wert_gueltig(typen[feld], wert):
        return "INVALID_VALUE"
    return None


class Abgewiesen(Exception):
    """Abweisung einer Gründung unter ihrem Namen (D641 Beschluss 4)."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.name = name


@dataclass(frozen=True, slots=True)
class Gruendung:
    """Vier Objekte in zwei Scopes (D641 Beschluss 3, 00 §4, 00 §4.1, 00 §4.2, 00 §5)."""

    verein: bytes
    vereinsleben: bytes
    constitution: bytes
    objekte: tuple[tuple[ObjectKind, bytes], ...]


def gruenden(vorlage: object, gruender: object, felder: object) -> Gruendung:
    """Vier Objekte, jede Satzung vor ihrem Genesis (D641 Beschluss 3, 00 §4, 00 §4.1, 00 §5).

    Führt die Vorlage ``geschuetzt`` und ist es nicht leer, steht ``protected_fields`` nach den
    Bytes der UTF-8-Kodierung sortiert in der Satzung des Vereins, nie im Vereinsleben
    (04 §1.1, D646). Jeder gereichte Wert muss zu seinem Typ passen, sonst ``INVALID_VALUE``;
    die Satzung des Vereins nennt ``vorlage`` als ``<vorlage>@<fassung>`` (D648).
    """
    if not isinstance(vorlage, str) or vorlage not in VORLAGEN:
        raise Abgewiesen("UNKNOWN_TEMPLATE")
    muster = VORLAGEN[vorlage]
    if not isinstance(gruender, list):
        raise Abgewiesen("INVALID_FOUNDERS")
    schluessel: list[bytes] = []
    for eintrag in gruender:
        if not isinstance(eintrag, str):
            raise Abgewiesen("INVALID_FOUNDERS")
        try:
            roh = bytes.fromhex(eintrag)
        except ValueError:
            raise Abgewiesen("INVALID_FOUNDERS") from None
        if len(roh) != 32:
            raise Abgewiesen("INVALID_FOUNDERS")
        schluessel.append(roh)
    if len(set(schluessel)) != len(schluessel):
        raise Abgewiesen("INVALID_FOUNDERS")
    if len(schluessel) < muster["mindestens"]:
        raise Abgewiesen("TOO_FEW_FOUNDERS")
    schluessel = sorted(schluessel)
    if not isinstance(felder, Mapping):
        raise Abgewiesen("INVALID_FIELDS")
    erlaubt = muster["felder"]
    werte: dict[str, str] = {}
    for name, wert in felder.items():
        if name not in erlaubt:
            raise Abgewiesen("UNKNOWN_FIELD")
        if not isinstance(wert, str):
            raise Abgewiesen("INVALID_FIELDS")
        werte[name] = wert
    pflicht = muster["pflicht"]
    for name in pflicht:
        if name not in werte or werte[name] == "":
            raise Abgewiesen("MISSING_FIELD")
    typen = muster["typen"]
    for name, wert in werte.items():
        if not wert_gueltig(typen[name], wert):
            raise Abgewiesen("INVALID_VALUE")
    schwellen = {
        name: list(paar) for name, paar in muster["thresholds"].items()
    }
    satzung: dict[str, object] = dict(werte)
    satzung["irrevocable_predicates"] = list(muster["irrevocable_verein"])
    satzung["thresholds"] = schwellen
    satzung["arbitration"] = {"arbitrators": list(schluessel)}
    satzung["participants"] = list(schluessel)
    if "geschuetzt" in muster and muster["geschuetzt"]:
        satzung["protected_fields"] = sorted(
            muster["geschuetzt"], key=lambda name: name.encode("utf-8")
        )
    satzung["vorlage"] = f"{vorlage}@{muster['fassung']}"
    leben: dict[str, object] = {
        "irrevocable_predicates": list(muster["irrevocable_vereinsleben"]),
        "thresholds": {name: list(paar) for name, paar in schwellen.items()},
        "arbitration": {"arbitrators": list(schluessel)},
    }
    hash_satzung = constitution_hash(satzung)
    genesis: dict[int, object] = {
        0: 1,
        1: list(schluessel),
        2: 0,
        3: list(schluessel),
        4: hash_satzung,
        5: muster["amendment_rule"],
        6: 0,
        7: 0,
    }
    verein = genesis_scope(genesis)
    hash_leben = constitution_hash(leben)
    genesis_leben: dict[int, object] = {
        0: 1,
        1: list(schluessel),
        2: 0,
        3: list(schluessel),
        4: hash_leben,
        5: muster["amendment_rule"],
        6: 0,
        7: 0,
        8: verein,
        9: dict(muster["trust_params"]),
    }
    gebaut = Gruendung(
        verein=verein,
        vereinsleben=genesis_scope(genesis_leben),
        constitution=hash_satzung,
        objekte=(
            (ObjectKind.CONSTITUTION, cbor_canon.encode(satzung)),
            (ObjectKind.GENESIS, cbor_canon.encode(genesis)),
            (ObjectKind.CONSTITUTION, cbor_canon.encode(leben)),
            (ObjectKind.GENESIS, cbor_canon.encode(genesis_leben)),
        ),
    )
    probelauf(gebaut)
    return gebaut


def probelauf(gruendung: Gruendung) -> None:
    """Probe im leeren Bestand, sonst UNSOUND_TEMPLATE (D641 Beschluss 5, 00 §4.2, 00 §5)."""
    store = SqliteStore(":memory:")
    try:
        try:
            for art, daten in gruendung.objekte:
                store.submit_object(art, daten)
            satzung = cbor_canon.decode(gruendung.objekte[0][1])
            vorgaenger = epoch_id(gruendung.verein, 1, gruendung.constitution)
            text = dict(satzung)
            text["probe"] = "a"
            store.submit_object(ObjectKind.CONSTITUTION, cbor_canon.encode(text))
            vorschlag = {0: gruendung.verein, 1: vorgaenger, 2: constitution_hash(text)}
            store.submit_object(ObjectKind.PROPOSAL, cbor_canon.encode(vorschlag))
            aufnahme = dict(satzung)
            fremd = b"\xff" * 32
            if fremd in satzung["participants"]:
                fremd = b"\xfe" * 32
            aufnahme["participants"] = sorted([*satzung["participants"], fremd])
            store.submit_object(ObjectKind.CONSTITUTION, cbor_canon.encode(aufnahme))
            vorschlag = {
                0: gruendung.verein,
                1: vorgaenger,
                2: constitution_hash(aufnahme),
            }
            store.submit_object(ObjectKind.PROPOSAL, cbor_canon.encode(vorschlag))
            bewegung = {0: gruendung.verein, 1: vorgaenger, 2: {"probe": [[], ["a"]]}}
            store.submit_object(ObjectKind.MOTION, cbor_canon.encode(bewegung))
            sicht = scope_view(store, gruendung.verein, 0)
            leben = scope_view(store, gruendung.vereinsleben, 0)
        except Exception:
            raise Abgewiesen("UNSOUND_TEMPLATE") from None
        if sicht.findings or sicht.verein is None:
            raise Abgewiesen("UNSOUND_TEMPLATE")
        if leben.findings or leben.vereinsleben is None:
            raise Abgewiesen("UNSOUND_TEMPLATE")
        staende = dict(sicht.verein.membership)
        for wer in satzung["participants"]:
            stand = staende.get(wer)
            if stand is None or stand.state is not MembershipState.GRANT_ONLY:
                raise Abgewiesen("UNSOUND_TEMPLATE")
        verfassungen = store.all_constitutions()
        vorschlaege = store.all_proposals()
        sachantraege = store.all_motions()
        arten: list[str] = []
        for digest, ergebnis in sicht.verein.decisions:
            if ergebnis.state is not TallyState.PENDING or ergebnis.findings:
                raise Abgewiesen("UNSOUND_TEMPLATE")
            if digest in sachantraege:
                arten.append("sach")
                continue
            ziel = verfassungen[vorschlaege[digest].constitution_hash]
            gleiche = list(ziel["participants"]) == list(satzung["participants"])
            arten.append("text" if gleiche else "aufnahme")
        if sorted(arten) != ["aufnahme", "sach", "text"]:
            raise Abgewiesen("UNSOUND_TEMPLATE")
    finally:
        store.close()
