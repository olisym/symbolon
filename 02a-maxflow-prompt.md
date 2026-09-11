# Prompt `02a-maxflow` — Trust-Flow-Solver (MaR Layer 02)

Revision 2 — gegen den Spec-Stand nach dem Nachzug D28–D40. Tool-agnostisch, läuft in Cursor
oder Claude Code.

**Voraussetzung:** `spec/02-vouch-weight-and-sybil-fix` ist auf `main`, `impl/02-trust-flow` ist
von dort abgezweigt. Dieser Prompt zitiert `02-trust-flow.md` und `02-golden-anchors.md` in der
Fassung nach dem Nachzug; gegen den alten Stand ist er falsch.

---

## 0. Rolle und Regeln

Du implementierst Schicht 02 der Referenzimplementierung von *Mensch als Republik*.

- **Die Spec ist normativ.** Lies `02-trust-flow.md` und `02-golden-anchors.md` aus dem Repo,
  bevor du eine Zeile schreibst. Bei Widerspruch zwischen diesem Prompt und der Spec: **halte an
  und frage.** Nicht selbst entscheiden.
- **Layer 01 ist eingefroren.** Du änderst **nichts** in `atom.py`, `errors.py`, `cbor_canon.py`,
  `domains.py`, `predicates.py`, `verifier.py`. Keine neuen Member in `ErrorCode` — die
  Trust-Findings sind eine eigene Enum (§5). Keine Änderungen an bestehenden Tests; sie bleiben
  am Ende vollzählig grün.
- **Abhängigkeiten:** ausschließlich `cbor2` und `cryptography`. Kein `networkx`, kein `numpy`,
  kein `fractions`, kein `decimal`.
- **Keine Gleitkommazahlen.** Alle Kapazitäten, Gewichte, Flusswerte sind `int`.
- **`now` ist immer Parameter.** Kein `time`-Import, kein `datetime`, keine Systemuhr — nirgends,
  auch nicht in Tests.
- **Determinismus.** Zwei Läufe über denselben Store liefern byte-gleiche Ergebnisse, inklusive
  Schnittmenge und Findings. Iteriere nie über `set` oder `dict` in ergebnisrelevanter
  Reihenfolge, ohne vorher zu sortieren.
- Branch: `impl/02-trust-flow`. Commits klein und einzeln grün.

---

## 1. Modul-Layout

Neu anzulegen, alles unterhalb von `symbolon/trust/`:

```
trust/__init__.py      öffentliche Re-Exporte
trust/findings.py      TrustFinding, Finding
trust/params.py        TrustParams
trust/index.py         classify_all
trust/groups.py        Gruppenbildung (I, J, N) → n_budget, n_kante
trust/graph.py         Aktiv-Set, Budget-Set, BFS, Kapazitäten, Knoten-Split
trust/dinic.py         Max-Flow-Solver
trust/flow.py          öffentliche API: trust()
```

Tests unter `tests/trust/`, ein Modul je Ankergruppe (siehe §7).

---

## 2. Normative Definitionen

Aus der Spec übernommen. Wenn die Spec etwas anderes sagt, gilt die Spec.

### 2.1 Parameter

```python
@dataclass(frozen=True, slots=True)
class TrustParams:
    C0: int            # Seed-Budget, > 0
    gamma_num: int     # Zähler von γ,  0 < gamma_num < gamma_den
    gamma_den: int     # Nenner von γ
    D: int             # Nenner des Vouch-Gewichts, ≥ 1
```

### 2.2 Kapazität

```
C(d) = (C0 * gamma_num**d) // gamma_den**d          für endliches d
C(d) = 0                                            für d = ∞
```

**Einmal am Ende abrunden, nicht pro Schritt.** Bei `γ = 2/3`, `C₀ = 16`, `d = 2` ist das `7`,
nicht `6`.

Es gibt **keine** Kurzform. `(n * C(d)) // D` lässt sich nicht zu `(n * gamma_num**d) //
gamma_den**d` zusammenziehen — doppelte Rundung. Gegenbeispiel `C₀ = D = 16, γ = 2/3, d = 2,
n = 9`: korrekt `3`, Kurzform `4`.

### 2.3 Vouch-Gewicht (D37)

