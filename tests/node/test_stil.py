"""Farben der Seite als Variablen, hell und dunkel lesbar (D511 Beschluss 3).

Der Test liest `style.css`: außerhalb der beiden Blöcke mit Variablen steht keine Farbe; jede
Variable ist in beiden Blöcken gesetzt; jede Regel, die `color` und `background` zugleich setzt,
hält 4,5 zu 1 in beiden Modi, dazu der Text von `body` auf dem Hintergrund von `.links`. Die Paare
kommen aus der Datei. Kontrast nach WCAG 2.1: relative Leuchtdichte, (L1 + 0,05) / (L2 + 0,05).
"""

from __future__ import annotations

import re
from pathlib import Path

_DATEI = Path("symbolon/node/static/style.css")
_MINDESTENS = 4.5

_HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
_FUNKTION = re.compile(r"\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\(", re.I)
_VAR = re.compile(r"var\((--[\w-]+)\)")
# Eigenschaften, deren Farbe nur aus einer Variable kommen darf.
_NUR_VARIABLE = {"color", "background", "background-color", "border-color"}
_MIT_FARBE = {"border", "border-top", "border-right", "border-bottom", "border-left", "outline"}
_TEIL = re.compile(r"([^{}]*)([{}])")
_DUNKEL = re.compile(r"@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)\s*\{")


def _ohne_kommentare(text: str) -> str:
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


def _deklarationen(rumpf: str) -> dict[str, str]:
    out = {}
    for teil in rumpf.split(";"):
        if ":" in teil:
            name, wert = teil.split(":", 1)
            out[name.strip()] = " ".join(wert.split())
    return out


def _zerlegen() -> tuple[dict[str, str], dict[str, str], list[tuple[str, dict[str, str]]]]:
    """Die Variablen hell (`:root`), dunkel (`:root` in der Medienabfrage) und die übrigen Regeln."""
    text = _ohne_kommentare(_DATEI.read_text(encoding="utf-8"))
    hell: dict[str, str] | None = None
    dunkel: dict[str, str] | None = None
    regeln = []
    medien: list[str] = []
    pos = 0
    while (treffer := _TEIL.match(text, pos)) is not None:
        kopf = " ".join(treffer.group(1).split())
        pos = treffer.end()
        if treffer.group(2) == "}":
            medien.pop()
            continue
        if kopf.startswith("@"):
            medien.append(kopf)
            continue
        ende = text.index("}", pos)
        rumpf = _deklarationen(text[pos:ende])
        pos = ende + 1
        if kopf == ":root" and not medien:
            assert hell is None, "zwei Blöcke :root außerhalb einer Medienabfrage"
            hell = rumpf
        elif kopf == ":root" and medien and _DUNKEL.fullmatch(medien[-1] + " {"):
            assert dunkel is None, "zwei dunkle Blöcke :root"
            dunkel = rumpf
        else:
            regeln.append((kopf, rumpf))
    assert text[pos:].strip() == "" and medien == [], "Klammern in style.css nicht ausgeglichen"
    assert hell is not None, "kein Block :root"
    assert dunkel is not None, "kein Block :root in @media (prefers-color-scheme: dark)"
    return hell, dunkel, regeln


def _variablen(block: dict[str, str]) -> dict[str, str]:
    return {name: wert for name, wert in block.items() if name.startswith("--")}


def _rgb(wert: str) -> tuple[int, int, int]:
    ziffern = wert.lstrip("#")
    if len(ziffern) == 3:
        ziffern = "".join(z * 2 for z in ziffern)
    assert len(ziffern) == 6, f"nur #rgb und #rrggbb sind messbar: {wert}"
    return tuple(int(ziffern[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _leuchtdichte(wert: str) -> float:
    """Relative Leuchtdichte nach WCAG 2.1."""

    def kanal(c: int) -> float:
        s = c / 255
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4

    r, g, b = (kanal(c) for c in _rgb(wert))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _kontrast(a: str, b: str) -> float:
    hoch, tief = sorted((_leuchtdichte(a), _leuchtdichte(b)), reverse=True)
    return (hoch + 0.05) / (tief + 0.05)


def _eine_variable(wert: str) -> str:
    treffer = _VAR.fullmatch(wert)
    assert treffer, f"keine einzelne Variable: {wert}"
    return treffer.group(1)


def _paare(regeln: list[tuple[str, dict[str, str]]]) -> list[tuple[str, str, str]]:
    """(Regel, Variable des Texts, Variable des Hintergrunds) aus der Datei."""
    paare = []
    for kopf, rumpf in regeln:
        grund = rumpf.get("background-color", rumpf.get("background"))
        if "color" in rumpf and grund is not None:
            paare.append((kopf, _eine_variable(rumpf["color"]), _eine_variable(grund)))
    body = [rumpf for kopf, rumpf in regeln if kopf == "body"]
    links = [rumpf for kopf, rumpf in regeln if kopf == ".links" and "background" in rumpf]
    assert len(body) == 1 and len(links) == 1, "body oder .links fehlt"
    paare.append(
        ("body auf .links", _eine_variable(body[0]["color"]), _eine_variable(links[0]["background"]))
    )
    return paare


def test_keine_feste_farbe_ausserhalb_der_variablen() -> None:
    """Außerhalb der beiden Blöcke steht keine Farbe, nur Variablen (D511 Beschluss 1 und 3)."""
    _, _, regeln = _zerlegen()
    fest = []
    for kopf, rumpf in regeln:
        for name, wert in rumpf.items():
            if _HEX.search(wert) or _FUNKTION.search(wert):
                fest.append((kopf, name, wert))
            elif name in _NUR_VARIABLE and not _VAR.fullmatch(wert):
                fest.append((kopf, name, wert))
            elif name in _MIT_FARBE and wert != "none" and not _VAR.search(wert):
                fest.append((kopf, name, wert))
    assert fest == []


def test_jede_variable_in_beiden_bloecken() -> None:
    """Jede Variable ist hell und dunkel gesetzt, und jede verwendete ist gesetzt (D511 Beschluss 3)."""
    hell, dunkel, regeln = _zerlegen()
    assert hell.get("color-scheme") == "light dark"
    hell_var, dunkel_var = _variablen(hell), _variablen(dunkel)
    assert hell_var
    assert sorted(set(hell_var) - set(dunkel_var)) == []
    assert sorted(set(dunkel_var) - set(hell_var)) == []
    verwendet = {name for _, rumpf in regeln for wert in rumpf.values() for name in _VAR.findall(wert)}
    assert sorted(verwendet - set(hell_var)) == []


def test_kontrast_hell_und_dunkel() -> None:
    """Jedes Paar aus Text und Hintergrund hält 4,5 zu 1 in beiden Modi (D511 Beschluss 2 und 3)."""
    hell, dunkel, regeln = _zerlegen()
    paare = _paare(regeln)
    zu_schwach = []
    for modus, werte in (("hell", _variablen(hell)), ("dunkel", _variablen(dunkel))):
        for kopf, text, grund in paare:
            verhaeltnis = _kontrast(werte[text], werte[grund])
            if verhaeltnis < _MINDESTENS:
                zu_schwach.append((modus, kopf, text, grund, round(verhaeltnis, 2)))
    assert zu_schwach == []
