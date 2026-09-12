# 00ar — ALWAYS_BOUND: CONTRIBUTING.md aufnehmen

**Branch:** `00ar-o53-contributing-method` (bereits ausgecheckt)
**Basis-Commit:** `7116659`

## Normative Grundlage

`tools/check_specs.py`, `ALWAYS_BOUND` (frozenset). `README.md` steht dort bereits mit dem
Kommentar „Projektsicht von aussen; niemand muss sie mit Abschnitt zitieren" (D318 hat das
Muster eingeführt). `CONTRIBUTING.md` ist mit diesem Lauf neu im Wurzelverzeichnis entstanden
und trägt denselben Charakter: eine Datei für externe Leser, kein Layer, keine Datei, die
jemand mit `§`-Abschnitt zitieren wird.

## Auftrag

In `tools/check_specs.py`, im `ALWAYS_BOUND`-Frozenset, einen weiteren Eintrag ergänzen:

```python
"CONTRIBUTING.md",  # Projektsicht für Mitwirkende von aussen; niemand zitiert sie mit Abschnitt
```

Position: alphabetisch oder thematisch neben `README.md` einsortieren, wie es die bestehende
Reihenfolge des Sets nahelegt — kein hartes Muss, nur Lesbarkeit.

## Ausdrückliche Nicht-Ziele

- Keine anderen Einträge in `ALWAYS_BOUND` anfassen.
- `docs/METHOD.md` **nicht** aufnehmen — sie liegt nicht im Wurzelverzeichnis, `ROOT.glob("*.md")`
  erfasst sie ohnehin nicht, ein Eintrag dafür wäre wirkungslos und irreführend.
- `LAYER_FILES` nicht anfassen.
- Keine weiteren Dateien ändern. Kein Reflow, keine Kommentar-Kosmetik an bestehenden Zeilen.

## Abgeleitete Abnahmekriterien

Vor der Änderung, gemessen auf `7116659`: `make check` meldet `gebunden: 29, ungebunden: 4`,
mit `CONTRIBUTING.md` in der ungebunden-Liste. Nach der Änderung muss gelten:

- `gebunden: 30, ungebunden: 3` — die ungebunden-Liste enthält nur noch
  `00aq-nachtrag-prompt.md`, `00aq-werkzeuge-prompt.md`, `sitzungsstart-00ap.md`.
- `make check` bleibt vollständig grün: 797 Tests weiterhin bestehen, `ruff` weiterhin sauber.
- Kein Diff außerhalb von `tools/check_specs.py`.

Diese Werte sind aus dem Lauf selbst abzulesen (vorher/nachher), nicht aus dieser Beschreibung
abzutippen.

## Abschluss

Ein Commit auf `00ar-o53-contributing-method`, kein Merge. Vollständiger `git diff` gegen
`7116659` im Bericht.
