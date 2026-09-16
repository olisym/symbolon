"""Fragen-Index: Zuordnung, Kopfzahlen, Befunde an Kopie (D386, D387, D395)."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from tools.check_fragen import ROOT, main

_LISTEN = (
    Path("go/FRAGEN.md"),
    Path("hs/FRAGEN-1.md"),
    Path("hs/FRAGEN-2.md"),
    Path("rs/FRAGEN.md"),
)
_KOPIE = (
    Path("fragen-adressen.md"),
    Path("fragen-index.md"),
    *_LISTEN,
)
_ADDR_PRAEFIX = "- **Adresse:** "
_ADDR_1 = "- **Adresse:** 02 §4"


def _ueberschriften(wurzel: Path) -> int:
    anzahl = 0
    for rel in _LISTEN:
        text = (wurzel / rel).read_text(encoding="utf-8")
        anzahl += len(re.findall(r"^## ", text, re.M))
    return anzahl


def _nennungen(wurzel: Path) -> int:
    anzahl = 0
    in_tabelle = False
    text = (wurzel / "fragen-adressen.md").read_text(encoding="utf-8")
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
    for rel in _LISTEN:
        for zeile in (wurzel / rel).read_text(encoding="utf-8").splitlines():
            if zeile.startswith(_ADDR_PRAEFIX):
                anzahl += len(zeile.removeprefix(_ADDR_PRAEFIX).split(" / "))
    return anzahl


def _baum_kopieren(ziel: Path) -> None:
    (ziel / "go").mkdir()
    (ziel / "hs").mkdir()
    (ziel / "rs").mkdir()
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
    assert int(fund.group(1)) == _nennungen(ROOT)


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


def test_ueberschrift_ohne_adresszeile_ist_befund(
    tmp_path: Path, monkeypatch: object, capsys: object
) -> None:
    _baum_kopieren(tmp_path)
    monkeypatch.setattr("tools.check_fragen.ROOT", tmp_path)
    ziel = tmp_path / "rs" / "FRAGEN.md"
    text = ziel.read_text(encoding="utf-8")
    assert _ADDR_1 in text
    ziel.write_text(text.replace(_ADDR_1 + "\n", "", 1), encoding="utf-8")
    assert main([]) == 1
    assert (
        "Überschrift ohne Adresszeile in `rs/FRAGEN.md`: 1"
        in capsys.readouterr().out
    )


def test_mehr_als_eine_adresszeile_ist_befund(
    tmp_path: Path, monkeypatch: object, capsys: object
) -> None:
    _baum_kopieren(tmp_path)
    monkeypatch.setattr("tools.check_fragen.ROOT", tmp_path)
    ziel = tmp_path / "rs" / "FRAGEN.md"
    text = ziel.read_text(encoding="utf-8")
    assert _ADDR_1 in text
    ziel.write_text(
        text.replace(_ADDR_1, _ADDR_1 + "\n" + _ADDR_1, 1), encoding="utf-8"
    )
    assert main([]) == 1
    assert (
        "mehr als eine Adresszeile in `rs/FRAGEN.md` Nr. 1"
        in capsys.readouterr().out
    )


def test_adresszeile_vor_erster_ueberschrift_ist_befund(
    tmp_path: Path, monkeypatch: object, capsys: object
) -> None:
    _baum_kopieren(tmp_path)
    monkeypatch.setattr("tools.check_fragen.ROOT", tmp_path)
    ziel = tmp_path / "rs" / "FRAGEN.md"
    text = ziel.read_text(encoding="utf-8")
    assert "## 1. " in text
    ziel.write_text(
        text.replace("## 1. ", _ADDR_PRAEFIX + "01 §2\n\n## 1. ", 1),
        encoding="utf-8",
    )
    assert main([]) == 1
    assert (
        "Adresszeile vor der ersten Überschrift in `rs/FRAGEN.md`"
        in capsys.readouterr().out
    )


def test_nicht_wohlgeformte_zelle_in_liste_ist_befund(
    tmp_path: Path, monkeypatch: object, capsys: object
) -> None:
    _baum_kopieren(tmp_path)
    monkeypatch.setattr("tools.check_fragen.ROOT", tmp_path)
    ziel = tmp_path / "rs" / "FRAGEN.md"
    text = ziel.read_text(encoding="utf-8")
    assert _ADDR_1 in text
    ziel.write_text(
        text.replace(_ADDR_1, _ADDR_PRAEFIX + "kein-abschnitt", 1),
        encoding="utf-8",
    )
    assert main([]) == 1
    assert (
        "Adresse nicht wohlgeformt in `rs/FRAGEN.md` Nr. 1"
        in capsys.readouterr().out
    )


def test_tabelle_und_marker_ist_befund(
    tmp_path: Path, monkeypatch: object, capsys: object
) -> None:
    _baum_kopieren(tmp_path)
    monkeypatch.setattr("tools.check_fragen.ROOT", tmp_path)
    quelle = tmp_path / "fragen-adressen.md"
    text = quelle.read_text(encoding="utf-8")
    alt = "## 1. `go/FRAGEN.md` — Layer 01, Go-Fassung\n"
    assert alt in text
    quelle.write_text(
        text.replace(alt, alt + "\nAdressen: in der Liste.\n", 1),
        encoding="utf-8",
    )
    assert main([]) == 1
    assert (
        "Abschnitt `go/FRAGEN.md` hat Tabelle und Marker"
        in capsys.readouterr().out
    )


def test_weder_tabelle_noch_marker_ist_befund(
    tmp_path: Path, monkeypatch: object, capsys: object
) -> None:
    _baum_kopieren(tmp_path)
    monkeypatch.setattr("tools.check_fragen.ROOT", tmp_path)
    quelle = tmp_path / "fragen-adressen.md"
    text = quelle.read_text(encoding="utf-8")
    assert "Adressen: in der Liste.\n" in text
    quelle.write_text(
        text.replace("Adressen: in der Liste.\n", "", 1), encoding="utf-8"
    )
    assert main([]) == 1
    assert (
        "Abschnitt `rs/FRAGEN.md` hat weder Tabelle noch Marker"
        in capsys.readouterr().out
    )


def test_fragenliste_ohne_abschnitt_ist_befund(
    tmp_path: Path, monkeypatch: object, capsys: object
) -> None:
    _baum_kopieren(tmp_path)
    monkeypatch.setattr("tools.check_fragen.ROOT", tmp_path)
    extra = tmp_path / "xx" / "FRAGEN.md"
    extra.parent.mkdir()
    extra.write_text("## 1. Test\n", encoding="utf-8")
    assert main([]) == 1
    assert "Fragenliste ohne Abschnitt: xx/FRAGEN.md" in capsys.readouterr().out
