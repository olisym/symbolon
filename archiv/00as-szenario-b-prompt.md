# Prompt 00as — Szenario B, Vertrauensentzug als Durchsetzung

## Modus

Prototyp nach D311 Beschluss 1. Der Szenario-Code ist Wegwerfcode. Es gibt keine Golden
Numbers, keine Rücknahmeproben, keine Zweitimplementierung, keine Abnahme gegen erwartete
Zahlen. Was zählt, sind die **Befunde**: jede Stelle, an der die Spec keine Antwort hat, eine
falsche gibt, oder eine erzwingt, die ein Zentrum voraussetzt.

**Ausnahme vom Wegwerf-Status:** Die Erweiterung von `tools/sim/szenario.py` (siehe unten) ist
**kein** Wegwerfcode — es ist der geteilte Rahmen, den auch `tests/test_sim.py` benutzt. Sie
bekommt normale Sorgfalt, aber keinen eigenen Registereintrag für sich allein; sie wird im
selben Commit gemeldet wie der Rest.

Erfinde nichts still. Eine Entscheidung, die weder Spec noch Prompt hergibt: **triff sie,
markiere sie im Bericht als Befund, begründe sie.**

## Branch und Basis

Branch `00as-szenario-b`, abgezweigt vom Kopf von `main` (Commit `b3b3c04` oder danach — lies
den tatsächlichen Kopf zu Beginn und nenne ihn im Bericht). Ein Commit am Ende, kein Merge.

## Normative Grundlage

- `07-decisions.md`: **D313** (die offen gelassene Frage — „ob Vertrauensentzug als
  Durchsetzung reicht, wo Teambrella Mittelsperrung braucht"), **D236** (Exit statt
  Ausschluss, dieselbe Grenze: unbestreitbar, nicht erzwungen), **D327** (O1/O2 verortet,
  keine Verwahrerrolle im Protokoll).
- `02-trust-flow.md §4` (Vertrauen als Fluss, Min-Cut-Bound), `§7` (Partitionstoleranz,
  Widerruf hat Vorrang), `§3.1` (Vouch-Gewicht, Selbstbindungsbudget).
- `03-profiles.md §3.3.2` (`settlement()`, Tilgungszustand), `§2.1` (`accusation@1`, opak).
- Widerruf: `core/revoke@1`, selbst-bezüglich, `J = (2, claim_id(target))`. Ein Vouch ist
  widerrufbar; eine Obligation ist es nach `example_nucleus`-Verfassung **nicht**
  (`irrevocable_predicates` in `N_res`) — das ist bereits so gebaut, nicht neu zu entscheiden.

Lies D313 und D236 vor Beginn.

## Was gemessen werden soll, bevor gebaut wird (Prüfregel 63)

`tools/sim/szenario.py`, Funktion `_schritt_claim`: das Prädikat-Dict kennt aktuell
`accept-rules`, `vote`, `propose`, `ratify`, `vouch`. Es fehlen `obligation` und `revoke`. Prüfe
das nach, bevor du erweiterst — vielleicht hat sich das seit diesem Prompt schon geändert.

## Was gebaut wird

**Erstens, im Rahmen selbst:** `_schritt_claim` um zwei Prädikate erweitern:

- `obligation`: `J` wie bei `vouch` aus `step["subject"]` auflösen (Ziel der Verpflichtung),
  `v` analog zu den anderen Wert-tragenden Prädikaten aus `step` (schau dir an, wie `vouch`
  sein `n` codiert, und übertrage das Muster auf das, was `obligation@1` nach `03 §3.3.1`
  tatsächlich für `v` verlangt — lies die Sektion, bevor du rätst).
- `revoke`: `J = (2, claim_id(ctx.labels[step["target"]]))`, `p = "core/revoke@1"` (ohne
  Scope-Präfix `nuc:` — das ist ein Core-Prädikat, kein Nukleus-Prädikat, prüfe das gegen
  `mensch_als_republik/predicates.py`, bevor du es festschreibst).