Der `v`-Payload eines `nuc:N/vouch@1`-Claims ist kanonisches CBOR:

```
v = { 0: n, ... }   n : uint,  1 ≤ n ≤ D
v abwesend (None)   ⇒  n = D   (w = 1, Default nach §3.1)
```

**Geprüft wird Key `0`, nicht die Map als Ganzes.** Weitere Keys sind zulässig und werden
ignoriert — `§2` liest dort einen Zweck-Tag, `§6.1` ein `bond_ref`, beides ist in diesem Schritt
nicht implementiert. `{0: 2, 1: 99}` ist ein gültiger Vouch mit `n = 2`.

| Fall | Kante | Budget-Beitrag | Finding |
|---|---|---|---|
| `v` nicht dekodierbar, keine Map, Key `0` fehlt, Wert kein uint | verworfen | **keiner** | `UNPARSABLE_VOUCH_PAYLOAD` |
| `n = 0` oder `n > D` | verworfen | **keiner** | `INVALID_VOUCH_WEIGHT` |

Kein Budget-Beitrag bei unlesbarem `n`, weil eine geratene Zahl eine **Falschbeschuldigung**
wegen Über-Commitment erzeugen könnte. D3: Teilwissen erzeugt Unter-Erkennung, nie
Falschbeschuldigung. Die Kante fällt weg, weil das Unter-Vertrauen ist. Beides ist die sichere
Richtung, in verschiedene Richtungen.

### 2.4 Aggregation je `(I, J, N)` — D40 ⚠️ neu

Mehrere Vouch-Claims derselben Identität auf dasselbe Subjekt im selben Scope bilden **eine**
Gruppe. Pro Gruppe zwei Zahlen:

```
n_budget = max(n über Gruppenmitglieder im Budget-Set)      0, wenn leer
n_kante  = max(n über Gruppenmitglieder im Aktiv-Set)       0 ⇒ keine Kante
```

**Maximum, nicht Summe.** Zwei Fehler, die das verhindert:

- Summenbildung machte die bloße **Erneuerung** eines Vouch zu einem `OVERCOMMITTED_AUTHOR` gegen
  den ehrlichen Autor — der Vorgänger bleibt nach D38 bis `t_exp` im Budget-Set.
- Parallelkanten trügen **doppelte Kapazität bei einfachem Budget**.

Weil Aktiv-Set ⊆ Budget-Set gilt, ist stets `n_kante ≤ n_budget`. Der Graph sieht nie parallele
Kanten: je Paar `(I, J)` genau eine.

### 2.5 Kantenkapazität

```
cap(I → J) = (n_kante * C(d(I))) // D
```

### 2.6 Zwei Mengen (§3.1, D38)

| Menge | Inhalt | Verwendung |
|---|---|---|
| **Aktiv-Set** | `classify(...).state == State.ACTIVE` **und** `p` ist `nuc:N/vouch@1` **und** `c.N == scope` | `n_kante`, Kantensatz |
| **Budget-Set** | wie oben, aber `state ∈ {ACTIVE, REVOKED, SUPERSEDED, PENDING, EQUIVOCATION_FLAGGED, TIME_REGRESSION_FLAGGED}` (D135, D356) | `n_budget`, Prüfung `Σ n_budget ≤ D` |

**Ein Vouch verlässt das Budget-Set ausschließlich durch `t_exp`** (`state == EXPIRED`). Weder
Widerruf noch Supersede geben Budget frei; eine Gruppe verlässt es erst, wenn **alle** ihre
Mitglieder abgelaufen sind. `MALFORMED` gehört in keine der beiden Mengen. Auch Equivocation gibt
kein Budget frei (D135) — sie ist kein Lebenszyklus-Akt und der Über-Commitment-Beweis beruht auf
Signaturen, nicht auf Aktivität.

**Die Aufzählung in der Tabelle ist die ausgerechnete Form dieses Satzes, nicht seine Definition.
Bei Abweichung gilt der Satz.** Die ursprüngliche Aufzählung ließ `EQUIVOCATION_FLAGGED` weg und
stand damit neun Zeilen über ihrer eigenen Widerlegung; der Code folgte der Aufzählung, und
Equivocation wurde zum Budget-Reset (D135).

