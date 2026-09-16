#!/usr/bin/env python3
"""Prüft die Zuordnung der Fragenlisten und den Index (D384, D385, D386, D387, D395).

Liest die Adressen aus ``fragen-adressen.md`` oder, bei Markerzeile, aus der Liste
selbst (D395 Beschluss 1); extrahiert keine (D386 Beschluss 2).
Ohne Argument nur prüfen; ``--schreiben`` erzeugt ``fragen-index.md`` (D387 Beschluss 4).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parent.parent

SECTION = re.compile(r"^## \d+\. `([^`]+)` — ")
LIST_HEADING = re.compile(r"^## (\d+)\. ", re.M)
ADDR_PART = re.compile(
    r"(?:AUFTRAG|WERKZEUG|"
    r"\d+[a-z]? (?:§\d+(?:\.\d+)*|Anhang [A-Z](?:\.\d+)*))"
)
ADDR_CELL = re.compile(rf"^{ADDR_PART.pattern}(?: / {ADDR_PART.pattern})*$")
SUFFIX = re.compile(r"-(\d+)$")
LAYER = re.compile(r"^(\d+)([a-z]?)$")
ADDR_ZEILE = re.compile(r"^- \*\*Adresse:\*\* (.+)$")
FRAGEN_DATEI = re.compile(r"^FRAGEN(?:-\d+)?\.md$")
MARKER = "Adressen: in der Liste."


class Liste(NamedTuple):
    """Eine zugeordnete Fragenliste aus ``fragen-adressen.md`` (D386 Beschluss 1)."""

    pfad: str
    zeilen: list[tuple[int, str]]


def kurzform(pfad: str) -> str:
    """Verzeichnisname plus Suffixziffer, falls die Datei eine trägt."""
    teile = Path(pfad).parts
    verzeichnis = teile[0]
    fund = SUFFIX.search(Path(pfad).stem)
    if fund is None:
        return verzeichnis
    return f"{verzeichnis}{fund.group(1)}"


def teile_von(zelle: str) -> list[str]:
    """Adressteile einer Zelle, getrennt durch `` / `` (D385 Beschluss 1)."""
    return zelle.split(" / ")


def adresse_wohlgeformt(zelle: str) -> bool:
    """Kanonische Adressform aus D385 Beschluss 1."""
    return ADDR_CELL.fullmatch(zelle) is not None


def sortierschluessel(adresse: str) -> tuple[int, int, str, int, tuple[object, ...]]:
    """Ordnung der Indexzeilen (D387 Beschluss 3, D385 Beschluss 4)."""
    if adresse == "AUFTRAG":
        return (1, 0, "", 0, ())
    if adresse == "WERKZEUG":
        return (2, 0, "", 0, ())
    quelle, _, stelle = adresse.partition(" ")
    fund = LAYER.fullmatch(quelle)
    if fund is None:
        return (3, 0, adresse, 0, ())
    layer_nr = int(fund.group(1))
    layer_sfx = fund.group(2)
    if stelle.startswith("§"):
        zahlen = tuple(int(x) for x in stelle[1:].split("."))
        return (0, layer_nr, layer_sfx, 0, zahlen)
    rest = stelle.removeprefix("Anhang ")
    buchstabe, *zahlen_s = rest.split(".")
    anhang = (buchstabe, *tuple(int(x) for x in zahlen_s))
    return (0, layer_nr, layer_sfx, 1, anhang)


def ueberschriften(text: str) -> list[int]:
    """Eintragsnummern der Form ``## <n>. <titel>`` in Dateireihenfolge."""
    return [int(n) for n in LIST_HEADING.findall(text)]


def _zellen(zeile: str) -> list[str]:
    return [teil.strip() for teil in zeile.strip().strip("|").split("|")]


def _ist_trenner(zellen: list[str]) -> bool:
    return bool(zellen) and all(z and set(z) <= set("-:") for z in zellen)


def zeilen_aus_liste(pfad: str) -> tuple[list[tuple[int, str]], list[str]]:
    """Adresszeilen einer selbsttragenden Liste (D395 Beschluss 2)."""
    probleme: list[str] = []
    zeilen: list[tuple[int, str]] = []
    ziel = ROOT / pfad
    if not ziel.is_file():
        return zeilen, probleme
    letzte: int | None = None
    anzahl: dict[int, int] = {}
    koepfe: list[int] = []
    for zeile in ziel.read_text(encoding="utf-8").splitlines():
        kopf = LIST_HEADING.match(zeile)
        if kopf is not None:
            letzte = int(kopf.group(1))
            koepfe.append(letzte)
            continue
        fund = ADDR_ZEILE.fullmatch(zeile)
        if fund is None:
            continue
        zelle = fund.group(1)
        if letzte is None:
            probleme.append(
                f"Adresszeile vor der ersten Überschrift in `{pfad}`: {zeile}"
            )
            continue
        anzahl[letzte] = anzahl.get(letzte, 0) + 1
        if anzahl[letzte] > 1:
            probleme.append(
                f"mehr als eine Adresszeile in `{pfad}` Nr. {letzte}"
            )
            continue
        if not adresse_wohlgeformt(zelle):
            probleme.append(
                f"Adresse nicht wohlgeformt in `{pfad}` Nr. {letzte}: `{zelle}`"
            )
        zeilen.append((letzte, zelle))
    ohne = [nr for nr in koepfe if anzahl.get(nr, 0) == 0]
    if ohne:
        probleme.append(
            "Überschrift ohne Adresszeile in `"
            + pfad
            + "`: "
            + ", ".join(str(n) for n in ohne)
        )
    return zeilen, probleme