**Zweitens, das eigentliche Szenario**, als JSON unter `tools/sim/scenarios/` (throwaway,
nicht in `tests/test_sim.py` aufgenommen) plus ein kurzes Treiberskript, das `run_scenario`
aufruft und die Befunde druckt:

1. Aufbau über `beispielnukleus` (liefert bereits einen Vouch-Graphen unter `anna`, `bruno`,
   `chris` in `N_res`, siehe `tools/example_nucleus.py`).
2. Chris signiert eine `obligation@1` an Anna (`N_res`). Keine `receipt@1` folgt — die
   Obligation bleibt offen.
3. **Baseline messen:** `zeige was=trust subject=chris anchors=[anna,bruno]` — Distanz,
   Kapazität, Kantenzahl, wie im Rahmen vorgesehen.
4. Anna widerruft ihren Vouch auf Chris (`core/revoke@1`, `J` zeigt auf den ursprünglichen
   Vouch-Claim — den musst du labeln, falls er das noch nicht ist, oder in
   `tools/example_nucleus.py` nachsehen, ob er schon ein Label trägt).
5. Zustellen an alle vier.
6. **Nachher messen:** derselbe `trust`-Schritt auf Chris. Vergleiche Distanz/Kapazität vorher
   und nachher.
7. **Settlement messen:** `settlement()` auf die Obligation aus Schritt 2, vor und nach dem
   Widerruf. Erwartung, die zu prüfen ist, nicht zu unterstellen: der Tilgungszustand ändert
   sich durch den Widerruf **nicht** — Layer 02 und Layer 03 sind entkoppelt. Wenn das nicht
   stimmt, ist **das** der wichtigste Befund des Laufs.

## Die Prüfung

- Ändert sich Kapazität/Distanz zu Chris messbar? Um wie viel, und ist das aus `02 §4`
  ableitbar oder musstest du es empirisch ablesen?
- Ändert sich der Tilgungszustand der Obligation? Sollte nicht — begründe, falls doch.
- Gibt es einen Unterschied zwischen den vier Beobachtern (Partitionstoleranz, `02 §7`), oder
  sehen alle nach dem Zustellschritt dasselbe?
- Ist die Kapazitätsminderung, gemessen an `TrustParams(C0=100, gamma_num=1, gamma_den=2,
  D=100)` (Vorgabe aus `szenario.py`), gross genug, um als Aussage über „Durchsetzung" zu
  taugen, oder bleibt sie marginal, weil nur eine von mehreren Vouch-Kanten entfällt? Das ist
  eine Messung, keine Vermutung — rechne mit den tatsächlichen Werten aus dem Lauf.

## Nicht-Ziele

- Keine Änderung an `mensch_als_republik/`, an einer Layer-Datei, an `07-decisions.md` oder
  `pruefregeln.md`.
- Keine Schlichtung, kein `submit-arbitration`, kein `verdict`, kein `accusation@1` in diesem
  Lauf — das bleibt Stufe C.
- Kein neues Prädikat ausser `obligation` und `revoke` im Rahmen.
- Keine Änderung an `tests/test_sim.py` — die Erweiterung von `szenario.py` muss die
  bestehenden sechs Szenarien unverändert bestehen lassen (`python -m pytest tests/test_sim.py
  -q`).
- Kein Merge, kein Push nach `main`.

## Abschluss

Ein Commit auf `00as-szenario-b`. `git add` mit expliziten Pfaden.

Melde:

1. Die Ausgabe des Laufs, gekürzt auf das Lesbare.
2. **Die Befundliste**, mit Zahlen, nicht nur Beschreibung: Kapazität/Distanz vorher/nachher,
   Tilgungszustand vorher/nachher.
3. Ob `python -m pytest tests/test_sim.py -q` weiterhin sechs von sechs besteht.
4. Den vollständigen `git diff` gegen den Branchpunkt.

Wenn der Durchlauf an einer Stelle nicht weitergeht, ist der benannte Abbruch das bessere
Ergebnis als ein Durchlauf, der über die Stelle hinweggeht.
