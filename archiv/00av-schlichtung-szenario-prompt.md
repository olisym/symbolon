# Prompt 00av — Szenario: Rechenschaft ohne Bindung (Stufe C, D332)

**Branch:** `00av-schlichtung-szenario`
**Basis-Commit:** `6b46273`
**Modus:** Prototyp nach D311. Szenario-Code ist Wegwerfcode. Es gelten **nicht**:
Registerpflicht für den Code, Golden Numbers, Rücknahmeproben, Zweitimplementierung, Abnahme
gegen einen Prompt-Commit im üblichen Sinn. Es gelten **weiter**: die Spec als normative
Wahrheit, das Register als oberste Instanz, und dass eine Messung eine Position ändern können
muss. Ins Register wandert ausschliesslich der **Befund**.

## Normative Grundlage

- `03-profiles.md §2` (Verdikt-Cluster), insbesondere §2.3 (wann ein Bond schlitzt) und §2.4
  (Bindungskraft, `verdict_status()`, Pfade (i)/(ii)).
- `05-enforcement.md §5` (subjektive Verdikte als attribuierte, beobachtergewichtete Meinungen;
  Anklage-Stake) und §6 (Haftungsreichweite, Bond-Slash).
- `02-trust-flow.md` (Distanz, Kapazität `C(x) = ⌊C₀·γ^d⌋`, Fluss, Pfade; Vouch/Widerruf-Mechanik).
- D311 (Prototypmodus), D328 (Messmethode: Baseline/Nachher-Vergleich derselben Kennzahlen,
  unabhängig nachbaubar), D332 (dieser Fork, Hypothese und Erwartung).

**Vor jeder neuen Zeile Code:** `tools/sim/szenario.py` und die vorhandenen Prädikate
(`claim`, `zustellen`, `uhr`, `zeige`, `erwarte`, `obligation`, `revoke`, `zeige was=settlement`,
`flow`/`paths` in `trust`-Zeilen) lesen. Prüfregel 63 gilt: erst messen, ob ein Prädikat für
`accusation`, `verdict`, `submit-arbitration` und `verdict_status()`-Auswertung schon existiert,
bevor eines gebaut wird.

## Auftrag

Ein Szenario mit mindestens vier Beteiligten: `A` (Ankläger), `B` (Beschuldigter), `Z`
(Schiedsrichter), `C` (Beobachter). Baseline-Vertrauensstruktur analog `00as`: `C` hat vor
Szenariobeginn sowohl zu `B` als auch zu `Z` einen aktiven Vouch, sodass `trust_flow(C, Z) > 0`
und `B` über mindestens zwei Pfade erreichbar ist (Redundanz wie in D328, damit der Trust-Flow-
Effekt überhaupt messbar ist und nicht durch eine triviale Kappung verdeckt wird).

**Zwei Phasen, aus demselben Baseline-Zustand geklont (nicht sequenziell auf demselben Zustand
gefahren — sonst vermischen sich die Effekte):**

**Phase 1 — Verdikt bindet.**
1. `B` und `A` unterwerfen sich beide `Z` per `submit-arbitration@1` im selben Schlichtungs-
   Kontext `N`.
2. `A` klagt `B` an (`accusation@1`, subjektiver Fehlertyp, z. B. „nicht geliefert" auf eine
   bestehende `obligation`, nicht Equivocation — das läuft mechanisch, nicht über ein Verdikt).
3. `Z` urteilt (`verdict@1`, Ausgang gegen `B`).
4. `verdict_status()` auswerten. **Erwartet:** `BINDING` über Pfad (ii) — beide Unterwerfungen
   sind aktiv.
5. `C` widerruft seinen Vouch auf `B` (bestehendes Prädikat `revoke`).
6. Messen: Distanz, Kapazität, Fluss, Pfade zu `B` aus Sicht von `C`, vor und nach dem Widerruf
   (dieselben Kennzahlen wie D328). Bond-Zustand von `B` (falls ein Bond hinterlegt war) vor und
   nach `verdict_status()`.

