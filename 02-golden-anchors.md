# Golden Anchors — Layer 02 (Trust Flow)

Revision 3 · Status: gerechnet, gegengerechnet und gegen die Implementierung geprüft · gilt gegen
`02-trust-flow.md` nach Anwendung von `02-spec-nachzug.md` Rev 2

Zweck: normative Testvektoren für `02a-maxflow`. Alle Werte exakt, ganzzahlig, von Hand geprüft.

## Änderungen gegenüber Revision 1

| # | Was | Warum |
|---|---|---|
| 1 | **K4 auf `a_in`** statt `a_out`, neue Variante **A′** | `a_out` umgeht die interne Kante des Ankers ⇒ der `§4`-Satz ist für einen über-committeten Anker falsch (48 gegen 16) |
| 2 | **K5 um die Endpunkt-Regel ergänzt**, neuer Vektor `TP-FAN` | ohne sie wäre jede Disjunktheitszahl von einem einzelnen Anker aus trivial 1 |
| 3 | **K7 neu:** Aggregation je `(I, J, N)` über `max n`, neue Variante **G** | sonst ist die Erneuerung eines Vouch ein selbst-validierender Beweis gegen den eigenen Autor |
| 4 | **K8 neu:** BFS über `E⁺` — der Fork N5 aus Rev 1 ist entschieden | Fälschungssicherheit des Disjunktheitslaufs |
| 5 | Abschnitt „Angreifer-Optimum" **neu gerechnet**, Variante **F** ergänzt | die alte Aussage („Streuung 9 gegen Konzentration 4, Trade-off") ist falsch: F dominiert C und E in jeder Spalte |
| 6 | **INV-1 korrigiert** | die Erwartung „`≠` für A und D" war für D falsch und widersprach INV-5 |
| 8 | **K5: Vouch-Kanten `1`** (D42), **INV-2 als Schranke**, **INV-8 verengt** (D44), Anker 5b um „beide aktiv", Variante E mit vier subgranularen Kanten | Befunde der `02a`-Abnahme; drei davon Fehler in Rev-2-Zahlen |
| 7 | **`include_flagged`-Voraussetzung explizit** (§1), **INV-8 neu** | die Flusswerte setzen stillschweigend voraus, dass über-committete Autoren ihre Kanten tragen — mit dem Default `False` liefert A `0/0/0` |

---

## 0. Festgelegte Konventionen

Die Punkte K1–K8 waren in der Spec offen und sind hier entschieden. Sie gehören als
Spec-Nachzug in `02 §2`/`§3`/`§4`/`§8`, nicht nur in dieses Dokument. K9 gehört ausdrücklich
nicht in `02` (D375) und ist hier normativ (D398).

| ID | Frage | Entscheidung |
|---|---|---|
| K1 | Rundung von `C(x)` | `C(x) = ⌊C₀ · γ^d⌋`, einmal am Ende. Alle Kapazitäten `int`; kein `Fraction` im gesamten Solver. |
| K2 | Budgetprüfung | `Σw ≤ 1 ⇔ Σn ≤ D` (ganzzahlig, `D` **scope**-fest). Keine Rationalarithmetik. |
| K3 | Super-Sink (Multi-Sink) | `gᵢ_in → T*` mit ∞. Konsistent zur Einzelabfrage `maxflow(· → T_in)`. |
| K4 | Super-Source (Ankerset) | `S* → a_in` mit ∞ für jeden Anker `a`; `d(x) = min_a d(a,x)`. Die interne Kante des Ankers liegt auf dem Pfad — Voraussetzung des `§4`-Satzes. |
| K5 | Einheitskapazitäts-Lauf | **Knoten**-disjunkt (D19): interne Kanten `= 1`, **Vouch-Kanten `= 1`** (D42 — ∞ ist dort nicht wohldefiniert und degeneriert ohne Zwischenknoten), **Endpunkte ungespalten** (Anker intern `∞`; Ziel intern liegt wegen K3 nicht auf dem Pfad). |
| K6 | Out-Degree | `wirksame Out-Degree(I) ≤ min(D, C(I))`, gezählt in **Subjekten** (Gruppen im Budget-Set), nicht in Claims. |
| K7 | Mehrere Claims auf dasselbe Subjekt | Aggregation je `(I, J, N)`: `n_budget = max n` über das Budget-Set, `n_kante = max n` über das Aktiv-Set. **Maximum, nicht Summe.** |
| K8 | BFS-Kantenset | `E⁺ = { e ∈ Aktiv-Set : cap(e) ≥ 1 }`. Kanten ohne Durchsatz verleihen keine Position. |
| K9 | Ausgabeform des Schnitts | `cut` ist der **quellseitige** minimale Schnitt des Flusslaufs: die im Residualgraphen von `S*` erreichbaren Knoten bestimmen ihn eindeutig. Ausgegeben werden die Identitäten, deren interne Kante im Schnitt liegt (`x_in` erreichbar, `x_out` nicht), aufsteigend nach Bytes. Besteht der Schnitt nur aus Vouch-Kanten, ist `cut` leer — kein Fehler, sondern: hier bindet eine Beziehung, keine Person (`02 §4`). Referenzschnittstelle, nicht Layer-Semantik (D375). |

---

## 1. Testprofil `TP-02` (kanonisch)

```
γ  = 1/2      C₀ = 16      D = 4      Scope N = "test"
now = 1000    t_exp = 5000 (Default für alle Vouches, Ausnahmen markiert)
```

Kapazitätsleiter `C(d) = ⌊16 · 2^{-d}⌋`:

| `d` | 0 | 1 | 2 | 3 | 4 | ≥5 |
|---|---|---|---|---|---|---|
| `C` | 16 | 8 | 4 | 2 | 1 | **0** |

Kantenkapazität `cap(I→J) = ⌊n_kante · C(I) / D⌋`. Granularitätsboden: `cap = 0`, sobald
`n·C(I) < D`. Bei diesem Profil: `⌊1·2/4⌋ = 0` (Sybil bei `d=3`, minimales `n`),
`⌊2·1/4⌋ = 0` (`d=4`, `n=2`).

