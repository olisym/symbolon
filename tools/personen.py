"""Personen mit eigenem Verhalten, Stufe (a) und (b) (D521 Beschluss 1 bis 4, D523)."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from tools.abgleich import _ZEITLIMIT, _anfrage
from tools.netz import GERAETE

# Der Takt des Antrags und die beantragte Änderung (D521 Beschluss 2).
ANTRAG_TAKT = 2
ANTRAG = {"set": {"field": "beitrag", "text": "30 Euro im Jahr, fällig im Januar, an die Kasse"}}

_ANTRAG_GERAET = "Annas Gerät"
_ANTRAG_PERSON = "ANNA"
_ZWEITGERAET = "Brunos Zweitgerät"
_FESTSTELLER = "ANNA"
_DORAS_ZWEITGERAET = "Doras Zweitgerät"

# Der Takt der Trennung und der Takt der Wiederverbindung (D523 Beschluss 3).
TRENNUNG = (3, 7)


def absichten(geraet: str, person: str, I: str, aufgaben: list[dict]) -> list[dict]:
    """Rümpfe für POST /sim/intent aus den Aufgaben, in deren Reihenfolge (D521 Beschluss 2)."""
    zweitgeraet = geraet == _ZWEITGERAET
    rumpfe: list[dict] = []
    for aufgabe in aufgaben:
        art = aufgabe["art"]
        if art == "VOTE":
            choice = "no" if zweitgeraet else "yes"
            rumpfe.append({"I": I, "art": "vote", "proposal": aufgabe["proposal"], "choice": choice})
        elif zweitgeraet:
            continue
        elif art == "CONFIRM_RULES":
            rumpfe.append(
                {
                    "I": I,
                    "art": "accept-rules",
                    "scope": aufgabe["scope"],
                    "constitution": aufgabe["constitution"],
                }
            )
        elif art == "RATIFY" and person == _FESTSTELLER:
            rumpfe.append({"I": I, "art": "ratify", "proposal": aufgabe["proposal"]})
        elif art == "RECEIPT":
            rumpfe.append({"I": I, "art": "receipt", "obligation": aufgabe["obligation"]})
    return rumpfe


def verzoegert(jetzt: list[dict], vorher: list[dict]) -> list[dict]:
    """Die Rümpfe aus ``jetzt``, die gleich einem aus ``vorher`` sind, in ihrer Reihenfolge.

    Dora handelt auf dem Zweitgerät einen Takt später (D523 Beschluss 2).
    """
    return [rumpf for rumpf in jetzt if rumpf in vorher]


def _handlung(rumpf: dict) -> str:
    """Was die Zeile über eine Absicht sagt (D521 Beschluss 4)."""
    art = rumpf["art"]
    if art == "accept-rules":
        return "bestätigt die Satzung"
    if art == "vote":
        return "stimmt Ja" if rumpf["choice"] == "yes" else "stimmt Nein"
    if art == "ratify":
        return "stellt den Beschluss fest"
    if art == "receipt":
        return "quittiert"
    return "beantragt den Beitrag"


def _einliefern(url: str, kopf: str, rumpf: dict) -> str:
    """Eine Absicht; eine Abweisung ist eine Zeile, kein Abbruch (D521 Beschluss 2 und 4).

    Abweisung ist jede Antwort 4xx, auch 409 bei mehr als einer Spitze.
    """
    request = urllib.request.Request(
        url.rstrip("/") + "/sim/intent",
        data=json.dumps(rumpf).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    zeile = f"{kopf} {_handlung(rumpf)}"
    try:
        with urllib.request.urlopen(request, timeout=_ZEITLIMIT) as response:
            response.read()
    except urllib.error.HTTPError as exc:
        if not 400 <= exc.code < 500:
            raise RuntimeError(f"POST /sim/intent: {exc.code}") from exc
        zeile += f", abgewiesen ({json.loads(exc.read())})"
    return zeile


def _vereinsscope(url: str) -> str:
    """Der Scope, dessen Ansicht einen Verein trägt (D521 Beschluss 2)."""
    for scope in _anfrage(url, "GET", "/scopes")[1]:
        if _anfrage(url, "GET", f"/scopes/{scope}")[1]["verein"] is not None:
            return scope
    raise RuntimeError("kein Scope trägt einen Verein")


def takt(
    urls: list[str],
    nummer: int,
    gemeldet: set[tuple[str, str]],
    geraete: list[tuple[str, str, frozenset[str]]] = GERAETE,
    gesehen: dict[tuple[str, str], list[dict]] | None = None,
) -> list[str]:
    """Ein Takt ohne den Durchgang: erst die Personen, dann der Antrag (D521 Beschluss 2 bis 4).

    Geräte in der Ordnung von ``geraete``, Personen je Gerät nach Namen sortiert. Eine Person mit
    etwas zu tun und mehr als einer Spitze handelt dort nicht und wird je Gerät einmal gemeldet.

    Enthält ``geraete`` Doras Zweitgerät, wird es in den Takten aus ``TRENNUNG`` vor den Personen
    getrennt und wieder verbunden (D523 Beschluss 3), und Dora handelt dort nur auf den Rümpfen,
    die schon im vorigen Takt unter ``gesehen`` lagen (D523 Beschluss 2).
    """
    namen_geraete = [name for name, _datei, _personen in geraete]
    versehen = _DORAS_ZWEITGERAET in namen_geraete
    if versehen and gesehen is None:
        raise ValueError("Doras Zweitgerät braucht gesehen")
    namen: dict[str, str] = {
        eintrag["name"]: eintrag["I"] for eintrag in _anfrage(urls[0], "GET", "/names")[1]
    }
    zeilen: list[str] = []
    if versehen and nummer in TRENNUNG:
        getrennt = nummer == TRENNUNG[0]
        url = urls[namen_geraete.index(_DORAS_ZWEITGERAET)]
        _anfrage(url, "POST", "/getrennt", {"getrennt": getrennt})
        zustand = "vom Netz getrennt" if getrennt else "wieder verbunden"
        zeilen.append(f"Takt {nummer}, {_DORAS_ZWEITGERAET}: {zustand}")
    for (geraet, _datei, personen), url in zip(geraete, urls):
        for person in sorted(personen):
            I = namen[person]
            aufgaben: list[dict[str, Any]] = _anfrage(url, "GET", f"/tasks/{I}")[1]
            rumpfe = absichten(geraet, person, I, aufgaben)
            if geraet == _DORAS_ZWEITGERAET:
                assert gesehen is not None
                vorher = gesehen.get((geraet, person), [])
                gesehen[(geraet, person)] = rumpfe
                rumpfe = verzoegert(rumpfe, vorher)
            if not rumpfe:
                continue
            kopf = f"Takt {nummer}, {geraet}: {person}"
            if len(_anfrage(url, "GET", f"/tips/{I}")[1]) > 1:
                if (geraet, person) not in gemeldet:
                    gemeldet.add((geraet, person))
                    zeilen.append(f"{kopf} hat sich widersprochen und handelt hier nicht weiter.")
                continue
            for rumpf in rumpfe:
                zeilen.append(_einliefern(url, kopf, rumpf))
    if nummer == ANTRAG_TAKT:
        url = urls[namen_geraete.index(_ANTRAG_GERAET)]
        rumpf = {
            "I": namen[_ANTRAG_PERSON],
            "art": "propose",
            "scope": _vereinsscope(url),
            "change": ANTRAG,
        }
        zeilen.append(_einliefern(url, f"Takt {nummer}, {_ANTRAG_GERAET}: {_ANTRAG_PERSON}", rumpf))
    return zeilen