**Phase 2 — Verdikt entzogen, auf frischer Baseline-Kopie.**
1. Identischer Ausgangszustand wie Phase 1, Schritte 1–3 identisch.
2. **Vor** der Auswertung von `verdict_status()`: `B` widerruft seine `submit-arbitration@1`
   (`core/revoke@1`).
3. `verdict_status()` auswerten. **Erwartet:** `ATTRIBUTED_OPINION` — Pfad (ii) trägt nicht mehr
   (§2.4.3: Bindung entfällt mit dem Widerruf).
4. Beobachter-Policy für `C`, im Szenario-Skript festgeschrieben, nicht im Protokoll: **`C`
   widerruft denselben Vouch auf `B`, wenn `trust_flow(C, Z) > 0`.** Diese Bedingung mit der
   vorhandenen Trust-Flow-Funktion auswerten, nicht neu erfinden.
5. Dieselben Kennzahlen messen wie in Phase 1, Schritt 6. Bond-Zustand von `B` vor und nach
   `verdict_status()`.

**Vergleich, als letzter Schritt:** die in Phase 1 und Phase 2 gemessenen Trust-Flow-Kennzahlen
nach dem jeweiligen Vouch-Widerruf nebeneinanderstellen. Bond-Zustand beider Phasen
nebeneinanderstellen.

## Nicht-Ziele

- **Keine neue Formel oder kein neuer Mechanismus** für „Gewicht eines Verdikts = Vertrauen des
  Beobachters in den Schiedsrichter". Geprüft wird nur, ob sich die im Szenario **angenommene**
  Beobachter-Regel (`revoke, wenn trust_flow(C,Z) > 0`) mit vorhandenen Layer-02/03-Funktionen
  ausdrücken lässt — nicht, ob eine bessere Regel denkbar wäre.
- **Keine Änderung** an `03-profiles.md`, `05-enforcement.md`, `02-trust-flow.md` oder
  `verdict_status()` selbst.
- **Kein Bau** eines neuen Bond-Slash- oder Reputations-Primitivs.
- **Keine Verschmelzung** mit den bestehenden `tools/sim`-Tests; das Szenario ist ein eigener,
  zusätzlicher Lauf, bestehende Tests bleiben unverändert grün.
- **Keine Aussage über Severity-Policy** (welcher Ausgang welche Enforcement-Stufe auslöst) — das
  ist laut `03 §2.2` ausdrücklich Policy, nicht Gegenstand dieses Laufs.

## Abnahmekriterien (abgeleitet, nicht getippt)

1. `verdict_status()` liefert in Phase 1 `BINDING`, in Phase 2 `ATTRIBUTED_OPINION` — abgeleitet
   direkt aus den Pfad-(i)/(ii)-Bedingungen in `03 §2.4`, nicht aus einer im Prompt getippten
   Erwartungstabelle.
2. Die gemessenen Trust-Flow-Kennzahlen (Distanz, Kapazität, Fluss, Pfade) nach dem jeweiligen
   Vouch-Widerruf sind in Phase 1 und Phase 2 identisch — oder die Abweichung ist benannt und
   erklärt, nicht stillschweigend hingenommen.
3. Der Bond-Zustand unterscheidet sich zwischen den Phasen: Phase 1 slasht (falls ein Bond
   hinterlegt war), Phase 2 nicht — konsistent mit `03 §2.3`.
4. Eine Befundliste im D312-Standard: keine Erfindung, um eine Phase zu retten; jede Abweichung
   von der in D332 benannten Erwartung wird gemeldet, nicht stillschweigend angepasst.
5. Bestehende Gesamtsuite bleibt unverändert grün (aktuell 797), `check_specs.py` sauber.

## Abschluss

Ein Commit auf `00av-schlichtung-szenario`, vollständiger `git diff` gegen `6b46273`. Kein Merge.