Prüfe `state == State.ACTIVE` **explizit**; übernimm nicht `trust_usable`. Siehe Test T-02.4.

### 2.7 BFS mit Kapazitätsfilter (K8, D36)

`d(x)` ist die kürzeste Pfadlänge über dem **wirksamen** Kantenset
`E⁺ = { e ∈ Aktiv-Set : cap(e) ≥ 1 }`.

Kein Fixpunkt nötig: `cap(I→J)` hängt nur von `d(I)` ab, und `d(I)` steht fest, wenn die BFS `I`
expandiert. Ein Durchlauf, Schicht für Schicht:

1. Schicht 0 = Ankermenge, `d = 0`.
2. Ist Schicht `k` vollständig, steht `C(k)` und damit `cap` **aller** von dort ausgehenden
   Kanten fest.
3. Schicht `k+1` = alle noch nicht zugeordneten Knoten, die über eine Kante mit `cap ≥ 1`
   erreichbar sind.

Kanten mit `cap == 0` erzeugen `SUBGRANULAR_VOUCH` und nehmen weder an der BFS noch am Fluss
teil.

### 2.8 Knoten-Splitting und Super-Knoten ⚠️ geändert

- Jeder Knoten `x` wird zu `x_in → x_out` mit Kapazität `C(d(x))`.
- Vouch-Kante wird zu `I_out → J_in` mit `cap(I→J)`.
- **Super-Source** `S* → a_in` mit ∞ für jeden Anker `a` (K4) — **nicht `a_out`**. Die interne
  Kante des Ankers muss auf dem Pfad liegen, sonst gilt der Satz aus `§4` für einen
  über-committeten Anker nicht (Vektor A′ in T-02.1b: `48` statt `16`).
- **Super-Sink** `t_in → T*` mit ∞ für jedes Ziel `t` (K3).
- ∞ wird als `INF = sum(alle endlichen Kapazitäten) + 1` realisiert, nie als `float('inf')`.

Fehler `ValueError`, wenn `anchors ∩ targets ≠ ∅` — die Frage ist nicht wohldefiniert.

### 2.9 Über-Commitment (D4)

Für jede Identität `I` und den angefragten Scope: `Σ_J n_budget(I, J, scope)` über alle Gruppen.
`> D` ⇒ `OVERCOMMITTED_AUTHOR` für `I`. **Autor-Flag, kein Claim-Reject** — dieselbe Bauform wie
Equivocation: alle Claims bleiben gültig und gespeichert.

### 2.10 Auswertungsreihenfolge

Die Reihenfolge ist ergebnisrelevant und daher normativ:

1. `classify_all(store, now)`
2. Vouch-Claims des Scopes sammeln, `v` dekodieren → `n` oder Payload-Finding
3. Gruppen `(I, J, N)` bilden → `n_budget`, `n_kante`
4. Budget je Autor prüfen → `OVERCOMMITTED_AUTHOR`
5. Flags anwenden (`include_flagged`, §3) → Kantenkandidaten
6. BFS über `E⁺`, schichtweise → `d`, `C`, `cap`, `SUBGRANULAR_VOUCH`
7. Graph bauen (Split, `S*`, `T*`)
8. Dinic zweimal (§4)

Schritt 4 vor 5 vor 6: das Flag hängt **nur** am Budget-Set, nie an Kapazitäten oder Distanzen —
deshalb ist die Kette azyklisch, obwohl Schritt 5 den Graphen und damit die Distanzen ändert.

---

## 3. Öffentliche API

```python
def trust(
    store: ClaimStore,
    *,
    anchors: frozenset[bytes],
    targets: frozenset[bytes],
    scope: bytes,
    now: int,
    params: TrustParams,
    include_flagged: bool = False,
) -> TrustResult: ...


@dataclass(frozen=True, slots=True)
class TrustResult:
    value: int                     # Multi-Sink-Max-Flow, Kapazitätsbelegung §2.5
    disjoint_paths: int            # derselbe Graph, Einheitskapazitäten (§4)
    cut: tuple[bytes, ...]         # Identitäten der Schnittknoten, sortiert
    findings: tuple[Finding, ...]  # sortiert, dedupliziert
```

