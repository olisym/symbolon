"""Geräte, ein Netz und der Startbefehl (D518 Beschluss 1 bis 3, D521 Beschluss 4, D523, D542, D588)."""

from __future__ import annotations

import datetime
import hashlib
import itertools
import json
import re
import subprocess
import sys
import threading
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

# Bild (c): die Geräte aus GERAETE_VERSEHEN, die Zweitgeräte mit eigenem Schlüssel
# (D542 Beschluss 1 und 2).
GERAETE_GERAETE: list[tuple[str, str, frozenset[str]]] = [
    (
        name,
        datei,
        {
            "Brunos Zweitgerät": frozenset({"BRUNO (Zweitgerät)"}),
            "Doras Zweitgerät": frozenset({"DORA (Zweitgerät)"}),
        }.get(name, personen),
    )
    for name, datei, personen in GERAETE_VERSEHEN
]

_PORT = 8471
_HOST = "127.0.0.1"
_WARTEN = 10
_TAKT = 2
_RUHE = 30.0
_BEREIT = 10.0
_BOTE_TAKT = "1"
_GESCHICHTEN = ("--personen", "--versehen", "--geraete", "--aufloesen")
_USAGE = (
    "usage: python -m tools.netz <verzeichnis> "
    "[--personen | --versehen | --geraete | --aufloesen] [--reticulum]"
)

