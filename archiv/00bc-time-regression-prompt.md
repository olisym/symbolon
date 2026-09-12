# 00bc — `time-regression-flagged` implementieren (D353, D356)

## Branch und Basis

Branch `time-regression`, abgezweigt von dem Commit, der diese Datei einführt. Ein Commit am
Ende, kein Merge, kein Push nach `main`.

## Normative Grundlage

Nicht erfinden, nicht auslegen — diese Stellen sind bereits beschlossen und im Baum:

- `01-claim-atom.md §6`, Block „Zeit — `t` ist monoton entlang der Autorenkette (normativ)":
  Regel, Nicht-Reject, die drei Abgrenzungen, Stellung in der Zustandsmaschine.
- `01-claim-atom.md` Anhang B.1: die Zeile `time-regression-flagged`.
- `02a-maxflow-prompt.md §2.6`: Budget-Set einschließlich `TIME_REGRESSION_FLAGGED`.
- `03-profiles.md §3.3.2`: `INDETERMINATE` mit Vermerk `OBLIGATION_TIME_REGRESSION`, dazu die
  beiden Vermerktabellen in `03 §6`.
- `07-decisions.md` D353 und D356: Begründungen und verworfene Alternativen.

Widerspricht eine Messung diesem Prompt oder einer dieser Stellen: **melden, nicht anpassen.**
Keine bestehende Erwartung, kein Golden Anchor und kein bestehender Vektor wird nachgezogen,
um einen Test grün zu bekommen.

## Auftrag

### 1. Zustand in `symbolon/verifier.py`

`State` bekommt `TIME_REGRESSION_FLAGGED = "time_regression_flagged"`, eingefügt nach
`EQUIVOCATION_FLAGGED`.

In `classify` liegt der Vorgänger bereits vor und wird heute verworfen:

```
pred_ok, _ = _predecessor_known_and_valid(claim, store)
```

Das zweite Element ist der Vorgänger-Claim. Es wird gebunden statt verworfen; ein zusätzlicher
Store-Zugriff ist weder nötig noch erlaubt. Ist der Vorgänger vorhanden und gilt
`claim.t < pred.t`, ist das Ergebnis `Classification(state=State.TIME_REGRESSION_FLAGGED,
trust_usable=False)`.

Reihenfolge in der Zustandsmaschine, unverändert bis auf den Einschub:

1. Scope-Prüfung der Policy
2. `FOREIGN_LIFECYCLE`
3. `EQUIVOCATION_FLAGGED`
4. `PENDING`
5. **`TIME_REGRESSION_FLAGGED`** (neu)
6. `SUPERSEDED`, `REVOKED`
7. `LINKED`, `EXPIRED`, `ACTIVE`

Genesis-Claims haben keinen Vorgänger (`_predecessor_known_and_valid` liefert `True, None`) und
werden nicht geprüft. `core/*` wird mitgeprüft — die Ausnahme aus `01 §5.3` betrifft `t_exp`
und nicht diese Regel. Gleichstand (`claim.t == pred.t`) ist erlaubt.

### 2. Derselbe Einschub in `symbolon/index.py`

`classify_all` führt dieselbe Zustandsmaschine ein zweites Mal. Der Einschub steht dort an
derselben Stelle, mit derselben Bedingung und demselben Ergebnis. Die beiden Pfade werden
getrennt getestet (siehe Abnahme) — ein Test, der nur einen von beiden trifft, deckt den
anderen nicht ab.

### 3. `symbolon/trust/groups.py`

`BUDGET_STATES` nimmt `State.TIME_REGRESSION_FLAGGED` auf (`02a §2.6`, D356). `_in_budget_set`
bleibt im Übrigen unverändert, insbesondere die eigenständige Ablaufprüfung.

### 4. `symbolon/profiles/credit.py` und `symbolon/profiles/findings.py`

`ProfileFinding` bekommt `OBLIGATION_TIME_REGRESSION = "OBLIGATION_TIME_REGRESSION"`, eingefügt
nach `OBLIGATION_AUTHOR_FLAGGED`.

In `settlement` steht der neue Zweig neben dem `EQUIVOCATION_FLAGGED`-Zweig und vor den
`assert`-Zeilen: Vermerk `OBLIGATION_TIME_REGRESSION` mit der `claim_id` der Obligation als
Subjekt, Ergebnis `SettlementState.INDETERMINATE`, `receipt_claim_id=None`. Die Restmenge der
`assert`-Zeilen bleibt unverändert.

### 5. Vektor NV32 in `tests/vectors/gen.py`

Ein Claim, der auf einen bekannten Vorgänger kettet und ein kleineres `t` trägt. Bauform
parallel zu TV2: derselbe Autor ALICE, `accept-rules`, verkettet auf `TV1.claim_id`, aber
`t = 1_700_000_000 - 1`, also kleiner als TV1s `t`. Kein `expect_reject` — NV32 ist wie NV3
kein Reject-Vektor, sondern ein Zustandsvektor.

Kommentar im Stil der Nachbarn, aber **ohne** Verweis auf einen Anhang-C-Abschnitt: nur
`(D353)`. Der Abschnitt in `01` Anhang C entsteht erst nach diesem Lauf, aus den hier
erzeugten Werten.

`vectors_01.json` wird durch Lauf von `gen.py` neu erzeugt, nicht von Hand bearbeitet. Prüfe,
dass alle bestehenden Einträge byte-gleich bleiben und nur NV32 hinzukommt.

