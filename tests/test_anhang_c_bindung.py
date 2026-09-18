"""Anhang C an vectors_01.json binden (D413; 01 Anhang C.0)."""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import pytest

_SPEC = Path(__file__).resolve().parent.parent / "01-claim-atom.md"
_VECTORS = Path(__file__).resolve().parent / "vectors" / "vectors_01.json"
_NAME = re.compile(r"(?:TV|NV|BV)\d+")
_HEX = re.compile(r"[0-9a-f]+")
_HEX_LABELS = frozenset({"bytes", "claim_id", "σ"})
_KNOWN_LABELS = _HEX_LABELS | frozenset({"erwartet", "core"})
_FELDARTEN = ("core_bytes", "wire_bytes", "claim_id", "sigma", "expect_reject")
_REJECT = re.compile(r"Reject: ([A-Z0-9_]+)\Z")
_UNLABELED = ""


@dataclass
class _Stelle:
    zeile: int
    ziffer: int


@dataclass
class _Block:
    name: str
    anfang: int
    ende: int
    roh: dict[str, str] = field(default_factory=dict)
    stellen: dict[str, _Stelle] = field(default_factory=dict)
    erwartet: str | None = None
    erwartet_zeile: int | None = None
    label_befunde: list[str] = field(default_factory=list)
    unlab_bei_sigma: bool = False


def _datei() -> dict:
    return json.loads(_VECTORS.read_text(encoding="utf-8"))


def _spec_text() -> str:
    return _SPEC.read_text(encoding="utf-8")


def _eigentuemer(zeile: str) -> str:
    titel = re.sub(r"^#{3,4}\s+", "", zeile)
    genannt = titel.split("—", 1)[0]
    namen = _NAME.findall(genannt)
    if len(namen) == 1:
        return namen[0]
    return ""


def _letzte_hexziffer(zeile: str) -> int:
    rumpf = zeile.split(";", 1)[0]
    for i in range(len(rumpf) - 1, -1, -1):
        if rumpf[i] in "0123456789abcdef":
            return i
    raise AssertionError("Hexzeile ohne Ziffer")


def _anhang_grenzen(zeilen: list[str]) -> tuple[int, int] | None:
    start = next(
        (i for i, zeile in enumerate(zeilen) if zeile.startswith("## Anhang C")),
        None,
    )
    ende = next(
        (
            i
            for i, zeile in enumerate(zeilen)
            if zeile.startswith("## Änderungshistorie")
        ),
        None,
    )
    if start is None or ende is None or ende <= start:
        return None
    return start, ende


def _block_auswerten(name: str, körper: list[tuple[int, str]]) -> _Block:
    block = _Block(name=name, anfang=-1, ende=-1)
    offen: str | None = None
    erwartet_offen = False
    for idx, rohzeile in körper:
        schnitt = rohzeile.split(";", 1)[0]
        if not schnitt.strip():
            continue
        eingerueckt = schnitt[0].isspace()
        nackt = schnitt.strip()
        if erwartet_offen:
            continue
        if "==" in nackt or "dekodiert zu" in nackt:
            offen = None
            continue
        if not eingerueckt:
            zuweisung = re.match(r"^(\S+)\s+=\s*(.*)$", nackt)
            if zuweisung is not None:
                label, wert = zuweisung.group(1), zuweisung.group(2).strip()
                if label not in _KNOWN_LABELS:
                    block.label_befunde.append(f"{name}: Label {label}")
                    offen = None
                    continue
                if label == "erwartet":
                    block.erwartet = wert
                    block.erwartet_zeile = idx
                    erwartet_offen = True
                    offen = None
                    continue
                if label == "core":
                    offen = None
                    continue
                if label in _HEX_LABELS and _HEX.fullmatch(wert):
                    block.roh[label] = wert
                    block.stellen[label] = _Stelle(idx, _letzte_hexziffer(rohzeile))
                    offen = label
                    continue
                offen = None
                continue
            if nackt.endswith(":"):
                offen = _UNLABELED
                continue
        if eingerueckt and _HEX.fullmatch(nackt):
            if offen is None:
                offen = _UNLABELED
                block.roh[offen] = nackt
                block.stellen[offen] = _Stelle(idx, _letzte_hexziffer(rohzeile))
            else:
                block.roh[offen] = block.roh.get(offen, "") + nackt
            continue
        offen = None
    return block


def _bloecke(text: str) -> list[_Block]:
    zeilen = text.splitlines(keepends=True)
    grenzen = _anhang_grenzen(zeilen)
    if grenzen is None:
        return []
    start, ende = grenzen
    eigentuemer = ""
    im_block = False
    anfang = -1
    körper: list[tuple[int, str]] = []
    gefunden: list[_Block] = []
    for i in range(start, ende):
        zeile = zeilen[i]
        if zeile.strip() == "```":
            if im_block:
                if eigentuemer:
                    block = _block_auswerten(eigentuemer, körper)
                    block.anfang = anfang
                    block.ende = i
                    gefunden.append(block)
                körper = []
                im_block = False
            else:
                im_block = True
                anfang = i
            continue
        if im_block:
            körper.append((i, zeile))
            continue
        if zeile.startswith("#### ") or zeile.startswith("### "):
            eigentuemer = _eigentuemer(zeile)
    return gefunden