# Der Ablauf, den der Startbefehl druckt (D518, „Der Ablauf, den der Startbefehl druckt“).
ABLAUF = [
    "Auf jedem Gerät ausser Brunos Zweitgerät erledigen, was unter „Jetzt zu tun“ steht. Brunos "
    "Aufgaben erscheinen auf beiden Geräten; auf zweien erledigt, gabelten sie sich schon hier.",
    "Annas Gerät: einen Satzungsantrag stellen, etwa den Beitrag. Warten, bis jedes Gerät „Es ist "
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

# Der Text zum Zusehen in Bild (c) (D542 Beschluss 1, D543 Beschluss 5).
ZUSEHEN_GERAETE = [
    *ZUSEHEN_VERSEHEN[:3],
    "Beide Zweitgeräte haben einen eigenen Schlüssel, den ihre Person aufgenommen hat. Bruno stimmt "
    "auf seinen zwei Geräten verschieden. Dora ist ehrlich: ihr Zweitgerät ist eine Weile getrennt, "
    "und sie stimmt dort ein zweites Mal gleich ab.",
    "Kommt Doras Zweitgerät zurück, zählt ihre Stimme einmal, und der Beschluss hält. Brunos Stimmen "
    "zählen nicht, seine Bürgschaften zählen weiter.",
]

# Der Text zum Zusehen im Folgebild: Anna wartet, Bruno löst auf (D551 Beschluss 2, D552 Beschluss 3).
ZUSEHEN_AUFLOESEN = [
    *ZUSEHEN_VERSEHEN[:3],
    "Beide Zweitgeräte haben einen eigenen Schlüssel, den ihre Person aufgenommen hat. Bruno vertut "
    "sich: auf seinem Gerät stimmt er Ja, auf dem Zweitgerät Nein. Dora ist ehrlich: ihr Zweitgerät "
    "ist eine Weile getrennt, und sie stimmt dort ein zweites Mal gleich ab.",
    "Anna stellt den Beschluss erst fest, wenn Bruno seinen Widerspruch aufgelöst hat. Bruno sieht "
    "die Karte und stimmt auf seinem Gerät neu Ja; die neue Stimme ersetzt beide.",
    "Kommt Doras Zweitgerät zurück, zählt ihre Stimme einmal, und der Beschluss hält.",
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


def schalter(argv: list[str]) -> tuple[str | None, bool]:
    """Eine Geschichte oder keine, ``--reticulum`` nur am Ende (D589 Beschluss 1)."""
    reticulum = bool(argv) and argv[-1] == "--reticulum"
    rest = argv[:-1] if reticulum else argv
    if not rest:
        return None, reticulum
    if len(rest) == 1 and rest[0] in _GESCHICHTEN:
        return rest[0], reticulum
    raise SystemExit(_USAGE)


def instanz_name(verzeichnis: Path) -> str:
    """Der Name der gemeinsamen Instanz aus dem aufgelösten Verzeichnis (D589 Beschluss 1)."""
    digest = hashlib.sha256(str(verzeichnis.resolve()).encode("utf-8")).hexdigest()
    return "symbolon-" + digest[:12]


def rns_konfiguration(verzeichnis: Path) -> Path:
    """Eine gemeinsame Instanz ohne Schnittstelle, im Verzeichnis des Laufs (D589 Beschluss 1)."""
    rns = verzeichnis / "rns"
    rns.mkdir(parents=True, exist_ok=True)
    zeilen = [
        "[reticulum]",
        "  enable_transport = No",
        "  share_instance = Yes",
        f"  instance_name = {instanz_name(verzeichnis)}",
        "[logging]",
        "  loglevel = 2",
        "[interfaces]",
    ]
    (rns / "config").write_text("".join(z + "\n" for z in zeilen), encoding="utf-8")
    return rns


def instanz_bereit(name: str, tabelle: Path = Path("/proc/net/unix")) -> bool:
    """Wahr, wenn der Socket ``@rns/<name>`` in der Tabelle steht (D589 Befund 1).

    Kein RNS-Programm als Probe: eines, das vor ``rnsd`` läuft, wird selbst zur gemeinsamen
    Instanz, und ``rnsd`` bleibt ohne sie. Die Tabelle ``/proc/net/unix`` gibt es nur unter Linux.
    """
    ziel = f"@rns/{name}"
    for zeile in tabelle.read_text(encoding="utf-8").splitlines():
        felder = zeile.split()
        if felder and felder[-1] == ziel:
            return True
    return False


def ruhe(urls: list[str], frist: float = _RUHE) -> float | None:
    """Wartet, bis jedes nicht getrennte Gerät denselben Stand trägt (D588 Beschluss 2).

    Gibt die Sekunden bis dahin zurück, nach der Frist ``None``. Ein Fehler beim Lesen gilt als
    nicht gleich.
    """
    beginn = time.monotonic()
    while True:
        try:
            staende = set()
            for url in urls:
                with urllib.request.urlopen(url + "/getrennt", timeout=1) as response:
                    if json.loads(response.read()) is True:
                        continue
                with urllib.request.urlopen(url + "/stand", timeout=1) as response:
                    staende.add(json.loads(response.read()))
            if len(staende) <= 1:
                return time.monotonic() - beginn
        except (urllib.error.URLError, OSError):
            pass
        if time.monotonic() - beginn >= frist:
            return None
        time.sleep(0.2)


class Ausgabe:
    """Jede Zeile auf den Schirm und in den Verlauf, unter einer Sperre (D588 Beschluss 3)."""

    def __init__(self, verlauf: Path) -> None:
        self.verlauf = verlauf
        self._sperre = threading.Lock()

    def __call__(self, zeile: str) -> None:
        with self._sperre:
            print(zeile, flush=True)
            with self.verlauf.open("a", encoding="utf-8") as datei:
                datei.write(zeile + "\n")


def _mitlesen(prozess: subprocess.Popen, geraet: str, namen: dict[str, str], ausgeben) -> None:
    """Die Zeilen eines Boten, ein Holen als „Gerät ← Nachbar: …“ (D589 Beschluss 1)."""
    for zeile in prozess.stdout:
        zeile = zeile.rstrip("\n")
        if zeile.startswith("adresse "):
            continue
        treffer = re.fullmatch(r"([0-9a-f]{32}): (.*)", zeile)
        if treffer and treffer.group(1) in namen:
            ausgeben(f"{geraet} ← {namen[treffer.group(1)]}: {treffer.group(2)}")
        else:
            ausgeben(f"{geraet}: {zeile}")


def boten(verzeichnis: Path, geraete, urls: list[str], ausgeben) -> list[subprocess.Popen]:
    """Die gemeinsame Instanz, dann je Gerät ein Bote mit allen anderen (D588, D589 Beschluss 1).

    Rückgabe: ``rnsd`` zuerst, dann die Boten.
    """
    # Erst hier: rns ist ein Zusatz, ohne ``--reticulum`` nicht verlangt (D584 Beschluss 4).
    from symbolon.bote.reticulum import adresse, identitaet

    rns = rns_konfiguration(verzeichnis)
    rnsd = subprocess.Popen(
        [sys.executable, "-m", "RNS.Utilities.rnsd", "--config", str(rns)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    name = instanz_name(verzeichnis)
    ende = time.monotonic() + _BEREIT
    while not instanz_bereit(name):
        if rnsd.poll() is not None or time.monotonic() > ende:
            rnsd.terminate()
            rnsd.wait()
            raise SystemExit("Die gemeinsame RNS-Instanz startet nicht.")
        time.sleep(0.1)
    dateien = [verzeichnis / f"{datei}.id" for _name, datei, _personen in geraete]
    adressen = [adresse(identitaet(pfad)).hex() for pfad in dateien]
    namen = {hex_: geraet for hex_, (geraet, _datei, _personen) in zip(adressen, geraete)}
    prozesse = [rnsd]
    for index, ((geraet, _datei, _personen), url, pfad) in enumerate(zip(geraete, urls, dateien)):
        nachbarn = [hex_ for anderer, hex_ in enumerate(adressen) if anderer != index]
        bote = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "symbolon.bote",
                url,
                "--rns",
                str(rns),
                "--identitaet",
                str(pfad),
                "--nachbar",
                *nachbarn,
                "--takt",
                _BOTE_TAKT,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        threading.Thread(
            target=_mitlesen, args=(bote, geraet, namen, ausgeben), daemon=True
        ).start()
        prozesse.append(bote)
    return prozesse


def main() -> None:
    """Legt an, startet, druckt und gleicht ab, bis Strg-C (D518 Beschluss 3, D521 Beschluss 4).

    Mit ``--personen`` fährt er vor jedem Durchgang einen Takt, beginnend bei 0. Mit
    ``--versehen`` ebenso, über ``GERAETE_VERSEHEN`` (D523 Beschluss 4). Mit ``--geraete``
    ebenso, über ``GERAETE_GERAETE`` und mit den Aufnahmen im Bestand (D542 Beschluss 1 und 3).
    Mit ``--aufloesen`` wie ``--geraete``, dazu die Regeln aus ``takt`` unter ``aufloesen``
    (D551 Beschluss 2). Mit ``--reticulum`` gleichen Boten über eine gemeinsame Instanz ab statt
    der Durchgänge; mit einer Geschichte wartet er nach jedem Takt auf gleichen Stand. Jede Zeile
    steht auch in ``verlauf.txt`` (D588 Beschluss 1 bis 3, D589 Beschluss 1).
    """
    if len(sys.argv) < 2:
        raise SystemExit(_USAGE)
    geschichte, reticulum = schalter(sys.argv[2:])
    personen_an = geschichte is not None
    aufloesen = geschichte == "--aufloesen"
    mit_geraeten = geschichte == "--geraete" or aufloesen
    if mit_geraeten:
        geraete = GERAETE_GERAETE
    elif geschichte == "--versehen":
        geraete = GERAETE_VERSEHEN
    else:
        geraete = GERAETE
    # Erst hier: tools.personen liest GERAETE aus diesem Modul.
    from tools.personen import takt

    verzeichnis = Path(sys.argv[1])
    verzeichnis.mkdir(parents=True, exist_ok=True)
    ausgeben = Ausgabe(verzeichnis / "verlauf.txt")
    for _name, datei, personen in geraete:
        if not (verzeichnis / datei).exists():
            anlegen(verzeichnis / datei, personen, geraete=mit_geraeten)
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
        if reticulum:
            prozesse.extend(boten(verzeichnis, geraete, urls, ausgeben))
        jetzt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ausgeben(f"Start {jetzt}: {' '.join(sys.argv[2:])}")
        for (name, _datei, _personen), url in zip(geraete, urls):
            ausgeben(f"{name}: {url}/")
        ausgeben("")
        if personen_an:
            ausgeben("Zum Zusehen:")
            if aufloesen:
                text = ZUSEHEN_AUFLOESEN
            elif mit_geraeten:
                text = ZUSEHEN_GERAETE
            elif geschichte == "--versehen":
                text = ZUSEHEN_VERSEHEN
            else:
                text = ZUSEHEN
        else:
            ausgeben("Der Ablauf:")
            text = ABLAUF
        for nummer, schritt in enumerate(text, start=1):
            ausgeben(f"{nummer}. {schritt}")
        ausgeben("")
        gemeldet: set[tuple[str, str]] = set()
        gesehen: dict[tuple[str, str], list[dict]] = {}
        nummer = 0
        while True:
            time.sleep(_TAKT)
            if personen_an:
                try:
                    for zeile in takt(urls, nummer, gemeldet, geraete, gesehen, aufloesen):
                        ausgeben(zeile)
                except Exception as exc:
                    ausgeben(f"Ein Takt ist gescheitert ({exc}); es geht weiter.")
                nummer += 1
            if reticulum:
                if personen_an:
                    dauer = ruhe(urls)
                    if dauer is None:
                        ausgeben(f"Abgleich über Reticulum: nach {_RUHE:.0f} s nicht gleich")
                    else:
                        ausgeben(f"Abgleich über Reticulum: gleicher Stand nach {dauer:.1f} s")
                continue
            try:
                verteilt = durchgang(urls)
            except Exception as exc:
                ausgeben(f"Ein Durchgang ist gescheitert ({exc}); es geht weiter.")
                continue
            if verteilt:
                ausgeben(f"Abgleich: {verteilt} Einträge verteilt")
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
