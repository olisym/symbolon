"""Fragen-Index: Zuordnung, Kopfzahlen, Befunde an Kopie (D386, D387)."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from tools.check_fragen import ROOT, main

_LISTEN = (Path("go/FRAGEN.md"), Path("hs/FRAGEN-1.md"), Path("hs/FRAGEN-2.md"))
_KOPIE = (
    Path("fragen-adressen.md"),
    Path("fragen-index.md"),
    *_LISTEN,
)


def _ueberschriften(wurzel: Path) -> int:
    anzahl = 0
    for rel in _LISTEN:
        text = (wurzel / rel).read_text(encoding="utf-8")
        anzahl += len(re.findall(r"^## ", text, re.M))
    return anzahl


def _nennungen(text: str) -> int:
    anzahl = 0
    in_tabelle = False
    for zeile in text.splitlines():
        if not zeile.startswith("|"):
            in_tabelle = False
            continue
        zellen = [teil.strip() for teil in zeile.strip().strip("|").split("|")]
        if zellen[:2] == ["Nr", "Adresse"]:
            in_tabelle = True
            continue
        if not in_tabelle:
            continue
        if zellen and set(zellen[0]) <= set("-:"):
            continue
        anzahl += len(zellen[1].split(" / "))
    return anzahl


def _baum_kopieren(ziel: Path) -> None:
    (ziel / "go").mkdir()
    (ziel / "hs").mkdir()
    for rel in _KOPIE:
        shutil.copy(ROOT / rel, ziel / rel)


def test_prueflauf_auf_dem_baum_ist_gruen() -> None:
    assert main([]) == 0


def test_eintraege_im_kopf_stimmen_mit_ueberschriften() -> None:
    kopf = (ROOT / "fragen-index.md").read_text(encoding="utf-8")
    fund = re.search(r"Einträge: (\d+)", kopf)
    assert fund is not None
    assert int(fund.group(1)) == _ueberschriften(ROOT)


def test_nennungen_stimmen_mit_adressteilen() -> None:
    kopf = (ROOT / "fragen-index.md").read_text(encoding="utf-8")
    fund = re.search(r"Nennungen: (\d+)", kopf)
    assert fund is not None
    adressen = (ROOT / "fragen-adressen.md").read_text(encoding="utf-8")
    assert int(fund.group(1)) == _nennungen(adressen)


def test_entfernte_zuordnungszeile_ist_befund(
    tmp_path: Path, monkeypatch: object
) -> None:
    _baum_kopieren(tmp_path)
    monkeypatch.setattr("tools.check_fragen.ROOT", tmp_path)
    quelle = tmp_path / "fragen-adressen.md"
    text = quelle.read_text(encoding="utf-8")
    zeilen = text.splitlines(keepends=True)
    rest: list[str] = []
    entfernt = False
    for zeile in zeilen:
        if not entfernt and re.match(r"\| 22 \| 01 Anhang C\.8 \|", zeile):
            entfernt = True
            continue
        rest.append(zeile)
    assert entfernt
    quelle.write_text("".join(rest), encoding="utf-8")
    assert main([]) == 1


def test_verfaelschter_index_ist_befund(
    tmp_path: Path, monkeypatch: object
) -> None:
    _baum_kopieren(tmp_path)
    monkeypatch.setattr("tools.check_fragen.ROOT", tmp_path)
    ziel = tmp_path / "fragen-index.md"
    text = ziel.read_text(encoding="utf-8")
    assert "—" in text
    ziel.write_text(text.replace("—", "-", 1), encoding="utf-8")
    assert main([]) == 1