**Keine skalare Überladung.** Die Einzelabfrage ist `targets = frozenset({T})`. Wer über mehrere
Identitäten aggregieren will, übergibt sie gemeinsam — VR-02.1 wird so von der Signatur
erzwungen statt von der Disziplin des Aufrufers.

`include_flagged` (D39): Vouches von `EQUIVOCATION_FLAGGED`- oder `OVERCOMMITTED_AUTHOR`-Autoren
tragen bei `False` **keine Kante**. Das Budget-Set ist davon unberührt — Flags ändern nie die
Budgetrechnung. Achtung: bei `False` fällt in Variante A der gesamte Sybil-Zufluss weg, weil
CAROL geflaggt ist. Die Ankerwerte in `02-golden-anchors.md §3–§5` gelten deshalb bei
**`include_flagged=True`**; T-02.8 prüft den Default separat.

`cut` ist der **quellseitige** minimale Schnitt: die im Residualgraphen von `S*` erreichbaren
Knoten bestimmen ihn eindeutig. Gib die Identitäten zurück, deren **interne Kante** im Schnitt
liegt, sortiert nach Bytes. Besteht der Schnitt ausschließlich aus Vouch-Kanten, ist `cut` das
**leere Tupel** — das ist kein Fehler, sondern die Aussage „hier bindet keine Person, sondern
eine Beziehung". Variante B ist genau dieser Fall und wird so getestet.

### `classify_all`

```python
def classify_all(store: ClaimStore, now: int) -> dict[bytes, Classification]: ...
```

Ein Durchlauf: `structural_check` **einmal** pro Claim, dabei `revokes_by_target` und
`supersedes_by_target` als Index aufbauen, danach klassifizieren. `classify` aus Layer 01 ruft
`structural_check` pro Kandidat **innerhalb** der Suchschleife auf — über alle Vouches iteriert
wären das `O(E²)` Ed25519-Verifikationen.

`classify` bleibt die normative Wahrheit. `classify_all` ist nur schneller. Der Kopplungstest in
§7 stellt sicher, dass beide nie auseinanderlaufen.

---

## 4. Solver

Dinic. Einmal implementieren, zwei Kapazitätsbelegungen darauf:

| Lauf | interne Kanten | interne Kanten **der Anker** | Vouch-Kanten | liefert |
|---|---|---|---|---|
| Fluss | `C(d(x))` | `C₀` (wie alle) | `cap(I→J)` | `value`, `cut` |
| Disjunktheit (K5) | `1` | **`INF`** | `INF` | `disjoint_paths` |

Der Disjunktheitslauf ist **knoten**-disjunkt, nicht kantendisjunkt, und **spaltet die Endpunkte
nicht**: die interne Kante der Anker trägt `INF`. Knoten-Disjunktheit zählt *Zwischen*knoten —
mit gespaltenem Anker wäre die Zahl von einem einzelnen Anker aus trivial `1`. Vektor `TP-FAN`
(T-02.3) unterscheidet die beiden Belegungen.

Die beiden Läufe unterscheiden sich damit in **zwei** Punkten: Kapazitätsvektor *und*
Quellanbindung. Wer nur den Vektor tauscht, bekommt überall `1`.

Beide Läufe arbeiten auf demselben bereits gefilterten Graphen (§2.7) — deshalb ist der Filter
dort sicherheitsrelevant: mit `INF` auf allen Vouch-Kanten wäre eine Kante mit `cap == 0` sonst
von einer vollwertigen nicht mehr unterscheidbar.

Determinismus: Knotenindizes nach Identity-Bytes aufsteigend vergeben, Adjazenzlisten in
Einfügereihenfolge, Einfügereihenfolge aus der sortierten Kantenliste.

---

## 5. Findings

```python
class TrustFinding(str, Enum):
    OVERCOMMITTED_AUTHOR      = "OVERCOMMITTED_AUTHOR"       # Σ n_budget > D
    SUBGRANULAR_VOUCH         = "SUBGRANULAR_VOUCH"          # cap == 0
    INVALID_VOUCH_WEIGHT      = "INVALID_VOUCH_WEIGHT"       # n = 0 oder n > D
    UNPARSABLE_VOUCH_PAYLOAD  = "UNPARSABLE_VOUCH_PAYLOAD"   # Key 0 fehlt / kein uint


@dataclass(frozen=True, slots=True, order=True)
class Finding:
    kind: TrustFinding
    subject: bytes          # Identity bei OVERCOMMITTED_AUTHOR, sonst claim_id
```