> ⚠️ **Alle Flusswerte in §3–§5 gelten bei `include_flagged = True`.** Über-committete Autoren
> (A: CAROL, D: `gᵢ`, A′: ALICE) tragen ihre Kanten. Mit dem Default `False` aus D39 fällt ihr
> Zufluss weg: A liefert dann `0/0/0` und simultan `0`, D fällt auf die Werte von B zurück
> (`1/1/1`, simultan `3`), A′ liefert `0`. Die Ankertabellen messen den **Mechanismus**, nicht
> die Policy; der Default wird separat geprüft (INV-8). Ohne diese Unterscheidung sind A, D und
> A′ mit den Vorgabewerten rot, ohne dass ein Rechenfehler vorläge.

### Knoten

| Identität | `d` | `C` | Rolle |
|---|---|---|---|
| ALICE | 0 | 16 | Seed (einziger Anker) |
| BOB | 1 | 8 | ehrlich |
| CAROL | 2 | 4 | ehrlicher **Grenzknoten** |
| g₁, g₂, g₃ | 3 / var. | 2 / var. | Sybil-Region `S` |
| EVE | ∞ | 0 | Neuling, unerreichbar |

### Fester Rumpf (alle Varianten außer A′)

| Claim | `n` | `w` | cap |
|---|---|---|---|
| ALICE → BOB | 4 | 1 | `⌊4·16/4⌋ = 16` |
| BOB → CAROL | 4 | 1 | `⌊4·8/4⌋ = 8` |

Interne Kanten: `ALICE 16`, `BOB 8`, `CAROL 4`, `gᵢ = C(gᵢ)`.
**Rumpf-Durchsatz in `CAROL_out`: `min(16, 16, 8, 8, 4) = 4`.** Die interne Kante von ALICE liegt
seit K4 auf dem Pfad, bindet hier aber nicht (`16 ≥ 16`); Variante A′ zeigt den Fall, in dem sie
bindet.

---

## 2. Varianten

| Var | CAROL → `S` | Kanten innerhalb `S` | Budget CAROL | Budget `gᵢ` |
|---|---|---|---|---|
| **A** | 3 × `n=4` | keine | `Σn = 12` ❌ | — |
| **B** | 3 × `n=1` | keine | `Σn = 3` ✅ | — |
| **C** | 3 × `n=1` | je `gᵢ → gⱼ`, `n=2` (6 Kanten) | `Σn = 3` ✅ | `Σn = 4` ✅ |
| **D** | 3 × `n=1` | je `gᵢ → gⱼ`, `n=4` (6 Kanten) | `Σn = 3` ✅ | `Σn = 8` ❌ |
| **E** | 1 × `n=4` auf g₁ | je `gᵢ → gⱼ`, `n=2` | `Σn = 4` ✅ | `Σn = 4` ✅ |
| **E₀** | 1 × `n=4` auf g₁ | keine | `Σn = 4` ✅ | — |
| **F** | `n=2, 1, 1` | je `gᵢ → gⱼ`, `n=2` | `Σn = 4` ✅ | `Σn = 4` ✅ |

Abgeleitete Kapazitäten:

| Var | `cap(CAROL→gᵢ)` | `d(g₁), d(g₂), d(g₃)` | `cap(gᵢ→gⱼ)` |
|---|---|---|---|
| A | `⌊4·4/4⌋ = 4` | 3, 3, 3 | — |
| B | `⌊1·4/4⌋ = 1` | 3, 3, 3 | — |
| C | 1 / 1 / 1 | 3, 3, 3 | `⌊2·2/4⌋ = 1` |
| D | 1 / 1 / 1 | 3, 3, 3 | `⌊4·2/4⌋ = 2` |
| E | 4 / — / — | 3, 4, 4 | `g₁→gⱼ: ⌊2·2/4⌋ = 1`; `g₂/g₃→·: ⌊2·1/4⌋ = 0` |
| E₀ | 4 / — / — | 3, ∞, ∞ (`C = 0`) | — |
| F | `⌊2·4/4⌋ = 2` / 1 / 1 | 3, 3, 3 | `⌊2·2/4⌋ = 1` |

---

## 3. Anker 1–3 — Einzelabfrage, Multi-Sink, VR-02.1-Differenz

`trust(ALICE→T) = maxflow(ALICE_in → T_in)` (K4) · Multi-Sink nach K3.

| Var | `trust→g₁` | `trust→g₂` | `trust→g₃` | **Σ einzeln** | **simultan** | **Δ (VR-02.1)** |
|---|---|---|---|---|---|---|
| **A** | 4 | 4 | 4 | **12** | **4** | **8** |
| **B** | 1 | 1 | 1 | **3** | **3** | **0** |
| **C** | 3 | 3 | 3 | **9** | **3** | **6** |
| **D** | 3 | 3 | 3 | **9** | **3** | **6** |
| **E** | 4 | 1 | 1 | **6** | **4** | **2** |
| **E₀** | 4 | 0 | 0 | **4** | **4** | **0** |
| **F** | 4 | 3 | 3 | **10** | **4** | **6** |

### Rechenwege

**A.** Einzeln: `min(Rumpf 4, cap 4) = 4`. Simultan: die interne Kante `CAROL_in→CAROL_out = 4`
schneidet; `3 × 4 = 12 > 4`. Δ = 8.

**B.** Einzeln: `min(4, 1) = 1`. Simultan: `1+1+1 = 3 ≤ Rumpf 4`. **Δ = 0** — bei isolierten
Blättern klafft nichts.

**C.** Einzeln nach `g₁_in`: direkt `1` + über `g₂`
(`CAROL_out→g₂_in 1 → g₂ intern 2 → g₂_out→g₁_in 1`) `1`
+ über `g₃` `1` = **3**. Begrenzt durch die Emission aus `CAROL_out` (3 Kanten à 1). Simultan:
Fluss verlässt `gᵢ_in` sofort nach `T*`, die `S`-internen Kanten tragen **nichts** → 3. Δ = 6.

**D.** Identisch zu C: der Engpass liegt an der ehrlichen Grenze, nicht in `S`. Das
Über-Commitment der Sybils untereinander kauft dem Angreifer **null**.

