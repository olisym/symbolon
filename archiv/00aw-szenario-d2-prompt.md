# Prompt 00aw — Szenario D′: saubere Isolierung von (a) und (b)

**Branch:** `00aw-szenario-d2`, Basis-Commit `f282ea4`.
**Normative Grundlage:** D338 (Fork), D336/D337 (Befund und Fehleranalyse),
`symbolon/profiles/verdict.py` (`UNKNOWN_ACCUSATION`; `State.PENDING` gilt nur Layer 01).

## Auftrag

Neue Datei `tools/sim/szenario_d2.py`, Wegwerf-Treiber. Wiederverwendbare Bausteine aus
`tools/sim/szenario_c.py` (Rollen A/B/Z/C, `_baseline`, `_bis_verdikt`,
`run_schritte_weiter`) und aus `tools/sim/szenario_d.py`
(`_bis_verdikt_ohne_acc_verdict_zustellung`, `_verdict_status_namen`) importieren, nicht
duplizieren. Keine Änderung an einer der bestehenden Dateien.

Drei Läufe, **vollständig unabhängig** — je ein eigener `run_schritte(...)`-Aufruf, kein
geteilter Kontext zwischen den Läufen.

**Lauf 1 „Broadcast".** Kontrolle, identisch zu Stufe C / Szenario D Lauf 1: Baseline +
`_bis_verdikt()`. `_verdict_status_row`, `_trust_row(..., B, [C])` für alle vier
ausgeben.

**Lauf 2 „Umordnung" (korrigiert).** Baseline +
`_bis_verdikt_ohne_acc_verdict_zustellung()`. `verdict_z` zugestellt an **bruno und
chris** (nicht anna) vor `acc_a_b`. Direkt danach `verdict_status` (beschränkt auf bruno,
chris, via `_verdict_status_namen`) und `classify(verdict_z)` für dieselben zwei ausgeben
— erwartet: `ATTRIBUTED_OPINION` + `UNKNOWN_ACCUSATION`, `classify` = `active` (nicht
`pending`). Danach `acc_a_b` an alle nachliefern, erneut auswerten — erwartet: `BINDING`
bei beiden (sofern dieselbe Pfad-ii-Bedingung erfüllt ist wie in Lauf 1).

**Lauf 3 „Dauerhafter Verlust" (korrigiert).** Baseline + `_bis_verdikt()` unverändert
(volle Zustellung, Verdikt bindet für alle wie Lauf 1). Danach Widerruf von
`vouch_c_b` signieren, zustellen nur an bruno, chris, dora — **niemals an anna. Keine
Uhrmanipulation in diesem Lauf.** `_trust_row(..., B, [C])` für alle vier ausgeben —
erwartet: anna identisch zu Lauf 1, bruno/chris/dora zeigen den Nach-Widerruf-Wert.

**`main()`** druckt alle drei Läufe und einen Abschnitt „Befunde", der (a) und (b) je
explizit bestätigt/widerlegt benennt, mit den jetzt korrekten Erwartungen aus D338.

## Ausdrückliche Nicht-Ziele

- Keine Änderung an `symbolon/`, `welt.py`, `szenario.py`, `szenario_c.py`,
  `szenario_d.py`.
- (c) wird **nicht** wiederholt — bereits in D337 unkonfundiert bestätigt.
- Keine Golden Numbers, kein Rollback-Probe (D311/D336 Szenariomodus).
- Kein Merge nach `main` ohne Abnahme durch den Supervisor.

## Abnahmekriterien (abgeleitet, nicht getippt)

- `python -m pytest -q` bleibt unverändert grün (neue Datei berührt keine bestehenden
  Tests).
- `tools/check_specs.py` bleibt sauber.
- Skriptlauf (`python -m tools.sim.szenario_d2`) erzeugt für (a)/(b) je eine explizite
  Aussage im „Befunde"-Abschnitt.
- Abschluss: ein Commit auf `00aw-szenario-d2`, vollständiger `git diff` gegen `f282ea4`
  für die Abnahme, kein Merge.