def listen_aus(text: str) -> tuple[list[Liste], list[str]]:
    """Abschnitte aus ``fragen-adressen.md``: Tabelle oder Marker (D395 Beschluss 1, 3)."""
    probleme: list[str] = []
    listen: list[Liste] = []
    pfad: str | None = None
    zeilen: list[tuple[int, str]] | None = None
    in_tabelle = False
    hat_tabelle = False
    hat_marker = False

    def ablegen() -> None:
        nonlocal pfad, zeilen, in_tabelle, hat_tabelle, hat_marker
        if pfad is not None and zeilen is not None:
            if hat_tabelle == hat_marker:
                if hat_tabelle:
                    probleme.append(
                        f"Abschnitt `{pfad}` hat Tabelle und Marker"
                    )
                    zeilen = []
                else:
                    probleme.append(
                        f"Abschnitt `{pfad}` hat weder Tabelle noch Marker"
                    )
            elif hat_marker:
                gelesen, extra = zeilen_aus_liste(pfad)
                probleme.extend(extra)
                zeilen = gelesen
            listen.append(Liste(pfad, zeilen))
        pfad = None
        zeilen = None
        in_tabelle = False
        hat_tabelle = False
        hat_marker = False

    for zeile in text.splitlines():
        if zeile.startswith("## "):
            ablegen()
            fund = SECTION.match(zeile)
            if fund is None:
                probleme.append(f"Abschnitt nicht in der Form: {zeile}")
                continue
            pfad = fund.group(1)
            zeilen = []
            continue
        if pfad is None or zeilen is None:
            continue
        if zeile == MARKER:
            hat_marker = True
            continue
        if not in_tabelle:
            if not zeile.startswith("|"):
                continue
            if _zellen(zeile)[:2] == ["Nr", "Adresse"]:
                in_tabelle = True
                hat_tabelle = True
            continue
        if not zeile.startswith("|"):
            in_tabelle = False
            continue
        zellen = _zellen(zeile)
        if _ist_trenner(zellen):
            continue
        if len(zellen) < 2:
            probleme.append(f"Zeile ohne Adresse in `{pfad}`: {zeile}")
            continue
        try:
            nr = int(zellen[0])
        except ValueError:
            probleme.append(f"Nr nicht lesbar in `{pfad}`: {zellen[0]}")
            continue
        zeilen.append((nr, zellen[1]))

    ablegen()
    return listen, probleme


def vollstaendigkeit_pruefen(listen: list[Liste]) -> list[str]:
    """FRAGEN-Dateien ausserhalb ``archiv/`` ohne Abschnitt (D395 Beschluss 4)."""
    genannt = {liste.pfad for liste in listen}
    probleme: list[str] = []
    for kind in sorted(ROOT.iterdir()):
        if not kind.is_dir() or kind.name == "archiv":
            continue
        for datei in sorted(kind.iterdir()):
            if not datei.is_file():
                continue
            if FRAGEN_DATEI.fullmatch(datei.name) is None:
                continue
            rel = f"{kind.name}/{datei.name}"
            if rel not in genannt:
                probleme.append(f"Fragenliste ohne Abschnitt: {rel}")
    return probleme


def nummern_befunde(nummern: list[int], name: str) -> list[str]:
    """Lücken und Dubletten ab 1, Form wie in ``tools/offen.py`` (D316)."""
    if not nummern:
        return [f"keine Zeilen in `{name}`"]
    probleme: list[str] = []
    gesehen: set[int] = set()
    for num in nummern:
        if num in gesehen:
            probleme.append(f"{num} doppelt in `{name}`")
        gesehen.add(num)
    fehlend = sorted(set(range(1, max(nummern) + 1)) - gesehen)
    if fehlend:
        probleme.append(
            "fehlend in `" + name + "`: " + ", ".join(str(n) for n in fehlend)
        )
    return probleme


