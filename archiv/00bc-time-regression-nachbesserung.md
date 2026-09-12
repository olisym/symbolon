# 00bc — Nachbesserung `time-regression` (D357, D358)

## Branch und Basis

Branch `time-regression`, aufsetzend auf `8a23862`. Ein zusätzlicher Commit, kein Merge, kein
Rebase. Der Branchpunkt bleibt `b76be14`; abgenommen wird der **Branch**, nicht der einzelne
Commit.

Der Lauf `8a23862` ist inhaltlich richtig und hat sich bei den roten Szenarien korrekt verhalten:
gemeldet statt angepasst. Zwei Punkte sind nachzubessern, einer davon geht auf einen Fehler im
ersten Prompt zurück.

## Normative Grundlage

- **D358** (`07-decisions.md`, auf `main` ab `662047c`): ein Vektor muss den Zustand, den er
  belegt, im **vollständigen** Vektorspeicher annehmen, nicht nur in einem für ihn gebauten
  Store. Andockpunkt ist ein kinderloses Kettenende, sofern nicht die Geschwisterschaft selbst
  der Gegenstand ist.
- **D357** (ebenda): `t` in den Szenarien war Dekoration. Die Szenariodaten werden umgetaktet,
  die `erwarte`-Blöcke bleiben unverändert.

## Auftrag

### 1. NV32 umhängen

Der erste Prompt hat `TV1` als Anker vorgegeben. Das war falsch: NV32 bekommt damit dasselbe
`(I, h_prev)` wie TV2 und ist dessen Equivocation-Geschwister. Gemessene Folge im vollständigen
Vektorspeicher — NV32 ist `equivocation_flagged` statt `time_regression_flagged`, und TV2 kippt
von `active` nach `equivocation_flagged`.

Neuer Anker ist `TV6`, das kinderlose Ende von Alices Kette:

- `h_prev = claim_id(tv6)`, `t = 1_700_000_409` gegen TV6s `t = 1_700_000_410`.
- Der NV32-Block wandert in `tests/vectors/gen.py` **hinter** `tv6 = _finalize(...)`; vorher ist
  `tv6` nicht gebunden.
- Felder sonst unverändert: `J = (3, CONST)`, `p = P_ACCEPT`, `N`, kein `expect_reject`.
- `vectors_01.json` durch Lauf von `gen.py` neu erzeugen, nicht von Hand.

Prüfe und melde: kein anderer Vektor ändert seine `claim_id`, und es entsteht keine neue
Gruppe von Claims mit gleichem `(I, h_prev)`.

### 2. Tests zu NV32 nachziehen

- Die beiden NV32-Tests legen `TV6` statt `TV1` in den Store.
- **Neu**, und der eigentliche Punkt aus D358: ein Test über den **vollständigen**
  Vektorspeicher — alle Vektoren mit `signed_bytes` in einen Store, dann
  `classify_all`. Erwartet wird, dass NV32 `TIME_REGRESSION_FLAGGED` ist **und** TV2 `ACTIVE`
  bleibt. Die zweite Zusicherung ist die Gegenprobe gegen den hier behobenen Defekt; ohne sie
  fällt der Fehler beim nächsten neuen Vektor wieder unter den Tisch.

`tests/trust/test_coupling.py` wird **nicht** erweitert. Der Test dort prüft
`classify_all == classify` und `trust_usable == (state == ACTIVE)`, nicht konkrete Zustände —
er konnte deshalb nie rot werden und ist der falsche Ort.

### 3. Szenarien umtakten (D357)

Genau drei Stellen im gesamten Szenarienbestand verletzen die Monotonie, alle dieselbe: Annas
`vote` trägt `t = 1`, nachdem ihr eigenes `propose` `t = 2` trug. In `s2.json` zweimal, weil das
Szenario zwei Welten aufsetzt, in `s3.json` einmal. Annas Stimme bekommt ein `t` hinter ihrem
Vorschlag.

Bruno und Chris tragen durchgehend `t = 1`, liegen also im erlaubten Gleichstand — nicht
anfassen. Ein `welt`-Schritt setzt die Ketten zurück; über ihn hinweg zu vergleichen erzeugt
Scheinverstöße.

**Kein `erwarte`-Block wird angefasst.** Dass die Reihe danach grün ist, ohne dass eine
Erwartung bewegt wurde, ist der Beleg dafür, dass die Erwartungen richtig waren und die Welt
falsch. Kippt eine Erwartung trotzdem: melden, nicht anpassen.

### 4. Rücknahmeprobe für den neuen Volltest

Den Einschub in `verifier.py` entfernen und bestätigen, dass der neue Volltest aus Abschnitt 2
rot wird. Wird er es nicht, ist NV32 im geteilten Korpus weiterhin ungedeckt — dann **nicht**
weiterbauen, sondern melden. Genau diese Probe hat den Defekt sichtbar gemacht.

### 5. Testzahl klären

Der Bericht zu `8a23862` meldet „808 passed, 2 failed". 798 bestehende plus die zehn benannten
Tests ergeben 808 **gesamt**, also 806 grün bei zwei roten. Melde die tatsächliche Zahl der neu
hinzugekommenen Testfunktionen und, falls sie über zehn liegt, welche im Diff des ersten Laufs
nicht sichtbar waren.

## Nicht-Ziele

- **Kein Rebase, kein Merge, kein Push nach `main`.**
- **Keine Markdown-Datei** außer dieser Prompt-Datei selbst.
- **`GOLDEN` und `GOLDEN_SIGMA` in `tests/test_vectors_01.py` bleiben unverändert.** NV32 wird
  dort nicht eingetragen; die Liste ist bewusst unvollständig.
- **Kein bestehender Vektor wird umgehängt, umbenannt oder neu gerechnet.**
- **Kein `erwarte`-Block, kein Golden Anchor, keine bestehende Erwartung** wird nachgezogen.
- Keine weiteren Szenarien anfassen; genau die drei benannten Stellen.
- Keine Änderung an Einschub, Zustand, `BUDGET_STATES` oder `credit.py` — die sind abgenommen.

## Abnahme

1. `make check` grün.
2. Der Volltest aus Abschnitt 2 vorhanden und grün.
3. Die Rücknahmeprobe aus Abschnitt 4 belegt.
4. Kein Vektor außer NV32 hat eine geänderte `claim_id`.
5. `git diff --numstat` gegen `8a23862` zeigt keine Markdown-Datei außer dieser.

## Abschluss

Ein Commit auf `time-regression`. Melde zurück:

- den **vollständigen** `git diff` gegen den Branchpunkt `b76be14`, also den ganzen Branch,
  nicht nur diesen Commit;
- die neuen Werte für NV32: `core`-Map wie in Anhang C geschrieben, `signed_bytes`, `claim_id`,
  `σ`, und den Vorgänger mit seinem `t`;
- das Ergebnis der Rücknahmeprobe mit der Liste der rot gewordenen Tests;
- die Antwort auf Abschnitt 5;
- jede Stelle, an der du diesem Prompt nicht folgen konntest oder ihn für widersprüchlich
  hältst, als Liste am Ende.
