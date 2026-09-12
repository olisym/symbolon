# Trust-Flow-Schicht — Spezifikation v1

Status: Entwurf · Protokollversion: 1 · Layer: Trust / Reputation (über Identity/Claim)

Diese Schicht verwandelt den Graphen aus **aktiven** Bürgschafts-Claims (Atom-Spec §7.1,
Aktiv-Set nach Atom-Spec §6) in einen *personalisierten, Sybil-resistenten* Vertrauenswert.
Sie führt **kein** neues Claim-Feld ein — sie ist reine Auswertung über dem Atom.

---

## 1. Leitsätze (Geltungsrahmen)

- **Fluss ist Fundament, PageRank ist Näherung.** Jede *harte* Entscheidung läuft über
  Max-Flow / Min-Cut (beweisbare Schranke). PageRank ist die erlaubte kapazitätsvergessende
  Relaxation für *billiges* Massen-Ranking. Ein Graph, zwei Sichten (§4, §5).
- **Geldblinde Kapazität.** Basis-Kapazität ist rein strukturell (Distanz-Decay). Ein Bond
  hebt Kapazität **niemals** an — seine einzige Protokollwirkung ist Slashbarkeit (§6.1).
  Geld kann Vertrauen *verpfänden*, nie *kaufen*.
- **Geschichtete Seeds, kein globaler.** Der individuelle Seed ist Grundwahrheit (immer
  lokal, unentziehbar). Der Nukleus-Seed ist eine optionale geteilte *Linse*, nie ein
  objektiver Score (§6.3).
- **Per-Verifizierer, per-Sicht, nie global.** Jeder rechnet von *seinem* Seed über *seinen
  aktuell bekannten* Teilgraphen. Es muss kein globaler Graph existieren. Die Lokalität der
  Metrik *erzeugt* die Partitionstoleranz (§7).
- **Vertrauen ist Zustand, kein Vermögen.** `C(x)` ist rein *positional* — durch Wohlverhalten
  lässt sich kein höheres `C` erarbeiten, und ein erfolgreicher Vouch erhöht die Kapazität des
  Bürgen **nicht**. `t_s` ist ein Zustand des aktuell bekannten Kantensets, kein Integral über
  die Vergangenheit: widerrufen die Bürgen, fällt der Wert sofort. Nicht akkumulierbar, nicht
  hortbar, nicht übertragbar. Damit existiert kein Guthaben, das als Puffer gegen Sanktionen
  dienen könnte.

---

## 2. Graphmodell

Für eine Anfrage `(Scope N, Zweck π)`:

- **Knoten** `V` = Identitäten (Ed25519-Verify-Keys).
- **Kanten** `E` = gerichtete Kante `I → J` für jeden **aktiven** `nuc:N/vouch@1`-Claim
  mit Autor `I`, Subjekt `J`. „Aktiv" heißt: strukturell gültig, nicht abgelaufen, nicht
  widerrufen, nicht supersediert (Atom-Spec §6). Ein **partial-sync**-Vouch, dessen Vorgänger
  noch fehlt, ist erst `pending` (Atom-Spec §6) und trägt **noch keine** Kante bei — er wird
  aufgenommen, sobald er `active` wird. Das ist dieselbe sichere Richtung wie §7: fehlendes
  Wissen senkt nur, es erfindet keine Kante.
- **Eine Kante je `(I, J)`.** Mehrere Vouches derselben Identität auf dasselbe Subjekt im
  selben Scope erzeugen **eine** Kante mit `n_kante = max n` über die aktiven
  Gruppenmitglieder (§3.1) — keine parallelen Kanten, keine addierten Kapazitäten. Eine
  Beziehung ist eine Kante. Trägt kein Gruppenmitglied eine gültige Belegung nach §3.1,
  entsteht **keine** Kante, auch wenn der Claim nach Atom-Spec §6 `active` ist.
- **Scope-Partition.** Es gibt einen Graphen *pro* `N`. Vertrauen aus Scope A fließt nicht
  nach Scope B (Kontextbindung).
- **Zweck-Filter.** Trägt der Vouch in `v` einen Zweck-Tag, werden für Zweck `π` nur passende
  (oder per Policy untypisierte) Kanten einbezogen. Gleiche Metrik, gefilterter Graph —
  ein Filter, kein neuer Mechanismus.
- **Torwächter-Zwecke getrennt führen (Policy-Default).** `t_s` trägt zwei verschiedene Dinge:
  *Gehört-werden* (epistemische Autorität, nicht-rival — dass viele einem guten Denker zuhören,
  nimmt niemandem etwas weg) und *Torwächterschaft* (Aufnahme, Zugang, Bürgschaft — rival und
  zwingend). Nur die zweite Sorte ist ein lohnendes Unterwanderungsziel. Die Referenz-Policy
  führt Torwächter-Zwecke daher in eigenen Scopes; das Budget aus §3.1 bindet dann nur die
  Torwächterschaft, nicht das Zuhören. Ein Nukleus darf beides zusammenlegen — er macht sich
  damit angreifbar.

---

## 3. Kapazitätsmodell (Distanz-Decay)

Die Kapazität bestimmt, wie viel Vertrauen *durch* einen Knoten fließen kann. Sie klingt
mit der Distanz vom Seed ab — und genau das erzeugt die Sybil-Schranke und die
„Neuling ≈ 0"-Eigenschaft **strukturell, ohne Sonderregel**.

- **Distanz** `d(s, x)` = kürzeste Pfadlänge in Hops von Seed `s` zu `x` über dem
  **wirksamen** Kantenset `E⁺ = { e ∈ E : cap(e) ≥ 1 }` (BFS). Unerreichbar ⇒ `d = ∞`. Wer
  keine Kapazitätseinheit weiterreicht, reicht auch keine Position weiter. Die Definition ist
  wohlfundiert: `cap(I→J)` hängt nur von `d(I)` ab, das feststeht, wenn die BFS `I`
  expandiert — ein Durchlauf, kein Fixpunkt.
- **Knotenbudget** `C(x) = ⌊ C₀ · γ^{d(s,x)} ⌋`, mit `γ = γ_num/γ_den ∈ (0,1)` und
  Seed-Budget `C₀ > 0` bei `d = 0`. **Einmal am Ende abgerundet, nicht pro Schritt** —
  iteratives Runden machte das Ergebnis von der Auswertungsreihenfolge abhängig. Es gilt
  `C(x) = 0` für unerreichbare `x` und für alle `d` mit `C₀·γ^d < 1`.
- **Knoten-Splitting (Advogato-Konstruktion).** Jeder Knoten `x` wird in `x_in → x_out`
  gespalten, mit interner Kantenkapazität `C(x)`. Jede Vouch-Kante `I → J` wird zu
  `I_out → J_in` mit Kapazität **`⌊ n_kante · C(I) / D ⌋`** (§3.1).
- **Ankerset statt einzelnem Seed.** Ist der Seed eine Menge (§6.3), gilt
  `d(x) = min_a d(a,x)`, und die Quelle im Flussgraphen ist ein Super-Source `S*` mit
  ∞-Kanten auf jedes `a_in`. Die interne Kante des Ankers liegt damit auf dem Pfad: sein
  Budget `C(a)` bindet auch auf der Quellseite. Bei gültigem Budget ist das identisch zur
  Anbindung an `a_out` (`Σ_e cap(e) ≤ C(a)`); es unterscheidet sich genau bei
  über-committetem Anker, und dort in Richtung Unter-Vertrauen.