def zuordnung_pruefen(listen: list[Liste]) -> list[str]:
    """Pfade, Nummern, Adressform (D385 Beschluss 1, D386 Beschluss 2)."""
    probleme: list[str] = []
    for liste in listen:
        ziel = ROOT / liste.pfad
        if not ziel.is_file():
            probleme.append(f"Pfad fehlt: {liste.pfad}")
            continue
        tabellen_nr = [nr for nr, _zelle in liste.zeilen]
        probleme += nummern_befunde(tabellen_nr, liste.pfad)
        koepfe = ueberschriften(ziel.read_text(encoding="utf-8"))
        nur_liste = sorted(set(koepfe) - set(tabellen_nr))
        nur_tabelle = sorted(set(tabellen_nr) - set(koepfe))
        if nur_liste:
            probleme.append(
                "Überschrift ohne Zeile in `"
                + liste.pfad
                + "`: "
                + ", ".join(str(n) for n in nur_liste)
            )
        if nur_tabelle:
            probleme.append(
                "Zeile ohne Überschrift in `"
                + liste.pfad
                + "`: "
                + ", ".join(str(n) for n in nur_tabelle)
            )
        for nr, zelle in liste.zeilen:
            if not adresse_wohlgeformt(zelle):
                probleme.append(
                    f"Adresse nicht wohlgeformt in `{liste.pfad}` Nr. {nr}: `{zelle}`"
                )
    return probleme


def matrix_von(
    listen: list[Liste],
) -> tuple[list[str], dict[str, list[list[int]]], int, int]:
    """Spalten, Adresse → Nummern je Fassung, Einträge, Nennungen (D387)."""
    spalten = [kurzform(liste.pfad) for liste in listen]
    matrix: dict[str, list[list[int]]] = {}
    eintraege = 0
    nennungen = 0
    for index, liste in enumerate(listen):
        for nr, zelle in liste.zeilen:
            eintraege += 1
            for teil in teile_von(zelle):
                nennungen += 1
                if teil not in matrix:
                    matrix[teil] = [[] for _ in spalten]
                matrix[teil][index].append(nr)
    return spalten, matrix, eintraege, nennungen


def index_text(listen: list[Liste]) -> str:
    """``fragen-index.md`` aus der Zuordnung (D387 Beschluss 1, 2, 3)."""
    spalten, matrix, eintraege, nennungen = matrix_von(listen)
    adressen = sorted(matrix, key=sortierschluessel)
    n_adressen = len(adressen)
    koepfe = ["Adresse", *spalten, "Σ"]
    trenner = ["---"] * len(koepfe)
    zeilen = [
        "# Fragen-Index",
        "",
        "Erzeugt aus `fragen-adressen.md` und den dort angemeldeten Listen durch",
        "`tools/check_fragen.py --schreiben`.",
        "Nicht von Hand ändern — was hier falsch steht, wird in der Zuordnung korrigiert.",
        "",
        f"Einträge: {eintraege}. Nennungen: {nennungen}. Adressen: {n_adressen}. "
        f"Die Summe der Spalte `Σ` ist `{nennungen}` und nicht",
        f"`{eintraege}`: ein Eintrag mit mehreren Adressen steht in jeder seiner "
        "Zeilen (D387 Beschluss 2).",
        "",
        "## 1. Die Matrix",
        "",
        "| " + " | ".join(koepfe) + " |",
        "| " + " | ".join(trenner) + " |",
    ]
    for adresse in adressen:
        spaltenwerte = matrix[adresse]
        zellen: list[str] = []
        sigma = 0
        for nummern in spaltenwerte:
            sigma += len(nummern)
            if nummern:
                zellen.append(", ".join(str(n) for n in sorted(nummern)))
            else:
                zellen.append("—")
        zeilen.append("| " + " | ".join([adresse, *zellen, str(sigma)]) + " |")
    zeilen.append("")
    return "\n".join(zeilen)


def main(argv: list[str] | None = None) -> int:
    """Prüft die Zuordnung; mit ``--schreiben`` entsteht der Index (D387 Beschluss 4, D395)."""
    args = sys.argv[1:] if argv is None else argv
    schreiben = "--schreiben" in args
    quelle = ROOT / "fragen-adressen.md"
    if not quelle.is_file():
        print("fragen-adressen.md fehlt")
        return 1
    listen, probleme = listen_aus(quelle.read_text(encoding="utf-8"))
    probleme += zuordnung_pruefen(listen)
    probleme += vollstaendigkeit_pruefen(listen)
    erwartet = index_text(listen)
    ziel = ROOT / "fragen-index.md"
    if schreiben:
        ziel.write_text(erwartet, encoding="utf-8")
    if ziel.is_file():
        if ziel.read_bytes() != erwartet.encode("utf-8"):
            probleme.append("fragen-index.md weicht von der Zuordnung ab")
    else:
        probleme.append("fragen-index.md fehlt")
    if probleme:
        for problem in probleme:
            print(problem)
        return 1
    print(sum(len(liste.zeilen) for liste in listen))
    return 0


if __name__ == "__main__":
    sys.exit(main())
