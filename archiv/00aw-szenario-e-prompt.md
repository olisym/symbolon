# Prompt 00aw — Szenario E: Equivocation unter Partition

**Branch:** `00aw-szenario-e`, Basis-Commit `8b07dce`.
**Normative Grundlage:** D340 (Fork), `01 §4` / `symbolon/atom.py::is_equivocation_pair`,
`symbolon/verifier.py::_is_in_equivocation_pair`/`State.EQUIVOCATION_FLAGGED`,
`tools/autor.py::gabeln()` (D129), `symbolon/trust/derive.py`
(`equivocation_flagged_authors` → vollständiger Ausschluss aller Vouch-Gruppen des
Autors).

## Auftrag

Neue Datei `tools/sim/szenario_e.py`, Wegwerf-Treiber. Bausteine aus
`tools/sim/szenario_c.py` (Rollen A/B/Z/C, `_baseline`, `_welt`, `run_schritte_weiter`)
und `tools/sim/szenario.py` (`run_schritte`, `_trust_row`, `_classify_row`)
wiederverwenden, nicht duplizieren. Keine Änderung an einer der bestehenden Dateien.

**Gemeinsame Bausteine (nach `_baseline()`):**

1. `{"art": "claim", "autor": B, "praedikat": "vouch", "scope": "res", "subject": Z,
   "n": 40, "t": 2, "t_exp": T_EXP, "label": "fork_b_dora",
   "kette_fortschreiben": false}` — die Gabel.
2. `{"art": "claim", "autor": B, "praedikat": "vouch", "scope": "res", "subject": C,
   "n": 30, "t": 2, "t_exp": T_EXP, "label": "real_b_chris"}` — reale Hälfte,
   **gleicher `h_prev`** wie (1), da `gabeln()` die Spitze nicht vorrückt.
3. `{"art": "claim", "autor": B, "praedikat": "vouch", "scope": "res", "subject": A,
   "n": 20, "t": 3, "t_exp": T_EXP, "label": "legit_b_anna"}` — unbeteiligt, neuer
   `h_prev` (nach (2)), kein Teil des Paars.

**Lauf 1 „Getrennte Partition"** — eigener, unabhängiger Kontext:
`{"zustellen", "von": B, "an": [Z], "nur": ["fork_b_dora"]}` (nur an dora, dauerhaft,
sonst niemand),
`{"zustellen", "von": B, "an": [A, C], "nur": ["real_b_chris", "legit_b_anna"]}` (nur an
anna/chris, dora bekommt sie **nie**). Danach `_trust_row(ctx, "dora", ["chris"])` und
`_trust_row(ctx, "anna", ["chris"])` für alle vier Teilnehmer ausgeben — erwartet: jede
Zeile zeigt einen in sich unauffälligen, aber zwischen dora einerseits und chris/anna/
bruno andererseits **unterschiedlichen** Wert, kein Fehler.

**Lauf 2 „Späte Konvergenz"** — eigener, unabhängiger Kontext:
`{"zustellen", "von": B, "an": [A, C], "nur": ["real_b_chris", "legit_b_anna"]}` sofort.
Danach `_classify_row(ctx, "real_b_chris")` und `_trust_row(ctx, "dora"/"anna",
["chris"])` (nur chris' Zeile relevant, alle vier ausgeben) als „vorher" drucken —
erwartet: `active`, unauffällige Werte. Danach
`{"zustellen", "von": B, "an": [C], "nur": ["fork_b_dora"]}` — die verspätete
Konvergenz, nur an chris. Danach dieselben drei Messungen erneut als „nachher" — erwartet:
`classify(real_b_chris)` bei chris jetzt `equivocation_flagged`; `trust(chris→dora)` und
`trust(chris→anna)` (chris' eigene Zeile) beide niedriger als vorher.

**`main()`** druckt beide Läufe und einen Abschnitt „Befunde", der beide Erwartungen
explizit bestätigt/widerlegt benennt.

## Ausdrückliche Nicht-Ziele

- Keine Änderung an `symbolon/`, `welt.py`, `szenario.py`, `szenario_c.py`.
- Keine Anklage/Verdikt-Maschinerie — reine Vouch-/Equivocation-Frage.
- Keine Golden Numbers, kein Rollback-Probe (D311/D340 Szenariomodus).
- Kein Merge nach `main` ohne Abnahme durch den Supervisor.

## Abnahmekriterien (abgeleitet, nicht getippt)

- `python -m pytest -q` bleibt unverändert grün.
- `tools/check_specs.py` bleibt sauber.
- Skriptlauf (`python -m tools.sim.szenario_e`) erzeugt für beide Erwartungen je eine
  explizite Aussage im „Befunde"-Abschnitt.
- Abschluss: ein Commit auf `00aw-szenario-e`, vollständiger `git diff` gegen `8b07dce`
  für die Abnahme, kein Merge.
