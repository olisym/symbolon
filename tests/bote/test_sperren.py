"""Gesperrte Nachbarn: die Sperrliste und der Rundgang des Boten (D594 Beschluss 3)."""

from __future__ import annotations

import pytest

from symbolon.bote import kern
from symbolon.bote.kern import Ergebnis, Formwidrig, rundgang, sperren_lesen, sperrliste

_A = bytes.fromhex("aa" * 16)
_B = bytes.fromhex("bb" * 16)
_C = bytes.fromhex("cc" * 16)


def test_sperrliste() -> None:
    """Je Zeile eine Adresse aus 16 Bytes, leere Zeilen zählen nicht (D594 Beschluss 3)."""
    assert sperrliste("") == frozenset()
    assert sperrliste("\n  \n") == frozenset()
    assert sperrliste(f"{_A.hex()}\n\n  {_B.hex()}  \n") == frozenset({_A, _B})
    assert sperrliste(f"{_A.hex()}\n{_A.hex()}\n") == frozenset({_A})


@pytest.mark.parametrize("zeile", ["zz" * 16, "ab" * 15, "ab" * 17, "abc", "aa bb"])
def test_sperrliste_formwidrig(zeile: str) -> None:
    """Eine Zeile, die keine Adresse aus 16 Bytes ist, macht die Liste formwidrig (D594 B. 3)."""
    with pytest.raises(Formwidrig):
        sperrliste(f"{_A.hex()}\n{zeile}\n")


def test_sperren_lesen(tmp_path) -> None:
    """Ohne Datei keiner gesperrt, formwidrig ``None`` (D594 Beschluss 3)."""
    pfad = tmp_path / "sperren.txt"
    assert sperren_lesen(pfad) == frozenset()
    pfad.write_text(_B.hex() + "\n", encoding="utf-8")
    assert sperren_lesen(pfad) == frozenset({_B})
    pfad.write_text("kein hex\n", encoding="utf-8")
    assert sperren_lesen(pfad) is None
    pfad.write_bytes(b"\xff\xfe")
    assert sperren_lesen(pfad) is None


def _gefragt(monkeypatch, beim_holen=None) -> list[bytes]:
    """Ersetzt ``holen``; zeichnet auf, bei welchem Nachbarn geholt wurde."""
    gefragt: list[bytes] = []

    def holen(_mein, nachbar):
        gefragt.append(nachbar)
        if beim_holen is not None:
            beim_holen(nachbar)
        return Ergebnis(0, {}, False, 0, 0)

    monkeypatch.setattr(kern, "holen", holen)
    return gefragt


def _quellen() -> list[tuple[bytes, bytes]]:
    # Der Nachbar steht für sich selbst; holen sieht nur, wer gefragt wird.
    return [(_A, _A), (_B, _B), (_C, _C)]


def test_rundgang_ohne_datei(monkeypatch, tmp_path) -> None:
    """Ohne Sperrliste und ohne Datei wird jeder Nachbar gefragt, ohne Zeile (D594 Beschluss 3)."""
    gefragt = _gefragt(monkeypatch)
    zeilen: list[str] = []
    assert rundgang(None, _quellen(), None, frozenset(), zeilen.append) == frozenset()
    assert rundgang(None, _quellen(), tmp_path / "fehlt.txt", frozenset(), zeilen.append) == (
        frozenset()
    )
    assert gefragt == [_A, _B, _C, _A, _B, _C]
    assert zeilen == []


def test_rundgang_sperrt(monkeypatch, tmp_path) -> None:
    """Ein gesperrter Nachbar wird nicht gefragt; die Zeile steht einmal (D594 Beschluss 3)."""
    gefragt = _gefragt(monkeypatch)
    pfad = tmp_path / "sperren.txt"
    pfad.write_text(_B.hex() + "\n", encoding="utf-8")
    zeilen: list[str] = []
    zuletzt = rundgang(None, _quellen(), pfad, frozenset(), zeilen.append)
    zuletzt = rundgang(None, _quellen(), pfad, zuletzt, zeilen.append)
    assert gefragt == [_A, _C, _A, _C]
    assert zeilen == ["gesperrt=1"]
    pfad.write_text("", encoding="utf-8")
    rundgang(None, _quellen(), pfad, zuletzt, zeilen.append)
    assert gefragt == [_A, _C, _A, _C, _A, _B, _C]
    assert zeilen == ["gesperrt=1", "gesperrt=0"]


def test_rundgang_formwidrig(monkeypatch, tmp_path) -> None:
    """Eine formwidrige Liste sperrt jeden Nachbarn und steht einmal (D594 Beschluss 3)."""
    gefragt = _gefragt(monkeypatch)
    pfad = tmp_path / "sperren.txt"
    pfad.write_text("kein hex\n", encoding="utf-8")
    zeilen: list[str] = []
    zuletzt = rundgang(None, _quellen(), pfad, frozenset(), zeilen.append)
    zuletzt = rundgang(None, _quellen(), pfad, zuletzt, zeilen.append)
    assert zuletzt is None
    assert gefragt == []
    assert zeilen == ["sperren formwidrig"]


def test_rundgang_liest_vor_jedem_nachbarn(monkeypatch, tmp_path) -> None:
    """Wird während des Rundgangs gesperrt, wird der nächste Nachbar schon nicht mehr gefragt.

    Darauf stützt sich das Lab: nach der Zeile ``gesperrt=`` holt dieser Bote über keine alte
    Grenze mehr (D594 Beschluss 3).
    """
    pfad = tmp_path / "sperren.txt"

    def sperren_nach_a(nachbar):
        if nachbar == _A:
            pfad.write_text(_C.hex() + "\n", encoding="utf-8")

    gefragt = _gefragt(monkeypatch, sperren_nach_a)
    zeilen: list[str] = []
    rundgang(None, _quellen(), pfad, frozenset(), zeilen.append)
    assert gefragt == [_A, _B]
    assert zeilen == ["gesperrt=1"]
