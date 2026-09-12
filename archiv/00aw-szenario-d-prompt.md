# Prompt 00aw — Szenario D: Rechenschaft unter Partition

**Branch:** `00aw-szenario-d`, Basis-Commit `be6cbea`.
**Normative Grundlage:** D336 (Fork), D332/D333 (Stufe-C-Baseline und -Befund),
`01-claim-atom.md §6` (`now` lokal/subjektiv), `symbolon/verifier.py::State.PENDING`,
`symbolon/profiles/verdict.py::ProfileFinding.UNRESOLVED_ACCUSED`.

## Auftrag

Neue Datei `tools/sim/szenario_d.py`, Wegwerf-Treiber nach dem Vorbild von
`tools/sim/szenario_c.py` (gleicher Stil: `run_schritte`/`run_schritte_weiter` aus
`tools/sim/szenario.py`, keine neue Mini-Sprache, keine neuen Primitive in `welt.py` oder
`szenario.py` — alles Vorhandene wiederverwenden).

Rollen wie Stufe C: A=anna (Ankläger), B=bruno (Beschuldigter), Z=dora (Schiedsrichter,
nicht in `arbitrators`), C=chris (Beobachter). Baseline identisch zu
`szenario_c.py::_baseline()` und `_bis_verdikt()` (Vouch-Graph C→B/C→Z/Z→B, Obligation B→A,
zwei `submit-arbitration`, `accusation`, `verdict`) — importieren oder duplizieren, wie es dem
Stil des Moduls besser entspricht; keine Änderung an `szenario_c.py` selbst.

**Lauf 1 „Broadcast".** Baseline + `_bis_verdikt()` unverändert (wie Stufe-C-Phase-1 bis zum
Verdikt). Danach `_verdict_status_row`, `_trust_row(..., anchors=["chris"])` für alle vier
Teilnehmer ausgeben.

**Lauf 2 „Funkstille".** Gleicher Baustein-Satz, aber:
1. `acc_a_b` wird signiert, aber **zunächst nicht zugestellt**. `verdict_z` wird signiert und
   per `zustellen(von=dora, an=["anna","chris"], nur=["verdict_z"])` **vor** `acc_a_b`
   zugestellt. Direkt danach `_verdict_status_row`/`_classify_row(..., "verdict_z")` für anna
   und chris ausgeben — erwartet: `PENDING` bzw. `UNRESOLVED_ACCUSED`, kein Fehler/Exception.
   Danach `acc_a_b` an alle nachliefern, erneut auswerten — erwartet: gleicher Endzustand wie
   Lauf 1 bei anna/chris.
2. Revoke von `vouch_c_b` (wie Stufe-C-Phase-1) wird signiert und nur an bruno und dora
   zugestellt (`an=["bruno","dora"]`), **niemals an anna**. `_trust_row(..., "bruno",
   anchors=["chris"])` für alle vier ausgeben — erwartet: anna zeigt weiterhin den
   Vor-Widerruf-Wert, bruno/chris/dora den Nach-Widerruf-Wert, kein Fehler.
3. Vor Schritt 2 die Uhr von anna weit über `T_EXP` der Vouch `vouch_c_b` setzen
   (`teilnehmer["anna"].write_now(...)`, deutlich > `T_EXP=1001000`), während bruno/chris/dora
   bei `now=1000` bleiben. `_classify_row(..., "vouch_c_b")` ausgeben — erwartet: nur anna zeigt
   `expired`.

**`main()`** druckt beide Läufe strukturiert (analog `szenario_c.py`) und am Ende einen
Abschnitt „Befunde", der jede der drei Erwartungen (a)/(b)/(c) explizit als
bestätigt/widerlegt benennt (Text, kein Assert-Abbruch nötig — Szenariomodus).

## Ausdrückliche Nicht-Ziele

- Keine Änderung an `symbolon/`, `welt.py`, `szenario.py` oder `szenario_c.py`.
- Keine Zufalls-/Netzwerksimulation, kein neuer Zustellmodus — nur die vorhandenen
  `zustellen(nur=...)`-Aufrufe mit gezielten Teilnehmerlisten.
- Keine Golden Numbers, kein Rollback-Probe (D311/D332 Szenariomodus).
- Kein Merge nach `main` ohne Abnahme durch den Supervisor.

## Abnahmekriterien (abgeleitet, nicht getippt)

- `python -m pytest -q` bleibt unverändert grün (neue Datei berührt keine bestehenden Tests).
- `tools/check_specs.py` bleibt sauber (neue Prompt-Datei zitiert nur bestehende
  Spec-Referenzen).
- Skriptlauf (`python -m tools.sim.szenario_d`) erzeugt für (a)/(b)/(c) je eine explizite
  Aussage im „Befunde"-Abschnitt.
- Abschluss: ein Commit auf `00aw-szenario-d`, vollständiger `git diff` gegen `be6cbea` für die
  Abnahme, kein Merge.