> **Warum Knoten- und nicht Kantenkapazität (bewusste Wahl).** Nur die Kapazität *am Knoten*
> macht die Schranke unabhängig von der Zahl der Sybils: der Engpass ist die endliche
> Kapazität der **ehrlichen Grenzknoten**, nicht die Zahl der Kanten oder Knoten dahinter.
> Das ist das tragende Element des Bounds in §4. Die Kantenkapazitäten aus §3.1 kommen
> additiv hinzu: sie können den Fluss nur weiter **senken** und berühren die
> `|S|`-Unabhängigkeit nicht.
>
> **Nachtrag seit D1.** Gilt die Budgetregel, ist `Σ_e ⌊n_e·C(I)/D⌋ ≤ (Σn_e)·C(I)/D ≤ C(I)`
> — die interne Knotenkante ist dann nie **allein** bindend (Gleichheit ist möglich,
> striktes Überschreiten nicht), und die Schranke wird gleichermaßen von den Kanten-Caps
> getragen. Sie bindet ausschließlich bei über-committeten Knoten, und auch dort nur, wenn
> tatsächlich mehr Fluss ankommt als `C(I)`. Das entwertet die Konstruktion nicht: sie ist
> weiterhin nötig, um Über-Commitment überhaupt sichtbar zu machen, und der
> Einheitskapazitäts-Lauf (§8) lebt vollständig auf ihr.

### 3.1 Vouch-Gewicht `w` und Selbstbindungsbudget

Ein Vouch deklariert in `v`, wie viel Vertrauen er weiterreicht.

- **Gewicht.** `w = n / D` mit `n ∈ [1, D]`; `D` ist Policy des Scopes (§8), Default `n = D`
  (also `w = 1`). Untypisierte Vouches gelten als `w = 1`.
- **Kantenkapazität.** `I_out → J_in` erhält `⌊ n_kante · C(I) / D ⌋`. Abrunden ist die
  sichere Richtung (Unter-Vertrauen) und erhält die exakte Integer-Arithmetik der harten
  Sicht.
- **Selbstbindungsbudget.** Für jede Identität `I` und jeden Scope `N` gilt `Σ wᵢ ≤ 1`,
  gleichbedeutend `Σ_J n_budget ≤ D`, über alle Gruppen `(I, J, N)` im Budget-Set.

> **Nicht abgelaufen ist ein Prädikat, kein Zustand.** Die Zugehörigkeit zum Budget-Set
> prüft `t_exp` gegen `now` (`now ≤ t_exp`, fehlendes `t_exp` bindet unbegrenzt) —
> **unabhängig** vom Lebenszyklus-Zustand. Wer sie an einen Zustand „abgelaufen" knüpft,
> erzeugt einen Deadlock: ein widerrufener Claim erreicht diesen Zustand nie, weil der
> Widerruf vorrangig ist, und bände sein Budget für immer (D41).

> **Aggregation je `(I, J, N)`.** Mehrere Vouches derselben Identität auf dasselbe Subjekt im
> selben Scope bilden **eine** Gruppe. Es zählen `n_budget = max n` über die
> Gruppenmitglieder im Budget-Set und `n_kante = max n` über die im Aktiv-Set; die Kante
> trägt `cap(I→J) = ⌊n_kante·C(I)/D⌋`, das Budget prüft `Σ_J n_budget ≤ D`. Weil
> Aktiv-Set ⊆ Budget-Set gilt, ist stets `n_kante ≤ n_budget`. **Maximum, nicht Summe** —
> sonst wäre die bloße Erneuerung eines Vouch ein selbst-validierender Beweis gegen den
> eigenen Autor (§6.2), und zwei aktive Vouches auf dasselbe Subjekt trügen doppelte
> Kapazität bei einfachem Budget.

> **Welches Gruppenmitglied die Kante benennt.** `kante_claim_id` — der Träger von
> `SUBGRANULAR_VOUCH` — ist die kleinste `claim_id` unter den Gruppenmitgliedern mit
> `n = n_kante`, nach der Benennungsregel aus Atom-Spec §4.1. Die Vertauschungsprobe hält:
> `cap`, das Budget, die BFS-Distanzen und der Fluss lesen `kante_claim_id` nicht. Trägt die
> Gruppe keine Kante, gibt es keinen Träger.

> **Out-Degree folgt aus dem Budget.** Aus `n ≥ 1` und `Σn ≤ D` folgt: höchstens `D`
> gleichzeitig bebürgte **Subjekte** pro Identität und Scope — gezählt werden Gruppen im
> Budget-Set, nicht Claims. Aus `cap ≥ 1 ⟺ n·C(I) ≥ D` folgt schärfer
> `wirksame Out-Degree(I) ≤ min(D, C(I))`. Bei `D ≥ C₀` (§8) bindet stets `C(I)`: **die Zahl
> der Menschen, für die man bürgen kann, ist die eigene Position** — keine gezählte
> Rationierung, sondern dieselbe positionale Größe wie alles andere in dieser Schicht.

> **Obergrenze, kein Anteil (bewusste Wahl).** Der Cap einer Kante hängt **nur von dieser
> Kante** ab — es gibt keine Normalisierung über `Σw`. Andernfalls wäre bei Teilwissen das
> beobachtete `Σw` zu klein, jeder bekannte Anteil zu groß, und **fehlendes Wissen erhöhte das
> errechnete Vertrauen** — ein Bruch der Monotonie aus §7. Der Defekt läge in der Kopplung, nicht
> in der Formel; keine Normalisierungsregel repariert ihn.

**Zwei Mengen, nicht eine.** Aktiv-Set und Budget-Set sind verschieden:

| Menge | Inhalt | Verwendung |
|---|---|---|
| **Aktiv-Set** | nicht widerrufen, nicht abgelaufen | Kantensatz für den Fluss (§2) |
| **Budget-Set** | nicht abgelaufen (**widerrufen, supersediert und `pending` eingeschlossen**), aggregiert je `(I, J, N)` über `max n` | Prüfung `Σ n_budget ≤ D` |

**`pending` bindet Budget.** Ein Vouch, dessen Vorgänger in der Autorenkette noch fehlt, trägt
keine Kante bei (§2), gehört aber ins **Budget-Set**: Er ist signiert, und der
Über-Commitment-Beweis beruht auf Signaturen, nicht auf Aktivität. Andernfalls ließe sich die
Budgetregel umgehen, indem ein Autor Vorgänger absichtlich zurückhält — alle Vouches blieben
`pending` und budgetfrei, bis der fehlende Vorgänger nachgereicht wird und sie gleichzeitig
`active` werden.

**Widerruf, Supersede und Freigabe.** Ein Widerruf stoppt den Fluss sofort (die Kante
verlässt das Aktiv-Set) und beendet die Haftung des Bürgen — **gibt das Budget aber nicht
frei**. Für Supersede gilt dasselbe. Frei wird Budget erst bei `t_exp` (§6.2), und erst, wenn
**alle** Vouches der Gruppe `(I, J, N)` abgelaufen sind. **Kein selbst-bezüglicher
Lebenszyklus-Akt gibt Budget frei; Budget folgt der Uhr, nicht dem Willen des Autors.**
Andernfalls ließe sich eine lange Laufzeit — das stärkste Signal — beliebig oft per Supersede
zurückholen, und die Knappheit wäre eine Formalität. Weil innerhalb einer Gruppe das
**Maximum** zählt und nicht die Summe, sind Erneuerung und Herabstufung dennoch frei: Ein
Autor kann seine Aussage jederzeit korrigieren, er kann nur ihr Gewicht nicht vorzeitig
anderswo einsetzen. Budget ist vorwärtsgerichtet, Haftung rückwärtsgerichtet; sie folgen
verschiedenen Uhren. Eine Nachhaftungsfrist wäre nicht auswertbar, weil sie eine
Cross-Chain-Zeitordnung verlangte, die es nicht gibt.