`SUBGRANULAR_VOUCH` betrifft eine **Gruppe**, nicht einen Claim: als `subject` die `claim_id` des
Mitglieds mit `n == n_kante`; bei Gleichstand die lexikographisch kleinste. Damit ist das Finding
deterministisch, auch wenn mehrere Claims dasselbe `n` tragen.

Keine Exceptions für Findings. Nichts davon bricht einen Aufruf ab.

---

## 6. Ausdrücklich nicht in diesem Schritt

- **Zweck-Filter (`§2`, `v`-Key `1`).** Kodierung ist erst mit `03`/`05` festgelegt. Nicht
  erfinden, kein Parameter, kein Platzhalter — Key `1` wird gelesen und verworfen wie jeder
  andere Zusatz-Key.
- **`bond_ref` (`v`-Key `2`).** Dito, Layer 05.
- **PageRank (`§5`).** Kommt in `02b`.
- **Haftungsdurchgriff, Bond, Slashing.** Layer 05.
- **Caching.** Erst wenn ein Benchmark es verlangt.

---

## 7. Tests

Alle Zahlen wörtlich aus `02-golden-anchors.md`. Übernimm sie als Literale; **generiere keine
Erwartungswerte aus dem eigenen Code** — das würde die Kopplung an die Spec durch eine Kopplung
an sich selbst ersetzen.

Sofern nicht anders vermerkt, laufen alle Tests mit **`include_flagged=True`**. Der Default
`False` wird in T-02.8 geprüft.

### Profil `TP-02`

`γ = 1/2`, `C₀ = 16`, `D = 4`, `now = 1000`, `t_exp = 5000`.
Ladder `C(d) = 16, 8, 4, 2, 1, 0` für `d = 0..5`.
Graph: ALICE (Anker) → BOB → CAROL → `{g₁,g₂,g₃}`, EVE ohne eingehende Kante.
Rumpf: `ALICE→BOB` und `BOB→CAROL` je `n = 4`.

**Hinweis:** `TP-02` verletzt absichtlich die SHOULD-Empfehlung `D ≥ C₀` aus `§8`. Es ist der
Grenzfall, in dem `D` statt der Position rationiert. Nicht „korrigieren".

### T-02.1 — Anker 1–3, sieben Varianten

| Var | CAROL→S | in S | `→g₁` | `→g₂` | `→g₃` | Σ | simultan | Δ |
|---|---|---|---|---|---|---|---|---|
| A | 3 × `n=4` | — | 4 | 4 | 4 | 12 | **4** | 8 |
| B | 3 × `n=1` | — | 1 | 1 | 1 | 3 | **3** | 0 |
| C | 3 × `n=1` | je `n=2` | 3 | 3 | 3 | 9 | **3** | 6 |
| D | 3 × `n=1` | je `n=4` | 3 | 3 | 3 | 9 | **3** | 6 |
| E | 1 × `n=4` auf g₁ | je `n=2` | 4 | 1 | 1 | 6 | **4** | 2 |
| E₀ | 1 × `n=4` auf g₁ | — | 4 | 0 | 0 | 4 | **4** | 0 |
| **F** | `n=2,1,1` | je `n=2` | **4** | **3** | **3** | **10** | **4** | 6 |

A erzeugt `OVERCOMMITTED_AUTHOR` für CAROL (`Σ n_budget = 12`), D für jedes `gᵢ` (`Σ = 8`).
B, C, E, E₀, **F** erzeugen **kein** `OVERCOMMITTED_AUTHOR` — F ist mit `Σn = 4` exakt am Limit.
In E gilt `cap(g₂→g₃) == 0` ⇒ `SUBGRANULAR_VOUCH`.

`trust(ALICE → EVE) == 0` in jeder Variante.