def _zuordnen(block: _Block) -> dict[str, str]:
    werte: dict[str, str] = {}
    traegt_sigma = "σ" in block.roh
    if "bytes" in block.roh:
        if traegt_sigma:
            werte["core_bytes"] = block.roh["bytes"]
        else:
            werte["wire_bytes"] = block.roh["bytes"]
    if _UNLABELED in block.roh:
        werte["wire_bytes"] = block.roh[_UNLABELED]
        if traegt_sigma:
            block.unlab_bei_sigma = True
    if "claim_id" in block.roh:
        werte["claim_id"] = block.roh["claim_id"]
    if traegt_sigma:
        werte["sigma"] = block.roh["σ"]
    if block.erwartet is not None:
        reject = _REJECT.fullmatch(block.erwartet)
        if reject is not None:
            werte["expect_reject"] = reject.group(1)
        else:
            werte["erwartet_prosa"] = block.erwartet
    return werte


def _stellen_der_werte(block: _Block, werte: dict[str, str]) -> dict[str, _Stelle]:
    stellen: dict[str, _Stelle] = {}
    traegt_sigma = "σ" in block.roh
    if "core_bytes" in werte and "bytes" in block.stellen:
        stellen["core_bytes"] = block.stellen["bytes"]
    if "wire_bytes" in werte:
        if _UNLABELED in block.stellen:
            stellen["wire_bytes"] = block.stellen[_UNLABELED]
        elif "bytes" in block.stellen and not traegt_sigma:
            stellen["wire_bytes"] = block.stellen["bytes"]
    if "claim_id" in werte and "claim_id" in block.stellen:
        stellen["claim_id"] = block.stellen["claim_id"]
    if "sigma" in werte and "σ" in block.stellen:
        stellen["sigma"] = block.stellen["σ"]
    if "expect_reject" in werte and block.erwartet_zeile is not None:
        stellen["expect_reject"] = _Stelle(block.erwartet_zeile, -1)
    return stellen


def befunde(text: str) -> list[str]:
    """Reine Funktion über den Spec-Text: Anhang C gegen vectors_01.json (D413)."""
    datei = _datei()
    nach_name = {vektor["name"]: vektor for vektor in datei["vectors"]}
    result: list[str] = []
    zeilen = text.splitlines(keepends=True)
    if _anhang_grenzen(zeilen) is None:
        return ["Anhang C fehlt"]
    bloecke = _bloecke(text)
    zaehlung = Counter(block.name for block in bloecke)
    for name in nach_name:
        n = zaehlung.get(name, 0)
        if n != 1:
            result.append(f"{name}: {n} Blöcke")
    for block in bloecke:
        if block.name not in nach_name:
            result.append(f"{block.name}: Datei kennt den Namen nicht")
            continue
        result.extend(block.label_befunde)
        werte = _zuordnen(block)
        if block.unlab_bei_sigma:
            result.append(f"{block.name}: unbeschriftetes Hexfeld bei σ")
        vektor = nach_name[block.name]
        for art, wert in werte.items():
            if art == "erwartet_prosa":
                if "expect_reject" in vektor:
                    result.append(
                        f"{block.name}: erwartet ist Prosa, Datei trägt expect_reject"
                    )
                continue
            if art not in vektor:
                result.append(f"{block.name}: {art} nicht in der Datei")
            elif vektor[art] != wert:
                result.append(f"{block.name}: {art} weicht ab")
        for art in ("claim_id", "sigma", "wire_bytes", "expect_reject"):
            if art in vektor and art not in werte:
                result.append(f"{block.name}: {art} fehlt im Text")
    return result


def _erste_stelle(text: str, art: str) -> tuple[str, _Stelle, str]:
    datei = _datei()
    nach_name = {vektor["name"]: vektor for vektor in datei["vectors"]}
    for block in _bloecke(text):
        if block.name not in nach_name:
            continue
        werte = _zuordnen(block)
        if art not in werte or art == "erwartet_prosa":
            continue
        stellen = _stellen_der_werte(block, werte)
        if art in stellen:
            return block.name, stellen[art], werte[art]
    raise AssertionError(f"kein Vorkommen von {art} im Text")


def _andere_reject(aktuell: str) -> str:
    codes = [
        vektor["expect_reject"]
        for vektor in _datei()["vectors"]
        if "expect_reject" in vektor and vektor["expect_reject"] != aktuell
    ]
    assert codes
    return codes[0]


def _verfaelsche(text: str, art: str) -> str:
    _, stelle, wert = _erste_stelle(text, art)
    zeilen = text.splitlines(keepends=True)
    zeile = zeilen[stelle.zeile]
    if art == "expect_reject":
        ersatz = _andere_reject(wert)
        if zeile.endswith("\n"):
            kopf, nl = zeile[:-1], "\n"
        else:
            kopf, nl = zeile, ""
        zeilen[stelle.zeile] = kopf.replace(wert, ersatz, 1) + nl
    else:
        alt = "0" if zeile[stelle.ziffer] != "0" else "1"
        zeilen[stelle.zeile] = (
            zeile[: stelle.ziffer] + alt + zeile[stelle.ziffer + 1 :]
        )
    return "".join(zeilen)


def _ohne_ersten_block(text: str) -> tuple[str, str]:
    bloecke = _bloecke(text)
    assert bloecke
    erster = bloecke[0]
    zeilen = text.splitlines(keepends=True)
    del zeilen[erster.anfang : erster.ende + 1]
    return erster.name, "".join(zeilen)


def test_echter_text_ohne_befunde() -> None:
    assert befunde(_spec_text()) == []


@pytest.mark.parametrize("art", _FELDARTEN)
def test_verfaelschte_kopie_liefert_befund(art: str) -> None:
    kopie = _verfaelsche(_spec_text(), art)
    assert befunde(kopie)


def test_fehlender_block_nennt_vektor() -> None:
    name, kopie = _ohne_ersten_block(_spec_text())
    getroffen = " ".join(befunde(kopie))
    assert name in getroffen