**Wirkung.** `w` ist dreifach gekoppelt: es bestimmt den Durchsatz der Kante, es verbraucht
Budget, und es bemisst die Haftung des Bürgen bei Defektion des Gebürgten (Enf-Spec §6). Damit
ist die **Deklaration selbst der Einsatz** — hohes Vertrauen lässt sich nicht billig behaupten.
Ein erfolgreicher Vouch bringt dem Bürgen umgekehrt **keine** Kapazitätsprämie (§1): der Ertrag
liegt in der Beziehung, nicht in der Metrik.

**Über-Commitment ist selbst-validierend.** Liegen mehrere signierte Vouches derselben Identität im
selben Scope mit `Σw > 1` vor, ist das ein unabhängig nachrechenbarer Beweis — dieselbe Klasse
wie Equivocation (Atom-Spec §4), mechanisch slashbar, ohne Verdikt. Bei Teilwissen ist das
beobachtete `Σw` zu klein: eine Verletzung wird möglicherweise **nicht erkannt**, aber nie eine
erfunden.

**Unlesbares oder ungültiges `n`.** Ist `v` keine CBOR-Map, fehlt der Key `0`, ist sein Wert
kein `uint`, oder liegt `n` außerhalb `[1, D]`, trägt dieser Vouch **keine Kante** und
**keinen Budget-Beitrag**. Weitere Keys sind unschädlich — geprüft wird Key `0`, nicht die
Map als Ganzes. Kein Beitrag, weil eine geratene Zahl eine Falschbeschuldigung wegen
Über-Commitment erzeugen könnte; keine Kante, weil das Unter-Vertrauen ist. Beides ist die
sichere Richtung, in verschiedene Richtungen.

**Nicht-kanonisches `v` ist unlesbar.** Atom-Spec §3 verlangt kanonische Kodierung, aber der
Re-Serialisierungs-Check des Verifizierers (Atom-Spec §6, Regel 2) deckt nur den **Core** ab;
`v` ist darin eine `bstr`, deren Inhalt uninterpretiert bleibt. Die Anforderung ist damit für
`v` nirgends durchgesetzt — sie liegt bei der Schicht, die `v` **liest**, und das ist für
`vouch@1` diese hier.

> **Normativ:** Ist `v` vorhanden und nicht kanonisch kodiert — nicht-minimale Ganzzahl,
> indefinite-length Map, unsortierte oder doppelte Schlüssel —, trägt dieser Vouch **keine
> Kante** und **keinen Budget-Beitrag**. Vermerk: `NON_CANONICAL_V`.

Drei Präzisierungen, weil jede von ihnen eine plausible Implementierung von einer korrekten
trennt:

- **Nicht wie ein abwesendes `v`.** Der Default `n = D` (`w = 1`) gilt für ein *fehlendes* `v`.
  Ihn auf ein *defektes* anzuwenden würde einen unlesbaren Payload zu maximalem Vertrauen
  aufwerten — Über-Vertrauen, die eine gefährliche Richtung (§7). Nicht-kanonisch fällt in
  denselben Zweig wie unlesbar, nicht in denselben wie abwesend.
- **Vor der Wertprüfung.** Kanonizität ist eine Eigenschaft der Bytes und geht jeder
  Interpretation voraus. Der Vorrang ist beobachtbar, sobald ein nicht-kanonisches `v` zugleich
  ein `n` außerhalb `[1, D]` trägt: der Vermerk lautet dann `NON_CANONICAL_V`, nicht
  `INVALID_VOUCH_WEIGHT`.
- **Der Rundlauf zählt in beide Richtungen.** Die Kanonizitätsprüfung ist selbst ein Dekodier-
  *und* Enkodiervorgang und kann an beiden Enden scheitern.

> **Normativ:** Scheitert der Rundlauf `decode → encode` an irgendeiner Stelle mit einer
> Exception, ist `v` **unlesbar** (`UNPARSABLE_VOUCH_PAYLOAD`). Liefert er ein Ergebnis, das den
> Eingabebytes nicht gleicht, ist `v` **nicht kanonisch** (`NON_CANONICAL_V`). Beides führt in
> denselben Zweig aus dem vorigen Absatz: keine Kante, kein Budget-Beitrag.

Der Grund ist die Nachsicht der Bibliothek, nicht die Bequemlichkeit des Aufrufers: `h'ff'`,
`h'a100ff'` und `h'a1ff01'` dekodieren **ohne Fehler** zu einem Sentinel-Objekt und scheitern
erst beim Re-Enkodieren — die beiden letzten sogar zu einem `dict`, sodass auch keine Formprüfung
sie abfängt. Solche Bytes sind kein Wert, der falsch geschrieben wurde; sie sind kein Wert.
`NON_CANONICAL_V` würde behaupten, es gebe eine kanonische Form desselben Inhalts, und die gibt
es nicht.

Für Payloads, die keine CBOR-Map sind, gilt dieselbe Reihenfolge; welcher der beiden Vermerke
erscheint, hängt von der Verstoßklasse ab. Die Zuordnung ist für jede Eingabe eindeutig, und die
Wirkung ist in beiden Fällen dieselbe.

Der **doppelte Schlüssel** ist der tragende Fall. Bei den übrigen Verstößen liefert das
Dekodieren den richtigen Wert, und der Schaden bleibt bei der Byte-Vergleichbarkeit. Bei einem
doppelten Key `0` verliert das Dekodieren einen Eintrag, und welcher der beiden gewinnt, steht
in keiner Spezifikation, sondern in der verwendeten Bibliothek. Atom-Spec §6, Regel 2 verlangt
„ohne doppelte Keys" — für den Core; für `v` gilt der Satz erst durch diesen Absatz. Ohne ihn
hinge `n` an einer undokumentierten Implementierungsentscheidung.

Dieselbe Regel gilt sinngemäß in jeder anderen Schicht, die ein `v` liest; der Vermerk trägt
dort denselben Namen (Profile-II §3.3).

---

## 4. Vertrauen als Fluss & der Min-Cut-Bound

**Definition.** `trust(s → T) = maxflow(s_in → T_in)` im gespaltenen, kapazitierten Graphen.
Die Quelle hängt an `s_in`, damit die interne Kante des Ankers — sein Budget `C(s)` — auf dem
Pfad liegt. Bei gültigem Budget ist das identisch zur Anbindung an `s_out`, weil
`Σ_e cap(e) ≤ C(s)` gilt; es unterscheidet sich genau dann, wenn der Anker über-committet
ist, und dann in Richtung Unter-Vertrauen.

**Schranke gegen Sybils.** Sei `H` die ehrliche Region (enthält `s`), `S` die Sybil-Region
(beliebig viele vom Angreifer erzeugte Identitäten). Eine **Angriffskante** ist ein Vouch
`h → g` von einem ehrlichen `h ∈ H` zu einem `g ∈ S` (der einzige Weg, wie Vertrauen `H`
verlassen kann).

> **Satz (simultaner Fluss).** Der **gleichzeitige** Vertrauensfluss in die Sybil-Region ist
> beschränkt durch die Kapazität der ehrlichen Endpunkte der Angriffskanten:
> ```
> maxflow(s → S)  ≤  Σ_{h ∈ Grenze} C(h)
> ```
> wobei `maxflow(s → S)` der Multi-Sink-Fluss über der **gesamten** Menge `S` ist und
> `Grenze` = die ehrlichen Knoten mit mindestens einer Angriffskante.