Schnitte: `cut(A, simultan) == (CAROL,)`, `cut(F, simultan) == (CAROL,)`,
`cut(B, simultan) == ()` — in B bindet keine interne Kante, nur die drei Vouch-Kanten (§3).

**F ist der wichtigste neue Vektor.** Es ist budgetgültig und dominiert C und E in jeder Spalte.
Eine Implementierung, die F falsch rechnet, hat die Rundung oder die Rekursion durch `S` falsch.

### T-02.1b — Quellanbindung, Vektor A′

Eigener Graph: Rumpf `ALICE→BOB n=4`, zusätzlich `ALICE→g₁,g₂,g₃` je `n=4`.
`Σ n_budget(ALICE) = 16 > 4` ⇒ `OVERCOMMITTED_AUTHOR` für ALICE. `include_flagged=True`.

```
d(gᵢ) == 1,  C(gᵢ) == 8,  cap(ALICE→gᵢ) == 16
trust(ALICE → gᵢ)        == 16     (einzeln, je Ziel)
trust(ALICE → {g₁,g₂,g₃}) == 16    ← der Testpunkt
cut                       == (ALICE,)
```

Eine Implementierung mit `S* → a_out` liefert hier **48** und `cut == ()`. Das ist der einzige
Vektor, der die beiden Konventionen unterscheidet; bei jedem budgetgültigen Anker sind sie
identisch.

Zusätzlich: `trust(ALICE → {g₁,g₂,g₃}) == C(ALICE)` — der Satz aus `§4` gilt hier mit Gleichheit.

### T-02.2 — Budget-Fall

Basis C. `CAROL→g₁` erhält `t_exp = 2000` und einen Widerruf bei `t = 900`.

| Schritt | `now` | Aktiv | Budget | `Σ n_budget` | `→g₁` | `→g₂` | `→g₃` | simultan |
|---|---|---|---|---|---|---|---|---|
| S1 | 1000 | g₂, g₃ | g₁, g₂, g₃ | 3 | 2 | 2 | 2 | **2** |
| S2 | 2001 | g₂, g₃ | g₂, g₃ | 2 | 2 | 2 | 2 | **2** |

In S1 ist `d(g₁) = 4`, `C(g₁) = 1`, und `cap(g₁→gⱼ) = ⌊2·1/4⌋ = 0` ⇒ `SUBGRANULAR_VOUCH`.

Budgetprüfung bei `now = 1000` mit einem zusätzlichen `CAROL→DAVE`:
`n = 2` ⇒ `OVERCOMMITTED_AUTHOR` (`3+2 > 4`), obwohl nur zwei Kanten aktiv sind.
`n = 1` ⇒ kein Finding. Bei `now = 2001` ist `n = 2` zulässig.

**Supersede-Variante (D38):** Ersetze den Widerruf durch einen `core/supersede@1`. Erwartung
**identisch** — insbesondere bleibt `Σ n_budget = 3` in S1.

### T-02.2b — Gruppen-Aggregation, Variante G ⚠️ neu

Basis B (`S` isoliert), `CAROL→g₂ n=1` und `CAROL→g₃ n=1` fest. Auf `g₁` zwei Vouch-Claims
derselben Gruppe.

| Fall | `n(V1)` | Zustand V1 | `n(V2)` | `n_budget` | `n_kante` | `cap` | `Σ n_budget` | `→g₁/g₂/g₃` | simultan | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| Erneuerung | 2 | SUPERSEDED | 2 | 2 | 2 | 2 | **4** | 2 / 1 / 1 | 4 | **keins** |
| Herabstufung | 2 | SUPERSEDED | 1 | 2 | 1 | 1 | **4** | 1 / 1 / 1 | 3 | **keins** |
| Heraufstufung | 1 | SUPERSEDED | 3 | 3 | 3 | 3 | **5** | 3 / 1 / 1 | 4 | `OVERCOMMITTED_AUTHOR` |
| beide aktiv | 2 | ACTIVE | 3 | 3 | 3 | 3 | **4** | 3 / 1 / 1 | 4 | **keins** |

Der Erneuerungsfall trennt drei Implementierungen:

| Implementierung | Ergebnis | Diagnose |
|---|---|---|
| Summe über das Budget-Set | `2+2+1+1 = 6 > 4` | falscher `OVERCOMMITTED_AUTHOR` |
| Parallelkanten (Multigraph) | `cap = 4`, `→g₁ = 4` | doppelte Kapazität bei einfachem Budget |
| **korrekt (`max n`)** | `Σ = 4`, `cap = 2`, `→g₁ = 2` | — |

Die Zeile „beide aktiv" prüft dasselbe ohne Lifecycle-Akt: zwei gleichzeitig gültige Vouches auf
dasselbe Subjekt sind **eine** Kante mit `n = 3`, nicht zwei Kanten und nicht `Σn = 5`.

### T-02.3 — Disjunktheit

Graph C, Einheitskapazitäten, Anker intern `INF`:

```
disjoint_paths(ALICE → g₁)            == 1
disjoint_paths(ALICE → {g₁,g₂,g₃})    == 1
cut                                    == (BOB,)
```

Und mit 1000 zusätzlichen Sybils hinter CAROL weiterhin `1`.

**Vektor `TP-FAN`** (eigener Graph, `γ = 1/2`, `C₀ = 16`, `D = 4`):

```
ALICE → BOB  n=2      ALICE → BOB2 n=2      (Σn = 4)
BOB   → X    n=4      BOB2  → X    n=4      (je Σn = 4)

trust(ALICE → X)          == 16       cut == (ALICE,)
disjoint_paths(ALICE → X) == 2
```

Mit gespaltenem Anker im Disjunktheitslauf käme `1` heraus. In `TP-02` ist die Antwort wegen BOB
ohnehin `1` — ohne `TP-FAN` ist die Endpunkt-Regel **nicht getestet**.

### T-02.4 — Kopplung an Layer 01

```
∀ c ∈ store:  classify_all(store, now)[c.claim_id] == classify(c, store, now)
∀ c ∈ store:  c.trust_usable == (c.state == State.ACTIVE)
```

Beide über den vollständigen Layer-01-Vektorsatz. Schlägt der zweite fehl, **melde es und ändere
nichts** — dann stimmt eine Annahme nicht, und das will ich wissen, statt es stillschweigend zu
erben.

### T-02.5 — Invarianten

| ID | Aussage |
|---|---|
| INV-1 | `maxflow(mit Split) == maxflow(ohne Split)`, einzeln **und** simultan, für B, C, **D**, E, E₀, F. **Ungleich nur** für A (simultan `4` gegen `8`) und A′ (simultan `16` gegen `48`). Für die *Einzelabfrage* von A sind beide Läufe `4`. |
| INV-2 | `value` ist invariant gegen zusätzliche Sybils und gegen jede Topologie innerhalb `S`. C, D und C+1000 liefern alle `3`. |
| INV-3 | Monotonie: Entfernen einer beliebigen Kante senkt jeden Wert oder lässt ihn gleich, nie Anstieg. Erschöpfend über alle Teilgraphen von B. |
| INV-4 | `simultan ≤ Σ einzeln` in allen sieben Varianten. Gleichheit genau in B und E₀; A ist die reine Engpass-Ursache, E die reine Rekursions-Ursache. Beide brauchen einen Test. |
| INV-5 | Ein `OVERCOMMITTED_AUTHOR` in `S` (Variante D) ändert **keinen** Flusswert gegenüber C. |
| INV-6 | Aggregation ist idempotent: G-Erneuerung liefert dieselben Werte wie ein einfacher Graph mit `CAROL→g₁ n=2, →g₂ n=1, →g₃ n=1` (`S` isoliert): `2/1/1`, Σ `4`, simultan `4`. |
| INV-7 | Der Anker ist kein Sonderfall: `simultan(A′) == C(ALICE) == 16`. |

⚠️ INV-1 galt in Rev 1 als „ungleich für A und D". Das war falsch: Ds Über-Commitment sitzt in
`S`, wo nie mehr als `1` ankommt — mit und ohne Split `3`. Wenn dein Lauf hier `≠` liefert,
stimmt etwas anderes nicht.

### T-02.6 — Bootstrap, Profil `TP-BOOT`

`γ = 1/2`, `C₀ = 16`, `D = 24`, 3 Anker, 17 Neulinge.

