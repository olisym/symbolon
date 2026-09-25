"""Prüft, ob Quelldateien unversioniert im Arbeitsbaum liegen.

Der Anlass: die vollständige Layer-02b-Implementierung (elf Dateien) lag als untracked
im Arbeitsbaum, während `main` einen Merge-Commit trug, der sie zu enthalten behauptete.
Alle Testläufe liefen gegen den Arbeitsbaum; der committete Stand war ungeprüft, und ein
`git clean -fd` hätte die Schicht gelöscht.

Ein schmutziger Arbeitsbaum ist beim Arbeiten normal und daher **kein** Fehler — eine
unversionierte Quelldatei ist es fast nie.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Unversioniert in diesen Bereichen ist ein vergessenes `git add`, kein Zwischenstand.
SOURCE_DIRS = ("symbolon/", "tests/", "tools/")
SOURCE_SUFFIXES = (".py",)
# .js, .html und .json nur unter symbolon/ (D481 Beschluss 5).
STATIC_SUFFIXES = (".js", ".html", ".json")

# Unversionierte Spec-Dateien im Wurzelverzeichnis zählen ebenso.
ROOT_SUFFIXES = (".md",)


def is_source(path: str) -> bool:
    """Quelldatei, einschließlich statischer Dateien unter symbolon/ (D481 Beschluss 5)."""
    if path.startswith(SOURCE_DIRS) and path.endswith(SOURCE_SUFFIXES):
        return True
    if path.startswith("symbolon/") and path.endswith(STATIC_SUFFIXES):
        return True
    return "/" not in path and path.endswith(ROOT_SUFFIXES)


def porcelain() -> list[str] | None:
    """Gibt None zurück, wenn hier kein Git-Repository liegt."""
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain=v1", "--untracked-files=all"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None
    if out.returncode != 0:
        return None
    return [line for line in out.stdout.splitlines() if line.strip()]


def main() -> int:
    lines = porcelain()
    if lines is None:
        print("  --  kein Git-Repository, Arbeitsbaum-Prüfung übersprungen")
        return 0

    untracked_source: list[str] = []
    untracked_other: list[str] = []
    modified = 0

    for line in lines:
        status, _, path = line[:2], line[2], line[3:]
        path = path.strip().strip('"')
        if status == "??":
            (untracked_source if is_source(path) else untracked_other).append(path)
        else:
            modified += 1

    if untracked_source:
        print("FEHLER  unversionierte Quelldateien im Arbeitsbaum:")
        for path in sorted(untracked_source):
            print(f"        {path}")
        print()
        print("        Diese Dateien sind in keinem Commit. Tests laufen gegen sie,")
        print("        ein frischer Clone hat sie nicht, `git clean -fd` löscht sie.")
        print("        Entweder `git add`, oder in .gitignore aufnehmen.")
        return 1

    parts = []
    if modified:
        parts.append(f"{modified} geändert")
    if untracked_other:
        parts.append(f"{len(untracked_other)} unversioniert (nicht Quellcode)")
    suffix = f" ({', '.join(parts)})" if parts else " (sauber)"
    print(f"  ok  Arbeitsbaum: keine unversionierten Quelldateien{suffix}")

    for path in sorted(untracked_other):
        print(f"        ?  {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