**Herleitung.** Führe einen Super-Sink `T*` mit ∞-Kanten von jedem `gᵢ_in` ein — an `T_in`,
nicht an `T_out`, sonst zählte die interne Kante des Ziels mit und die Multi-Sink-Semantik
wiche von der Einzelabfrage ab. Dann ist der simultane Gesamtfluss in `S` gleich
`maxflow(s_in → T*)`. Nach dem Max-Flow-Min-Cut-Theorem ist das gleich der minimalen
Schnittkapazität. Jeder Pfad von der Quelle nach `T*` passiert einen ehrlichen Grenzknoten
`h` — **einschließlich des Ankers selbst** —, dessen Durchsatz durch seine interne Kante
`C(h)` gedeckelt ist. Also `maxflow(s → T*) ≤ Σ_{h ∈ Grenze} C(h)`. Die endlichen
Kantenkapazitäten `⌊n·C(·)/D⌋` aus §3.1 können den Fluss nur weiter **senken**, nie anheben;
die Schranke gilt daher erst recht. ∎

Hinge die Quelle an `a_out`, wäre der Satz **falsch**: drei Kanten mit `n = D` von einem
Anker mit `C₀ = 16, D = 4` tragen je `⌊4·16/4⌋ = 16` und simultan 48 gegen eine behauptete
Schranke von 16. Die Anbindung an `a_in` ist kein Konventionsdetail, sondern die
Voraussetzung des Beweises.

> **⚠️ Die Summe der Einzelabfragen ist nicht beschränkt.** `Σ_{T ∈ S} trust(s → T)` ist eine
> **andere Größe** als `maxflow(s → S)` und kann diese überschreiten. Gegenbeispiel: `C(h) = 10`,
> `h` bürgt für `g₁` und `g₂`; einzeln berechnet ist `trust(s→g₁) = trust(s→g₂) = 10`, Summe 20,
> simultaner Fluss 10. Innerhalb von `S` verteilt sich der bei `g` ankommende Fluss über die
> internen Kanten auf jedes Ziel — **bei Einzelabfrage verdünnt nichts.**

> **Zwei unabhängige Divergenzursachen.** `Σ trust(s→Tᵢ)` übersteigt `maxflow(s→S)`, wenn
> (i) ein gemeinsamer Engpass stromaufwärts bindet, **oder** (ii) eine Einzelabfrage Knoten
> aus `S` als Zwischenknoten benutzt — im simultanen Lauf wird der Fluss dort schon an
> `gᵢ_in` absorbiert. Jede Ursache erzeugt für sich allein Divergenz (Golden Anchors: A nur
> (i), E nur (ii)); greift keine, sind beide Größen gleich (B, E₀). Wer nur einen der beiden
> Fälle testet, hat VR-02.1 halb getestet.

> **VR-02.1 — Aggregation MUSS simultan rechnen.** Jede Entscheidung, die Vertrauen über
> **mehrere** Identitäten verrechnet (Quorum, Abstimmung, „N unabhängige Attestierungen",
> Versicherungspool), MUSS den Multi-Sink-Fluss über der gesamten Anfragemenge berechnen.
> Die Summe einzeln berechneter `trust(s→Tᵢ)` ist **keine** gültige Näherung und trägt
> **keine** Sybil-Schranke.

**Korollar (`|S|`-Unabhängigkeit).** Die simultane Schranke hängt **nur** von den ehrlichen
Grenzknoten ab — **nicht von `|S|`**. Sind es `g` Angriffskanten mit Grenz-Kapazität `≤ C_max`,
gilt `maxflow(s → S) ≤ g · C_max`. Eine Million zusätzliche Sybils teilen dasselbe feste Budget.
Das ist „Identitäten gratis, Kanten teuer" — **bewiesen**, nicht erhofft. Die Schranke ist eine
Aussage über den Graphen, wie er vorliegt, und **keine** Aussage über Angriffskosten: `C(h)` wird
über demselben Kantenset gerechnet, das der Angreifer mitgestaltet hat.

> **⚠️ Distanz ist kaufbar (D139).** `d(s,h)` ist keine Eigenschaft des ehrlichen Knotens `h`,
> sondern die BFS-Distanz über dem **aktuellen** `E⁺`. Ein Angreifer, der einen seed-nahen
> ehrlichen Knoten `p` verwirrt, zieht durch dessen Bürgschaften bis zu `min(D, C(p))` weitere
> ehrliche Knoten gleichzeitig näher an den Seed und hebt damit deren Kapazität. `p` bürgt dabei
> für **ehrliche** Knoten, nicht für Sybils — `p` ist also **kein Grenzknoten** und taucht in
> `Σ_{h ∈ Grenze} C(h)` nicht auf. Gekauft wird genau der Knoten, den die Schranke nicht sieht.
>
> **Gemessen** mit `γ = ½`, `C₀ = 16`, `D = 16` (D141). Ein Ziel `S`, ein Grenzknoten `h`, der
> über vier Ketten der Länge 4 einen Zufluss von `8` hat. Ohne Angriff sitzt `h` bei `d = 4` mit
> `C(h) = 1`, und `maxflow(A → S) = 1`: die Knotendecke schneidet vorhandenen ehrlichen Zufluss
> ab. Der Angreifer verwirrt `p` bei `d = 1` und lässt `p` mit `n = 2` für `h` bürgen — die Kante
> trägt `cap = ⌊2 · 8 / 16⌋ = 1`. Danach sitzt `h` bei `d = 2` mit `C(h) = 4`, und
> `maxflow(A → S) = 4`.
>
> Gekauft wird also **nicht Fluss, sondern das Entfernen einer Decke.** `p` steuert eine einzige
> Kapazitätseinheit bei; drei der vier Einheiten sind ehrlicher Fluss, der vorher an `C(h) = 1`
> abgeschnitten wurde. Deshalb ist der lohnende Grenzknoten nicht der unerreichbare, sondern der
> **gut verbundene, aber seed-ferne** — Peripherie mit Substanz.
>
> Der Min-Cut-Satz bleibt davon unberührt — er gilt über dem Graphen, der vorliegt. Was **nicht**
> folgt, ist der Schluss, eine seed-ferne Angriffskante sei von sich aus billig. Seed-Ferne wird
> aus demselben Vorrat verwirrter ehrlicher Menschen bezahlt wie die Angriffskanten selbst; die
> beiden Verteidigungslinien sind nicht unabhängig. Die Konstruktion stammt von Rudermans Kritik
> an der Advogato-Metrik, deren Kapazitätsmodell dasselbe Distanz-Decay ist.
>
> **Wann sie wandert (D142).** `Σ_{h ∈ Grenze} C(h)` ist genau dann angreiferabhängig, wenn ein
> Zug die **Distanz** eines Grenzknotens verschiebt. Ein Zug, der `d` unberührt lässt — etwa eine
> breite Bürgschaft auf einen bereits seed-nahen Knoten —, ändert keine Kapazität und addiert
> höchstens den Fluss, den er selbst trägt. Gemessen: Hebel `3` beim Distanzkauf gegen Hebel
> `≤ 1` bei jedem Zug ohne Distanzänderung (`tests/trust/test_deckenelastizitaet.py`). Wo die
> Decke nicht bindet, ist die Schranke schlaff und überschätzt den Angreifer — das ist die
> sichere Richtung und kein Defekt. Der Defekt ist allein die Beweglichkeit.
>
> **Kein Mechanismus dagegen (D143).** Entschieden und begründet: der Hebel entsteht daraus, dass
> die Decke ehrlichen Fluss abschneidet, der bereits anliegt. Wer den Kauf verhindert, hält
> genau diesen ehrlichen Fluss draußen.