| `m` | `n` | `cap` | `trust` | `disjoint_paths` |
|---|---|---|---|---|
| 1 | 4 | 2 | **2** | 1 |
| 2 | 2 | 1 | **2** | 2 |
| 3 | 1 | **0** | **0** | 0 |

Bei `m = 3` sind alle Kanten subgranular ⇒ 17 × `SUBGRANULAR_VOUCH`, alle Neulinge `d = ∞`,
`C = 0`.

Simultan über **alle 17** Neulinge bei `m = 2`: `value == 34`. Nominell stünden `f·C₀ = 48`
Einheiten bereit, real emittiert jeder Gründer nur `12` — die Rundung kostet ein Viertel, und
`34 ≤ 36` ist die tatsächliche Reserve. Kein Gründer überschreitet dabei `C₀`.

Zusätzlich als Eigenschaftstest: `θ ≤ f·C₀/M` ist erreichbar und `θ+1` nicht, für
`(f,M) ∈ {(3,17), (3,24), (1,8)}`.

### T-02.7 — Payload-Randfälle

`v = None` ⇒ `n = D`. `v = {0: 2, 1: 99}` ⇒ `n = 2`, **kein** Finding (Zusatz-Keys sind zulässig).
`v = {0: 0}` und `v = {0: D+1}` ⇒ `INVALID_VOUCH_WEIGHT`, keine Kante, kein Budget-Beitrag.
`v = h'ff'` und `v = {1: 4}` ⇒ `UNPARSABLE_VOUCH_PAYLOAD`, dito.

Ein Autor mit einem unlesbaren und zwei gültigen `n = 2`-Vouches auf **verschiedene** Subjekte:
`Σ n_budget = 4 ≤ D` ⇒ **kein** `OVERCOMMITTED_AUTHOR`. Das ist der Falschbeschuldigungs-Test.

### T-02.8 — `include_flagged` ⚠️ neu

Default ist `False`. Dann tragen Vouches geflaggter Autoren keine Kante:

| Variante | `include_flagged=True` | `include_flagged=False` | Grund |
|---|---|---|---|
| A | 4 / 4 / 4, simultan 4 | **0 / 0 / 0**, simultan 0 | CAROL geflaggt, gesamter Zufluss weg |
| D | 3 / 3 / 3, simultan 3 | **1 / 1 / 1**, simultan 3 | `gᵢ` geflaggt ⇒ Graph = B |
| C, F | unverändert | unverändert | keine Flags |
| A′ | 16, simultan 16 | **0**, simultan 0 | ALICE geflaggt, auch `ALICE→BOB` fällt weg |

Das Budget-Set bleibt in **allen** Zeilen identisch: `Σ n_budget` und die Findings ändern sich
nicht, wenn das Flag kippt. Nur der Kantensatz ändert sich. Ein Lauf mit `False`, der andere
Findings meldet als der mit `True`, hat die Reihenfolge aus §2.10 verletzt.

---

## 8. Abnahme

1. `pytest -q` grün, alle bestehenden Layer-01-Tests weiterhin enthalten.
2. Kein Import von `time`, `datetime`, `random`, `fractions`, `decimal`, `numpy`, `networkx`.
3. Kein `float` im gesamten neuen Code (`grep -n 'float\|\.0\b\|/ '` prüfen; nur `//` erlaubt).
4. Zwei Läufe liefern identische `TrustResult`, inklusive `cut` und `findings`.
5. Kein Diff in Layer-01-Dateien: `git diff --stat main -- symbolon/*.py` zeigt nur
   Neuzugänge unter `trust/`.

Melde am Ende: `git diff --stat`, die pytest-Ausgabe, die Liste neuer Dateien, und **jede Stelle,
an der du diesem Prompt nicht folgen konntest oder ihn für widersprüchlich hältst.** Der letzte
Punkt ist kein Höflichkeitssatz — jeder bisherige Widerspruch in diesem Projekt wurde beim
Implementieren gefunden, nicht beim Spezifizieren. Rückfragen bitte als Liste ans Ende, nicht im
Verlauf klären: sie sind Kandidaten für echte Spec-Lücken und sollen ins Register, nicht in den
Code.
