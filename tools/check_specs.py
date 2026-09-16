#!/usr/bin/env python3
"""Prüft die Spec-Dateien auf Defekte, die beim Editieren entstehen.

Fängt genau die Klasse von Fehlern, die in der Rev-2-Sitzung aufgetreten ist:
Markdown-Autoformatierung escaped Bezeichner, Heredocs zerhacken Multibyte-Zeichen,
Registereinträge verschwinden beim Zurückkopieren.

Aufruf: make check-specs
Rückgabe: 0 sauber, 1 Befund.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SPECS = sorted(
    (q.name for q in ROOT.glob("*.md")),
    key=lambda n: (not n[0].isdigit(), n),
)

# Escapes, die legitim vorkommen: als Fußnotenmarker und in grep-/Regex-Ausdrücken
# sowie in Markdown-Tabellenzellen. Alles andere ist Editor-Schaden.
ALLOWED_ESCAPES = set("*|.b")

# Bezeichner, die als `\_` verstümmelt in der Spec auftauchen können. Ein escapter
# Unterstrich in Backticks rendert mit sichtbarem Backslash und ist damit falsch.
NEVER_ESCAPED = set("_{}[]<>#")


def read(path: Path) -> str | None:
    """Liest UTF-8 und meldet die Byte-Position bei Defekt."""
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        ctx = raw[max(0, exc.start - 40) : exc.start + 40]
        print(f"  UTF-8 defekt bei Byte {exc.start}: {exc.reason}")
        print(f"    Kontext: {ctx!r}")
        return None


def check_escapes(text: str) -> list[str]:
    """Backslash-Escapes, die kein Markdown-Autor absichtlich setzt."""
    found: dict[str, int] = {}
    for match in re.finditer(r"\\(.)", text, re.S):
        char = match.group(1)
        if char in ALLOWED_ESCAPES:
            continue
        found[char] = found.get(char, 0) + 1

    problems = []
    for char, count in sorted(found.items()):
        marker = "  ← Editor-Autoformatierung" if char in NEVER_ESCAPED else ""
        problems.append(f"escapte Zeichen: \\{char} ({count}x){marker}")
    return problems


def check_line_length(text: str) -> list[str]:
    """Prosa höchstens 100 Zeichen; Tabellenzeilen und Codeblöcke ausgenommen (D222).

    Gezählt wird mit ``len()`` über den dekodierten Text, nicht in Bytes.
    Führende Leerzeichen und Blockzitat-Zeichen samt folgenden Leerzeichen
    werden nur für die Klassifikation abgezogen.
    """
    problems: list[str] = []
    in_code = False
    for line_no, line in enumerate(text.splitlines(), 1):
        body = line.lstrip(" \t")
        while body.startswith(">"):
            body = body[1:].lstrip(" \t")
        if body.startswith("```"):
            in_code = not in_code
            continue
        if in_code or body.startswith("|"):
            continue
        n = len(line)
        if n > 100:
            problems.append(f"Zeile {line_no} zu lang: {n} Zeichen")
    return problems


def check_control_chars(text: str) -> list[str]:
    """Ersetzungszeichen und unsichtbare Steuerzeichen aus fehlgeschlagenen Kopien."""
    problems = []
    if "\ufffd" in text:
        problems.append(f"Ersetzungszeichen U+FFFD ({text.count(chr(0xFFFD))}x)")
    for line_no, line in enumerate(text.splitlines(), 1):
        for char in line:
            if unicodedata.category(char) == "Cc" and char != "\t":
                problems.append(f"Steuerzeichen U+{ord(char):04X} in Zeile {line_no}")
                break
    if "\r" in text:
        problems.append("CRLF-Zeilenenden")
    return problems


# Überschriften: "### D28 — ..." und kombiniert "### D16 / D22 — ..."
HEADING = re.compile(r"^### (D\d+(?:\s*/\s*D\d+)*)\s+—", re.M)


def decision_numbers(text: str) -> list[int]:
    """Alle im Register definierten D-Nummern, auch aus kombinierten Überschriften."""
    numbers = []
    for heading in HEADING.findall(text):
        numbers += [int(n) for n in re.findall(r"D(\d+)", heading)]
    return numbers


def check_decisions(text: str) -> list[str]:
    """Register: D-Einträge lückenlos und ohne Dubletten.

    Die Reihenfolge wird NICHT geprüft — das Register ist thematisch nach
    Abschnitten geordnet, nicht numerisch. Das ist Absicht.
    """
    numbers = decision_numbers(text)
    problems = []

    if not numbers:
        return ["keine D-Einträge gefunden"]

    seen: set[int] = set()
    for num in numbers:
        if num in seen:
            problems.append(f"D{num} doppelt")
        seen.add(num)

    missing = sorted(set(range(1, max(numbers) + 1)) - seen)
    if missing:
        problems.append("fehlend: " + ", ".join(f"D{n}" for n in missing))

    return problems


def check_references(text: str, known: set[int]) -> list[str]:
    """Verweise auf D-Nummern, die es im Register nicht gibt."""
    referenced = {int(n) for n in re.findall(r"\bD(\d+)\b", text)}
    unknown = sorted(referenced - known)
    if unknown:
        return [
            "verweist auf unbekannte Entscheidung: "
            + ", ".join(f"D{n}" for n in unknown)
        ]
    return []


# Zuordnung Präfix → Layer-Datei. Explizite Tabelle, kein Glob: 03 und 04
# bezeichnen je vier Dateien (D209). Die gleichnamigen Abnahme-Dateien sind
# nicht die Ziele der Kurzform; die Tabelle bindet die Kurzform, und der
# Dateiname bindet sich selbst (D219, D230).
LAYER_FILES = {
    "00": "00-nucleus-genesis-constitution.md",
    "01": "01-claim-atom.md",
    "02": "02-trust-flow.md",
    "03": "03-profiles.md",
    "04": "04-governance.md",
    "05": "05-enforcement.md",
    "06": "06-services.md",
    "07": "07-decisions.md",
    "08": "08-scope.md",
    "01a": "01a-policy-prompt.md",
    "02a": "02a-maxflow-prompt.md",
    "02b": "02b-golden-anchors.md",
    "04a": "04a-korrektur-prompt.md",
}

# Gebunden ohne Paragraphenverweis, weil sie selbst der Einstieg sind (D314 Beschluss 2).
ALWAYS_BOUND = frozenset(
    {
        "pruefregeln.md",  # das Regelwerk; Volltext der Prüfregeln, Einstieg jeder Sitzung
        "README.md",  # Projektsicht von aussen; niemand muss sie mit Abschnitt zitieren
        "CONTRIBUTING.md",  # Projektsicht für Mitwirkende von aussen; niemand zitiert sie mit Abschnitt
        "VISION.md",  # Absicht, nicht Layer, aber der Einstieg in die Leitsätze
        "werkzeuge.md",  # Werkzeugschicht ohne Layer-Nummer
        "example-nucleus.md",  # gerechnetes Beispielobjekt, Anker der Tests
        "02-golden-anchors.md",  # Ankerdatei zu 02; 02b steht bereits in LAYER_FILES
        "03-golden-anchors.md",  # Ankerdatei zu 03
        "arbeitsweise.md",  # stabile Disziplin; Einstieg nach D316, niemand zitiert sie mit Abschnitt
        "offen.md",  # nummerierte Posten; Einstieg nach D316, niemand zitiert sie mit Abschnitt
    }
)


def latest_handoff(root_md: set[str]) -> str | None:
    """Jüngste Übergabedatei der Wurzel, oder None (D314, D316).

    Kandidaten sind Namen in ``root_md``, die mit ``sitzungsstart-`` beginnen
    und auf ``.md`` enden. Verglichen wird der Teil zwischen Präfix und Endung.
    Es gewinnt der längere; bei gleicher Länge der alphabetisch spätere.
    Kein Kandidat bindet nichts und ist kein Fehler.
    """
    best: tuple[int, str, str] | None = None
    for name in root_md:
        if not name.startswith("sitzungsstart-") or not name.endswith(".md"):
            continue
        infix = name[len("sitzungsstart-") : -len(".md")]
        key = (len(infix), infix, name)
        if best is None or key > best:
            best = key
    if best is None:
        return None
    return best[2]


HEADING_NUM = re.compile(r"^#{2,4} ((?:[A-Z]\.)?\d+(?:\.\d+)*)", re.M)
SECTION_REF = re.compile(
    r"(?<![A-Za-z0-9.-])([A-Za-z0-9-]+(?:\.md)?)`? §((?:[A-Z]\.)?\d+(?:\.\d+)*)"
    r"(?:[–-]§((?:[A-Z]\.)?\d+(?:\.\d+)*))?"
)
SHORT_NAME = re.compile(r"0[0-8][a-z]?$")

# Anhangsverweise: Kurzform-Name, optional Backtick, Leerzeichen, dann entweder
# "Anhang" mit Grossbuchstabe und optionaler Nummer oder Grossbuchstabe, Punkt,
# Nummer ohne das Wort. Ein einzelner Buchstabe ohne "Anhang" wird nicht erkannt.
# Dateinamen- und Bereichsformen sind bewusst nicht enthalten (D401 Beschluss 4).
APPENDIX_REF = re.compile(
    r"(?<![A-Za-z0-9.-])(0[0-8][a-z]?)`? "
    r"(?:Anhang ([A-Z])(?:\.(\d+(?:\.\d+)*))?|([A-Z])\.(\d+(?:\.\d+)*))"
    r"(?![A-Za-z0-9]|\.\d)"
)

# Überschriften der Form "## Anhang <Buchstabe>" (D401 Beschluss 2).
APPENDIX_HEADING = re.compile(r"^## Anhang ([A-Z])", re.M)


def layer_headings() -> dict[str, frozenset[str]]:
    """Überschriftennummern der Ebene 2–4 je Layer-Datei und je Wurzel-Stamm (D209, D221).

    Dazu die Buchstaben der Überschriften ``## Anhang <Buchstabe>`` (D401
    Beschluss 2). Die Buchstaben tragen keine Ziffer und kollidieren nicht mit
    den Überschriftennummern.
    """
    result: dict[str, frozenset[str]] = {}
    for name in SPECS:
        text = read(ROOT / name)
        if text is None:
            nums = frozenset()
        else:
            nums = frozenset(HEADING_NUM.findall(text))
            nums |= frozenset(APPENDIX_HEADING.findall(text))
        result[name.removesuffix(".md")] = nums
    for prefix, name in LAYER_FILES.items():
        result[prefix] = result[name.removesuffix(".md")]
    return result


def heading_covers(wanted: str, headings: frozenset[str]) -> bool:
    """Getroffen bei genauer Nummer oder bei Nummer plus Punkt (D209)."""
    if wanted in headings:
        return True
    prefix = wanted + "."
    return any(heading.startswith(prefix) for heading in headings)


def check_section_refs(
    text: str, headings: dict[str, frozenset[str]]
) -> tuple[int, list[str]]:
    """Verweise mit Kurzform oder Dateiname gegen die Zieldatei (D209, D219, D221, D228).

    Drei Klassen (D221): Kurzform über ``LAYER_FILES``, Dateiname über den
    Stamm einer Wurzel-``.md``-Datei, sonst übergangen. Ein Kurzform-Name
    ohne Tabelleneintrag ist ein Befund (D219). Ein fehlender Dateistamm
    ist keiner. Ein Bereich ``NAME §A–§B`` bindet beide Nummern an denselben
    Namen (D228). Dazu Anhangsverweise: Kurzform-Name, dann ``Anhang`` mit
    Buchstabe und optionaler Nummer oder Buchstabe, Punkt, Nummer (D401).
    Ein Buchstabe allein zählt, wenn die Zieldatei ``## Anhang`` mit diesem
    Buchstaben trägt; ein Buchstabe mit Nummer über ``heading_covers``.
    Rückgabe: Zahl der aufgelösten Verweise, Befunde.
    """
    unknown_names: dict[str, int] = {}
    counts: dict[str, int] = {}
    appendix_counts: dict[str, int] = {}
    n_resolved = 0
    for match in SECTION_REF.finditer(text):
        name = match.group(1)
        sections = [match.group(2)]
        if match.group(3) is not None:
            sections.append(match.group(3))
        if SHORT_NAME.fullmatch(name):
            if name not in headings:
                unknown_names[name] = unknown_names.get(name, 0) + len(sections)
                n_resolved += len(sections)
                continue
        else:
            stem = name.removesuffix(".md")
            if f"{stem}.md" not in SPECS:
                continue
        for section in sections:
            n_resolved += 1
            ref = f"{name} §{section}"
            counts[ref] = counts.get(ref, 0) + 1
    for match in APPENDIX_REF.finditer(text):
        name = match.group(1)
        if name not in headings:
            unknown_names[name] = unknown_names.get(name, 0) + 1
            n_resolved += 1
            continue
        word = match.group(2) is not None
        letter = match.group(2) if word else match.group(4)
        number = match.group(3) if word else match.group(5)
        ref = f"{name} Anhang {letter}" if word else f"{name} {letter}"
        if number is not None:
            ref += f".{number}"
        n_resolved += 1
        if number is None:
            covered = letter in headings[name]
        else:
            covered = heading_covers(f"{letter}.{number}", headings[name])
        if not covered:
            appendix_counts[ref] = appendix_counts.get(ref, 0) + 1
    problems: list[str] = []
    for name in sorted(unknown_names):
        problems.append(f"unbekannter Zitiername: {name} ({unknown_names[name]}x)")
    for ref in sorted(counts):
        prefix, section = ref.split(" §", 1)
        key = prefix.removesuffix(".md")
        if not heading_covers(section, headings[key]):
            problems.append(
                f"verweist auf unbekannten Abschnitt: {ref} ({counts[ref]}x)"
            )
    for ref in sorted(appendix_counts):
        problems.append(
            f"verweist auf unbekannten Anhang: {ref} ({appendix_counts[ref]}x)"
        )
    return n_resolved, problems


def check_bare_refs(text: str, headings: dict[str, frozenset[str]]) -> list[str]:
    """Bare Paragraphenverweise: § plus Ziffer, kein auflösbarer Name davor (D227).

    Auflösbar wie in ``check_section_refs``: Kurzform über ``LAYER_FILES`` oder
    Stamm einer Wurzel-``.md``. Von ``SECTION_REF`` gebundene Bereiche decken
    beide Nummern (D228). Rückgabe: Befunde, leer wenn keiner.
    """
    covered: list[tuple[int, int]] = []
    for match in SECTION_REF.finditer(text):
        name = match.group(1)
        if SHORT_NAME.fullmatch(name):
            if name not in headings:
                continue
        else:
            stem = name.removesuffix(".md")
            if f"{stem}.md" not in SPECS:
                continue
        covered.append((match.start(), match.end()))
    n_bare = 0
    for match in re.finditer(r"§\d", text):
        pos = match.start()
        if any(start <= pos < end for start, end in covered):
            continue
        n_bare += 1
    if n_bare:
        return [f"barer Paragraphenverweis ({n_bare}x)"]
    return []


def section_ref_target(name: str, root_md: set[str]) -> str | None:
    """Wurzeldatei, die ein Abschnittsverweis nennt, oder None (D221, D314).

    Dieselbe Auflösung wie ``check_section_refs``: Kurzform über ``LAYER_FILES``,
    sonst Stamm einer Wurzel-``.md``. Kein neuer Ausdruck, nur das Ziel.
    """
    if SHORT_NAME.fullmatch(name):
        return LAYER_FILES.get(name)
    filename = f"{name.removesuffix('.md')}.md"
    if filename in root_md:
        return filename
    return None


def bound_root_files() -> tuple[frozenset[str], frozenset[str]]:
    """Gebundene und ungebundene Markdown-Dateien der Wurzel (D314).

    Eine Wurzeldatei ist gebunden, wenn sie in ``LAYER_FILES`` oder
    ``ALWAYS_BOUND`` steht, oder die jüngste Übergabedatei ist (siehe
    ``latest_handoff``), oder wenn eine Python-Datei (ausserhalb von
    ``archiv/``) oder eine *andere gebundene* Markdown-Datei der Wurzel sie
    in der Form eines Abschnittsverweises nennt. Eine blosse namentliche
    Nennung bindet nicht. Eine Quelle, die selbst ungebunden ist, bindet
    nicht: sonst fiele die gebundene Datei mit dem Archivieren der Quelle
    wieder heraus.
    """
    root_md = set(SPECS)
    cited_from_md: dict[str, set[str]] = {name: set() for name in SPECS}
    cited_from_py: set[str] = set()

    for name in SPECS:
        text = read(ROOT / name)
        if text is None:
            continue
        for match in SECTION_REF.finditer(text):
            target = section_ref_target(match.group(1), root_md)
            if target is None or target == name:
                continue
            cited_from_md[name].add(target)

    for path in python_sources():
        if "archiv" in path.parts:
            continue
        text = read(path)
        if text is None:
            continue
        for match in SECTION_REF.finditer(text):
            target = section_ref_target(match.group(1), root_md)
            if target is None:
                continue
            cited_from_py.add(target)

    bound: set[str] = set(LAYER_FILES.values()) & root_md
    bound.update(ALWAYS_BOUND & root_md)
    handoff = latest_handoff(root_md)
    if handoff is not None:
        bound.add(handoff)
    bound.update(cited_from_py & root_md)
    growing = True
    while growing:
        growing = False
        for source in list(bound):
            for target in cited_from_md.get(source, ()):
                if target not in bound:
                    bound.add(target)
                    growing = True

    return frozenset(bound), frozenset(root_md - bound)


def report_binding() -> None:
    """Meldet gebundene und ungebundene Wurzeldateien; kein Befund (D314 Beschluss 4)."""
    bound, unbound = bound_root_files()
    print(f"gebunden: {len(bound)}, ungebunden: {len(unbound)}")
    if unbound:
        print("ungebunden:")
        for name in sorted(unbound):
            print(f"  {name}")


def python_sources() -> list[Path]:
    """``.py`` unter der Wurzel, ohne ``.venv``, stabil sortiert (D215)."""
    return sorted(p for p in ROOT.rglob("*.py") if ".venv" not in p.parts)


def check_python_section_refs(
    headings: dict[str, frozenset[str]],
) -> tuple[int, int, list[tuple[str, list[str]]]]:
    """``check_section_refs`` und ``check_bare_refs`` über alle Python-Dateien
    (D215, D221, D227).

    Rückgabe: Dateizahl, Zahl der aufgelösten Verweise, Befunde je Relativpfad.
    """
    files = python_sources()
    n_refs = 0
    findings: list[tuple[str, list[str]]] = []
    for path in files:
        text = read(path)
        if text is None:
            findings.append((str(path.relative_to(ROOT)), ["UTF-8 defekt"]))
            continue
        n_resolved, problems = check_section_refs(text, headings)
        problems += check_bare_refs(text, headings)
        n_refs += n_resolved
        if problems:
            findings.append((str(path.relative_to(ROOT)), problems))
    return len(files), n_refs, findings


def main() -> int:
    register = ROOT / "07-decisions.md"
    known: set[int] = set()
    if register.exists():
        text = read(register)
        if text:
            known = set(decision_numbers(text))

    headings = layer_headings()
    failures = 0
    for name in SPECS:
        path = ROOT / name
        if not path.exists():
            continue

        problems: list[str] = []
        text = read(path)
        if text is None:
            print(f"FEHLER {name}")
            failures += 1
            continue

        problems += check_escapes(text)
        problems += check_control_chars(text)
        problems += check_line_length(text)
        if name == "07-decisions.md":
            problems += check_decisions(text)
        if known:
            problems += check_references(text, known)
        excepted = name == "07-decisions.md" or name.startswith("sitzungsstart-")
        if not excepted:
            _, section_problems = check_section_refs(text, headings)
            problems += section_problems

        if problems:
            print(f"FEHLER {name}")
            for problem in problems:
                print(f"  {problem}")
            failures += 1
        else:
            lines = text.count("\n") + 1
            print(f"  ok  {name:36} {lines:>5} Zeilen")

    n_py, n_py_refs, py_findings = check_python_section_refs(headings)
    if py_findings:
        for rel, problems in py_findings:
            print(f"FEHLER {rel}")
            for problem in problems:
                print(f"  {problem}")
            failures += 1
    else:
        print(f"  ok  {'Python-Dateien':36} {n_py:>5} Dateien, {n_py_refs} Verweise")

    if failures:
        print(f"\n{failures} Datei(en) mit Befund.")
        report_binding()
        return 1

    print(f"\nAlle Spec-Dateien sauber. Register: D1–D{max(known)}.")
    report_binding()
    return 0


if __name__ == "__main__":
    sys.exit(main())