### 6. Tests

Alle erwarteten Mengen und Werte werden **abgeleitet**, nicht getippt.

- `classify` auf NV32 (Vorgänger im Store) liefert `TIME_REGRESSION_FLAGGED`,
  `trust_usable` ist `False`.
- `classify_all` auf derselben Welt liefert für dieselbe `claim_id` denselben Zustand. Eigener
  Test, nicht derselbe Test mit anderem Aufruf.
- Gleichstand: ein Claim mit `t == pred.t` ist `ACTIVE`.
- Genesis ohne Vorgänger wird nicht geprüft.
- Unbekannter Vorgänger bleibt `PENDING`, auch wenn der Claim bei bekanntem Vorgänger
  zurückdatiert wäre.
- `core/*` wird mitgeprüft: ein `core/revoke@1` mit kleinerem `t` als sein Vorgänger ist
  `TIME_REGRESSION_FLAGGED`.
- Vorrang: ein Claim, der zugleich in einem Equivocation-Paar steht und zurückdatiert ist,
  ist `EQUIVOCATION_FLAGGED`. Ein Claim, der zurückdatiert und widerrufen ist, ist
  `TIME_REGRESSION_FLAGGED`.
- Budget-Set: statt einer getippten Aufzählung prüft der Test
  `BUDGET_STATES == set(State) - {State.LINKED, State.EXPIRED}`. Diese Form ist Absicht — sie
  wird bei jedem künftigen Zustand rot und erzwingt dort eine Entscheidung, statt sie still
  ausfallen zu lassen. Kommentar im Test mit Verweis auf D135 und D356.
- `settlement` auf eine zurückdatierte Obligation liefert `INDETERMINATE` und genau den
  Vermerk `OBLIGATION_TIME_REGRESSION` mit der `claim_id` der Obligation.

### 7. Rücknahmeprobe

Für die beiden Klassifikationspfade getrennt durchzuführen und im Bericht getrennt zu belegen:

1. Den Einschub in `verifier.py` entfernen, Testreihe laufen lassen, festhalten **welche**
   Tests rot werden.
2. Einschub zurück, Einschub in `index.py` entfernen, Testreihe laufen lassen, festhalten
   welche Tests rot werden.
3. Beide Einschübe zurück, `make check` grün.

Wird in Schritt 1 oder 2 kein Test rot, ist der betroffene Pfad ungedeckt. Dann **nicht**
weiterbauen, sondern melden — ein Regressionstest, der die Regression nicht sieht, ist keiner
(D352).

## Nicht-Ziele

Was hier nicht steht, wird gemeldet und nicht gebaut.

- **Keine Änderung an Markdown-Dateien.** Weder Spec, noch Register, noch Anhang C. Der
  Anhang-C-Abschnitt für NV32 wird nach diesem Lauf aus den erzeugten Werten gesetzt.
- **`02-trust-flow.md` bleibt unberührt** — dort ist die Budget-Zugehörigkeit als Prädikat
  formuliert und nicht als Aufzählung (D356, ausdrücklich).
- **`include_flagged` wird nicht angefasst** (D39, D356): das ist ein Autor-Flag, der neue
  Zustand flaggt den Claim.
- **`_is_temporally_valid`, `now` und der gesamte `t_exp`-Pfad bleiben unverändert.**
  Insbesondere keine Arbeit an einem Intervall-`now` — das ist mit D355 zurückgestellt.
- **Kein neuer Reject-Code**, kein Zuwachs an `ErrorCode`, keine Änderung an
  `structural_check`. Die Regel ist kein Reject (`01 §6`).
- **Kein `t`-Vergleich zwischen verschiedenen Autoren.** Die Regel ist strikt intra-Autor;
  ein Vergleich über Autorgrenzen wäre D78 direkt zuwider.
- **Keine Änderung an bestehenden Vektoren, Golden Anchors oder Erwartungswerten.**
- Kein Merge, kein Push nach `main`, kein Aufräumen fremder Baustellen.

## Abnahme

1. `make check` grün, 798 bestehende Tests weiterhin enthalten und weiterhin grün.
2. Die neuen Tests aus Abschnitt 6, einzeln benannt.
3. Die Rücknahmeprobe aus Abschnitt 7, für beide Pfade getrennt belegt.
4. `git diff --numstat` zeigt keine Markdown-Datei.
5. Der Diff in `vectors_01.json` enthält genau einen neuen Eintrag.

## Abschluss

Ein Commit auf `time-regression`. Melde zurück:

- den **vollständigen** `git diff` gegen den Branchpunkt, nicht `--numstat` und keine
  Zusammenfassung;
- die erzeugten Werte für NV32: `core`-Map in derselben Schreibweise wie die Nachbarn in
  Anhang C, `wire_bytes`, `claim_id`, `σ`, und auf welchen Vorgänger mit welchem `t` er kettet;
- das Ergebnis der beiden Rücknahmeproben, jeweils mit der Liste der rot gewordenen Tests;
- **jede Stelle, an der du diesem Prompt nicht folgen konntest oder ihn für widersprüchlich
  hältst.** Das ist kein Höflichkeitssatz. Rückfragen als Liste ans Ende, nicht unterwegs
  entscheiden: sie sind Kandidaten für Spec-Lücken und gehören ins Register, nicht in den Code.