> **Schärfere Schranke.** Unter gültigem Budget gilt zusätzlich
> `maxflow(s → S) ≤ Σ_{h ∈ Grenze} Σ_{e Angriffskante von h} ⌊n_e·C(h)/D⌋ ≤ Σ_{h} C(h)`.
> Die Kanten-Caps sind die tatsächlich bindende Größe; `Σ C(h)` ist die schwächere, aber
> budget-unabhängige Form.

**Wirkung des Gewichts auf die Einzelabfrage.** Auch ohne Verdünnung über `|S|` ist der Wert
eines einzelnen Sybils nicht durch `C(h)` gedeckelt, sondern durch `w_e` — durch das, was der
ehrliche Bürge **dieser einen Kante** explizit zugewiesen hat (§3.1). Um Sybils über eine
Schwelle zu heben, braucht ein Angreifer daher ein großes `w`; ein großes `w` bindet das Budget
des Bürgen und aktiviert seine Haftung. Identitäten bleiben gratis — ohne teuer gebundenes
fremdes `w` bleiben sie wertlos.

> **Was `Σw ≤ 1` kostet — und was nicht.** Am kanonischen Testgraphen (Golden Anchors §3)
> senkt die Budgetregel den **simultanen** Fluss in die Sybil-Region **nicht**: 4 mit
> über-committetem Bürgen (Variante A), 4 mit gültigem Budget (E, F). Sie senkt allein die
> Summe der Einzelabfragen, und auch die nur von 12 auf 10. Der Ertrag liegt nicht in der
> Unterdrückung, sondern darin, dass A mechanisch beweisbar wird (Über-Commitment, §3.1) und
> F nicht. Das ist L2 in Zahlen — wer `Σw ≤ 1` für eine Sybil-Abwehr hält, hat den
> Mechanismus falsch verstanden.
>
> **Die Angriffsform hängt nicht vom Verifizierer ab — die Schranke tut es.** Bei fester
> Sybil-Zahl ist eine gemischte Belegung (`n = 2,1,1` auf drei Ziele, `S` vernetzt) gegen
> **beide** Verifiziererformen optimal: Summe 10, simultan 4, drei Identitäten über einer
> Schwelle von 2. Es gibt keinen Trade-off zwischen Streuung und Konzentration, den ein
> Angreifer zu treffen hätte. Der Unterschied liegt allein beim Verifizierer: gegen die Summe
> der Einzelabfragen ist der Angriff **unbeschränkt**, weil `|S|` frei ist und jeder weitere
> erreichbare Sybil addiert; gegen den simultanen Fluss greift die Schranke dieses
> Abschnitts. Wer VR-02.1 verletzt, wählt nicht eine ungenauere Zahl — er wählt eine Größe
> ohne obere Schranke.

> **⚠️ Die Sybil-Schranke ist keine Kollusions-Schranke.** Der Beweis setzt voraus, dass
> zwischen `H` und `S` **wenige** Angriffskanten liegen. Bei echter Unterwanderung gilt das
> nicht: kollaborierende Menschen haben je ihre eigenen, *echten* Beziehungen — der Schnitt ist
> nicht dünn, er existiert nicht als Schnitt. Die bewiesene Schranke schützt gegen **gefälschte
> Identitäten**, nicht gegen **echte Menschen, die sich abstimmen**. Das ist keine Schwäche
> dieser Konstruktion, sondern die Grenze der gesamten Klasse sozialgraph-basierter Abwehren
> (Viswanath et al., SIGCOMM 2010: solche Verfahren betreiben im Kern lokale
> Community-Erkennung; die Erkennungsgenauigkeit fällt, je näher am vertrauten Knoten der
> Angreifer seine Kanten platziert). Für MaR folgt daraus die Form des optimalen Angriffs:
> **nicht viele Kanten, sondern wenige nahe** — ein Komplize bei `d = 1` ist mehr wert als
> hundert bei `d = 4`. Gegenmittel sind Pfad-Disjunktheit und die Kennzahlen aus §8, nicht die
> Schranke dieses Abschnitts.

**Neuling ≈ 0.** Eine frische Identity ohne eingehende Vouch-Kante ist von `s` unerreichbar
(`d = ∞`), trägt also `C = 0` und empfängt Fluss 0 — strukturell, ohne Sonderfall.

---

## 5. PageRank-Relaxation (die schnelle Sicht)

Personalisierter Random-Walk-mit-Restart vom Seed:

```
t_s = α · e_s + (1−α) · Pᵀ · t_s     ⇔     t_s = α (I − (1−α) Pᵀ)⁻¹ · e_s
```

mit **sub-stochastischer** Übergangsmatrix `P` (absolute, an `D` gemessene Vouch-Adjazenz),
Restart-Vektor `e_s` (der Seed, §6.3) und Restart-Wahrscheinlichkeit `α`.

> **Die Relaxation liest `w` absolut (§3.1; D45, korrigiert D27).** Der Übergangsanteil ist
> `P[J][I] = n_kante(I, J) / D` — an `D` gemessen, **ohne** Normalisierung über `Σw` und ohne
> Kopplung an andere Kanten desselben Autors. Weil `Σ n ≤ D` gilt, ist jede Spalte
> sub-stochastisch; es folgt `Σt ≤ 1 − (1−α)^K`, und das Defizit `1 − Σt` ist das ungenutzte
> Budget, als Zahl lesbar (Anker PR-5).
>
> Eine Normalisierung über `Σw` kürzte `D` heraus: ein Autor mit einer einzigen Kante und `n = 1`
> bei `D = 100` bekäme `P = 1`, exakt wie bei `n = 100`. Der Probe-Vouch mit `w = 0.05` würde
> also gerade dann wie eine volle Bürgschaft behandelt, wenn er allein steht — das erklärte Ziel
> von D27 verfehlt seine eigene Regel. Sie bräche zudem die Monotonie aus §7: eine zusätzliche
> Kante von `I` senkte den Anteil jeder bestehenden, also höbe **fehlendes Wissen fremde Werte**.
> Erschöpfend gemessen über alle 32 Teilgraphen der Variante B: **9 Verletzungen** unter der
> normalisierten Fassung, **0** unter dieser (02b, Anker K9).
>
> **Es gibt hier keine D9-Ausnahme.** §5 trägt keine Kopplung, die D9 verbietet; §7 gilt in
> **beiden** Sichten, nicht nur in §4.
>
> Der Buchstabe `P` ersetzt das frühere `C`, um die Kollision mit der Knotenkapazität `C(x)`
> (§3) zu vermeiden. Reine Umbenennung, keine inhaltliche Änderung.

> **Distanzkauf greift hier nicht (D140, zu D139).** Der Angriff aus §4 hebt Kapazitäten, indem
> er Distanzen verkürzt. In §5 wirkt `C(x)` allein als Filter, welche Kanten in `E⁺` liegen
> (Anker K13); das Gewicht einer Kante hängt nicht von `C` ab. Ein verwirrter seed-naher Knoten
> kann damit den Kantensatz verändern, aber **keine Masse erzeugen**: seine Spalte ist
> sub-stochastisch, er gibt höchstens weiter, was er empfängt. Der Ertrag bleibt durch die
> **Vor-Angriffs-Masse** der verwirrten Knoten beschränkt, und es entsteht kein quadratischer
> Term. Das macht §5 **nicht** zum Ersatz für §4 — die Relaxation trägt weiterhin keine harte
> Schranke und bleibt für Gates verboten. Die Verwundbarkeit von §4 ist der Preis der harten
> Schranke, nicht ein Fehler in der Wahl der Sicht.

