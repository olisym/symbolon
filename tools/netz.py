"""Fünf Geräte, ein Netz und der Startbefehl (D518 Beschluss 1 bis 3, D521 Beschluss 4, D523)."""

from __future__ import annotations

import itertools
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from tools.abgleich import runde
from tools.verein_node import anlegen

# Gerät, Datei und die Namen, deren Schlüssel es trägt (D518 Beschluss 1).
GERAETE: list[tuple[str, str, frozenset[str]]] = [
    ("Annas Gerät", "anna.sqlite", frozenset({"ANNA"})),
    ("Brunos Gerät", "bruno.sqlite", frozenset({"BRUNO"})),
    ("Brunos Zweitgerät", "bruno2.sqlite", frozenset({"BRUNO"})),
    ("Chris' Gerät", "chris.sqlite", frozenset({"CHRIS", "KASSE"})),
    ("Doras Gerät", "dora.sqlite", frozenset({"DORA"})),
]

# Bild (b): GERAETE plus Doras Zweitgerät, Port 8476 aus der Reihenfolge (D523 Beschluss 1).
GERAETE_VERSEHEN: list[tuple[str, str, frozenset[str]]] = [
    *GERAETE,
    ("Doras Zweitgerät", "dora2.sqlite", frozenset({"DORA"})),
]

_PORT = 8471
_HOST = "127.0.0.1"
_WARTEN = 10
_TAKT = 2

# Der Ablauf, den der Startbefehl druckt (D518, „Der Ablauf, den der Startbefehl druckt“).
ABLAUF = [
    "Auf jedem Gerät ausser Brunos Zweitgerät erledigen, was unter „Jetzt zu tun“ steht. Brunos "
    "Aufgaben erscheinen auf beiden Geräten; auf zweien erledigt, gabelten sie sich schon hier.",
    "Annas Gerät: einen Satzungstext beantragen, etwa den Beitrag. Warten, bis jedes Gerät „Es ist "
    "Neues angekommen“ zeigt.",
    "Doras Gerät und Brunos Zweitgerät: vom Netz trennen.",
    "Anna und Chris stimmen Ja, jede auf ihrem Gerät.",
    "Bruno stimmt Ja auf Brunos Gerät und Nein auf Brunos Zweitgerät, sonst nichts.",
    "Annas Gerät: den Beschluss feststellen. Die neue Satzung gilt dort.",
    "Brunos Zweitgerät: wieder verbinden. Nach ein paar Sekunden zeigt jedes Gerät den Widerspruch.",
    "Doras Gerät: wieder verbinden und Ja stimmen; dann stellt Anna den Beschluss neu fest.",
]

# Der Text zum Zusehen, wenn die Personen handeln (D521 Beschluss 4).
ZUSEHEN = [
    "Die Personen handeln selbst: in jedem Takt erst auf jedem Gerät, dann gleichen die Geräte ab.",
    "Nicht selbst klicken, solange sie handeln. Im Terminal steht, wer was tut.",
    "In den Tabs „Aktualisieren“, sobald „Es ist Neues angekommen“ erscheint.",
    "Bruno stimmt auf beiden Geräten, bevor sie sich sehen. Nach dem Abgleich zeigt jedes Gerät den "
    "Widerspruch.",
]

# Der Text zum Zusehen in Bild (b) (D523 Beschluss 4).
ZUSEHEN_VERSEHEN = [
    "Die Personen handeln selbst: in jedem Takt erst auf jedem Gerät, dann gleichen die Geräte ab.",
    "Nicht selbst klicken, solange sie handeln. Im Terminal steht, wer was tut.",
    "In den Tabs „Aktualisieren“, sobald „Es ist Neues angekommen“ erscheint.",
    "Bruno lügt: er stimmt auf beiden Geräten verschieden. Dora ist ehrlich: ihr Zweitgerät ist eine "
    "Weile getrennt, und sie stimmt dort ein zweites Mal gleich ab.",
    "Kommt Doras Zweitgerät zurück, zeigt jedes Gerät zwei Widersprüche, und der Beschluss fällt.",
]