**E.** `g₁`: `min(4, 4) = 4`. `g₂`: `Rumpf 4 → g₁_in 4 → g₁ intern 2 → g₁_out→g₂_in 1` = **1**.
Kein zweiter Weg: `g₃_out→g₂_in` hat `cap ⌊2·1/4⌋ = 0` (Granularitätsboden, `C(g₃)=1`).
**Vier** der sechs `S`-internen Kanten sind subgranular: `d(g₂) = d(g₃) = 4`, `C = 1`, also sind
`g₂→g₁`, `g₂→g₃`, `g₃→g₁`, `g₃→g₂` null. Nur `g₁→g₂` und `g₁→g₃` tragen (`C(g₁) = 2`).
Simultan: alles, was `g₁_in` erreicht, geht direkt nach `T*` → 4.

**E₀.** `g₂, g₃` ohne eingehende Kante ⇒ `d = ∞`, `C = 0`, Fluss 0 (`§4` „Neuling ≈ 0").

**F.** `g₁`: direkt `2` + über `g₂` `1` + über `g₃` `1` = **4**; die interne Kante von CAROL wird
mit `2+1+1 = 4` exakt ausgeschöpft. `g₂`: direkt `1` + über `g₁` (`cap 2 → g₁ intern 2 →
g₁_out→g₂_in 1`) `1` + über `g₃` `1` = **3**. `g₃` symmetrisch. Simultan: Schnitt an den drei
Angriffskanten `2+1+1 = 4`, gleich der internen Kante von CAROL → **4**.

### Anker 3b — Quellanbindung (`a_in` gegen `a_out`), Variante A′

**A′:** Rumpf `ALICE→BOB n=4`, zusätzlich `ALICE→g₁,g₂,g₃` je `n=4` ⇒ `Σn = 16 > 4` ❌.
`cap(ALICE→gᵢ) = ⌊4·16/4⌋ = 16`, `d(gᵢ) = 1`, `C(gᵢ) = 8`.

| Quelle | `trust→gᵢ` einzeln | Σ | **simultan** | `Σ_{h ∈ Grenze} C(h)` | `§4`-Satz |
|---|---|---|---|---|---|
| `a_out` (verworfen) | 16 | 48 | **48** | 16 | **verletzt** |
| **`a_in` (K4, normativ)** | 16 | 48 | **16** | 16 | erfüllt, mit Gleichheit |

Dies ist der einzige Vektor, der die beiden Konventionen unterscheidet. Bei jedem
budgetgültigen Anker sind sie identisch, weil `Σ_e cap(e) ≤ C(a)` gilt — deshalb ändert K4
**keinen** anderen Ankerwert. Die Einzelabfrage ist in beiden Fassungen 16: dort bindet die
interne Kante des Ankers ohnehin, weil nur eine Kante genutzt wird.

*Test:* `simultan(A′) == 16` und `simultan(A′) == Σ_h C(h)`. Eine Implementierung, die 48 liefert,
hat die Quelle an `a_out` gehängt.

### Anker 3c — Schnitt (K9)

Simultane Abfrage `ALICE → {g₁,g₂,g₃}`, Flusslauf, `include_flagged = True`:

| Var | `cut` | bindend |
|---|---|---|
| **A** | `(CAROL,)` | interne Kante CAROL, `C = 4` |
| **B** | `()` | die drei Vouch-Kanten `CAROL→gᵢ`, je `cap = 1`; keine interne Kante |
| **F** | `(CAROL,)` | interne Kante CAROL, `C = 4`; die Vouch-Kanten tragen zusammen ebenfalls `4` |
| **A′** | `(ALICE,)` | interne Kante ALICE, `C = 16` |

B ist der Vektor für den leeren Schnitt: `Σ_{h ∈ Grenze} C(h) = 4`, und der Schnitt enthält
trotzdem keinen Knoten (`02 §4`). F ist der Vektor für die Eindeutigkeit: zwei minimale Schnitte
gleicher Kapazität, K9 wählt den quellseitigen, und dort ist CAROLs interne Kante die erste
gesättigte.

### Angreifer-Optimum (bei festem `|S| = 3`)

| Var | Budget | max. Einzelwert | Σ einzeln | simultan | Sybils mit `trust ≥ 2` |
|---|---|---|---|---|---|
| B | ✅ | 1 | 3 | 3 | 0 |
| C | ✅ | 3 | 9 | 3 | 3 |
| E | ✅ | 4 | 6 | 4 | 1 |
| **F** | ✅ | **4** | **10** | **4** | **3** |
| A | ❌ | 4 | 12 | 4 | 3 |

**F dominiert C und E in jeder Spalte.** Es gibt keinen Trade-off zwischen Streuung und
Konzentration, den ein Angreifer zu treffen hätte; die gemischte Belegung `n = 2,1,1` ist gegen
beide Verifiziererformen optimal.

**Was `Σw ≤ 1` tatsächlich kostet:** den **simultanen** Wert **nichts** — A liefert 4, das
budgetgültige F ebenfalls 4. Die Summe der Einzelabfragen fällt von 12 auf 10. Der Ertrag der
Budgetregel liegt **nicht** in der Unterdrückung, sondern darin, dass A mechanisch beweisbar und
slashbar ist (D4) und F nicht. Das ist konsistent mit L2 („detect-not-prevent") und muss in `§4`
ehrlich so stehen, damit kein Implementierer die Budgetregel für eine Sybil-Abwehr hält.

**Die Summe ist unbeschränkt.** Bei freiem `|S|` addiert jeder weitere erreichbare Sybil zur
Summe der Einzelabfragen; ein „Optimum" existiert dort nicht. Die Tabelle oben gilt ausschließlich
bei `|S| = 3` und vollvernetztem `S`. Genau deshalb trägt nur der simultane Lauf eine Schranke.

---

## 4. Anker 4 — `w`-Varianten (bereits in §3 enthalten)

Explizit die von `§8`/E-C geforderte Gegenüberstellung für CAROL bei festem Rumpf:

| CAROL-Strategie | `Σn` | Kanten | Einzelwerte | Σ | simultan |
|---|---|---|---|---|---|
| gleichverteilt, `S` vernetzt (C) | 3 | 3 × cap 1 | 3 / 3 / 3 | 9 | 3 |
| gemischt, `S` vernetzt (F) | 4 | cap 2 / 1 / 1 | 4 / 3 / 3 | 10 | 4 |
| konzentriert, `S` vernetzt (E) | 4 | 1 × cap 4 | 4 / 1 / 1 | 6 | 4 |
| gleichverteilt, `S` isoliert (B) | 3 | 3 × cap 1 | 1 / 1 / 1 | 3 | 3 |
| konzentriert, `S` isoliert (E₀) | 4 | 1 × cap 4 | 4 / 0 / 0 | 4 | 4 |

Der simultane Fluss hängt **nur** von der Summe der Angriffskanten-Caps ab (3 bzw. 4), nie von der
Topologie innerhalb `S`. Das ist die operative Bestätigung des Satzes in `§4` und ein
Invarianztest.

---

## 5. Anker 5 — Budget-Fall (Widerruf, zwei Uhren)

Basis: Variante C. Der Vouch `CAROL → g₁` erhält `t_exp = 2000` und wird bei `900` widerrufen.
Die übrigen CAROL-Vouches: `t_exp = 5000`. Alle Gruppen sind hier einelementig (K7 greift nicht).

| Schritt | `now` | Aktiv-Set (CAROL) | Budget-Set (CAROL) | `Σ n_budget` | frei |
|---|---|---|---|---|---|
| S1 | 1000 | g₂, g₃ | g₁, g₂, g₃ | 3 | 1 |
| S2 | 2001 | g₂, g₃ | g₂, g₃ | 2 | 2 |

**S1 — Flusswirkung.** `n_kante(CAROL, g₁) = 0` ⇒ keine Kante. `g₁` bleibt über `g₂_out→g₁_in`
und `g₃_out→g₁_in` erreichbar (`cap = ⌊2·2/4⌋ = 1`, also in `E⁺`) ⇒ `d(g₁) = 4`, `C(g₁) = 1`.

```
trust(ALICE → g₁) = 2       (1 über g₂, 1 über g₃; CAROL_out emittiert nur noch 2)
trust(ALICE → g₂) = 2       (direkt 1 + über g₃ 1; der Weg über g₁ liefert
                             cap(g₁→g₂) = ⌊2·1/4⌋ = 0)
trust(ALICE → g₃) = 2
Σ einzeln = 6 · simultan = 2 · Δ = 4
```

**S1 — Budgetwirkung (der eigentliche Testpunkt).** Bei `now = 1000` versucht CAROL einen neuen
Vouch auf DAVE:

| `n` | Prüfung über Budget-Set | Ergebnis |
|---|---|---|
| 2 | `3 + 2 = 5 > 4` | **`ERR_OVERCOMMIT`** — obwohl nur **zwei** Kanten aktiv sind |
| 1 | `3 + 1 = 4 ≤ 4` | zulässig, `cap = ⌊1·4/4⌋ = 1`, `d(DAVE) = 3` |

**S2 — Freigabe.** Bei `now = 2001` ist der widerrufene Vouch abgelaufen und verlässt das
Budget-Set. `CAROL → DAVE` mit `n = 2` ist jetzt zulässig.

Wer Aktiv- und Budget-Set zusammenlegt, produziert genau einen der beiden Fehler: bei
„Widerruf gibt frei" ist S1/`n=2` fälschlich erlaubt (Budget-Leck), bei „Widerruf lässt die
Kante stehen" ist `trust(→g₁)` in S1 fälschlich 3 (Phantomkante).

### Anker 5b — Gruppen-Aggregation (Variante G, entscheidet K7)

Basis: Variante B (`S` isoliert). `CAROL→g₂ n=1` und `CAROL→g₃ n=1` fest. Auf `g₁` zwei Claims
derselben Gruppe: **V1 supersediert, nicht abgelaufen**; **V2 aktiv**.

| Fall | `n(V1)` | `n(V2)` | `n_budget` | `n_kante` | `cap` | `Σ n_budget` CAROL | `trust` g₁/g₂/g₃ | simultan |
|---|---|---|---|---|---|---|---|---|
| **Erneuerung** | 2 | 2 | 2 | 2 | 2 | **4 ✅** | 2 / 1 / 1 | 4 |
| **Herabstufung** | 2 | 1 | 2 | 1 | 1 | **4 ✅** | 1 / 1 / 1 | 3 |
| **Heraufstufung** | 1 | 3 | 3 | 3 | 3 | **5 ❌** | `ERR_OVERCOMMIT` | — |
| **beide aktiv** | 2 (aktiv) | 2 | 2 | 2 | 2 | **4 ✅** | 2 / 1 / 1 | 4 |

Der Erneuerungsfall trennt drei Implementierungen:

| Implementierung | Ergebnis | Fehler |
|---|---|---|
| Summe über das Budget-Set | `2+2+1+1 = 6 > 4` | falscher `ERR_OVERCOMMIT` — die ehrliche Erneuerung wird als selbst-validierender Beweis gewertet (`05 §3` Stufe 3) |
| Multigraph (parallele Kanten) | `cap = 2+2 = 4`, `trust(→g₁) = 4` | doppelte Kapazität bei einfachem Budget |
| **K7 (`max n`)** | Budget 4, `cap = 2`, `trust(→g₁) = 2` | — |

Die Herabstufung ist der zweite Testpunkt: `n_kante` fällt sofort auf 1, `n_budget` bleibt bis
`t_exp` bei 2. **Fluss folgt dem Willen, Budget folgt der Uhr.**

Die Zeile **beide aktiv** prüft dasselbe ohne Lifecycle-Akt: zwei gleichzeitig gültige Vouches
auf dasselbe Subjekt sind **eine** Kante mit `n = 2`, nicht zwei Kanten und nicht `Σn = 4` aus
dieser Gruppe. Sie liefert dieselben Werte wie die Erneuerung — Duplikat und Supersede-Kette
werden identisch behandelt, und genau das ist INV-6.

---

### Anker 5c — Budget-Fall **ohne** `t_exp` (D364)

Basis: Variante C, wie Anker 5. Abweichend tragen der Rumpf und CAROLs übrige Vouches
`t_exp = 10**9` (markierte Ausnahme zu §1), damit allein der Widerruf und das fehlende `t_exp`
variieren. Der Vouch `CAROL → g₁` trägt **kein** `t_exp`; die Zeile ohne Widerruf wiederholt
denselben Aufbau ohne den Widerrufs-Claim.

Die Vergleichszeilen geben Anker 5 **in diesem** Aufbau wieder, nicht die in §5 gedruckten
Werte: dort stehen die Nachbarn beim Default `t_exp = 5000` und laufen bis `now = 10**6`
selbst ab, womit `Σ n_budget` dort auf 0 fällt. Verglichen wird nur die eine Mechanik.

| Lage | `now` | Aktiv-Set (CAROL) | Budget-Set (CAROL) | `Σ n_budget` | frei |
|---|---|---|---|---|---|
| Anker 5 **in diesem Aufbau** (`t_exp = 2000`, widerrufen bei 900) | 1000 | g₂, g₃ | g₁, g₂, g₃ | 3 | 1 |
| | 2001 | g₂, g₃ | g₂, g₃ | 2 | 2 |
| | 10**6 | g₂, g₃ | g₂, g₃ | 2 | 2 |
| **ohne `t_exp`, widerrufen bei 900** | 1000 | g₂, g₃ | g₁, g₂, g₃ | **3** | 1 |
| | 2001 | g₂, g₃ | g₁, g₂, g₃ | **3** | 1 |
| | 10**6 | g₂, g₃ | g₁, g₂, g₃ | **3** | 1 |
| **ohne `t_exp`, nicht widerrufen** | 1000 | g₁, g₂, g₃ | g₁, g₂, g₃ | **3** | 1 |
| | 2001 | g₁, g₂, g₃ | g₁, g₂, g₃ | **3** | 1 |
| | 10**6 | g₁, g₂, g₃ | g₁, g₂, g₃ | **3** | 1 |

**Ableitung.** `02 §3.1` kennt genau einen Austritt aus dem Budget-Set, und der hängt an
`t_exp`. Fehlt es, gibt es keinen — die Zeile ist in `now` konstant. D135 hält `REVOKED` im
Budget-Set, also ändert der Widerruf am Budget nichts; er senkt nur `n_kante` auf 0 und damit
das Aktiv-Set. Genau deshalb sind die beiden unteren Blöcke in ihrer Budgetspalte identisch und
unterscheiden sich allein im Aktiv-Set.

**Der Testpunkt.** Eine neue Bürgschaft `CAROL → DAVE` mit `n = 2` ergibt `3 + 2 = 5 > 4` und
damit `ERR_OVERCOMMIT` — bei Anker 5 nur bis `now = 2000`, hier **bei jedem `now`**. Anker 5
zeigt Selbstheilung durch Ablauf; 5c zeigt ihr Fehlen. Wer den Budget-Austritt an den Widerruf
statt an `t_exp` hängt, liefert hier fälschlich `Σ = 2` und übersieht D364.

**Warum dieser Anker gedruckt wird.** Vor ihm trug die gesamte Layer-02-Messfläche in jedem
Vektor ein `t_exp`; §1 setzt es als Default für alle Vouches. Eine Zweitimplementierung, die den
Austritt falsch bindet, liefe über alle übrigen Anker grün durch (D256 Beschluss 1, D367).

---

### Anker 5d — Intervall-`now` (Profil `TP-UHR`, D406)

Eigenes Profil, weil der Fall zwei disjunkte Pfade mit **verschieden datierten Abläufen**
braucht; in eine bestehende Variante gebogen wären beide Anker schwerer zu lesen. Parameter wie
`TP-02` (`C₀ = 16`, `γ = 1/2`, `D = 4`), `include_flagged = False` (§1).

**Bestand.** Scope `N_uhr`, alle `t = 100`:

| Vouch | `n` | `t_exp` |
|---|---|---|
| ALICE → BOB | 2 | 10000 |
| ALICE → CAROL | 2 | 10000 |
| BOB → DAVE | 3 | 10000 |
| BOB → ERIN | 3 | 600 |
| CAROL → DAVE | 4 | 600 |

Dazu **ein Vouch ALICE → ERIN mit `n = 1` und `t_exp = 650` in einem anderen Scope**. Er gehört
zum Anker und ist kein Beiwerk; was er trennt, steht unten.

Anker ALICE, Ziel DAVE.

**Rechenweg.** `C(ALICE) = 16`, `cap(ALICE→BOB) = ⌊2·16/4⌋ = 8`, ebenso nach CAROL; ALICEs Budget
im Scope ist `2 + 2 = 4 ≤ 4`. `d(BOB) = d(CAROL) = 1`, also `C = 8`. Daraus
`cap(BOB→DAVE) = ⌊3·8/4⌋ = 6` und `cap(CAROL→DAVE) = ⌊4·8/4⌋ = 8`. BOBs Budget ist `3 + 3 = 6 > 4`,
solange `BOB→ERIN` im Budget-Set liegt; CAROLs ist `4 ≤ 4`.

**Punktwerte.**

| `now` | Wert | Vermerke | Grund |
|---|---|---|---|
| 500 | 8 | `OVERCOMMITTED_AUTHOR` (BOB) | BOB überzeichnet, seine Kanten fallen; der Weg über CAROL trägt 8 |
| 600 | 8 | `OVERCOMMITTED_AUTHOR` (BOB) | Grenzfall: `now ≤ t_exp` schliesst 600 ein |
| 601 | 6 | — | `BOB→ERIN` abgelaufen, BOB frei; `CAROL→DAVE` abgelaufen, dieser Pfad tot |
| 700 | 6 | — | wie 601 |

`disjoint_paths = 1` an allen vier Punkten. Der Schnitt ist leer: die Engstelle ist eine
Vouch-Kante, und K9 benennt nur identitätsinterne Kanten.

**Fenster `[500, 700]`.** Bruchstellen sind `t_exp + 1` der **Scope**-Vouches mit
`500 ≤ t_exp < 700` (`02 §11.1`), also allein `601` — beide `t_exp = 600` fallen auf denselben
Punkt. Ausgewertet wird an `500` und `601`.

| Grösse | Erwartung |
|---|---|
| Wert (Minimum über die Punkte) | **6** |
| obere Schranke (Maximum) | **8** |
| Vermerke | **keine** |
| `disjoint_paths` | 1 |

Der Punktfall ist `lo = hi` und reproduziert die Tabelle darüber unverändert.

**Was dieser Anker trennt.** Drei Implementierungen fallen hier, und keine von ihnen an einem
anderen Anker:

- **Vermerke vereinigt statt vom Minimum-Punkt genommen.** Liefert `OVERCOMMITTED_AUTHOR`, obwohl
  der zurückgegebene Wert von `601` stammt, wo BOB nach seinen eigenen Zahlen nichts vorzuwerfen
  ist. Dasselbe gilt für `cut` und `disjoint_paths`: alle vier Grössen kommen aus **einem** Punkt.
- **Gemischte Auswertung** — Kanten gegen `hi`, Budget gegen `lo`. Liefert `0`: BOBs Pfad fällt
  über das Budget von `500`, CAROLs über die Kante von `700`. **Kein Punkt des Fensters trägt
  diesen Wert**, und genau darum ist die Mischung in `02 §11.1` ausgeschlossen.
- **Scope-Leck im Budget.** Zählt der Fremdscope-Vouch in ALICEs Budget, ist es `2 + 2 + 1 = 5 > 4`,
  ALICE wird geflaggt, und der Wert fällt auf `0` statt `6`. Zöge eine Implementierung die
  Bruchstellen aus dem ganzen Bestand statt aus den Scope-Vouches, käme `651` hinzu; die Zahlen
  blieben gleich, die Zahl der Auswertungen nicht — das trennt dieser Anker nicht, das Leck schon.

**Herkunft der Zahlen.** Die vier Punktwerte sind gegen die bestehende Implementierung gemessen
(`eb11f2a`, Punktform); die Fensterzahlen folgen daraus nach der Rechenregel in `02 §11.1` und
sind zum Zeitpunkt des Drucks von keiner Implementierung erzeugt worden.

---

## 6. Anker 6 — Einheitskapazitäten, Pfad-Disjunktheit (D19/D24)

Belegung nach K5: alle internen Kanten `= 1`, alle Vouch-Kanten **`= 1`** (D42), **Endpunkte
ungespalten** (ALICE intern `∞`; das Ziel endet an `T_in`). Quelle `S* → ALICE_in`, Senke
`T_in` bzw. `T*`.
Graph: Variante C.

| Abfrage | Wert | Min-Cut |
|---|---|---|
| knoten-disjunkte Pfade `ALICE → g₁` | **1** | `BOB_in→BOB_out` (auch `CAROL` schneidet) |
| knoten-disjunkte Pfade `ALICE → {g₁,g₂,g₃}` (simultan) | **1** | `BOB_in→BOB_out` |
| Quellenunabhängigkeit von `g₁` (Bürgen = {CAROL, g₂, g₃}) | **1** | `BOB_in→BOB_out` |
| Ersetzbarkeit von BOB | Fluss zur Peripherie fällt auf **0** | BOB ist Schnittknoten |
| Ersetzbarkeit von CAROL | Fluss zur Peripherie fällt auf **0** | CAROL ist Schnittknoten |

Kernvektor: **`|S| = 3`, aber Min-Cut `= 1`.** Eine Policy „drei unabhängige Attestierungen"
lehnt das gesamte Sybil-Trio ab, während die Einzelabfrage jedem der drei den Wert 3 zuweist.
Der Wert ist invariant gegen `|S|` — 1000 Sybils hinter CAROL ergeben ebenfalls 1.

### Gegenprobe 1 — zweiter Anker

Derselbe Lauf mit ALICE **und** einem zweiten Anker ALICE₂, der unabhängig auf CAROL bürgt:

| Ziel | Wert | Grund |
|---|---|---|
| `CAROL` | **2** | zwei Pfade, disjunkt in den Zwischenknoten (BOB bzw. keiner) |
| `g₁` | **1** | CAROL bleibt Schnittknoten — Unabhängigkeit *bis* CAROL hilft dahinter nicht |

Die zweite Zeile ist der eigentliche Vektor: ein zweiter Anker erhöht die Disjunktheit nur bis zum
gemeinsamen Schnittknoten. (Gehört in den `TP-BOOT`-Testsatz, nicht in `TP-02`.)

### Gegenprobe 2 — `TP-FAN` (entscheidet die Endpunkt-Regel aus K5)

```
ALICE → BOB  n=2      ALICE → BOB2 n=2      (Σn = 4 ✅)
BOB   → X    n=4      BOB2  → X    n=4      (je Σn = 4 ✅)
γ = ½, C₀ = 16, D = 4
```

| Lauf | Wert | Rechnung |
|---|---|---|
| Kapazität, `trust(ALICE→X)` | **16** | `cap(ALICE→BOBᵢ) = ⌊2·16/4⌋ = 8`, `C(BOBᵢ) = 8`, `cap(BOBᵢ→X) = ⌊4·8/4⌋ = 8` ⇒ `8+8`, gedeckelt durch `C(ALICE) = 16` |
| Einheiten, Disjunktheit `ALICE→X` | **2** | zwei knoten-disjunkte Pfade über BOB und BOB2 |
| Einheiten **ohne** Endpunkt-Regel | 1 | die interne Kante von ALICE trüge `1` und läge auf jedem Pfad |
| Einheiten mit **∞** auf Vouch-Kanten | Sentinel | kein Zwischenknoten ⇒ jede Kante des Pfades ist ∞ (D42) |

Ohne diesen Vektor ist die Endpunkt-Regel nicht getestet: in `TP-02` ist die Antwort wegen BOB
ohnehin 1, dort unterscheiden die beiden Belegungen nichts.

---

## 7. Anker 7 — Bootstrap (`TP-BOOT`)

`D = 4` ist für dieses Szenario **unbrauchbar**: nach K6 kann eine Identität dann höchstens
4 Personen bebürgen; drei Gründer erreichen maximal 12 Mitglieder. Eigenes Profil:

```
γ = 1/2   C₀ = 16   D = 24   f = 3 Gründer (Ankerset, alle d = 0)
M = 17 Neulinge → 20 Mitglieder   m = Bürgen pro Neuling   θ = Admission-Schwelle
```

### Geschlossene Wachstumsbedingung

Aus `Σ_e cap(I→e) ≤ C(I)` folgt für die Gesamtkapazität der Gründerrunde:

```
θ  ≤  f · C₀ / M          (Kapazitätsbedingung — unabhängig von D und m)
D  ≥  M · m / f           (Granularitätsbedingung — Out-Degree pro Gründer)
```

Bei `f = 3, C₀ = 16, M = 17`: **`θ ≤ 48/17 = 2.82` ⇒ `θ_max = 2`.**

Seit K4 ist die erste Bedingung tatsächlich eine Kapazitätsaussage: die interne Kante des Ankers
liegt auf dem Pfad, `f · C₀` ist ein echter Schnitt. Unter der verworfenen `a_out`-Konvention
folgte sie nur aus der Budgetregel.

### Erreichbarkeit nachgerechnet

| `m` | Kanten/Gründer | `n = ⌊D/e⌋` | `cap = ⌊n·C₀/D⌋` | `trust = m·cap` | Disjunktheit | `θ = 2`? |
|---|---|---|---|---|---|---|
| 1 | 6 | 4 | `⌊64/24⌋ = 2` | **2** | 1 | ✅ |
| 2 | 12 | 2 | `⌊32/24⌋ = 1` | **2** | 2 | ✅ |
| 3 | 17 | 1 | `⌊16/24⌋ = **0**` | **0** | — | ❌ |

`m = 2` liefert dieselbe Vertrauenshöhe wie `m = 1` bei **doppelter Pfad-Disjunktheit** — die
Rundung frisst genau den Unterschied. Redundanz ist hier gratis und sollte Policy-Default sein.
`m = 3` kollabiert am Granularitätsboden: **volle Redundanz ist bei diesem `C₀` nicht bezahlbar.**

**Die Rundung kostet ein Viertel.** Nominell stehen `f·C₀ = 48` Einheiten bereit; real emittiert
jeder Gründer nur `6·2 = 12` bzw. `12·1 = 12`, zusammen **36**. Der simultane Bedarf bei `θ = 2`
ist `2·17 = 34` — machbar, aber mit 6 % Reserve statt der nominellen 29 %. Wer nur die
Kapazitätsbedingung prüft, kalibriert zu optimistisch.

*Test:* simultaner Multi-Sink über alle 17 Neulinge = 34 bei `m = 2`.

### Ringwachstum und harte Reichweite

Verteilbare Kapazität eines Rings `k`: `M_k · C(k)`. Damit `M_{k+1} ≤ M_k · C(k) / θ`:

| Ring `k` | `d` | `C(k)` | max. `M_k` bei `θ = 2` |
|---|---|---|---|
| 0 | 0 | 16 | 3 (Gründer) |
| 1 | 1 | 8 | 24 |
| 2 | 2 | 4 | 96 |
| 3 | 3 | 2 | 192 |
| 4 | 4 | 1 | 192 |
| 5 | 5 | **0** | 96 |
| 6 | 6 | 0 | **0** |

**Harte Reichweite:** ab `d` mit `⌊C₀γ^d⌋ = 0` kann ein Mitglied **keinen** Vouch mehr tragen,
gleich wie viel Budget es einsetzt und gleich wie viele Bürgen ein Kandidat sammelt. Bei
`C₀ = 16, γ = ½` ist das `d = 5`: `r_max = ⌊log_{1/γ} C₀⌋ = 4` für die Bürgschaftsfähigkeit, `5`
für die Mitgliedschaft. Der Nukleus sättigt bei rund **600 Mitgliedern** und einem Radius von 5 —
nach oben durch `C₀` und `γ` gedeckelt, nicht durch die Budgetregel.

Das ist kein Defekt, sondern die quantitative Fassung von „maximal lokal" — gehört als Zahl in
`§8`, weil ein Nukleus, der 5000 Mitglieder will, `C₀` oder `γ` ändern **muss** und das vorher
wissen soll.

---

## 8. Abgeleitete Invarianten (als Tests zu implementieren)

**INV-1 — Der Knoten-Split ist bei gültigem Budget redundant.**
`Σ_e ⌊n_e·C(I)/D⌋ ≤ (Σn_e)·C(I)/D ≤ C(I)`. Sind alle Knoten budgetgültig, ist die interne Kante
nie **allein** bindend.
*Test:* `maxflow(mit Split) == maxflow(ohne Split)`, einzeln **und** simultan, für
B, C, **D**, E, E₀, F — und `≠` nur für **A** (simultan `4` gegen `8`; der Engpass ohne Split ist
die Kante `BOB→CAROL`) und **A′** (simultan `16` gegen `48`).
⚠️ **Nicht** für D: dessen Über-Commitment sitzt in `S`, wo nie mehr als 1 ankommt — mit und ohne
Split 3. Rev 1 erwartete hier `≠` und widersprach damit INV-5. Und **nicht** für die
Einzelabfrage von A: dort sind beide Läufe 4.

**INV-2 — `|S|`-Unabhängigkeit ist eine Schranke, keine Gleichheit.** Der simultane Fluss in die
Sybil-Region ist durch `Σ_{h ∈ Grenze} C(h)` beschränkt, **unabhängig von `|S|`** — er wächst
nicht mit der Zahl der Sybils. Bei `TP-02` ist diese Schranke `C(CAROL) = 4`.
*Test:* C mit Zielmenge `{g₁,g₂,g₃}` liefert `3`; C plus 1000 weitere Sybils **hinter CAROL**,
alle 1003 in der Zielmenge, liefert `4` und damit weiterhin `≤ 4`. Der Wert steigt, die Schranke
hält. D liefert `3` wie C — die Topologie innerhalb `S` ist ohne Wirkung.
⚠️ Die frühere Fassung („C+1000 liefert `3`") war falsch: sie galt nur, solange die Zielmenge bei
drei blieb, und dann ändern zusätzliche Sybils trivialerweise nichts. `§4` sagt `≤`, nicht `=`.
Nebenwirkung: CAROL kann bei `D = 4` höchstens vier Subjekte bebürgen, 1003 sind notwendig
über-committet — der Vektor prüft damit zugleich, dass die Schranke gegen einen über-committeten
Grenzknoten hält.

**INV-3 — Monotonie (§7).** Entfernen einer beliebigen Kante senkt jeden `trust`-Wert oder lässt
ihn gleich. Nie Anstieg.
*Test:* alle `2^|E|` Teilgraphen von B (klein genug für Erschöpfung).

**INV-4 — Multi-Sink ≤ Σ einzeln.** Gilt in allen Varianten. Zwei unabhängige Divergenzursachen,
jede allein hinreichend: (i) gemeinsamer Engpass stromaufwärts — **A**, (ii) eine Einzelabfrage
benutzt Knoten aus `S` als Zwischenknoten, die der simultane Lauf an `gᵢ_in` absorbiert — **E**.
Greift keine, gilt Gleichheit — **B, E₀**. Beide Ursachen brauchen einen Vektor; wer nur einen
testet, hat VR-02.1 halb getestet.

**INV-5 — Über-Commitment ist knotenlokal.** Die Prüfung `Σ n_budget ≤ D` ist pro
`(Identität, Scope)` und unabhängig vom Fluss. D zeigt: ein über-committeter Knoten in `S` ändert
**keinen** Flusswert — Erkennung und Bewertung sind entkoppelt.

**INV-6 — Aggregation ist idempotent.** Ein weiterer Vouch von `I` auf `J` mit `n' ≤ n_budget`
ändert weder Budget noch Kapazität.
*Test:* G-Erneuerung liefert dieselben Werte wie ein einfacher Graph mit
`CAROL→g₁ n=2, →g₂ n=1, →g₃ n=1` (`S` isoliert): `2 / 1 / 1`, Σ 4, simultan 4.

**INV-7 — Der Anker ist kein Sonderfall.** Der `§4`-Satz `maxflow(s→S) ≤ Σ_h C(h)` gilt auch,
wenn der Anker selbst Grenzknoten ist.
*Test:* A′ simultan `== 16 == C(ALICE)`.

**INV-8 — Das Flag ändert den Kantensatz, nicht die Budgetrechnung.** `Σ n_budget` und die
**Budget- und Payload-Befunde** sind identisch, ob `include_flagged` `True` oder `False` ist —
sie entstehen vor der Flag-Anwendung. Der **Subgranularitätsbefund** entsteht danach und ist
flag-abhängig: fällt die Kante eines geflaggten Autors weg, verschlechtern sich stromabwärts die
Distanzen, sinken die Kapazitäten, und Kanten rutschen unter die Granularitätsgrenze (D44). Das
ist konstruktiv so und kein Defekt.
*Test:* je Variante beide Läufe; Budget- und Payload-Befunde byte-gleich, Flusswerte nach der
Tabelle in §1 (A: `4/4/4` gegen `0/0/0`, D: `3/3/3` gegen `1/1/1`, C und F unverändert).

---

## 9. Effizienzhinweise für `02a`

1. **Ein Multi-Sink-Lauf statt `|S|` Einzelläufen.** VR-02.1 ist nicht nur korrekter, sondern
   billiger: eine Dinic-Ausführung gegen `|S|`.
2. **Distanz und Kapazität in einem BFS-Durchlauf.** `cap(I→J)` hängt nur von `d(I)` ab, und
   `d(I)` steht fest, wenn die BFS `I` expandiert. Kein zweiter Durchlauf, kein Fixpunkt. Die
   Filterung nach `E⁺` (K8) geschieht im selben Durchlauf.
3. **Aggregation vor dem Graphbau.** K7 ist ein `dict[(I,J,N)] → (n_budget, n_kante)`, gefüllt in
   einem Lauf über die Claims. Danach existiert je Paar genau eine Kante — der Solver sieht nie
   parallele Kanten.
4. **Keine Rationalarithmetik.** K1 + K2 ⇒ `int` überall. Kein `Fraction`, kein `decimal`.
   Budgetprüfung ist eine Integer-Summe pro Knoten, `O(|E|)`.
5. **Cache-Schlüssel.** Der abgeleitete Graph ist zwischen zwei aufeinanderfolgenden `t_exp`
   konstant. Schlüssel `(Ankerset, Scope, Claim-Epoche, ⌊now⌋ auf das nächste t_exp)` —
   `now` bleibt Parameter, das Caching wird trotzdem exakt.
6. **Einheitskapazitäts-Lauf teilt den Graphen.** Gleiche Topologie, andere Belegung — aber
   **zwei** Unterschiede: Kapazitätsvektor *und* Quellanbindung (Anker intern `∞` statt `C(a)`).
   Wer nur den Vektor tauscht, bekommt überall 1.
7. **Dinic auf Einheitskapazitäten** läuft in `O(E√V)`; der allgemeine Fall in `O(V²E)`. Bei
   diesen Graphgrößen irrelevant, aber die Belegung sollte den Solver nicht zwingen, generisch
   zu bleiben.

---

## 10. Forkstand

**Erledigt seit Rev 1:**

- **N5 (BFS kapazitätsblind)** — entschieden: filtern, `E⁺ = {cap ≥ 1}` (K8, D36). Auf `TP-02`
  ändert das keinen Ankerwert, auf `TP-BOOT` `m = 3` schon.
- **Quellanbindung** — entschieden: `a_in` (K4, D31), belegt durch A′.
- **Endpunkt-Regel im Einheitslauf** — entschieden (K5, D32), belegt durch `TP-FAN`.
- **Mehrere Claims je Subjekt** — entschieden: `max n` (K7, D40), belegt durch G.

**Offen, nicht blockierend für `02a`:**

- Ist `Σ n_budget > D` im Sinne von `05 §4` terminal oder kurierbar? (Policy)
- Kodierung der `v`-Keys `1` (Zweck-Tag) und `2` (`bond_ref`) — gehört zu `03`/`05`, trägt bis
  dahin keinen Testvektor.