- **Garantie:** nur **weich/probabilistisch** sybil-resistent — Walks überqueren wenige
  Angriffskanten selten, also erreicht `S` wenig stationäre Masse, aber **keine harte
  Schranke**.
- **Erlaubt für:** billiges Ranking/Gewichten vieler Knoten, „wer ist grob vertraut".
- **Verboten für:** harte Admission-/Gate-Entscheidungen — die laufen über §4.

Beide Sichten teilen denselben Graphen. Keine zwei Welten, nur eine harte und eine schnelle
Projektion.

---

## 6. Bond, Seeds & harte Decke — wie sie präzise eingehen

### 6.1 Bond: Oberseite verboten, Unterseite erlaubt

- Die Kapazitätsfunktion `C(·)` liest `v.bond_ref` **nicht**. Zwei Menschen an gleicher
  struktureller Position bekommen identische Kapazität, egal ob reich oder arm.
- Die **einzige** Protokollwirkung eines Bonds: er macht den Vouch unter einem
  Defektions-/Equivocation-Beweis **slashbar** (ökonomische Schicht). Bonden ist
  selbst-auferlegtes Risiko (Costly Signal), kein Privileg — der Ehrliche gewinnt nichts,
  nur der Defektor verliert.
- Eine Policy darf für Hochrisiko-Kontexte verlangen, dass *nur gebondete* Kanten **zählen**
  (ein Filter wie der Zweck-Tag). Auch dann erhält die gebondete Kante dieselbe strukturelle
  Kapazität wie ungebondet — Bond ist nie ein Multiplikator.
- **Ehrlicher Residual (offen benannt):** Glaubwürdigkeit-durch-Risiko ist mild „kaufbar" —
  ein Armer kann nicht so teuer bewehren. Aber das ist *Risiko*, nicht *Kapazität*; der
  Ehrliche verliert nie, egal wie arm. Größenordnungen milder als „Geld kauft Standing".

### 6.2 Harte Decke `t_exp`

Ein Vouch mit `t_exp` voidet sich selbst nach Ablauf — **auch wenn sein Widerruf nie
ankommt**. Das ist der partitionstolerante Backstop gegen den steckengebliebenen Revoke
(§7). Strukturell, ohne Policy. **Ausgewertet wird `t_exp` lokal** gegen die subjektive
Verifizierer-Zeit `now` (Atom-Spec §6): zwei Verifizierer dürfen legitim uneins sein, ob ein
Vouch schon abgelaufen ist — die sichere Richtung ist stets Unter-Vertrauen. „Voidet sich
selbst" meint also *strukturell definiert*, nicht *global synchron*.

**`t_exp` ist für Vouches verpflichtend.** In Scopes mit Budgetregel (§3.1) MUSS ein Vouch
`t_exp` tragen, oder die Policy setzt eine Maximallaufzeit als Default — andernfalls bindet er
Budget unbefristet. Damit wird `t_exp` zur ökonomischen Entscheidung und nicht bloß zum
Sicherheits-Backstop: kurze Laufzeit bedeutet liquides Budget, häufige Erneuerung und ein
schwächeres Signal; lange Laufzeit bedeutet ein starkes Signal bei gebundener Kapazität.
Erneuerung ist wiederholte aktive Bestätigung und damit frischere Evidenz als ein alter,
nie widerrufener Vouch.

### 6.3 Geschichtete Seeds

Der Restart-/Quellvektor unterscheidet die Sichten; die Berechnung ist identisch:

- **Individuell:** `e_s` setzt Masse auf das eigene, out-of-band verifizierte Ankerset.
  Grundwahrheit, immer verfügbar, unentziehbar.
- **Nukleus:** `e_N` setzt Masse auf das vom Nukleus deklarierte Ankerset. Optionale
  geteilte Linse für billige Koordination, explizit „die Sicht des Nukleus".
- **Fallback:** fehlt die Nukleus-Linse (Partition), fällt der Verifizierer sauber auf `e_s`
  zurück. Ein globaler Seed existiert nie.

---

## 7. Partitionstoleranz

Jeder rechnet über seinen *aktuell bekannten* Teilgraphen (die per Gossip erhaltenen
Vouch-Claims). Die Partition ist kein zu behebender Defekt — die Lokalität *macht* die
Toleranz.

- **Monotonie (sichere Richtung).** Max-Flow ist monoton in den Kanten. Fehlende Vouch-Kanten
  können den berechneten Fluss nur **senken** ⇒ das Ergebnis ist eine konservative
  **Untergrenze** des wahren Flusses. Im Zweifel wird **unter**-vertraut — die sichere
  Richtung für Sybil-Resistenz. (Distanz analog: fehlende Kanten ⇒ geschätzte Distanz ≥ wahre
  ⇒ wieder Unter-Vertrauen.)
- **⚠️ Monotonie gilt für den Graphen, nicht für den Claim-Bestand (D118).** Zwischen beiden
  liegt die Budgetprüfung `Σ n ≤ D` aus §3.1, und die ist **nicht** monoton: ein hinzukommender
  Vouch kann `Σ n` über `D` heben, und dann fallen **alle** Kanten dieses Autors aus — nicht die
  letzte, nicht anteilig. Wer weniger weiß, sieht dann **mehr** Vertrauen.
  Kleinstes Gegenbeispiel: zwei Vouches mit `n = 51` bei `D = 100`.
  Das ist die **zweite** gefährliche Richtung, und die drei Abwehren unten greifen gegen sie
  nicht — der fehlende Claim ist hier eine Bürgschaft und kein Widerruf. Sie heilt beim
  Zustellen: sobald der überzeichnende Vouch eintrifft, fällt alles, und die Richtung ist danach
  dauerhaft konservativ. Der Autor verliert dabei sein gesamtes Budget und hinterlässt einen
  signierten Beweis; die Folge regelt Layer 05 (D40).
- **⚠️ Und nicht monoton in `now` (D362).** Dieselbe Budgetprüfung macht den Wert auch
  in der Zeit nicht monoton: läuft eine Bürgschaft ab, verlässt sie das Budget-Set,
  `Σ n` fällt unter `D`, das Autor-Flag verschwindet, und **alle** Kanten dieses Autors
  kehren zurück. Der Wert steigt dann mit fortschreitender Uhr. Abwehr 1 unten ist
  deshalb keine Decke gegen jede Form von Über-Vertrauen — hier ist `t_exp` die Ursache.
  Zwei ehrliche Knoten mit Uhrversatz rechnen verschieden, und der mit der vorlaufenden
  Uhr sieht mehr. Gilt bei `include_flagged = False`, dem Default; bei `True` ist der
  Wert monoton fallend.
- **Die andere gefährliche Richtung:** ein fehlender *Widerruf* (nicht eine fehlende
  Bürgschaft). Hast du den Vouch, aber sein `revoke` steckt in einer Partition, dann
  **über**-vertraust du. Drei gestaffelte Abwehren:
  1. `t_exp` — strukturelle harte Decke (§6.2).
  2. Widerrufe propagieren mit **Priorität** (sicherheitskritisch) — Policy.
  3. Für Hochrisiko: **frische positive Evidenz** verlangen, nicht bloße Abwesenheit eines
     Widerrufs — denn über eine Mesh ist Abwesenheit von Evidenz keine Evidenz der
     Abwesenheit. Policy.

---

## 8. Policy-Knöpfe (parametrisiert, nicht im Protokoll fixiert)