def durchgang(urls: list[str]) -> int:
    """Ein Durchgang: runde über jedes Paar in der Ordnung von combinations (D518 Beschluss 2)."""
    return sum(runde(url_a, url_b).eingeliefert for url_a, url_b in itertools.combinations(urls, 2))


def _antwortet(url: str, prozess: subprocess.Popen) -> bool:
    """Wartet bis zu zehn Sekunden, bis GET /now antwortet (D518 Beschluss 3)."""
    ende = time.monotonic() + _WARTEN
    while time.monotonic() < ende and prozess.poll() is None:
        try:
            with urllib.request.urlopen(url + "/now", timeout=1) as response:
                if response.status == 200:
                    return True
        except (urllib.error.URLError, OSError):
            pass
        time.sleep(0.1)
    return False


def main() -> None:
    """Legt an, startet, druckt und gleicht ab, bis Strg-C (D518 Beschluss 3, D521 Beschluss 4).

    Mit ``--personen`` fährt er vor jedem Durchgang einen Takt, beginnend bei 0. Mit
    ``--versehen`` ebenso, über ``GERAETE_VERSEHEN`` (D523 Beschluss 4).
    """
    if len(sys.argv) not in {2, 3} or sys.argv[2:] not in ([], ["--personen"], ["--versehen"]):
        raise SystemExit("usage: python -m tools.netz <verzeichnis> [--personen | --versehen]")
    schalter = sys.argv[2] if len(sys.argv) == 3 else None
    personen_an = schalter is not None
    geraete = GERAETE_VERSEHEN if schalter == "--versehen" else GERAETE
    # Erst hier: tools.personen liest GERAETE aus diesem Modul.
    from tools.personen import takt

    verzeichnis = Path(sys.argv[1])
    verzeichnis.mkdir(parents=True, exist_ok=True)
    for _name, datei, personen in geraete:
        if not (verzeichnis / datei).exists():
            anlegen(verzeichnis / datei, personen)
    urls = [f"http://{_HOST}:{_PORT + index}" for index in range(len(geraete))]
    prozesse: list[subprocess.Popen] = []
    try:
        for index, (name, datei, _personen) in enumerate(geraete):
            prozesse.append(
                subprocess.Popen(
                    [
                        sys.executable,
                        "-m",
                        "symbolon.node",
                        str(verzeichnis / datei),
                        "--port",
                        str(_PORT + index),
                        "--uhr-ab",
                        "1000",
                        "--geraet",
                        name,
                    ]
                )
            )
        for (name, _datei, _personen), url, prozess in zip(geraete, urls, prozesse):
            if not _antwortet(url, prozess):
                raise SystemExit(f"{name} antwortet nicht unter {url}; alle Knoten werden beendet.")
        for (name, _datei, _personen), url in zip(geraete, urls):
            print(f"{name}: {url}/")
        print()
        if personen_an:
            print("Zum Zusehen:")
            text = ZUSEHEN_VERSEHEN if schalter == "--versehen" else ZUSEHEN
        else:
            print("Der Ablauf:")
            text = ABLAUF
        for nummer, schritt in enumerate(text, start=1):
            print(f"{nummer}. {schritt}")
        print(flush=True)
        gemeldet: set[tuple[str, str]] = set()
        gesehen: dict[tuple[str, str], list[dict]] = {}
        nummer = 0
        while True:
            time.sleep(_TAKT)
            if personen_an:
                try:
                    for zeile in takt(urls, nummer, gemeldet, geraete, gesehen):
                        print(zeile, flush=True)
                except Exception as exc:
                    print(f"Ein Takt ist gescheitert ({exc}); es geht weiter.", flush=True)
                nummer += 1
            try:
                verteilt = durchgang(urls)
            except Exception as exc:
                print(f"Ein Durchgang ist gescheitert ({exc}); es geht weiter.", flush=True)
                continue
            if verteilt:
                print(f"Abgleich: {verteilt} Einträge verteilt", flush=True)
    except KeyboardInterrupt:
        pass
    finally:
        for prozess in prozesse:
            if prozess.poll() is None:
                prozess.terminate()
        for prozess in prozesse:
            prozess.wait()


if __name__ == "__main__":
    main()
