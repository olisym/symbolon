"""Ein Bündel als Datei über die HTTP-Schnittstelle (D614 Beschluss 5)."""

from __future__ import annotations

import sys
from pathlib import Path

from symbolon import buendel
from symbolon.bote.kern import Getrennt, HttpKnoten, einliefern


def _schreiben(url: str, pfad: Path) -> int:
    """Legt den Bestand ab; die Zeile zählt die Datei (D614 Beschluss 5, D615 Beschluss 1)."""
    knoten = HttpKnoten(url)
    try:
        claims, objekte = knoten.bestand()
        roh = knoten.paket(claims, objekte)
    except Getrennt:
        print("getrennt")
        return 1
    try:
        pfad.write_bytes(roh)
    except OSError as exc:
        print(f"datei: {exc}")
        return 1
    datei_claims, datei_objekte = buendel.lesen(pfad.read_bytes())
    zeile = (
        f"claims={len(datei_claims)} objekte={len(datei_objekte)} "
        f"bytes={pfad.stat().st_size}"
    )
    bestand = len(claims) + len(objekte)
    in_datei = len(datei_claims) + len(datei_objekte)
    if in_datei < bestand:
        zeile += f" weggelassen={bestand - in_datei}"
    print(zeile)
    return 0


def _lesen(url: str, pfad: Path) -> int:
    """Liefert jeden Eintrag ein. ``neu`` ist, was der Bestand danach mehr hat
    (D614 Beschluss 5)."""
    try:
        roh = pfad.read_bytes()
    except OSError as exc:
        print(f"datei: {exc}")
        return 1
    try:
        claims, objekte = buendel.lesen(roh)
    except buendel.Formwidrig:
        print("formwidrig")
        return 1
    knoten = HttpKnoten(url)
    try:
        vorher_claims, vorher_objekte = knoten.bestand()
        geholt, abgewiesen, getrennt = einliefern(knoten, claims, objekte)
        if not getrennt:
            nachher_claims, nachher_objekte = knoten.bestand()
    except Getrennt:
        print("getrennt")
        return 1
    if getrennt:
        print("getrennt")
        return 1
    neu = (len(nachher_claims) + len(nachher_objekte)) - (len(vorher_claims) + len(vorher_objekte))
    print(f"eingeliefert={geholt} neu={neu} abgewiesen={abgewiesen}")
    return 0


def main(argv: list[str]) -> int:
    """``schreiben`` oder ``lesen``; 2 bei falschem Aufruf (D614 Beschluss 5)."""
    if len(argv) != 4 or argv[1] not in ("schreiben", "lesen"):
        print("aufruf: python -m tools.buendel schreiben|lesen <url> <datei>")
        return 2
    url, pfad = argv[2], Path(argv[3])
    if argv[1] == "schreiben":
        return _schreiben(url, pfad)
    return _lesen(url, pfad)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