Der *Mechanismus* ist festgelegt; die *Werte* sind Interpretation (A2):

- `γ` (Distanz-Decay) und `α` (PageRank-Restart): Default eher **schnelles** Abklingen —
  passt zum Lokal-Ethos und verbessert die Sybil-Resistenz (weniger Fluss in die Peripherie).
- `C₀` (Seed-Budget): skaliert die Leiter. **Nicht mehr verhältniserhaltend**, seit die
  Kantenkapazität abrundet: bei `C₀ = 16` ist `⌊1·2/4⌋ = 0`, bei `C₀ = 160` ist
  `⌊1·20/4⌋ = 5`. `C₀` bestimmt zusammen mit `D` den Granularitätsboden und damit, wie weit
  vom Seed noch gebürgt werden kann.
- Schwelle & Gate pro Aktion: die Metrik **exponiert** nur einen Wert; ob er „reicht", ist
  Policy. (Der Neuling hat Null — die anderen *sehen* das und entscheiden selbst.)
- Zweck-Filter, Bond-Pflicht für Hochrisiko: Filter, keine neuen Mechanismen.
- `D` (Nenner des Vouch-Gewichts, §3.1): bestimmt die Granularität von `w`. **Über die
  Lebensdauer eines Scopes unveränderlich** — ein anderes `D` bedeutet einen neuen Scope,
  sonst würden bestehende signierte Vouches still umbewertet. **SHOULD `D ≥ C₀`**, damit die
  Out-Degree an der Position hängt (§3.1) und nicht an einer gezählten Grenze. Eine
  geschlossene Kurzform der Kantenkapazität gibt es **nicht**: `⌊n·⌊C₀γ^d⌋/D⌋` ist doppelt
  gerundet und lässt sich nur bei ganzzahligem `C₀γ^d` zu `⌊n·γ^d⌋` zusammenziehen
  (Gegenbeispiel `C₀ = D = 16, γ = ⅔, d = 2, n = 9`: `3` gegen `4`).
- **⚠️ Granularitätsboden.** `cap(I→J) = 0`, sobald `n·C(I) < D`. Ein Knoten mit kleiner
  Kapazität kann nur noch für wenige — am Rand für genau einen — mit vollem Budget bürgen,
  oder für niemanden. `D` schneidet die Peripherie ab, unabhängig von `γ`.
- **Budgetgrenze:** Default `Σw ≤ 1`. Ein Nukleus darf lockerer oder strenger setzen.
- **Pfad-Disjunktheit statt bloßer Anzahl.** Eine Policy kann „N Attestierungen über
  **knoten-disjunkte** Pfade vom Seed" verlangen statt nur „N Attestierungen". Berechnung:
  derselbe Max-Flow mit **Einheitskapazitäten auf den internen Knotenkanten und auf den
  Vouch-Kanten** — also **knoten**-disjunkt, nicht kantendisjunkt. Zwei Pfade durch denselben
  Bürgen sind ein Bürge. Die Vouch-Kanten tragen `1` und nicht ∞: zwei knotendisjunkte Pfade
  teilen nie eine Kante, die Kappung ist daher verlustfrei — und ohne sie liefert der Solver bei
  einer direkten Anker→Ziel-Kante keinen Pfadwert, sondern den ∞-Sentinel (D42).
  **Endpunkte werden nicht gespalten:** die internen Kanten der Anker
  tragen ∞, die des Ziels liegt ohnehin nicht auf dem Pfad (§4). Sonst wäre die Zahl von
  einem einzelnen Anker aus trivial 1. Wirkung: eine Koalition, die über *einen*
  Bürgen eingesickert ist, hat Min-Cut 1 — egal wie viele Mitglieder sie hat. Das ist die
  strukturelle Fassung von „Zeugen dürfen nicht voneinander abhängen".
- **Beobachtungskennzahlen (keine Schwellen, kein Zwang).** Zwei Zahlen, die jeder Verifizierer
  auf seinem eigenen Teilgraphen rechnet:
  *Quellenunabhängigkeit* — sind die Bürgen von `X` untereinander pfad-disjunkt zum Seed?
  (Tausend Bürgen aus einem Cluster sind ein Bürge.)
  *Ersetzbarkeit* — ist `X` ein Schnittknoten, bricht der Fluss zur Peripherie ohne ihn zusammen?
  Hohe Stellung aus vielen unabhängigen Quellen bei vorhandenen Alternativpfaden ist verdient
  und jederzeit bestreitbar. Hohe Stellung aus einer Quelle ohne Alternative ist ein
  Kaperungsziel, unabhängig von der Verdienstlage der Person. Die Metrik exponiert nur die
  Zahlen; die Deutung bleibt beim Beobachter.
- **⚠️ Kalibrierungs-Nebenbedingung (Bootstrap).** `Σw ≤ 1` macht die Frühphase eng. Für `f`
  Gründer, `M` Neulinge, `m` Bürgen je Neuling und Admission-Schwelle `θ`:
  ```
  θ ≤ f · C₀ / M          (Kapazität — unabhängig von D und m)
  D ≥ M · m / f           (Granularität — Out-Degree je Gründer)
  ```
  Beide Bedingungen sind unabhängig und beide bindend. Für `f = 3, C₀ = 16, M = 17` folgt
  `θ ≤ 2`; `m = 2` liefert dieselbe Vertrauenshöhe wie `m = 1` bei doppelter
  Pfad-Disjunktheit (die Rundung frisst den Unterschied — Redundanz ist dort gratis),
  `m = 3` kollabiert am Granularitätsboden auf null. Die Kapazitätsbedingung ist dabei die
  **optimistische** Form: nach Rundung sind von `f·C₀ = 48` Einheiten real nur 36
  verteilbar (Golden Anchors §7).
- **⚠️ Harte Reichweite.** Ab `d` mit `⌊C₀γ^d⌋ = 0` kann ein Mitglied **keinen** wirksamen
  Vouch mehr tragen — gleich wie viel Budget es einsetzt und gleich wie viele Bürgen ein
  Kandidat sammelt. Damit gilt `r_max = ⌊log_{1/γ} C₀⌋`, bei `C₀ = 16, γ = ½` also
  `r_max = 4` für die Bürgschaftsfähigkeit und `5` für die Mitgliedschaft. Ein Nukleus mit
  `θ = 2` sättigt bei rund **600 Mitgliedern** und Radius 5; wer mehr will, muss `C₀` oder
  `γ` ändern. Das ist die quantitative Fassung von „maximal lokal" und keine Panne.
- **Geflaggte Autoren.** Ob ein Bürge mit `equivocation-flagged` oder erwiesenem
  Über-Commitment noch Fluss trägt, ist Policy (`include_flagged`, Default *nein*). Die
  Budgetrechnung ist davon **unberührt** — ein Flag darf die Grundlage nicht verschieben, auf
  der es erkannt wurde.

---

### 8.1 Woher die Kalibrierung kommt (D147)

Die Werte sind Policy, ihre **Herkunft** ist es nicht. `C₀`, `γ` und `D` stehen nach
`00 §4` Schlüssel 9 im Genesis, und `D` steckt über `n/D` in jeder signierten Vouch. Wer mit
einem anderen `D` rechnet als der Scope deklariert, bewertet Bestandssignaturen still um —
genau das, was der Absatz oben mit „ein anderes `D` bedeutet einen neuen Scope" ausschließt.

**Der Ort der Herleitung ist getrennt von der Rechnung.** `resolve_trust_params` nimmt Scope und
Genesis-Objekt, rechnet `SHA-256(DOM_NUC_GEN ‖ cbor(genesis_obj)) == scope` nach und liefert die
`TrustParams` dieses Nukleus. `derive`, `trust` und `rank` bleiben parametrisiert und kennen kein
Genesis — dieselbe Naht wie in `03 §1.2`, wo `resolve_policy` das Genesis verlangt und die
Profilfunktionen die fertige Policy übergeben bekommen.

| Lage | Antwort |
|---|---|
| Genesis passt nicht zum Scope | `ValueError` |
| Schlüssel 9 vorhanden, keine Parameter übergeben | die Werte des Genesis |
| Schlüssel 9 vorhanden, übergebene Werte weichen ab | `ValueError` |
| Schlüssel 9 fehlt, Parameter übergeben | die übergebenen Werte |
| Schlüssel 9 fehlt, keine Parameter übergeben | `ValueError` |

**Ein fehlender Schlüssel 9 ist kein Teilwissen.** `00 §4.0` erklärt ihn für optional: fehlt er,
hat der Nukleus die Kalibrierung out-of-band gelassen. Das ist eine Aussage des Nukleus und nicht
eine Lücke im Bestand des Lesers — deshalb trägt hier keine Sicherheits-Voreinstellung, sondern
die Frage, ob der Aufrufer die Werte anderswoher hat.

**Warum kein Vermerk und kein Weiterrechnen bei Abweichung.** Die Praxis kennt dafür den
Soft-Fail: fehlt die Prüfinformation, wird trotzdem gerechnet. Er hat sich in der Web-PKI als
untauglich erwiesen, weil die Prüfinformation dort **online** geholt werden muss und ein
Angreifer, der ohnehin den Kanal hält, sie schlicht blockiert. Die Antwort der Praxis war nicht
ein besserer Soft-Fail, sondern die Information mitzuliefern statt sie nachzuschlagen. Ein
Genesis ist unveränderlich, wenige hundert Bytes groß, content-adressiert, und sein Hash steht
als `N` in jedem Claim; es kann mitreisen. Die Verfügbarkeitssorge, die den Soft-Fail erzwungen
hat, besteht hier nicht.

**Nicht hergeleitet werden `α` und `K`** (§5). Sie stehen nicht im Genesis, sind reine
Policy-Knöpfe und bleiben Feld von `RelaxParams` neben dem hergeleiteten `base`.

---

## 9. Bewusst getragene v1-Grenzen & gemachte Designentscheidungen

- **Geometrischer Decay** `⌊C₀ γ^d⌋` ist eine *gewählte* Form (ein Knopf, saubere Monotonie);
  Advogatos Original nutzt ein gestuftes Schema. Austauschbar, solange monoton fallend.
- **Hop-Distanz** (BFS) als Default; gewichtete Distanz wäre ein Knopf.
- **PageRank nur als Relaxation** — bei Missbrauch für harte Gates verliert man die Schranke
  aus §4. Diese Trennlinie ist nicht verhandelbar.
- **Berechnungskosten.** Max-Flow ist paarweise/on-demand teurer als ein PageRank-Lauf —
  bewusst akzeptiert, weil „paarweise und lokal" exakt zum Lokal-Ethos passt. Caching der
  Aktiv-Sets und der BFS-Distanzen ist Implementierungssache.
- **Seed-Integrität** bleibt die wertbildende Voraussetzung (Atom-Spec §8): die gesamte
  Schranke aus §4 setzt voraus, dass das initiale Ankerset out-of-band sauber etabliert ist.
- **Einzelabfragen verdünnen nicht** (§4). Wer Sybil-Schutz über eine Menge braucht, muss
  simultan rechnen (VR-02.1). Die Summe von Einzelwerten trägt keine Schranke.
- **Kollusion ist nicht Sybil** (§4). Gegen eine hinreichend große, geduldige, echt eingebettete
  Koalition hilft kein Protokoll. Die Mechanismen dieser Schicht erhöhen die nötige
  Koalitionsgröße und machen die Vorbereitung sichtbar — mehr ist nicht zu haben.
- **Restfenster bei Widerruf vor Defektion** (§3.1). Ein Bürge kann kurz vor der Defektion
  seines Komplizen widerrufen und der Haftung entgehen. Bepreist ist das durch den Verlust der
  Bürgschaftskapazität bis `t_exp` — nicht über eine neue Identität rückholbar, weil Standing
  positional ist (§1). Zusätzlich ist das Muster in der Widerrufs-Historie lesbar.
- **Seed-Kompromittierung** (§6.3). Wer `e_N` kompromittiert, kompromittiert jeden, der diese
  Linse benutzt. Der Fallback auf `e_s` ist **Eindämmung, keine Abwehr**.

---

## 10. Vermerke und ihre Subjekte

Die Ableitung wirft keine Ausnahmen für schadhafte Eingaben; sie legt Vermerke ab und rechnet
weiter. Ein Vermerk benennt in seinem `subject` das zurückgewiesene Objekt — notfalls gröber, wenn
das Objekt ein Feld ist und keine eigene Adresse hat (D198, `04 §3.5`).

| Vermerk | Subjekt |
|---|---|
| `UNPARSABLE_VOUCH_PAYLOAD` | `claim_id` des Vouch |
| `NON_CANONICAL_V` | `claim_id` des Vouch |
| `INVALID_VOUCH_WEIGHT` | `claim_id` des Vouch |
| `VOUCH_WITHOUT_TEXP` | `claim_id` des Vouch |
| `SUBGRANULAR_VOUCH` | `claim_id` des Mitglieds mit `n == n_kante` |
| `OVERCOMMITTED_AUTHOR` | **Identity des Autors** |

Die vier ersten Lagen entstehen beim Dekodieren von `v` (`02a §2.3`): `v` ist nicht dekodierbar,
ist kein Map, führt den Schlüssel 0 nicht oder trägt dort keinen nichtnegativen `int` — das ergibt
`UNPARSABLE_VOUCH_PAYLOAD`; `v` dekodiert, ist aber nicht kanonisch kodiert — `NON_CANONICAL_V`;
`n` liegt ausserhalb von `1 ≤ n ≤ D` — `INVALID_VOUCH_WEIGHT`; der Vouch trägt kein `t_exp` —
`VOUCH_WITHOUT_TEXP`. `SUBGRANULAR_VOUCH` entsteht beim Aufbau des Graphen, wenn die
Kantenkapazität `⌊n_kante·C_author/D⌋` auf null fällt. `OVERCOMMITTED_AUTHOR` entsteht danach,
wenn die Summe der Budgets eines Autors `D` überschreitet.

**`OVERCOMMITTED_AUTHOR` ist die Ausnahme, und sie ist nicht am Typ erkennbar.** Sein Subjekt ist
ein öffentlicher Schlüssel, kein `claim_id`. Beide sind 32 Byte; wer `subject` pauschal im Speicher
nachschlägt, greift genau dort ins Leere. Der Grund ist derselbe wie überall sonst: das
zurückgewiesene Objekt ist hier der Autor und nicht ein einzelner Claim, denn kein einzelner Vouch
ist der überzählige — erst ihre Summe verletzt das Budget.

**`SUBGRANULAR_VOUCH` betrifft eine Gruppe, nicht einen Claim.** Als Adresse dient die `claim_id`
des Mitglieds mit `n == n_kante`, bei Gleichstand die lexikographisch kleinste. Damit ist der
Vermerk deterministisch, auch wenn mehrere Claims dasselbe `n` tragen (`02a §5`).

Ein Claim mit einem der vier Dekodier-Vermerke trägt nichts zum Fluss bei; er wird übersprungen,
nicht zurückgewiesen.
