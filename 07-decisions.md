# Entscheidungs-Register — Session 2026-08-10

Status: beschlossen · Protokollversion: 1 · Betroffene Layer: 00, 02, 04, 05, 06, VISION

Dieses Dokument ist ein **Register**, keine Spezifikation. Die normative Wahrheit bleibt in
`00`–`06`. Hier steht, *welche* Änderungen an diesen Dateien vorzunehmen sind und *warum* —
inklusive der explizit verworfenen Alternativen, damit sie nicht in einer späteren Sitzung
erneut als Neuvorschlag auftauchen.

Auslöser: die Frage, ob ein akkumuliertes Reputationsguthaben einen Anreiz zur Defektion
erzeugt („Sünden-Puffer"). Antwort: in Layer 02 nein (Vertrauen ist positional), in Layer 05
ja (Beta-Reputation ist ein Konto). Aus der Analyse sind 26 Entscheidungen gefolgt, davon
eine **Korrektur eines fehlerhaften Satzes in `02 §4`** (→ D6).

---

## Leitprinzipien der Sitzung

**L1 — Das Protokoll beantwortet keine Wertfragen, es macht sie entscheidbar.**
Wohlfahrts-, Solidaritäts- und Aufnahmemodelle sind Nukleus-Policy, nie Protokoll. Das
Protokoll liefert verifizierbare Reziprozitätshistorie, lokale Bewertung und funktionierenden
Exit; welches Verhalten als Beitrag zählt, entscheidet jeder Nukleus für sich. Der Markt der
Gesellschaftssysteme (`VISION §3`) ist der Selektionsmechanismus, nicht die Spec.

**L2 — Nicht verhindern, sondern sichtbar und bepreisbar machen.**
„detect-not-prevent", ausgeweitet auf Urteilsverzerrung, Kollusion und Machtkonzentration.
Ein systematisch voreingenommener Schiedsrichter wird nicht ausgeschlossen — seine
Verdikt-Historie wird auditierbar, und wer das Muster erkennt, senkt sein Gewicht.

**L3 — Downside-only.**
`02 §6.1` sagt über den Bond: „der Ehrliche gewinnt nichts, nur der Defektor verliert."
Dasselbe gilt für Bürgschaft (D18), Standing (D10) und `w` (D1). Man darf sich selbst
schlechter stellen, nie besser. Jeder Vorschlag, der eine positive Prämie einführt, ist
gegen dieses Prinzip zu prüfen.

**L4 — Begrenzte Voraussicht wird durch Exit getragen, nicht durch Vollständigkeit.**
Wir sitzen in derselben Position wie jeder Verfassungsgeber und denken nur an die Fälle, die
wir uns vorstellen können. Der Unterschied ist nicht größere Klugheit, sondern dass eine
verlassbare Ordnung nicht alle Fälle vorhersehen muss — sie muss überlebbar falsch sein
können. Daraus folgt: im Protokoll so wenig wie möglich fixieren.

---

## A. Kapazitätsmodell und Bürgschaft (Layer 02)

### D10 — Leitsatz: Vertrauen ist Zustand, kein Vermögen

Neu in `02 §1`. `C(x) = C₀·γ^{d(s,x)}` ist rein **positional** — durch Wohlverhalten lässt sich
kein höheres `C` erarbeiten. `t_s` ist ein Zustand des aktuellen Kantensets, kein Integral über
die Vergangenheit. Nicht akkumulierbar, nicht hortbar, nicht übertragbar. Damit existiert kein
Guthaben, das als Sünden-Puffer dienen könnte.

Diese Eigenschaft ist tragend, war aber nirgends benannt.

### D1 — Vouch-Gewicht `w` als Kanten-Obergrenze

Die Vouch-Kante `I_out → J_in` erhält Kapazität **`w · C(I)`** statt ∞.

```
w ∈ (0, 1]     Default w = 1
```

Bei `w = 1` identisch zum bisherigen Spec-Stand (die interne Knotenkante `C(I)` bleibt der
bindende Engpass). Untagged Vouches ⇒ `w = 1`.

**Warum Obergrenze und nicht Anteil:** Der Cap einer Kante hängt **nur von dieser Kante** ab.
Keine Kopplung an andere Kanten ⇒ neue Kanten können bestehende nie anheben ⇒ die Monotonie
aus `02 §7` bleibt erhalten (fehlendes Wissen senkt nur).

**Wirkung auf den Beweis in `02 §4`:** Das Argument „alle Vouch-Kanten haben ∞, also durchtrennt
kein Min-Cut sie" gilt nicht mehr. Die Schranke hält trotzdem — Kapazitätssenkung kann Max-Flow
nur senken. Ein Zusatzsatz, kein Beweisumbau.

### D2 — `w` als Rational mit nukleus-festem Nenner

```
w = n / D      n ∈ [1, D],  D = Nukleus-Policy,  Default n = D
Kantenkapazität = ⌊ n · C(I) / D ⌋
```

Abrunden ist die sichere Richtung (Unter-Vertrauen). Erhält die exakte Integer-Arithmetik der
harten Sicht; byte-reproduzierbar über Implementierungen hinweg.

**Verworfen:** Float (bricht Exaktheit). Festes Enum `{¼,½,¾,1}` (willkürlich granular).
Absoluter Integer-Cap (bricht die `C₀`-Skaleninvarianz aus `02 §8`).

### D3 — `Σw ≤ 1` als Selbstbindungsbudget

```
Für jede Identität I und Scope N:   Σ wᵢ ≤ 1
                                    über alle budget-bindenden ausgehenden Vouches von I
```

Bürgschaft wird knapp, weil sie **bindet**, nicht weil sie gezählt wird. Eine Bürgschaft für `X`
bindet Kapazität, die im Defektionsfall von `X` beim Bürgen haftet (→ D5).

**Ersetzt den zuvor erwogenen Out-Degree-Cap `k`.** Ein Zähler wäre eine willkürliche
Rationierung ohne ökonomische Begründung — und inkonsistent, solange unbegrenztes Bürgen keine
Haftung erzeugt. Die Bindung ist ein Preis, der Zähler war nur eine Grenze.

**Monotonie:** Die Budgetregel ist eine Gültigkeitsbedingung über dem Aktiv-Set, **keine
Normalisierung**. Bei Teilwissen ist das beobachtete `Σw` zu klein ⇒ eine Verletzung wird
möglicherweise **nicht erkannt**, aber nie eine erfunden. Teilwissen erzeugt Unter-Erkennung,
nie Falschbeschuldigung.

**Marktwirkung:** Bürgschaft wird zum Portfolio-Problem — `0.5` auf einen langjährigen Partner
oder `10 × 0.05` auf Neulinge? Sicherheit oder Reichweite? Preisbildung ohne eine einzige
Preisangabe im Protokoll, allein aus Knappheit plus Haftung.

### D4 — Über-Commitment ist ein selbst-validierender Fehler

`n` signierte Vouches derselben Identität mit `Σw > 1` im selben Scope sind ein unabhängig
nachrechenbarer Beweis — dieselbe Klasse wie Equivocation (Atom-Spec §4). **Mechanisch
slashbar, kein Verdikt nötig.** Kein neuer Beweistyp, keine neue Propagationsklasse.

### D5 — `w` wirkt dreifach

| Wirkung | Formel | Bedeutung |
|---|---|---|
| Durchsatz | Kante erhält `w · C(I)` | wie viel Vertrauen `I` weiterreicht |
| Knappheit | `Σw ≤ 1` | dass es begrenzt ist |
| Haftung | Defektion von `J` schlägt anteilig `w` auf `I` durch | was es `I` kostet |

Ein Parameter, drei gleichgerichtete Wirkungen. **Die Deklaration ist der Einsatz** — hohes
Vertrauen lässt sich nicht billig behaupten. Kein separater Ehrlichkeitsmechanismus nötig.
Konkretisiert `05 §6` („individuelle Haftung, eine Sprunghöhe"), das die Höhe offenließ.

### D5a — Haftungsdurchreichung nur bei selbst-validierenden Beweisen

- **Equivocation / Über-Commitment von `J`** ⇒ mechanischer Durchgriff `w · Schaden` auf `I`.
- **Subjektives Verdikt gegen `J`** ⇒ **kein** Bond-Slash beim Bürgen; nur Reputationswirkung
  (Enf-Spec Stufe 1).

Andernfalls haftete `I` für ein Urteil, an dem er nicht beteiligt war, und die Bürgschaft würde
zum Diffamierungshebel gegen den Bürgen — gegen die Schutzlogik von `05 §5`.

### D17 — Laufzeit, Widerruf und Freigabe

```
Widerruf   ⇒ Fluss stoppt sofort (Kante verlässt das Aktiv-Set)
           ⇒ Haftung endet
           ⇒ Budget bleibt gebunden bis t_exp
t_exp      ⇒ Budget wird frei
```

**Zwei Uhren, nicht eine.** Budget ist vorwärtsgerichtet (welche Kapazität kann ich künftig
binden?), Haftung rückwärtsgerichtet (wofür stehe ich ein?). Sie zusammenzulegen war der
ursprüngliche Fehler.

**Warum keine Nachhaftungsfrist:** Sie bräuchte „Defektion innerhalb Δ nach Widerruf", also eine
Cross-Chain-Zeitordnung, die MaR verweigert (`06` VR-06.3). `t_exp` wird lokal gegen `now`
ausgewertet und ist bereits gebaut.

**Warum Haftungsende beim Widerruf (Variante ii statt i):** Haftung bis `t_exp` wäre
unverhältnismäßig — man haftete für jemanden, von dem man sich vor 19 Monaten öffentlich
losgesagt hat — und würde alle `t_exp` nach unten drücken, also genau die langen Laufzeiten
entwerten, die das stärkste Signal tragen.

**Restfenster, bewusst getragen:** Ein Kollusions-Bürge kann kurz vor der Defektion seines
Komplizen widerrufen und der Haftung entgehen. Bepreist ist das durch den Verlust der gesamten
Bürgschaftskapazität für die Restlaufzeit — nicht über eine neue Identität rückholbar, weil
Standing positional ist (D10). Zusätzlich wird der Widerruf selbst zum sichtbaren Signal:
Ein Bürge, dessen Widerrufe auffällig oft kurz vor Defektionen liegen, hat eine lesbare
Historie (L2, wie D15/D18).

**Widerruf bleibt dominant:** Er kostet nichts extra und schützt andere; nicht zu widerrufen
hält die Haftung für einen Defektor lebendig. Niemand hat einen Grund zu zögern.

**Nebeneffekt:** `t_exp` wird zur ökonomischen Entscheidung statt zum bloßen Backstop — kurze
Laufzeit = liquides Budget, häufige Erneuerung, schwächeres Signal; lange Laufzeit = starkes
Signal, gebundenes Kapital. Erneuerung ist wiederholte aktive Bestätigung und damit frischere
Evidenz als ein zehn Jahre alter, nie widerrufener Vouch.

### D18 — Keine Kapazitätsbelohnung für erfolgreiche Bürgschaft

Ein erfolgreicher Vouch erhöht `C(I)` **nicht**. Begründung, an D10 anzuhängen, damit der
Vorschlag nicht erneut auftaucht:

- **D10 stirbt sonst.** `C` wäre akkumulativ — genau das Vermögen, dessen Abwesenheit das
  Feature ist.
- **Der Sünden-Puffer kehrt zurück**, eine Ebene versetzt: erst Kapazität sammeln, dann
  verbrennen.
- **Vouch-Farming.** Rational wäre, für möglichst *sichere* Kandidaten zu bürgen — also für
  längst Etablierte, nicht für Neulinge. Der Mechanismus würde Onboarding bestrafen.

**Die Belohnung existiert bereits, nur nicht in der Metrik:** Der Gebürgte wird zum
funktionierenden Gegenüber — Handelspartner, Lieferant, Poolmitglied. Der Ertrag liegt in der
Beziehung. Dazu L3: Der Lohn guten Bürgens ist, nichts zu verlieren und weiter bürgen zu können.

**Legitim ist zweite Ordnung:** Die eigene Vouch-Historie ist als Claim-Historie sichtbar; andere
lesen sie und entscheiden, wie viel `w` sie *mir* geben. Keine Protokollprämie, sondern
menschliches Urteil auf Basis von Information.

### D9 — Anteilige Kapazitätsteilung verworfen

`C(I)/deg_out(I)` bzw. Anteil `wᵢ/Σw` bricht die Monotonie aus `02 §7`: Bei Teilwissen ist `Σw`
zu klein ⇒ jeder bekannte Anteil zu groß ⇒ **fehlendes Wissen erhöht das errechnete Vertrauen**.
Über eine Mesh mit partial sync nicht tolerierbar.

Nicht durch eine Normalisierungsregel reparierbar: Jede Regel, in der andere Kanten den Anteil
einer Kante beeinflussen, hat diesen Defekt. Er liegt in der Kopplung, nicht in der Formel.

### D27 — Die PageRank-Relaxation liest `w`

Nachtrag aus der Prüfung des Spec-Nachzugs. D1 hinterließ `§5` unterspezifiziert: ob die
Übergangsmatrix das Vouch-Gewicht berücksichtigt, war offen — zwei Implementierungen hätten
legitim auseinanderlaufen können.

**Beschluss:** Der Übergangsanteil ist proportional zu `w`, danach spaltenstochastisch
normalisiert. Begründung: Ignorierte `§5` das Gewicht, behandelte es einen Probe-Vouch mit
`w = 0.05` wie eine volle Bürgschaft und wäre damit **großzügiger als die harte Sicht** — die
falsche Richtung. Eine Relaxation darf ungenauer sein, nie über-vertrauend.

**Kein Widerspruch zu D9.** Die dort verworfene Normalisierung bricht die Monotonie der *harten*
Schranke. In `§5` ist sie zulässig, weil dieser Abschnitt keine harte Schranke trägt und für
Gates verboten ist (`§5`, `§9`).

**Nebenbeschluss:** Übergangsmatrix `C` → `P` umbenannt (Kollision mit der Knotenkapazität
`C(x)`). Reine Notation.

**Weitere Nachbesserungen aus derselben Prüfung** (ohne eigene Entscheidungsnummer):
Symbolkollision `n` in `§3.1` aufgelöst; Abgrenzung des Knotenkapazitäts-Blockzitats in `§3`
gegen `§3.1`; `pending`-Vouches binden Budget (sonst umgeht ein zurückgehaltener Vorgänger die
Budgetregel).

**Präzisiert durch D40:** `w` ist in `§5` das Gewicht der **Gruppe** `(I, J, N)`, also
`n_kante / D`, nicht das eines einzelnen Claims. Sonst trüge ein erneuerter Vouch in der
Relaxation doppeltes Gewicht, während er in der harten Sicht einfach zählt — wieder die falsche
Richtung.

---

## B. Sybil-Schranke und Kollusion (Layer 02) ⚠️

### D6 — `02 §4` überclaimt: Summe der Einzelflüsse ≠ Multi-Sink-Fluss

`02 §4` definiert `trust(s → T) = maxflow(s_out → T_in)` **pro Ziel** und behauptet dann
`Σ_{T ∈ S} trust(s → T) ≤ Σ_{h ∈ Grenze} C(h)`. Die Super-Sink-Herleitung beweist jedoch den
**simultanen** Multi-Sink-Fluss — eine andere Größe.

**Gegenbeispiel:** `C(h) = 10`, `h` bürgt für `g₁` und `g₂`. Einzeln berechnet ist
`trust(s→g₁) = trust(s→g₂) = 10`, Summe 20. Der simultane Fluss ist 10. Der Satz gilt für 10.

Praktische Folge: **Bei Einzelabfrage verdünnt nichts.** Alle Kanten innerhalb der Sybil-Region
sind ∞, also erreicht der bei `g` ankommende Fluss jedes `T ∈ S`. Jeder Sybil bekommt einzeln
den vollen Kantenwert.

**Was `Σw ≤ 1` hieran repariert — und was nicht.** Die Summenidentität wird **nicht** repariert
(eine Angriffskante hat genau einen Kopf, aber innerhalb `S` verteilt sich der Fluss über
∞-Kanten auf alle Ziele). Repariert wird der praktisch gefährliche Teil: Der Wert eines
einzelnen Sybils ist nicht mehr durch `C(h)` gedeckelt, sondern durch `w_e` — durch das, was der
ehrliche Bürge *dieser einen Kante* explizit zugewiesen hat. Um Sybils über eine Schwelle zu
heben, braucht der Angreifer ein großes `w`, und ein großes `w` bindet das Budget des Bürgen und
aktiviert seine Haftung. **Identitäten bleiben gratis; ohne teuer gebundenes fremdes `w` bleiben
sie wertlos.**

### D7 — Reparatur: Satz umformulieren + VR-02.1

Gewählt: **Variante (a)** — den Satz ehrlich auf den simultanen Fluss beschränken und die Grenze
sichtbar machen. **Verworfen: Variante (b)** (`trust()` generell als Multi-Sink definieren) —
teurer und ändert die Semantik jeder Einzelabfrage.

> **VR-02.1 — Aggregation MUSS simultan rechnen.** Jede Entscheidung, die Vertrauen über
> **mehrere** Identitäten verrechnet (Quorum, Abstimmung, „N unabhängige Attestierungen",
> Versicherungspool), MUSS den Multi-Sink-Fluss über der gesamten Anfragemenge berechnen.
> Die Summe einzeln berechneter `trust(s→Tᵢ)` ist **keine** gültige Näherung und trägt
> **keine** Sybil-Schranke.

Zusätzlich unter „bewusst getragene Grenzen": *Einzelabfragen verdünnen nicht; wer Sybil-Schutz
über eine Menge braucht, muss simultan rechnen.*

### D20 — Sybil-Schranke ist keine Kollusions-Schranke

Expliziter Satz in `02 §4`. Der Beweis funktioniert, weil zwischen ehrlicher Region `H` und
Sybil-Region `S` **wenige Angriffskanten** liegen; er bindet den Fluss an `Σ C(h)` über die
Grenzknoten. Bei echter Unterwanderung gilt diese Annahme nicht: Kollaborierende Menschen haben
je ihre eigenen, *echten* Beziehungen. Der Schnitt ist nicht dünn — er existiert nicht als
Schnitt.

**Die bewiesene Schranke schützt gegen gefälschte Identitäten, nicht gegen echte Menschen, die
sich abstimmen.** Keine Schwäche dieser Konstruktion, sondern die Grenze der gesamten Klasse —
Viswanath et al. (SIGCOMM 2010) zeigten, dass sozialgraph-basierte Sybil-Abwehren im Kern lokale
Community-Erkennung betreiben, dass Netzwerke mit ausgeprägter Community-Struktur dadurch
*anfälliger* sind, und dass die Erkennungsgenauigkeit fällt, je näher am vertrauten Knoten der
Angreifer seine Kanten platziert.

**Direkte Folge für MaR:** `C(x) = C₀γ^d` macht Seed-Nähe zur einzigen Ressource. Der optimale
Angriff ist damit bestimmt — **nicht viele Kanten, sondern wenige nahe.** Ein Komplize bei
`d = 1` ist mehr wert als hundert bei `d = 4`. Muss ein Implementierer wissen, sonst nimmt er
einen Schutz an, den er nicht hat.

### D19 — Pfad-Disjunktheit als Policy-Primitiv

Statt „N Attestierungen" verlangt eine Policy „N Attestierungen über **knoten-disjunkte** Pfade
vom Seed". Berechnung: Max-Flow mit Einheitskapazitäten — derselbe Dinic, andere
Kapazitätsbelegung.

**Wirkung:** Eine Koalition, die über *einen* Bürgen eingesickert ist, hat Min-Cut 1, egal wie
viele Mitglieder sie hat. Sie kann kein Quorum von 3 unabhängigen Zeugen stellen.

Strukturelle Übersetzung von „Zeugen dürfen nicht voneinander abhängen" — Rechtsordnungen kennen
das als Befangenheitsregel, hier als Graphenkennzahl. **Die einzige Anti-Kollusions-Maßnahme,
die aus der vorhandenen Mathematik direkt folgt.** Aufzunehmen in `02 §8` neben der Schwelle.

### D8 — Brückenbelohnung (Betweenness) verworfen

Erwogen als Gegenmittel zur Clan-Schließung, verworfen aus zwei unabhängigen Gründen:

1. **Falscher Anreiz.** Wer für das Verbinden zweier Cluster belohnt wird, hat ein Interesse
   daran, dass die Cluster getrennt *bleiben* (Burt, *structural holes* / *tertius gaudens*).
   Der Mechanismus prämiert im Gleichgewicht Fragmentierung.
2. **Sybil-anfällig.** Betweenness ist trivial fälschbar: Pseudo-Cluster erzeugen, sich als
   einzige Verbindung dorthin setzen, Prämie für eine Brücke ins Nichts kassieren. Max-Flow ist
   gegen genau diesen Angriff bewiesen robust; Betweenness ist es nicht.

**Das Problem löst D1/D3 besser:** Ein billiger Probe-Vouch (`w = 0.05`) macht Onboarding wieder
attraktiv. Anreiz an der Eintrittsschwelle statt Prämie für Vermittler.

### D24 — Beobachtungskennzahlen: Unabhängigkeit und Ersetzbarkeit

**Korrigierte Fassung.** Die ursprünglich vorgeschlagene Konzentrationsmetrik (Flussanteil der
Top-`k`-Knoten, Min-Cut Seed↔Mitgliedschaft) behandelte Konzentration als Pathologie. Sie kann
nicht zwischen drei vereinnahmten Engpässen und drei Menschen unterscheiden, denen tausend
andere unabhängig vertrauen — sie schlägt bei Kaperung und bei Exzellenz gleichermaßen an.

Stattdessen zwei Zahlen, beide auf dem eigenen Teilgraphen, ohne globale Sicht:

- **Quellenunabhängigkeit:** Sind die Bürgen von `X` untereinander pfad-disjunkt zum Seed?
  Tausend Bürgen aus einem Cluster sind ein Bürge; tausend aus disjunkten Regionen sind echte
  Mehrfachbestätigung. Derselbe Solver wie D19.
- **Ersetzbarkeit:** Ist `X` ein Schnittknoten — bricht der Fluss zur Peripherie zusammen, wenn
  `X` entfällt?

**Interpretation:** Hohe Stellung aus vielen unabhängigen Quellen bei vorhandenen
Alternativpfaden ist Leistung — verdient und jederzeit bestreitbar. Hohe Stellung aus einer
Quelle ohne Alternative ist ein Kaperungsziel, unabhängig von der Verdienstlage der Person.

Kein Protokollzwang, keine Schwelle. Eine Zahl, die jeder selbst rechnet (L2).

---

## C. Sanktionsmechanik (Layer 05)

### D11 — Sanktionsschwere ∝ Standing, beschränkt monoton

```
severity = base · f(standing)
f = 1 + c · min(t_s / t_ref, m)        c, m, t_ref = Policy
```

Reputation ist ein **Versprechen, kein Puffer**: Wer hohes Standing hat, hat viel versprochen,
der Bruch wiegt schwerer. Empirisch gestützt (Drittparteien sanktionieren hochstatus-Akteure
härter, wenn sie nach öffentlichem Kooperationsbekenntnis defektieren; Statustyp moderiert:
dominanzbasiert härter als prestigebasiert).

**Deckelung `m` ist konstitutiv, nicht kosmetisch.** Ohne sie entsteht ein neuer Fehlanreiz:
Standing zu *vermeiden* — unauffällig bleiben, nicht bürgen, keine Verantwortung übernehmen.
Kalibrierungsbedingung zum Policy-Knopf:

```
∂Nutzen/∂Standing  >  ∂Sanktionserwartung/∂Standing
```

Ein Nukleus, der sie verletzt, züchtet Duckmäuser — und soll das sehen können.

Zweitwirkung im Kontext von D25/D26: Für den Leistungsträger ist ein erwiesener Bruch teurer als
für jeden anderen. Das ist der Preis dafür, sich beeinflussen zu lassen, und er steigt mit dem,
was die Person zum lohnenden Ziel macht.

### D12 — Beta-Update multiplikativ **und** additiv

```
α ← α · (1 − k_slash)     # entfernt den Puffer
β ← β + 1                 # erhält die Rückfälligkeits-Akkumulation
```

**Der Defekt:** Mit `E = (α+1)/(α+β+2)` gilt `∂E/∂β ≈ −(α+1)/(α+β+2)²`. Der marginale Schaden
eines Fehltritts fällt **quadratisch** mit der Kontogröße — ein tausendfach bewährter Akteur
zahlt einen Bruchteil dessen, was ein Neuling zahlt. Falsche Richtung, nicht bloß falsche
Kalibrierung.

Nur die erste Zeile würde `05 §4` („Cure-Kosten steigen mit Rückfälligkeit") zerstören, weil `β`
die Historie trägt. Beide zusammen sind die richtige Asymmetrie.

**Kalibrierungshinweis zu `k_slash`:** konservativ (niedrig) ansetzen. Begründung → Abschnitt F.

---

## D. Macht, Rotation und Nachvollziehbarkeit (Layer 00/04/06)

### D13 — Mitgliedschaft und Ressourcen-Scope trennen

`grant-membership` darf **nicht** automatisch Zugang zu gepoolten Ressourcen bedeuten.
Zwei getrennte Claims ⇒ ein Nukleus kann offen aufnehmen **und** den Pool schützen.

**Begründung:** Offene Aufnahme wird nicht per se instabil, sondern erst in Kopplung mit
gepooltem Ressourcenzugang — dann trägt der Eintretende keine Eintrittskosten, zieht aber aus
gemeinsamem Bestand. Ostroms Design-Prinzipien sagen dasselbe: klare Grenzen sind für
*Common-Pool-Ressourcen* konstitutiv, nicht für Assoziation überhaupt.

### D21 — Losverfahren und Amtszeitbegrenzung als Nukleus-Policy

Gegen gezielte Unterwanderung wirksam, weil der Angreifer nicht weiß, wen er unterwandern muss.
**Lokal gezogen:** Jeder Verifizierer lost aus seiner eigenen berechtigten Menge mit eigener
Zufälligkeit. Kein globaler Randomness-Beacon, kein Konsens — und weil verschiedene Beobachter
verschieden ziehen, kann der Angreifer nicht einmal die Zielmenge bestimmen. Die
„nie global"-Invariante ist hier Verstärker, nicht Hindernis.

Amtszeitbegrenzung fast gratis: `t_exp` existiert, muss nur auf Mandate und Ämter angewandt
werden.

**⚠️ Nicht ohne D23 anwenden** (siehe dort).

### D23 — Rotation gilt der persistenten Schicht, nicht nur den Ämtern

**Warnung aus der Forschung:** Amtszeitbegrenzung allein verschiebt Macht in die persistente
Schicht. Polsby (1990) vor Kaliforniens Term-Limit-Initiative: Amtszeitbegrenzungen verschieben
Macht lediglich zu den unzugänglicheren Beamten und Einflussvermittlern im Umfeld. Bestätigt
durch Befragungen in Staaten mit und ohne Term Limits: Führungsfiguren in der Legislative
verloren Einfluss, Gouverneure, Stäbe und Verwaltungsapparate gewannen (Carey, Niemi, Powell
1998); Lobbyisten-Befragungen in fünf betroffenen Staaten fanden starken Konsens für dieselbe
Verschiebung. Mechanismus: Reduktion institutionellen Wissens stärkt die, die bleiben. Für
Sortition gilt das verschärft — wer zufällig ausgewählt wird, ist per Konstruktion unerfahren.

**Wo bei MaR Persistenz sitzt — drei Orte, nur einer ist ein Amt:**

1. **Nukleus-Seed `e_N`.** Wer im Ankerset steht, definiert die Linse für alle, die sie
   benutzen. Ohne Seed-Rotation ist jede Ämterrotation Kosmetik.
2. **Dienstbetreiber** (Zeitdienst, Validierungs-Nodes, `06 §5/§6`). Langlebig, alle hängen
   davon ab — strukturelle Macht ohne Amt.
3. **Positionale Kapazität.** `C(x) = C₀γ^d` verleiht Macht **ohne Amt**. Man kann jeden Posten
   rotieren, und dieselben Menschen bei `d = 1` halten weiterhin die strukturelle Kapazität.
   Amtszeitbegrenzung greift hier prinzipiell nicht.

**Beschluss:**

- **Seed und Dienst-Deklarationen tragen `t_exp` und müssen periodisch neu erklärt werden.**
  Ein Ankerset ist eine Erklärung, keine gewachsene Beziehung — rotierbar, ohne
  Vertrauenssemantik zu zerstören. Ablauf ohne Neuerklärung ⇒ sauberer Fallback auf `e_s`
  (`02 §6.3`). Das ist der eingebaute Sicherheitszustand, kein Ausnahmezustand.
- **Positionale Kapazität ist nicht rotierbar — nur messbar** (→ D24).
- **Einarbeitungslücke:** Wissen liegt in signierten, auditierbaren Claims, nicht in den Köpfen
  der Bleibenden. Ein ausgeloster Schiedsrichter liest die Verdikt-Historie seines Vorgängers
  (D15). Kein voller Ersatz für Erfahrung, aber genau der Vorsprung, den ein permanenter Apparat
  sonst monopolisiert.

### D25 — Ansehen und Torwächterschaft trennen (Policy-Default)

`t_s` trägt aktuell zwei verschiedene Dinge in einer Zahl:

- **Gehört-werden** — epistemische Autorität. **Nicht-rival:** Dass tausend Menschen einem guten
  Denker zuhören, nimmt niemandem etwas weg. Eine Obergrenze wäre Verschwendung.
- **Torwächterschaft** — wer wird aufgenommen, wer bekommt Zugang, wessen Bürgschaft trägt.
  **Rival und zwingend:** Was ich zulasse, müssen andere hinnehmen.

Nur die zweite Sorte ist ein lohnendes Unterwanderungsziel. Einen Denker zu bestechen bringt
wenig, wenn seine Argumente von jedem geprüft werden können. **Der Lobbyist kauft keine Ideen,
er kauft Entscheidungen.**

Mechanismus vorhanden: der **Zweck-Tag** (`02 §2`). Torwächter-Zwecke werden in eigenen Scopes
geführt; `Σw ≤ 1` bindet dann nur das Torwächter-Budget, nicht das Zuhören. Folge: **Ansehen
unbegrenzt, Torwächterschaft begrenzt.** Ungleiche Begabung darf sich ungleich auswirken, ohne
proportional Zugangsmacht zu erzeugen.

**Als Policy-Default, nicht als Invariante** (L1, L4): Die Referenz-Verfassung trennt, ein
Nukleus darf zusammenlegen — mit ausdrücklicher Warnung im Spec-Text. Ein Nukleus, der vermengt,
macht sich angreifbar; andere sehen an seiner Struktur, was daraus wird.

### D26 — Amtsführung in nachvollziehbarer Kette

**Das Problem ist nicht Macht, sondern Unnachvollziehbarkeit.** Was eine unantastbare Klasse
erzeugt, ist plausibles Abstreiten: dass nachträglich nicht rekonstruierbar ist, wer was auf
welcher Grundlage entschieden hat.

Primitiv dafür ist die **Autorenkette** (`h_prev`). Wer ein Amt bekleidet und Entscheidungen als
Claims signiert, erzeugt eine manipulationssichere Amtshistorie — nichts kann nachträglich
eingefügt, entfernt oder umdatiert werden, weil sonst die Kette bricht. Zwei widersprüchliche
Versionen derselben Kettenposition sind **Equivocation**: mechanisch slashbar, ohne Verdikt.
**„Das habe ich so nie gesagt" ist damit keine Verteidigung, sondern ein selbst-validierender
Beweis gegen den Sprecher.**

**Regel:** Eine Amts- oder Torwächter-Rolle wird per `obligation@1` angenommen; die Obligation
bindet daran, Entscheidungen im Scope als Claims in der eigenen Kette zu signieren. Bruch ist
dann kein subjektiver Vorwurf, sondern erwiesener Obligationsbruch über bestehende Mechanik.

> **VR-04.1 — Kettenlose Amtsführung trägt kein Vertrauen.** Ein Akteur, der eine Amts- oder
> Torwächter-Rolle innehat, ohne die zugehörige Kettenbindung eingegangen zu sein, wird für
> Entscheidungen in diesem Scope **nicht** als vertrauenswürdig gewertet.

Kein Verbot — die Bewertung fällt einfach aus. Dieselbe Bewegung wie „Neuling ≈ 0": kein
Sonderfall, nur die Abwesenheit von Grundlage.

**Zwei Sonderfälle:**

- **Lücken sind sichtbar, aber nicht beweisbar.** Wer eine Entscheidung gar nicht signiert,
  bricht die Kette nicht — er entscheidet außerhalb. Erkennbar nur, wenn die Wirkung sichtbar
  ist und der Claim fehlt („Abwesenheit von Evidenz ist keine Evidenz der Abwesenheit",
  `02 §7`). Was bleibt, ist Reputationswirkung.
- **Nachvollziehbarkeit ≠ Öffentlichkeit.** Eine Kette kann unmanipulierbar sein, während
  Inhalte erst später oder nur gegenüber einem Prüfgremium offengelegt werden.
  Verhandlungspositionen brauchen mitunter Vertraulichkeit *jetzt*, aber nie
  Unnachvollziehbarkeit *später*. Der Hash steht fest, bevor der Inhalt offen ist.

**Zweiseitigkeit:** Der Einflussnehmer hat selbst eine Identität. Ein erwiesener
Bestechungsversuch trifft sein Standing und seinen Bond — dieselbe Logik wie der Anklage-Stake
(`05 §5`). Beeinflussen wird ebenso riskant wie beeinflusst werden. Zusammen mit D11 (Preis
steigt mit Standing) und D5 (Bürgen verlieren mit, also Peer Monitoring dort, wo es am meisten
wert ist).

### D14 — Referenzimplementierung bleibt meinungsfrei

Die Referenzimplementierung implementiert **nur** Mechanismus und Policy-Knöpfe, ohne
Default-Meinung. Eine konkrete Wertvorstellung lebt als `example-nucleus.md` im Repo — klar als
*eine Instanz* gekennzeichnet, neben der später eine mit gegenteiligen Parametern stehen kann.

Andernfalls wird die Referenzimplementierung stillschweigend normativ, und jede abweichende
Implementierung wirkt wie eine Abweichung statt wie eine gleichberechtigte Variante.

### D15 — Verdikt-Historie auditierbar (`06`)

Kein neues Profil. Ein Schiedsrichter ist eine Identity mit `service-announce@1`; seine Verdikte
sind bereits Claims mit Autorenkette. Ergänzt wird der normative Satz:

> Wer als Schiedsrichter auftritt, dessen Verdikt-Historie MUSS abfragbar sein — sonst ist er
> nicht bewertbar.

Damit wird ein systematischer Milde-Bias gegenüber Angesehenen (*moral credentials*) nicht
verhindert, aber **beobachtbar und bepreisbar**: Verdikte reisen ohnehin als attribuierte
Meinungen, gewichtet mit dem Vertrauen des Beobachters in den Schiedsrichter (`05 §5`).

### D16 / D22 — Neue getragene Grenzen in `VISION §6`

1. **Reputationsgebundene Solidarität ist regressiv.** „Neuling ≈ 0" trifft Bedürftige und
   Angreifer identisch. Unglück korreliert negativ mit Standing (Krankheit, Pflege,
   kollabierende Region). `C(x) = C₀γ^d` verstärkt ererbte Netzwerkposition exponentiell.
   Historisches Vorbild mit dokumentierten Deckungslücken: Friendly Societies / Fraternal
   Societies (Beito, *From Mutual Aid to the Welfare State*) — Wandernde, chronisch Kranke,
   Konjunkturkrisen mit gleichzeitiger Anspruchsberechtigung (= korreliertes Risiko).
2. **Moral-Credentials-Residual.** Der Bias wirkt auf die Deutung mehrdeutigen Verhaltens, also
   vor der Signatur. Gegen einen nukleus-weit geteilten Bias hilft nur Exit. Kategorie:
   irreduzibler Orakel-Residual.
3. **Einzelabfragen verdünnen nicht** (→ D6/D7).
4. **Kollusion ist nicht Sybil** (→ D20). Gegen eine hinreichend große, geduldige, echt
   eingebettete Koalition hilft kein Protokoll. Die Mechanismen erhöhen die nötige
   Koalitionsgröße und machen die Vorbereitungszeit sichtbar — mehr ist nicht zu haben, und ein
   Protokoll, das mehr verspricht, lügt.
5. **D22 — Seed-Kompromittierung.** Wer `e_N` kompromittiert, kompromittiert jeden, der diese
   Linse benutzt. Der Fallback auf `e_s` (`02 §6.3`) ist **Eindämmung, keine Abwehr.**
6. **Restfenster bei Widerruf vor Defektion** (→ D17).
7. **Kettenlücken.** Entscheidungen außerhalb der Kette sind nicht beweisbar, nur auffällig
   (→ D26).

---

## E. Offene Lücken aus der Prüfung

**A — `t_exp` wird für Vouches verpflichtend.** `02 §6.2` formuliert `t_exp` als optional. Mit
D17 hängt die Budgetfreigabe daran: Ein Vouch ohne `t_exp` bindet Budget **für immer**. Also:
In Scopes mit `Σw ≤ 1` MUSS ein Vouch `t_exp` tragen, oder die Policy setzt eine Maximallaufzeit
als Default. Kein Fork, eine Lücke.

**B — Zwei Mengen, nicht eine.** Implementierungskritisch für `02a`:

| Menge | Inhalt | Verwendung |
|---|---|---|
| **Aktiv-Set** | nicht widerrufen, nicht abgelaufen | Kantensatz für den Fluss |
| **Budget-Set** | nicht abgelaufen (widerrufen **eingeschlossen**) | Prüfung `Σw ≤ 1` |

> **Korrigiert durch D38 und D40:** Das Budget-Set schließt `superseded` und `pending` ein
> und wird je `(I, J, N)` über `max n` aggregiert. Die Tabelle oben gibt den Stand vor der
> Golden-Anchor-Rechnung wieder.

Wer beides zusammenlegt, bekommt entweder ein Budget-Leck oder Phantomkanten im Graphen.

**C — Bootstrap-Enge.** `Σw ≤ 1` macht die Frühphase quantitativ eng: Drei Gründer haben
zusammen Budget 3; zwanzig frühe Mitglieder bedeuten `w ≈ 0.05`, also Kantenkapazität
`0.05·C₀`. Ob das über der Admission-Schwelle liegt, hängt jetzt von `C₀`, `γ` **und** der
Schwelle gemeinsam ab — die Knöpfe aus `02 §8` sind nicht mehr unabhängig kalibrierbar. Kein
Fehler, aber eine neue Nebenbedingung im Parameterraum; gehört als Warnung dorthin. Testbar über
ein Bootstrap-Szenario, das zeigt, ab wann eine Gruppe wachsen kann.

---

## F. Kalibrierungshinweis: `w`-Haftung konservativ ansetzen

Was hier gebaut wird, ist strukturell **Joint Liability Lending** (Grameen, ab 1976): Ein Kreis
haftet füreinander, weil er sich besser kennt als jede zentrale Instanz. Peer Screening plus
Peer Monitoring.

Der empirische Befund ist unbequem: Die Institutionen, die Joint Liability erfunden haben —
Grameen, BancoSol, ASA — sind davon abgerückt und auf individuelle Haftung umgestiegen; ein
MFI-Panel (MIX Market, 2008–2014) belegt den Trend. Die Umstellung ließ die Rückzahlungsquoten
**unverändert**. Beibehalten wurden dagegen die regelmäßigen Gruppentreffen. **Die Gruppe wirkt,
die formale Mithaftung kaum** — was trägt, ist wiederholte Interaktion und geteilte Information.

Dokumentierte Kosten:

- Klienten mögen die durch Gruppenhaftung erzeugte Spannung nicht; übermäßige Spannung unter
  Mitgliedern ist häufiger Grund für freiwillige Abwanderung. Übertragen: Der Nachbar, dessen
  `w` ich binde, ist nicht mehr nur Nachbar.
- Strategische Defektion: Kreditnehmer, die unter Einzelhaftung zurückgezahlt hätten,
  defektieren, wenn sie die Gesamtlast der Gruppe nicht tragen können — der Effekt rührt
  möglicherweise eher von Gruppendruck als von der Haftung selbst her. Kaskadenrisiko; `05 §6`
  deckelt es auf eine Sprunghöhe.

**Ableitung:** Die `w`-Haftung ist nicht falsch, aber wahrscheinlich **nicht der
Hauptmechanismus**. Der Hauptmechanismus ist Knappheit (`Σw ≤ 1`) plus Sichtbarkeit — dass
sorgfältig ausgewählt werden *muss* und andere sehen, wie ausgewählt wurde. Haftung ist der
Backstop für den Extremfall, nicht der Alltagsanreiz. Daher `k_slash` niedrig, mit Kommentar in
`example-nucleus.md`, der auf diesen Befund verweist — Kalibrierung begründet statt geraten.

Theoretischer Anker für `w` als solches: **Costly Signaling** (Zahavi; Gintis/Smith/Bowles) —
Glaubwürdigkeit erfordert Kosten. Ostroms Design-Prinzip 5 (abgestufte Sanktionen) ist über
`05 §3` bereits erfüllt.

---

## G. Änderungsliste pro Datei

| Datei | Änderung | Quelle |
|---|---|---|
| `02-trust-flow.md §1` | Leitsatz „Vertrauen ist Zustand, kein Vermögen"; keine Kapazitätsprämie | D10, D18 |
| `02-trust-flow.md §2` | Torwächter-Zwecke in eigenen Scopes (Policy-Default) | D25 |
| `02-trust-flow.md §3` | `w`-Obergrenze `⌊n·C(I)/D⌋`, Default `n=D`; `Σw ≤ 1` über dem Budget-Set | D1, D2, D3 |
| `02-trust-flow.md §4` | **Satz auf simultanen Fluss korrigieren**; Monotonie-Zusatz für `w`-Caps; Satz *Sybil ≠ Kollusion* | D6, D7, D1, D20 |
| `02-trust-flow.md §6.2` | `t_exp` für Vouches verpflichtend; Widerruf/Freigabe-Semantik | E-A, D17 |
| `02-trust-flow.md §8` | Policy-Knöpfe `D`, Budgetgrenze; VR-02.1; Pfad-Disjunktheit; Kennzahlen; Bootstrap-Warnung | D2, D7, D19, D24, E-C |
| `02-trust-flow.md §9` | Getragene Grenzen: Einzelabfrage, Kollusion, Widerruf-Restfenster | D6, D20, D17 |
| `01-claim-atom.md §7.1` | `v`-Payload Key `0: n` normativ, Key-Vergabe; Float-Vorschlag entfernt; `t_exp` in Budget-Scopes Pflicht | D37, E-A |
| `02-trust-flow.md §2` | eine Kante je `(I, J)`, `max n`; keine Kante ohne gültiges `n` | D40, D37 |
| `02-trust-flow.md §3` | `⌊·⌋` bei `C`; BFS über `E⁺`; Ankerset und Super-Source an `a_in` | D28, D31, D36 |
| `02-trust-flow.md §3.1` | Aggregation je `(I,J,N)`; Out-Degree aus Budget; Budget-Set inkl. `superseded`; ungültiges `n` | D40, D33, D38, D37 |
| `02-trust-flow.md §4` | Definition auf `s_in`; Super-Sink an `T_in`; schärfere Schranke; zwei Divergenzursachen; Angriffsform | D31, D30 |
| `02-trust-flow.md §8` | `C₀` nicht verhältniserhaltend; `D` scope-fest + SHOULD `≥ C₀`, keine Kurzform; Granularitätsboden; Bootstrap-Ungleichungen; `r_max`; knoten-disjunkt mit Endpunkt-Regel; `include_flagged` | D28, D32–D35, D39 |
| Repo-Wurzel | `02-golden-anchors.md` aufnehmen | J |
| `02-trust-flow.md §3.1` | Budget-Austritt als `t_exp`-Prädikat, nicht als Zustand | D41 |
| `02-trust-flow.md §8` | Vouch-Kanten im Disjunktheitslauf tragen `1`, nicht ∞ | D42 |
| `02-golden-anchors.md §8` | INV-2 als Schranke; INV-8 verengt | D42, D44 |
| Repo-Wurzel | `02a-abnahme.md` aufnehmen | D41–D44 |
| `05-enforcement.md §1` | Beta-Update multiplikativ + additiv | D12 |
| `05-enforcement.md §3` | Über-Commitment ⇒ direkt Stufe 3 (wie Equivocation) | D4 |
| `05-enforcement.md §4` | `severity = base · f(standing)`, Deckelung, Kalibrierungsbedingung | D11 |
| `05-enforcement.md §6` | Sprunghöhe = `w · Schaden`; nur bei selbst-validierenden Beweisen | D5, D5a |
| `06-services.md` | Verdikt-Historie MUSS abfragbar sein; Dienst-Deklarationen mit `t_exp` | D15, D23 |
| `04-governance.md` | Losverfahren + Amtszeitbegrenzung als Policy; VR-04.1; `obligation@1` für Amtsannahme | D21, D23, D26 |
| `00-…-constitution.md` | Mitgliedschaft ≠ Ressourcen-Scope; Seed mit `t_exp` | D13, D23 |
| `VISION.md §6` | Sieben getragene Grenzen | D16, D22 |
| Repo-Wurzel | `example-nucleus.md` anlegen; `k_slash` niedrig, mit Begründung | D14, F |

---

## H. Konsequenzen für die Implementierung

**Golden Anchors neu rechnen.** D6/D7 betreffen unmittelbar die aggregate Sybil-Schranke und die
`|S|`-Unabhängigkeit. Für den kanonischen Testgraphen (ALICE-Seed, Kette ALICE→BOB→CAROL, drei
parallele Sybil-Kanten von CAROL, EVE unerreichbar) werden gebraucht:

1. `trust(s→gᵢ)` **pro Ziel einzeln**
2. **simultan** über `{g₁, g₂, g₃}` (Multi-Sink)
3. Differenz aus 1 und 2 als **Testvektor für VR-02.1**
4. `w`-Varianten neben den `w = 1`-Fällen
5. Budget-Fall mit widerrufenem-aber-nicht-abgelaufenem Vouch (prüft E-B)
6. Einheitskapazitäts-Lauf für Pfad-Disjunktheit (D19/D24)
7. Bootstrap-Szenario: ab wann wächst eine Gruppe unter `Σw ≤ 1`? (E-C)

**`w`-Caps sind additiv.** Bei `n = D` ist das Verhalten identisch zum bisherigen Stand — die
bestehenden Testvektoren bleiben gültig und bekommen `w`-Varianten als Ergänzung.

**Reihenfolge — Spec vor Prompt.** `02 §4` enthält aktuell einen falschen Satz. Ein Prompt gegen
eine fehlerhafte Spec produziert fehlerhafte Tests. Also: Spec-Nachzug (Änderungsliste G,
Layer 02) → Golden Anchors → `02a-maxflow` → `02b-pagerank` → Layer 03.

**Umfang `02a-maxflow`:** Dinic, Knoten-Splitting, `w`-Caps in exakter Rational-Arithmetik,
`Σw`-Prüfung über dem Budget-Set, Multi-Sink-Pfad, Einheitskapazitäts-Pfad für
Disjunktheitszählung, Über-Commitment-Erkennung als Fehlerklasse.

**`02b-pagerank` unverändert** — die Relaxation war nie kapazitätstragend (`02 §5`) und bleibt
für harte Entscheidungen verboten.

---

## I. Nicht entschieden

- Ist `Σw > 1` im Sinne von `05 §4` terminal oder kurierbar? (Policy, vor Merge)
- Konkrete Werte für `c`, `m`, `t_ref` (D11), `k_slash` (D12), `D` (D2) — gehören in
  `example-nucleus.md`, nicht in die Spec.
- Erneuerungsintervall für Seed und Dienst-Deklarationen (D23).
- `D` (D2) ist für den `example-nucleus` auf **100** festgelegt, damit TV1 byte-identisch
  bleibt und `n` sich als Prozent liest. `C₀ ≤ 100` folgt aus D34. Die konkreten Werte für
  `c`, `m`, `t_ref`, `k_slash` bleiben offen.

---

## J. Aus der Golden-Anchor-Rechnung (Layer 01/02)

Sieben Ankerwerte wurden von Hand gerechnet, dann gegengerechnet. Die Rechnung hat acht
Definitionslücken freigelegt, die keiner der Spec-Durchgänge gefunden hat — weil sie erst sichtbar
werden, wenn man eine Zahl produzieren muss. Zwei davon fielen erst beim **zweiten** Durchgang,
als die Zahlen gegen die Prosa geprüft wurden, die sie belegen sollte. Das ist der Ertrag von
„Golden Numbers vor Prompt".

### D28 — `C(x)` wird abgerundet, einmal am Ende

```
C(d) = ⌊ C₀ · γ^d ⌋        γ = γ_num / γ_den, exakt rational
     = (C₀ · γ_num^d) // γ_den^d
```

`§3` schrieb `C(x) = C₀·γ^d` ohne Rundung, während `§3.1` nur die Kantenkapazität rundet. Bei
`γ = ½, C₀ = 16` divergiert das ab `d = 5` (`½` gegen `0`).

**Einmal am Ende, nicht pro Schritt.** Bei `γ = ⅔, C₀ = 16, d = 2` ist das `7`, iterativ gerundet
wäre es `6`. Iteratives Runden macht das Ergebnis von der Auswertungsreihenfolge abhängig.

Folge: alle Kapazitäten sind `int`, der gesamte Solver rechnet ganzzahlig.

**Verworfen:** exakte Rationale für `C` (zwingt `Fraction` in den Fluss und damit gebrochene
Flusswerte, ohne dass irgendeine Aussage davon profitiert).

### D29 — Budgetprüfung ist eine Integer-Summe

```
Σw ≤ 1   ⟺   Σn ≤ D
```

Weil `D` scope-fest ist (D35), teilen alle `w` eines Scopes denselben Nenner. Die Prüfung braucht
keine Rationalarithmetik. Zusammen mit D28: **kein `Fraction`, kein `decimal`, kein `float` in der
gesamten harten Sicht.**

### D30 — Super-Sink hängt an `T_in`

`§4` sagt „∞-Kanten von jedem `g ∈ S`" — nach Knoten-Splitting mehrdeutig. Normativ:
`gᵢ_in → T*`. Konsistent zur Einzelabfrage; bei `gᵢ_out` zählte die interne Kante des Ziels mit
und die Multi-Sink-Semantik wiche von der Einzelabfrage ab.

### D31 — Super-Source hängt an `a_in` ⚠️

`§6.3` kennt ein Anker**set**, `§3`/`§4` sprechen durchgehend von einem einzelnen `s`. Normativ:
`S* → a_in` mit ∞ für jeden Anker `a`, und `d(x) = min_a d(a,x)`. Die Definition in `§4` lautet
damit `trust(s → T) = maxflow(s_in → T_in)`.

**Warum `a_in` und nicht `a_out`.** Die zuerst gewählte Fassung `a_out` — begründet mit der
Gleichheit zur bestehenden `s_out`-Konvention — bricht den Satz aus `§4`. Sie umgeht die interne
Kante des Ankers, also genau die Kapazität, über die der Beweis argumentiert. Gegenbeispiel
(Anker A′): ein Anker mit `C₀ = 16, D = 4` bürgt für drei Sybils mit je `n = 4`; die Kanten tragen
je `⌊4·16/4⌋ = 16`, der simultane Fluss ist **48** gegen eine behauptete Schranke von
`Σ_h C(h) = 16`.

Bei gültigem Budget sind beide Fassungen identisch, weil `Σ_e cap(e) ≤ C(a)` gilt. Sie
unterscheiden sich **genau dann**, wenn der Anker über-committet ist — und dort ist `a_in` die
sichere Richtung. Der Preis ist nominell: die Definition liest `s_in` statt `s_out`. Der Ertrag
ist ein **unbedingter** Satz, der auch gegen einen kompromittierten Anker trägt.

Nebenwirkung, ins Positive korrigiert: `C₀` bindet damit auf der Quellseite direkt. Die
Bootstrap-Ungleichung `θ ≤ f·C₀/M` ist dadurch tatsächlich eine Kapazitätsaussage; unter `a_out`
folgte sie aus der Budgetregel und das Etikett „Kapazitätsbedingung" war falsch.

**Kein Ankerwert von `TP-02` ändert sich** — ALICE ist budgetgültig, `cap(ALICE→BOB) = 16 = C₀`.

### D32 — Der Einheitskapazitäts-Lauf ist knoten-disjunkt, Endpunkte ungespalten

`§8` sagt „derselbe Max-Flow mit Einheitskapazitäten", D19 sagt „knoten-disjunkte Pfade". Beides
zusammen ist unterbestimmt. Normativ: **interne Kanten `= 1`, Vouch-Kanten `= ∞`.** Kantendisjunkt
wäre die falsche Größe — zwei Pfade durch denselben Bürgen sind ein Bürge.

**Endpunkte werden nicht gespalten:** die internen Kanten der Anker tragen `∞`; die des Ziels
liegt wegen D30 ohnehin nicht auf dem Pfad. Knoten-Disjunktheit zählt *Zwischen*knoten. Ohne diese
Ausnahme wäre jede Disjunktheitszahl von einem einzelnen Anker aus trivial `1` — die interne
Kante der Quelle läge auf jedem Pfad —, und die Kennzahl aus D24 wäre wertlos.

Damit unterscheidet sich der Einheitslauf in zwei Punkten vom Kapazitätslauf (Belegung **und**
Quellanbindung). Beide teilen Topologie und Indizes; getauscht werden nur die Kapazitätsvektoren.

### D33 — `D` ist zugleich der Out-Degree-Cap

Aus `n ∈ [1,D]` ganzzahlig und `Σn ≤ D` folgt: **höchstens `D` gleichzeitig bebürgte Subjekte pro
Identität und Scope** — gezählt werden Subjekte, nicht Claims (D40), und nur solche im Budget-Set.
Aus `cap ≥ 1 ⟺ n·C(I) ≥ D` folgt schärfer:

```
wirksame Out-Degree(I)  ≤  min( D , C(I) )
```

D3 hatte den Out-Degree-Cap `k` als „willkürliche Rationierung" verworfen. Die Granularität führt
ihn wieder ein — aber in der richtigen Form: **bei `D ≥ C₀` (D34) bindet `C(I)`, und damit ist die
Grenze positional statt gezählt.** Deine Out-Degree ist deine Kapazität. Der Einwand aus D3 ist
damit nicht umgangen, sondern erfüllt.

### D34 — `D ≥ C₀` als SHOULD, nicht MUST

Bei `D < C(I)` bindet `D` statt der Position — genau die willkürliche Rationierung aus D3. Ein
Produktivnukleus SOLL daher `D ≥ C₀` setzen.

**Kein MUST**, weil das Testprofil `TP-02` (`D = 4 < C₀ = 16`) genau das Regime prüft, in dem der
Out-Degree-Cap bindet. Ein MUST machte den eigenen Testgraphen illegal.

**Keine Kurzform.** Die Fassung „bei `D = C₀` vereinfacht sich `cap` zu `⌊n·γ^{d(I)}⌋`" ist
**falsch** und ist gestrichen. `cap = ⌊ n·⌊C₀γ^d⌋ / D ⌋` ist doppelt gerundet und lässt sich nur
zusammenziehen, wenn `C₀γ^d` ganzzahlig ist. Gegenbeispiel `C₀ = D = 16, γ = ⅔, d = 2, n = 9`:
`C = 7`, `cap = ⌊63/16⌋ = 3`, die Kurzform sagt `⌊4⌋ = 4`. Eine Implementierung, die abkürzt,
divergiert bei jedem nicht-dyadischen `γ`.

### D35 — `D` ist über die Lebensdauer eines Scopes unveränderlich

`n` steht im signierten Claim, `D` in der Policy. Änderte ein Nukleus `D`, würden **alle
bestehenden Vouches still umbewertet** (aus `w = 1` würde `w = 1/6`) und jede `Σn ≤ D`-Prüfung
kippte rückwirkend. Das ist keine Kalibrierung, sondern eine unbemerkte Neuinterpretation
signierter Aussagen.

Normativ: **ein anderes `D` bedeutet einen neuen Scope.** Passt zur Scope-Partition aus `§2` und
präzisiert D2 („nukleus-fest") — ein Nukleus mit getrennten Torwächter-Scopes (D25) darf je Scope
ein eigenes `D` führen, innerhalb eines Scopes nie.

**Verworfen:** `D` im Claim mitführen — bringt gemischte Nenner in die Budgetprüfung und damit
die Rationalarithmetik zurück, die D29 gerade beseitigt.

### D36 — Die BFS läuft über dem wirksamen Kantenset

```
E⁺ = { e ∈ Aktiv-Set : cap(e) ≥ 1 }
d(s,x) = kürzeste Pfadlänge über E⁺
```

`§3` definierte `d` über `E`, kapazitätsblind. Eine Kante mit `cap = 0` verkürzte damit die
Distanz und schenkte dem Ziel positionale Kapazität, ohne je Fluss zu tragen.

**Der bindende Grund ist der Disjunktheitslauf (D32).** Dort tragen alle Vouch-Kanten `∞`; eine
`cap = 0`-Kante ist von einer vollwertigen nicht mehr unterscheidbar. Ohne Filter wäre die
Quellenunabhängigkeit aus D24 mit subgranularen Vouches gratis fälschbar: unter `TP-BOOT`
(`C₀ = 16, D = 24`) erzeugen drei Kolludierende bei `d = 2` mit je `n = 1` drei knoten-disjunkte
Pfade auf ein gemeinsames Ziel, deren Vertrauensfluss exakt null ist (`⌊1·4/24⌋ = 0`).

**Keine Zirkularität:** `cap(I→J)` hängt nur von `d(I)` ab, und `d(I)` steht fest, wenn die BFS
`I` expandiert. Ein Durchlauf, `O(V+E)`.

**Zum Einwand „ein Vouch ist eine soziale Aussage, die auch ohne Durchsatz Position verleihen
sollte":** dann ist es kein Vouch. D5 — ein Parameter, drei gleichgerichtete Wirkungen, die
Deklaration ist der Einsatz. Ein gratis übertragbarer Positionskanal neben dem teuren wäre genau
die Ressource, die D20 als knapp identifiziert. Wer Bekanntschaft ohne Kapazitätsgewährung
ausdrücken will, braucht ein eigenes Prädikat, das in `§2` gar nicht erst als Kante zählt.

### D37 — `v`-Payload für `vouch@1` festgelegt

`01 §7.1` schlug `{ weight ∈ [0,1], … }` vor — ein **Float**, gegen `01 §3` Regel 6 („keine
Floats") und gegen die Integer-Arithmetik aus D28/D29. Der Vorschlag stammt aus der Zeit vor
D1/D2 und wurde nie nachgezogen.

```
v = { 0: n, … }     n : uint,  1 ≤ n ≤ D
v abwesend          ⇒  n = D   (w = 1, Default nach 02 §3.1)
```

**Geprüft wird Key `0`, nicht die Map als Ganzes.** Weitere Keys sind zulässig und für das Atom
opak — `§2` liest einen Zweck-Tag aus `v`, `§6.1` nennt `v.bond_ref`. Eine strikte Lesart
(„`v` muss exakt `{0: uint}` sein") hätte beide getötet. Reserviert: `0` = `n` (normativ),
`1` = Zweck-Tag, `2` = `bond_ref`; deren Kodierung wird mit `03`/`05` festgelegt und trägt bis
dahin keinen Testvektor.

| Fall | Kante | Budget-Beitrag |
|---|---|---|
| `n = 0` oder `n > D` | verworfen | **keiner** |
| `v` keine CBOR-Map, Key `0` fehlt oder ist kein `uint` | verworfen | **keiner** |

**Kein Budget-Beitrag bei unlesbarem `n`.** Eine geratene Zahl könnte eine Falschbeschuldigung
wegen Über-Commitment erzeugen. D3: Teilwissen erzeugt Unter-Erkennung, nie Falschbeschuldigung.
Die Kante fällt weg, weil das Unter-Vertrauen ist. Beides ist die sichere Richtung, in
verschiedene Richtungen.

**TV1 bleibt byte-identisch.** Sein `v = h'a1001864'` ist `{0: 100}`; mit `D = 100` im
`example-nucleus` ist das exakt `n = D`, also der Default `w = 1`. Alle Layer-01-Testvektoren
bleiben gültig, und `n` liest sich nebenbei als Prozent.

### D38 — Nur `t_exp` gibt Budget frei ⚠️

E-B und `§3.1` definieren das Budget-Set als „nicht abgelaufen, widerrufen eingeschlossen". Über
`superseded` schweigen beide — und der Referenz-Verifizierer liefert für Widerruf und Supersede
denselben `trust_usable = False`.

**Der Angriff:** Ein Bürge setzt `n = D` mit zehn Jahren Laufzeit (maximales Signal, gebundenes
Kapital), supersediert den Vouch per `core/supersede@1` und hat das Budget sofort zurück. Beliebig
oft. Damit ist `t_exp` als ökonomische Entscheidung (D17) wertlos: man wählt immer die längste
Laufzeit und rotiert per Supersede.

Normativ:

> Das **Budget-Set** enthält alle nicht abgelaufenen Vouches — **widerrufen, supersediert und
> `pending` eingeschlossen** —, aggregiert je `(I, J, N)` nach D40. Eine Gruppe verlässt das
> Budget-Set erst, wenn **alle** ihre Mitglieder abgelaufen sind. **Kein selbst-bezüglicher
> Lebenszyklus-Akt gibt Budget frei — Budget folgt der Uhr, nicht dem Willen des Autors.**

Der letzte Satz ist die eigentliche Regel; er schließt jeden künftigen Lifecycle-Akt mit ein.
Ohne D40 wäre er zu scharf: er machte jede Erneuerung zur Straftat gegen sich selbst.

### D39 — Geflaggte Autoren: Policy, nicht Metrik

`01 §4` sagt, Equivocation invalidiert Downstream nicht rückwirkend. Ob ein geflaggter Bürge
Fluss trägt, ist damit Policy und gehört nicht in die Metrik. Normativ: ein Parameter
`include_flagged`, Default **`False`** (sichere Richtung). Gilt für `equivocation-flagged` und
für Über-Commitment.

**Das Budget-Set ist davon unberührt** — ein Flag darf die Budgetrechnung nie ändern, sonst
verschöbe eine Erkennung rückwirkend die Erkennungsgrundlage.

### D40 — Aggregation je `(I, J, N)` über `max n` ⚠️

```
Gruppe(I, J, N) = alle vouch@1-Claims von I auf J im Scope N
n_budget = max n über die Gruppenmitglieder im Budget-Set   (0, wenn leer)
n_kante  = max n über die Gruppenmitglieder im Aktiv-Set     (0 ⇒ keine Kante)

Budget:  Σ_J n_budget(I, J, N)  ≤  D
Kante:   cap(I→J) = ⌊ n_kante · C(I) / D ⌋
```

Weil Aktiv-Set ⊆ Budget-Set gilt, ist stets `n_kante ≤ n_budget`.

**Der Befund.** D38 (Budget-Set inkl. `superseded`, Freigabe nur bei `t_exp`) zusammen mit D4
(Über-Commitment ist selbst-validierend, `05 §3` Stufe 3, mechanischer Slash ohne Verdikt) machte
die gewöhnliche Erneuerung eines Vouch zu einem signierten Beweis gegen den eigenen Autor: wer
`n = D` mit langer Laufzeit setzt und den Claim später ersetzt, hat `Σn = 2D > D`. Auch beim
**Herabsetzen** von `n`. Der Angriff aus D38 ist real, die Regel in Summenform bestrafte aber
jede Korrektur bis `t_exp` — und zwar in derselben Klasse wie Equivocation.

**Warum Gruppierung und nicht Supersede-Kette.** Layer 01 verlinkt den Nachfolger nicht mit dem
Vorgänger: `core/supersede@1` zeigt gezielt auf ein Ziel (`J = [claim-ref, ziel.claim_id]`,
`01 §5.3`), trägt aber keinen Ersatz-Claim. Eine Ketten-Semantik verlangte eine Layer-01-Änderung.
Gruppierung nach `(Autor, Subjekt, Scope)` ist rein lokal, `O(|E|)` und lässt Layer 01
unangetastet.

Vier Wirkungen:

- **Erneuerung und Herabstufung sind frei.** Ein Autor kann seine Aussage jederzeit korrigieren;
  er kann nur ihr Gewicht nicht vorzeitig anderswo einsetzen.
- **Der D38-Angriff bleibt tot.** Das Gruppenmaximum steht bis `t_exp`. Ein Vouch auf ein
  *anderes* Subjekt ist eine andere Gruppe und kostet volles Budget.
- **Fluss folgt dem Willen, Budget folgt der Uhr.** Eine Herabstufung wirkt sofort über
  `n_kante`, nie über `n_budget`. Das ist die Trennung, die D38 behauptet, sauber durchgezogen.
- **Schließt eine bestehende Lücke.** `§2` erzeugte eine Kante *je Claim*, also parallele Kanten
  mit addierten Kapazitäten: zwei aktive Vouches auf dasselbe Subjekt kosteten einfaches Budget
  und trugen doppelte Kapazität. `max` statt Summe beseitigt das.

Teilwissen bleibt sicher: fehlende Claims senken beide Maxima ⇒ Unter-Erkennung, nie
Falschbeschuldigung (D3).

**Verworfen:** Trennung von Ausstellungssperre und slashbarer Klasse (Budget über dem
Budget-Set, Beweis nur über dem Aktiv-Set). Das repariert die Erneuerung ebenfalls, öffnet aber
die Umgehung aus `§3.1`: ein Autor hält Vorgänger zurück oder widerruft reihum und hält seine
aktive Menge stets klein.

### D41 — Budget-Austritt ist ein `t_exp`-Prädikat, kein Zustand

Der `02a`-Prompt verkürzte den Austritt aus dem Budget-Set auf `state == EXPIRED`. Das ist falsch,
und die Spec sagt bereits das Richtige: `02 §3.1` definiert das Budget-Set als „nicht abgelaufen
(widerrufen, supersediert und `pending` eingeschlossen)". **„Nicht abgelaufen" ist ein Prädikat
über `t_exp` und `now`, kein Zustand der Layer-01-Zustandsmaschine.**

Der Fehler war folgenreich, weil `classify()` `REVOKED`/`SUPERSEDED`/`PENDING` **vor** der
Ablaufprüfung entscheidet. Ein einmal widerrufener Claim erreicht `EXPIRED` daher nie. Unter der
Prompt-Fassung bände ein widerrufener Vouch **für immer** Budget — kein konservatives Verhalten,
sondern ein Deadlock: der Autor bekäme die Kapazität nie zurück, und Anker 5 Schritt S2 wäre
unerreichbar.

Normativ:

```
im Budget-Set  ⟺  state ∈ {ACTIVE, REVOKED, SUPERSEDED, PENDING}
                  UND (t_exp fehlt ODER now ≤ t_exp)
```

Die Ablaufbedingung wird **unabhängig vom Layer-01-State** geprüft. Die Grenzkonvention ist
`now ≤ t_exp` und stimmt mit dem Verifizierer überein — gleiche Konvention, zwei
Auswertungsstellen. Das ist der Preis dafür, dass Layer 01 eingefroren ist; die Kopplung ist
dokumentiert und getestet, aber sie ist eine Kopplung. Ändert Layer 01 je seine Ablaufkonvention,
muss Layer 02 mitgezogen werden.

### D42 — Vouch-Kanten tragen im Disjunktheitslauf Kapazität 1, nicht ∞ ⚠️

Korrigiert D32. Die dortige Belegung „interne Kanten `1`, Vouch-Kanten `∞`" ist **defekt**, aus
zwei unabhängigen Gründen.

**Der Sentinel ist nicht wohldefiniert.** `INF = Σ(endliche Kapazitäten) + 1` war gegen den
Kapazitätslauf definiert. Im Einheitslauf sind die Vouch-Kanten selbst die ∞-Kanten; „Summe der
endlichen" ist dort zirkulär.

**Ohne Zwischenknoten degeneriert jeder Pfad.** Anker intern ∞ (D31/D32), Vouch-Kante ∞, Ziel
intern wegen D30 nicht auf dem Pfad — jede Kante des Pfades trägt ∞, und der Solver liefert den
Sentinel statt einer Pfadzahl. In `TP-BOOT` bürgen die Gründer **direkt** für die Neulinge; es
gibt keinen Zwischenknoten. Gemessen wurden 219 statt 1. In `TP-02` fällt es nicht auf, weil BOB
und CAROL dazwischenliegen — die Konvention wurde an einem Graphen entworfen, der den Fehler
nicht zeigen kann, und `TP-BOOT` stand mit seiner Disjunktheitsspalte daneben, ohne dass der
Widerspruch auffiel.

Normativ:

| Lauf | interne Kanten | interne Kanten der Anker | Vouch-Kanten |
|---|---|---|---|
| Fluss | `C(d(x))` | `C(0)` wie alle | `⌊n_kante·C(I)/D⌋` |
| Disjunktheit | `1` | `INF` | **`1`** |

**Die Änderung ist beweisbar verlustfrei.** Zwei knotendisjunkte Pfade teilen nie eine Kante —
teilten sie `I→J`, teilten sie die Knoten `I` und `J`. In jedem knotendisjunkten Pfadsystem trägt
also jede Kante höchstens eine Einheit. Die Kappung entfernt kein gültiges Pfadsystem und lässt
keines zusätzlich zu. Sie ist äquivalent, wo ∞ wohldefiniert war, und wohldefiniert, wo ∞ es
nicht war. Wegen D40 existiert ohnehin nur eine Kante je Paar, es entsteht keine
Aggregationsfrage.

Die Endpunkt-Regel aus D32 bleibt unberührt: die internen Kanten der Anker tragen weiterhin
`INF`. `TP-FAN` prüft, dass die Kappung sie nicht mitgekappt hat.

### D43 — Equivocation ist global, Über-Commitment ist scope-gebunden

D39 nennt zwei Flags, ohne ihren Geltungsbereich zu klären. Sie unterscheiden sich, und zwar
zwingend:

- **Equivocation** ist eine Aussage über die **Hash-Kette einer Identität** — zwei Claims mit
  demselben `h_prev`. Die Kette ist scope-übergreifend, also ist der Befund es auch. Ein Autor,
  der in *irgendeinem* Scope äquivoziert, hat seine Kette gebrochen; das ist keine Eigenschaft
  eines Scopes.
- **Über-Commitment** ist `Σ n_budget ≤ D` je Scope, und `D` ist scope-fest (D35). Der Befund
  kann gar nicht anders als scope-gebunden sein.

Normativ: bei `include_flagged = False` trägt keine Kante eines Autors, der (a) in irgendeinem
Scope `equivocation-flagged` ist **oder** (b) im **abgefragten** Scope über-committet ist. Das
Budget-Set bleibt in beiden Fällen unberührt (D39).

### D44 — Subgranularität gilt nur für erreichbare Autoren

Ein Befund „Kante ohne Durchsatz" entsteht genau dann, wenn ein Autor mit `d(I) < ∞` eine Gruppe
mit `n_kante ≥ 1` trägt, deren Kapazität `⌊n_kante·C(I)/D⌋` null ist.

Bei `C(I) = 0` wegen **Unerreichbarkeit** ist die Ursache nicht Granularität, sondern Position.
Ein Subgranularitäts-Befund wäre dort eine Falschaussage über die Ursache und würde bei jeder
Abfrage für jeden nicht erreichten Teil des Stores feuern — Rauschen proportional zur
Store-Größe statt einer Aussage über den ausgewerteten Graphen.

Folge für D39: Der Befund ist damit **flag-abhängig**. Fällt die Kante eines geflaggten Autors
weg, verschlechtern sich stromabwärts die Distanzen, sinken die Kapazitäten, und Kanten rutschen
unter die Granularitätsgrenze. Das ist konstruktiv so — die Budgetbefunde bleiben flag-invariant,
der Subgranularitätsbefund nicht.

### D45 — `P` ist sub-stochastisch, ohne Rückführung ⚠️ (korrigiert D27)

`§5` schrieb „spaltenstochastisch normalisiert" über `Σw`. Die Fassung hat zwei Defekte.

**Der absolute Pegel von `w` verschwindet.** Normalisiert man je Knoten über `Σn`, kürzt sich
`D` heraus. Ein Autor mit **einer** ausgehenden Kante und `n = 1` bei `D = 100` bekommt
`P = 1` — exakt wie bei `n = 100`. Damit erreicht D27 sein erklärtes Ziel nicht: der
Probe-Vouch mit `w = 0.05` wird sehr wohl wie eine volle Bürgschaft behandelt, sobald er
allein steht. Die Begründung von D27 trug die Regel von D27 nicht.

**Die Monotonie aus `§7` bricht.** Eine zusätzliche Kante von `I` senkt den Anteil jeder
bestehenden Kante von `I`. Umkehrschluss: **fehlendes Wissen hebt fremde Werte** — wörtlich
der Defekt, den D9 als nicht reparierbar verworfen hat. Erschöpfend gemessen an Variante B
(alle 32 Teilgraphen): **9 Verletzungen** unter der alten Fassung, **0** unter der neuen.

Normativ:

```
P[J][I] = n_kante(I, J) / D          — absolut, keine Kopplung an andere Kanten
Sigma t <= 1 − (1 − alpha)^K         — das Defizit ist das ungenutzte Budget
```

**Keine Rückführung des Defizits.** Die zunächst gewählte Fassung leitete das Defizit auf den
Restart-Vektor, um `Σt = 1` zu erhalten. Sie ist überflüssig: mit `T = (I − (1−α)Pᵀ)⁻¹` ist
der Fixpunkt mit Rückführung `t = (α + (1−α)ℓ(t))·T·e_s` und ohne `t' = α·T·e_s`; weil `ℓ(t)`
ein **Skalar** ist, gilt `t = (s/α)·t'`. Beide Fixpunkte sind proportional — gleiche Ordnung,
gleiche Verhältnisse, nur andere Normierung. Die Rückführung kostet einen Rang-1-Term je
Iteration und ein `min()` je Knoten und ist zudem ein Informationsverlust: ohne sie ist
`1 − Σt` das ungenutzte Budget, als Zahl lesbar (Anker PR-5).

**Die D9-Ausnahme entfällt ersatzlos.** Es gibt keine Normalisierung über `Σw` mehr. Der
Sonderstatus von `§5` gegenüber D9 wird gestrichen, nicht umformuliert — `§5` ist damit frei
von der Kopplung, die D9 verbietet, und `§7` gilt in **beiden** Sichten.

**Nebenwirkung:** Dangling Nodes sind kein Fall. Ein Knoten ohne ausgehende Kante in `E⁺`
reicht nichts weiter; die bei ihm angekommene Masse bleibt bei ihm.

### D46 — Exakte Integer-Arithmetik über festem Nenner

```
u_0[J]     = 0
u_{k+1}[J] = a·D·(b·D)^k · [J in A]  +  (b−a) · Sum_{(I,J) in E+} u_k[I] · n_kante(I,J)
t[J]       = u_K[J] / Delta_K              Delta_K = |A| · (b·D)^K,  alpha = a/b
```

Der Streckfaktor je Runde ist `Δ_{k+1}/Δ_k = bD`; damit sind Restart- und Transferterm
ganzzahlig, und `|A|` kürzt sich aus der Rekursion heraus. **Es gibt an keiner Stelle eine
Division, also keine Rundung und keine Rundungsrichtung.** Kein `Fraction`, kein `decimal`,
kein `float` — dieselbe Aussage wie D28/D29, ein zweites Mal.

Nur unter D45 ist das billig: die spaltenstochastische Fassung hätte knotenweise Nenner
`Σn_I`, deren kgV unkontrolliert wächst. Dann bliebe Festkomma mit Abrundung je
Multiplikation, samt Rundungsrichtungs-Fork und Fehlerakkumulation. **Das ist das praktische
Argument für D45, unabhängig vom prinzipiellen.**

Bei `TP-02` (`a=1, b=2, D=4, K=20`) ist `Δ = 8²⁰ = 2⁶⁰` — unter `2⁶³` und damit auch in einer
Sprache ohne Bigints darstellbar.

### D47 — Feste Rundenzahl, `t₀ = 0`

Mit `t₀ = 0` ist `t_K = α · Σ_{i=0}^{K−1} (1−α)^i (Pᵀ)^i e_s` die abgeschnittene
Neumann-Reihe. Bei sub-stochastischem `P` gilt `‖t_K − t_*‖₁ ≤ (1−α)^K`, und die Folge ist
**monoton wachsend** in `K` — jeder Abbruch ist eine Untergrenze und damit die sichere
Richtung.

`t₀ = e_s` wäre die naheliegendere Wahl und ist schlechter: die Schranke verdoppelt sich auf
`2(1−α)^K`, die Monotonie in `K` geht verloren, und `u₀` ist teurer.

**Normativ ist `t_K`, nicht `t_*`.** Der Fixpunkt ist die Motivation, nicht die Definition.
Nur so ist der Wert exakt und byte-reproduzierbar. Ein Konvergenztest zur Laufzeit ist damit
verboten: er machte das Ergebnis implementierungsabhängig.

`K` folgt aus `α` und der Zielgenauigkeit: `K = ⌈log ε / log(1−α)⌉`. Für `α = ½, ε = 2⁻²⁰`
ist `K = 20`.

### D48 — `α = 1 − γ` als Profilkopplung

Entlang eines Pfades zerfällt die Masse in `§5` wie `(1−α)^d`, die Kapazität in `§3` wie
`γ^d`. Mit `α = 1 − γ` zerfällt `§5` **mindestens** so schnell wie `§3` — schneller, weil
sich die Masse zusätzlich über die Kanten aufteilt. Das ist die sichere Richtung, und das
Profil hat einen Knopf weniger.

Der Standardwert `α = 0.15` aus der Suchmaschinenliteratur ist auf globale Reichweite
kalibriert und steht quer zum Lokal-Ethos aus `§1`/`§8` („Default eher schnelles Abklingen").

**SHOULD, nicht MUST.** `§5` trägt keine Schranke, also ist die Kopplung nicht beweisbar —
sie ist begründbar und dokumentierbar, mehr nicht. Eine Policy darf `α` unabhängig setzen;
sie sollte es begründen. Für `γ = ½` folgt `α = ½`, also `a = 1, b = 2`.

### D49 — `§5` läuft über demselben Kantensatz wie `§4`

Gruppen-Aggregation `max n` (D40), `E⁺`-Filter (D36) und Flag-Anwendung (D39) gelten
unverändert. `§5` selbst sagt es: „Beide Sichten teilen denselben Graphen."

Drei Klarstellungen, die im Code sonst schiefgehen:

- **`C(x)` geht in `§5` ein, aber nur als Filter, nie als Faktor.** Ohne `E⁺` wäre der
  D36-Angriff eins zu eins übertragbar: drei Kolludierende mit `n = 1` bei `d = 2`, die in
  `§4` exakt null Fluss tragen, bekämen volle Übergangswahrscheinlichkeit. Eine Gewichtung
  mit `cap(e)` statt `n_e` wurde geprüft und verworfen — knotenweise kürzt sich `C(I)` bis
  auf Rundungsartefakte weg, das kauft nichts und bringt Rauschen.
- **Kein Knoten-Splitting.** Der Split ist eine Max-Flow-Konstruktion für Knotenkapazitäten;
  `§5` hat keine. Wer den `02a`-Graphbauer arglos wiederverwendet, rechnet über einer
  verdoppelten Knotenmenge und bekommt einen zusätzlichen `(1−α)`-Faktor je Hop. Belegt durch
  Anker PR-4 (`TP-FAN`).
- **Das Budget-Set spielt keine Rolle.** `§5` liest `n_kante` aus dem Aktiv-Set. Das
  Budget-Set dient der Über-Commitment-Erkennung, und die geschieht vor der Sichttrennung.

Folge für die Implementierung: `02b` teilt die Ableitungsstufe mit `02a` und beginnt danach.

### D50 — „Nie über-vertrauend" ist eine Kanalaussage, keine Wertaussage ⚠️ (präzisiert D27)

`§4` liefert Fluss in Kapazitätseinheiten, `§5` stationäre Wahrscheinlichkeitsmasse. **Die
Größen sind nicht kommensurabel.** „`§5 ≤ §4`" ist punktweise nicht formulierbar, und die
Ordnungen stimmen im Allgemeinen auch nicht überein: `§4` misst Engpässe, `§5` misst
Erreichbarkeitsmasse.

Prüfbar ist allein, dass `§5` **keinen Signalkanal ignoriert, den `§4` benutzt, um einen Wert
zu senken**:

| Kanal | Regel |
|---|---|
| Gewicht `w` | D45 |
| wirksames Kantenset `E⁺` | D36/D49 |
| Gruppenmaximum `n_kante` | D40/D49 |
| Flag | D39/D49 |

Vier Kanäle, vier Tests. Ohne diese Präzisierung steht in `§5` und D27 ein Satz, den niemand
widerlegen und niemand prüfen kann — und die nächste Abnahme sucht vergeblich nach dem
Testvektor.

### D51 — Restart-Vektor gleichverteilt über das Ankerset

`e_a = 1/|A|` für `a ∈ A`, sonst `0`. Eine gewichtete Fassung bräuchte einen Mechanismus, aus
dem Gewichte kämen; `§6.3` kennt keinen.

**Zu benennende Asymmetrie:** in `§4` hängt der Super-Source mit ∞ an *jedem* Anker — ein
zweiter Anker kann den Wert nur heben. In `§5` verdünnt ein zweiter Anker den ersten: das
Hinzufügen eines Ankers kann einen Knotenwert **senken**. Das ist kein `§7`-Bruch (`§7`
handelt von Kanten), aber ein echter Verhaltensunterschied zwischen den Sichten. Er gehört
ins Register, nicht in einen Codekommentar.

### D52 — Die Oberfläche trägt die Trennlinie aus `§9`

`§9`: „PageRank nur als Relaxation — bei Missbrauch für harte Gates verliert man die
Schranke. Diese Trennlinie ist nicht verhandelbar." Im Code ist die Oberfläche die einzige
verfügbare Durchsetzung.

Normativ: eigenes Modul, eigener Name, eigener Rückgabetyp. **Nicht `trust`, nicht
`TrustResult`.** Der Rückgabetyp führt `Δ` mit; wer eine Schwelle vergleichen will, muss sich
sichtbar dafür entscheiden.

Mehr ist mechanisch nicht zu haben, und das steht so in der Spec, statt Sicherheit zu
suggerieren.

### D53 — Kein Clamp für über-committete Autoren ⚠️

Ohne Deckel kann ein über-committeter Autor (`Σn_I > D`) in `§5` Masse **erzeugen**. Gemessen
an Variante D (`gᵢ` mit `Σn = 8 > 4`): `t(gᵢ) = 17/64` gegen `131071/4194304` in der
budgetgültigen Variante C, und `Σt = 107/64 > 1`. `§4` liefert für beide `3/3/3` (INV-5).
Die schnelle Sicht überzeichnet also um das Achtfache.

**Jede Reparatur wurde geprüft und verworfen.** Ob `n/max(D, N_I)` oder `ñ = ⌊n·D/N_I⌋` — der
Anteil einer Kante hinge an den **anderen** Kanten desselben Autors. Das ist wörtlich der
D9-Defekt: bei Teilwissen ist `N_I` zu klein, der Clamp greift nicht, und fehlendes Wissen
hübe Werte. Wir hätten die Monotonie, für die D45 überhaupt gewählt wurde, gegen einen
Randfall wieder eingetauscht.

Zwei Eigenschaften erledigen den Fall stattdessen:

- **Der Default schützt.** `include_flagged = False` entfernt die Kanten über-committeter
  Autoren. Gemessen: Variante D mit `False` ist **byte-gleich mit B**. Wer `True` setzt, sagt
  ausdrücklich „ich weiß, dass dieser Autor über-committet ist, und will ihn trotzdem
  zählen", und trägt die Deutung.
- **Die Massenbilanz ist ein Detektor, kostenlos.** Bei budgetgültigem Kantensatz gilt per
  Induktion `Σt ≤ 1 − (1−α)^K`. Also:

  ```
  Sigma t > 1 − (1 − alpha)^K   ==>   ein einbezogener Autor ist ueber-committet
  ```

  Einseitig — kein Falschalarm, nur Unter-Erkennung. Exakt D3, exakt die Richtung, die `§3.1`
  für das beobachtete `Σw` schon festhält. Eine Summe, die ohnehin gebildet wird.

**Getragene Grenze:** `§5` ist gegen einen über-committeten Autor bei `include_flagged = True`
nicht konservativ. Das ist die dokumentierte Grenze der Relaxation und gehört in `§9` zu den
bewusst getragenen v1-Grenzen.

### D54 — Die Massenschranke exakt und profilunabhängig

Die Schranke aus D45 lautet `Σt ≤ 1 − (1−α)^K`. `02b-golden-anchors.md` Rev 1 gab dafür keine
ganzzahlige Form an, und die naheliegende Umsetzung `Δ − Δ // 2^K` ist **profilabhängig**: sie
ist nur exakt, wenn `2^K` den Nenner `Δ = |A|·(b·D)^K` teilt — also genau für `α = ½`.

Der Implementierer hat das in der `02b`-Abnahme gemeldet. Die allgemeine Form ist exakt und
für jedes `α` ganzzahlig, weil sich `b^K` vollständig gegen `Δ` kürzt:

```
Delta * (1-alpha)^K  =  |A| * (b*D)^K * (b-a)^K / b^K  =  |A| * D^K * (b-a)^K

mass  <=  Delta - |A| * D^K * (b-a)^K
```

Ein Produkt aus Ganzzahlen, ohne Division und ohne Fallunterscheidung.

Nachgerechnet bei `TP-02` (`|A| = 1, D = 4, K = 20, b−a = 1`): `2⁶⁰ − 2⁴⁰ =
1152920405095219200`, identisch zur profilabhängigen Form, und Variante F erreicht die
Schranke mit **Gleichheit**. Gegenprobe an einem Profil, in dem die alte Form bricht
(`α = 1/3, D = 6, K = 7, |A| = 2`): `Δ = 1224440064`, Schranke `1152776448`; `Δ // 2^K` ist
dort bedeutungslos, weil `(1−α)^K` den Nenner `3^7` trägt.

**Dieselbe Klasse wie D41/D42:** eine Zahl in den Vorgaben, die der kanonische Testgraph nicht
widerlegen konnte, weil das Profil der Sonderfall ist. `α = ½` ist der einzige Wert, unter dem
der Fehler unsichtbar bleibt — und es ist der Default (D48). Ein Profil mit `α = 1/3` hätte
ihn sofort gezeigt; genau deshalb steht ein solcher Vektor jetzt als offener Punkt in
`02b-golden-anchors.md §11`.

Normativ ist die Produktform. Sie ersetzt jede Fassung mit `//`, auch dort, wo die Division
zufällig aufgeht.

---

## K. Aus der Forkanalyse Layer 03 (Profile II — Verdikt · Wert · Mitgliedschaft)

Fünfzehn Forks aus 183 Zeilen. Drei der zehn eingebrachten Punkte waren bereits in `00`
entschieden und in `03` nur nicht nachgezogen — `03-profiles.md` ist im Bestand die älteste
Profil-Datei, und ihre Antworten sind nach `00` gewandert, ohne dass sie mitkam. Ein
Widerspruch zwischen zwei Dateien auf `main` wurde dabei sichtbar (→ D68).

**Vorab geklärt (kein Befund):** `trust()` mit leerem Ankerset auf Variante A liefert
`OVERCOMMITTED_AUTHOR` für CAROL, byte-identisch zum Lauf mit ALICE-Anker. INV-8 hält in
Layer 02a. Der Vektor aus `02b-golden-anchors.md §11` ist fällig, nicht offen, und gehört
nach `tests/trust/test_invariants.py`.

---

### D55 — `v`-Kodierung der Layer-03-Profile: typ-normativ, bedeutungsblind

Der Keyraum von `v` ist **prädikat-lokal**. `v` ist für das Atom opak; ein Key trägt nur
innerhalb seines Profils Bedeutung. Key `0` in `vouch@1` und Key `0` in `obligation@1` sind
verschiedene Dinge und kollidieren nicht.

```
obligation@1   0 : uint   amount      uninterpretiert
               1 : bstr   unit_ref    byte-vergleichbar, nie geparst
receipt@1      0 : uint   amount      löst KEINE Tilgung aus (D65)
verdict@1      0 : uint   outcome     Bedeutung ist Policy
               1 : bstr   reason_ref
accusation@1   keine reservierten Keys — vollständig opak (D67)
```

**Normativ ist der Typ, nicht die Bedeutung.** Ist ein reservierter Key vorhanden, MUSS er den
deklarierten Typ tragen; ein Verstoß erzeugt ein Finding, keinen Reject. Fehlt der Key, ist das
kein Fehler. Weitere Keys sind zulässig und opak. Das ist exakt die Bauform aus D37: geprüft
wird der Key, nicht die Map als Ganzes.

**Verworfen — vollständig opak.** Dann gäbe es in `03` keinen einzigen Byte-Vektor. Die
`02b`-Abnahme lief beim ersten Versuch durch, weil die Golden Numbers exakt und rundungsfrei
waren; eine Schicht ohne prüfbare Bytes hat kein Äquivalent dazu und fällt auf „der Code stimmt
mit sich selbst überein" zurück.

**Verworfen — semantisch normativ** (Beträge werden gelesen und verglichen). Bricht die
Preisblindheit aus `03 §3.1` und A2, und braucht eine Einheiten-Registry, die es nicht gibt.
Wäre nur nötig, wenn ungedeckte Emission eine mechanische Schranke bekäme — sie bekommt keine
(D66).

### D56 — Vouch-`v` Key `1` wird vertagt, Key `2` nur typ-fest

D37 sagte, die Kodierung der Keys `1` (Zweck-Tag) und `2` (`bond_ref`) werde „mit `03`/`05`
festgelegt". Das war eine Terminplanung, keine Ableitung. **Key `1` ist Layer-02-Semantik und
hat in `03` keine Verwendung.**

Er ist außerdem teurer als er aussieht. Sobald er kodiert ist, ziehen drei Dinge nach:

1. `trust()` und `rank()` brauchen einen `purpose`-Parameter. Er fehlt in beiden Signaturen.
2. Der Gruppenschlüssel aus D40 ist `(I, J, N)`. Mit Zweck-Tag muss `n_kante` über der
   **gefilterten** Teilmenge maximiert werden, sonst erbt ein Probe-Vouch für `π₁` das Gewicht
   eines vollen Vouch für `π₂` — die falsche Richtung, und zwei Implementierungen laufen dort
   legitim auseinander.
3. Das Budget bleibt `(I, N)` über **alle** Zwecke, sonst kauft ein Autor durch Zweck-Splitting
   neues Budget. Das ist zugleich die Begründung, warum D25 für Torwächterschaft eigene
   *Scopes* verlangt und nicht eigene Zwecke.

**Beschluss:** Key `1` bleibt unkodiert bis zu einem eigenen Durchgang `02c-purpose`, nach `03`.
Key `2` bekommt jetzt nur den Typ — `2 : bstr`, Länge 32, nie dereferenziert —, damit `03` und
`05` denselben Slot nicht verschieden belegen. Kein Testvektor, keine Wirkung.

### D57 — Die Policy ist Parameter der Klassifikation und wird aus dem Claim aufgelöst ⚠️

`01 §5.4` und `§6` sagen beide, eine Nukleus-Policy dürfe die Aktiv-Sicht überschreiben. Die
eingefrorene Signatur `classify(claim, store, now)` hat dafür keinen Ort. Der Satz war zwei
Layer lang dekorativ und fällt erst auf, weil `03` ihn braucht: ohne ihn ist `03 §3.3.3`
(`obligation@1` irrevocable) unauswertbar, und das Schulden-Lösch-Loch bleibt offen.

```python
def classify(claim, store, now, policy: NucleusPolicy | None = None) -> Classification: ...
```

**Der Aufrufer wählt die Policy nicht — sie wird aufgelöst.** Der Claim trägt `N`; `N` bestimmt
das Genesis; das Genesis bestimmt `constitution_hash`; die Verfassung bestimmt
`irrevocable_predicates` (`00 §5`). Ist das Verfassungsobjekt lokal nicht bekannt (Partition),
greift der Sicherheits-Default aus `00 §5.2`: **exakt** `["obligation@1"]`, nichts sonst.

**Warum kein Wrapper in `03` (Variante b).** Die Regel muss unumgehbar sein. Ein Wrapper ist es
nie: jeder Aufrufer, der ihn vergisst, reißt das Loch wieder auf — genau der Fehlermodus, vor
dem `03 §5` warnt. Zusätzlich entstünde eine zweite Definition von „aktiv" neben `02 §2`, und
zwei Definitionen driften.

**Warum kein Store-Filter (Variante c).** Revokes zu verstecken bricht A3 und `01 §5.2`: sowohl
der Claim als auch sein Widerruf bleiben sichtbar.

**Der Preis, offen benannt:** Layer 01 wird für einen additiven Parameter mit Default
aufgetaut. Feldsatz, Serialisierung, Signatur, elf Reject-Codes und acht Zustände bleiben
unberührt; `policy=None` ist die heutige Semantik, die 61 Tests bleiben grün. Der Durchgang
heißt `01a-policy` und läuft **vor** `03`, weil drei `03`-Funktionen den Parameter nehmen.

### D58 — Trust-gewährende Prädikate dürfen nicht irrevocable sein ⚠️

`00 §5` deklariert `irrevocable_predicates` als freies `array[text]`. Ein Nukleus, der dort
`vouch@1` einträgt, macht Widerrufe wirkungslos — also genau die **eine gefährliche Richtung**
aus `02 §7`, und zwar permanent und strukturell statt nur partitionsbedingt.

> **Normativ:** Irrevocable darf nur ein Prädikat sein, dessen **Fortbestehen** die konservative
> Lesart ist. Steht `vouch@1` in `irrevocable_predicates`, ist die Deklaration unwirksam: Finding
> `UNSAFE_IRREVOCABLE_PREDICATE`, und Widerrufe wirken weiterhin.

Für `obligation@1` ist Fortbestehen konservativ (die Schuld bleibt stehen), für `vouch@1` ist es
das Gegenteil (Vertrauen bleibt stehen). Die Asymmetrie ist der ganze Punkt und stand nirgends.

Testvektor: eine Verfassung, die es versucht.

### D59 — `obligation.t_exp` bleibt erlaubt, wird aber zum Finding

`03 §3.3.1` erlaubt `t_exp` als „harte Decke". Zusammen mit `§3.3.3` ergibt das: der Schuldner
kann seine Schuld nicht widerrufen, darf sie aber bei Ausstellung so programmieren, dass sie
von selbst verfällt. Irrevocability schützt gegen den **nachträglichen** Willen, nicht gegen
den vorprogrammierten.

Entschärft ist es dadurch, dass die Obligation einseitig ist: es gibt keine signierte Annahme
des Gläubigers, also trägt er die Prüfpflicht ohnehin, und `t_exp` ist für ihn vor der Lieferung
sichtbar.

**Beschluss:** erlauben, aber sichtbar machen. Eine `obligation@1` mit `t_exp` erzeugt
`EXPIRING_OBLIGATION`. Bedeutungsblind, billig, und es macht die Falle für Werkzeuge lesbar.

**Verworfen — Policy-Verbot.** Befristete Verpflichtungen sind ein legitimer Fall (`06 §5`,
SLA-Fenster). Ein Verbot verlöre mehr, als es schützt.

### D60 — Mitgliedschaft hat vier Zustände, nicht zwei

```python
def membership(store, *, subject, scope, constitution_hash, now,
               authorized_keys, policy=None) -> MembershipResult
```

```
MEMBER        beide Claims aktiv
APPLICANT     nur accept-rules aktiv
GRANT_ONLY    nur grant-membership aktiv
NONE          keiner
```

**Kein bool.** `05 §1` Stufe 4 unterscheidet Ausschluss (N widerruft den Grant) von Austritt
(X widerruft die Annahme); mit einem Wahrheitswert sind beide `False` und nicht
auseinanderzuhalten. `03 §4` nennt `GRANT_ONLY` „ungültig" — das ist richtig als Wirkung, aber
der Zustand muss benennbar bleiben.

`MembershipResult` trägt zusätzlich die beiden `claim_id` und `findings`, in der Form von
`TrustResult`.

**„Aktiv" heißt dasselbe wie `02 §2`** — Layer-01-`active`, `pending` zählt nicht —, ausgewertet
unter der Policy aus D57. Da weder `accept-rules@1` noch `grant-membership@1` irrevocable sind,
fallen beide Begriffe in `03` faktisch zusammen; die Regel steht trotzdem einmal geschrieben,
sonst driftet sie beim nächsten Prädikat.

### D61 — Der `constitution_hash` ist Parameter, nicht Auflösung

`accept-rules@1.J = [object-hash, H(Verfassung)]` bindet eine Mitgliedschaft an eine **Version**.
Nach einem Amendment sind alte Annahmen strukturell weiter aktiv, zeigen aber auf den falschen
Hash. Welcher Hash gilt, entscheidet die Ratifizierung über die `amendment`-Schwelle
(`00 §5.3`) — eine Layer-04-Frage.

**Beschluss:** `membership()` nimmt `constitution_hash` als Parameter und vergleicht byte-weise.
`03` löst nicht auf, welche Version aktuell ist. Damit bleibt `03` frei von Layer 04 und
bedeutungsblind.

Testvektoren gegen den Bestandsanker aus `00 §3.1`: `890b21e7…` ⇒ `MEMBER`; ein abweichender
Hash ⇒ die Annahme zählt für diese Version **gar nicht**, also `GRANT_ONLY` bzw. `NONE`.

### D62 — `resolve_current_key` gehört nicht in `03`

`00 §7` ersetzt die alte Regel `I == N` durch `akt.I ∈ resolve_current_key(akt.N)`. Damit ist
die Frage „trägt `03` einen Gruppenschlüssel?" beantwortet und zwar mit **nein**: `key_mode = 1`
bedeutet einen FROST-Gruppenschlüssel, und eine FROST-Signatur verifiziert als gewöhnliche
Ed25519-Signatur unter diesem Schlüssel. Layer 01 bleibt unberührt. Die Tabelle in `03 §4`
(`I = N`) ist toter Text und wird ersetzt.

`resolve_current_key` selbst ist eine Kettenauflösung über `rotate-key@1` ab `root_keys`, mit
eigenen Equivocation-Fällen (`01 §8`: ein gestohlener Schlüssel, der zwei Nachfolger signiert).

**Beschluss:** `03` nimmt `authorized_keys: frozenset[bytes]` als Parameter.
`resolve_current_key` und `rotate-key@1` bekommen einen eigenen Durchgang `00a`. Sonst zöge `03`
die Schlüsselrotation samt Diebstahlsfällen herein — ein größerer Brocken als alle drei Cluster
zusammen.

**Ebenfalls ausgeklammert:** der Kompositionspfad aus `04 §3` (`vote_mode = 0`), bei dem eine
Mitgliedschaft ohne einzelnen `grant-membership`-Autor durch Auszählung entsteht. `03` wertet
nur den claim-basierten Pfad. Getragene Grenze, in `03 §5` zu nennen.

### D63 — „Passende" Quittung ist ein vierteiliges strukturelles Prädikat

`03 §3.3.2` verlangt eine „passende" Quittung, ohne sie zu definieren.

```
receipt.J  == [claim-ref, obligation.claim_id]
receipt.I  == obligation.J.value    und  obligation.J.tag == identity
receipt.N  == obligation.N
beide aktiv (Obligation unter der Policy aus D57)
```

Die dritte Bedingung ist **nicht** redundant. `01 §2.2` Regel 3 erzwingt nur, dass `N` gesetzt
und selbstkonsistent ist, nicht dass zwei Claims denselben Scope teilen. Ohne sie quittiert eine
Identität in Nukleus B eine Schuld aus Nukleus A.

Trennende Vektoren: Quittung vom Schuldner statt vom Gläubiger; Quittung mit fremdem `N`;
Quittung auf eine Obligation, deren `J.tag` `claim-ref` statt `identity` ist.

### D64 — Die Quittung bleibt widerrufbar

Aus D63 folgt eine Asymmetrie, die nirgends stand: die Obligation ist irrevocable, die Quittung
nicht. Der Gläubiger kann quittieren und den Widerruf nachschieben — die Schuld lebt wieder auf.
Tilgung ist damit **nicht monoton**.

**Beschluss: getragen.** Die Quittung bleibt per A3 sichtbar, ihr Widerruf ist selbst Evidenz,
und der Missbrauch ist ein oracle-abhängiger Streit — also genau der Fall, für den `§2.3` das
Verdikt vorsieht. Gehört als getragene Grenze in `03 §5`.

**Verworfen — `receipt@1` ebenfalls irrevocable empfehlen.** Sieht sicherer aus und erzeugt den
schlechteren Fehlerzustand: eine irrtümliche Quittung wäre unheilbar, und die Korrektur wäre
eine neue `obligation@1` des Gläubigers — also eine Schuld, die es nie gab.

### D65 — Teil-Tilgung: ein `amount` im Receipt tilgt nicht

`03 §5` („in v1 nicht modelliert") und `§3.3.2` („optional, z. B. Teilbetrag") widersprechen
sich in derselben Datei. Die naive Auflösung — `receipt.v` opak lassen und jede Quittung als
Voll-Tilgung werten — ist die gefährliche: ein Gläubiger, der einen Teilbetrag meint, quittiert
versehentlich die ganze Schuld. Über-Tilgung, also die falsche Richtung.

> **Normativ:** Trägt `receipt.v` Key `0`, **tilgt die Quittung nicht** und erzeugt
> `PARTIAL_RECEIPT_UNSUPPORTED`. Die Schuld bleibt stehen.

Sichere Richtung, testbar, und der Erweiterungspfad bleibt offen, ohne dass v1 rät. `§3.3.2`
wird auf diese Formulierung nachgezogen, `§5` bleibt.

### D66 — Ungedeckte Emission ist auditierbar, nicht selbst-validierend

`03 §3.3.4` zieht die Parallele zum Über-Commitment aus `02 §3.1`. Dort trägt sie die
Deckungsgrenze `Σn ≤ D`. Hier gibt es keine — die Parallele trägt nicht.

**Beschluss:** `§3.3.4` umformulieren. „Beweisbar" heißt hier **auditierbar** (der signierte
Schuldgraph ist vollständig nachvollziehbar), nicht **selbst-validierend**. Kein mechanischer
Slash, kein Stufe-3-Auslöser in `05 §3`.

**Verworfen — Schranke `Σ amount ≤ credit_limit(I)` aus der Verfassung.** Der Grund ist nicht
der Aufwand: die Prüfung wäre in genau dem Sinn bedeutungsblind, in dem `n ≤ D` es ist, ein
Integer-Vergleich ohne Interpretation. Der Grund ist, dass die Grenze willkürlich wäre.
`Σw ≤ 1` ist ökonomisch begründet, weil es **Haftung** bindet (D3, D5). Eine Emissionsgrenze
bindet nichts. In einem Mutual-Credit-System setzt der **Gläubiger** das Limit pro Trustline,
nicht die Verfassung pro Person; diese Form gehört in eine Wert-/Exchange-Schicht, die es nicht
gibt (L4: im Protokoll so wenig wie möglich fixieren).

**Namensbereinigung.** `Über-Commitment` (Vouch-Budget, D4, mechanisch slashbar) und
`Über-Emission` (IOU, sozial) unterscheiden sich um zwei Silben und um die gesamte Konsequenz.
Da `05 §3` laut Änderungsliste G „Über-Commitment ⇒ Stufe 3" bekommt, stehen beide bald in
derselben Datei. `Über-Emission` wird durchgängig zu **`ungedeckte Emission`**.

### D67 — Verdikt-Status ist eine Funktion, und `submit-arbitration@1` ist ein Profil

Drei Teile.

**(a) Die Funktion.** `00 §5.1` ist bereits maschinenlesbar formuliert und nennt sich selbst
„die maschinenlesbare Antwort auf E-1"; `05 §3` hängt daran. Also implementieren:

```python
def verdict_status(store, *, verdict, scope, arbitrators, now,
                   policy=None) -> VerdictStatus   # BINDING | ATTRIBUTED_OPINION
```

**(b) Parteienauflösung.** Pfad (ii) verlangt, dass **beide Parteien** vorab gezeigt haben. Wer
sie sind, stand nirgends. Normativ: Ankläger ist `accusation.I`. Der Beschuldigte ist
`accusation.J.value`, falls `J.tag == identity`; bei `J.tag == claim-ref` ist es der **Autor**
des bestrittenen Claims. Je ein Vektor.

**(c) `submit-arbitration@1` bekommt eine Profiltabelle.** `03 §2.4` nennt es beiläufig
„optional", `00 §5.1` macht es zur normativen Bedingung für Pfad (ii). Ohne Tabelle ist der
Absatz nicht auswertbar.

| Feld | Belegung |
|------|----------|
| `I`  | die sich unterwerfende Partei |
| `J`  | `[identity, schiedsrichter]` |
| `N`  | **Pflicht** — der Schlichtungs-Kontext |
| `v`  | opak |

Lebenszyklus über `core/revoke@1`, selbst-bezüglich. Bindung ist selbst ein Claim — das ist die
Komposition, die `§2.4` behauptet, sauber durchgezogen.

**Nicht implementiert:** die Beweise in `accusation.v`. `§2.1` verlangt „self-contained
Beweise", aber Layer 01 flaggt Equivocation ohnehin aus dem Store; ein zweiter Prüfpfad in `03`
wäre Redundanz mit eigener Fehlerfläche. `accusation.v` bleibt vollständig opak (D55). Der Satz
in `§2.1` ist als Konvention für Menschen zu lesen, nicht als Verifizierer-Pflicht — und so
umzuformulieren.

### D68 — `00 §5.1` behauptet eine Fassung von `05 §3`, die es nicht gibt

`00 §5.1` verweist auf „Enforcement-Spec §3, geänderte Fassung — siehe DF-2". `05 §3` auf `main`
enthält weder `attributed_opinion` noch überhaupt eine Statusunterscheidung. Ein Widerspruch
zwischen zwei Dateien im Bestand, unabhängig von `03`.

**Vor `03` nötig ist nur das Vokabular**, weil `03` es produziert: `BINDING` und
`ATTRIBUTED_OPINION`. Severity-Schwellen, Cure-Kurven und Slash-Höhen bleiben Policy und Layer
05.

**Für den zweiten `05`-Durchgang vorgemerkt:** `§3` bekommt den Satz, dass ein Verdikt ohne
Bindung nach `00 §5.1` **keinen** Statuswechsel auslöst, unabhängig von seiner Severity.

### D69 — Oberfläche und Modulschnitt von Layer 03

```
mensch_als_republik/profiles/
  policy.py      NucleusPolicy, Auflösung, Sicherheits-Default (00 §5.2)
  membership.py  membership()      -> MembershipResult
  credit.py      settlement()      -> SettlementResult
  verdict.py     verdict_status()  -> VerdictStatus
  findings.py
```

`03` ist reine Komposition über Layer 01 plus Policy: kein Graph, keine Anker, kein
`TrustParams`. `classify_all` aus `02` wird **geteilt, nicht kopiert**, abgesichert durch
denselben Identitätsvergleich der Funktionsobjekte, den PR-INV-4 für `derive()` eingeführt hat.

Drei getrennte Funktionen statt einer, weil `03 §1` drei getrennte Cluster behauptet und die
Trennung sonst nur in der Prosa steht — dieselbe Bewegung wie D52 (`§9` trägt die Trennlinie in
die Oberfläche).

---

## L. Golden Anchors für Layer 03 — anderer Maßstab, gleiche Disziplin

`03` ist weitgehend nicht-numerisch. Die Trennschärfe kommt hier nicht aus Arithmetik, sondern
aus **Negativvektoren**. Drei Sorten:

1. **Byte-exakte CBOR-Vektoren** für die Kodierungen aus D55, im Format von TV1
   (`v = h'a1001864'` = `{0: 100}`). Von Hand nachrechenbar, byte-vergleichbar.
2. **Bestandsanker.** `00 §3.1` liefert `constitution_hash = 890b21e7…` und
   `N = 65309fe2…`, byte-identisch mit `01` Anhang C. `03` bindet daran, statt neue Zahlen zu
   erfinden — dieselbe Disziplin wie „die ganze Spec-Reihe testet gegen denselben Anker".
3. **Konjunktionstabellen:** Mitgliedschaft (vier Zustände, D60), Tilgung (vier Bedingungen,
   D63), Verdikt-Status (zwei Pfade × zwei Parteiformen, D67).

**Das unbequeme zweite Profil (Konsequenz aus D54) ist hier keine Parameterwahl, sondern eine
zweite Verfassung.** Das kanonische Beispiel aus `00 §3.1` trägt jeden Default, den es gibt:
`irrevocable_predicates: ["obligation@1"]`, ein Arbitrator, `key_mode = 0`, Ankerset der
Größe 1. Das Gegenprofil verletzt fünf davon, und jede Verletzung trennt zwei plausible
Implementierungen:

| Abweichung | prüft |
|---|---|
| Verfassung **schweigt** zu `irrevocable_predicates` | Sicherheits-Default `00 §5.2` |
| Verfassung nennt `vouch@1` als irrevocable | D58 |
| **zwei** Arbitratoren, einer davon nicht in `arbitration.arbitrators` | D67, Pfad (i) vs (ii) |
| `accept-rules` auf einen **anderen** `constitution_hash` | D61 |
| `grant-membership` von einem Schlüssel **außerhalb** `authorized_keys` | D62 |

Keiner dieser fünf Fälle ist unter dem kanonischen Profil sichtbar.

---

## M. Änderungsliste Layer 03

| Datei | Änderung | Quelle |
|---|---|---|
| `01-claim-atom.md §5.4`, `§6` | `policy`-Parameter der Klassifikation; Auflösungsregel; Sicherheits-Default | D57 |
| `01-claim-atom.md §5.4` | Negativliste: trust-gewährende Prädikate nicht irrevocable | D58 |
| `01-claim-atom.md §7.1` | Key `1` bleibt unkodiert (Verweis auf `02c`); Key `2` typ-fest `bstr[32]` | D56 |
| `00-…-constitution.md §5` | `UNSAFE_IRREVOCABLE_PREDICATE`; Verweis auf die Negativliste | D58 |
| `03-profiles.md` | **vollständig ersetzt** — drei Abschnitte durch `00` überholt, zwei intern widersprüchlich, `submit-arbitration@1` fehlt | D55–D69 |
| `03-profiles.md §2.1` | `accusation.v` opak; „self-contained Beweise" als Konvention, nicht als Pflicht | D67 |
| `03-profiles.md §2.4` | `submit-arbitration@1` mit Profiltabelle; Parteienauflösung | D67 |
| `03-profiles.md §3.3.1` | `v`-Keys typ-normativ; `EXPIRING_OBLIGATION` | D55, D59 |
| `03-profiles.md §3.3.2` | „passend" als vierteiliges Prädikat; Teilbetrag tilgt nicht | D63, D65 |
| `03-profiles.md §3.3.3` | Verweis auf `00 §5` statt freistehender Pflicht | D57 |
| `03-profiles.md §3.3.4` | auditierbar statt selbst-validierend; `ungedeckte Emission` | D66 |
| `03-profiles.md §4` | `I ∈ authorized_keys` statt `I = N`; vier Zustände; `constitution_hash` als Parameter | D60–D62 |
| `03-profiles.md §5` | getragene Grenzen: widerrufbare Quittung, Kompositionspfad, keine Emissionsschranke | D64, D62, D66 |
| `05-enforcement.md §3` | Vokabular `BINDING`/`ATTRIBUTED_OPINION`; kein Statuswechsel ohne Bindung | D68 |
| Repo-Wurzel | `03-golden-anchors.md`; zweite Verfassung als Gegenprofil | L |
| Repo-Wurzel | `02b-golden-anchors.md §11`: INV-8-Vektor bei leerem Ankerset ist fällig, nicht offen | K |

**Reihenfolge:** `01a-policy` → `03` (Anker → Prompt → Abnahme → Merge) → `02c-purpose` →
`00a-rotate-key` → zweiter Durchgang `05`/`06`/`04`/`00`/`VISION`.

---

## N. Aus dem Spec-Nachzug `01a-policy`

Drei Festlegungen, die beim Schreiben des Ersatztextes zu D57/D58 nötig wurden und über beide
hinausgehen. D70 ist formal eine **Wiedereröffnung** von `00 §5.2` und daher als eigener Fork
geführt, nicht als Nachtrag.

### D70 — Der Sicherheits-Default ist ein Boden, keine Rückfallebene ⚠️

`00 §5.2` lautete: „Schweigt die Verfassung zu `irrevocable_predicates`, gilt **trotzdem**
`obligation@1` als irrevocable. Weitere Prädikate werden nur durch explizite Nennung
irrevocable."

**Der Befund.** Der Satz regelt nur das Schweigen. Er sagt nicht, was gilt, wenn eine Verfassung
`["foo@1"]` deklariert und `obligation@1` weglässt. Wörtlich gelesen greift der Default dann
nicht — und das Schulden-Lösch-Loch ist durch das bloße Nennen einer beliebigen anderen Zeile
wieder offen. Genau das Loch, das der Abschnitt „nicht durch Vergessen" aufreißbar machen
wollte, nur mit einem Zwischenschritt.

```
wirksame Menge  =  { "obligation@1" }  ∪  irrevocable_predicates  ∖  unsicher (01 §5.4.3 b)
```

**Beschluss:** Der Default ist ein **Boden**. Die Liste erweitert die Menge, sie kann sie nie
verkleinern. Drei Fälle — Schweigen, Nennung, Nennung anderer Prädikate ohne `obligation@1` —
sind damit identisch geschützt.

**Verworfen — Alles-oder-nichts bei unsicherer Deklaration.** Nennt eine Verfassung `vouch@1`
(D58), wäre es denkbar, die ganze Liste zu verwerfen. Das ist schlechter: eine einzelne
Fehldeklaration nähme dem Nukleus auch den Schuldenschutz. Der unsichere Eintrag fällt heraus,
der Rest bleibt wirksam.

Dieselbe Bewegung wie D37 („kein Budget-Beitrag bei unlesbarem `n`"): der defekte Teil fällt
weg, nicht die Aussage als Ganzes.

### D71 — `core/*` kann nie irrevocable sein

`00 §5` deklariert `irrevocable_predicates` als freies `array[text]`. Ein Eintrag `"revoke@1"`
würde Widerrufe gegen Widerruf immunisieren — das ist keine Aussage über einen Lebenszyklus,
sondern ein Fixpunkt in ihm.

**Beschluss:** Der Abgleich greift nur für `nuc:`-Prädikate (`01 §5.4.2`). Einträge, die auf
`core`-Prädikate zeigen, werden ignoriert — nicht als Fehler, sondern weil `core/revoke@1` und
`core/supersede@1` *der* Lebenszyklus sind und das geschlossene Aufnahmekriterium aus `01 §5`
sie genau deshalb enthält.

Zusammen mit D58 ergibt das zwei Ausschlussgründe verschiedener Natur: D58 schließt aus, was
gefährlich wäre; D71 schließt aus, was bedeutungslos wäre.

### D72 — Oberfläche: der Typ trägt die Invarianten, der Resolver liegt in `03`

```python
@dataclass(frozen=True, slots=True)
class NucleusPolicy:
    irrevocable: frozenset[str]      # normalisiert: Boden gesetzt (D70), Unsicheres entfernt (D58)
    warnings: tuple[str, ...]        # UNSAFE_IRREVOCABLE_PREDICATE, …

def classify(claim, store, now, policy: NucleusPolicy | None = None) -> Classification: ...
```

**Die Invarianten leben im Konstruktor**, nicht in der Aufrufkonvention. Nach D57 darf die
Regel nicht umgehbar sein; ein Aufrufer, der `NucleusPolicy` baut, kann keine unsichere Menge
erzeugen, weil Boden und Filter beim Bauen greifen. Layer 01 honoriert die Menge und ignoriert
`warnings`.

**`NucleusPolicy` liegt in Layer 01, der Resolver in Layer 03.** Der Typ muss aus `01`
importierbar sein, sonst wird der Import zyklisch. Die Auflösung aus Genesis- und
Verfassungsobjekt braucht dagegen ein Objektmodell, das `01` nicht kennt — sie lebt in
`profiles/policy.py` und liefert `NucleusPolicy` plus Diagnose.

**`Classification` bleibt unverändert** und trägt die angewandte Policy **nicht**. Erwogen als
Nachvollziehbarkeitshilfe (zwei Verifizierer mit verschiedenen Ergebnissen sähen sofort, woran
es liegt), verworfen: `Classification` ist heute ein reiner Zustandswert, jedes Zusatzfeld
verkompliziert die Vergleichbarkeit in Tests, und der Aufrufer kennt die Policy ohnehin — er
hat sie übergeben.

**`resolve_policy` wird in `01a` nicht gebaut.** `00 §4` und `§5` sind Schemata, kein Code; ein
Objektmodell dafür entsteht erst mit `03` (D61 braucht die Verfassungsobjekte ohnehin). `01a`
liefert Typ und Honorierung, mit handgebauten `NucleusPolicy`-Instanzen in den Tests.

---

**Konsequenz für die Zustandsmaschine, offen benannt.** `01` Anhang B sagte bisher, alle
Zustände außer `expired` seien „deterministisch gegeben denselben Bytes". Ab jetzt gilt
„gegeben denselben Bytes **und derselben Policy**". Das ist eine echte Abschwächung eines
tragenden Satzes. Sie ist vertretbar, weil abweichende Verfassungen für dasselbe `N` kein
legitimer Uneinigkeitsfall sind, sondern ein Synchronisationsdefekt: `N` ist der Hash des
Genesis, der Genesis fixiert `constitution_hash`, und die Ratifizierung einer neuen Version ist
selbst prüfbar (`00 §5.3`). `expired` bleibt damit der einzige Zustand, in dem zwei korrekte
Verifizierer legitim uneins sein dürfen.

### D73 — Die Policy trägt ihren Scope, und eine Fehlpaarung ist laut ⚠️

Lücke in D72, sichtbar geworden beim Schreiben des `01a`-Prompts: `NucleusPolicy` hatte kein
Feld, das sagt, für **welchen** Nukleus sie gilt. Layer 01 kann die Auflösung aus `C.N` nicht
selbst leisten (`01 §5.4.1` braucht Genesis- und Verfassungsobjekte, die Layer 01 nicht kennt) —
also hätte ein Aufrufer die Policy des Nukleus A auf einen Claim aus Nukleus B anwenden können,
und nichts hätte es gemerkt.

Das ist kein akademischer Fall: sobald Layer 03 über Stores mit mehreren Scopes läuft, ist die
falsche Paarung der Normalfall eines Programmierfehlers.

**Beschluss:** `NucleusPolicy` trägt `scope: bytes` als Pflichtfeld. Trifft `classify` auf einen
`nuc:`-Claim mit `claim.N ≠ policy.scope`, wird `ValueError` geworfen. Für `core/*`-Claims wird
die Policy ohne Prüfung ignoriert.

**Warum ein Fehler und kein stilles Ignorieren.** Eine nicht angewandte Policy heißt: der
Widerruf auf eine `obligation@1` wirkt. Das ist die **unsichere** Richtung — genau das
Schulden-Lösch-Loch, das D57 schließt. Anders als bei Teilwissen (D3) gibt es hier keine sichere
Voreinstellung, weil der Zustand nicht unvollständig, sondern falsch zugeordnet ist. Ein lauter
Fehler ist die einzige Antwort, die nicht rät.

**Verworfen — `scope: bytes | None = None` mit „gilt für alles".** Bequemer in Tests, aber der
Default wäre der unsichere Fall, und Defaults setzen sich durch.

**Verworfen — `NucleusPolicy` als Abbildung `scope → Prädikate`.** Löst dasselbe Problem und
nimmt die Auflösung gleich mit, verlagert aber Mehr-Scope-Logik nach Layer 01. Die Auflösung
gehört nach `03` (D72); ein Objekt, das mehrere Nuklei kennt, ist dort zu bauen, nicht hier.

---

## O. Aus der `01a`-Abnahme

Der Lauf war beim ersten Versuch grün: 234 Tests, alle neunzehn Vektoren aus dem Prompt beim
ersten Anlauf richtig, eine Rückfrage (`helpers.py` hatte keinen generischen Anhänger — korrekt
gemeldet statt `vouch_raw` zweckzuentfremden). Die drei Befunde der Durchsicht sind **allesamt
Strukturfragen, keine Rechenfehler** — dasselbe Muster wie bei `02b`, wo beide Vorgabefehler in
Formulierungen lagen.

Zwei der drei sind Fehler in meinem Prompt, nicht in der Ausführung.

### D74 — Policy-Vermerke tragen ihr Subjekt

`01a-policy-prompt.md §2` gab `warnings: tuple[PolicyWarning, ...]` vor — einen nackten Code
ohne Subjekt. Der Betreiber erfährt damit, dass *etwas* Unsicheres deklariert war, nicht *was*.
Bei einer Verfassung mit zwanzig Einträgen ist das unbrauchbar.

**Beschluss:** `PolicyNote(code, predicate)`, ein Eintrag je unsicher deklariertem Prädikat,
sortiert nach `predicate`.

Die Sortierung ist nicht Kosmetik: `declared` ist ein `frozenset`, die Iterationsreihenfolge
schwankt zwischen Läufen, und ein Vektor über zwei unsichere Einträge wäre sonst nicht
reproduzierbar. Dieselbe Erwägung wie bei `TrustResult.findings` („sortiert, dedupliziert").

**Der Vorgabefehler ist der eigentliche Eintrag:** Layer 02 hatte `Finding(kind, subject)`
bereits richtig gebaut. Der Prompt hat die Form nicht übernommen, obwohl der Zweck identisch
ist. Neue Schichten erben die Diagnoseform der bestehenden, statt sie neu zu erfinden.

### D75 — Die drei Prädikatmengen sind disjunkt, geprüft beim Import

Die Normalisierung aus D70/D58/D71 lautet:

```
irrevocable = (PROTOCOL_IRREVOCABLE ∪ declared) ∖ TRUST_GRANTING ∖ CORE_ENTRIES
```

Boden setzen, dann filtern. Läge je ein Prädikat in `PROTOCOL_IRREVOCABLE` **und**
`TRUST_GRANTING`, verschwände der Boden aus D70 still — und **kein Testvektor kann das
prüfen**, weil die Konstanten heute disjunkt sind. P-1 bis P-6 bestehen unter jeder Anordnung
der drei Regeln.

**Beschluss:** zwei `assert` auf Modulebene statt eines weiteren Vektors. Ein künftiger
Widerspruch zwischen den Mengen wird beim Import laut, nicht in der Semantik leise.

**Das ist die D54-Lage in neuer Form.** Dort versteckte das kanonische Profil (`α = ½`) einen
Formelfehler; hier verstecken disjunkte Konstanten eine Reihenfolgefrage. Die Lehre aus D54 war
„ein zweites Testprofil mit unbequemen Zahlen". Sie greift hier nicht, weil sich der unbequeme
Fall nicht konstruieren lässt, ohne die Konstanten selbst zu verfälschen. Die Ergänzung:
**wo ein Fall untestbar ist, weil er heute unmöglich ist, wird die Unmöglichkeit zugesichert —
nicht die Semantik getestet.**

### D76 — Unter Policy schlägt `expired` den Widerruf, ohne Policy umgekehrt

Sichtbar geworden am Kontrollfluss von `classify`: ohne Policy greift der Widerruf-Zweig vor der
Zeitprüfung, mit Policy fällt die Auswertung auf den `temporal`-Zweig durch.

| Lage | `policy=None` | mit Policy |
|---|---|---|
| Obligation, abgelaufen **und** widerrufen | `REVOKED` | `EXPIRED` |

`01` Anhang B legt zwischen `revoked`, `superseded` und `expired` **keine** Rangfolge fest —
alle drei sind inaktiv, und für jeden Konsumenten der Zustandsmaschine ist das die einzige
Aussage, die zählt. Die Umkehrung ist damit kein Fehler.

**Beschluss:** Ist-Zustand festhalten, nicht vereinheitlichen. Vektor C-9 hält ihn fest, damit
er sich nicht unbemerkt ändert. Eine Vereinheitlichung würde entweder den Kontrollfluss von
`classify` umbauen (Risiko ohne Ertrag) oder eine Rangfolge in Anhang B einführen, die dort
bewusst fehlt.

**Vorgemerkt für Layer 03:** Sobald ein Konsument die Zustände *unterscheidet* statt nur
„aktiv/inaktiv" zu fragen, wird die Rangfolge relevant und muss dann entschieden werden. In
`03` ist das nicht der Fall — D60 und D63 fragen ausschließlich auf `active`.

---

## P. Aus dem Eigenauftrag zur Sitzung `03`

### D77 — Kanonizität von `v` prüft die lesende Schicht, nicht das Atom ⚠️

D37 verlangt kanonisches CBOR für `v`. **Durchgesetzt war es nirgends.** `cbor_canon.decode` ist
ein dünner `cbor2.loads`-Wrapper ohne Prüfung; `is_canonical` steht an genau einer Stelle im
Paket (`verifier.py`, Re-Serialisierung des **Cores** nach `01 §6` Regel 2). `v` ist im Core eine
`bstr`, deren Inhalt dabei uninterpretiert bleibt. `trust/groups.py` liest sie per nacktem
`decode`. Nicht-minimale Ganzzahlen, indefinite-length Maps, unsortierte und doppelte Schlüssel
gehen durch.

**Kein Testvektor konnte es zeigen.** Jedes `v` im Repo entsteht durch `cbor_canon.encode`
(`helpers.py`, `tests/trust/test_payload.py`, `tests/vectors/gen.py`) — kanonisch by
construction. Es gibt keinen Pfad, auf dem ein nicht-kanonisches `v` in einen Test gerät.
Dieselbe Mechanik wie beim unversionierten `02b`: eine einzige Darstellung des Zustands, und die
stimmt mit sich selbst überein.

**Nicht in Layer 01.** Ein zwölfter Reject-Code hieße, das Atom liest `v`. Das bricht die
Bedeutungsblindheit und D55 in derselben Bewegung. Layer 01 bleibt eingefroren.

**Beschluss:** Jede Schicht, die `v` liest, prüft vorher `is_canonical` und behandelt einen
Verstoß als **unlesbar** im Sinne von D37 — Vermerk `NON_CANONICAL_V`, defekter Teil fällt weg,
Claim bleibt gültig und sichtbar.

| Schicht | liest | Wirkung bei Verstoß |
|---|---|---|
| 02 | `vouch.v` Key `0` | keine Kante, kein Budget-Beitrag (D37, Zeile 2) |
| 03 | `receipt.v` Key `0` | tilgt nicht (D65-Richtung) |
| 03 | `obligation.v`, `verdict.v` | Vermerk, sonst folgenlos |

Drei Festlegungen, die den Beschluss erst ausführbar machen:

**(a) Nicht wie ein abwesendes `v`.** Der Abwesend-Default `n = D` (`w = 1`) auf einen defekten
Payload angewandt wertet ihn zu maximalem Vertrauen auf — Über-Vertrauen, die eine gefährliche
Richtung (`02 §7`). Nicht-kanonisch fällt in den Zweig „unlesbar", nie in den Zweig „abwesend".

**(b) Vor der Wertprüfung.** Kanonizität ist eine Eigenschaft der Bytes und geht der
Interpretation voraus. Beobachtbar an genau einem Fall: `v = h'a2001864001865'` bei `D = 100`
dekodiert zu `{0: 101}`, also `n > D`. Heute `INVALID_VOUCH_WEIGHT`, künftig `NON_CANONICAL_V`.
Ohne diesen Vektor ist der Vorrang nicht festgelegt und zwei Implementierungen laufen legitim
auseinander.

**(c) Nach dem Dekodieren.** `is_canonical` dekodiert selbst und **wirft** bei undekodierbarer
Eingabe, statt `False` zu liefern (gemessen: `h'a1'` → `CBORDecodeEOF`, `h'ff'` →
`CBOREncodeError` beim Re-Enkodieren). Ein Wächter vor dem `try` verwandelt
`UNPARSABLE_VOUCH_PAYLOAD` in eine durchschlagende Exception. Die Prüfung steht **nach** dem
geglückten `decode`.

**Der doppelte Schlüssel ist der tragende Fall.** Bei den übrigen Verstößen liefert das
Dekodieren den richtigen Wert und der Schaden bleibt bei der Byte-Vergleichbarkeit. Bei einem
doppelten Key `0` verliert `decode` einen Eintrag, und welcher gewinnt, steht in keiner
Spezifikation, sondern in cbor2. `01 §6` Regel 2 verlangt „ohne doppelte Keys" — für den Core.
Für `v` galt der Satz bis hier nicht, und damit hing `n` an einer undokumentierten
Bibliotheksentscheidung.

**Verworfen — `encode(obj) != v` statt `is_canonical(v)`.** Rechnerisch identisch und spart den
zweiten Dekodierdurchlauf, dupliziert aber die Definition von „kanonisch" an eine zweite Stelle.
Zwei Definitionen driften; die Ersparnis liegt bei einem Payload von vier Bytes.

**Der Vermerk trägt in jeder Schicht denselben Namen, das Enum wird nicht geteilt.** Layer 02 und
Layer 03 haben nach `02a §5` und D69 je einen eigenen Findings-Enum — richtig so, weil beide
keine Claim-Rejects sind. Die **Zeichenkette** muss beide Male `"NON_CANONICAL_V"` lauten, sonst
trägt derselbe Defekt zwei Namen und wer `grep` benutzt, findet die Hälfte.

**Reihenfolge.** Der Durchgang heißt `02c-canon-v` und läuft **vor** `03`, weil `03 §5.1` der
Anker Byte-Vektoren gegen die `v`-Kodierungen aus D55 setzt; ohne durchgesetzte Kanonizität sind
diese Vektoren illustrativ statt normativ. Der bisher als `02c-purpose` geführte Durchgang
(D56) heißt ab hier **`02d-purpose`**. Änderungsliste M liest damit: `01a-policy` →
`02c-canon-v` → `03` → `02d-purpose` → `00a-rotate-key` → zweiter Durchgang.

**Kein Bestandsanker ändert sich.** `TrustFinding` ist ein `str`-Enum und `Finding` sortiert
`(kind, subject)`; `NON_CANONICAL_V` reiht sich alphabetisch zwischen `INVALID_VOUCH_WEIGHT` und
`OVERCOMMITTED_AUTHOR` ein. Da kein bestehender Vektor die neue Art trägt, verschiebt sich keine
bestehende Findings-Liste. **235 grüne Tests sind damit Abnahmekriterium, nicht Hoffnung:** ein
roter Bestandstest wäre der Beweis, dass die Prüfung an der falschen Stelle sitzt.

**Änderungsliste:**

| Datei | Änderung |
|---|---|
| `02-trust-flow.md §3.1` | neuer Absatz „Nicht-kanonisches `v` ist unlesbar" (vollständige Datei geliefert) |
| `mensch_als_republik/trust/findings.py` | `NON_CANONICAL_V` |
| `mensch_als_republik/trust/groups.py` | Prüfung in `_decode_weight`, nach `decode`, vor der Wertprüfung |
| `tests/trust/test_payload.py` | `V-CANON-1` bis `V-CANON-6` |
| `tests/helpers.py` | roher `v`-Anhänger für den End-zu-End-Vektor |
| `03-profiles.md` | `NON_CANONICAL_V` im Vermerk-Katalog (mit `03`) |
| `03-golden-anchors.md §5.1` | Negativvektoren gegen die vier Verstoßklassen (mit `03`) |
| `01-claim-atom.md §7.1` | Satz, dass die Durchsetzung bei der lesenden Schicht liegt (zusammen mit der D56-Zeile) |

---

## Q. Beim Schreiben von `03-profiles.md`

Vier Forks aus der Widerspruchsprüfung vor dem Schreiben, ein fünfter beim Schreiben selbst,
dazu zwei Reparaturen im Register. Keine der fünfzehn Entscheidungen aus Abschnitt K wurde dabei
neu aufgemacht — alle fünf schließen Lücken, die K offen ließ.

### D78 — „Vorab" heißt „aktiv zum Bewertungszeitpunkt" ⚠️

`00 §5.1` und `03 §2.4` verlangen für Pfad (ii), dass beide Parteien sich **vorab** dem
Schiedsrichter unterworfen haben. D67 übernimmt das als normative Bedingung.

**Der Befund.** Zwischen zwei verschiedenen Autoren gibt es keine Ordnung. `01 §5.3` und
`00 §6.1` sagen beide: Ordnung kommt aus der Autorenkette, nie aus Wall-Clock `t` — und zwei
Autoren teilen keine Kette. `submit-arbitration` der Partei A und das `verdict` des
Schiedsrichters stehen in verschiedenen Ketten. „Vorab" ist damit prinzipiell nicht auswertbar,
nicht bloß aufwendig.

**Beschluss:** Pfad (ii) verlangt, dass beide Unterwerfungen zum Bewertungszeitpunkt `now`
**aktiv** sind. `00 §5.1` zieht im zweiten Durchgang auf dieselbe Formulierung nach.

Das ist auch die bessere Regel, nicht nur die berechenbare: wer widerruft und dabei bleibt,
trägt die Bindung nicht mehr; wer sie nachreicht, trägt sie. Beobachter dürfen über `now`
legitim uneins sein — dieselbe Lage wie bei `t_exp` (`01 §6`), mit derselben sicheren Richtung:
im Zweifel `ATTRIBUTED_OPINION`.

**Verworfen — `t` als Ordnung heranziehen.** Es wäre die einzige Stelle im ganzen Protokoll,
an der Wall-Clock eine Rangfolge zwischen zwei Autoren stiftet. Genau das schließt `01 §5.3`
aus, und ein Angreifer mit falscher Uhr bekäme Kontrolle über die Bindungsfrage.

### D79 — `settlement()` hat vier Zustände

D60 gab der Mitgliedschaft vier Zustände, D67 dem Verdikt zwei; `settlement()` stand in D69 nur
als Name. Dieselbe Begründung wie bei D60 trägt hier: mit einem Wahrheitswert fallen „nie
quittiert", „Quittung widerrufen" (D64) und „Teilbetrag, tilgt nicht" (D65) auf denselben Wert
zusammen — obwohl D64 und D65 diese Unterscheidung gerade erzeugt haben.

```
SETTLED         Obligation aktiv, passende aktive Quittung ohne Key 0
OPEN            Obligation aktiv, keine passende Quittung oder eine, die nicht tilgt
EXPIRED         Obligation durch t_exp erloschen
INDETERMINATE   Obligation pending oder unverlinkt — Teilwissen
```

**`EXPIRED` ist nicht kosmetisch.** Nach D70 ist `obligation@1` **immer** irrevocable, also ist
`t_exp` der einzige Weg, auf dem eine Obligation inaktiv wird. Der Fall ist nicht selten,
sondern der einzige, und er verlangt vom Gläubiger etwas anderes als `OPEN`.

**`INDETERMINATE` folgt D3.** Auf Teilwissen `OPEN` zu behaupten hieße, eine Schuld zu
behaupten, die es vielleicht nicht gibt — die Falschbeschuldigungsrichtung.

Falsches Prädikat oder falscher Scope: `ValueError`, kein fünfter Zustand. Präzedenz D73 — eine
falsche Zuordnung ist kein unvollständiger Zustand.

**`revoked`/`superseded` sind für `obligation@1` unerreichbar**, weil der Boden aus D70
unbedingt gilt. Das ist die D75-Lage in neuer Form: die Unmöglichkeit wird zugesichert
(`assert`), die Semantik nicht getestet.

### D80 — `policy` ist in `settlement()` Pflicht, sonst nicht

D57 verwarf den Wrapper mit dem Satz „die Regel muss unumgehbar sein". D72 machte sie über den
Konstruktor unumgehbar für die **Menge** — eine unsichere `NucleusPolicy` lässt sich nicht bauen
—, nicht für den **Aufruf**. `policy=None` bleibt erreichbar, und in `settlement()` ist das
exakt das Schulden-Lösch-Loch, eine Schicht höher: der Schuldner-Widerruf würde wirken.

**Beschluss:** `settlement(store, *, obligation, scope, now, policy)` — Pflicht-Keyword ohne
Default. `membership()` und `verdict_status()` behalten `policy=None`, weil keines ihrer
Prädikate irrevocable ist und der Parameter dort folgenlos bleibt.

**Verworfen — überall Pflicht, der Symmetrie halber.** Symmetrie ist kein Sicherheitsargument.
Ein Pflichtparameter ohne Wirkung erzieht Aufrufer dazu, irgendeine Policy zu bauen, damit der
Aufruf durchgeht — und die dann auch dort zu benutzen, wo sie falsch ist.

### D81 — Scope-Gleichheit gilt im ganzen Verdikt-Cluster

D63 normierte `receipt.N == obligation.N` mit der Begründung, `01 §2.2` Regel 3 erzwinge nur
Selbstkonsistenz, nicht geteilten Scope. Dieselbe Lücke bestand für `accusation`, `verdict` und
`submit-arbitration`: eine Unterwerfung aus Nukleus B konnte einen Streit in Nukleus A binden.

**Beschluss:** Wo zwei Claims in Beziehung gesetzt werden, müssen beide dasselbe `N` tragen, und
dieses `N` muss der ausgewertete Scope sein. Als eigener Absatz `03 §1.4` geschrieben statt
dreimal wiederholt, damit die Regel nicht beim nächsten Profil vergessen wird. Vermerk
`SCOPE_MISMATCH`, ein Negativvektor je Prädikatpaar.

### D82 — Der Resolver rechnet nach; Genesis-Fehler werfen, Verfassungs-Fehler fallen zurück

Beim Schreiben von `03 §1.2` sichtbar geworden. `resolve_policy` bekommt Genesis- und
Verfassungsobjekt übergeben. Prüft es nicht nach, ist die Content-Adressierung aus `00 §3` eine
Behauptung des Aufrufers — und der Sicherheits-Default aus D70 hinge an dessen Sorgfalt.

**Beschluss:** Der Resolver rechnet `scope == SHA-256(DOM_NUC_GEN ‖ cbor(genesis))` und
`genesis.constitution_hash == SHA-256(cbor(constitution))` nach.

| Lage | Antwort |
|---|---|
| Genesis passt nicht zu `scope` | `ValueError` |
| Verfassung fehlt | Sicherheits-Default, `CONSTITUTION_UNAVAILABLE` |
| Verfassung passt nicht zum Hash | Sicherheits-Default, `CONSTITUTION_HASH_MISMATCH` |

Die Asymmetrie folgt D73 gegen D3: ein falsches Genesis ist eine **falsche Zuordnung**, dafür
gibt es keine sichere Voreinstellung. Eine fehlende oder nicht passende Verfassung ist
**Teilwissen**, und dafür gibt es genau eine: `{"obligation@1"}`.

**Nicht geprüft wird die Ratifizierung.** Ob dieses Verfassungsobjekt die *aktuelle* Version
ist, entscheidet die `amendment`-Schwelle (`00 §5.3`) — Layer 04, nicht hier. D61 hält.

---

### Reparaturen

**Abschnitt L, Zeile 3 der Gegenprofil-Tabelle** lautete „zwei Arbitratoren, einer davon nicht
in `arbitration.arbitrators`" — in sich widersprüchlich; wer in der Verfassung steht, ist per
Definition darin. Gemeint und ab hier gültig: **die Verfassung nennt zwei Arbitratoren, das
Verdikt kommt von einem Dritten.** Pfad (i) fällt, Pfad (ii) muss tragen. Das ist der Vektor,
der die beiden Pfade aus D67 trennt.

**Abschnitt M, Zeile `01-claim-atom.md §7.1`** (D56: Key `1` unkodiert, Key `2` typ-fest
`bstr[32]`) ist noch offen — `01 §7.1` sagt auf `main` weiterhin „die Kodierung von `1` und `2`
wird mit `03`/`05` festgelegt". Sie gehört in diesen Durchgang, zusammen mit dem D77-Satz zur
lesenden Schicht: beide betreffen denselben Absatz, und eine Datei zweimal vollständig zu
liefern wäre unnötig.

---

## R. Aus dem `02c`-Lauf

### D83 — Der Kanonizitäts-Rundlauf zählt in beide Richtungen ⚠️

Aus einer Rückfrage im Implementierungsfenster, nicht aus einem roten Test der neuen Regel: ein
**Bestandstest** wurde rot. D77 (c) legte fest, die Kanonizitätsprüfung stehe *nach* dem
Dekodieren, weil `is_canonical` bei undekodierbarer Eingabe wirft. Das war richtig und zu wenig.

**Der Befund.** `cbor2.loads` ist an zwei Stellen nachsichtiger, als CBOR erlaubt. Ein nacktes
Break-Byte dekodiert zu einem Sentinel-Objekt, statt zu werfen:

```
h'a1'      decode RAISE CBORDecodeEOF
h'ff'      decode ok (Sentinel), kein dict, encode RAISE CBOREncodeError
h'a100ff'  decode ok, IST ein dict,         encode RAISE CBOREncodeError
h'a1ff01'  decode ok, IST ein dict,         encode RAISE CBOREncodeError
```

Die beiden letzten schließen die naheliegende Reparatur aus — die Prüfung hinter einen
`isinstance(obj, dict)`-Test zu schieben. Sie **sind** Dicts. Es gibt keine Vorprüfung, die den
Fall abfängt.

**Beschluss:** Scheitert der Rundlauf `decode → encode` an irgendeiner Stelle mit einer
Exception, ist `v` **unlesbar** (`UNPARSABLE_VOUCH_PAYLOAD` bzw. `UNPARSABLE_V`). Liefert er ein
Ergebnis, das den Eingabebytes nicht gleicht, ist `v` **nicht kanonisch** (`NON_CANONICAL_V`).
Beide Vermerke führen in denselben Zweig aus D37: keine Kante, kein Budget-Beitrag. In Layer 03
gilt dasselbe für das Lesen der reservierten Keys.

Implementierung: `decode` und `is_canonical` stehen im **selben** `try`.

**Warum unlesbar und nicht nicht-kanonisch.** `h'a100ff'` ist kein Wert, der falsch geschrieben
wurde — es ist kein Wert. `NON_CANONICAL_V` würde behaupten, es gebe eine kanonische Form
desselben Inhalts, und die gibt es nicht. Die Wirkung ist in beiden Fällen dieselbe; die
Unterscheidung ist Diagnose, und eine falsche Diagnose schickt den Betreiber in die falsche
Richtung.

**Nicht-Map-Payloads.** Für Bytes, die kein CBOR-Map kodieren, gilt dieselbe Reihenfolge; welcher
Vermerk erscheint, hängt von der Verstoßklasse ab (`h'c11a514b67b0'` — ein Datums-Tag —
dekodiert, ist keine Map und ist nicht kanonisch, liefert also `NON_CANONICAL_V`). Die Zuordnung
ist für jede Eingabe eindeutig; das ist die Anforderung, nicht die Übereinstimmung mit der
Intuition.

**Herkunft des Fundes.** Der Implementierer hat die Frage zurückgegeben, statt sie im
Implementierungsfenster zu entscheiden — die Regel aus `§7` der Prompts hat gehalten. Es ist
der dritte Befund in Folge, der in einer **Formulierung des Prompts** lag und nicht in der
Ausführung (nach D74 und D75). Alle drei entstanden dadurch, dass eine Bedingung mit einer
plausiblen, aber unvollständigen Begründung geschrieben wurde. D77 (c) begründete die
Platzierung mit *einem* Fehlermodus; es gab zwei.

**Betroffene Dateien:** `02-trust-flow.md §3.1`, `03-profiles.md §1.3`, `02c-canon-v-prompt.md`
§3 und §5 (alle drei vollständig geliefert). `01 §7.1` bleibt unberührt — dort steht keine
Reihenfolgeaussage.

---

## S. Aus dem Abgleich mit dem tatsächlichen Code vor `03-prompt`

Vier Befunde, alle aus dem Lesen von fünf Bestandsdateien (`policy.py`, `trust/__init__.py`,
`trust/index.py`, `trust/derive.py`, `tests/helpers.py`) vor dem Schreiben des Prompts. Keiner
davon wäre beim Schreiben aufgefallen; alle vier hätten im Implementierungsfenster als Rückfrage
oder — schlimmer — als stille Umdeutung geendet.

### D84 — Eine Diagnose, ein Produzent

`03 §6.1` führte `UNSAFE_IRREVOCABLE_PREDICATE` im `ProfileFinding`-Katalog. Der Vermerk
existiert aber schon: `NucleusPolicy.__post_init__` erzeugt ihn als
`PolicyNote(PolicyWarning.UNSAFE_IRREVOCABLE_PREDICATE, predicate)` in `policy.warnings`.

**Beschluss:** Der Eintrag fällt aus dem `ProfileFinding`-Katalog. `PolicyResolution.findings`
trägt ausschließlich Befunde der **Auflösung** (`CONSTITUTION_UNAVAILABLE`,
`CONSTITUTION_HASH_MISMATCH`); die unsichere Deklaration liest der Aufrufer aus
`policy.warnings`.

Zwei Kanäle für denselben Befund tragen verschiedene Subjekte — `PolicyNote` ein Prädikat,
`Finding` eine `claim_id` — und laufen auseinander, sobald einer gepflegt wird. Die Übersetzung
wäre außerdem verlustbehaftet: es gibt keine `claim_id`, an der eine unsichere
Verfassungsdeklaration hinge.

### D85 — `INDETERMINATE` deckt auch Gabelung, nicht nur Teilwissen

D79 nannte für `INDETERMINATE` nur `pending`. `State` hat mehr: eine Obligation, deren Autor
equivokiert hat, steht in `EQUIVOCATION_FLAGGED` und ist weder aktiv noch abgelaufen noch
schwebend.

**Beschluss:** `INDETERMINATE` heißt nicht mehr „Teilwissen", sondern **„der Zustand der
Obligation erlaubt keine Aussage"**, mit zwei Ursachen und je eigenem Vermerk:

| Zustand | Vermerk | Grund |
|---|---|---|
| `pending` | `OBLIGATION_PENDING` | ich weiß zu **wenig** |
| `equivocation_flagged` | `OBLIGATION_AUTHOR_FLAGGED` | ich weiß zu **viel** |

Die zweite Zeile ist die interessantere: bei einer Gabelung existiert die Obligation womöglich
in zwei Fassungen mit verschiedenen Konditionen, und `OPEN` behauptete eine bestimmte davon.
Beide Male ist die Alternative eine Schuldbehauptung ohne Deckung — D3.

`LINKED` kommt hinzu und ist unerreichbar: es entsteht nur bei `now is None`, und `now` ist in
dieser Schicht immer ein `int`. D75-Behandlung, `assert` statt Vektor — wie `revoked` und
`superseded` unter dem Boden aus D70.

### D86 — `classify_all` wandert nach `mensch_als_republik/index.py`

`03` teilt `classify_all`, statt es zu kopieren (D69). Der Helfer lag in `trust/index.py`, was
`profiles/ → trust/` erzwungen hätte — eine Abhängigkeit quer zur Schichtung zwischen zwei
Geschwistern, von denen das eine vom anderen nichts braucht.

**Beschluss:** `classify_all` liegt in `mensch_als_republik/index.py`. Beide Schichten
importieren von dort; `trust/` re-exportiert weiter, damit die bestehende Oberfläche
unverändert bleibt.

Das Argument ist nicht Ästhetik. Der Kopplungstest `T-02.4` sichert, dass `classify_all` und
`verifier.classify` nicht auseinanderlaufen — eine Aussage über Layer 01 und ihren schnellen
Zwilling, nicht über den Trust-Solver. Der Helfer gehört dorthin, wo seine Invariante hingehört.

### D87 — `classify_all` bekommt den `policy`-Parameter ⚠️

`01a-policy-prompt.md §4` schloss ihn ausdrücklich aus: „Layer 02 wertet ausschließlich
`vouch@1` aus, und `vouch@1` kann nach D58 nie irrevocable sein — der Parameter hätte dort keine
Wirkung. Nicht anfassen."

**Der Satz stimmt für Layer 02 und trägt für Layer 03 nicht.** `settlement()` steht und fällt
damit, dass `obligation@1` **unter der Policy** klassifiziert wird. Ohne Parameter liefert
`classify_all` für den Kernvektor `SE-11` — Schuldner widerruft seine eigene Obligation — den
Zustand `REVOKED`, und `settlement()` bekäme einen Zustand, für den D79 keine Antwort vorsieht.
Das Schulden-Lösch-Loch wäre auf dem Umweg über den Helfer wieder offen.

**Beschluss:** `classify_all(store, now, policy=None)`. Layer 02 ruft weiterhin ohne auf,
Verhalten dort unverändert. Die Kopplungsinvariante erweitert sich mit:

```
∀ c ∈ store:  classify_all(store, now, policy)[claim_id(c)] == classify(c, store, now, policy)
```

**Verworfen — `03` ruft `classify()` je Claim.** Gibt die geteilte Definition von „aktiv" auf,
für die D69 und `PR-INV-10` gerade eingerichtet wurden.

**Verworfen — `03` rechnet den Irrevocable-Fall nach.** Die Regel stünde zweimal da. Genau die
Duplikation, gegen die `T-02.4` gebaut wurde.

D86 und D87 sind derselbe Eingriff: die Verschiebung ist damit keine Aufräumarbeit, sondern
notwendig.

---

**Muster, vierter Fall.** D74, D75, D83 und jetzt D87 haben dieselbe Form: eine Bedingung, deren
Begründung im damaligen Kontext trug und im nächsten nicht mehr. Bei D87 war die Begründung
sogar wörtlich richtig — sie sagte „Layer 02", und niemand las mit, dass sie damit ihren eigenen
Geltungsbereich benannte. Konsequenz für den Sitzungsabschluss vorgemerkt, nicht hier
entschieden.

---

## T. Aus den Rückfragen zum `03`-Lauf

Drei Befunde aus dem Implementierungsfenster, alle zurückgegeben statt entschieden. Der erste
ist eine echte Lücke, der zweite ein Widerspruch in derselben Datei, der dritte eine
Unbestimmtheit.

### D88 — Testidentitäten kommen aus festen Seeds, der Helfer bekommt einen Konstruktionspfad dazu

`tests/helpers.py::Identity` leitet den Schlüssel aus einem **Label** ab. Die Anker in
`00 §3.1` und `03-golden-anchors.md §3.1` stammen aus den Seeds `01×32`, `02×32`, `03×32`. Beide
treffen sich nicht — `Identity("ALICE")` liefert `3e18794e…`, die Spec verlangt `8a88e3dd…`.

**Verworfen — das Ankerdokument auf Label-Seeds umstellen.** Die Seeds sind normativ: sie stehen
in `00 §3.1`, und `tests/vectors/vectors_01.json` trägt `8a88e3dd…` und `8139770e…` bereits als
Bytes. Es bräche einen eingefrorenen Vektorsatz.

**Verworfen — ein eigener Fixture-Helfer für `tests/profiles/`.** Das wäre eine zweite
Implementierung von Kettenfortführung, Signatur und `h_prev`. Zwei Implementierungen desselben
Dings driften — dieselbe Begründung, mit der D86 `classify_all` teilt statt kopiert.

**Beschluss:** `Identity.__init__(self, label, *, seed=None)`. Bei `seed is None` bleibt die
Label-Ableitung; bestehende Aufrufe ändern sich nicht. Ein Konstruktionspfad, ein Label für die
Lesbarkeit, ein optionaler Seed für die Fälle, in denen der Schlüssel normativ ist.

**Die drei Seeds bekommen genau eine Definition** — in `tests/helpers.py`. Wo sie heute ein
zweites Mal stehen (`tests/vectors/gen.py`), kommen sie von dort. Konstanten an zwei Stellen
sind die Bauform, die in dieser Sitzung viermal einen Befund erzeugt hat.

### D89 — `verdict_status()` gibt `VerdictResult` zurück, nicht den Enum

`03 §2.4.2` schrieb `-> VerdictStatus` mit zwei Werten; `03 §11` (`PR-INV-9`) verlangte
`findings` in **allen vier** Ergebnistypen. Zwei Sätze derselben Datei, die sich widersprechen —
gefunden nicht durch Nachdenken, sondern beim Versuch, beide gleichzeitig zu erfüllen.

**Beschluss:** `VerdictResult(status: VerdictStatus, findings: tuple[Finding, ...])`.
`VerdictStatus` bleibt zweiwertig — die Zweiwertigkeit ist eine Aussage über den **Status**, nicht
über den Rückgabetyp (D67 hält).

Der Widerspruch war folgenreich und nicht kosmetisch: `VS-7` (`SCOPE_MISMATCH`), `VS-8`
(`UNRESOLVED_ACCUSED`) und `VS-9` (`INACTIVE_VERDICT`) liefern alle `ATTRIBUTED_OPINION` und
unterscheiden sich **ausschließlich** im Vermerk. Ohne Kanal wären drei Vektoren nicht prüfbar,
und `03 §2.4.4` — „Teilwissen senkt, was ich behaupten kann" — bliebe unbelegbar.

### D90 — `subject` ohne Claim ist der deklarierte `constitution_hash`

`CONSTITUTION_UNAVAILABLE` und `CONSTITUTION_HASH_MISMATCH` betreffen keinen Claim. `03 §6`
verlangt trotzdem ein Subjekt (D74).

**Beschluss:** `subject = genesis_obj[4]`, der im Genesis **deklarierte** `constitution_hash`.

Nicht der **berechnete** Hash des übergebenen Objekts: der ist eine Eigenschaft dessen, was der
Aufrufer gereicht hat, und wechselt mit jedem falschen Objekt. Der deklarierte Hash ist der
stabile Bezeichner und der, unter dem ein Betreiber suchen würde.

Nicht `scope`: der steht bereits im Aufruf, und ein Subjekt, das für alle Vermerke desselben
Aufrufs gleich ist, trägt keine Information. Nie ein Leerwert — das war der Befund, der D74
ausgelöst hat.

**Allgemeine Regel, hier zum ersten Mal ausgeschrieben:** `subject` ist in der Regel eine
`claim_id`; wo kein Claim betroffen ist, ist es das **Objekt, um das es geht**, in der Form, in
der der Betreiber es benennen würde.

---

### D91 — Die Policy wird scope-lokal angewandt ⚠️

Aus dem `03`-Lauf, zurückgegeben statt entschieden. `classify_all(store, now, policy)` wirft bei
jedem `nuc:`-Claim mit `N != policy.scope`, weil D73 genau das für einen einzelnen Claim
verlangt. Damit ist **jeder Store mit mehr als einem Nukleus unklassifizierbar** — und die
Vektoren `SE-5`, `MB-9` und `VS-7` legen fremd-gescopte Claims ausdrücklich in denselben Store,
weil sie prüfen, dass `03 §1.4` sie nicht zählt.

**Der Fehler liegt in D87, nicht in D73.** D73 entschied über `classify(claim, …)`: dort behauptet
der Aufrufer für **einen** Claim, diese Policy gelte für ihn, und eine Fehlpaarung ist eine
falsche Zuordnung ohne sichere Voreinstellung. D87 hat den Parameter an `classify_all`
weitergereicht, ohne zu bedenken, dass diese Funktion über einen **heterogenen Bestand** läuft
und gar nichts behauptet.

**Beschluss:** `classify_all` wendet `policy` auf genau die Claims an, für die sie definiert ist
— `nuc:`-Prädikate mit `N == policy.scope`. Alle übrigen klassifiziert sie mit `policy=None`.
D73 bleibt für `classify()` unverändert in Kraft.

Kopplungsinvariante entsprechend zweiteilig (`PR-INV-11`), dazu `PR-INV-12`: `classify_all`
wirft nie, gleich wie viele Nuklei der Store trägt.

**Getragene Grenze.** Der Zustand eines fremd-gescopten Claims ist damit policy-frei bestimmt
und kann für dessen eigenen Nukleus falsch sein. Er ist nirgends tragend: jede Beziehung dieser
Schicht verlangt `N == scope` (D81), und der einzige Claim, der außerhalb des Scopes gelesen
wird — der bestrittene Claim in D67 (b) — wird nur nach seinem **Autor** gefragt, nie nach
seinem Zustand. Wer das ändert, muss diese Zeile mit ändern.

**Verworfen — gefilterter Store-Wrapper.** Der Implementierer hat ihn gebaut und wieder
entfernt, richtigerweise: er nimmt den drei Vektoren genau die Claims weg, deren Nichtzählen sie
prüfen. Ein Filter, der das Prüfobjekt entfernt, macht den Test grün und die Aussage leer.

**Fünfter Fall desselben Musters** (nach D74, D75, D83, D87): eine Bedingung, deren Begründung
im ursprünglichen Kontext trug — ein Claim, ein Aufrufer, eine Behauptung — und beim Übertragen
auf einen anderen Kontext still ihren Geltungsbereich verlor. Diesmal war der Übertragende ich,
im selben Register, vier Einträge später.

---

## U. Aus der `03`-Abnahme

Drei Beschlüsse aus sechs Befunden. Die anderen drei (`_dedupe_sort`-Benennung, `KeyError` statt
`ValueError` im Verdikt, `KeyError` bei defektem Genesis) sind Ausführung und brauchen keinen
Registereintrag — sie fallen unter D92 bzw. sind kosmetisch.

### D92 — Der bewertete Claim wird an der Eingangstür geprüft ⚠️

`03 §1.4` normierte Scope-Gleichheit für **Beziehungen zwischen zwei Claims** —
`receipt` ↔ `obligation`, `accept-rules` ↔ `grant-membership`, `submit-arbitration` ↔ `verdict`.
Für den Claim, den eine Funktion als **Argument** entgegennimmt, stand die Regel nur bei
`settlement()` (`§3.3.2`) und nirgends allgemein. `verdict_status()` hatte sie deshalb nicht.

**Die Folge war real.** Ein Verdikt aus Nukleus B, mit `scope = N_A` ausgewertet, wurde nicht
abgewiesen: steht sein Autor in A's Arbitratorenliste, lautete die Antwort `BINDING`. Ein
anerkannter Schiedsrichter sitzt typischerweise in mehreren Nuklei — der Fall ist der Normalfall.

**Beschluss:** Jede Funktion dieser Schicht, die einen Claim als Argument nimmt, prüft als
Erstes: erwartetes Prädikat, `N == scope`, im Store. Sonst `ValueError`, vor jedem weiteren
Zugriff. Vektoren `VS-13`, `VS-14`, Invariante `PR-INV-13`.

**Der Unterschied zum Beziehungsfall ist die Herkunft des Claims.** Einen Claim, den ich im
Bestand *finde*, darf ich nicht zählen — Vermerk, weiter. Bei einem, den der Aufrufer mir
*reicht*, hat er eine Behauptung aufgestellt, die falsch ist, und dafür gibt es keine sichere
Voreinstellung (D73). Dass diese Unterscheidung nirgends stand, ist der ganze Befund.

Derselbe Beschluss deckt das defekte Genesis-Objekt ab: `resolve_policy` bekommt es gereicht,
also wirft es, statt still in einen `KeyError` zu laufen (Vektor `P-G`).

### D93 — `EXPIRING_OBLIGATION` erscheint unbedingt, nicht beim Verfall

Der Vermerk stand im `EXPIRED`-Zweig und erschien damit genau dann, wenn er wertlos ist: nach
dem Erlöschen sagt `EXPIRED` es ohnehin.

`03 §3.3.1` begründet ihn damit, dass `t_exp` dem Gläubiger **vor der Gegenleistung** sichtbar
sein soll — die einseitige Obligation hat keine signierte Annahme, er trägt die Prüfpflicht
allein.

**Beschluss:** `obligation.t_exp is not None` ⇒ `EXPIRING_OBLIGATION`, unabhängig vom Zustand.
Vektor `SE-13`: aktive Obligation mit `t_exp` in der Zukunft, `OPEN` plus Vermerk.

Die Fehlform ist notierenswert, weil sie nicht falsch *aussah*: die Bedingung stand in einem
Zweig, der sie erwähnt, statt an der Stelle, an der sie gilt. Ein Vermerk, der nur im
Schadensfall erscheint, ist kein Warnhinweis, sondern ein Nachruf.

### D94 — Vier Nicht-Auflösbar-Fälle, drei Vermerke

`03 §2.4.4` sagte „mit dem entsprechenden Vermerk", ohne die Zuordnung auszuschreiben. Die
Implementierung wählte für **alle** Fälle `UNKNOWN_ACCUSATION`, auch für eine Anklage aus
fremdem Scope.

**Beschluss:**

| Lage | Vermerk |
|---|---|
| `verdict.J.tag` ist nicht `claim-ref` | `UNKNOWN_ACCUSATION` |
| Anklage lokal unbekannt | `UNKNOWN_ACCUSATION` |
| Anklage in einem anderen Nukleus | `SCOPE_MISMATCH` |
| bestrittener Claim lokal unbekannt | `UNRESOLVED_ACCUSED` |

Die dritte Zeile ist der Grund für die Tabelle: eine Anklage aus fremdem Scope ist **bekannt**
und zählt nur nicht. `UNKNOWN_ACCUSATION` schickte den Betreiber in die Partitionsecke, während
das Objekt vor ihm liegt. Wirkung identisch, Diagnose entscheidend — dritte Wiederholung von
D74. Vektor `VS-12`.

---

**Neue Fehlerform.** D74, D75, D83, D87 und D91 hatten dieselbe Bauart: eine Begründung verlor
beim Übertragen still ihren Geltungsbereich. D92 ist anders — die Regel wurde **gar nicht erst
übertragen**. `settlement()` und `verdict_status()` nehmen beide einen Claim entgegen, bewerten
ihn im Scope und geben Zustand plus Vermerke zurück; sie hätten dieselbe Eingangsstrecke haben
müssen. `§3.3.2` hat sie ausgeschrieben, `§2.4.2` nicht, weil beim Schreiben von `§2.4` die
Bindungsfrage im Vordergrund stand und nicht die Eingangsprüfung.

Drei der sechs Abnahmebefunde waren Asymmetrien zwischen genau diesen beiden Funktionen.

---

## V. Vor Layer 04 — Verfassungsdefekte, Epochen, Auszählung

Acht Beschlüsse. D95 stammt aus dem `03a`-Lauf; D96 bis D102 entstehen aus der Forkanalyse für
Layer 04 und aus einer Recherche zum Stand der Technik, die zwei eigene Vorschläge widerlegt hat.

### D95 — Formwidriger Eintrag in `irrevocable_predicates`

Gemessen im `03a`-Lauf: eine Verfassung, die statt eines Arrays den Text `"obligation@1"` trägt,
wird in `resolve_policy` über `frozenset(raw)` still zu einer Menge von zwölf Einzelzeichen. Der
Hash stimmt, das Objekt ist richtig zugeordnet, die Wirkung ist heute harmlos — Müll trifft
keinen echten Prädikatnamen, und der Boden `obligation@1` (D70) hält unabhängig davon.

Die Harmlosigkeit ist allerdings zufällig: sie beruht darauf, dass kein Prädikatname aus einem
Zeichen besteht. Sie ist keine zugesicherte Eigenschaft.

**Kein `ValueError`.** D92 lässt werfen, wenn ein gereichtes Objekt **fehlzugeordnet** ist. Hier
ist die Zuordnung korrekt und der Defekt liegt im Inhalt. Also die D37/D70-Bewegung: der defekte
Teil fällt weg, der Rest gilt.

**Beschluss:**

- Formkriterium, bedeutungsblind: ein Eintrag ist wohlgeformt, wenn er ein `str` ist, genau ein
  `@` enthält, beidseits davon nicht leer ist und weder `/` noch `:` trägt. Alles andere fällt
  heraus.
- Vermerk `PolicyWarning.MALFORMED_IRREVOCABLE_ENTRY`, Subjekt ist der Eintrag selbst, bei
  Nicht-`str` als `repr`. **Nicht** in `PolicyResolution.findings` und **nicht** mit dem
  `constitution_hash` als Subjekt: D84 hat für den strukturgleichen Fall in derselben Liste
  bereits `policy.warnings` mit dem Eintrag als Subjekt festgelegt. Zwei Defekte einer Liste über
  zwei Kanäle zu führen wäre die D92-Asymmetrie.
- Ort ist `NucleusPolicy.__post_init__`, nicht `resolve_policy`. D72 hat Boden und Filter genau
  deshalb in den Konstruktor gelegt: ein Aufrufer, der die Klasse von Hand baut, darf keine
  unsichere Menge erzeugen können. Läge die Prüfung im Resolver, umginge sie jeder Testaufbau —
  derselbe Umgehungsvorwurf, mit dem D57 den Wrapper verworfen hat.
- `resolve_policy` reicht den gelesenen Wert **unverändert** weiter und zwingt ihn nicht mehr
  vorab in ein `frozenset`. Der Konstruktor nimmt ein `Iterable[object]` entgegen. Ist der Wert
  gar nicht iterierbar, gilt die Liste als vollständig ausgefallen: leere Menge plus ein Vermerk.

Damit hat die Liste drei Ausschlussgründe mit drei Behandlungen: `core/*` still ignoriert (D71),
unsicher mit Vermerk (D58), formwidrig mit Vermerk (D95). Wirkung gleich, Diagnose verschieden —
D94.

**Vektoren:** `P-7` Zeichenmenge aus einem Textwert; `P-8` Eintrag, der kein `str` ist; `P-9`
Eintrag mit Scope-Präfix, etwa `nuc:N/obligation@1`. Der dritte ist der wichtigste: `01 §5.4.2`
verlangt Profilnamen **ohne** Präfix, der Fehler ist der wahrscheinlichste echte Betreiberfehler,
und heute schützt so ein Eintrag lautlos niemanden.

**Nebenbefund.** `frozenset(42)` wirft heute einen unbehandelten `TypeError`. Nach D92 hätte ein
gereichtes defektes Objekt einen definierten Ausgang; er fehlte. Der Beschluss oben schließt das
mit ein.

### D96 — Epochenkette statt Snapshot ⚠️

`04 §4.2` band die Auszählung an einen Snapshot: eine Merkle-Wurzel über die `claim_id` der zum
Zeitpunkt der Vorschlagserstellung aktiven Vouch-Kanten, mit der Behauptung, die Auszählung sei
damit deterministisch und Uneinigkeit reduziere sich auf fehlende Claims.

**Die Behauptung hält aus drei unabhängigen Gründen nicht.**

1. Die Wurzel bindet `claim_id`, nicht Aktivität. Aktivität ist eine Funktion von Bytes, Store,
   `now` und Policy. Nach E-A trägt jeder Vouch in einem Budget-Scope ein `t_exp`, und `01 §6`
   erklärt genau den Ablauf zum einzigen legitimen Uneinigkeitsfall. Zwei Beobachter mit
   identischem Snapshot und identischem Bestand rechnen verschiedene Kantensätze. Wegen
   `C = C0 * gamma^d` verschiebt eine ablaufende Brückenkante die Kapazität eines ganzen
   Teilbaums exponentiell.
2. Der Seed ist selbst `now`-abhängig. `§4.2` nannte ihn genesis-deklariert; D23 verlangt
   `t_exp` und Neuerklärung, und der Ablauf fällt nach `02 §6.3` auf das **persönliche**
   Ankerset zurück. Läuft die Nukleus-Linse während einer Abstimmung ab, divergiert die
   Auszählung nicht, sie wird pro Beobachter beliebig.
3. Der Snapshot deckt die falsche Menge. Der Nenner einer Schwelle ist die stimmberechtigte
   Menge; die steht nicht darin und ist unter Teilwissen unter-bekannt. Ein zu kleiner Nenner
   macht die Schwelle **leichter** erreichbar — die Über-Ratifizierungsrichtung, also die
   Umkehrung von `02 §7`.

**Die Folge reicht über `04` hinaus.** D72 hält fest, abweichende Verfassungen für dasselbe `N`
seien kein legitimer Uneinigkeitsfall, weil die Ratifizierung selbst prüfbar ist, und schließt
daraus, `expired` bleibe der einzige Zustand, in dem zwei korrekte Verifizierer uneins sein
dürfen. Ist die Auszählung `now`-abhängig, wandert `expired` durch die Ratifizierung in die
Policy, und `01` Anhang B ist nicht mehr deterministisch gegeben dieselben Bytes und dieselbe
Policy, sondern gegeben dieselbe Uhr.

**Der erste Reparaturversuch war falsch und wird mitprotokolliert.** Vorgeschlagen war, den
Snapshot total zu machen: zwei Merkle-Wurzeln, `t_exp` innerhalb der Auszählung nicht
ausgewertet. Das funktioniert formal, verschiebt die Koordination aber auf den Vorschlagenden,
der damit auch die Wählerschaft aussucht. Nach dem CALM-Theorem hat ein Problem genau dann eine
konsistente koordinationsfreie Implementierung, wenn es monoton ist; ein nicht-monotones Problem
wird nicht dadurch monoton, dass man seine Eingabemenge einfriert — die Koordination taucht an
anderer Stelle wieder auf. Hier tauchte sie als Agenda-Macht auf.

**Beschluss:** Der Snapshot entfällt ersatzlos. `§4.2` wird gestrichen.

An seiner Stelle steht die **Epochenkette**:

- Eine Epoche beginnt mit einem ratifizierten Verfassungsobjekt. Der Genesis ist Epoche 1.
- Die stimmberechtigte Menge `P` und die Schwelle stehen in der Verfassung der laufenden Epoche.
  `P` wird deklariert, nie aus dem Bestand abgeleitet: eine abgeleitete Menge wäre unter
  Teilwissen unter-bekannt, und das ist die gefährliche Richtung.
- Eine Stimme ist ein Claim, gebunden an Instanz, Epoche und Vorschlag.
- Eine Entscheidung ist ein Claim, der die zählenden Stimmen mitführt. Jeder Beobachter prüft
  ihn offline gegen die Epochenverfassung. Kein `now`, keine Merkle-Wurzel über Vouch-Kanten.

`P` als Verfassungsfeld ist **optional**, damit das kanonische Beispiel es weglässt und `N`
byte-identisch bleibt (`65309fe2…`). Ein Nukleus ohne deklariertes `P` ist nicht auszählbar; die
Anker für `04` brauchen deshalb ein eigenes Profil.

**Getragene Grenze.** Die Epochenverfassung ist ein Stand, kein Livewert. Wer nach ihrer
Ratifizierung aufgenommen wird, stimmt erst in der nächsten Epoche mit.

### D97 — Stimmen sind innerhalb einer Epoche unwiderruflich

Damit die Auszählung monoton bleibt, darf die Stimmenmenge nur wachsen. Ein Widerruf oder ein
ausgewertetes `t_exp` lässt sie schrumpfen und macht das Prädikat nicht-monoton — womit D96
wieder aufgehoben wäre.

**Beschluss:** Eine Stimme in einer laufenden Epoche ist unwiderruflich. Ihr `t_exp` wird nicht
ausgewertet; trägt sie eines, bleibt es folgenlos. Die Verhältnismäßigkeit zu E-A ist beim
Schreiben von `04` gegen `02 §6.2` zu prüfen: bindet `vote@1` kein Budget, greift E-A nicht.

**Verhältnis zu D58.** Dem Wortlaut nach kollidiert das mit dem Verbot unwiderruflicher
vertrauensgewährender Prädikate; dem Kriterium nach nicht. D58 fragt, ob **Fortbestehen** die
konservative Lesart ist. In einem Verfahren, in dem der Status quo der Default ist und eine
Stimme sich nur von ihm weg bewegen kann, hält Fortbestehen eine getroffene Entscheidung, statt
Vertrauen künstlich am Leben zu erhalten. Eine Stimme gewährt zudem keine fortdauernde Autorität,
sondern ist ein einmaliger Akt — anders als `vouch@1` und `submit-arbitration@1`.

**Was an die Stelle des Ablaufs tritt.** Ein `t_exp` darf auf dem **Vorschlag** stehen und wird
von den Abstimmenden gelesen, nicht vom Protokoll ausgewertet. Uhren informieren Verhalten, nie
Gültigkeit.

### D98 — Auszählung nach Kopfzahl; `weight_mode = 1` vertagt

`04 §4` sah eine gewichtete Auszählung über dem Vertrauensgraphen vor. Sie fällt für v1 aus drei
Gründen, von denen der dritte allein trägt.

1. Gewichte aus dem Graphen sind keine Eigenschaft der Epoche; an ihnen hing die ganze
   `now`-Kette aus D96.
2. Der Zweckbegriff aus `§4.1` verlangt den Vouch-Zweck-Tag, der mit D56 vertagt ist. `§4` war
   in seiner bisherigen Form nicht implementierbar.
3. Ein Stimmgewicht ist eine übertragbare, akkumulierbare Größe, sobald jemand bemerkt, dass es
   sich lohnt. Vertrauen ist in diesem Protokoll ein Flussverstärker und kein Zahlungsmittel
   (`08 §4`); die gewichtete Auszählung verwandelt es in genau das, was es nicht sein darf. Das
   ist derselbe Einwand, mit dem D25 Ansehen von Torwächterschaft trennt.

**Beschluss:** Auszählung nach Kopfzahl über deklariertem `P`. `weight_mode = 1` bleibt im
Genesis-Schema zulässig, ist in v1 aber nicht ausgewertet; ein Nukleus, der es setzt, bekommt
kein Ergebnis, sondern den unentschiedenen Zustand.

**Was dabei nicht verloren geht.** `04 §4` verortet den Sybil-Schutz bei der **Mitgliedschaft**,
nicht beim Gewicht. Der Vertrauensgraph bleibt in voller Wirkung als das, was Mitglieder bei der
Aufnahmeentscheidung lesen. Er ist nur nicht mehr das, was das Protokoll multipliziert.

**Getragene Grenze.** Die zweck-gescopte Gewichtung war eine eigenständige Idee des Entwurfs. Sie
wird nicht widerlegt, sondern aus der Schicht genommen: sie ist Policy und keine Infrastruktur.

### D99 — Epochenidentität über dem Ergebnis, nicht über dem Beleg

Zwei ehrliche Mitglieder können dieselbe gesättigte Entscheidung unabhängig materialisieren, mit
verschiedenen Zeugenmengen — beide gültige Supermajoritäten, beide auf dasselbe Ergebnis. Steckt
die Zeugenmenge im gehashten Objekt, sind das zwei Identitäten für eine Entscheidung, und die
Verfassungskette spaltet sich ohne jedes Fehlverhalten.

**Beschluss:** Die Epochenidentität hasht das Ergebnis, nicht den Beleg.

```
epoch_id = SHA-256( DOM_NUC_EPOCH || cbor_deterministic([N, i, constitution_hash_neu]) )
```

Die Zeugenmenge reist daneben als austauschbarer Beleg. Zwei Materialisierungen desselben
Ergebnisses sind damit zwei Claims über dieselbe Epoche, und wer beide sieht, sieht keinen
Widerspruch.

Dieselbe Fehlerform wie D92 — zwei Wege, die dasselbe tun sollen, und nur einer trägt die Regel.
Diesmal vor der Abnahme gefunden.

### D100 — Die Stimme bindet an das Vorschlagsobjekt; Schließung durch Epochenwechsel

Ein Stichtag setzt voraus, dass zwei Beobachter sich einig sind, welche Stimmen davor abgegeben
wurden. Das `t`-Feld setzt der Autor selbst, und `01 §5.3` nimmt die Ordnung ausschließlich aus
der Autorenkette. Eine Frist würde von genau der Person durchgesetzt, die sie binden soll; und
selbst bei ehrlichen Uhren ist „zu spät abgegeben" von „zu spät zugestellt" nicht unterscheidbar,
womit die Frist zur Waffe dessen wird, der Zustellung verzögern kann. Ein Wahllokal ist eine
Autorität in Konventionsform. Mit ihr fällt die Frist.

**Beschluss:**

- Eine Stimme gilt einem **konkreten Vorschlagsobjekt**, nie einer Sachfrage. Wer seine Meinung
  ändert, holt seine Zustimmung zu diesem Objekt nicht zurück — sie hilft aber auch nur diesem
  Objekt.
- Eine Abstimmung wird nicht durch Zeit geschlossen, sondern durch den **Epochenwechsel**:
  Stimmen sind an Instanz, Epoche und Vorschlag gebunden, und mit der Materialisierung einer
  Entscheidung sind alle Stimmen der alten Epoche erledigt.
- Wer nicht abstimmt, senkt den Nenner nicht. Nichtteilnahme wirkt wie Ablehnung. Die Schwelle
  gilt gegenüber den **Berechtigten**, nicht gegenüber den Erschienenen.

**Getragene Grenze.** In einer Epoche, in der nichts durchgeht, hängt ein Vorschlag unbegrenzt.
Eine Entscheidung bildet damit gesetzte Zustimmung ab und nicht, wer an einem bestimmten Tag
besser mobilisiert hat. Für `example-nucleus.md`: eine hohe Schwelle bei lauer Beteiligung macht
die Verfassung faktisch unveränderlich; die Schwelle ist gegen realistische Beteiligung zu wählen.

**Verworfen — Zeugenquorum für Fristen.** Die Verfassung könnte `k` Zeugen benennen, die Stimmen
mit ihrer beobachteten Zeit gegenzeichnen; rechtzeitig wäre, was ein Zeugenquorum bestätigt.
Scope-lokal, also kein Bruch von „nie global", und additiv nachrüstbar. Für v1 verworfen: es
schafft eine Rolle mit Verfügbarkeitsanforderung und einen neuen Fehlermodus, denn kolludierende
Zeugen können Stimmen ausschließen. Zensur ist schlimmer als Hängenbleiben.

### D101 — Nein ist arithmetisch neutral und trotzdem ausgezeichnet

Würde die Schwelle gegen `Ja + Nein` gerechnet, könnte eine hinzukommende Nein-Stimme ein bereits
wahres Ergebnis wieder falsch machen. Der feste Nenner `n = |P|` ist es, der es überhaupt
erlaubt, das Nein aufzuschreiben: **wir können es uns leisten, weil es nicht mitzählt.**

**Beschluss:** Drei Antworten — Ja, Nein, keine Äußerung. Nein und Nichtteilnahme wirken gleich;
sie werden getrennt geführt, weil die Diagnose verschieden ist (D94). Mit `n = |P|` und der
Schwelle `num/den` gilt, in exakter Integer-Form ohne Division:

```
durchgekommen:   |Ja| * den   >  num * n
gescheitert:     (n - |Nein|) * den   <=   num * n
```

Beide Mengen wachsen nur, beide Bedingungen sind einmal wahr für immer wahr, und sie schließen
einander aus. Drei Zustände, zwei davon absorbierend, ohne jede Frist. Ein Vorschlag scheitert
daran, dass genug Berechtigte ihn ausdrücklich ablehnen — nicht daran, dass ein Tag vorbei ist.

**Höchstens ein Ja je Mitglied je Epoche. Neins beliebig viele.** Gegen mehrere Vorschläge
gleichzeitig zu sein ist kohärent; zwei verschiedene Dokumente gleichzeitig als das geltende zu
benennen ist es nicht. Niemand muss Nein zu A sagen, um Ja zu B sagen zu können, und ein Ja zu A
wird B **nicht** als Nein angerechnet.

**Abgrenzung zu `03`.** `membership()` löst mehrere aktive `accept-rules` mit `min(claim_id)` auf,
weil alle dasselbe sagen. Zwei aktive Stimmen desselben Autors sagen Verschiedenes: dann zählt
**keine**, plus Vermerk — die Parallele ist `02 §2`, wo ohne gültige Belegung keine Kante
entsteht. Wer `03` als Vorbild liest, harmonisiert das falsch; der Prompt muss es ausschreiben.

**Getragene Grenze.** Ein Vorschlag ist damit ein Bündel — eine ganze Verfassungsversion, nicht
eine einzelne Regeländerung. Der feinere Weg, Änderungen je Slot mit unabhängiger Geltung, bringt
Parallelität, erlaubt aber die Teilannahme eines Pakets und braucht eine Slot-Zerlegung. Grob
gebündelt und fein zerlegt sind beide sicher; gefährlich ist das Mischen.

### D102 — Rivalisierende Nachfolger sind arithmetisch unmöglich ⚠️

**Dieser Eintrag ersetzt einen eigenen Fehler.** Zunächst war beschlossen worden, bei zwei
Entscheidungen auf derselben Epoche setze sich die **erste Materialisierung** durch. Beim
Nachlesen von Rafts Konfigurationswechsel fiel auf, dass „zuerst" hier keine Bedeutung hat: zwei
Materialisierungen sind Claims verschiedener Autoren, und zwischen ihnen gibt es keine Ordnung.

Es ist derselbe Fehler, den Ongaro 2015 für Rafts Einzelserver-Wechsel dokumentiert hat: zwei
nebenläufige konkurrierende Konfigurationsänderungen können Quoren haben, die sich nicht
überschneiden, und erzeugen Split Brain. Die Produktionsantwort dort ist Serialisierung — höchstens
eine uncommittete Konfiguration zur Zeit —, die theoretische ist Joint Consensus, bei dem je zwei
konkurrierende Konfigurationen eine gemeinsame haben und sich deshalb überschneiden.

**Geprüft und verworfen: kleinster `epoch_id` gewinnt.** Deterministisch, uhrenfrei und sogar
konvergent, weil das Minimum über einer wachsenden Menge einen Halbverband bildet. Aber ein
Beobachter, der unter A gehandelt hat und später ein kleineres B lernt, muss zurückrollen. Das ist
Fork Choice mit Reorg und steht quer zu allem, wofür dieses Protokoll gebaut ist.

**Beschluss:** Es braucht keine Auflösung, weil der Fall nicht eintreten kann. Aus D101 folgt
höchstens ein Ja je Mitglied je Epoche; bei einer Schwelle über der Hälfte müssten sich die
Ja-Mengen zweier rivalisierender Versionen überschneiden, und niemand hat zweimal Ja gesagt. Zwei
gültig ratifizierte Nachfolger derselben Epoche sind arithmetisch unmöglich, solange kein Mitglied
doppelt gestimmt hat — und Doppelstimmen sind nach D101 nicht bloß verboten, sondern zählen nicht.

Das ist das Überschneidungsargument aus Joint Consensus, nur aus dem Stimmverhalten geholt statt
aus der Konfiguration. Damit entfällt auch der Fall, um dessentwillen der Eintrag begonnen wurde:
einen unterlegenen Vorschlag mit echter Supermajorität kann es nicht geben.

---

**Zur Fehlerform dieses Abschnitts.** D96 und D102 sind beide eigene Vorschläge, die an
Bestandsliteratur gescheitert sind — der erste am CALM-Theorem, der zweite an einem zehn Jahre
alten Raft-Befund. Beide Male war der Vorschlag intern stimmig und die widerlegende Eigenschaft
lag außerhalb des Registers. Das ist eine andere Bauart als D74 bis D92, wo die Begründung beim
Übertragen ihren Geltungsbereich verlor.

**Konsequenz — Standprüfung:** Bevor ein Mechanismus normiert wird, der Nebenläufigkeit,
Ordnung oder Schwellen betrifft, wird gefragt, unter welchem Namen dieses Problem außerhalb des
Projekts gelöst ist. Die beiden Fälle hier haben je eine Runde gekostet; ohne die Recherche
hätten sie eine Abnahme gekostet.

---

## W. Nachzug zu Layer 04 — Auflösbarkeit, Klassen, Unwiderruflichkeit

Drei Beschlüsse aus dem Entwurf des Modulschnitts. Alle drei sind Lücken, die beim Schreiben von
`04-governance.md` nicht sichtbar waren und erst auftraten, als die Signaturen der Funktionen
neben den Zustandsautomaten aus Layer 01 gelegt wurden.

### D103 — Unauflösbare Epochenzugehörigkeit einer fremden Ja-Stimme

`04 §4.4` verlangt, dass zwei aktive Ja-Stimmen desselben Autors auf verschiedene Vorschläge
**derselben Epoche** beide nicht zählen. Aus dieser Regel folgt D102: bei einer Schwelle über der
Hälfte können zwei rivalisierende Nachfolger keine getrennten Ja-Mengen haben.

Eine Stimme trägt aber nur `J = (3, proposal_hash)`. Die Epochenzugehörigkeit steht in
`proposal[1]`. Ist das Vorschlagsobjekt lokal unbekannt, ist die Bedingung nicht auswertbar, und
`04 §4.4` sagte dazu nichts.

**Beschluss:** Eine aktive Ja-Stimme auf einen lokal unbekannten Vorschlag gilt als
**möglicherweise epochengleich** und blockiert die andere Ja-Stimme desselben Autors. Vermerk
`UNKNOWN_PROPOSAL`, Subjekt die `claim_id` der unauflösbaren Stimme.

Die Richtung ist erzwungen: die Gegenannahme — unbekannt heißt fremde Epoche, also kein Konflikt —
lässt bei Teilwissen zwei gültige Nachfolger derselben Epoche entstehen. Das ist die
Über-Ratifizierungsrichtung, die `INV-04.3` ausschließt.

**Getragene Grenze.** Eine Ja-Stimme auf einen Vorschlag, dessen Objekt nie verbreitet wurde,
setzt ihren Autor für diese Epoche aus. Heilbar, indem jemand das Objekt nachreicht — es ist
content-adressiert und nicht fälschbar. Verhindern kann das Mitglied es nicht.

**Verworfen — die Epoche in der Stimme führen.** `vote.v` könnte einen Key `1` mit dem `epoch_id`
tragen; dann wäre die Zugehörigkeit ohne das Vorschlagsobjekt auswertbar. Verworfen, weil es eine
zweite Darstellung desselben Zustands neben `proposal[1]` schafft, die ihr widersprechen kann.
Zwei Darstellungen desselben Zustands haben in diesem Projekt viermal einen Befund erzeugt; bei
Widerspruch zählte die Stimme dann ohnehin nicht, und der Fall wäre nur verschoben.

### D104 — Die Reihenfolge der Schwellenklassen ist normativ

`04 §3.4` verweist für die Klasse eines allgemeinen Vorschlags auf `genesis[5]`, einen `uint`. Das
Beispiel in `00 §3.1` trägt den Wert `2` und eine Verfassung mit drei benannten Schlüsseln in
`thresholds`. Welcher Index welchen Namen bezeichnet, stand nirgends — die Zuordnung war
offensichtlich und unaufgeschrieben.

**Beschluss:** `0 = ordinary`, `1 = membership`, `2 = amendment`.

Fehlt der benannte Schlüssel in `thresholds`, ist der Vorschlag nicht auszählbar. Ein Index über
`2` ist ebenfalls nicht auszählbar und wird **nicht** auf `amendment` zurückgeführt: ein unbekannter
Index ist ein unbekannter Wille, und die sichere Richtung ist, keine Ratifizierung zu erzeugen.

### D105 — `vote@1` ist irrevocable; `t_exp` macht eine Stimme ungültig ⚠️

D97 verlangt, dass eine Stimme innerhalb einer Epoche unwiderruflich ist und ihr `t_exp` nicht
ausgewertet wird. `04 §3.1` Bedingung 5 verlangte, dass eine zählende Stimme nach `classify_all`
`ACTIVE` ist.

**Beides zusammen geht nicht.** `_classify_one` liefert für eine widerrufene Stimme `REVOKED` und
für eine abgelaufene `EXPIRED`. Wer Bedingung 5 wörtlich umsetzt, hat eine schrumpfende
Stimmenmenge — und damit fallen D96, D101 und D102 gemeinsam, weil alle drei auf der Monotonie der
Ja- und Nein-Mengen stehen.

Der naheliegende Ausweg wäre eine eigene Aktivitätsdefinition in `04`. Er ist versperrt: eine
zweite Lesart von „aktiv" neben `classify()` und `classify_all()` ist genau die Drift, gegen die
`T-02.4` gebaut wurde.

**Beschluss, dreiteilig:**

1. **`irrevocable_predicates` MUSS `vote@1` enthalten.** Damit greift der bestehende Schutz aus
   D70/D72 — `is_irrevocable` setzt `protected`, und Widerruf wie Supersede laufen ins Leere. Kein
   neuer Mechanismus, keine Sonderregel in `04`.
2. **Eine `vote@1` mit gesetztem `t_exp` ist keine gültige Stimme.** Sie zählt weder als Ja noch
   als Nein; Vermerk `VOTE_WITH_EXPIRY`. Nicht still ignoriert: `protected` schützt nicht vor
   Ablauf, und ein Feld, dessen Wert wortlos übergangen wird, ist die Stummheit, die D95 gekostet
   hat.
3. **Ein Nukleus, dessen Verfassung `vote@1` nicht führt, ist nicht auszählbar.** Vermerk
   `VOTE_REVOCABLE`, Zustand `UNEVALUABLE`. Seine Auszählung wäre nicht monoton, und dann darf sie
   kein Ergebnis liefern statt eines fragilen.

**Verhältnis zu D58.** Die Negativliste dort nennt `vouch@1`, und das Kriterium lautet, ob
Fortbestehen die konservative Lesart ist. Eine Stimme gewährt keine fortdauernde Autorität; sie ist
ein einmaliger Akt an einem einzelnen, content-adressierten Objekt. D97 hatte die Begründung
bereits geschrieben, ohne den Mechanismus zu benennen.

**Kosten.** Profil D in `04-golden-anchors.md` wurde vollständig neu gerechnet: alle drei
`constitution_hash`, `N_D`, alle drei `epoch_id` und beide `proposal_hash` ändern sich. Die
Schwellenarithmetik ist davon unberührt. Die Bestandsanker aus `00 §3.1` bleiben unangetastet;
Profil D ist ein eigener Nukleus.

**Nebenbefund.** Der Bestandsnukleus `65309fe2…` führt nur `obligation@1` und trifft damit
zusätzlich zu `weight_mode = 1` auch diese Bedingung. Er bleibt nicht auszählbar, jetzt aus zwei
unabhängigen Gründen.

---

**Zur Fehlerform dieses Abschnitts.** D105 ist die Parallelenprüfung, die diese Sitzung zweimal
selbst empfohlen und beim Schreiben von `04 §3.1` unterlassen hat: die Bedingung wurde formuliert,
ohne den Zustandsautomaten aus `01` Anhang B danebenzulegen. D103 und D104 sind Lücken, die erst
beim Entwerfen der Funktionssignaturen sichtbar wurden.

**Konsequenz — Signaturprüfung:** Der Modulschnitt wird entworfen, **bevor** der Prompt geschrieben
wird, nicht als sein erster Abschnitt. Drei der Befunde dieser Runde lagen zwischen zwei
Funktionen, nicht in einer.

---

## X. Aus dem Layer-04-Lauf

### D106 — `participants` auf `TallyResult`; zwei Vermerke für die Zeugenmenge

Zwei Rückfragen aus dem Implementierungslauf, beide korrekt zurückgegeben statt umgedeutet.

**(a) Woher kennt `verify_ratification` die Wählerschaft?** `04 §4.1` Bedingung 2 verlangt
`ratify.I` in `P`. Die Signatur im Prompt reichte `store`, `ratify`, `epoch`, `proposal`, `tally`,
`now` und `policy` — `P` war in keinem davon enthalten. Aus `tally.yes` und `tally.no` ist es nicht
rekonstruierbar: `P` wird deklariert, nie abgeleitet (D96), und ein Mitglied, das nicht abgestimmt
hat, darf materialisieren.

**Beschluss:** `TallyResult` trägt `participants: frozenset[bytes] | None`. Das bisherige Feld `n`
entfällt und wird eine abgeleitete Eigenschaft. Die Signatur von `verify_ratification` bleibt
unverändert.

Ein zusätzlicher Parameter an `verify_ratification` ist verworfen: er erlaubte, die Ratifizierung
gegen eine andere Wählerschaft zu prüfen als die, mit der ausgezählt wurde. `n` neben
`participants` wäre derselbe Fehler eine Ebene tiefer — zwei Darstellungen desselben Zustands, die
einander widersprechen können.

Folgesatz: ist `tally.state` gleich `UNEVALUABLE`, ist `participants` gleich `None`, und
`verify_ratification` liefert nie eine Epoche.

**(b) Zwei Vermerke, nicht einer.** Eine in `ratify.v[0]` zitierte `claim_id` kann auf zwei
verschiedene Weisen nicht tragen, und die Diagnose ist verschieden (D94):

| Lage | Vermerk | Bedeutung |
|---|---|---|
| Claim im Store nicht vorhanden | `UNKNOWN_WITNESS_VOTE` | mir fehlt ein Claim |
| Claim vorhanden, zählt aber nicht | `UNSUPPORTED_RATIFICATION` | die Behauptung stimmt nicht |

Beide führen dazu, dass keine Epoche entsteht — die Wirkung ist gleich, die Diagnose entscheidet.
Im ersten Fall weiß der Beobachter, welche `claim_id` er holen muss; im zweiten weiß er, dass
Holen nichts nützt.

`04-prompt.md §5` hatte `UNKNOWN_WITNESS_VOTE` auf jede `claim_id` außerhalb von `tally.yes`
angewandt und damit beide Lagen zusammengezogen. `04-governance.md §4.1` nannte nur
`UNSUPPORTED_RATIFICATION` und stellte den zweiten Vermerk nie daneben. Der Lauf hat die Lücke
zwischen beiden gefunden.

Neuer Vektor `GV-30`: `ratify@1` zitiert eine `claim_id`, die im Store nicht vorhanden ist.
Erwartung `UNKNOWN_WITNESS_VOTE`, keine Epoche. `GV-2` bleibt unverändert und deckt den zweiten
Fall.

**Zur Form dieser Runde.** Beide Punkte sind zwischen zwei Artefakten entstanden, nicht in einem:
(a) zwischen einer Spec-Bedingung und einer Prompt-Signatur, (b) zwischen einer Spec-Vermerkliste
und einer Prompt-Vermerkliste. Die Signaturprüfung aus Abschnitt W hätte (a) gefunden, wenn sie
auch die zweite Funktion erfasst hätte statt nur die erste.

---

## Y. Symmetrie an der Epochengrenze

### D107 — `ratify@1` ist irrevocable; `propose@1` ist ungeprüft ⚠️

Aus der Parallelenprüfung, die D106 als Konsequenz aufgeschrieben hatte: `decide()` und
`verify_ratification()` nebeneinandergelegt statt nacheinander gelesen.

**Der Befund.** `04 §4.1` Bedingung 2 verlangt, dass der `ratify@1`-Claim `ACTIVE` ist. D105 hat
`vote@1` in `irrevocable_predicates` gezwungen; `ratify@1` stand dort nicht.

Folge: eine bereits etablierte Epoche kann wieder verschwinden. Wer als Einziger materialisiert
hat, widerruft seinen `ratify@1`, und für jeden Beobachter, der nur diesen einen Beleg kennt,
fällt der Nukleus auf die alte Verfassung zurück — bei unveränderter Stimmenlage im Store.

Das ist derselbe Monotoniebruch, den D105 eine Ebene tiefer geschlossen hat, nur an der
Epochengrenze statt an der Stimme. `INV-04.7` sichert die Stimmenmenge; darüber war nichts
gesichert. Kein Angriff — die Tatsache bleibt nachrechenbar und jedes Mitglied kann neu
materialisieren —, aber ein Hebel in einer Hand, die ihn nicht haben sollte: nicht die Änderung
rückgängig machen, sondern sie aussetzen, bis jemand tätig wird.

**Beschluss, in der Form von D105:**

1. **`irrevocable_predicates` MUSS `ratify@1` enthalten.** Der Schutz entsteht über `is_irrevocable`
   (D70/D72), nicht über eine Sonderregel in `04`.
2. **Eine `ratify@1` mit gesetztem `t_exp` etabliert keine Epoche.** Vermerk
   `RATIFY_WITH_EXPIRY`. `protected` schützt nicht vor Ablauf, und ein still übergangenes Feld ist
   die Stummheit aus D95.
3. **Ein Nukleus, dessen Verfassung `ratify@1` nicht führt, ist nicht auszählbar.** Vermerk
   `RATIFY_REVOCABLE`, Zustand `UNEVALUABLE`.

Zu D58 verhält es sich wie bei D105: eine Materialisierung gewährt keine fortdauernde Autorität.
Sie bezeugt eine unabhängig nachrechenbare Tatsache an einem content-adressierten Objekt, und
Fortbestehen ist die konservative Lesart.

**Die Gegenrichtung, im selben Zug festgestellt.** `propose@1` wird von der Auszählung **nie
gelesen**. Eine Stimme zeigt auf den `proposal_hash`, nicht auf den `propose@1`-Claim; dieser
dient allein der Auffindbarkeit. Er braucht deshalb keinen Schutz, und eine Aktivitätsprüfung auf
ihn wäre ein Fehler — sie gäbe dem Vorschlagenden nachträglich Macht über eine Abstimmung, die
ohne ihn weiterläuft. Das stand bisher nirgends und ist die Sorte Selbstverständlichkeit, die im
Implementierungsfenster still zu einer Zeile wird.

**Verworfen — die Aktivitätsprüfung auf `ratify@1` streichen.** Billiger, aber es wäre eine
Sonderregel neben `classify_all` statt der bestehenden Mechanik, und Equivocation des
Materialisierenden bliebe ungeprüft.

**Verworfen — als getragene Grenze stehen lassen.** Selbstheilend, sobald jemand neu
materialisiert. Verworfen, weil „selbstheilend, sobald jemand tätig wird" bei einer Verfassung
etwas anderes bedeutet als bei einem Vouch: bis dahin gilt für einen Teil des Nukleus eine andere
Verfassung, und `03` bindet `constitution_hash` daran (D61).

**Kosten.** Profil D zum zweiten Mal in dieser Sitzung neu gerechnet: alle drei
`constitution_hash`, `N_D`, alle drei `epoch_id`, beide `proposal_hash`. Die Arithmetik ist
unberührt. Neue Vektoren `GV-31` bis `GV-34` und die Invariante `INV-04.8`. Der Prompt wurde vor
dem Losschicken des Werkzeugs korrigiert; es hat nie gegen die alten Zahlen gebaut.

**Zur Fehlerform.** D105 und D107 sind dieselbe Lücke auf zwei Ebenen. D105 entstand, weil `§3.1`
ohne den Zustandsautomaten aus `01` Anhang B danebengelegt geschrieben wurde; D107, weil die
Korrektur danach nur auf `vote@1` angewandt und nicht auf jedes Prädikat dieser Schicht geprüft
wurde. Eine Reparatur ist selbst eine Regel und braucht dieselbe Übertragungsprüfung wie die
Bedingung, die sie ersetzt.

**Konsequenz — Prädikatendurchgang:** Wird ein Prädikat einer Schicht mit einer
Zustandsbedingung belegt, werden **alle** Prädikate derselben Schicht daraufhin durchgegangen,
und die, die keine bekommen, werden ausdrücklich als ungeprüft benannt.

---

## Z. Aus der Layer-04-Abnahme

Drei Beschlüsse. Alle drei betreffen Zeilen, die die Umsetzung korrekt befolgt hat — es sind
Spec-Fehler, keine Implementierungsfehler.

### D108 — Eine Schwelle unterhalb der Mehrheit ist nicht auswertbar ⚠️

D102 begründet die Eindeutigkeit einer Epoche damit, dass sich die Ja-Mengen zweier rivalisierender
Vorschläge überschneiden müssen. Diese Aussage gilt nicht für jede Schwelle. Bei
`amendment: [1,3]` können zwei disjunkte Ja-Mengen von je mehr als einem Drittel entstehen — zwei
gültig ratifizierte Nachfolger derselben Epoche, und die Argumentation aus D102 fällt vollständig.

Weder `04-governance.md` noch die Anker noch der Code prüften es. **Die Voraussetzung stand in D102
in einem Nebensatz der Begründung und in keiner prüfbaren Zeile.** Das ist die Bauform aus D74 und
D87: eine Begründung, die in ihrem Ursprungskontext trug und beim Übertragen ihren Geltungsbereich
verlor — hier beim Übertragen von der Begründung in die Norm.

**Die Rechnung.** Seien `A` und `B` disjunkte Ja-Mengen, die beide durchkommen. Dann gilt
`|A| * den > num * n` und `|B| * den > num * n`; addiert und mit `|A| + |B| <= n`:

```
n * den   >=   (|A| + |B|) * den   >   2 * num * n        ->        den > 2 * num
```

Zwei disjunkte Ja-Mengen sind also genau dann unmöglich, wenn **`2 * num >= den`**. Die Grenze ist
nicht strikt: `[1,2]` bleibt zulässig, `[1,3]` und `[2,5]` nicht. Erschöpfend nachgeprüft über alle
`n` bis 60.

Weil `[1,2]` zulässig bleibt, betrifft die Bedingung `ordinary: [1,2]` aus `00 §3.1` nicht, und der
Bestandsanker `890b21e7…` bleibt gültig. Geprüft wird trotzdem nur die **angewandte** Klasse — eine
Verfassung soll nicht daran scheitern, dass ein in v1 unbenutzter Eintrag unglücklich gesetzt ist.

**Beschluss:** Die angewandte Schwelle einer Auszählung MUSS `2 * num >= den` erfüllen. Andernfalls
ist der Vorschlag nicht auswertbar: Zustand `UNEVALUABLE`, Vermerk `THRESHOLD_BELOW_MAJORITY`. Die
Prüfung gilt der **angewandten** Schwelle nach der Maximum-Regel (`04 §3.4`), also nach
`ratio_max`.

**Zur Auswertungszeit, nicht zum Inkrafttreten.** Geprüft wird beim Auszählen, nicht bei der
Ratifizierung der Verfassung, die die Schwelle setzt. Die Alternative wäre sauberer — eine
Verfassung mit zu niedriger Schwelle träte gar nicht erst in Kraft —, greift aber beim Genesis
nicht, dessen Verfassung ohne Abstimmung gilt. Die Regel stünde dann an zwei Stellen, und zwei
Darstellungen derselben Regel sind in diesem Projekt die häufigste Fehlerquelle.

Folge, offen getragen: ein Nukleus kann eine Verfassung mit zu niedriger Schwelle in Kraft haben.
Er kann dann nichts mehr ändern, weil jede Auszählung `UNEVALUABLE` liefert. Das ist eine
Sackgasse, aber eine sichtbare mit eigenem Vermerk — und die sichere Richtung gegenüber einer
Verfassung, die sich in zwei Nachfolger spaltet.

### D109 — `TallyResult` bindet sich an Epoche und Vorschlag

`verify_ratification` nahm `epoch`, `proposal` und `tally` als unabhängige Argumente und prüfte
nie, ob die Auszählung zu diesem Paar gehört. Ein Aufrufer mit einem fremden `TallyResult` bekam
die Zeugenmenge gegen eine fremde `yes`-Menge validiert und konnte eine Epoche etablieren, die
niemand beschlossen hat.

Das ist D106 eine Ebene höher. Dort wurde `participants` als Parameter gestrichen, damit die
Wählerschaft nicht auseinanderlaufen kann; dabei blieb unbemerkt, dass das ganze `tally` genauso
frei gereicht wird.

**Beschluss:** `TallyResult` trägt `epoch_id: bytes` und `proposal_hash: bytes`.
`verify_ratification` vergleicht beide mit `epoch.epoch_id` und `proposal.proposal_hash` und wirft
bei Abweichung `ValueError`.

`ValueError` und kein Vermerk: nach D82 und D92 ist ein fehlzugeordnetes Objekt ein Aufruferfehler.
Ein Vermerk hieße, der Fall sei eine Lage der Welt; er ist ein Programmierfehler.

### D110 — Kein Urteil aus einem Objekt mit ungeprüfter Zugehörigkeit

Zwei Befunde derselben Regel.

**(a) `STALE_EPOCH_VOTE` ist eine Paar-Eigenschaft, keine Stimmbedingung.** `04 §3.1` führte
`proposal.predecessor == epoch_id` als Bedingung 3 unter den Stimmen auf. Die Bedingung betrifft
das Paar `(epoch, proposal)` und ist einmal zu prüfen, nicht je Stimme. Wörtlich umgesetzt entsteht
Rauschen über Stimmen fremder Epochen — und, schwerer, bei einem nicht passenden Paar **ohne**
Stimmen wird die Bedingung nie erreicht: die Auszählung läuft durch und liefert `PENDING` statt
eines Fehlers.

**(b) Die Identitätsprüfung des Zielobjekts kam zu spät.** `04 §3.5` führte
`PROPOSAL_CONSTITUTION_UNAVAILABLE` als letzte Zeile, während die Klassen- und Schwellenprüfung
darüber das Zielobjekt bereits las. Passt dessen Hash nicht, wird eine Diagnose aus einem Objekt
gezogen, das nicht das gemeinte ist.

**Beschluss:**

1. Die Paarprüfung wandert an den Anfang von `decide()`, **vor** die Abbruchtabelle. Abweichung
   ergibt `UNEVALUABLE` mit `STALE_EPOCH_VOTE`, Subjekt der `proposal_hash`. Innerhalb der
   Stimmschleife entfällt die Bedingung ersatzlos.
2. Die Identitätsprüfung beider Verfassungsobjekte steht **vor** jeder Prüfung, die ihren Inhalt
   liest.

Die gemeinsame Regel, ab hier normativ für alle Schichten: **kein Vermerk und kein Zustand wird aus
einem Objekt abgeleitet, dessen Zugehörigkeit nicht vorher bestätigt wurde.**

### Nachzug ohne eigene Nummer

Aus derselben Abnahme, ohne Fork und deshalb hier statt als eigener Eintrag:

- **Schwellenform.** `_is_ratio` prüfte zwei Integer. Bei `den = 0` ist jeder Vorschlag lautlos
  sofort `FAILED`, bei `num < 0` ist er ohne eine einzige Stimme `PASSED` — `reached(0, n, -1, 2)`
  vergleicht `0 > -n`. Verlangt sind `den >= 1`, `num >= 0`, `num <= den`, dazu `2 * num >= den`
  aus D108; sonst `MALFORMED_THRESHOLD`.
- **Doppelte Klassenbestimmung.** `decide()` leitet die Klasse inline ab und ruft danach
  `threshold_for()` auf, das dieselbe Ableitung wiederholt. Zwei Implementierungen einer Regel in
  einer Datei, mit der Driftgefahr, gegen die `T-02.4` gebaut wurde. `decide()` benutzt
  `threshold_for()`.
- **`§4.1` Bedingung 4 ist impliziert, nicht geprüft.** Die Spec verlangt, dass keine zwei
  zitierten `claim_id` Stimmen desselben Autors bezeichnen; der Code prüft doppelte `claim_id`.
  Das genügt nur, weil `tally.yes` je Autor höchstens eine Stimme führt — eine Invariante trägt
  eine Bedingung, statt dass sie geprüft wird.
- **`SCOPE_MISMATCH` für jede fremde Stimme.** Jede `vote@1` eines beliebigen anderen Nukleus im
  Store erzeugt einen Vermerk. `membership()` vergibt ihn erst, nachdem Subjekt und Prädikat
  passen; in einem Multi-Nukleus-Store schwemmt die Liste sonst über.
- **`NucleusPolicy.declared` wird überschrieben.** Der Konstruktor ersetzt das Feld durch die
  gefilterte Menge. Nach der Konstruktion ist nicht mehr feststellbar, was die Verfassung erklärt
  hat; der Vergleich „erklärt gegen wirksam" ist verloren. Entweder bleibt `declared` unangetastet
  oder es tritt ein zweites Feld daneben.
- **`NucleusPolicy.warnings` ist nicht sortiert und nicht dedupliziert.** Die Malformed-Notizen
  werden in Eingabereihenfolge angehängt. Bekommt der Konstruktor ein `frozenset` — was
  `resolve_policy` in zwei von drei Rückgabepfaden tut —, ist die Reihenfolge nicht bestimmt:
  **zwei Läufe über dieselbe Verfassung liefern verschiedene Tupel.** Jede andere Vermerkliste im
  Projekt geht durch `dedupe_sort`; diese muss es auch.
- **Leere `participants`.** Eine leere Liste ist sortiert und duplikatfrei und passiert die
  Formprüfung. Mit `n = 0` ist jeder Vorschlag sofort `FAILED`, und die Diagnose sagt „abgelehnt",
  wo „niemand konnte abstimmen" gemeint ist. Mindestens ein Eintrag, sonst
  `MALFORMED_PARTICIPANTS`.
- **`TALLY_UNEVALUABLE`.** `verify_ratification` meldete bei nicht auswertbarer Auszählung
  `UNSUPPORTED_RATIFICATION` — „die Behauptung stimmt nicht", wo „ich konnte nicht auswerten"
  gemeint ist. Eigener Vermerk nach D94.
- **Bedingungsreihenfolge in `04 §3.1`.** Die Umsetzung prüft `t_exp` und `choice` vor `ACTIVE`.
  Wirkung identisch, Diagnose besser: eine abgelaufene Stimme mit gesetztem `t_exp` bekommt
  `VOTE_WITH_EXPIRY` statt lautlos zu verschwinden. **Die Spec wird auf die Implementierung
  nachgezogen**, wie bei `Derivation(bfs, findings)` in Layer 02.
- **Textwert in `irrevocable_predicates`.** Ein `str` ist iterierbar; `list("obligation@1")` liefert
  zwölf Einzelzeichen und damit zwölf Vermerke auf Symptome statt einen auf die Ursache. Ein `str`
  wird wie ein nicht iterierbarer Wert behandelt: ein Vermerk mit `repr`, Liste vollständig
  ausgefallen. Präzisierung zu D95.

### D111 — `membership()` prüft die Zugehörigkeit seiner Teilnehmerliste

Dieselbe Regel wie D109, eine Schicht tiefer. `membership()` nimmt `constitution_hash` und
`participants` als unabhängige Argumente entgegen und prüft nie, dass die Liste zu genau dieser
Verfassungsversion gehört. Ein Aufrufer kann `participants` aus Epoche 3 mit dem
`constitution_hash` aus Epoche 2 verbinden und bekommt `MEMBER`.

Die Lücke stammt aus `04-prompt.md §7`, nicht aus der Umsetzung: dort steht der Parameter genau so.

**Beschluss:** `membership()` nimmt statt `participants` ein `constitution_obj: dict | None`. Ist
es gesetzt, prüft die Funktion `constitution_hash(constitution_obj)` gegen den Parameter
`constitution_hash` und wirft bei Abweichung `ValueError` (D82, D92, D109); die Teilnehmerliste
wird daraus gelesen, nicht separat gereicht.

Damit zeigen beide Konjunkte der Mitgliedschaft auf **dasselbe** content-adressierte Objekt, wie
`04 §6.1` es beschreibt. Die vier Zustände und die `accept-rules`-Strecke bleiben unverändert.

**Zur Fehlerform.** Von siebzehn Abnahmebefunden aus zwei unabhängigen Durchgängen lagen elf
**zwischen** zwei Stellen, nicht in einer. Vier der fünf Blocker beschreiben Zeilen, die die
Umsetzung korrekt befolgt hat.

Der zweite Durchgang war die Kontrolle wert: er hat D108 korrigiert — die dort zunächst behauptete
Grenze `2 * num > den` war zu streng und ohne Herleitung aufgeschrieben — und sechs Befunde
ergänzt, von denen einer (`warnings` ohne feste Reihenfolge) ein Determinismusbruch ist.

**Konsequenz — Voraussetzungsprüfung:** Trägt eine Invariante eine Voraussetzung, gehört diese in
dieselbe normative Tabelle wie die Invariante, nie in ihren Begründungstext. D108 wäre sonst erst
an einem echten Nukleus aufgefallen.

---

## AA. Zugehörigkeit aller Felder

### D112 — `proposal.scope` wird geprüft; Schwellenvalidierung vor Umwandlung ⚠️

Zwei Befunde aus der zweiten Abnahme (`impl/04a-korrektur`, `e576663`). Beide sind klein, beide
gehören zu derselben Regel, und der erste ist die **vierte** Wiederholung derselben Form.

**(a) `proposal.scope` wird nirgends geprüft.** `Proposal` trägt ein eigenes `scope`-Feld. Weder
`decide()` noch `verify_ratification()` vergleichen es mit `epoch.scope`. Ein Vorschlagsobjekt
eines fremden Nukleus, dessen `predecessor` zufällig oder absichtlich auf diese Epoche zeigt, wird
ausgezählt; die daraus entstehende Epoche trägt `scope = epoch.scope` und eine Verfassung, die für
einen anderen Nukleus geschrieben wurde.

Das ist wörtlich der Satz, den D110 normativ gemacht hat: kein Vermerk und kein Zustand aus einem
Objekt, dessen Zugehörigkeit nicht vorher bestätigt wurde. D109 hat `epoch_id` und
`proposal_hash` gebunden; das dritte Feld desselben Objekts blieb ungeprüft.

**Beschluss:** `proposal.scope != epoch.scope` ist ein **`ValueError`**, geprüft als erste
Bedingung in `decide()` und in `verify_ratification()`, vor der Paarprüfung. Kein Vermerk: ein
fehlzugeordnetes Objekt ist ein Aufruferfehler und keine Lage der Welt (D82, D92, D109).

**(b) Die Schwellenvalidierung läuft nach der Umwandlung.** `threshold_for()` coerciert mit
`int(old_th[0])`, bevor `_is_ratio` je aufgerufen wird. Bei `thresholds.amendment = ["a","b"]`
wirft `int("a")` einen `ValueError`, der in der `except (KeyError, TypeError, IndexError)`-Liste
von `decide()` nicht steht: eine formwidrige Verfassung reißt den Aufruf ab, statt
`MALFORMED_THRESHOLD` zu liefern.

**Beschluss:** `_is_ratio` läuft auf den Rohwerten beider Verfassungen, **bevor** `threshold_for`
sie anfasst. `threshold_for` coerciert nicht mehr; sie bekommt bereits geprüfte Integer-Paare.

Vektoren: `GV-46` fremder `proposal.scope` → `ValueError`; `GV-47` `thresholds` mit Textwerten →
`MALFORMED_THRESHOLD`, kein Abbruch.

**Zur Fehlerform — vierte Wiederholung.** D105 schützte `vote@1` und vergaß `ratify@1` (→ D107).
D106 zog `participants` nach `TallyResult` und ließ `epoch_id` und `proposal_hash` draußen
(→ D109). D109 band beide und übersah `membership()` (→ D111). D111 band die Teilnehmerliste und
übersah `proposal.scope` (→ D112). Jedes Mal war die Reparatur richtig und unvollständig auf die
Geschwister ihrer eigenen Art.

Die bisherigen Konsequenzen — Prädikatendurchgang (D107) und die Eingabenprüfung aus der Abnahme —
setzen beide beim **Beheben** an. Das ist zu spät: wer einen Befund behebt, sieht die Geschwister
des Befunds, nicht die Geschwister des Feldes.

**Konsequenz — Zugehörigkeitsliste am Datentyp:** Trägt ein Datentyp Felder, die seine
Zugehörigkeit zu einem Kontext behaupten, wird die vollständige Liste dieser Felder **bei seiner
Definition** aufgeschrieben, zusammen mit dem Kontext, gegen den jedes zu prüfen ist. Für
`Proposal` sind es drei: `scope`, `predecessor`, `constitution_hash`. Die Liste wird nicht beim
Beheben eines Befunds angelegt, sondern beim Schreiben des Typs — sonst wächst sie immer nur um
das eine Feld, das gerade wehgetan hat.

---

## AB. Reihenfolge und Abhängigkeit

### D113 — `threshold_for` wird geteilt

Befund aus der dritten Abnahme (`impl/04b-korrektur`, `5714bbc`). Klein, aber es ist die
Wiederkehr eines bereits behobenen Befunds, und der Grund dafür ist lehrreich.

**Was passiert ist.** D112 verlangte, dass `_is_ratio` auf den Rohwerten läuft, **bevor**
`threshold_for` sie anfasst. `threshold_for` liefert aber zugleich die Klasse, und die
`_is_ratio`-Schleife braucht sie. Ohne Umbau der Signatur gab es genau einen Weg: die
Klassenableitung wurde ein zweites Mal inline in `decide()` eingesetzt, und `threshold_for`
bestimmt sie danach erneut.

Damit ist **B-3 der ersten Abnahme wiederhergestellt** — zwei Implementierungen derselben Regel in
derselben Datei, in `04a` behoben, in `04b` zurück. Laufen sie je auseinander, wird die Schwelle
einer anderen Klasse validiert als angewandt.

Zusätzlich ist das `try/except (KeyError, TypeError, IndexError)` um `threshold_for` seit der
vorgezogenen Validierung **unerreichbar**. Unerreichbarer Code, der einen Fehlerfall vortäuscht,
ist die stille Variante des Problems: er suggeriert eine Absicherung, die nichts absichert.

**Beschluss:** `threshold_for` wird in zwei Funktionen geteilt.

```
threshold_class(old_obj, new_obj, genesis_obj) -> str
applied_threshold(old_obj, new_obj, klass)     -> tuple[int, int]
```

`decide()` ruft `threshold_class` **einmal**, validiert beide Schwellen mit `_is_ratio`, ruft dann
`applied_threshold`. Das `try/except` entfällt. Eine Implementierung der Regel, kein unerreichbarer
Zweig, und die Reihenfolge aus D112 bleibt.

Keine neue Bedingung, keine neue Zahl: die Testzahl bleibt unverändert.

**Zur Fehlerform — eine neue.** Die Kette D105 bis D112 war viermal dieselbe Unvollständigkeit auf
Geschwister. Dies hier ist etwas anderes: eine Reparatur hat eine **Reihenfolge** vorgeschrieben,
ohne zu sagen, wie die Abhängigkeit aufzulösen ist, die in der alten Reihenfolge miterledigt wurde.
Die einzig mögliche Auflösung hat einen früheren Befund zurückgebracht.

Der Korrekturprompt schrieb „die Klassenbestimmung darf vorher laufen" und ließ offen, **woher**
sie dann kommt. Die Umsetzung war die einzige, die ohne Signaturänderung möglich war.

**Konsequenz — Abhängigkeitssatz bei Reihenfolgeänderungen:** Wird eine Reihenfolge normativ
geändert, wird für jede Größe, die in der alten Reihenfolge nebenbei entstand, ausdrücklich
benannt, woher sie in der neuen kommt. Fehlt der Satz, wählt die Umsetzung den kürzesten Weg — und
der ist Duplikation.

---

## AC. Trennung, Nachfolge und der Schnitt bei der Gründung

### D114 — `parent_scope` ist deklarativ; Governance und Substanz gehören getrennt

Ausgelöst durch eine Frage, die kein Randfall ist: zwei Gründer zerstreiten sich. Aldi und
Vapiano sind die bekannten Fälle, und in beiden war die Auflösung nicht eine Abstimmung, sondern
eine Trennung.

**Die Ausgangslage ist unparametrierbar.** Bei `n = 2` verlangt **jede** nach D108 zulässige
Schwelle Einstimmigkeit — das folgt direkt aus `2 * num >= den`: was zwei disjunkte Ja-Mengen
ausschließt, ist mit einer von zwei Stimmen nicht erreichbar. Es gibt keinen Wert, der hilft. Bei
`n = 3` gibt es Klassen ohne Einstimmigkeit, aber nur mit `num/den` nahe der Hälfte; ab `2/3`
fällt es zurück. Der neutrale Dritte ist damit ausdrückbar — als **Mitglied** unter Gleichen, nie
als Instanz darüber, denn die gibt es in MaR nicht (`04 §8`).

Bleibt die Frage, was eine Trennung kostet. Und die entscheidet sich bei der Gründung.

**(a) `parent_scope` ist eine Behauptung, keine Beziehung.** Das Feld steht seit `00 §4` im
Genesis-Schema, wird aber von **keiner** Funktion gelesen — nicht in `02`, nicht in `03`, nicht in
`04`. Sein Name suggeriert eine Über-/Unterordnung, die es nicht gibt und nach `02 §2` auch nicht
geben kann: es gibt einen Graphen je `N`, Vertrauen fließt nicht über Scope-Grenzen, und D92
verbietet scope-fremde Verdikte.

**Beschluss:** Das Feld ist rein deklarativ und bekommt in `00 §4.1` einen ausdrücklichen Satz
dazu. Es begründet keine Autorität, keine Übertragung, keinen Vorrang. Es behauptet eine
Zugehörigkeit oder Nachfolge, prüfbar über die Genesis-Kette, bewertet vom Leser — das Protokoll
erzwingt Zurechenbarkeit, nicht Wahrheit (`08 §2.1`).

Ausdrücklich zugelassen: **mehrere Nuklei dürfen dieselbe Elternschaft behaupten.** Spaltet sich
eine Gemeinschaft, berufen sich beide Hälften auf denselben Vorgänger, und keine kann die andere
daran hindern. Welche als Fortsetzung gilt, entscheiden die Beteiligten. Das Protokoll bildet den
Streit ab, statt ihn zu entscheiden.

**(b) Governance und Substanz gehören in getrennte Scopes.** Empfehlung, keine Prüfung, in
`00 §4.2`. Vouches, Obligationen und Quittungen gehören nicht in den Scope, dessen `participants`
abgestimmt werden. Der Governance-Scope regiert genau eine Sache: sich selbst. Die Substanz lebt
daneben, in einem Scope ohne `participants` — er ist damit nach `04 §3.5` nicht auszählbar und
braucht es nicht, weil Bürgen, Verpflichten und Quittieren zweiseitige Akte ohne Kollektivbeschluss
sind.

Damit kostet ein Zerwürfnis das Regelwerk und nicht die Substanz: die Kanten tragen ein anderes
`N` und bleiben unberührt, egal wie fest der Governance-Scope steckt. Wer beide Hälften trennen
will, gründet zwei neue Governance-Scopes und bleibt im gemeinsamen Substanz-Scope — verschiedene
Regelwerke, dieselbe Wirtschaft.

**Der Preis, offen benannt:** ein Scope ohne Governance hat **unveränderliche Arbitratoren**, weil
`03 §2.4` sie aus der Verfassung des eigenen Scopes nimmt. Mit zwei Personen bekommt man nicht
beides — änderbare Regeln und unangreifbare Substanz —, ohne einen dritten Scope oder einen der
beiden Nachteile.

Und der teure Fall bleibt teuer: wollen die Hälften auch getrennte Wirtschaften, beginnt eine bei
null. Das folgt aus der Kontextbindung in `02 §2` und lässt sich für den Trennungsfall nicht
aussetzen, ohne die Eigenschaft aufzugeben, wegen der das Ganze funktioniert.

**(c) Keine Stilllegungsmarkierung.** Ein Nukleus, in dem niemand mehr signiert, ist stillgelegt;
das erkennt jeder Beobachter an seinem eigenen Bestand. Eine Markierung wäre eine globale Aussage
über etwas, das nur lokal beobachtbar ist.

**Nebenbei korrigiert.** `00 §4` Key 5 trug noch „in v1 selbst unveränderlich" — überholt durch
die Maximum-Regel aus `04 §3.4`, und die Klassenzuordnung aus D104 fehlte. Beides nachgezogen.

**Zur Fehlerform.** `parent_scope` stand seit Layer 00 im Schema und hatte nie eine Wirkung. Kein
Durchgang hat es gefunden, weil alle Prüfungen von einer Funktion ausgingen und fragten, ob sie
richtig ist — nicht von einem Feld und ob es überhaupt gelesen wird.

**Konsequenz — Feldinventur:** Vor der Abnahme einer Schicht wird für jedes Feld ihrer Schemata
benannt, welche Funktion es liest. Felder ohne Leser sind entweder zu streichen oder als
deklarativ zu kennzeichnen; sie schweigend stehen zu lassen erzeugt eine Erwartung, die niemand
einlöst.

---

## AD. Trust-Parameter bekommen einen Ort

### D115 — Optionaler Genesis-Key 9 `trust_params`

`C₀`, `γ` und `D` haben seit Layer 02 keinen deklarierten Ort. `02 §8` nennt sie „Policy-Knöpfe",
ohne zu sagen wo; die acht Genesis-Keys und die vier Verfassungsfelder tragen sie nicht. Für
Layer 04 war das folgenlos, seit D98 die Gewichtung herausgenommen hat. Für einen **rechenbaren**
Nukleus ist es das nicht: ohne festen Ort rechnen zwei Betreiber verschiedene Kapazitäten, und
`trust()` ist nicht reproduzierbar.

**Beschluss:** Optionaler Genesis-Key `9`.

```
9 trust_params : { 0: C₀, 1: γ_num, 2: γ_den, 3: D }     ; alle uint
```

**Genesis, nicht Verfassung.** `D` steckt über `n/D` in signierten Vouches; eine änderbare
Deklaration würde Bestandssignaturen still umbewerten. D35 verlangt genau deshalb
Unveränderlichkeit über die Lebensdauer eines Scopes, und unveränderlich ist nur das Genesis.
`C₀` und `γ` reisen mit, weil sie zur selben Kalibrierung gehören und ein Nukleus, der die eine
Hälfte festlegt und die andere nicht, keine reproduzierbare Kapazität hat.

**Optional.** Fehlt der Key, gilt Bestandsverhalten: die Parameter sind out-of-band und
`trust()`/`rank()` verlangen sie weiterhin als Aufruferargument. Damit bleibt der Bestandsanker
`65309fe2…` unberührt — das kanonische Beispiel aus `00 §3.1` lässt den Key weg.

**Wohlgeformtheit**, geprüft bei Anwesenheit: `C₀ >= 1`, `D >= 1`, `1 <= γ_num < γ_den`. Dazu die
Empfehlung aus `02 §8` als SHOULD: `D >= C₀`, damit stets `C(I)` bindet und nicht `D`.

Die Reichweite folgt daraus und ist keine Wahl mehr, sondern eine Rechnung:
`r_max = ⌊log_{1/γ} C₀⌋`. Bei `C₀ = 100` und `γ = 1/2` sind das sechs Hops — jenseits davon ist
`⌊C₀γ^d⌋ = 0`, und kein Vouch trägt mehr.

**Was das nicht ist.** Ein Nukleus darf jeden Wert wählen; das Protokoll fixiert keinen Default.
Ein Reichweitenparameter entscheidet, wie weit jemand wirken kann, und verteilt damit Macht —
nach `08 §3` gehört er in die Verfassung eines konkreten Nukleus und nicht in die Schicht. Das
Genesis ist hier nur der **Ort der Festlegung**, nicht der Ort der Wahl.

---

## AE. Wer entscheidet und wer gebunden ist

### D116 — `participants` und Mitgliedschaft sind zwei Fragen

Aufgefallen beim Vervollständigen des Beispielnukleus, also an einem gerechneten Fall und nicht
beim Lesen.

**Zwei Abschnitte derselben Datei definieren „gehört dazu" verschieden.** `04 §2.1` macht die
Stimmberechtigung an `vote.I ∈ P` fest — der deklarierten Liste, mehr nicht. `04 §6.1` macht
Mitgliedschaft an der Konjunktion aus `participants` und einer aktiven `accept-rules` auf genau
diesen `constitution_hash` fest (D60).

Nach jeder Ratifizierung fallen beide auseinander: der Hash ist neu, die alten Annahmen zeigen auf
den vorigen, und `03 §4` zählt sie für die neue Version ausdrücklich **gar nicht**
(`CONSTITUTION_VERSION_MISMATCH`).

**Folge: unmittelbar nach jeder Verfassungsänderung ist niemand mehr `MEMBER`.** Alle sind
`GRANT_ONLY`, bis jede und jeder einzeln die neue Fassung annimmt — und zugleich dürfen alle
weiter abstimmen, weil `participants` unverändert gilt. Es stimmt also jemand unter einer
Verfassung ab, der ihr ausdrücklich nicht zugestimmt hat.

**Beschluss: keine Mechanikänderung.** Die Mechanik ist richtig, die Spec war stumm.

Die Alternative wäre schlechter: verlangte die Stimmberechtigung `MEMBER`, könnte eine
Ratifizierung den Nukleus einfrieren — niemand dürfte abstimmen, bis alle angenommen haben, und
wer nie annimmt, blockiert dauerhaft. Das ist die Sackgasse aus dem Zwei-Personen-Fall, nur mit
einem zusätzlichen Schritt davor.

Normativ in `04 §6`:

> `participants` und Mitgliedschaft beantworten zwei verschiedene Fragen. Die Liste bestimmt,
> **wer entscheidet**; die Annahme bestimmt, **wer gebunden ist**. Nach einer Ratifizierung ist
> jedes Mitglied `GRANT_ONLY`, bis es die neue Fassung annimmt; die Stimmberechtigung bleibt davon
> unberührt. Wer eine Änderung ablehnt, behält damit die Mittel, sie rückgängig zu machen.

Getragene Grenze in `04 §8` und Betriebswarnung in `example-nucleus.md`: **eine
Verfassungsänderung entzieht allen still den `MEMBER`-Status.** Alles, was auf `MEMBER` prüft,
hört auf zu wirken, bis neu signiert ist. Kein Fehler, aber eine Rechnung, die ein Betreiber vor
der ersten Änderung kennen muss.

**Zur Fehlerform.** Kein Durchgang hat das gefunden — weder die Parallelenprüfung noch die
Feldinventur, weil beide Definitionen für sich richtig sind und erst über einen **Epochenwechsel**
hinweg auseinanderlaufen. Sichtbar wurde es, als ein Beispiel mit echten Zahlen zwei Epochen
durchlaufen musste.

**Konsequenz — Zustandsübergang statt Zustand:** Wo zwei Begriffe denselben Sachverhalt
beschreiben, werden sie nicht nur nebeneinandergelegt, sondern über den Übergang geführt, der
beide berührt. Nebeneinander waren `§2.1` und `§6.1` widerspruchsfrei; erst die Ratifizierung
zwischen ihnen zeigt die Lücke.

---

## AF. Der dritte Ausgang aus `ACTIVE`

### D117 — Equivocation hebt Monotonie auf ⚠️

Gefunden beim Durchrechnen eines Simulationsszenarios mit **vier getrennten Stores** — nicht
beim Lesen des Codes und nicht in einem Durchgang durch die Spec.

**Der Befund.** D105 und D107 haben die Monotonie der Stimmen- und Epochenmenge gesichert, indem
`vote@1` und `ratify@1` in `irrevocable_predicates` stehen: Widerruf und Supersede laufen ins
Leere, Ablauf ist über `VOTE_WITH_EXPIRY` ausgeschlossen. Damit waren zwei Ausgänge aus `ACTIVE`
geschlossen.

Es gibt einen dritten. In `_classify_one` steht die Equivocation-Prüfung **vor** allem anderen und
vor der Ermittlung von `protected`:

```
if _is_in_equivocation_pair(claim, store):
    return Classification(state=EQUIVOCATION_FLAGGED, trust_usable=False)
```

`is_irrevocable` schützt nicht davor — und soll es nicht, denn ein Schutz gegen Equivocation wäre
ein Schutz des Doppelzüngigen. Eine Stimme, die eben noch zählte, hört auf zu zählen, sobald ihr
Zwilling beim Beobachter eintrifft.

**Damit sinkt die Ja-Menge durch Wissenszuwachs.** Gerechnet, `n = 3`, Schwelle `[1,2]`, zwei Ja
nötig. Anna signiert zwei Stimmen mit demselben `h_prev` — ein Ja an Bruno, ein Nein an Chris.
Chris stimmt mit Ja.

| Beobachter | kennt | Ja | Nein | Zustand |
|---|---|---|---|---|
| Bruno, vor Austausch | Anna-Ja, Chris-Ja | 2 | 0 | **`PASSED`** |
| Chris, vor Austausch | Anna-Nein, Chris-Ja | 1 | 1 | `PENDING` |
| beide, nach Austausch | Anna geflaggt, Chris-Ja | 1 | 0 | `PENDING` |

Brunos `PASSED` kippt zurück — `INV-04.7` ist verletzt. Hat er zwischenzeitlich materialisiert,
zitiert sein `ratify@1` eine nicht mehr zählende Stimme, es entsteht
`UNSUPPORTED_RATIFICATION`, und die Epoche fällt — `INV-04.8` ist verletzt.

**Beschluss: keine Mechanikänderung.** Die Mechanik ist richtig, die Invarianten waren zu stark
formuliert.

Richtig, weil die Richtung sicher ist: es fällt weg, es entsteht nichts. Und weil der Vorgang
einen vom Urheber **selbst signierten** Beweis seiner Doppelzüngigkeit hinterlässt — das ist
`08 §2.2` in Reinform, nicht verhindert, sondern unbestreitbar. Die Folge gehört nach Layer 05,
nicht in eine Sonderregel hier.

Normativ, als Vorbehalt an `INV-04.7` und `INV-04.8`:

> Beide Invarianten gelten unter der Bedingung, dass kein Mitglied equivociert. Eine Equivocation
> entzieht der betroffenen Stimme rückwirkend die Wirkung; eine darauf gestützte Ratifizierung
> wird `UNSUPPORTED_RATIFICATION`, und die Epoche fällt. Die Richtung ist stets abwärts.

Ein einzelnes Mitglied kann damit eine Epoche kippen — aber nur einmal, nur unter Hinterlassung
des Beweises, und nur nach unten.

**Zur Fehlerform.** Bei D105 wurden die Ausgänge aus `ACTIVE` aufgezählt und zwei genannt:
Widerruf und Ablauf. Der dritte stand als **erste Zeile** derselben Funktion.

Und er wurde von keinem Durchgang gefunden, weil alle bisherigen mit einem gemeinsamen Wissensstand
gerechnet haben. In einem gemeinsamen Store trifft der Zwilling sofort ein, `PASSED` entsteht gar
nicht erst, und der Rückfall ist unsichtbar. Sichtbar wurde es erst beim Entwurf einer Simulation
mit **getrennten** Stores.

**Konsequenz — Ausgänge aufzählen:** Wo eine Invariante einen Zustandsübergang ausschließt, werden
**alle** Ausgänge aus dem Zustand aufgezählt und einzeln geprüft — nicht die, an die man beim
Schreiben dachte. Die Aufzählung entsteht aus dem Code der Zustandsfunktion, nicht aus dem
Gedächtnis.

**Konsequenz — getrennte Sicht:** Eigenschaften über Wissenszuwachs werden mit **mehreren**
Beobachtern geprüft, die verschiedene Teilmengen halten. Ein einzelner Store kann Konvergenz nicht
widerlegen, weil in ihm nichts auseinanderläuft.

---

## AG. Monotonie gilt für den Graphen, nicht für den Bestand

### D118 — Die Budgetprüfung ist die zweite gefährliche Richtung ⚠️

Gefunden beim Durchrechnen einer Fuzzing-Eigenschaft, **bevor** sie aufgeschrieben wurde. Die
Eigenschaft lautete zunächst „eine Teilmenge des Claim-Bestands liefert nie höheres Vertrauen als
der volle Bestand". Sie ist falsch.

**Was `02 §7` zusagt.** Max-Flow ist monoton in den Kanten; fehlende Vouch-Kanten können den
Fluss nur senken, das Ergebnis ist eine konservative Untergrenze, im Zweifel wird
unter-vertraut. Und: „Die einzige gefährliche Richtung: ein fehlender *Widerruf*."

**Was tatsächlich gilt.** Der Satz stimmt für den **Graphen**. Zwischen Claim-Bestand und Graph
sitzt aber die Budgetprüfung `Σ n ≤ D`, und die ist **nicht monoton**: ein hinzukommender Vouch
kann `Σ n` über `D` heben, und dann fallen nach `02 §3.1` **alle** Kanten dieses Autors aus —
nicht die letzte, nicht anteilig.

Gerechnet, `D = 100`, Anna bürgt dreimal mit `n = 50`:

| Beobachter kennt | `Σ n` | Kanten von Anna |
|---|---|---|
| einen Vouch | 50 | zählt |
| zwei Vouches | 100 | beide zählen |
| alle drei | 150 | **alle drei fallen aus** — `OVERCOMMITTED_AUTHOR` |

**Wer weniger weiß, sieht mehr Vertrauen.** Das ist Über-Vertrauen bei Teilwissen, also die
gefährliche Richtung — und der fehlende Claim ist eine **Bürgschaft**, die `02 §7` ausdrücklich
als harmlos führt.

Die drei dort genannten Abwehren greifen nicht: `t_exp` ist eine Decke gegen alte Kanten, nicht
gegen unbekannte; Priorität beim Widerruf betrifft ein anderes Prädikat; frische positive Evidenz
hilft nicht, wenn gerade die Evidenz das Problem ist.

Kleinstes Gegenbeispiel: **zwei Vouches mit `n = 51`** bei `D = 100`. Zwei Claims genügen.

**Beschluss: keine Mechanikänderung.** Die Mechanik ist richtig, `02 §7` war zu stark.

Richtig, weil der Ausfall aller Kanten die einzige Antwort ist, die nicht interpretiert: welche
zwei der drei Bürgschaften „gemeint" waren, kann niemand entscheiden, und eine anteilige Kürzung
wäre eine Erfindung des Verifizierers. Und weil der Fall selbstheilend ist: sobald der dritte
Vouch eintrifft, fällt alles, und die Richtung ist danach dauerhaft konservativ. Ein Angriff mit
Gewinn ist es nicht — der Überzeichnende verliert sein gesamtes Budget und hinterlässt einen
signierten Beweis. Die Folge gehört nach Layer 05 (D40), nicht in eine Sonderregel hier.

Normativ in `02 §7`:

> Die Monotonie gilt für den **Graphen**, nicht für den **Claim-Bestand**. Zwischen beiden liegt
> die Budgetprüfung, und sie ist nicht monoton: ein hinzukommender Vouch kann `Σ n > D` auslösen
> und damit alle Kanten seines Autors entfernen. Ein Beobachter mit Teilwissen kann deshalb
> **über**-vertrauen. Das ist neben dem fehlenden Widerruf die zweite gefährliche Richtung; sie
> heilt beim Zustellen und hinterlässt einen signierten Beweis.

**Zur Fehlerform.** Dritte Wiederholung derselben Bauart nach D117 und D116: eine Zusage, die auf
ihrer eigenen Stufe stimmt und beim Blick über die Stufengrenze nicht mehr. Bei D116 war es der
Übergang zwischen zwei Epochen, bei D117 der dritte Ausgang aus einem Zustand, hier die Stufe
zwischen Bestand und Graph.

**Konsequenz — Monotonie stufenweise:** Wird eine Monotonieaussage über eine Ableitung gemacht,
gilt sie zunächst nur für die **letzte** Stufe. Jede Stufe davor — Filter, Budgetprüfung,
Zustandsauswertung, Kanonizitätsprüfung — wird einzeln daraufhin geprüft, ob sie monoton ist, und
das Ergebnis wird im Text benannt. Max-Flow ist monoton; der Weg dorthin ist es an zwei Stellen
nicht.

## AH. Autorschaft, Werkzeug und Schreibautorität

### D119 — `02 §6.2` bekommt einen Leser

`02 §6.2` verlangt: in Scopes mit Budgetregel MUSS ein Vouch `t_exp` tragen, oder die Policy
setzt eine Maximallaufzeit als Default. `§8` macht `Σw ≤ 1` zum Default, ein schweigender
Nukleus trägt die Regel also, und `check_overcommit` rechnet sie im Beispiel durch.

**Beide Zweige sind im Bestand unausdrückbar.** `_Author.claim()` hat keinen `t_exp`-Parameter,
und das Verfassungsschema hat kein Feld für eine Maximallaufzeit. Schwerer wiegt: **niemand
liest die Pflicht.** `§3.1` sagt ausdrücklich, fehlendes `t_exp` binde unbegrenzt; es fällt kein
Vermerk, nichts wird abgelehnt. Der Satz hat zwei Layer überdauert, weil seine einzige Wirkung
darin bestand, dass ein wohlerzogener Autor etwas hinschreibt.

**Beschluss:**

- Vermerk `TrustFinding.VOUCH_WITHOUT_TEXP`, Subjekt die `claim_id` des Vouch, wenn ein Vouch
  in einem Scope mit Budgetregel kein `t_exp` trägt.
- **Ohne Wirkung.** Der Vouch bleibt im Budget-Set und bindet weiter unbegrenzt. Ihn
  auszuschließen gäbe Budget frei, und `§3.1` schließt das aus: kein Akt außer der Uhr gibt
  Budget frei. Diagnose verschieden, Wirkung gleich — D94.
- `claim()` bekommt `t_exp`, `vouch()` reicht durch, der Beispielnukleus setzt eine Laufzeit.

**Warum kein Verfassungsfeld.** Der zweite Zweig aus `§6.2` verlangte ein neues Feld, damit einen
neuen `constitution_hash`, ein neues `N` und die Neuberechnung von `00 §3.1`. Kosten am gesamten
Bestand für einen Knopf, den kein Nukleus bisher braucht. Der Zweig bleibt möglich und bekommt
einen eigenen Durchgang, falls er je gebraucht wird.

**Kein Ankerbruch.** Geprüft: keine Ankerdatei fixiert eine Vouch-`claim_id`. `02` und `02b`
führen keine, `03` und `04` nennen `claim_id` nur in strukturellen Invarianten, `example-nucleus.md`
gar nicht. Die Zahlen der Trust-Schicht hängen an `n`, `D`, `C₀`, `γ` und der Graphform. Ein
`t_exp > now` lässt Aktiv-Set und Budget-Set unverändert. Es ändern sich die `claim_id` der
Vouches und das `h_prev` ihrer Kettennachfolger — beides nirgends festgeschrieben.

**Nebenertrag.** Derselbe Parameter macht den Grenzwertvektor `now = t_exp` in Layer 01 baubar.
Die Vektorlücke folgte aus einer Erzeugerlücke: nicht geprüft werden kann, was nicht erzeugt
werden kann.

**Konsequenz — Leserprüfung.** Trägt ein normativer Satz eine Pflicht an den **Autor** von
Claims, wird bei seiner Formulierung benannt, welche Funktion die Erfüllung liest. Gibt es keine,
ist der Satz entweder auf SOLL zurückzunehmen oder mit einem Vermerk zu versehen. Die
Feldinventur (D114) fragt nach dem Leser eines Feldes; diese Regel fragt nach dem Leser einer
Pflicht.

**Nachzug: Reichweite.** Die erste Fassung dieses Eintrags nannte als Erzeuger nur
`tools/example_nucleus.py`. Es sind **drei**, und alle drei bauen Vouches ohne `t_exp`:

1. `tools/example_nucleus.py`
2. die Fixtures unter `tests/`, die die Golden Anchors materialisieren
3. `tools/sim/scenarios/`

Sobald der Vermerk existiert, feuert er in allen dreien. Die Reparatur an einer Stelle wäre die
sechste Wiederholung der Kette D105 bis D112 gewesen: richtig und nicht auf die Geschwister der
eigenen Art durchgezogen.

**Beschluss:** alle drei Stellen setzen `t_exp` weit jenseits ihres jeweiligen `now`, nie gleich
`now` — der Grenzwert ist einem eigenen Vektor vorbehalten. Damit feuert der Vermerk in keiner
bestehenden Prüfung, alle dokumentierten Finding-Mengen der Ankerdateien bleiben unverändert, und
der Vermerk wird durch **neue** Tests belegt statt durch veränderte alte.

**Verworfen:** die Fixtures unangetastet lassen und die Finding-Listen der Ankerdateien um einen
universellen Zusatz erweitern. Das schriebe in jede Ankerzeile einen Vermerk, der über den Anker
nichts aussagt.

**Kein Feld in `TrustParams`.** „Scopes mit Budgetregel" aus `02 §6.2` hat im Code keine
Entsprechung: `derive()` prüft `Σ n_budget > D` unbedingt, und nichts löst `TrustParams` aus einer
Verfassung auf. Ein Feld dafür hätte weder Schreiber noch Leser — D114. Die Einschränkung des
Satzes ist damit heute gegenstandslos, und der Vermerk gilt für jeden Vouch ohne `t_exp`.

**Ort des Vermerks:** `build_groups`, nach `_decode_weight` und nur für Vouches, die einen
Budget-Beitrag tragen. Ein Vouch mit defektem `v` trägt nach `02 §3.1` keinen Beitrag, bindet
also nichts unbefristet; für ihn zu vermerken wäre Rauschen über ein Nichtproblem.

**Erlaubte Abweichung.** `build_groups` bricht den Gleichstand über `sorted(...)` der `claim_id`.
Ein zusätzliches `t_exp` ändert alle `claim_id` der Vouches, daher kann die gewählte
`kante_claim_id` bei zwei aktiven Vouches derselben Gruppe mit gleichem `n` umspringen. `n_kante`,
jede Kapazität und jeder Fluss bleiben unverändert. Eine Abweichung dort ist **kein** Fehler.

### D120 — Absturzordnung, und die Monotonie ist eine Beobachtereigenschaft

`_Author.claim()` rückt die Spitze bei der Konstruktion vor, unabhängig davon, ob der Claim je
gespeichert oder ausgesandt wird. In einem Prozess harmlos, für ein dauerhaftes Werkzeug nicht.

| Ordnung | Absturz dazwischen | Folge |
|---|---|---|
| signieren, dann persistieren | Spitze veraltet | nächster Claim auf dasselbe `h_prev` ⇒ Equivocation, beweisbar, dauerhaft |
| Spitze festschreiben, dann signieren | Spitze zeigt auf einen nie ausgesandten Claim | alle Nachfolger bleiben bei jedem Beobachter `pending`, unheilbar |
| Core festschreiben, signieren, aussenden, Spitze festschreiben | Core liegt vor | Wiederaufnahme erzeugt denselben Claim |

Die dritte trägt, weil Ed25519 deterministisch signiert (RFC 8032): aus denselben Core-Bytes
entsteht dieselbe Signatur, also derselbe Claim, byteweise. Die Wiederaufnahme ist **idempotent**
und nicht bloß möglich. Das ist der Unterschied zwischen einer Rettung und einer Gabelung.

**Beschluss:** Core-Redo-Eintrag festschreiben, signieren, aussenden, Spitze festschreiben. Beim
Start wird ein offener Redo-Eintrag **fortgesetzt**, nie neu gebaut. Die Zustandsmaschine der
Spitze hat fünf Ausgänge:

1. leer ⇒ Genesis, `h_prev = id_genesis_anchor(I)`
2. gesetzt, Claim im eigenen Store ⇒ Normalfall
3. gesetzt, Redo-Eintrag offen ⇒ fortsetzen
4. gesetzt, Store kennt sie nicht ⇒ **anhalten**
5. zwei eigene Claims auf dieselbe Spitze ⇒ selbst equivociert, **anhalten**

Drei davon halten an. Anhalten und nicht warnen: Weiterschreiben ist in beiden Fällen genau der
Fehler, den die Prüfung erkannt hat.

**Der allgemeine Satz.** Die Monotonie aus `08 §2.2` und `02 §7` — fehlendes Wissen senkt ein
Ergebnis nur — ist eine **Beobachtereigenschaft**. Für den Autor über seine eigene Kette gilt sie
nicht: fehlt ihm sein letzter Claim, senkt das nichts, es erzeugt einen Fork gegen ihn selbst.
Das ist die dritte gefährliche Richtung neben den beiden aus `02 §7`, und sie ist die einzige,
in der der Schaden beim Wissenden selbst entsteht.

**Wiederherstellung ist Migration, nicht Vervielfältigung.** Ein Sicherungsblob trägt Seed **und**
Spitze. Wer ihn zweimal einspielt, läuft in Ausgang 5. Ein Seed allein ist keine Sicherung,
sondern die Waffe.

**Verworfen: die Spitze aus dem Netz rekonstruieren.** Aus fremden Stores lässt sich der letzte
bekannte Claim eines Autors lesen, aber nicht, dass es der letzte ist. Teilwissen wählt eine zu
frühe Spitze — und das ist exakt der Fork, den die Rekonstruktion verhindern sollte.

### D121 — Einlesepfad: ein Ausgang statt vier, und ein unsigniertes Bündel

`claim_from_bytes` dekodiert und baut direkt. Für fremde Bytes wirft es `KeyError`, `IndexError`,
`TypeError` oder `ValueError` und prüft keine Kanonizität. Es ist damit kein Einlesepfad: wer
Empfangenes darüber liest, umgeht die elf Reject-Codes aus `01 Anhang B`.

**Beschluss:**

- Fremde Bytes gehen durch eine Funktion, die **nie wirft** und entweder einen Claim oder einen
  Reject-Code liefert. Die Kanonizitätsprüfung liegt im selben `try` wie das Dekodieren (D83).
- Die Abgrenzung zu D92: dessen `ValueError` gilt für ein vom **Programmierer** fehlzugeordnetes
  Objekt. Fremde Bytes sind eine Lage der Welt und folgen der D95-Bewegung — der defekte Teil
  fällt weg, der Vermerk bleibt.
- Ein Bündel ist ein **unsigniertes** CBOR-Array aus Claim-Bytes plus eine Map
  `object-hash → Objektbytes`. Keine Ordnungsgarantie, Duplikate harmlos, Import idempotent.
  Jedes Element wird einzeln geprüft; dem Container wird nie geglaubt.

**Warum unsigniert.** Nach `08 §3` senkt ein Container keine Feststellungskosten — jeder Claim
ist nach A1 selbstenthalten und trägt seine Signatur schon. Ein signiertes Bündel wäre eine
Aussage über eine **Menge**, also Bedeutung, und ein zweites Ding, das verifiziert werden müsste.
Werkzeugkonvention, kein Transport-Profil.

### D122 — Bauform gegen Feldverlust, und der Modulschnitt der Autorschaft

Weil `Claim` frozen ist, baut `_Author.claim()` zweimal und zählt acht Felder von Hand auf.
`t_exp` ist der Beweis, dass die Aufzählung unvollständig sein kann, ohne dass es auffällt: es
steht in der Kopie und ist trotzdem tot.

Die Fehlerform ist das Gefährliche. Ein vergessenes Feld erzeugt keinen defekten Claim, sondern
einen **in sich stimmigen und gültigen** mit anderem `claim_id` und korrekter Signatur über genau
das, was dasteht. Kein Verifizierer findet das. Der Autor hat etwas anderes gesagt, als er sagen
wollte, und nichts zeigt es an.

**Beschluss:** `dataclasses.replace(unsigned, sigma=...)`, normativ für alles, was Claims erzeugt.
Der zugehörige Test iteriert über `Claim.__dataclass_fields__` und nicht über eine Liste im Test
— sonst trägt die Prüfung dieselbe Schwäche wie die Sache, die sie prüft.

**Modulschnitt.** `_Author` verschmilzt drei Dinge; nur eines ist protokollbestimmt.

| Teil | Ort | Grund |
|---|---|---|
| Bau und Signatur | Paket | `core_bytes`, `DOM_SIG`, Feldsatz sind `01`; zwei Kodierwege driften |
| Kettenspitze | Werkzeug, mit Persistenz | braucht Dauerhaftigkeit und die Zustandsmaschine aus D120 |
| Schlüsselverwahrung | Werkzeug | Betriebsfrage, nach `08 §3` nicht Protokoll |

**Oberflächenregel.** Keine Operation gibt den Schlüssel oder die Spitze heraus. Es gibt genau
eine: gib mir einen signierten Claim zu diesem Inhalt. Überquert der Schlüssel die Grenze nie,
ist ein späterer entfernter Aufruf (D123) eine Transportfrage und kein Umbau.

### D123 — Ein Schreiber, ein Ort; Geräte sind Endpunkte

**Nicht der Claim lebt an einem Ort, die Schreibautorität.** Claims sind selbstenthalten und
müssen überall hinreisen (A1) — Kollision entsteht durch Verbreitung. Singulär sind Schlüssel und
Spitze. Speicher ist repliziert, Autorschaft ist es nie.

**Der Ort ist der Sequenzer.** `h_prev` ordnet, und zwei gleichzeitige Schreiber verlangten eine
Einigung darüber, wer die Spitze fortschreibt — Konsens, unabhängig davon, wie klein die Menge
ist. Auch FROST löst das nicht: ein Gruppenschlüssel gibt eine Identität und eine Kette, aber er
**ordnet nichts**; zwei Signiersitzungen können dieselbe Spitze greifen. FROST löst Verlust und
Diebstahl, nicht Nebenläufigkeit.

**Geräte signieren die Anfrage, nicht den Claim.** Ein Gerät hält ein eigenes Schlüsselpaar und
autorisiert damit eine Anfrage; der Ort signiert den Claim. Die Gerätesignatur betritt das
Protokoll **nie** — kein Atom-Feld, keine zweite Kette, keine zweite Identität im Trust-Graph.
Nach außen eine Identität, nach innen eine kleine Hierarchie, die niemanden angeht. Das ist die
Stelle, an der Matrix' Cross-Signing passt: unterhalb des Protokolls, nicht darüber. Oberhalb
löste es das falsche Problem — es beantwortet „gehört dieses Gerät zu Alice", während `08 §2.1`
„hat Alice anderswo etwas anderes gesagt" beantwortet, und parallele Geräteketten machen
Equivocation zu einer freien Handlung.

**Schlüsselträger ist nicht Schreiber.** Ein Secure Element oder NFC-Träger darf den Schlüssel
halten, solange die Spitze am selben Ort geführt wird. Wandert der Träger ohne die Spitze zu
einem zweiten Ort, gibt es zwei Schreiber. Als reines Transportmittel ist NFC ohnehin gedeckt.

**Getragene Grenze: Autorschaft ist erreichbarkeitsabhängig, Lesen nicht.** Wer seinen Ort nicht
erreicht, kann nicht bürgen, nicht abstimmen, keine Obligation eingehen. Verifikation bleibt
offline vollständig. Die Milderung für längere Trennung ist **Migration** der Kette (D62), nicht
Delegation. Der Alltagsfall trägt sich selbst über die selektive Stille aus `01 §7`: was keinen
Claim erzeugt, braucht keinen Ort — und die Akte, die einen erzeugen, sind die, die warten können.

**Der Trust-Score offline ist über-vertrauend.** Ein alter Store hat weder den fehlenden Widerruf
(`02 §7`) noch den fehlenden über-zeichnenden Vouch (D118); beide zeigen nach oben. Als Gate für
Hochrisiko ist er damit ungeeignet — dieselbe Linie, die `02 §5` zwischen Relaxation und harter
Sicht zieht. D119 mildert es: abgelaufene Vouches fallen gegen die lokale Uhr weg, auch ohne Netz.

**Zur Reihenfolge:** D62 (`00a-rotate-key`, `resolve_current_key`) wird damit zur Voraussetzung
des ersten echten Nukleus und nicht zur Nacharbeit. Ein zweiter Ort ist eine Rotation, und der
Fall tritt beim ersten Gerätewechsel ein.

> **Nachgezogen durch D124.** Der letzte Satz trägt nicht. `00 §6` regelt ausschließlich die
> Nukleus-Autorität; für einen Menschen gibt es keine Rotation, die die Identität erhält. Der
> Gerätewechsel ist **Migration von Seed und Spitze** und damit D120s Fall — dieselbe Aussage, die
> D120 unter „Wiederherstellung ist Migration, nicht Vervielfältigung" bereits trifft. `00a` bleibt
> fällig, aber nicht aus diesem Grund und nicht zu diesem Zeitpunkt.

---

## AI. Rotation: was sie erhält und was sie kostet

Ausgelöst durch die Frage, was Schritt 1 der Anwendungssitzung (`00a-rotate-key`) eigentlich
lösen soll. Die Antwort war, dass er zwei verschiedene Dinge löst und das dringendere davon
nirgends spezifiziert ist. Vorgeschaltet: eine Literaturprüfung, weil das Problem außerhalb von
MaR seit einem Jahrzehnt bearbeitet wird.

### D124 — Persönliche Rotation ist nicht identitätserhaltend

**Die Frage.** Alice wechselt den Schlüssel. Bleibt sie dieselbe Identity?

**Der Befund.** `00 §6` regelt ausschließlich die **Nukleus**-Autorität. Kettenanker ist
`genesis.root_keys`, `I` ist der aktuell autorisierte Nukleusschlüssel, `N` der Scope. Ein Mensch
hat kein Genesis-Objekt, also ist `R_1 ist gültig ⟺ R_1.I ∈ genesis.root_keys` für ihn nicht
auswertbar. D123s Satz „die Milderung für längere Trennung ist Migration der Kette (D62)" hat beim
Transfer vom Nukleus auf die Person seinen Anker verloren — Begründungsprüfung, dieselbe Klasse
wie D77, D83, D87, D91.

**Beschluss: nein.** Ein neuer Schlüssel ist eine neue Identity. Der alte Schlüssel darf als
letzten Akt seiner Kette einen Nachfolger benennen; diese Aussage ist ein gewöhnlicher Claim,
bedeutungsblind wie jeder andere. `02` folgt ihr **nicht**, `03` kennt sie nicht. Trust wird durch
Neu-Bürgen wiederhergestellt.

**Begründung.** Identitätserhaltende Rotation verlangt, dass zwei Leser nicht verschiedene
Rotationsgeschichten sehen. Das ist Nichtequivokation über eine gemeinsame Historie, also ein
globales Log. **Es ist D123, auf den Leser angewandt:** dort verlangten zwei gleichzeitige
Schreiber eine Einigung darüber, wer die Spitze fortschreibt; hier verlangen zwei konkurrierende
Rotationen eine Einigung darüber, welche gilt. Derselbe Satz, andere Seite.

**Belege aus der Literatur.** Jedes System, das die Identität über die Rotation rettet, bezahlt
mit globaler Ordnung:

| System | Bauform | Preis |
|---|---|---|
| did:plc (AT Protocol) | Genesis-Objekt, dessen Hash der Identifikator ist; Operationen per Hash verkettet | zentrales Verzeichnis, Streit über ein 72-Stunden-Fenster gelöst |
| Keybase | Sigchain je Konto, Vorgängerhash, alte Links bleiben nach Widerruf gültig | öffentlicher Merkle-Baum plus Verankerung in einer Fremdkette gegen Rollback |
| CONIKS / Key Transparency | signierte, verkettete Verzeichnis-Snapshots | Auditoren oder Gossip; rückwirkend, schützt den isolierten Leser nicht |
| Nostr | Pubkey **ist** Identität, kein Verzeichnis — MaRs Randbedingungen | NIP-41 nennt sich selbst bestmöglich und nicht garantiert; Rückdatierung offen; Fenster zählen ab dem lokalen Sehen |
| Secure Scuttlebutt | ein Feed je Gerät, weil zwei Schreiber einen Feed nicht teilen können | Fusion IDs verbinden Feeds **oberhalb** des Protokolls |

Die erste Spalte von did:plc ist bemerkenswert: es ist strukturell MaRs Nukleus. Das zeigt, dass
die Bauform nicht das Problem ist — die Zustellgarantie ist es. Und SSB ist unabhängig auf D123
gekommen und hat es außerhalb des Feed-Begriffs beantwortet.

**Verworfen — Auflösung bei jedem `I` und `J`** (did:plc-Form für Personen: `I` wäre ein
Genesis-Hash statt eines Pubkeys). Knüpft Offline-Prüfung an eine Nachschlage-Vorbedingung —
wörtlich das Argument, mit dem `01 §2` den 16-Byte-Truncation-Hash verworfen hat. Ändert außerdem
die Feldsemantik von Layer 01: Protokollversion 2, kein Layer.

**Verworfen — Widerspruchsfenster** (Nostr NIP-41). Zählt ab dem lokalen Sehen und nicht ab dem
Zeitstempel, weil ohne Ordnung nichts anderes möglich ist. MaR hat über `h_prev` eine Ordnung **je
Autor**, aber keine zwischen Autoren; ein Fenster wäre eine Wall-Clock-Regel gegen `01 §5.3`.

**Einordnung nach `08 §3`.** Die Nachfolgeaussage senkt keine Kosten — sie ist bereits
feststellbar, weil signiert und verkettet — und verteilt keine Macht. **Werkzeug.** Kein Layer,
keine Golden Anchors, keine Zahl im Dateinamen. Das ist die dritte Spalte, dieselbe wie beim
Wallet in D122.

**Getragene Grenze.** Wer den Schlüssel verliert, verliert seinen Trust-Score und baut ihn sozial
neu auf. Das ist der Preis für „alles lokal, nie global" und wird bewusst getragen. Sollte eine
spätere Fassung ihn senken wollen, ist die Stelle benannt: sie braucht eine Zustellgarantie, die
`01` heute ausdrücklich nicht gibt.

**Nicht betroffen: der Gerätewechsel.** Er ist Migration von Seed und Spitze an einen anderen Ort
(D120), keine Rotation. Ein Schreiber, eine Kette, keine neue Identity, kein
Protokollmechanismus. Rotation braucht es nur bei Kompromittierung oder Verlust.

### D125 — Rotation gilt erst mit Gegenzeichnung des Nachfolgers

**Geltung.** Die Nukleus-Rotation nach `00 §6.1` — nach D124 die einzige, die es gibt.

**Bisher genügt eine Signatur von `K_{n-1}`.** Das lässt drei Fälle offen: die einseitige
Einsetzung eines Dritten, den Rotate auf einen Schlüssel, dessen Halter nichts davon weiß, und
den zweiten Rotate an anderer Stelle derselben Kette.

**Beschluss.** Eine Rotation ist **vollständig**, wenn `K_n` sie gegenzeichnet — ein Claim in
`K_n`s eigener Kette, der die `claim_id` des Rotate-Claims nennt. Eine unvollständige Rotation ist
wirkungslos: kein Zustand, kein eigener Vermerk, sie zählt nicht. Der **erste vollständige** Rotate
bindet.

**Begründung.** TUF verlangt für neue Root-Metadaten einen Schwellenwert an Signaturen aus dem
**alten und dem neuen** Schlüsselsatz. Dieselbe Form, mit Schwelle eins. Sie kommt ohne Uhr und
ohne globale Ordnung aus: beide Signaturen sind selbstenthalten, das Paar reist zusammen. Sie
erledigt außerdem drei offene Forks auf einmal und erzeugt damit **weniger** Spec als ihre
Alternative.

**Verworfen — letzter gewinnt.** Ein Altschlüssel bliebe dauerhaft mächtig; ein Diebstahl wäre
nie ausheilbar.

**Verworfen — einseitig mit Widerspruchsfenster.** Uhr, wie in D124.

**`00 §6.3` bleibt unberührt.** Signiert `K_{n-1}` zwei Nachfolger auf dieselbe `h_prev`, ist das
Equivocation und bleibt es, auch wenn beide gegenzeichnen. Auflösung weiterhin über §6.2.

**`00 §6.2` bleibt unberührt.** Ist `K_{n-1}` verloren, kann niemand gegenzeichnen — dafür ist der
Governance-Pfad da.

**Parallelenprüfung.** Die Regel steht auch in `00 §6.5`: im FROST-Pfad zeichnet der **neue**
Gruppenschlüssel gegen. Ohne diesen Satz nähme `key_mode = 1` sich still aus.

**Getragene Grenze.** Ein Rotate auf einen Schlüssel, dessen Halter nicht mitwirkt, wirkt nicht.
Das ist die Absicht.

**Offen bis `00a`.** Das Prädikat der Gegenzeichnung ist benannt, nicht kodiert. Kein Testvektor
bis dahin.

### D126 — `key_mode` unterscheidet die Signaturform, nicht die Kardinalität

**Widerspruch auf `main`, innerhalb von vier Zeilen.** `00 §7` schreibt die Regel als
`akt.I ∈ resolve_current_key(akt.N)` — Mengenzugehörigkeit, für jede Mächtigkeit definiert — und
setzt darunter „für `key_mode = 0`: genau ein Schlüssel". Der Beispiel-Nukleus aus `00 §3.1` führt
`root_keys = [BRUNO, ANNA]` bei `key_mode = 0` und folgt damit der Formel, nicht der Prosa. Der
Fall ist keine Randlage, sondern der Zustand unmittelbar nach der Gründung.

**Beschluss: die Formel gilt, der Satz fällt.** `key_mode` wählt zwischen gewöhnlicher
Ed25519-Signatur und FROST-Gruppensignatur; in beiden Fällen trägt der Akt genau **eine**
Signatur. Bei mehreren autorisierten Schlüsseln genügt einer.

**Bestätigt durch die Literatur.** Weder TUF noch did:plc verwechseln Signaturform mit
Kardinalität: beide führen **mehrere** Schlüssel je Rolle, TUF mit einer Schwelle, did:plc mit
einer nach Autorität sortierten Liste.

**Nicht entschieden: die Schwelle.** Ob ein Nukleus statt „einer genügt" ein `k`-von-`n` verlangen
können soll, bleibt offen. Es wäre ein Verfassungsknopf nach `00 §4`, kein Protokolldefault, und
es ist der Punkt, an dem `root_keys` von einer Liste zu einer Rolle würde.

**Zur Fehlerform.** Zwei Durchgänge über `00` haben den Widerspruch nicht gesehen, weil Formel und
Prosa je für sich richtig aussehen und erst am gerechneten Beispiel auseinanderlaufen — dieselbe
Fehlerform wie D116, dort über einen Epochenwechsel, hier über eine Mächtigkeit größer eins.

### D127 — Der Rückhalt, nicht die Kette

D120 legt die Absturzordnung fest, sagt aber nicht, wo sie im Code sitzt. Die Frage stellte sich
beim Zählen: **die Kettenfortführung existiert dreimal.**

| Ort | Bestand |
|---|---|
| `tools/example_nucleus.py` | `_Author.claim`, `_h_prev = id_genesis_anchor(pub)` |
| `tests/helpers.py` | `Identity._append`, dieselben acht Argumente an `build_signed`, gleiche Zuweisung |
| `tools/sim/welt.py` | `Teilnehmer.claim_signieren`, `h_prev` als Hexdatei |

D122 hat **Bau und Signatur** ins Paket gezogen — `build_signed` — und die **Fortführung** an allen
drei Stellen gelassen. Die Oberflächen sind bereits auseinander: `helpers.py` trägt vier Helfer,
`_Author` einen. Und `welt.py` trägt D120s Defekt wörtlich: signieren, einlegen, Spitze schreiben,
ohne Redo, ohne `fsync`, ohne atomaren Rename. Harmlos nur, weil `Welt.anlegen` bei jedem Lauf
`rmtree` ruft.

**Beschluss 1 — die Naht liegt unter der Kettenfortführung.** Eine Fortführung, zwei Rückhalte
(Speicher, Dateien), ein Testsatz über beide. Der Rückhalt kennt fünf Operationen ohne
Protokollsemantik: Spitze lesen, Spitze schreiben, Redo lesen, Redo schreiben, Redo schließen. Er
rechnet **nie** `h_prev`.

Damit ist der Einwand aus `03-prompt` — „zwei Implementierungen von Kettenfortführung und Signatur
driften" — erfüllt statt umgangen: was doppelt ist, kann über `h_prev` nicht uneins werden, weil es
`h_prev` nicht kennt. Die Literatur gibt dazu die schärfere Fassung: ein Test-Double hält sich
nicht notwendig an den Vertrag der Sache, die es ersetzt, und veraltet unbemerkt, wenn die echte
Implementierung sich ändert. Die dort gezogene Konsequenz ist nicht Verzicht, sondern **ein
Testsatz über beide** — und Treue wird am Vertrag gemessen, nicht an der Implementierung.

**Beschluss 2 — der Redo-Eintrag trägt die signierten Claim-Bytes.** Abweichung vom Wortlaut
„Core-Redo-Eintrag" in D120, mit Begründung: die Signatur ist eine deterministische reine Funktion
der Core-Bytes (RFC 8032), und bei atomarem Schreiben ist „Core schreiben, dann signieren"
genauso sicher wie „signieren, dann Bytes schreiben" — die Absturzordnung, um die es D120 geht,
betrifft die **Spitze**. Der Gewinn: die Wiederaufnahme benutzt `claim_from_bytes` und braucht
**keinen zweiten Dekodierweg für Core-Bytes**, den es heute nicht gibt. Einen zweiten Kodierweg zu
vermeiden war der Zweck von D122; ihn beim Wiederanlauf einzuführen wäre derselbe Fehler mit
umgekehrtem Vorzeichen. Nebenertrag: `t` bleibt beim Fortsetzen zwingend unverändert, weil es aus
den Bytes kommt und nicht neu gesetzt werden **kann** — die Idempotenz hängt daran, und eine
Eigenschaft, die nicht verletzt werden kann, braucht keinen Test, der sie prüft.

**Beschluss 3 — Redo vor Spitze.** Die Prüfreihenfolge ist normativ. D120 zählt fünf Ausgänge auf;
der Zustand hat aber drei unabhängige Bits (Spitze gesetzt, Redo offen, Claim der Spitze bekannt),
und die Lage „Spitze leer, Redo offen" fehlt. Prüfte man die Spitze zuerst, führe sie in Ausgang 1
und baute einen **zweiten Genesis-Claim** mit neuem `t` — Selbst-Equivocation, genau der Fehler,
den D120 verhindern soll. Die Reihenfolge beseitigt die Lage, statt einen sechsten Ausgang zu
brauchen.

**Beschluss 4 — `claim_id` ist die Hochwassermarke.** D120 ist strukturell ein Redo-only-Log mit
idempotenter Wiederholung, also ARIES' „Repeating History". ARIES erkauft die Idempotenz über den
Vergleich der `pageLSN` mit der LSN des Log-Eintrags: ein zusätzliches Feld, eine zusätzliche
Invariante. MaR bekommt sie geschenkt, weil der Claim inhaltsadressiert ist — die Wiederaufnahme
fragt den Store, ob er die rekonstruierte `claim_id` kennt. **Kein „erledigt"-Flag, kein
zusätzlicher Zustand.** Daraus folgt, dass Ausgang 3 keine Fallunterscheidung braucht, wo der
Absturz lag: die Folge ab „aussenden" ist durchgehend idempotent, und die Wiederaufnahme ist
schlicht ihre Fortsetzung von vorn.

**Der Fork-Schalter.** `welt.py` trägt `kette_fortschreiben: bool = True`, damit die Simulation
absichtlich equivozieren kann. Die Fähigkeit bleibt nötig, das Flag nicht: der gefährlichste
Zustand der Kette darf kein Default-Argument an der gewöhnlichen Operation sein. Er wird eine
eigene, anders benannte Operation, und sie entsteht mit dem Umzug von `welt.py`, nicht vorher.

**Vertagt: Ausgang 5** (zwei eigene Claims auf dieselbe Spitze). Er ist keine Eigenschaft des
Spitzenzustands, sondern eine Abfrage über den Store, und die dafür nötige Schnittstelle
(`index.py`) ist ungeprüft. Schwerer wiegt: ein doppelt eingespielter Sicherungsblob erzeugt den
Fork in **zwei getrennten Stores**, von denen keiner beide Zweige sieht. Der Ausgang ist damit
durch eine Startprüfung gar nicht erreichbar, sondern erst bei der Vereinigung — was ihn zu einer
Frage an den Einlesepfad (D121) macht und nicht an die Spitze.

**Getragene Grenze: die Persistenzeigenschaften.** Der Datei-Rückhalt setzt drei Eigenschaften
voraus — atomares `os.replace`, `fsync` der Datei vor dem Rename, `fsync` des Verzeichnisses
danach. Sie werden im Modul benannt und sind **nicht geprüft**. Die Literatur ist an dieser Stelle
unangenehm eindeutig: ALICE (OSDI '14) fand 60 Crash-Vulnerabilities in elf ausgereiften
Anwendungen — darunter Git, SQLite, PostgreSQL, ZooKeeper —, weil die Persistenzeigenschaften
zwischen sechs verbreiteten Linux-Dateisystemen weit auseinandergehen; insbesondere garantiert ein
`fsync` auf eine Datei nicht, dass ihr Verzeichniseintrag persistiert ist, und ext3 im
Ordered-Mode persistiert in Reihenfolge und erzeugt damit eine falsche Sicherheit. Ohne
ALICE-Klasse-Werkzeug ist die Annahme argumentierbar, nicht prüfbar. Sie wird benannt statt
behauptet.

**Was dagegen prüfbar ist: die Zustandsmaschine.** Die Absturzpunkte liegen in der **Reihenfolge
der Operationen**, nicht im Rückhalt. Ein Rückhalt, der beim k-ten Schreibvorgang wirft,
aufgezählt über alle k, prüft sie erschöpfend — im Speicher, deterministisch, ohne Dateisystem.
`signieren` schreibt viermal (Redo, Aussenden, Spitze, Redo-Schluss), also fünf Läufe je Vektor
einschließlich des ungestörten. Der ungestörte Lauf ist die Referenz für alle anderen: **zwei
Läufe, eine Variable**, und deshalb braucht dieser Lauf **keinen neuen Golden Anchor**.

**Schnitt.** Zwei Läufe. Der erste baut `tools/autor.py` und rührt nichts an; der zweite zieht die
drei Stellen um und prüft gegen „426 grün, alle Anker byteweise unverändert". Neubau und Umzug
gemischt hieße, am Ende nicht zu wissen, welche der beiden Änderungen einen Anker bewegt hat.

### D128 — Der Halt ist eine Ableitung, und eine abgefangene Ausnahme ist ein Absturz mit Zeugen

Zwei Befunde aus der Abnahme des Autorlaufs, die dieselbe Wurzel haben: D120 beschreibt den
**Absturz**, und ein Absturz ist der einzige Fall, in dem das schreibende Objekt danach nicht mehr
existiert.

**Beschluss 1 — der Halt klebt am Objekt, nicht am Rückhalt.** `wiederaufnehmen` leitet den
Zustand bei jedem Aufruf aus Rückhalt und Ausgang neu ab; ein Halt aus Ausgang 4 heilt, sobald der
fehlende Claim nachgeliefert ist. Begründung: Ausgang 4 sagt „der Ausgang kennt die Spitze nicht",
und das ist eine Aussage über den Ausgang und nicht über die Kette. Ein klebriger Halt verlangte
einen Eingriff, wo keiner nötig ist, und wäre eine zweite Wahrheit neben dem Rückhalt — dieselbe
Linie wie D61: keine abgeleitete Größe wird zusätzlich gespeichert.

Der fremde Redo bleibt dagegen angehalten, solange er offen ist. Das ist keine Ausnahme von der
Regel, sondern dieselbe Ableitung über eine Lage, die sich nicht von selbst ändert. Der Prompt
hatte „nach `ANGEHALTEN` bleibt jeder weitere Aufruf `ANGEHALTEN`" verlangt; das war zu grob und
wird hier zurückgenommen.

**Beschluss 2 — innerhalb eines Objekts klebt der Halt sehr wohl.** Bricht in `signieren` ein
Schreibvorgang mit einer Ausnahme ab und **fängt der Aufrufer sie**, ist der Zustand des Objekts
derselbe wie nach einem Absturz — nur läuft der Prozess weiter. Ohne Halt baut der nächste Aufruf
einen zweiten Claim auf dasselbe `h_prev`: Selbst-Equivocation, beweisbar und dauerhaft, also
genau der Fehler, gegen den das Modul existiert.

Das ist keine Randlage. `DateiRueckhalt` wirft `OSError` bei vollem Datenträger, bei `EACCES`, bei
einer schreibgeschützt neu eingehängten Partition. Das sind Lagen der Welt, und ein Prozess, der
sie behandeln will, ist danach in einem Zustand, den D120 als „anhalten" führt.

**Beschluss 3 — der Halt gilt einheitlich für alle vier Schreibvorgänge**, auch für den letzten.
Bricht `redo_schliessen` ab, ist die Lage sachlich unbedenklich: der Claim ist ausgesandt, die
Spitze steht. Der Halt kostet dort ein `wiederaufnehmen` und nichts sonst, weil die Wiederaufnahme
idempotent ist. Eine Fallunterscheidung nach Schritt wäre teurer zu lesen als der Gewinn — und
jede Fallunterscheidung an dieser Stelle wäre eine Behauptung darüber, was der abgebrochene
Schritt bereits bewirkt hat, die das Objekt nicht prüfen kann.

**Zur Fehlerform — neue Prüfregel.** Die Absturzaufzählung konnte den Befund strukturell nicht
sehen: **jeder** ihrer Läufe baut nach dem Bruch einen frischen `Autor`. Der Injektor modellierte
den Absturz und nicht die abgefangene Ausnahme, obwohl beide durch denselben Code laufen.

> **Prüfregel 13 — Neustart als Annahme.** Modelliert ein Test einen Neustart, wird gefragt, ob
> dieselbe Ursache auch **ohne** Neustart eintreten kann. Wenn ja, ist der Weiterlauf ein eigener
> Vektor und keine Variante.

Sie ist die Umkehrung der Lehre aus dem Autorschaftslauf: dort lagen vier von vier Befunden in
Tests, hier liegt der Befund im Produktivcode und wurde durch die Frage gefunden, was der Test
**nicht** tut.

**Beschluss 4 — der Halt fängt `BaseException`, nicht `Exception`.** `KeyboardInterrupt` und
`SystemExit` erben nicht von `Exception`. In einem bedienten Werkzeug ist Strg-C während des
Signierens der wahrscheinlichste Abbruch überhaupt — wahrscheinlicher als der volle Datenträger,
mit dem Beschluss 2 begründet wurde —, und eine Schleife, die `KeyboardInterrupt` fängt und
weiterläuft, ist die übliche Bauform und keine exotische. Ohne die weite Klausel liefe genau
dieser Fall am Halt vorbei und ließe `_zustand` auf `NORMAL` stehen.

Die Klausel **schluckt nichts**: sie setzt den Zustand, räumt `_h_prev` und wirft mit nacktem
`raise` unverändert weiter. Das ist die anerkannte Ausnahme von der Regel gegen weite
`except`-Klauseln — die Regel selbst bleibt unangetastet, und für jede Klausel, die eine Ausnahme
nicht weiterreicht, gilt sie fort. Nebenbei gedeckt: `asyncio.CancelledError`, seit Python 3.8
ebenfalls `BaseException`.

**Beschluss 5 — der Halt am Objekt ist über `wiederaufnehmen` verlassbar.** Hier berühren sich
Beschluss 1 und 2: der Halt klebt am Objekt, aber die Ableitung liest den dauerhaften Zustand neu.
Dasselbe Objekt nimmt die Kette also wieder auf, ohne weggeworfen werden zu müssen — das ist der
vorgesehene Weg nach einem behandelten `OSError`. Der Satz braucht eine eigene Zusicherung, weil
ein späterer Lauf, der den Halt „richtig klebrig" machte, die Erholung bräche und dabei durch jede
bestehende Prüfung liefe.

**Abgenommen** mit `impl/autor` (`8615889`), 468 Tests. Der Weg dorthin ging über drei Läufe und
vier Befunde, von denen die letzten beiden — die Ausnahmeklasse und die Erholung — erst sichtbar
wurden, nachdem der Halt existierte. Das ist die gewöhnliche Reihenfolge: ein Mechanismus wirft
seine eigenen Fragen erst auf, wenn er da ist.

## AJ. Der absichtliche Fork

### D129 — `gabeln` fasst den dauerhaften Zustand nicht an

Die Zählung aus D127 war zu niedrig. Die Kettenfortführung existiert **fünfmal**:
`tools/example_nucleus.py`, `tests/helpers.py`, `tools/sim/welt.py` und zusätzlich
`tests/property/welten.py` (`_Signer`, Zeilen 64–91) — dazu seit dem Autorlauf `tools/autor.py`
als die einzige richtige. Zwei der vier alten erzeugen absichtlich Forks: `welt.py` über
`kette_fortschreiben` und `welten.py` über denselben Namen, gesteuert von `twin`.

D127 hatte entschieden, dass das Flag aus der Signieroberfläche verschwindet — der gefährlichste
Zustand der Kette darf kein Default-Argument sein. Die Ersatzoperation heißt **`gabeln`**.

**Beschluss: `gabeln` signiert und sendet aus, schreibt aber weder Redo noch Spitze.**

Der Punkt ist nicht offensichtlich und trägt die Entscheidung allein: Schriebe `gabeln` einen
Redo-Eintrag, machte ein späteres `wiederaufnehmen` den absichtlichen Fork zur **echten Spitze** —
der Zwilling würde zum Hauptzweig und der Hauptzweig zum Zwilling, und zwar still. Schriebe
`gabeln` die Spitze, wäre es kein Fork, sondern ein gewöhnlicher Anhang.

Es bleibt also nur, den dauerhaften Zustand gar nicht zu berühren. Das ist auch die richtige
Aussage über die Sache: ein absichtlicher Fork ist etwas, das ein Autor **neben** seine Kette
stellt, nicht etwas, das seine Kette tut. Die Wächter aus D128 gelten unverändert — `gabeln`
verlangt ein vorheriges `wiederaufnehmen` und verweigert im Zustand `ANGEHALTEN`.

**Das Szenario-Schema behält `kette_fortschreiben`.** `s5.json` führt das Feld viermal,
`szenario.py` liest es, und `sim-abnahme.md` schreibt Namen und Voreinstellung fest. Der Konflikt
mit D127 ist keiner: dort steht `false` ausdrücklich in einer Datendatei, von einem Autor, der
genau das will. Die Grenze liegt zwischen **Datei und Aufrufkonvention** — ein Szenarioautor, der
`false` schreibt, hat es getippt; ein Programmierer, der ein Argument wegläßt, hätte es nicht.
`szenario.py` verzweigt auf zwei benannte Operationen, statt ein Bool durchzureichen.

**Die vier alten Klassen bleiben als Oberflächen.** `Identity`, `_Author`, `_Signer` und
`Teilnehmer` behalten ihre Signaturen; damit ändert sich in den 26 Testdateien, die sie benutzen,
keine Zeile. Sie hören nur auf, Implementierungen zu sein. Der Zähler `_t` in `_Signer` bleibt bei
ihm: er ist eine Eigenschaft des Weltgenerators und nicht der Kette, und `t` bleibt Parameter von
`signieren`.

**Das Abnahmekriterium wird abgeleitet, nicht aufgezählt** (Lehre aus D122): nach dem Umzug findet
`grep -rn "_h_prev" tools/ tests/` nichts außerhalb von `tools/autor.py`, und keine der vier
Dateien importiert noch `build_signed` oder `id_genesis_anchor`. Eine Liste erlaubter Fundstellen
im Kriterium trüge dieselbe Schwäche wie die Sache, die sie prüft.

**Nicht mitrepariert: B-4** (die Zwillingsbuchführung in `welten()` zieht kein Budget ab). Der
Befund liegt in der Buchführung des Generators, nicht in der Kettenfortführung, und ist vom Umzug
unabhängig. Ihn mitzunehmen hieße, bei einer Ankerabweichung nicht zu wissen, welche der beiden
Änderungen sie bewegt hat.

## AK. Eine Tür pro Sprache

### D130 — Der Rundlauf ist eine Form, keine Fundstelle

D83 hat entschieden, dass `decode` und `is_canonical` im selben `try` stehen: der Rundlauf ruft
`encode` auf, und `encode` wirft bei Werten, die `decode` durchlässt. Der Beschluss wurde auf
`trust/groups.py` angewandt, von `profiles/payload.py` übernommen — und ist nie nach Layer 01
zurückgegangen. `verifier.structural_check` prüft die Kanonizität zwei Schritte nach dem
Dekodier-`try`, ungeschützt.

Die Parallelenprüfung zeigt Layer 01 als den Ausreißer unter drei gleichartigen Stellen:

```
02 groups.py:41   try: decode ; is_canonical   except Exception → UNPARSABLE_VOUCH_PAYLOAD
03 payload.py:18  try: decode ; is_canonical   except Exception → UNPARSABLE_V
01 verifier.py    try: decode                  except Exception → MalformedCbor
                  … is_canonical zwei Schritte später, ungeschützt
```

Der Vektor ist `h'a100ff'` — eine Map, deren **Wert** zu Schlüssel `0` das Break-Sentinel ist.
`decode` liefert ein `dict`, die Schlüsselprüfung 2b sieht nur Integer-Schlüssel und läßt es
durch, `is_canonical` ruft `encode` und bekommt `CBOREncodeError`. Die Ausnahme verläßt
`structural_check` als Nicht-`VerifierError`.

`h'a1ff01'` — Sentinel im **Schlüssel** — ist auf Layer 01 dagegen harmlos: Schritt 2b fängt es
vorher ab. Auf Layer 02 waren beide Vektoren gefährlich, weil `_decode_weight` keinen
Schlüsseltypfilter hat. **Ein Vektor, nicht zwei.** Die Tabelle aus D83 gilt für die dortige
Fundstelle und nicht für diese; sie ungeprüft zu übernehmen wäre derselbe Fehler noch einmal.

**Beschluss: der Rundlauf steht auf jeder Schicht im selben `try` wie das Dekodieren; was von dort
kommt, ist unlesbar.** Auf Layer 01 heißt das `MALFORMED_CBOR`.

Nicht aufgezählt wird, welche Ausnahmen `cbor2` werfen kann. Das ist eine Eigenschaft der
Bibliothek, nicht von MaR, und über die Version nicht stabil; tiefe Verschachtelung, die beim
Dekodieren durchgeht und beim Enkodieren rekursiert, wäre ein weiterer Geschwisterfall, den keine
Liste kennt. Der `try` fängt die Form, nicht die Namen.

**Kein `False` aus `is_canonical`.** Die naheliegende Vereinfachung — die Hilfsschicht fängt selbst
und meldet „nicht kanonisch" — löscht die Unterscheidung, die D83 gerade begründet hat: eine
Ablehnung als `NON_CANONICAL_ENCODING` behauptet, es gebe eine kanonische Kodierung desselben
Inhalts. Bei `h'a100ff'` gibt es die nicht. Auf Layer 01 wiegt das schwerer als auf 02, weil dort
zwei verschiedene Reject-Codes daran hängen und ein Absender in die falsche Richtung suchen würde.
`cbor_canon` bleibt dünn und wirft; die Zuordnung zum Code bleibt am Aufrufer.

**Die Reihenfolge bleibt erhalten.** „Im selben `try`" wörtlich genommen zöge die Kanonizität vor
die Schlüsseltypprüfung 2b. Der trennende Vektor ist `h'bf616100ff'` — die
indefinite-length-Kodierung von `{"a": 0}`: dekodierbar, nicht kanonisch, Schlüssel ist `str`.
Vorgezogen ergäbe er `NON_CANONICAL_ENCODING`, und das wäre falsch, denn die kanonische
Neukodierung derselben Map bliebe ein ungültiger Claim; Anhang B führt den falschen Feldtyp unter
`MALFORMED_CBOR`. Der Rundlauf bekommt also einen eigenen `try` **an seinem bisherigen Platz**,
nicht einen gemeinsamen weiter vorn. §6 Punkte 1–7 behalten ihre normative Ordnung, und D113
braucht keinen Abhängigkeitssatz.

**Warum es nicht folgenlos ist, obwohl die Entscheidung dieselbe bleibt.** `h'a100ff'` scheitert
zwei Schritte später ohnehin an der Längenprüfung von `m[1]`; falsch ist allein der Fehlerkanal.
Der trägt aber zwei Dinge: `_build_lifecycle_index`, `_find_revoking_claim` und
`_find_superseding_claim` fangen `VerifierError` und überspringen — ein `CBOREncodeError`
überspringt nicht, er reißt den Index-Aufbau ab, und ein einziger solcher Claim im Store legt
`classify_all` still. Und er ist die Ausnahme, an der D131 bräche, bevor sie geschrieben ist.

**Testpunkt an der Hilfsschicht.** `test_cbor_canon.py` hat keinen Vektor, der `is_canonical` zum
Werfen bringt. Drei Aufrufer verlassen sich darauf, dass sie es tut. Die Zusicherung gehört dorthin,
wo die Eigenschaft entsteht.

**Mitbefund: `Anhang B.2` führte indefinite-length unter `MALFORMED_CBOR`.** Der Code sagt etwas
anderes, und der Code hat recht. Eine indefinite-length-Kodierung, deren einziger Mangel die
Längenform ist, dekodiert sauber, passiert die Schlüssel- und Feldtypprüfung und scheitert erst am
Rundlauf — `NON_CANONICAL_ENCODING`. Das ist auch die richtige Aussage: es gibt eine kanonische
Kodierung desselben Inhalts, und sie ist eine andere. Genau die Bedingung, an der dieser Eintrag
die beiden Codes trennt. Unter `MALFORMED_CBOR` gehört die Längenform nur, wenn sie
**unabgeschlossen** ist, und das deckt „nicht dekodierbar" ab. B.2 verliert das Stichwort und
gewinnt „Nicht-uint-Schlüssel", das dort fehlte, obwohl §6 Punkt 2b es prüft.

Belegt durch **BV3** (`Anhang C.8`): TV1s signierte Map in indefinite-length-Form, 310 statt 309
Byte, re-serialisiert zu TV1s Bytes, `NON_CANONICAL_ENCODING`. Die drei Byte-Vektoren `BV1`–`BV3`
sind zusammen mit diesem Eintrag entstanden und normativ.

### D131 — Der Einlesepfad fängt `VerifierError`; „wirft nie" wird zugesichert, nicht gefangen

D121 verlangt eine Funktion, die nie wirft und entweder einen Claim oder einen Reject-Code liefert.
Die Frage, die der Beschluss offenließ: **was fängt sie?**

Fängt sie `Exception`, ist der Wortlaut erfüllt und die Sache verdorben. Ein Programmierfehler im
Erkenner würde dann zu `MALFORMED_CBOR` auf **jedem** Claim: das Netz sähe aus, als bestünde es aus
kaputten Bytes, der Store bliebe leer, und nichts zeigte an, dass die Ursache lokal ist. Das ist
D92 eine Ebene höher — eigene Fehler sind keine Lage der Welt.

Die Literatur hat die Grenze vor MaR gezogen. Joe Duffys Bericht über Midoris Fehlermodell
(2016) trennt **Bugs** von **behebbaren Fehlern** und behandelt sie mit verschiedenen Mitteln:
Fail-Fast für die einen, geprüfte Ausnahmen für die anderen, mit der Begründung, dass Bugs
grundsätzlich nicht behebbar sind und der Versuch, sie zu behandeln, systematisch zu unzuverlässigem
Code führt. Die Einteilung ist seither Konsens — Go, Rust, Swift und Zig sind bei ihr angekommen.

**Beschluss: der Einlesepfad fängt `VerifierError` und nichts sonst.** Alles andere schlägt durch.

**Die Totalität wird zugesichert, nicht erkauft.** Ein Eigenschaftstest über beliebige Bytes
behauptet, dass nichts anderes als ein `Claim` oder ein `ErrorCode` herauskommt. Dieselbe Bewegung
wie D75: eine Unmöglichkeit wird geprüft statt eine Semantik. Der Test ist zugleich derjenige, der
D130 heute rot machen würde.

**Verworfen: die Umkehrung.** Naheliegende Alternative wäre, `structural_check` selbst auf
Rückgabewerte umzubauen — elf `raise` werden elf `return` — und die werfende Fassung zum dünnen
Adapter zu machen. Das entspräche der Literatur besser. Der Grund dagegen ist nicht der Diff:
**auch diese Bauform macht „wirft nie" nicht strukturell.** Ein `AttributeError` im Erkenner
entkommt der Rückgabefassung genauso wie dem Wrapper. Die Totalität hängt in beiden Fällen am Test,
und dann gewinnt die Bauform, die elf Stellen mitten in Layer 01 und die daran hängenden
`pytest.raises`-Vektoren nicht anfaßt.

**Die Grenze verläuft an der Herkunft des Codes, nicht an der Breite der Klausel.**
`groups.py` und `payload.py` fangen `Exception` und bleiben richtig: in ihrem `try` steht ein
**fremder** Aufruf, dessen Ausnahmemenge weder aufzählbar noch versionsstabil ist. Im `try` des
Einlesepfads steht **eigener** Code, und dort verwandelt dieselbe Klausel Bugs in Weltlagen.
Gleiche Syntax, gegensätzliche Wirkung. Ein späterer Lauf, der D131 als „schmal fangen" liest und
auf die beiden anderen Stellen anwendet, macht sie kaputt.

### D132 — Fremde Bytes gehen an keiner Stelle durch `claim_from_bytes`

`structural_check` ist ein ordentlicher Erkenner: eine Tür, feste Reihenfolge, liefert strukturierte
Daten. Daneben steht `atom.claim_from_bytes` — dieselbe Sprache, schwächere Grammatik, keine
Kanonizitätsprüfung, keine Feldtypen, keine Signatur.

Das ist das Muster, gegen das LangSec geschrieben ist: der faktische Erkenner verteilt sich über
das Programm und deckt sich nicht mit den Annahmen der Programmierer über die Gültigkeit der Daten.
Die Gegenform heißt Recognizer Pattern — erst Erkennung, dann eine klare Grenze, jenseits derer die
Rohbytes nicht mehr erreichbar sind. Ein Wrapper um Tür eins läßt Tür zwei offen und ändert am
Muster nichts.

**Beschluss: fremde Bytes gehen an keiner Stelle durch `claim_from_bytes`.**

Der legitime Rest bleibt: `tools/autor.py` liest über diesen Weg den **eigenen** Redo, und das ist
nach D92 richtig. Die Voraussetzung wandert aus dem Kommentar in den Namen. Der Satz ist als Regel
formuliert und nicht als Liste von Aufrufstellen, weil eine Liste den nächsten Aufrufer nicht kennt
— Prüfregel 11.

Heute hat der Satz genau einen Verstoß im Produktivcode: `tools/sim/welt.py:86` in `store_laden`.
Alle übrigen Fundstellen sind Tests, die Vektor-Hex aus der Spec dekodieren, also eigene Bytes.

**Der Container wird auch im Dateinamen nicht geglaubt.** Die Inbox der Simulation adressiert über
`{cid.hex()}.cbor`, `zustellen` kopiert Bytes ohne Prüfung, und `hat_claim` beantwortet „kenne ich"
allein aus der Existenz des Dateinamens. Niemand rechnet nach, dass in `abc….cbor` ein Claim mit
`claim_id == abc…` steht. Die Inbox **ist** das unsignierte Bündel aus D121, nur als Verzeichnis;
der Satz „dem Container wird nie geglaubt" gilt für sie mit demselben Wortlaut. Der Zusammenhang
ist nicht bloß formal: `claim_id` ist der Hash über `core_bytes`, und erst die Kanonizitätsprüfung
bindet empfangene Bytes an diese Id. Ohne sie ist die Zuordnung von Name zu Inhalt eine Behauptung
des Absenders.

**Zuschnitt: zwei Läufe.** D130 und D131 sind Paketarbeit an Layer 01 — Reparatur im Bestand plus
`read_claim` daneben. D132 ist Werkzeugarbeit — Bündelformat, `store_laden` und `zustellen` über
den neuen Pfad, `claim_id` nachgerechnet. Getrennt, damit ein roter Bestandstest nicht in einer
Abnahme über neues Bündelformat untergeht.

## AL. Was der Erzeuger schuldet

### D133 — `welten()` erzeugt gültige Claims; die Vorbedingung liegt beim Aufrufer

Der Einlesepfad hat beim ersten Lauf etwas gefunden, wofür er nicht gebaut war. Die Messung aus
`impl/einlesen`: von 534 erzeugten Claims liefert `read_claim` 532 mal einen `Claim` und zweimal
`INCOHERENT_EXPIRY`. Die Lage `"vergangen"` in `tests/property/welten.py` zieht
`t_exp ∈ [1, now-1]` ohne Blick auf `t`; wo `t ≥ t_exp` herauskommt, entsteht kein abgelaufener
Claim, sondern gar keiner. Zwei Fundstellen — die Ziehung steht für den ersten Claim und für den
Zwilling.

**Warum es nie auffiel.** `classify_all` ruft `structural_check` nur für Lifecycle-Kandidaten beim
Indexaufbau, nie für den zu klassifizierenden Claim selbst. Die Eigenschaftstests klassifizieren
also Claims, die ein Empfänger zurückgewiesen hätte, ohne dass irgendwo eine Prüfung liegt, die es
merkt.

**`classify_all` trägt daran keine Schuld.** `02a §3` setzt strukturelle Gültigkeit voraus und legt
die Prüfung ausdrücklich beim Aufrufer ab; das ist der Grund, warum der schnelle Zwilling schnell
ist. Der Befund lautet nicht „`classify_all` prüft zu wenig", sondern „die Vorbedingung wird in der
Testschicht von niemandem hergestellt". Dieser Satz steht hier, damit kein späterer Lauf
`classify_all` repariert und es dabei langsamer und falscher zugleich macht.

**Beschluss: `welten()` erzeugt in der Voreinstellung ausschließlich strukturell gültige Claims.**

Die Begründung kommt aus D131 und ist erst seit ihm formulierbar: ein Store in einem
Eigenschaftstest modelliert, was ein Beobachter hält — und ein Beobachter hält seit dem
Einlesepfad genau das, wofür `read_claim` einen `Claim` geliefert hat. Ohne diese Regel sagen der
Erzeuger und der Einlesepfad Widersprüchliches über denselben Gegenstand, und jeder Lauf, der auf
beidem aufbaut, erbt den Widerspruch.

**Kein Verbot, nur eine Voreinstellung.** Ein Erzeuger, der auf Verlangen ungültige Claims baut,
ist etwas, das dem Einlesepfad noch fehlt. Der Unterschied liegt zwischen *versehentlich
ungültig* und *ungültig, wenn man es verlangt*; das erste ist der Befund, das zweite eine
Fähigkeit. Die Schalter `erlaube_ueberzeichnung` und `erlaube_equivocation` sind das Muster.

**Die Reparatur ist nicht die Schranke, sondern die Sichtbarkeit von `t`.** `_Signer.claim()` zählt
`_t` **innerhalb** der Methode hoch; der Aufrufer kennt das `t` erst, wenn der Claim signiert ist,
und kann deshalb keine Untergrenze setzen. Nach D129 bleibt der Zähler bei `_Signer` — er ist eine
Eigenschaft des Weltgenerators und nicht der Kette — und genau deshalb darf er auch gelesen werden.

Verworfen: eine feste Untergrenze wie `min_value=100`. Sie hielte nur, solange keine Welt mehr als
hundert Claims je Identität baut, und diese Schranke stünde nirgends.

**Vierte Lage `"grenze"` mit `t_exp = now`.** Die drei bestehenden Lagen decken `now ≤ t_exp`
überall ab **außer** an der Kante: `künftig` beginnt bei `now + 1`, `vergangen` endet bei
`now - 1`. Der Grenzwertvektor `now = t_exp` steht seit D119 als „baubar und ungebaut" in der
Offen-Liste — er war ungebaut, weil der Erzeuger ihn nicht ziehen konnte. Gewichtung
`4 : 4 : 1 : 1`; ein einzelner Punkt braucht keine Masse, er muss nur erreichbar sein.

**Der Schaden ist heute null, und das gehört dazu.** Ein Claim mit `t ≥ t_exp` und `t_exp < now`
landet ohnehin in `EXPIRED` — demselben Zustand wie ein sauber gebauter abgelaufener Claim — und
bindet kein Budget. Kein Fingerabdruck ändert sich, kein bestehender Anker bewegt sich. Der
Beschluss ist vorwärtsgerichtet und keine Fehlerbehebung an einem falschen Ergebnis.

### D134 — Die Budgetbuchführung des Erzeugers ist gruppenweise

`02 §3.1`: `n_budget = max n` über die Mitglieder einer Gruppe `(I, J, N)` im Budget-Set,
`Σ_J n_budget ≤ D` über die Gruppen. **Maximum innerhalb, Summe darüber.**

`welten()` führt `remaining[author] -= n` **pro Claim**. Das ist die falsche Form, und sie hat zwei
Symptome:

- **Der Zwilling.** Erster und Zwilling teilen `(I, J, N)`. Die Gruppe zahlt `max(n, n2)`, nicht
  `n + n2`. Im Regelfall `n2 = n - 1` kostet der Zwilling **nichts**; nur im Zweig
  `min(d_budget, n+1)` bei `n = 1` steigt das Maximum, und dann um eins.
- **Die Wiederholung.** Bürgt derselbe Autor in zwei Schleifendurchläufen für denselben
  Empfänger, zieht `remaining` zweimal ab, wo die Spec einmal das Maximum zählt.

**Verworfen: die wörtliche Reparatur von B-4.** „Der Zwilling zieht Budget ab wie der erste"
überzieht — sie addiert, wo die Spec maximiert, und verschärft die Unterschätzung, statt sie zu
beheben. B-4 war als eigener Befund richtig beobachtet und als Ursache falsch benannt; er geht in
diesem Eintrag auf und verschwindet aus der Offen-Liste.

**Der Zwilling gehört ins Budget-Set.** `02 §8`: ob ein geflaggter Bürge Fluss trägt, ist Policy
(`include_flagged`), die Budgetrechnung ist davon unberührt — ein Flag darf die Grundlage nicht
verschieben, auf der es erkannt wurde. „Zwilling ignorieren" ist damit ebenso ausgeschlossen wie
„Zwilling addieren".

**Die Ablaufregel erbt dieselbe Form.** `02 §3.1` gibt Budget erst frei, wenn **alle** Vouches der
Gruppe abgelaufen sind. `welten()` prüft `t_exp` je Claim. Eine Gruppe bindet also weiter, solange
ein Mitglied nicht abgelaufen ist — auch dann, wenn das nicht abgelaufene Mitglied der Zwilling
ist.

**Ein dritter Symptompfad, und er kehrt die Richtung um (Nachtrag).** Die beiden Symptome oben
teilen eine stillschweigende Annahme: dass der erste Claim einer Gruppe lebt. Trifft sie nicht zu,
bucht der Erzeuger nichts ab — richtig, denn ein abgelaufener Claim ist nicht im Budget-Set — aber
`lage2` wird unabhängig gezogen. Ist der Zwilling lebend, ist er das einzige Mitglied, das
`_in_budget_set` passiert, und die Gruppe zahlt `n2`, während der Erzeuger null gebucht hat. Über
mehrere Empfänger summiert sich das unbeschränkt: `Σ_J n_budget > D` ist bei
`erlaube_ueberzeichnung = False` erreichbar, und `derive.py` Schritt 4 setzt
`OVERCOMMITTED_AUTHOR`.

**Der Satz, den das ersetzt**, lautete: zu wenig Budget heiße zu wenige Vouches, nie eine
verletzte Invariante, `erlaube_ueberzeichnung = False` halte, was es verspreche. Er war aus der
zweigliedrigen Aufzählung darüber abgeleitet und hat deren Geltungsbereich still verloren —
dieselbe Form wie D77, D83, D87, D91, D130 und D135, und der Grund, warum Prüfregel 18 existiert.
Die Wirkung lag wieder nicht dort, wo die Zahl entsteht (Prüfregel 16): verfolgt worden war der
Zweig „der Erste lebt", nicht der andere.

**Kein falsches Grün heute, und das ist kein Trost.** Die Kombination
`erlaube_ueberzeichnung = False` mit `erlaube_equivocation = True` kommt einmal vor, in
`test_p3b_finds_equivocation_passed_to_pending`, und dessen Prädikat liest ausschließlich den
Auszählungszustand; Budget geht dort nirgends ein. Die Lücke ist heute folgenlos und wäre es ab
dem ersten Test nicht mehr, der auf dieser Kombination eine Trust-Aussage trifft. Genau der ist
der Zweck dieses Eintrags.

**Die Buchführung wird deshalb über lebende Mitglieder formuliert, nicht über den ersten Claim.**
`gruppe[(I, J)] = max n über die lebenden Mitglieder`, `verbraucht[I] = Σ_J gruppe[(I, J)]`,
Schranke `verbraucht[I] ≤ D`. Ein abgelaufenes Mitglied trägt null, gleich an welcher Stelle es
gezogen wurde. Der Preis der ersten beiden Symptome bleibt Abdeckung; der des dritten war es nie.

**Warum es trotzdem fällig ist.** Eine Eigenschaft mit `erlaube_ueberzeichnung = False` **und**
`erlaube_equivocation = True` ist heute nicht schreibbar: der Erzeuger kann nicht sagen, wie viel
Budget eine Welt mit Zwillingen verbraucht hat. Genau diese Kombination braucht jeder Test, der
Equivocation unter gültigem Budget prüfen will — und das ist die interessante Lage, weil
`include_flagged` dort seinen einzigen Sinn hat.

## AM. Ein Flag verschiebt die Grundlage nicht

### D135 — `EQUIVOCATION_FLAGGED` gehört ins Budget-Set

Gefunden auf dem Weg zu D134, an einer Zeile, die nicht zur Sache gehörte: `BUDGET_STATES` in
`trust/groups.py` führt `{ACTIVE, REVOKED, SUPERSEDED, PENDING}` und lässt
`EQUIVOCATION_FLAGGED` weg. Weil **beide** Claims eines Equivocation-Paars geflaggt werden, fällt
die ganze Gruppe `(I, J, N)` aus der Budgetrechnung.

**Gerechnet.** Ein Autor bürgt für B mit `n = D = 16`, equivoziert auf diesen Vouch
(`n₂ = 15`) und bürgt danach für C mit `n = 16`. Drei signierte Vouches, `Σ n_budget = 16`,
keine Findings. Der Autor hat sein Budget zweimal ausgegeben, und die Rechnung sieht ihn bei
einmal.

**Equivocation ist damit ein Budget-Reset — und er wirkt bei `include_flagged = True`.**
`derive.py` Schritt 5 schließt geflaggte Autoren **autorweit** aus den Kantenkandidaten aus, nicht
gruppenweit: bei `include_flagged = False` verliert der equivozierende Autor **alle** seine Kanten
im Scope, auch die zu C, und der Reset kauft ihm dort nichts. Bei `True` dagegen werden die Flags
vollständig ignoriert — und dann ist `Σ n_budget ≤ D` die einzige verbleibende Schranke gegen
einen Autor. Genau die hatte die Equivocation ersatzlos entfernt.

Das ist keine Randeinstellung. `02a` hält fest, dass die Ankerwerte in
`02-golden-anchors.md §3–§5` bei `include_flagged = True` gelten; die dokumentierte
Bezugskonfiguration ist die, in der das Loch klaffte.

`02 §3.1` sagt: „Kein selbst-bezüglicher Lebenszyklus-Akt gibt Budget frei; Budget folgt der Uhr,
nicht dem Willen des Autors." Equivocation ist kein Lebenszyklus-Akt und umgeht den Satz an ihm
vorbei. Der tragende Satz desselben Abschnitts — „die Deklaration selbst ist der Einsatz" — hält
nicht, wenn der Einsatz durch Doppelsignatur zurückgeholt werden kann.

**Beschluss: das Budget-Set ist `{ACTIVE, REVOKED, SUPERSEDED, PENDING, EQUIVOCATION_FLAGGED}`
und nicht abgelaufen. Ein Vouch verlässt es ausschließlich durch `t_exp`.**

Die Begründung ist dieselbe, mit der `02 §3.1` `pending` einschließt: der
Über-Commitment-Beweis beruht auf **Signaturen, nicht auf Aktivität**. Und `02 §8` sagt es
direkt — ein Flag darf die Grundlage nicht verschieben, auf der es erkannt wurde.

**Vier Stellen gegen eine.** `02 §8`, `02a §2.6` Satz nach der Tabelle („ausschließlich durch
`t_exp`"), `02a` zu `include_flagged` („Flags ändern nie die Budgetrechnung") und
`02-spec-nachzug §…` sagen dasselbe; allein die Aufzählung in `02a §2.6` sagt etwas anderes. Sie
steht **neun Zeilen** über ihrer eigenen Widerlegung, in derselben Tabelle-plus-Absatz-Einheit.
Die Parallelenprüfung hätte sie gefunden — sie ist auf diese Datei nie angewandt worden, weil
`02a` als erledigte Prompt-Datei galt und nicht als Text, gegen den geprüft wird.

**Wie es entstand.** Die Aufzählung listet die Zustände, in denen ein *gewöhnlicher* Claim landet.
Als Beschreibung war sie richtig; als Definition übernommen, hat sie still ihren Geltungsbereich
verloren. Prüfregel 8, zum vierten Mal nach D77, D83, D87, D91 — und diesmal in der teuersten
Fassung, weil die falsche Hälfte in Code gegossen wurde.

**Sprengweite gemessen, bevor entschieden wurde.** Mit erweitertem `BUDGET_STATES`: 488 Tests
grün, einer rot. Die Golden Anchors aus `02-golden-anchors.md §3–§5` bewegen sich **nicht**;
Variante A bleibt trotz geflaggter CAROL innerhalb `D`.

**Der rote Test ist der Befund selbst.** `test_no_vouch_without_texp_on_flagged_author` behauptet,
ein geflaggter Vouch ohne `t_exp` erzeuge kein `VOUCH_WITHOUT_TEXP`. Das folgt aus der Whitelist
und aus nichts sonst. Unter dem Beschluss bindet dieser Vouch Budget **für immer** — genau die
Lage, vor der das Finding warnt (`02 §…`: `t_exp` ist für Vouches in Scopes mit Budgetregel
verpflichtend). Die Erwartung dreht sich um: das Finding **muss** fallen. Findings sind
bedeutungsblinde Diagnosen; dass der Autor ohnehin slashbar ist, macht die Dauerbindung nicht
kleiner.

**D134 hängt daran.** Die gruppenweise Buchführung in `welten()` kann nicht gebaut werden, bevor
feststeht, wogegen sie rechnet. Reihenfolge: D135, dann `welten.py`.

**Nachtrag zur Wirkung.** Der Absatz über den Budget-Reset stand zuerst in der Gegenrichtung: er
behauptete, der Reset wirke bei `include_flagged = False`, weil der Autor dort „nur die Kante zu B"
verliere. Das war falsch — die Ausschlussmenge in `derive.py` Schritt 5 ist autorweit. Aufgefallen
ist es beim Lesen des Regressionstests, nicht beim Schreiben des Eintrags: `Σ n_budget` war
ausgerechnet, aber nicht bis zu seinem Verbraucher verfolgt.

Daraus die **Wirkungsprüfung**: bevor einem Befund eine Folge zugeschrieben wird, wird der falsche
Wert bis zu der Stelle verfolgt, die ihn verbraucht. Die Wirkung liegt nie dort, wo die Zahl
entsteht. Der Beschluss selbst ist davon unberührt — vier normative Stellen gegen eine Aufzählung,
und das Finding muss fallen.

## AN. Ein Verweis auf gelöschten Text

### D136 — Gelöschte Prompt-Dateien werden umgelenkt, nicht wiederhergestellt

Achtzehn Docstring-Zitate in zwölf Quelldateien zeigen auf `fuzz-prompt.md` und `sim-prompt.md`.
Beide Dateien sind gelöscht. `check_specs.py` führt sie nicht, kann sie also nicht prüfen — und
nach Prüfregel 17 sind sie normativer Text, solange Code auf sie zeigt.

**Ein Verweis auf gelöschten Text ist schlechter als kein Verweis.** Er sieht aus wie eine
Verankerung und ist keine. Wer `welten.py` liest und `fuzz-prompt.md §2` nachschlagen will, findet
nichts und muss raten, ob die Regel noch gilt, wo sie steht oder ob sie je bestand. Ein Docstring
ohne Quellenangabe hätte ihn wenigstens nicht in die Irre geschickt.

**Beschluss: die Zitate werden auf `werkzeuge.md` umgelenkt. Die gelöschten Dateien kehren nicht
zurück.**

Die Begründung ist, dass `werkzeuge.md` kein Ersatzdokument ist, sondern der Nachfolger mit
demselben Inhalt in eigenen Paragraphen: `§4.1` der Generator, `§4.2` die sechs Eigenschaften
`P-1` bis `P-6`, `§2.4` `gabeln` — dort ausdrücklich „für die Simulation (S5) und die
Eigenschaftstests (P-3b) und für nichts sonst" —, `§3.1` bis `§3.3` die Simulation. Die Löschung
war richtig; nur die Docstrings wurden nicht nachgezogen.

**Verworfen: Wiederherstellung aus der Historie.** Sie brächte zwei Dateien zurück, die dasselbe
sagen wie `werkzeuge.md`, und schüfe genau die Parallele, deren stilles Auseinanderdriften
Prüfregel 8 fängt. Zwei Quellen für eine Aussage sind auf Dauer teurer als ein toter Verweis, weil
der tote Verweis wenigstens beim Nachschlagen auffällt.

**Die Tabelle ist normativ.**

| Zitat im Code           | Ziel                |
|-------------------------|---------------------|
| `fuzz-prompt.md §2`     | `werkzeuge.md §4.1` |
| `fuzz-prompt.md §3`     | `werkzeuge.md §4.2` |
| `fuzz-prompt.md §7`     | `werkzeuge.md §2.4` |
| `sim-prompt.md` (ohne §)| `werkzeuge.md §3`   |
| `sim-prompt.md §2`      | `werkzeuge.md §3.1` |
| `sim-prompt.md §3`      | `werkzeuge.md §3.2` |
| `sim-prompt.md §6`      | `werkzeuge.md §3.3` |

Beigefügte Zusätze bleiben, wie sie sind: `02 §7`, `01 §6`, `INV-04.3`, `P-1`. Sie zeigen auf
lebende Dateien. Passt ein Zitat nicht in die Tabelle, wird es gemeldet und nicht geraten.

**Stehende Prüfung daraus.** Vor der Löschung einer Prompt-Datei wird gegriffen, ob Code auf sie
zeigt. Zeigt er, wird im selben Lauf umgelenkt. Eine Löschung, die Verweise hinterlässt, ist nicht
abgeschlossen — und beide hier haben zwei Sitzungen überdauert, weil niemand die Frage gestellt
hat.

## AO. Eine Existenzbehauptung handelt keine Abdeckung

### D137 — `find` bekommt ein festes Budget und einen festen Seed

Drei Tests behaupten die **Existenz** einer Welt statt einer Eigenschaft über viele:
`test_p3a_finds_overcommit_violation`, `test_p3b_finds_equivocation_passed_to_pending` und
`test_finds_budget_exit_via_clock`. Alle drei rufen `find(..., settings=settings())` und erben
damit das Profil aus `tests/property/conftest.py` — unter `schnell` zehn Beispiele, dazu einen
frischen Zufallsseed je Lauf.

**Der Befund: `main` bei `40ee7a5` ist auf einem kalten Klon rot.** Gemessen mit gelöschtem
`.hypothesis/` und altem Generator: `p3a` und `p3b` scheitern beide mit `NoSuchExample`. Grün
waren sie zwei Sitzungen lang, weil die Beispieldatenbank die gefundenen Welten vorhielt — und
`.hypothesis/` ist gitignored. Grün war eine Eigenschaft der Arbeitskopie, nicht des Commits.

**Aufgefallen ist es auf dem Weg zu etwas anderem.** Der Lauf `impl/welten` meldete `p3a` als neu
fragil und vermutete die geänderte Ziehungsreihenfolge. Die Gegenprobe kehrt das um: kalt bei
`4da3304` grün, kalt bei `40ee7a5` rot, einzige verhaltenswirksame Variable `welten.py`. Der Lauf
hat den Test nicht zerbrochen, er hat ihn repariert. Der Defekt lag woanders und war älter.

**Beschluss: `find` läuft mit `max_examples=200` und `derandomize=True`, unabhängig vom Profil.**

Die Begründung ist, dass `schnell` gegen `voll` **Abdeckung gegen Zeit** handelt. Bei einer
Eigenschaft über viele Welten ist das ein sinnvoller Handel: weniger Beispiele heißt weniger
geprüfte Fälle, aber jede geprüfte Aussage bleibt wahr. Eine Existenzbehauptung hat nichts zu
handeln — die Antwort ist ja oder nein. Ein Nein aus Zeitmangel ist von einem Nein aus Sachgrund
nicht zu unterscheiden, und genau diese Verwechslung hat hier zwei Sitzungen überdauert.

`derandomize=True` nimmt dem Test das Streuen über Läufe. Bei einer Eigenschaft wäre das ein
Verlust; hier ist es der Zweck. Findet ein Lauf nichts, ist das nach `werkzeuge.md §4.2` der
Befund — und er soll reproduzierbar sein, nicht launisch.

**Die Zahl ist gemessen, nicht geraten.** Unter festem Seed genügen zehn Beispiele für alle drei.
Zweihundert ist Faktor zwanzig Abstand zum Rand. Null Abstand wäre auf andere Weise spröde: die
nächste Generatoränderung verschiebt den Ziehungsstrom, und ein fester Seed ohne Reserve ist dann
dauerhaft rot statt gelegentlich.

**Verworfen: die gefundene Welt als festen Vektor einfrieren.** `test_p3.py` führt zwei solche
Vektoren, und sie behaupten etwas anderes als die Suche. Ein Vektor sagt „diese Welt verletzt die
Eigenschaft"; die Suche sagt „**der Erzeuger erreicht diese Gegend**". Das zweite ist die Aussage,
die hier gebraucht wird, und genau sie ist eingetreten und war unsichtbar. Ein späterer Lauf, der
die Suche gegen einen Vektor tauscht, löscht die Aussage und hält es für Aufräumen. Dieser Absatz
steht hier, damit er es nicht tut.

**Der gemessene Preis, und was er wirklich ist.** Nach der Umstellung steht `make check` bei 16,46 s
gegen 10,09 s zur Prompt-Grundlinie und gegen 6,44 s zum warmen Arbeitsstand. Die zweite Zahl ist
die ehrliche: `find` spielt nicht mehr aus `.hypothesis/` ab, und die alte Laufzeit war ein
Cache-Preis, kein Rechenpreis. Die Kosten sind nicht gestiegen, sie sind zum ersten Mal sichtbar.
Dieser Absatz steht hier, damit der Satz "D137 hat den Testlauf verlangsamt" nicht in einem Jahr als
Argument gegen D137 wiederkommt.

**Verworfen: `.hypothesis/` einchecken.** Es macht den Cache zur Grundlage statt ihn zu
entwerten — dieselbe Abhängigkeit, nur committet.

**Messfehler in der eigenen Vorarbeit, für die Akte.** Die Laufzeiten zu dieser Entscheidung waren
zuerst unbrauchbar: `derandomize=True` schaltet die Beispieldatenbank nicht ab, der erste
Messlauf füllte sie, der zweite las daraus. `n=200` kam auf 7,59 s, `n=10` auf 12,45 s — bei
festem Seed unmöglich. Zwei Läufe, zwei Variablen. Der Fund-Befund selbst ist davon unberührt,
weil er unter festem Seed nicht vom Cache abhängt; die Kosten misst deshalb `make check` und
nichts sonst.

## AP. Die Tür der Simulation

### D138 — Lauf B ist zwei Funktionen; der Einlesepfad lädt ohne Store

Drei Beschlüsse, jeder mit eigener Begründung, weil sie unabhängig voneinander falsch sein können.

**Erstens: das Bündelformat gehört nicht in diesen Lauf.**

Der Zuschnitt-Absatz in D132 zählt Lauf B als drei Dinge auf — Bündelformat, `store_laden` und
`zustellen` über den neuen Pfad, `claim_id` nachgerechnet. Das erste folgt aus keinem der beiden
normativen Sätze von D132. D132 schreibt selbst: die Inbox **ist** das unsignierte Bündel aus
D121, nur als Verzeichnis. Wenn sie es ist, verlangt D132 kein neues Format; die Aufzählung hat es
aus D121s Kontext mitgebracht, wo es hingehört.

Dieselbe Form wie D77, D83, D87, D91, D130, D134 und D135: ein Satz und eine Aufzählung, und die
Aufzählung hat beim Wandern still ihren Geltungsbereich gewechselt. Prüfregel 18.

**Lauf B ist damit `store_laden` und `hat_claim`, und sonst nichts.** `zustellen` schiebt
unvertraute Bytes zwischen unvertrauten Verzeichnissen; die Grenze liegt beim Lesen, nicht beim
Kopieren. Ein zweiter Erkenner an der Kopierstelle wäre genau der über das Programm verteilte
Erkenner, gegen den D132 geschrieben ist.

**Zweitens: `store_laden` ruft `read_claim(data)` ohne Store.**

`structural_check` benutzt den Store an genau einer Stelle: `_check_foreign_lifecycle`. Ohne Store
ist diese Prüfung nicht falsch, sondern **stumm** — Ziel unbekannt, also kein Reject. Dasselbe
Muster wie in `classify`: „bei bekannter Ziel-Identity".

Der Grund gegen einen durchgereichten Store ist nicht, dass er beim Laden halbfertig wäre; das ist
das Symptom. Der Grund ist, dass ein Teilstore `FOREIGN_LIFECYCLE` **an die Hex-Sortierung von
Dateinamen bindet**. Derselbe Claim wäre je nach Ladereihenfolge Reject oder nicht. Ein Reject,
den ein Beobachter nur bei günstiger Hash-Reihenfolge sieht, ist schlimmer als keiner: er macht
die Ablehnung selbst zu einer lokalen Laune. `werkzeuge.md §4.2` P-1 — Reihenfolgeunabhängigkeit —
ist die Eigenschaft, gegen die dieses Projekt seit zwei Sitzungen prüft, und sie gilt für den
Einlesepfad genauso wie für die Ableitung.

Ohne Store ist die Prüfung stumm und **gleichbleibend** stumm. Die Kontextarbeit macht
`classify_all` später auf dem vollständigen Bestand, wo sie hingehört.

**Vermerk, damit es niemand für einen Fehler hält.** `FOREIGN_LIFECYCLE` hat damit im
Produktivcode keinen Träger mehr. Der Code existiert, Vektortests prüfen ihn, und der einzige
Produktivpfad, der ihn auslösen könnte, ruft ohne Store. Das ist vertretbar, weil `index.py` die
Prüfung als Zustandsprüfung ein zweites Mal führt und dort `ForeignLifecycle` wirft. Es ist aber
eine Aussage und kein Zufall, und ohne diesen Absatz hält sie in einem Jahr jemand für einen Bug
und repariert sie in die falsche Richtung.

**Drittens: `hat_claim` glaubt dem Dateinamen nicht.**

Heute ist `hat_claim` ein `is_file()` auf `{cid.hex()}.cbor`. Niemand rechnet nach, dass in
`abc….cbor` ein Claim mit `claim_id == abc…` steht. `claim_id` ist der Hash über `core_bytes`,
und erst die Kanonizitätsprüfung bindet empfangene Bytes an diese Id — ohne sie ist die Zuordnung
von Name zu Inhalt eine Behauptung des Absenders.

Der Name bleibt der Hinweis, wo nachzusehen ist. Die Antwort kommt aus dem Inhalt.

**Die Wirkung liegt nicht dort, wo der Fehler entsteht.** `Teilnehmer.kennt` ist der
`Ausgang.kennt`-Port, den `Autor.wiederaufnehmen` in `tools/autor.py:189` befragt, um zu
entscheiden, ob die gespeicherte Spitze im Ausgang vorliegt. Ein falsches „kenne ich" aus einem
Dateinamen lässt `wiederaufnehmen` die Kette über einen Vorgänger fortschreiben, den niemand hält
— statt sie nach D120 anzuhalten. Ein Absender kann heute die Kette des Empfängers stören, **ohne
eine einzige Signatur zu fälschen.** Das ist der Grund für diesen Lauf; die nachgerechnete
`claim_id` ist nur das Mittel.

**Der Preis ist gemessen und wird bezahlt.** `zustellen` fragt für jede Datei bei jedem Ziel
`hat_claim`; aus einem `is_file()` wird ein Lesen plus Prüfen. Die Szenarien laufen mit `nur=` und
über Inboxen einstelliger Größe, die Zahlen tragen es. Kein Cache und kein Index — ein Index wäre
wieder etwas, dem geglaubt wird, und damit derselbe Fehler eine Ebene höher.

**Zurückgestellt: eine Meldung übersprungener Claims.** `store_laden` überspringt still, was
`read_claim` als `ErrorCode` liefert; das ist nach D133 die richtige Semantik — ein Beobachter
hält genau das, wofür `read_claim` einen `Claim` geliefert hat. Ein Zähler oder ein Protokoll wäre
ein zweiter Kanal aus derselben Funktion und verbreiterte den Port, den D127 schmal hält. Wenn
sich beim Debuggen von Szenarien herausstellt, dass die Stille teuer ist, ist das ein eigener
Fork mit eigener Begründung und nicht ein Zusatz hier.

**Gemessen vor dem Prompt:** es gibt heute keinen Test, in dem Dateiname und Inhalt
auseinanderfallen. `tests/test_sim.py` führt einen parametrisierten Szenariotest und berührt
weder `inbox_path` noch `fromhex`. Der Regressionstest ist deshalb neu zu bauen, und die
Rücknahmeprobe hat einen eindeutigen Ort.

### D139 — Distanz ist kaufbar; der Satz vom doppelten Schutz fällt

**⚠️ Die Zahlen dieses Eintrags sind durch D141 ersetzt** (`02 §4`, Warnblock). Der Befund
bleibt, die Rechnung war falsch: `Σ C(h)` ist eine Schranke, kein Ertrag.

Ausgelöst durch die Frage, was ein erster realer Einsatz eigentlich prüfen würde. Vorgeschaltet
war eine Literaturprüfung (Prüfregel 15), weil das Problem außerhalb von MaR seit
fünfundzwanzig Jahren bearbeitet wird. Ergebnis der Prüfung: die Feldfrage und die
Angriffsfrage sind verschiedene Fragen, und die zweite ist heute entscheidbar, ohne einen
einzigen weiteren Menschen.

**Erstens: der Satz vom doppelten Schutz fällt.**

Das Korollar in `02 §4` schließt mit der Beobachtung, eine seed-ferne Angriffskante sei ohnehin
billig, weil `C(h) = ⌊C₀ γ^{d(s,h)}⌋` mit der Distanz falle. Der Satz behandelt `d(s,h)` als
Eigenschaft des ehrlichen Knotens. Das ist sie nicht: `d` ist die BFS-Distanz über dem
**aktuellen** wirksamen Kantenset `E⁺`, und dieses Kantenset gestaltet der Angreifer mit.

Der Satz ist außerdem eine **Kostenaussage** — „billig" —, und ein Kostenmodell für verwirrte
ehrliche Knoten hat die Spec nirgends. Die Schranke selbst braucht keines: sie ist eine Aussage
über den Graphen, wie er vorliegt. Der angehängte Satz behauptet mehr, als der bewiesene Satz
trägt, und verliert dabei still den Geltungsbereich seiner eigenen Begründung.

**Zweitens: der Angriff wird benannt, nicht abgewehrt.**

Ein Angreifer, der einen seed-nahen ehrlichen Knoten `p` verwirrt, kann durch Bürgschaften bis zu
`min(D, C(p))` andere ehrliche Knoten gleichzeitig näher an den Seed ziehen und damit deren
Kapazität heben. Entscheidend ist die Rollenverteilung: `p` bürgt für **ehrliche** Knoten, nicht
für Sybils, ist also kein Grenzknoten im Sinne des Satzes und taucht in `Σ_{h ∈ Grenze} C(h)`
überhaupt nicht auf. Gekauft wird genau der Knoten, den die Schranke nicht sieht, und er
multipliziert die Kapazität derer, die sie sieht.

`02 §4` bekommt dazu einen Warnabsatz. Kein neuer Mechanismus, keine Änderung an Kapazität,
Budget oder Fluss: die Spec sagt an der Stelle, was gilt, statt an der Stelle etwas zu
versprechen, was sie nicht hält.

**Drittens: der Min-Cut-Beweis bleibt unangetastet.**

`maxflow(s → S) ≤ Σ_{h ∈ Grenze} C(h)` ist korrekt, die `|S|`-Unabhängigkeit steht, und
„Identitäten gratis, Kanten teuer" steht ebenfalls. Was fällt, ist allein die Behauptung, die
zweite Verteidigungslinie sei von der ersten unabhängig. Sie ist es nicht — beide werden aus
demselben Vorrat verwirrter ehrlicher Menschen bezahlt.

**Gemessen vor dem Prompt.** Mit den Anker-Parametern `γ = ½`, `C₀ = 16` und `D ≥ C₀` (§8) ist
`C(d) = 16, 8, 4, 2, 1, 0` für `d = 0…5`. Ein verwirrter Knoten `p` bei `d = 1` trägt `C(p) = 8`
und hat wirksamen Out-Degree `min(D, C(p)) = 8`. Acht ehrliche Knoten bei `d ≥ 5` tragen `C = 0`
und sind nach `§3` nicht einmal bürgschaftsfähig; nach `p`s Bürgschaft sitzen sie bei `d = 2` und
tragen je `C = 4`. Die Grenzsumme steigt damit von `0` auf `32`. Allgemein ist der Ertrag
`C(p) · ⌊γ · C(p)⌋`, also **quadratisch in der Kapazität des einen teuren Knotens**. Ohne den
Trick müsste derselbe Angreifer acht Menschen bei `d = 2` verwirren; sobald Seed-Nähe teurer ist
als Seed-Ferne — und darauf beruht das gesamte Distanz-Decay-Argument —, ist der Trick strikt
billiger. Die Zahlen sind gerechnet, nicht gemessen; der Simulationslauf hat damit einen
abgeleiteten Erwartungswert und keine getippte Menge.

**Belege aus der Literatur.** Levien betrieb die Advogato-Metrik jahrelang mit echten Nutzern und
berichtet als Ergebnis, die Metriken hätten ihren Zweck erfüllt, entscheidend sei aber die
Deckung zwischen den Annahmen der abstrakten Berechnung und der realen Implementierung. Der
eigentliche Defekt kam nicht aus dem Feldbetrieb: Ruderman fand beim Nachlesen des Beweises, dass
dieser über die Kapazitäten **nach** dem Angriff beschränkt statt über die davor, und
konstruierte daraus einen Ertrag im Quadrat der Angriffskosten. MaRs Kapazitätsmodell ist
dasselbe Distanz-Decay, also überträgt sich die Konstruktion. Bei Secure Scuttlebutt fand der
Feldbetrieb dafür anderes — Replikationslecks, eine Kanonisierung ohne deterministische
Schlüsselordnung, ein einzelnes langlebiges Signaturschlüsselpaar. Zwei davon sind in MaR
strukturell geschlossen, das dritte ist die offene Schlüsselrotation. Die Lehre für die
Reihenfolge: **Feldbetrieb findet Implementierungsränder, Nachrechnen findet Beweislücken.**

**Nicht entschieden.** Ob ein Mechanismus reagieren soll, bleibt offen und ist ein eigener Fork
mit sozialer Konsequenz — es geht darum, wessen Position kaufbar ist. Offen bleibt insbesondere,
ob die PageRank-Relaxation aus `02 §5` an dieser Stelle robuster ist als der maßgebliche
Max-Flow; Ruderman hält PageRank für unempfindlich, weil der erlangte Score durch den
Vor-Angriffs-Score der verwirrten Knoten beschränkt bleibt. `02 §5` ist zum Zeitpunkt dieses
Eintrags ungelesen, die Übertragung daher Hypothese und ausdrücklich keine Entscheidung.

**Prüfregel 20 — Kostenaussage braucht Kostenmodell.** Ein Satz, der etwas „billig", „teuer"
oder „ohnehin unattraktiv" nennt, ist eine Aussage über Angriffskosten. Steht in der Spec kein
Kostenmodell, das ihn trägt, fällt der Satz — auch und gerade dann, wenn der Satz daneben
bewiesen ist. Ein bewiesener Nachbar macht eine unbelegte Behauptung nicht wahr, er macht sie
nur schwerer sichtbar.

**Neuntes Auftreten der Form „Satz und Anhang".** Nach D77, D83, D87, D91, D130, D134, D135 und
dem Zuschnitt-Absatz in D132 ist dies der neunte Fall, in dem eine tragende Aussage einen zweiten
Satz mitführt, der ihren Geltungsbereich still überschreitet. Prüfregel 18 fängt die Form beim
Hinsehen; gefunden wurde sie auch diesmal nicht beim Lesen der Spec, sondern beim Versuch, gegen
sie zu argumentieren.

### D140 — Abschnitt 5 wird auf D45 nachgezogen; die Relaxation ist gegen den Distanzkauf immun

Aufgefallen beim Versuch, die in D139 offengelassene Frage aus `02 §5` zu beantworten: der
Abschnitt beschrieb das Gegenteil dessen, was seit D45 gilt.

**Erstens: die Layer-Datei widersprach dem Register.**

`02 §5` führte `P` als spaltenstochastisch über `Σw` normalisiert — zweimal im Fließtext und in
einem Blockabsatz, der diese Normalisierung gegen `§4` rechtfertigte und sie „genau die
Trennlinie zwischen beiden Sichten" nannte. D45 hat beides aufgehoben: normativ gilt
`P[J][I] = n_kante(I, J) / D` ohne Kopplung an andere Kanten, und die D9-Ausnahme für `§5`
entfällt **ersatzlos**, womit `§7` in beiden Sichten gilt. Der Rechtfertigungsabsatz, der noch
in der Layer-Datei stand, **war** der gestrichene Sonderstatus.

`02b-golden-anchors.md` führt unter K9 die richtige Fassung, die Implementierung folgt K9, und
die Testnamen in `tests/trust/` nennen die spaltenstochastische Fassung ausdrücklich als die
verworfene. Kein Test konnte deshalb rot werden: **nur die Spec war falsch.** Genau das ist die
Driftform, gegen die das Register gebaut ist — die Entscheidung war getroffen, begründet und
implementiert, und die Datei, die ein Leser zuerst aufschlägt, sagte das Gegenteil.

Nachgezogen wird ausschließlich Text. Kein Mechanismus, keine Zahl, kein Anker ändert sich.

**Zweitens: die überholte Zeile in `02-spec-nachzug.md` wird markiert, nicht stillschweigend
umgeschrieben.** Sie steht unter „Was danach noch offen ist" und trägt die D27-Fassung. Ein
falscher normativer Satz in einer Bestandsliste ist teurer als ein sichtbar aufgehobener, also
bleibt der ursprüngliche Verweis stehen und bekommt die Aufhebung danebengeschrieben.

**Drittens: die offene Frage aus D139 ist beantwortet — mit korrigierter Begründung.**

Der Distanzkauf greift in `§5` nicht. Ich hatte das zunächst damit begründet, `§5` kenne keinen
Distanzterm. Das ist **falsch**: `C(x)` geht sehr wohl ein, nämlich als Filter darüber, welche
Kanten in `E⁺` liegen (Anker K13, so auch der Kommentar in `trust/relax.py`). Ein verwirrter
seed-naher Knoten kann den Kantensatz von `§5` also durchaus verändern — Knoten mit `C = 0`
werden emissionsfähig, sobald sie näher an den Seed rücken.

Der tragende Grund ist ein anderer und ist Rudermans eigener: das **Gewicht** einer Kante hängt
nicht von `C` ab, und wegen `Σ n ≤ D` ist jede Spalte von `P` sub-stochastisch. Ein Knoten gibt
höchstens weiter, was er empfängt. Der Ertrag des Angriffs bleibt damit durch die
**Vor-Angriffs-Masse** der verwirrten Knoten beschränkt; ein quadratischer Term entsteht nicht.
Die Immunität kommt aus der Massenerhaltung, nicht aus der Abwesenheit einer Größe.

Das macht `§5` **nicht** zum Ersatz für `§4`. Die Relaxation trägt keine harte Schranke und ist
für Gates verboten; sie ist unverwundbar, weil sie nichts verspricht. Damit steht der Trade-off
sauber: **die Verwundbarkeit von `§4` ist der Preis der harten Schranke.** Der Min-Cut-Beweis
braucht eine harte Knotendecke, die Decke braucht eine Positionsgröße, und jede Positionsgröße
über dem Vouch-Graphen ist mit Vouches beeinflussbar.

**Der Fork lautet damit präziser als in D139:** Gibt es eine harte Knotendecke, die nicht über
den Graphen gekauft werden kann? Das ist eine Literaturfrage — die SybilLimit-Linie arbeitet mit
Random Routes statt mit Distanz — und sie ist groß genug für eine eigene Runde. Sie bleibt offen
und wird hier ausdrücklich nicht entschieden.

**Gemessen.** Einträge, die im Titel eine Korrektur eines älteren Eintrags ausweisen: **genau
einer**, D45. Und genau dieser eine war nicht nachgezogen. Die Stichprobe ist klein, die
Trefferquote ist eins. Träger des veralteten Satzes außerhalb des Registers: zwei Zeilen in
`02-trust-flow.md` plus der Rechtfertigungsabsatz, eine Zeile in `02-spec-nachzug.md`. Alle
übrigen Fundstellen — `02b-abnahme.md`, `02b-golden-anchors.md`, zwei Testmodule — nennen die
spaltenstochastische Fassung korrekt als die verworfene.

**Konvention:** Hebt ein Registereintrag einen älteren auf, weist der Titel das aus und der Text
nennt **Datei und Abschnitt**, die nachzuziehen sind. Ohne diese Angabe ist die Aufhebung im
Register vollständig und in der Spec unsichtbar — der Zustand, der hier zwei Jahre gehalten hat.

### D141 — Der Distanzkauf entfernt eine Decke, er trägt keinen Fluss (korrigiert D139)

Nachzuziehen war `02-trust-flow.md §4`, Warnblock „Distanz ist kaufbar". Der Befund von D139
bleibt vollständig bestehen; falsch war die Rechnung darin.

**Der Fehler.** D139 schrieb, die Grenzsumme steige von `0` auf `32`, und nannte das den
„Ertrag `C(p) · ⌊γ · C(p)⌋`, quadratisch in `C(p)`". `Σ_{h ∈ Grenze} C(h)` ist aber eine
**obere Schranke**, kein erzielter Fluss. Die dort beschriebene Konstruktion — acht vorher
unerreichbare Knoten mit `C = 0`, neu angehängt an `p` — trägt sogar **gar keinen** zusätzlichen
Fluss: aller Fluss zu diesen Knoten müsste durch `p` laufen, und `p` deckelt bei `C(p)`. Der
Angriff, wie ich ihn aufgeschrieben hatte, ist wertlos. Die Verwechslung von Schranke und Ertrag
ist genau die Sorte Fehler, die Prüfregel 20 im Nachbarsatz gefunden hat und im eigenen Satz
nicht.

**Aufgefallen beim Versuch, den Testgraphen zu bauen.** Die Behauptung war zwei Tage alt und
hatte einen Registereintrag, einen Warnblock in der Layer-Datei und eine Runde Prosa überstanden.
Sie fiel in dem Moment, in dem sie für eine Maschine präzise genug formuliert werden musste —
das D118-Muster, inzwischen zum wiederholten Mal.

**Gemessen** (`γ = ½`, `C₀ = 16`, `D = 16`, Messlauf gegen `trust()` und `derive()`):

| | ohne Angriff | mit Angriff |
|---|---|---|
| `d(h)` | 4 | 2 |
| `C(h)` | 1 | 4 |
| Zufluss zu `h` | 8 | 9, davon 1 von `p` |
| `Σ C(h)` über der Grenze | 1 | 4 |
| `maxflow(A → S)` | **1** | **4** |
| `disjoint_paths` | 1 | 1 |

Die Topologie: ein Anker `A`, vier Ketten `A → a_i → b_i → x_i → h` der Länge 4, dann `h → S`.
`h` hat damit `8` Zufluss und sitzt bei `d = 4` mit `C(h) = 1` — die Knotendecke schneidet sieben
Achtel des vorhandenen ehrlichen Zuflusses ab. Der Angreifer verwirrt `p` bei `d = 1` und lässt
`p` mit `n = 2` von Budget `16` für `h` bürgen. Die Kante trägt `cap = ⌊2 · 8 / 16⌋ = 1`, genügt
aber, um in `E⁺` zu liegen; `bfs_capacities` setzt `distance` beim **ersten** Sehen und
schichtweise, also rutscht `h` auf `d = 2` und `C(h)` auf `4`.

**Die korrigierte Aussage.** Gekauft wird nicht Fluss, sondern das **Entfernen einer Decke**. `p`
steuert genau eine Kapazitätseinheit bei; drei der vier Einheiten sind ehrlicher Fluss, der
vorher an `C(h) = 1` abgeschnitten wurde. Daraus folgt, welcher Grenzknoten für einen Angreifer
lohnt: nicht der unerreichbare — der trägt nichts —, sondern der **gut verbundene, aber
seed-ferne**. Peripherie mit Substanz. Wer lange dabei und weit vom Seed ist, ist das lohnendste
Ziel, und das ist eine unangenehmere Aussage als die ursprüngliche.

`disjoint_paths` bleibt bei `1` und ist damit die Größe, die der Angriff **nicht** bewegt. Ob das
trägt oder ein Artefakt dieser Topologie ist, ist nicht gemessen und wird hier nicht behauptet.

**Was unverändert bleibt.** Der Min-Cut-Satz stimmt, die Schranke steigt mit (`1 → 4`) und bleibt
wahr — sie ist eine Aussage über den Graphen nach dem Angriff. Was fällt, bleibt der gestrichene
Satz vom doppelten Schutz aus D139. Die Immunität der Relaxation aus D140 ist von dieser
Korrektur nicht berührt: dort ging es um Masse, nicht um Decken.

**Offen und ausdrücklich nicht entschieden.** Wie der Effekt mit `p`s Budget skaliert — `p` kann
`⌊D / (D/C(p))⌋ = C(p)` solcher Kanten legen, ohne dass der eigene Durchsatz von `C(p)` je
gebraucht wird — ist gerechnet plausibel und **nicht gemessen**. Es steht deshalb in keiner
Spec-Datei. Ebenso offen bleibt der Fork aus D140: gibt es eine harte Knotendecke, die nicht über
den Graphen gekauft werden kann?

**Nächster Schritt.** Der Messlauf wird zu einem Charakterisierungstest unter `tests/trust/`. Er
repariert nichts; er nagelt fest, dass die Zahl `4` ist und nicht `1` oder `8`. Entsteht je ein
Mechanismus gegen den Distanzkauf, wird genau dieser Test rot — das ist die Rücknahmeprobe im
Voraus.

### D142 — Die Decke wandert genau dann, wenn `d` sich bewegt (ergänzt D141)

**Die Frage.** D141 hält fest, dass `Σ_{h ∈ Grenze} C(h)` beim Distanzkauf von `1` auf `4`
steigt und der Min-Cut-Satz davon unberührt bleibt. Ungemessen war, **unter welcher Bedingung**
die Schranke mitwandert — und ob es Züge gibt, bei denen sie stillsteht. Der Satz „bleibt
unberührt" ist wahr und liest sich wie eine Beruhigung; ohne die Bedingung ist er keine.

**Gemessen** (`γ = ½`, `C₀ = 16`, `D = 16`, `tests/trust/test_deckenelastizitaet.py`). Der
Beitrag von `p` ist der **zugeführte Fluss** `min(cap(A → p), Σ cap(p → h))`, nicht die
Ausgangskapazität. Der Term `C(p)` ist nach `02 §3`, Nachtrag seit D1, redundant und darum nicht
Teil der Definition.

| Fall | Zug | `Σ C(h)` ohne → mit | `maxflow` ohne → mit | Beitrag `p` | Hebel |
|---|---|---|---|---|---|
| A | Distanzkauf, `p → h` mit `n = 2` | 1 → 4 | 1 → 4 | 1 | **3** |
| B | Spende, `d(h)` bleibt `1`, ungesättigt | 8 → 8 | 1 → 5 | 4 | **1** |
| B2 | Spende, `d(h)` bleibt `1`, gesättigt | 8 → 8 | 1 → 8 | 8 | **7/8** |
| C, `k = 1` | `1` gekaufte Kante | 1 → 4 | 1 → 4 | 1 | 3 |
| C, `k = 2` | `2` gekaufte Kanten | 2 → 8 | 2 → 8 | 2 | 3 |
| C, `k = 3` | `3` gekaufte Kanten | 3 → 12 | 3 → 12 | 3 | 3 |

**Erstens: die Elastizität hat eine Bedingung.** In A und C bewegt der Zug `d(h)`, und `Σ C(h)`
wandert exakt mit dem Fluss. In B und B2 bewegt er `d(h)` nicht, und `Σ C(h)` steht still,
während der Fluss steigt. Die Schranke ist nicht generisch angreiferabhängig — sie ist es genau
dann, wenn der Zug eine **Distanz** verschiebt. Alles andere lässt sie unberührt.

**Zweitens: nur der Distanzkauf hat Hebel.** Ein Zug, der keine Distanz ändert, ändert keine
Kapazität und kann folglich höchstens den Fluss addieren, den er selbst trägt — Hebel `≤ 1`.
B zeigt den Gleichstand (`4` zugeführt, `4` Zuwachs), B2 den Verfall an der Decke (`8` zugeführt,
`7` Zuwachs). Der Distanzkauf zahlt `1` und bekommt `3`. Das ist der ganze Unterschied zwischen
den beiden Angriffsformen, und er sitzt nicht in der Größe des Einsatzes.

**Drittens: die Schranke ist schlaff, wo die Decke nicht bindet.** In B steht `maxflow = 5`
gegen `Σ C(h) = 8`. `Σ C(h)` ist dort keine Näherung des Flusses, sondern überzeichnet ihn um
`60 %`. In A, B2 und C ist sie scharf. Wer `Σ C(h)` als Kennzahl liest statt als Schranke, liest
je nach Graphlage etwas anderes.

**Skalierung — das offene Stück aus D141 ist geschlossen.** Der Hebel ist über `k = 1, 2, 3`
konstant `3`; `Σ C(h)` und `maxflow` wachsen beide linear. D141 vermutete, `p` könne `C(p)`
solcher Kanten legen. Gemessen bindet in dieser Topologie **das Budget des Ankers zuerst**:
`A` liegt bei `k = 3` mit `4 + 4k = 16` genau auf `D`, während `p` bei `2k = 6` noch weit unter
`D` sitzt. Die ehrliche Substanz, die der Kauf freilegt, musste selbst durch das Ankerbudget.
Das ist ein Befund über diese Topologie, keine allgemeine Aussage — behauptet wird nur, dass
`p`s Budget **nicht** notwendig die bindende Größe ist.

**Literaturprüfung (PR-15).** Cheng/Friedman (P2PECON 2005) zeigen, dass keine symmetrische,
nichttriviale Reputationsfunktion sybilproof sein kann, und geben für **flussbasierte,
quellrelative** Funktionen Bedingungen an, unter denen sie es sind. `02 §4` liegt damit in der
erreichbaren Klasse; verwundbar ist nicht der Fluss, sondern die darübergelegte
Kapazitätszuweisung, deren Eingang `d(s,h)` ein Kürzeste-Pfad-Maß ist — und ein kürzester Pfad
ist genau das, was eine einzelne Kante verkürzt. SumUp (Tran et al., NSDI 2009) benutzt dieselbe
Konstruktion (mit der Distanz fallende Kantenkapazität, approximierter Max-Flow zu einem
vertrauten Sammler) und hat **keine** unkaufbare Knotendecke: die Garantie sitzt dort an der
Zahl der Angriffskanten, nicht am Knoten. Die SybilLimit-Linie scheitert an MaRs Constraints vor
der Arithmetik: sie braucht `r = Θ(√m)` und eine Schätzung der Mixing-Zeit, also lokale
Schätzungen **globaler** Größen.

**Was daraus folgt.** Eine harte Knotendecke, die nicht über den Graphen kaufbar ist, existiert
in dieser Familie nicht, und die reifsten Systeme haben die Garantie stattdessen auf den Schnitt
verlegt. `02 §4` tut das bereits. Der Distanzkauf ist der Preis der harten Schranke, nicht ein
Fehler in der Wahl der Sicht.

**Methodik.** Der Lauf brauchte vier Anläufe, und alle vier Defekte lagen im Prompt, nicht in der
Arbeit des Werkzeugs. Zweimal derselbe Fehlertyp: eine **Kapazität als Ertrag** geführt — erst
`cap(p → h) = 8` als Beitrag, obwohl `p` über `A → p` nur `4` empfängt, dann `C(p)` als Term
einer Minimumsbildung, obwohl `02 §3` ihn als nie allein bindend beweist. Beide Male fiel die
Behauptung erst, als sie an einer konkreten Topologie präzise werden musste. Daraus **Prüfregel
21: eine Kapazität ist eine Schranke, kein Ertrag** — wer eine Kapazität in eine Bilanz
einsetzt, muss den Weg rechnen, den der Fluss zu ihr nimmt. Und als Zusatz: ein Term, den die
Spec als redundant beweist, kann von keiner Rücknahmeprobe rot gefärbt werden; eine Probe, die
ihn treffen soll, ist falsch gebaut.

**Was unverändert bleibt.** Der Min-Cut-Satz, die `|S|`-Unabhängigkeit, VR-02.1, die Immunität
der Relaxation aus D140. D141 ist in keinem Punkt korrigiert, nur ergänzt.

**Offen und ausdrücklich nicht entschieden.** Ob `02 §4` einen normativen Satz erhält, der
`Σ C(h)` für Gates ausschließt — die Größe ist schlaff, wo die Decke nicht bindet, und sie
wandert mit dem Angreifer, wo sie es tut. Ebenso offen bleibt der Fork selbst: ob ein Mechanismus
gegen den Distanzkauf gebaut wird. Beides sind Entscheidungen des Operators.

### D143 — Kein Mechanismus gegen den Distanzkauf (schließt den Fork aus D140/D141)

**Entschieden.** Es wird kein Mechanismus gebaut, der den Distanzkauf verhindert, erkennt oder
abmildert. `C(x) = ⌊C₀ · γ^{d(s,x)}⌋` bleibt wie in `02 §3`. Die Kaufbarkeit von `d` bleibt eine
benannte, gemessene und getestete Eigenschaft der Schicht.

**Erstens — das Aufnahmekriterium schließt es aus.** `08 §3` fragt: senkt der Mechanismus die
Kosten dafür, festzustellen, wer was gesagt hat, oder verteilt er Macht? Eine Positionsgröße
gegen Bürgschaften zu stabilisieren, senkt keine Feststellungskosten. Es legt fest, wessen
Position beweglich ist und wessen nicht — das ist Machtverteilung, also Policy, nicht Protokoll.

**Zweitens — und das trägt die Entscheidung: der Schaden ist zu einem großen Teil gar keiner.**
D141 hat gemessen, dass `p` eine Kapazitätseinheit beisteuert und der Fluss um drei steigt. Die
drei Einheiten sind **ehrlicher Fluss, den die Decke vorher abgeschnitten hat**: `h` hatte einen
Zufluss von `8` und durfte `1` weiterreichen. Der Kauf hebt eine Unterschätzung auf, die die
Schicht selbst erzeugt hat. Ein Mechanismus, der den Kauf verhindert, hält genau diesen ehrlichen
Fluss weiter draußen — er macht das Protokoll über einen gut verbundenen, seed-fernen ehrlichen
Knoten dauerhafter falsch, um einem Angreifer einen Hebel zu nehmen, den dieser mit dem Budget
eines verwirrten Menschen bezahlen muss. Der Tausch lohnt nicht.

**Drittens — die Literatur kennt die gesuchte Größe nicht.** Nach D142: eine harte Knotendecke,
die nicht über den Graphen kaufbar ist, existiert in der Familie sozialgraph-basierter Abwehren
nicht; die reifsten Systeme (SumUp) haben die Garantie stattdessen an die Zahl der Angriffskanten
gehängt. `02 §4` tut das bereits. Die Alternative mit der stärksten Schranke (SybilLimit) setzt
Schätzungen globaler Größen voraus und ist mit „alles lokal, nichts global" unvereinbar.

**Was damit als Preis angenommen ist.** Ein Angreifer, der einen seed-nahen ehrlichen Menschen
verwirrt, kann seed-ferne ehrliche Knoten näher an den Anker ziehen und deren Decke heben — mit
Hebel `3` bei Kosten von einer Kapazitätseinheit, linear in der Zahl der so behandelten
Grenzknoten, gedeckelt in der gemessenen Topologie durch das Budget des Ankers. Das ist der Preis
der harten Schranke aus `02 §4` und keine Schwäche in der Wahl der Sicht: die Schranke braucht
eine Obergrenze pro Knoten, die Obergrenze braucht eine Positionsgröße, und jede Positionsgröße
über dem Vouch-Graphen wird mit Vouches gestaltet. `02 §5` ist davon frei, weil es nichts
verspricht — keine harte Schranke, für Gates verboten.

**Rücknahmeprobe im Voraus.** Entsteht je ein Mechanismus gegen den Distanzkauf, werden
`tests/trust/test_distanzkauf.py` und `tests/trust/test_deckenelastizitaet.py` rot. Diese
Entscheidung ist damit nicht still zurücknehmbar: wer sie aufhebt, muss zwei Testdateien
anfassen und diesen Eintrag überschreiben.

**Nicht entschieden.** Ob `02 §4` einen normativen Satz über die Verwendung von
`Σ_{h ∈ Grenze} C(h)` erhält (D142, letzter Absatz). Der Fork ist geschlossen, diese Frage nicht.

### D144 — Die Prüfregeln bekommen eine Datei; sechs abgelöste Sitzungsstarts fallen

**Der Befund.** `sitzungsstart-decke.md` schrieb „die neunzehn aus den Vorsitzungen gelten
unverändert" und führte nur Regel 20 aus. Der Volltext der Regeln 1–19 stand **verteilt über
fünf abgelöste Sitzungsstart-Dateien**: sieben in `05`, drei in `anwendung`, drei in
`einlesepfad`, drei in `buchfuehrung`, eine in `kollision`. Das Register nennt sie nur als
Verweise. Der meistbenutzte methodische Bestand des Projekts hatte damit keinen Ort — er lag in
Dateien, deren einziger Zweck es ist, abgelöst zu werden.

Das ist kein Aufräumproblem. Ein Aufräumen ohne diesen Befund hätte die Regeln gelöscht, und
zwar in einem Commit, dessen Nachricht „abgelöste Sitzungsstarts entfernt" gelautet hätte.

**Entschieden.** Neue Datei `pruefregeln.md` mit den Regeln 1–21 im Volltext, thematisch
gruppiert nach dem Zeitpunkt, an dem sie greifen, mit der Nummer als stabilem Bezeichner. Sie ist
der einzige Ort ihres Volltextes. Ein `sitzungsstart-*.md` **verweist** künftig darauf und
wiederholt ihn nicht; neue Regeln entstehen weiter aus Befunden und wandern von dort in diese
Datei.

**Nummern 8 und 9 vergeben.** Parallelenprüfung und Begründungsprüfung liefen seit
`sitzungsstart-05.md` unnummeriert als „die beiden älteren" mit. Ohne Nummer waren sie in
Prompts nicht zitierbar, und beide sind laufend im Gebrauch. 8 ist die Parallelenprüfung, 9 die
Begründungsprüfung.

**Regel 21 ist neu** und stammt aus D142: eine Kapazität ist eine Schranke, kein Ertrag.

**Löschung geprüft, nicht angenommen.** Nach Prüfregel 17 ist eine Datei normativer Text, solange
Code oder Spec auf sie zeigt. Gegrept über alle `*.py` und `*.md` außerhalb der
`sitzungsstart-*`-Familie und außerhalb von `.venv`: **keine einzige Fundstelle**. Damit fallen
`sitzungsstart-03.md`, `-05.md`, `-anwendung.md`, `-buchfuehrung.md`, `-einlesepfad.md` und
`-kollision.md`. `sitzungsstart-decke.md` fällt mit dem Schreiben seines Nachfolgers.

**Was mit den Dateien verlorengeht — benannt, nicht behauptet.** Die Abschnitte „Was die letzte
Sitzung gelehrt hat" sind Erzählung, nicht Regel; was daran trug, ist entweder in eine Regel
geworden oder steht in einem Registereintrag. Was in keinem von beidem steht, war nicht wichtig
genug, es dorthin zu schaffen — das ist die Aussage dieses Eintrags und nicht ihr Nebeneffekt.
Wer sie doch braucht, findet sie in der Historie.

### D145 — Das Genesis wird in `04` geglaubt, nicht nachgerechnet

**Die Lage.** `decide()` liest `genesis_obj[5]` (Schwellenklasse) und `genesis_obj[6]`
(Gewichtungsmodus) und rechnet nie nach, dass
`SHA-256(DOM_NUC_GEN ‖ cbor(genesis_obj)) == epoch.scope`. `resolve_policy` rechnet genau das
nach, mit ausformulierter Begründung in `03 §1.2`: der Resolver rechnet nach statt zu glauben,
sonst wäre die Content-Adressierung eine Behauptung.

**Die Fehlerform — Prüfregel 18, mit dem Beweis im selben Abschnitt.** `04 §3` schreibt den
allgemeinen Satz selbst: „Dann die Objektidentitäten, vor jedem Zugriff auf ihren Inhalt." Die
darunterstehende Tabelle führt zwei Objekte, beide Verfassungen. Das Genesis fehlt in der
Aufzählung, obwohl der Satz es erfasst — und der Code ist der Aufzählung gefolgt, nicht dem
Satz. Zugleich Prüfregel 9: die Begründung aus `03 §1.2` ist an keine Eigenschaft von `03`
gebunden, sie gilt für jeden Leser eines Genesis. Sie ist beim Übergang nach `04` nicht
mitgereist.

**Die Wirkung liegt beim Konsumenten, nicht am Ort des Defekts** (Prüfregel 16). `genesis[5]`
wählt die Schwellenklasse. Ein nicht gebundenes Genesis mit `[5] = 0` lässt eine
Verfassungsänderung mit der `ordinary`-Schwelle ratifizieren — genau der Routine-Capture, gegen
den `00 §6.2` die `amendment`-Schwelle setzt. `[6] = 0` erlaubt Kopfzahl-Auszählung in einem
Nukleus, der gewichtet abstimmt. Beide Wege enden in `RATIFIED`, wohlgeformt und ohne Vermerk.
Das ist die stille Variante: nicht ein Fehler, der auffällt, sondern eine Entscheidung, die
falsch fällt und richtig aussieht.

**Beschluss: `ValueError`, unmittelbar nach der Scope-Prüfung.** Kein Vermerk, kein zwölfter
Code. Die Begründung ist die Asymmetrie aus `03 §1.2`: ein falsches Genesis ist eine falsche
Zuordnung — der Zustand ist nicht unvollständig, sondern falsch, und dafür gibt es keine sichere
Voreinstellung. Eine fehlende Verfassung ist Teilwissen und behält ihren Vermerk. `decide` wirft
bereits an dieser Stelle für `proposal.scope != epoch.scope`; die neue Prüfung ist derselbe Typ
und steht daneben.

**Verworfen — ein Vermerk `GENESIS_MISMATCH`.** Er behauptete, der Zustand sei auswertbar und
nur unvollständig. Er ist nicht unvollständig. Ein Vermerk gäbe `decide` außerdem einen
Rückgabewert für eine Lage, in der keine der gelesenen Zahlen einem Nukleus zurechenbar ist —
eine Auszählung ohne Nukleus.

**Zwei Golden-Anchor-Vektoren konstruieren eine unmögliche Lage.** `GV-24` und `GV-29` mutieren
`GENESIS_D` und übergeben das Ergebnis an eine Epoche mit `N_D`; das mutierte Genesis hat einen
anderen Hash. Nach dieser Entscheidung ist das kein zulässiger Zustand mehr. **Die
Erwartungswerte bleiben unverändert** — beide Befunde sind weiterhin erreichbar, über ein eigenes
Genesis mit eigenem Scope und eine Epoche darauf; `STOCK_GENESIS` mit `[6] = 1` und `STOCK_N` ist
genau diese Bauform und liegt bereits im Fixture. Geändert wird die Konstruktion, nicht die
Erwartung. Wäre eine Erwartung zu ändern, wäre das der Abbruchgrund und nicht der nächste
Schritt.

**Nicht repariert: `threshold_class`.** Sie ist exportiert, liest `genesis_obj[5]` ungeschützt
und wird in `tools/example_nucleus.py` direkt aufgerufen, wo `decide`s Indexprüfung nicht greift.
Eine eigene Prüfung dort brächte die zweite Implementierung derselben Regel zurück, die D111
gerade beseitigt hat. Die Vorbedingung gehört in den Docstring, nicht in den Code.

**Offen, eigener Fork: `trust_params`.** `trust/params.py` trägt `TrustParams` eigenständig,
`00 §4` Key 9 deklariert dieselben Zahlen unveränderlich im Genesis, und nichts gleicht sie ab.
D35 verlangt Unveränderlichkeit von `D`, weil `n/D` in jeder Vouch-Signatur steckt. Dieselbe
Klasse wie dieser Eintrag, anderer Layer — nicht in diesem Lauf.

### D146 — Regel 14 zum dritten Mal, und eine neue Regel 22

**Zwei Prompt-Defekte im Lauf zu D145.** Der Prompt nannte `passed()`, die Funktion heißt
`reached()`. Und er behauptete, `_tally` habe einen Importeur außerhalb seiner Datei; es waren
zwei, und `test_invariants.py` wäre ohne die Meldung des Werkzeugs rot geworden.

**Der zweite ist kein neuer Befund.** Regel 14 sagt bereits, dass eine Aufzählung von Fundstellen
gegrept und nicht gelesen wird, und führt zwei Präzedenzen: D119 nannte einen Erzeuger, es waren
drei; D127 nannte vier Kettenfortführungen, es waren fünf. „Ein Importeur, es waren zwei" ist der
dritte Fall derselben Regel. Ihn zum Anlass einer neuen Regel zu nehmen, hätte die bestehende
verwässert und den eigentlichen Punkt verdeckt: die Regel stand, sie wurde nicht angewandt.

**Ein Zusatz zu 14 trägt trotzdem.** Die Behauptung stammte aus einem `head -20`, das genau
zwanzig Zeilen zurückgab. Eine Ausgabe an der Grenze ihres Limits sieht aus wie eine
vollständige, und darin unterscheidet sie sich von einem leeren Ergebnis, das sich selbst
anzeigt. Deshalb: ein Limit, das exakt erreicht wird, ist ein Nulltreffer.

**Der erste Defekt ist neu.** Ein Bezeichner ist keine Aufzählung. `passed()` entstand daraus,
dass der Rumpf der Funktion gelesen und die `def`-Zeile ergänzt wurde — und ein Funktionsrumpf
ohne seine Signatur sieht nicht abgeschnitten aus. Dagegen hilft keine Zählregel, sondern nur die
Herkunft: **Regel 22**, Namen und Signaturen im Prompt werden übernommen, nicht rekonstruiert.

**Auch nicht „Modulcode vor Prompt".** Der Modulcode war gelesen. Gelesen und vollständig gelesen
sind zwei Zustände, und die Differenz war beide Male unsichtbar.

**Zur Fehlerform.** Der Supervisor war in dieser Sitzung wie in der vorigen die Fehlerquelle, und
beide Male hat das Werkzeug gemeldet statt still anzupassen. Das ist die Bedingung, unter der ein
falscher Prompt billig bleibt — keine Erlaubnis, ihn falsch zu schreiben, aber die Erklärung
dafür, warum der Schaden ein Nachlauf war und kein Defekt in `main`.

**Offen, aus D145 mitgenommen: die Genesis-Felder haben keinen gemeinsamen Durchgang.**
`[5]`/`[6]` waren ungebunden und sind es nicht mehr. `[4]` ist an die Epochenkette nicht gebunden
— `GV-24` führt ein Genesis, dessen deklarierte Verfassung in der Auszählung nirgends vorkommt.
`[9]` hat mit `trust/params.py` eine zweite Quelle ohne Abgleich, obwohl D35 Unveränderlichkeit
von `D` verlangt, weil `n/D` in jeder Vouch-Signatur steckt. `[1]`, `[2]`, `[3]` und `[7]` haben
gar keinen Träger. Das ist einmal zu beantworten und nicht viermal: welches Feld hat einen
Träger, und woran ist er gebunden. Der Durchgang steht vor `00a`, weil `root_keys` eines der
trägerlosen Felder ist.

### D147 — Die Kalibrierung bekommt einen Herleitungsort, die Rechnung bleibt parametrisiert

**Die Lage.** `TrustParams` trägt `C0`, `gamma_num`, `gamma_den`, `D` — feldgleich mit
`genesis[9]` nach `00 §4`. Nichts gleicht beide ab. `derive`, `trust` und `rank` nehmen die
Parameter vom Aufrufer entgegen; `tools/sim/szenario.py` und `tools/example_nucleus.py` tippen
sie als Literale. D35 verlangt Unveränderlichkeit von `D` über die Lebensdauer eines Scopes,
weil `n/D` in jeder signierten Vouch steckt. Ein Leser kann heute mit einem anderen `D` rechnen
als der Scope deklariert, und nichts zeigt es an.

**Zweitens, kleiner:** `TrustParams.__post_init__` prüft dieselben Wohlgeformtheitsbedingungen
wie `00 §4.0`, in eigener Formulierung. Sie stimmen heute überein — `C0 > 0` und `C₀ >= 1` sind
über `int` dasselbe, ebenso `0 < γ_num < γ_den` und `1 <= γ_num < γ_den`. Zwei Orte, eine Regel:
notiert, nicht zusammengelegt, weil eine Zusammenlegung `params.py` an die Spec-Prosa binden
würde statt an ein Objekt.

**Die Literaturprüfung hat den Fork aufgelöst, statt ihn zu entscheiden** (Prüfregel 15). Die
Frage war, was ein Verifizierer ohne Genesis tun soll. Zwei Familien antworten:

| System | Bauform | Antwort bei fehlender oder abweichender Quelle |
|---|---|---|
| TUF | Trust Anchor out-of-band, alles Weitere aus signierten Metadaten | Schwellen nie aus Client-Konfiguration; abgelaufenen Metadaten wird nicht vertraut |
| go-ethereum | Genesis trägt nur einen Teil der Chain-Spec, der Rest liegt im Client | `CheckCompatible` meldet `ConfigCompatError` mit Rückspulpunkt, kein Vermerk |
| Web-PKI (OCSP) | Widerrufsstatus wird online geholt | Soft-Fail — und er ist wirkungslos, weil der Angreifer den Kanal hält |

**Ethereum ist derselbe Fall, nicht nur ein ähnlicher:** dass die Parameter teils im
content-adressierten Anker und teils in der Implementierung stehen, ist dort die benannte Ursache
dafür, dass zwei Clients dasselbe Netz verschieden sehen. Genau diese Lücke hatte MaR.

**Die Web-PKI liefert die Begründung dafür, warum ihre eigene Antwort hier nicht gilt.** Der
Soft-Fail existiert, weil ein Responder ausfallen kann und ein Hard-Fail dann funktionierende
Verbindungen bricht. Ein Genesis ist kein Responder: unveränderlich, klein, content-adressiert,
und über `N` in jedem Claim referenziert. Die Antwort der Praxis auf den Soft-Fail war Stapling
und Mitliefern — die Information reist mit, statt nachgeschlagen zu werden. In MaR ist das der
Normalfall und nicht die Verschärfung; D121s Bündel trägt die Objektmap bereits.

**Beschluss: `resolve_trust_params` in `mensch_als_republik/trust/params.py`.** Signatur und
fünf Lagen stehen in `02 §8.1`. Die Bindungsprüfung ist die aus D145, mit derselben Begründung
aus `03 §1.2`: ein falsches Genesis ist eine falsche Zuordnung, kein Teilwissen.

**Der eigentliche Defektfall ist die dritte Lage** — Schlüssel 9 vorhanden **und** abweichende
Parameter übergeben. Nur dort behauptet jemand zwei verschiedene Kalibrierungen für denselben
Scope, und nur dort kann eine Vouch still umbewertet werden. Die anderen vier Lagen sind
Nebenwirkungen einer sauberen Signatur.

**Verworfen — `derive` bindet das Genesis selbst.** Das zöge ein Objekt in Layer 02, das Layer 02
nie brauchte, und machte den Trust-Graphen ohne Nukleus unrechenbar. Die Naht aus `03 §1.2` ist
billiger und bereits erprobt.

**Verworfen — Rückgabe eines Vermerks statt einer Ausnahme.** Ein Trust-Score, der unter
bestrittener Kalibrierung entstanden ist, ist keine schwächere Aussage, sondern eine über einen
anderen Scope. Und `02 §7` verlangt, dass fehlendes Wissen ein Ergebnis nur **senkt**; ein
falsches `C₀` senkt nicht, es verschiebt — dieselbe dritte Richtung, die D120 für den Autor über
seine eigene Kette gefunden hat.

**Nicht entschieden: `anchor_set` (`genesis[3]`).** Nach TUFs Trennung ist es der Trust Anchor
und nicht ein abgeleiteter Parameter; `02 §6.3` führt es ausdrücklich als out-of-band etabliert.
Wer bewusst mit einer Teilmenge der Anker rechnet, tut nichts Falsches. Bleibt ungebunden, als
benannte Grenze und nicht als Versehen.

**Offen: `D >= C₀` ist ein SHOULD in `00 §4.0` und `02 §8` und wird nirgends geprüft.** Kein
Defekt — ein SHOULD erzwingt nichts —, aber ein Kandidat für einen Vermerk, sobald es einen Ort
gibt, der ihn trägt.

### D148 — Prüfregel 23: die Rücknahmeprobe setzt an der ungeschützten Seite an

**Der Vorgang.** Der Nachlauf zu D147 sollte feststellen, dass `genesis_res[9]` und das
`TrustParams`-Literal im Beispielnukleus dieselben vier Zahlen tragen. Die Rücknahmeprobe im
Prompt lautete: eine Zahl in `genesis_res[9]` ändern und bestätigen, dass der Test rot wird. Er
wurde rot — mit der Meldung `N_res: got …, expected …`, also aus dem Bestandsanker in `build()`
und nicht aus dem neuen Test. Eine Änderung an `genesis_res` ändert den Scope, und den prüft der
Beispielnukleus seit Layer 04.

**Die beiden Seiten waren ungleich bewacht.** `genesis_res[9]` hängt am Hash und damit an einem
Golden Anchor. `ExampleNucleus.params` hängt an nichts. Der neue Test existiert für die zweite
Seite, und die Probe hatte die erste angefasst.

**Die Wiederholung an der richtigen Seite hat gegriffen:** `D=100` auf `D=99` im Literal ergibt
`ValueError: out_of_band does not match genesis trust_params`, sechs andere Tests bleiben grün.
Der Test ist damit berechtigt und der Nachlauf gut.

**Beschluss: Prüfregel 23.** Vor jeder Probe die Frage, was außer dem geprüften Test hier noch
rot werden könnte; die Antwort muss „nichts" sein.

**Abgegrenzt gegen Regel 21.** Deren Zusatz aus D142 betrifft die **unmögliche** Probe: ein von
der Spec als redundant bewiesener Term lässt sich nicht rot färben. Hier war die Probe möglich
und hat gefärbt — nur aus fremder Ursache. Unmöglich gegen zweideutig; die zweite Form ist die
gefährlichere, weil sie wie eine Bestätigung aussieht.

**Zur Fehlerform.** Die Meldung nannte `N_res` und einen Ankerwert, also einen Test, den es
vorher schon gab. Die Diagnose war ohne zweiten Lauf möglich; der Supervisor hat das Rot als
Bestätigung durchgewinkt, statt die Meldung zu lesen. Der Bericht des Werkzeugs war korrekt und
vollständig — er hätte die Frage beantwortet, wenn sie gestellt worden wäre. Das ist die
Umkehrung der bekannten Regel: nicht der Bericht ersetzt das Lesen nicht, sondern **das Rot
ersetzt das Lesen nicht**.

**Nachtrag zum eigenen Splice, gleiche Sitzung, gleiche Klasse.** Der erste Anlauf dieses
Eintrags scheiterte am Endanker: der Supervisor hatte den Schlusssatz von D147 aus dem eigenen
Entwurf rekonstruiert statt aus der Datei abgelesen, und der Zeilenumbruch lag anderswo als
erinnert — Prüfregel 22, eine Runde nach ihrer Einführung. Der Trockenlauf verdeckte es, weil die
Schlusszeile für die Simulation von Hand getippt worden war. Daraus die operative Fassung: **eine
selbst getippte Ankerzeile prüft den Anker nicht.** Ein Anhang ans Dateiende braucht überhaupt
keinen Prosa-Anker; die tragende Vorbedingung ist, dass der letzte Registereintrag der erwartete
ist, und die lässt sich ohne Zitat prüfen.

### D149 — Die Schwellenfrage war bereits verortet; `00a` ist kleiner als vermutet

**Der Anlass.** Vor der Design-Runde zu `00a` standen vier vermeintliche Forks: das
Gegenzeichnungsprädikat kodieren, „die längste Kette" bei mehreren `root_keys`, ein uhrfreier
Effektivpunkt der Governance-Rotation, und der Befund, dass `rotate-key@1` mit
`J = [identity, K_n]` nicht ausdrücken kann, was mit den übrigen Schlüsseln geschieht. Drei davon
sind keine.

**`00 §7` hatte die Frage gestellt und beantwortet.** Wörtlich: `∈` ist Mengenzugehörigkeit und
für jede Mächtigkeit definiert; bei mehreren autorisierten Schlüsseln genügt einer; und ob ein
Nukleus stattdessen eine Schwelle verlangen können soll, ist **nicht entschieden und wäre ein
Verfassungsknopf nach §4, kein Protokolldefault**. Der Supervisor hat diese Verortung über eine
`08 §3`-Prüfung und drei Literaturrecherchen neu hergeleitet, statt den Absatz zu lesen — obwohl
`§6` und `§7` als gelesen geführt wurden. Prüfregel 22 in ihrer teuersten Form: nicht ein
falscher Bezeichner, sondern ein übersprungener Absatz, und die Kosten waren eine ganze
Sitzungshälfte.

**Die `08 §3`-Prüfung bestätigt die Verortung** und braucht keine Auslegung: die Bestandstabelle
führt „Schwellenwerte, Arbitratorenlisten, Ressourcengrenzen" bereits unter Policy. Die Spec ist
darin konsistent — `genesis[5]` ist ein **Index auf eine Klasse**, die Ratios selbst stehen in der
Verfassung. Dieselbe Trennung, die für die Autorität gesucht wurde, ist eine Ebene tiefer schon
gebaut. Damit entfällt auch die Spannung, an der die Runde hing: eine Schwelle im unveränderlichen
Genesis wäre für immer festgeschrieben, in der Verfassung ist sie per `amendment` änderbar.

**Was für `00a` folgt.** `resolve_current_key` liefert eine **Menge**; `|root_keys| = 2` bedeutet
zwei parallele Ketten, deren Köpfe beide darin landen. Es gibt keine Auswahl zwischen
konkurrierenden Ketten zu treffen, weil jede Rotation den Schlüssel **ihres eigenen Autors**
ersetzt — Konkurrenz entsteht nur innerhalb einer Wurzel, und das ist Equivocation, die Layer 01
seit jeher führt. `J = [identity, K_n]` ist damit korrekt und nicht defekt, und die
Gegenzeichnung bleibt ein einzelner Claim. Offen bleibt allein das Gegenzeichnungsprädikat
(D125, Belegung) und der uhrfreie Effektivpunkt der Governance-Rotation.

**Die Literatur, damit sie nicht ein zweites Mal gesucht wird** (Prüfregel 15):

| Quelle | Befund | Trägt für MaR |
|---|---|---|
| TUF-Spec, Root-Rolle | mehrere Schlüssel **plus** Schwelle; ein Angreifer unterhalb der Schwelle kompromittiert nichts; jeder Schlüssel zählt einmal | ja — die Kette ab einem out-of-band-Anker ist normativ, kein Vorschlag |
| TUF TAP 8 | Rotate trägt Menge **und** Schwelle, dazu Zyklusprüfung und Selbstwiderruf per Selbstschleife | **nein** — seit 2017 nicht angenommen, TAP 20 legt einen Teil neu auf, und TAP 8 erklärt ausdrücklich, den Root-Fall nicht anzufassen |
| did:plc | `rotationKeys` nach Autorität geordnet; ein höherrangiger Schlüssel überschreibt Historie **innerhalb von 72 Stunden** | nein — die Rangordnung ist uhrfrei, das Fenster nicht, und ohne Fenster bleibt ein Altschlüssel dauerhaft mächtig (D125 hat das verworfen) |
| Web-PKI, Soft-Fail vs. Hard-Fail | Soft-Fail ist wirkungslos, wo der Angreifer den Kanal hält; die Antwort der Praxis war Mitliefern statt Nachschlagen | ja, als Begründung in D147 |
| go-ethereum | Parameter teils im content-adressierten Anker, teils im Client — die benannte Ursache dafür, dass zwei Clients dasselbe Netz verschieden sehen | ja, als Begründung in D147 |

**Ein Verweisdefekt, mitkorrigiert.** `00 §7` schrieb dem Beispiel-Nukleus in `§3.1` zwei
Wurzelschlüssel zu. `§3.1` und `04-golden-anchors.md` führen `[ALICE]`, also einen;
`example-nucleus.md` führt an zwei Stellen `[BRUNO, ANNA]`. Die Zahl stimmte, die Fundstelle
nicht. Nach Prüfregel 17 ist das schlechter als ein fehlender Verweis, weil er auf eine Stelle
zeigt, die das Gegenteil belegt. Der Verweis geht auf `example-nucleus.md`.

**Notiert, nicht entschieden.** `example-nucleus.md` führt damit eine **1-von-2-Autorität**: Bruno
und Anna dürfen jeder allein als der Nukleus handeln. Das ist nach `§7` zulässig und bewusst. Es
ist zugleich der erste Ort, an dem diese Bauform auf echte Menschen träfe, und damit der erste
Kandidat für den Verfassungsknopf, falls er je gebaut wird.

### D150 — Die Governance-Rotation bekommt einen Träger: `nucleus_keys` in der Verfassung

**Der Befund.** `00 §6.2` verlangt „ein `propose@1`/Abstimmung, dessen Payload den neuen
autorisierten Schlüssel deklariert". Diese Payload gibt es nicht. Das Vorschlagsobjekt
(`04 §2.4`) trägt genau drei Felder — `{0: scope, 1: predecessor, 2: constitution_hash}`, fest
kodiert in `governance/objects.py` — und das Verfassungs-Minimal-Schema (`00 §5`) trägt vier,
von denen keines einen Schlüssel aufnimmt. `§6.4` Schritt 3 war damit nicht bloß im
Effektivpunkt unterbestimmt; er verwies auf ein Objekt, das die Aussage nicht ausdrücken kann.

**Die Fehlerform ist die von D145.** Der allgemeine Satz existiert und ist richtig; die
Aufzählung darunter trägt ihn nicht. Gefunden nicht beim Lesen von `00`, sondern beim Lesen
von `objects.py` gegen `00 §6.2` — dieselbe Bewegung wie in D118.

**Beschluss.** Die Verfassung bekommt ein fünftes normatives Feld `nucleus_keys`
(`array[bytes32]`, optional). Fehlt es, gilt `genesis.root_keys`. Ist es gesetzt, **ersetzt** es
den Anker der Key-Chain (`00 §5.4`, `§6.4` Schritt 1).

**Begründung, in dieser Reihenfolge.**

1. Die Bauform steht schon da. `arbitration.arbitrators` ist bereits eine Autoritätsliste im
   Verfassungsobjekt: wer im Scope urteilen darf. `nucleus_keys` ist dieselbe Form für: wer als
   der Nukleus handeln darf. Kein neues Primitiv, und `08 §3` fällt eindeutig aus — die
   Bestandstabelle führt Autoritätslisten unter Policy.
2. Die Schwelle stimmt ohne Zusatzregel. `§6.2` verlangt die `amendment`-Schwelle; eine
   Verfassungsänderung **ist** diese Schwelle (`00 §5.3`, `04 §5`).
3. Der Effektivpunkt löst sich ersatzlos auf. Die Epochenkette ist über `predecessor` total
   geordnet und uhrfrei. Die Verfassung der jüngsten ratifizierten Epoche setzt den Anker neu,
   statt mit einem Kettenende verglichen zu werden. Der verbotene Vergleich zweier Ordnungen aus
   `§6.4` Schritt 3 entsteht nicht mehr — und die Frage, ob ein Rotate-Claim vor oder nach der
   Epoche liegt, entsteht ebenfalls nicht: ein Rotate eines nicht mehr genannten Schlüssels
   verliert seine Wurzel und wirkt nicht, unabhängig davon, wann er signiert wurde.
4. Kein Golden Anchor bricht. `proposal_hash` bleibt unverändert, `04`s Vektoren bleiben gültig.

**Verworfen — ein viertes Feld im Vorschlagsobjekt.** Ändert die CBOR-Kodierung von
`proposal_hash` und damit jeden Anker in `04-golden-anchors.md`. Außerdem trägt heute jeder
Vorschlag einen `constitution_hash`; ein Vorschlag ohne Verfassungsänderung ist nicht vorgesehen,
und eine Rotation ohne Verfassungsänderung wäre genau das.

**Verworfen — ein eigenes Profil `govern-rotate@1`.** Ein neuer Mechanismus für eine Aussage,
die ein bestehendes Objekt tragen kann. `08 §3`: keines von beidem, also nicht ins Protokoll.

**Neu und nicht vorgelegt: die leere Liste.** `nucleus_keys = []` bedeutet **keine** autorisierten
Schlüssel; Nukleus-Akte sind dann nicht autorisiert. Das ist die sichere Richtung, dieselbe wie in
`§6.4` Schritt 3 und `§9` („lieber kein gültiger Akt als ein falsch autorisierter"). Die
Gegenrichtung — leer wie fehlend behandeln, also zurück auf `genesis.root_keys` — lässt eine
Governance, die entmachten will, ins Leere laufen und lässt den alten Schlüssel mächtig. Der
Preis ist, dass eine Verfassung den Nukleus per Amendment handlungsunfähig machen kann. Das ist
ausdrückbar und wird nicht verhindert.

### D151 — `00a` baut die Key-Chain, `00b` den Verfassungsanker

**Beschluss.** Der Lauf `00a-rotate-key` baut `resolve_current_key` mit dem Anker als
**Parameter** und `rotate-key@1`/`rotate-ack@1` als Kettenmechanik. Das Bestimmen des Ankers aus
der jüngsten ratifizierten Epoche (D150) ist ein eigener Lauf `00b`.

**Begründung.** D150 zieht `00a` sonst in Layer 04 hinein — Epochenkette lesen, jüngste
ratifizierte Epoche bestimmen, `policy.py` um ein Verfassungsfeld erweitern — und diese Arbeit
teilt mit der Kettenauflösung nichts außer der Signatur. Die Entscheidung fällt trotzdem jetzt,
damit `00a` keine Signatur baut, die `00b` umbauen muss.

**Die Naht ist die bekannte.** `03 §4` nimmt `authorized_keys` als Parameter (D62),
`resolve_policy` trägt die Bindungsprüfung für die Verfassung (`03 §1.2`),
`resolve_trust_params` die für die Kalibrierung (D147). `resolve_current_key` nimmt den Anker
gleichermaßen als Parameter; das Herleiten des Ankers bekommt in `00b` seinen eigenen Ort.

**Getragene Grenze bis `00b`.** Ein vorgefundenes `nucleus_keys` wird nicht ausgewertet. Das ist
die **unsichere** Richtung — ein Leser vertraut weiter dem alten Schlüssel, obwohl die Mitglieder
ihn abgesetzt haben. Als benannte Grenze tragbar, als Schweigen wäre sie eine Lücke; derselbe
Satz und derselbe Grund wie beim „Zustand vor `00a`" in `§6.4`.

### D152 — Die Gegenzeichnung ist `nuc:N/rotate-ack@1`, ein vierteiliges Strukturprädikat

**Die offene Stelle aus D125.** `00 §6.1` sagt „ein Claim `C` mit `C.I == K_n`, der die
`claim_id` des Rotate nennt" und lässt die Feldbelegung offen.

**Der Satz ist zu weit.** Ein `core/revoke@1` mit `J = [claim-ref, claim_id(R_n)]`, signiert von
`K_n`, erfüllt ihn wörtlich. Eine Rücknahme als Zustimmung zu lesen ist nicht die abwegigste
Belegung, sondern die naheliegendste Fehlbelegung: `claim-ref` ist der Tag, den die
`core`-Prädikate ohnehin führen (`01 §5`).

**Beschluss.** Ein eigenes Prädikat, vierteilig nach dem Muster von D63:

```
ack.p  == nuc:N/rotate-ack@1
ack.J  == [claim-ref, claim_id(R_n)]
ack.I  == R_n.J.value    und   R_n.J.tag == identity
ack.N  == R_n.N
```

**Die vierte Bedingung ist nicht redundant** — dieselbe Begründung wie die dritte in D63.
`01 §2.2` Regel 3 erzwingt nur, dass `N` gesetzt und selbstkonsistent ist, nicht dass zwei Claims
denselben Scope teilen. Ohne sie zeichnet eine Ack aus Nukleus B eine Rotation in Nukleus A gegen.

**Trennende Vektoren für `00a`:** Ack vom Vorgängerschlüssel statt vom Nachfolger; Ack mit
fremdem `N`; Ack als `core/revoke@1` statt `rotate-ack@1`; Rotate, dessen `J.tag` `claim-ref`
statt `identity` ist.

### D153 — `rotate-key@1` und `rotate-ack@1` sind Protokoll-Default irrevocable

**Der Fall.** Wäre `rotate-ack@1` widerrufbar, könnte `K_n` die eigene Zustimmung
zurücknehmen und die Autorität spränge auf `K_{n-1}` zurück. Das ist der Zustand, den D125
unter „Verworfen — letzter gewinnt" ausgeschlossen hat, nur von der anderen Seite erreicht.
Dasselbe gilt für den Rotate selbst.

**Beschluss.** Beide Prädikate gehören in die Protokoll-Default-Menge der irrevocablen
Prädikate, neben `obligation@1` (`00 §5.2`, D70). `irrevocable_predicates` kann die Menge
weiterhin nur erweitern.

**Wirkungsprüfung (Prüfregel 16).** Der Träger ist `PROTOCOL_IRREVOCABLE` in `policy.py`, heute
`frozenset({"obligation@1"})`. Der Konsument ist `is_irrevocable`, aufgerufen aus der
Klassifikation; die Wirkung ist, dass ein `core/revoke@1` auf einen Rotate oder eine Ack ignoriert
und vermerkt wird. Die Erweiterung gehört in den `00a`-Lauf, nicht in diese Spec-Runde — sie ist
ohne Kettenmechanik nicht prüfbar.

**Getragene Grenze.** Ein Vertipper in der Ack ist nicht heilbar, sondern nur über die
Governance-Rotation (`§6.2`). Das ist derselbe Preis, den D125 für den Rotate bereits akzeptiert
hat, und dieselbe Bauform wie beim Schuldenschutz: ein Boden, keine Rückfallebene.

### D154 — Ordnung über die Autorenkette; der Kopf kann unter Wissenszuwachs zurückspringen

**Der Fall.** `K_{n-1}` signiert nacheinander `R_a` und `R_b` auf verschiedene Nachfolger mit
**verschiedener** `h_prev`. Das ist keine Equivocation (`§6.3` verlangt dieselbe `h_prev`), beide
sind nach der Kettenregel gültig, und D125 sagt: der **erste vollständige** bindet. Trifft
zuerst nur die Ack zu `R_b` ein, bindet nach lokalem Wissen `R_b`; trifft später die Ack zu `R_a`
ein, bindet `R_a`, und alle Akte des zwischenzeitlichen Kopfes verlieren rückwirkend ihre
Autorisierung.

**Beschluss.** „Erster" ist die Position in der eigenen Kette von `K_{n-1}` (`h_prev`), nicht die
Empfangsreihenfolge. Der Rücksprung wird **benannt** und getragen.

**Verworfen — erster nach Empfang.** Zwei Leser mit demselben Claim-Bestand kämen zu
verschiedenen Ergebnissen. Das ist schlechter als Nicht-Monotonie: nicht reproduzierbar statt
revidierbar.

**Die Klasse ist bekannt.** Mehr Wissen revidiert einen Zustand — dieselbe Lage wie nachträglich
entdeckte Equivocation, Detect-not-Prevent (`01 §A3`, `02 §7`). Neu ist nur, dass sie hier die
Autorität trifft und damit indirekt jeden Nukleus-Akt.

**Ein defektes Kettenglied blockiert nichts.** Eine ungültige oder unvollständige Rotation ist
schlicht kein Nachfolger; der Kopf bleibt beim letzten vollständigen Glied. Der Betriebsschaden
der TUF-Referenzimplementierung — eine ungültige Version blockierte alle folgenden dauerhaft —
setzt eine lückenlos versionsnummerierte Kette voraus. Die Kette hier ist autorverkettet und hat
diese Voraussetzung nicht. Damit ist der dritte offene Punkt aus dem Sitzungsstart keiner.

**Ebenfalls erledigt: „folge der längsten Kette".** Nach D149 gibt es nichts zu maximieren; der
Wortlaut fällt aus `§6.4` und wird durch „bis zum Schlüssel ohne vollständigen Nachfolger"
ersetzt.

### D155 — Vier Belegungen, ohne die `resolve_current_key` nicht rechenbar ist

Die vier Stellen fielen beim Lesen von `verifier.py` und `index.py` gegen `§6.4` an. Keine
folgt aus D150 bis D154; jede wäre sonst im Implementierer entschieden worden.

**(a) Zwei vollständige Rotationen desselben Autors, die nicht vergleichbar sind.** D154 ordnet
über die eigene Kette: bindend ist die frühere. Rechenbar ist das, indem geprüft wird, ob `R_a`
auf dem `h_prev`-Pfad von `R_b` liegt (`store.get(h_prev)` läuft rückwärts). Fehlt ein Glied
dazwischen im lokalen Bestand, liegt keine auf dem Pfad der anderen und die Ordnung ist
unbestimmt. **Beschluss: dann liefert diese Wurzel keinen Kopf**, wie bei Equivocation. Die
Alternative — irgendeine nehmen — wählt eine Autorität aus Unwissen.

**(b) Welcher Zustand zählt.** **Beschluss: Rotate und Ack müssen `ACTIVE` sein**, wie die vierte
Bedingung in D63 („beide aktiv"). Kein neuer Satz, nur die Übernahme des Präzedenzfalls. Damit
fallen `PENDING` (Vorgänger unbekannt) und `EQUIVOCATION_FLAGGED` von selbst heraus.

**(c) `t_exp` auf Rotate oder Ack.** Heute nicht verboten. Wäre es wirksam, liefe eine Rotation
ab und die Autorität spränge zum Vorgänger zurück — dieselbe Nicht-Monotonie, aus der `01 §5.3`
bereits folgert, dass `core/*` sein `t_exp` ignoriert. **Beschluss: `EXPIRED` zählt bei diesen
beiden Prädikaten wie `ACTIVE`**, geprüft in `keys.py`. Das geht (b) vor.

Verworfen — eine Ignorierregel nach dem Muster von `01 §5.4`: ein Eingriff in eine eingefrorene
Schicht für einen Fall, den `00a` lokal erledigen kann. Die getragene Grenze: ein `t_exp` auf
einer Rotation bleibt sichtbar und wirkt woanders, nur nicht auf die Autoritätsauflösung.

**(d) Zyklen. Neu und nicht vorgelegt.** Rotiert `K_1` auf `K_2` und `K_2` zurück auf `K_1`, läuft
ein naiver Vorwärtslauf endlos. **Beschluss: der Lauf führt die Menge der besuchten Schlüssel;
trifft er einen bereits besuchten, liefert die Wurzel keinen Kopf.** Eine zyklische Kette ist
keine Nachfolge. TAP 8 hat für dieselbe Lage eine Zyklusprüfung vorgesehen (Literaturtabelle in
D149); übernommen wird die Prüfung, nicht der übrige Vorschlag.

**Zur Equivocation, die keine dieser vier ist.** `§6.4` Schritt 3 sagt: ist die Kette an einem
Punkt equivoziert, liefert die Wurzel keinen Kopf. Das gilt **unabhängig von Vollständigkeit** —
ein Equivocation-Paar aus zwei Rotationen ohne Gegenzeichnung blockiert ebenso. Andernfalls bliebe
im Diebstahlfall (`§6.3`) der kompromittierte Schlüssel selbst der Kopf, und die Entscheidung
fiele nicht an die Mitglieder. Das steht bereits in der Spec und wird hier nur ausgeschrieben,
weil der Zustandstest aus (b) allein es nicht leistet.

### D156 — Der Protokoll-Boden gilt auch ohne Policy ⚠️

**Der Befund**, aus der `00a`-Abnahme. `is_irrevocable(predicate, policy)` in `policy.py` gibt
`False` zurück, sobald `policy is None` ist — vor jeder weiteren Prüfung. Der Boden aus
`00 §5.2` und D70 hängt damit an der Anwesenheit einer aufgelösten Policy.

**Das widerspricht normativem Text.** `01 §5.4.1` sagt: fehlt das Verfassungsobjekt lokal
(Partition, noch nicht synchronisiert), gilt der Sicherheits-Default aus `00 §5.2`. Der Anker
`P-D` in `03-golden-anchors.md` schreibt genau das aus: `constitution_obj=None`, Ergebnis
trotzdem der Boden. Es wäre widersinnig, dass „gar keine Policy aufgelöst" weniger Schutz trägt
als „Verfassung fehlt".

**Die Wirkung trifft nicht nur die Rotationen.** Ohne Policy wirkt ein `core/revoke@1` auf eine
`obligation@1` — das Schulden-Lösch-Loch aus D57, das D70 auf der Verfassungsebene geschlossen
hat, eine Ebene höher wieder offen. Gefunden wurde es nur, weil `00a` einen zweiten Nutzer des
Bodens bekam; für `obligation@1` allein war es fünfzig Registereinträge lang unsichtbar.

**Beschluss.** `is_irrevocable` prüft bei `policy is None` gegen `PROTOCOL_IRREVOCABLE` statt
gegen nichts. Die übrigen Bedingungen — `nuc:`-Präfix, Profilname nach dem letzten Schrägstrich
— bleiben unverändert, ebenso D73 (Fehlpaarung bleibt laut) und D91 (scope-lokale Anwendung).

**Verworfen — `keys.py` fingiert sich eine Policy.** Der Lauf `0c3f9ad` hat
`NucleusPolicy(scope=scope)` konstruiert, um an der Stelle vorbeizukommen. Das Ergebnis war
richtig, die Bauform nicht: eine Funktion, die keine Verfassung kennt, erfindet eine, und der
Aufrufer kann die echte nicht mehr einspeisen. `resolve_current_key` bekommt stattdessen
`policy` als durchgereichten Parameter, dieselbe Naht wie `membership` in `03 §4`.

**Getragene Grenze.** Ein Aufrufer ohne Policy bekommt weiterhin nur den Boden, nicht die
erweiterte Menge der Verfassung. Das ist richtig so: mehr kann er ohne das Objekt nicht wissen.

### D157 — Die `03`-Anker zur wirksamen Menge werden nachgezogen, nicht die Tests gelöst

**Der Fall.** D153 macht die wirksame Menge dreielementig. `03-golden-anchors.md` schreibt sie in
`P-A` bis `P-E` als `{obligation@1}` aus. Der `00a`-Lauf hat die betroffenen Tests daraufhin
gegen `PROTOCOL_IRREVOCABLE` verglichen statt gegen die Ankerwerte. Damit prüft `P-B` — der
einzige Vektor, der D58 und D70 gleichzeitig stellt — nichts mehr: er vergleicht die Konstante
mit sich selbst.

**Der Prompt war schuld.** Das Nicht-Ziel „keine Änderung an den Golden Anchors irgendeiner
Schicht" war unerfüllbar, sobald D153 im selben Lauf steht. Die Wirkungsprüfung zu D153 hat
`is_irrevocable` als Konsumenten geführt und nicht gefragt, welche Datei die Menge **ausschreibt**.

**Beschluss.** `P-A` bis `P-E` tragen `{obligation@1, rotate-ack@1, rotate-key@1}`, der
`P-B`-Absatz entsprechend. Die Tests binden wieder an die Ankerwerte.

**Warum das kein nachgezogener Anker im verbotenen Sinn ist.** Die Regel lautet: keinen Anker
bewegen, um einen Test grün zu bekommen. Hier hat sich die **Norm** geändert (D153), und der
Anker war ihr Abbild. Der Unterschied ist prüfbar: ein verbotener Nachzug hat keinen
Registereintrag, der die Normänderung nennt. Dieser hat einen, und D153 steht vor dem Lauf.

**Nicht geändert: `01a-policy-prompt.md §5.1` und `03-prompt.md`.** Beide schreiben die Menge
ebenfalls aus, sind aber erteilte Aufträge und zum Zeitpunkt ihrer Erteilung richtig gewesen.
Sie bekommen eine Hinweiszeile auf D153, keine neuen Zahlen. Eine erteilte Vorgabe
umzuschreiben, damit sie heute stimmt, nimmt der Datei ihren Zweck als Beleg.

### D158 — Berichtigung der Begründung von D152: der Vektor ist die Quittung, nicht der Widerruf

**Der Beschluss von D152 bleibt.** Nur seine Begründung nannte einen Fall, den es nicht gibt.

D152 argumentierte, „ein Claim `C` mit `C.I == K_n`, der die `claim_id` nennt" sei zu weit, weil
ein `core/revoke@1` von `K_n` auf den Rotate von `K_{n-1}` ihn wörtlich erfülle. Ein solcher
Claim ist nicht einlesbar: `_check_foreign_lifecycle` wirft `FOREIGN_LIFECYCLE`, weil das Ziel
einen anderen Autor hat als der Widerruf (`01 §4`). Der Angriff war nicht konstruierbar, und der
`00a`-Lauf hat es beim Bauen des Vektors gemessen.

**Der tragende Vektor ist die Quittung.** Ein `nuc:N/receipt@1` von `K_n` mit
`J = [claim-ref, claim_id(R)]` erfüllt **alle vier** Bedingungen aus D152 — Autor, Ziel, Scope,
Zustand — und unterscheidet sich einzig in `p`. Er ist einlesbar, weil `receipt@1` kein
`core`-Prädikat ist und der Lifecycle-Test ihn nicht sieht. Damit ist die Notwendigkeit des
eigenen Prädikats schärfer belegt als vorher: die Belegung allein trennt nicht, erst der Name
tut es.

Dass ausgerechnet D63s Quittung die Form trifft, ist kein Zufall — D152 hat ihr Muster
übernommen, und zwei Prädikate mit gleichem Muster sind ohne Namensprüfung ununterscheidbar.

**Für `00a`:** Testlage 6 wird auf `receipt@1` umgebaut. Der Widerrufsvektor entfällt ersatzlos.

### D159 — M-5, C-1 und C-9 aus `01a` sind abgelöst; D156 trägt aus `00 §5.2`, nicht aus `§5.4.1`

**Zwei Dinge auf einmal.** Der `00a`-Nachtrag (`11658b4`) hat drei Bestandstests rot gemacht,
und keiner davon ist ein Kollateralschaden: alle drei schreiben aus, dass ohne Policy ein
Widerruf auf eine `obligation@1` wirkt.

| Vektor | Erwartung aus `01a` | unter D156 |
|---|---|---|
| `M-5` | `policy = None` ist nie irrevocable | Bodenprädikate sind es |
| `C-1` | Obligation + eigener Revoke, `policy=None` → `revoked` | `active` |
| `C-9` | abgelaufen und widerrufen ohne Policy → `revoked` | `expired` |

**Die Begründung von D156 war zu stark und wird berichtigt.** D156 stützte sich auf `01 §5.4.1`
(„fehlt das Verfassungsobjekt lokal, gilt der Sicherheits-Default"). Der Satz regelt den Fall
eines **fehlenden Objekts**, nicht den eines Aufrufers, der die Auflösung gar nicht beschritten
hat. Das ist nicht dasselbe, und die Gleichsetzung war ein Fehler.

**Der Beschluss trägt aus `00 §5.2`.** Die Menge heißt dort **Protokoll**-Default. Eine Menge,
die per Definition von keiner Verfassung abhängt, hinter einem Verfassungsparameter zu
verstecken, ist die Fehlform — unabhängig davon, was `§5.4.1` über Partitionen sagt. `P-D` ist
weiterhin ein Beleg, aber kein Beweis.

**`01a §3.3` hat die Frage nie sicherheitsseitig entschieden.** Der Wortlaut: kein Override, alle
Widerrufe wirken wie bisher, „das ist der Pfad, den alle bestehenden Aufrufer nehmen" — dazu die
Eingangszeile des Prompts, die Bestandstests grün halten wollte, weil `policy=None` „exakt die
heutige Semantik" sei. Das ist eine **Migrationsaussage** aus einem Schritt, in dem der Resolver
noch fehlte (`01a §4`: der Resolver kommt mit `03`, D72). Seit D72 gibt es ihn; M-5 und C-1
konservieren einen Übergangszustand, dessen Grund entfallen ist.

**C-1 ist der schärfste Beleg gegen sich selbst:** Obligation plus eigener Widerruf, ohne Policy,
Ergebnis `revoked`. Das Schulden-Lösch-Loch aus D57, als Vektor festgeschrieben.

**Verworfen — `policy=None` bleibt override-frei.** Dann müsste `resolve_current_key` eine Policy
verlangen, der Aufrufer müsste `resolve_policy` bemühen, und die Autoritätsauflösung hinge an der
Verfügbarkeit einer Verfassung — obwohl D153 die Rotationsprädikate gerade als
verfassungsunabhängigen Protokoll-Default gesetzt hat. Das zöge `00a` in genau das Layer 03/04,
das D151 herausgehalten hat.

**Beschluss.** Die drei Tests werden abgelöst und umbenannt; `..._never_irrevocable` kodiert die
alte Norm im Namen. Nach der Trennung aus D157 bleiben die Vektortabellen in
`01a-policy-prompt.md` unverändert stehen und bekommen eine Hinweiszeile: erteilte Aufträge sind
Belege, keine lebenden Erwartungswerte.

**Trennschärfe.** Die neuen Tests müssen belegen, dass ohne Policy **nicht** jeder Widerruf
wirkungslos ist, sondern nur der auf Bodenprädikate. Ohne einen Gegenvektor mit einem
Nicht-Bodenprädikat verkommt die Aussage zu „ohne Policy wirkt kein Widerruf", und das wäre
falsch in die andere Richtung.

**Zweite berichtigte Begründung in dieser Sitzung** (nach D158). Beide Male trug der Beschluss
und die genannte Stelle nicht. Ein Beschluss, dessen Begründung erst beim Widerspruch geprüft
wird, ist so weit gehärtet wie der erste Widerspruch reicht.

### D160 — Abschluss `00a`: gebaut, aber ohne Aufrufer

**Was steht.** `mensch_als_republik/keys.py` mit `resolve_current_key`, der Protokoll-Boden auch
ohne Policy (D156), die Rotationsprädikate im Boden (D153). 526 Tests, vierzehn Eigenschaftstests.
Vier Commits: `0c3f9ad` der Lauf, `11658b4` die Nachbesserung, `2ca9f51` die Ablösung der
`01a`-Vektoren, `768361e` die Verweiskorrektur.

**Die tragende Grenze: niemand ruft die Funktion.** `03 §4` nimmt `authorized_keys` weiterhin als
Parameter von außen entgegen; kein Produktivpfad im Paket füllt ihn aus der Kette. Die
Autoritätsauflösung ist damit rechenbar, aber unwirksam — ein Aufrufer, der eine veraltete Menge
übergibt, bekommt weiterhin ein veraltetes Ergebnis, wie `03 §5` es schon beschreibt.

Das ist **nicht** dieselbe Lage wie `FOREIGN_LIFECYCLE` ohne Produktivträger (D138). Dort wurde
ein Träger bewusst entfernt; hier ist einer neu entstanden und noch nicht angeschlossen. Die Naht
gehört zu `00b`: wer den Anker aus Genesis und Verfassung herleitet, ist auch der Ort, an dem
`authorized_keys` gefüllt wird.

**Zweite getragene Grenze.** Die Equivocation-Prüfung in `_head_from` sieht nur equivozierte
**Rotationen** eines Schlüssels, nicht eine an anderer Stelle gespaltene Autorenkette. `§6.4`
Schritt 3 sagt „die Kette", `§6.3` definiert nur den Rotationsfall. Ob eine Spaltung außerhalb
der Rotationen die Wurzel ebenfalls entwerten soll, ist offen und wird in `00b` entschieden.

**Der Supervisor war fünfmal die Fehlerquelle, das Werkzeug null mal.** Ein unerfüllbares
Nicht-Ziel (D157), zwei Begründungen, die den Beschluss nicht trugen (D158, D159), eine
mehrdeutig beschriebene Testlage, deren naheliegende Lesart am Prüfobjekt vorbeiging (Lage 11),
und ein `classify_all`-Aufruf ohne Policy im Prompt. Das Werkzeug hat jeden dieser Fälle gemeldet
statt still zu reparieren — auch den, den es umgehen musste, um den Auftrag überhaupt auszuführen.

Daraus zwei Prüfregeln:

**Prüfregel 24 — ein Nicht-Ziel, das eine beschlossene Norm verletzt, ist keines.** Vor jedem
„keine Änderung an X" wird geprüft, ob eine Norm desselben Laufs X zwangsläufig bewegt. In `00a`
stand D153 im selben Prompt wie „keine Änderung an den Golden Anchors irgendeiner Schicht"; das
Werkzeug hatte keinen Weg, beides zu erfüllen, und der einzige verbleibende war, die Tests von
den Ankern zu lösen. Ein unerfüllbares Nicht-Ziel erzeugt genau den stillen Umbau, den es
verhindern soll.

**Prüfregel 25 — die Begründung wird beim Beschluss geprüft, nicht beim Widerspruch.** Zweimal in
einer Sitzung hat ein Beschluss getragen und die genannte Stelle nicht: D152 nannte einen
Angriff, den `FOREIGN_LIFECYCLE` ausschließt, D156 einen Paragraphen, der einen anderen Fall
regelt. Beide fielen erst auf, als eine Messung widersprach. Für jede zitierte Stelle wird gefragt,
ob sie den Fall des Beschlusses regelt oder einen benachbarten — ein Beschluss ist nur so weit
gehärtet, wie seine Begründung geprüft wurde, und eine ungeprüfte Begründung sieht aus wie eine
geprüfte.

Der Anlass für 25 war im letzten Sitzungsstart als offen geführt: „ob das eine eigene Regel
braucht, ist beim nächsten Vorfall zu entscheiden — zweimal derselbe Fehlertyp war bisher das
Kriterium". Er trat zweimal in derselben Sitzung ein.

### D161 — Zuschnitt `00b`: der Anker wird hergeleitet, die Epochenkette nicht

**Befund.** Keine Funktion liefert die jüngste ratifizierte Epoche. `verify_ratification` prüft
**einen** Schritt und bekommt `epoch`, `proposal` und `tally` vom Aufrufer; die Kette baut
ausschließlich `tools/example_nucleus.py` von Hand (`Epoch(scope=…, index=1, …)`, dann `index=2`).
`00 §6.4` Schritt 1 sagt „die Verfassung der jüngsten ratifizierten Epoche" und versprach damit
eine Herleitung, die nirgends stattfindet.

**Beschluss.** Die Verfassung wird übergeben, nicht hergeleitet. Der Herleitungsort ist

```
resolve_authorized_keys(store, *, scope, genesis_obj, constitution_hash,
                        constitution_obj=None, now, policy=None)
    -> KeyResolution(keys: frozenset[bytes], findings: tuple[Finding, ...])
```

in `mensch_als_republik/keys.py`. Er rechnet Schritt 1 und reicht das Ergebnis als `anchor_keys`
an `resolve_current_key` weiter, das unverändert bleibt (D151). `scope` wird gegen
`SHA-256(DOM_NUC_GEN || cbor(genesis_obj))` nachgerechnet, `constitution_hash` gegen
`H(constitution_obj)`, sofern das Objekt übergeben wird; beide Abweichungen sind `ValueError`,
kein Vermerk — ein fehlzugeordnetes Objekt ist ein Aufruferfehler und keine Lage der Welt
(D82, D92, D109). Der Typ heißt nach dem, was er trägt: die aufgelösten Schlüssel, nicht den
Anker.

**Ein formwidriges `genesis_obj[1]` ist ebenfalls `ValueError`.** Fehlt der Schlüssel, ist der
Wert keine Liste, oder ist ein Eintrag nicht `bytes` der Länge 32, bricht die Auflösung ab. Der
Unterschied zu `nucleus_keys` (D163) ist der **Ort**: die Verfassung ist ein Fund der Welt, den
ein Leser vorfindet und dessen Defekte er ertragen muss; der Genesis ist das Objekt, aus dem
derselbe Aufrufer eine Zeile vorher den Scope gerechnet hat. Ein Defekt dort ist kein Fund,
sondern ein Widerspruch im eigenen Aufruf. Eine leere Liste ist kein Defekt und liefert einen
leeren Anker.

**Begründung.** `03 §4` hat denselben Fork bereits entschieden und begründet: „`constitution_hash`
ist Parameter, keine Auflösung … welche Version gilt, entscheidet die Ratifizierung … eine
Governance-Frage. Diese Schicht vergleicht byte-weise." `resolve_policy` und `membership` tragen
dieselbe Naht in derselben Signaturform. Eine dritte Bauform an derselben Stelle wäre genau die
Asymmetrie, nach der Prüfregel 8 sucht.

**Warum `constitution_hash` neben `constitution_obj` steht.** `genesis[4]` trägt die Verfassung
der **ersten** Epoche; nach einem Amendment weicht die geltende Fassung zulässig davon ab, und es
gibt lokal nichts, wogegen sie zu prüfen wäre. Der Hash ist deshalb Parameter und nicht aus dem
Genesis ableitbar. Er trägt zugleich das Subjekt des Vermerks aus D164 — dieselbe Rolle wie
`declared_hash` in `resolve_policy`.

**`membership` behält seinen Parameter.** `authorized_keys` intern aufzulösen bräche die normative
Signatur in `03 §4`; stünde beides im selben Prompt, wäre es ein unerfüllbares Nicht-Ziel nach
Prüfregel 24.

**Benannte Grenze: die Epochenkette bleibt ungebaut.** Wer `resolve_authorized_keys` eine veraltete
Verfassung übergibt, bekommt einen veralteten Anker. Das ist dieselbe Grenze, die `03 §4` für
`constitution_hash` schon trägt, und sie wandert mit dieser Entscheidung nicht weiter nach unten.

**Was „angeschlossen" hier heißen kann.** Im Paket ruft **niemand** `membership` auf; gegrept sind
die Aufrufer `tests/profiles/test_membership.py`, `tests/profiles/test_invariants.py`,
`tests/governance/test_vectors.py`, `tools/example_nucleus.py` (Zeilen 459 und 658) und
`tools/sim/szenario.py` (Zeile 221). Das Paket ist eine Bibliothek von Auflösern, komponiert wird
am Rand. Angeschlossen heißt deshalb: es gibt genau **eine** Stelle, die Schritt 1 rechnet, und der
Beispielnukleus benutzt sie. Dort steht heute `authorized_keys=frozenset()`, und die Mitgliedschaft
läuft über `participants`; die hergeleitete Menge ist `{BRUNO, ANNA}` aus `genesis_gov[1]` und
ändert am Zustand nichts. Die Wirkung liegt in der **Prüfung** der hergeleiteten Menge, nicht im
Durchreichen — ein falscher Schritt 1 fiele an der Mitgliedschaft dieses Nukleus nicht auf, weil
er kein `grant-membership@1` führt.

### D162 — Eine Spaltung der Autorenkette an beliebiger Stelle entwertet die Wurzel

**Messung.** `_is_in_equivocation_pair` prüft **den Claim** — Autor und `h_prev` —, nicht den
Autor. `_predecessor_known_and_valid` prüft nur, ob der Vorgänger vorliegt und denselben Autor
hat; ein geflaggter Vorgänger vererbt nichts. Nachfahren einer Spaltung sind `ACTIVE`. Damit
behält heute ein nachweislich verdoppelter Nukleusschlüssel seinen Kopf, und jedes
`grant-membership@1`, das er signiert, ist autorisiert.

**Beschluss.** Hat `k` irgendeinen Claim im Zustand `EQUIVOCATION_FLAGGED`, liefert `k` keinen
Kopf. Ohne Einschränkung auf Rotationen und ohne Einschränkung auf den Scope: die Autorenkette
ist identitäts- und nicht scopegebunden, eine Spaltung ist die Spaltung dieser Identität.

**Begründung.** `§6.3` unterstellt, der Diebstahl zeige sich an einer doppelten Rotation. Das ist
der **späte** Fall. Ein Dieb benutzt den Schlüssel für Akte, lange bevor er um eine Rotation
rennt, und solange beide Halter schreiben, entstehen Paare überall in der Kette. Die Regel „nur
Rotationen" deckt den auffälligen Angreifer und lässt den geduldigen durch.

**Was nicht trägt.** „D155 fängt das ohnehin" gilt nur, wenn zwei Rotationen auf verschiedenen
Zweigen liegen und dadurch unvergleichbar werden. Bei **einer** Rotation und einer Spaltung
anderswo greift D155 nicht — und das ist genau der Fall, um den es geht (Prüfregel 25).

**Preis.** Ein ehrlicher Nukleus, dessen Client einmal zwei Claims auf dieselbe Spitze schreibt,
verliert seine Autorität. Der Ausweg ist `§6.2`, derselbe wie beim Diebstahl, und die
Governance-Rotation braucht den Nukleusschlüssel nicht: `ratify@1` kommt aus `P`. Der Preis ist
also ein bereits vorhandener, erreichbarer Pfad und kein neuer Schaden.

**Richtung.** Monoton in der sicheren Richtung: mehr Wissen nimmt Autorität, gibt keine. Dieselbe
Klasse wie D154.

**Umsetzung.** Die neue Prüfung subsumiert die bisherige — eine equivozierte Rotation ist ein
Claim ihres Autors. Eine Änderung von `nucleus_keys` löst den Fall nicht dadurch auf, dass sie
denselben Schlüssel erneut nennt; sie löst ihn, indem sie einen anderen nennt.

**Literaturprüfung (Prüfregel 15).** Die Fork-Regel von Secure Scuttlebutt wäre der Präzedenzfall.
Eine Suche hat sie nicht belegt; sie wird deshalb nicht als Begründung geführt.

### D163 — Ein gesetztes `nucleus_keys` fällt nie auf den Genesis zurück

**Frage.** Was tut ein Eintrag in `nucleus_keys`, der kein `bytes32` ist.

**Der Bestand kennt beide Muster.** `irrevocable_predicates` verwirft eintragsweise und behält den
Rest (D95); `participants` in `profiles/membership.py` verwirft bei einem einzigen defekten Eintrag
die **ganze** Liste. Das Unterscheidungskriterium ist die sichere Richtung des jeweiligen Feldes,
nicht die Form.

**Hier ist sie eindeutig.** Die ganze Liste zu verwerfen hieße nach `§5.4` „Feld fehlt" und damit
`genesis.root_keys`. Ein einziges formwidriges Byte holte die abgesetzten Wurzelschlüssel zurück.
Das ist die Absetzungs-Umgehung und dieselbe Bauform wie das Schulden-Lösch-Loch aus D57 und D156:
eine Deklaration, die durch ihre eigene Fehlerhaftigkeit den Schutz aufhebt, den sie setzt.

**Beschluss.** Wohlgeformt ist ein Eintrag, der `bytes` der Länge 32 ist. Formwidrige Einträge
werden verworfen und vermerkt (`MALFORMED_NUCLEUS_KEY`), die übrigen bleiben wirksam. Duplikate
fallen wortlos zusammen: `nucleus_keys` bezeichnet eine Menge und ist keine Auszählungsgrundlage —
anders als `participants`, wo ein zu kleiner Nenner jede Schwelle senkt (D96). Eine
Sortierpflicht gibt es aus demselben Grund nicht.

**Ein gesetztes Feld fällt nie auf den Genesis zurück.** Sind alle Einträge formwidrig, oder ist
der Wert gar keine Liste, ist der Anker die **leere** Menge und die Nukleus-Autorität stillgelegt.

**Der Vermerk ist einer je Verfassung.** Subjekt ist `constitution_hash`, nicht der defekte
Eintrag — er ist im Allgemeinen kein `bytes` und passt nicht in `Finding.subject`. Mehrere
formwidrige Einträge erzeugen denselben Vermerk, den `dedupe_sort` zusammenzieht. Die Anzahl geht
verloren; das ist entschieden und kein Versehen.

**Der Preis steht schon in `§5.4`:** „Der Preis ist, dass eine Verfassung den Nukleus per Amendment
handlungsunfähig machen kann. Das ist ausdrückbar und wird nicht verhindert." Dieselbe Zeile trägt
den Tippfehlerfall mit, und der Ausweg ist `§6.2`.

### D164 — Die lokal unbekannte Verfassung ist nicht „die Verfassung nennt kein Feld"

**Befund.** `§6.4` Schritt 1 kennt zwei Lagen — das Feld ist genannt oder nicht. Es gibt eine
dritte: die Verfassung liegt lokal nicht vor. `resolve_policy` führt für sie
`CONSTITUTION_UNAVAILABLE`; im Anker fiel sie stillschweigend in denselben Zweig wie „nennt kein
Feld" und lieferte `genesis.root_keys` — genau die Menge, die eine Absetzung ersetzt haben könnte.
Prüfregel 25: der Satz, auf den man sich berief, regelt den Nachbarfall.

**Beschluss.** Genesis-Rückfall **mit Vermerk** `CONSTITUTION_UNAVAILABLE`, Subjekt
`constitution_hash`. Nicht die leere Menge.

**Begründung gegen die leere Menge.** `nucleus_keys = []` bedeutet seit D150 „die Mitglieder haben
abgesetzt" — eine Aussage. Unwissen als dieselbe Aussage zu kodieren wäre genau die Verwechslung,
die D163 an der anderen Flanke behebt. Der Vermerk trägt den Zweifel; ein Aufrufer, der Findings
als fatal behandelt, bekommt die sichere Richtung, ohne dass die Auflösung sie ihm aufzwingt.

**Damit hat Schritt 1 drei Lagen und nicht zwei.** Der Wortlaut wird nachgezogen.

### D165 — Abnahme `00b`: der Anschluss steht, der Satz über die Kette war verengt

**Was steht.** `mensch_als_republik/findings.py` mit `NucleusFinding`,
`resolve_authorized_keys` und `KeyResolution` in `keys.py`, die auf jede Spaltung erweiterte
Prüfung in `_head_from`, und im Beispielnukleus `check_anchor_resolution` samt `_member`, das die
hergeleitete Menge weiterreicht. Commit `1115281`, gemergt. **541 Tests** und **14**
Eigenschaftstests unter `voll`, kalt auf `main` gemessen. Die Tabelle aus
`tools/example_nucleus.py` ist bytegleich zum Stand davor.

**Befund 1: der neue Satz in `§6.4` Schritt 3 war enger als der alte.** Die abgelöste Fassung
sagte „ist die Kette von k **an einem Punkt** equivoziert"; meine Neufassung sagte „hat k
irgendeinen Claim". Der Code prüft — richtig, und schon vor `00b` — bei **jedem** Schlüssel, den
Schritt 2 auf der Kette erreicht, nicht nur beim Anker. Damit stand die Spec hinter dem Code, und
zwar in der sicheren Richtung, was den Fall nicht besser macht: ein Leser, der `§6.4` umsetzt,
hätte weniger gebaut als das, was gilt. **Der Satz wird mit diesem Eintrag berichtigt**, `00
§6.4` Schritt 3.

Daraus ein Zusatz zu Prüfregel 18: er galt bisher für Aufzählungen, die neben einem Satz stehen.
Er gilt ebenso für einen Satz, der einen älteren **ersetzt**. Der Geltungsbereich des alten wird
zuerst benannt und gegen den Code geprüft, der ihn umsetzt.

**Befund 2: zwei Nähte, zwei Fehlertypen, keine Notiz.** `resolve_authorized_keys` wirft bei
einer Hash-Abweichung `ValueError`, `resolve_policy` gibt an derselben Stelle
`CONSTITUTION_HASH_MISMATCH` als Vermerk zurück. Der Unterschied ist begründet und das Kriterium
ist, **wer den Hash geliefert hat**: `resolve_policy` zieht ihn selbst aus `genesis[4]`, eine
Abweichung ist dort eine Lage der Welt. Bei `resolve_authorized_keys` kommen Hash und Objekt
beide vom Aufrufer, eine Abweichung ist ein Widerspruch im eigenen Aufruf — dieselbe Behandlung
wie in `membership` (D82, D92, D109). Das steht hier, weil eine unbegründete Asymmetrie zwischen
zwei benachbarten Funktionen genau die Stelle ist, an der später jemand harmonisiert (Prüfregel 8).

**Der Supervisor war dreimal die Fehlerquelle, das Werkzeug null mal — zweite Sitzung in Folge.**
Der Prompt sagte „Elf Lagen" und zählte zwölf auf; Abnahmekriterium 4 nannte `python3` statt
`.venv/bin/python`; die Rücknahmeproben 2 und 3 nannten je einen roten Test, wo eine ganze Gruppe
dieselbe Aussage trägt. Das Werkzeug hat alle drei gemeldet und keinen still repariert. Die
Proben selbst haben getragen: jede hat den Test rot gefärbt, für den sie gebaut war, und die
zusätzlich roten hingen nachweislich an derselben Ursache.

**Getragene Grenzen nach `00b`.** Die Epochenkette bleibt ungebaut; wer eine veraltete Verfassung
übergibt, bekommt einen veralteten Anker (D161). `membership` bekommt `authorized_keys` weiterhin
von außen — neu ist, dass es genau **eine** Herleitungsstelle dafür gibt und der Beispielnukleus
sie benutzt. Ein Nukleus mit einem echten `grant-membership@1` würde den Anschluss zum ersten Mal
wirksam machen; der Beispielnukleus führt keines, und `check_anchor_resolution` prüft deshalb die
hergeleitete Menge selbst statt ihrer Wirkung.

### D166 — Autoritätslisten tragen keine Schwelle; die Frage wird umformuliert, nicht beantwortet

**Herkunft.** D126 ließ offen, ob ein Nukleus statt „einer genügt" ein `k`-von-`n` verlangen
können soll. D149 verortete die Frage in der Verfassung, D150 schuf mit `nucleus_keys` das Feld,
an dem eine Schwelle hinge.

**Befund: die Frage war falsch gestellt.** Es gibt drei Autoritätslisten, und alle drei sagen
dasselbe. `genesis.root_keys` und `nucleus_keys` über `§7` — „bei mehreren autorisierten
Schlüsseln genügt einer" —, `arbitration.arbitrators` über `§5.1`, wo ein `verdict@1` bindet,
sobald sein Autor in der Liste steht, ohne Zahl. Eine Schwelle nur für `nucleus_keys` wäre genau
die Asymmetrie, nach der Prüfregel 8 sucht: dieselbe Bauform, verschieden behandelt, ohne
benannten Grund. **Die Frage wird deshalb von `nucleus_keys` gelöst und auf alle drei Listen
gestellt.** Beantwortet wird sie einmal, oder gar nicht.

**Beschluss.** In v1 trägt keine Autoritätsliste eine Schwelle. `§7` wird auf diesen Stand
gezogen.

**Warum nicht jetzt.** Zwei Wege geben einem Nukleus heute `k`-von-`n`: `key_mode = 1` mit FROST
(`§6.5`) auf der Signaturebene, und der Governance-Pfad `propose`/`vote`/`ratify` gegen
`thresholds` (Gov-Spec §5). `grant-membership@1` unter dem Nukleusschlüssel ist die **Abkürzung**
für Nuklei, die keine Abstimmung fahren wollen; eine Schwelle darauf zu legen machte daraus eine
langsame Abstimmung mit weniger Maschinerie — eine zweite, schwächere Kopie von `04`.

**Was ein protokollseitiges `k`-von-`n` zusätzlich entscheiden müsste.** Die Bauform selbst ist
nicht fremd — `rotate-ack@1` (D152) und die Auszählung in `04` sind sie zweimal. Offen wären vier
Wechselwirkungen, jede eine eigene Entscheidung:

1. Ein Assent wird später widerrufen — fällt der Akt rückwirkend?
2. Ein Signierender equivoziert später und verliert nach D162 seine Autorität. Verliert der Akt,
   der bereits zählte, sie auch?
3. `nucleus_keys` schrumpft per Amendment unter `k`. Was gilt für Akte davor, was für danach?
4. Sind Assents scopelokal und fristgebunden, oder gelten sie unbefristet?

Das ist eine Schicht, kein Knopf.

**Der tragende Grund ist `08 §2.2`, nicht der Aufwand.** Es gibt keinen Nukleus, der die Frage
stellt. Ein Mechanismus ohne Kollisionsdichte ist Spezifikationstiefe, und die ist in diesem
Projekt der teurere Fehler.

**Die Gegenposition, ausdrücklich (Prüfregel 15).** TUF entscheidet an derselben Stelle anders:
jede Rolle trägt `keys` **und** `threshold`, `k`-von-`n` auf der Metadatenebene statt per
Schwellensignatur, und die Begründung dort ist, dass ein einzelner kompromittierter Root-Key
nicht allein handeln können soll. Das ist derselbe Bedrohungsfall, der D162 getragen hat. Ist
Diebstahl die Bedrohung, dann **ist** „einer genügt" die Lücke, und die Schwelle ist die
Standardantwort. Dazu kommt, dass FROST für zwei Gründer schwer ist — eine DKG-Zeremonie — und
dass `key_mode` im Genesis steht: später wechseln heißt neuer Nukleus. Der Beispielnukleus hat
heute genau diese Lage; jeder seiner zwei Gründer kann allein aufnehmen, und es ist nicht
belegt, dass sie das gemeint haben.

**Diese Zurückstellung ist deshalb kein erledigtes Nein.** Wer sie aufhebt, beantwortet sie für
alle drei Listen zugleich und entscheidet die vier Wechselwirkungen. Der Anlass, auf den zu warten
sich lohnt, ist der erste Nukleus mit mehr als einem Halter, der einen Diebstahl fürchtet — nicht
der erste, der die Schwelle hübsch fände.

**Zwei Nebenbefunde mitgezogen.** `§7` verwies für den Verfassungsknopf auf `§4`; das ist das
Genesis-Schema, die Verfassung ist `§5`. Und `§9` zählte „nur vier Verfassungsfelder" als
normativ; seit D150 sind es fünf, wie die Tabelle in `§5` schon zeigt.

### D167 — Die Auflösungskette in `03 §1.2` hatte keinen Epochenschritt

**Befund.** `03 §1.2` schreibt die Auflösung normativ als `C.N → Genesis → constitution_hash →
Verfassungsobjekt → irrevocable_predicates`. Diese Kette führt auf `genesis[4]`, und `genesis[4]`
ist nach `00 §4` der Hash der **initialen** Verfassung. `resolve_policy` setzt das genau so um:
ein Verfassungsobjekt, das nicht zu `genesis[4]` passt, ergibt den Boden und den Vermerk
`CONSTITUTION_HASH_MISMATCH`.

Gleichzeitig sagt `00 §5.3`, ein Verfassungsupdate erzeuge ein neues Objekt mit neuem Hash, und
die Ratifizierung sei die Re-Akzeptanz auf diesen Hash. `membership` honoriert das — im
Beispielnukleus wird DORA gegen `constitution_hash_2` gerechnet. **Derselbe Nukleus hatte damit
zwei geltende Verfassungen, je nachdem, welche Funktion man fragt.** Wer `resolve_policy` die
ratifizierte Fassung 2 übergibt, bekommt einen Vermerk, der behauptet, das Objekt gehöre nicht zu
diesem Nukleus. Es gehört dazu; es ist die aktuelle.

Der Beispielnukleus trägt die Frage bereits, ohne sie zu stellen: `_policy(ex)` baut die Policy
immer aus `constitution_gov`, auch für die Prüfungen der Epoche 2.

**Beschluss.** `constitution_hash` wird Parameter von `resolve_policy`, wie in D161 für den Anker
entschieden. Die Kette in `§1.2` bekommt den fehlenden Schritt: welche Fassung gilt, entscheidet
die Ratifizierung, nicht das Genesis. `genesis[4]` bindet die **Epoche 1** und wird von
`resolve_policy` nicht mehr gelesen.

**Verworfen — genesisgebunden lassen und `§5.3` einschränken.** Die Begründung wäre D35 gewesen:
läge `D` in der änderbaren Verfassung, würde ein Amendment Bestandssignaturen still umbewerten.
Sie trägt hier nicht. `D` steckt als `n/D` **in** jeder Vouch-Signatur; `irrevocable_predicates`
steckt in keiner Signatur, es wird beim Lesen angewandt. Prüfregel 25: die zitierte Begründung
regelt den Nachbarfall.

**Verworfen — monotone Vereinigung über die Epochenkette.** Wirksam wäre die Vereinigung aller
ratifizierten Fassungen; mehr Wissen fügte Schutz hinzu und nähme nie welchen. Das ist die
Designmonotonie dieses Projekts und parallel zu `§5.2`. Sie verlangt aber den Kettenlauf, den
D161 ausdrücklich nicht gebaut hat, und sie macht jede Fehldeklaration unwiderruflich — eine
Governance, die nichts zurücknehmen kann, ist die Capture-Fläche, die `00 §9` bei
`amendment_rule` vermeiden wollte.

**`CONSTITUTION_HASH_MISMATCH` entfällt ersatzlos.** Sind Hash und Objekt beide vom Aufrufer, ist
eine Abweichung ein Widerspruch im eigenen Aufruf und damit `ValueError` — dieselbe Behandlung wie
in `membership` und `resolve_authorized_keys` (D82, D92, D109, D161). Damit löst sich auch die in
D165 als Befund 2 notierte Asymmetrie auf: drei Nähte, eine Bauform.

Der Fall, den der Vermerk abdeckte, verschwindet nicht, er wandert: liefert ein Peer ein Objekt,
dessen Hash nicht zum erwarteten passt, **hat man die Verfassung nicht** — der Aufrufer übergibt
`None` und bekommt `CONSTITUTION_UNAVAILABLE`. Das ist die zutreffendere Aussage, weil sie den
Zustand des Lesers benennt und nicht die Zugehörigkeit eines Objekts.

**Was `genesis[4]` damit trägt.** Es ist der Hash, den ein Aufrufer in Epoche 1 übergibt. Das ist
sein Träger, und die in D146 als ungebunden notierte Grenze ist damit beantwortet — als
Nebenprodukt, nicht als Ziel. `GV-24` bleibt konstruierbar wie bisher; die Entscheidung berührt
die Auszählung nicht.

**Nicht in diesem Eintrag, eigene Frage:** ob ein Amendment ein in der Vorgängerfassung
deklariertes Prädikat **weglassen** darf. Heute entschützt es damit Bestandsclaims, und zwar
nicht sichtbar, sondern erst beim Widerruf. Das gehört an `04 §5` und hat mit dem Auflösungsort
nichts zu tun.

**Der Code folgt in einem eigenen Lauf.** `resolve_policy`s Signatur ist in `§1.2` normativ, und
rund fünfzehn Testaufrufstellen hängen daran. Die Spec geht voran, damit der Prompt „die Spec
steht" sagen kann, ohne nach Prüfregel 24 unerfüllbar zu werden.

### D168 — Ein Auflöser prüft, was er liest; die P-Vektoren folgen

**Was D167 nicht ausgesprochen hat.** Die Lagentabelle in `03 §1.2` führte eine Zeile „Genesis
ohne `constitution_hash` oder mit falschem Typ darin → `ValueError`". D167 hat sie gestrichen,
weil `resolve_policy` `genesis[4]` nicht mehr liest. Die Folge stand nirgends: **wer das Feld
nicht liest, prüft es auch nicht.** Ein Genesis ohne Key `4` ist nach `00 §4` defekt, aber das
festzustellen ist nicht Aufgabe dieses Auflösers — sonst stünde die Wohlgeformtheit aus `00 §4`
ein zweites Mal im Code, und genau das haben D111 und D147 abgeräumt.

**Die Regel, die dahintersteht.** `resolve_authorized_keys` prüft `genesis[1]` streng, weil es
den Wert liest, und prüft Key `4` überhaupt nicht (D161). `resolve_policy` prüft den Scope, weil
es das ganze Genesis hasht. Beide prüfen genau ihre Eingabe. Das ist kein Sparen an Sorgfalt: eine
Prüfung ohne Lesegrund ist eine zweite Kopie einer fremden Norm, und Kopien laufen auseinander.

**Zwei Vektoren in `03-golden-anchors.md` §4 werden nachgezogen.** `P-E` erwartete den Boden plus
`CONSTITUTION_HASH_MISMATCH` und erwartet jetzt `ValueError` — der Vermerk entfällt mit D167.
`P-G` erwartete `ValueError` für ein Genesis ohne Key `4` und erwartet jetzt das **normale**
Ergebnis; er ist damit der Vektor, der belegt, dass die Prüfung fort ist. Nachgezogen, weil die
Norm sich geändert hat, nicht um einen Test grün zu bekommen (D157). Wäre eine Erwartung zu
ändern gewesen, ohne dass eine Norm sie bewegt, wäre das der Abbruchgrund.

**`P-G` ist nach der Änderung kein Doppel von `P-A`.** Beide liefern den Boden ohne Vermerk, aber
`P-A` sagt „die Verfassung sagt es" und `P-G` sagt „das Genesis ist unvollständig und der
Auflöser stört sich nicht daran". Der zweite Satz ist die Aussage, die ohne diesen Vektor
niemand prüft.

**Zwei erteilte Prompt-Dateien bekommen Nachträge, keine Korrekturen** (D157-Konvention).
`03-prompt.md` führt die alte Lagentabelle und die alte Subjektregel; `03a-korrektur-prompt.md`
begründet ausdrücklich, warum ein Genesis ohne `constitution_hash` `ValueError` sei. Beide
bleiben im Wortlaut stehen — sie sind erteilt und ihre Zahlen waren zum Zeitpunkt der Erteilung
richtig —, und jede bekommt eine Zeile, die auf `03 §1.2` als normative Fassung zeigt. Nach
Prüfregel 17 sind sie normativer Text, solange Code auf sie zeigt; ein stiller Umbau erteilter
Prompts nähme jeder späteren Abnahme ihren Vergleichspunkt.

### D169 — Abnahme `03b`: der Epochenschritt steht, die Zählung war abgelaufen

**Was steht.** `resolve_policy` nimmt `constitution_hash` als Pflichtparameter, liest
`genesis_obj[4]` nicht mehr und wirft bei Hash-Abweichung `ValueError`.
`ProfileFinding.CONSTITUTION_HASH_MISMATCH` ist entfernt, zwanzig Aufrufstellen sind ergänzt,
`P-E` und `P-G` sind nachgezogen, `P-H` ist neu, und `_policy` im Beispielnukleus geht durch den
Auflöser statt die Policy von Hand zu bauen. Commits `fd408dd` und `c6d63e4`, gemergt. **542
Tests** und **14** Eigenschaftstests unter `voll`, kalt auf `main` gemessen. Die Tabelle aus
`tools/example_nucleus.py` ist bytegleich zum Stand davor.

**Befund 1: eine Zahl im Prompt war nicht falsch getippt, sondern abgelaufen.** Der Prompt nannte
sechs `_policy`-Aufrufstellen; gemessen waren es zehn. Die Zahl stammte aus einem `grep` über die
Projektkopie, und die Kopie hing auf `c32b6e6` — dem Stand **vor** dem `00b`-Merge, der
`check_anchor_resolution` überhaupt erst angelegt hat. Der Hashabgleich zu Sitzungsbeginn war
richtig und galt für diesen Commit; ich habe die Datei danach über zwei Merges hinweg
weiterbenutzt, ohne den Abgleich zu erneuern. Die übrigen Zahlen des Prompts stimmten genau
deshalb, weil `00b` jene Dateien nicht angefasst hatte — die Methode war nicht teilweise richtig,
sie war zufällig nicht falsch. Daraus **Prüfregel 26**.

**Befund 2: eine Aufzählung im Prompt hat einen Fall mitgerissen.** Der Satz „die übrigen fünf
übergeben `constitution_hash_gov, constitution_gov`" traf auch Lage 2 in
`check_anchor_resolution` — den Aufruf, der den Anker gegen die **zweite** Epoche auflöst. Damit
stand die Verschränkung zweier Epochen ausgerechnet in dem Vektor, der sie trennen soll, und zwar
aus dem Grund, den D167 zwei Einträge vorher im selben Beispielnukleus beschrieben hat. Behoben in
`c6d63e4` auf demselben Branch, vor dem Merge.

Kein Ergebnis hat sich dadurch bewegt, und das ist der eigentliche Punkt: `constitution_2`
entsteht als `dict(constitution_gov)` mit geändertem `participants`, `irrevocable_predicates` ist
in beiden Fassungen dieselbe Liste, und der Store dieser Prüfung ist leer. **Zufällige
Harmlosigkeit ist keine Richtigkeit.** Eine Rücknahmeprobe war deshalb nicht möglich; ein Test,
der den Unterschied sähe, müsste die zwei Fassungen in `irrevocable_predicates` auseinanderziehen.

**Getragene Grenze.** Genau das ist der Beispielnukleus heute nicht: er kann eine Policy der
Epoche 1 nicht von einer der Epoche 2 unterscheiden, weil seine beiden Verfassungen in dem Feld
übereinstimmen, um das es geht. Der Epochenschritt aus D167 wird deshalb ausschließlich von `P-H`
gemessen. Ein Beispielnukleus, dessen Amendment `irrevocable_predicates` bewegt, wäre der zweite
Messpunkt — eine eigene Entscheidung, weil er die dokumentierten Hashes in `example-nucleus.md`
bewegt.

**Der Supervisor war zweimal die Fehlerquelle, das Werkzeug null mal — dritte Sitzung in Folge.**
Beide Male hat das Werkzeug gemessen und gemeldet statt still zu reparieren, und beide Male war
die gemeldete Abweichung der Befund. Die Zahl `20` für die Aufrufstellen von `resolve_policy` hat
gestimmt; sie kam aus Dateien, die seit dem Abgleich niemand angefasst hatte.

### D170 — Die Prompt-Verweise im Paketcode: fünf sind richtig, einer zeigt auf eine Spec-Lücke

**Anlass.** Die offene Liste führte „`03-prompt.md`-Verweise im Paketcode — vier Stellen unter
`mensch_als_republik/profiles/` und `policy.py`". Gemessen sind es **sieben**, und sie sind nicht
eine Sorte.

**Fünf nennen die Spec zuerst und den Prompt als zweiten Zeiger.** `profiles/credit.py`
(`03 §3.3.2`), `profiles/verdict.py` (`03 §2.4.2`), `profiles/policy.py` (`03 §1.2`),
`policy.py` (`00 §3`) und `tools/example_nucleus.py` (`01 §4`). Dort ist der Prompt Beleg, nicht
Quelle; er zeigt, woher eine Entscheidung kam, und die normative Fassung steht davor. Diese fünf
bleiben.

**Einer ist ein reiner Zeigerfehler.** `profiles/payload.py` nennt ausschließlich
`03-prompt.md §3.1`, obwohl `03 §1.3` die Kanonizitätsregel samt `NON_CANONICAL_V` im Volltext
führt. Der Verweis wandert auf die Spec.

**Einer ist kein Fehler, sondern der Beleg für eine Lücke.** `governance/findings.py` nennt
`04-prompt.md §2`, und das ist die einzige Stelle, die es gibt: **`INV-04` kommt in
`04-governance.md` nicht vor.** Die Invariantenreihe der Governance-Schicht lebt in
`04-prompt.md`, `04-golden-anchors.md` und `04-abnahme.md` — also in erteilten Prompt- und
Abnahmedateien, die per Konvention nicht mehr umgeschrieben werden (D157). Genau dafür ist
Prüfregel 17 da: der Prompt ist normativ, **weil** Code auf ihn zeigt. Hier zeigt der Code auf
ihn nicht aus Bequemlichkeit, sondern mangels Alternative.

Das ist der eigentliche Fund dieser Runde und wird nicht hier behoben: die `INV-04`-Reihe in
`04-governance.md` aufzunehmen ist eine Spec-Migration und ein eigener Zug. Sie berührt auch D117,
wo zwei dieser Invarianten als schwächer beschrieben sind, als sie scheinen.

**Nebenbefund: `dedupe_sort` existiert viermal.** `04b-korrektur-prompt.md` notierte drei; die
vierte hat mein `00b`-Prompt beauftragt, ohne dass mir die Notiz präsent war. `profiles`,
`governance` und die Nukleus-Schicht führen je eine für `Finding`, `policy.py` eine für
`PolicyNote`. `trust/findings.py` hat **keine** und schreibt dieselbe Operation in
`derive.py:80` inline aus: `tuple(sorted(set(a) | set(b) | set(c)))`.

**Gemessen, nicht vermutet: kein Determinismusbruch.** `trust/graph.py` gibt
`tuple(sorted(findings))` zurück — sortiert, aber nicht dedupliziert, was zunächst nach der Klasse
`B-9` aus `04-abnahme.md` aussieht. Es ist keine: `sorted` ist unabhängig von der
Eingabereihenfolge, und Duplikate sind dort strukturell unmöglich, weil jede
`(author, subject)`-Gruppe im BFS genau einmal besucht wird (`seen` verhindert die
Wiederaufnahme) und `kante_claim_id` je Gruppe eindeutig ist. Vier Schichten, vier Praxen, kein
Schaden.

**Beschluss.** Der Zeigerfehler in `payload.py` und die fehlende Zitatzeile für `dedupe_sort` in
`mensch_als_republik/findings.py` sind zwei Docstrings; sie reiten beim nächsten Lauf mit, statt
einen eigenen zu bekommen. Eine Zusammenlegung der vier `dedupe_sort` findet **nicht** statt: die
vier Enums sind bewusst getrennt (D90), und eine gemeinsame Hilfsfunktion über vier
`Finding`-Typen hinweg bräuchte entweder ein gemeinsames Protokoll oder `Any` — beides teurer als
vier Zeilen, die je zwei Zeilen lang sind.

**Zur Methode.** „Vier Stellen" stand seit Monaten in der offenen Liste und war schon beim
Aufschreiben eine Zählung. Prüfregel 26 gilt auch für die eigene Merkliste: eine Zahl darin ist
ein Messwert mit Verfallsdatum, kein Merkposten. Aufgefallen ist es nur, weil der Grep neu
gelaufen ist — und ein zweiter Grep derselben Runde wäre beinahe untergegangen, weil eine Pipe
auf `tail` seinen roten Status verschluckt hat. Dass `INV-04` nirgends in `04-governance.md`
steht, war ein **leeres** Ergebnis, und leere Ergebnisse sind die, die eine Maskierung frisst.

### D171 — Berichtigung zu D170: es gibt keine `INV-04`-Lücke, sondern eine ungeschriebene Bauform

**Was D170 behauptet und was nicht stimmt.** D170 schließt mit dem Satz, die `INV-04`-Reihe lebe
„in erteilten Prompt- und Abnahmedateien, die per Konvention nicht mehr umgeschrieben werden", und
benennt ihre Aufnahme in `04-governance.md` als nächsten Zug. Beides ist falsch. Die Reihe steht
vollständig in **`04-golden-anchors.md §8`**, als Tabelle `INV-04.1` bis `INV-04.8`, mit den
Vorbehalten aus D117 an Ort und Stelle. `tests/governance/test_invariants.py` zitiert im Kopf
genau diese Stelle und nicht den Prompt. Golden-Anchors-Dateien sind gepflegte Spec-Dateien: D157
hat die `03`-Anker nachgezogen, und `P-H` ist heute dort eingefügt worden.

**Der Fehlschluss.** Aus „`INV-04` steht nicht in `04-governance.md`" wurde „steht nirgends
Normatives", ohne zu prüfen, wie die anderen Schichten es halten. Gemessen: **keine** Layer-Datei
nennt ihre Invarianten. `00`, `02`, `03` und `04` enthalten je null Treffer auf `PR-INV`, `INV-0`
und `golden-anchors`. `04` ist nicht die Ausnahme, sondern die Regel.

Das ist Prüfregel 8, und der Handgriff hat gefehlt, obwohl er in derselben Sitzung zweimal
angewandt wurde — bei D166 für die drei Autoritätslisten und bei D168 für die zwei Auflöser.
Eine Auffälligkeit an **einer** Stelle ist erst ein Befund, wenn die Nachbarstellen dieselbe
Erwartung erfüllen.

**Die Bauform, ausdrücklich.** Die Layer-Datei sagt, **was gilt**; die zugehörige
`*-golden-anchors.md` sagt, **was daran geprüft wird**, mit benannten Vektoren und Invarianten.
Die Trennung ist getragen und hat einen Grund: eine Invariante ist eine Aussage über eine
Implementierung, keine Norm für einen Teilnehmer. Ein Nukleus, der die Spec liest, muss `INV-04.7`
nicht kennen; wer die Auszählung baut, muss es. Dass diese Trennung nirgends aufgeschrieben ist,
ist der Grund, aus dem sie in D170 wie eine Lücke aussah — und der einzige tragfähige Rest jenes
Eintrags.

**Was von D170 stehen bleibt.** Die Zählung sieben statt vier, die Aufteilung in fünf richtige
Verweise und die Messung, dass `trust/graph.py` keinen Determinismusbruch trägt. Der Beschluss zu
den vier `dedupe_sort` bleibt ebenfalls.

**Was sich ändert.** Es gibt keine `INV-04`-Migration und keinen nächsten Zug daraus. Der Verweis
in `governance/findings.py` auf `04-prompt.md §2` betrifft nur „sortiert und dedupliziert" und
nicht die Invariantenreihe; er ist damit derselbe Zeigerfehler wie der in `payload.py`, mit
`04-golden-anchors.md §8` als besserer Stelle. **Drei** Docstring-Zeiger reiten beim nächsten Lauf
mit, nicht zwei:

- `profiles/payload.py` → `03 §1.3` statt `03-prompt.md §3.1`
- `governance/findings.py` → `04-golden-anchors.md §8` statt `04-prompt.md §2`
- `mensch_als_republik/findings.py` → eine Zitatzeile für `dedupe_sort`, die heute fehlt

**Zur Methode.** Ein Registereintrag, der einen Zug später widerlegt wird, ist billiger als einer,
der stehen bleibt: D170 hat den nächsten Schritt benannt, und der Versuch, ihn zu beginnen, hat
den Fehler in einem Zug gefunden. Teuer wäre die Reihenfolge andersherum gewesen — erst migrieren,
dann merken, dass `02` und `03` es genauso halten.


### D172 — Die Ordnung der `claim_id` benennt, sie entscheidet nicht (erweitert D101)

**Der Befund.** Fünf Stellen im Paket wählen aus mehreren Claims, die dieselbe Regel gleich
erfüllen, einen aus. Sie zerfallen in zwei Regeln, nicht in eine:

| Stelle | Bruch | Wirkung |
|---|---|---|
| `trust/groups.py` `build_groups` | `sorted(...)[0]` | kleinste `claim_id` |
| `profiles/membership.py` | `min(accept_ids)`, `min(grant_ids)` | kleinste `claim_id` |
| `profiles/credit.py` `settlement` | `sort(key=claim_id)`, erster passende | kleinste nach Filter |
| `keys.py` `_earliest_on_chain` | Vorfahr aller anderen, sonst `None` | kein Bruch |
| `governance/tally.py` | zwei Stimmen eines Autors, `AMBIGUOUS_VOTE` | kein Bruch |

Die **Entscheidungsseite** ist zweimal ausgeschrieben: `00 §6.3`/`§6.4` (D149, D154, D155, D162)
und `04 §3.1` (D101). Die **Benennungsseite** steht genau einmal, als Abgrenzungs-Zitat in
`04 §3.1` — `membership()` löse mehrere aktive `accept-rules` mit `min(claim_id)` auf, das sei
dort richtig, weil alle dasselbe sagen. Also in der Datei, die sie am wenigsten braucht: `02`
müsste heute `04` zitieren, um zu erklären, wie eine Vouch-Kante benannt wird, und `02` hat mit
Governance nichts zu tun.

**Der erste Anlauf war zu weich.** Als allgemeine Regel formuliert, hätte das Kriterium „die
Kandidaten sagen dasselbe" vom Atom ein Urteil über die **Bedeutung** von Aussagen verlangt —
gegen `01 §1 A2`. In `04 §3.1` geht der Satz durch, weil er Prosa über einen benannten Fall ist;
an der Basis wäre er ein Leitsatzbruch. Der Supervisor hat ihn geschrieben und auf Nachfrage des
Operators zurückgezogen, bevor ein Splice lief.

**Die Entscheidung: eine strukturelle Probe statt eines semantischen Urteils.**

> **Vertauschungsprobe.** Ersetzt man den benannten Claim durch einen beliebigen anderen aus
> derselben Kandidatenmenge, ist das Ergebnis der Ableitung byte-gleich — das benannte Feld
> ausgenommen.

Hält sie, ist es Benennen und die kleinste `claim_id` gilt. Hält sie nicht, ist es Entscheiden;
dann darf keine **abgeleitete** Ordnung wählen (Hash, Kodierungslänge, Ankunftszeit), sondern nur
eine **deklarierte** — Verfassung oder Governance-Akt. Gibt es keine, fällt die Aussage weg. Die
Probe ist mechanisch nachprüfbar und braucht kein Urteil über Bedeutung.

**Warum die Mahlbarkeit die Regel trägt.** Die `claim_id`-Ordnung ist ein Nebenprodukt des
Hashes; wer einen Schlüssel hält, erzeugt Claims, bis seiner der kleinere ist. Auf der
Benennungsseite ist das folgenlos, weil per Vertauschungsprobe kein Ergebnis daran hängt — wer
mahlt, gewinnt einen Namen. Auf der Entscheidungsseite wäre Autorität durch Rechenzeit wählbar.
Dieselbe sichere Richtung wie D162: mehr Wissen entzieht Autorität, es verteilt sie nicht neu.

**Was die Literatur beisteuert (Prüfregel 15).** Drei Vorbilder, ein Ergebnis.

- **CRDT, Multi-Value gegen LWW-Register.** Das MV-Register behält alle nebenläufigen Werte, das
  LWW-Register kollabiert sie über eine willkürliche Totalordnung und verliert dabei still
  Schreibvorgänge (Lost Update). Der gangbare Mittelweg ist bekannt und genau unserer: ein
  mehrwertiger Zustand mit **einem** willkürlich gewählten *angezeigten* Wert. Die Willkür lebt
  in der Anzeige, nie im Zustand.
- **Ethereum, LMD-GHOST.** Bricht Gleichgewicht über die lexikografisch höhere Blockwurzel, mit
  der ausdrücklichen Begründung, die konkrete Wahl sei gleichgültig, solange alle dieselbe
  treffen. Das ist eine Entscheidung über eine abgeleitete Ordnung, und tragbar ist sie dort nur,
  weil eine getrennte Finalisierungsschicht (Casper FFG) den Kopf später einschränkt und
  revidiert. Diese Schicht gibt es hier nicht; derselbe Griff wäre bei uns endgültig.
- **did:plc.** Konkurrierende Operationen werden über den **Index im deklarierten**
  `rotationKeys`-Array aufgelöst, nicht über den Inhaltshash — und auch das nur in einem
  72-Stunden-Fenster und gegenüber einem zentralen Verzeichnis. Deklarierte Ordnung plus
  Zeitfenster plus Verzeichnis für das, was hier ein Governance-Akt ist.

**Was sich ändert.**

- `01 §4.1` ist neu und trägt die Regel: Benennen, Entscheiden, Vertauschungsprobe, die
  ausdrückliche Feststellung, dass die Probe kein Bedeutungsurteil ist.
- `02 §3.1` sagt jetzt, dass `kante_claim_id` der Benennungsregel folgt und warum die Probe hält
  (`cap`, Budget, BFS und Fluss lesen das Feld nicht).
- `03 §6` sagt dasselbe für `subject` und die `*_claim_id`-Felder.

**Was sich ausdrücklich nicht ändert.** `04 §3.1` bleibt byte-gleich. Ein Umschreiben dort
riskierte, den Geltungsbereich von D101 beim Neuformulieren zu verlieren (Zusatz zu Prüfregel
18), und der Gewinn wäre ein Rückverweis. `01 §4.1` nennt `04 §3.1` und D101 als Herkunft; eine
Richtung genügt.

**Folge für den Lauf.** Aus einem Vektortest werden zwei Prüfstücke. Ein Vektor hält den Wert
fest (`kante_claim_id` ist die kleinste `claim_id` unter den Gleichständigen), ein
Eigenschaftstest prüft die Vertauschungsprobe selbst. Die Rücknahmeprobe unterscheidet beide: mit
`tied[-1]` statt `tied[0]` muss der Vektor rot werden und der Eigenschaftstest **grün bleiben**.
Ein Eigenschaftstest, der dabei mitrötet, prüft den Wert und nicht die Norm.

**Herkunft.** Der Anlass war der ungeprüfte Bruch über `sorted(...)[0]` in `build_groups`, offen
seit der Abnahme der Autorschaft. Dass daraus fünf Stellen und zwei Regeln wurden, ist Prüfregel
8 — und dass sie beim ersten Anlauf nur drei waren, weil `00` und `04` nicht gegrept worden
waren, ist derselbe Handgriff, einmal versäumt.


### D173 — Abnahme `00c`: die Benennungsregel ist geprüft; Berichtigung zu D171

**Was gebaut wurde.** `tests/trust/test_groups.py` hält den Wert fest — bei zwei aktiven Vouches
derselben Gruppe mit gleichem `n` trägt die Kante die kleinste `claim_id`, und die Kandidatenmenge
wird im Test aus dem Store abgeleitet, nicht getippt. `tests/trust/test_benennung.py` hält die
Norm: zwei Welten, die sich allein im deklarierten `t` des zweiten Vouch unterscheiden, benennen
verschiedene Claims und stimmen in allem übrigen byte-genau überein. 544 Tests, 14
Eigenschaftstests.

**Die Rücknahmeproben haben die beiden Prüfstücke getrennt**, und das war der Zweck des Laufs:

| Eingriff | Vektor | Vertauschungsprobe |
|---|---|---|
| `groups.py`: `tied[0]` → `tied[-1]` | rot | grün |
| `graph.py`: Kanten nach `claim_id` sortiert | grün | rot |

Die erste Zeile verletzt den Wert, nicht die Norm: bei zwei Kandidaten ist `tied[-1]` weiterhin
eine Auswahl aus der Kandidatenmenge und schlägt in beiden Welten um. Die zweite macht den Namen
zur Eingabe in die Kantenreihenfolge. Wäre die Vertauschungsprobe in beiden Zeilen rot geworden,
prüfte sie den Wert und nicht die Aussage — sie wäre dann wertlos gewesen, nicht doppelt gut.

**Berichtigung zu D171: `04-golden-anchors.md §8` trägt die Aussage nicht.** D170 führte den
Verweis auf `04-prompt.md §2` im Docstring von `governance/findings.py` als Zeigerfehler und
nannte `04-golden-anchors.md §8` als bessere Stelle; D171 ließ das stehen. Gemessen: §8 ist die
Invariantentabelle `INV-04.1` bis `INV-04.8` und sagt zu Vermerken nichts. Der Satz, um den es
geht, steht in `04-prompt.md` Zeile 97, im Abschnitt `## 2. Modulschnitt`: `findings` ist überall
sortiert und dedupliziert. Der ursprüngliche Zeiger war **richtig**; der Lauf hat ihn zuerst
verschlechtert und im selben Branch zurückgenommen.

**Die Bauform, die dabei sichtbar wurde.** Jedes `findings.py` zitiert die eigene Schicht:
`trust/findings.py` auf `02a §5`, `profiles/findings.py` auf `03-profiles.md §6`,
`governance/findings.py` auf `04-prompt.md §2`. Nur `mensch_als_republik/findings.py` hat keine
Stelle in `00`, die den Satz trägt, und zitiert deshalb denselben schichtübergreifenden Satz —
sichtbar als Ausnahme, nicht als Regel. Dass `00` die Form seiner Vermerke nirgends festhält,
bleibt offen.

**Woraus Prüfregel 27 kommt.** Der Verweis hat vier Stationen durchlaufen — D170, D171, den
`00c`-Prompt und den Lauf —, und an keiner hat jemand die Datei aufgeschlagen. Prüfregel 8 hätte
gereicht: die drei Nachbarn zitieren ihre eigene Schicht, `04-prompt.md §2` war für `governance/`
genau das, und der vermeintliche Fehler war die Regel. Das ist derselbe Fehlertyp wie in D169 —
eine Behauptung, die einmal richtig aussah und danach nicht mehr nachgemessen wurde —, nur ohne
Verfallsdatum: dieser Verweis war nie richtig.

**Zwei benannte Grenzen des Laufs.** Die Sondierwelt der Vertauschungsprobe erzeugt keine
Vermerke: `Σ n_budget` bleibt bei allen drei Autoren innerhalb von `D`, also gibt es weder
`OVERCOMMITTED_AUTHOR` noch `SUBGRANULAR_VOUCH`. Der Vermerksvergleich läuft damit leer, und die
Ausnahmeliste — `Edge.claim_id` und das `subject` von `SUBGRANULAR_VOUCH` — ist nur zur Hälfte
geprüft. Zweitens werden die Vermerke dort als Menge verglichen, nicht als Folge; Reihenfolge und
Vielfachheit fallen weg. Bei leerer Menge folgenlos, bei einer künftigen Sondierwelt nicht mehr.

**Was aus Auftrag A entfiel.** Der zweite Messpunkt für `SUBGRANULAR_VOUCH.subject` ist nicht
gebaut worden: die Gleichstandsgruppe sitzt am Anker, dort gilt `C = C₀ = 16` und
`cap = ⌊2·16/4⌋ = 8`, also nie null. Eine zweite, ankerferne Gruppe wäre Umbau gewesen. Das
Werkzeug hat es gemeldet statt gebaut — richtig so; der Punkt gehört auf die offene Liste.

**Zur Fehlerquelle.** Vierte Sitzung in Folge: der Supervisor war die Fehlerquelle, das Werkzeug
nicht. Der Bericht war in jeder Zelle zutreffend, und der Defekt stand trotzdem im Diff — er
stammte aus dem Prompt.

### D174 — Die Epochenkette: `resolve_epoch` leitet die geltende Epoche her

**Entscheidung.** `mensch_als_republik/governance/chain.py` erhält `resolve_epoch`. Die Funktion
beginnt bei Epoche 1 aus dem Genesis (`04 §1.1`), sucht zu jeder Epoche die tragenden `ratify@1`
und läuft, bis keine mehr trägt. Ergebnis ist ein `EpochResolution` aus geltender Epoche,
zugehörigem Verfassungsobjekt und Vermerken. Normiert in `04 §4.5`.

**Warum eine eigene Datei.** `epoch.py` prüft **einen** Übergang und ist damit fertig; die Kette
läuft **alle**. Zwei Fragen, zwei Dateien.

**Kein `policy`-Parameter.** Die Policy wird je Epoche aus deren Verfassung über `resolve_policy`
hergeleitet. Eine von außen gereichte Policy gälte für alle Epochen der Kette; nach einem
Amendment, das `irrevocable_predicates` ändert, wäre sie falsch — und zwar still. `04 §1.2`
verlangt ausdrücklich, dass eine Auszählung in Epoche `i` gegen die Verfassung von `i` rechnet.

**Die neue Kante.** `governance/` importiert bisher nirgends aus `profiles/`; nur `tools/`
verbindet beide. `chain.py` importiert `resolve_policy` und zieht damit die erste Kante dieser
Art. Sie ist schichtungskonform (04 über 03). Die Alternative wäre, `NucleusPolicy` in `chain.py`
selbst zu bauen — dieselbe Regel an zwei Stellen, also derselbe Defekt, den D147 für
`TrustParams.__post_init__` bereits notiert hat.

**`scope` bleibt Parameter** und wird gegen `genesis_obj` geprüft, mit `ValueError` bei
Abweichung. Das ist die Form, die `resolve_authorized_keys`, `resolve_policy` und `decide` alle
drei schon haben; eine vierte Form wäre eine Sonderregel ohne Grund.

**Terminierung ohne Zyklusprüfung.** Jeder Übergang braucht mindestens ein `ratify@1`, dessen `J`
auf einen Vorschlag mit `predecessor == epoch_id(i)` zeigt. Beide Felder sind fest, also trägt
jeder Claim höchstens einen Übergang; und `epoch_id` hasht den streng wachsenden Index mit, also
ist jede Epoche der Kette verschieden. Die Schrittzahl ist durch die Zahl der `ratify@1` im
Speicher begrenzt. Eine `visited`-Menge wie in `_head_from` (`keys.py`) ist deshalb **nicht** zu
bauen: die Rotationskette dort ist autorverkettet und kann zyklisch werden, diese Kette nicht.
Der Punkt gehört ausdrücklich in den Prompt, sonst baut das Werkzeug die Prüfung aus Analogie mit.

**`constitution_obj` gehört in die Rückgabe.** Ein leeres Feld ist selbst die Meldung, dass die
Verfassung der geltenden Epoche unbekannt ist; der Aufrufer reicht es unverändert an
`resolve_authorized_keys` weiter, wo D164 den Rückfall auf `genesis.root_keys` regelt. Ein eigener
Vermerk dafür wäre dieselbe Auskunft ein zweites Mal.

**Vermerke nur zur erreichten Epoche.** Die Kette gibt die Vermerke der Prüfungen nach `04 §4.1`
weiter, soweit sie auf die erreichte Epoche zeigen, und die Vermerke der Auszählungen nach
`04 §3` gar nicht. Begründung: die Kette beantwortet, welche Epoche gilt. Ein Vermerk über eine
Ratifizierung, die in einer längst überholten Epoche nicht trug, beantwortet eine Frage, die
niemand gestellt hat; und ein Auszählungsvermerk ohne die zugehörige Auszählung ist für den
Aufrufer nicht lesbar. Die Tatsache erreicht ihn über `TALLY_UNEVALUABLE`.

**Neuer Vermerk `EPOCH_PROPOSAL_UNAVAILABLE`**, Subjekt der `proposal_hash`, wenn das
Vorschlagsobjekt einer sonst tragenden Ratifizierung fehlt. `UNKNOWN_PROPOSAL` ist dafür nicht
wiederverwendbar: dort ist das Subjekt die `claim_id` einer Stimme. Derselbe Vermerkstyp mit
verschiedenem Subjekttyp nennt auf zwei ehrlichen Knoten Verschiedenes — die falsche Kollision
aus D172.

### D175 — Objektbeschaffung wird gegen den Schlüssel geprüft (berichtigt `04 §3`)

**Befund.** `decide` nimmt vier Objekte von außen. Drei werden gegen ihren Hash geprüft:
`genesis_obj` gegen `epoch.scope`, `constitution_obj` gegen `epoch.constitution_hash`,
`target_constitution_obj` gegen `proposal.constitution_hash`. Das vierte, `known_proposals`, wird
geglaubt: `known_proposals[other.J[1]]` wird gelesen, ohne dass `proposal_hash` des Werts gegen
den Schlüssel geprüft wird.

**Wirkung.** Bildet das Mapping einen Hash auf ein `Proposal` mit falschem `predecessor` ab, so
unterbleibt `CONFLICTING_APPROVAL`, und ein Autor stimmt in derselben Epoche zweimal Ja. Damit
fällt `04 §4.4` — die Regel, die die Spec selbst „sicherheitstragend, nicht ordnungspolitisch"
nennt und gegen Split Brain stellt. Die Wirkung greift gegen einen Aufrufer, der ein empfangenes
Objekt unter dem mitgelieferten Hash ablegt statt unter dem gerechneten; die drei Nachbarstellen
zeigen, dass die Codebasis diesen Aufrufer sonst nirgends voraussetzt.

**Entscheidung.** Jeder Zugriff auf eine Objektabbildung prüft den Wert gegen den Schlüssel. Ein
Eintrag, der nicht passt, gilt als **unbekannt** und läuft in den bestehenden Zweig — bei
`known_proposals` also in `UNKNOWN_PROPOSAL`, die sichere Richtung nach `04 §4.4`. Kein
`ValueError`: der Aufrufer kontrolliert den Inhalt fremder Objekte nicht. Das ist die Asymmetrie,
die `04 §3.5` für Genesis gegen Verfassungsobjekte bereits aufschreibt.

**Form der Beschaffung.** Abbildung vom Hash auf das Objekt, kein eigenes Protocol. `decide` führt
`known_proposals` bereits so; die Kette ergänzt `known_constitutions`. Nach `08 §3` entscheidet
Beschaffung nichts und senkt keine Kollisionskosten — sie ist Werkzeug, nicht Protokoll, und
bekommt die kleinste Oberfläche, die trägt.

### D176 — Zwei Nachfolger derselben Epoche sind unerreichbar (vervollständigt `04 §4.4`)

**Der Fork, der keiner war.** Die Designrunde hatte gefragt, welche Ordnung einen Gleichstand
zwischen zwei tragenden Nachfolgern bricht, und D172 als Antwort erwogen: die Vertauschungsprobe
hält nicht, also darf keine abgeleitete Ordnung wählen. Die Prämisse war falsch. `04 §3.5`
verlangt `2 * num >= den` auf den Rohwerten beider Verfassungen; eine Schwelle unter der Hälfte
ergibt `MALFORMED_THRESHOLD`, und die Auszählung läuft nicht. Es gibt keinen Gleichstand.

**Der Beweis, in beiden Fällen.** `durchgekommen` ist strikt (`04 §3.2`), also ist jede erreichte
Schwelle eine echte Mehrheit von `P`. Disjunkte Ja-Mengen schließt `04 §3.5` aus und führt die
Rechnung dort. Überschneidende Mengen schlägt `04 §4.4`: `CONFLICTING_APPROVAL` entfernt den
Schnitt `S` aus beiden, für den Rest von `A` gilt `|A| - |S| <= n - |B|`, und aus
`|B| * den > num * n` folgt `n - |B| < n * (den - num) / den`. Die Schwelle zu erreichen verlangte
`den > 2 * num` — ausgeschlossen. Erschöpfend gegengerechnet für alle `n <= 40` und alle
wohlgeformten Schwellen mit `den <= 40`: kein Paar bleibt stehen.

**Nachzug an `04 §4.4`.** Der Abschnitt behauptete die Unmöglichkeit mit halbem Beweis — er endete
bei der Überschneidung und nannte den tötenden Schritt nicht. Und er schrieb „bei einer Schwelle
über der Hälfte", während die Schranke `2 * num >= den` lautet, also **ab** der Hälfte; bei genau
`1/2` trägt die Aussage über die Striktheit von `§3.2`, nicht über die Schwelle.

**Der Ausgang bleibt definiert.** `resolve_epoch` hält bei zwei tragenden Nachfolgern an: kein
Kopf ab `i`, Ergebnis ist `i`, Vermerk `EPOCH_FORK` je `epoch_id`. Das ist die Form, die
Tendermint für den erkannten Fork wählt — der Light Client hält an, sendet den Beweis und
verifiziert nicht weiter —, und sie deckt sich mit der Quorum-Literatur: wo die Überschneidung
fehlt, ist die Konfiguration kaputt und nicht auflösbar; wo sie da ist, ist Divergenz unmöglich.
Ein Tiebreak über eine abgeleitete Ordnung kommt in keiner der gesichteten Quellen vor.

**Ohne Produktivträger, ausdrücklich.** `EPOCH_FORK` wird nie erzeugt. Ein Test darauf ist nicht
zu bauen: er prüfte eine unmögliche Lage und wäre ein Regressionstest, der keine Regression sieht.
Präzedenz ist `FOREIGN_LIFECYCLE` (D138), das aus demselben Grund im Enum steht und nirgends
ausgelöst wird. Der Punkt gehört als Nicht-Ziel in den Prompt.

### D177 — Berichtigung `04 §8`: `resolve_current_key` ist gebaut, nicht vertagt

**Befund.** `04 §8` führte `resolve_current_key` (D62) in der Liste „Vertagt und ausdrücklich
nicht in v1". Die Funktion ist seit `00a` gebaut (D160), und `04 §5` schreibt das zwei Abschnitte
weiter oben selbst. Zwei Sätze derselben Datei widersprachen einander.

**Prüfregel 8 erfüllt.** Die Nachbarn derselben Aufzählung — gewichtete Auszählung (D98),
Zweck-Tag am Vouch (D56), Kettenbindung nach VR-04.1 (D26), Zeugenquorum für Fristen (D100) —
sind sämtlich unverändert gültig. Nur dieser eine Eintrag war von `00a` überholt und nie
nachgezogen worden. Er entfällt ersatzlos.

**Fehlertyp.** Derselbe wie in D169 und D173: eine Behauptung, die einmal richtig war und danach
nicht mehr nachgemessen wurde. Anders als bei D173 gab es hier ein Verfallsdatum — der Satz war
bis `00a` zutreffend. Das ist Prüfregel 26 in ihrer allgemeinen Form: auch ein Spec-Satz gilt für
den Stand, an dem er geschrieben wurde.

### D178 — Die Aussetzung aus D103 wirkt über Epochengrenzen

**Befund, gemessen im Lauf `00d`.** D103 nennt als getragene Grenze, dass eine Ja-Stimme auf einen
nie verbreiteten Vorschlag ihren Autor „für diese Epoche" aussetzt. Die Formulierung ist zu eng.
`decide` prüft für Epoche `i` alle aktiven Ja-Stimmen eines Autors und kann bei einem unbekannten
Vorschlag nicht feststellen, zu welcher Epoche er gehört — das ist gerade die Lage, die D103
regelt. Eine Stimme aus `i+1` schlägt deshalb auf die Auszählung in `i` durch.

**Wie es sichtbar wurde.** Ein Abnahmekriterium des Laufs erwartete, dass die Kette bei
unbekanntem zweitem Vorschlag bei Epoche 2 endet. Gemessen wurde Epoche 1. Ursache: die
Teilnehmermenge der ersten Verfassung ist Teilmenge der zweiten, also stimmen dieselben Autoren in
beiden Runden. Ist der zweite Vorschlag unbekannt, blockieren ihre Stimmen aus Runde zwei ihre
Stimmen aus Runde eins, alle vier landen in `excluded`, und schon der erste Übergang trägt nicht
mehr. Das Kriterium war falsch, nicht der Code; der Vektor hält die Messung fest.

**Die Rechnung.** Bei vier Teilnehmern und `amendment = [3, 4]` verlangt `§3.2`
`yes * 4 > 3 * 4`, also alle vier Stimmen. Ein einziger ausgesetzter Autor genügt, damit kein
Übergang mehr trägt.

**Der Angriff.** Ein Mitglied kann die Epochenkette rückwirkend anhalten, indem es auf einen
Vorschlag Ja stimmt, dessen Objekt es nie veröffentlicht. Heilbar nur dadurch, dass jemand das
Objekt nachreicht — und wenn nur der Autor es besitzt, tut das niemand. Verhindern kann die
Gruppe es nicht: die Stimme ist wohlgeformt, signiert und aktiv.

**Warum die Richtung trotzdem bleibt.** Die Gegenannahme — unbekannt heißt fremde Epoche — lässt
bei Teilwissen zwei gültige Nachfolger derselben Epoche entstehen und bricht `INV-04.3`. Die
Wirkung ist stets abwärts: eine erreichte Epoche fällt zurück, es entsteht nie eine. Und sie
heilt bei Wissenszuwachs.

**Literatur (Prüfregel 15).** Die Verfügbarkeitsschicht moderner Ketten trifft dieselbe Wahl:
fehlende Daten heißen nicht vorrücken, und ein Block, dessen Daten fehlen, wird verworfen statt
angehängt. LazyLedger macht Verfügbarkeit sogar zum einzigen Gültigkeitskriterium. Ein
Unterschied ist zu benennen: dort darf Gültigkeit sich **nicht durch Zeitablauf** ändern, weil das
Abwarten belohnen würde; hier ändert sie sich durch **Wissenszuwachs**, was Faulheit nicht
belohnt.

**Die Grenze, die bleibt.** Dort ist Verfügbarkeit erzwingbar — Stichprobenverfahren, Erasure
Coding, Strafen. Diese Schicht gibt es hier nicht und wird es nicht geben; `08 §3` ordnet sie als
Policy ein, nicht als Protokoll. Die Selbstaussetzung ist damit eine getragene Grenze, keine
Lücke im Entwurf. Sie gehört auf die offene Liste, nicht in einen Lauf.

**Nicht entschieden.** Ob ein Mitglied, das wiederholt auf unveröffentlichte Vorschläge stimmt,
eine Folge tragen soll, ist eine Frage an Layer 05 und hier ausdrücklich offen.

### D179 — Abnahme `00d`: die Epochenkette steht; vier Kriterien waren unmöglich

**Was gebaut wurde.** `governance/chain.py` mit `resolve_epoch` und `EpochResolution`; zwei neue
Vermerke `EPOCH_PROPOSAL_UNAVAILABLE` und `EPOCH_FORK`; die Schlüsselprüfung für
`known_proposals` in `decide` (D175). 556 Tests, davon zwölf neue in
`tests/governance/test_chain.py`. `resolve_authorized_keys` hat damit erstmals eine Quelle für
`constitution_hash`, die nicht von außen kommt — der Anschluss selbst bleibt ein eigener Lauf.

**Die Zählung.** Von neun Testfällen, die aus den Prompts dieses Laufs stammten, waren **vier
falsch**, und alle vier waren vor dem Werkzeug entschieden. Kein einziger Defekt lag in der
Umsetzung. Das ist die fünfte Sitzung in Folge mit dieser Verteilung.

**Die vier, nach Fehlerform.**

1. *Ein Objekt, das für den Übergang bekannt und für das Ergebnis unbekannt ist.* Die Verfassung
   von `i+1` ist zugleich das Zielobjekt des Übergangs. Nachgezogen in `§4.5`.
2. *Zwei Objekte unter einem Schlüssel.* Ein falsch geschlüsseltes `C3` unter dem Hash von `C2`
   heißt, dass `C2` fehlt — die Kette kommt aus Epoche 1 nicht heraus.
3. *Eine Rückwirkung, die überlappende Teilnehmermengen ausschließen.* Daraus wurde D178.
4. *Der Widerruf eines Prädikats, das die Verfassung zwingend schützt.* D107 verlangt `ratify@1`
   in `irrevocable_predicates` und erklärt einen Nukleus ohne diesen Eintrag für nicht auszählbar.
   Der Aktivitätsfilter der Kette ist deshalb **nur über Equivocation** prüfbar — und genau das
   steht seit D107 im Register, unter der verworfenen Alternative. Der Supervisor hatte den
   Eintrag nicht aufgeschlagen.

**Daraus Prüfregel 28.** Ein Abnahmekriterium behauptet einen Weltzustand, nicht nur eine Aussage.
Vor dem Prompt ist der Zustand zu konstruieren, nicht nur die Erwartung zu prüfen. Alle vier
Fälle lasen sich schlüssig; Schlüssigkeit ist an dieser Stelle kein Prüfmittel.

**Wie mit den Messungen verfahren wurde.** Die drei fehlgeschlagenen Kriterien wurden **nicht**
durch bequemere ersetzt, sondern als Vektoren mit der gemessenen Erwartung festgeschrieben, jeder
mit einem Docstring, der den Grund nennt. Daneben stehen drei isolierende Tests für die Normen,
die eigentlich gemeint waren. Der Operator hat diese Trennung verlangt; der erste Entwurf des
Supervisors hätte die Beobachtungen gelöscht. Ein nachgezogener Anker löscht die Messung, ein
aufgeschriebener Vektor bewahrt sie — und im Fall von Kriterium 2 war die Messung einen eigenen
Registereintrag wert.

**Die Rücknahmeproben.** Drei von vier haben getrennt. Die vierte konnte es nicht, weil sie einen
unmöglichen Zustand ansteuerte; nach dem Umbau auf Equivocation trennt sie. Eine Probe, die einen
nicht konstruierbaren Zustand prüft, ist keine Probe — sie bleibt rot, egal was man zurücknimmt.

**Offen geblieben.** `chain.py` importiert `_is_nuc_name` aus `epoch.py`. Der führende Unterstrich
sagt modulprivat, der Import sagt geteilt; eines von beiden stimmt nicht. Nicht blockierend,
gehört auf die offene Liste.

### D180 — Der Aufrufer der Kettenauflösung ist der Node; die Bibliothek kennt ihn nicht

**Die Frage.** Wer verkettet `resolve_epoch`, `resolve_authorized_keys` und `membership`? Solange
niemand als Aufrufer benannt ist, lässt sich der Zuschnitt einer Fassade nicht begründen — jede
Grenze ist dann gleich gut vertretbar.

**Die Antwort steht seit VISION §5 und `06 §2`.** Der Lebensraum eines Atoms ist ein Node; „Node"
ist Betriebs-Vokabular, keine Protokoll-Entität — im Protokoll erscheint er allein als Identity mit
`service-announce`. Dieser Eintrag entscheidet nichts Neues; er **benennt** den Empfänger für die
Vertagungen aus `08 §3`.

**Was daraus folgt.** Der Zuschnitt der Auflösung ist damit abgeleitet statt gesetzt. Ein Node hat
eine wiederkehrende Aufgabe: ein fremder Claim kommt herein, und er muss wissen, unter welcher
Verfassung und mit welchen Schlüsseln er ihn prüft. Soviel tut die Fassade, keinen Schritt mehr.

**Die Gegenrichtung ist normativ.** Die Bibliothek darf den Node nicht kennen. Kein Pfad, kein
Socket, kein Daemon in `mensch_als_republik/`; `store` bleibt eine Abbildung, `now` bleibt
Parameter. Unix ist nicht Teil von TCP/IP — ein Protokoll, das seine Umgebung voraussetzt, hat sie
global gemacht.

**Kein Bauauftrag.** Der Node selbst wird nicht gebaut. `08 §2.2` gilt unverändert; ein Lebensraum
ohne Leben darin ist Infrastruktur auf Vorrat.

### D181 — `is_nuc_name` steht einmal, in `predicates.py`, und trägt keinen Unterstrich

**Der Befund.** `_is_nuc_name` ist **sechsmal** definiert — `governance/tally.py`,
`governance/epoch.py`, `profiles/verdict.py`, `profiles/credit.py`, `profiles/membership.py` und
`keys.py` —, alle sechs byte-identisch, dazu ein modulübergreifender Import in
`governance/chain.py`. Gemessen: 18 Vorkommen in 7 Dateien, davon 11 Aufrufstellen. Die Übergabe
`00e` hatte den Fall als einen Import über eine Modulgrenze notiert; das war zu klein gemessen.

**Warum das ein Befund ist.** Die Funktion kodiert die Prädikat-Grammatik aus `01 §2.2` und
Anhang A — eine normative Regel, sechsmal geschrieben. Die sechs Fassungen divergieren heute nicht.
Genau das war der Zustand vor D147 und vor D175.

**Der Ort.** `mensch_als_republik/predicates.py`, kein neues Modul. Zwei Messungen tragen das:
dort stehen `is_core_predicate` und `is_nuc_predicate` bereits in derselben Form, und
`parse_predicate` wird in allen sechs Dateien **ausschließlich** von `_is_nuc_name` gebraucht —
die sechs Importe fallen mit weg.

**Das Verhalten bleibt.** Der Rumpf fängt `Exception`, nicht `VerifierError`, und das bleibt so.
Ein Claim aus `claim_from_map`, dessen `p` kein `str` ist, gilt damit weiterhin als nicht passend,
statt eine Ausnahme durch den Aufrufer zu tragen — die sichere Richtung. Eine Angleichung an
`is_nuc_predicate` wäre eine Verhaltensänderung und ist ausdrücklich **nicht** Teil dieses Laufs.

**Offen.** `is_nuc_predicate` und `is_core_predicate` fangen `VerifierError`, `is_nuc_name` fängt
`Exception`: drei Funktionen nebeneinander, zwei Fangbreiten. Das gehört auf die offene Liste.

### D182 — `ruff` unter `dev`, mit genau zwei Regeln: F401 und F811

**Der Anlass.** Der Lauf `00e-benennung` hat in `profiles/membership.py` einen toten Import
hinterlassen: `Claim` kam dort genau zweimal vor, im Import und in der Signatur der entfernten
Funktion. Kein Test fängt das, `make check` hatte keinen Linter, und gefunden wurde es allein
durch das Lesen des Diffs. Diese Fehlerklasse wächst mit jedem Refactoring, und sie ist die
einzige bisher gefundene, die eine Maschine zuverlässiger sieht als der Supervisor.

**Die Entscheidung.** `ruff` kommt unter `[project.optional-dependencies] dev`, mit einer
ausdrücklich benannten Regelmenge: **F401** (ungenutzter Import) und **F811** (Redefinition eines
ungenutzten Namens). `make check` bekommt ein Ziel `check-lint` und ruft es mit auf.

**Warum nur zwei Regeln.** Ein Formatter oder eine breite Stilmenge trüge Formatierung in jeden
künftigen Diff und verteuerte die Abnahmen — Abnahme heißt hier Lesen, und gelesen wird
schlechter, wenn Rauschen danebensteht. `E501` bleibt ausdrücklich aus: die 100 Zeichen sind
Konvention, kein Tor, und `check_specs.py` prüft sie aus demselben Grund nicht.

**Der Preis, benannt.** Das ist die erste Abhängigkeit, die nicht aus dem Protokoll folgt, und sie
ist eine Rust-Binärdistribution. Sie steht unter `dev`, nie unter `dependencies`; wer die
Bibliothek benutzt, zieht sie nicht mit. Die geprüfte Alternative — ein eigenes
`tools/check_unused.py` über `ast` — wurde verworfen: selbst gewarteter Prüfcode kann selbst
falsch sein, und dann prüft niemand den Prüfer.

**Die Messung vor der Entscheidung.** `ruff check --select F401,F811` gegen `d75a499` liefert
**16 Funde**, alle in `tests/` und `tools/`, keinen einzigen in `mensch_als_republik/`. Fünf davon
sahen nach pytest-Fixtures aus, was ein bekannter Falschbefund dieser Regel ist — sie sind es
nicht: `fresh_alice` und die vier Nachbarn tragen kein `@pytest.fixture`, sind gewöhnliche
Funktionen und wirklich ungenutzt. Die `__init__.py` der Unterpakete führen `__all__` und lösen
deshalb nichts aus. Ohne diese Messung wäre die Regelmenge blind gewählt worden.

### D183 — `resolve_state`: die Fassade über Kette, Policy und Schlüssel

**Was sie tut.** `resolve_state` in `mensch_als_republik/resolve.py` nimmt Speicher, Scope, Genesis
und die beiden Objektabbildungen, ruft `resolve_epoch`, leitet daraus die Policy der **geltenden**
Epoche her und löst damit die Autoritätsliste auf. Sie hört vor `membership` auf — soviel, wie ein
Node beim Empfang eines fremden Claims braucht (D180), keinen Schritt mehr.

**Der Rückgabetyp trägt die Invariante.** `NucleusState` hält Epoche, Verfassungsobjekt, Policy und
`authorized_keys` — und die Zusage, dass alle vier aus derselben aufgelösten Kette stammen. Diese
Zusage trägt heute niemand: wer die Aufrufe selbst verkettet, kann `constitution_hash` aus dem
Genesis nehmen und rechnet dann unter der Verfassung der ersten Epoche weiter. Ob das auffällt oder
still bleibt, hängt davon ab, ob er `constitution_obj` mitgibt — **berichtigt in D184**. Das
Vorbild ist `TrustedMetadataSet` aus `python-tuf` — ein Typ, dessen Inhalt per Konstruktion
konsistent ist, mit einem angeleiteten Weg darüber.

**Sie entscheidet nichts (D172).** Ersetzt man jeden Zwischenwert durch den, den der jeweilige
Primitivaufruf ohnehin liefert, ist das Ergebnis byte-gleich. Die Fassade ist Benennung, kein
Mechanismus; das Aufnahmekriterium aus `08 §3` ist auf sie deshalb nicht anwendbar. Setzte sie
irgendwo eine Vorgabe — eine Policy, eine Reihenfolge, eine Schwelle —, verteilte sie Macht und
gehörte nicht hierher.

**Die Primitive bleiben.** `resolve_epoch`, `resolve_policy`, `resolve_authorized_keys` und
`membership` behalten ihre expliziten Parameter, ohne Default, der still eine Kette unterstellt;
`membership` behält insbesondere `authorized_keys` (D161). Die Fassade ist ein Angebot neben den
Primitiven und zugleich der einzige empfohlene Weg.

**Vermerke bleiben getrennt.** Die drei Aufrufe liefern drei verschiedene `Finding`-Typen:
`GovernanceFinding`, `NucleusFinding`, `ProfileFinding`. `NucleusState` führt sie in drei Feldern,
nicht in einem Strom. Die Herkunft ist Information — `EPOCH_FORK` und ein Vermerk zum
`constitution_hash` verlangen Verschiedenes vom Aufrufer. Ein vereinheitlichter Vermerkstyp würde
`00`, `03` und `04` aneinander koppeln, ohne dass die Spec das verlangt. Der Preis ist benannt: der
Aufrufer trägt drei Listen statt einer.

**Offen, nicht in diesem Lauf.** Vier `Finding`-Klassen — in `findings.py`, `governance/`,
`profiles/` und `trust/` — sind strukturell identisch und unterscheiden sich nur im `kind`-Enum;
`dedupe_sort` steht dreimal mit gleicher Signatur daneben. Derselbe Befund wie D181, aber über vier
Schichten. Er braucht eine eigene Entscheidung.

### D184 — Abnahme `00f`: die Fassade steht; eine Begründung war zu breit

**Was gebaut wurde.** `mensch_als_republik/resolve.py` mit `resolve_state` und `NucleusState`, 73
Zeilen, dazu 145 Zeilen Tests in `tests/test_resolve.py`. 567 Tests. Die Fassade enthält **null**
Verzweigungen. Das war das schärfste Abnahmekriterium des Laufs, weil eine Fassade, die verzweigt,
entscheidet — und dann trüge die Substitutionsprobe aus D172 nicht mehr.

**Die Berichtigung.** D183 begründete die Fassade damit, dass ein Aufrufer, der
`constitution_hash` aus dem Genesis nimmt, still die Policy der ersten Epoche bekomme. Die
Rücknahmeprobe hat das widerlegt: in der Prüfwelt sind die Policies von `C1` und `C3` byte-gleich,
und der Fehlgriff fliegt als `ValueError` auf, weil `constitution_obj` nicht zum Hash passt. Still
wird er nur, wenn der Aufrufer `constitution_obj` weglässt — dann fehlt das Gegenstück, an dem der
Widerspruch auffiele. Die Begründung war an einen Fehlermodus gebunden und hat beim Aufschreiben
Umfang gewonnen, den sie nicht hat. Dasselbe Muster wie D77, D83, D130 und D172.

Die Entscheidung selbst trägt weiter: die Verkettung stand an zwei Stellen, und die Invariante
„alle vier Werte stammen aus derselben Kette" trug niemand. Überzeichnet war allein die
Dringlichkeit.

**Zwei Vorbehalte an den Tests.** `test_resolve_state_authorized_keys_match_direct` übergibt
`policy=state.policy` an den Vergleichsaufruf und prüft damit, dass bei gleicher Policy dasselbe
herauskommt — nicht, dass die Fassade die richtige weiterreicht; diese Aussage trägt allein
`test_resolve_state_policy_from_current_constitution`. Und `policy_findings` ist von keinem Test
berührt: Test 4 prüft zwei der drei Vermerklisten, und die zweite Rücknahmeprobe tauschte
entsprechend nur `epoch_findings` gegen `key_findings`. Ein Vertauschen mit `policy_findings`
bliebe unbemerkt. Beides notiert, nicht blockierend.

**Die Zählung dieser Sitzung.** Drei Defekte, davon einer beim Werkzeug: ein toter `Claim`-Import
in `profiles/membership.py`, den weder ein Test noch ein Kriterium des Prompts gesehen hätte. Er
hat D182 ausgelöst; seither prüft `make check` diese Klasse mit. Die anderen beiden lagen beim
Supervisor — ein Grep-Kriterium, das Namen vorschrieb statt Zustände zu messen, und die
überzeichnete Begründung oben. Dazu eine Untermessung in der Übergabe `00e`, die `_is_nuc_name` als
Einzelfall führte, wo sechs Kopien standen.

### D185 — Berichtigung an D184: der Fassadentest war nicht zirkulär, sondern reglos

**Der Vorbehalt war zu eng gefasst.** D184 notierte, dass
`test_resolve_state_authorized_keys_match_direct` mit `policy=state.policy` in den
Vergleichsaufruf geht und damit nur prüfe, dass gleiche Policy gleiches Ergebnis liefert. Die
Nachmessung zeigt mehr: keine der drei Verfassungen der Prüfwelt — `C1`, `C2`, `C3` in
`tests/governance/fixtures.py` — führt `nucleus_keys`, und ihre `irrevocable_predicates` stehen
alle drei auf dem Default aus `_constitution()`. Der Anker ist deshalb in jedem Fall
`genesis_obj[1]`, ein einziger Schlüssel, und die drei Policies sind byte-gleich. Der
Vergleichsaufruf liefert unter der **falschen** Verfassung dasselbe Ergebnis wie unter der
richtigen. Der Test war also nicht nur zirkulär gebaut; seine Behauptung ist in dieser Welt für
jede beliebige Verfassung wahr. Kein Umbau des Vergleichsaufrufs ändert daran etwas.

**Was `policy` auf diesem Pfad überhaupt bewegen kann.** `resolve_authorized_keys` reicht die
Policy allein an `classify_all` weiter. `rotate-key@1` und `rotate-ack@1` liegen in
`PROTOCOL_IRREVOCABLE` und werden in `NucleusPolicy.__post_init__` weder von `TRUST_GRANTING` noch
von den core-Einträgen abgezogen; sie können `policy.irrevocable` also nie verlassen. Widerrufe
gegen Rotationsclaims greifen unabhängig von der Policy nie. Der einzige verbliebene Hebel ist
`EQUIVOCATION_FLAGGED`: `resolve_current_key` prüft ihn über **alle** Claims mit
`claim.I == k_cur`, nicht nur über Rotationen. Ob eine Policy diesen Zustand für einen anderen
Claim desselben Autors bewegen kann, ist **nicht gemessen** und hier nicht entschieden.

**Was dieser Lauf ändert.** Erstens: der Vergleichsaufruf leitet seine Policy unabhängig aus `C3`
her statt sie aus `state` zu entnehmen — die Zirkularität fällt weg, auch wenn sie in dieser Welt
folgenlos ist. Zweitens trägt der Test den Namen seiner Aussage; die stärkere Aussage trägt er
nicht und behauptet sie nicht mehr. Drittens bekommt `policy_findings` einen Test.

**Die Prüflage für `policy_findings`.** Derselbe Speicher, aber `C1` fehlt in
`known_constitutions`. Dann hält die Kette bei `EPOCH_1`, `constitution_obj` ist `None`, und alle
drei Vermerklisten sind besetzt: `epoch_findings` mit `TALLY_UNEVALUABLE`, `policy_findings` mit
`ProfileFinding.CONSTITUTION_UNAVAILABLE` auf `CONSTITUTION_HASH_1`, `key_findings` mit
`NucleusFinding.CONSTITUTION_UNAVAILABLE` auf demselben Subjekt. Die beiden letzten sind
inhaltsgleich und trotzdem unterscheidbar, weil es zwei verschiedene Dataclasses aus zwei Modulen
sind: Gleichheit zwischen ihnen ist falsch. Ein Vertauschen der beiden Felder in `resolve_state`
wird damit rot — vorab gemessen, nicht angenommen (Prüfregel 28).

**Warum die Welt nicht in diesem Lauf ersetzt wird.** Siehe D186.

### D186 — Zurückgestellt: eine Kettenwelt, in der die Verfassung den Schlüsselsatz bewegt

**Was fehlt.** Es gibt im Baum keine Prüflage, in der zwei aufeinanderfolgende Epochen
verschiedene `authorized_keys` haben. `tests/nucleus/test_anchor.py` prüft `nucleus_keys`
gründlich, aber ohne Epochenkette; `tests/governance/fixtures.py` hat die Kette, aber Verfassungen
ohne `nucleus_keys`. Solange beides getrennt bleibt, ist die Zusage aus D183 — alle vier Werte
stammen aus derselben Kette — an der Stelle, an der sie am meisten wert wäre, nicht prüfbar.

**Warum die vorhandenen Fixtures gesperrt sind.** `CONSTITUTION_HASH_1` bis `3` sind über
`DOC_CONSTITUTION_HASH_1` bis `3` als Golden Anchors festgelegt, und `DOC_PROPOSAL_HASH_2` sowie
`DOC_EPOCH_ID_3` hängen daran. Ein `nucleus_keys` in `C1`, `C2` oder `C3` verschöbe sie alle.
Anker werden nicht nachgezogen, um einen Test zu ermöglichen. Die Welt müsste also neben der
bestehenden stehen, mit eigenem Genesis und eigenem Scope — und damit mit eigenen Claim-Bauern,
denn `vote` und `ratify_claim` in den Fixtures haben `N=N_D` fest verdrahtet.

**Warum jetzt nicht.** Der Ertrag dieser Welt liegt nicht bei den Fassadentests, sondern beim
Beispielnukleus: D169 hält fest, dass er Epoche-1- von Epoche-2-Policy nicht unterscheiden kann,
und `_member` in `tools/example_nucleus.py` bekommt `constitution_hash` und Verfassungsobjekt bis
heute von aussen. Wer die Welt baut, sollte sie dort bauen, wo sie gebraucht wird. Sie an einen
Aufräumlauf an `tests/test_resolve.py` zu hängen, wäre stiller Scope-Zuwachs an der falschen
Stelle.

**Die Bedingung.** Diese Entscheidung wird zusammen mit der Frage beantwortet, ob der
Beispielnukleus eine aufgelöste Kette bekommt — nicht davor und nicht getrennt.

### D187 — Abnahme `00h`: die zwei Vorbehalte aus D184 sind geschlossen

**Was gebaut wurde.** `tests/test_resolve.py` und `Makefile`, sonst nichts;
`mensch_als_republik/resolve.py` blieb unangetastet. 568 Tests. Der Vergleichsaufruf in
`test_resolve_state_authorized_keys_match_primitive_call` leitet seine Policy jetzt unabhängig
aus `C3` her, und `test_resolve_state_missing_c1_keeps_findings_separate` hält die drei
Vermerklisten auseinander. Damit sind beide Vorbehalte aus D184 erledigt. Gemergt als
Fast-Forward, `main` bei `056728f`.

**Die Reglosigkeitsprobe ist der Ertrag, nicht die Reparatur.** Probe B hat den direkten Aufruf
auf `CONSTITUTION_HASH_1` und `C1` gesetzt — die falsche Verfassung — und der Test blieb grün.
Damit ist die Aussage aus D185 nicht mehr nur eine Messung des Supervisors an einer Sondierwelt,
sondern eine geprüfte Eigenschaft des committeten Tests. Der Docstring, der die Schwäche benennt,
ist belegt und nicht behauptet. Das ist die Form, in der eine Reglosigkeit stehen bleiben darf:
benannt, gemessen, mit dem Ausweg in D186 verknüpft.

**Der Test sichert mehr als das Kriterium verlangte.** Der Auftrag hat `epoch_findings` nur auf
„nicht leer plus `kind` des ersten Eintrags“ festgelegt, weil das Subjekt eine `claim_id` ist.
Dadurch sind trotzdem alle drei Vertauschungen gefangen und nicht nur die eine aus Probe A: ein
Tausch von `epoch_findings` gegen `policy_findings` bricht die `kind`-Zusicherung und zusätzlich
die Gleichheit auf `policy_findings`, weil dort dann ein Vermerk aus `governance/findings.py`
stünde. Ein schwächeres Kriterium kann einen stärkeren Test ergeben, wenn es den Zustand
beschreibt statt die Form vorzuschreiben.

**Der Name kam vom Werkzeug.** `test_resolve_state_missing_c1_keeps_findings_separate` stand
nicht im Auftrag; das Werkzeug hat ihn gesetzt und gemeldet. Er beschreibt die Prüflage und nicht
das Kriterium — die Rückwirkung, aus der Prüfregel 29 entstand, ist hier nicht eingetreten.

**Die Zählung.** Kein Werkzeugdefekt. Ein Supervisorfehler: die Zeilenzahl des D185-Splice war mit
64 angegeben, `git diff --numstat` meldet 63. Die Messvorschrift zählte das leere Element vor dem
führenden Umbruch mit. Dieselbe Klasse wie die geschätzten Zeilenzahlen früherer Sitzungen, nur
diesmal in der Vorschrift selbst statt in der Schätzung.

### D188 — Der Beispielnukleus führt die Kette vor; D186 bleibt gebunden

**Die Messung zuerst.** `resolve_state` läuft gegen den Beispielnukleus, ohne dass dort etwas
geändert werden müsste: Speicher aus `claim_set`, `known_constitutions` aus `constitution_gov` und
`constitution_2`, `known_proposals` aus `ex.proposal`. Ergebnis `epoch_2`, alle drei
Vermerklisten leer. Die Kette trägt also heute schon, es fehlt allein der Aufruf. Gemessen wurde
weiter: die beiden Verfassungen unterscheiden sich in **genau einem** Feld, `participants`.
`irrevocable_predicates`, `thresholds` und `arbitration` sind gleich.

**Damit ist D169 beantwortet, und zwar negativ.** `resolve_state` löst nicht auf, dass der
Beispielnukleus Epoche-1- von Epoche-2-Policy nicht unterscheiden kann — es verschiebt den Befund.
Policy und Schlüsselsatz sind über beide Epochen byte-gleich, aus demselben Grund wie in den
Governance-Fixtures (D185). Was die Kette hier bewegt, ist `participants`, und das wirkt erst in
`membership`, also hinter der Stelle, an der die Fassade nach D183 aufhört.

**Die Entscheidung.** Der Beispielnukleus bekommt eine zusätzliche Prüfung, die den Zustand
ableitet statt ihn vorauszusetzen. Sie tritt neben die bestehenden Prüfungen; keine von ihnen
wird umgestellt. `_member` bedient Epoche 1 und Epoche 2 mit derselben Funktion, und
`check_membership_epoch1` braucht ausdrücklich die Verfassung, die **nicht** die geltende ist;
`check_anchor_resolution` hält absichtlich verschiedene Verfassungen gegeneinander. Eine halbe
Umstellung erzeugte Asymmetrie ohne Gewinn und entwertete eine bestehende Prüfung.

**Was die Prüfung trägt und was nicht.** Epochenscharf sind allein zwei Zusicherungen: dass der
abgeleitete Zustand `epoch_2` ist und dass sein Verfassungsobjekt `constitution_2` ist. Der
Vergleich der Policy und des Schlüsselsatzes ist **reglos** — beide Werte stimmen auch unter der
Verfassung der ersten Epoche, und der Anker ist in jedem Fall `genesis_gov[1]`. Diese beiden
Vergleiche stehen deshalb nicht als Epochenprüfung da, sondern als Substitutionsprobe im Sinne von
D172: die Fassade liefert byte-gleich das, was die Primitivaufrufe liefern. So benannt sind sie
ehrlich; unbenannt wären sie derselbe Fehler wie der Vorbehalt aus D184.

**Der Ertrag.** D183 und D187 halten fest, dass die Fassade keinen Träger hat. Mit dieser Prüfung
hat sie ihren ersten Aufrufer ausserhalb der Tests. Der Beispielnukleus bleibt dabei, was er ist:
eine Vorführung, kein Node. D180 gilt unverändert — kein Pfad, kein Socket, kein Daemon.

**D186 bleibt gebunden.** Die zurückgestellte Frage ist nicht, ob eine Prüfung die Kette
vorführt, sondern ob die Verfassungen so gebaut werden, dass die Kette Policy oder Schlüsselsatz
wirklich bewegt. Das verschöbe `constitution_hash_2`, den `proposal_hash` und `epoch_id_2`, die
alle in `example-nucleus.md` stehen. Es ist ein Spec-Nachzug mit eigener Golden-Number-Rechnung
und keine Zugabe zu einem Prüfungslauf.

### D189 — Abnahme `00i`: die Fassade hat einen Träger

**Was gebaut wurde.** `check_resolved_chain` in `tools/example_nucleus.py`, eingehängt in
`verify_all` nach `check_ratification`, dazu ein Test nach dem Modulmuster. 569 Tests. Der Diff
ist rein additiv — 53 und 5 eingefügte Zeilen, **keine** gelöschte —, womit auch mechanisch belegt
ist, dass keine der bestehenden Prüfungen angefasst wurde. Gemergt als Fast-Forward, `main` bei
`68807ed`.

**Der Befund aus D183 und D187 ist geschlossen.** `resolve_state` hatte bis hierher keinen
Aufrufer ausserhalb der Tests. Jetzt steht einer in einem Werkzeug und nicht in der Bibliothek —
die Richtung, die D180 vorschreibt. Die Fassade wird damit von etwas benutzt, das ihr Ergebnis
gegen unabhängig gerechnete Werte hält, nicht nur von einem Test, der sie beschreibt.

**Die Substitutionsprobe ist nicht zirkulär gebaut.** Die Policy entsteht aus
`_policy(ex, constitution_hash_2, constitution_2)`, wird gegen `state.policy` geprüft und erst
danach in den direkten Schlüsselaufruf gereicht. Der Vergleichswert steht also fest, bevor er
benutzt wird. Genau diese Reihenfolge musste in `00h` an `tests/test_resolve.py` erst nachgezogen
werden; hier stand sie von Anfang an richtig.

**Probe A hat schärfer getroffen als vorhergesagt.** Der Auftrag hat mit einem `AssertionError`
gerechnet. Gefallen ist die **erste** Zusicherung, also die epochenscharfe, nicht eine der
reglosen. Die Probe hat damit nicht nur belegt, dass die Prüfung reagiert, sondern auch, dass sie
an der tragenden Stelle reagiert. `test_verify_all` fiel mit und bestätigt den Einhängepunkt.
Probe B blieb grün und bestätigt die Reglosigkeit aus D188 am gebauten Artefakt.

**Eine Beobachtung, keine Regel.** Zum zweiten Mal in Folge hat ein Auftrag einen Test verlangt,
ohne ihn zu benennen, und zum zweiten Mal hat das Werkzeug den Namen gesetzt und gemeldet statt
ihn stillschweigend zu wählen. Beide Namen waren richtig. Daraus folgt keine Prüfregel: die
Rückwirkung, vor der Prüfregel 29 warnt, entsteht aus Namen in **Messkriterien**, nicht aus Namen
in Aufträgen. Eine Regel gegen ein Verhalten, das zweimal folgenlos blieb, wäre Zeremonie.

**Neu offen.** `example-nucleus.md` hat für diese Prüfung keinen Abschnitt. Der Docstring verweist
deshalb auf das Register statt auf einen Paragraphen. Das ist so gewollt und in diesem Lauf
ausdrücklich Nicht-Ziel gewesen, aber es ist eine Lücke und gehört zum Spec-Nachzug, der ohnehin
für D186 ansteht.

**Die Zählung.** Kein Werkzeugdefekt, kein Supervisorfehler in diesem Lauf.

### D190 — D186 beantwortet: die Welt entsteht in `tests/`, nach dem Vorbild des RepositorySimulator

**Was D186 offenliess.** Ob die Kettenwelt, in der die Verfassung Policy oder Schlüsselsatz
bewegt, im Beispielnukleus oder in den Tests entsteht. D188 hat die Vorfrage beantwortet — der
Beispielnukleus führt die Kette vor, ohne umgestellt zu werden —, damit ist diese hier fällig.

**Der Beispielnukleus scheidet aus, und zwar aus einem gemessenen Grund.** `threshold_class`
liefert `membership` nur, wenn beide Verfassungsobjekte ausserhalb von `participants` byte-gleich
sind; jede andere Änderung fällt auf `genesis_gov[5]`, und das ist `2`, also `amendment`. `build()`
prüft `klass == "membership"` und wirft sonst. Der eine Übergang des Beispielnukleus **ist** die
Aufnahme Doras. Policy oder Anker liessen sich dort nur unterbringen, indem man aus der Aufnahme
ein Amendment macht oder eine dritte Epoche anhängt. Beides ändert, was die Vorführung vorführt.
Die Arithmetik bliebe unbeeindruckt — alle drei Schwellen stehen dort auf `[1, 2]` —, die
Kollision ist erzählerisch und normativ, nicht rechnerisch.

**Berichtigung an D186.** Dort steht, `vote` und `ratify_claim` in den Fixtures hätten `N=N_D`
fest verdrahtet. Für `vote` ist das falsch: die Funktion nimmt seit jeher ein optionales
`scope`-Argument. Fest verdrahtet sind nur `ratify_claim` und `propose_claim`. Die Behauptung war
beim Aufschreiben nicht nachgemessen. Dieselbe Klasse wie die Fehler aus `00e`, diesmal im
eigenen Register.

**Die Welt ist billiger als angenommen.** Gemessen an einer Sondierwelt: Genesis mit einem
`root_key`, zwei Verfassungen, deren zweite `nucleus_keys` führt, ein `propose`, drei `vote`, ein
`ratify`. `resolve_state` löst auf Epoche 2 auf, alle drei Vermerklisten leer, und
`authorized_keys` ist der in der zweiten Verfassung benannte Schlüssel — **nicht** der Wurzel-
schlüssel aus dem Genesis. Damit ist die Zusage aus D183 zum ersten Mal prüfbar: die vier Werte
stammen nachweislich aus derselben Kette, weil ein Fehlgriff in der Epoche einen anderen
Schlüsselsatz ergäbe. Rund zwanzig Zeilen Aufbau, keine neuen Claim-Bauer.

**Das Vorbild ist dasselbe wie in D183.** `python-tuf` hält seine Prüfwelten nicht als
festgeschriebene Dateien, sondern in einem `RepositorySimulator`: ein Aufbau im Speicher, der
Metadatenstände auf Zuruf erzeugt, mit Hilfsmethoden für Schlüsselwechsel und Veröffentlichung,
ohne Dateizugriff und ohne Netz. Nichts darin ist von Hand festgeschrieben; die Tests behaupten
Beziehungen, keine Literale. Übernommen wird die Form, nicht der Umfang: MaR braucht keinen
Simulator, sondern einen Kettenbauer, der aus einer Liste von Verfassungen einen Speicher, ein
Genesis, die beiden Objektabbildungen und die Epochen liefert.

**Beide Arten von Prüfdaten bleiben nebeneinander stehen.** `tests/governance/fixtures.py` ist
über die `DOC_*`-Anker an das Spec-Dokument gebunden und wird deshalb **nicht** angefasst; der
Bauer bedient das Verhalten. `python-tuf` hält dieselbe Trennung — festgeschriebene Daten für die
Übereinstimmung mit der Spezifikation, ein Aufbau im Speicher für das Verhalten. Die Duplikation
ist damit begründet und nicht bloss geduldet; der Einwand aus D181 gegen strukturgleiche Kopien
zielt auf Produktivcode ohne Grund, nicht auf zwei Prüfschichten mit verschiedenen Aufgaben.

**Die Prüffälle kommen aus der Literatur, nicht aus der Fantasie.** Zwei Befunde aus `python-tuf`
haben in MaR ein Gegenstück und gehören in die Reihe, sobald der Bauer steht:

- Eine unbrauchbare Zwischenversion sperrt alle späteren gültigen (`python-tuf` Nr. 2669). In MaR:
  eine Verfassung, die mitten in der Kette in `known_constitutions` fehlt.
- Der neueste Stand ist mit Schlüsseln signiert, die zu Beginn nicht bekannt waren
  (`python-tuf` Nr. 885). In MaR: eine Epoche, deren `nucleus_keys` erst den Schlüssel
  autorisieren, der den nächsten Übergang trägt.

**Zuschnitt des ersten Laufs.** Der Bauer und **eine** Welt, in der der Schlüsselsatz sich
zwischen Epoche 1 und Epoche 2 bewegt, dazu die Tests, die das festhalten. Die beiden Fälle oben
sind benannt und folgen danach, nicht in demselben Lauf.

### D191 — Abnahme `00j`: die Reglosigkeit ist nicht mehr behauptet, sondern vorgeführt

**Was gebaut wurde.** `tests/kettenwelt.py` und `tests/test_kettenwelt.py`, zusammen 205 Zeilen,
beide neu. Ein Bauer, der aus Identitäten, Wurzelschlüsseln und einer Folge von Verfassungen eine
Kette baut, und eine Welt, deren zweite Verfassung `nucleus_keys` führt. 571 Tests. Gemergt als
Fast-Forward über zwei Commits, `main` bei `dbe4f9a`.

**Die Probe ist das Ergebnis, nicht der Test.** Probe A hat in `resolve_state` die Verfassung der
geltenden Epoche gegen die des Genesis getauscht — den Fehlgriff also, gegen den D183 den Typ
`NucleusState` stellt. Der neue Test wurde rot; **alle** Tests in `tests/test_resolve.py` und
`tests/test_example_nucleus.py` blieben grün. Damit ist zweierlei am Artefakt belegt statt
behauptet: die Zusage aus D183 ist zum ersten Mal prüfbar, und die Reglosigkeit der übrigen
Prüfwelten, die D185 und D188 nur gemessen hatten, ist vorgeführt. Eine Probe, die genau eine von
drei Prüfschichten trifft, sagt mehr über die anderen zwei als jede Zusicherung darin.

**Der Prompt schrieb einen unmöglichen Weltzustand vor.** Die Feldliste für die beiden
Verfassungen nannte Schwellen, Schlichter, `participants` und `nucleus_keys` — und ließ
`irrevocable_predicates` weg. Ohne `vote@1` liefert `decide` den Vermerk `VOTE_REVOCABLE` und
Zustand `UNEVALUABLE`, ohne `ratify@1` entsprechend `RATIFY_REVOCABLE`; nachgemessen ist jeder
der beiden für sich zu wenig. Das steht seit langem in `04 §3.5`, als `GV-27` und `GV-31` in
`04-golden-anchors.md` und im Fließtext von `example-nucleus.md`. Die Sondierwelt der Designrunde
hatte beide Einträge; verloren gingen sie beim Abschreiben in den Prompt. Das Werkzeug hat es
bemerkt, richtig ergänzt und gemeldet. Daraus die Schärfung von Prüfregel 28 — keine neue Regel,
weil die alte den Fall schon meint und nur an der falschen Stelle endete.

**Drei Abnahmedefekte, keiner davon durch Test oder Kriterium gefallen.** Erstens war `now` ein
toter Parameter: er stand in der Signatur und kam im Rumpf nicht vor, während die Tests zweimal
`1000` als Literal tippten. Zweitens lief der Vergleichsaufruf ohne `policy`, womit sich die
beiden verglichenen Aufrufe in zwei Dingen unterschieden und der Test den Unterschied einem davon
zuschrieb — dieselbe Klasse wie der Vorbehalt aus D184, folgenlos gemessen, aber die Aussage wird
erst mit der Behebung eindeutig. Drittens war die Vorbedingung ungeschrieben, dass
`identitaeten[0]` unter der jeweils geltenden Epoche autorisiert sein muss; ist sie es nicht, baut
der Bauer stillschweigend eine Kette, die nicht vorrückt. Alle drei auf demselben Branch behoben.

**Offen, als Messung und nicht als Regel.** `ruff` kennt mit `ARG` eine Regelgruppe für
ungenutzte Argumente, die den ersten Defekt maschinell gefangen hätte. D182 hat den Linter
bewusst auf F401 und F811 festgelegt, und eine dritte Gruppe braucht denselben Nachweis wie die
ersten beiden: erst die Zahl der Funde im Baum messen, dann entscheiden. Vorher ist es eine
Vermutung.

### D192 — Der Vorlaufbefund zur dreiepochigen Ratifizierung war eine verunreinigte Welt

**Was behauptet war.** `sitzungsstart-00k.md` führte als ersten offenen Punkt einen möglichen
Produktivbefund: in einer Welt mit drei Verfassungen halte die Kette bei Epoche 1 mit zwei
`UNSUPPORTED_RATIFICATION`, sobald B statt A den zweiten Übergang ratifiziert — und es falle auch
der erste Übergang, obwohl sich die beiden Welten nur im Autor eines Claims aus dem zweiten
unterschieden. Dazu ein ungeklärter Widerspruch: der Subjektabgleich löste die Vermerke auf
`vote@1`-Claims auf, während `_unsupported` in `governance/epoch.py` `claim_id(ratify)` als
Subjekt setzt.

**Der Widerspruch ist keiner.** `verify_ratification` hat zwei Ausgänge mit demselben Vermerk.
`_unsupported` setzt `claim_id(ratify)`; die Schleife über die zitierten Stimmen setzt
`subject=cid` der **Stimme**, im Zweig `cid not in tally.yes`. Beide Lesarten sind richtig, sie
gehören zu verschiedenen Pfaden. Ein Stimm-Subjekt bedeutet nicht „die Ratifizierung trägt
nicht", sondern „diese zitierte Stimme liegt im Speicher und zählt nicht mit".

**Die Ursache liegt im Bau, nicht im Code.** `Identity` in `tests/helpers.py` ist eine
fortlaufende Autorenkette; ihr Docstring sagt es: jeder Aufruf hängt an, `h_prev` wird intern
fortgeführt. Die zweite Welt wurde aus denselben `Identity`-Objekten gebaut wie die erste. Ihre
Claims zeigten auf Vorgänger, die in ihrem eigenen Speicher nicht liegen; die Stimmen waren damit
nicht `ACTIVE`, fielen aus `tally.yes` und lösten in der Zitatschleife je Stimme einen Vermerk
aus. Dass auch der erste Übergang fiel, hat keinen Grund in einer Fernwirkung des zweiten: die
Verunreinigung begann schon bei den Stimmen des ersten.

**Gemessen.** Mit frischen Identitäten je Welt ist die Nachbildung des Bauers mit A als
Ratifizierer beider Übergänge claim-ID-genau der Bauer und löst auf Epoche 3 auf, alle drei
Vermerklisten leer. Ratifiziert B den zweiten Übergang, ebenfalls Epoche 3 ohne Vermerke.
Dieselbe Nachbildung mit wiederverwendeten Identitäten liefert Epoche 1 mit zwei
`UNSUPPORTED_RATIFICATION`, und zwar unabhängig davon, wer ratifiziert. Der Ratifizierer war nie
die Ursache.

**Folge.** Kein Produktivdefekt, keine richtige Sperre, kein Auftrag. Daraus Prüfregel 30: eine
Variantenwelt wird zuerst mit unverändertem Feld gebaut und gegen die Referenzwelt nachgewiesen.

### D193 — Berichtigung an D191: die Vorbedingung des Kettenbauers trifft nicht zu

D191 verzeichnet als dritten Abnahmedefekt von `00j`, es sei ungeschrieben geblieben, dass
`identitaeten[0]` unter der jeweils geltenden Epoche autorisiert sein müsse, weil der Bauer sonst
stillschweigend eine Kette baue, die nicht vorrückt. Behoben wurde der Defekt, indem genau diese
Zusage in den Docstring von `kettenwelt()` geschrieben wurde. Die Zusage ist falsch.

**Gemessen.** In einer Welt mit drei Verfassungen, deren zweite `nucleus_keys` auf B und deren
dritte auf C setzt, sind die autorisierten Schlüssel je Epoche `{A}`, `{B}` und `{C}`. A ist Autor
jedes `propose` und jedes `ratify` und ab Epoche 2 nicht mehr autorisiert — die Kette erreicht
dennoch Epoche 3, ohne einen einzigen Vermerk.

**Was stattdessen trägt, ist Teilnehmerschaft.** `04 §4.1` verlangt `ratify.I` als Element von
`P`, und `decide` vermerkt eine Stimme von außerhalb als `NON_MEMBER_VOTE`. Wird A aus
`participants` der zweiten Verfassung genommen und sonst nichts verändert, hält die Kette bei
Epoche 2 mit einem `UNSUPPORTED_RATIFICATION`. Der Docstring wird entsprechend berichtigt: der
Autor muss Teilnehmer der jeweils geltenden Verfassung sein, autorisiert muss er nicht sein.

**Die Klasse.** Eine Zusage, die einmal geschrieben und nie nachgemessen wurde, ist eine
Verbindlichkeit — hier eine, die im selben Zug entstanden ist, in dem ein Defekt behoben wurde.
Prüfregel 25 zielt auf Begründungen; dies ist ihr Gegenstück für Vorbedingungen.

### D194 — Die Auszählung weiß, was fehlt; die Ratifizierung gibt es weiter

**Der Befund.** Fehlt einem Beobachter eine Verfassung mitten in der Kette, liefert `decide` den
Zustand `UNEVALUABLE` und genau einen Vermerk, der benennt, was fehlt — etwa
`PROPOSAL_CONSTITUTION_UNAVAILABLE` mit dem Hash der fehlenden Verfassung als Subjekt.
`verify_ratification` verwirft diesen Vermerk und setzt an seine Stelle `TALLY_UNEVALUABLE` auf
dem `ratify`. `04 §4.1` begründet seine beiden Vermerke ausdrücklich damit, dass der Beobachter im
einen Fall weiß, welche `claim_id` er holen muss, und im anderen weiß, dass Holen nichts nützt.
Hier ist die zweite Auskunft unwahr: die fehlende Verfassung zu holen behebt alles.

**Die Literatur.** RFC 8914 (Extended DNS Errors, 2020) beschreibt denselben Fehler im Großen.
DNS hat mit SERVFAIL ein einziges grobes Signal für viele verschiedene Lagen; Anwendungen müssen
raten, und der übliche Ausweg ist der nächste Resolver — der entweder wieder scheitert oder, falls
er nicht validiert, ein potenziell schädliches Ergebnis liefert. Die Lösung ist ein getrenntes,
additives Feld: der Info-Code steht neben dem RCODE, verändert dessen Verarbeitung nicht und darf
sie nach den Security Considerations auch nicht verändern; mehrere Einträge sind zugelassen.
Diagnose informiert, sie steuert nicht. Genau diese Trennung wird hier übernommen.

**Die Entscheidung.** `verify_ratification` gibt im Zweig `tally.state is UNEVALUABLE` die
Vermerke der Auszählung zusätzlich weiter, als `dedupe_sort` über `TALLY_UNEVALUABLE` auf
`claim_id(ratify)` und die Einträge aus `tally.findings`. `TALLY_UNEVALUABLE` bleibt unverändert
stehen, `next_epoch` bleibt `None` in genau denselben Fällen, die Kettenauflösung wird nicht
angefasst. `_unevaluable` in `governance/tally.py` baut an seiner einzigen Stelle genau einen
Vermerk; die Zahl der Vermerke steigt also um genau eins.

**Was das kostet.** Erstens wird der Subjektraum sichtbar untypisiert: `epoch_findings` führt dann
eine `claim_id` und einen Verfassungshash nebeneinander. Das ist schon heute so, fällt aber erst
an der Fassade auf, und es hängt an dem mit D173 offenen Punkt, dass `00` die Form seiner Vermerke
nirgends festhält. Zweitens ändern sich drei Tests, alle gemessen:
`test_chain_missing_c3_stops_at_epoch_2` und `test_chain_miskeyed_c3_stops_at_epoch_1` vergleichen
exakt und bekommen einen Vermerk mehr, `test_resolve_state_missing_c1_keeps_findings_separate`
greift auf `epoch_findings[0]` einer sortierten Folge zu und behauptet damit eine Position statt
einer Aussage.

**Der Schnitt ist eng, und das ist eine Entscheidung.** Weitergegeben wird nur bei `UNEVALUABLE`.
Scheitert die Ratifizierung auf einer auswertbaren Auszählung, etwa weil Stimmen als
`NON_MEMBER_VOTE` ausgefallen sind, bleibt der Beobachter weiter ohne Adresse. RFC 8914 lässt sein
Feld ausdrücklich auch bei fehlerfreien Antworten zu; die Literatur zielt also auf die breite
Fassung. Sie bleibt hier offen und wird nicht stillschweigend mitgenommen.

### D195 — Eine fehlende Zwischenverfassung sperrt die Kette, in MaR aber nicht aus Politik

**Die Prüfwelt.** Drei Verfassungen, sonst feldgleich: C1 ohne `nucleus_keys`, C2 mit `[B]`, C3
mit `[C]`, `irrevocable_predicates` überall mit `vote@1` und `ratify@1`. Bekannt sind C1 und C3,
C2 fehlt. Gemessen löst `resolve_state` auf `epochen[0]` auf, `constitution_obj` ist C1,
`authorized_keys` sind die Wurzelschlüssel aus `genesis_obj[1]`, `policy_findings` und
`key_findings` sind leer, und `epoch_findings` führt nach D194 zwei Einträge:
`PROPOSAL_CONSTITUTION_UNAVAILABLE` auf dem Hash von C2 und `TALLY_UNEVALUABLE` auf der
`claim_id` des ersten `ratify`. Beide Subjekte werden im Test abgeleitet, nicht getippt.

**Die Literatur, und wo MaR abweicht.** python-tuf 2669 beschreibt denselben Umriss: eine
fehlerhafte Root-Version N sperrt jede spätere gültige Version, weil der Client über alle neueren
Versionen läuft und bei jeder ungültigen abbricht — bis hin zu Fällen, in denen der Fehler für die
Sperre gar nicht einschlägig ist, etwa zehn gültige und ein ungültiger Schlüssel bei Schwelle
fünf. Die dort gestellte Frage lautet, ob ein Client überhaupt scheitern soll, wenn N ungültig und
N+1 gültig ist. In MaR ist diese Frage nicht offen: Epoche 2 auszuwerten verlangt das
Verfassungsobjekt von Epoche 2, und fehlt es, ist auch das Überspringen versperrt. Die Sperre ist
strukturell und keine Politik. Damit ist der Fall in MaR der schwächere: es gibt keine Wahl zu
treffen, sondern nur die Pflicht, die Adresse mitzuliefern — und die erfüllt D194.

### D196 — Abnahme `00k`: der Defekt lag im Kriterium, nicht im Lauf

**Was gebaut wurde.** Die Weitergabe der Auszählungsvermerke nach D194, der Prüffall nach D195 und
die Berichtigung des Kettenbauer-Docstrings nach D193. Gemessen mit `git diff --numstat` gegen den
Prompt-Commit `2a02104`: fünf Dateien, 91 eingefügte und 10 entfernte Zeilen. Der Produktivteil
ist zwei Zeilen gegen eine — `*tally.findings` in einer Liste, die es schon gab. 572 Tests.
Gemergt als Fast-Forward über zwei Commits, `main` bei `f6720b1`.

**Die Proben.** Probe A nahm die Weitergabe zurück: genau vier rote Tests, der neue und die drei
nachgezogenen, 568 grün. Probe B ließ die mittlere Verfassung in der Kopie stehen: genau ein roter
Test, der neue, 571 grün, und die Kette lief bis Epoche 3. Beide Mengen standen vorher im Prompt.
Prüfregel 23 verlangt, dass außer dem geprüften Test nichts anderes rot wird; wo vier Tests
zwangsläufig fallen, wird die Vierermenge selbst zum Kriterium, sonst wäre die Probe zweideutig
statt eindeutig. Der Supervisor hat den Lauf zusätzlich in einem eigenen Baum nachgebaut und beide
Proben unabhängig gefahren; sie reproduzieren.

**Der einzige Defekt war ein Abnahmekriterium.** Es nannte `32c55c9` als Vergleichspunkt, also den
Registercommit, während der Prompt auf `2a02104` liegt. Der Prompt ist selbst eine Datei im
Wurzelverzeichnis und erscheint deshalb im Diff gegen den Commit darunter; gemessen wurden sechs
Dateien statt der geforderten fünf. Das Werkzeug hat den Unterschied gemeldet, die Herkunft der
sechsten benannt und nichts nachgezogen. Gegen den richtigen Vergleichspunkt ist das Kriterium
erfüllt. Daraus Prüfregel 31: die Regel stand seit langem in der dauerhaften Anweisung und in
jedem Sitzungsstart, aber nicht in `pruefregeln.md` — und was dort nicht steht, wird beim
Schreiben eines Prompts nicht geprüft.

**Notiert, nicht behoben.** Der neue Test vergleicht `state.epoch_findings` gegen `dedupe_sort`
über eine handgebaute Liste. Für den Inhalt trägt das; für die Reihenfolge steht auf beiden Seiten
dieselbe Sortierfunktion, die Aussage über die Ordnung ist also zirkulär. Das ist der Hausstil von
`tests/governance/test_chain.py` und wurde hier nicht ausgenommen. Wer die Ordnung von
`dedupe_sort` je prüfen will, braucht dafür einen eigenen Ort.

### D197 — Die untaugliche Zwischenverfassung sperrt anders als die fehlende

**Der zweite Fall aus D190 ist einer, und ein anderer als angenommen.** Gedacht war er als „ein
Schlüssel, den erst die neue Epoche autorisiert"; D193 hat das erledigt, weil Autorisierung für
den Ratifizierer keine Rolle spielt. Gemessen an der Kettenwelt aus D195, jeweils nur C2
verändert:

| C2 | aufgelöste Epoche | Vermerk neben `TALLY_UNEVALUABLE` |
|---|---|---|
| fehlt ganz | 1 | `PROPOSAL_CONSTITUTION_UNAVAILABLE` auf H(C2) |
| ohne `participants` | 2 | `PARTICIPANTS_UNDECLARED` auf H(C2) |
| `participants` leer | 2 | `MALFORMED_PARTICIPANTS` auf H(C2) |
| ohne `vote@1` | 2 | `VOTE_REVOCABLE` auf H(C2) |
| Schwelle `[3, 2]` | 1 | `MALFORMED_THRESHOLD` auf H(C1) |

**Die fehlende Verfassung sperrt davor, die untaugliche danach.** `decide` prüft den Inhalt nur
der geltenden Verfassung; von der Zielverfassung werden Vorhandensein, Hash und Schwelle geprüft,
sonst nichts (`04 §3.5`). Eine Verfassung ohne `participants` ist damit ein zulässiges
Übergangsziel. Die Kette rückt in sie ein — und sie regiert: gemessen ist `constitution_obj` das
untaugliche C2, `authorized_keys` sind Bs Schlüssel, `policy_findings` und `key_findings` sind
leer. Der Nukleus steht in einer Epoche, in der nie wieder eine Entscheidung ausgewertet werden
kann, und nur die Epochenschicht weiß davon.

**Das ist das MaR-Gegenstück zu python-tuf 2669**, und ein schärferes als D195: dort ist die
Zwischenversion abwesend, hier ist sie vorhanden und unbrauchbar. Genau das beschreibt 2669 — eine
fehlerhafte Version N, die jede spätere gültige sperrt.

**Was hier entschieden wird und was nicht.** Entschieden ist der Prüffall: die Welt mit C2 ohne
`participants`, auf Kettenebene. Nicht entschieden ist, ob `decide` die Zielverfassung auf Inhalt
prüfen soll, bevor sie Übergangsziel wird. Das änderte, welche Epoche die Kette erreicht, und ist
keine kleine Runde; es bleibt als benannter Fork offen.

### D198 — Das Subjekt eines Auszählungsvermerks benennt das zurückgewiesene Objekt

**Der Befund.** `decide` hat zwölf `UNEVALUABLE`-Ausgänge; gemessen übergeben zehn davon
`epoch.constitution_hash` als Subjekt, gleich wo der Fehler sitzt. Dreimal ist das die falsche
Adresse. Bei `UNSUPPORTED_WEIGHT_MODE` und bei dem `MALFORMED_THRESHOLD` aus `genesis[5]` liegt
der Fehler im Genesis, nicht in einer Verfassung. Und die Schwellenprüfung, die `04 §3.5`
ausdrücklich in beiden Verfassungen verlangt, kann die Zielverfassung zurückweisen: eine Schwelle
`[3, 2]` in C2 ergibt gemessen `MALFORMED_THRESHOLD` auf dem Hash von C1, dessen Schwelle
einwandfrei ist.

**Keine Verletzung, eine unbesetzte Stelle.** `04 §3.5` nannte ein Subjekt nur für
`STALE_EPOCH_VOTE`. `04-golden-anchors.md` nennt für `GV-24`, `GV-29` und `GV-47` Art und Zustand,
kein Subjekt. Der Code war frei und hat die Freiheit ungünstig genutzt.

**Nichts bewacht es.** Die vorhandenen Vektortests prüfen über einen `_kinds`-Helfer
ausschließlich die Art des Vermerks. Alle drei Subjekte umzustellen lässt die volle Reihe mit 572
grün durchlaufen. Eine Änderung, die drei Diagnosen umlenkt, läuft heute still durch — dieselbe
Klasse wie die reglosen Tests aus D185, nur eine Ebene tiefer.

**Die Entscheidung.** `04 §3.5` bekommt die Regel, dass das Subjekt das zurückgewiesene Objekt
benennt, mit den beiden nicht offensichtlichen Fällen ausgeschrieben. `decide` zieht an drei
Stellen nach: die Schwellenschleife führt den Hash des jeweils geprüften Objekts mit, die beiden
Genesis-Fälle adressieren den Scope. Die drei Subjekte bekommen Tests, sonst bleiben sie
unbewacht.

**Der Anschluss an D173.** Dort steht offen, dass die Form der Vermerke nirgends festgehalten ist.
Dieser Eintrag schließt das für `04 §3.5` und für nichts sonst; die übrigen Vermerkorte bleiben
unbestimmt.

### D199 — Abnahme `00l`: die Proben belegen mehr als den Code, den sie prüfen

**Was gebaut wurde.** Die drei Subjekte aus D198 in `decide`, der Prüffall aus D197 auf
Kettenebene und drei Prüffälle auf `decide`-Ebene in der neuen Datei
`tests/governance/test_vermerk_subjekte.py`. Gemessen mit `git diff --numstat` gegen den
Prompt-Commit `dc5c04d`: drei Dateien, 137 eingefügte und 6 entfernte Zeilen. 576 Tests. Gemergt
als Fast-Forward über zwei Commits, `main` bei `bf50375`.

**Die Proben.** Drei Rücknahmen, drei vorher festgelegte Rotmengen, alle drei getroffen: die
Schwellenschleife einen roten Test, die beiden Genesis-Subjekte zwei, die Variantenwelt des
Kettentests einen. Kein bestehender Test ist mitgefallen — und genau das ist die Aussage. Die
Proben zeigen nicht nur, dass die neuen Tests greifen, sondern am Artefakt, dass vor diesem Lauf
**nichts** die drei Adressen gehalten hat. Dieselbe Form wie Probe A in `00j`, wo eine Rücknahme
die Reglosigkeit zweier älterer Prüfschichten vorführte.

**Kein Defekt.** Der Supervisor hat den Lauf in einem eigenen Baum nachgebaut, die volle Reihe und
alle drei Proben unabhängig gefahren, `ruff` mit der Projektauswahl laufen lassen; alles
reproduziert. Es ist der erste Lauf dieser Sitzung ohne Befund in der Abnahme — der einzige Defekt
von `00k` lag im Kriterium des Supervisors, nicht im Werkzeug.

**Eine Beobachtung, kein Befund.** Die neue Signatur von `_welt3()` ist 101 Zeichen lang.
Nachgemessen, bevor das ein Defekt genannt wurde: `pyproject.toml` wählt `F401` und `F811`,
`line-length` ist nicht gesetzt, und die Hundert-Zeichen-Regel des Projekts gilt Spec-Dateien.
Für Python gibt es also keine Zeilenlängenregel, gegen die das verstoßen könnte. Ob es eine geben
soll, gehört zu der schon offenen Frage nach einer dritten `ruff`-Gruppe und wird dort mit
entschieden, nicht hier nebenbei.

### D200 — Die Zielverfassung muss regieren können, geprüft am Übergang

**Der Fork aus D197.** `decide` prüft die Zielverfassung heute auf Vorhandensein, Hash und die
Schwelle der angewandten Klasse. Auf `participants` und auf `irrevocable_predicates` prüft es nur
die Verfassung der Epoche. Eine Zielverfassung ohne `participants` ist damit ein zulässiges Ziel:
die Kette rückt in sie ein, sie liefert `authorized_keys`, und erst der nächste Übergang
scheitert — festgehalten im Prüffall zur untauglichen Zwischenverfassung in
`tests/test_kettenwelt.py`.

**Gemessen, drei Varianten**, jede im Baum des Supervisors gegen die Welt aus D197 gefahren:

| Variante | Epoche | Schlüssel | Auszählung 1 nach 2 | Vermerke | rot |
|---|---|---|---|---|---|
| heute | 2, `C1` regiert | aus `C1` | `UNEVALUABLE` erst bei 2 nach 3 | zwei | — |
| `§3.5`, eng | 1, `C0` | Genesis-Wurzel | `UNEVALUABLE` | zwei | 1 |
| `§3.5`, mit Schwellenklassen | 1, `C0` | Genesis-Wurzel | `UNEVALUABLE` | zwei | 1 |
| `§4.1`, eng | 1, `C0` | Genesis-Wurzel | `PASSED`, 3 von 3, `[1,2]` | einer | 1 |

Jede Variante kostet denselben einen Test — den Prüffall aus D197 selbst, kein Kollateral im
576er Korpus. Die Kosten entscheiden die Gabel also nicht.

**Entschieden: ja, prüfen — in `§4.1`, in der engen Fassung.** Bedingung 6 dort.

**Der Grund für das Ob.** Heute liefert der Zustand Schlüssel aus einer Verfassung, aus der der
Nukleus nie wieder herauskommt, und `policy_findings` wie `key_findings` sind dabei **leer**
(gemessen). Wer die Schlüssel liest und die Epochenvermerke nicht, hält eine Aussage, die mit
nichts kollidieren kann. `08 §2.2` verlangt das Gegenteil.

**Der Grund für das Wo.** Die Regierbarkeit des Ziels geht in die Auszählung nicht ein. In `§3.5`
eingebaut, meldete sie `UNEVALUABLE`, wo `PASSED` gemessen ist — dieselbe Art Fehladressierung,
die D194 und D198 abgestellt haben. Der Übergang scheitert, nicht die Zählung.

**Literatur.** python-tuf hat dieselbe Stelle. Im Client-Workflow fehlte Schritt 1.3: neu geladene
Root-Metadaten wurden nicht gegen die Schwelle der Schlüssel geprüft, die in der neuen Root selbst
stehen, und dadurch konnte eine ungültige Root zur vertrauten werden — GHSA-f8mr-jv2c-v8mg,
behoben in PR 1101, enthalten ab v0.14.0. Die strukturelle Lehre ist dieselbe: das Rotationsziel
muss die Regeln erfüllen, die es selbst auferlegen wird, bevor es übernommen wird.

**Benannt und abgelehnt: die Signaturfassung.** TUFs Schritt 1.3 ist eine Signaturprüfung, das
Ziel muss von den eigenen Schlüsseln getragen sein. In MaR hieße das: die Zielverfassung muss
unter ihren eigenen `participants` und ihrer eigenen Schwelle Zustimmung finden. Das wird **nicht**
übernommen, und zwar aus benanntem Grund. TUFs Bedrohungsmodell ist ein Dritter, der Metadaten
ausliefert; in MaR wählt die laufende Epoche das Ziel und ist die legitime Autorität. Es gibt
keinen Dritten. Die Lehre überträgt sich, das Modell nicht.

**Die Gegenseite.** Auch TUF nimmt unerreichbare Endzustände hin: ein Repository, dessen
Rotationen in einen Zyklus laufen, wird als ungültig markiert, ohne Weg zurück. Der Unterschied
trägt die Entscheidung — ein Zyklus ist erst hinterher erkennbar, die untaugliche Zielverfassung
schon vorher.

**Ein Helfer, nicht zwei Fassungen.** Die vier Lagen stehen in `§3.5` als eine Tabelle und
bekommen eine Implementierung: `constitution_governable` in `tally.py`, aufgerufen von `decide`
mit dem Subjekt `epoch.constitution_hash` und von `verify_ratification` mit dem Subjekt
`proposal.constitution_hash`. Der andere Weg — die vier Prüfungen in `§4.1` noch einmal
schreiben — hätte eine Regel mit zwei Fassungen hinterlassen, und die driften.

**Nebenbefund, mit erledigt: die vier Subjekte in `decide` waren unbewacht.** Beim Bau der
Rücknahmeproben gemessen: stellt man die Adresse dieser vier Vermerke von
`epoch.constitution_hash` auf `proposal.constitution_hash` um, läuft die volle Reihe grün durch.
D198 hat drei Subjekte in `decide` besetzt, die Schwellenschleife und die beiden
Genesis-Subjekte; diese vier nicht. Dieselbe Form wie der Befund aus D199 — ein Test kann die Art
prüfen und die Adresse nie. Der Lauf zu D200 schließt die Lücke mit einem Prüffall in
`tests/governance/test_vermerk_subjekte.py`.

**Offen und hier benannt: wie weit die Regierbarkeit reicht.** Die enge Fassung prüft
`participants` und die beiden Unwiderruflichkeiten. Die vollständige prüfte zusätzlich die
Schwellenklassen, und erreichbar sind genau zwei — `membership` und die Klasse aus `genesis[5]`,
weil `threshold_class` keine dritte liefern kann. Sie ist also konstruierbar und kostet dasselbe,
braucht aber `genesis_obj` als zweiten neuen Parameter in `§4.1`. Dagegen spricht, dass eine
fehlende von zwei Klassen keine Sackgasse ist, sondern eine Teilsperre. Die Frage wird beantwortet,
wenn ein Fall auftritt, der sie braucht, nicht vorher.

### D201 — Abnahme `00m`: der Verweis stimmte, die Anweisung lag daneben

**Was gebaut wurde.** Zwei Läufe auf einem Branch. Der erste gegen den Prompt-Commit `46eba03`:
zehn Dateien, 214 eingefügt und 75 entfernt, Testzahl von 576 auf 582, Commit `beddac8`. Der
Nachlauf gegen den Prompt-Commit `459581a`: zwei Dateien, 37 eingefügt und 5 entfernt, Testzahl
583, Commit `72dfebb`.

**Sechs Proben, sechs vorher festgelegte Rotmengen, alle sechs getroffen.** Den
Regierbarkeitsblock entfernen und das Subjekt in `verify_ratification` umstellen treffen dieselben
fünf Fälle; der ValueError-Wächter, das Subjekt in `decide` und die Ortsprobe des Nachlaufs je
einen; den Wächter ganz entfernen zwei. Kein bestehender Test ist mitgefallen.

**Der Nebenbefund aus D200 hat sich bestätigt.** Vor dem Lauf ließ sich das Subjekt der vier
Regierbarkeitsvermerke in `decide` von `epoch.constitution_hash` auf `proposal.constitution_hash`
umstellen, ohne dass ein Test rot wurde. Nach dem Lauf trifft dieselbe Umstellung genau einen.

**Der Defekt lag im Prompt, nicht im Lauf.** `04 §4.1` knüpft den `ValueError` auf ein
fehlzugeordnetes Zielobjekt an keine der Bedingungen 1 bis 5; der Prompt schrieb den Wächter
ausdrücklich dahinter. Das Werkzeug hat den Prompt korrekt umgesetzt. Die Folge war beobachtbar:
trug der `ratify@1` nicht, kehrte `verify_ratification` mit `UNSUPPORTED_RATIFICATION` zurück und
sah das Zielobjekt nie an — ein Aufruferfehler als Lage der Welt, genau das, was Bedingung 0
verhindert. Gemessen mit einem `ratify@1` ohne Zeugen und dem Zielobjekt `C1` bei einem Vorschlag
auf `C2`: erwartet `ValueError`, bekommen kein Fehler.

**Was die Ortsprobe vorführt.** Wird der Wächter an die verworfene Stelle zurückgeschoben, fällt
**nur** der neue Prüffall; `test_mismatched_target_object_raises` bleibt grün. Der ältere Fall hat
also die Prüfung gehalten und ihren Ort nie. Dieselbe Form wie der Befund aus D199 — dort prüfte
ein Helfer die Art und verdeckte die Adresse, hier prüfte ein Fall die Prüfung und verdeckte die
Stelle. Daraus Prüfregel 34.

**Der Supervisor bleibt die Fehlerquelle.** Zum wiederholten Mal lag der einzige Defekt eines
Laufs im Prompt. Prüfregel 27 hat ihn nicht gefangen: sie verlangt, dass ein Verweis die
behauptete Aussage trägt, und das tat er. Daraus Prüfregel 33.

### D202 — Der aufgelöste Zustand des Beispielnukleus hat einen Abschnitt

**Der offene Punkt aus D189 ist geschlossen.** `check_resolved_chain` rechnete seit `00i` einen
Zustand nach, den `example-nucleus.md` nirgends behauptete. Ein Prüfer ohne Text im Dokument prüft
sich selbst: er kann nicht mit der Spec kollidieren, weil die Spec zu ihm schweigt. `§5.1` schreibt
die fünf Werte hin, gegen die er rechnet.

**Die Reglosigkeit wird im Abschnitt benannt, nicht überspielt.** Keine der beiden Verfassungen
des Beispiels setzt `nucleus_keys`; `authorized_keys` ist deshalb in beiden Epochen
`genesis_gov[1]`. Ein Leser, der `§5.1` für eine Vorführung der Epochenschärfe hält, zöge daraus
einen falschen Schluss, und der Verweis auf die Kettenwelt (D190) sagt ihm, wo sie zu finden ist.
D169 bleibt damit offen wie bisher: dass der Beispielnukleus Epoche-1- von Epoche-2-Policy nicht
unterscheiden kann, ist ein benannter Zustand.

**Kein Lauf, keine Entscheidung.** Der Abschnitt beschreibt bestehenden, geprüften Code. Er
verändert weder `tools/example_nucleus.py` noch eine Layer-Datei. Registriert wird er trotzdem,
weil D189 den Punkt als offen führt und ein stilles Schließen ihn dort stehen ließe.

### D203 — Die Auszählungsvermerke gehen mit, wenn keine Epoche entsteht

**Der offene Punkt aus D194.** Weitergegeben wurde bisher nur bei `UNEVALUABLE`. Scheitert eine
Ratifizierung, während die Auszählung auswertbar ist, blieb der Beobachter ohne Adresse.

**Eine Korrektur am eigenen Aufschlag.** Gemessen wurde zuerst ein weiter gefasster Verlust: läuft
ein Übergang durch, während die Auszählung `NON_MEMBER_VOTE` führt, meldet `resolve_state` gar
nichts. Das ist kein Loch, sondern die benannte Grenze aus `§4.5` — die Vermerke der Kette sind
keine Chronik, sondern die Begründung des Halts, und ein Vermerk aus einem Übergang, der getragen
hat, beantwortet diese Frage nicht. Der zweite Grund der Spec trägt in der engen Fassung dagegen
nicht mehr: bei `PASSED` gibt es kein `TALLY_UNEVALUABLE`, über das die Tatsache den Beobachter
erreicht.

**Entschieden: Weitergabe auf jedem Pfad ohne Folgeepoche, auf keinem mit.** Eine Regel, kein
Katalog. Die Form ist die aus D194 nach RFC 8914: additiv, der eigene Vermerk bleibt, die
Verarbeitung ändert sich nicht.

**Gemessen.** In der Welt aus D178 wächst die Diagnose von vier auf acht Vermerke: die vier
`UNKNOWN_PROPOSAL` benennen die Stimmen, die ein fehlendes Vorschlagsobjekt ausgesetzt hat, und
erklären damit die drei `UNSUPPORTED_RATIFICATION`, die heute unbegründet dastehen. Ein einziger
bestehender Prüffall musste seine Erwartung erweitern.

**Die Grenze wird von zwei Schichten gehalten.** Der erste Grenztest lag auf Kettenebene und blieb
**grün**, als die Weitergabe versuchsweise auf den tragenden Pfad von `§4.1` gelegt wurde:
`resolve_epoch` liest `result.findings` dort nicht. Erst ein zweiter Wächter auf `§4.1`-Ebene fängt
das. Die Kettenebene wiederum wird nicht von einer Zeile gehalten, sondern vom Neuaufbau der
Vermerkliste je Schleifenschritt; die Probe dafür ist die verworfene Bauform — Liste aus der
Schleife heben und auf dem tragenden Pfad füllen —, und sie trifft zwei Fälle, darunter den
bestehenden `test_chain_stale_epoch_findings_absent`. Daraus Prüfregel 35.

**Benannt und nicht gebaut.** Von den fünf Pfaden ohne Folgeepoche halten Prüffälle drei:
`TALLY_UNEVALUABLE` über `test_chain`, `UNSUPPORTED_RATIFICATION` und Bedingung 6 über die neue
Datei. `RATIFY_WITH_EXPIRY` und der Zeugenpfad tragen die Regel ungeprüft. Das ist eine Wahl aus
Verhältnismässigkeit, kein Versehen, und steht hier, damit niemand sie für Deckung hält.

### D204 — Abnahme `00n`, kein Defekt

**Was gebaut wurde.** Ein Lauf gegen den Prompt-Commit `f07cf3d`: drei Dateien, 195 eingefügt und
15 entfernt, Testzahl von 583 auf 587, Commit `0699bbf`. Acht Aufrufe von `_unsupported`
umgestellt, fünf Rückgaben ohne Folgeepoche hängen die Auszählungsvermerke an, die tragende bleibt
`findings=()`, `chain.py` unberührt.

**Vier Proben, vier vorher festgelegte Rotmengen, alle vier getroffen.** Die Weitergabe aus
`_unsupported` und aus dem Regierbarkeitsblock zu entfernen trifft je einen Fall; sie zusätzlich
auf die tragende Rückgabe zu legen ebenfalls einen, und der Kettentest bleibt dabei grün wie
vorhergesagt; die verworfene Bauform in `chain.py` trifft zwei, darunter den bestehenden
`test_chain_stale_epoch_findings_absent`. Kein bestehender Test ist mitgefallen.

**Die abgeleitete Erwartung hat gehalten.** In `test_chain_missing_proposal_2` werden die
`UNKNOWN_PROPOSAL`-Subjekte aus dem Speicher der Welt gefiltert statt getippt, und das Werkzeug hat
die gemessene Vier mit einem eigenen `assert` festgehalten. Damit fällt der Fall auf, wenn die Welt
sich ändert, statt still eine andere Aussage zu prüfen.

**Ein Zug, der im Prompt nicht stand und besser ist als das Vorbild.** Die fremde Identität der
neuen Prüffälle entsteht über einen Helfer, der mit `assert fremd.pub not in C1["participants"]`
seine eigene Voraussetzung sichert. Der Entwurf des Supervisors hatte die Nichtteilnahme nur
angenommen. Das ist Prüfregel 30 an der richtigen Stelle: die Variantenwelt weist nach, was sie
voraussetzt.

### D205 — Eine dritte `ruff`-Gruppe: `ARG` ja, Zeilenlänge nein

**Der Nachweis, den D182 verlangt hat.** D182 hat den Linter bewusst auf `F401` und `F811`
festgelegt und für jede weitere Gruppe verlangt, zuerst die Zahl der Funde im Baum zu messen.
Gemessen: **drei** `ARG001`, **null** davon im Produktivcode.

**Zwei der drei sind kein Rauschen.** `tests/trust/test_bootstrap.py` parametrisiert die fünf
Spalten der `TP-BOOT`-Tabelle aus `02-golden-anchors.md` — `m`, `n`, `cap`, `trust`, `disjoint` —
und vergleicht **zwei**. `expected_n` und `expected_cap` werden geparst und nie benutzt. Das ist
die Form aus D199: die Tabelle sieht aus, als prüfe sie den Anker, und prüft die Hälfte. Beide
Spalten wurden gegen die gebaute Welt nachgerechnet und stimmen: `n` aus den erzeugten
`vouch`-Claims ist 4, 2, 1 und `⌊n·C₀/D⌋` ist 2, 1, 0. Der dritte Fund, `path_name` in
`tools/check_specs.py`, ist ein toter Parameter und wird entfernt, nicht unterdrückt.

**Was die Reparatur hinzufügt, ist eine Adresse und keine Erkennung.** Gemessen durch Vergleich der
Rotmengen: wird in `_build` ein falsches `n` emittiert, fallen mit und ohne die neuen Behauptungen
**dieselben fünf** Fälle. Ein falsches `n` bricht ohnehin jeden Vertrauenswert; die neue Zeile sagt
nur früher und genauer, woran es liegt. Was die beiden Behauptungen wirklich halten, ist die
Übertragung der Ankertabelle in den Test: ein Transkriptionsfehler in der `n`-Spalte oder in der
`cap`-Spalte färbt je genau eine Zeile rot. Zwei Kopien derselben Tabelle, und die Drift zwischen
ihnen ist bewacht. Daraus Prüfregel 36.

**Entschieden: `ARG` wird zugeschaltet.** `check-lint` ruft `ruff check` ohne eigene Select-Liste,
die Gruppe aus `pyproject.toml` greift also unmittelbar. Nachgewiesen mit dem wieder eingeführten
toten Parameter: ein Fehler.

**Entschieden: keine Zeilenlängenregel für Python.** Der Baum führt 16.898 Python-Zeilen. Über 88
Zeichen liegen **300** in 76 Dateien, über 100 **26** in 13, über 120 **12** in zwei. Bei 88 wären
das 300 Umbrüche für null gefundene Defekte; das ist Formatierung ohne Ertrag. Die 100-Zeichen-
Regel gilt für Spec-Dateien aus einem Grund, der für Python nicht dasselbe Gewicht hat — dort geht
es um die Lesbarkeit des Diffs eines Fließtexts. Der Ausreißerschwanz über 120 sitzt zudem in
`test_vectors.py` und `test_invariants.py` und stammt aus den mechanischen Einschüben des Laufs
`00m`; er ist Folge eines Auftrags, nicht eines fehlenden Linters. Damit ist die von D199
zurückgestellte Frage beantwortet und nicht wieder aufzumachen, solange die Zahlen so liegen.

### D206 — Abnahme `00o`, kein Defekt

**Was gebaut wurde.** Ein Lauf gegen den Prompt-Commit `c82a652`: drei Dateien, 9 eingefügt und 3
entfernt, Testzahl unverändert **587**, Commit `621f202`. `ruff check` mit `ARG` meldet null Funde.

**Drei Proben, drei vorher festgelegte Ergebnisse, alle drei getroffen.** Ein Transkriptionsfehler
in der `n`-Spalte und einer in der `cap`-Spalte färben je genau die betroffene Tabellenzeile rot;
der wieder eingeführte tote Parameter erzeugt genau einen `ARG001`. Damit ist am Artefakt gezeigt,
dass die neue Gruppe beisst und nicht nur in der Konfiguration steht.

**Eine Lücke im Bericht, vom Supervisor geschlossen.** Das Werkzeug konnte die Proben N und O nur
gegen `tests/trust/test_bootstrap.py` fahren, nicht gegen die volle Reihe, und hat das gemeldet
statt es zu verschweigen. Der Supervisor hat beide im eigenen Baum gegen alle 587 nachgefahren: je
genau ein roter Fall, 586 grün. Die Einschränkung hat nichts verdeckt. Gemeldete Unvollständigkeit
ist billiger als eine unvollständige Messung, die als vollständig auftritt.

**Ein Zug, der im Prompt nicht stand.** Die Gruppen werden aus `store.all_claims()` gebildet, nicht
aus der lokalen Claim-Liste des Weltbauers. Gleichwertig, weil der Speicher aus eben dieser Liste
entsteht, und eine Spur strenger: gemessen wird, was im Speicher liegt, nicht was hineingereicht
wurde.

### D207 — Die Vermerkslage ohne eigene Adresse: zwei Tabellenzeilen, kein Formeingriff

**Die Bestandsaufnahme, die D173 verlangt hat.** Vier Vermerks-Enums, **44 Arten**, jede mit
Produktivträger. Die Deckung des Subjekttyps in der normativen Schicht ist ungleich: `04` nennt ihn
vollständig (`§3.5`, D198, mit zwei ausgeschriebenen Sonderfällen), `03` nennt in `§6` eine
allgemeine Regel ohne Spalte je Art, `00` nennt ihn für eine seiner zwei Arten (`§5.4`), und `02`
nennt ihn in der Layer-Datei überhaupt nicht — die einzige Aussage steht in
`02a-maxflow-prompt.md §5` und kennt `NON_CANONICAL_V` und `VOUCH_WITHOUT_TEXP` nicht. Die fünf
Treffer auf „Subjekt" in `02-trust-flow.md` meinen sämtlich das Vouch-Subjekt `J` — dieselbe
Namenskollision wie in `01 §2.1` und bei `Edge.subject`, das dritte Mal in derselben Messung.

**Der gemeldete Rollenwechsel ist keiner. Die Meldung wird zurückgenommen.** Gemessen wurde
zunächst, dass drei Stellen den Vermerksträger statt des zurückgewiesenen Objekts benennen:
`epoch.py:140`, `verdict.py:84` und `verdict.py:117`. Beim Nachlesen gegen `04 §4.1` und
`03 §2.4.4` fällt die Klassifikation. In allen drei Fällen ist das defekte Objekt ein **Feld** —
`verdict.J`, `accusation.J`, die Zeugenliste des `ratify@1`. Felder haben keine eigene Adresse. Das
Subjekt benennt also dasselbe Objekt, nur gröber, und das ist genau der Fall, den `04 §3.5` für
`genesis[5]` und `genesis[6]` bereits normiert hat. **D198 ist vollständig**; eine zweite Rolle gibt
es nicht und ist nicht zu schreiben.

**Drei Varianten gebaut und gemessen, alle drei verworfen.** Die Rotmenge unterscheidet sie nicht —
jede kostet genau einen Test, `test_VS_11`. Entschieden hat der Rest.

- **A, `subject: bytes | None`** nach SARIF `§3.27.12` (null oder mehr Orte; EXAMPLE 1 ist der
  Analysator, der kein globales `main` findet) und JSON:API (`source` wird weggelassen statt
  ersetzt). Kostet zwei Feldtypen, drei Erzeugungsstellen — und **zwingt in `dedupe_sort`**, weil
  `order=True` `bytes` gegen `None` vergleicht. Ohne diesen Eingriff wirft der Produktivpfad einen
  `TypeError`, und die volle Reihe sieht ihn nicht: 586 grün. Damit fasste A auch D183 an.
- **B, ein zweites Feld für die Rolle** nach SARIF `§3.27.13` (`analysisTarget` neben `locations`).
  28 Erzeugungsstellen in vier Modulen für eine Unterscheidung, die nach der Widerlegung oben gar
  nicht besteht.
- **D, eigene `kind` je Bedingung.** Bricht drei benannte Entscheidungen auf: `04 §4.1` legt die
  Zweiteilung mit Kriterium fest („welche `claim_id` er holen muss" gegen „dass Holen nichts
  nützt"), `03 §2.4.4` fasst zwei Lagen bewusst zusammen und begründet, warum nur die dritte Zeile
  abgetrennt wird, und `04a-korrektur-prompt.md §6` stellt die feinere Aufschlüsselung von
  `UNSUPPORTED_RATIFICATION` ausdrücklich zurück — „benannt und nicht übersehen".

**Was wirklich fehlt, sind zwei Tabellenzeilen.** Beide Lagen treten im Produktivcode auf und haben
in der zuständigen Tabelle keine Zeile; der Code fällt jeweils auf eine Sammelzeile zurück, die ihn
nicht deckt.

| Ort | Lage ohne Zeile | Was der Code heute meldet |
|---|---|---|
| `04 §4.1` | ein zitierter Eintrag in `ratify` ist keine `claim_id` | `UNSUPPORTED_RATIFICATION` |
| `03 §2.4.4` | `accusation.J.tag` ist weder `identity` noch `claim-ref` | `UNRESOLVED_ACCUSED` |

Die Sammelzeile in `04 §4.1` lautet „der Claim ist da und trägt nicht". Im ersten Fall ist kein
Claim da; es ist keine `claim_id`. Die Zeile trifft nicht zu, das Verhalten ist trotzdem richtig —
der Beobachter erfährt, dass Holen nichts nützt. Fehlt nur die Begründung in der Spec.

**Drei Pfade ohne Prüffall — der Befund, der schwerer wiegt als die Gabel.** In allen drei Varianten
war `test_VS_11` der einzige rote Test. Nur `verdict.py:84` ist gedeckt. `epoch.py:140` und
`verdict.py:117` lassen sich beliebig umstellen, ohne dass die 587er Reihe reagiert; deshalb ging
auch der `TypeError` aus Variante A durch. Was fehlt, ist nicht eine Regel, sondern Abdeckung.

**Zwei Korrekturen an früheren Aussagen.** Erstens: der offene Punkt zu D183 lautet „vier
`Finding`-Klassen, vier `dedupe_sort`". Gemessen sind es vier Klassen und **drei** `dedupe_sort` —
`trust/findings.py` hat keins; das vierte gehört `PolicyNote` in `policy.py`, einer fünften
Vermerksfamilie mit anderer Feldform (`code` / `predicate: str`), deren Trennung `03 §1.2`
ausdrücklich begründet. Zweitens: `sitzungsstart-00p.md` begründet D173 damit, dass `08 §2.2`
daran hänge, weil Vermerke kollidieren können sollen. `§2.2` handelt ausschließlich von
**signierten Claims**; Vermerke sind unsignierte lokale Ableitungen und kollidieren in seinem Sinne
nicht. Die Begründung trägt nicht und wird nicht weitergeschrieben. Was D173 trägt, ist schwächer
und ausreichend: Konsistenz über 44 Arten in vier Modulen, und die Weitergabe über die Grenze aus
D203, bei der Auszählungsvermerke in ein `RatificationResult` gelangen.

**Entschieden: kein Formeingriff.** Weder `subject` optional noch ein Rollenfeld noch neue `kind`.
Der Lauf `00q` schreibt die zwei Tabellenzeilen mit benannter Begründung und legt für die drei
Pfade Prüffälle an. Die Subjektspalten je Layer aus D173 bleiben offen und werden danach billiger,
weil jede Art dann genau einen Subjekttyp führt.

### D208 — Abnahme `00q`, kein Defekt im Lauf; der Defekt lag in der Prompt-Basis

**Der Lauf.** `d3d7197` auf `00q`, zwei Prüffälle, 587 auf **589**. `git diff --numstat` meldet
`49 2` in `tests/governance/test_vermerk_subjekte.py` und `45 0` in
`tests/profiles/test_vermerk_subjekte.py`. Die zwei gelöschten Zeilen sind zwei Importzeilen, die
zu Mehrzeilern erweitert wurden; kein Produktivpfad ist berührt. Beide Welten stehen Feld für Feld
wie vor dem Prompt gemessen. Die Erwartung in PF-1 ist über `dedupe_sort` abgeleitet und nicht in
Reihenfolge getippt, und der Prüffall sichert seine eigene Voraussetzung mit `tally.findings == ()`
ab. Beide Rücknahmeproben trafen genau ihren Prüffall, je `1 failed, 588 passed`.

**Der Defekt lag in der Basis, die der Prompt vorgab.** `00q` verzweigt von `cc29a2d`, dem Commit
mit den zwei Tabellenzeilen — der Prompt-Commit liegt darüber. Prüfregel 31 verlangt den
Prompt-Commit als Vergleichspunkt; hier war es der Spec-Commit darunter. Für die Abnahme ist das
folgenlos, denn `00q` fasst keine Datei an, die der Prompt-Commit anfasst. Für den Merge ist es
nicht folgenlos: ein Fast-Forward setzt voraus, dass `main` seit `cc29a2d` nicht weitergelaufen
ist, und das ist bei dieser Reihenfolge nie gegeben.

**Daraus Prüfregel 37.** Die Basis eines Laufs ist der Commit, der den Prompt enthält. Wer einen
Prompt schreibt, bevor er ihn committet, nennt darin eine Basis, die es noch nicht gibt — der
Prompt wird deshalb zuerst committet und die Basis danach eingetragen, nicht umgekehrt.

**Die überlangen Docstrings sind zulässig.** Zwei Zeilen in den neuen Prüffällen laufen über
hundert Zeichen. D205 hat die Zeilenlängenregel für Python mit Zahlen verneint; die Regel gilt für
Spec- und Prompt-Dateien im Wurzelverzeichnis, nicht für Testcode. Kein Befund.

**Was der Lauf belegt.** Vor `00q` liessen sich beide Stellen umstellen, ohne dass die Reihe
reagierte: der Nicht-Bytes-Zweig in `verify_ratification` durfte seinen Vermerk verlieren und das
Subjekt im `else`-Zweig von `verdict_status` durfte auf Nullbytes wechseln, beides bei 587 grün.
Jetzt sieht die Reihe beides. Damit ist der Teil von D173 erledigt, der Abdeckung war; der Teil,
der Subjektspalten je Layer verlangt, bleibt offen und beginnt bei `02`, wo die Layer-Datei
überhaupt keine Aussage über Subjekttypen führt.

### D209 — Zwei Werkzeuge gegen das Wiederfinden, nicht gegen die Komplexität

**Die Diagnose ist gemessen und lautet anders als vermutet.** Der Verdacht war, die Schichten seien
zu stark verzahnt. Gemessen am Importgraphen laufen 74 Kanten von `trust`, `profiles` und
`governance` nach unten in den Kern und 6 zurück, fünf davon aus der Fassade `resolve.py`. Die
Schichten stapeln, sie verflechten nicht. Von 672 Abschnittsverweisen auf Layer-Dateien zeigen
drei ins Leere. Was wächst, ist das Register: 7375 Zeilen, 208 Einträge, 29 Prozent des Projekts.

**Die Fehlerquelle sitzt vor dem Prompt, nicht im Prompt.** In der Sitzung zu D207 wurden vier
Positionen bezogen und drei zurückgenommen; jede Rücknahme hatte dieselbe Ursache, nämlich eine
Entscheidung, die es schon gab — die Sammelform in `04 §4.1`, die Zusammenfassung in `03 §2.4.4`,
die Zurückstellung in `04a §6`. Prüfregel 27 und 33 greifen, wenn ein Prompt entsteht. Zwischen
Positionsbildung und Prompt liegt aber die eigentliche Arbeit, und dort greift keine Regel.

**Daraus Prüfregel 38** und zwei Werkzeuge, die sie ausführbar machen statt sie zu mahnen.

**`tools/register_index.py`.** Nimmt einen Abschnittsnamen und gibt die Registereinträge aus, die
ihn nennen. Gemessen an `04 §4.1` liefert er `D106 D107 D174 D193 D194 D201`; D106 ist genau der
Eintrag, der die Sammelform entschied. Der Index wird **gerechnet, nicht gepflegt** — eine
generierte Datei im Baum wäre eine dritte Wahrheitsquelle neben Code und Spec und würde driften.
Benannte Grenze: 40 Prozent der Einträge nennen keinen Abschnitt und tauchen im Index nicht auf.

**`check_specs.py` prüft Abschnittsverweise.** Ein Verweis der Form `NN §X.Y` auf eine Layer-Datei
muss dort eine Überschrift treffen. Zwei Einschränkungen, beide mit Grund:

- **Nur Ziffernpräfixe.** Die Zitierkonvention ist nicht injektiv: `03` und `04` bezeichnen je vier
  Dateien, `01a` zwei. Ein Verweis `01a §3.3` ist ohne festgelegte Tabelle nicht auflösbar. Solange
  es die nicht gibt, prüft das Werkzeug nur `00` bis `08`.
- **Nicht in `07-decisions.md` und `sitzungsstart-*.md`.** Beide beschreiben vergangene Stände. Ein
  Registereintrag, der einen inzwischen umgebauten Abschnitt nennt, ist richtig und wird nicht
  nachgezogen; zwei der drei gefundenen Verweise sind genau das.

Nach diesen Einschränkungen bleibt ein einziger Fund: `welten-prompt.md` verweist auf `01 §6.7`.
Der Abschnitt `01 §6` ist nicht untergliedert; gemeint ist Listenpunkt 7 darin (`t < t_exp`). Der
Verweis wird auf `01 §6` berichtigt. **Benannte Grenze der Prüfung:** sie kann einen Listenpunkt
nicht von einem Unterabschnitt unterscheiden und hätte `§6.7` auch dann gemeldet, wenn die
Zitierweise beabsichtigt gewesen wäre.

**Ausdrücklich nicht entschieden.** Kein Übersichtsdokument über die Schichten, kein gemaltes
Abhängigkeitsdiagramm, keine Aufteilung des Registers auf mehrere Dateien. Das Erste driftet, das
Zweite ist aus dem Code in Sekunden zu rechnen, das Dritte zerbricht 345 bestehende Verweise.

### D210 — Die Verweisprüfung unterscheidet Erwähnung nicht von Verwendung

**Der Befund kam aus dem Lauf `00r` und betraf den Prompt, nicht den Lauf.** Die neue Prüfung aus
D209 meldete vier Verweise in `00r-registerindex-prompt.md` selbst — die Beispielzeilen, mit denen
der Prompt beschreibt, welche kaputten Verweise zu finden sind. D209 nimmt `07-decisions.md` und
`sitzungsstart-*.md` aus; für einen Prompt, der über Verweise spricht, war nichts vorgesehen. Das
Werkzeug hat den Widerspruch gemeldet statt ihn aufzulösen, und das war richtig.

**Entschieden: die Beispiele werden umgeschrieben, keine Ausnahme gebaut.** Wer über einen nicht
existierenden Abschnitt schreiben muss, nennt seine Nummer ohne das Paragraphenzeichen — „der
Unterabschnitt 6.7 von `01 §6`" statt der Zitierform. Die Prüfung sieht dann nur den gültigen
Verweis.

**Benannt und verworfen: eine Abschaltmarke.** Der Stand der Technik in Lintern ist die lokale
Unterdrückung, `noqa` und seinesgleichen. Sie schaltet hier die ganze Datei ab, auch für echte
Funde, und sie bleibt liegen, wenn ihr Grund verschwunden ist. Der Preis der gewählten Fassung
setzt sich dagegen selbst durch: wer die Konvention vergisst, sieht es beim ersten `make check`.

**Ebenfalls verworfen: Prompt-Dateien aus der Prüfmenge nehmen.** Der einzige echte Fund der
gesamten Messung lag in `welten-prompt.md`. Eine Prüfung, die Prompt-Dateien auslässt, hätte ihn
nicht gefunden.

**Drei Zahlen aus D209 werden berichtigt.** Der Supervisor hat 672 geprüfte Verweise und sechs
Registereinträge zu `04 §4.1` an `65ab37d` gemeldet und beides an einer älteren Arbeitskopie
gemessen, der D207 bis D209 fehlten. Richtig sind **704** Verweise, davon **238** nach der
Ausnahme, und **acht** Einträge zu `04 §4.1` — D207 und D209 nennen den Abschnitt selbst. Ein
Commit-Name an einer Messung, die nicht an ihm entstand, ist genau der Fall aus Prüfregel 19.

**Der Lauf `00r` bleibt gültig.** Die drei Teile sind gebaut und ungebrochen. Die Berichtigung
des Prompts geht in den Lauf-Commit selbst, weil er ohne sie nicht grün werden kann; damit bleibt
`main` bis zum Merge stehen und das Fast-Forward erhalten (Prüfregel 37). Dieser Eintrag folgt nach
dem Merge. Die `numstat`-Menge des Laufs wächst dadurch um `00r-registerindex-prompt.md`.

### D211 — Abnahme `00r`; der Lauf landete auf `main`, weil eine Ausgabe für eine Bedingung galt

**Der Lauf.** `7e93a6a`, vier Dateien, `145 +` und `13 -`. `tools/register_index.py` ist neu,
`tools/check_specs.py` bekommt die Verweisprüfung, `welten-prompt.md` eine berichtigte Zeile, der
Prompt seine umgeschriebenen Beispiele. Beide Werkzeuge setzen D209 um: explizite Präfixtabelle
statt Glob, Ausnahme für Register und Sitzungsstart, „Nummer plus Punkt" in `heading_covers`, und
eine leere Trefferzeile mit Rückgabewert 0 für einen Abschnitt ohne Eintrag. **Kein Defekt im
Werkzeugcode.**

**Der Lauf hat keinen Branch bekommen.** Der Block des Supervisors begann mit
`git branch --show-current` und behandelte dessen Ausgabe als Prüfung. Der Befehl gibt den Namen
aus und liefert Status 0, gleich welcher Branch anliegt; die Kette lief auf `main` weiter und der
Commit landete dort direkt. Inhaltlich ist er byte-gleich mit dem, was ein Fast-Forward gebracht
hätte, deshalb wird die Historie nicht umgeschrieben. **Daraus Prüfregel 39.**

**Die Proben des Werkzeugs galten für einen anderen Stand.** Sie liefen vor der Berichtigung des
Prompts und meldeten damals zusätzlich `00r-registerindex-prompt.md`; der committete Stand war
ungeprobt. Beide wurden nachgefahren: Probe A meldet genau einen Befund in `welten-prompt.md`,
Probe B genau einen in `00o-arg-prompt.md`, der Schlusslauf null. Nicht das Werkzeug hat hier
geschludert — der Supervisor hat die Berichtigung nach den Proben eingeschoben und sie nicht neu
verlangt.

**Ein Zug, der im Prompt nicht stand.** `REF` in `register_index.py` erlaubt neben dem
Ziffernpräfix auch `VISION`. Das Register nennt `VISION §…` dreimal; ohne die Alternative verlöre
der Index diese Verweise. Die Anpassung ist damit richtig, aber sie stand in keinem Auftrag und
kam in keinem Bericht vor. Sie bleibt stehen, weil ihr Entfernen einen Lauf kostet und nichts
verbessert; benannt wird sie hier.

**Die Verweisprüfung greift.** Über alle Wurzeldateien werden 704 Verweise gelesen, 238 davon
geprüft. Der eine echte Fund der Messung ist behoben, und zwei Proben zeigen, dass die Prüfung
nicht nur ihn kennt.

### D212 — Die Vermerkssubjekte von `03` und `00`; der Doppeleintrag war ein Streichungsrest

**Der Befund.** `03 §6` nannte in derselben Aufzählung zweimal `CONSTITUTION_UNAVAILABLE`. Die
zweite Nennung war nicht der falsche Name einer anderen Art, sondern der Rest einer Streichung:
`03-prompt.md` Zeile 82 führt den Satz im Original mit `CONSTITUTION_UNAVAILABLE` **und**
`CONSTITUTION_HASH_MISMATCH`, und D167 lässt die zweite Art ersatzlos entfallen. Beim Nachzug
wurde das Subjekt richtig auf „der übergebene" korrigiert und der leergewordene Name mit dem
ersten aufgefüllt. Die Reparatur ist Streichung, nicht Ersetzung.

**Die Messung.** Vierzehn Arten in `ProfileFinding`, keine Erzeugungsstelle ausserhalb von
`profiles/`. Dreizehn tragen eine `claim_id`; `CONSTITUTION_UNAVAILABLE` trägt den übergebenen
`constitution_hash` (`policy.py`). `CONSTITUTION_VERSION_MISMATCH` — der einzige Kandidat, den
der Name nahelegt — trägt die `claim_id` des `accept-rules` und kommt als zweite Nennung nicht in
Frage. Zwei Arten tragen je nach Lage zwei verschiedene Subjekte, und beide Male ist es die Regel
aus D198: hat das zurückgewiesene Objekt eine eigene Adresse, wird sie benannt, sonst gröber der
Claim, der das Feld führt.

**Beschluss für `03`.** Eine zweite Tabelle in `03 §6.1`, Bauform wie `02 §10`, dazu die Prosa
für die drei Sonderlagen. **Verworfen: eine dritte Spalte in der bestehenden Tabelle.** Die
längste Zeile dort misst heute 92 Zeichen; jede Subjektangabe sprengt die hundert. Wer die
Tabelle dafür kürzte, tauschte die Auslöserbeschreibung gegen die Subjektangabe — beide werden
gebraucht.

**Beschluss für `00`.** Ein neuer `00 §10` derselben Bauform. `00` hielt die Form seiner Vermerke
nirgends fest; das steht seit D173 offen. `00 §5.4` trägt nur das Subjekt von
`MALFORMED_NUCLEUS_KEY`, obwohl D164 das Subjekt von `CONSTITUTION_UNAVAILABLE` ausdrücklich
entschieden hat — die Entscheidung war getroffen und nie aufgeschrieben.

**Verworfen: ein Halbsatz in `00 §6.4` Schritt 1 c.** Dort entsteht der Vermerk, und der Satz
stünde richtig. Aber die Formaussage — eigener Enum, kein Reject, sortiert und dedupliziert —
bliebe heimatlos, die beiden Arten stünden in zwei Abschnitten, und der Docstring von
`mensch_als_republik/findings.py` zeigte weiter auf `00 §5.4` für eine Aussage, die dort nicht
steht. Ein Ort für beide Arten ist die billigere Antwort auf dieselbe Frage.

**Was offen bleibt.** Die Zeiger im Code sind nicht nachgezogen: der Modul-Docstring von
`mensch_als_republik/findings.py` nennt `00 §5.4`, `dedupe_sort` dort nennt `04-prompt.md §2`
schichtübergreifend. Beides ist Produktivcode und gehört in den nächsten Lauf, der die Datei
ohnehin anfasst. Damit ist D173 in der Spec erledigt; im Code bleiben zwei Docstring-Zeilen.

### D213 — Die Fangbreite wird an der Wurzel geschlossen, nicht an den drei Fängern

**Der Befund, gemessen.** `is_core_predicate` und `is_nuc_predicate` fangen `VerifierError`,
`is_nuc_name` fängt `Exception` (offen seit D181). Der enge Fänger fängt nichts von dem, was
tatsächlich austritt:

| `claim.p` | `is_core_predicate` | `is_nuc_predicate` | `is_nuc_name` |
|---|---|---|---|
| `bytes` | `TypeError` | `TypeError` | `False` |
| `None`, `int`, `list` | `AttributeError` | `AttributeError` | `False` |

`parse_predicate` kommt für ein nicht-`str` `p` gar nicht bis zu einem `raise`; es stolpert an
`p.startswith` beziehungsweise an `re.match`. Ein `VerifierError` entsteht nie.

**Aus dem Verifier heraus ist die Lage unerreichbar.** `_validate_field_types` verlangt
`isinstance(m.get(3), str)` und wirft sonst `MalformedCbor`; der Aufruf steht in
`structural_check` **vor** `claim_from_map`. Jeder Claim aus `read_claim` trägt `p: str`.
Erreichbar ist die Lage nur über `claim_from_map` oder `claim_from_bytes` direkt — genau der Weg,
den D181 benannt hat, als es die breite Fangweite bewusst stehen liess.

**Beschluss.** `parse_predicate` prüft `isinstance(p, str)` und wirft sonst `MalformedCbor`.
Danach tritt aus keinem der drei Prüfer etwas anderes als ein `VerifierError` aus, und
`is_nuc_name` kann auf `VerifierError` verengt werden, ohne dass sich an einer Aufrufstelle etwas
ändert. Die Divergenz löst sich auf, statt zugedeckt zu werden.

**Warum `MALFORMED_CBOR` und kein neuer Code.** `01` Anhang B zählt „falscher Feldtyp" bereits
unter `MALFORMED_CBOR`; der Verifier fällt für dasselbe `p` schon heute genau dieses Urteil. Die
Wache spricht es an der zweiten Tür noch einmal aus, statt eine zweite Antwort auf dieselbe Frage
zu erfinden. Die elf Reject-Codes bleiben elf.

**Verworfen: `is_nuc_name` auf `VerifierError` verengen und sonst nichts.** Das kippt
`test_nuc_name_bytes_p_returns_false`, den D181 mit Begründung gesetzt hat, und trägt die
Ausnahme wieder in den Aufrufer.

**Verworfen: alle drei auf `Exception` verbreitern.** Das ist keine Angleichung, sondern die
Übernahme des schlechteren Zustands in zwei weitere Funktionen: eine Fangweite, die
`AttributeError` schluckt, macht jeden künftigen Programmierfehler in `parse_predicate` still zu
`False`.

**Die Proben sind ungleich, und das ist die Aussage.** Die Wache ist einzeln prüfbar: ohne sie
wird der neue Prüffall rot — und mit ihr **auch** `test_nuc_name_bytes_p_returns_false`, weil die
verengte Fangweite dann ihr Netz verliert. Genau diese Kopplung ist der Beleg. Die Verengung
dagegen ist bei stehender Wache **nicht** einzeln prüfbar: ihre Rücknahme lässt die Reihe
vollständig grün. Das ist kein wertloser Probelauf, sondern die Behauptung des Beschlusses —
wäre sie rot, änderte die Verengung Verhalten, und der Beschluss wäre falsch.

**Nebenbefund: `is_nuc_predicate` hat null Aufrufstellen** — nicht im Paket, nicht in `tools/`,
nicht in den Tests, in keiner Spec-Datei. Die Löschung ist vorgeschlagen und **nicht**
entschieden; sie bleibt offen. Solange die Funktion steht, wird sie mitgeprüft, sonst entstünde
dieselbe Asymmetrie neu, die dieser Eintrag schliesst.

### D214 — Abnahme `00s`, kein Defekt im Lauf; der Defekt lag zweimal in der Erwartung

**Der Lauf.** `4aefa5d`, zwei Dateien, `44 +` und `3 -`. `predicates.py` bekommt die Wache und
die verengte Fangweite, `test_predicates.py` acht Prüfpunkte. Beide Eingriffe stehen so, wie D213
sie entschieden hat; `is_nuc_predicate` bleibt, `verifier.py` ist unangetastet, kein Scope-Zuwachs.

**Die Mengen weichen um zwei Zeilen von der Vorabmessung ab**, `6 -2` statt `5 -1` in
`predicates.py`. Die Differenz sind vollständig die zwei Docstring-Zeilen, die der Prompt verlangt
hat. Die geänderte Zeile in `is_nuc_name` misst 103 Zeichen; nach D205 ist das für Python
zulässig, kein Befund.

**Die Proben haben getan, was sie sollten.** Probe A — Wache entfernt, Verengung stehen gelassen —
ergab **9 rot, 588 grün**, und die neunte Zeile war `test_nuc_name_bytes_p_returns_false`. Damit
ist die Kopplung belegt: die verengte Fangweite hängt an der Wache und an nichts sonst. Probe B —
Verengung zurück, Wache stehen gelassen — blieb **597 grün** und belegt die Behauptung von D213,
dass die Verengung kein Verhalten ändert. Eine Probe, die grün bleiben **muss**, ist hier keine
leere Übung, sondern die Aussage selbst.

**Was der Lauf sonst belegt.** Vor `00s` liess sich die Wache nicht einmal vermissen: die Variante
ohne sie lief mit 589 grün durch. Erst die acht Prüfpunkte machen die Divergenz sichtbar, die seit
D181 auf der offenen Liste stand.

**Befund, nicht blockierend: die vier Formen stehen zweimal als Literal-Liste**, einmal je
`parametrize`. Wer eine fünfte ergänzt, ergänzt sie an einer Stelle, und die andere deckt sie
still nicht mehr ab — dieselbe Driftform wie bei den sechs Kopien von `_is_nuc_name` (D181), nur
klein und im Testcode. Eine Modulkonstante behebt es. Nicht jetzt: die Behebung kostet einen
eigenen Lauf und reist beim nächsten mit, der `test_predicates.py` ohnehin anfasst.

**Der Fehler dieser Runde lag beim Supervisor, zweimal.** Erst wurde `d9db6fc` als Kopfstand
behauptet, obwohl der Übergabe-Commit darüber lag; dann `52b464c` als `main`, obwohl der
D213-Commit dazwischen lag und nur nicht gepusht war. Beide Male stimmte der Baum und die
Erwartung nicht. Beide Male stammte die Zahl aus dem zuletzt **gesehenen** Zustand statt aus dem,
den der vorige Block hinterlassen hat. Daraus **Prüfregel 40**.

**Offen bleibt** die Löschung von `is_nuc_predicate` — vorgeschlagen, nicht entschieden (D213).

### D215 — Die Zeiger im Code werden geprüft, nicht nur berichtigt

**Der Befund: es sind drei Zeiger, nicht zwei.** D212 hat die Zeile dazwischen übersehen.
`mensch_als_republik/findings.py` führt:

| Zeile | steht | Aussage der Zeile | Anker |
|---|---|---|---|
| 1 | `00 §5.4` | eigener Enum, kein Claim-Reject | `00 §10`, wörtlich |
| 16 | `00 §5.4` | Vermerk mit Subjekt, `constitution_hash` | `00 §10` |
| 23 | `04-prompt.md §2` | sortiert und dedupliziert | `00 §10`, wörtlich |

Zeile 16 nennt D164 und zeigt auf einen Abschnitt, der nach D212s eigenem Satz nur das Subjekt
von `MALFORMED_NUCLEUS_KEY` trägt. Derselbe Defekt wie in Zeile 1, nur an einer dritten Stelle,
und deshalb hat ihn dieselbe Durchsicht nicht gesehen: gesucht wurde nach einer falschen
Aussage, gefunden wurde eine Adresse, die für die halbe Aussage stimmt.

**Der Zwilling bleibt stehen.** `mensch_als_republik/governance/findings.py` trägt denselben
`dedupe_sort`-Docstring mit `04-prompt.md §2`. Dort ist er richtig: Governance ist Schicht 04,
der Verweis bleibt in der eigenen Schicht. Schichtübergreifend war nur die Kopie im Nukleus.
`04-prompt.md` bleibt normativer Text — `policy.py` und `tests/governance/test_anchors.py`
zeigen weiter darauf.

**Beschluss.** Alle drei Zeilen nennen `00 §10`. **Verworfen: `00 §5.4` in Zeile 16 neben
`00 §10` stehen lassen.** Der Abschnitt trägt dann die schwächere Hälfte einer Aussage, deren
starke Hälfte daneben steht; die Spur zur Herkunft führen die D-Nummern, nicht ein zweiter
Abschnittsverweis.

**Die Prüfung dahinter.** `tools/check_specs.py` prüfte `ROOT.glob("*.md")`. Docstrings waren
ungeprüft, und genau deshalb hat der falsche Zeiger überlebt. `check_section_refs` läuft
zusätzlich über alle `.py` unter der Wurzel: 120 Dateien, 60 Verweise der Form `NN §X.Y`.
Ein Befund vor der Berichtigung — `tests/trust/test_distanzkauf.py` nannte `02 §2.7`, und
`02` hat unter `§2` überhaupt keine Unterabschnitte. Die Aussage der Zeile, `⌊n·C(I)/D⌋` und
`E⁺ = {cap ≥ 1}`, steht in `02 §3`.

**Verworfen: `check_escapes` und `check_control_chars` mitlaufen lassen.** Python führt legitime
Backslashes — Regex-Klassen, Byte-Literale. Die beiden Prüfungen fangen Editor-Schaden in Markdown
und meldeten hier nur Rauschen.

**Die Reichweite, ausdrücklich.** Geprüft wird, ob die Adresse existiert, nicht ob sie die
Aussage trägt. Den Defekt aus D212 hätte diese Prüfung **nicht** gefangen, weil `00 §5.4`
existiert. Sie fängt jeden Zeiger, der auf einen gelöschten oder umnummerierten Abschnitt zeigt
— die kleinere Klasse, aber die einzige, die maschinell entscheidbar ist.

**Die doppelte Formenliste**, Befund aus D214, wird zur Modulkonstante `NICHT_STR_FORMEN`. Die
Probe ist eine Differenz, keine Rücknahme: eine fünfte Form ergänzt ergibt in der neuen Fassung
zwei zusätzliche Prüffälle (23 auf 25), in der alten an nur einer der beiden Literal-Listen
ergänzt einen (23 auf 24). **Verworfen: den zweiten `parametrize`-Block streichen und die drei
Prüfer in den ersten Test ziehen.** Das mischt zwei Aussagen in einen Prüffall — dass
`parse_predicate` wirft, und dass die Prüfer nicht werfen. Fällt eine, sagt die Fehlermeldung
nicht welche.

**Was ohne Probe bleibt.** Die drei Zeiger in `findings.py` bekommen keine rote Probe; ihre
Rücknahme lässt auch die neue Prüfung grün. Die Abnahme ist dort der Diff.

### D216 — `is_nuc_predicate` wird gelöscht

**Korrektur an D213.** Der Nebenbefund dort — null Aufrufstellen, „nicht in den Tests" — ist seit
`00s` veraltet: `tests/test_predicates.py` ruft die Funktion in
`test_praedikatpruefer_non_str_p_returns_false` auf. Die Aufrufstelle ist von dem Lauf angelegt
worden, der die Funktion mitgeprüft hat.

**Die Substanz hält.** Null Produktiv-Aufrufstellen, im Paket wie in `tools/`, in keiner
Spec-Datei. Die einzige Aufrufstelle prüft die Funktion auf eine Eigenschaft ihrer selbst. Eine
Funktion, deren ganze Rechtfertigung ist, dass sie geprüft wird, rechtfertigt sich zirkulär.

**Beschluss: löschen**, neun Zeilen, dazu der Import und eine von drei Zusicherungen im
Prüffall. `_NUC_PREDICATE` verwaist dabei nicht — die Regex wird von `parse_predicate` selbst
benutzt, nicht vom Wrapper.

**Verworfen: behalten wegen der Fangbreite aus D213.** Die Gleichheit der Fangbreite ist eine
Eigenschaft der Wache in `parse_predicate`, nicht der Zahl der Wrapper. Sie bleibt für die
verbleibenden zwei wahr. D213s Satz, die Funktion werde mitgeprüft solange sie steht, ist eine
Regel für das Behalten und kein Grund dafür.

**Verworfen: behalten wegen der Symmetrie zu `is_core_predicate`.** Die Symmetrie ist keine:
`is_core_predicate` trägt acht Produktiv-Aufrufstellen in `verifier.py` und `index.py`. Zwei
Funktionen sehen gleich aus und stehen ungleich im Baum; die Bauform nachzubilden ist kein
Zweck.

**Verworfen: den Lauf nicht anfassen, weil `00s` eine Runde alt ist.** Die Löschung wickelt
nichts Normatives zurück. Wache und verengte Fangbreite aus D213 bleiben unberührt.

**Ohne rote Probe, und das ist die Aussage.** Es gibt keinen Aufrufer, der rot werden könnte —
das ist der Grund für die Löschung und zugleich der Grund, warum sie sich nicht durch einen Test
belegen lässt. Der Beleg ist der Grep über den Baum. Wer die Funktion wieder einführt, braucht
einen Produktiv-Aufrufer, den dieser Eintrag nicht gemessen hat.

### D217 — Abnahme `00t`, kein Defekt; die Vorabvariante war an einer Stelle schlechter

**Der Lauf.** `91410c2`, fünf Dateien, `50 +` und `33 -`. Alle vier Eingriffe stehen so, wie
D215 und D216 sie entschieden haben. Die Nicht-Ziele halten: `governance/findings.py`,
`policy.py`, `tests/governance/test_anchors.py`, `verifier.py` und `index.py` sind unberührt.
597 Tests, `ruff` sauber, `check_specs.py` meldet 120 Dateien und 60 Verweise.

**Die Abweichung von vier Zeilen ist begründet, und die Begründung dreht die Richtung um.**
`tools/check_specs.py` wuchs um 37 statt der vorab gemessenen 33 Zeilen. Zwei der vier
bezahlen eine Gruppierung der Befunde je Datei — und damit eine Zählung, die die Vorabvariante
des Supervisors **falsch** hatte: dort erhöhte ein einziges `failures += 1` den Zähler für alle
Python-Befunde zusammen, sodass zwei defekte Dateien als eine gemeldet worden wären. Der Prompt
verlangte, Befunde würden gezählt wie die übrigen; das Werkzeug hat den Prompt befolgt und nicht
die Variante. Daraus **Prüfregel 41**.

Die beiden übrigen Zeilen sind der Docstring der neuen Prüffunktion und der Zweig für
`read() is None`. Letzterer führt nebenbei eine UTF-8-Prüfung für Python ein, die der Prompt
nicht verlangt hat. Sie ist gemeldet und nicht still gebaut, inhaltlich richtig — Python-Quelltext
ohne Deklaration ist UTF-8 — und ohne sie stünde an der Stelle ein `TypeError`. Kein Befund.

**Die Proben haben getan, was sie sollten.** Probe A ergab Rückgabewert 1 mit genau einer
Meldung und nach dem Zurücksetzen wieder 0. Probe B ergab 25 statt 23 Prüffälle; die zwei
zusätzlichen belegen, dass beide `parametrize` an derselben Liste hängen.

**Was D212 übersehen hat, war eine Zählung.** Der Eintrag benannte zwei Zeiger und reparierte
damit zwei von drei. Der dritte stand zwischen ihnen und zeigte für die halbe Aussage richtig —
`00 §5.4` trägt das Subjekt aus D163, nicht das aus D164. Wer eine Defektklasse repariert,
zählt zuerst ihre Vorkommen; wer die gefundenen repariert, repariert die gefundenen.

**Neue Messung für den D209-Fork.** In den Python-Dateien stehen **260** Paragraphenverweise,
davon **201 ohne Ziffernpräfix**, verteilt über siebzig Dateien. Die neue Prüfung erfasst 59
von 260, knapp ein Viertel. Eine Zuordnung Verzeichnis auf Schicht wäre der billige Weg, ist
aber nicht sauber: `mensch_als_republik/policy.py` nennt `00 §3` und daneben die Prompt-Datei
der Schicht 04. Der Fork bleibt offen und ist grösser, als der Sitzungsstart nahelegte.

### D218 — Was die Literatur zum Entwicklungsloop hergibt; drei Forks, zwei Verwerfungen

**Anlass.** Prüfregel 15 verlangt, dass nachgesehen wird, was ausserhalb von MaR zu einer Gabelung
gefunden wurde, bevor sie geschlossen wird. Die Gabelung war hier der eigene Loop: Oli als
Operator, Claude als Supervisor, ein Werkzeug als Werkstatt. Vier Befunde tragen, der Rest ist
Wiederholung davon.

**Der Verifikationsaufwand ist der unsichtbare Posten.** METRs randomisierter Versuch (Becker,
Rush, Barnes, Rein, 2025): sechzehn erfahrene Entwickler, 246 echte Aufgaben in Repositories, die
sie selbst pflegen. Mit AI-Werkzeugen 19 Prozent langsamer, geschätzt 20 Prozent schneller. Die
Nachfolgeuntersuchung 2026 hielt bei etwa achtzehn Prozent Verlangsamung. Die Bedingungen sind
unsere: erfahrene Beitragende, reife Codebasis, hohe Qualitätsansprüche. Der genannte Mechanismus
ist, dass der schnelle erste Schritt erinnert wird und der langsame Verifikationsschritt nicht.

**Qualitätssicherung muss mit der Geschwindigkeit mitwachsen.** He, Miller, Agarwal, Kästner,
Vasilescu (MSR 2026), Difference-in-Differences über 806 Repositories: rund 29 Prozent mehr
hinzugefügte Zeilen, 30 Prozent mehr Static-Analysis-Warnungen, 42 Prozent mehr Komplexität. Der
Geschwindigkeitsgewinn war vorübergehend, die Qualitätsverschlechterung blieb. Der Kausalpfad
läuft über Tempo auf Codemenge auf technische Schuld — die Werkzeuge verstärken bestehende
Dynamiken, statt eigene Fehlerarten einzuführen.

**Einfache Pipelines schlagen autonome Agenten.** Xia, Deng, Dunn, Zhang (FSE 2025, Agentless):
Lokalisierung, Reparatur, Validierung, ohne dass das Modell über den nächsten Schritt entscheidet
— bei besserer Lösungsrate und rund einem Fünftel der Kosten agentischer Aufbauten. Die
Begründung ist die für uns wichtige: ein falscher Schritt wird verstärkt und verdirbt alle
folgenden Entscheidungen.

**Kontexte kollabieren, wenn man sie neu schreibt statt sie zu ergänzen.** Zhang et al. (ICLR
2026, ACE) benennen zwei Fehlerarten: brevity bias, bei dem Fachwissen zugunsten knapper
Zusammenfassungen wegfällt, und context collapse, bei dem wiederholtes Umschreiben Details
erodiert. Die Antwort sind inkrementelle Aktualisierungen statt monolithischer Neufassung.

**Einordnung.** Galster et al. (AIware 2026) haben 2853 Repositories vermessen: Kontextdateien
dominieren und sind oft der einzige Mechanismus; über 85 Prozent der Skills tragen keine
ausführbaren Ressourcen, und kein einziges Repository nutzt das persistente Subagent-Gedächtnis.
Register, Prüfregeln und `tools/` liegen deutlich darüber. Der Kern des Loops ist damit gedeckt
und wird nicht angefasst.

**Drei Forks werden eröffnet, keiner entschieden.**

1. **Die Sitzungsstart-Datei ist ein monolithisches Rewrite.** Gemessen über zwölf Dateien wächst
   die offene Liste von 22 auf 31 Punkte — in der Summe **kein** Kollaps, und damit ein
   Gegenbefund zur These. Von sieben Punkten, die zwischen `00r` und `00u` verschwanden, waren
   sechs erledigt; einer nicht: der Vermerk aus D211, dass `register_index.py` `VISION` erkennt,
   obwohl das in keinem Auftrag stand. Ein belegter Scope-Zuwachs ist beim Umschreiben aus der
   Historie gefallen. Vorgeschlagen ist, die offene Liste in eine nur per Splice editierte Datei
   herauszulösen, sodass eine Streichung eine Änderung ist und kein Weglassen. Kosten: ein Lauf.
   Dagegen spricht eine zwölfte Datei im Wurzelverzeichnis und dass der Sitzungsstart aufhört,
   allein als Einstieg zu genügen.

2. **Es gibt keine Kontextdatei für das Werkzeug.** Der Tokengewinn wäre klein: die Prompts
   messen 81 bis 191 Zeilen, davon drei bis acht stehende. Der Gewinn liegt woanders — in `00t`
   musste der Satz, dass D205 keine Zeilenlängenregel für Python setzt, von Hand in die
   Nicht-Ziele. Solche Sätze gehören einmal ins Repository. Dagegen spricht, und es wiegt: eine
   ständig gelesene Datei ist der Kanal, über den stiller Scope-Zuwachs entsteht.

3. **Die Projektkopie des Supervisors hat kein Nachziehverfahren.** Sie stand während dieser
   Sitzung vier Commits hinter `main` und kannte D215 bis D217 nicht. Der billige Schritt ist ein
   repomix-Lauf nach dem letzten Push, dessen Kopfzeile Commit, Testzahl, Registerstand und
   Prüfregelzahl trägt — dann ist die Kaltmessung ein Hash-Abgleich statt einer
   Anforderungsrunde. Das Verfahren steht in `sitzungsstart-00u.md`; ein Beschluss ist es nicht,
   solange nichts es erzwingt.

**Verworfen: Subagenten und Multi-Agent-Orchestrierung.** Die gemessene Verbreitung ist niedrig,
der Nutzen gegenüber Kontextdateien unbelegt, und ein zweiter autonomer Kanal bricht die Regel,
dass die Kanäle nur über Commits reden. Genau diese Regel macht den Loop überhaupt prüfbar.

**Verworfen: die Werkzeugketten für spec-driven development** (Spec Kit, Kiro und Verwandte). Sie
erzeugen, was `07-decisions.md` bereits führt, und mit schwächerer Begründungspflicht. Wer sie
wieder aufmacht, braucht eine Aussage, die das Register nicht tragen kann.

### D219 — Die Buchstabenpräfixe der Zitierkonvention werden gebunden (D209, Teil A)

**Anlass.** D209 hat die Zitierkonvention als nicht injektiv benannt und die Position von der
Messung getrennt. Teil A ist gemessen, auf `ef807e2`: einunddreissig Verweise der Form `NNx §Y`
in `.md` und `.py` zusammen, verteilt auf fünfzehn Dateien, mit vier benutzten Namen.

**Die Messung schliesst den Fork, statt ihn zu eröffnen.** Die drei Abnahme-Dateien führen keine
einzige nummerierte Überschrift; sie gliedern nach `## Teil A` und `### D41`. Damit kann keine
von ihnen unter der geltenden Konvention Zitierziel sein, und die vermutete Zweideutigkeit ist
keine.

| Name | Verweise | zitierte Abschnitte | Zitierziel | ohne Nummern |
|---|---|---|---|---|
| `02a` | 24 | 2.1, 2.3, 2.4, 2.6, 2.7, 2.10, 3, 4, 5 | `02a-maxflow-prompt.md` | `02a-abnahme.md` |
| `01a` | 3 | 3.3, 4 | `01a-policy-prompt.md` | `01a-nachtrag-prompt.md` |
| `02b` | 2 | 2 | `02b-golden-anchors.md` | `02b-abnahme.md` |
| `04a` | 2 | 6 | `04a-korrektur-prompt.md` | — |

Die Zitierziele führen 19, 16, 12 und 8 nummerierte Überschriften; die drei Dateien rechts
führen null.

**Entscheidung, drei Teile.** Erstens erhält `LAYER_FILES` in `tools/check_specs.py` die vier
Einträge oben. Zweitens erlaubt `SECTION_REF` einen optionalen Kleinbuchstaben hinter dem
Ziffernpaar. Drittens ist ein Buchstabenname ohne Tabelleneintrag ein **Befund**, keine
Auslassung — das ist die Injektivität, die D209 will: ein Zitiername ohne gebundene Datei ist
der Defekt selbst. Der Preis ist benannt und erwünscht: wer eine Prompt-Datei mit
Buchstabennamen anlegt und daraus zitiert, wird rot, bis er die Tabelle ergänzt.

**Zahlen.** In Python stehen 260 Paragraphenverweise. Vor der Änderung prüft `check_specs.py` 60
davon, danach 75; 185 bleiben präfixlos und ungeprüft. Der Sitzungsstart nennt für die
präfixlosen 201 — das war eine Handzählung, die gemessene Zahl ist 185. Die Erweiterung läuft
grün: kein einziger der einunddreissig Verweise zeigt ins Leere.

**Verworfen: eine der Dateien umbenennen.** Es gibt nichts umzubenennen, was die Prüfung
brauchte. Ein Dateiname, der einen vergangenen Lauf beschreibt, wird nicht umgeschrieben, damit
eine Tabelle ihn nicht führen muss.

**Verworfen: die Regex aus den Tabellenschlüsseln bauen.** Das ist der kürzere Weg und der
schlechtere: ein Name ohne Eintrag trifft die Regex dann nicht mehr und verschwindet still.
Genau die stille Klasse ist der Gegenstand.

**Verworfen: Teil B mitziehen.** Die 185 präfixlosen Verweise brauchen eine eigene Position; eine
Zuordnung Verzeichnis auf Schicht trägt nicht, weil `mensch_als_republik/policy.py` `00 §3` und
die Prompt-Datei der Schicht 04 nebeneinander nennt. Teil B bleibt offen und ist kein Anhängsel.

**Probe.** Für `tools/check_specs.py` gibt es keinen Test; die Rücknahmeprobe ist der Lauf selbst.
Wird ein Tabelleneintrag entfernt, muss `make check-specs` rot werden.

### D220 — Teil B der Zitierkonvention ist vermessen, nicht entschieden (D209)

**Anlass.** D219 hat Teil A geschlossen. D209 hat Teil B — die präfixlosen Paragraphenverweise in
Python — ausdrücklich als eigene Position offengelassen. Diese Messung ist die Vorarbeit dazu und
enthält **keine Entscheidung**. Sie steht im Register, weil die Zahlen sonst wieder aus der
Historie fallen: der Sitzungsstart führte 201 präfixlose Verweise, gemessen sind 185.

**Zahlen, gemessen auf `253d649`.** In `.py` stehen 260 Paragraphenverweise. 75 tragen ein
Präfix und werden seit D219 geprüft. Die übrigen 185 sind präfixlos. Gegen die acht Layer-Dateien
gehalten:

| Befund | Zahl |
|---|---|
| trifft Überschriften in **mehr als einer** Layer-Datei | 146 |
| trifft genau eine Layer-Datei | 30 |
| trifft keine Layer-Datei | 9 |

**Damit ist jede Heuristik über die Abschnittsnummer erledigt.** Bei 146 von 185 identifiziert die
Nummer die Schicht nicht. Ein Verfahren, das aus `§2.2` die Datei ableitet, rät in vier von fünf
Fällen.

**Die neun ohne Treffer sind keine Defekte.** Sie zeigen aus dem Zuständigkeitsbereich der
Layer-Dateien heraus. `mensch_als_republik/policy.py` nennt Abschnitt 0.2 der Datei
`04-prompt.md`, `tests/trust/test_coupling.py` zweimal Abschnitt 0 von `03-prompt.md`; beide
Abschnitte gibt es. Der Rest sind Fortsetzungen: `mensch_als_republik/trust/graph.py` nennt in
Zeile 1 die Abschnitte 2.7 und 2.8 der Datei `02a-maxflow-prompt.md` und schreibt in späteren
Docstrings desselben Moduls nur noch die Nummer.

**Verzeichnis auf Schicht trägt nicht.** Gegen die Annahme, das Paketverzeichnis nenne die
Schicht: 98 Verweise gedeckt, 18 widerlegt, 69 in Dateien ohne Schichtverzeichnis. Die 98 sind
schwaches Material, weil dieselben Verweise zu grossen Teilen ohnehin mehrdeutig sind. Von den 18
zeigen mehrere auf die Anchor-Dateien statt auf die Layer-Datei — `tests/profiles/test_credit.py`
auf Abschnitt 8, `tests/trust/test_pagerank_invariants.py` auf Abschnitt 11.

**Fünf Namensformen sind im Umlauf.** Das ist der eigentliche Befund. D209 hat die Injektivität
für die ersten beiden Formen gefragt; die anderen drei standen nirgends.

1. `NN` — die Layer-Datei. Geprüft seit D209.
2. `NNx` — Prompt- und Anchor-Dateien mit Buchstabennamen. Gebunden seit D219.
3. `NN-golden-anchors.md` — vier Dateien, ungebunden.
4. `NN-prompt.md` — ungebunden, teils ohne Endung zitiert (`03-prompt`).
5. Der bare Verweis, der ein zuvor im selben Modul genanntes Präfix fortsetzt.

**Keine Entscheidung, aber eine festgehaltene Reihenfolge.** Zuerst ist zu entscheiden, welche
Namensformen zulässig sind und woran jede gebunden wird. Danach, was ein barer Verweis bedeutet:
Fortsetzung im Modulkontext, Verweis auf die eigene Schicht, oder unzulässig. Erst danach die 185.
Wer mit den 185 anfängt, entscheidet die beiden Fragen davor nebenbei und ohne Begründung — genau
die stille Normativität, gegen die das Register steht.

**Nicht entschieden und ausdrücklich offen:** ob die 185 qualifiziert werden, ob ein
Verzeichnis-Mapping kommt, ob bare Verweise verboten werden.

### D221 — Die Zitiergrammatik hat zwei Namensformen (D209 Frage 1, berichtigt D220)

**Berichtigung zuerst.** D220 hat 185 präfixlose Verweise in Python gezählt und sie gegen die
Layer-Dateien gehalten: 146 mehrdeutig, 30 eindeutig, 9 nirgends. Die Messung war falsch. Sie hat
nur `NN`- und `NNx`-qualifizierte Verweise abgezogen, nicht die dateinamensqualifizierten. Von
den 185 tragen **112 sehr wohl einen Namen** — den Dateinamen. Wirklich bar sind **73**, davon
62 mehrdeutig, 5 eindeutig, 6 nirgends. Die Aussage von D220 hält damit unverändert und anteilig
schärfer, aber die Zahlen dort sind zu ersetzen. Der Fehler liegt beim Supervisor, nicht am
Werkzeug: dieselbe Lücke ist in derselben Sitzung zweimal aufgetreten, weil eine Regex das Wort
vor dem Paragraphenzeichen nicht als Namen gelesen hat.

**Die Dateinamensform ist die grösste ungeprüfte Klasse.** Gemessen auf `d39daec`, über `.md` und
`.py`:

| Form | Verweise | geprüft |
|---|---|---|
| `NN` (Kurzform Layer) | 860 | ja, seit D209 |
| Dateiname, `.md` optional | 321 | nein |
| bar | 73 in `.py` | nein |
| `NNx` (Kurzform Anhang und Prompt) | 31 | ja, seit D219 |

**Entscheidung: zwei Namensformen, mehr nicht.**

1. **Der Dateiname**, mit oder ohne `.md`. Diese Form ist injektiv von selbst — der Name **ist**
   die Datei, sie braucht keinen Tabelleneintrag und trägt jede künftige Datei ohne Pflege. Sie
   trägt heute schon 321 Verweise.
2. **Die Kurzform `NN` und `NNx`** als Abkürzung, gebunden durch `LAYER_FILES`. Die Tabelle ist
   damit ein **geschlossener** Satz von dreizehn Einträgen. Sie wächst nicht mehr, weil Form 1
   jede neue Datei trägt.

Alles andere ist ein Befund. Keiner der 1212 bestehenden qualifizierten Verweise muss angefasst
werden; die Entscheidung kostet keine Migration.

**Ein fehlender Dateistamm ist kein Befund.** Gemessen: dreizehn Verweise zeigen auf
`fuzz-prompt.md` und `sim-prompt.md`, die `ab73450` gelöscht hat. Kein einziger ist ein Defekt —
neun stehen in der Umzugstabelle in `welten-prompt.md`, die den Umzug angeordnet hat, vier im
Register. Beide Fundorte **erwähnen** den toten Namen als linke Spalte, sie **benutzen** ihn
nicht, und syntaktisch sind die Fälle nicht zu trennen. Wer hier einen Befund erhebt, braucht eine
Ausnahmeliste, und die verrottet. Der Preis wird benannt: ein vertippter Dateiname fällt durch.

**Verworfen: die Anhangs-Zielform mitbauen.** Verweise wie `§B.2` gibt es, und `01-claim-atom.md`
führt fünfzehn Anhangsüberschriften. Aber gemessen ist jeder solche Verweis heute **bar** — ohne
Dateinamen davor. Eine Erweiterung von `HEADING_NUM` hätte null Wirkung und wäre Umfang ohne
Messung. Die Anhangs-Zielform gehört zu Frage 2 und wird dort entschieden.

**Drei tote Zeiger, mit ihren Zielen.** Die Erweiterung macht sie sichtbar; sie werden im selben
Lauf berichtigt, sonst landet die Prüfung rot:

1. `distanzkauf-prompt.md` nennt `02-trust-flow.md §2.7` für den BFS-Kapazitätsfilter und Anker
   K8. Die Nummer stimmt, die Datei nicht: der Abschnitt steht in `02a-maxflow-prompt.md`.
2. `02b-abnahme.md` nennt `02b-golden-anchors.md §10.1`. Die Datei hat kein `§10.1`; gemeint ist
   Punkt 1 der Liste in `§10`. Der Verweis geht auf `§10`. Dass die Prüfung Listenpunkte nicht
   von Unterabschnitten trennt, ist der offene Punkt aus D209 und bleibt offen.
3. `welten-prompt.md` nennt `01-claim-atom.md §6.7` für `INCOHERENT_EXPIRY`. Die Aussage steht in
   Anhang B.2. Da die Zielgrammatik Anhänge nicht trägt, wird der Verweis in Prosaform gesetzt,
   ohne Paragraphenzeichen.

**Dazu ein toter Zeiger in der Spec selbst.** Die Tabelle in `01-claim-atom.md` Anhang B.2 führt
hinter der Definition von `INCOHERENT_EXPIRY` den baren Verweis auf einen Abschnitt 6.7, den es
nicht gibt. Die Zelle definiert die Bedingung vollständig; der Zeiger trägt nichts, was sie nicht
schon sagt. Er wird gestrichen statt umgehängt.

**Erwartung an den Lauf.** Die Python-Zeile geht von 75 auf **187** Verweise, insgesamt werden
**545** geprüft. Vor den vier Korrekturen meldet die Prüfung **genau drei** Befunde, danach
keinen. Übrig bleiben **73** bare Verweise in `.py`; das ist Frage 2 und nicht Gegenstand.

### D222 — Die 100-Zeichen-Grenze gilt für Prosa, nicht für Tabellenzeilen

**Anlass.** Die Grenze stand nie in einer Entscheidung. Sie wurde geübt, und sie hielt nur, weil
jeder Splice sie selbst assertete. Damit war sie weder prüfbar noch begründet — die schlechteste
Form von Normativität, und genau die, gegen die dieses Register steht. Für Python ist dieselbe
Frage mit D205 verneint worden; für Markdown war sie offen.

**Messung auf `0137a86`.** 27194 Zeilen in den `.md`-Dateien des Wurzelverzeichnisses, davon 268
über 100 Zeichen — 1,0 Prozent. Aufgeschlüsselt nach Art der Zeile:

| Art | über 100 |
|---|---|
| Tabellenzeile, auch im Blockzitat | 244 |
| Prosa | 21 |
| Zeile im Codeblock | 3 |

**Die Messung teilt die Frage in zwei Antworten.**

Für **Prosa** ist die Grenze keine Setzung, sondern eine Beschreibung. 21 Ausreisser auf 27194
Zeilen heisst: der Bestand hält sie zu 99,9 Prozent, ohne dass sie je geprüft wurde. Die meisten
liegen bei 101 bis 108 Zeichen und sind Umbrüche, keine Entscheidungen. Vier sind Altbestand —
522, 148, 143 und 131 Zeichen, unumbrochene Absätze.

Für **Tabellenzeilen** ist sie unerfüllbar. Eine Markdown-Tabellenzeile lässt sich nicht
umbrechen; die Grenze ist dort keine Formatierung, sondern eine Obergrenze für Spalteninhalt. 244
Verletzungen sind kein schlampiger Bestand, sondern das Format. Und sie hat in derselben Sitzung
Inhalt gekostet: die Tabelle in D219 musste gekürzt werden, eine Spalte ist der Grenze zum Opfer
gefallen und nicht einer Überlegung.

**Entscheidung.** Für `.md`-Dateien im Wurzelverzeichnis gilt: **Prosa höchstens 100 Zeichen**,
gezählt als Zeichen und nicht als Bytes. **Ausgenommen sind Tabellenzeilen** — auch die im
Blockzitat — **und Zeilen innerhalb eines Codeblocks**. Für Python gilt weiterhin keine Grenze
(D205).

**`07-decisions.md` und `sitzungsstart-*.md` werden mitgeprüft.** Sie sind von der Verweisprüfung
ausgenommen, weil sie vergangene Stände beschreiben und ein Zeiger dort eine historische Aussage
ist. Zeilenlänge ist keine Aussage über Inhalt. Der Preis ist eine Zeile im Register mit 522
Zeichen.

**Verworfen: semantische Umbrüche**, ein Satz je Zeile ohne Grenze. Für Diffs wäre das besser —
eine geänderte Formulierung bricht dann nicht den halben Absatz um. Der Bestand ist aber auf
27194 Zeilen hart umbrochen; die Umstellung wäre eine Migration ohne gemessenen Gewinn und machte
jeden älteren Diff unlesbar. Wer sie wieder aufmacht, braucht eine Messung, die diesen Preis
schlägt.

**Verworfen: die Grenze streichen.** Dass die Prosa sie ungeprüft zu 99,9 Prozent hält, ist das
stärkste vorliegende Argument dafür, dass sie trägt.

**Verworfen: Tabellenzeilen mit einer höheren Grenze führen**, etwa 140. Jede Zahl dort wäre
gesetzt statt gemessen, und der Bestand führt 22 Zeilen über 200.

**Erwartung an den Lauf.** Unter dieser Regel meldet eine Prüfung heute **21** Befunde in
**11** Dateien; die Zahl 13 im ursprünglichen Eintrag war von Hand gezählt und falsch. Sie
werden im selben Lauf umbrochen, sonst landet die Prüfung rot. Danach ist der offene Punkt
geschlossen und die Splices müssen die Grenze nicht mehr einzeln assertieren — sie dürfen es
weiter tun, ein zweiter Wächter schadet nicht.

### D223 — Abnahme `00w`, kein Defekt; die Stummelzeilen sind der Preis und bleiben

**Abnahme.** `00w` hat die Prosagrenze aus D222 prüfbar gemacht und die einundzwanzig Zeilen
umbrochen. `make check-specs` grün, 597 Tests, `ruff` grün. Beide Proben sind rot geworden: P1 mit
21 Befunden in 11 Dateien in genau der Verteilung aus dem Prompt, darunter einer in
`07-decisions.md` — der belegt, dass die Ausnahme für Register und Sitzungsstart auf die
Zeilenlänge nicht angewandt wird. P2 hat drei Klassen zugleich geprüft und genau einen Befund
gemeldet: die Prosazeile, nicht die gleich lange Tabellenzeile und nicht die Zeile im Codeblock.

**Damit ist der offene Punkt geschlossen.** Die 100-Zeichen-Regel war seit ihrer Einführung
ungeprüft und hielt nur, weil jeder Splice sie selbst assertete. Sie hält jetzt, weil `make
check-specs` sie hält.

**Die Nebenwirkung, benannt statt repariert.** Der Prompt verlangte einen Umbruch je Zeile und
keine Neuumbrechung des Absatzes, gebunden durch ein Abnahmekriterium, das die Löschungen je
Datei auf die Befundzahl festnagelte. Das erzeugt Stummelzeilen: von 46 neuen Zeilen sind 17
kürzer als 40 Zeichen, darunter `Befund,` und `Lauf,` als eigene Zeile. Das ist hässlich und
bleibt so. Ein Reflow der elf Absätze hätte einen Diff erzeugt, den niemand Wort für Wort
nachprüfen kann, und Abnahmekriterium 4 — kein Wort verändert — wäre nicht mehr belegbar gewesen.
Wer die Absätze später glättet, tut es als eigenen Lauf mit eigener Begründung, nicht nebenbei.

**Zwei Handzählungen dieser Sitzung waren falsch**, beide vom Supervisor: die erwartete
`numstat`-Zeile für D221 (72 statt gemessener 66) und die Dateizahl in D222 (13 statt gemessener
11). Beide standen in einem Satz, der mit einer Messung hätte belegt werden können und es nicht
war. Die zweite stand bereits committet auf `main` und ist mit dem Prompt-Commit zu `00w`
berichtigt worden.

**Daraus Prüfregel 42.** Der erste Anlauf der Berichtigung an D222 ersetzte einen Teilstring und
prüfte die Zeilenlänge am **eingesetzten Text**. Der war unter 100 Zeichen; die Zeile, die im
Ergebnis daraus entstand, hatte 149. Ein Assert über den Einsatz sagt nichts über die Datei.

### D224 — Die Projektkopie wird nach jedem Push nachgezogen (D218, Fork 3)

**Anlass.** D218 hat als dritten Fork benannt, dass es für die Projektkopie kein erzwungenes
Nachziehverfahren gibt. Diese Sitzung hat den Preis vorgeführt: über vier Merges hinweg hat der
Supervisor auf einer Kopie gerechnet, in der `tools/check_specs.py` nicht die Fassung des
Werkzeugs trug, sondern seine eigene Rekonstruktion des gemeldeten Diffs. Die Zahlen stimmten
trotzdem — das war kein Beleg, sondern Glück.

**Entscheidung.** Nach **jedem** Push, nicht nach jeder Sitzung, läuft repomix. Drei Teile:

1. **Ziel `/tmp`**, nicht das Arbeitsverzeichnis. Die alte Ablage in der Wurzel hat in dieser
   Sitzung eine unversionierte Datei im Baum hinterlassen, die in der Kaltmessung als offener
   Posten auftauchte und erst nachträglich erklärt werden konnte.
2. **Der Kopf trägt fünf Kaltzahlen** — Commit, Testzahl, Registerstand, Prüfregelzahl,
   Branchzahl. Damit kann die nächste Sitzung ihren ersten Griff gegen den Kopf machen statt
   gegen eine Erinnerung.
3. **Ein Wächter zählt gegen.** Gepackte Dateien gegen versionierte. Der Security-Check von
   repomix kann Dateien stillschweigend auslassen, und dieses Repo führt Hex-Vektoren und
   Byte-Testfälle. Im ersten Lauf: 219 gepackt, 218 versioniert — ein Überschuss durch eine
   unversionierte lokale Datei, also die harmlose Richtung.

**Verworfen: Lesezugriff des Supervisors auf das Repository**, etwa über einen GitHub-Spiegel.
Er bräuchte ein Credential, das zwischen Sitzungen nicht gehalten werden kann und sonst je
Sitzung in den Chat getippt würde. Er schüfe eine zweite Wahrheitsquelle neben Gitea, während die
dauerhafte Anweisung genau eine kennt. Und das Repository verliesse das LAN. Der Gewinn gegenüber
dem Nachziehen je Push ist ein gesparter Handgriff des Operators.

**Verworfen: `--compress`.** Streicht Funktionsrümpfe und lässt Signaturen stehen. Das ist genau
der Modulcode, der vor jedem Prompt gelesen wird.

**Verworfen: `--remove-comments`.** In diesem Repo tragen die Docstrings die
Paragraphenverweise. Die Option löschte den Gegenstand von D215, D219 und D221.

**Verworfen: `--remove-empty-lines` und `--output-show-line-numbers`.** Die erste verschiebt jede
Zeilennummer; `00v` und `00w` haben Zeilennummern in den Prompt geschrieben. Die zweite stellt
jeder Zeile eine Nummer voran und zerstört damit die Extraktion aus der Kopie.

**Verworfen: `--no-file-summary`.** Der `--header-text` wird nach der Doku innerhalb dieses
Abschnitts gerendert; ohne ihn fiele der Hash weg, der den Zweck trägt. Die Annahme ist beim
ersten Lauf nicht widerlegt worden.

**Gemessen und benannt: das Register wird gross.** Die Kopie umfasst 219 Dateien und 631113
Tokens. `07-decisions.md` allein trägt davon 140336, also 22,2 Prozent, und wächst mit jedem
Eintrag. Kein Handlungsbedarf heute; ein offener Punkt ab heute. Wer ihn aufmacht, misst zuerst,
ob eine Teilung nach Ären den Index aus `tools/register_index.py` trägt oder bricht.

**Daraus Prüfregel 43.**

### D225 — Zwei Änderungen am Takt, und eine zurückgenommene Sorge

**Zurückgenommen: das Register mache den Nachzug teuer.** D224 hat notiert, das Register sei
22,2 Prozent der Projektkopie und wachse. Der Anteil stimmt, die Folgerung nicht. Projektwissen
erlaubt unbegrenzt viele Dateien mit 30 MB je Datei; die Kopie misst 2,15 MB. Das Register mit
rund 500 KB ist ein Fünftel von etwas, das reichlich Platz hat. Es gibt heute keinen Engpass, und
eine Teilung nach Ären wäre Aufwand ohne gemessenen Anlass. Der offene Punkt bleibt als
Beobachtung stehen, nicht als Dringlichkeit. Wer eine Zahl als Anteil nennt, nennt den Nenner
dazu — sonst klingt Knappheit, wo keine ist.

**Was wirklich kostet, sind Runden.** Ein Werkzeuglauf braucht heute vier: Prompt hinaus, Bericht
zurück, Diff anfordern, Merge. Sechs Splices dieser Sitzung trugen je neun Zeilen reine
Zeremonie im Befehlsblock — Temp-Verzeichnis wegräumen, anlegen, Zieldateien kopieren,
hinwechseln, trocken laufen, zweiten Lauf prüfen, zurückwechseln, live laufen. 54 Zeilen, die der
Operator kopiert, und ebenso viele Stellen für einen falschen Pfad.

**Entscheidung 1: der Prompt verlangt den vollständigen Diff.** Im Abschluss steht künftig
`git diff` gegen den Branchpunkt, nicht nur `git diff --numstat`. Damit liegt der Diff in
derselben Runde vor wie der Bericht, und Abnahme und Merge fallen zusammen. Der Preis sind
Diff-Zeilen im Chat, die eine Runde später ohnehin gelesen worden wären. Unberührt bleibt, dass
**der Bericht nie die Abnahme ist**: geprüft wird weiterhin der Diff, nur früher.

**Entscheidung 2: ein Harness für Splices**, `tools/splice_run.py`. Ein Aufruf statt neun Zeilen.
Er lässt den Splice im Arbeitsverzeichnis laufen — **nicht** gegen eine Kopie —, erzwingt danach
das Scheitern des zweiten Laufs, prüft am Ergebnis die Zeilenlänge nach D222 und setzt bei jedem
Fehlschlag mit `git checkout --` zurück.

**Verworfen: das Temp-Verzeichnis beibehalten.** Der Trockenlauf gegen eine Kopie schützt die
Dateien vor einem fehlerhaften Splice. Genau das tut Git schon; die dauerhafte Anweisung führt
Schreiben im Arbeitsverzeichnis als Tier 2 mit Git als Rollback. Zwei Rollback-Mechanismen
nebeneinander sind einer zu viel, und der schwächere ist der handgeschriebene.

**Verworfen: den Baum vorher auf Sauberkeit zu prüfen und sonst nichts.** Der Harness prüft es,
aber die Prüfung allein genügt nicht — sie muss mit einem Rücksetzpfad verbunden sein, sonst
bleibt ein halb angewandter Splice liegen.

**Verworfen: ein eigenes Werkzeug für Registereinträge**, das aus Feldern einen Eintrag baut. Die
Einträge sind Prosa mit benannter Begründung; ein Formular erzeugt Formulare.

**Verworfen: die Kopie verkleinern** — durch `--compress`, Auslassen der Tests oder Auslassen des
Registers. D224 hat die ersten beiden schon verworfen; das dritte nähme dem Supervisor die
oberste Instanz.

### D226 — Abnahme `00x`, kein Defekt; zwei benannte Grenzen des Harness

**Abnahme.** `tools/splice_run.py` steht, 129 Zeilen, keine bestehende Datei geändert.
`check_line_length` war importierbar; eine zweite Fassung der Klassifikation ist nicht entstanden.
597 Tests, `ruff` grün. Alle drei Proben sind eingetreten: P1 hat den durchlaufenden zweiten Lauf
gefangen und den doppelten Anhang zurückgenommen, P2 die zu lange Prosazeile mit Nummer und Länge
gemeldet und zurückgesetzt, P3 **vor** dem ersten Lauf abgebrochen und die vorhandene Änderung
unangetastet gelassen.

**Grenze 1: der Längenvergleich zählt, er identifiziert nicht.** Der Harness vergleicht die
**Anzahl** zu langer Prosazeilen im Arbeitsstand mit der im Basisstand. Ein Splice, der eine zu
lange Zeile entfernt und eine andere einsetzt, läuft deshalb durch. Aus demselben Grund kann der
Bericht bei einem Abbruch alte Zeilen als neu ausweisen, wenn oberhalb eingefügt wurde: die
Befundstrings tragen Zeilennummern, und jede Einfügung verschiebt alles darunter. Das ist keine
Nachlässigkeit, sondern die Folge der Befundform, und eine Identifikation über den Zeileninhalt
statt über die Nummer wäre ein eigener Fork.

**Grenze 2: ein gescheiterter Splice kann eine unversionierte Datei hinterlassen.** Zurückgesetzt
wird über `git diff --name-only`, und das kennt nur versionierte Pfade. Das ist gewollt: die
Alternative wäre `git checkout .` oder `git reset --hard`, und beide räumen fremde Arbeit weg —
genau das, was P3 verhindert. Nach einem Fehlschlag ist der Baum also **nicht zwingend** sauber.

**Entscheidung 1 aus D225 hat sofort gewirkt.** `00x` war der erste Lauf, bei dem Abnahme und
Merge in derselben Runde lagen, weil der Prompt den vollständigen Diff verlangt hat.

**Dieser Eintrag ist der erste, den der Harness selbst anwendet.**

### D227 — Bare Paragraphenverweise in Python sind unzulässig (D220, D221 Frage 2)

**Anlass.** D221 hat Frage 1 der Zitiergrammatik entschieden und Frage 2 ausdrücklich offen
gelassen: was ein **barer** Verweis bedeutet. Drei Lesarten standen zur Wahl — Fortsetzung im
Modulkontext, Verweis auf die eigene Schicht, oder unzulässig. Der Sitzungsstart `00y` hat
verlangt, dass zuerst gemessen wird, wie viele der 73 jede Lesart trägt. Diese Messung liegt vor.

**Grundzählung, gemessen auf `b49358e`.** In `.py` stehen 266 Paragraphenzeichen. 187 tragen
einen auflösbaren Namen und werden seit D221 geprüft. 73 sind bar. Die übrigen 6 sind
Regex-Literale in `tools/check_specs.py` und `tools/register_index.py`; auf das Zeichen folgt
dort `(`, `{` oder ein Leerzeichen, sie fallen unter keine Verweisform und brauchen später keine
Ausnahme.

**Die Definition, die dabei scharf geworden ist.** Bar ist ein Verweis, dessen unmittelbar
vorangehendes Token **kein auflösbarer Zitiername** ist. `SECTION_REF` liest jedes ASCII-Wort vor
dem Paragraphenzeichen als möglichen Namen und verwirft es erst im Nachtest gegen `SPECS` und
`LAYER_FILES`. Sechzehn der 73 haben deshalb ein Wort davor — `aus §2.7`, `Kein §3.1`, und bei
`Gültigkeit §4.1` bricht der Regex am Umlaut und liest `ltigkeit`. Sie sind nicht qualifiziert,
sondern bar mit Vorlauf. Wer 187 von 260 abzieht, bekommt dieselbe 73 auf zwei verschiedenen
Wegen; nur der zweite Weg sagt, was die Zahl bedeutet.

**Lesart 1 — Fortsetzung im Modulkontext — trägt 41 von 73.** Gemessen: 47 der baren Verweise
haben überhaupt ein zuvor im selben Modul genanntes auflösbares Präfix, 26 haben keins. Von den
47 trägt das Vorgängerpräfix den Abschnitt in 41 Fällen, in 6 nicht.

**Die sechs Widerlegungen sind kein Rand, sondern ein Muster.** Zuletzt genannt wird oft eine
Anker- oder Prompt-Datei, gemeint ist die Layer-Datei:

| Fundstelle | Verweis | zuletzt genanntes Präfix |
|---|---|---|
| `mensch_als_republik/trust/graph.py:111` | `§2.7` | `02b` — hat kein `§2.7`, `02a` hat es |
| `mensch_als_republik/trust/params.py:14` | `§2.2` | `02` |
| `tests/helpers.py:55` | `§2.3` | `03-golden-anchors.md` |

`mensch_als_republik/trust/derive.py` zeigt es in Reinform. Der Docstring der ersten Zeile lautet
sinngemäß: geteilte Ableitungsstufe zwischen `§4` (trust) und `§5` (rank), Klammerzusatz
`02b §2`. Das einzige qualifizierte Präfix im ganzen Modul ist `02b`; gemeint sind beide Male
Abschnitte von `02-trust-flow.md`. Lesart 1 bindet hier nicht bloß nichts — sie bindet falsch.

**Lesart 2 — die eigene Schicht aus dem Paketverzeichnis — trägt 33 von 73.** Gemessen: 33
gedeckt, 9 widerlegt, 31 unanwendbar, weil die Datei in keinem Schichtverzeichnis liegt. Die 31
sind fast durchweg `mensch_als_republik/*.py` in der Paketwurzel — `atom.py`, `cbor_canon.py`,
`domains.py`, `predicates.py`, `policy.py`, `verifier.py`. Ihre Verweise zeigen im Kontext
gelesen ausnahmslos auf `01-claim-atom.md`: `§2` für die Felder, `§3` für CBOR, `§4` für Domänen
und Signatur, `§5.3` und `§5.4` für die Policy, `§6` für den Verifier. Die tragende Regularität
ist dort das **Modulthema**, nicht das Verzeichnis. Lesart 2 greift nach dem richtigen Gedanken
mit dem falschen Signal.

**Mehrdeutigkeit, und eine Berichtigung der Grundmenge.** D221 nannte 62 mehrdeutig, 5 eindeutig,
6 nirgends. Diese Zahlen sind reproduziert und richtig — sie gelten gegen die **acht**
Layer-Dateien. Gegen die dreizehn Einträge von `LAYER_FILES`, also gegen alle heute zulässigen
Zitierziele, sind es 63 mehrdeutig, 10 eindeutig, **0 nirgends**. Die zweite Messung ist die
normativ maßgebliche, und sie sagt zweierlei: kein barer Verweis zeigt ins Leere, und bei 63 von
73 identifiziert die Nummer die Datei nicht. 39 davon treffen in zwölf der dreizehn Dateien.

**Entscheidung: Lesart 3. Bare Paragraphenverweise in `.py` sind unzulässig.** Jeder Verweis
trägt einen der beiden Namen aus D221.

**Die Begründung ist nicht Ästhetik, sondern die Fehlerrichtung.** Keine der beiden Alternativen
erreicht zwei Drittel, und beide lösen an gemessenen Stellen **falsch** auf: Lesart 1 an 6, Lesart
2 an 9. Heute ist ein barer Verweis erkennbar ungeprüft — er fällt aus der Prüfung heraus und
niemand hält ihn für bestätigt. Unter Lesart 1 oder 2 wäre derselbe Verweis scheinbar geprüft und
in acht beziehungsweise zwölf Prozent der Fälle still an die falsche Datei gebunden. Eine Regel,
die Vertrauen erzeugt, wo sie rät, ist schlechter als keine Regel. Das ist genau die Drift, gegen
die das Register steht.

**Benannt und verworfen: ein Mapping von Modulthema auf Schicht.** Es ist die einzige Regularität,
die alle 73 erklären würde — die Paketwurzel ist Layer 01, `trust/` ist 02, und so fort. Verworfen,
weil es eine zweite Tabelle neben `LAYER_FILES` wäre, die gepflegt werden muss und still veraltet,
sobald ein Modul umzieht oder zwei Schichten berührt. `derive.py` berührt heute schon zwei.

**Benannt: der Preis.** Der Docstring `Feldtypen aus §2 prüfen.` liest sich besser als
`Feldtypen aus 01 §2 prüfen.`, und in `atom.py` ist `01` für jeden redundant, der die Datei
kennt. Der Einwand ist echt. Er setzt aber genau den Leser voraus, gegen den gehärtet wird — den
Autor in drei Jahren, der nicht mehr weiß, welche Datei `atom.py` bedient.

**Berichtigung zu D221: die Anhangs-Zielform gehört nicht zu Frage 2.** D221 hat sie mit der
Begründung vertagt, jeder `§B`-Verweis sei heute bar und werde in Frage 2 mitentschieden.
Gemessen auf `b49358e`: in `.py` gibt es **null** bare Anhangsverweise. Die 19 Vorkommen stehen
sämtlich in `.md` — sieben in `02b-abnahme.md`, fünf im Register, drei in `00`, je eines in
`00v-grammatik-prompt.md`, `02b-golden-anchors.md` und zwei Sitzungsstart-Dateien. Diese
Entscheidung berührt sie nicht. Die Anhangsform bleibt offen und braucht eine eigene Runde.

**Reihenfolge für die Umsetzung, damit sie nicht nebenbei entschieden wird.** Die 73 werden in
Tranchen nach Verzeichnis qualifiziert; die Auflösung ist nicht mechanisch abzuleiten, weil 63
mehrdeutig sind, sondern je Stelle aus dem Modulzweck zu lesen und im Diff zu prüfen. Der Befund
für bare Verweise in `check_specs.py` entsteht **im letzten Lauf**, zusammen mit der letzten
Tranche. Erst dann ist die Rücknahmeprobe scharf: eine einzelne Qualifizierung zurücknehmen und
bestätigen, dass die Prüfung genau diese eine Stelle meldet. Käme die Prüfung zuerst, stünde der
Baum über mehrere Läufe rot und die Probe liefe gegen 73 gleichzeitige Befunde.

**Erwartung nach Abschluss aller Tranchen.** In `.py` sind 260 Paragraphenverweise geprüft, bare
gibt es keine mehr, und die Grammatik ist geschlossen: zwei Namensformen, beide gebunden, keine
dritte Klasse, die durch die Prüfung fällt.

### D228 — Bereichsverweise binden beide Nummern an denselben Namen (D227)

**Anlass.** D227 verbietet bare Paragraphenverweise in `.py`, sagt aber nicht, wie ein
**Bereich** qualifiziert wird. Beim Vorbereiten der dritten Tranche fiel die Form auf:
`example-nucleus.md §2–§5` trägt den Namen vor der ersten Nummer, die zweite steht bar. Sie
fällt unter D227 und wäre beim Formulieren des Prompts nebenbei entschieden worden. Das ist
genau der Fehler, vor dem D220 warnt.

**Messung auf `b84d0eb`.** In `.py` stehen 8 Bereichsverweise, in den Wurzel-`.md` 6. Alle
tragen bereits einen auflösbaren Namen vor der ersten Nummer, und alle sind **beidseitig
gedeckt** — auch die zweite Nummer trifft eine Überschrift der genannten Datei. Der Trennstrich
ist uneinheitlich: sechsmal Halbgeviertstrich, zweimal Bindestrich, letzteres in
`tests/trust/pr02.py` und `tests/trust/tp02.py`.

| Fundstelle | Form |
|---|---|
| `tools/example_nucleus.py` (2x) | `example-nucleus.md §2–§5` |
| `tests/governance/fixtures.py` | `04-golden-anchors.md §2–§3` |
| `tests/governance/test_tally_math.py` | `04-golden-anchors.md §4–§5` |
| `tests/profiles/fixtures.py` | `03-golden-anchors.md §2–§3` |
| `tests/profiles/test_payload.py` | `03-golden-anchors.md §5–§6` |
| `tests/trust/pr02.py` | `02-golden-anchors.md §1-§2` |
| `tests/trust/tp02.py` | `02-golden-anchors.md §1-§2` |

**Entscheidung.** Die Form `NAME §A–§B` ist zulässig und bindet **beide** Nummern an denselben
Namen. `tools/check_specs.py` löst beide auf und prüft beide gegen die Zieldatei. Als Trennstrich
sind Halbgeviertstrich und Bindestrich zulässig.

**Das ist keine dritte Namensform.** Die Grammatik bleibt bei den zwei Namen aus D221
geschlossen. Der Bereich ist eine Kurzschreibung für zwei Verweise auf dieselbe Datei, nicht ein
neuer Weg, eine Datei zu benennen. Wer die Zahl der zulässigen Namensformen zählt, zählt
weiterhin zwei.

**Benannt und verworfen: den Namen wiederholen.** `example-nucleus.md §2–example-nucleus.md §5`
braucht keine Änderung an der Prüfung und wäre der billigste Weg. Verworfen, weil er an acht
Stellen Text erzeugt, den niemand freiwillig schreibt — und Text, den niemand freiwillig
schreibt, wird beim nächsten Mal nicht geschrieben. Die Form käme als bare Fortsetzung zurück,
und dann steht dieselbe Frage noch einmal. Bei der Kurzform wäre die Wiederholung erträglich, bei
der Dateinamensform nicht; eine Regel, die nur für eine der beiden Namensformen trägt, ist keine.

**Benannt und verworfen: Bereiche verbieten.** Jede Nummer als eigener Verweis verliert die
Aussage, dass ein zusammenhängender Bereich gemeint ist. `example-nucleus.md §2, §3, §4, §5`
sagt weniger als der Bereich und ist länger.

**Benannt und verworfen: den Trennstrich vereinheitlichen.** Zwei Schreibweisen für dasselbe
Zeichen sind sonst genau die Drift, gegen die dieses Register steht. Hier trägt der Strich aber
keine Bedeutung, die Regex trägt beide Varianten kostenlos, und eine Vereinheitlichung wäre eine
zweite Änderung im selben Lauf mit eigener Rücknahmeprobe. Der Aufwand steht in keinem Verhältnis
zum Gewinn. Wer das später anders sieht, ändert acht Stellen und diesen Absatz.

**Reihenfolge.** Die Regex-Erweiterung entsteht in Tranche C, nicht im letzten Lauf — dort werden
die ersten beiden Bereichsstellen qualifiziert, und ohne die Erweiterung bliebe ihre zweite
Nummer ungeprüft. Der Befund für bare Verweise bleibt davon unberührt und kommt weiterhin im
letzten Lauf, wie D227 festlegt.

**Erwartung.** Die Erweiterung löst alle acht Bereiche in `.py` sofort beidseitig auf, auch die
sechs in `tests/`, ohne dass eine Testdatei angefasst wird. Die Zahl der ungeprüften Stellen in
`tests/` sinkt dadurch von 24 auf 18, bevor Tranche D überhaupt beginnt.

### D229 — Die Zitiergrammatik ist geschlossen (D219, D221, D227, D228)

**Was erreicht ist.** In `.py` steht kein barer Paragraphenverweis mehr. Gemessen auf `f9c0fab`:
121 Dateien, 260 geprüfte Verweise, null Befunde. Zu Sitzungsbeginn waren es 187 geprüfte und 73
bare. Die Differenz ist vollständig aufgelöst, nicht weggelassen.

**Vier Läufe, jeder mit Rücknahmeprobe.**

| Lauf | Commit | Umfang | Verweise danach |
|---|---|---|---:|
| A | `d853b1b` | 26 Stellen in der Paketwurzel | 213 |
| B | `b84d0eb` | 17 Stellen im Trust-Paket | 230 |
| C | `b51b56c` | 4 Stellen plus Bereichsform in `check_specs.py` | 242 |
| D | `f9c0fab` | 18 Stellen in `tests/` plus Befund für bare Verweise | 260 |

**Was die Grammatik jetzt ist.** Zwei Namensformen (D221): Kurzform über `LAYER_FILES` oder
Stamm einer Wurzel-`.md`. Eine Bereichsform (D228), die beide Nummern an denselben Namen bindet.
Alles andere ist ein Befund (D227). Es gibt keine dritte Klasse mehr, die durch die Prüfung
fällt — das war der Zustand, den D220 als Grammatikproblem benannt hatte.

**Entscheidung: kein eigener Test für `tools/`.** Für die Werkzeuge gibt es heute keine Tests;
sie werden durch `make check` an den echten Spec-Dateien ausgeführt, und die Spec-Dateien sind
ihre Testdaten. Die Bereichsauflösung aus D228 bekommt deshalb **keinen** Regressionstest. Sie
ist trotzdem abgesichert, weil der Befund für bare Verweise sie mit abdeckt: bricht die optionale
Gruppe in `SECTION_REF`, werden die acht zweiten Bereichsnummern bar, und der Befund feuert.
Probe 3 des Laufs D hat das gezeigt — acht bare Verweise über sieben Dateien, nach Rücknahme
wieder grün.

**Benannt und verworfen: eine erste Testdatei für `tools/`.** Sie wäre nicht bloß eine Datei,
sondern eine neue Kategorie, und sie prüfte etwas, das `make check` schon prüft. Wer das später
anders sieht, hat mit der Kopplung an den baren Befund ein Argument gegen sich, das erst
verschwindet, wenn dieser Befund verschwindet.

**Die Grenze, die bleibt und nicht zu schließen ist.** Die Prüfung sichert, dass das Ziel
**existiert**, nicht dass es **stimmt**. Ein Verweis auf einen vorhandenen, aber sachlich
falschen Abschnitt bleibt grün. Ein gemessener Fall aus dieser Sitzung: `example-nucleus.md`
zitiert für die Kapazitätsformel den Abschnitt 2 von `02-trust-flow.md`, wo das Graphmodell
steht; die Formel steht in Abschnitt 3 derselben Datei und in `02a`. Formal gültig, inhaltlich
daneben. Deshalb ist bei Qualifizierungsläufen der Diff die Abnahme und nicht die grüne Zeile.

**Was offen bleibt.** Die Anhangsform mit Buchstaben ist nicht entschieden. D221 hatte sie zu
Frage 2 geschoben, D227 hat das berichtigt: in `.py` gibt es keinen einzigen Fall, die 19
Vorkommen stehen sämtlich in Wurzel-`.md`. Sie braucht eine eigene Runde und wird von dieser
Entscheidung nicht berührt.

---

### D230 — Die Anhangsform wird auf `§X.n` beschränkt und geprüft (D221, D227, D229)

**Anlass.** Die Anhangsform ist dreimal verschoben worden: D221 hat sie zu Frage 2 geschoben,
D227 hat berichtigt, dass sie dort nicht hingehört, D229 hat sie als einzigen offenen Teil der
Grammatik benannt. Gemessen auf `b0ff1e8`.

**Grundzählung.** Das Muster Paragraphenzeichen plus Großbuchstabe steht **29-mal in zehn
Dateien**. Davon sind 17 Zitate der Grammatik selbst — Prompt-Dateien, Register,
Sitzungsstart-Dateien und der Docstring von `tools/check_specs.py`. Echte Verweise sind
**zwölf**. Die Übergabedatei nannte 19 auf `b49358e` und behauptete, keines stehe in `.py`.
Beides ist überholt: seit D228 trägt der Docstring von `check_specs.py` die Bereichs-Metasyntax.

**Die zwölf sind nicht eine Form, sondern drei Referenten.**

| Referent | Fälle | Ziel |
|---|---|---|
| Anhangsabschnitt | 7 | reguläre Überschriften der Ebene 3, `### B.1` bis `### C.8` |
| Anhang als Ganzes | 1 | `## Anhang C — Test-Vektoren` in `01-claim-atom.md`, Wortform ohne Nummer |
| Axiom aus einer Liste | 3 | `01-claim-atom.md` Zeile 23, kein Abschnitt |
| toter Zeiger | 1 | `02b-abnahme.md` nennt A.1; gemeint ist B.4 |

**Der Fund ist A3.** `A3` ist kein Anhang, sondern das dritte Axiom im Abschnitt 1 von
`01-claim-atom.md` — Erkennen statt verhindern. Dieselbe Datei zitiert es an Zeile 264 selbst
richtig, in Prosaform mit der Abschnittsnummer davor. Die beiden Stellen in
`00-nucleus-genesis-constitution.md` schreiben stattdessen Paragraphenzeichen plus A3 hinter dem
Namen Atom-Spec und behaupten damit einen Abschnitt, den es nicht gibt, unter einem Namen, den
die Grammatik nicht kennt. Dasselbe Zeichen trägt zwei Bedeutungen — genau die Überladung, gegen
die D209, D219 und D227 stehen.

**Drei von zwölf zeigen ins Leere, und keiner der zwölf ist heute geprüft.** `SECTION_REF` und
`check_bare_refs` verlangen beide eine Ziffer hinter dem Paragraphenzeichen. Die Form ist der
Prüfung vollständig unsichtbar; die Fehlerquote von drei aus zwölf liegt über allem, was D227
gemessen hat.

**Zwei Angaben der Übergabe sind zu berichtigen.** Erstens führen die Anhänge sehr wohl
nummerierte Überschriften der Ebene 3 — fünfzehn in `01-claim-atom.md`, zehn in
`02b-abnahme.md`. Eine zweite Überschriftenquelle ist nicht nötig; nur das Alphabet der Nummer
ist ein anderes. Zweitens werden die Test-Vektoren nicht mit dieser Form zitiert: die sieben
Vorkommen in `02b-abnahme.md` sind Selbstverweise auf eigene Berichtsabschnitte.

**Entscheidung: geprüft wird genau die Form Großbuchstabe, Punkt, Zahl.** `HEADING_NUM` erhält
ein optionales Großbuchstaben-Punkt-Präfix, `SECTION_REF` ebenso. `check_bare_refs` bleibt
unverändert.

**Die Selbst-Rot-Falle feuert nicht, und das ist gemessen.** Die Bereichs-Metasyntax mit den
bloßen Buchstaben A und B trägt keine Ziffer und trifft die erweiterte Regex nicht. Das Literal
in `00v-grammatik-prompt.md` trifft sie, steht aber ohne Namen davor — und `.md` hat keinen
Bare-Check. Register und Sitzungsstart-Dateien sind ohnehin ausgenommen.

**Ertrag heute: ein einziger neu geprüfter Verweis** — `02b-golden-anchors.md` auf den Abschnitt
C.1 von `02b-abnahme.md`, und der ist korrekt. Das ist der ehrliche Wert am Bestand. Der Ertrag
liegt in der Zukunft: eine Regel, die erst bei der ersten Anwendung entsteht, kommt zu spät, und
die Erweiterung kostet zwei Regexzeilen.

**Vier Textkorrekturen im selben Lauf**, alle in Prosaform nach dem Vorbild aus D221:

1. `00-nucleus-genesis-constitution.md` Zeile 76 nennt Anhang C von `01-claim-atom.md` mit
   Paragraphenzeichen vor dem Wort. Die Wortform bekommt keine Regex und wird Prosa.
2. und 3. Dieselbe Datei, Zeilen 371 und 418: Atom-Spec plus A3 wird zum qualifizierten Verweis
   auf Abschnitt 1 von `01-claim-atom.md`, mit dem Axiom als Prosa dahinter.
4. `02b-abnahme.md` Zeile 30 nennt A.1 für die Schnittstellenform von `derive()`. Gemeint ist
   B.4, deren Überschrift die Schnittstelle der geteilten Ableitung nachzieht.

**Verworfen: die Form in `.md` verbieten, analog D227.** Das bräuchte eine Ausnahmeliste für die
Prompt-Dateien, die die Grammatik als Literal zitieren — und Ausnahmelisten verrotten, was D221
in eigener Sache schon einmal ausgeschlossen hat. Dazu kommt die Unstimmigkeit: in `.md` ist der
bare Selbstverweis mit Ziffern zulässig und überall. Ihn mit Buchstaben zu verbieten,
unterschiede zwei Fälle allein danach, welches Alphabet die Zielüberschrift trägt.

**Verworfen: gar nicht prüfen und nur die Grenze benennen.** Das war die Position des Supervisors
vor der Messung der drei Referenten und ist mit ihr gefallen. Sie lässt drei falsche Zeiger ohne
Wächter zurück und macht die Korrektur zu einer, die in einem Jahr wieder aufgeht.

**Verworfen: die Wortform mittragen.** Eine zweite Überschriftenquelle für die Ebene-2-Formen mit
Wort statt Nummer, für genau ein Vorkommen. Prosa ist billiger und hat mit D221 ein Vorbild.

**Verworfen: `check_bare_refs` auf Buchstaben erweitern.** In `.py` gibt es null Fälle, und der
erste Effekt wäre, dass `check_specs.py` seinen eigenen Docstring meldet. Eine Regel ohne
Anwendung, die als erstes den Prüfer rot macht.

**Erwartung an den Lauf.** `make check-specs` bleibt grün. Die Python-Zeile bleibt bei 121
Dateien und 260 Verweisen; kein `.py` trägt die Form. Vor den vier Korrekturen meldet die Prüfung
**keinen** Befund, weil keiner der vier falschen Verweise einen auflösbaren Namen vor sich hat —
die Korrekturen sind darum vom Diff abzunehmen, nicht von der grünen Zeile.

**Zwei Rücknahmeproben, je eine pro Änderung.** Erstens das Großbuchstaben-Präfix in
`HEADING_NUM` zurücknehmen: der Verweis aus `02b-golden-anchors.md` muss als unbekannter
Abschnitt fallen. Zweitens denselben Verweis auf eine nicht vorhandene Nummer setzen: dieselbe
Befundklasse muss feuern, was zeigt, dass `SECTION_REF` die Form überhaupt liest. Keine der
beiden Proben formt Produktivcode.

**Die Grenze aus D229 bleibt unberührt.** Geprüft wird, dass das Ziel existiert, nicht dass es
stimmt. Mit dieser Entscheidung ist die Zitiergrammatik in allen vier Teilen geschlossen.

---

### D231 — Die Backtick-Form wird toleriert, und eine Berichtigung zu D230 (D221, D227, D230)

**Berichtigung zuerst.** D230 nennt als Ertrag der Anhangserweiterung einen einzigen neu
geprüften Verweis: den aus `02b-golden-anchors.md` auf den Abschnitt C.1 von `02b-abnahme.md`.
Der Verweis existiert, aber er ist nicht qualifiziert. Der schließende Backtick steht zwischen
dem Dateinamen und dem Paragraphenzeichen, und `SECTION_REF` verlangt an dieser Stelle ein
Namenszeichen. Der Ertrag der Erweiterung allein ist **null**. Der Fehler liegt beim Supervisor,
und es ist dieselbe Klasse wie in D221: eine Form wurde gelesen, ohne sie gegen die Regex zu
halten.

**Die vierte Oberflächenform, gemessen auf `2919e76`.** Elf Verweise in sieben Dateien schreiben
den Namen in Backticks und lassen das Paragraphenzeichen draußen. In `.py` gibt es null Fälle.

| Datei | Fälle |
|---|---|
| `00b-prompt.md` | 3 |
| `03b-prompt.md` | 3 |
| `02b-golden-anchors.md` | 1 |
| `03-prompt.md` | 1 |
| `einlesen-a-prompt.md` | 1 |
| `einlesen-a-nachlauf-prompt.md` | 1 |
| `07-decisions.md` (von der Verweisprüfung ausgenommen) | 1 |

**Alle elf lösen gegen ihr Ziel grün auf.** Kein Defekt darunter, und das ist der Grund, warum die
Form so lange getragen hat: sie ist für einen Leser vollständig qualifiziert und für den Prüfer
vollständig unsichtbar. Genau diese Kombination hat D227 für `.py` als schlechter beurteilt als
einen sichtbar ungeprüften Verweis.

**Warum die beiden Fragen zusammenhängen.** `02b-abnahme.md` führt keine einzige
Ziffernüberschrift; seine zehn Überschriften der Ebene 3 tragen Buchstabennummern. Würde die
Backtick-Form aufgelöst, ohne dass D230 die Buchstabenform trägt, ginge dieser eine Verweis rot.
Umgekehrt hat die Erweiterung aus D230 ohne diese Entscheidung keine einzige Anwendung. Die
beiden gehören in einen Lauf.

**Entscheidung.** `SECTION_REF` toleriert einen optionalen schließenden Backtick zwischen dem
Namen und dem Paragraphenzeichen. Der Name bleibt derselbe, die Injektivität bleibt unberührt —
dieselbe Begründung, mit der D228 zwei Strichformen für den Bereich zugelassen hat. Zehn Verweise
werden damit geprüft, der elfte steht im ausgenommenen Register.

**Verworfen: die elf Stellen umschreiben.** Elf Textänderungen in sieben Dateien gegen ein
Zeichen in der Regex. Vier der Dateien beschreiben vergangene Läufe, und D219 hat für diesen Fall
schon einmal entschieden, dass nichts umgeschrieben wird, damit eine Prüfung es führen kann.

**Verworfen: einen Befund für die Form erheben.** Das machte zehn sachlich richtige Verweise rot,
um eine Schreibweise durchzusetzen, die keinen Leser irreführt. Der Gegenstand ist die
Prüfbarkeit, nicht die Typografie.

**Verworfen: nichts tun.** Elf Verweise, die qualifiziert aussehen und keiner sind, sind kein
Randfall mehr, sondern eine Klasse. Sie wächst, weil die Form sich gut liest.

**Erwartung an den Lauf.** `make check-specs` bleibt grün. Die Python-Zeile bleibt bei 121
Dateien und 260 Verweisen: kein `.py` trägt eine der beiden Formen, und gemessen trifft die
erweiterte Regex über alle Wurzel-`.md` und alle `.py` keinen Verweis neu, den die alte nicht
schon traf. Die Zahl der in `.md` aufgelösten Verweise wird nicht ausgegeben; die Abnahme ist
darum der Diff und sind die beiden Proben, nicht die grüne Zeile.

**Zwei Rücknahmeproben, je eine pro Änderung.** Erstens das Großbuchstaben-Präfix aus D230 in
`HEADING_NUM` zurücknehmen: der Verweis aus `02b-golden-anchors.md` muss als unbekannter
Abschnitt fallen, und nur dieser eine. Zweitens bei beiden Änderungen in Kraft einen
backtick-getrennten Verweis auf eine nicht vorhandene Nummer setzen: dieselbe Befundklasse muss
feuern, was zeigt, dass die Toleranz die Form überhaupt liest. Keine der beiden Proben formt
Produktivcode.

**Was damit geschlossen ist.** Die Zitiergrammatik kennt zwei Namensformen (D221), eine
Bereichsform (D228), die Anhangsnummer (D230) und zwei Schreibweisen des Namens (hier). Bare
Verweise sind in `.py` ein Befund (D227) und in `.md` weiterhin zulässig, weil dort der
Selbstverweis der Normalfall ist. Eine fünfte Klasse ist nicht gemessen worden.

---

### D232 — Abnahme `00z`; ein Defekt aus dem Prompt und ein Versatz in der Messgrundlage

**Der Lauf.** Zwei Commits auf `impl/00z`, drei Dateien. `tools/check_specs.py` trägt die
Anhangsnummer in `HEADING_NUM` und in beiden Nummerngruppen von `SECTION_REF`, dazu den
tolerierten Backtick aus D231 und den berichtigten Kommentar über `LAYER_FILES`. Vier Textstellen
sind korrigiert. Die abgeleiteten Zahlen halten: 43 zusätzliche Überschriften über vier Dateien,
die Python-Zeile unverändert bei 121 Dateien und 260 Verweisen, 597 Tests. Beide Rücknahmeproben
melden genau einen Befund mit der erwarteten Nummer und werden nach dem Zurücksetzen wieder grün.

**Ein Defekt, und er stammt aus dem Prompt.** Die beiden neuen Verweise standen im ersten Commit
ohne Backticks. `00-nucleus-genesis-constitution.md` führt elf qualifizierte Verweise, elf davon
in Backticks und keinen ohne; die neue Form war im Bestand einmalig. Der Prompt hatte das Ziel in
einem Code-Span genannt, und das Werkzeug hat die Backticks folgerichtig als Auszeichnung des
Prompts gelesen statt als Teil des einzusetzenden Textes. Behoben im zweiten Commit, zwei Zeilen.
Der Verweis war schon vorher grün — die Prüfung sah die Form nicht, der Bestand schon.

**Der Versatz in der Messgrundlage.** Jeder der 227 Dateikörper im repomix-Archiv beginnt mit
einem Zeilenumbruch hinter dem Dateitag. Wer den Körper aufteilt, zählt eine Leerzeile mit:
**jede Zeilennummer und jede Zeilenzahl aus der Kopie ist um genau eins zu hoch.** Betroffen
waren fünf Zeilenangaben im Prompt und beide Splice-Trockenläufe dieser Sitzung, die 8377 und
8473 meldeten, wo der Baum 8376 und 8472 hatte.

**Warum er drei Runden gehalten hat.** Der Versatz fällt in jeder Differenz heraus. Der Zuwachs
von 96 und 70 Zeilen stimmte beide Male, und die Zeilenzahl selbst war nie ein Abnahmekriterium.
Erst eine absolute Angabe im Prompt hat ihn sichtbar gemacht. Das Werkzeug hat ihn gemeldet und
die Stellen nach Inhalt getroffen, statt still zu suchen — genau so war es beauftragt.

**Nicht berichtigt: die fünf Zeilenangaben im committeten Prompt.** Er beschreibt einen
vergangenen Lauf und ist als dessen Beschreibung richtig; D219 hat für diesen Fall entschieden.

**Daraus Prüfregel 46.**

---

### D233 — Zwei sachlich falsche Verweise in `example-nucleus.md`, keine zweite Prüfklasse (D229)

**Was gemessen wurde.** Auf `3d35972` führt `example-nucleus.md` 25 qualifizierte Layer-Verweise.
Alle 25 lösen auf einen vorhandenen Abschnitt auf; `check_specs.py` ist an der Datei grün und
bleibt es nach dieser Berichtigung. Zwei der 25 zeigen auf den falschen Abschnitt.

| Zeile | genannt | richtig | was am Ziel steht |
|---|---|---|---|
| 78 | `04 §2.1` | `04 §1.1` | das MUSS über `irrevocable_predicates`; `§2.1` ist `propose@1` |
| 157 | `02 §2` | `02 §3` | das Knotenbudget mit einmaliger Rundung; `§2` ist das Graphmodell |

**Berichtigung zu D229.** Dort steht „Ein gemessener Fall aus dieser Sitzung". Gemessen war nur
der erste; die übrigen 24 Verweise waren nicht geprüft, sondern ungeprüft geblieben. Der zweite
Fall ist erst beim vollständigen Auszählen aufgefallen, und er ist der ältere von beiden.

**Die drei übrigen `02 §2` bleiben stehen.** Sie nennen die Scope-Partition, und die steht in
`§2`. Eine Ersetzung über die ganze Datei wäre falsch gewesen — der Befund ist zeilengenau, nicht
namensweit.

**Entscheidung: es kommt keine zweite Prüfklasse.** D229 hatte die Richtigkeit eines Verweises
dem Leser überlassen. Der zweite Fund war ein benannter Grund, das zu prüfen, weil beide Fälle
derselben billigen Probe zugänglich gewesen wären: nimmt der Zielabschnitt mindestens einen
Code-Span aus der Zeile des Verweises auf? Gegen die Datei mit jetzt bekannter Wahrheit gemessen:
zwei richtige Alarme, zwei falsche, neun still und richtig, kein verpasster Fall — und **zwölf von
25 Verweisen ohne Code-Span in der Zeile**, für die Probe also unsichtbar. Darunter alle drei
richtigen `02 §2`.

**Warum die Zahlen die Probe erledigen.** Eine Prüfung, die 48 Prozent ihres Gegenstands nicht
sieht, meldet Grün für einen Bestand, den sie nicht angesehen hat; das ist schlechter als keine
Prüfung, weil es sich wie eine anfühlt. Dazu kommt, dass beide Fehlalarme dieselbe Ursache haben
— `n = 3` und `n = 50` sind Beispielwerte, die im Zielabschnitt naturgemäß nicht stehen. Ein
Beispielnukleus besteht aus solchen Werten. Die Probe ist gerade dort am blindesten und am
lautesten, wo sie gebraucht würde.

**Was bleibt.** Die Grenze aus D229 steht unverändert, jetzt mit einer Messung statt einer
Erwartung dahinter. Wer sie erneut aufmachen will, braucht mehr als einen weiteren Einzelfund: er
braucht eine Probe, deren Blindquote gemessen ist.

**Kein Werkzeuglauf.** Zwei Zeilen, beide längenneutral, als Splice gefahren.

---

### D234 — Die Föderationsstimme trägt keinen Autorisierungsweg (Befund, keine Entscheidung)

**Anlass.** Die offene Liste führte `04 §7.2` als „nie durchgerechnet". Beim Lesen hält das nicht:
der Abschnitt ist bewusst dünn und delegiert alles Weitere an `08 §3`. Was er dagegen ungeprüft
behauptet, ist ein Autorisierungsweg, den keine Schicht einlöst. **Kein Registereintrag nennt die
Föderation** — gemessen über alle Einträge D1 bis D233. Die Frage ist nie gestellt worden.

**Der Widerspruch, drei Stellen.**

1. `00 §7` zählt die Föderationsstimme als Nukleus-Akt auf und autorisiert sie über
   `akt.I` Element von `resolve_current_key(akt.N)`, wobei `akt.N` zum aufgelösten Scope passen
   MUSS.
2. `04 §7.2` sagt, `participants` der Föderationsverfassung enthalte „die aktuellen Schlüssel der
   konstituierenden Nuklei", und deren Stimme entstehe bei jedem von ihnen über `§5`.
3. `04 §3.1` Bedingung 3 prüft `vote.I` als Element von `P` byte-fest. Nach `04 §1.1` ist
   `participants` ein `array of bstr (32 B)`. Es findet keine Auflösung statt.

**Warum kein Pfad trägt.** `04 §5` trennt Epochen- und Schlüsselpfad nach `vote_mode` und erklärt
diese Zuordnung für normativ. Für die Föderationsstimme scheitern beide, und zwar verschieden. Im
Epochenpfad bindet `participants` byte-fest: rotiert ein Kind seine `nucleus_keys` — nach D150 für
den Nukleus identitätserhaltend und jederzeit zulässig —, fällt seine Stimme aus, bis die
Föderationsverfassung nachgezogen ist. Die ist nur über eine Auszählung änderbar, an der es dann
nicht mehr teilnimmt. Im Schlüsselpfad ist `akt.N` nach der Bindungsregel (`01 §2.2`) der Scope
der Stimme, also `N_fed`; `resolve_current_key(N_fed)` liefert die Schlüssel der Föderation, nicht
die des stimmenden Kindes. Der Weg zeigt auf den falschen Scope.

**Der strukturelle Grund.** Die Föderationsstimme ist der einzige der fünf aufgezählten Akte, der
in einem **fremden** Scope stattfindet. Bei den übrigen ist `akt.N` der Scope, dessen Autorität
geprüft wird; hier ist es der Scope, in dem gehandelt wird, und der gehört einem anderen. Deshalb
ist die Regel aus `00 §7` auf sie nicht anwendbar — nicht, weil sie falsch gerechnet wäre, sondern
weil ihr Argument etwas anderes bezeichnet, als der Satz meint.

**Die Aufzählung in `00 §7` trägt ihre eigene Regel nur einmal.** Gemessen an den fünf genannten
Akten:

| Akt | tatsächlich autorisiert in | über `resolve_current_key` |
|---|---|---|
| `grant-membership@1` | `00 §7`, umgesetzt in `03 §4` | ja |
| `verdict@1` eines Panels | `03 §2.4`, byte-weise gegen `arbitration.arbitrators` | nein, ausdrücklich |
| Föderationsstimme | `04 §3.1` Bedingung 3 | nein |
| Ratifizierung | `04 §4.1` Bedingung 1 | nein |
| `rotate-key@1` | `00 §6.4` | ist die Kette, nicht ihr Nutzer |

Das ist die Fehlerform von D145 und D150: der allgemeine Satz stimmt für den Fall, aus dem er
gewonnen wurde, und die Aufzählung darunter trägt ihn nicht. `04 §5` hat den Teil davon, der die
Pfade betrifft, bereits berichtigt; `00 §7` ist nie nachgezogen worden.

**Die Gabel, benannt und nicht entschieden.** Entweder bleibt `participants` byte-fest, dann fällt
in `04 §7.2` das Wort „aktuellen", und die Kosten gehören offen benannt: jede Rotation eines
Kindes verlangt eine Verfassungsänderung der Föderation, und eine Föderation kann darüber
einfrieren. Oder die Stimmbedingung bekommt einen Auflösungsschritt. Gegen die zweite steht D154 —
der Kettenkopf kann unter Wissenszuwachs zurückspringen; eine aufgelöste Stimmberechtigung wäre
dann nicht monoton, und D96, D101 und D102 hängen an der Monotonie. Die Neigung des Supervisors
ist die erste Gabel; sie ist nicht gerechnet und darf hier nicht als entschieden gelten.

**Kein Lauf.** Dieser Eintrag ändert keine Spec-Datei. Er hält fest, was gemessen ist, damit die
Entscheidung eine Grundlage hat und nicht wieder bei „nie durchgerechnet" beginnt.

---

### D235 — Die Autoritätsliste ist ein Bearer-Recht: drei Fälle, zwei entschieden (D234)

**Die gemeinsame Ursache.** MaR hat mit `resolve_current_key` eine Indirektion gebaut und benutzt
sie an genau einer der fünf Stellen, die `00 §7` unter dieselbe Regel stellt (D234). Überall sonst
bindet Autorität unmittelbar an Schlüsselbytes: `participants`, `arbitration.arbitrators`,
`nucleus_keys`. Das ist mit D124 und `03 §2.4` konsistent, macht aber jede Autoritätsliste zu
einem Bearer-Recht — wer die Bytes hält, hat die Befugnis, und entziehen kann sie ihm nur eine
Auszählung, an der er selbst teilnimmt. Die Föderation ist bloß der Ort, an dem das zuerst weh
tut, weil dort die Mitglieder selbst rotierende Entitäten sind.

**Der Stand außerhalb.** RFC 2693 (SPKI/SDSI) kennt für ein Subject drei Formen: einen Schlüssel,
einen Namen mit Auflösung über ein name cert, oder ein Threshold-Subject. `04 §7.2` mischt die
erste und die zweite in einem Satz. Das SAFE-System (arXiv 1510.04629) nennt die übliche Antwort:
Prinzipale handeln über Sub-Prinzipale, denen sie eine Delegation ausstellen, damit der
Hauptschlüssel offline bleiben und rotieren kann, ohne die Delegation zu berühren.

**Fall A entschieden: der Föderationseintrag ist ein eigener Schlüssel.** `participants` einer
Föderationsverfassung benennt **nicht** den aktuellen Nukleus-Schlüssel des Kindes, sondern den
Schlüssel, mit dem dieses Kind in dieser Föderation spricht. Er ist von der Rotation im
Kind-Scope entkoppelt, weil er mit ihr nichts zu tun hat. Damit fällt in `04 §7.2` das Wort
„aktuellen", und der gerechnete Einfrierfall verschwindet: eine Rotation im Kind-Scope berührt
die Föderation nicht mehr.

Begründung, in dieser Reihenfolge. Erstens ist es die Form, die schon dasteht — dieselbe wie bei
`arbitration.arbitrators` nach `03 §2.4`, das ausdrücklich byte-weise vergleicht und keine
Schlüsselauflösung vornimmt. Zweitens verlangt die Alternative eine Auflösung in der
Stimmbedingung, und der aufgelöste Kopf kann nach D154 unter Wissenszuwachs zurückspringen; die
Stimmberechtigung wäre dann nicht mehr monoton, woran D96, D101 und D102 hängen. Drittens sagt
`00 §7` selbst, dass `akt.N` zum aufgelösten Scope passen muss — für eine Stimme im
Föderations-Scope ist das `N_fed`, und `resolve_current_key(N_fed)` liefert die Schlüssel der
Föderation, nicht die des stimmenden Kindes. Der Weg zeigt strukturell auf den falschen Scope.

**Folge für `00 §7`:** die Föderationsstimme gehört nicht in die Aufzählung der Nukleus-Akte. Sie
ist der einzige dort genannte Akt in einem **fremden** Scope. Die Streichung ist ein eigener Lauf.

**Fall B getragen, nicht behoben: der alte Schlüssel bleibt stimmfähig.** `04 §3.1` prüft an
`vote.I` die Mengenzugehörigkeit zu `P` und den Claim-Zustand, nichts über die Lebendigkeit des
Schlüssels; der `rotate-key@1`-Claim des Kindes trägt `N_kind` und ist im Föderations-Scope nach
`02 §2` unsichtbar. Wer einen abgelösten Eintragsschlüssel behält, stimmt weiter.

Der Fall hat außerhalb einen Namen: „I still work here", beschrieben in der Arbeit zur
asynchronen Reconfiguration unter byzantinischen Fehlern (arXiv 2005.13499). Die dortige
Gegenmaßnahme sind forward-sichere Signaturen mit einem Quorum, das seine alten Schlüssel
vernichtet. Entscheidend ist die Grenze, die dieselbe Arbeit zieht: sicherzustellen, dass **alle**
veralteten Konfigurationen ihre Schlüssel löschen, verlangt Konsens. MaR ist nach `08 §2.3`
konsensfrei. B ist damit in diesem Protokoll nicht schließbar — dieselbe Beweisfigur wie in D124,
wo identitätserhaltende Rotation aus genau diesem Grund verworfen wurde.

**Beschluss zu B:** eine getragene Grenze in `04 §8`, mit dem Unmöglichkeitsgrund. Der praktische
Satz dazu gehört in `example-nucleus.md §8.1`: ein Eintragsschlüssel ist so lange gültig, wie
seine Bytes in der Liste stehen, und die einzige Entwertung ist die Änderung der Liste.

**Fall C festgestellt: die Abweichung ist nicht gewollt.** Ein kompromittierter `participants`-
Eintrag blockiert seine eigene Entfernung. Nach `04 §3.2` ist der Nenner `|P|` einschließlich des
Betroffenen, Nichtteilnahme wirkt wie Ablehnung, und „gescheitert" ist einmal wahr für immer wahr.
Gemessen, kleinstes `m`, das die eigene Entfernung endgültig scheitern lässt:

| `n` | 1/2 | 2/3 | 3/4 |
|---:|---:|---:|---:|
| 3 | 2 | 1 | 1 |
| 4 | 2 | 2 | 1 |
| 7 | 4 | 3 | 2 |
| 12 | 6 | 4 | 3 |

Je strenger die Schwelle, desto leichter die Blockade. Das ist **kein** Föderationsproblem,
sondern eine Eigenschaft jeder Auszählung in jedem Nukleus.

Der Stand der Technik trennt an dieser Stelle das Entfernungsrecht vom Stimmrecht. In MLS
(RFC 9420) ist die Entfernung ein Vorschlag, den ein anderes Mitglied ausführt, und wer entfernen
darf, ist Policy und keine Abstimmung. MaR geht diesen Weg nicht. **Festgestellt wird: das ist
nicht gewollt, sondern unbemerkt.** Gewollt hieße in diesem Projekt ein Registereintrag mit
benannter Begründung; über D1 bis D234 gibt es keinen. `04 §8` führt die verwandte Grenze — eine
hohe Schwelle bei lauer Beteiligung macht die Verfassung faktisch unveränderlich —, aber nicht die
aktive Selbstblockade. D116 und `§6.3` entkoppeln die Stimmberechtigung ausdrücklich von der
Mitgliedschaft und begründen das gegen eine **andere** Blockade; dass damit kein zweiter Hebel
mehr existiert, einen Eintrag zu entwerten, ist dort nicht gesehen worden.

**Warum C hier nicht entschieden wird.** Der naheliegende Ersatz ist das Stimmverbot bei
Betroffenheit — wer in `participants_alt` steht und in `participants_neu` fehlt, zählt weder im
Zähler noch im Nenner. Es wäre billig: `§3.4` leitet die Klasse bereits aus dem Unterschied der
beiden Verfassungen ab, beide Objekte sind content-adressiert und vollständig bekannt, es entsteht
kein Teilwissensproblem, und die Monotonie bliebe erhalten. Es hat aber einen Preis in der
Gegenrichtung: bei `n = 12` und Schwelle 2/3 verlangt ein Ausschluss heute neun Ja-Stimmen, bei
Stimmverbot von vier Betroffenen nur noch sechs. Die Schutzwirkung einer hohen Schwelle
verschwindet genau dort, wo sie am dringendsten ist. Das Gesellschaftsrecht federt dieselbe
Spannung mit dem „wichtigen Grund" ab, den ein Gericht prüft; MaR hat kein Gericht, wohl aber
Schlichtung nach `03 §2.4`, und ob die diese Rolle tragen kann, ist nie gefragt worden.

**Offen und benannt:** welcher Mechanismus die Ausschlussfähigkeit herstellt, ohne den
Minderheitenschutz zu opfern, in einem Protokoll ohne Konsens und ohne Instanz. Das ist eine
Frage nach vorhandenen Bauformen, nicht nach einer Erfindung, und sie bekommt eine eigene Runde.

**Kein Lauf.** Dieser Eintrag ändert keine Spec-Datei. Die Streichung in `04 §7.2`, die Grenze in
`04 §8` und die Betriebswarnung in `example-nucleus.md §8.1` sind ein eigener, dann gebündelter
Lauf.

---

### D236 — Kein Ausschlussmechanismus; Exit ist die Antwort (D234, D235)

**Die Frage.** D235 hat festgestellt, dass ein kompromittierter Eintrag in `participants` seine
eigene Entfernung endgültig blockiert und dass dieser Zustand nicht gewollt, sondern unbemerkt
war. Offen blieb, was an die Stelle tritt. Recherchiert wurde die Frage: wie entfernen Systeme
ohne Zentrale, ohne Gericht und ohne Konsens einen feindlichen Träger einer Autoritätsliste, und
was kostet es.

**Der Stand außerhalb**, nach dem Muster von D124:

| System | Bauform der Entfernung | Preis |
|---|---|---|
| BFT-SMaRt | signierter Reconfiguration-Request durch die Totalordnung; der Betroffene stimmt nicht mit | Konsens, Totalordnung, ein Admin-Schlüssel über den Knoten |
| Kuznetsov/Tonkikh, arXiv 2005.13499 | konsensfreie Reconfiguration über Lattice Agreement | forward-sichere Schlüssel, die vernichtet werden — Zeitbegriff und Monotoniebruch |
| MLS, RFC 9420 | Remove-Proposal, das ein anderes Mitglied ausführt | wer entfernen darf, ist Anwendungspolicy; das Protokoll regelt es nicht |
| SPKI/SDSI, RFC 2693 | Threshold-Subject: K von N zeichnen gemeinsam | löst nichts — der Feindliche zeichnet einfach nicht mit |
| Stellar/SCP | jeder streicht ihn aus seinen eigenen Quorum-Slices | keine kollektive Wirkung, die Entfernung ist rein lokal |
| Mastodon | einseitiger Instanz-Block durch jeden Betreiber | dasselbe: lokal, kein Beschluss, kein gemeinsamer Zustand |
| Steem zu Hive, 2020 | die Übrigen gründen neu und lassen ihn zurück | Netzwerkspaltung, Verlust von Kontinuität und Marke |
| Gesellschaftsrecht, § 47 Abs. 4 GmbHG | Stimmverbot des Betroffenen bei eigener Sache | die Missbrauchskontrolle liegt bei einem Gericht |

**Was davon geprüft ist.** Selbst gelesen wurden RFC 2693, RFC 9420, RFC 9750 sowie die Arbeiten
arXiv 2005.13499, arXiv 2304.02156 und arXiv 1510.04629. Die übrigen Zeilen stammen aus einem
Recherchebericht und sind nicht am Primärtext nachgeprüft. Sie stützen die Entscheidung, sie
tragen sie nicht allein; die tragende Aussage steht in den geprüften Quellen.

**Das negative Ergebnis, und es ist der Kern.** Keine Bauform wahrt zugleich Konsensfreiheit,
Uhrenlosigkeit, Monotonie und Instanzlosigkeit **und** entfernt einen Eintrag verbindlich gegen
seinen Willen. Wer verbindlich entfernt, braucht Konsens, eine Frist oder eine Instanz. Wer alle
vier Bedingungen wahrt, entfernt nur lokal oder gar nicht. Das ist keine Lücke der Recherche,
sondern folgt aus der Bauform: ein monotoner, uhrenloser Beschluss, dessen Nenner stets `|P|` ist
und in dem Nichtteilnahme wie Ablehnung wirkt (`04 §3.2`), kann eine Sperrminorität nicht gegen
ihren Willen auflösen, ohne entweder den Nenner zu verändern oder den Kontext zu verlassen.

**Berichtigung eines vorgeschlagenen Auswegs.** Der Bericht empfahl einen Nachfolge-Mechanismus:
ein Verfassungsobjekt deklariert einen Nachfolger, der den Feindlichen nicht übernimmt, statt ihn
zu entfernen. Das umgeht die Blockade **nicht**, solange der Nachfolgebeschluss derselben
Auszählung unterliegt — der Feindliche stimmt auch dagegen, mit denselben Zahlen. Strukturell
umgangen wird sie nur, wenn der neue Kontext **ohne jeden Beschluss** entsteht.

**Beschluss.** Es wird kein Ausschlussmechanismus gebaut.

1. **Kein Stimmverbot bei Betroffenheit**, weder generell noch an eine Schlichtung gebunden. Es
   kippt den Minderheitenschutz genau dort, wo er am nötigsten ist: bei zwölf Mitgliedern und
   Schwelle 2/3 verlangt ein Ausschluss heute neun Ja-Stimmen, bei Stimmverbot von vier
   Betroffenen nur noch sechs. Eine knappe Mehrheit könnte sich zur Supermajorität machen, indem
   sie genug Gegner in einen Vorschlag aufnimmt.
2. **Keine Schlichtung als „wichtiger Grund".** Der Ausweg ist zirkulär:
   `arbitration.arbitrators` ist dieselbe Bauform wie `participants` und trägt dasselbe
   Bearer-Problem. Ein kompromittierter Schiedsrichter ist ebenso wenig zu entfernen. D166
   verlangt zudem, die Frage für `root_keys`, `nucleus_keys` und `arbitration.arbitrators`
   zugleich zu beantworten oder gar nicht; ein Sonderweg für eine der drei Listen fällt damit aus.
3. **Exit ist die Antwort, und sie steht bereits.** Ein Genesis ist von jedem gründbar und
   braucht niemandes Zustimmung — das ist der einzige Vorgang in MaR, der ohne Auszählung
   auskommt, und deshalb der einzige, den eine Sperrminorität nicht erreicht. Der Preis ist
   ebenfalls schon geschrieben: Vertrauen aus einem Scope fließt nicht in einen anderen
   (`02 §2`), und die neue Lage beginnt bei null (`example-nucleus.md §6`).
4. **Die Selbstblockade wird als getragene Grenze benannt**, mit den Zahlen aus D235, in `04 §8`.
   Ein Zustand, den man kennt und ausspricht, ist etwas anderes als einer, den man übersieht.

**Warum das keine Kapitulation ist.** Die Entscheidung ist dieselbe, die `08 §2.2` für das ganze
Protokoll trifft: Widersprüche werden unbestreitbar, nicht unmöglich. Ein feindlicher Eintrag
wird nicht ausgeschlossen, sondern sichtbar — und die Übrigen entscheiden selbst, ob sie mit ihm
weitermachen. Das ist genau die Lage, in der Menschen sich ohnehin befinden, wenn keine Instanz
über ihnen steht. Eine Protokollmechanik, die etwas anderes verspricht, müsste eine der vier
Bedingungen aufgeben, und jede dieser Aufgaben ist teurer als die Blockade.

**Verworfen, mit Grund.** Der forward-sichere Weg aus arXiv 2005.13499 wäre der einzige
konsensfreie Mechanismus mit verbindlicher Wirkung; er scheitert daran, dass die Vernichtung
alter Schlüssel ein Zeitbegriff ist und ein Claim damit ungültig würde — beides gibt es in MaR
nicht. Der Weg über eine Instanz mit Vetorecht scheitert an `04 §8`: innerhalb eines Nukleus gibt
es keine Instanz über den Überstimmten, und das ist eine tragende Entscheidung, keine Lücke.

**Kein Lauf.** Der Spec-Anschluss — Streichung in `04 §7.2`, Grenze in `04 §8`, Betriebswarnung
in `example-nucleus.md §8.1` — ist ein eigener, gebündelter Lauf.

---

### D237 — Reifegrad und Reihenfolge: die Spec prüft sich nicht selbst

**Anlass.** Nach vier Läufen und einer Recherche in einer Sitzung die Frage, woran als nächstes
zu arbeiten ist. Der Eintrag hält die Antwort fest, damit die nächste Sitzung nicht wieder bei
der Frage beginnt.

**Die Spec ist breit reif und in der Tiefe ungeprüft.** Layer 00 bis 04 sind vollständig, 236
Entscheidungen sind begründet, 46 Prüfregeln kodifiziert. Dagegen steht eine gemessene Zahl: in
`example-nucleus.md` waren zwei von 25 qualifizierten Verweisen sachlich falsch (D233), und
`00 §7` hat seit Layer 00 eine Autorisierungsregel verallgemeinert, die nur einer von fünf dort
aufgezählten Fällen trägt (D234, D235). Beides stand jahrelang grün, weil die Prüfung sichert,
dass ein Ziel existiert, und nicht, dass es stimmt (D229). Die Spec ist nie systematisch gegen
sich selbst gelesen worden.

**Die Implementierung erbt die Mehrdeutigkeiten der Spec, statt sie aufzudecken.** 597 Tests und
14 Eigenschaftstests laufen gegen eine Referenzimplementierung, die aus derselben Spec über
denselben Kanal abgeleitet wurde. Die Golden Anchors sind Selbstkonsistenzproben, keine
Interop-Tests. Wo die Spec zweideutig ist, hat der Ableitungsweg eine der Lesarten stillschweigend
gewählt, und der Test bestätigt genau diese Wahl.

**Beschlossene Reihenfolge.**

1. **Die Stummelzeilen aus `00w` glätten** (D223). Klein, abgeschlossen, räumt einen Punkt der
   offenen Liste. Die Menge ist nur über den Diff des Umbruch-Commits bestimmbar, nicht über ein
   Muster: eine Suche nach kurzen Zeilen mitten im Absatz findet über den ganzen Bestand 139
   Stellen, überwiegend nummerierte Listen und eingerückten Code. Der Splice muss je Absatz
   belegen, dass die Wortfolge unverändert bleibt — das war der Grund, warum D223 den Reflow
   abgelehnt hat, und es ist die Bedingung, unter der er jetzt zulässig ist.
2. **Die MUSS-Aussagen gegen ihre Prüfer messen.** Eine endliche, mechanisch aufzählbare Menge;
   jede Aussage hat entweder einen Test oder ist ein Befund. Das ist der Spec-Review, der Zahlen
   liefert statt Eindrücke, und er ist billiger als ein Durchlesen, das Funde in zufälliger
   Reihenfolge produziert.
3. **Eine zweite Implementierung von Layer 01 in einer anderen Sprache**, gegen die bestehenden
   Golden Anchors. Kanonische CBOR-Kodierung, Signaturprüfung, die elf Reject-Codes, die acht
   Zustände. Jede Stelle, an der die zweite Implementierung abweicht oder eine Rückfrage erzwingt,
   ist eine Mehrdeutigkeit der Spec, die sich von allein meldet. Das ist ein Review, der sich
   selbst durchführt, und der Schnitt ist klein genug für einen Lauf: Layer 01 ist die Schicht,
   auf der alles andere steht.

**Verworfen für jetzt, mit Grund.**

- **Layer 05.** Enforcement ohne beobachtete Verstöße ist Spekulation über Verhalten. Die
  Beta-Reputation trägt ein ungelöstes Moral-Licensing-Problem, das ohne Daten nicht zu
  entscheiden ist.
- **Weitere Arbeit an der Zitiergrammatik.** Mit D232 erschöpft; wer dort weitermacht, braucht
  einen benannten Grund.
- **Die Föderation weiter ausbauen.** Mit D235 und D236 entschieden; alles Weitere verlangt
  Teilnehmer.

**Der Zustand, der dabei nicht unbemerkt bleiben soll.** Der größte Reifegradmangel ist kein
technischer. `08 §2.2` verlangt Menschen mit einem echten gemeinsamen Anliegen, und es gibt sie
nicht. Alles hier ist gegen sich selbst geprüft. Eine zweite Implementierung ist der beste
verfügbare Ersatz für die fehlende Außenprüfung — sie bringt einen zweiten Blick ein, keinen
zweiten Menschen —, und keine Menge weiterer Spec-Arbeit ersetzt ihn. Warten bleibt ein zulässiger
Zustand; die letzten Läufe haben allerdings überwiegend das Werkzeug geschärft und nicht das Werk.

---

### D238 — Die Stummelzeilen aus `00w`: vierzehn sind zu glätten, drei nicht

**Anlass.** D223 hat den Reflow abgelehnt und die Nebenwirkung mit einer Zahl benannt: von 46
eingefügten Zeilen sind 17 kürzer als 40 Zeichen. D237 hat ihn als ersten Schritt wieder
zugelassen, unter der Bedingung aus D223, dass je Absatz die unveränderte Wortfolge belegt wird.
Beim Nachrechnen fällt die Menge auseinander.

**Die siebzehn sind einzeln lokalisiert.** Aus `git show e98b7f2` wurden die eingefügten Zeilen
unter 40 Zeichen genommen und im Arbeitsstand gesucht; jede kommt genau einmal vor. Ein Muster
ersetzt das nicht: die Suche nach kurzen Zeilen mitten im Absatz liefert über die neun betroffenen
Dateien 54 Treffer und trifft in sieben von neun Dateien die falsche Zahl. Das bestätigt D237 an
einem kleineren Ausschnitt.

**Drei Blöcke sind nicht zu glätten**, jeder aus eigenem Grund. Zeilennummern im Stand vor dem
Lauf:

| Ort | Block | Grund |
| --- | --- | --- |
| `00 §9` | 537-540 | die kurze Zeile ist der Absatzschluss; ein Greedy-Umbruch ergibt den Ist-Zustand |
| `07-decisions.md`, D137 | 4448-4453 | dieselbe Lage |
| `00 §6.3` | 390-395 | Greedy verkürzt sie von 16 auf 6 Zeichen und zerreißt dabei einen Verweis; mit D239 ist der Ist-Zustand bereits das Ergebnis |

**Damit ist die 17 kein Maß.** Eine eingefügte Zeile unter 40 Zeichen ist nicht dasselbe wie eine
Stummelzeile: jeder umbrochene Absatz endet mit einer Restzeile, und die darf kurz sein. Der
prüfbare Begriff ist die kurze Zeile, der im selben Absatz noch eine folgt. Nach ihm sind es
vierzehn.

**Beschluss.** Die vierzehn Blöcke werden neu umbrochen, greedy auf 100 Zeichen, unter der Regel
aus D239. Die drei übrigen bleiben unverändert; sie sind kein Befund und gehören nicht auf die
offene Liste.

**Gemessen vor der Auslieferung.** Sieben Dateien, vierzehn Blöcke, jeder Anker genau einmal im
Bestand. Wortfolge je Block nach Normalisierung des Umbruchs gleich, ausgenommen die zwei
ausdrücklich beschlossenen Änderungen aus D240 und D241. Keine neu erzeugte Zeile über 100
Zeichen, keine Restzeile unter 40 Zeichen mit Nachfolger im selben Absatz.

| Datei | Blöcke | Zeilen |
| --- | --- | --- |
| `01-claim-atom.md` | 4 | 925 auf 922 |
| `02-golden-anchors.md` | 1 | 503 auf 503 |
| `04-governance.md` | 2 | 799 auf 797 |
| `06-services.md` | 3 | 409 auf 406 |
| `example-nucleus.md` | 1 | 417 auf 416 |
| `genesis-bindung-prompt.md` | 1 | 101 auf 100 |
| `werkzeuge.md` | 2 | 385 auf 383 |

Summe 3539 auf 3527, gezählt wie `wc -l`. `tools/check_specs.py` meldet je Datei eine Zeile mehr,
weil es `text.count` über die Umbrüche plus eins rechnet; das ist kein Widerspruch.
`00-nucleus-genesis-constitution.md` und `07-decisions.md` bleiben vom Reflow unberührt.

---

### D239 — Ein Verweis und ein Code-Span werden nicht über die Zeilengrenze getrennt

**Anlass.** Der erste gerechnete Reflow zu D238 hat zwei qualifizierte Verweise auf zwei Zeilen
verteilt, den auf die Gov-Spec in `00 §6.3` und den auf die Vision in `06 §2`, und einen
Inline-Code-Span in `01 §2.2` gespalten.

**Die Wirkung ist nicht kosmetisch.** `SECTION_REF` in `tools/check_specs.py` verlangt den Namen
unmittelbar vor dem Paragraphenzeichen, getrennt durch genau ein Leerzeichen. Ein Zeilenumbruch an
dieser Stelle macht den Verweis für die Prüfung unsichtbar. Er wird nicht falsch, er wird nicht
mehr geprüft, und `make check-specs` bleibt grün. Gemessen: ohne die Regel fallen die gefundenen
Verweise in `00-nucleus-genesis-constitution.md` von 67 auf 66 und in `06-services.md` von 44 auf
43; mit der Regel bleiben beide Zahlen stehen. Für Code-Spans dieselbe Lage in schwächerer Form:
die Zahl der Zeilen mit ungerader Backtick-Zahl steigt in `01-claim-atom.md` von 38 auf 40 und
fällt mit der Regel auf 38 zurück.

**Norm.** Wer Prosa umbricht, trennt einen qualifizierten Verweis der Form Name-Paragraph-Ziffer
und einen Inline-Code-Span nicht über die Zeilengrenze. Beide gelten beim Umbrechen als ein Wort.

**Offen, nicht beschlossen.** Diese Klasse ist die erste im Umfeld der Zitiergrammatik, die
mechanisch entscheidbar ist: eine Zeile endet auf einen über `LAYER_FILES` oder einen Dateistamm
auflösbaren Namen, die folgende beginnt mit dem Paragraphenzeichen. Sie hat das Blindquotenproblem
nicht, an dem D229 und D233 gescheitert sind, weil sie keine Sachaussage prüft, sondern eine Form.
D237 verlangt für weitere Arbeit an der Zitiergrammatik einen benannten Grund; er liegt hier vor,
ohne dass er heute eingelöst werden muss.

---

### D240 — Der Aufnahmetest in `06 §10` war über den Zeilenumbruch getrennt

**Befund.** In `06-services.md` steht seit Layer 06 eine mit Bindestrich abgebrochene Wortfolge am
Zeilenende und ihre Fortsetzung am Anfang der Folgezeile. Markdown macht aus einem weichen Umbruch
ein Leerzeichen; im gerenderten Text steht dort also ein Leerzeichen mitten im Wort. Der Umbruch
aus `00w` hat die Stelle nicht verursacht, er hat sie nur an eine Stummelzeile geheftet. Es ist die
einzige Stelle dieser Art im Bestand: die Suche nach einem Bindestrich am Zeilenende über alle
`.md` findet genau eine.

**Beschluss.** Die Trennung wird geschlossen, das Wort in einem Stück geschrieben. Das ist eine
Änderung der Wortfolge und damit ausdrücklich nicht von der Bedingung aus D223 gedeckt; sie steht
deshalb hier und nicht in D238. Der Reflow ist der Anlass, nicht der Grund — ohne ihn bliebe die
Stelle im Quelltext unauffällig und im Rendering falsch.

---

### D241 — Der Kopfblock von `02-golden-anchors.md` trennte zwei Angaben ohne Leerzeile

**Befund.** Die Zeilen 3 bis 6 tragen zwei Kopfangaben, die Revision samt Geltungsbereich und den
Zweck der Datei. Zwischen ihnen steht keine Leerzeile, also sind sie ein einziger Absatz. Gerendert
laufen sie schon heute in eine Zeile zusammen. Ein Reflow ohne Reparatur hätte diesen Zustand in
den Quelltext geschrieben, tokengleich und trotzdem falsch.

**Beschluss.** Vor die Zweckangabe wird eine Leerzeile gesetzt; der verbleibende Block aus drei
Zeilen wird umbrochen und ergibt zwei. Die Datei behält dadurch ihre 503 Zeilen. Das ändert das
Rendering — aus einem Absatz werden zwei — und ist die einzige Änderung dieses Laufs, die man
sieht statt sie nur zu lesen.

---

### D242 — Punkt 2 aus D237: vierzehn Pflichten, geprüft mit der Rücknahmeprobe

**Die Menge, gemessen.** Über die acht normativen Layer-Dateien stehen 24 RFC-2119-Marker: 16 MUSS,
1 MUSS NICHT, 4 SHOULD, 3 MAY. Gezählt werden Vorkommen, nicht Zeilen — die Zählung ist damit
unabhängig davon, wie der Reflow aus D238 umbrochen hat. Davon abzuziehen sind ein Falsch-Positiv
und zwei Dubletten: `03 §3.3.3` zitiert eine ausdrücklich **überholte** Formulierung, um zu
erklären, warum sie überholt ist; VR-02.1 in `02 §4` läuft über zwei Zeilen; und die
Alias-Invariante steht einmal als Prosa in `01 §2.2` und einmal als Kommentar in der Grammatik in
Anhang A derselben Datei. Es bleiben vierzehn distinkte Pflichten. Die vier SHOULD und die drei
MAY sind nicht Teil dieses Laufs: eine Erlaubnis verlangt keinen Prüfer, und die beiden SHOULD
zu `D >= C₀` in
`00 §4.0` und `02 §8` stehen seit D147 mit demselben Befund auf der offenen Liste.

| | Pflicht | Ort |
| --- | --- | --- |
| N01 | `akt.N` ist gesetzt und passt zum aufgelösten Scope | `00 §7` |
| N02 | ein Alias trifft das kanonische Muster nicht | `01 §2.2`, Anhang A |
| N03 | Bindungsregel: `N` ist gesetzt | `01 §2.2` |
| N04 | `N` entspricht dem aufgelösten Scope | `01 §2.2` |
| N05 | bei kanonischer Kodierung gilt Byte-Gleichheit | `01 §2.2` |
| N06 | der Verifizierer serialisiert neu und vergleicht byte-genau | `01 §3` |
| N07 | der Verifizierer ignoriert `t_exp` auf einem `core/*`-Claim | `01 §5.3` |
| N08 | VR-02.1: die Aggregation rechnet simultan | `02 §4` |
| N09 | ein Vouch trägt `t_exp`, wo die Budgetregel gilt | `02 §6.2` |
| N10 | ein vorhandenes `v` trägt den deklarierten Typ | `03 §1.3` |
| N11 | dieses `N` ist der ausgewertete Scope | `03 §1.4` |
| N12 | `irrevocable_predicates` enthält `vote@1` und `ratify@1` | `04 §1.1` |
| N13 | `decide` rechnet die Genesis-Bindung vor jedem Feldzugriff nach | `04 §3.5` |
| N14 | es wird geworfen, nicht vermerkt | `04 §4.5` |

Die Ortsangaben sind gemessen, nicht geschlossen. Neun von vierzehn waren beim ersten Ansatz aus
der Zeilennummer geraten und falsch; erst der Abgleich gegen die Überschriften hat sie berichtigt.
Prüfregel 27 in der Fassung, die für eigene Zwischenergebnisse gilt.

**Verworfen: die Zuordnung über Stichworte.** Ein erster Anlauf hat je Pflicht Suchbegriffe
gebildet und ihre Treffer über die 77 Testdateien gezählt. Das Ergebnis misst Vokabular statt
Prüfung: für N11 meldet `test_rotate_key.py` 133 Treffer, weil das Wort Scope überall vorkommt,
für N09 meldet `tp02.py` 55 Treffer auf `t_exp`. Eine solche Tabelle sähe aus wie ein Beleg und
wäre keiner — dieselbe Blindquote, an der D229 und D233 mit Zahlen gescheitert sind, nur in
anderer Verkleidung.

**Das Verfahren: die Rücknahmeprobe.** Eine Pflicht hat genau dann einen Prüfer, wenn ihre
Durchsetzung im Produktivcode zurückgenommen werden kann und daraufhin mindestens ein Test rot
wird. Bleibt der Lauf grün, ist die Pflicht ungeprüft, und das ist der gesuchte Befund. Findet sich
keine durchsetzende Stelle, ist die Pflicht ohne Träger — ein schwererer Befund derselben Art. Das
ist kein neues Instrument: dieselbe Probe verlangt die Prompt-Regel für jeden neu entstehenden
Regressionstest, hier auf bestehenden Code angewandt.

**Ausgelagert.** Vierzehn Neutralisierungen mit je einem Testlauf gehören zum Werkzeug, nicht in
diesen Kanal; durch ihn müsste sonst der halbe Produktivcode laufen. Zurück kommt je Pflicht die
durchsetzende Stelle, die rot gewordenen Tests namentlich, oder die Feststellung, dass keiner rot
wird.

---

### D243 — Die RFC-2119-Marker sind keine Landkarte der Normativität

**Befund.** Die Marker verteilen sich über die Layer so: `00` zwei, `01` zehn, `02` vier, `03`
drei, `04` drei, `06` zwei, `05` null, `08` null. Layer 02 ist durchweg normativ — die Budgetregel,
die Kapazitätsformel, die Determinismusforderung an die Aggregation — und trägt vier Marker, von
denen zwei dieselbe Aussage in zwei Zeilen sind. `06-services.md` trägt zwei, und beide sind MAY.
Die Marker sind also eine dünn und uneinheitlich gesetzte Teilmenge der Normativität, keine
Aufzählung von ihr.

**Was daraus nicht folgt.** Kein Auftrag, die Spec mit Markern nachzurüsten. Zu entscheiden,
welcher Satz einen verdient, ist Ermessensarbeit ohne mechanische Grenze — genau die Klasse, die
D229 und D233 mit gemessenen Zahlen verworfen haben. Wer sie doch aufmacht, misst vorher die
Falsch-Positiv-Rate an einer Datei mit bekannter Wahrheit.

**Was folgt.** D237 Punkt 2 leistet weniger, als sein Name verspricht. Das Ergebnis aus D242 sagt
über die vierzehn markierten Pflichten etwas und über die übrige Normativität nichts. Wer es
zitiert, zitiert diese Grenze mit.

---

### D244 — Eine abgeleitete `numstat`-Erwartung zieht die randgleichen Zeilen ab

**Anlass.** Für den Lauf zu D238 war die Erwartung mit +179 −82 fixiert und wurde mit +147 −50
gemessen. Die Abweichung war kein Defekt, sondern ein Fehler in der Ableitung: gerechnet war je
Block die vollständige Alt-Menge als Löschung und die vollständige Neu-Menge als Einfügung.

**Die Ursache.** Git zieht Zeilen, die am oberen oder unteren Rand eines Blocks unverändert
bleiben, nicht in den Hunk. Nachgerechnet sind es über die vierzehn Blöcke 32 solcher Zeilen, und
179 minus 147 wie 82 minus 50 ergeben genau 32; je Datei stimmt es einzeln ebenfalls, mit 9 in
`werkzeuge.md`, 8 in `06-services.md` und 7 in `01-claim-atom.md`.

**Norm.** Wer eine `numstat`-Erwartung aus einer Blockersetzung ableitet, zieht je Block die am
Rand gleich gebliebenen Zeilen von beiden Seiten ab. Ohne diesen Abzug ist die Erwartung
systematisch zu hoch, und eine Abweichung, die nichts bedeutet, sieht aus wie ein Befund. Das
ergänzt Prüfregel 41 um einen Fall, in dem die Abweichung vor der Bewertung gerechnet werden kann.

---

### D245 — Die Rücknahmeprobe misst die Stelle, nicht die Pflicht, solange Träger redundant sind

**Anlass.** Der Lauf zu D242 hat vierzehn Pflichten geprobt und elf als geprüft, drei als
ungeprüft klassifiziert. Bei zweien beantwortet die Messung eine andere Frage als die gestellte.

**Der Befund im Code.** Vier Module berechnen unabhängig voneinander
`SHA-256(DOM_NUC_GEN ‖ cbor(genesis_obj))` und vergleichen das Ergebnis mit `scope`:
`governance/chain.py`, `profiles/policy.py`, `keys.py` und `trust/params.py`. Die Bedingung ist
byte-gleich, die geworfene Meldung wortgleich. Drei weitere Stellen werfen wortgleich zur
Policy-Bindung: `profiles/membership.py`, `profiles/verdict.py`, `profiles/credit.py`. Für N11
nennt der Befund vier parallele Träger in `credit.py`, `verdict.py`, `membership.py` und
`tally.py`, von denen einer geprobt wurde.

**Warum das die Aussage bricht.** Wird eine von vier gleichwertigen Stellen neutralisiert und der
Lauf bleibt grün, ist damit gezeigt, dass *diese Stelle* für die bestehenden Tests unsichtbar ist —
nicht, dass die Pflicht ungeprüft ist. Ein Test, der über einen anderen Einstiegspunkt läuft,
bekommt dieselbe Ausnahme von einer der übrigen drei. N14 ist deshalb nicht ungeprüft, sondern
unbestimmt. Bei N11 wurde ein Test rot, die Klasse stimmt also; die drei übrigen Träger sind
trotzdem ungemessen, und ohne sie ist offen, ob dort etwas fehlt.

**Norm.** Wer eine Pflicht mit der Rücknahmeprobe misst, bestimmt zuerst die vollständige Menge
ihrer Träger und neutralisiert sie geschlossen. Erst dann heißt ein grüner Lauf, dass die Pflicht
ungeprüft ist. Bleibt bei geschlossener Neutralisierung ein Test rot, ist sie geprüft, auch wenn
keine Einzelstelle für sich rot zu färben war.

**Was nicht folgt.** Die vierfache Prüfung ist kein Defekt. `04 §3.5` verlangt die Bindung vor
jedem Feldzugriff, und jede der vier Funktionen ist ein eigener Einstiegspunkt, der sie nicht
voraussetzen darf. Redundanz ist hier die Umsetzung der Norm, nicht ihr Versagen. Was fehlt, ist
nicht eine Zusammenlegung, sondern das Wissen, ob alle vier gemeint sind — das entscheidet ein
eigener Eintrag nach dem Nachlauf.

**Verhältnis zu Prüfregel 41.** Die Regel verlangt, eine Abweichung zu bewerten, bevor sie als
Defekt gilt. D245 ergänzt den umgekehrten Fall: eine *ausbleibende* Abweichung ist erst dann ein
Befund, wenn ausgeschlossen ist, dass ein paralleler Träger sie aufgefangen hat.

---

### D246 — Abnahme der Rücknahmeproben: zwölf Pflichten, zehn geprüft

**Der Lauf.** `00ab-mussproben`, Prompt-Commit `28afdde`, Proben in `c9ada0e`, Nachlauf in
`e03ec1d`. Befund in `00ab-mussproben-befund.md`. Produktivcode, Tests und Werkzeuge sind
unberührt; der Diff gegen den Branchpunkt enthält nur die Befunddatei und die beiden Dateien
dieses Auftrags. `make check-all` grün, 597 Tests plus 14 Eigenschaftstests.

**Die Menge ist zwölf, nicht vierzehn.** Zwei der vierzehn Kennungen aus D242 benennen keine
eigene Pflicht, und das ist ein Ergebnis des Laufs, nicht eine nachträgliche Zurechtlegung.
N05 ist die Konkretisierung von N04 für den kanonischen Fall und teilt sich mit ihr eine einzige
Vergleichsstelle; eine Neutralisierung, die nur eine von beiden träfe, gibt es nicht. N01 hat
keinen eigenen Träger: `00 §7` schreibt die Bindungsregel nicht selbst vor, sondern verweist für
sie auf `01 §2.2`, und der Code setzt sie generisch für jedes `nuc:`-Prädikat am Einlesepfad
durch. Damit zählt N01 wie N02 bis N05 zur Atom-Bindungsregel.

**Ergebnis.**

| Klasse | Pflichten |
| --- | --- |
| geprüft | N03, N04, N06, N08, N09, N10, N11, N12, N13, N14 |
| unbestimmt | N02 |
| ungeprüft | N07 |
| ohne Träger | keine |

**Was der Nachlauf gedreht hat.** N14 galt nach der ersten Probe als ungeprüft. Geschlossen
neutralisiert über alle vier Träger werden sechs Tests rot; die Pflicht ist geprüft, und der erste
Befund war ein Artefakt der Einzelstelle. Bei N11 hat der Nachlauf acht Träger gefunden statt der
fünf des ersten Befundes — die Argumentprüfung in `verdict_status` war ungenannt — und alle acht
zugleich neutralisiert ergeben acht rote Tests. Beide Male hat D245 gegriffen.

**Zwei Einschränkungen, die das Wort geprüft nicht trägt.** N09 ist über den Vermerk
`VOUCH_WITHOUT_TEXP` geprüft, und dieser Vermerk bleibt nach D119 ausdrücklich **ohne Wirkung**:
der Vouch bleibt im Budget-Set und bindet weiter unbegrenzt. Die Pflicht aus `02 §6.2` ist damit
beobachtet, nicht durchgesetzt — beschlossen so, nicht versehentlich. N10 hat drei
Erzeugungsstellen für `INVALID_V_TYPE` in `profiles/credit.py` und genau eine Teststelle; rot wird
der Lauf über Key 0 der Obligation, Key 1 und die Quittung sind ungemessen. Wer die Zahl zehn
zitiert, zitiert diese beiden Fußnoten mit.

**Grenze der Aussage.** Es gilt weiter D243: gemessen sind die markierten Pflichten, nicht die
Normativität der Spec.

---

### D247 — N07: der Vektor trägt nicht, was der Test zu sehen behauptet

**Befund.** `01 §5.3` verlangt, dass ein Verifizierer ein `t_exp` auf einem `core/*`-Claim
ignoriert. `_is_temporally_valid` löst das mit einem frühen `return True` für `core/*`. Wird dieser
Zweig entfernt, bleibt der Lauf grün: der einzige Test dafür klassifiziert TV3, und TV3 trägt kein
`t_exp`. Ohne gesetztes `t_exp` greift die nächste Zeile mit demselben Ergebnis. Der Test kann
nicht sehen, was er zu sehen behauptet.

**Dieselbe Klasse wie D117.** Auch dort prüft ein Test eine schwächere Aussage, als sein Name
verspricht, weil die Welt die Bedingung nicht herstellt. Der Unterschied: dort steht der Vorbehalt
in einer Ankerdatei, hier hätte ihn niemand bemerkt.

**Beschluss.** Die Reparatur ist ein Vektor oder eine Sondierwelt mit einem `core/*`-Claim, der
ein abgelaufenes `t_exp` trägt, und ein Test, der dessen Gültigkeit prüft. Sie gehört in einen
eigenen Lauf mit Rücknahmeprobe: ohne den `core/*`-Zweig muss der neue Test rot werden. Nicht in
dieser Sitzung.

---

### D248 — N02: der Alias-Lookahead ist tot, und die Probe hat es nicht gezeigt

**Befund im Code.** `parse_predicate` prüft `_CANONICAL_SCOPE` vor `_ALIAS_SCOPE`. Ein
scope-Teil aus 64 Hexziffern wird deshalb im ersten Zweig gefangen und erreicht den zweiten nie.
Der negative Lookahead in `_ALIAS_SCOPE` kann also nichts ausschließen, was nicht schon
ausgeschlossen wäre. Zweiter Fall derselben Art in `resolve_scope`: in der Bedingung
`claim.N is None or claim.N != expected` ist der linke Zweig redundant, weil `None` nie gleich
`expected` ist. Träger der Pflicht ist dort allein die Prüfung im Alias-Zweig.

**Warum die Klasse unbestimmt ist und nicht ungeprüft.** Die Probe hat die beiden Lookaheads
neutralisiert und die **Reihenfolge** stehen lassen. Die Reihenfolge ist aber der eigentliche
Träger. Nach D245 wäre geschlossen zu neutralisieren, also zusätzlich die beiden Zweige zu
tauschen. Das ist nicht gemessen worden, und die Vermutung, dass dann
`test_alias_matching_64_hex_rejected` rot wird, bleibt eine Vermutung. D245 ist beim Schreiben
selbst an dieser Stelle nicht angewandt worden.

**Beschluss.** Nicht in dieser Sitzung nachmessen: eine Pflicht von zwölf, gegen eine dritte
Werkzeugrunde. Der Punkt geht offen und ausdrücklich als ungemessen auf die Liste. Die Reparatur —
toten Lookahead und redundante Bedingung löschen — ist eine Codelöschung und gehört zusammen mit
der Probe in einen Lauf.

---

### D249 — Die drei Normen aus `00ab` erhalten die Nummern 47 bis 49

**Anlass.** D239, D244 und D245 sind als Norm formuliert worden, ohne eine Prüfregelnummer zu
bekommen; `pruefregeln.md` blieb bei 46. Das ist derselbe Zustand, den D144 für die Parallelen-
und die Begründungspruefung beschrieben hat: ohne Nummer ist eine Regel in einem Prompt nicht
zitierbar, und was nicht zitierbar ist, wirkt nicht. Der Verlust wäre still gewesen — die
Registereinträge bleiben ja stehen und lesen sich richtig.

**Beschluss.** 47 aus D239, 48 aus D244, 49 aus D245. Der Volltext steht in `pruefregeln.md`, wie
D144 es für alle Regeln festgelegt hat; die Registereinträge behalten Anlass, Messung und
Begründung. Die Herkunftsliste am Dateiende wird mitgezogen.

**Was der Volltext gegenüber dem Registereintrag verliert.** Regel 49 nennt vier Module für die
Genesis-Bindung und drei für die Policy-Bindung, nicht die Modulnamen; die stehen in D245. Die
vier parallelen Träger zu N11 sind im Regeltext weggelassen, weil sie den Fall nicht schärfen.
Eine Regel ist ein Merksatz mit Beleg, kein Ersatz für den Eintrag.

**Einordnung.** Angehängt an den letzten Abschnitt, wie 37 bis 46 vor ihnen. Die angekündigte
Ordnung nach dem Zeitpunkt, an dem eine Regel greift, ist für die Nummern ab 37 faktisch die
Ordnung ihrer Entstehung: 38, 39, 40, 43 und 46 stehen unter einer Überschrift über Tests und
handeln nicht von Tests. Das ist ein Befund an der Gliederung, keine Änderung an ihr; er geht auf
die offene Liste.

**Nicht beschlossen.** Der Kandidat aus `00ab` — eine neu formulierte Norm wird vor dem Commit
gegen die offenen Befunde derselben Sitzung gehalten — bekommt hier keine Nummer. Sein einziger
Anlass ist D248, wo D245 im selben Eintrag nicht angewandt wurde. Er wird formuliert, wenn der
Nachlauf zu D248 gemessen hat, ob die Anwendung der Norm den Befund verändert hätte; vorher ist
offen, ob die Regel den Fehler gefangen oder nur benannt hätte.

**Was nicht dazugehört.** Kein Test und kein Werkzeug liest die Zahl der Prüfregeln.
`tools/register_index.py` und `tools/splice_run.py` nennen Regelnummern nur im Docstring. Der
Splice berührt zwei Markdown-Dateien und keine Zusicherung.

---

### D250 — TV5: der Vektor für `t_exp` auf `core/*` wird als C.9 angehängt

**Anlass.** D247 hat den Befund festgehalten: `test_core_revoke_ignores_t_exp` klassifiziert TV3,
und TV3 trägt kein `t_exp`. Der Test kann nicht sehen, was sein Name behauptet. Nachgelesen ist
die Lage genau so — der Core von TV3 trägt die Keys 0, 1, 2, 3, 6 und 8; Key 7 fehlt, und die
Überschrift von C.3 sagt es ausdrücklich.

**Vektor statt Sondierwelt.** D247 hatte beides offengelassen. Anhang C ist das einzige Artefakt,
das die Zweitimplementierung aus D237 sehen wird; eine Reparatur, die nur in einer Python-Welt
lebt, prüft die Verifizierer-Pflicht aus `01 §5.3` nur in Python. Die Pflicht ist aber genau von
der Art, die eine fremde Implementierung falsch machen wird, wenn niemand sie ihr vorlegt.

**Angehängt, nicht eingeschoben.** Ein TV5 zwischen C.4 und C.5 würde C.5 bis C.8 verschieben. Auf
`§C.8` zeigen sechs Stellen in fünf Dateien. Eine Umnummerierung ist der Fehlertyp, den die
Verweisprüfung nach D229 nicht sehen kann: das Ziel existiert weiter, es bedeutet nur etwas
anderes. Der Preis ist die gebrochene Gruppierung — C.1 bis C.4 positiv, C.5 bis C.7 negativ, C.8
Bytes, C.9 wieder positiv. Das ist billiger als sechs stille Fehlverweise.

**Ziel ist TV1, nicht TV2.** TV5 widerruft einen Claim, den TV3 bereits widerrufen hat. Die
Wiederholung ist Absicht: in jedem Store, der TV3 enthält, ändert TV5 keinen Zustand.
`tests/trust/test_coupling.py` lädt alle Vektoren mit `signed_bytes` in einen Store; dort wird nur
die Kopplung geprüft, aber ein Vektor, der beim Hinzufügen fremde Zustände kippt, macht künftige
Erwartungen von seiner Anwesenheit abhängig. Der Vektor trägt eine Eigenschaft, keine Wirkung.

**Wohlgeformtheit.** `t` ist 1700000300, `t_exp` ist 1700000400. `INCOHERENT_EXPIRY` verlangt
`t < t_exp`; die Bedingung ist erfüllt, der Claim ist strukturell gültig. Nach `01 §B.3` ist
`t_exp` auf `core/*` ausdrücklich kein Reject-Grund.

**Gerechnet, nicht getippt.** Dieselbe Kette reproduziert TV1 und TV3 byteweise gegen die
committeten Werte; erst danach ist TV5 gerechnet worden. `claim_id` ist
`8b19196274b2a8ac08e9a34337de5f445e6efd19fb75155eb187b069f5fd8022`. Der Lauf erzeugt den Vektor
unabhängig neu; trifft er den Wert nicht, ist das ein Befund und keine Nachziehung.

---

### D251 — Die in D248 beschlossene Löschung wird zurückgenommen

**Was D248 beschlossen hat.** Den toten Lookahead in `_ALIAS_SCOPE` und die redundante Bedingung
in `resolve_scope` zu löschen. Der Beschluss stand, bevor gemessen war, was die Lookaheads sind.

**Sie sind normativer Text.** Anhang A von `01-claim-atom.md` druckt die äquivalenten Regexe zur
ABNF, und dort steht der negative Lookahead wörtlich in beiden Formen — in der Alias-Regex und in
der zusammengesetzten nuc-Regex. Die ABNF-Zeile für `alias-scope` trägt die Ausschlussregel als
Begleitnorm, und `01 §2.2` Regel 2 macht sie zur MUSS-NICHT-Aussage. Was `predicates.py` trägt,
ist die Spiegelung einer gedruckten Norm, nicht eine Bequemlichkeit des Autors.

**Zwei Messungen.** Über 200000 erzeugte Kandidaten unterscheidet sich die Alias-Regex ohne
Lookahead in drei Fällen von der mit; sie ist also nicht sprachlich tot, sondern nur tot relativ
zur Zweigreihenfolge in `parse_predicate`. Die zusammengesetzte nuc-Regex unterscheidet sich in
null Fällen — dieser Lookahead ist unbedingt wirkungslos, und zwar in der gedruckten Fassung
ebenso wie in der implementierten. Das gehört an Anhang A und nicht an das Modul; siehe D252.

**Dieselbe Begründung trägt die redundante Bedingung.** `claim.N is None or claim.N != expected`
spiegelt die zwei MUSS aus `01 §2.2` Regel 3: `N` muss gesetzt sein, und `N` muss entsprechen. Wer
den linken Zweig streicht, behält das Verhalten und verliert die Entsprechung zum normativen Satz.
Prüfregel 8 legt beide nebeneinander; der Gewinn wäre eine Zeile, der Verlust die Lesbarkeit der
Spiegelung.

**Was folgt.** Keine Löschung in `predicates.py`. Der Befund aus D248 bleibt gültig als
Beschreibung — beide Stellen können in der heutigen Anordnung nichts ausschließen —, aber die
Folge ist nicht die Streichung. D248 ist damit in seinem Beschlussteil überholt und in seinem
Befundteil bestätigt.

---

### D252 — Der Lookahead in der gedruckten nuc-Regex kann nichts ausschließen

**Befund.** Anhang A von `01-claim-atom.md` druckt für das nuc-Prädikat eine Regex, deren
Alias-Alternative den negativen Lookahead auf 64 Hexziffern mit Zeilenende-Anker trägt. An dieser
Stelle folgt aber zwingend ein Schrägstrich mit Name und Version, das Zeilenende ist dort nie
erreichbar, und die Alternative davor fängt 64-Hex ohnehin zuerst. Gemessen: null Unterschiede
zwischen der gedruckten Regex und derselben ohne diesen Lookahead über 200000 Kandidaten.

**Warum das nicht sofort repariert wird.** Der Lookahead spiegelt die Alias-Regex zwei Zeilen
darüber, wo er wirkt. Ob die Spiegelung mehr wert ist als die Genauigkeit, ist eine Frage an den
Text und nicht an den Code; sie wird nicht nebenbei in einem Lauf entschieden, der Vektoren baut.
Der Punkt geht offen auf die Liste.

**Was ausdrücklich nicht folgt.** Die Grammatik ist nicht falsch. Eine Regex, die eine Bedingung
zweimal ausdrückt, akzeptiert dieselbe Sprache; der Mangel ist Lesbarkeit, nicht Semantik.

---

### D253 — N02 ist geprüft, sobald geschlossen neutralisiert wird

**Die Lage.** D248 hat N02 als unbestimmt eingetragen: die Probe hatte die Lookaheads
neutralisiert und die Zweigreihenfolge stehen lassen. Nach D245 ist das die Einzelprobe an einem
von zwei Trägern.

**Vier Zellen, an einem Modell der beiden Funktionen gerechnet.** Lookahead vorhanden und
kanonisch zuerst: kein Test rot. Lookahead vorhanden, Alias zuerst: kein Test rot. Lookahead
entfernt, kanonisch zuerst: kein Test rot. Lookahead entfernt **und** Alias zuerst: ein
64-Hex-Scope wird als Alias klassifiziert, und `test_alias_matching_64_hex_rejected` wird rot.

**Folge.** Die Pflicht aus `01 §2.2` Regel 2 ist getragen, nicht ungeprüft. Keine Einzelstelle ist
für sich rot zu färben, und genau diesen Fall nennt Prüfregel 49 als geprüft. N02 wandert von
unbestimmt nach geprüft, sobald der Lauf die vierte Zelle im Repo bestätigt.

**Der Vorbehalt.** Gerechnet ist ein Modell, das die Logik von `parse_predicate` und
`resolve_scope` nachbildet, nicht der Code selbst. Die Bestätigung ist Aufgabe des Laufs; bleibt
die vierte Zelle grün, ist der Eintrag falsch und wird zurückgenommen, nicht angepasst.

---

### D254 — Korrektur zu D253: vier rote Tests, nicht einer

**Gemessen.** Probe B3 färbt vier Tests in `tests/test_predicates.py` rot:
`test_parse_canonical_nuc`, `test_bad_scope_binding_wrong_n`, `test_alias_matching_64_hex_rejected`
und `test_alias_that_looks_like_hex_but_wrong_n`. B1 und B2 färben keinen. Die Aussage von D253
steht damit: die geschlossene Neutralisierung sieht die Pflicht, jede Einzelneutralisierung sieht
sie nicht. N02 ist geprüft.

**Falsch war die Zahl.** Das Modell in D253 hat drei Fälle gerechnet und dabei `resolve_scope`
nachgebildet. Drei der vier roten Tests behaupten aber über `parse_predicate`: sie prüfen die
Klassifikation eines Scopes als kanonisch oder Alias, nicht das Ergebnis der Auflösung. Der vierte
verlangt einen Fehler bei kanonischem Scope mit falschem `N`; wird derselbe String als Alias
gelesen, ist `N` die einzige Scope-Quelle, der Vergleich entfällt und der Fehler bleibt aus. Keinen
dieser drei konnte das Modell sehen, weil es sie nicht enthielt.

**Die Fehlklasse.** Nicht das Modell war falsch, sondern die Reichweite der daraus abgeleiteten
Aussage. Aus einem Modell, das drei von achtzehn Tests einer Datei nachbildet, ist eine Aussage
über die Zahl der roten Tests geworden. Das Abnahmekriterium hätte den Aliastest als mindestens
rot verlangen müssen, nicht als einzigen roten Test.

**Was das Werkzeug richtig gemacht hat.** Gemeldet und nicht angepasst — die Meldung stand vor dem
Diff und war der Grund, den Punkt überhaupt nachzurechnen.

**Folge.** Prüfregel 50.

---

### D255 — Der Anker im Lookahead der nuc-Regex wird angepasst, nicht gestrichen

**Die Frage aus D252.** Anhang A von `01-claim-atom.md` druckt in der zusammengesetzten nuc-Regex
einen negativen Lookahead, der an seiner Stelle nichts ausschließen kann. D252 hat daraus eine
Textfrage gemacht: Spiegelung der Zeile darüber oder Genauigkeit. Beides war zu wenig gemessen.

**Der Mechanismus ist ein nicht mitgeführter Anker.** Die Alias-Regel ist verankert; ihre beiden
Anker begrenzen den Scope-String. Beim Einsetzen in die zusammengesetzte Regex wurden die äußeren
Anker angepasst — der Zeilenanfang wurde zum Präfix mit dem Namensraum, das Zeilenende wanderte
hinter die Version. Das Zeilenende-Zeichen **innerhalb** des Lookaheads wurde nicht mitgeführt und
bezeichnet seither das Ende des ganzen Prädikats, das hinter dem Scope nie erreichbar ist. Die
Fehlklasse heißt nicht "überflüssiger Lookahead", sondern "verankerte Teilregex eingesetzt,
innerer Anker nicht angepasst".

**Die Messung.** Drei Fassungen der Alias-Alternative — Bestand, ohne Lookahead, mit auf den
Schrägstrich angepasstem Anker — mal zwei Reihenfolgen der Alternativen, über 200000 Kandidaten.
Die Sprache unterscheidet sich in allen sechs Fällen in null Kandidaten; das bestätigt D252. Die
**Klassifikation** unterscheidet sich bei getauschter Reihenfolge: Bestand 25502, ohne Lookahead
25502, mit angepasstem Anker null. Der gedruckte Lookahead trägt gegen den Fall, für den er
dasteht, exakt so viel wie kein Lookahead.

**Warum Behalten die schlechteste Option ist.** D251 hat ihn als Spiegelung einer Norm behalten.
Die Spiegelung ist eine des Wortlauts, nicht der Wirkung: was der Lookahead zu sichern scheint,
sichert allein die Reihenfolge der beiden Alternativen. Behalten kostet jeden Leser die Analyse aus
D252 und liefert keine Robustheit.

**Warum Anpassen vor Streichen.** Gleiche Sprache, gleiche Länge, aber unabhängig von der
Reihenfolge der Alternativen. D254 hat gemessen, dass Reihenfolgeabhängigkeit ein Träger ist, den
keine Einzelprobe sieht. Anhang A ist das Artefakt, das eine Zweitimplementierung liest (D237); eine
Grammatik, deren Klassifikation an der Reihenfolge zweier Alternativen hängt, ist die schlechtere
Vorlage. Streichen würde diese Abhängigkeit festschreiben, statt sie aufzulösen.

**Beschluss.** In der nuc-Zeile von Anhang A wird im negativen Lookahead das Zeilenende-Zeichen
durch den Schrägstrich ersetzt. Die Alias-Zeile darüber bleibt unberührt; dort ist der Anker
richtig. `_NUC_PREDICATE` in `predicates.py` folgt im selben Commit: nach D251 ist die Zeile
Spiegelung der gedruckten Norm, und eine Spiegelung, die eine Fassung hinterherhinkt, ist die Drift,
gegen die das Register steht.

**Die Grenze.** Im Modul ist die Änderung nicht testbar. `parse_predicate` klassifiziert nicht
über die Alternation, sondern prüft die kanonische und danach die Alias-Regel einzeln;
`_NUC_PREDICATE` ist reine Formprüfung. Kein Test kann rot werden, eine Rücknahmeprobe nach
Prüfregel 49 ist nicht konstruierbar. Der Wert der Zeile liegt vollständig in der Spiegelung.

**Was nicht folgt.** N02 bleibt geprüft (D253, D254). Der Lookahead in `_ALIAS_SCOPE` bleibt
unverändert: dort ist der Anker richtig, und er ist Teil des gemeinsamen Trägers. D252 ist
geschlossen — sein Befund bleibt gültig, sein Beschlussteil war keiner.

---

### D256 — Vorentscheidung zur Zweitimplementierung von Layer 01

**Gemessen an Anhang C.** Layer 01 ist das einzige Layer ohne eigene Datei mit Golden Anchors;
Anhang C ist die gesamte Messfläche. Drei der elf Reject-Codes tragen dort einen Vektor mit
erwartetem Ausgang: der Genesis-Anker, die nicht-kanonische Kodierung und das unlesbare CBOR. Acht
tragen keinen, darunter die Signaturprüfung selbst. Von den acht Zuständen sind vier über Vektoren
belegt.

**Was daraus folgt.** D237 hält fest, jede Abweichung einer fremden Implementierung sei eine
Mehrdeutigkeit der Spec, die sich von allein melde. Das gilt für die **Rückfrage beim Lesen**. Für
die **Abweichung beim Laufen** gilt es nur dort, wo ein Vektor hinsieht. Wo keiner ist, läuft die
fremde Implementierung grün durch, und wir erfahren nichts — die teuerste Art, nichts zu lernen.

**Beschluss 1: die Messfläche zuerst.** Anhang C wird um die fehlenden Fehlerklassen erweitert,
bevor die Zweitimplementierung beauftragt wird. Das ist ein Lauf gegen die vorhandene Referenz mit
aus Anhang B abgeleiteten Erwartungen und kostet nichts von dem, was für die Zweitsprache
bereitliegt.

**Der Einwand und warum er nicht trägt.** Die Vektoren stammen vom selben Autor wie die Referenz
und können denselben blinden Fleck tragen. Das ist richtig und entscheidet nicht: ein **falscher**
Vektor wird von der Zweitimplementierung als Abweichung gemeldet und ist damit Ertrag; ein
**fehlender** Vektor erzeugt Schweigen. Ein falscher Vektor ist besser als keiner.

**Beschluss 2: der Umfang ist die zustandslose Stufe.** Gebaut wird die Prüfung von Bytes zu
Ausgang — kanonische Serialisierung nach `01 §3`, Berechnung der Claim-Kennung, Signaturprüfung,
Prädikat-Grammatik nach Anhang A, Bindungsregel nach `01 §2.2`. Nicht gebaut werden Store,
Vorgängerauflösung und Zustandsmaschine. Begründung: das ist genau die Hälfte, die Anhang C
byteweise messen kann, und die Mehrdeutigkeiten sitzen dort am dichtesten.

**Die Grenze dieser Stufe, benannt.** Ein Reject-Code ist so nicht messbar: sein aktiver Träger
sitzt nach D138 in der Zustandsprüfung und verlangt ein bekanntes Ziel. Er bleibt der
Zustandsstufe vorbehalten und wird nicht behelfsweise in einen zustandslosen Vektor gezwungen.

**Beschluss 3: gemessen wird gegen die Vektoren, nicht gegen die Referenzausgabe.** Ein Abgleich
der fremden Implementierung gegen die Ausgabe der Python-Referenz prüft die Referenz und nicht die
Spec; das ist dieselbe Zirkularität, die D196 für die Sortierung festgehalten hat. Die Erwartung
kommt aus Anhang B und aus dem gedruckten Vektor, nie aus einem Lauf der Referenz.

**Offen: die Sprache.** Sie wird nach einem Literaturcheck entschieden (Prüfregel 15) und nicht
vorab geraten. Zwei Kriterien stehen schon fest. Erstens wird die deterministische Kodierung aus
`01 §3` von Hand geschrieben und nicht aus einer Bibliothek genommen, weil sonst die Bibliothek
eines Dritten geprüft wird und nicht die Spec. Zweitens wird die Signaturprüfung ausdrücklich
**nicht** selbst gebaut: sie ist RFC 8032 und nicht MaR-normativ, eine Eigenimplementierung misst
nichts und schafft Risiko.

**Was nicht folgt.** D237 bleibt unberührt: die Zweitimplementierung ist der beste verfügbare
Ersatz für die fehlende Außenprüfung und ersetzt sie nicht.

---

### D257 — Anhang C deckt zehn der elf Reject-Codes; Prüfregel 51

**Was gebaut wurde.** Acht negative Vektoren NV4 bis NV11 in `01 §C.10`, angehängt und nicht
eingeschoben. Sie decken sieben Fehlerklassen: nicht unterstützte Version, unbekanntes J-Tag,
unbekannter Namensraum, verletzte Scope-Bindung in beiden Zweigen der Regel, reserviertes
core-Prädikat, falsche Signatur, inkohärente Ablaufzeit. Zusammen mit den drei vorhandenen trägt
Anhang C damit zehn der elf Reject-Codes. 617 Tests.

**Das Konstruktionsprinzip.** Jeder Vektor trägt genau einen Mangel und ist im Übrigen gültig und
korrekt signiert. Nur so ist der erwartete Code eindeutig, unabhängig davon, an welcher Stelle
ihrer Prüfreihenfolge eine fremde Implementierung ihn findet. Ein Vektor mit zwei Mängeln
behauptet ungewollt über die Reihenfolge.

**Die verbleibende Lücke, benannt.** Für den elften Code gibt es keinen Vektor: sein aktiver
Träger sitzt nach D138 in der Zustandsprüfung und verlangt ein bekanntes Ziel. Er gehört in die
Zustandsstufe der Zweitimplementierung und wurde nicht behelfsweise in einen zustandslosen Vektor
gezwungen.

**Die Abnahme lief ohne gelesenen Diff.** Die acht Claim-Kennungen, Signaturen und Core-Bytes
wurden aus der Feldspezifikation des Prompts unabhängig nachgerechnet und gegen drei Artefakte
gehalten: die Golden-Liste, die Vektordatei und den Anhang. Achtmal deckungsgleich in jeder
Spalte, achtmal der beauftragte Code. Von den 175 Zeilen des Anhangs wurde keine gelesen; geprüft
wurde, dass sie die gerechneten Werte enthalten.

**Die Proben.** Acht Vektoren, acht Neutralisierungen, kein Vektor ohne roten Test. Die Meldung
des Werkzeugs korrigiert eine Erwartung des Prompts: NV7 und NV8 treffen zwei verschiedene
Bedingungen in `resolve_scope` und nicht dieselbe Prüfstelle. Das war der Grund, beide Vektoren zu
bauen, und die Probe hat ihn bestätigt.

**Prüfregel 51, aus einem eigenen Fehler.** Das erste Diagnoseskript suchte die signierten Bytes
im Anhang und fand sie achtmal nicht, obwohl der Anhang fehlerfrei war: er führt nach dem Muster
von C.1 den Core und die Signatur getrennt. Die Rücknahmeprobe des Skripts hatte das nicht
gefangen, weil sie gegen den Vorzustand aus dem richtigen Grund rot war und gegen den Zielzustand
aus dem falschen. Daraus die Regel: ein Prüfer, der eine Menge misst, wird zuerst an einem
Element geeicht, das im Bestand schon steht. Ein Probelauf gegen TV1 hätte den Umlauf gespart.

**Was offen bleibt.** Die Sprache der Zweitimplementierung, nach D256 mit Literaturcheck. Die
Zustandsstufe mit dem elften Code. Die Gliederung von `pruefregeln.md`, durch Regel 51 nicht
schlechter und nicht besser geworden.

---

### D258 — Sprache, Prompt-Form und Anker der Zweitimplementierung

**Der Literaturbefund, gegen den entschieden wird.** Knight und Leveson haben 1986 an
siebenundzwanzig unabhängig gebauten Fassungen gemessen, dass unabhängige Entwicklung keine
unabhängigen Ausfälle erzeugt. Eine Wiederholung vom Juni 2026 misst denselben Aufbau mit
Coding-Agents über die drei Achsen Werkzeug, Modell und Zielsprache: achtundvierzig zugelassene
Fassungen, eine Million Eingaben, 429 gleichzeitige Ausfälle gegen 115,36 erwartete. Für die
Sprachfrage ist eine andere Zahl entscheidend: von 146 sprachübergreifenden Paaren mit definierter
Korrelation liegen 81 bei genau eins — sie versagen auf denselben Eingaben. Ein Sprachwechsel
entkoppelt die Fehler also nicht.

**Beschluss 1: die Sprache ist Go, und die Wahl ist keine methodische.** Ed25519 liegt in der
Standardbibliothek, die Bauzeiten sind kurz, und explizite Fehlerrückgaben statt Ausnahmen zwingen
dazu, jeden Reject-Code zu benennen. Das sind Bequemlichkeitsgründe, und sie dürfen entscheiden,
weil die Sprache nach dem Befund oben der schwächste der drei Hebel ist. Die kanonische Kodierung
nach `01 §3` wird von Hand geschrieben und nicht aus einer Bibliothek genommen, weil sonst die
Bibliothek eines Dritten geprüft wird und nicht die Spec. Die Signaturprüfung wird ausdrücklich
nicht selbst gebaut.

**Beschluss 2: der Prompt ist minimal, und das kehrt die sonst geltenden Prompt-Regeln um.** Der
Auftrag nennt die Spec-Datei, das Ein- und Ausgabeformat und das erwartete Artefakt. Er nennt
keine Prüfreihenfolge, keine Liste der Fehlerklassen, kein Gerüst und keine Auflösung einer
Mehrdeutigkeit. Begründung: jede Präzisierung im Prompt repariert die Spec außerhalb der Spec und
vernichtet genau den Befund, den der Lauf erzeugen soll. Wer in den Prompt schreibt, was der Text
offenlässt, misst danach seinen eigenen Prompt. Die übrigen Prompt-Regeln — Basis-Commit,
Abschluss, ein Commit — gelten weiter; nur die Enge fällt.

**Beschluss 3: alle Fassungen lesen denselben Spec-Stand.** Der Anker ist der Commit, auf dem
Anhang C zehn der elf Reject-Codes trägt. Fassungen dürfen zeitlich weit auseinanderliegen, aber
eine Fassung, die eine wegen ihrer Vorgängerin reparierte Spec liest, sagt nichts mehr über die
Vorgängerin. Ohne gemeinsamen Anker gibt es keine Häufung, und die Häufung ist das Instrument.

**Warum die Häufung und nicht die Unabhängigkeit.** Die Wiederholung von 2026 findet die Fehler
nicht verstreut, sondern auf wenigen schwierigen oder mehrdeutigen Stellen der Spezifikation
gebündelt; an zwei Bedingungen ließ sich die gemeinsame Fehllesart direkt auf eine Unklarheit im
Text zurückführen. MaR sucht keine Fehlertoleranz durch Mehrheitsvotum, sondern die Stellen, an
denen `01-claim-atom.md` mehrdeutig ist. Für diesen Zweck ist die Korrelation, die das Verfahren
als Fehlertoleranz beschädigt, das Messinstrument. Daraus folgt, dass mehrere Fassungen mehr wert
sind als die richtige Sprache, und dass verschiedene Modelle mehr bringen als verschiedene
Sprachen.

**Beschluss 4: eine durchgefallene Fassung wird ausgewertet, nicht ausgeschlossen.** Die
Wiederholung von 2026 siebt Fassungen aus, die den Aufnahmetest nicht bestehen, weil ihr Ziel
Zuverlässigkeit ist. Unser Ziel ist das Gegenteil: eine Fassung, die an einem Vektor aus Anhang C
scheitert, ist der wertvollste Fall, den der Lauf erzeugen kann. Anhang C ist hier Messpunkt und
nicht Aufnahmesieb.

**Verfeinerung von D256 Beschluss 3.** Dort steht, die Erwartung komme nie aus einem Lauf der
Referenz. Für die Vektoren bleibt das gültig; dort gibt es eine gedruckte Erwartung. Für eine
randomisierte Kampagne gibt es keine, und der Abgleich gegen die Referenz ist der einzig mögliche.
Er ist zulässig unter einer Bedingung: eine Abweichung ist eine Frage an die Spec und kein Urteil
gegen die Zweitimplementierung. Bei jeder Abweichung entscheidet `01-claim-atom.md`, nicht die
Python-Fassung.

**Offen, für den Kampagnenlauf.** Zufällige Bytes liefern fast durchweg dieselbe Fehlerklasse; eine
Kampagne braucht strukturierte Eingaben, also mutierte gültige Claims. Die Bauform dieser Mutation
ist noch nicht entschieden.

**Was nicht folgt.** D237 bleibt: die Zweitimplementierung ist der beste verfügbare Ersatz für die
fehlende Außenprüfung und ersetzt sie nicht. Der Befund von 1986 und der von 2026 machen sie nicht
wertlos, sondern verschieben, wonach in ihrem Ergebnis zu suchen ist.

---

### D259 — Was die Zweitimplementierung sehen darf

**Die Quelle ist eine einzige Datei.** Gemessen an `01-claim-atom.md`: die drei
Domänen-Separatoren sind dort definiert, und alle zwölf Verweise auf
`00-nucleus-genesis-constitution.md` betreffen Verfassung, Governance oder die Policy-Sicht, also
die Zustandsstufe. Der Separator der Nukleus-Scope-ID wird in C.0 im Klartext genannt. Für die
zustandslose Stufe nach D256 ist die Datei selbsttragend, und es geht nichts weiter mit.

**Anhang C wird bei C.1 abgeschnitten.** Mitgegeben wird der Text bis einschließlich des ersten
positiven Vektors; C.2 bis C.10 werden zurückgehalten. Begründung: Anhang C ist bis zum Bau der
Kampagne der einzige Messpunkt, und ein Messpunkt, gegen den entwickelt wurde, misst die
Entwicklung und nicht die Spec. Wer dem Agenten die negativen Vektoren gibt, bekommt eine Fassung,
die sie besteht, und erfährt nichts darüber, ob der Text sie trägt.

**Warum der Schnitt nicht vor C.0 liegt.** Ohne einen vollständig gerechneten positiven Vektor
kann eine falsche Kodierung die gesamte Fassung zu Rauschen machen: alles wird abgelehnt, und
keine einzige Fehlerklasse wird sichtbar. Der erste Vektor fixiert die Kodierung, die
Claim-Kennung und die Signatur und kostet dafür genau einen von elf Messpunkten. Das ist der
billigste verfügbare Schutz gegen einen Totalausfall der Messung.

**Die Arbeit findet außerhalb des Arbeitsverzeichnisses statt.** Die Zweitimplementierung
entsteht in einem eigenen Verzeichnis ohne Sicht auf die Python-Fassung, die Tests, die
Vektordatei und das Register. Sonst ist die Trennung eine Bitte und keine Eigenschaft. Die
beschnittene Spec-Datei wird durch ein Skript aus dem committeten Stand erzeugt, mit Quell- und
Zielhash, damit nachweisbar bleibt, welcher Text vorlag.

**Die Schnittstelle wird vorgegeben, die Semantik nicht.** Ein- und Ausgabeformat müssen
festliegen, sonst ist nichts vergleichbar; das ist keine Präzisierung der Spec im Sinne von D258
Beschluss 2, sondern die Bedingung dafür, überhaupt zu messen. Die Namen der Fehlerklassen kommen
aus Anhang B und werden im Prompt nicht aufgezählt.

**Was das kostet, benannt.** Nach dem Lauf ist der Messpunkt verbraucht: eine zweite Fassung
gegen dieselben zurückgehaltenen Vektoren ist noch möglich, eine Nachbesserung derselben Fassung
gegen sie nicht. Wird die Fassung nach der Messung repariert, ist sie danach kein Messpunkt mehr,
sondern Code wie jeder andere.

---

### D260 — Die Zweitimplementierung ist gelaufen: 18 von 19, siebzehn Fragen

**Der Lauf.** Go 1.27, Commit `365df9b` in einem eigenen Verzeichnis, 2039 Zeilen in acht Dateien,
eigenes deterministisches CBOR ohne Bibliothek, Signatur aus der Standardbibliothek. Vorgelegen
hat allein die bei C.1 beschnittene Spec, deren Hash lautet:

```
b16251fc02d07c8761a0583fe77ddadd6a6f59e6b7167d889231733170cc051a
```

Der Prompt nannte keinen Abschnitt, keine Fehlerklasse und keine Prüfreihenfolge.

**Die Messung.** Neunzehn Vektoren aus Anhang C, achtzehn davon der fremden Fassung unbekannt.
Achtzehn deckungsgleich, eine Abweichung. Alle acht Fehlerklassen aus `01 §C.10` trafen beim
ersten Durchlauf zu, ebenso die drei älteren negativen Vektoren und alle fünf positiven samt
Claim-Kennung.

**Das ist ein Ergebnis über die Spec, nicht über Go.** Eine fremde Implementierung, die nichts als
den Text und einen einzigen Vektor gesehen hat, trifft achtzehn von neunzehn Ausgängen byte- und
codegleich. Für die Kodierung, die Kennungsberechnung, die Signaturprüfung, die
Prädikat-Grammatik und die Bindungsregel trägt der Text.

**Die Abweichung sitzt am einzigen Vektor mit zwei Mängeln.** BV2 ist indefinite-length **und**
trägt einen Text-Schlüssel. Die Referenz meldet die Schlüsselklasse, die fremde Fassung die
Kodierungsklasse. Beide Lesarten sind mit dem Hauptteil vereinbar; die Reihenfolge entscheidet,
und der Hauptteil legt sie nicht fest. Das bestätigt D257 von der anderen Seite: ein Vektor mit
zwei Mängeln behauptet über die Reihenfolge, und ein Vektorsatz mit genau einem Mangel je Stück
ist gegen Reihenfolgefragen blind.

**Befund an BV2, gemessen.** Der Vektor begründet sich mit einer Prüfreihenfolge aus `01 §6`, die
er als 2b vor 2c benennt. Diese Nummerierung kommt in der ganzen Datei genau einmal vor, nämlich
in dieser Begründung; sie stammt aus den Kommentaren von `verifier.py`. Der Hauptteil
`01 §6` Punkt 2 zählt die vier Bedingungen in einem Satz auf und nennt die kanonische Kodierung
dabei zuerst. Zweiter Befund: die Einleitung desselben Abschnitts sagt, der Code müsse derselbe
sein, unabhängig davon, an welchem Schritt der Prüfreihenfolge eine Implementierung ihn findet.
BV2 widerspricht ihr.

**Die Sache ist entschieden, die Begründung nicht.** Inhaltlich trägt BV2: eine Kodierungsklasse
behauptet, es gebe eine gültige kanonische Fassung desselben Inhalts, und bei einem
Text-Schlüssel gibt es die in keiner Kodierung. Der Ausgang bleibt also, wie er ist. Zu
reparieren ist der Text: entweder normiert der Hauptteil die Reihenfolge, oder BV2 verliert seine
Berufung auf eine Nummerierung, die nur im Modul existiert. Das ist ein eigener Beschluss.

**Der schwerste Befund steht nicht in der Messung.** Eintrag 1 der Fragenliste: `01 §3` verlangt,
den dekodierten **Core** neu zu serialisieren und mit den **empfangenen Bytes** byte-genau zu
vergleichen. Der Core ist die Map ohne die Signatur, die empfangenen Bytes enthalten sie. Wörtlich
befolgt lehnt diese Regel jeden signierten Claim ab. Beide Implementierungen haben unabhängig
voneinander dieselbe vernünftige Lesart gewählt und sind darum deckungsgleich; kein Vektor kann
das sehen. Genau das ist die Klasse von Defekt, für die D237 die Zweitimplementierung wollte.

**Siebzehn Einträge, dreizehn offen.** Die Fragenliste nennt siebzehn Stellen, an denen der Text
eine Entscheidung erzwang. Zwei sind oben behandelt, zwei weitere sind messbare Abweichungen ohne
Vektor: die Auslösebedingung der Lifecycle-Fremdheit ohne Store, und die Frage, ob die
Feldkonsistenz von `t` und `t_exp` auf `core/*` mitentfällt, wenn die Ablaufzeit dort ignoriert
wird. Die übrigen dreizehn werden einzeln geprüft und einzeln entschieden; keiner wird als
erledigt geführt, bevor er einen eigenen Eintrag hat.

**Was der Lauf über das Verfahren sagt.** Der Ertrag liegt in der Fragenliste, nicht in der
Abweichungszahl. Achtzehn Treffer haben null Befunde erzeugt, ein Treffer daneben einen, und die
Liste siebzehn. Wer eine Zweitimplementierung nur gegen Vektoren misst, wirft den Hauptteil des
Ertrags weg. Das ändert die Erwartung an eine mögliche dritte Fassung: verlangt wird die Liste,
gemessen wird die Häufung der Fragen, nicht die der Abweichungen.

---

### D261 — `01 §3`: verglichen wird die dekodierte Map, nicht der Core

**Der Defekt.** Der Durchsetzungssatz in `01 §3` verlangt, den dekodierten **Core** neu kanonisch
zu serialisieren und mit den **empfangenen Bytes** byte-genau zu vergleichen. Der Core ist nach
`01 §4` die Map ohne `σ`; die empfangenen Bytes eines signierten Claims enthalten `σ` als Key 9.
Wörtlich befolgt lehnt die Regel jeden signierten Claim ab. Der Satz kommt in der Datei genau
einmal vor; die Reject-Tabelle in Anhang B nennt die Bedingung neutral als Re-Serialisierung
gegen empfangene Bytes und ist nicht betroffen.

**Beschluss.** Verglichen wird die dekodierte Map einschließlich `σ`. `01 §3` wird entsprechend
gefasst und um eine Begründung ergänzt: der Core kommt in den empfangenen Bytes nie für sich vor,
und aus der Kanonizität der Map folgt die des Cores, weil `σ` den höchsten Key trägt und sein
Wegfall die Kodierung der übrigen Einträge unberührt lässt. `01 §6` Punkt 2 trägt dieselbe
Zuschreibung in schwächerer Form und wird mitgezogen: kanonisch kodiert sind die empfangenen
Bytes, nicht der Core. Die Reihenfolge der vier Bedingungen in Punkt 2 bleibt unangetastet; sie
gehört zum offenen Beschluss über BV2 (D260).

**Gemessen, nicht angenommen.** Die Python-Fassung prüft in `cbor_canon.is_canonical` die
empfangenen Bytes gegen ihre eigene Re-Serialisierung, also die volle Map; der Aufruf sitzt in
`verifier.py` in `structural_check` unter der Marke 2c. Die Go-Fassung hat unabhängig davon
dieselbe Lesart gewählt und sie in `00ad-fragen-befund §1` samt zweier verworfener Alternativen
aufgeschrieben. Keine der beiden Fassungen folgt dem Text; beide folgen derselben Reparatur.

**Was ein Vektor hier kann und was nicht.** Er kann die wörtliche Lesart ausschließen: eine
Fassung, die sie befolgt, fällt an jedem positiven Vektor durch. Er kann den Defekt nicht
anzeigen, denn jede Fassung, die die Vektoren besteht, hat den Text bereits stillschweigend
repariert. Sichtbar wurde er allein dadurch, dass eine zweite Fassung ihre Abweichung
aufgeschrieben hat (D260). Für diese Klasse wird kein Vektor gebaut, weil es keinen geben kann.

**Verworfen:** den Core aus der Wire-Form zu schneiden und nur diesen Ausschnitt zu vergleichen.
Der Schnitt ist ohne vorheriges Dekodieren nicht definiert, und die Kanonizität von `σ` bliebe
ungeprüft. Ebenfalls verworfen, die Kanonizitätsprüfung zu streichen: sie ist es, die die
Wire-Form eindeutig macht (`01 §2.4`, Invariante 5). Ebenfalls verworfen, den Satz stehen zu
lassen und die Lesart nur im Register zu vermerken — der Text ist die normative Wahrheit, und
eine dritte Fassung liest ihn und nicht das Register.

---

### D262 — Der Vorrang der Fehlerklassen wird inhaltlich normiert, nicht als Prüfreihenfolge

**Die Lage, gemessen.** BV2 begründet seinen Ausgang mit einer Prüfreihenfolge aus `01 §6`, die er
als 2b vor 2c benennt. Die Zeichenfolge kommt in `01-claim-atom.md` genau einmal vor, nämlich in
dieser Begründung; sie stammt aus den Kommentarmarken von `verifier.py`. Die Einleitung von C.8
sagt das Gegenteil: geprüft wird, welchen Code der Verifizierer liefert, unabhängig davon, an
welchem Schritt seiner Prüfreihenfolge er ihn findet. Seit D261 nennt `01 §6` Punkt 2 die
kanonische Kodierung in seiner Aufzählung sogar zuerst.

**Beschluss.** Normiert wird der Vorrang, nicht die Reihenfolge. `Anhang B.2` bekommt eine Regel:
`NON_CANONICAL_ENCODING` behauptet, es gebe eine kanonische Kodierung desselben Inhalts, die
gültig wäre; trägt der dekodierte Inhalt einen Mangel, den keine Kodierung behebt, ist der Code
`MALFORMED_CBOR`. BV2 beruft sich auf diese Regel statt auf eine Schrittnummer. Der Ausgang des
Vektors bleibt unverändert.

**Warum nicht die Reihenfolge.** Die Ordnungsunabhängigkeit ist eine tragende Eigenschaft und
keine Nachlässigkeit: `01 §6` verlangt, dass jedes Gerät die Zustände offline aus den gehaltenen
Bytes berechnet, und die Einleitung von C.8 macht daraus eine Zusage an fremde Implementierungen
mit anderer CBOR-Bibliothek. Eine normierte Schrittfolge bände jede Fassung an einen Ablauf, ohne
einen einzigen Ausgang zusätzlich festzulegen — dieselben Fälle entscheidet die inhaltliche Regel,
und sie ist an jedem einzelnen Claim prüfbar. Der Preis ist benannt: wer die Kanonizität zuerst
prüft, muss vor dem Reject feststellen, dass der Inhalt sonst zulässig ist. Das ist eine Pflicht
über den Code, nicht über den Ablauf.

**Wirkung auf die beiden Fassungen.** Die Python-Fassung findet den Nicht-uint-Schlüssel in
`structural_check` vor der Kanonizitätsprüfung und liefert `MALFORMED_CBOR`; sie bleibt
unberührt. Die Go-Fassung prüft zuerst auf Kanonizität und liefert an BV2
`NON_CANONICAL_ENCODING`. Ihre Abweichung war vor diesem Beschluss ein Befund über den Text und
ist danach einer über die Fassung. Das ist die einzige der neunzehn Messungen, die kippt.

**Reichweite.** Entschieden ist allein die Überschneidung von Kodierungs- und Inhaltsmangel. Die
vollständige Ordnung der zehn Fehlerklassen, die `00ad-fragen-befund §4` vorschlägt, bleibt offen
und ist keine Norm; sie beschreibt, was eine Fassung getan hat.

**Verworfen:** die Prüfreihenfolge zu normieren — sie widerspricht der Einleitung von C.8 und
bindet ohne Gewinn. Verworfen, BV2 zu streichen: sein Ausgang ist richtig, nur seine Berufung war
es nicht. Verworfen, die Marken `2a` bis `2d` in `verifier.py` umzubenennen: sie sind lokale
Kommentarmarken und kein Verweisziel, sobald kein normativer Text sich auf sie beruft. Gerät die
Nummerierung je wieder in einen Prompt oder eine Spec-Datei, ist der Befund dieser Eintrag.

---

### D263 — `core/*`: falscher `J.tag` ist `MALFORMED_CBOR`, `ziel.I` nur bei bekanntem Ziel

**Der Defekt.** `01 §6` Punkt 4 verlangt für `core/*` drei Bedingungen: das Prädikat ist eines der
beiden gesegneten, `J.tag == claim-ref`, und `ziel.I == C.I`. Die dritte ist am Atom allein nicht
entscheidbar — `ziel` steht nur als `claim_id` im Feld `J`, die Identity des Ziels in einem
anderen Claim. Ein Verifizierer ohne Speicher kann sie weder erfüllen noch verletzen. Für die
zweite nennt `Anhang B.2` keinen Code. Das ist der Defekttyp aus D261 in seiner zweiten Ausprägung:
der Text verlangt wörtlich etwas, das keine zustandslose Fassung leisten kann, und die beiden
Fassungen haben ihn verschieden gelesen.

**Gemessen.** Die Python-Fassung wirft bei `core/*` mit `J.tag != claim-ref` `MALFORMED_CBOR`
(`verifier.py`, Schritt 4) und prüft `ziel.I` nur, wenn ein Store übergeben ist und den Ziel-Claim
kennt; ohne Store fällt `_check_foreign_lifecycle` still durch. Die Go-Fassung meldet beim
falschen Tag `FOREIGN_LIFECYCLE` und begründet das in `00ad-fragen-befund §2` damit, dass der Tag
lokal sichtbar ist und die Selbstbezüglichkeit unmöglich macht.

**Beschluss.** `J.tag != claim-ref` auf `core/*` ist `MALFORMED_CBOR`. `ziel.I == C.I` wird
geprüft, sobald der Ziel-Claim lokal bekannt ist, und entfällt sonst ersatzlos; `FOREIGN_LIFECYCLE`
bleibt an diese Bedingung gebunden. `01 §6` Punkt 4 und die beiden Zeilen in `Anhang B.2` werden
entsprechend gefasst.

**Warum nicht `FOREIGN_LIFECYCLE` für den Tag.** Ein Code ist eine Behauptung (D262).
`FOREIGN_LIFECYCLE` behauptet, ein Lebenszyklus-Claim ziele auf den Claim eines fremden Autors.
Wer ohne Speicher arbeitet, hat das nicht gemessen; gesehen hat er nur, dass das Feld nicht die
Form trägt, die `01 §5.1` für Selbstbezüglichkeit verlangt. Behauptet werden darf, was gemessen
wurde.

**Verworfen:** ein zwölfter Code für „Tag passt nicht zum Prädikat". Elf Codes tragen den
Fehlerkanal, zehn davon mit Vektor; ein weiterer kostet jede fremde Fassung eine Zeile und sagt
nichts, was `MALFORMED_CBOR` nicht sagt — die Feldbelegung ist für dieses Prädikat unzulässig.
Verworfen auch, `ziel.I == C.I` aus Punkt 4 zu streichen: die Bedingung gilt, sobald das Ziel
bekannt ist, und `01 §5.1` hängt an ihr.

**Folge.** Für den falschen Tag fehlt ein Vektor; er wird gebaut. Die Go-Fassung weicht an dieser
Stelle ab, und wie bei D262 ist die Abweichung nach dem Beschluss eine über die Fassung.

---

### D264 — `t_exp` auf `core/*` entfällt auch für die Feld-Konsistenz

**Die Frage.** `01 §5.3` verlangt, ein `t_exp` auf einem `core/*`-Claim zu ignorieren. `01 §6`
Punkt 7 verlangt unbedingt `t < t_exp`, sobald beide Felder da sind. Gilt die Feld-Konsistenz auf
Lifecycle-Claims weiter, oder fällt sie mit dem Feld?

**Gemessen.** Die Python-Fassung prüft Punkt 7 unbedingt und lehnt einen `core/revoke@1` mit
`t ≥ t_exp` als `INCOHERENT_EXPIRY` ab. Die Go-Fassung lässt die Prüfung dort entfallen
(`00ad-fragen-befund §5`). NV11 trifft die Frage nicht, er trägt ein `nuc:…/vouch@1`.

**Beschluss.** Auf `core/*` findet die Prüfung `t < t_exp` nicht statt. Das Feld hat dort keine
Wirkung, auch keine ablehnende.

**Begründung, aus der Spec selbst.** `01 §5.3` nennt den Grund für das Ignorieren beim Namen: ein
ablaufender Widerruf belebt widerrufenes Vertrauen wieder, Über-Vertrauen, die eine gefährliche
Richtung. Ein Reject wegen `t ≥ t_exp` hat exakt dieselbe Wirkung wie der Ablauf — der Widerruf
wird nicht wirksam, der widerrufene Claim bleibt aktiv. Die Feld-Hygiene aus Punkt 7 kauft nichts,
was diesen Preis wert wäre. Dazu kommt die Selbstbezüglichkeit aus `01 §5.2`: abgelehnt würde
nicht die Aussage eines Dritten, sondern die Rücknahme des Autors über seine eigene frühere
Aussage. Wer sie ablehnt, hält den Autor an der stärkeren Behauptung fest.

**Verworfen:** `t_exp` auf `core/*` ganz zu verbieten. TV5 lebt von seiner Zulässigkeit, und
`01 §5.3` sagt SHOULD, nicht MUST NOT. Verworfen auch, die Feld-Konsistenz als bloße Hygiene
stehen zu lassen: sie ist Teil der strukturellen Gültigkeit und entscheidet damit über den Reject,
nicht über einen Vermerk.

**Folge.** Die Referenz ändert sich, nicht die Zweitimplementierung — das ist die erste Stelle, an
der die fremde Fassung die Python-Seite korrigiert. Gebraucht werden: die Änderung in
`verifier.py` mit Rücknahmeprobe und ein positiver Vektor, ein `core/revoke@1` mit `t ≥ t_exp`,
der `ok` liefert.

---

### D265 — Keine Gesamtordnung der Fehlerklassen; der Code ist Grund, kein Zustand

**Die Frage.** `00ad-fragen-befund §4` schlägt eine Prüfreihenfolge über zehn Fehlerklassen vor.
D262 hat davon ein Stück entschieden, den Vorrang zwischen Kodierungs- und Inhaltsmangel. Soll der
Rest normiert werden, oder bleibt die Liste ein Befund?

**Gemessen.** `01 §B.1` führt genau einen Reject-Zustand, `malformed`. Die elf Einträge in
`01 §B.2` stehen unter der Überschrift „Fehlerklassen (Reject-Gründe)". Der Absatz unter der
Zustandstabelle erklärt alle Zustände außer `expired` für verifiziererübergreifend determiniert —
die Aussage gilt dem Zustand, nicht dem Grund. `01 §C.10` sagt von seinen acht Vektoren selbst,
jeder trage genau einen Mangel; der einzige Vektor mit zweien ist BV2 (D262).

**Beschluss.** Keine Gesamtordnung. Tragen mehrere Codes eine wahre Aussage über dieselbe
Bytefolge, ist die Wahl frei. Normativ bleibt allein das Verbot des falschen Satzes aus D262, und
es gilt für alle elf Klassen, nicht nur für die drei dort genannten Inhaltsmängel. Der Satz kommt
nach den Vorrang-Absatz in `01 §B.2`; die Liste in `00ad-fragen-befund §4` bleibt Befund.
`01 §6` bleibt unberührt — seine Aufzählung ist eine Konjunktion, keine Folge (D262).

**Begründung.** Eine Ordnung entschiede keinen einzigen zusätzlichen Ausgang. Abgelehnt wird so
oder so, und der Zustand ist derselbe; sie entschiede nur, welcher von mehreren wahren Sätzen
genannt wird. Der Preis wäre dauerhaft: jede fremde Fassung an einen Ablauf gebunden, den sie
nicht braucht, und jeder künftige Code in die Ordnung einzuhängen. Das ist die Rechnung aus D262,
eine Ebene höher — dort ist der Vorrang normiert worden, weil er Ausgänge entscheidet, und die
Reihenfolge nicht, weil sie keine entscheidet.

**Verworfen:** die Liste des Befunds als Norm. Sie ist nicht einmal durchweg zulässig — ihr
Schritt 2 vor Schritt 3 ist genau die Lesart, die D262 an BV2 verworfen hat. Verworfen auch, den
Code als Zustandskomponente zu führen: dann müssten alle Fassungen je Bytefolge übereinstimmen,
und die Gesamtordnung wäre die Folge, nicht die Wahl.

**Folge.** Anhang C bleibt scharf, aber eng: ein negativer Vektor bindet den Code für den Mangel,
den er trägt. Ein Vektor mit zwei Mängeln ist nur dann eine Norm, wenn der Vorrang ihn entscheidet.

---

### D266 — Feldsatz-Verstöße sind `MALFORMED_CBOR`; die Feldtabelle gilt je Version

**Die Frage.** `00ad-fragen-befund §7` fragt nach dem Code für einen Key außerhalb der Tabelle,
ein fehlendes Pflichtfeld, `I` mit 31 Byte, `J` mit Länge ungleich 2. `01 §2` führt die Tabelle
mit Pflicht und Größe; `01 §B.2` nennt als Auslöser nur „falscher Feldtyp".

**Gemessen.** Die Zeile in `01 §B.2` listet fünf Auslöser; Länge, Pflicht und fremder Key stehen
nicht darunter. `01 §6` Punkt 2 verlangt „korrekte Feldtypen" und nennt den Feldsatz nicht. Die
Go-Fassung liest „falscher Feldtyp" weit und fängt alle vier Fälle.

**Beschluss.** Die weite Lesart wird Text. Fehlendes Pflichtfeld, Key außerhalb der Feldtabelle
und falsche Byte- oder Array-Länge sind `MALFORMED_CBOR`. `01 §6` Punkt 2 und die Zeile in
`01 §B.2` werden entsprechend gefasst.

**Begründung.** Es ist derselbe Defekttyp wie in D261 und D263: die Tabelle in `01 §2` ist
normativ, aber kein Code hängt an ihrer Verletzung. Ein fremder Key ist dabei der schärfste Fall —
er ändert den Core, und `claim_id` wäre damit nicht mehr die eine Adresse des Inhalts, sondern
eine von mehreren (`01 §2.4` Invariante 5). Bei fehlendem Pflichtfeld entfällt jede Prüfung, die
an ihm hängt; ablehnen ist die sichere Richtung.

**Der zweite Teil folgt aus D262.** Bei nicht unterstützter Version werden Feldsatz-Prüfungen
nicht mehr angestellt: `MALFORMED_CBOR` behauptete dort einen Mangel, den erst die v1-Tabelle
setzt, und eine fremde Version darf einen anderen Feldsatz tragen. Der Satz wäre falsch. Er wird
trotzdem ausgeschrieben, weil er sonst aus zwei Einträgen zusammenzusetzen wäre.

**Verworfen:** eine eigene Fehlerklasse für Längen- oder Pflichtverstöße. `01 §B.2` hat keine, und
ein zwölfter Code kostet jede fremde Fassung eine Zeile — dieselbe Rechnung wie in D263. Verworfen
auch, fremde Keys zu ignorieren; das ist die zweite ID-Familie und trifft `01 §2.4` Invariante 5.

**Folge.** Für alle vier Fälle fehlt ein Vektor. D265 macht sie nicht zur Pflicht; jeder von ihnen
trüge genau einen Mangel und wäre damit von der Ordnungsfrage unberührt.

---

### D267 — Zwölfter Reject-Code `INVALID_PREDICATE` für Formverstöße unter `nuc:`

**Die Frage.** `00ad-fragen-befund §6`: Anhang A ist als normativ überschrieben und bindet Scope,
Name und Version eines Prädikats. `01 §B.2` kennt keinen Code für einen Formverstoß.
`UNKNOWN_NAMESPACE` gilt dem Namensraum, `RESERVED_CORE_PREDICATE` dem geschlossenen `core`,
`BAD_SCOPE_BINDING` der Bindung an `N`. Welcher Code trägt `nuc:hasenpfote/VOUCH@1`?

**Gemessen.** `predicates.py` wirft für jeden String mit `nuc:`-Präfix, der die nuc-Regex nicht
matcht, `UnknownNamespace` — Scope, Name und Version ohne Unterschied. Die Go-Fassung liest es
ebenso (`00ad-fragen-befund §6`). Träger im Test sind zwei Fälle, beide mit fremdem Präfix
(`svc:foo/bar@1`); kein bestehender Test und kein Vektor liegt auf dem strittigen Fall. NV6 trägt
`foo/vouch@1` und ist von der Frage nicht berührt.

**Beschluss.** Ein zwölfter Code, `INVALID_PREDICATE`. Er trägt jeden String mit `nuc:`-Präfix,
der die Grammatik aus Anhang A nicht erfüllt — fehlerhafter Scope, fehlerhafter Name, fehlerhafte
Version. `UNKNOWN_NAMESPACE` wird auf seinen Wortlaut zurückgeschnitten: weder `core/`- noch
`nuc:`-Präfix. `RESERVED_CORE_PREDICATE` und `BAD_SCOPE_BINDING` bleiben unberührt. Gefasst
werden `01 §6` Punkt 4, die Zeile in `01 §B.2`, der Absatz in `01 §2.2` und der Schluss von
Anhang A.

**Begründung.** D265 verbietet den falschen Satz. `UNKNOWN_NAMESPACE` behauptet, der Namensraum
sei unbekannt; bei `nuc:hasenpfote/VOUCH@1` ist er bekannt und die Behauptung falsch. Beide
Fassungen machen sie heute, und dass sie übereinstimmen, sagt darüber nichts — es ist der Fall aus
D237, in dem der Text gar keinen Code vorsah und beide dieselbe Lücke gleich gefüllt haben. Der
Preis ist gemessen und klein: keine bestehende Zusicherung wandert, kein Vektor ändert sich, in
`predicates.py` sind es zwei Zeilen.

**Warum die Form überhaupt durchgesetzt wird.** `01 §2.2` nennt den Prädikat-Namen opak — das gilt
seiner **Bedeutung**, nicht seiner **Form**; derselbe Absatz sagt, neue Profile seien neue *Namen*
unter `nuc:`, und Anhang A sagt, welche Zeichenfolgen Namen sind. Die Form nicht durchzusetzen
hieße, eine als normativ überschriebene Grammatik zur Zierde zu erklären und dabei genau den
Defekt zu erzeugen, den D266 eine Runde vorher behoben hat. Dazu kommt der Verwechslungsvektor aus
`01 §2.4`: `vouch@01` neben `vouch@1` ist für die Profilschicht ein anderer String und für einen
Menschen derselbe.

**Verworfen:** die Auslöserzeile von `UNKNOWN_NAMESPACE` auf „Form verletzt Anhang A" zu
verbreitern und bei elf Codes zu bleiben. Das kostet nichts und macht den Satz wahr — aber es
macht ihn wahr, indem es die Wörter verschiebt, und lässt einen Codenamen zurück, der über die
Fehlerursache täuscht. Ein Grund, der die Ursache falsch benennt, hat seinen einzigen Zweck
verloren (D265). Verworfen auch, Name und Version gar nicht zu prüfen und nur den Scope zu binden:
das erweitert die angenommene Menge dauerhaft, und die Umkehrung ist teurer als die Einschränkung.

**Folge.** Gebraucht werden: `errors.py` um eine Klasse, die beiden `raise` in `predicates.py`,
ein negativer Vektor in Anhang C mit einer Rücknahmeprobe. Ohne Vektor fiele die Abdeckung aus
D257 von zehn Codes auf zehn von zwölf zurück; mit ihm sind es elf von zwölf. Historische
Zählungen „elf Reject-Codes" in Prompts und älteren Registereinträgen bleiben stehen: sie waren
wahr, als sie geschrieben wurden.

---

### D268 — Selbstenthaltene Gültigkeit wird benannt; `00ad-fragen-befund §3` ändert keine Norm

**Die Frage.** `00ad-fragen-befund §3` legt fest, dass eine zustandslose Fassung weder die Uhr
noch den Vorgänger befragt. Ist das eine Abweichung von der Spec oder deren korrekte Lesart? Und
wenn es die Lesart ist: wie heißt der Prüfumfang, den eine solche Fassung abdeckt?

**Gemessen.** `01 §6` Punkt 7 sagt selbst „kein Wall-Clock nötig". `01 §B.3` führt den unbekannten
Vorgänger unter den Nicht-Fehlern; `01 §B.1` nennt `expired` den einzigen verifizierer-relativen
Zustand. Von den sieben Punkten in `01 §6` hängt nach D263 genau einer an einem Speicher:
`ziel.I == C.I` in Punkt 4, und der greift nur, sofern der Ziel-Claim lokal bekannt ist. Die
übrigen sechs und der Rest von Punkt 4 sind aus den empfangenen Bytes allein entscheidbar.

**Beschluss.** Die Lesart des Befunds ist die der Spec; an ihr ändert sich nichts. Benannt wird
der Umfang: **selbstenthaltene Gültigkeit** sind die Punkte 1 bis 7 ohne den bedingten Konjunkt
aus Punkt 4. Der Absatz steht in `01 §6` hinter Punkt 7. Er definiert und verlangt nichts.

**Begründung.** „Zustandslose Stufe von Layer 01" ist seit D256 ein Ausdruck des Registers, nicht
der Spec; er hat den Umfang der Go-Fassung bezeichnet und den Prüfstand ihrer Abnahme, ohne dass
irgendwo stünde, welche Punkte dazugehören. Der Ausdruck ist inzwischen dreimal tragend gewesen —
D256, D258, D259 — und eine dritte Fassung müsste ihn wieder erraten. Dass er sich sauber
definieren lässt, ist erst durch D263 wahr geworden: vorher war `ziel.I == C.I` unbedingt und der
Umfang damit nicht abschließbar.

**Der Zusatz, der ihn tragfähig macht.** Wissen kann das Urteil nur verengen. Ein selbstenthalten
gültiger Claim kann strukturell ungültig werden, sobald sein Ziel bekannt ist; umgekehrt kann
kein Zuwachs an Wissen einen Reject aufheben. Damit ist der Umfang eine sichere Untermenge und
kein zweiter, konkurrierender Gültigkeitsbegriff — die Richtung ist dieselbe wie bei `expired`
und bei `pending` (`01 §6`, Unter-Vertrauen).

**Verworfen:** den bedingten Konjunkt aus der strukturellen Gültigkeit herauszunehmen und in einen
eigenen Zustand zu heben. Das änderte die Zustandsmenge in `01 §B.1` von acht auf neun und
entschiede keinen einzigen Ausgang zusätzlich; `FOREIGN_LIFECYCLE` bliebe derselbe Code am
denselben Bedingungen. Verworfen auch, den Begriff als MUSS zu fassen: eine Fassung, die Speicher
und Uhr hat, soll den vollen Umfang prüfen, nicht den kleineren.

**Folge.** Die Abnahme einer Fassung ohne Speicher hat jetzt einen benannten Bezugspunkt. Für eine
dritte Fassung (D258) ist damit sagbar, was sie bauen soll, ohne auf das Register zu verweisen.
Ein Prüfer für den Begriff selbst ist nicht gebaut und wird es vorerst nicht: die Aussage ist eine
über den Text, nicht über eine Menge im Repo.

---

### D269 — Die Hex-Schnittstelle ist keine Norm, erzwingt aber einen falschen Satz

**Die Frage.** `00ad-fragen-befund §8` fragt nach Hex-Alphabet, Innen-Whitespace, Leerzeilen und
der Zusage „je Eingabezeile genau eine Ausgabezeile". Gestellt hat sie der Auftrag an die
Go-Fassung (D256); die Spec kennt sie nicht.

**Beschluss.** Kein Normbezug. Die Hex-Zeilen sind Transport in den Harness, nicht Wire-Form.
`01 §3` spricht von empfangenen Bytes und sagt nichts darüber, wie sie ankommen. Die Lesart des
Befunds bleibt eine Eigenschaft der Fassung und wird nicht Text.

**Ein Befund bleibt trotzdem.** Die 1:1-Zusage zwingt den Harness, auch dort einen Reject-Code
auszugeben, wo gar keine Bytefolge entstanden ist: ungerade Länge, Nicht-Hex-Zeichen,
Innen-Whitespace. `MALFORMED_CBOR` behauptet dann etwas über empfangene Bytes, und es wurden keine
empfangen. Das ist der falsche Satz, den D265 als einzige Norm über der Codewahl stehen lässt.
Der Grenzfall ist die leere Zeile: die leere Bytefolge ist eine Bytefolge und ist kein Claim,
dort trägt der Code.

**Folge.** Nicht für die Spec, sondern für den nächsten Auftrag. Eine dritte Fassung (D258)
bekommt eine Schnittstelle, die Transportfehler und Verdikt getrennt ausgibt — ein eigenes Wort
für „diese Zeile ist keine Bytefolge", das kein Code aus `01 §B.2` ist. Der Auftrag der Go-Fassung
wird nicht nachgezogen; er ist gelaufen, und sein Ergebnis ist gemessen.

**Verworfen:** eine Klasse `BAD_INPUT` in `01 §B.2` aufzunehmen. Sie beträfe keinen Verifizierer,
sondern eine Aufrufkonvention, und jede fremde Fassung müsste sie tragen, ohne dass ein Claim sie
je auslöst — dieselbe Rechnung wie in D263 und D266. Verworfen auch, Leerzeilen zu überspringen:
das bräche die Zusage, die den zeilenweisen Vergleich zweier Fassungen erst möglich macht.

---

### D270 — Die empfangenen Bytes sind genau ein CBOR-Item; Restbytes sind `MALFORMED_CBOR`

**Die Frage.** `00ad-fragen-befund §9` fragt, ob `claim ‖ 0x00` nicht-kanonisch oder nicht
dekodierbar ist, und behandelt das als Wahl zwischen zwei Codes. Die Frage darunter ist eine
andere: was die Eingabe eines Verifizierers überhaupt ist.

**Gemessen.** `01 §3` Regel 1 sagt „Top-Level ist eine CBOR-Map"; das Wort „Item" kommt in
`01-claim-atom.md` genau einmal vor, in Regel 2 über indefinite-length. `01 §6` Punkt 2 verlangt
„dekodierbar" und definiert es nicht. Die Python-Fassung liefert an `TV1 ‖ 0x00` wie an
`TV1 ‖ TV1` `NON_CANONICAL_ENCODING`, gemessen an geeichtem Bestand: 626 grün, acht Vektoren mit
dokumentiertem Ausgang reproduziert. Die Go-Fassung hat `MALFORMED_CBOR` gewählt und die Wahl in
`00ad-fragen-befund §9` aufgeschrieben.

**Beschluss.** `01 §3` bekommt den Satz, dass die empfangenen Bytes die Kodierung genau eines
CBOR-Items sind und nichts darüber hinaus enthalten. Restbytes hinter dem Item sind
`MALFORMED_CBOR`; die Zeile in `01 §B.2` nennt sie.

**Warum die Freiheit aus D265 hier nicht greift.** D265 überlässt die Wahl, wo mehrere Codes eine
wahre Aussage über dieselbe Bytefolge tragen. Ohne den Arity-Satz reicht die Offenheit weiter als
bis zum Code: `TV1 ‖ TV1` ist dann unentschieden, und ein Verifizierer dürfte den zweiten Claim
ebenso gut verarbeiten wie verwerfen. Die Fassung tut heute ein Drittes — sie liest die Folge als
nicht-kanonische Kodierung des ersten und verwirft den zweiten signierten Claim stillschweigend.
Was mit den Bytes geschieht, ist keine Codewahl.

**Warum `MALFORMED_CBOR`.** `NON_CANONICAL_ENCODING` behauptet nach D262, es gebe eine kanonische
Kodierung desselben Inhalts, die gültig wäre. Die Behauptung setzt voraus, dass die empfangenen
Bytes eine Kodierung dieses Inhalts sind. Eine Folge zweier Items ist keine Kodierung einer Map;
die Voraussetzung fällt weg, und mit ihr der Satz.

**Verworfen:** die Frage unter D265 offen zu lassen — die Offenheit wäre nicht auf den Code
beschränkt. Verworfen, den Satz als siebte Regel in die Liste in `01 §3` zu nehmen: die sechs
Regeln beschreiben die Kodierung einer Map, die Arity beschreibt die Eingabe und steht vor ihnen.
Verworfen, Restbytes zu überlesen und den ersten Claim zu nehmen: dann trüge dieselbe `claim_id`
beliebig viele Wire-Formen, und `01 §2.4` Invariante 5 fiele in genau der Richtung, die D272 an
der Fassung misst.

---

### D271 — `00ad-fragen-befund §10` und `§11` ändern keine Norm

**Die Frage.** `00ad-fragen-befund §10` fragt nach Indefinite-Length, Break, Floats, Tags und
Simple Values, `§11` danach, ob `0x01` und `0x18 0x01` derselbe Map-Key sind.

**Beschluss.** Beide sind vom Text entschieden; die Lesart des Befunds ist die der Spec. Kein Satz
in `01` ändert sich, keine neue Klasse kommt hinzu.

**`§10` im einzelnen.** Dekodierbare indefinite-length ist `NON_CANONICAL_ENCODING` (BV3),
unabgeschlossene Länge und Break in Wertposition sind `MALFORMED_CBOR` (BV1, `01 §B.2`). Major 6
und Major 7 in Feldposition sind falscher Feldtyp und damit `MALFORMED_CBOR` (D266) — kein Feld in
`01 §2` trägt Tag, Float, Boolean oder Null. Ein Top-Level, das keine Map ist, trägt kein
Pflichtfeld und fällt unter dieselbe Zeile.

**`§11` im einzelnen.** D262 entscheidet es: eine Map mit zwei Einträgen gleichen Schlüsselwerts
trägt einen Mangel, den keine Kodierung behebt. Maßgeblich ist damit die semantische Gleichheit
der dekodierten Schlüssel, und die Kodierungslänge des Schlüssels ist gleichgültig. `01 §B.2`
nennt doppelte Keys ausdrücklich unter `MALFORMED_CBOR`.

**Verworfen:** die zehn Fehlerklassen aus `00ad-fragen-befund §4` doch noch zu ordnen, weil beide
Fragen an einer Ordnung hingen. Sie hängen nicht daran: entschieden hat in beiden Fällen der
Inhalt der Aussage, nicht ihre Stelle in einer Reihe. D265 bleibt unberührt.

**Was die Prüfung nebenbei ergeben hat.** Die Fassung folgt dem Text an beiden Stellen nicht. Das
ist ein Befund über sie und nicht über die Norm; er steht in D272.

---

### D272 — D266 ist Text ohne Code: fünf gemessene Abweichungen der Fassung

**Der Anlass.** D266 hat Feldsatz-Verstöße auf `MALFORMED_CBOR` gelegt und die Geltung der
Feldtabelle je Version normiert. Der Beschluss ist in `01 §2`, `01 §6` Punkt 2 und `01 §B.2`
gefahren worden. Ein Werkzeuglauf hat ihn nicht gebaut, und die Fassung ist nie gegen ihn gemessen
worden. Aufgefallen ist das bei der Prüfung von `00ad-fragen-befund §10` und `§11` (D271).

**Gemessen.** Am ausgepackten Bestand, geeicht an 626 grünen Tests und acht Vektoren mit
dokumentiertem Ausgang, dann Mutanten von TV1, mit dem Alice-Seed neu signiert, wo die Signatur
betroffen war:

| Bytefolge | Fassung liefert | Norm verlangt |
|---|---|---|
| TV1 mit angehängtem Key 20, Signatur unangetastet | angenommen, `claim_id` unverändert | `MALFORMED_CBOR` (D266) |
| `version` als `true` (`h'f5'`), neu signiert | angenommen, `version` liest `True` | `MALFORMED_CBOR` (`01 §2`) |
| `t` als `true`, `false` oder negativ, neu signiert | angenommen | `MALFORMED_CBOR` (`01 §2`) |
| Key 6 doppelt, Map-Header von `h'a9'` auf `h'aa'` | `NON_CANONICAL_ENCODING` | `MALFORMED_CBOR` (`01 §B.2`) |
| `version` 2 mit fehlendem `t` oder `I` mit 31 Byte | `MALFORMED_CBOR` | `UNSUPPORTED_VERSION` (D266) |

**Der erste Fall ist schärfer, als D266 ihn gedacht hat.** Dort ist der fremde Key als zweite
ID-Familie verworfen worden. Gemessen ist die Umkehrung. Die Kanonizitätsprüfung sieht nichts,
weil die erweiterte Map selbst kanonisch kodiert ist; der Verifizierer baut sein Preimage aus
einer Map, die er zuvor auf die bekannten Keys zurückschneidet. Der fremde Key fällt also weg,
bevor die Signatur geprüft wird. Sie verifiziert, `claim_id` bleibt dieselbe, der Claim wird
angenommen. Zwei Wire-Formen von 309 und 311 Byte tragen damit eine Adresse und dedupen
gegeneinander weg (`01 §B.3`, Gossip-Replay). `01 §2.4` Invariante 5 nennt als Zweck, dass
`claim_id` eine echte Inhaltsadresse ist und Dedup und Equivocation-Erkennung nicht vergiftet
werden; in dieser Richtung fällt sie ohne Zutun des Autors — anhängen kann jeder Dritte.

**Die zweite Ursache ist eine Eigenheit der Sprache.** `bool` ist in Python eine Unterklasse von
`int`, und `True == 1`. Der Typtest auf `int` lässt `h'f5'` und `h'f4'` durch, und der
Versionsvergleich gegen `1` fällt für `True` positiv aus. Damit hat derselbe logische Claim eine
zweite gültige `claim_id` — das Grinding, das Invariante 5 ausschließt. Negative Integer passieren
aus demselben Grund die Tore; `01 §2` schreibt uint.

**Nullprobe vor dem Prompt.** Die vier Typtore auf CBOR-uint verengt, ohne einen einzigen neuen
Test: 626 grün vor und nach der Änderung, und alle sieben Mutanten kippen auf `MALFORMED_CBOR`.
Der Bestand ist für diese Klasse vollständig blind, und er blockiert die Reparatur nicht. Die
Rücknahmeprobe des kommenden Laufs ist damit vorab geeicht (Prüfregeln 49, 51).

**Beschluss.** Ein Werkzeuglauf repariert die fünf Ausgänge und legt die Vektoren dazu; er bekommt
einen eigenen Prompt und einen eigenen Anhangsabschnitt in `01`. Die Norm ändert sich dabei nicht
— jeder der fünf Ausgänge steht bereits im Text. Der Kommentar in `verifier.py`, doppelte Keys
seien vom Dekoder ausgeschlossen, ist falsch und fällt mit.

**Verworfen:** die Reparatur in denselben Schnitt zu legen wie die Registereinträge. Der Textteil
ist über Zielhashes abnehmbar, der Codeteil nicht; gemischt wäre keiner von beiden sauber
abzunehmen. Verworfen auch, eine Prüfreihenfolge vorzuschreiben, damit die Version vor dem
Feldsatz geprüft wird: D262 normiert Ausgänge und keine Reihenfolge, und der Prompt fixiert
deshalb Welten und Codes, nicht Schritte.

**Folge für die Zweitimplementierung.** D266 hält fest, dass die Go-Fassung alle vier Fälle aus
`00ad-fragen-befund §7` fängt, und sie hat das aus dem Text vor D266 getan. Die Python-Fassung
fängt keinen davon. Damit ist die Referenz an fünf Ausgängen die abweichende Fassung; in D262 war
es die Go-Fassung an einem. Das ist der Ertrag, den D237 sich von einer zweiten Fassung versprochen
hat, und er fällt zum ersten Mal auf die Referenz zurück.

---

### D273 — `00ad-fragen-befund §12` bis `§17` ändern keine Norm; der Befund ist abgearbeitet

**Die Fragen.** Sechs Abschnitte: `N` auf `core/*`, Alias gegen 64-Hex, die Profilregeln und `v`,
das Signatur-Preimage, der Genesis-Anker außer Null, die kanonische Map-Sortierung.

**Beschluss.** Alle sechs sind vom Text entschieden; die Lesart des Befunds ist in jedem Fall die
der Spec. Kein Satz in `01` ändert sich. Aus dem Abschnitt zu den Profilregeln folgt eine eigene
Entscheidung an anderer Stelle, D274.

**Geprüft, nicht angenommen.**

- **`N` auf `core/*`.** `01 §2.3` schreibt „z. B. ein reiner Identity-Announce oder ein
  `core/*`-Claim". Das ist ein Beispiel und kein Verbot. `check_scope_binding` löst den Scope nur
  unter `nuc:` auf; `N` auf einem `core/*`-Claim ist weder verboten noch an `p` gebunden.
- **Alias gegen 64-Hex.** Invariante 3 in `01 §2.4` reserviert genau `^[0-9a-f]{64}$` der
  kanonischen Kodierung. Der Code trägt dasselbe Muster, und der Alias-Zweig nimmt `N` als
  einzige Quelle, ohne Byte-Vergleich gegen den Alias-Text. Zeichenfolgen der Länge 63 und 65
  sind damit Alias. Die Frage nach dem Lookahead ist mit D255 entschieden: die ABNF in Anhang A
  ist maßgeblich.
- **Signatur-Preimage.** `01 §4` schreibt die Verkettung, nicht `cbor(...)`; `domains.py` führt
  die Separatoren als rohe ASCII-Bytes. Gemessen: ein `I` aus lauter Einsbits und ein `I` aus
  lauter Nullbytes liefern beide `BAD_SIGNATURE` und keine Exception.
- **Genesis-Anker.** `01 §6` Punkt 6 macht allein den Nullvektor zum Reject. Die
  Genesis-Gleichung ordnet ein, sie verlangt nichts; ohne Log-Zustand gibt es keinen „ersten"
  Claim.
- **Map-Sortierung.** Die Frage kann in einem Claim nicht auftreten. Für uints fallen kodierte
  und numerische Ordnung immer zusammen: die kürzeste Form wächst in der Länge monoton mit dem
  Wert, und innerhalb einer Längenklasse ist die Bytefolge die Zahl. Über 5305 Werte bis 2 hoch
  64 nachgerechnet, identisch. Da `01 §3` Nicht-uint-Keys ausschließt, ist die Unterscheidung
  gegenstandslos.

**Damit ist `00ad-fragen-befund.md` abgearbeitet.** Siebzehn Abschnitte, geschlossen von D261 bis
D273. Elf davon haben keinen Normtext bewegt. Was der Befund insgesamt getragen hat: einen
zwölften Reject-Code (D267), den Arity-Satz in `01 §3` (D270), die Geltung der Feldtabelle je
Version (D266) und den Fund, der ihn überragt — D272, fünf Ausgänge, an denen die Referenzfassung
vom geltenden Text abwich. Das ist die Ausbeute, die D237 sich von einer zweiten Fassung
versprochen hat.

**Verworfen:** die drei Abschnitte ohne Codebefund offen zu halten, bis eine dritte Fassung
dieselbe Frage noch einmal stellt. Text und Code stimmen an allen dreien überein; ein offener
Punkt, auf den niemand handeln kann, kostet bei jedem Sitzungsstart und trägt nichts.

---

### D274 — Kanonizität von `v` gilt auch in der Auszählung; `04 §2.3` sagt es jetzt

**Die Lücke.** `01 §7.1` setzt die Kanonizitätsanforderung aus `01 §3` dort durch, wo `v` gelesen
wird, und nennt zwei Stellen: Trust-Flow `§3.1` für Key `0` und Profile-II `§1.3` für die
Profil-Keys. Der Absatz handelt von `vouch@1`, deshalb nennt er nur zwei. `vote@1` und `ratify@1`
lesen `v` ebenfalls, und `04-governance.md` sagt zur Kanonizität an keiner Stelle etwas.

**Gemessen.** `profiles/payload.py` und `trust/groups.py` prüfen `is_canonical(v)` im selben `try`
wie den Dekodierschritt (D83). `governance/tally.py` und `governance/epoch.py` prüfen nichts.
`_choice` liefert für `h'a1001801'` — Key 0, Wert 1 in nicht-kürzester Form — dieselbe Eins wie
für `h'a10001'`. Eine so kodierte Stimme zählt also, während derselbe Defekt in einem Vouch einen
`NON_CANONICAL_V`-Vermerk erzeugt und den defekten Teil wegfallen lässt.

**Was schon dicht ist.** `_is_yes_choice` und `_is_known_choice` prüfen mit `type(value) is int`
und lassen CBOR `true` nicht als Ja durch — dieselbe Konstruktion, die der Verifizierer mit D272
bekommen hat. Der Boolean-Pfad ist in der Auszählung nie offen gewesen.

**Beschluss.** Der Grundsatz aus `01 §7.1` gilt bereits; `04` hat den Satz nur nie geschrieben.
`04 §2.3` bekommt ihn: die auszählende Schicht dekodiert `v` und prüft die Re-Serialisierung im
selben Zug, in der Form aus Profile-II `§1.3`. Ein Verstoß erzeugt den Vermerk `NON_CANONICAL_V`
und lässt den defekten Teil wegfallen — nie einen Reject und nie den Abwesend-Default. Bei
`vote@1` zählt die Stimme dann weder als Ja noch als Nein, wie bei einem unbekannten `choice`;
bei `ratify@1` fällt die Zeugenmenge weg, die nach `04 §2.3` ohnehin austauschbarer Beleg und
nicht Teil der Epochenidentität ist.

**Warum nicht ausnehmen.** Die Gegenposition wäre, `v` in der Governance ausdrücklich ungeprüft
zu lassen. Sie scheitert daran, dass dann die Zahl der zählenden Stimmen eines Autors an einem
Kodierungsdetail hängt, das keine Schicht prüft, und `01 §2.4` Invariante 5 nennt genau das
Grinding mehrerer Kodierungen desselben Inhalts als das, was die Kanonizität verhindern soll.
Zwei Schichten, die dasselbe Feld verschieden streng lesen, sind außerdem die Defektform, die
D272 gerade gekostet hat.

**Nicht gemessen und nicht nötig.** Ob die Ausschlusslogik in `governance/tally.py` zwei so
entstandene Stimmen desselben Autors als Doppelstimme behandelt, ist offen geblieben. Die Frage
entfällt mit dem Beschluss, weil die zweite Stimme nicht mehr zählt.

**Folge.** Ein Werkzeuglauf zieht `governance/tally.py` und `governance/epoch.py` auf die Form
von `read_v` und legt `NON_CANONICAL_V` in die Governance-Vermerke. Eigener Prompt, eigene Runde.
Der Textsatz in `04 §2.3` fährt mit diesem Eintrag; der Code folgt und ist bis dahin ein
benannter Rückstand, kein stiller.

### D275 — Wo `NON_CANONICAL_V` entsteht und was er verdrängt; D274 hat sich verrechnet

**Gemessen, vier Welten, Bestand gegen eine Fassung mit der Prüfung.** Die Fassung ist lokal
gebaut und nicht ausgeliefert; sie diente der Eichung der Rücknahmeproben (Prüfregeln 49, 51).

| Welt | Bestand | mit der Prüfung |
|---|---|---|
| eine nicht-kanonische Ja-Stimme allein | zählt als Ja, kein Vermerk | fällt weg, `NON_CANONICAL_V` |
| kanonisches Ja + nicht-kanonisches Ja, selber Autor, selber Vorschlag | `AMBIGUOUS_VOTE`, beide fallen weg | `NON_CANONICAL_V`, das kanonische Ja zählt |
| nicht-kanonisches Zweit-Ja auf einen anderen Vorschlag | `CONFLICTING_APPROVAL`, Autor ausgeschlossen | `NON_CANONICAL_V`, das erste Ja zählt |
| `ratify@1` mit nicht-kanonischem `v` | **Folgeepoche entsteht**, kein Vermerk | keine Epoche |

Der vierte Fall ist der schärfste: ein Epochenwechsel materialisiert heute auf einem
nicht-kanonischen Zeugenbeleg, stillschweigend und ohne Vermerk.

**Berichtigung an D274.** Dort steht, die Frage nach der Ausschlusslogik entfalle mit dem
Beschluss, weil die zweite Stimme nicht mehr zähle. Das ist falsch. Sie entfällt nicht, sie
kippt: heute fallen beide Stimmen weg, mit der Prüfung zählt die kanonische. Der Satz war eine
Ableitung ohne Messung und hat den Ort der Prüfung als gleichgültig behandelt, obwohl er das
Ergebnis bestimmt. Prüfregel 25 gilt auch für den eigenen Registereintrag von gestern.

**Beschluss 1 — der Ort.** Die Kanonizitätsprüfung steht dort, wo `v` gelesen wird, also vor der
Zusammenfassung nach Autor und vor der Ausschlussprüfung nach `04 §4.4`. `04 §3.1` sagt bereits,
dass die Formprüfungen vor der Zustandsprüfung stehen; die Kanonizität ist eine Formprüfung und
reiht sich dort ein. Die Wirkung ist die eines unbekannten `choice`, und `04 §2.3` nennt genau
diese Parallele. Gemessen: ein unbekanntes `choice` desselben Autors lässt dessen kanonische
Stimme heute schon zählen — die Parallele ist also nicht neu, sondern schon gebaut.

**Beschluss 2 — die Form, nicht der Code.** Governance bekommt einen eigenen Leser in der Form
von `profiles/payload.py::read_v`, keinen Import von `ProfileFinding`. `04 §3.5` hält den
Governance-Enum getrennt (D94); ein Layer-03-Import für eine Zweiwertabbildung kauft nichts und
koppelt zwei Schichten, die verschiedene Vermerksräume haben. `04 §2.3` verlangt die Form aus
Profile-II `§1.3`, nicht deren Funktion.

**Beschluss 3 — ein `v`, das nicht dekodiert, bleibt wo es ist.** D274 nennt genau einen Vermerk.
Ein nicht dekodierbares `v` behält sein heutiges Ergebnis: `UNKNOWN_VOTE_CHOICE` bei `vote@1`,
`UNSUPPORTED_RATIFICATION` bei `ratify@1`. Ein `UNPARSABLE_V` in den Governance-Vermerken wäre
Scope über D274 hinaus und wird hier **nicht** eingeführt. Verworfen, nicht vergessen: die
Unterscheidung zwischen „nicht lesbar" und „nicht kanonisch" ist in `03` vorhanden und in `04`
nicht, und ob das ein Defekt ist, steht offen.

**Beschluss 4 — bei `ratify@1` verdrängt der neue Vermerk den alten.** Ein nicht-kanonisches `v`
erzeugt `NON_CANONICAL_V` und **nicht** `UNSUPPORTED_RATIFICATION`. Das Kriterium der Tabelle in
`04 §4.1` ist nach D207 die Auskunft an den Beobachter und nicht die Ursache; „nicht kanonisch"
enthält „trägt nicht" bereits und nennt zusätzlich den Grund. Subjekt bleibt die `claim_id` des
`ratify@1`, weil die Zeugenliste ein Feld ohne eigene Adresse ist.

**Beschluss 5 — der Vermerk hängt am Lesen, nicht am ausgezählten Vorschlag.** Die
Ausschlussschleife nach `04 §4.4` liest `v` fremder Ja-Stimmen und muss dieselbe Prüfung fahren,
sonst schließt ein nicht-kanonisches Ja weiter aus (dritte Welt oben). Sie erzeugt dabei
`NON_CANONICAL_V` mit der `claim_id` der fremden Stimme als Subjekt. Die Alternative — die
Wirkung entfällt lautlos — ist verworfen: sie nähme eine bisher sichtbare Folge aus den
Vermerken heraus, ohne etwas an ihre Stelle zu setzen, und die Schleife trägt mit
`UNKNOWN_PROPOSAL` und `CONFLICTING_APPROVAL` ohnehin fremde `claim_id` als Subjekt.

**Nullprobe.** Die Codeänderung ohne neue Tests lässt alle 632 Tests grün. Der Bestand ist an
dieser Stelle blind; kein bestehender Test bewegt sich, und alle vier Welten kippen. Die vier
Rücknahmeproben des Laufs sind damit vorab geeicht.

**Text.** `04 §3.1`, `04 §4.1` und `04 §4.4` bekommen je einen Absatz, `04-golden-anchors §7` die
Vektoren `GV-48` bis `GV-51`. Der Code folgt im selben Lauf; anders als bei D266 und D274 bleibt
kein Textsatz ohne Träger.

### D276 — Die Form aus `03 §1.3` ist normativ; `UNPARSABLE_V` kommt in die Governance

**Befund aus der Abnahme des D275-Laufs.** Der Lauf hat `decode` und `is_canonical` in denselben
`try` gestellt, wie verlangt, aber den `except`-Zweig auf `pass` gesetzt und danach
weitergelesen. Damit fällt eine Stimme, deren Re-Serialisierung wirft, durch die
Kanonizitätsprüfung hindurch und wird anschließend von `_choice` erneut dekodiert — erfolgreich.

**Gemessen, drei Fassungen, ein Claim mit `v = h'a2000101ff'`.** Die Bytes kodieren eine Map mit
zwei Paaren: Key `0` auf Wert `1`, Key `1` auf das nackte Break-Byte. `cbor2.loads` liefert dafür
ein internes Sentinel, `cbor2.dumps` wirft darauf. Der Claim ist vollständig gültig; `read_claim`
liefert ihn und keinen Reject-Code, weil der Umschlag kanonisch ist und der Inhalt eines `bstr`
vom Verifizierer nicht gelesen wird.

| Fassung | Ergebnis |
|---|---|
| Bestand vor dem Lauf | zählt als Ja, kein Vermerk |
| Lauf `cbf1a1e` | zählt als Ja, kein Vermerk — **unverändert** |
| Form aus `03 §1.3` | zählt nicht, Vermerk |

Derselbe Griff in der Ausschlussschleife nach `04 §4.4`: eine so kodierte fremde Ja-Stimme
schließt ihren Autor weiterhin aus, weil `_choice` sie als Ja liest.

**Beschluss 1 — die Form ist normativ, nicht nur der `try`.** `04 §2.3` verlangt die Form aus
Profile-II `§1.3`, und deren tragender Teil ist, dass der `except`-Zweig **abbricht** statt
weiterzulesen. Ein `try`, dessen `except` auf `pass` steht, erfüllt den Buchstaben und nicht den
Satz. Governance bekommt **einen** Leser mit den vier Lagen aus `04 §2.3`; `tally.py` und
`epoch.py` rufen ihn, statt die Prüfung je Stelle noch einmal hinzuschreiben. Der Lauf hat sie
zweimal wörtlich dupliziert und dabei dreifach dekodiert.

**Beschluss 2 — `UNPARSABLE_V` kommt in `GovernanceFinding`.** D275 Beschluss 3 hat ihn
zurückgestellt und die Frage ausdrücklich offen gelassen. Sie ist jetzt gemessen und mit Ja zu
beantworten: ohne ihn verlöre die Ausschlussschleife eine bisher sichtbare Wirkung ersatzlos, und
genau dieses Argument hat D275 Beschluss 5 für `NON_CANONICAL_V` schon einmal gezogen. Der
Vermerk gilt für die zweite Lage: `v` vorhanden, Dekodierung oder Re-Serialisierung wirft, oder
das Ergebnis ist keine Map. Er tritt im Kandidatenfilter an die Stelle von
`UNKNOWN_VOTE_CHOICE`; kein Bestandsvektor ist betroffen, weil `GV-19` mit `v[0] = 2` in der
vierten Lage liegt.

**Beschluss 3 — das abwesende `v` bleibt, wo es ist.** Ohne `v` gibt es kein `v[0]`, und `04 §3.1`
Bedingung 5 verlangt genau dieses. Der Vermerk bleibt `UNKNOWN_VOTE_CHOICE`. `UNPARSABLE_V` sagt
„da ist etwas und es ist nicht lesbar", nicht „da ist nichts".

**Verworfen: nicht re-serialisierbar als Unterfall von nicht-kanonisch.** Der Vermerk wäre dann
`NON_CANONICAL_V`, mit dem Argument, `01 §3` definiere Kanonizität als Gleichheit mit der
Re-Serialisierung, und was keine habe, sei nicht gleich. Verworfen, weil `03 §1.3` dieselbe Lage
als `UNPARSABLE_V` führt und zwei Schichten, die dasselbe Feld verschieden benennen, die
Defektform sind, gegen die D274 selbst argumentiert hat.

**Folge.** Reparatur auf demselben Branch vor dem Merge, mit den Vektoren `GV-52` und `GV-53`.
Die Rücknahmeprobe ist der `except`-Zweig: steht dort wieder `pass` mit anschließendem
Weiterlesen, wird `GV-52` rot.

### D277 — Die Lagen 2 und 3 überschneiden sich; die Kanonizität wird zuerst geprüft

**Befund aus der Abnahme.** D276 beschreibt die Lage 2 als „Dekodierung oder Re-Serialisierung
wirft, oder das Ergebnis ist keine Map" und die Lage 3 als „lesbar und nicht kanonisch". Beides
trifft auf dasselbe `v` zu, wenn es weder kanonisch noch eine Map ist. Der Text entscheidet
nicht, welcher Vermerk dann gilt; die Aufzählung ist keine Prüfreihenfolge.

**Gemessen am gelieferten Stand, sieben Randlagen in einem Lauf.** `h'1801'` trägt
`NON_CANONICAL_V`, `h'01'` trägt `UNPARSABLE_V`. Die gebaute Fassung prüft also die Kanonizität
vor der Form. Beide Ausgänge lassen die Stimme wegfallen; unterschieden hat sich nur der Name.

**Beschluss.** Die gebaute Reihenfolge wird zur Norm, und `04 §2.3` sagt es. Der Grund liegt
nicht in der Bequemlichkeit, sondern in `03 §1.3`: dort steht dieselbe Reihenfolge, und D276 hat
sich für die Form dieser Stelle entschieden. Eine zweite Schicht mit umgekehrter Reihenfolge wäre
genau die Doppelung, gegen die D276 selbst argumentiert hat.

**Verworfen: Lage 2 zuerst.** Das Argument wäre, „keine Map" sei die gröbere Aussage und solle
deshalb zuerst greifen. Verworfen, weil es die Kanonizitätsprüfung an einer Stelle wirkungslos
machte, an der sie etwas aussagt: `h'1801'` ist ein Kanonizitätsverstoß, und ihn als bloße
Formverfehlung zu melden verlöre die Auskunft, die den Autor angeht.

**Kein Vektor.** Der Fall ist eine Kante zwischen zwei Lagen, die beide bereits einen Vektor
haben (`GV-52`, `GV-48`), und beide Ausgänge sind unschädlich. Er steht als benannter Punkt im
Text und in diesem Eintrag, nicht in `04-golden-anchors.md §7`.

### D278 — `superseded` überlebt drei Mutanten; `malformed` hat keinen Erzeuger

**Wie gesucht wurde.** Das Suchmuster aus `00ag` — welcher Beschluss taucht in keinem Test auf —
ist über D-Nummern zu grob: 47 Registereinträge nennen einen Vermerks- oder Verdiktcode und
kommen in keiner Testdatei vor. Die Umkehrung trägt: von den 73 Vermerks- und Verdiktcodes im
Produktivcode kommen vier in keinem Test vor. Zwei davon sind benannt (`EPOCH_FORK` nach D138 und
D176, `FOREIGN_LIFECYCLE` nach D263 und D268); zwei waren es nicht: `State.MALFORMED` und
`State.SUPERSEDED`.

**Erste Messung: Erreichbarkeit.** Die Erzeugerstellen von `State.SUPERSEDED` wurden mit einem
Seiteneffekt versehen und der Bestand gefahren. Sie werden 34-mal erreicht, 30-mal aus
`index.py`, viermal aus `verifier.py`. Der Zustand ist also nicht tot, nur ungenannt.
`State.MALFORMED` hat im ganzen Produktivcode **keine** Erzeugerstelle.

**Zweite Messung: eine Mutantenmatrix über die Zustandszuweisungen.** Beide Erzeugerdateien
zugleich mutiert, je Mutant der volle Bestand gefahren. Für jeden der sieben erzeugten Zustände
wurde mindestens eine Mutation gefahren, für `SUPERSEDED` alle sechs.

| von `SUPERSEDED` nach | rote Tests |
|---|---|
| `ACTIVE` | 4 |
| `EXPIRED` | 1 |
| `LINKED` | 1 |
| `REVOKED` | **0** |
| `PENDING` | **0** |
| `EQUIVOCATION_FLAGGED` | **0** |

Sechs der sieben Zustände kippen bei jeder gefahrenen Mutation; `ACTIVE` bei über 200 Tests,
`EXPIRED` und `EQUIVOCATION_FLAGGED` bei sechs bis sieben, `LINKED` bei genau einem.
`SUPERSEDED` ist der einzige, der Mutanten überlebt. Gebunden ist an ihm nur, dass er nicht
`ACTIVE`, `EXPIRED` oder `LINKED` ist — also die Aussage „gültig, inaktiv". Seine Trennung von
`REVOKED`, `PENDING` und `EQUIVOCATION_FLAGGED` ist ungeprüft, obwohl `01 §B.1` für die drei
verschiedene Bedingungen und für `pending` und `equivocation-flagged` sogar ein anderes
Verhalten vorschreibt.

**Beschluss 1 — `superseded` bekommt einen Träger, der den Namen behauptet.** Ein Test, der nur
„inaktiv" oder `trust_usable is False` prüft, ist genau der Test, den die drei überlebenden
Mutanten schon passieren. Der Träger muss `State.SUPERSEDED` behaupten, und er muss beide
Erzeugerpfade treffen, `verifier.py` und `index.py` — die Matrix hat beide zugleich mutiert und
kann deshalb nicht sagen, ob einer allein gebunden wäre.

**Beschluss 2 — `State.MALFORMED` wird gelöscht.** `01 §B.1` führt `malformed` mit dem Verhalten
„Reject, nicht speichern". Die Klassifikation beschreibt einen gehaltenen Claim; ein nicht
gehaltener hat keinen Zustand, sondern einen Reject-Code. Ein Aufzählungswert ohne Erzeuger ist
ein Versprechen, das nie eingelöst wird, und wer `State` liest, sucht ihn. Die Tabelle in
`01 §B.1` bleibt achtzeilig, weil sie richtig ist; ein Absatz darunter benennt die Differenz.

**Verworfen: `State.MALFORMED` behalten und einen Erzeuger bauen.** Das hieße, den Reject-Pfad
von `read_claim` in eine `Classification` umzuleiten, und damit fiele die Grenze zwischen „nicht
gespeichert" und „gespeichert und inaktiv" — die Grenze, an der `01 §B.1` und D272 hängen.

**Nicht in diesem Beschluss.** `LINKED` hängt an genau einem Test. Das ist dünn, aber gebunden;
ob es reicht, ist offen und wird hier nicht entschieden.

---

### D279 — Der Wert eines Reject-Codes ist seine Drahtform und wird als solcher gebunden

**Anlass.** Eine Mutantenkampagne auf die zwölf Reject-Codes, nach dem Verfahren aus D278. Erste
Probe: je Code den Wert des Aufzählungsmembers auf einen Sentinel gesetzt, danach der volle
Bestand. Alle zwölf überleben.

**Der Grund ist gemessen, nicht vermutet.** `tests/test_verifier.py` vergleicht den Ausgang eines
Vektors gegen einen Lookup in `ErrorCode` über den **Membernamen**. Kein Test im Bestand vergleicht
einen Codewert als Zeichenfolge. Elf der zwölf Codes stehen in `tests/vectors/vectors_01.json` als
`expect_reject`; gebunden ist damit ihr Name, nicht ihr Wert.

**Beschluss.** Der Wert eines `ErrorCode`-Members ist die Drahtform des Codes, und Membername und
Wert sind identisch. Ein Träger behauptet das über alle Member zugleich.

**Begründung.** `01 §B.2` führt die Codes als Zeichenfolgen, und Anhang C ist das einzige Artefakt,
das eine fremde Fassung von ihnen sieht (D250, D257). Driftete ein Wert von seinem Namen ab, bliebe
der Bestand grün und die fremde Fassung vergliche gegen etwas anderes. Ein Aufzählungswert, den
niemand behauptet, ist derselbe Fall wie `SUPERSEDED` in D278: erzeugt, wirksam, austauschbar.

**Verworfen: den Vergleich in `tests/test_verifier.py` vom Namen auf den Wert umzustellen.** Das
bindet nur die Codes, die in Vektoren vorkommen — heute elf von zwölf, und `FOREIGN_LIFECYCLE` kann
nach D263 keinen zustandslosen Vektor bekommen. Ein Träger über die Aufzählung bindet alle zwölf
und kostet drei Zeilen.

---

### D280 — Die Feldtabelle aus `01 §2` bekommt Zeile für Zeile einen negativen Vektor

**Anlass.** Zweite Probe derselben Kampagne: an jeder der 37 Erzeugerstellen im Verifizierer den
erzeugten Code durch einen fremden ersetzt, je Mutant der volle Bestand. Achtzehn werden gefangen,
neunzehn überleben. Mit Überdeckung getrennt: drei Stellen werden erreicht und behaupten ihren Code
ungebunden, sechzehn werden vom Bestand nie erreicht.

**Der Befund.** Die Feldtabelle in `01 §2` hat zehn Felder; der Verifizierer prüft sie mit elf
Toren, weil `J` außen und innen geprüft wird. Zusammen mit der Prüfung auf den Pflichtfeldsatz sind
es zwölf. Der Bestand löst genau eines davon aus, das Tor auf `t`. D266 hat vier Fälle benannt:
fremder Key, fehlendes Pflichtfeld, `I` mit 31 Byte, `J` mit Länge ungleich zwei. Ein Vektor liegt
auf dem ersten (NV14 in `01 §C.13`), die anderen drei haben keinen. D272 hat fünf Ausgänge gemessen
und den Lauf beauftragt, die Vektoren dazuzulegen; für den Ausgang mit `version` als CBOR `true`
ist keiner entstanden. Beide Male ist die Abnahme gegen das gelaufen, was geliefert wurde, und
nicht gegen das, was geschuldet war.

**Beschluss.** Elf negative Vektoren, angehängt als neuer Anhangsabschnitt hinter `01 §C.13`. Jeder
verletzt genau eine Zeile der Feldtabelle aus `01 §2` oder den Pflichtfeldsatz, jeder ist im
Übrigen kanonisch kodiert und über seinen eigenen Core signiert, und jeder erwartet
`MALFORMED_CBOR`.

**Vollständig statt nur die vier benannten Fälle.** Die vier aus D266 sind nicht die vier
gefährlichsten, sondern die vier, die eine zweite Fassung zufällig gefragt hat. Gemessen ist, dass
elf Tore blind sind; eine Auswahl daraus hinterließe sieben, die niemand vermisst, bis sie in einer
späteren Kampagne wieder auffallen. Die Tabelle ist die Einheit, in der `01 §2` normiert, und sie
ist klein genug, um sie in einem Lauf vollständig zu belegen.

**Zur Forderung aus D257, dass ein Vektor genau einen Mangel trägt.** Zwei der elf tragen einen
Mangel, den auch die Signaturprüfung sähe: ein `I` mit 31 Byte ist kein Schlüssel, ein `sigma` mit
63 Byte keine Signatur. Sie behaupten trotzdem nichts über die Prüfreihenfolge, weil kein anderer
Code wahr wäre. `BAD_SIGNATURE` behauptet eine falsche Signatur; gemessen ist eine Feldlänge
außerhalb der Tabelle (D262, D265).

**Zwei Tore sind doppelt geschützt, und das ist vorab gemessen.** Wird das Typtor auf `p` allein
neutralisiert, fängt `parse_predicate` denselben Fall (D213) und der Vektor bleibt grün. Wird die
Prüfung auf den Pflichtfeldsatz allein neutralisiert, fängt das Typtor auf `p` das fehlende Feld,
weil es gegen `None` prüft. Die beiden Rücknahmeproben nehmen deshalb zwei Tore zugleich zurück;
die neun übrigen treffen ihr Tor allein. Ohne diese Eichung wären zwei von elf Proben stumm grün
geblieben (Prüfregeln 49, 51).

**Verworfen: Sondierwelten statt Vektoren.** Dieselbe Rechnung wie in D250 und D257. Anhang C ist
das einzige Artefakt, das eine fremde Fassung sieht, und die Feldtabelle ist genau die Art Pflicht,
die eine fremde Fassung weit auslegt — D266 hält fest, dass die Go-Fassung alle vier Fälle fing,
bevor der Text es verlangte, und D272, dass die Referenz keinen davon fing.

**Nicht in diesem Beschluss.** Acht überlebende Erzeugerstellen außerhalb der Feldtabelle: das
zweite Versionstor hinter dem Aufbau des Claims, das Tor für `FOREIGN_LIFECYCLE` in der
Klassifikation und sein Duplikat im Index, das Formtor unter `nuc:` für einen Scope, der weder
kanonisch noch Alias ist, und das Tor für `core/*` in `resolve_scope`. Dazu die drei erreichten,
aber ungebundenen Stellen. Sie gehen auf die offene Liste. Das zweite Versionstor ist nach dem
Kontrollfluss vermutlich unerreichbar; das ist eine Ableitung und braucht eine eigene Messung.

---

### D281 — Die Vermerkskampagne ist gefahren: 47 von 48 gebunden, ein bekannter Einzelfall

**Anlass.** D278 hat die Mutantenmatrix für die Klassifikationszustände eingeführt und ihre
Ausdehnung auf die Reject-Codes und die Vermerkskonstanten als nächsten Schritt benannt. Die
Reject-Codes sind mit D279 und D280 erledigt. Dieser Eintrag hält das Ergebnis für die Vermerke
fest.

**Gemessen.** Fünf Aufzählungen tragen die Vermerke: `GovernanceFinding`, `ProfileFinding`,
`TrustFinding`, `NucleusFinding` und `PolicyWarning`, zusammen 48 Member an 82 Erzeugerstellen im
Produktivcode. Zuerst die Überdeckung, dann die Mutation (Prüfregel 53): elf der 82 Stellen
erreicht der Bestand nie, und je Member alle Vorkommen zugleich auf ein anderes Member derselben
Aufzählung gesetzt, fallen 47 von 48 Mutanten. Der einzige Überlebende ist `EPOCH_FORK`, und er
hat nach D138 und D176 bewusst keinen Produktivträger.

**Beschluss.** Die Vermerkskonstanten gelten als gebunden; kein Lauf folgt. Der Schritt aus D278
ist damit für alle drei Mengen abgeschlossen: Zustände, Reject-Codes, Vermerke.

**Die Grenze dieser Messung, benannt.** Die Mutation setzt alle Vorkommen eines Members zugleich.
Sie belegt, dass der Name irgendwo behauptet wird, nicht dass jede seiner Erzeugerstellen gebunden
ist — genau die Lücke, die Prüfregel 57 beschreibt. Zehn der elf nie erreichten Stellen sind
Doppelerzeuger eines Vermerks, der anderswo erzeugt und geprüft wird: `INVALID_V_TYPE` und
`UNPARSABLE_V` je zweimal, dazu `MALFORMED_PARTICIPANTS`, `MALFORMED_THRESHOLD`, `SCOPE_MISMATCH`,
`TALLY_UNEVALUABLE`, `UNKNOWN_ACCUSATION` und `UNPARSABLE_VOUCH_PAYLOAD`. Sie gehen auf die offene
Liste, nicht in einen Lauf.

**Warum kein Lauf.** Ein Nullbefund ist ein Ergebnis. Die drei Mengen unterscheiden sich messbar:
bei den Zuständen war einer von sieben austauschbar, bei den Reject-Codes waren zwölf von zwölf
über ihren Wert ungebunden und elf von zwölf Toren der Feldtabelle unerreicht, bei den Vermerken
ist einer von 48 offen und der ist benannt. Die Vermutung, die Vermerksschicht sei so dünn geprüft
wie der Fehlerkanal, ist widerlegt.

**Verworfen: die Matrix auf Stellenebene zu fahren, 82 Läufe statt 48.** Sie fände genau die
Doppelerzeuger, die die Überdeckung schon benannt hat, und für die erreichten Stellen wäre der
Ertrag die Aufteilung eines bereits gebundenen Namens auf seine Träger. Der Preis ist eine
Verdopplung der Rechenzeit für eine Verfeinerung ohne Adressat. Wird eine der zehn Doppelstellen
später berührt, ist sie einzeln zu messen.

---

### D282 — Prüfregeln 52 bis 59

**Anlass.** Die Kandidatenliste stand bei sechs Einträgen und ist in `00ai` auf acht gewachsen.
Eine Kandidatenliste, die nicht geschrieben wird, wird nicht kürzer; ungeschriebene Regeln sind in
Prompts nicht zitierbar und in der nächsten Sitzung verloren.

**Beschluss.** Acht Regeln, 52 bis 59, im bestehenden Format angehängt. Ihre Herkunft wird in der
Schlussliste der Datei ergänzt.

- **52** — der Prüfer misst am Code, nicht am Register (aus D278).
- **53** — die Überdeckung geht der Mutation voraus (aus D280).
- **54** — wer eine Form vorschreibt, benennt ihren tragenden Teil (aus D276).
- **55** — ein Anzahl-Assert in einem Splice wird abgelesen, nicht gerechnet (aus `00ah`).
- **56** — ein Bericht ohne den Diff ist keine Lieferung (aus `00ah`).
- **57** — wo zwei Pfade gekoppelt geprüft werden, braucht jeder zusätzlich einen Träger (aus
  D278).
- **58** — im Merge-Block steht `git push` vor `git branch -d` (aus `00ag`).
- **59** — eine aus einem Diff rekonstruierte Fassung wird über Quellhashes verankert (aus `00af`).

**Was ausdrücklich nicht dazukommt.** Die Eichung einer Rücknahmeprobe an doppelt geschützten
Toren, aufgefallen in `00ai` an `NV24` und `NV30`, ist keine neue Regel. Sie ist Prüfregel 49 —
geschlossene Neutralisierung — zusammen mit Prüfregel 51 — Eichung an einem vorhandenen Element.
Beide haben in `00ai` genau das geleistet, wofür sie geschrieben wurden; eine dritte Regel daneben
verdünnte sie.

**Die Gliederung bleibt offen.** D249 hält fest, dass die Datei ab Regel 37 eine Gliederung
braucht. Acht weitere Regeln machen das dringender und nicht anders; die Gliederung ist ein
eigener Schnitt, weil sie jede Nummer berührt und die Nummern stabil bleiben müssen.

**Verworfen: die Regeln einzeln zu setzen, wenn sie gebraucht werden.** Das ist der Zustand, aus
dem die Kandidatenliste entstanden ist. Eine Regel wird gebraucht, bevor jemand weiß, dass er sie
braucht; das ist ihr Zweck.

---

### D283 — Die fünf nie erreichten Erzeugerstellen: zwei sind unerreichbar, drei bekommen Träger

**Anlass.** D280 hat acht überlebende Erzeugerstellen außerhalb der Feldtabelle auf die offene
Liste gesetzt, fünf davon namentlich, drei als „erreicht, aber ungebunden" ohne Namen. Dieser
Eintrag schließt die Liste.

**Gemessen, im ausgepackten Baum, Überdeckung vor Mutation (Prüfregel 53).** 37 Erzeugerstellen
von Reject-Codes im Produktivcode. Fünf erreicht der Bestand nie: das zweite Versionstor
(`verifier.py`, hinter dem Aufbau des Claims), das Formtor unter `nuc:` für einen Scope, der weder
kanonisch noch Alias ist (`predicates.py`), die beiden Tore für `FOREIGN_LIFECYCLE` in `classify`
und im Index, und das Tor für `core/*` in `resolve_scope`. Die 32 erreichten je auf einen fremden
Code mutiert, fällt 31 von 32; der einzige Überlebende ist das Tor „Top-Level ist kein Map".

**Die Zahl aus D280 ist damit berichtigt.** Dort standen drei erreichte, aber ungebundene Stellen;
gemessen ist eine. Die elf Vektoren aus D280 haben zwei davon mitgebunden, ohne dass die Abnahme
es behauptet hat.

**Zwei Stellen sind unerreichbar und werden gestrichen.**

- Das zweite Versionstor. `claim_from_map` übernimmt `m[0]` unverändert; vor ihm hat entweder das
  erste Versionstor bei einem uint ungleich 1 geworfen oder die Feldtypprüfung bei allem, was kein
  uint ist. Die Fallunterscheidung ist vollständig, es bleibt kein Wert übrig. Nachgefahren mit
  zwölf Werten über alle CBOR-Typklassen: fünf enden in `UNSUPPORTED_VERSION`, sieben in
  `MALFORMED_CBOR`, keiner erreicht das zweite Tor.
- Das Formtor unter `nuc:`. Wenn die Grammatik-Regex gematcht hat, ist der Teil vor dem ersten
  Schrägstrich entweder 64 Hexziffern — dann greift der kanonische Zweig — oder er erfüllt
  `[a-z0-9_-]+` und ist nicht 64 Hexziffern, denn genau das steht als Lookahead in der Grammatik.
  Der Alias-Test danach entscheidet nichts; er wiederholt eine Bedingung, die die Grammatik schon
  durchgesetzt hat. Nachgefahren mit 250 000 konstruierten Prädikaten, die auf die Grammatik
  passen: keines fällt durch beide Scope-Tests.

Mit dem Formtor fällt die Alias-Regex selbst. Der kanonische Test bleibt, weil er *unterscheidet*
— Hex-Scope gegen Alias-Scope —, nicht weil er prüft. Die Alias-Form ist damit nicht aus dem Code
verschwunden: sie steht in der Grammatik-Regex, die Anhang A abbildet, und dort gehört sie hin.

**Warum streichen und nicht Träger bauen.** Ein Tor, das kein Wert erreichen kann, erzeugt einen
Reject-Code, der über keinen Claim je wahr wird — dieselbe Klasse von Aussage, die D262 verbietet,
nur unbeobachtbar. Es kostet in jeder künftigen Kampagne einen Mutanten und eine Erklärung, und es
behauptet gegenüber einem Leser eine Prüfung, die der Kontrollfluss längst erledigt hat. Der
Nachweis der Unerreichbarkeit ist hier nicht Abwesenheit von Evidenz: beide Male ist die
Fallunterscheidung vollständig und nachgefahren.

**Drei Stellen bekommen Träger.** Die beiden `FOREIGN_LIFECYCLE`-Tore je eine Sondierwelt, das
Tor in `resolve_scope` einen Träger nach D284. Für `FOREIGN_LIFECYCLE` ist ein Vektor nach D263
ausgeschlossen und nach D268 liegt der Fall als einziger außerhalb der selbstenthaltenen
Gültigkeit; die Welt ist zweistufig: den fremden Lifecycle-Claim lesen, solange sein Ziel unbekannt
ist, dann das Ziel nachlegen, dann klassifizieren. Beide Tore sind gemessen erreichbar — eine Welt,
zwei Einstiege, `classify` und `classify_all`. Beide Rücknahmeproben sind vorab gefahren und
schließen einzeln (Prüfregel 49).

**Nicht in diesem Beschluss.** Die zehn toten Doppelerzeuger von Vermerken aus D281. Sie liegen in
der Vermerksschicht, nicht im Fehlerkanal, und die dortige Frage ist eine andere: nicht
„unerreichbar oder ungebunden", sondern „zweite Stelle desselben Namens".

---

### D284 — `resolve_scope` auf `core/*` ist ein Aufruferfehler, kein Reject

**Anlass.** Eine der fünf nie erreichten Stellen aus D283. `resolve_scope` wirft für ein
`core/*`-Prädikat `BAD_SCOPE_BINDING`. Vom Draht ist die Stelle nicht erreichbar, weil
`check_scope_binding` `resolve_scope` nur für `nuc:` aufruft.

**Der Befund.** `BAD_SCOPE_BINDING` behauptet die Verletzung der Bindungsregel aus `01 §2.2`
Regel 3. Diese Regel gilt ihrem Wortlaut nach „für jedes `nuc:…`-Profil". `01 §2.3` sagt
ausdrücklich, dass ein `core/*`-Claim kontextfrei ist und kein `N` trägt. Ein solcher Claim
verletzt die Bindungsregel nicht — er fällt nicht unter sie. Der Code wäre eine falsche Aussage
über den Claim (D262), und dass sie den Draht heute nicht erreicht, macht sie nicht wahr.

**Beschluss.** Die Stelle wirft `ValueError`. Das ist kein Reject-Code, sondern die Meldung, dass
der Aufrufer nach dem Scope eines Claims gefragt hat, der keinen hat. Der Träger ist ein Test auf
genau diesen Aufruf.

**Der Bestand kennt diese Trennung schon.** `classify` wirft `ValueError`, wenn eine Policy fremden
Scopes hereingereicht wird (`01 §5.4`). Ein Reject-Code ist eine Aussage über einen Claim; ein
`ValueError` ist eine Aussage über einen Aufruf. Die zwölf Codes aus Anhang B.2 sind Gründe, aus
denen Bytes zurückgewiesen werden (D265), und kein Vokabular für Programmierfehler.

**Verworfen: die Stelle streichen.** Sie ist erreichbar — `resolve_scope` ist eine öffentliche
Funktion, die `01 §2.2` Regel 4 namentlich als Partitionierungsschritt der Evaluatoren nennt. Ohne
das Tor liefe ein `core/*`-Claim in den Alias-Zweig und stürbe dort an `N is None`, wieder mit
`BAD_SCOPE_BINDING` — dieselbe falsche Aussage, nur eine Zeile später und ohne Absicht. Streichen
wäre hier keine Beseitigung von totem Code, sondern das Verstecken einer Vorbedingung.

**Verworfen: `BAD_SCOPE_BINDING` behalten und nur einen Test dazulegen.** Der Test hielte die
falsche Aussage fest, statt sie zu beseitigen. Ein Träger für ein Tor ist nur so viel wert wie das
Tor.

---

### D285 — NV31: die Drahtform ist kein Map

**Anlass.** Die einzige erreichte, aber ungebundene Erzeugerstelle aus D283: das Tor auf
„Top-Level ist kein Map". `01 §3` Regel 1 verlangt eine CBOR-Map mit uint-Keys; kein Vektor und
kein Test hat je behauptet, welcher Code aus ihrer Verletzung folgt.

**Beschluss.** Ein zwölfter negativer Vektor, `NV31`, als neuer Anhangsabschnitt `01 §C.15` hinter
`§C.14` (D250). Er trägt die zehn Werte von TV1 in aufsteigender Key-Reihenfolge als CBOR-Array,
299 Byte, kanonisch kodiert, mit der unveränderten Signatur von TV1. Erwarteter Code:
`MALFORMED_CBOR`.

**Warum das Array der zehn Werte und nicht die leere Liste.** Beide verletzen dieselbe Regel und
beide liefern denselben Code; die leere Liste isoliert das Tor sogar schärfer, weil sie am
Key-Typtor vorbeikommt. Sie behauptet aber nichts, was eine fremde Fassung falsch machen könnte.
Das Array der zehn Werte ist der Angriff: eine Fassung, die die Felder über ihre Position liest,
baut daraus TV1 zurück, prüft die Signatur gegen den aus der Map gebauten Core erfolgreich und
akzeptiert einen Claim mit TV1s `claim_id`. Dieselbe Bauart wie NV22 aus D280 — eine Drahtform,
die auf dem Weg zum Preimage zurechtgeschnitten wird. Anhang C ist das einzige Artefakt, das eine
fremde Fassung sieht (D250, D257, D280); der Vektor ist dort mehr wert als seine 299 Byte kosten.

**Der Preis, benannt.** Der Vektor ist doppelt geschützt: entfernt man allein das Map-Tor, fängt
ihn das Key-Typtor, weil die Iteration über eine Liste deren Werte liefert und der zweite Wert
kein int ist. Die Rücknahmeprobe nimmt deshalb beide Tore zugleich zurück. Vorab gemessen: mit
einem Tor bleibt sie stumm grün, mit beiden wird sie rot (Prüfregeln 49, 51). Damit bindet NV31
das Paar, nicht das einzelne Tor — für ein Artefakt, das den Code festlegt und nicht den Weg
dorthin (Anhang C, Vorbemerkung zu den Byte-Vektoren), ist das die richtige Auflösung.

**Warum `MALFORMED_CBOR` und nicht `NON_CANONICAL_ENCODING`.** Die 299 Byte sind kanonisches CBOR;
ihre Re-Serialisierung ist byte-gleich. `NON_CANONICAL_ENCODING` behauptet, dass dieselbe Aussage
anders hätte kodiert werden müssen — über diese Bytes ist das falsch (D262). `01 §3` erklärt
Kanonizität an der Claim-Map; was keine Map ist, hat keine Kodierung, die sich beurteilen ließe.

---

### D286 — Die Zustandsmatrix ist vollständig: 42 von 42 Paaren gefangen

**Anlass.** D278 hat die Mutantenmatrix über die Klassifikationszustände eingeführt und 28 der 42
geordneten Paare gefahren; die restlichen vierzehn standen als „billig, mechanisch" auf der offenen
Liste. Dieser Eintrag hält das Ergebnis des vollständigen Laufs fest.

**Gemessen.** Sieben Zustände, vierzehn Erzeugerstellen — sieben in `verifier.py`, sieben in
`index.py`. Je Paar beide Dateien zugleich mutiert und der volle Bestand gefahren, 42 Läufe im
ausgepackten Baum, geeicht auf 658 Tests. Kein Paar überlebt. Die kleinste Fangbreite je
Quellzustand:

| von | kleinste Zahl roter Tests |
|---|---|
| `ACTIVE` | 205 |
| `EQUIVOCATION_FLAGGED` | 7 |
| `EXPIRED` | 6 |
| `REVOKED` | 5 |
| `PENDING` | 3 |
| `SUPERSEDED` | 2 |
| `LINKED` | 1 |

**Die drei Überlebenden aus D278 sind gefallen.** Dort blieben `SUPERSEDED` nach `REVOKED`,
`PENDING` und `EQUIVOCATION_FLAGGED` bei null roten Tests. Jedes dieser drei Paare fängt jetzt
zwei Tests. Der mit D278 Beschluss 1 gebaute Träger leistet genau das, wofür er geschrieben wurde
— und das ist hier zum ersten Mal gemessen und nicht nur behauptet.

**`LINKED` ist gebunden, aber an einem einzigen Test — in jede der sechs Richtungen.** Die
Gleichheit der Zahl über alle sechs Mutationen zeigt, dass es derselbe Test ist. Das ist der
Befund aus D278, jetzt beziffert. Er bleibt auf der offenen Liste und bekommt keinen Lauf: ein
zweiter Träger ohne benanntes Risiko ist Zeremonie, und der eine Test bindet den Namen. Wer
`01 §B.1` an dieser Stelle ändert, wird es merken.

**Beschluss.** Die Zustandsmatrix gilt als geschlossen; kein Lauf folgt. Der Schritt aus D278 ist
damit für alle drei Mengen zu Ende gemessen: Zustände hier, Reject-Codes mit D279 und D280,
Vermerke mit D281. In allen drei Mengen ist der Befund derselbe Form: die Namen sind gebunden, die
Lücken liegen bei einzelnen Erzeugerstellen, nicht bei den Namen.

**Verworfen: die Matrix auf Stellenebene, vierzehn Quellen statt sieben.** Dieselbe Rechnung wie in
D281. Die Trennung von `verifier.py` und `index.py` fände, welcher der beiden Pfade einen bereits
gebundenen Zustand trägt; der Preis ist die doppelte Rechenzeit für eine Aufteilung ohne Adressat.
Für `SUPERSEDED` hat D278 diese Frage ausdrücklich offengelassen und der Träger beantwortet sie,
weil er beide Pfade trifft.

**Der Nullbefund ist das Ergebnis.** Zwei der drei Mengen aus D278 haben bei der vollständigen
Messung Arbeit erzeugt — zwölf ungebundene Reject-Codewerte, elf blinde Feldtabellentore. Diese
nicht. Das ist kein Grund, die Messung nachträglich für überflüssig zu halten: dieselbe Vermutung
stand vor D279 über den Reject-Codes und war dort falsch.

---

### D287 — Die zehn Doppelerzeuger sind erreichbar und bekommen je einen Träger

**Anlass.** D281 hat zehn nie erreichte Erzeugerstellen von Vermerken auf die offene Liste gesetzt
und ausdrücklich nicht entschieden, was mit ihnen geschieht. D283 hat für den Fehlerkanal die Frage
gestellt, die hier zu beantworten ist: unerreichbar und zu streichen, oder erreichbar und
ungeprüft.

**Gemessen.** Die zehn Stellen sind zeilengenau geortet und liegen genau dort, wo D281 sie
benannt hat. **Keine davon ist toter Code.** Neun sind aus gewöhnlichen Welten erreichbar; die
zehnte nur aus einem von Hand gebauten `TallyResult`.

| Stelle | Vermerk | Auslösende Welt |
|---|---|---|
| `governance/tally.py` `read_v` | `UNPARSABLE_V` | `v` dekodiert kanonisch und ist keine Map |
| `profiles/payload.py` `read_v` | `UNPARSABLE_V` | dieselbe Form |
| `trust/groups.py` `_decode_weight` | `UNPARSABLE_VOUCH_PAYLOAD` | `v[0]` ist keine nichtnegative Ganzzahl |
| `governance/tally.py` `constitution_governable` | `MALFORMED_PARTICIPANTS` | `participants` ist keine Folge |
| `governance/tally.py` `decide` | `MALFORMED_THRESHOLD` | `thresholds` trägt die anzuwendende Klasse nicht |
| `governance/epoch.py` `verify_ratification` | `TALLY_UNEVALUABLE` | Auszählung ohne `participants` |
| `profiles/credit.py` Obligation | `INVALID_V_TYPE` | `v[1]` ist keine Bytefolge |
| `profiles/credit.py` Quittung | `INVALID_V_TYPE` | `v[0]` ist kein uint |
| `profiles/membership.py` | `SCOPE_MISMATCH` | `grant-membership` mit fremdem `N` |
| `profiles/verdict.py` | `UNKNOWN_ACCUSATION` | Verdikt auf einen Claim, den der Store nicht kennt |

**Beschluss.** Zehn Träger, keine Streichung. Findet der Lauf eine der zehn Stellen doch
unerreichbar, wird das gemeldet und nicht weggeräumt — die Ableitung steht hier, die Messung liegt
im Lauf.

**Drei Leser desselben Feldes, dieselbe blinde Stelle.** `governance/tally.read_v`,
`profiles/payload.read_v` und `trust/groups._decode_weight` lesen alle `v` nach der Form aus
`03 §1.3`, die D276 für jede Schicht normativ gemacht hat. In allen dreien ist der Zweig „dekodiert,
kanonisch, aber nicht die erwartete Form" ungeprüft geblieben, während die beiden Nachbarzweige —
Dekodierfehler und Kanonizität — je einen Test tragen. Die Lücke ist keine drei Zufälle, sondern
eine Form, die dreimal abgeschrieben und dreimal gleich unvollständig geprüft wurde.

**Das Tor in `verify_ratification` trägt und wird darum nicht gestrichen.** `decide` baut ein
`TallyResult` an genau zwei Stellen: mit `participants = None` und `state = UNEVALUABLE`, oder mit
beidem gesetzt. Durch `decide` ist der Zweig also unerreichbar. Er ist trotzdem kein toter Code:
`verify_ratification` nimmt die Auszählung als Parameter, und ohne das Tor liefe `ratify.I not in
participants` gegen `None`. Anders als in D283 ist der erzeugte Vermerk hier **wahr** — eine
Auszählung ohne Teilnehmermenge ist nicht auswertbar. Der Träger baut das `TallyResult` direkt.

**Zwei Träger waren grün, ohne ihre Zeile zu erreichen.** Vorab gemessen und berichtigt. Der eine
prüfte `MALFORMED_THRESHOLD` und traf das Nachbartor für den Schwellenindex; der andere prüfte
`UNPARSABLE_VOUCH_PAYLOAD` und traf das Tor für die fehlende Null. `decide` erzeugt
`MALFORMED_THRESHOLD` an drei Stellen, `_decode_weight` erzeugt `UNPARSABLE_VOUCH_PAYLOAD` an drei
Stellen — ein Test, der den Vermerk behauptet, sagt nicht, welches Tor ihn erzeugt hat. Genau die
Lücke aus Prüfregel 57, diesmal beim Bau des Trägers selbst. Die Überdeckung des Trägers gegen
seine Zielzeile hat beide in einem Lauf gefunden; zehn Rücknahmeproben hätten dasselbe in zehn
Läufen gefunden. Die Überdeckung ist der billige Vorlauf von Prüfregel 49, keine neue Regel.

**Ein elfter Fall, doppelt geschützt.** Für `MALFORMED_PARTICIPANTS` war die erste Welt eine
Zeichenkette. Nimmt man das Typtor zurück, läuft die Schleife über die Zeichen, findet keine
32-Byte-Folge und erzeugt denselben Vermerk eine Prüfung später — die Probe bliebe stumm grün. Die
gewählte Welt ist eine Map mit einem 32-Byte-Schlüssel: sie passiert die Schleife vollständig und
lässt nur das Typtor übrig. Alle zehn Proben schließen damit einzeln (Prüfregeln 49, 51).

**Verworfen: die zehn Stellen zu streichen.** Das war die Antwort in D283 und sie passt hier nicht.
Dort waren die Zweige durch eine vollständige Fallunterscheidung ausgeschlossen; hier fehlt nur die
Welt, die sie auslöst. Neun der zehn sind aus einem gewöhnlichen Claim erreichbar, und drei davon
liegen im Lesepfad für `v`, also an der Stelle, an der ein fremder Autor am ehesten etwas
Unerwartetes schickt.

**Verworfen: je Vermerk ein Träger statt je Stelle.** Das ist der Zustand, den D281 gemessen hat:
47 von 48 Namen gebunden, und trotzdem zehn Stellen ohne Prüfung. Der Name ist nicht die Stelle.

---

### D288 — `pruefregeln.md` bekommt elf Abschnitte; die Nummern bleiben, wo sie sind

**Anlass.** D249 hält seit `00y` fest, dass die Datei ab Regel 37 eine Gliederung braucht; D282 hat
den Rückstand mit acht weiteren Regeln vergrößert und den Schnitt ausdrücklich als eigenen Vorgang
benannt. Gemessen: von 59 Regeln standen 32 unter einer einzigen Überschrift, „Beim Bauen und Lesen
von Tests", darunter der Merge-Block, der Zeilenumbruch von Verweisen und die Alterung der
Projektkopie.

**Beschluss.** Elf Abschnitte entlang des Arbeitsbogens, dem die Datei ihre Ordnung ohnehin
entnimmt: Entwerfen, Typen und Felder, normativer Text, Code und Spec nebeneinander, Reihenfolgen
und Stufen, Prompt, Tests, Rücknahmeproben und Mutanten, Messen, Blöcke und Splices, Abnahme und
Merge. Die Nummern bleiben unverändert; sie stehen im Text nicht mehr in Reihenfolge, und der Kopf
sagt das.

**Warum die Nummern nicht mitwandern.** Sie sind der einzige stabile Griff auf eine Regel. Register
und Prompts zitieren sie zu Dutzenden, und ein Prompt aus `00m` bleibt lesbar, solange die 34 die
34 ist. Eine Umnummerierung machte jeden früheren Verweis still falsch — genau der Fehler, gegen
den Prüfregel 27 gerichtet ist, nur flächig.

**Vier Regeln wechseln den Abschnitt.** 22, 24 und 25 standen bei „Code und Spec nebeneinander"
beziehungsweise beim normativen Text und greifen beim Schreiben des Prompts. 23 stand beim
normativen Text und ist eine Rücknahmeprobe. Alle vier sind an ihren Zeitpunkt gerückt; kein
Regeltext ist angefasst.

**Wie der Schnitt geprüft ist.** Das Skript zerlegt die Datei an den Regelköpfen, setzt die Blöcke
nach der Zuordnung neu und behauptet danach dreierlei: 59 Blöcke, jede Nummer genau einmal, und die
Menge der Blocktexte vor und nach dem Schnitt ist zeichengleich. Damit ist eine Umstellung von einer
Änderung unterscheidbar, ohne die 443 Zeilen zu lesen — dieselbe Bauart wie der Zielhash bei einem
reinen Textschnitt.

**Verworfen: die Regeln nach Herkunft zu gliedern.** Die Datei nennt ihre Herkunft bereits in der
Schlussliste, und die Herkunft sagt nichts darüber, wann eine Regel greift. Wer prüft, sucht den
Zeitpunkt.

---

### D289 — Bauform der Mutation: erst das vollständige Gitter, dann die Kombinationen

**Anlass.** D258 hält am Ende fest, dass zufällige Bytes fast durchweg dieselbe Fehlerklasse
liefern und eine Kampagne mutierte gültige Claims braucht — und lässt die Bauform dieser Mutation
ausdrücklich offen. Prüfregel 15 verlangt hier die Literaturprüfung: der Fork wird außerhalb von
MaR seit zwölf Jahren an genau unserem Gegenstand bearbeitet, nämlich signierten strukturierten
Nachrichten, deren Prüfung eine informell geschriebene Spec umsetzt.

**Der Literaturbefund, in drei Schritten.**

- *Frankencert* (Brubaker u. a., 2014) ist die Urform: Zertifikate werden in ihre Felder zerlegt
  und zufällig neu zusammengesetzt, das Orakel ist die Uneinigkeit zweier Implementierungen. Teuer
  und ungeführt — zehn Millionen Eingaben aus 100 000 Saatzertifikaten ergaben zehn verschiedene
  Abweichungen.
- *Mucert* (Chen und Su, 2015) behält die Bauform und führt sie über MCMC-Sampling. Tausend
  Mucerts liefern dreimal so viele verschiedene Abweichungen wie acht Millionen Frankencerts.
  Führung schlägt Menge um vier Größenordnungen.
- *NEZHA* (Petsios u. a., 2017) tauscht die Führungsgröße aus: nicht die Überdeckung einer
  Implementierung, sondern die Verschiedenheit der Ausgabetupel zwischen allen Implementierungen.
  52-fache Rate gegenüber Frankencert, 27-fache gegenüber Mucert; die reine Blackbox-Führung über
  Rückgabewerte war dabei so gut wie die Pfadführung mit Instrumentierung.

**Die Zahl, die für MaR entscheidet.** NEZHA hat die Empfindlichkeit gegen die Feinheit des
Fehleralphabets ausgemessen. Drei Bibliotheken, künstlich auf höchstens 32 Codes beschränkt, finden
merklich weniger; bei sechzehn Codes über alle drei findet das Verfahren **überhaupt nichts** mehr.
`01 §B.2` kennt zwölf. MaR liegt unterhalb der Schwelle, an der die evolutionäre Führung über
Ausgabetupel nachweislich zu tragen aufhört. Damit ist das Verfahren, das die Literatur als bestes
ausweist, für unseren Gegenstand nicht das erste Mittel.

**Der zweite Befund gegen den bloßen Nachbau.** Frankencert und Mucert fanden drei beziehungsweise
fünfzehn Abweichungen, die NEZHA verfehlte — weil sie auf der Ebene der Felder mutieren und die
Struktur nicht verletzen, während NEZHA formunkundig auf Bytes arbeitet. Feldweise Mutation ohne
Führung findet anderes als byteweise Mutation mit Führung, nicht weniger.

**Beschluss 1 — Stufe 1 ist ein vollständiges Gitter und braucht keine Führung.** Die Maschinerie
der Literatur ist für offene Formate gebaut; `01 §2` hat zehn Felder. Über zehn Felder mal eine
feste Operatorenmenge führt kein Suchverfahren, sondern eine Aufzählung. Saat sind die gültigen
Vektoren aus Anhang C, nicht Zufallsbytes. Mutiert wird die **dekodierte Map**, nicht die
Bytefolge; je Feld: Typ tauschen, Länge ändern, Key entfernen, Key außerhalb der Tabelle
hinzufügen, Wert aus einem anderen Vektor übernehmen. Danach kanonisch neu kodieren.

**Beschluss 2 — jeder Mutant der Stufe 1 wird über seinen mutierten Core neu signiert.** Ohne das
stirbt jeder an `BAD_SIGNATURE`, und die Kampagne misst die Signaturprüfung statt der Spec. Es ist
dasselbe Argument, mit dem D257 verlangt, dass ein Vektor genau den Mangel trägt, den er behauptet.

**Beschluss 3 — eine dritte Familie bleibt unsigniert.** Mutanten, deren Signatur nicht nachgezogen
wird, prüfen, wo `BAD_SIGNATURE` gegenüber den übrigen Codes steht. Nach D265 ist diese Ordnung
nicht normiert; das ist der wahrscheinlichste Ort einer stillen Übereinkunft zwischen zwei
Fassungen, die der Text nicht deckt.

**Beschluss 4 — Stufe 2 ist zufällig und betrifft nur Kombinationen.** Zwei und drei gleichzeitige
Mängel erreicht das Gitter nicht, und dort können zwei Fassungen sich über den **Vorrang** uneinig
sein — wieder D265. Erst hier trägt die Ausgabe-Diversität als Führung, weil das Tupel bei
mehreren Mängeln überhaupt Streuung bekommt.

**Beschluss 5 — die Beobachtungsgröße ist breiter als die zwölf Codes.** Das Tupel trägt zusätzlich
den Ausgang „angenommen" mitsamt der `claim_id`. Zwei Fassungen, die dieselben Bytes annehmen und
ihnen verschiedene `claim_id` geben, sind der schwerste Befund, den die Kampagne erzeugen kann, und
ein reiner Code-Vergleich sähe ihn nicht. Das ist zugleich die Antwort auf das enge Alphabet: wer
die Ausgabe nicht verbreitern kann, muss die Eingabe aufzählen.

**Verworfen: die evolutionäre Führung als Hauptverfahren.** Sie ist das Mittel gegen einen Raum,
den man nicht ausschöpfen kann. Unserer besteht aus zehn Feldern und einer Handvoll Operatoren.

**Verworfen: Mutation auf der Bytefolge.** Sie erzeugt fast nur `MALFORMED_CBOR` — das steht schon
in D258 — und sie kann nicht neu signieren, weil sie die Feldgrenzen nicht kennt.

**Was von D257 hier ausdrücklich nicht gilt.** Ein Mangel je Artefakt ist eine Regel für Anhang C,
wo eine gedruckte Erwartung neben dem Vektor steht. Die Kampagne hat keine gedruckte Erwartung; ihr
Orakel ist die Uneinigkeit. Mehrfache Mängel sind dort nicht nur zulässig, sie sind der Zweck der
zweiten Stufe.

---

### D290 — Der Anker der Kampagne ist der laufende Stand, und der Preis wird benannt

**Anlass.** D258 Beschluss 3 verlangt, dass alle Fassungen denselben Spec-Stand lesen, und nennt
als Anker den Commit, auf dem Anhang C zehn der elf Reject-Codes trägt. Seither sind D266 bis D272,
D279, D280 und D285 in `01-claim-atom.md` eingegangen; der zwölfte Code ist mit D267 dazugekommen,
Anhang C trägt mit `§C.14` und `§C.15` zwölf weitere negative Vektoren. Der Text, den die Go-Fassung
gelesen hat, ist nicht mehr der Text, der heute in `main` steht.

**Der Unterschied, der bisher übersehen wurde.** D258 Beschluss 3 regelt den Fall mehrerer
**neuer** Fassungen: ohne gemeinsamen Anker gibt es keine Häufung, und die Häufung ist das
Instrument. Die hier beschlossene Kampagne vergleicht aber zwei **vorhandene** Artefakte, und eines
davon ist gegen den alten Text gebaut. Liefe sie so, wäre jede Abweichung, die D266 bis D285 bereits
entschieden haben, ein Treffer — und diese Treffer sind keine Fragen an die Spec, sondern
Wiedervorlagen. Sie würden den Befund ersäufen.

**Beschluss.** Die Go-Fassung wird auf den laufenden Stand gebracht, bevor die Kampagne fährt; die
Kampagne misst den Text, wie er heute dasteht. Begründung: gesucht wird die Mehrdeutigkeit, die ein
künftiger Implementierer vorfindet. Die Mehrdeutigkeit des alten Textes ist Archäologie — ihre
Antworten stehen in D266 bis D285 und haben seit D280 Vektoren.

**Der Preis, benannt.** Die Go-Fassung liest damit einen Text, der wegen ihrer eigenen Fragen
repariert wurde; sie ist an den Antworten geschult und in diesem Umfang nicht mehr unabhängig. Was
die Kampagne verliert, sind Falschnegative an genau den Stellen, die `00ad-fragen-befund.md` schon
benannt hat. Was sie behält, ist tragfähig: eine Uneinigkeit über den **reparierten** Text heißt,
dass die Reparatur das Verhalten nicht festlegt, und das ist ein schärferer Befund als eine
Uneinigkeit über den alten.

**Für neue Fassungen bleibt D258 Beschluss 3 unverändert.** Eine dritte Fassung liest einen
eingefrorenen Anker, und dieser Anker ist ab jetzt der Stand, gegen den auch die Go-Fassung
nachgezogen wird. Ohne diesen Satz wandert der Anker mit jeder Sitzung, und die Häufung, die D258
messen will, wäre nie wieder herstellbar.

**Verworfen: die Kampagne gegen den alten Anker fahren und die bekannten Abweichungen vorher
herausfiltern.** Der Filter wäre eine Liste aus zwanzig Registereinträgen, von Hand gepflegt, und
jede Lücke darin erzeugt einen Scheinbefund, jede Übervorsicht ein stilles Übersehen. Ein Filter,
der so groß ist wie der Befund, den er reinigen soll, ist kein Filter.

**Verworfen: zuerst eine dritte Fassung gegen den alten Anker.** Das wäre der sauberste Versuch für
die Frage nach der Häufung — und die falsche Frage zuerst. Die Spec-Arbeit braucht die
Mehrdeutigkeit von heute; die Häufung ist ein Nebenertrag, der nicht die Reihenfolge bestimmt.

---

### D291 — NV2 bekommt seine Signatur; der Vektor trug zwei Mängel statt einem

**Anlass.** Der Nachzug der Go-Fassung nach D290 hat fünf neue Einträge in ihrer Fragenliste
erzeugt. Einer davon fragt, was gilt, wenn eine Bytefolge zugleich nicht kanonisch kodiert ist und
ein Pflichtfeld vermissen lässt, und benennt `C.7` als den Fall.

**Gemessen.** Die in `C.7` gedruckte Bytefolge trägt die Keys 0 bis 8. **Key 9 fehlt.** Sie ist der
*Core* von TV1, unsortiert kodiert, nicht die signierte Map. Damit trägt der Vektor zwei Mängel:
eine nicht-kanonische Kodierung und ein fehlendes Pflichtfeld.

**Warum das den Code falsch macht.** `B.2` erklärt, `NON_CANONICAL_ENCODING` behaupte, es gebe eine
kanonische Kodierung desselben Inhalts, die gültig wäre. Für die gedruckte Folge ist das falsch:
ihre kanonische Kodierung ist TV1s Core, und der ist ohne `σ` kein gültiger Claim. Nach D262 ist ein
Code, dessen Aussage die Bytefolge nicht trägt, das einzige, was über allen Codewahlen verboten ist.
Der Vektor hat seit `00c` einen Code gedruckt, den er selbst widerlegt.

**Beschluss.** NV2 wird die vollständige signierte TV1-Map, einschließlich `σ`, in der
Key-Reihenfolge 8,6,5,3,2,1,0,7,4,9 kodiert. 309 Byte. Der erwartete Code bleibt
`NON_CANONICAL_ENCODING` und ist damit zum ersten Mal wahr: die kanonische Kodierung desselben
Inhalts ist TV1, und TV1 ist gültig.

**Warum der Vektor geändert wird und nicht sein Code.** Die Absicht von `C.7` steht in seiner
Überschrift — nicht-kanonische Kodierung, sonst nichts. Ein Vektor trägt nach D257 genau den
Mangel, den er behauptet. Das fehlende `σ` war ein Fehler beim Abschreiben der Konstante, keine
Aussage. Den Code auf `MALFORMED_CBOR` zu ziehen hieße, den Vektor für die Kanonizität zu
verlieren, den einzigen, den `01` dafür hat.

**Ein zweiter Mangel fällt mit.** NV2 ist bisher der einzige Vektor ohne Drahtbytes und damit der
einzige, der nicht in der parametrisierten Vektorprüfung steht — festgehalten in
`einlesen-a-abnahme.md` und geprüft von `test_reject_vectors_without_wire_are_exactly_nv2`. Mit der
neuen Fassung ist er eine Bytefolge wie jede andere, wird parametrisiert gefahren und die Ausnahme
entfällt.

**Berichtigung an dieser Stelle.** Bei der Abnahme des Laufs stand hier zunächst, der Vektor mit dem
Widerspruch sei genau der, den niemand ausgeführt habe. Das ist zu stark. Nachgemessen:
`tests/test_verifier.py` hat in `_nv2_wire` die signierte Fassung im Test **selbst gebaut** — den
gedruckten Core dekodiert, `σ` als Key 9 angehängt, nicht-kanonisch zurückgeschrieben — und zwei
Tests darauf gefahren. Diese Rekonstruktion ergibt byte-genau dieselben 309 Byte, die dieser
Beschluss festlegt. Nicht ausgeführt war also die **gedruckte** Bytefolge, und falsch war der
Spec-Text; der Code hatte die Lücke bereits im Test geschlossen, ohne sie zu melden. Damit ist der
Befund enger und zugleich schärfer: eine Testdatei hat einen Vektor stillschweigend berichtigt,
statt den Vektor zu berichtigen. Der Lauf zieht diese Rekonstruktion in die Vektordatei zurück.

**Nicht nachgezogen.** `einlesen-a-abnahme.md`, `einlesen-a-prompt.md` und
`einlesen-a-nachlauf-prompt.md` halten fest, dass NV2 keine Drahtbytes trägt. Das war zutreffend,
als es geschrieben wurde. Befund- und Prompt-Dateien sind Protokoll eines Laufs und werden nicht
rückwirkend berichtigt; dieselbe Begründung wie in D232.

---

### D292 — Der Vorrang nennt seine Fälle abschließend; `§6` Punkt 4 wird aufgeteilt

**Anlass.** Zwei weitere Einträge aus dem Nachzug der Go-Fassung. Beide betreffen Stellen, an denen
der Text eine Entscheidung erzwingt, ohne sie zu treffen — und an beiden haben Referenz und
Go-Fassung dieselbe Wahl getroffen, ohne dass der Text sie vorgibt.

**Erstens: der Vorrang in `B.2` zählte Beispiele, wo er eine Menge braucht.** Der Satz nennt
Nicht-uint-Schlüssel, doppelten Key und falschen Feldtyp als Mängel, die keine Kodierung behebt.
Nicht genannt sind zwei Fälle, die dieselbe Eigenschaft haben: die oberste Ebene ist keine Map, und
ein Pflichtfeld fehlt. Für den ersten hat D285 mit `C.15` einen Vektor beschlossen — und damit eine
Norm in einen Anhang gelegt, statt sie in `B.2` auszusprechen. Genau das musste die Go-Fassung neu
entscheiden, drei Sitzungen nach dem Beschluss.

**Beschluss 1.** Die Aufzählung wird vollständig und ausdrücklich abschließend: keine Map, kein
uint-Schlüssel, doppelter Key, fehlendes Pflichtfeld, Key außerhalb der Feldtabelle, falscher Typ
oder falsche Länge. Was nicht in ihr steht, hebt `NON_CANONICAL_ENCODING` nicht auf.

**Zweitens: `§6` Punkt 4 hängt ein „sonst" an eine Konjunktion.** Der Text lautet: bei `core/*`
Prädikat ∈ `{revoke@1, supersede@1}` **und** `J.tag == claim-ref` (sonst `MALFORMED_CBOR`). Das
Klammerwort kann auf beide Bedingungen gehen — dann wäre `core/rotate@1` ein `MALFORMED_CBOR` — oder
nur auf die zweite. `B.2` und `§2.4` Invariante 4 sagen `RESERVED_CORE_PREDICATE`; `§6` allein sagt
es nicht.

**Beschluss 2.** Die drei Bedingungen werden einzeln geführt, jede mit ihrem eigenen Code.

**Warum das kein Verhalten ändert.** Beide Fassungen tun das Beschlossene schon. Nachgemessen:
`core/rotate@1` liefert in der Referenz `RESERVED_CORE_PREDICATE`, `core/revoke@1` mit `J.tag` 1
oder 3 liefert `MALFORMED_CBOR`, und die Go-Fassung liefert dasselbe. Der Schnitt schreibt auf, was
gilt; er ändert es nicht. Genau deshalb ist er billig und genau deshalb wäre er ohne die zweite
Fassung nie aufgefallen — eine Mehrdeutigkeit, die alle gleich auflösen, sieht niemand von innen.

**Was der Nachzug sonst noch gebracht hat, und was nicht.** Fünf neue Fragen, drei davon Defekte
(diese beiden und der aus D291). Zwei sind Klarstellungen ohne Verhaltensfolge: ob der Präfixtest
auf den Rohstring geht — der Text sagt „beginnt mit", und beide Fassungen lesen es so — und ob ein
Break in Wertposition beim Dekodieren oder beim Re-Serialisieren scheitert, was `B.2` ausdrücklich
freistellt. Sie werden nicht Text.

**Der Ertrag von D290, beziffert.** Elf von siebzehn alten Fragen hat der reparierte Text
geschlossen, sechs blieben offen, fünf kamen hinzu. Der Nachzug allein, ohne eine einzige Mutation,
hat drei Defekte gefunden. Das ist der Beleg dafür, dass die Kampagne aus D289 gegen den heutigen
Text zu fahren ist und nicht gegen den alten.

---

### D293 — Ort und Schnitt der Kampagne: Korpus und Verdikt im Repo, der Vergleich außerhalb

**Die Frage.** Wo läuft das Gitter aus D289 — im Hauptrepo als Werkzeug oder als Wegwerf-Skript im
ausgepackten Baum? Der benannte Preis der ersten Antwort: ein Werkzeug, das die Zweitfassung
aufruft, wäre die erste Stelle, an der das Hauptrepo etwas außerhalb seiner selbst braucht.

**Der Preis hängt an einem Schnitt, den niemand gefordert hat.** Er entsteht nur, wenn ein einziges
Werkzeug Korpus, Lauf und Vergleich zugleich trägt. Zerfällt die Kampagne in drei Teile, ruft das
Repo nichts Fremdes auf.

**Beschluss 1 — der Korpusbauer liegt im Repo.** `tools/korpus.py` liefert die Drahtbytes als
Hexzeilen und dieselbe Menge als Namensmanifest. In dieser Stufe ist die Mutationsmenge leer: der
Korpus ist Anhang C. Das Gitter aus D289 wird darauf gesetzt, nicht daneben.

**Beschluss 2 — der Verdiktläufer liegt im Repo.** `tools/verdikt.py` liest Hexzeilen und schreibt
je Eingabezeile eine Verdiktzeile in der Form der Go-Fassung: Annahme mit der `claim_id` in Hex,
Ablehnung mit dem Codenamen aus `01 §B.2`. Damit ist die Referenz kein Sonderfall, sondern eine
Fassung unter Gleichen, und der Vergleich zweier Fassungen ist ein Zeilenvergleich.

**Beschluss 3 — der Vergleich liegt außerhalb.** Er ruft beide Fassungen auf und legt das Ergebnis
gegen das Manifest. Er ist Wegwerfware und bleibt es; kein Werkzeug im Repo kennt die Go-Fassung.

**Warum die ersten beiden trotzdem ins Repo gehören.** D258 will die Häufung über mehrere
Fassungen, D290 friert dafür den Anker ein. Ein Korpus, dessen Erzeuger nach der Sitzung
verschwindet, ist für eine dritte Fassung nicht wieder herstellbar, und ein Befund, der sich nicht
wieder herstellen lässt, ist keiner.

**Beschluss 4 — der Korpus liest die committete Vektordatei, nicht den Generator.**
`tests/vectors/vectors_01.json` ist das Artefakt, das auch eine fremde Fassung läse. Damit zeigt
die Abhängigkeit von `tools` auf Daten und nicht auf `tests`. Die Datei ist dafür an ihren
Generator zu binden; das entscheidet D295.

**Beschluss 5 — die Hex-Konventionen der Go-Fassung werden gespiegelt, obwohl D269 sie ausdrücklich
für nicht-normativ erklärt hat.** Ungerade Länge, Nicht-Hexzeichen und Innen-Whitespace ergeben
`MALFORMED_CBOR`, Großbuchstaben sind zulässig, das Zeilenende wird gekürzt. Begründung: ein
Formatunterschied erzeugt Diffzeilen, die wie ein Befund aussehen und keiner sind. Der Zweck der
Kampagne ist Uneinigkeit über den Text, nicht Uneinigkeit über den Transport. Gemessen an sechs
Sonderzeilen gegen die gebaute Go-Fassung, alle sechs gleich. Nötig ist das Spiegeln, weil
`bytes.fromhex` Innen-Whitespace annimmt: ohne ausdrückliches Tor wäre die Referenz hier
großzügiger als die Go-Fassung, und die Abweichung fiele erst an mutiertem Material auf.

**Verworfen: das Wegwerf-Skript im ausgepackten Baum.** Es kostet in dieser Sitzung nichts und in
der nächsten alles. Der ausgepackte Baum ist ein Messplatz, kein Ablageort; was dort entsteht, ist
nach der Sitzung fort, und die Kampagne wäre einmalig statt wiederholbar.

**Verworfen: ein Werkzeug im Repo, das die Go-Fassung aufruft.** Es bindet das Hauptrepo an eine
Toolchain, ein Arbeitsverzeichnis und eine Fassung, von denen keines seine Sache ist. Der Aufruf
gehört dorthin, wo auch der Pfad zur zweiten Fassung steht.

---

### D294 — Der Rückstand der Go-Fassung ist dokumentarisch; D290 wird gemessen statt nachgezogen

**Die Frage.** D290 verlangt die Go-Fassung auf dem laufenden Stand, bevor die Kampagne fährt. Ihr
gelesener Spec-Stand ist `b3cf487`, der Kopf ist `79b73a2`.

**Gemessen.** Genau ein Commit berührt `01-claim-atom.md` dazwischen: `88361b2`, zweiundzwanzig
Zeilen ein und dreizehn aus, und das ist D291 plus D292. Die gebaute Go-Fassung bei `127a74c`
liefert über die vierzig Zeilen des heutigen Anhang C vierzig Verdikte, die den vierzig der
Referenz Zeichen für Zeichen gleichen.

**Beschluss.** Kein Code-Nachzug. Der Rückstand ist dokumentarisch: D291 setzt einen Vektor
instand, D292 schreibt auf, was beide Fassungen bereits tun. Der Text hat sich geändert, das
Verhalten nicht.

**Warum nicht einfach nachziehen.** Ein Nachzug hätte diesen Satz nicht bestätigt, sondern
gelöscht. Er repariert, bevor er fragt, und danach ist nicht mehr feststellbar, ob D292 Verhalten
geändert hat oder nur beschrieben. Die Behauptung aus D292, beide Fassungen lösten die drei
Mehrdeutigkeiten gleich auf, war bis hierher eine Behauptung; jetzt ist sie gemessen.

**Die Reichweite, benannt.** Die Messung deckt vierzig Vektoren und sagt nichts über Eingaben
außerhalb Anhang C. Genau das ist der Grund, warum die Kampagne überhaupt fährt. Einigkeit auf der
bekannten Menge ist die Eichung des Messgeräts nach Prüfregel 51, nicht das Ergebnis.

**Benannter Rückstand.** Die Spec-Kopie unter `~/mar-go/spec` trägt weiter den alten Text. Sie ist
auf `79b73a2` zu bringen, damit der mit D290 eingefrorene Anker für eine dritte Fassung dort steht,
wo er behauptet wird. Das ist eine Dateikopie, kein Lauf.

**Was daneben liegt.** Die Go-Fassung ist ab jetzt das Orakel einer laufenden Kampagne und hat
weiterhin kein Remote. Ein Plattenschaden nimmt nicht mehr nur eine Zweitimplementierung mit.

**Verworfen: nachziehen und danach messen.** Dann wäre die Gleichheit der vierzig Verdikte trivial
und die eigentliche Frage unbeantwortbar.

---

### D295 — Die Vektordatei war nicht an ihren Generator gebunden

**Der Befund.** `tests/vectors/vectors_01.json` wird von `tests/vectors/gen.py` erzeugt und von
fünf Testdateien als Fixture gelesen: `tests/test_vectors_01.py`, `tests/test_verifier.py`,
`tests/test_atom.py`, `tests/test_vouch_payload.py` und `tests/trust/test_coupling.py`. Kein Test
hat die beiden Artefakte aneinander gebunden. `test_claim_id_matches_golden` rechnet mit
`build_vectors()` neu und sieht die Datei nicht; `test_vectors_json_exists` prüft aus der Datei ein
einziges Feld. Eine veraltete Datei wäre grün durchgelaufen, und die vier übrigen Testdateien
hätten stillschweigend alten Bestand geprüft.

**Gemessen.** Heute stimmen Datei und Generator in jedem Feld überein. Der Befund ist eine offene
Tür, kein Schaden.

**Beschluss.** Ein Test bindet die geladene Datei vollständig an `build_vectors()`. Geeicht mit
drei Rücknahmeproben in der Driftrichtung, die zählt — veraltete Datei bei laufendem Generator:
ein geänderter Vektorname, eine geänderte Erwartung, eine geänderte `claim_id`, jede einzeln rot.

**Was das nicht ist.** Nicht die bekannte Generatordrift auf der offenen Liste. Die betrifft den
Spec-Text gegen die Vektordatei, und gegen einen eigenen Prüfer dafür spricht D233. Hier stehen
zwei Artefakte im selben Repo nebeneinander, und die Bindung kostet eine Zeile.

**Nicht geprüft: die Gegenrichtung.** Ein geänderter Generator bei stehender Datei lässt die
Fixture selbst abstürzen, weil die NV17-Konstruktion auf einem getippten Bytepaar aus TV1 aufsetzt;
der Bindungstest läuft dann gar nicht. Das ist keine Eigenschaft des Tests, sondern eine von
`gen.py`, und sie bleibt als Beobachtung stehen.

---

### D296 — Eine Rücknahmeprobe wird an ihrem roten Test abgenommen, nicht an ihrer Anzahl

**Der Befund.** Der Lauf zu D293 hat die Fällemenge geliefert, die der Prompt verlangt hat, und die
Probe „Hexziffern-Tor entfernt" schloss mit einem roten Test. Beide Aussagen stimmen, und die
geprüfte Sache war trotzdem ungeprüft. Die zwei Zeilen mit Innen-Whitespace tragen neun und elf
Zeichen; das Längentor davor fängt sie, bevor das Hexziffern-Tor überhaupt gefragt wird. Rot wurde
allein die Zeile aus zwei Buchstaben z, und die wird rot, weil `bytes.fromhex` eine Ausnahme wirft
— ein Absturz, keine Aussage über den Code. Die mit D293 Beschluss 5 beschlossene Spiegelung der
Go-Konvention hing damit an keinem Test.

**Der zweite Fehler steht im Prompt.** Er verlangte einen Trennfall gerader Länge und hielt das für
hinreichend. Das ist es nicht: eine achtstellige Folge wie die geforderte dekodiert auch ohne
Whitespace zu einer abgeschnittenen Map und ergibt wieder `MALFORMED_CBOR`. Der Fall käme durch das
vordere Tor und bliebe hinter dem hinteren stumm. Ein Trennfall muss beides — das vordere Tor
passieren und hinter dem hinteren ein anderes Ergebnis erzeugen.

**Beschluss 1 — der Trennfall wird abgeleitet, nicht getippt.** Eine Vektorzeile mit zwei
eingefügten Leerzeichen: gerade Länge, und ohne das Tor wäre das Verdikt eine Annahme statt einer
Ablehnung. Gemessen im ausgepackten Baum: mit diesem Fall macht die Probe zwei Tests rot statt
einem.

**Beschluss 2 — Prüfregel 60.** Ein Bericht über eine Rücknahmeprobe nennt den Namen des roten
Tests, nicht seine Anzahl. Die Regel steht in `pruefregeln.md` im Abschnitt über Rücknahmeproben
und Mutanten; die Herkunftsliste am Dateiende nennt D296.

**Was nicht geändert wird.** Die beiden ungeraden Zeilen bleiben in der Fällemenge. Sie prüfen das
Längentor an einer Eingabe mit Innen-Whitespace und kosten nichts.

**Wem der Defekt gehört.** Beiden Seiten. Das Werkzeug hat zwei ungerade Fälle geliefert, wo der
Prompt einen geraden verlangte; der Prompt hat eine Bedingung genannt, die nicht hinreicht. Der
Bericht war in jeder Zahl zutreffend. Deshalb steht die neue Regel bei den Berichten und nicht bei
den Tests.

---

### D297 — Die Operatorenmenge aus D289 erreicht fünf von zwölf Codes und bekommt drei Operatoren

**Anlass.** Vor dem Bau des Gitters stand die Frage, ob „Typ tauschen" ein Operator ist oder einer
je Zielklasse. Gemessen wurde beides im ausgepackten Baum gegen die Referenz, und die Frage war zu
klein gestellt.

**Gemessen, Menge aus D289 Beschluss 1, Typklasse bereits aufgefächert.** Sechs gültige
Saatvektoren, zehn Felder, fünf Operatoren: 624 Rohmutanten, nach Entdopplung 1272 verschiedene
Drahtfolgen in zwei Familien. Erreicht werden davon **fünf** der zwölf Reject-Codes.

**Der Grund liegt in der Menge, nicht in ihrer Größe.**

- „Typ tauschen" erzeugt nie einen anderen Wert **derselben** Klasse. Kein Mutant trägt darum eine
  Version ungleich eins; `UNSUPPORTED_VERSION` ist unerreichbar.
- Kein Operator greift **in** ein zusammengesetztes Feld hinein. `J` wird nur als Ganzes ersetzt,
  `J.tag` bleibt unberührt, `UNKNOWN_J_TAG` unerreichbar.
- `INVALID_GENESIS_ANCHOR` verlangt zweiunddreißig Nullbytes, `INCOHERENT_EXPIRY` ein `t_exp`
  unterhalb von `t`, `UNKNOWN_NAMESPACE` ein fremdes Präfix. Alle drei sind Werte innerhalb der
  richtigen Klasse und keiner Typänderung erreichbar.

**Beschluss 1 — die Typklasse wird aufgefächert, zehn Klassen.** Nachgemessen: alle zehn sind vom
kanonischen Kodierer erzeugbar. Damit bleibt die Mutation auf der dekodierten Map, wie D289 es
verlangt, und muss nicht auf die Byteebene ausweichen, die D289 ausdrücklich verwirft.

**Beschluss 2 — drei Operatoren kommen hinzu, alle mechanisch.**

- *Wert innerhalb der Klasse.* uint: null, eins, plus eins, minus eins, zwei hoch zweiunddreißig,
  zwei hoch vierundsechzig minus eins. bstr: Nullfolge und Einsfolge gleicher Länge, umgekehrt, um
  ein Byte kürzer, um ein Byte länger. tstr: Groß- und Kleinschreibung, ein Zeichen vorn, ein
  Zeichen hinten, ein Zeichen kürzer. bool negiert; Array kürzer, länger, umgekehrt. Dieser
  Operator **ersetzt** „Länge ändern" aus D289 und verallgemeinert ihn.
- *Rekursion in zusammengesetzte Felder.* Auf jedes Element eines Arrays werden die Typmenge und
  die Wertmenge angewandt.
- *Feldkopie innerhalb desselben Claims.* Der Wert eines Feldes wird auf ein anderes gelegt.

**Keiner der drei wählt Grenzwerte von Hand aus der Spec.** Das ist die Bedingung, unter der sie
zulässig sind: ein Gitter aus handgewählten Werten prüft, was der Autor schon bedacht hat, und wäre
nur ein zweites Anhang C. Dass die mechanischen Varianten die Grenzwerte trotzdem treffen, ist der
Befund und nicht die Absicht.

**Gemessen, erweiterte Menge.** 1217 Rohmutanten, 1146 in Familie A und 1236 in Familie B, zusammen
2382 verschiedene Drahtfolgen. Erreicht sind **zehn** der zwölf Codes. 185 Mutanten der Familie A
werden angenommen und tragen damit eine `claim_id` in den Vergleich. Der ganze Lauf samt Verdikten
braucht unter einer Sekunde; das Gitter kann deshalb in der Testsuite stehen und muss kein Werkzeug
bleiben, das nur von Hand gefahren wird.

**Die zwei fehlenden fehlen aus benanntem Grund.** `NON_CANONICAL_ENCODING` ist bauartbedingt
unerreichbar, weil Stufe 1 jeden Mutanten kanonisch neu kodiert. `FOREIGN_LIFECYCLE` braucht einen
Speicher, liegt nach D268 als einziger Fall außerhalb der selbstenthaltenen Gültigkeit und kann
nach D263 keinen Vektor bekommen. Beides ist entschieden und wird nicht nachgebessert.

**Beschluss 3 — signiert wird mit dem Schlüssel der Saat, nicht mit dem des mutierten Feldes.**
Wird `I` mutiert, gibt es zu ihm keinen Schlüssel. Der Mutant bekommt dennoch eine Signatur über
seinen eigenen Core, gerechnet mit dem Autor der Saat; das Ergebnis ist `BAD_SIGNATURE`, und zwar
ein echtes. Beim ersten Bau ist der Harness auf einen Nullschlüssel zurückgefallen und hätte
dieselbe Zahl geliefert — dieselbe Beobachtung, andere Ursache, und niemand hätte es gesehen.

**Was die Beiträge der drei Operatoren einzeln sind, gemessen.** Ohne den Wertoperator sechs Codes,
ohne die Rekursion neun, ohne die Feldkopie zehn. Die Feldkopie trägt **keinen** eigenen Code bei;
sie trägt sechzehn angenommene Mutanten bei, die kein anderer Operator erzeugt, und nach D289
Beschluss 5 ist die Annahme mit `claim_id` die schwerere Beobachtung. Sie bleibt darum, aber knapp,
und der Preis ist benannt: 466 Mutanten für sechzehn Annahmen.

**Was die Verteilung sagt.** Vier Fünftel aller Mutanten enden in `MALFORMED_CBOR`. Das ist die
Warnung aus D258 eine Ebene höher: auch feldweise Mutation trifft überwiegend dieselbe Klasse. Es
spricht nicht gegen das Gitter, denn die Aufzählung ist billig und vollständig; es sagt, wo die
Unterscheidungskraft sitzt — in den 185 angenommenen Mutanten und in den 146 der Familie A, die
einen der neun übrigen Codes tragen.

**Nachgetragen mit D298.** Die drei Mutantenzahlen dieses Eintrags sind an einem Prototyp gemessen,
dessen Vertreter der Typklassen andere waren als die der gebauten Fassung. Der laufende Stand ist
1174 in Familie A, 1264 in Familie B und 2438 zusammen; die Rohzahl, die Zahl der Annahmen und die
Reichweite sind unverändert.

---

### D298 — Die Mutantenzahlen in D297 sind Prototypzahlen; die Musterwahl entscheidet sie

**Der Befund.** Der Lauf zu D297 meldet 1174 Mutanten in Familie A, 1264 in Familie B und 2438
zusammen. D297 nennt 1146, 1236 und 2382. Das Werkzeug hat die Abweichung gemeldet statt sie
anzupassen, wie der Prompt es verlangt.

**Gemessen.** Die Operatorenmenge ist in beiden Fassungen dieselbe, und die Rohzahl 1217 stimmt
überein. Verschieden sind die zehn Vertreter der Typklassen: der Prototyp hat nichtleere Werte
gewählt, die gelieferte Fassung leere und Nullwerte. Wird die gelieferte Fassung allein auf die
Muster des Prototyps umgestellt, ergeben sich 1146, 1236 und 2382 — auf den Mutanten genau. Die
Ursache ist die Entdopplung: ein leeres Muster fällt häufiger mit einer Wertvariante zusammen als
ein nichtleeres.

**Was invariant ist, unter beiden Mustermengen gemessen.** Die Rohzahl 1217, die Zahl der
angenommenen Mutanten 185 und die Reichweite von zehn der zwölf Codes. Das sind die Größen, an
denen die Kampagne hängt. Die Mutantenzahl ist keine davon.

**Beschluss 1 — die Vertreter der Typklassen bleiben Sache des Codes, nicht des Registers.** Sie
ändern die Reichweite nicht, und zehn Konstanten im Register wären eine zweite Wahrheit neben
`tools/gitter.py`, die beim nächsten Anfassen niemand nachzieht. Das Register hält die
Operatorenmenge und die Reichweite fest; den Korpus legt der committete Code fest. Für eine dritte
Fassung nach D258 heißt das: sie bekommt den Korpus als Hexzeilen, nicht als Bauanleitung.

**Beschluss 2 — D297 bekommt einen Nachtrag statt einer Berichtigung.** Die drei Zahlen dort waren
richtig gemessen; ihr Gegenstand ist eine Fassung, die es nicht mehr gibt. Eine Zahl, die im
Register steht und die niemand mehr nachrechnen kann, ist genau das, wovor dieser Eintrag warnt —
deshalb nennt D297 künftig in einer Zeile den laufenden Stand und verweist hierher.

**Beschluss 3 — die Feldkopie bekommt einen Träger.** Ein Test verlangt, dass jeder der drei mit
D297 hinzugekommenen Operatoren mindestens einen angenommenen Mutanten erzeugt. Für den
Wertoperator und die Rekursion war das schon über die Codemenge gesichert, für die Feldkopie nicht:
sie trägt keinen eigenen Code bei, und ihre Rechtfertigung in D297 sind allein die sechzehn
Annahmen, die kein anderer Operator erzeugt. Geeicht mit drei Rücknahmeproben, jede einzeln, jede
rot am selben Test.

**Was der Lauf richtig gemacht hat.** Die dritte Rücknahmeprobe hat keinen Test rot gemacht, und
der Bericht hat das gemeldet statt nachzubessern. Genau dafür steht Prüfregel 60. Ein Bericht, der
nur die Zahl der roten Tests nennt, hätte hier eine Null gezeigt und wäre wahrscheinlich als
Fehlbedienung durchgegangen. Die Regel verlangt den Namen, und wo kein Name steht, steht die Lücke.

---

### D299 — Erster Lauf der Kampagne: 2438 Mutanten, null Befunde; der Vergleich war falsch gebaut

**Was gefahren wurde.** Der Korpus aus `tools/gitter.py`, 2438 Zeilen, durch `tools/verdikt.py` und
durch die gebaute Go-Fassung bei `127a74c`, Zeile für Zeile verglichen. 2426 Zeilen sind gleich.

**Die zwölf verschiedenen Zeilen tragen keinen Befund.** Alle liegen in Familie B, also bei
Mutanten ohne Neusignierung. Sechs betreffen `h_prev == 32×0x00`, sechs die Fristkohärenz bei TV1,
dem einzigen Saatvektor mit `t_exp`. Die Referenz meldet dort `BAD_SIGNATURE`, die Go-Fassung
`INVALID_GENESIS_ANCHOR` beziehungsweise `INCOHERENT_EXPIRY`. Nachgeprüft: die Ed25519-Prüfung
scheitert wirklich, `h_prev` ist wirklich die Nullfolge, und `t ≥ t_exp` ist wirklich erfüllt bei
einem Prädikat, das kein `core/*` ist. Beide Codes tragen einen wahren Satz.

**`01 §B.2` stellt genau das frei.** Der Absatz „Der Code ist ein Grund, kein Zustand" normiert
ausdrücklich keine Gesamtordnung: tragen mehrere Codes eine wahre Aussage über dieselbe Bytefolge,
ist die Wahl der Implementierung überlassen; verboten ist allein der falsche Satz. Und: die
Aufzählungen in `§6` sind Konjunktionen, keine Folgen. Die zwölf Zeilen sind die Ausübung dieser
Freiheit durch zwei Fassungen, die sie verschieden ausüben.

**Der Befund ist das Verfahren, nicht das Ergebnis.** Ein zeilenweiser Vergleich behandelt jede
Ausgabe als bestimmt. Wo der Text die Wahl freistellt, meldet er Freiheit als Uneinigkeit. Die
Kampagne hätte bei jedem weiteren Lauf dieselben zwölf Zeilen wieder gemeldet, und irgendwann hätte
jemand sie für Rauschen gehalten und nicht mehr hingesehen.

**Beschluss 1 — der Vergleich wird zweistufig ausgewertet.** Stufe eins ist immer ein Befund: eine
Fassung nimmt an und die andere lehnt ab, oder beide nehmen an und die `claim_id` unterscheidet
sich. Stufe zwei ist ein Kandidat: beide lehnen ab, mit verschiedenem Code. Ein Kandidat wird zum
Befund erst, wenn einer der beiden Codes einen Satz behauptet, den die Bytefolge nicht trägt — die
Prüfung ist die Auslöserspalte in `01 §B.2`, nicht eine Rangliste. In diesem Lauf: Stufe eins null,
Stufe zwei zwölf, davon null Befunde.

**Beschluss 2 — Prüfregel 61.** Eine Abweichung zwischen zwei Fassungen ist erst ein Befund, wenn
die Spec den Punkt festlegt. Die Regel steht in `pruefregeln.md` im Abschnitt über die Abnahme und
den Merge; die Herkunftsliste am Dateiende nennt D299.

**Was der Supervisor falsch gemacht hat.** Zwei Züge lang wurde ein Fork aufgebaut — welcher Code
bei mehreren Mängeln gewinnt —, den `01 §B.2` in einem Absatz schließt. Es wurde eine Position
bezogen, ein Literaturbefund eingeholt, eine eigene Begründung aufgestellt und wieder
zurückgenommen, und erst danach der normative Absatz gelesen. Prüfregel 38 verlangt den
Registerindex vor der Position; hier wäre schon das Lesen von `B.2` genug gewesen. Der Befund über
den Text war ein Befund über den, der ihn nicht gelesen hat.

**Ein Umstand, der es nicht entschuldigt und trotzdem zählt.** `tools/register_index.py` liefert
für `01 §B.2` eine leere Zeile, weil der Index nur `§` mit Ziffernfolge kennt. Der billigste erste
Griff des Arbeitsbogens ist genau dort stumm, wo dieser Text steht — in einem Anhang. Der Mangel
stand als Kleinkram auf der offenen Liste; er hat jetzt zwei Züge gekostet und ist der nächste
Lauf.

**Was der Lauf positiv zeigt.** Zwei unabhängig gebaute Fassungen stimmen über 2438 Eingaben in
allem überein, was der Text festlegt, einschließlich zehn der zwölf Fehlerklassen. Das ist die
Häufung, die D258 wollte, und es ist der erste Beleg dafür, dass die Reparaturen aus D291 und D292
gehalten haben. Was es nicht zeigt: eine Mehrdeutigkeit, die beide Fassungen gleich auflösen,
sieht auch dieser Vergleich nicht — die Grenze aus `00aj` steht unverändert.

---

### D300 — Der Registerindex lernt Anhangsverweise

**Anlass.** Prüfregel 38 nennt `tools/register_index.py` den billigsten ersten Griff vor jeder
Position. In `00ak` war er stumm: `01 §B.2` liefert eine leere Zeile, weil die Verweiserkennung
nach dem Paragraphenzeichen nur eine Ziffernfolge kennt. Der normative Absatz, der D299 entschieden
hätte, steht in einem Anhang. Der Mangel stand als Kleinkram auf der offenen Liste und hat zwei
Züge gekostet.

**Gemessen.** Mit der Anhangsform erkennt der Index sechs weitere Abschnitte und 23 weitere
Verweise; die Zahl der Abschnitte steigt von 115 auf 121, und kein bestehender Eintrag ändert sich.
`01 §B.2` allein trägt elf Einträge: D265, D266, D267, D269, D270, D271, D272, D279, D289, D293 und
D299. Genau die Menge, die die Vorrangfrage entschieden hätte.

**Beschluss.** Die Verweiserkennung nimmt neben der Ziffernform auch die Anhangsform aus D230 an —
ein Großbuchstabe, ein Punkt, dann eine Ziffernfolge, die weitere punktgetrennte Ziffern tragen
kann. Die Ziffernform bleibt unverändert. Der Index bekommt seinen ersten Test; bisher hatte er
keinen.

**Die Grenze bleibt, wo D229 sie gezogen hat.** Der Index sagt, welche Einträge einen Abschnitt
nennen, nicht ob sie ihn richtig nennen. Ein vollständigerer Index macht Prüfregel 27 nicht
überflüssig — er macht sie nur bezahlbar.

**Nachgetragen nach dem Lauf.** Die Liste zu `01 §B.2` trägt zwölf Einträge, nicht elf, und die
sechs neuen Abschnitte tragen 24 Verweise, nicht 23. Der zwölfte ist D300 selbst: der Eintrag nennt
den Abschnitt, und er existierte bei der Messung noch nicht. Beide Zahlen oben sind an einem
Register ohne diesen Eintrag gemessen.

**Eine Grenze des Tests, benannt.** `test_b2_list_is_derived_from_register_text` leitet die
erwartete Menge über das Vorkommen der Zeichenfolge ab, nicht über die Verweisgrammatik — sonst
prüfte er das Werkzeug mit dem Werkzeug. Der Preis: entstünde je ein Abschnitt `B.2.1` oder `B.20`,
zählte die Ableitung ihn zu `B.2`, und der Test würde falsch rot. Heute gibt es keinen, und die
Nichtzirkularität ist den Preis wert (Prüfregel 51 in der Gegenrichtung).

---

### D301 — Die Backslashes in den Wurzel-Markdowns sind tragend, kein Rückstand

**Der Befund.** Die offene Liste führt sieben Zeilen in fünf Dateien als Kleinkram und daneben die
neunzehn Zeilen der `sitzungsstart`-Reihe. Nachgesehen, was dort steht:

- Vier Zeilen in `02b-golden-anchors.md` und eine in `02-spec-nachzug.md` escapen einen senkrechten
  Strich **innerhalb einer Tabellenzelle**. Ohne den Backslash bricht die Zelle, weil der Strich
  der Spaltentrenner ist. Der Ausdruck ist eine Betragsklammer, keine Escape-Sequenz für ein Byte.
- Die Zeile in `01-claim-atom.md` escapet einen Stern am Zeilenanfang. Ohne den Backslash wird aus
  der Fußnote ein Listenpunkt.
- Die beiden übrigen und die neunzehn der `sitzungsstart`-Reihe stehen in zitierten Suchmustern
  innerhalb von Inline-Code und sind deren Inhalt.

**Beschluss 1 — die Regel gilt Escape-Sequenzen in normativem Text, nicht der Markdown-Auszeichnung
und nicht zitierten Mustern.** Bytes werden als `h'ff'` geschrieben; das ist ihr Zweck. Ein
Backslash, der einen Tabellentrenner oder einen Listenmarker neutralisiert, ist Auszeichnung und
kein Inhalt. Der Posten wird von der offenen Liste gestrichen, nicht abgearbeitet.

**Beschluss 2 — die beiden baren Verweise in `02b-abnahme.md` bekommen die Dateinamensform.** Sie
zeigen auf `B.4` und `C.3` **derselben** Datei. Die Kurzform `02b` wäre falsch, weil
`02b-golden-anchors.md` kein `B.4` trägt; `tools/check_specs.py` fängt sie, nachgeprüft. Richtig
ist die Dateinamensform. Damit sind beide Verweise geprüft statt nur vorhanden — und der dritte
Posten des angekündigten Kleinkram-Laufs ist erledigt, ohne dass er stattgefunden hat.

**Was daran allgemein ist.** Ein Posten auf der offenen Liste ist eine Behauptung wie jede andere
und untersteht Prüfregel 27. Zwei der drei Punkte waren keine Mängel, der dritte war eine Zeile.

---

### D302 — Der Anker der Zweitfassung wird als Text verkörpert, nicht nur als Dateiinhalt

**Die Frage.** D294 hinterlässt einen benannten Rückstand: die Spec-Kopie unter `~/mar-go/spec` ist
nachzuziehen, damit der mit D290 eingefrorene Anker für eine dritte Fassung dort steht, wo er
behauptet wird. Welcher Stand das ist und wo er stehen soll, sagt der Eintrag nicht.

**Gemessen — der Stand.** Der Unterschied zwischen der Kopie und dem heutigen Text besteht aus drei
Hunks in `01-claim-atom.md`, zweiundzwanzig Zeilen ein und dreizehn aus. Das sind Zeile für Zeile
die Zahlen, die D294 für `88361b2` misst. Seither ist die Datei nicht erneut berührt worden: der
Nachzug auf `79b73a2`, den D294 wörtlich verlangt, und der Nachzug auf den heutigen Kopf `a1f4751`
liefern dieselbe Datei mit dem Blob `0271a180`.

**Gemessen — der Ort.** Die Zeichenfolge `88361b2` kommt in `~/mar-go` in keiner Datei vor, und
kein anderer Kurzhash steht dort. Der Anker ist ausschließlich als Dateiinhalt verkörpert. Eine
dritte Fassung, die `spec/01-claim-atom.md` liest, kann nicht feststellen, welchen Stand sie liest;
ein späterer Nachzug hinterlässt keine Spur, und ein versehentlicher ebenso wenig.

**Beschluss 1 — die Kopie wird nachgezogen.** Zielblob `0271a180`, prüfbar mit `git hash-object`.

**Beschluss 2 — der Anker bekommt eine Textform.** `spec/STAND.md` nennt die Quelle, den Commit,
die Datei und ihren Blob-Hash. Damit ist der Anker feststellbar statt behauptet, und ein
Verschieben ist eine sichtbare Änderung statt einer stillen.

**Beschluss 3 — der benannte Commit ist `79b73a2`, nicht der laufende Kopf.** D290 friert den Anker
ein, damit die Häufung aus D258 herstellbar bleibt. Dass die Datei heute unverändert gilt, ist ein
Messergebnis und kein Grund, den Namen mitwandern zu lassen; `git show 79b73a2:01-claim-atom.md`
liefert genau diese Bytes, und das ist die Prüfung, die eine dritte Fassung fahren kann.

**Verworfen: den Anker auf den jeweils laufenden Kopf setzen.** Genau davor warnt D290. Der Text
hat sich nicht geändert, also gibt es nichts zu benennen; wandert der Name trotzdem, ist bei der
nächsten Änderung nicht mehr unterscheidbar, ob sie den Anker verschoben hat oder nicht.

**Verworfen: nur die Datei kopieren, ohne Vermerk.** Damit wäre der Rückstand aus D294 dem Wortlaut
nach erfüllt und der Sache nach nicht. Der Eintrag verlangt, dass der Anker dort steht, wo er
behauptet wird — eine Datei ohne Herkunftsangabe behauptet nichts.

**Was daneben liegt.** `~/mar-go/spec` trägt nur `01-claim-atom.md`. Das ist der Umfang aus D256
und D268 und keine Lücke; eine dritte Fassung mit anderem Umfang bräuchte einen eigenen Anker.

---

### D303 — Familie C: nicht-kanonische Kodierung auf der unmutierten Saat

**Anlass.** Das Gitter erreicht zehn der zwölf Reject-Codes, gemessen über die 2438 Mutanten des
Bestands. `NON_CANONICAL_ENCODING` fehlt bauartbedingt: alle drei Erzeugungswege in
`tools/gitter.py` enden in `cbor_canon.encode`, und was kanonisch kodiert wurde, kann den Code
nicht auslösen. Anhang C erreicht ihn zweimal, über eigene Vektoren, nicht über das Gitter.

**Beschluss 1 — eine dritte Familie auf der Byteebene.** Familie C nimmt eine Saat unverändert und
kodiert sie nicht-kanonisch. Der Inhalt bleibt gültig, die Bytes werden es nicht. Etikettpräfix
`C/`, Ort `tools/gitter.py` neben den bestehenden Familien; ein eigenes Werkzeug bräuchte einen
zweiten Aufruf im Vergleichslauf, ohne etwas zu trennen, was zusammengehört.

**Beschluss 2 — Familie C wird nicht mit Inhaltsmutationen kombiniert.** Trägt der Inhalt einen der
in `01 §B.2` abschließend aufgezählten Mängel, verdrängt der Vorrang nach `MALFORMED_CBOR` und die
Kodierung wird stumm; das trifft vier Fünftel der abgelehnten Gittermutanten. Trägt er einen
anderen Mangel, stehen zwei wahre Codes nebeneinander und `01 §B.2` stellt die Wahl ausdrücklich
frei. Beide Fälle erzeugen kein Urteil, und der zweite erzeugt zusätzlich Rauschen der Art, die
D299 bereits als Nichtbefund entlarvt hat.

**Beschluss 3 — der Operatorensatz zielt auf Formvielfalt, nicht auf Saatvielfalt.** Eine
Kodierungsform, die eine zweite Fassung anders behandelt, behandelt sie auf jeder Saat gleich
anders; der Erkenntniswert liegt in der Zahl der Formen. Fünf Operatoren sind prototypisch
gefahren und liefern durchweg `NON_CANONICAL_ENCODING`: die umgekehrte Schlüsselreihenfolge, der
Map-Kopf als indefinite-length, der Map-Kopf mit breiterem Längenfeld, die Schlüssel mit breiterem
Kopf, und der Kopf eines einzelnen Feldwerts eine Stufe breiter. Der letzte greift je Feld einzeln
und trägt allein vierzig Zeilen.

**Beschluss 4 — die Zahlen sind Prototypzahlen.** Wie in D298: die Wahl der Operatoren entscheidet
den Umfang, nicht die Reichweite. Die Zeilenzahl der gelieferten Fassung wird bei der Abnahme
gemessen und steht nicht im Prompt.

**Was Familie C tatsächlich misst.** `01 §B.2` rechnet dekodierbare indefinite-length ausdrücklich
zu `NON_CANONICAL_ENCODING`, während die Auslöserzeile von `MALFORMED_CBOR` mit "nicht dekodierbar"
beginnt. Eine Fassung, die einen nicht-minimalen Kopf gar nicht erst dekodiert, hält ihren Code für
wahr — und die Referenz hält den ihren für wahr, weil ihr Dekodierer tolerant ist. Das ist keine
freie Wahl unter zwei wahren Sätzen, sondern eine Uneinigkeit darüber, welcher Satz wahr ist. Genau
dafür fährt die Kampagne.

**Verworfen: die Kodierungsvarianten als Vektoren in Anhang C.** Dort stehen bereits zwei; eine
dritte Stelle im Spec-Text hätte den Generatordriftbefund aus D295 wieder aufgemacht, ohne die
Menge zu vergrößern.

**Was daneben liegt.** `FOREIGN_LIFECYCLE` bleibt auch mit Familie C unerreichbar, weil er einen
Speicher braucht (D263, D268). Mit C sind elf der zwölf Codes über das Gitter erreichbar.

---

### D304 — Abnahme der Familie C; eine Rücknahmeprobe darf ihre eigene Menge nicht leeren

**Abnahme.** Die gelieferte Fassung wurde aus dem Diff rekonstruiert und gefahren, nicht aus dem
Bericht übernommen. Die beiden Blob-Hashes `96f0fe1` und `fd9ab52` treffen die Indexzeilen des
Diffs; damit ist die gemessene Fassung byteweise die gelieferte (Prüfregel 59).

**Gemessen.** 2502 Zeilen, davon 2438 ohne Präfix und 64 mit. Die Codeverteilung der 2438 ist
Zahl für Zahl die des Vorlaufs, einschliesslich der 1758 auf `MALFORMED_CBOR` und der 185
Annahmen; Familie A und B sind unberührt. Alle 64 Zeilen der Familie C werden mit
`NON_CANONICAL_ENCODING` abgelehnt, und jede führt beim kanonischen Neukodieren auf die Bytes ihrer
Saat zurück. Etiketten und Bytes sind über die ganze Menge paarweise verschieden. Damit sind elf
der zwölf Reject-Codes über das Gitter erreichbar; `FOREIGN_LIFECYCLE` bleibt draussen (D263,
D268).

**Befund gegen den Prompt, nicht gegen den Lauf.** Die zweite Rücknahmeprobe verlangte, die Bytes
der Familie C vor der Ausgabe kanonisch neu zu kodieren, und erwartete den Bauart-Test rot. Sie
wurde gefahren und blieb grün: die Aufnahme verwirft kanonische Saatbytes, die Familie wurde leer,
und ein Test, der über sie allquantifiziert, ist über der leeren Menge wahr. Das Werkzeug hat die
Abweichung gemeldet statt sie anzupassen, wie der Prompt es verlangt.

**Prüfregel 62.** Eine Rücknahmeprobe darf die Menge nicht leeren, über die ihr roter Test
quantifiziert. Der Zusatz zu Prüfregel 60: dort geht es darum, welcher Test rot wird, hier darum,
dass er überhaupt rot werden kann.

**Was der Bauart-Test trägt und was nicht.** Er sichert die Bauform jeder vorhandenen C-Zeile,
nicht ihre Existenz. Getragen wird die Nichtleere allein vom Operatorentest, der zu jedem der fünf
Namen aus der Modulkonstanten mindestens eine Zeile verlangt. Beide zusammen sind vollständig,
einzeln ist es keiner — das ist kein Mangel, aber es ist der Grund, warum die Probe stumm blieb.

**Offen, klein und benannt.** Der Operator `feldkopf_breiter` greift nicht auf `t` und `t_exp`. Die
beiden Felder tragen Additional Information 26, und der Prompt lässt den Operator bei 26 und 27
aussetzen. Der Schritt von 26 auf 27 wäre möglich und ergäbe zwölf weitere Zeilen in einer
Kodierungsform, die eine zweite Fassung anders behandeln könnte. Zurückgestellt, weil die
Erreichbarkeit damit nicht wächst.

---

### D305 — Der Zuschnitt der Stufe 2 folgt der Aussagekraft, nicht der Vollständigkeit

**Die Vorfrage.** Für Stufe 2 stand offen, ob die Kombinationsmenge vollständig aufgezählt oder
gezogen wird. Beides ist verkehrt. Die Menge wird geschnitten, und der Schnitt folgt der Frage,
wo `01 §B.2` überhaupt eine Antwort erzwingt.

**Gemessen.** Paare aus zwei Mängeln auf verschiedenen Feldern derselben Saat innerhalb derselben
Familie ergeben 216692 Kombinationen. Nach den Einzelverdikten ihrer beiden Mängel zerfallen sie
in vier Klassen: 2125 aus zwei angenommenen Mängeln, 27403 aus einem angenommenen und einem
abgelehnten, 10436 aus zwei verschiedenen Ablehnungen, und 176728, bei denen mindestens ein Mangel
allein schon `MALFORMED_CBOR` erzeugt.

**Beschluss 1 — die Klassen eins bis drei werden vollständig aufgezählt.** Das sind 39964 Paare.
In Klasse eins müssen beide Fassungen annehmen und dieselbe `claim_id` liefern; in Klasse zwei
trägt nur ein Mangel einen Code, und die Wahl ist nicht frei. Beide Klassen erzwingen genau eine
Antwort und tragen deshalb einen Befund, der nicht wieder zerfällt.

**Beschluss 2 — Klasse vier wird nicht gezogen, sondern durch eine benannte Vorrangprobe
ersetzt.** Der Vorrang aus `01 §B.2` macht dort den Partner stumm: beide Fassungen liefern
`MALFORMED_CBOR`, und 176728 Zeilen belegen dieselbe Aussage wie ein paar Dutzend. Die Probe nimmt
je Familie, Saat und Code einen Vertreter und paart ihn mit einem Mangel auf einem anderen Feld,
der allein `MALFORMED_CBOR` erzeugt. Gemessen sind das 85 Fälle, und es gibt keine Kombination
ohne Partner.

**Beschluss 3 — Klasse drei wird nur auf der ersten Stufe ausgewertet.** Zwei verschiedene
Ablehnungen nebeneinander sind der Fall, den `01 §B.2` ausdrücklich freistellt; D299 hat daraus
zwölf Nichtbefunde erzeugt. Annahme gegen Ablehnung bleibt aussagekräftig, verschiedener Code
nicht. Die Klasse wird gefahren, weil sie billig ist, aber ihre zweite Stufe erzeugt keinen Befund.

**Beschluss 4 — Kombinationen aus drei Mängeln bleiben zurückgestellt**, bis Stufe 2 einen Befund
erzeugt hat. Das Verhältnis von Zeilen zu Beobachtungen ist schon bei Paaren das Thema; bei
Tripeln wächst es um zwei Größenordnungen, ohne dass eine neue Art von Aussage entsteht.

**Beschluss 5 — Familie C geht nicht in die Paarbildung ein.** D303 Beschluss 2 schliesst sie aus,
und der Grund gilt hier unverändert.

**Verworfen: die vollständige Aufzählung.** Zweiundachtzig Prozent der Menge liegen in Klasse vier
und belegen nur, dass der Vorrang hält.

**Verworfen: eine gezogene Stichprobe mit festem Startwert.** Sie ist nicht stabil gegen
Änderungen der Einzelmenge — jeder neue Operator verschiebt sie —, und ihre Nachvollziehbarkeit
hängt an einem Implementierungsdetail statt an einer benannten Regel. Die Vorrangprobe leistet
dasselbe und lässt sich in einem Satz beschreiben.

**Die Zahlen sind Prototypzahlen** im Sinne von D298. Der Zuschnitt entscheidet sie, nicht die
Reichweite; die gelieferte Fassung wird bei der Abnahme gemessen.

**Was der Zuschnitt voraussetzt.** Die Klassifikation nach dem Einzelverdikt stammt aus der
Referenzfassung. Sie wählt die Testmenge aus und fällt kein Urteil; das Urteil fällt danach im
Vergleich. Tragfähig ist sie nur, solange Stufe 1 befundfrei ist: sähe eine zweite Fassung einen
Einzelmangel anders als die Referenz, landete sein Paar womöglich in Klasse vier und käme nie zum
Lauf. Genau dieser Unterschied wäre aber bereits auf Stufe 1 sichtbar, und dort ist er gemessen —
D299 nennt null Befunde. Fällt auf Stufe 1 je ein Befund an, wird dieser Zuschnitt neu bewertet,
bevor Stufe 2 erneut läuft.

---

### D306 — Berichtigung von D305: Klassenschnitt, Vorrangprobe und doppelte Drahtfolgen

**Anlass.** Der Lauf zu D305 hat gestoppt und drei Abweichungen gemeldet, statt sie aufzulösen.
Zwei davon sind Fehler des Registereintrags, die dritte ist eine Lücke des Prompts. Alle drei sind
nachgemessen worden, bevor hier entschieden wird.

**Berichtigung 1 — die Zahlen zu Klasse zwei und vier in D305 sind falsch.** Sie stammen aus einer
Zählung, die ein Paar aus einer Annahme und einem `MALFORMED_CBOR` zu Klasse zwei schlug. Der
Beschlusstext von D305 verlangt das Gegenteil: ausgegeben wird, wobei **keiner** der beiden
Einzelmängel allein `MALFORMED_CBOR` erzeugt. Richtig sind 4382 in Klasse zwei und 199749 in
Klasse vier; die ausgegebene Menge ist 16943 statt 39964. Der Beschluss selbst bleibt unverändert
gültig, ebenso die Zahlen 216692, 2125 und 10436. Die Zahl 16943 stand bereits in der ersten
Messung zu D305 und ist beim zweiten Schnitt unbemerkt verlorengegangen — der Fehler liegt beim
Supervisor, nicht am Lauf.

**Berichtigung 2 — die Vorrangprobe endet nicht durchweg in `MALFORMED_CBOR`.** Von den 85
Fällen tragen zwölf den Code `UNSUPPORTED_VERSION`, nämlich genau die, deren nicht-strukturellen
Partner die Version betrifft. Das ist kein Mangel der Probe, sondern der Inhalt von `01 §B.2`:
wird eine Version nicht unterstützt, werden Pflichtfelder, Keys und Längen nicht mehr
gegen `01 §2` geprüft, und `MALFORMED_CBOR` behauptete dort einen Mangel, den erst die v1-Tabelle
setzt. Der Code wäre der falsche Satz.

**Beschluss — die Erwartung wird abgeleitet, nicht gesetzt.** Eine Zeile der Vorrangprobe wird
abgelehnt mit `UNSUPPORTED_VERSION`, wenn einer ihrer beiden Einzelmängel allein diesen Code
erzeugt, und sonst mit `MALFORMED_CBOR`. Die zwölf Zeilen bleiben in der Menge. Sie
herauszunehmen hiesse, den einzigen Fall zu entfernen, in dem die Probe eine Verschachtelung
prüft statt einer flachen Regel.

**Was diese Regel riskiert, und warum das erwünscht ist.** Sie gilt, weil die gewählten Partner
ihren Mangel aus der Feldtabelle beziehen. Ein struktureller Mangel — nicht dekodierbar, doppelter
Key, Nicht-uint-Schlüssel, oberste Ebene keine Map — bliebe auch unter fremder Version wahr und
ergäbe `MALFORMED_CBOR`. Träfe die Partnerwahl je einen solchen, würde der Test rot. Das ist
gewollt: die Regel ist scharf, und ihr Bruch wäre ein Befund über die Vorrangordnung, kein
Testfehler. Angepasst wird sie dann nicht stillschweigend, sondern hier.

**Beschluss — doppelte Drahtfolgen.** Zwei verschiedene Saaten können denselben Paarmutanten
ergeben; gemessen sind 70 solche Fälle. Es gilt dieselbe Regel wie im Gitter: die in der stabilen
Reihenfolge spätere Zeile wird verworfen. Damit die Vorrangprobe davon nie getroffen wird, steht
sie in der Reihenfolge **vor** den Klassen eins bis drei.

**Gemessen und bestätigt.** Alle 2438 Einzelmutanten der Familien A und B unterscheiden sich von
ihrer Saat in genau einem Schlüssel; es gibt keine nicht paarbaren. Die Zahl 85 für die
Vorrangprobe und das Fehlen jeder Lücke bestätigen sich ebenso.

---

### D307 — Abnahme der Stufe 2; die Deduplikation lässt die Klassenzuordnung wohldefiniert

**Abnahme.** Beide neuen Dateien wurden aus dem Diff rekonstruiert und gefahren. Die Blob-Hashes
`6f1d875` und `2357a0e` treffen die Indexzeilen; die gemessene Fassung ist byteweise die gelieferte
(Prüfregel 59). 16958 Zeilen, davon 85 in der Vorrangprobe, 2059 in Klasse eins, 4378 in Klasse
zwei und 10436 in Klasse drei; 70 Doppelte verworfen, keine nicht paarbaren Einzelmutanten.
`tools/gitter.py` ist unberührt, fünfzehn Tests in beiden Dateien grün.

**Bestätigt: die zwölf aus D306.** Die Vorrangprobe endet 73 mal in `MALFORMED_CBOR` und 12 mal in
`UNSUPPORTED_VERSION`. Die abgeleitete Erwartung hält, und kein Partner hat einen strukturellen
Mangel getragen, der die Regel gebrochen hätte.

**Neu gemessen: die Deduplikation ist gefahrlos.** Weder der Prompt noch der Bericht haben
geprüft, was passiert, wenn dieselbe Bytefolge aus zwei Quellen entsteht. Gemessen sind 68 solcher
Bytefolgen, die 70 Verwerfungen auslösen; zwei entstehen dreifach. Alle 68 laufen über
Saatgrenzen, **keine** über Klassengrenzen. Damit bleibt die Klasse einer Zeile wohldefiniert.
Entstünde je eine Bytefolge einmal als Paar zweier Annahmen und einmal als Paar aus Annahme und
Ablehnung, hinge ihr Etikett an der Iterationsreihenfolge, und die Auswertung würde eine Zahl
melden, die kein Text festlegt. Das ist heute nicht der Fall und wird bei einer Erweiterung der
Operatorenmenge erneut gemessen.

**Extern geprüft, im Bestand ungeprüft.** Für jede der 16873 Klassenzeilen wurde die Klasse aus
den beiden Einzelverdikten nachgerechnet; keine einzige weicht ab. Ein Test dafür fehlt.
`tests/test_paare.py` prüft die Bauart, die Eindeutigkeit, die Nichtleere jeder Klasse und das
Verdikt der Vorrangprobe — nicht aber, dass ein Etikett `P1` zwei angenommene Einzelmängel meint.
Das ist ein benannter Rückstand, kein Fehler der Lieferung: der Prompt hat den Test nicht verlangt.

**Befund: `tools/paare.py` importiert fünf private Namen aus `tools/gitter.py`.** Der Prompt hatte
erlaubt, eine Hilfsfunktion öffentlich zu machen; der Lauf hat stattdessen `_SEED_NAMES`,
`_SIG_KEY`, `_author_sk`, `_clone` und `_sign_a` mit Unterstrich importiert. Ein Unterstrich sagt
aus, dass an einem Namen nichts hängt, und diese Aussage ist jetzt falsch.

**Beschluss: angenommen, ohne Nachlauf.** Ein Bruch dieser Kopplung erzeugt einen `ImportError`
und ist damit laut, nicht still; das ist der Fall, für den D183 und die Werkzeugschicht die
niedrigere Schwelle vorsehen. Die Gegenmassnahme müsste ausgerechnet die Datei anfassen, deren
Unberührtheit das Abnahmekriterium war. Wird `tools/gitter.py` das nächste Mal aus einem anderen
Grund geändert, werden die fünf Namen dabei geöffnet.

**Was jetzt fehlt.** Die Menge steht, der Vergleich nicht. Stufe 2 ist erst gefahren, wenn die
Go-Fassung dieselben 16958 Zeilen beurteilt hat und beide Ausgaben nach D299 zweistufig
ausgewertet sind.

---

### D308 — Ergebnis der Stufe 2; eine Konvergenz ohne normative Grundlage

**Der Lauf.** 16958 Paarmutanten, beiden Fassungen über dieselbe Hexdatei vorgelegt, Vergleich
ausserhalb des Repos (D293). Stufe eins der Auswertung nach D299: **null Abweichungen**. Über die
ganze Menge sind sich beide Fassungen einig, ob angenommen oder abgelehnt wird, und bei jeder
Annahme über die `claim_id`.

**Stufe zwei: 512 verschiedene Codes, kein Befund.** Sie zerfallen in zwei Muster, in denen die
Referenz `BAD_SIGNATURE` meldet und die Zweitfassung etwas anderes. Beide sind nachgemessen: bei
allen 224 Zeilen mit `INVALID_GENESIS_ANCHOR` trägt `h_prev` tatsächlich 32 Nullbytes, bei allen
288 mit `INCOHERENT_EXPIRY` gilt tatsächlich `t ≥ t_exp` auf einem Prädikat ausserhalb von
`core/*`. Und `BAD_SIGNATURE` ist ebenfalls wahr: keine der 5343 so beurteilten Zeilen trägt eine
gültige Signatur. Zwei wahre Sätze, freie Wahl nach `01 §B.2`, keine normierte Prüfreihenfolge.
Prüfregel 61 greift, und das Ergebnis ist derselbe Nichtbefund wie in D299 — diesmal in einem Zug
erkannt statt in zweien.

**Was der Lauf tatsächlich gefunden hat.** Von 1095 Zeilen mit wahrer Expiry-Inkohärenz zeigt die
Zweitfassung bei 486 auf sie und meldet sonst einen anderen wahren Code; darunter 120 mal
`UNSUPPORTED_VERSION`. Das führte auf die Frage, was eine fremde Version verdrängt — und dort
liegt eine Lücke im Text.

**Gemessen.** Die Referenz meldet bei `version` ungleich 1 **nie** einen Code, dessen Aussage eine
Feldbedeutung aus `01 §2` voraussetzt: über 242 Einzelmutanten 66 mal `UNSUPPORTED_VERSION` und
176 mal `MALFORMED_CBOR`, über 3490 Paarmutanten 3417 und 73. Die Zweitfassung tut in den
fraglichen Zeilen dasselbe. Die Übereinstimmung ist vollständig.

**Der Befund: sie ist nicht begründet.** `01 §B.2` nimmt unter der Überschrift zur Feldtabelle nur
Pflichtfelder, Keys und Längen aus und begründet das damit, dass `MALFORMED_CBOR` dort einen
Mangel behauptete, den erst die v1-Tabelle setzt. Dieselbe Begründung trägt für
`INCOHERENT_EXPIRY`, `INVALID_GENESIS_ANCHOR`, `BAD_SCOPE_BINDING`, `UNKNOWN_NAMESPACE`,
`INVALID_PREDICATE`, `RESERVED_CORE_PREDICATE`, `UNKNOWN_J_TAG` und `BAD_SIGNATURE` — gesagt wird
sie für keinen davon. Zwei unabhängige Fassungen tun übereinstimmend etwas, das der Text nicht
verlangt.

**Beschluss — der Absatz wird ergänzt.** Unter fremder Version trägt eine Bytefolge keinen Code,
dessen Aussage eine Feldbedeutung aus `01 §2` voraussetzt; strukturelle Mängel bleiben unberührt,
weil sie an keiner Version hängen. Das ist keine Verhaltensänderung, sondern der fehlende Satz zu
einem Verhalten, das beide Fassungen bereits zeigen.

**Warum das ein Fund ist und keine Formalie.** Eine Übereinstimmung zweier Fassungen belegt nichts
über die Spec, wenn der Text den Punkt nicht festlegt — das ist Prüfregel 61 in der
Gegenrichtung. Eine dritte Fassung dürfte hier abweichen, ohne unrecht zu haben, und die
Kampagne hätte den Unterschied dann als Befund gemeldet, obwohl er keiner wäre. Genau dafür wird
verglichen.

**Was daneben liegt.** 3490 der 16958 Paarmutanten tragen eine fremde Version und messen damit im
Wesentlichen nur die Versionsprüfung. Für einen künftigen Zuschnitt ist das ein Posten: ein
Fünftel der Menge trägt eine Beobachtung. Ausserdem bleibt die neue Norm ungeprüft, solange kein
Test sie an das Gitter bindet; das ist ein benannter Rückstand.

**Nachtrag: die Ausnahme setzt eine lesbare Version voraus.** Die Nullprobe zum Einschub hat 176
Einzelmutanten gefunden, die eine von 1 verschiedene `version` tragen und dennoch
`MALFORMED_CBOR` erhalten. Sie widerlegen den neuen Satz nicht, sie schärfen ihn: bei allen 176
ist das Feld gar nicht als uint lesbar — Bytes, Text, Array, Map, Bool, Null, Float, Tag, ein
negativer Integer, oder das Feld fehlt. Nur 66 Mutanten tragen eine als uint lesbare fremde
Version, und die erhalten sämtlich `UNSUPPORTED_VERSION`. Die Trennung ist vollständig und ohne
Ausnahme.

**Warum das im Text stehen muss.** Ohne diesen Satz liesse sich ein fehlendes Versionsfeld als
nicht unterstützte Version lesen, und dann wäre `UNSUPPORTED_VERSION` der Code — mit der Folge,
dass die Feldtabelle nicht mehr prüfbar wäre und 176 Zeilen ihr Verdikt umdrehten. Die Referenz
entscheidet es seit je richtig; der Text trug es nicht. Ein zweiter Fund derselben Art wie D308
selbst, aus der Nullprobe zu dessen eigener Ergänzung.

**Der Rückstand ist geschlossen.** `test_foreign_version_requires_a_readable_uint` in
`tests/test_gitter.py` bindet beide Sätze an die Mutantenmenge: von 2502 Zeilen tragen 2260 die
Version 1, 66 eine lesbar fremde Version und erhalten sämtlich `UNSUPPORTED_VERSION`, und 176
tragen keine lesbare Version und erhalten sämtlich `MALFORMED_CBOR`. Der uint-Begriff steht als
`type(wert) is int` im Test, nicht als `isinstance`, sonst ginge ein `True` im Versionsfeld als
Version 1 durch (D272). Beide Rücknahmeproben greifen am Verifizierer an und machen je eine der
beiden Gruppen rot.

---

### D309 — Die drei Rückstände aus `00al`: Klassentest, Namensöffnung, Schritt 26 auf 27

**Anlass.** D307 hat zwei Rückstände benannt und D304 einen dritten. Alle drei sind klein, benannt
und voneinander unabhängig; keiner ändert das Verhalten des Verifizierers. Sie werden in einem Lauf
erledigt, weil der dritte `tools/gitter.py` ohnehin anfasst und D307 die Öffnung der fünf Namen
genau daran geknüpft hat.

**Beschluss 1 — der Klassentest leitet die Klasse aus den beiden Einzelverdikten ab.** D307 hat für
alle Klassenzeilen extern nachgerechnet, dass das Etikett `P1`, `P2` oder `P3` zur Klasse passt;
ein Test dafür fehlt. Er wird in `tests/test_paare.py` ergänzt und formuliert die Regel aus D305
und D306 neu: Klasse eins, wenn beide Einzelmängel angenommen werden; Klasse zwei, wenn genau
einer; Klasse drei sonst. Zusätzlich prüft er, dass keine Klassenzeile einen Einzelmangel trägt,
der allein `MALFORMED_CBOR` erzeugt — das ist die Aussage, die den Schnitt aus D306 Berichtigung 1
trägt, und sie stand bisher in keinem Test.

**Die Regel wird nicht importiert.** Ein Test, der die Klassenfunktion aus `tools/paare.py` holt,
prüft sie gegen sich selbst. Die Einzelverdikte kommen aus `tools/verdikt.py`, die Rückführung des
Paaretiketts auf seine beiden Einzeletiketten aus der Hilfe, die
`test_vorrangprobe_verdict_is_derived_from_the_two_singles` bereits benutzt.

**Beschluss 2 — die fünf Namen werden umbenannt, nicht aliasiert.** `_SEED_NAMES`, `_SIG_KEY`,
`_author_sk`, `_clone` und `_sign_a` verlieren den Unterstrich; alle Verwendungsstellen in
`tools/gitter.py` und `tools/paare.py` ziehen mit. Ein öffentliches Alias neben dem privaten Namen
liesse beide am Leben und sagte damit weniger als jeder von beiden.

**Die gleichnamigen Kopien in den Testdateien bleiben.** `tests/test_gitter.py` und
`tests/test_paare.py` führen `_SEED_NAMES`, `_SIG_KEY` und `_author_sk` je eigen. Das ist kein
Rückstand, sondern Absicht: ein Test, der seine Erwartung aus dem Prüfling importiert, prüft
nichts.

**Beschluss 3 — der Kopfverbreiterer erhält den Schritt von Additional Information 26 auf 27.**
Damit greift `feldkopf_breiter` auch auf `t` und `t_exp`, die beide vierbytige Köpfe tragen. Der
Ertrag ist eine Kodierungsform auf zwei Feldern, die bisher keine trug; die Erreichbarkeit der
Reject-Codes wächst nicht, und das war schon in D304 der Grund für die Zurückstellung. Sie wird
jetzt aufgehoben, weil die Datei ohnehin geöffnet wird.

**Beschluss 4 — die neuen Zeilen bekommen einen Träger.** Bisher verlangt kein Test, welche Felder
`feldkopf_breiter` erreicht; der Operatorentest verlangt nur, dass es überhaupt eine Zeile je
Operator gibt. Ein Test in `tests/test_gitter.py` leitet die erwartete Etikettmenge aus den
Saatbytes ab: ein Feld ist erreichbar genau dann, wenn der Kopf seines Wertes einen anderen Major
als sieben und eine Additional Information kleiner als 27 trägt. Ohne diesen Träger wäre der
Schritt aus Beschluss 3 nicht rücknehmbar prüfbar, und nach Prüfregel 62 darf die Rücknahme die
Menge nicht leeren, über die der rote Test quantifiziert — hier bleibt sie es nicht.

**Berichtigung von D304 — es sind neun Zeilen, nicht zwölf.** D304 nennt zwölf und rechnet damit
sechs Saaten mal zwei Felder. `t_exp` ist nach `01 §2` optional und steht nur in TV1, TV5 und TV6;
`t` ist Pflichtfeld und steht in allen sechs. Sechs plus drei ergibt neun. Die Zahl ist gemessen
und keine Prototypzahl im Sinne von D298: sie folgt aus der Saatmenge und hat keinen
Freiheitsgrad.

**Was daneben liegt.** D308 nennt 2260 Zeilen mit Version 1 bei 2502 Zeilen der Stufe 1. Die neuen
Zeilen tragen sämtlich Version 1, also verschiebt sich die erste Zahl. Der Eintrag bleibt
unverändert; er beschreibt den Stand, an dem er gemessen wurde. Der Test dazu trägt keine getippte
Zahl und bleibt gültig. Die Menge der Stufe 2 ist unberührt, weil Familie C nach D305 Beschluss 5
nicht in die Paarbildung eingeht.

**Verworfen: eine eigene Familie D für den breiteren Kopf.** Der Operator ist derselbe, nur eine
Stufe weiter; eine zweite Familie hätte die Etiketten gespalten, ohne eine andere Art von Mangel
zu erzeugen.

**Verworfen: die fünf Namen über ein öffentliches Alias zu führen.** Der Unterstrich sagt aus, dass
an einem Namen nichts hängt. Steht daneben ein zweiter Name ohne Unterstrich, sagt keiner von
beiden noch etwas.

---

### D310 — Abnahme der drei Rückstände; die Berichtigung von D304 bestätigt sich

**Abnahme.** Die gelieferte Fassung wurde aus dem Diff rekonstruiert und gefahren, nicht aus dem
Bericht übernommen. Vier Blob-Hashes treffen die Indexzeilen auf beiden Seiten: `fd9ab52` auf
`7638778` für `tools/gitter.py`, `6f1d875` auf `285890c` für `tools/paare.py`, `60a3a28` auf
`3ffbc34` für `tests/test_gitter.py`, `2357a0e` auf `e85189a` für `tests/test_paare.py`. Die
Ausgangshashes sind dieselben, die D304 und D307 genannt haben; damit steht auch die Basis
(Prüfregel 59).

**Gemessen.** 789 Tests grün. Das Gitter liefert 2511 Zeilen, davon 1174 in Familie A, 1264 in B
und 73 in C. Der Operator `feldkopf_breiter` trägt 49 Zeilen: zehn auf TV1, je acht auf TV2, TV4,
TV5 und TV6, sieben auf TV3. Nach Schlüssel sind es je sechs auf 0, 1, 2, 3, 6, 8 und 9, drei auf
5 und 7, eine auf 4. Die Stufe 2 ist unberührt: 16958 Zeilen, 85 in der Vorrangprobe, 2059, 4378
und 10436 in den drei Klassen.

**Die Berichtigung aus D309 hält.** Neu sind genau neun Zeilen, sechs auf Schlüssel 6 und drei auf
Schlüssel 7. Alle fünf Mengenzahlen waren vor dem Lauf unabhängig gerechnet und wurden dem Prompt
vorenthalten; sie treffen ohne Abweichung.

**Beide Rücknahmeproben nachgefahren, nicht geglaubt** (Prüfregel 60). Ohne den Schritt von 26 auf
27 wird `test_feldkopf_breiter_labels_match_reachable_value_heads` rot, und die übrigen elf Tests
der Datei bleiben grün, darunter der Operatorentest; die Erwartungsmenge behält 49 Elemente, die
gemessene fällt auf 40, keine von beiden ist leer. Mit vertauschten Klassennummern eins und zwei
wird `test_class_prefix_matches_the_two_single_verdicts` rot, und beide Klassen bleiben nichtleer.
Nach dem Zurücksetzen stimmen die Blob-Hashes wieder — die Proben haben nichts hinterlassen.

**Was der neue Klassentest zusätzlich trägt.** Er prüft nicht nur die Zuordnung, sondern auch, dass
keine Klassenzeile einen Einzelmangel trägt, der allein `MALFORMED_CBOR` erzeugt. Das ist der
Schnitt aus D306 Berichtigung 1, und er stand bis hierher in keinem Test.

**Angenommen ohne Nachlauf.** Der Docstring von `tools/paare.py` nennt D309 nicht, obwohl die Datei
geändert wurde; die Änderung ist rein mechanisch und trägt keine eigene normative Grundlage. Der
Importblock derselben Datei ist seit der Umbenennung nicht mehr alphabetisch — `sign_a` steht
hinter `mutant_lines` —, weil der Unterstrich vorher vor den Buchstaben sortierte. Der Linter
beanstandet es nicht; wird die Sortierregel je eingeschaltet, ist das die erste Stelle, die
auffällt.

**Was daneben liegt.** Die drei Posten aus `00al` sind erledigt und fallen aus der offenen Liste.
Die Erreichbarkeit der Reject-Codes ist unverändert: elf der zwölf über das Gitter,
`FOREIGN_LIFECYCLE` weiterhin nicht (D263, D268). Die Zahlen in D304, D307 und D308 beschreiben
weiterhin den Stand, an dem sie gemessen wurden, und werden nicht nachgezogen.

---

### D311 — Moduswechsel in den Anwendungsabschnitt; drei Befunde vor der ersten Prototypzeile

**Anlass.** Layer 01 ist ausgelesen. Über 2511 Einzel- und 16958 Paarmutanten hat kein einziger
Verdikt-Unterschied einen Befund getragen; die beiden Funde aus D308 kamen aus dem Nachdenken über
eine Übereinstimmung und aus einer Nullprobe, nicht aus der Kampagne. Weitere Verifikationsarbeit
an derselben Achse erzeugt gerechtfertigte Arbeit ohne Ertrag. Die Frage, die das Projekt trägt,
ist eine andere: ob sich gegenseitige Absicherung ohne Machtmonopol abbilden lässt. Sie wird beim
Fahren beantwortet, nicht beim Prüfen.

**Beschluss 1 — Prototypmodus für den Anwendungsabschnitt.** Szenarioskripte sind Wegwerfcode. Für
sie gelten **nicht**: Registerpflicht für den Code, Golden Numbers, Rücknahmeproben,
Zweitimplementierung, Abnahme gegen einen Prompt-Commit. Es gelten **weiter**: die Spec als
normative Wahrheit, das Register als oberste Instanz, die Zitiergrammatik, und dass eine Messung
eine Position ändern können muss. Ins Register wandert aus einem Prototyplauf ausschliesslich der
**Befund**: die Stelle, an der die Spec keine Antwort hatte, eine falsche gab, oder eine erzwang,
die ein Zentrum voraussetzt. Der Prototyp erzeugt Befunde, keine Normen.

**Der Grund für die Trennung.** Der Anspruch des Projekts gilt der Spec und den Befunden. Gilt er
auch dem Prototyp, entsteht dieselbe Schleife wie in der Kampagne: jede Runde einwandfrei, der
Ertrag gegen null. Ein Prototyp, der die Registerschwelle nehmen muss, wird nicht gebaut.

**Beschluss 2 — das erste Szenario ist zweiphasig.** Gegenseitige Absicherung unter vier
Beteiligten, in einem Durchlauf zweimal versucht: einmal als Fonds mit einem gewählten Verwahrer,
einmal als Umlage ohne Verwahrer. Der Kontrast ist die Messung, nicht der einzelne Durchlauf. Eine
Phase allein zeigt nur, dass es geht oder nicht geht; beide nebeneinander zeigen, **woran** es
hängt.

**Befund 1 — Obligationen sind bilateral, ein Topf braucht einen Verwahrer.** `settlement` in
`03 §3.3.2` verlangt ein Identity-Subjekt und nimmt nur eine Quittung des Gläubigers an. Es gibt
keine Form, sich gegenüber einer Gruppe zu verpflichten. Wer Beiträge sammelt, ist eine benannte
Person, und das Protokoll kann feststellen, dass sie nicht auszahlt, aber nichts erzwingen. Das
ist keine Lücke, sondern die Konsequenz aus L3: es gibt keinen Ort, an dem Wert liegt.

**Befund 2 — Abstimmungen gibt es nur über Verfassungen.** Ein Vorschlag nach `04 §2.4` besteht
aus Scope, Vorgängerepoche und Verfassungshash. Über einen Sachverhalt kann in `04` nicht
abgestimmt werden. Ob eine Auszahlungsentscheidung deshalb als Verfassungsänderung zu modellieren
ist, ob sie gar keine kollektive Entscheidung sein soll, oder ob `04` einen Mechanismus vermissen
lässt, ist offen und wird vom Szenario beantwortet, nicht hier.

**Befund 3 — der Kettenrückhalt ist persistent, der Claimspeicher nicht.** `DateiRueckhalt`
schreibt Spitze und Redo atomar auf Platte; der `Ausgang` ist bisher nur ein Adapter über
`InMemoryStore`. Für vier getrennte Verzeichnisse fehlt ein dateibasierter Ausgang und ein Leser
dazu. Das sind zwei Methoden und gehört nach Beschluss 1 in das Szenarioskript, nicht nach
`mensch_als_republik/`.

**Was der erste Durchlauf beantworten soll.** Ist der Zustand aus jedem der vier Verzeichnisse
heraus gleich ablesbar, ohne dass einer mehr weiss als die anderen? Und an welcher Stelle musste
etwas erfunden werden, das die Spec nicht hergibt?

**Verworfen: eine dritte Implementierung als nächster Schritt.** D308 liefert das Argument dafür,
und der Anker aus D302 stünde bereit. Aber eine dritte Fassung prüft dieselbe Achse wie die
Kampagne, und die hat gemessen nichts geliefert. Sie bleibt möglich, wenn der Anwendungsabschnitt
Fragen an `01` zurückwirft.

**Verworfen: Kombinationen aus drei Mängeln.** D305 Beschluss 4 stellt sie zurück, solange Stufe 2
keinen Befund erzeugt hat. Sie hat keinen erzeugt.

---

### D312 — Abnahme des ersten Prototyplaufs; zwei Fehler im Prompt und was Stufe A beantwortet hat

**Abnahme.** Der Lauf hat geliefert, was D311 verlangt: einen Durchlauf in zwei Phasen und eine
Befundliste. Vierzehn Befunde, keine Erfindung, um eine Phase zu retten. Geprüft wurde nach dem
Modus aus D311 nicht der Code gegen den Bericht, sondern die Befunde gegen die Spec.

**Erster Fehler im Prompt — `00 §4.2` wurde nicht konsultiert.** Der Prompt ordnete einen Nukleus
an und Obligationen in demselben Scope. `00 §4.2` sagt, dass Vouches, Obligationen und Quittungen
**nicht** in den Scope gehören, dessen `participants` abgestimmt werden. Das ist Prüfregel 38 in
ihrer einfachsten Form, und sie wurde übergangen. Der Lauf hat es als Befund gemeldet.

**Das verändert die Gewichtung des ersten Befunds.** Dass eine Auszahlung keine kollektive
Entscheidung ist, ist keine Lücke in `04`. `00 §4.2` sagt es bereits: sich verpflichten und
quittieren sind zweiseitige Akte ohne Kollektivbeschluss. Das Szenario hat damit nicht eine
fehlende Norm gefunden, sondern eine bestätigt, die niemand nachgeschlagen hatte.

**Zweiter Fehler im Prompt — der Bestand wurde nicht gemessen.** Unter `tools/sim/` liegt ein
Simulationsrahmen mit getrennten Beobachtern, getrennten Uhren und getrennten Schlüsseln, einem
Verzeichnis je Teilnehmer samt Inbox, deklarativen Szenarien in JSON mit den Schritten `claim`,
`zustellen`, `uhr`, `zeige` und `erwarte`, sechs bestehenden Szenarien und einer Testdatei. Der
Prompt liess davon einen erheblichen Teil neu bauen. Das Werkzeug hat den Rahmen gefunden, seine
Inbox-Konvention benannt und trotzdem eine zweite erfunden, weil der Prompt es verlangte — es hat
gemeldet statt eigenmächtig umzubauen, und damit richtig gehandelt.

**Daraus Prüfregel 63.** Vor einem Prompt, der etwas bauen lässt, wird gemessen, ob es das schon
gibt. Der Griff davor ist nicht Prüfregel 38, die auf die Spec zeigt, sondern ein Blick in den
Baum.

**Was Stufe A beantwortet hat.** Die Verpflichtungsschicht trägt, und sie trägt für alle vier
gleich: nach ausdrücklicher Verteilung liegt in jedem Verzeichnis derselbe Bestand, und jeder
rechnet dieselben Tilgungszustände. Das Wiederlesen aus den Verzeichnissen ändert nichts. Damit
ist die Frage aus D311 beantwortet, aber mit einer Bedingung: die Gleichheit ist eine Eigenschaft
der Verteilung, nicht von `settlement`. Das Protokoll erzwingt die Kopie nicht.

**Und was sie nicht trägt.** Es gibt kein Gruppen-Soll. Drei bilaterale Obligationen an dieselbe
Person sind drei Obligationen, nicht ein Anspruch gegen eine Gemeinschaft. Es gibt keine
Verwahrerrolle, kein Prädikat für den Versicherungsfall, keine Deckung und keine Summe. Eine
Versicherung im gewohnten Sinn ist damit nicht abbildbar; abbildbar ist die Buchung, nicht die
Institution.

**Der zweitwichtigste Befund ist die Ununterscheidbarkeit.** `OPEN` heisst zugleich "quittiert
nicht" und "Quittung noch nicht angekommen". Das ist die bekannte Grenze verteilter Systeme, und
das Protokoll erbt sie. Sie begrenzt, was Reputation aus Nichtleistung ableiten darf — wer aus
`OPEN` auf Unwilligkeit schliesst, verwechselt Partition mit Absicht.

**Ungenau im Bericht.** Der Befund, der Fall habe kein Prädikat, gilt nur für ein Profil eines
Versicherungsfalls. `accusation@1` existiert und ist nach D67 vollständig opak; es hätte den Fall
tragen können. Der Prompt hatte den Verdikt-Cluster ausgeschlossen, die Anklage aber nicht
ausdrücklich.

**Nachtrag zu den Prüfregeln.** Die Herkunftsliste endet bei 61 aus D299; Regel 62 aus D304 wurde
nie eingetragen. Mit diesem Eintrag kommen 62 und 63 hinzu.

**Für Stufe B.** Zwei Scopes statt einem, nach `00 §4.2`: die Substanz ohne `participants`, die
Governance getrennt. Und der Rahmen ist `tools/sim/`, nicht `tools/szenario_absicherung.py`. Die
Frage, die Stufe B stellt: kann ein Gruppen-Soll aus bilateralen Akten entstehen, wenn jeder für
sich prüft, ob eine Zusage gedeckt ist? Dafür liegt `02 §8` bereit.

**Verworfen: `tools/szenario_absicherung.py` zu verwerfen.** Es ist Wegwerfcode nach D311 und hat
seinen Zweck erfüllt. Es bleibt als Gegenstand des Befundberichts im Baum und wird nicht
fortgeschrieben.

---

### D313 — Zwei Vorarbeiten zur Risikoteilung, und wohin eine Versicherung gehört

**Anlass.** D312 formulierte als Frage für Stufe B, ob ein Gruppen-Soll aus bilateralen Akten
entstehen kann, wenn jeder Beobachter für sich prüft, ob eine Zusage gedeckt ist. Die Frage ist
ausserhalb von MaR seit Jahrzehnten bearbeitet, theoretisch wie praktisch. Dazu kam die Frage, ob
eine Versicherung überhaupt der richtige Gegenstand ist oder schon eine Anwendung.

**Befund 1 — die theoretische Grenze ist ein Schnitt.** Ambrus, Mobius und Szeidl modellieren
informelle Versicherung in sozialen Netzwerken, in denen Beziehungen als soziale Sicherheit
dienen, um Zahlungen durchzusetzen. Ihr Ergebnis: der erreichbare Versicherungsgrad wird von der
Expansivität des Netzes bestimmt, gemessen an der Zahl der Verbindungen, die eine Gruppe zum Rest
der Gemeinschaft hat, im Verhältnis zu ihrer Grösse. Das ist eine Aussage über Schnitte, und ein
Schnitt ist die Grösse, die `02` über Max-Flow ohnehin rechnet. Ihr zweites Ergebnis lautet, dass
Versicherung lokal ist: innerhalb endogen entstehender Gruppen vollständig, zwischen ihnen
unvollständig. Das ist L2 in ökonomischer Sprache. Quelle: American Economic Review 104(1), 2014,
Seiten 149 bis 182.

**Warum das zählt.** Die theoretische Obergrenze gegenseitiger Absicherung und die Grösse, die
Layer 02 berechnet, sind dieselbe. Das ist der erste Beleg von aussen dafür, dass Trust-Flow in
MaR nicht Zierrat ist, sondern der Ort, an dem Deckung gemessen würde.

**Befund 2 — ein dritter Weg neben Fonds und Umlage.** Teambrella hat gegenseitige Versicherung
gebaut, ohne einen Topf zu bilden. Jedes Guthaben gehört einem Mitglied und ist zugleich unter
geteilter Verfügung: eine Zahlung verlangt die Unterschrift des Versicherten und mehrerer
halbzufällig bestimmter Mitglieder, sodass weder der Einzelne noch die Gruppe allein verfügt.
Niemand haftet über das hinaus, was er selbst hinterlegt hat, und was jemand einlegt, ist zugleich
der Höchstbetrag, den andere für ihn tragen. Quelle: Whitepaper von Paperno, Kravchuk und
Porubaev, 2016; die verfügbaren Berichte reichen bis 2021, der heutige Zustand des Projekts wurde
nicht gemessen.

**Was daran nicht auf MaR passt.** Die Durchsetzung ist Mittelsperrung: wer seinen Anteil nicht
zeichnet, verliert Zugriff auf das eigene Guthaben. Das verlangt eine Kette, die
Mehrfachunterschriften auflöst, und eine Stelle, die die Mitzeichnerlisten führt. MaR hat weder
das eine noch das andere; seine Mittel sind Ausschluss und Vertrauensentzug. Ausserdem stimmt
Teambrella kollektiv über den Schadensfall ab — genau das, was `00 §4.2` für Substanz ablehnt. Und
die Reziprozitätsregel ist eine Aussage über Beträge, die `03 §3.1` dem Protokoll verwehrt.

**Klärung — es gibt drei Orte, nicht zwei.** `08 §3` fragt, ob ein Mechanismus die Kosten der
Feststellung senkt oder Macht verteilt, und weist ihn danach Protokoll oder Policy zu. Der
Schlussabsatz desselben Abschnitts nennt einen dritten: ein Werkzeug, das Claims erzeugt und
einliest, und eine Wertschicht, die es nicht gibt.

**Eine Versicherung ist keiner dieser drei, sondern eine Zusammensetzung aus allen.** Profile für
Verpflichtung, Quittung und Verdikt aus dem Protokoll; Schwellen und Arbitratorenliste aus der
Policy; die Zahlungen aus der Wertschicht; die Oberfläche aus dem Werkzeug. Als Erzeugnis ist sie
Anwendung, und Prämien und Deckungssummen gehören nicht in das Protokoll.

**Das Szenario baut sie nicht, es belastet die Übergänge.** Es prüft, welche Zahnräder eine
Versicherung braucht und welche davon vorhanden sind. Das ist Protokollarbeit, und `08 §3`
verlangt selbst, die Prüftabelle bei jedem neuen Mechanismus fortzuschreiben. Die Grenze hält, so
lange keine Zahl in den Protokollpfad gerät; in `00an` hat das gehalten, und der Bericht wies die
Summen getrennt aus.

**Beschluss — Stufe B beginnt als Spec-Arbeit, nicht als Lauf.** Die drei Befunde ohne Ort aus
D312 werden durch das Aufnahmekriterium geschickt und als Zeilen in die Tabelle von `08 §3`
eingetragen: das Gruppen-Soll, die Verwahrerrolle, das Prädikat für den Fall. Erst danach lohnt
ein weiterer Durchlauf, und dann mit der Frage, ob Vertrauensentzug als Durchsetzung reicht, wo
Teambrella Mittelsperrung braucht.

**Keine Zuordnung wird hier vorweggenommen.** Die Vermutung lautet, dass ein Gruppen-Soll Macht
verteilt und deshalb nicht ins Protokoll gehört, dass die Verwahrerrolle Policy ist, und dass
`accusation@1` den Fall bereits trägt. Vermutungen sind keine Einträge; die Begründung entsteht
beim Eintragen, nicht davor.

**Verworfen: die Wertschicht jetzt zu füllen.** Sie ist nach `08 §3` ein benannter und
ausdrücklich leerer Empfänger, kein Versäumnis. Eine Anbindung an ein Inhaberinstrument nach
`03 §3.2` bliebe zudem an einem Verwahrer hängen — an einem Betreiber, an einer Gruppe von
Treuhändern oder an einem Hersteller gesicherter Hardware. Für die Frage, ob Absicherung ohne
Machtstelle möglich ist, liefert keine dieser Formen eine neue Antwort.

---

### D314 — Das Wurzelverzeichnis bekommt eine Bindungsregel und ein Archiv

**Anlass.** Das Wurzelverzeichnis trägt 128 Markdown-Dateien. Davon sind 28 normativ oder werden
zitiert; die übrigen 100 sind Prompts, Abnahmen und Übergabedateien abgeschlossener Läufe. Für den
Supervisor ist das billig, weil gezielt gegriffen wird. Für ein Werkzeug, das im
Anwendungsabschnitt einen Auftrag bekommt, ist es nicht billig: es sieht 128 Dateien und kann
nicht erkennen, welche gelten. D312 hat gezeigt, was das kostet, wenn schon der Prompt den Bestand
nicht gemessen hat.

**Nicht der Anlass ist die Grösse.** D225 hat die Sorge um die Kopiengrösse ausdrücklich
zurückgenommen, und der Anteil des Registers hat sich seither um einen Prozentpunkt bewegt. Es
geht um Lesbarkeit des Baums, nicht um Platz. Das Register bleibt, wo es ist.

**Beschluss 1 — es bindet nur ein Paragraphenverweis.** Eine Datei bleibt im Wurzelverzeichnis,
wenn eine Wurzeldatei oder eine Python-Datei sie in der Form `NAME §X` nennt. Eine blosse
namentliche Nennung bindet **nicht**. Sonst nagelte jede Erwähnung im Register eine Datei für
immer fest, und es würde nie aufgeräumt. Der Preis ist, dass eine im Register genannte Datei nach
dem Verschieben einen Ordner tiefer liegt; der Pfad ist mit `archiv/` vorhersagbar, und die
Prüfung nach D229 fasst Nennungen ohne Paragraphen ohnehin nicht an.

**Beschluss 2 — dazu eine feste Liste.** Gebunden sind ausserdem alle Einträge aus `LAYER_FILES`,
das Regelwerk, `README.md`, `VISION.md`, `werkzeuge.md`, `example-nucleus.md`, die beiden
Ankerdateien zu `02` und `03`, und die jeweils aktuelle Übergabedatei. Ohne diese Liste fielen
Dateien heraus, auf die niemand mit Paragraphen zeigt, weil sie selbst der Einstieg sind.

**Beschluss 3 — Verschieben, nicht Löschen.** Ziel ist `archiv/`. `tools/check_specs.py` glob't
die Wurzel und steigt nicht ab; damit fallen die verschobenen Dateien aus der Prüfung. Das ist für
Historie richtig und für normativen Text falsch, und genau darum trennt Beschluss 1. Verweise in
archivierten Dateien dürfen von da an verrotten.

**Beschluss 4 — die Prüfung meldet, sie blockiert nicht.** `check_specs` nennt am Ende, wie viele
Wurzeldateien gebunden sind und welche Kandidaten fürs Archiv wären. Eine harte Prüfung würde bei
jedem neuen Prompt sofort scheitern, weil auf ihn beim Anlegen noch kein Paragraphenverweis zeigt;
das wäre Zeremonie je Lauf ohne Ertrag. Eine Zahl am Ende genügt, damit die Wurzel nicht in zehn
Sitzungen wieder zuwächst.

**Was daneben liegt.** Die Kandidatenliste umfasst auch Dateien, die offene Posten tragen — etwa
die Anhangsform-Datei aus D232 mit ihren fünf zu hohen Zeilenangaben. Der Posten bleibt offen, die
Datei liegt danach unter `archiv/`. Das ist beabsichtigt: ein offener Posten wird im Register
geführt, nicht durch den Ort einer Datei.

**Verworfen: eine Teilung des Registers nach Ären.** D225 hat sie mit Begründung zurückgestellt,
und es ist seither kein Engpass entstanden. Das Register wird über `tools/register_index.py`
gelesen, nicht am Stück.

**Verworfen: Löschen statt Verschieben.** Git hält die Dateien ohnehin, aber ein Pfad, den man
tippen kann, ist billiger zu finden als ein Commit, den man suchen muss.

---

### D315 — Abnahme des Archivlaufs; die Bindungsregel im Prompt war nicht idempotent

**Abnahme.** Der Lauf hat geliefert, was D314 verlangt: die Regel als Funktion, die Meldung ohne
Fehlschlag, 104 Umbenennungen nach `archiv/` bei voller Ähnlichkeit, und danach null ungebundene
Wurzeldateien. `make check` bleibt bei 789 Tests.

**Die Golden Numbers wichen ab, und der Fehler lag im Prompt.** Erwartet waren 28 gebundene
Dateien, gemessen wurden 27. Der Nenner erklärt sich aus drei Prompt-Dateien, die seit der
Vorabmessung entstanden sind. Der Zähler nicht: die eine Datei ist `einlesen-a-abnahme.md`.

**Sie hing an einer Quelle, die selbst ins Archiv gehörte.** Nur
`einlesen-a-nachlauf-prompt.md` nennt sie mit Abschnitt, und auf diese Datei zeigt niemand. Der
Prompt verlangte, dass eine beliebige Wurzeldatei binde; das Werkzeug hat daraus gemacht, dass nur
eine **gebundene** Quelle bindet, und bis zum Fixpunkt gerechnet. Nachgerechnet: mit der Fassung
des Prompts hält der erste Durchgang 28 Dateien, der zweite 27, und die herausfallende ist genau
diese. Ein Aufräumen, das beim nächsten Mal wieder etwas findet, und eine Zahl, die nichts sagt.

**Das ist Scope-Zuwachs, und er war richtig.** Er wurde gemeldet, begründet und ist zwingend: ohne
den Fixpunkt ist die Regel nicht stabil. Ein Werkzeug, das die Lücke schliesst und es sagt, tut
mehr für die Sache als eines, das den Prompt wörtlich befolgt. Daraus Prüfregel 64.

**Was daneben liegt.** Der Prompt dieses Laufs ist im selben Commit mit ins Archiv gewandert; er
beschreibt einen abgeschlossenen Lauf und ist damit am richtigen Ort. Die Sammelfunktion für
Python-Quellen steigt weiterhin unter `archiv/` ab; dort liegt keine Python-Datei, der Punkt ist
folgenlos und wird nicht nachgezogen. Ein Teil des Diffs ist Umformatierung bestehender Funktionen
durch den Formatierer, kein Semantikwechsel.

**Der Bestand danach.** 27 Markdown-Dateien im Wurzelverzeichnis, 104 unter `archiv/`. Die
verschobenen Dateien werden nicht mehr auf Zeilenlänge, Escapes und Verweise geprüft; ihre
Verweise dürfen von hier an verrotten (D314 Beschluss 3).

### D316 — Die Übergabedatei zerfällt; die offene Liste wird nummeriert

**Kontext.** Die Übergabedatei war ein Monolith, der zu jedem Sitzungsbeginn vollständig in den
Kontext ging und jedes Mal neu geschrieben wurde. D218 nennt das monolithische Rewrite seit
mehreren Sitzungen als offenen Posten. Der Preis fällt doppelt an: einmal als Kontext, einmal
als Abtippen einer Liste, von der sich pro Sitzung ein oder zwei Posten ändern.

**Beschluss 1.** Die offene Liste steht in `offen.md`, mit nummerierten Posten `O1` bis `On`. Sie
wird **fortgeschrieben, nicht neu geschrieben**. Nummern werden nie wiederverwendet; ein
geschlossener Posten bleibt als Zeile stehen, mit dem Registereintrag, der ihn geschlossen hat.
Zählvorschrift: `grep -c '^### O' offen.md`.

**Beschluss 2.** Die stabile Disziplin steht in `arbeitsweise.md`: Rollen, Arbeitsbogen,
Prototypmodus, Risiko-Tiers, Shell, Messvorschriften, Splices, Zitiergrammatik. Sie wird selten
angefasst und geht nicht in jede Sitzung. `pruefregeln.md` bleibt der Volltext der Regeln;
`arbeitsweise.md` sagt, wann man dorthin greift. Die Datei `sitzungsstart-*.md` trägt nur noch
Stand, letzte Entscheidungen und nächsten Schritt.

**Beschluss 3.** Das Werkzeug misst, läuft, liest Diffs vor und macht mechanische Refactorings.
Der Supervisor bekommt **Zahlen und Befunde, keine Dateiinhalte**. Eine Datei wird nur gelesen,
wenn eine benannte Entscheidung von ihrem Inhalt abhängt — dann aber vollständig, und vor dem
Prompt. Das ändert die **Messung**, nicht die Abnahme: die Abnahme bleibt beim Supervisor und
bleibt am Diff (Prüfregel 56).

**Beschluss 4.** Die Projektkopie `/tmp/mar-context.xml` wird gezogen, wenn ein Nachbau ansteht,
nicht als Reflex. Für die Frage, ob etwas irgendwo steht, reicht ein `grep` mit wenigen Zeilen
Ausgabe.

**Begründung.** Der Engpass dieser Arbeit ist nicht die Rechenzeit, sondern der Kontext pro
Sitzung. Die drei Posten oben sind die drei grössten Einzelposten, und keiner von ihnen trägt
zur Prüfbarkeit bei. Was der Prüfbarkeit dient — Register, Prüfregeln, Zitiergrammatik,
Abnahme am Diff — bleibt unverändert.

**Was das schliesst.** Der Posten aus D218 zum monolithischen Rewrite ist damit erledigt. Der
zweite Posten aus D218, dass es keine Kontextdatei für das Werkzeug gibt, bleibt offen und steht
als `O47` in `offen.md`: `arbeitsweise.md` ist für den Supervisor geschrieben, nicht für das
Werkzeug.

**Was das nicht ist.** Kein Beschluss über die Sprache und keiner über den Umfang der Spec. Die
Layer-Dateien sind unberührt.

### D317 — Der Repositoriumsname wird `symbolon`; umbenannt wird später

**Kontext.** `mensch-als-republik` ist als Verzeichnis-, Paket- und Repositoriumsname zu lang und
im englischsprachigen Raum nicht sprechbar. Für eine Öffnung nach aussen braucht das Projekt
einen kurzen Namen. Der **Titel** der Spec bleibt davon unberührt.

**Messung, 4. September 2026.** Zwei Kandidaten wurden gegen PyPI, npm, crates.io, RubyGems und
die GitHub-Repositoriumssuche gehalten.

`symbolon`: auf PyPI belegt durch ein Paket der Version 0.1.0 aus fremdem Fach (ein Dashboard für
Token-Verbrauch); npm, crates.io und RubyGems frei; 19 gleichnamige GitHub-Repositorien, das
grösste mit neun Sternen, ein Universitätsprojekt zu symbolic execution.

`ostracon`: auf PyPI, crates.io und RubyGems frei; auf npm belegt durch ein Werkzeug zur
Rekonstruktion von Entscheidungshistorie aus Git-Historie; auf GitHub belegt durch
`Finschia/ostracon` mit siebzig Sternen, **ein Konsensalgorithmus, geforkt von Tendermint Core**.

**Beschluss.** Der Name ist `symbolon`. Das griechische Objekt ist die in zwei Hälften gebrochene
Marke; die Hälften weisen sich aus, indem sie zusammenpassen. Das ist `08 §2.2`: Aussagen sind
überprüfbar, weil sie kollidieren können, nicht weil sie signiert sind.

**Begründung für die Ablehnung von `ostracon`.** Die Kollision liegt im selben Fach. Ein
Konsensalgorithmus im Feld dezentraler Protokolle ist genau die Verwechslung, die ein Name
verhindern soll. `symbolon` kollidiert nur mit einem 0.1.0-Paket fremden Fachs und mit keinem
Projekt von Gewicht.

**Was das nicht ist.** Kein Beschluss zur Ausführung. Umbenannt wird nichts, bevor die Öffnung
steht; der Posten ist `O55`. Der PyPI-Name bleibt belegt und ist `O56`; Ausweichnamen wären
`symbolon-protocol` oder `mar`, und die Frage stellt sich erst bei einer Veröffentlichung.

**Der Titel bleibt.** Die Spec heisst weiter *Mensch als Republik*. `08` trägt ihn, und er sagt,
worum es geht. Ein Repositoriumsname benennt nicht den Gegenstand.

### D318 — Der Kopf der Projektkopie trägt sechs Zahlen (D224, D316)

**Abnahme des Laufs `00aq-werkzeuge`.** Drei Aufträge, alle geliefert. Die Bindungsmeldung nennt
weder die beiden neuen Einstiegsdateien noch die aktuelle Übergabedatei; der zweite Lauf liefert
dieselbe Menge wie der erste (Prüfregel 64). Beide Rücknahmeproben zu `tools/offen.py` wurden
vom Supervisor selbst gefahren und waren rot. Die Erwartung des Supervisors an die Bindungszahl
war um eins zu hoch und in sich falsch, bevor sie gemessen wurde; der Lauf hat genau die drei
Dateien gebunden, die zu binden waren.

**Ein Defekt, vor dem Merge behoben.** Der Ausdruck, mit dem `tools/offen.py` Nennungen von
Postennummern findet, hatte keinen Schutz gegen Wortmitten. Ein grosser Buchstabe O unmittelbar
vor einer Ziffernfolge wurde auch dann als Nennung gelesen, wenn er Teil einer Normbezeichnung
oder einer Summenformel war. Das Vorbild `tools/register_index.py` trägt den Schutz seit D209;
der Prompt hat es als Vorbild benannt, aber die Eigenschaft nicht verlangt.

Der Fehler ist in beide Richtungen scharf. Eine erfundene Zahl aus einer Wortmitte, die zufällig
keinen Posten trifft, blockiert `make check` für alle. Eine, die zufällig einen trifft, wird
stillschweigend angenommen. Seit diesem Lauf sitzt der Prüfer in `make check`, also blockiert die
erste Richtung jeden Commit.

**Die Nebenwirkung ist derselbe Fall wie D210.** Ein Registereintrag, der den Defekt an einem
Beispiel beschreibt, löst ihn aus: `tools/offen.py` liest `07-decisions.md` mit. Dieser Eintrag
nennt die Beispiele deshalb in Worten. Nach der Behebung wäre das nicht mehr nötig, aber die
Umschreibung bleibt, weil sie ohnehin lesbarer ist.

**Beschluss: der Kopf trägt sechs Zahlen.** Commit, Testzahl, Registerstand, Prüfregelzahl,
**Postenzahl**, Branchzahl. D224 Teil 2 nannte fünf; die Postenzahl kommt hinzu, weil D316 die
offene Liste zu einer fortgeschriebenen Datei gemacht hat und eine verlorene Fortschreibung sonst
unbemerkt bleibt.

**Nicht aufgenommen: die Zahl der Markdown-Dateien der Wurzel.** Eine Kaltzahl ist eine Zahl,
deren Abweichung eine Entscheidung ändert. Die Branchzahl deckt einen nicht gemergten Lauf auf,
die Postenzahl eine verlorene Fortschreibung. Die Zahl der Wurzeldateien ändert sich mit jeder
Prompt-Datei und trägt keine Entscheidung; sie bleibt über `check_specs.py` abrufbar, wo sie
neben der Bindungsmeldung steht und dort auch hingehört.

**Was das nicht ist.** Keine Änderung an D224 Teil 1 und Teil 3: Ziel bleibt `/tmp`, und der
Wächter, der gepackte gegen versionierte Dateien zählt, bleibt unberührt.

**Eine Beobachtung zum Prompt, nicht zum Lauf.** Der Prompt verlangte für die Nummern
"lückenlos aufsteigend"; gebaut wurde Mengensemantik ohne Reihenfolge, und das Werkzeug hat die
Abweichung gemeldet. Die Abweichung ist besser als der Auftrag. Sobald ein neuer Posten
thematisch in eine frühere Gruppe gehört, steht seine Nummer mitten in der Datei; eine
Reihenfolgeprüfung wäre dann falsch. Die Nummern sind Identität, nicht Position. Der Prompt
war ungenau, der Bau ist richtig, und nichts wird nachgezogen.

### D319 — Zwei Lizenzen: Apache-2.0 für den Code, CC-BY-4.0 für den Text

**Der Anlass.** Die Öffnung braucht eine Lizenz; ohne sie ist die Bezeichnung als offenes
Projekt eine Behauptung. Förderlinien verlangen, dass Software vollständig unter einer
anerkannten freien Lizenz veröffentlicht wird.

**Es sind zwei Entscheidungen, nicht eine.** MaR besteht aus Code und aus Text, und der Text ist
der grössere Teil: neun Layer-Dateien, dreihundert Registereinträge, vierundsechzig
Prüfregeln. Eine Codelizenz auf Prosa ist eine Kategorienverwechslung; sie regelt Quelltext und
Objektcode und sagt über ein Spezifikationsdokument nichts.

**Beschluss 1: der Code steht unter Apache-2.0.** Drei Gründe, nach Gewicht.

Erstens die Patentklausel. Ein Protokoll besteht aus Verfahren, und Verfahren ziehen
Patentansprüche an. Apache-2.0 gewährt eine ausdrückliche Patentlizenz und entzieht sie jedem,
der wegen Patenten klagt. Die MIT-Lizenz hat dazu nichts.

Zweitens der Beitragsabschnitt. Apache-2.0 regelt, unter welchen Bedingungen ein fremder Beitrag
hereinkommt. Damit braucht das Projekt **kein** CLA, und ein Beitrag von aussen kostet keinen
Vertrag.

Drittens die Anerkennung: die Lizenz ist bei jeder Distribution und jeder Förderlinie ohne
Rückfrage durch.

**Beschluss 2: Spec, Register und Prüfregeln stehen unter CC-BY-4.0.** Namensnennung, sonst
nichts. Ein Protokoll will maximal ungehindert implementierbar sein. Steht die Spec unter
Copyleft, wird eine unabhängige Zweitimplementierung juristisch heikel — und das ist die
stärkste Prüfmethode, die dieses Projekt hat (D302).

Nicht CC-BY-SA, weil die Weitergabeklausel bei abgeleiteten Spezifikationen dieselbe Reibung
erzeugt. Nicht CC0, weil die Namensnennung zählt: das Register ist der Beleg der Methode.

**Gegen Copyleft am Code, ausdrücklich.** Die naheliegende Wahl wäre die AGPL: ein Protokoll
gegen Machtkonzentration, also eine Lizenz gegen Vereinnahmung. Sie ist trotzdem falsch. Die
Netzwerkklausel richtet sich gegen gehostete Dienste; MaR ist ein Peer-Protokoll, dort greift sie
kaum. Was sie sehr wohl tut, ist Reimplementierer abzuschrecken — und damit besteuert sie genau
das Verfahren, das in diesem Projekt funktioniert hat.

**Was die Lizenz nicht leistet.** Sie verhindert keinen kustodialen Fork. Dagegen hilft
Markenrecht, nicht Urheberrecht, und eine Marke wird nicht angemeldet. Das ist ein benannter,
angenommener Verlust. Was einen kustodialen Umbau strukturell verhindert, steht in `03 §3.1` und
im Fehlen einer Verwahrerrolle: das Protokoll kann den Betrag nicht lesen. Das ist die Sorte
Durchsetzung, die MaR baut.

**Gegen eine ethische Quelllizenz, ausdrücklich.** Reticulum stellt sein Protokoll gemeinfrei
und lizenziert die Referenzimplementierung unter selbstgeschriebenen Zusatzbedingungen. Der
Schnitt ist derselbe wie hier und war die Anregung; die Zusatzbedingungen sind die Warnung. Eine
Beschränkung nach Anwendungsfeld ist nicht quelloffen im Sinne der Open Source Definition,
erzeugt Inkompatibilität mit anderen Lizenzen, und verlagert eine strukturelle Frage ins
Urheberrecht, wo sie nur so weit trägt, wie jemand zu klagen bereit ist. Das ist dieselbe
Konstruktion, die dieses Projekt an Zentren kritisiert.

**Mechanik.** `LICENSE` trägt den Apache-Text, `LICENSE-SPEC` den CC-BY-Text, beide ohne
Dateiendung, damit sie nicht in die Menge der Wurzel-Markdown-Dateien fallen. Die README erklärt
die Zweiteilung. Das Urheberrecht bleibt beim Autor; ohne CLA lässt sich später nichts
relizenzieren, sobald fremde Beiträge eingegangen sind, und das ist beabsichtigt.

**Eine Messung nebenbei.** Die Linie, die in einer früheren Runde als Ziel genannt wurde, hat
ihren letzten Aufruf im Juni 2026 geschlossen. Welche Linie heute passt, ist zu messen, bevor ein
Antrag geschrieben wird. Der Lizenzbeschluss hängt davon nicht ab.

### D320 — Das Übergabeverfahren wird aufgeschrieben

**Der Anlass war eine Frage.** Wo die Übergabedateien liegen und wie die Übergabe funktioniert,
stand nirgends. Das Verfahren lief seit Dutzenden Sitzungen aus Gewohnheit. Das ist genau die
Sorte Wissen, gegen die dieses Projekt sonst anschreibt: eine Regel, die gilt, weil sich jemand
an sie erinnert.

**Beschluss 1: die Datei heisst nach der Sitzung, die sie schreibt.** `sitzungsstart-00aq.md` ist
von Sitzung `00aq` verfasst und eröffnet Sitzung `00ar`. Sie nennt den Stand **vor** ihrer
eigenen Übergabe; der Übergabe-Commit selbst steht nicht mehr darin. Wer den Kopf abschreibt
statt ihn zu messen, liegt deshalb regelmässig um einen Commit daneben (Prüfregel 40).

**Beschluss 2: die Suffixe laufen einstellig, dann zweistellig.** Von `00a` bis `00z`, dann
`00aa` fort. Die jüngste Datei ist die mit dem längeren Namensteil; bei gleicher Länge die
alphabetisch spätere. Das ist die Regel, die `latest_handoff` in `tools/check_specs.py` seit
D318 ausführt, und sie steht jetzt auch in Worten.

**Beschluss 3: zu Sitzungsbeginn gehen zwei Dinge in den Kontext.** Die dauerhafte Anweisung und
die jüngste Übergabedatei. Sonst nichts. `arbeitsweise.md`, `offen.md` und `pruefregeln.md`
liegen im Repositorium und werden geholt, wenn eine Entscheidung an ihnen hängt — nicht als
Reflex (D316 Beschluss 3 und 4).

**Beschluss 4: der erste Zug ist die Kaltmessung.** Die Übergabedatei ist eine Hypothese, keine
Messung. Ihre Zahlen werden gemessen. In dieser Sitzung wich der Stand um einen Commit ab, und
die Abweichung war die Datei, nicht das Repositorium.

**Beschluss 5: die Bindungsmeldung ist die Erinnerung ans Archivieren.** Gebunden wird nur die
jüngste Übergabedatei; jede ältere erscheint als ungebunden. Diese Zeile ist kein Mangel,
sondern der Auftrag, sie wegzuräumen. Der Rückstand betrug zuletzt drei Sitzungen.

**Ausdrücklich nicht gebaut: ein zweiter Prüfer.** Erwogen war ein Abgleich zwischen dem
Präfix des jüngsten Commits und der jüngsten Übergabedatei. Er misst dasselbe wie die
Bindungsmeldung und schlüge bei jedem Commit an, der keine Übergabe ist. Zwei Prüfer auf
denselben Gegenstand sind keine doppelte Sicherheit, sondern ein zweiter Ort, an dem eine Regel
driften kann.

**Die benannte Grenze.** Es gibt kein erzwungenes Verfahren, das sicherstellt, dass eine
Übergabedatei überhaupt geschrieben wurde. Fällt sie aus, startet die nächste Sitzung blind
und ist auf die Projektkopie und die Suche in alten Gesprächen angewiesen. Beides ist
schwächer. Mechanisch schliessen lässt sich die Lücke nicht, weil eine Sitzung im
Repositorium kein Gegenstand ist.
### D321 — O58: mar-go wird per `filter-repo` + Merge zu `go/`, nicht per `git subtree`

**Der Anlass.** O58 nennt zwei Kandidaten offen: `git subtree` oder ein Merge mit
`--allow-unrelated-histories` nach `git filter-repo --to-subdirectory-filter`. Beide erhalten
die Historie; die Wahl war offen.

**Entscheidung.** `git filter-repo` auf einem Wegwerf-Klon von `~/mar-go`, danach Merge mit
`--allow-unrelated-histories` in den Hauptbaum. Nicht `git subtree`.

**Begründung.** `git subtree` ist ein Contrib-Kommando, dessen Verfügbarkeit auf diesem System
ungeprüft war. `git filter-repo` war für diesen Lauf ohnehin zu installieren und arbeitet auf
einem Klon, der das Original unter `~/mar-go` nie berührt — ein Fehlschlag kostet nur das
Wegwerfverzeichnis, nicht das Quellrepositorium. Das Ergebnis ist mechanisch gleichwertig: fünf
Commits, Nachrichten, Autoren und Zeitstempel erhalten, referenzierbar unter `go/`. Die Hashes
ändern sich zwangsläufig, weil sich der Baum jedes Commits ändert; das gilt für `subtree`
ebenso.

**Golden Number.** `~/mar-go` trug fünf Commits (`719905d` bis `4ec54cd`, Erstcommit „start:
Auftrag und beschnittene Spec"). Nach dem Merge müssen exakt fünf Commits unter `go/`
auffindbar sein.

**Geprüft, nicht angenommen.** `tools/check_specs.py` liest Wurzel-Markdown nicht-rekursiv
(`ROOT.glob("*.md")`). Dateien unter `go/`, etwa `go/AUFTRAG.md`, fallen nicht in die
Bindungs- oder Zitatprüfung. Der Umzug bindet keine neue Datei und bricht keine bestehende
Prüfung.

**Nicht-Ziel.** Ob das eigenständige Gitea-Repositorium `mar-go` danach archiviert,
umbenannt oder stillgelegt wird, ist hier nicht entschieden. Das bleibt ein offener Posten.
### D322 — Projektkopie: `07-decisions.md` aus der Repomix-Packung ausgeschlossen

**Der Anlass.** Die Datei trug zuletzt 217.870 Tokens, 21,5 % der gepackten Kopie, bei
unverändertem Inhalt seit Sitzungen. Das ist Overhead: kein Kontextfenster braucht das
komplette Register, wenn eine Entscheidung nur einzelne Einträge betrifft.

**Entscheidung.** `repomix.config.json` trägt `ignore.customPatterns: ["07-decisions.md"]`.
Die Datei bleibt im Repositorium vollständig erhalten; nur die gepackte Kopie lässt sie aus,
auch aus der Verzeichnisstruktur.

**Was das nicht ändert.** `tools/register_index.py` und `grep` bleiben der Weg zu einzelnen
Einträgen (Prüfregel 38); eine Entscheidung wird gezielt angefordert, wenn ihr genauer
Wortlaut gebraucht wird (Prüfregel 27). Kein Werkzeug, das direkt auf `07-decisions.md`
zeigt (`stand.py`, `register_index.py`, `splice_run.py`), ist betroffen — sie lesen die
Datei selbst, nicht die Kopie.
### D323 — O57 neu gemessen: NGI Zero endet, Nachfolger „Open Internet Stack", `Restack` passt

**Der Anlass.** D319 verwies auf eine spätere Neumessung, weil der zuvor gemeinte Fonds seinen
letzten Aufruf im Juni 2026 geschlossen hatte. Die Messung war offen; hier ist sie nachgeholt,
mit Quellen, Stand 5. September 2026.

**Befund.** Der gemeinte Fonds ist der NGI Zero Commons Fund von NLnet. Sein dreizehnter und
letzter Aufruf schloss am 1. Juni 2026; NLnet pausierte danach alle offenen Aufrufe, um „NGI
Zero" nach zehn Jahren abzuschließen. Seit 3. September 2026 laufen die Aufrufe unter neuem
Namen weiter: „Open Internet Stack", mit drei Programmen — `Restack`, `CodeSupply`, `ELFA`.
Der Kadenz-Wechsel gehört zur Umstellung dazu: Frist neu am dritten statt am ersten Tag, und
in ungeraden statt geraden Monaten. Nächste Frist: **3. November 2026**.

**Passung.** `Restack` trägt die Formulierung „P2P infrastructure" und „internet commons
across the entire technology stack" — das deckt sich eng mit MaR als Koordinationsprotokoll.
`CodeSupply` und `ELFA` liegen näher bei Local-First-Anwendungen bzw. Software-Supply-Chain,
nicht bei einem Konsensprotokoll selbst. `Restack` ist die Empfehlung.

**Bedingungen unverändert passend.** 5.000–50.000 € pro Vorhaben, offen für Einzelpersonen,
Pflicht zur Veröffentlichung unter freier Lizenz — bereits erfüllt durch D319.

**Was offen bleibt.** O57 setzt O52 und O53 voraus (öffentlicher Spiegel, englische Schale);
ohne beides gibt es nichts, worauf ein Antrag verweisen könnte. Diese Messung beantwortet nur,
welche Linie passt und wann die nächste Frist liegt — nicht, ob rechtzeitig vor dem 3.
November beide Vorarbeiten stehen.

**Quellen.** nlnet.nl/commonsfund/, nlnet.nl/news/2026/20260612-NGIZero-stocktaking.html,
nlnet.nl/news/2026/20260803-phaseshift.html, nlnet.nl/restack/, nlnet.nl/propose/.
### D324 — Zitierfehler „08 §2.2 verlangt vier Menschen" gefunden und korrigiert

**Der Befund.** In über zwanzig Prompt-Dateien wiederholt sich wortgleich: „08 §2.2 verlangt
vier Menschen mit einem echten gemeinsamen Anliegen." `08 §2.2` behandelt aber Equivocation
(„Widersprüche werden unbestreitbar, nicht unmöglich"), nicht Anwendungsbedingungen. Die
eigentliche Quelle ist D237, und selbst dort steht keine Zahl — nur „Menschen mit einem echten
gemeinsamen Anliegen", unbezifferte Mehrzahl.

**Wie es entstand.** Vermutlich ein Prompt-Abschluss, über viele Sitzungen kopiert und nie
gegen die Spec geprüft (Prüfregel 27, Prüfregel 38). Wo genau „vier" hinzukam, ist nicht mehr
rekonstruierbar — die Zahl steht in keiner gefundenen Quelle vor der ersten Wiederholung.

**Korrektur.** `README.md` und `CONTRIBUTING.md` zitieren jetzt D237 statt `08 §2.2` und nennen
keine Zahl. Die alten Prompt-Dateien im Wurzelverzeichnis bleiben unverändert — Altlast, kein
aktiver Text, ihre Korrektur ist keinen eigenen Posten wert.

**Was offen bleibt.** Ob „vier" irgendwann bewusst entschieden wurde und nur nie einen eigenen
Registereintrag bekam, lässt sich nicht ausschließen. Ohne Beleg gilt die unbezifferte Fassung
aus D237 als maßgeblich.
### D325 — Direkter Spiegel-Zugriff ersetzt die Repomix-Pflicht

**Der Anlass.** Seit O52 ist `github.com/olisym/mensch-als-republik` ein öffentlicher,
synchron gehaltener Spiegel. Der Supervisor kann ihn im eigenen Sandbox klonen und lesen, ohne
dass Oli etwas einfügt oder Repomix laufen lässt.

**Entscheidung.** `arbeitsweise.md` beschreibt jetzt den direkten Klon/Pull als den Weg, auf
dem der Supervisor Dateien holt, wenn eine Entscheidung von ihrem Inhalt abhängt. Repomix wird
kein Pflichtschritt mehr; es bleibt ein optionales Werkzeug für Token-Diagnosen, wie es D322
schon einmal genutzt hat.

**Die Sicherung.** Vor jedem Lesen aus dem Klon steht ein Hash-Abgleich: der geklonte `HEAD`
muss den von Oli gemeldeten Commit tragen. Weicht er ab, wird neu gepullt, nicht einfach
gelesen — der Spiegel ist ausdrücklich nicht die primäre Quelle, Gitea bleibt es (O52). Die
Kaltmessung selbst — Testzahl, Registerstand — bleibt bei Oli; sie hängt an einem echten
`pytest`-Lauf, den der Supervisor nicht nachstellen kann.

**Was das nicht ändert.** Die Zwei-Dinge-Regel aus Abschnitt 10 (dauerhafte Anweisung, jüngste
Übergabedatei) bleibt bestehen. Ob die Übergabedatei künftig ebenfalls aus dem Klon gelesen
statt eingefügt wird, ist eine offene Frage, keine hier getroffene Entscheidung.

### D326 — Externe Analyse bestätigt D234–D236; ein Ausweg wiederholt sich (O31, O59)

**Anlass.** Eine unabhängig erstellte vergleichende Analyse („Removing Hostile Authorities
without Center, Court, or Consensus") stellt exakt die Frage aus D236 noch einmal: wie entfernen
Systeme ohne Zentrale, Gericht und Konsens einen feindlichen Träger einer Autoritätsliste. Sie
kennt D234–D236 nicht und kam unabhängig zum selben negativen Kernergebnis.

**Was sich deckt, ohne neuen Ertrag.** MLS/RFC 9420, SPKI/SDSI/RFC 2693, Stellar/SCP, Mastodon-
Defederation, Steem→Hive, PBFT/BFT-SMaRt und Kuznetsov/Tonkikh (arXiv 2005.13499) stehen bereits
namentlich in der Tabelle von D236, mit denselben Preisen. Das ist Redundanz, keine Bestätigung
zweiter Ordnung — dieselben Primärquellen, zweimal gelesen.

**Ein bereits verworfener Ausweg, unabhängig wiederholt.** Die Analyse empfiehlt als Stufe 2
einen Nachfolge-/Tombstone-Mechanismus (neues Verfassungsobjekt übernimmt alle Teilnehmer außer
dem Feindlichen). Das ist wortgleich der Vorschlag, den D236 unter „Berichtigung eines
vorgeschlagenen Auswegs" bereits geprüft und verworfen hat: er umgeht die Blockade nicht, solange
der Nachfolgebeschluss derselben Auszählung unterliegt — nur ein Nachfolger **ohne jeden
Beschluss** (also: Exit/Genesis, D236 Punkt 3) umgeht sie strukturell. Die Analyse benennt diesen
Vorbehalt selbst nicht; er gilt unverändert.

**Neu, und was er trägt.**
- Buchanan/Tullock (*The Calculus of Consent*, 1962, Kap. 6–8): die U-förmige Kostenkurve
  (Externalitätskosten fallend, Entscheidungskosten steigend mit der Schwelle) ist die
  theoretische Herleitung dessen, was D235s gemessene Tabelle (kleinstes blockierendes `m` je
  Schwelle) empirisch zeigt. Stützt O31, ändert nichts an der Entscheidung.
- Schiedsfähigkeit II–IV (BGH, insb. BGHZ 180, 221): die dort verlangten Mindestbedingungen für
  bindende Schiedsklauseln (Mitwirkung aller Betroffenen an der Schiedsrichterbenennung) treffen
  auf `arbitration.arbitrators` dasselbe Bearer-Problem wie auf `participants` selbst — das
  bestätigt D236 Punkt 2 (Schlichtung als „wichtiger Grund" verworfen, zirkulär), liefert aber
  die externe Doktrin dazu, die D236 nur benannt, nicht belegt hatte.
- Vouchsafe (arXiv:2601.02254): monotone, capability-artige Widerrufsform, bei der
  Unterdrückung/Verzögerung eines Tokens Autorität nur verlängern, nie ausweiten kann. Das
  betrifft nicht `participants` (D236 bleibt unberührt), sondern die in D313 offen gelassene
  Frage, ob Vertrauensentzug (Layer 02) als Durchsetzung reicht. Bisher ungeprüft am Primärtext.

**Genauigkeitsvorbehalt (Prüfregel 27).** Die Analyse trägt selbst den Hinweis, dass die
Buchanan/Tullock-Seitenangabe und die Hirschman-Zitate aus Sekundärquellen stammen, nicht aus
verifiziertem Primärtext. Für dieses Register gilt dieselbe Regel wie in D236 für den
Recherchebericht dort: die Analyse stützt, sie trägt nicht allein. Vouchsafe, die Matrix-CVEs
(2025-49090, 2025-54315) und die Schiedsfähigkeit-Entscheidungen sind hier ebenfalls nicht am
Primärtext nachgeprüft.

**Was das für offene Posten bedeutet.** O31 bekommt eine Zeile zur theoretischen Fundierung
(Buchanan/Tullock), keine neue Entscheidung. Neuer Posten O59: Vouchsafe als mögliche Antwort auf
die D313-Frage nach Vertrauensentzug als Durchsetzung — ungeprüft, niedrige Dringlichkeit.

**Kein Lauf.** Dieser Eintrag ändert keine Spec-Datei.

### D327 — Stufe B: O1, O2 und das Fall-Prädikat durch das Aufnahmekriterium geschickt (D313)

**Anlass.** D313 hat beschlossen, dass Stufe B als Spec-Arbeit beginnt: die drei Befunde ohne Ort
aus D312 werden durch das Aufnahmekriterium aus `08 §3` geschickt und als Zeilen in dessen
Prüftabelle eingetragen.

**O1 — Gruppen-Soll.** Der Test lautet: senkt der Mechanismus Prüfkosten, oder verteilt er Macht?
Ein Gruppen-Soll bräuchte eine Regel, wer zur Gruppe zählt und wessen Nichtzustimmung die anderen
bindet — das ist Machtverteilung, keine Kostensenkung beim Feststellen, wer was gesagt hat. Die
Umlage aus bilateralen `obligation`-Claims erreicht dasselbe Ergebnis bereits mit vorhandenen
Protokollprimitiven. **Ort: kein neuer Mechanismus nötig**, Policy nur falls überhaupt gewünscht.

**O2 — Verwahrerrolle.** Eine Sammelstelle mit Auszahlungspflicht konzentriert Macht: wer über
Auszahlung entscheidet, hält die Position, die MaR sonst nirgends vergibt. `00 §4.2` verlangt
zusätzlich einen eigenen Scope, getrennt von dem, dessen `participants` abgestimmt werden. **Ort:
Policy, in einem eigenen Scope** — bestätigt die Vermutung aus `offen.md`.

**Das dritte Element aus D313 — Prädikat für den Versicherungsfall.** D312 selbst korrigiert das
unter „Ungenau im Bericht": `accusation@1` existiert bereits, ist nach D67 vollständig opak und
hätte den Fall tragen können. Das war ein Messfehler im ursprünglichen Prompt, keine Lücke im
Protokoll. **Ort: Protokoll, bereits vorhanden.**

**Was das für Stufe B insgesamt heisst.** Kein einziges der drei Elemente verlangt einen neuen
Protokollmechanismus. Eine Versicherung im gewohnten Sinn bleibt damit — wie D312 schon
feststellte — eine Zusammensetzung aus Protokoll (Obligation, Quittung, `accusation@1`), Policy
(Verwahrerscope, falls gewünscht) und Werkzeug, nicht ein fehlendes Protokollstück.

**Kein Lauf.** Dieser Eintrag ändert `08-scope.md` (Prüftabelle) und schliesst O1, O2 in
`offen.md`. Keine Code-Datei ist betroffen.

### D328 — Abnahme 00as: Vertrauensentzug ist Kostenmechanismus, nicht Durchsetzung (D313)

**Abnahme.** Der Lauf hat geliefert, was der Prompt verlangt: Baseline und Nachher-Messung für
Distanz, Kapazität, Fluss, Pfade und Tilgungszustand. Unabhängig nachgebaut (eigener Klon,
Diff angewendet, Lauf wiederholt) — identische Zahlen. `tests/test_sim.py`: 8 von 8, unverändert
gegenüber der Meldung. Gesamtsuite unverändert bei 797, `check_specs.py` sauber.

**Die Zahlen.**

| | vorher | nachher |
| --- | ---: | ---: |
| `d` (Chris, von allen vier Beobachtern gleich) | 1 | 1 |
| `C` (Chris) | 50 | 50 |
| `edges` | 4 | 3 |
| `flow` (`02 §4`) | 100 | 50 |
| `paths` (disjunkt) | 2 | 1 |
| `settlement` | OPEN | OPEN |

**D313 beantwortet: Vertrauensentzug reicht nicht als Durchsetzung, wenn Redundanz besteht.**
Anna widerruft ihren Vouch auf Chris. Distanz und Knotenkapazität (`02 §3`,
`C(x) = ⌊C₀·γ^d⌋`) ändern sich nicht — Chris bleibt über Bruno auf derselben Stufe erreichbar.
Der Max-Flow (`02 §4`) fällt auf die Hälfte, weil eine von zwei edge-disjunkten Vertrauenskanten
entfällt. Das ist eine Kostensteigerung, keine Grenze: Chris verliert Kapazität, nicht Zugang.
Die Obligation bleibt in beiden Messungen `OPEN` — Layer 02 (Vertrauen) und Layer 03
(Verpflichtung) sind entkoppelt, wie D311/D312 vermuteten, jetzt mit einem Lauf belegt.

**Die Verallgemeinerung.** Mit `n` unabhängigen, redundanten Vouch-Kanten auf denselben
Ziel-Knoten sinkt der Fluss pro Widerruf um `1/n` des ursprünglichen Werts, nicht auf null.
Das ist dieselbe Struktur wie Mastodon-Defederation oder Stellar-Slices (D236): kein
kollektiver Beschluss, sondern viele lokale Akte, die sich erst in der Aggregation zu etwas
Durchsetzungsähnlichem summieren — und selbst dann ist es Beobachtung, keine Erzwingung. Das
Protokoll zwingt niemanden zur Zahlung; es macht nur sichtbar, wie viel Vertrauen noch da ist.

**B5 — Architekturnotiz, kein Befund gegen die Spec.** `tools/example_nucleus.py::claim_set()`
baut einen Vouch-Graphen in einer eigenständigen `ExampleNucleus`-Instanz, der nicht
automatisch in eine `tools/sim`-`Welt` injiziert wird. Der Lauf hat den Graphen deshalb über
eigene Szenario-Schritte nachgebaut. Werkzeug-Merkmal, keine Protokolllücke.

**B6/B7 — Rahmenerweiterungen, dauerhaft, kein Wegwerfcode.** `_schritt_claim` kennt jetzt
`obligation` und `revoke` (`core/revoke@1`, `J=(2, claim_id(target))`, kein Scope, `01 §2.3`);
`zeige was=settlement` ist neu; `flow`/`paths` stehen jetzt in jeder `trust`-Zeile; der frühere
Druck-Bug in `_schritt_zeige` (Rückgabewert wurde verworfen) ist behoben. Bleiben mit dem Merge
im Baum, decken die sechs bestehenden Szenarien unverändert ab.

**O59 korrigiert und geschlossen.** Vouchsafe (arXiv:2601.02254, verifiziert: echtes Paper,
Jay Kuri, Ionzero Inc., Jan. 2026) beantwortet Offline-Widerruf von Capability-Tokens, nicht
wirtschaftliche Durchsetzung durch Reputationsverlust — falsche Passung zu D313. Die
tatsächliche Antwort liefert dieser Eintrag, gemessen statt aus einer Fremdquelle übernommen.

**Abschluss.** Merge von `00as-szenario-b` nach `main`. Die Prompt-Datei bindet sich über den
Verweis auf D313/D328 selbst.

### D329 — O54 entschieden: Deutsch bleibt normativ, Englisch ist keine Übersetzung

**Anlass.** O54 stellte eine Gabelung: Deutsch normativ mit driftender englischer Übersetzung,
oder Englisch normativ mit einer Zuordnungstabelle für D1 bis D315.

**Befund.** `README.md` trifft diese Entscheidung bereits, nur nie als eigener Registereintrag
festgehalten. Der Text sagt: die Arbeitssprache ist Deutsch, Spec, Register und Prozess bleiben
es; `README.md`, `CONTRIBUTING.md` und `docs/METHOD.md` sind für ein englischsprachiges
Publikum direkt verfasst, nicht aus etwas übersetzt.

**Beschluss.** Layer-Dateien, Register und Prüfregeln bleiben ausschliesslich Deutsch und
normativ. Die drei englischen Dateien sind keine Übersetzungen — eigenständiger Text ohne
Anspruch auf 1:1-Entsprechung. Damit entfällt die in O54 unterstellte Drift-Gefahr: es gibt
keine Übersetzungsbeziehung, die auseinanderlaufen könnte.

**Was das für `tools/check_specs.py` heisst.** Keine Änderung nötig. Der Linter prüft
Zitiergrammatik unabhängig von der Sprache, und die drei englischen Dateien tragen keine
`§`-Zitate, die eine Zuordnungstabelle bräuchten.

**Kein Lauf.** Dieser Eintrag ändert `offen.md` (schliesst O54), sonst nichts.

### D330 — O58 abgeschlossen: das Gitea-Repositorium `mar-go` wird archiviert

**Anlass.** D321 hat `~/mar-go` nach `go/` gemergt, aber offengelassen, was mit dem
eigenständigen Gitea-Repositorium geschieht — archivieren, umbenennen oder stilllegen.

**Beschluss.** Archivieren, nicht umbenennen oder löschen. Archivieren macht das Repositorium
schreibgeschützt, ohne Historie oder eingehende Links zu zerstören — dieselbe Haltung wie D314
gegenüber Wurzeldateien: Git hält ohnehin alles, also wird markiert, nicht gelöscht. Umbenennen
böte keinen Vorteil, da niemand mehr auf das Repositorium verweisen soll; wer es findet, soll es
als abgeschlossen erkennen, nicht als umgezogen.

**Ausführung, ausserhalb von Git.** Oli archiviert `git.h.error13.de/oli/mar-go` über die
Gitea-Weboberfläche (Repository-Einstellungen → Archive Repository). Die Beschreibung des
Repositoriums sollte auf `go/` im Hauptrepositorium verweisen, damit ein Betrachter den neuen
Ort findet.

**Kein Lauf, keine Codeänderung.** Dieser Eintrag ändert `offen.md` (schliesst O58), sonst
nichts.

### D331 — Abnahme 00at: O55 ausgeführt, `symbolon` ist Verzeichnis, Paket und Gitea-Name

**Abnahme.** Der Lauf hat geliefert, was der Prompt verlangt. Unabhängig nachgebaut (eigener
Klon, vollständiger Diff angewendet, Tests und `check_specs.py` wiederholt) — identische Zahlen:
123 Dateien, +561/−440, `archiv/`, `go/` und `07-decisions.md` unberührt, 797 Tests unverändert,
Register unverändert bei D1–D330 (dieser Lauf schrieb nicht ins Register). Eine einzelne
abweichende Beobachtung beim Nachbau (`mensch_als_republik/` blieb als leeres Verzeichnis
stehen) ist ein Artefakt von `git apply` gegenüber einem echten `git mv`-Commit, kein Befund
gegen den Lauf. `governance/__init__.py` (Löschen+Neuanlage statt Rename, Ähnlichkeit unter der
Schwelle) inhaltlich geprüft: reiner Bezeichnerwechsel, keine zusätzliche Änderung.

**Zwei Spuren, unabhängig ausgeführt.** Server-seitig (ausserhalb von Git, per Gitea-API):
`git.h.error13.de/oli/mensch-als-republik` → `oli/symbolon` umbenannt, `oli/mar-go` archiviert
(D330), lokaler `origin`-Remote umgestellt. Code-seitig (dieser Lauf, `00at-umbenennung`):
Verzeichnis, Importe, `pyproject.toml`, `Makefile`, Codepfad-Zitate in `03-profiles.md` und den
aktiven Prompt-Dateien. Bewusst **nicht** angefasst: der GitHub-Spiegel bleibt unter
`github.com/olisym/mensch-als-republik` — der Push-Mirror pusht unter dem alten Namen weiter,
das bricht nichts, und eine GitHub-Umbenennung war nie Teil dieses Laufs.

**Was noch nachzuziehen war.** `README.md` behauptete weiterhin, die Umbenennung sei „planned
but hasn't happened yet" — das war zum Zeitpunkt des Prompts richtig (Nicht-Ziel 2 schloss die
Reponame-Sätze aus diesem Lauf ausdrücklich aus), ist es nach der Server-Umbenennung nicht mehr.
Dieser Eintrag zieht den Satz nach.

**O55 abgeschlossen.**

**Kein weiterer Lauf vorgesehen.** `O56` (PyPI-Name) bleibt ein weicher Blocker, erst relevant
bei einer Veröffentlichung — unverändert, kein Teil dieses Eintrags.

---

### D332 — Fork zu Stufe C: Rechenschaft ohne Bindung, geprüft an Law Merchant und Bernstein

**Anlass.** Nach D236 (kein Ausschlussmechanismus) und der zweifachen Verwerfung von
„Schlichtung als wichtiger Grund" (D236 Punkt 2, D326) bleibt die einzige noch offene Rolle von
`03 §2` das bilaterale Verdikt zwischen zwei Parteien (Pfad ii, `§2.4`) — kein Ausschluss,
sondern Rechenschaft im Einzelfall.

**Der Fund, der die Frage schärft.** `submit-arbitration@1` ist bewusst widerrufbar (`§2.4.1`)
— anders als reale Schiedsklauseln, die unter der FAA §2 als „valid, irrevocable, and
enforceable" gelten, gerade weil ihre Durchsetzung auf der Bindung beruht. MaR scheint diese
Bindung nicht zu brauchen: `05-enforcement.md §5` sagt bereits normativ, subjektive Verdikte
reisten „als attribuierte Meinungen, deren Gewicht das Vertrauen des Beobachters in den
Schiedsrichter ist — nie eine globale Score-Änderung" — unabhängig vom
`BINDING`/`ATTRIBUTED_OPINION`-Status aus `03 §2.4`. Das ist strukturell die
Durchsetzungslogik des Law Merchant (Milgrom/North/Weingast 1990, Champagne-Messen, private
Richter ohne Staatsmacht) und der Diamantenhändler (Bernstein 1992): keine erzwingbare
Bindung, sondern Reputationsinformation, die sich in einer eng verflochtenen Gruppe verbreitet
(vgl. auch Ellickson 1991, Shasta County).

**Was das nicht ist.** Keine Bestätigungsübung wie die verworfene Ausschluss-Idee — die
Beobachtungsgewichtung ist in `05-enforcement.md` als Prinzip benannt, aber nirgends als
Formel oder Code. Offen bleibt: lässt sich dieses Prinzip mit den vorhandenen Primitiven
(Layer 02 Trust-Flow, Layer 03 Verdikt-Cluster) tatsächlich abbilden, oder verlangt es einen
Mechanismus, den es noch nicht gibt?

**Die Hypothese für den Prototyp.** Zwei Pfade im selben Lauf:
1. B unterwirft sich, A klagt an, Z urteilt gegen B, `verdict_status()` liefert `BINDING`. Ein
   Beobachter C, der Z vertraut, widerruft seinen Vouch auf B. Trust-Flow-Effekt messen (wie
   D328: Distanz, Kapazität, Fluss, Pfade).
2. B widerruft seine Unterwerfung, bevor `verdict_status()` ausgewertet wird — Status kippt zu
   `ATTRIBUTED_OPINION`. Derselbe Beobachter C sieht Anklage, Verdikt und den Zeitpunkt des
   Widerrufs; die Szenario-Regel für C lautet: widerruft denselben Vouch, wenn
   `trust_flow(C, Z) > 0` — eine Beobachter-Policy, keine Protokollmechanik. Denselben
   Trust-Flow-Zustand danach messen.

**Erwartung, vor dem Lauf benannt (Golden Anchors werden nie nachgezogen).** Zeigen beide
Pfade denselben Trust-Flow-Effekt nach dem jeweiligen Vouch-Widerruf, trägt die
Reputationsschiene unabhängig von `BINDING`. Der Bond-Slash (`03 §2.3`) bliebe im
widerrufenen Pfad trotzdem aus — eine bereits benannte, keine neu gefundene Asymmetrie, wenn
sie sich bestätigt.

**Modus.** D311 gilt: Wegwerfcode, keine Golden Numbers, keine Rücknahmeprobe, keine
Zweitimplementierung. Nur der Befund geht ins Register.

---

### D333 — Abnahme Szenario C (00av): Reputationsschiene traegt unabhaengig von BINDING

**Lauf.** Branch `00av-schlichtung-szenario`, Commit `445b423`, Basis `6b46273`. Zwei Phasen
aus identischer Baseline (`anna`=Anklaeger, `bruno`=Beschuldigter, `dora`=Schiedsrichter,
`chris`=Beobachter). Unabhaengig nachgebaut: Diff angewendet, Umgebung neu aufgesetzt,
`tools/sim/szenario_c.py` selbst ausgefuehrt — Ausgabe deckungsgleich mit der Meldung.

**B1 — Hypothese aus D332 bestaetigt.** `verdict_status()` liefert `BINDING` (Phase 1) bzw.
`ATTRIBUTED_OPINION` (Phase 2, nach Widerruf der Unterwerfung). Trust-Flow-Kennzahlen
(`d`, `C`, `edges`, `flow`, `paths`) nach dem jeweiligen Vouch-Widerruf sind in beiden Phasen
identisch (`d=2, C=25, edges=2, flow=25, paths=1`). Die Beobachter-Regel
`revoke, wenn trust_flow(C,Z)>0` ist mit der vorhandenen `trust()`-Funktion ausdrueckbar, ohne
neue Formel oder neuen Code in `symbolon/`. Die Reputationsschiene aus `05-enforcement.md §5`
traegt damit unabhaengig vom formalen Bindungsstatus aus `03 §2.4` — die gleiche Struktur wie
beim Law Merchant (Milgrom/North/Weingast 1990) und den Diamantenhaendlern (Bernstein 1992):
Durchsetzung ueber Reputation, nicht ueber erzwingbare Bindung.

**B2 — Bond-Slash bleibt Spec-Satz, nicht Laufbefund.** Kein Bond-Primitiv in `symbolon/`
(unabhaengig per Volltextsuche bestaetigt). Abnahmekriterium 3 konnte nicht eintreten, weil
nichts hinterlegt war — korrekt als nicht anwendbar gemeldet, nicht erfunden. Die in D332
benannte Asymmetrie (Bond-Slash erfordert `BINDING`, Reputationsschiene nicht) bleibt damit
eine Aussage aus `03 §2.3`, kein Prototyp-Ergebnis.

**B3 — Szenario-Design verifiziert.** `constitution_res.arbitration.arbitrators =
[bruno, chris, anna]` (unabhaengig in `tools/example_nucleus.py` geprueft) — `dora` fehlt.
Waere sie gelistet, triege Pfad (i) in Phase 2 trotz Widerrufs der Unterwerfung, und der
Kontrast waere zerstoert. Bewusste, korrekte Wahl.

**B4–B6 — Rahmenbefunde, wie gemeldet.** Kein Klon-Schritt im Rahmen (zwei unabhaengige
Laeufe aus identischen Baseline-Schritten). Beobachter-Policy steht im Treiber, nicht in
einer Szenariodatei — `03 §2.2` (die Schicht liest den Ausgang nicht). Rahmenerweiterung um
`submit-arbitration`, `accusation`, `verdict`, `zeige was=verdict_status`; `test_sim.py`
unveraendert (8/8, wie vor dem Lauf).

**Abnahme.** Diff eigenstaendig gegen `6b46273` angewendet, Umgebung neu aufgesetzt,
Gesamtsuite (797/797) und `test_sim.py` (8/8) selbst laufen lassen, `verdict_status()` gegen
`03 §2.4` gelesen — keine Aenderung an einer Spec-Datei. Alle Nicht-Ziele aus dem Prompt
eingehalten. **Merge freigegeben.**

---

### D334 — GitHub-Spiegel umbenannt zu symbolon

**Anlass.** D331 benannte den GitHub-Spiegel bewusst nicht mit um — reiner Scope-Schnitt
des `00at`-Laufs, keine Dauerentscheidung. Vor dem Restack-Antragstext (Phase 1,
Repo-Link) nachgezogen, damit Gitea-Name, Paketname und oeffentlicher Spiegel wieder
uebereinstimmen. Lokaler Ordnername bleibt bewusst `~/mensch-als-republik`
(Arbeitsbequemlichkeit, keine Konsistenzpflicht).

**Ausgefuehrt (ausserhalb von Git, durch Oli).** GitHub-Repository umbenannt:
`github.com/olisym/mensch-als-republik` → `github.com/olisym/symbolon` (GitHub legt
automatisch einen Redirect vom alten Pfad an). Gitea-Push-Mirror-Ziel-URL entsprechend
umgestellt. Beim Editieren der Mirror-URL gingen die hinterlegten Zugangsdaten verloren
(bekannte Gitea-Eigenheit) — Push schlug zunaechst mit `terminal prompts disabled` fehl.
Behoben durch neu erzeugten GitHub Personal Access Token, im eingeklappten
„Authentifizierung"-Abschnitt der Mirror-Einstellungen nachgetragen. Manueller Sync
danach erfolgreich, kein Fehler-Badge mehr.

**Stand.** Gitea `git.h.error13.de/oli/symbolon`, GitHub-Spiegel
`github.com/olisym/symbolon`, Paketname `symbolon`, lokaler Ordner
`~/mensch-als-republik` — drei von vier Namen jetzt deckungsgleich, der vierte bewusst
unveraendert.

---

### D335 — Tagline fuer Symbolon: A Self-Verifying Trust Layer for Local-First Networks

**Anlass.** Im Zuge des Restack-Antragsentwurfs (O57) wurde ein englischer Untertitel
gebraucht, der die aktuelle Ausrichtung traegt, ohne D317 zu widersprechen — der Titel der
Spec bleibt *Mensch als Republik*.

**Wortwahl.** „Self-Verifying" statt „consensus-free": zieht D317 direkt weiter — die
Marke verifiziert sich, indem die Haelften zusammenpassen, nicht weil eine Autoritaet
signiert (`08 §2.2`). „Local-First Networks" statt „Mesh Networks": Reticulum beschreibt
sich selbst als Mesh-Stack, aber die fuer MaR eigentlich tragende Eigenschaft ist
"no IP addresses, no DNS, no central authority" — Adressierung und Vertrauen sind
selbstausgestellt, nicht von einer Registrierstelle vergeben. „Local-first" trifft das und
zitiert wortwoertlich Restacks eigene Sprache ("local-first infrastructure").

**Ausgefuehrt.** Zeile in `README.md` direkt nach dem Titel ergaenzt (Commit `6b31ecd`).
Kurzbeschreibungen bei Gitea (`git.h.error13.de/oli/symbolon`) und GitHub
(`github.com/olisym/symbolon`) ausserhalb von Git durch Oli auf denselben Wortlaut gesetzt.

---

### D336 — Fork zu Szenario D: Rechenschaft unter Partition (LoRa/Reticulum-Frage)

**Anlass.** Offene Forschungsfrage aus `00av`/Sitzungsstart `00aw`: trägt das Stufe-C-Ergebnis
(D332/D333 — Trust-Flow-Konsequenz unabhängig von `BINDING`/`ATTRIBUTED_OPINION`) auch dann,
wenn Beobachter nicht wie in Stufe C sofort und vollständig beliefert werden, sondern wie unter
LoRa/Reticulum: Pakete gehen dauerhaft verloren, Reihenfolge ist nicht garantiert, Uhren sind
nicht synchron.

**Der Fund, der die Frage schärft.** Die Bausteine dafür existieren bereits, ungenutzt in dieser
Kombination: `tools/sim/welt.py::Welt.zustellen(nur=...)` erlaubt selektive, dauerhaft partielle
Zustellung; `Teilnehmer.write_now()` setzt lokale Uhren unabhängig je Teilnehmer;
`tools/sim/szenario.py::_trust_row/_verdict_status_row/_classify_row` werten bereits pro
Teilnehmer aus dessen eigenem `store_laden()` aus, nicht global. Spec-seitig ist Degradation bei
fehlender Referenz vorgesehen (`State.PENDING`, `symbolon/verifier.py`;
`ProfileFinding.UNRESOLVED_ACCUSED`, `symbolon/profiles/verdict.py`) — aber bisher nur an
Einzelatomen unit-getestet, nie an einem Mehrparteien-Vertrauensgraphen unter echter,
dauerhafter Wissensasymmetrie durchgespielt.

**Was das nicht ist.** Kein neues Primitiv, keine Netz-Simulation mit Zufallsverlust — die
vorhandene selektive Zustellung reicht, um jedes Zustellmuster deterministisch nachzustellen.
Kein Golden-Number-Lauf, kein Rollback (Szenariomodus, D311).

**Die Hypothese für den Prototyp.** Zwei Läufe auf demselben Stufe-C-Baseline (A=anna, B=bruno,
Z=dora, C=chris; Vouch-Graph C→B, C→Z, Z→B; Obligation B→A; `submit-arbitration` ×2,
`accusation`, `verdict`):

- **Lauf 1 „Broadcast"** — Kontrolle, identisch zu Stufe C: sofortige, vollständige Zustellung,
  chronologische Reihenfolge.
- **Lauf 2 „Funkstille"** — dieselben Claims, aber:
  (a) **Umordnung**: `verdict_z` erreicht A und C, bevor `acc_a_b` (sein Referenzziel) dort
      ankommt — erwartet: `PENDING`/`UNRESOLVED_ACCUSED`, kein Absturz; nach Nachlieferung
      Konvergenz auf denselben Endzustand wie Lauf 1.
  (b) **Dauerhafter Verlust**: der Widerruf von `vouch_c_b` (wie Stufe-C-Phase-1) erreicht Z und
      B, aber nie A — erwartet: A behält lokal einen stabilen, von B/Z/C abweichenden, aber in
      sich widerspruchsfreien `trust(C→B)`-Wert.
  (c) **Uhrendrift**: A's lokale Uhr wird über `t_exp` einer der Vouches gesetzt, während
      B/C/Z darunter bleiben — erwartet: nur A sieht diese Vouch lokal als `expired`.

Jede Abweichung von (a)–(c) ist ein Befund, keine Regression — die Erwartung selbst ist die
Messlatte, nicht ein vorab getippter Zahlenwert.

---

### D337 — Abnahme Szenario D: Rechenschaft unter Partition (a/b widerlegt, c bestätigt)

**Anlass.** Abnahme zu D336, Branch `00aw-szenario-d`, Commit `2351ee2`. Unabhängig
nachgebaut: Diff angewendet, `python -m tools.sim.szenario_d` selbst laufen lassen —
Ausgabe deckungsgleich mit der gemeldeten.

**Ausgeführt.** Neue Datei `tools/sim/szenario_d.py` (Wegwerf), keine Änderung an
`symbolon/`, `welt.py`, `szenario.py`, `szenario_c.py`. `_verdict_status_namen` als
beschränkte Kopie von `_verdict_status_row` — begründet, da `verdict_status()` explizit
`raise ValueError("verdict not in store")` verlangt (`symbolon/profiles/verdict.py`),
sobald der Verdikt-Claim lokal fehlt: kein Bug, sondern Vorbedingung — die Funktion
beantwortet „ist dieses Verdikt für mich bindend", nicht „was hältst du von einem
Verdikt, das du nicht hast".

**Befund (a) — widerlegt, korrigiert eine eigene Prompt-Annahme des Supervisors.**
Umordnung (Verdikt vor Anklage) führt zu keinem Absturz und konvergiert nach
Nachlieferung — aber die erwarteten Marker `PENDING`/`UNRESOLVED_ACCUSED` treten nicht
ein, weil zwei Ebenen verwechselt wurden (Prüfregel 38): `State.PENDING` (Layer 01,
unbekannter Kettenvorgänger) ist nicht dieselbe Mechanik wie die Anklage/Verdikt-
Querverweise in `verdict_status()` (Layer 03, eigene Finding-Familie). Die tatsächliche
Degradation ist `UNKNOWN_ACCUSATION` (referenzierte Anklage fehlt im Store) —
`UNRESOLVED_ACCUSED` gilt einem anderen Fall (fehlender bestrittener Claim hinter einer
zweistufigen Anklage). Zusätzlich: Autoren besitzen ihren eigenen Claim trivial (kein
Zustellungsbedarf) — anna bleibt deshalb durchgehend `BINDING`, weil sie `acc_a_b` selbst
verfasst hat. Realer Befund für D336: Layer 01 und Layer 03 degradieren bei fehlender
Referenz unterschiedlich, aber beide graceful — kein Absturz auf keiner der beiden
Ebenen, nur unterschiedliche Vokabeln.

**Befund (b) — widerlegt, Ursache ist eine Konfundierung im Prompt (Supervisor).** Die
Uhrendrift (c) wurde vor dem Widerruf-Test (b) auf demselben Subjekt/Anker verlangt:
annas Uhrendrift löscht bereits vor dem Widerruf-Test alle Baseline-Vouches lokal
(`t_exp`-Ablauf), wodurch anna schon vorher `d=None/flow=0` zeigt und der eigentliche
Test — bleibt der Vor-Widerruf-Wert erhalten, wenn der Widerruf nie ankommt? — nicht
isoliert beobachtbar ist. Tatsächlich bestätigt: anna weicht stabil und fehlerfrei von
bruno/chris/dora ab (Wert vor und nach dem nie zugestellten Widerruf identisch) — das
erfüllt D336s eigentliche Kernaussage („stabil, abweichend, widerspruchsfrei"), nur nicht
mit der im Prompt getippten Vergleichszahl aus Lauf 1.

**Befund (c) — bestätigt.** Nur anna sieht `vouch_c_b` als `expired`; `now` bleibt
lokal/subjektiv auch im Mehrparteien-Graphen, wie `01-claim-atom.md §6` normativ verlangt.

**Gesamtbild.** Kein Absturz, keine widersprüchliche Kennzahl, keine stille
Fehlbehandlung in einem der drei Fälle — die Rechenschaftsschiene (D332/D333) bricht
unter Partition nicht. Zwei der drei „erwarteten Marker" waren vom Supervisor falsch
benannt bzw. konfundiert, nicht vom Protokoll widerlegt.

**Offen, falls sauber isoliert gewünscht.** Ein Szenario D' mit (i) einem Nicht-Autor
als Ziel des Umordnungstests (nicht anna selbst) und (ii) getrennten Subjekten/Läufen
für (b) und (c), damit beide unabhängig voneinander messbar sind. Kein Zwang — die
Kernfrage aus D336 ist bereits ausreichend beantwortet.

**Nebenbefund, kein Blocker.** `check_specs.py` zeigt `00aw-szenario-d-prompt.md`
bereits als gebunden, `00av-schlichtung-szenario-prompt.md` weiterhin als ungebunden,
obwohl `szenario_c.py` dieselbe Zitierform verwendet wie `szenario_d.py` — Ursache
ungeklärt, außerhalb des Prompt-Scopes.

---

### D338 — Fork zu Szenario D′: saubere Isolierung von (a) und (b) aus D336

**Anlass.** D337 hat zwei Konstruktionsfehler im Prompt zu D336 benannt: (a) wurde an
anna gemessen, der Autorin von `acc_a_b` — Autoren besitzen ihren eigenen Claim trivial,
die Umordnung testet dort nichts. (b) und (c) liefen sequenziell im selben Kontext auf
demselben Subjekt (`vouch_c_b`), wodurch annas Uhrendrift (c) bereits vor der
Widerruf-Messung (b) alle Baseline-Vouches lokal ablaufen ließ und den eigentlichen Test
überdeckte.

**Was das nicht ist.** Kein neuer Fund über MaR, keine neue Hypothese — dieselbe
Fragestellung wie D336, nur ohne die zwei benannten Konfundierungen. (c) selbst war in
D337 bereits unkonfundiert und bestätigt; wird nicht wiederholt.

**Die Korrektur.**
- **(a) neu:** Umordnung an bruno (Beschuldigter, Autor weder von `acc_a_b` noch
  `verdict_z`) und chris (Beobachter) messen, nicht an anna. Erwartete Marker jetzt
  korrekt aus D337 abgeleitet: `verdict_status` zeigt `ATTRIBUTED_OPINION` +
  `UNKNOWN_ACCUSATION`, solange `acc_a_b` fehlt, danach `BINDING`. `classify(verdict_z)`
  bleibt durchgehend `active` — `State.PENDING` gilt nur für fehlende *Kettenvorgänger*
  (revoke-/supersede-Ziel), nicht für die Anklage-Querreferenz; keine Erwartung von
  `PENDING` mehr.
- **(b) neu:** eigener, unabhängiger Lauf ohne jede Uhrmanipulation — nur die Baseline
  plus Widerruf von `vouch_c_b`, zugestellt an bruno/chris/dora, niemals an anna.
  Erwartung: anna behält exakt den Vor-Widerruf-Wert aus der Broadcast-Kontrolle, die
  anderen drei zeigen den Nach-Widerruf-Wert.

Jede Abweichung ist wie in D336 ein Befund, kein Golden-Number-Lauf, kein Rollback
(Szenariomodus, D311).

---

### D339 — Abnahme Szenario D′: (a) und (b) sauber isoliert bestätigt

**Anlass.** Abnahme zu D338, Branch `00aw-szenario-d2`, Commit `31c17de`. Unabhängig
nachgebaut: Diff angewendet, `python -m tools.sim.szenario_d2` selbst laufen lassen —
Ausgabe deckungsgleich mit der gemeldeten.

**Ausgeführt.** Neue Datei `tools/sim/szenario_d2.py` (Wegwerf), keine Änderung an
bestehenden Dateien. Drei vollständig unabhängige Läufe (kein geteilter Kontext), wie in
D338 verlangt.

**Befund (a) — bestätigt.** Verdikt an bruno und chris (nicht an der Autorin) vor der
Anklage zugestellt: beide zeigen `ATTRIBUTED_OPINION` + `UNKNOWN_ACCUSATION`,
`classify(verdict_z)` bleibt `active`. Nach Nachlieferung von `acc_a_b`: beide `BINDING`.
Damit ist die in D337 korrigierte Erwartung (Layer-03-Degradation über
`UNKNOWN_ACCUSATION`, nicht `State.PENDING`) am richtigen Beobachter — einem Nicht-Autor
— bestätigt.

**Befund (b) — bestätigt.** Ohne jede Uhrmanipulation, in einem eigenen Lauf: anna
behält exakt den Broadcast-Wert (`d=1 C=50 flow=75 paths=2`), bruno/chris/dora zeigen den
Nach-Widerruf-Wert (`d=2 C=25 flow=25 paths=1`). Die Konfundierung aus D336/D337 ist
damit beseitigt — dauerhaft asymmetrisches Wissen allein erzeugt einen stabilen,
abweichenden, fehlerfreien lokalen Wert.

**Gesamtbild D336–D339.** Alle drei Teilfragen (a)/(b)/(c) sind jetzt unkonfundiert
beantwortet: die Rechenschaftsschiene (D332/D333) bricht unter Partition (Umordnung,
dauerhafter Verlust, Uhrendrift) in keinem Fall — kein Absturz, keine widersprüchliche
Kennzahl, durchgehend graceful degradation, nur über zwei verschiedene, jetzt korrekt
benannte Mechanismen (Layer 01 `State.PENDING` für Kettenvorgänger, Layer 03
`ProfileFinding.*` für Anklage-/Verdikt-Querreferenzen). Die LoRa/Reticulum-Kernfrage aus
`00av`/`00aw` ist damit für dieses Szenario abgeschlossen; kein weiterer Nachlauf offen.

---

### D340 — Fork zu Szenario E: Equivocation unter Partition

**Anlass.** D336–D339 haben ehrliche, aber verspätete/unvollständige Zustellung geprüft.
Offen bleibt der bösartige Fall: ein Autor, der bewusst zwei widersprüchliche Claims am
selben `h_prev` signiert (`01 §4`, `is_equivocation_pair`, `symbolon/atom.py`) — erkennt
ein Beobachter das noch, wenn die Netzpartition die beiden Hälften dauerhaft trennt?

**Der Fund, der die Frage schärft.** `_is_in_equivocation_pair` (`symbolon/verifier.py`)
prüft ausschließlich gegen `store.by_author_hprev(...)` — also gegen das, was der
jeweilige Beobachter selbst besitzt. `tools/autor.py::gabeln()` signiert bewusst an der
aktuellen Kettenspitze, ohne sie vorzurücken (D129) — der eingebaute Mechanismus für eine
Gabelung, bislang nur einzeln unit-getestet, nie unter echter, dauerhafter
Wissensasymmetrie. `derive.py` schließt bei **jedem** `EQUIVOCATION_FLAGGED`-Fund alle
Vouch-Gruppen des betroffenen Autors aus — auch unbeteiligte, nicht selbst geflaggte
Claims desselben Autors.

**Was das nicht ist.** Kein neues Primitiv — `kette_fortschreiben: false` in
`szenario.py::_schritt_claim` ruft `gabeln()` bereits. Kein Golden-Number-Lauf, kein
Rollback (Szenariomodus, D311).

**Die Hypothese für den Prototyp.** bruno equivoziert: Gabel-Vouch an dora (n=40,
`gabeln`), reale Vouch an chris (n=30, gleicher `h_prev`, `signieren`), danach eine
dritte, unbeteiligte Vouch an anna (n=20, neuer `h_prev`). Budgetsumme 90 ≤ D=100, damit
`OVERCOMMITTED_AUTHOR` nicht hineinspielt.

- **Lauf 1 „Getrennte Partition"**: Gabel nur an dora, reale Hälfte plus unbeteiligte
  Vouch nur an chris/anna — dauerhaft, keine Seite bekommt je beide Hälften. Erwartung:
  jede Seite sieht bruno lokal als unauffällig, mit je einem anderen, in sich
  konsistenten Bild — kein Fehler, stille Divergenz.
- **Lauf 2 „Späte Konvergenz"**: chris bekommt zuerst nur die reale Hälfte, später
  zusätzlich die Gabel. Erwartung: `classify(real_b_chris)` kippt bei chris von `active`
  auf `equivocation_flagged`; `trust(chris→dora)` und `trust(chris→anna)` fallen beide —
  auch `anna`, obwohl die Vouch dorthin nie Teil des Paars war.

Jede Abweichung ist ein Befund, keine Regression.

---

### D341 — Abnahme Szenario E: Equivocation-Erkennung sauber, Vorhersagen zweimal zu grob

**Anlass.** Abnahme zu D340, Branch `00aw-szenario-e`, Commit `dead3a6`. Unabhängig
nachgebaut: Diff angewendet, `python -m tools.sim.szenario_e` selbst laufen lassen —
Ausgabe deckungsgleich mit der gemeldeten.

**Befund Lauf 1 — Divergenz bestätigt, Gruppierung falsch vorhergesagt.** Kein Fehler,
keine widersprüchliche Kennzahl — aber keine Zweiteilung „dora vs. Rest", sondern eine
Dreiteilung, aus einem Mechanismus, den ich zum dritten Mal in dieser Sitzungsreihe
übersehen habe (D337, D340): **bruno besitzt als Autor beide Hälften seiner eigenen
Gabelung immer, unabhängig von jeder Zustellung.** Aus bruno's eigener Sicht sind daher
sowohl `real_b_chris` als auch `fork_b_dora` `equivocation_flagged` — und die
Ausschlussregel (`derive.py`) entfernt konsequent **alle** seine eigenen Vouch-Gruppen aus
seiner eigenen Trust-Berechnung, auch die unbeteiligte `legit_b_anna`. dora (einzige
Besitzerin von `fork_b_dora`) sieht dagegen einen zusätzlichen, für sie unauffälligen Pfad
über bruno — höherer Flow, nicht niedrigerer. anna/chris kennen nur die reale Hälfte und
`legit_b_anna` und sehen beide als völlig normal. Drei Gruppen, drei verschiedene
Gründe (Selbstverurteilung, zusätzlicher unentdeckter Pfad, schlicht fehlende Information)
— kein einheitlicher „dora vs. Rest"-Schnitt, wie im Prompt behauptet.

**Befund Lauf 2 — Kernaussage bestätigt, sogar stärker als vorhergesagt.**
`classify(real_b_chris)` kippt bei chris korrekt `active` → `equivocation_flagged`,
sobald `fork_b_dora` nachträglich ankommt. `trust(chris→anna)` fällt wie vorhergesagt
(10→0) — `legit_b_anna` war bereits als zählender Beitrag etabliert, bevor der Autor
entdeckt wurde, und wird beim Entdecken korrekt entfernt. `trust(chris→dora)` fällt
entgegen meiner Erwartung **nicht** (50→50, nur Kantenzahl 5→3): der neu ankommende
Beitrag von `fork_b_dora` wird im selben `derive()`-Durchlauf erkannt und ausgeschlossen,
in dem er erstmals erscheint — es gibt kein Zeitfenster, in dem ein soeben entdeckter
Equivocations-Beitrag kurz zählt, bevor er entfernt wird. Das ist eine **stärkere**
Eigenschaft als die im Prompt behauptete: Erkennung und Ausschluss sind atomar, nicht
sequenziell.

**Gesamtbild.** In keinem der beiden Läufe ein Fehler, eine widersprüchliche Kennzahl
oder ein stiller Fehlschluss — die Equivocation-Schiene degradiert unter Partition
genauso graceful wie die Rechenschaftsschiene aus D336–D339. Beide „widerlegt"-Urteile
des Werkzeugs sind zutreffend; die Ursache liegt in zwei zu groben Vorhersagen meinerseits,
nicht in einem Fund über MaR.

**Wiederkehrendes Muster, drei Sitzungen in Folge (D337, D340).** Ein Autor besitzt jeden
selbst signierten Claim immer, unabhängig von jeder `zustellen`-Aussage — das gilt auch für
beide Hälften einer selbst erzeugten Gabelung. Vorschlag, keine Aktion: eine Prüfregel
dazu wäre wahrscheinlich sinnvoll, überlasse ich Oli.

---

### D342 — Szenario F: Epochen-Rückfall bei rivalisierender Zustimmung unter Partition

**Anlass.** Abnahme zu Szenario F, Branch `00ax-szenario-f`, Commit `12eb86c`.
Unabhängig nachgebaut: Diff gelesen, `python -m tools.sim.szenario_f` selbst
laufen lassen, Claim-IDs von `chris_a`/`chris_b` gegen die gedruckten Vermerke
gegengeprüft (`dedupe_sort` sortiert nach Subjekt-Bytes, nicht Anhänge-
Reihenfolge im Code — Quelle der anfänglichen Verwechslung, aufgeklärt, kein
Fehler).

**Befund.** Eine bereits materialisierte Folgeepoche kann bei einem Beobachter
mit unvollständigem Wissen zurückfallen, sobald eine bislang unbekannte,
rivalisierende Ja-Stimme desselben Autors eintrifft (`04 §4.4`,
`CONFLICTING_APPROVAL`) — obwohl `ratify@1` nach `01 §5.4` unwiderruflich ist
und keine Epoche je „widerrufen" wird. Ursache: `resolve_epoch` (`chain.py`)
baut die Kette bei jedem Aufruf vollständig neu aus Epoche 1; ohne einen
aktuell tragenden Übergang endet sie wieder dort, wo die Kette zuletzt sicher
stand. Drei Stufen bei einem isolierten Beobachter (bruno): nur Vorschlag A
bekannt → `decide(A)=PASSED`, Epoche 2; `chris`s Konfliktstimme trifft ein,
Vorschlagsobjekt B fehlt noch → `UNKNOWN_PROPOSAL`, `chris` ausgeschlossen,
Epoche fällt auf 1 zurück; Vorschlagsobjekt B trifft nach → Diagnose wechselt
auf `CONFLICTING_APPROVAL`, Ergebnis (Epoche, `PENDING`) bleibt gleich — nur die
Diagnose wird präziser. Kontrastprobe (dora): fehlt das Vorschlagsobjekt A
dauerhaft, bleibt die Epoche dauerhaft bei 1, Vermerk
`EPOCH_PROPOSAL_UNAVAILABLE`.

**Einordnung.** Kein Implementierungsfehler. Die Kette ist bewusst zustandslos
und rein lokal (`04 §4.5`: „Die Prüfung ist offline und vollständig lokal");
ein Rückfall ist die Kehrseite derselben Eigenschaft, die eine falsche
Ratifizierung verhindert (`§3.5`: „`UNEVALUABLE` ist nie `PASSED`"). Damit ist
die im Vergleichsdokument (D326) belegte Grenze — kein Ausschluss ohne Konsens,
Uhr oder Zentrale, siehe Buchanan/Tullock-Blockadeanalyse — um eine konkrete,
selbst nachgebaute Variante ergänzt: nicht nur die Entfernung eines feindlichen
Eintrags blockiert (`08 §8`, „Ein feindlicher Eintrag blockiert seine eigene
Entfernung"), auch eine bereits erreichte, gutartige Epoche ist bei
Teilwissen nicht dauerhaft gesichert, bis das Wissen aller relevanten Stimmen
vollständig ist. Das ist dieselbe „Exit statt Voice"-Struktur wie bei der
Rechenschaftsschicht (D336–D339, D340/D341): lokale, monotone Sicherheit vor
globaler Verfügbarkeit.

---

### D343 — Methodik: Splice-Assert muss den Erfolgszustand verbrauchen (Prüfregel 65)

**Anlass.** Eigener Fehler beim Anhängen von D342 in `00ax`: der erste Lauf von
`tools/splice_run.py` gegen mein Splice-Skript hängte den Eintrag korrekt an; der
Anker (letzter Satz von D341) blieb danach unverändert einmalig, weil ich nur
danach eingefügt habe, statt ihn zu verbrauchen. Der zweite, vom Harness
erzwungene Lauf gelang deshalb ein zweites Mal — Symptom: zwei D342-Einträge —
und der Harness setzte beide Läufe zusammen zurück (`git checkout --`), zu Recht.

**Befund.** Der Assert eines Splices muss nicht nur den Anker prüfen, sondern
auch, dass der *Erfolgszustand des ersten Laufs* beim zweiten Lauf nicht mehr
zutrifft — z. B. durch eine zusätzliche Prüfung auf das neu eingesetzte
Zielmuster (hier: die Überschrift `### D342`). Ohne diese Prüfung erkennt der
Harness die fehlende Idempotenz nicht als Fehler im *Skript*, sondern als
Fehlschlag der *Anwendung*, und verwirft eine eigentlich korrekte erste
Ausführung.

**Einordnung.** Kein Fund über MaR, ein Fund über die eigene
Werkzeugdisziplin — ergänzt Prüfregel 42 (Assert prüft das Ergebnis, nicht den
eingesetzten Text) um die Idempotenz-Richtung: nicht nur *was* geprüft wird,
sondern *ob die Prüfung nach der Anwendung noch dieselbe Antwort gibt*. Als
Prüfregel 65 aufgenommen.

---

### D344 — Gekürzte Ausgabe an einem Gate macht das Gate blind (Prüfregel 66)

**Anlass.** In `00ax` stand vor Merge und Push der Block
`make check 2>&1 | tail -8`, eingebunden in eine `and`-Kette. In einer Pipe
entscheidet der Rückgabewert des **letzten** Glieds; `tail` gelingt praktisch
immer. `make check` brach mit `Fehler 1` ab (`check-specs`: drei bare
Paragraphenverweise in `tools/sim/szenario_f.py`), die Kette lief trotzdem
weiter — Merge nach `main`, Push nach Gitea und Branch-Löschung erfolgten auf
einem roten Zustand. Reparatur in `204f535`.

**Zweiter Fund bei derselben Gelegenheit.** Der anschließende, ungekürzte Lauf
zeigte einen zweiten roten Punkt, der **nicht** aus dieser Sitzung stammte:
`ruff` beanstandete einen ungenutzten Import (`T_EXP`) in
`tools/sim/szenario_d.py`, eingeführt in `2351ee2` (`00aw`). Derselbe
Pipe-Mechanismus hatte ihn eine Sitzung lang verdeckt. Ein blindes Gate
verdeckt nicht nur den eigenen Fehler, sondern konserviert alle früheren.

**Befund und Auflösung eines Konflikts.** `arbeitsweise.md` verlangt, lange
Diagnoseausgabe per Pipe zu kürzen; Prüfregel 39 verlangt, dass in einer
`and`-Kette der Rückgabewert entscheidet, nicht der gedruckte Text. Beide
Regeln bestanden bereits, aber keine sagte, welche gewinnt, wenn ein
**Tier-1-Schritt** (Merge, Push, Löschung) von dem gekürzten Lauf abhängt. Sie
tut es jetzt: an einem Gate wird nicht gekürzt. Entweder läuft der Befehl
ungekürzt, oder der Status wird explizit geprüft (`$pipestatus[1]` in fish),
oder das Gate steht in einem eigenen Block, dessen Ergebnis vor dem Tier-1-Zug
gelesen wird. Als Prüfregel 66 aufgenommen.

**Einordnung.** Kein Fund über MaR. Ein Fund über die Stelle, an der die
Token-Ökonomie (kürzen, bündeln) die Prüfdisziplin untergräbt — und die
Bündelungsregel aus `arbeitsweise.md` („Ein Shell-Block pro Zug") ist genau
deshalb an dieser Stelle einzuschränken: ein Gate und der davon abhängige
Tier-1-Zug gehören nicht in dieselbe Kette, weil sonst niemand das Ergebnis
zwischen beiden liest.

---

### D345 — Szenario G: wie weit die Kette zurückfällt und was davon sichtbar bleibt

**Anlass.** D342 zeigte den Rückfall auf einer einstufigen Kette (1→2). Offen blieb,
wie weit eine zweistufige Kette zurückfällt und ob eine Abweichung zwischen zwei
Beobachtern irgendwo vermerkt wird. `tools/sim/szenario_g.py` (`00ay`), drei Läufe:
Kette 1→2→3, vier Teilnehmer, Schwelle `1/2`, also drei Ja von vier.

**Befund 1 — der Rückfall endet am Bruchpunkt, nicht an der Wurzel.** Eine
rivalisierende Ja-Stimme auf einen Vorschlag mit `predecessor == epoch_1` wirft den
Beobachter auf Epoche 1; dieselbe Stimme auf einen Vorschlag mit
`predecessor == epoch_2` lässt ihn auf Epoche 2 stehen. `resolve_epoch` baut ab Epoche 1
neu auf und endet an der ersten Sprosse, die nicht mehr trägt (`04 §4.5`). Nicht „die
Kette kollabiert", sondern „die Kette endet dort, wo sie zuerst nicht mehr getragen
wird".

**Befund 2 — der Rückfall braucht weder Partition noch Gabelung.** Lauf 3: gerade
Autorenkette, eine einzige Konfliktstimme, Vollzustellung an alle vier. Alle vier
Beobachter landen auf demselben Index mit denselben Vermerkarten. Ein Mitglied, das ein
zweites Ja abgibt, wirft das ganze Netz gemeinsam zurück; Teilwissen verschiebt nur, wer
es wann sieht. Die erste Fassung des Szenarios hängte drei Konfliktstimmen per
`claim_gabeln` an eine Spitze und band den Befund damit an eine Equivokation, die er
nicht braucht (Prüfregel 67).

**Befund 3 — die überholte obere Sprosse hinterlässt keinen Vermerk.** Beim Rückfall auf
Epoche 1 trägt kein Vermerk die `claim_id` der Ratifizierung der zweiten Sprosse oder den
Hash ihres Vorschlags: `chain.py` überspringt Ratifizierungen mit fremdem `predecessor`
stumm, und die Vermerkliste entsteht in jedem Schleifenschritt neu (`04 §4.5`). Der
Beobachter erfährt, warum die Kette bei 1 endet, nicht, dass sie einmal bei 3 stand.

**Befund 4 — selektives Zurückhalten hält einen Beobachter dauerhaft zurück, ohne
Vermerk bei irgendwem.** Wird einem Beobachter das `ratify@1` der zweiten Sprosse
vorenthalten, steht er auf Epoche 2 mit leerer Vermerkliste, während die übrigen auf
Epoche 3 stehen — ebenfalls mit leerer Liste. Kein lokaler Vermerk unterscheidet „noch
nicht ratifiziert" von „mir vorenthalten". Sichtbar wird die Divergenz allein im
Quervergleich zweier Beobachter. Das ist die Governance-Entsprechung zu D340/D341.

**Verworfen: ein Vermerk „du hängst zurück".** Er setzte voraus, dass ein Beobachter die
Epoche der anderen kennt, also globalen Zustand. `04 §4.5` legt die Gegenrichtung fest:
die Kette beantwortet, welche Epoche gilt, nicht, was in einer überholten Epoche geschah.
Kein Implementierungsfehler — dieselbe Eigenschaft wie in D342.

---

### D346 — Die zurückgehaltene Ja-Stimme setzt ihren Autor dauerhaft aus

**Anlass.** Fall L3-3 aus Szenario G (`00ay`): ein Mitglied stimmt mit Ja auf einen
Vorschlag, dessen Objekt es nie herausgibt. Alle vier Beobachter fallen auf Epoche 1,
Vermerk `UNKNOWN_PROPOSAL`.

**Befund.** Nach `04 §4.4` gilt eine aktive Ja-Stimme auf einen unbekannten Vorschlag als
möglicherweise epochengleich und blockiert die andere Ja-Stimme desselben Autors — in
jeder Auszählung, die eine Kettenauflösung noch braucht (D178). Ist das Objekt nirgends
vorhanden, gilt das bei allen Beobachtern gleichzeitig und unbefristet: heilen kann nur
der Autor selbst, weil das Objekt content-adressiert ist und niemand sonst es liefern
kann.

**Einordnung.** Das ist keine Sperrminorität über die Schwelle, sondern die dauerhafte
Stilllegung genau einer Ja-Stimme, zum Preis von null. `k` Mitglieder legen so `k`
Stimmen still; beschlussfähig bleibt die Verfassung, solange `n − k` die Schwelle über
`n` noch erreicht — im Szenario (`n = 4`, `1/2`) fehlte damit die dritte Ja-Stimme.
Nicht-Teilnahme wirkt in MaR ohnehin wie Ablehnung; diese Stimme ist mehr: aktiv, gültig,
in jeder künftigen Epoche wirksam und von einer legitim schwebenden Stimme von außen
nicht zu unterscheiden. Wo eine Verfassung `vote@1` nicht in `irrevocable_predicates`
führt, kann der Autor zurücknehmen; die Wirkung hält, solange er es nicht tut. Anschluss
an D234–D236: dort kann ein feindlicher Eintrag nicht entfernt werden — hier muss er
dafür nicht einmal blockieren, sondern nur schweigen.

**Keine Spec-Änderung vorgeschlagen.** Die Richtung von `04 §4.4` ist erzwungen: die
Gegenannahme (unbekannt heißt möglicherweise fremd) erzeugt zwei Nachfolger derselben
Epoche und damit Über-Ratifizierung. Eine Frist auf unaufgelöste Stimmen wäre eine Uhr.

---

### D347 — Budgetrahmen und AI-Offenlegung für den Restack-Antrag

**Anlass.** O57 blockierte auf zwei Punkten, die nur der Operator entscheiden kann: der
Budgetzahl (abhängig von der Hinzuverdienstgrenze der Rente) und der Offenlegung der
KI-Nutzung im Formularfeld. Beide sind hier entschieden; die Faktensammlung bleibt
Rohmaterial, die Formularsätze schreibt der Operator selbst.

**Entscheidung Budget.** Beantragt werden 15.000 €: 12.000 € Arbeitsanteil (200 Stunden zu
60 €/h) und 3.000 € Sachkosten in getrennten Zeilen (vServer, API-Nutzung, Hardware für
die LoRa/Reticulum-Phase, externer Review). Ausgezahlt wird gegen Meilensteine; die
Aufgabenblöcke werden entlang natürlicher Abnahmepunkte geschnitten.

**Begründung.** Die Summe ist nicht durch den Bedarf nach oben begrenzt, sondern durch zwei
Randbedingungen. Erstens die Hinzuverdienstgrenze der vollen Erwerbsminderungsrente, zu der
die Arbeitsmarktrente zählt: 20.763,75 € im Kalenderjahr 2026. 15.000 € liegen auch dann
darunter, wenn der volle Zufluss ohne Abzug der Sachkosten angerechnet würde, und ein
Projektlauf über einen Jahreswechsel verteilt ihn zusätzlich. Zweitens der im Antrag selbst
dokumentierte Zeitaufwand: das Formularfeld verlangt Stunden, und der Antrag wird bei
Bewilligung veröffentlicht. 200 Stunden über zwölf Monate sind rund vier Stunden pro Woche
und damit mit dem Leistungsbild der vollen Erwerbsminderung vereinbar. Der Satz von 60 €/h
folgt daraus: ein niedrigerer Satz übersetzt dieselbe Summe in eine höhere, schriftlich
fixierte Stundenzahl, ein höherer provoziert bei einem Erstantrag ohne Referenzförderung
Rückfragen zum Satz selbst.

**Entscheidung Offenlegung.** Die KI-Nutzung wird im Feld „AI disclosure" vollständig
offengelegt, einschließlich der Rollenteilung (Spec-Supervisor und Prompt-Autor gegenüber
ausführendem Werkzeug) und der Prüfdisziplin.

**Begründung.** `08 §2.2` verlangt, dass Nachweisbarkeit nie an einer stillen Auslassung
hängt. Ein Antrag über dieses Protokoll, der die eigene Entstehungsweise verschweigt,
widerlegt die Prämisse, für die er wirbt. Hinzu kommt, dass die Arbeitsweise der Beleg
gegen den naheliegenden Einwand ist: dokumentierte Negativbefunde entstehen nur, wo
gemessen und nicht nur erzeugt wird — D234–D236 (die zentrale Frage hat keine bekannte
Lösung), D312 (die eigene Bauform erzwingt einen Verwahrer), D311 (aus 2511 Einzel- und
16958 Paarmutanten kam kein einziger Befund; alle kamen aus Lesen und Rücknahmeproben).

**Verworfen: schriftliche Vorabklärung beim Rentenversicherungsträger.** Die Betragsfrage
ist ohne Anfrage entscheidbar, und eine schriftliche Anfrage klärt mehr, als die
Entscheidung verlangt. Die Zeitfrage wird stattdessen als Gestaltungsauflage an das
Budgetfeld geführt (Satz hoch, Stundenzahl niedrig). Die Rentensituation selbst gehört
nicht in den Antrag: sie ist für die Bewertung ohne Belang.

**Verworfen: minimale Offenlegung.** Eine knappe Angabe hätte dasselbe Feld gefüllt, aber
die Prüfdisziplin ungenannt gelassen — also genau das weggelassen, was den Unterschied
zwischen dieser Arbeit und generiertem Text belegt.

---

### D348 — Programmierbare Kryptographie geprüft, als Gegenposition verortet, nicht aufgenommen

**Anlass.** Prüfung von 0xPARC, „Programmable Cryptography (Part 1)" (gubsheep, Juli 2024),
auf Verwendbarkeit für Symbolon. Der Text beschreibt eine zweite Generation von Primitiven
(FHE, MPC, zkSNARKs, Witness Encryption, Obfuscation), die beliebige Programme innerhalb
kryptographischer Objekte ausführen lassen, und drei darauf aufbauende Systementwürfe:
Universal Protocol, Hallucinated Servers, Cryptomata.

**Befund 1 — entgegengesetzte Richtung zu `08 §2.2`.** Der Ansatz macht eine Aussage
unbestreitbar, indem das Objekt seinen Beweis mitführt. `08 §2.2` gründet Überprüfbarkeit
darauf, dass Aussagen kollidieren können, ausdrücklich nicht darauf, dass sie signiert sind.
Ein Beweis erzeugt keine Kollidierbarkeit; er entzieht ihr den Gegenstand. Das ist kein
Reifegrad- oder Aufwandsproblem, sondern eine Richtungsentscheidung.

**Befund 2 — „Hallucinated Servers" ist die Gegenthese zu D312 und hält nicht.** Der Entwurf
verspricht Anwendungen, die einen Zustand führen, den kein Teilnehmer kennt: der Verwahrer
verschwindet, weil die Nutzerschaft ihn gemeinsam simuliert (Ahnenlinie im Text benannt:
Szabo, „The God Protocols"). D312 sagt, ein gemeinsamer Topf brauche einen benannten
Verwahrer. Der Widerspruch löst sich nicht zugunsten des Entwurfs: MPC und FHE setzen
Interaktion und kollektive Verfügbarkeit voraus. Der Text räumt selbst ein, dass erst
Obfuscation die Liveness-Anforderungen solcher Netze senken würde und dass Witness Encryption
und Obfuscation praktisch noch zu ineffizient sind. Der Verwahrer verschwindet also nicht, er
wird auf ein Quorum mit Verfügbarkeitsanforderung verteilt. Unter Partition ist die nicht
gegeben — D336–D342.

**Befund 3 — die Unvermeidbarkeit des Forks wird von der Gegenseite bestätigt.** Der Text
hält fest, dass eine Cryptomata mit den beschriebenen Technologien nicht verhindern kann,
unendlich kopiert und geforkt zu werden. Die Vergleichsanalyse (D326) hatte den Fork als
einzige Familie identifiziert, die alle Randbedingungen wahrt und die Blockade löst. Hier
erscheint dieselbe Eigenschaft als eingestandene Grenze der stärksten denkbaren
Konstruktion. Stützt D234–D236 aus fremder Richtung.

**Befund 4 — kein offener Blocker wird adressiert.** Beweise richten sich gegen Zweifel an
der Gültigkeit einer Aussage. Die offenen Befunde betreffen Unterdrückung und Zustellung:
D346 (die nie herausgegebene Ja-Stimme — der Beweis ihrer Wohlgeformtheit ändert nichts),
D345 (ein Beobachter hängt ohne Vermerk auf einer früheren Epoche — rekursive Beweise
komprimieren Historie, sie stellen sie nicht zu), D234–D236 (Autorität, nicht Verifikation).
Deckungsgleich mit dem Vouchsafe-Befund aus D326: Zurückhalten bleibt der einzige wirksame
Angriff, und Kryptographie greift ihn nicht an.

**Verworfen: POD/POD2 als Transportformat für claim-atoms.** Content-Adressierung und
Signaturen sind vorhanden; was zusätzlich käme, sind Vertraulichkeit und komprimierte
Historie. Beide lösen keinen im Register offenen Punkt. Technologie vor Frage.

**Verworfen: ZK-Beweise über Beträge.** Ein Beweis, der eine Aussage über einen Betrag
protokollseitig verwertbar macht, umgeht die Preisblindheit aus `03 §3.1` nicht, sondern
unterläuft sie. Jede Arithmetik bleibt Szenarioaussage; eine solche Stelle wäre ein Befund,
kein Feature.

**Einordnung.** Verwendbar als Vergleichspunkt aus der Gegenrichtung: alle bisherigen
Vergleichspunkte (BFT, Stellar, Gesellschaftsrecht, Moloch) sind Koordinationssysteme,
dieser ist ein Programm, Vertrauen durch Beweisbarkeit zu ersetzen. Symbolons Beitrag
dagegen: die Ersetzung gelingt an einer Stelle nicht (D312) und ist an anderer nicht nötig
(D333).

---

### D349 — O57 eingereicht; zwei Prüfläufe mit verschiedenen Werkzeugen finden Verschiedenes

**Anlass.** Der Restack-Antrag wurde am 10. September 2026 eingereicht, Code `2026-11-0c4`,
beantragt sind 15.000 € nach dem Rahmen aus D347. Beigefügt ist ein kuratiertes
Prompt-Provenance-Log gemäß der Offenlegungsentscheidung. Damit ist O57 geschlossen; die
Bewertung erfolgt erst nach der Frist am 3. November 2026, und bis dahin zählt die zuletzt
vollständige Fassung, eine Nachbesserung bleibt also möglich.

**Befund (Methodik).** Das beigefügte Log musste von Passagen befreit werden, die nicht in den
Antrag gehören. Geprüft wurde zweimal, mit verschiedenen Werkzeugen, und jeder Lauf fand, was
der andere übersah. Der erste Lauf war eine Mustersuche über Schlagwörter; er fand die Stellen,
die diese Wörter enthielten, und ordnete dabei zunächst eine Fundstelle dem falschen Kanal zu,
weil die Filterung den Kontext verlor. Der zweite Lauf war ein vollständiges Lesen durch ein
zweites Werkzeug; er fand einen zusammenhängenden Abschnitt, der keines der gesuchten Wörter
enthielt und deshalb für die Mustersuche unsichtbar war.

**Einordnung.** Das ist derselbe Mechanismus wie Prüfregel 67, in einer anderen Domäne: eine
Prüfung findet nur, was ihre Konstruktion zu finden erlaubt. Eine Suche über benannte Begriffe
kann nichts finden, was ohne diese Begriffe auskommt — sie ist gegenüber Umschreibungen blind,
und ihr Ausbleiben von Treffern ist kein Beleg für Abwesenheit. Ergänzend: Ein Ausschnitt als
Prüfgrundlage erbt die Grenzen seines Zuschnitts. Der erste Lauf arbeitete auf einer auf 110
Zeichen gekürzten Übersicht; eine Fundstelle lag jenseits dieser Grenze und blieb unsichtbar,
bis dieselbe Suche auf dem vollen Text lief.

**Konsequenz.** Wo eine Prüfung Abwesenheit feststellen soll und nicht bloß Anwesenheit, braucht
sie einen zweiten Lauf mit anderem Fehlermodus. Zwei Läufe desselben Verfahrens sind keine
zweite Prüfung. Ob daraus eine eigene Prüfregel wird, ist offen; der Fall stammt aus Arbeit
ausserhalb des Codes und ist der erste dieser Art im Register.

**Verworfen: ein dritter Prüflauf.** Nach zwei Läufen mit je eigenem Fund wäre ein dritter eine
Wiederholung des zweiten Verfahrens gewesen, kein neuer Fehlermodus. Die verbleibenden
Fundstellen wurden stattdessen durch eine präzisere Kopfzeile aufgefangen, die die ausgelassenen
Kategorien benennt und die Zahl der ausgelassenen Nachrichten je Stelle ausweist — eine benannte
Auslassung statt einer stillen, nach `08 §2.2`.

---

### D350 — `now` bekommt keine Quelle; zeitliche Rechenschaft läuft über `t`

**Anlass.** Die Übertragung auf unterbrochene Zustellung (LoRa/Reticulum) warf die Vorfrage auf,
was „Zeit" in MaR überhaupt heisst. Drei Grössen, bisher nie nebeneinander benannt: `t` (Feld 6,
vom Autor behaupteter Zeitstempel, signiert, nach `01 §2` ausdrücklich **kein** Ordnungsprimitiv
und nirgends im Code gegen eine Uhr geprüft), `t_exp` (signiert, die einzige Stelle, an der Zeit
Wirkung entfaltet) und `now` (je Beobachter, in keinem Claim, in keinem Vermerk, nicht signiert).

**Befund 1 — `now` ist die einzige Grösse, die das Ergebnis ändert und nicht kollidieren kann.**
`08 §2.2` gründet Überprüfbarkeit darauf, dass Aussagen kollidieren können. `now` ist keine
Aussage, sondern eine private Lesart, aus der ein öffentlich wirksamer Zustand folgt (`EXPIRED`,
`trust_usable=False`). Ein Beobachter mit verstellter Uhr lügt nicht — er hat eine andere
Wahrheit, und nichts an ihr ist überführbar. Das steht systematisch ausserhalb des
Rechenschaftsmodells und fällt nur deshalb nicht auf, weil Uhren in der Praxis grob
übereinstimmen.

**Befund 2 — zwei Zeitregime.** Der Governance-Pfad ist uhrenfrei, und zwar begründet:
`04 §3.1` Bedingung 4 wirft jede Stimme mit gesetztem `t_exp` als `VOTE_WITH_EXPIRY` aus der
Zählung, `epoch.py` ebenso jede Ratifizierung (`RATIFY_WITH_EXPIRY`), und im Ausschlusszweig aus
D346 blockiert eine ablaufende Stimme nicht einmal. Begründung ist D97: eine Stimme, die durch
Zeitablauf aus der Menge verschwindet, darf es nicht geben. Der Trust-Pfad ist umgekehrt
konstitutiv uhrgebunden — `02a §2.6` verlangt den Budget-Austritt über `t_exp`. Unter
zuverlässiger Zustellung fällt die Asymmetrie nicht auf; unter Partition wird sie zur Bruchlinie:
dieselben Beobachter können sich über die Verfassung einig sein und über die Kreditwürdigkeit
nicht.

**Entscheidung: kein Mechanismus zur Bestimmung von `now`.** `now` bleibt lokal, unzuverlässig
und ohne Autorität. Verworfen wurden Netzabfrage nach Roughtime-Art, Uhrenabgleich unter
Anwesenden (Marzullo, Berkeley, NTP) und jede Form von Zeitautorität. Alle drei setzen
wechselseitige Erreichbarkeit voraus, die unter Partition nicht gegeben ist — dieselbe Gegenthese,
an der in D348 die kollektiv rechnenden Konstruktionen gescheitert sind. Eine Zeitautorität wäre
zudem genau die zentrale Instanz, gegen die das Protokoll gebaut ist. Eine bessere Uhr ist nicht
das Ziel; eine Uhr, deren Wirkung rechenschaftsfähig ist, ist es.

**Richtung stattdessen, zwei Sätze.**

1. *Wo `now` das Ergebnis ändert, ist das ein Befund, kein Betriebszustand.* Der Verifier kennt
   den dritten Ausgang bereits: `temporal is None` führt auf `LINKED`, nicht auf eine Vermutung.
   „Ich kann die Zeit nicht beurteilen" ist damit schon sagbar. Der Kandidat für die Erweiterung
   ist ein Intervall statt eines Punktes, mit Überlappung zu `t_exp` als `LINKED` — konservativ,
   kostet Entscheidbarkeit, kauft Ehrlichkeit, verlangt keine fremde Annahme.
2. *Zeitliche Rechenschaft läuft über `t`, nicht über `now`.* `t` ist signiert und damit
   kollidierbar, wird heute aber nirgends ausgewertet. Ein Beobachter, der auf Grundlage von
   Ablauf handelt, gibt dabei ohnehin einen Claim mit eigenem `t` ab — seine Ablaufbewertung ist
   implizit bereits signiert. Überführbar wäre nicht die falsche Uhr, sondern die
   Unvereinbarkeit der eigenen Behauptungen. Das ist die Bauform der Equivocation: niemand muss
   wissen, welche der beiden Aussagen die wahre ist; es genügt, dass beide vom selben Autor
   stammen. Zeit käme so in das Rechenschaftsmodell hinein, statt daran vorbeigeführt zu werden.

**Verworfen: `t_exp` ersetzen.** Der Bedarf aus `02a §2.6` ist real, und ein zählbares statt
zeitliches Austrittskriterium ist nicht trivial. Die Frage bleibt offen, ist aber für keinen der
beiden Sätze oben eine Voraussetzung.

**Keine Spec-Änderung mit diesem Eintrag.** Szenario H misst zuerst den Ist-Zustand der beiden
Zeitregime, bevor an einem von ihnen etwas geändert wird.

---

### D351 — `UNSUPPORTED_RATIFICATION` benennt die Stimmen statt der Ratifizierung

**Anlass.** Szenario H, Lauf 2 (`00ba`): eine gerade Epochenkette, deren drei Stimmen ein `t_exp`
tragen. Erwartet war die Vermerkmenge, die aus dem Code folgt — ein
`UNSUPPORTED_RATIFICATION` mit dem Subjekt der Ratifizierung, dazu drei `VOTE_WITH_EXPIRY` mit
den Subjekten der drei Stimmen, zusammen vier Vermerke. Gemessen wurden **sechs**: drei je Art,
und beide Arten tragen dieselben drei Subjekte, naemlich die der Stimmen. Die `claim_id` der
Ratifizierung (`5a05e8f9...`) kommt in keinem Vermerk vor, obwohl sie sich von den Stimmen
unterscheidet und beide Praedikate verschieden sind (`.../vote@1` gegen `.../ratify@1`).

**Befund.** Der Vermerk zeigt auf das falsche Subjekt, und er zeigt dreimal statt einmal. Aus den
drei beteiligten Bausteinen folgt das nicht: `resolve_epoch` filtert die Kandidaten ueber
`is_nuc_name(claim, "ratify")` und reicht genau die eine Ratifizierung weiter, `_unsupported`
setzt ein einziges Finding mit `claim_id(ratify)`, und `dedupe_sort` ist
`tuple(sorted(set(...)))` ohne Kreuzprodukt. Die Ursache liegt zwischen `decide` und
`verify_ratification` und wurde durch Lesen dieser drei Stellen nicht auffindbar; sie wird
gesondert ermittelt.

**Einordnung.** Ein Vermerk ist in MaR keine Fehlermeldung, sondern die Zurechnung eines Mangels
auf einen benannten Claim. Ein Subjekt, das auf einen anderen Claim zeigt als den beanstandeten,
beschuldigt die Falschen — hier die Stimmenden statt der Ratifizierenden. Das trifft `08 §2.2` im
Kern: eine Aussage, die kollidieren koennen soll, muss zuerst sagen, wovon sie handelt.
Gleichzeitig verschwindet der tatsaechlich beanstandete Claim vollstaendig aus der Vermerkliste,
also die einzige Stelle, an der die gescheiterte Ratifizierung ueberhaupt benannt wuerde.

**Warum es bisher unentdeckt blieb.** Kein bestehender Lauf und kein Test erzeugt beide
Vermerkarten gleichzeitig. Szenario G kennt `UNSUPPORTED_RATIFICATION` nur ohne begleitende
Tally-Vermerke, die Golden Anchors `GV-26` und `GV-33` pruefen je eine Art fuer sich. Der Defekt
war erst sichtbar, als eine Lage beide Arten zugleich hervorbrachte — das war keine Absicht des
Szenarios, sondern ein Nebenprodukt von Lauf 2.

**Entscheidung: das ist ein Defekt, kein Verhalten.** Repariert wird das Subjekt, nicht die
Erwartung. Verworfen wurde, die gemessene Vermerkmenge als Ist-Stand in einen Golden Anchor zu
schreiben; das haette den Fehler normativ gemacht. Szenario H bleibt unveraendert — es ist der
Zeuge, nicht der Patient, und seine Ausgabe muss sich durch die Reparatur aendern.

**Methodischer Nebenbefund.** Der Fund kam nicht aus dem Werkzeugbericht, der ihn als
`zusaetzlicher Ist-Wert (nicht widersprochen)` fuehrte, sondern aus dem Abgleich der berichteten
Vermerkmenge gegen den gelesenen Code. Zwischenzeitlich stand der Verdacht im Raum, die berichtete
Ausgabe sei nachgebaut statt gemessen; er wurde durch einen eigenen Lauf widerlegt, bevor daraus
eine Folgerung wurde. Beide Schritte gehoeren zusammen: der Bericht ist nicht die Wahrheit, und
der Verdacht gegen den Bericht ist es auch nicht.

---

### D352 — Abnahme `00ba`/`00bb`: die Reparatur war seit D207 entschieden, die Abdeckung fehlte

**Die Reparatur.** In `verify_ratification` trug der Zweig für eine zitierte Stimme, die nicht in
`tally.yes` steht, `subject=cid` — die `claim_id` der **Stimme**. Richtig ist `subject=rid`, die
`claim_id` der Ratifizierung; die beiden benachbarten Zweige setzten sie bereits so. Eine Zeile,
Merge `a5a2748`, 798 Tests.

**Sie war normativ längst entschieden.** `04 §4.1` sagt es wörtlich: `UNSUPPORTED_RATIFICATION`
sagt, dass diese Ratifizierung nicht trägt. Und D207 hat genau diese Lage abgeräumt — die
Zeugenliste eines `ratify@1` ist ein Feld, Felder haben keine eigene Adresse, das Subjekt benennt
dasselbe Objekt nur gröber. Der Code widersprach also nicht einer Erwartung, sondern der eigenen
Spec.

**Der Befund, der schwerer wiegt als der Defekt.** D207 hat `epoch.py:140` namentlich als einen
von drei Pfaden gemeldet, die sich beliebig umstellen lassen, ohne dass die Testreihe reagiert:
„Was fehlt, ist nicht eine Regel, sondern Abdeckung." Der Lauf `00q` sollte für diese drei Pfade
Prüffälle anlegen. Der Defekt saß danach in einem davon und hat bis `00ba` überlebt. Eine
gemeldete Lücke ist nicht geschlossen, solange kein Test sie rot werden lässt — die Meldung selbst
deckt nichts ab, und ein Eintrag im Register ersetzt keinen Prüffall.

**Warum keine Vermerkart verloren geht.** Bei mehreren untauglichen Zitaten entsteht jetzt ein
Vermerk statt mehrerer, und die einzelne untaugliche Stimme wird nicht mehr benannt. Das ist die
normierte Lage: `04 §4.1` begründet sie mit der Adresse und trägt die Auskunft über die
Weitergabe der Auszählungsvermerke (D203), nicht über das Subjekt der Ratifizierung. Der Fall
einer zitierten Nein-Stimme ohne eigenen Tally-Vermerk bleibt damit gröber ausgewiesen als vorher;
das ist der Preis der richtigen Adresse und in `04 §4.1` bereits gewählt.

**Zwei Einschränkungen von Szenario H, für die Nachwelt festgehalten.** Erstens messen Lauf 1 und
Lauf 2 `resolve_epoch(now=X)` mit durchgereichtem Wert; die Teilnehmeruhr in der Welt bleibt in
allen Zeilen bei ihrem Anfangswert. Wirkungsgleich, weil nur `_beobachte` sie liest — gemessen ist
aber die Funktion unter fremdem `now`, nicht ein Teilnehmer mit verstellter Uhr. Zweitens
signiert Lauf 3 in einem Scope ohne Nukleus, ohne Genesis und ohne Verfassung. Er belegt damit,
dass `_is_temporally_valid` uhrabhängig ist, und nicht, dass der Trust-Pfad aus `02a §2.6`
divergiert. Der Befund der zwei Zeitregime (D350) steht, aber schmaler als die Formulierung des
Werkzeugberichts nahelegt.

**Verworfen: Szenario H nachbessern.** Beide Einschränkungen sind benannt, und die Frage, die H
beantworten sollte, ist beantwortet. Ein zweiter Lauf für eine bereits beantwortete Frage kostet
mehr, als die schärfere Fassung einbringt. Wenn der Trust-Pfad selbst geprüft werden soll, ist das
ein eigener Lauf mit eigener Frage, nicht eine Korrektur an diesem.

**Prüfregel-Kandidat, Nummer offen.** Ein als ungedeckt gemeldeter Pfad ist erst geschlossen, wenn
ein Test ihn rot werden lässt. Die Meldung, der Registereintrag und der Vorsatz, Prüffälle
anzulegen, decken nichts ab; nur der Test tut es. Wer eine Abdeckungslücke schliesst, nimmt die
Reparatur zurück und sieht den Test fallen — sonst ist unbekannt, ob er die Lücke trifft.

### D353 — `t` wird monoton entlang der Autorenkette

**Beschluss.** Für jeden Claim `C` mit lokal bekanntem Vorgänger gilt `C.t >= pred(C).t`.
Die Verletzung ist **kein Reject**, sondern ein Zustand am `linked`-Übergang:
`TIME_REGRESSION_FLAGGED`, `trust_usable=False`, Subjekt ist die `claim_id` von `C`.
Der Zustand gehört **in** `BUDGET_STATES`.

**Warum das `t` überhaupt erst verknüpft.** `t` ist Pflichtfeld, signiert und im Preimage —
und wird heute an genau einer Stelle ausgewertet: `01 §6` Punkt 7, `t < t_exp`, claim-intern
(`verifier.py:217`). Sonst liest nur die Serialisierung es. `t` ist also nicht unbenutzt,
sondern **unverknüpft**, und `08 §2.2` sagt genau darüber: was auf nichts zeigt und worauf
nichts zeigt, ist unwiderlegbar und folgenlos. Das gilt für ein Feld wie für einen Claim.

Die Kette schließt die Lücke, weil sie der einzige **uhrenfreie Index** im Protokoll ist.
`01 §5.3` sagt es in der Gegenrichtung: Ordnung kommt aus `h_prev`, nie aus Wall-Clock `t`.
Genau deshalb kann `h_prev` leisten, was keine Uhr leisten kann — zwei Aussagen desselben
Autors in eine unbestreitbare Reihenfolge bringen, ohne dass irgendwo eine Zeitquelle steht.
Die Monotonieregel **stiftet keine Ordnung aus `t`**; sie prüft `t` gegen die Ordnung, die
`h_prev` bereits hergibt. `t` bleibt kein Ordnungsprimitiv.

**Abgrenzung zu D78.** Dort wurde `t` als Rangfolge verworfen, weil es die einzige Stelle
wäre, an der Wall-Clock eine Rangfolge **zwischen zwei Autoren** stiftet, und ein Angreifer
mit falscher Uhr Kontrolle über die Bindungsfrage bekäme. Hier ist die Prüfung strikt
intra-Autor und die Wirkungsrichtung umgekehrt: eine rückwärts laufende Uhr in der eigenen
Kette belastet ausschließlich den Signierer. Dieselbe Abgrenzung trägt gegen das in D123
verworfene Widerspruchsfenster — ein Fenster bräuchte Ordnung zwischen Autoren, diese Regel
nicht.

**Warum `>=` und nicht `>`.** `t` ist in Sekunden aufgelöst. Zwei Claims desselben Autors
in derselben Sekunde sind legitim; strenge Monotonie würde die Claim-Rate an die
Uhrenauflösung binden und eine Form von Zeitautorität durch die Hintertür einführen.

**Warum kein Reject.** `01 §6` hält für die selbstenthaltene Gültigkeit fest, dass die Punkte
1 bis 7 bis auf **einen** benannten Konjunkt (`ziel.I == C.I`) ohne Speicher entscheidbar
sind. Ein zweiter vorgängerabhängiger Reject würde den Prüfumfang des speicherlosen Geräts
verschieben — der Begriff aus `01 §6` ist ausdrücklich der Bezugspunkt für Fassungen, die nur
diesen Teil bauen. Das richtige Vorbild ist `EQUIVOCATION_FLAGGED`: store-abhängig, Zustand
statt Fehler. Ist der Vorgänger unbekannt, bleibt es bei `PENDING` und es wird nicht geprüft —
Wissen verengt das Urteil, es kehrt es nicht um.

**Warum in `BUDGET_STATES`.** Wörtlich die Begründung aus D135: der Über-Commitment-Beweis
beruht auf Signaturen, nicht auf Aktivität. Eine rückwärts laufende Uhr ist kein
Lebenszyklus-Akt, und `02a §2.6` sagt, dass ein Vouch das Budget-Set ausschließlich über
`t_exp` verlässt. Ein Zustand, der Budget freigibt, wäre eine Prämie auf die kaputte Uhr.
Diese Zeile steht hier **vor** der Implementierung, weil D135 genau an dieser Stelle
nachträglich repariert werden musste.

**Geflaggt wird `C`, nicht die Kette und nicht der Autor.** `EQUIVOCATION_FLAGGED` trifft
beide Glieder eines Paares, weil beide dasselbe `h_prev` beanspruchen und keines Vorrang hat.
Hier hat der Vorgänger Vorrang: er steht definitorisch früher. Der Widerspruch ist `C`
zuzurechnen.

**Golden Numbers.** Alices Kette in `01` Anhang C ist bereits streng monoton:

```
TV1 1700000000 -> TV2 1700000100 -> TV3 1700000200 -> TV5 1700000300 -> TV6 1700000410
Delta:                    +100           +100           +100           +110
```

Bobs TV4 ist Genesis. Sämtliche NV-Vektoren hängen an `h_prev_genesis(ALICE)` und haben
keinen Vorgänger. **Kosten am Vektorsatz: null.** Gebraucht wird genau ein neuer
Negativvektor — ein Claim, der auf einen Vorgänger mit größerem `t` kettet.

**Verworfen — nichts tun.** Die Lage bliebe, dass ein signiertes Pflichtfeld in jedem Claim
steht und nichts trägt. Solange `t` nicht kollidieren kann, ist es Ballast für LoRa und eine
Einladung, es später doch als Ordnung zu lesen.

**Verworfen — Punkt 8 in `01 §6`.** Siehe oben: verschiebt die selbstenthaltene Gültigkeit.

**Verworfen — die ganze Folgekette flaggen.** Wirkt wie eine Sperre statt wie ein Vermerk und
bestraft Claims, die selbst widerspruchsfrei sind. `05` ist die Schicht für Folgen.

### D354 — Die Prämissennennung macht die Ablaufbewertung kollidierbar; Fork eröffnet und verortet

**Die Frage aus D350.** Kann die Aussage „dieser Claim ist abgelaufen" zu einem signierten,
kollidierbaren Claim werden? Zerlegt man sie gegen `_is_temporally_valid`, bleiben zwei
Aussagen, und nur eine gehört dem Beobachter: `C.t_exp = X` ist die Aussage des **Autors**,
längst signiert und kollidierbar. Seine eigene ist „meine Uhr stand bei der Auswertung über
X" — eine Aussage über sein **Instrument**, nicht über die Welt, und indexikalisch: wahr nur
relativ zu einem Auswertungsmoment. Zwei solche Aussagen widersprechen einander nur, wenn sie
auf denselben Moment zeigen, und das Einzige, was sie darauf festnageln könnte, wäre eine Uhr.
Zirkel. Das ist der Grund, warum `now` nach D350 außerhalb von `08 §2.2` steht, und er liegt
tiefer als die fehlende Quelle.

**Der Ausweg.** Das bestehende Kollisionsprimitiv trägt ihn nicht: `is_equivocation_pair` ist
gleiche `(I, h_prev)` bei verschiedener `claim_id` — strukturell, bedeutungsblind, eine
Gabelung. Zwei Claims, die inhaltlich Gegenteiliges sagen und dabei brav hintereinander
hängen, sind darüber unsichtbar. Inhaltliche Kollision existiert im Projekt nur dort, wo ein
Profil die Bedeutung definiert: `AMBIGUOUS_VOTE`, `CONFLICTING_APPROVAL`. Das ist der zu
übertragende Bauplan.

**Beschluss (Verortung, nicht Ausführung).** Der Fork ist eröffnet und verortet: Träger ist
die **Prämissennennung im opaken `v`**, Key 1, ausgewertet in `02a`/`03`. Layer 01 bleibt
unangetastet. Nennt ein Claim `B` die Bürgschaft `V` als Prämisse, dann ist

```
B.t > V.t_exp
```

ein Widerspruch zwischen zwei **signierten Zahlen** — ohne `now`, ohne Zeitquelle, ohne
Erreichbarkeit, auf einem Gerät ohne Uhr in einer Partition nachrechenbar. Er sagt nicht
„deine Uhr war falsch", sondern „du hast selbst bezeugt, wann du gehandelt hast, und selbst
bezeugt, worauf".

**Kosten am Feldsatz: null.** `02a` T-02.7 hält ausdrücklich fest, dass Zusatz-Keys in `v`
zulässig sind und kein Finding erzeugen (`v = {0: 2, 1: 99}` ergibt `n = 2`). Der Steckplatz
existiert und ist getestet. Keine Protokollversion, kein Vektor-Nachzug in `01`.

**Reihenfolge ist normativ: D353 vor D354.** Ohne die Monotonie ist D354 durch Rückdatierung
erledigt — man setzt `B.t` kleiner als `V.t_exp` und der Widerspruch verschwindet. Mit ihr
greifen beide ineinander: zu spät handeln belastet über D354, zu früh behaupten belastet über
D353. Beide Ausgänge produzieren ausschließlich Beweise gegen den Signierer; keiner gibt einem
Angreifer Kontrolle über eine Bindungsfrage. Das ist die Bauform aus `08 §2.2` — nicht
verhindern, sondern unbestreitbar machen.

**Nachtrag zu D350.** „`now` bekommt keine Quelle" heißt: kein Primitiv, keine Autorität,
keine Netzabfrage. Es heißt **nicht**, dass eine signierte Zeitaussage ausgeschlossen wäre.
`VISION.md §5` nennt den Zeitdienst bereits als **Profil** — signierte Zeit-Attestierung „ich
sah das zu meiner lokalen Zeit T", gestakt über `05`, ausdrücklich „kein neues Primitiv".
D354 ist dessen allgemeinere Form: statt eines eigenen Attestierungsprofils trägt jeder
abhängige Claim seine Prämissen, und die Zeitaussage fällt als `t` ohnehin schon an.

**Getragene Grenze.** Wer schweigt, bleibt unwiderlegbar — `01 §1` selektive Stille, `08 §2.2`
Schlusssatz. Das Loch wird nicht geschlossen, es bekommt einen Preis: wer will, dass sein
Handeln zählt, muss zeigen, worauf er sich stützt, und legt damit die Zeitstempel offen.

**Verworfen — neuer `J`-Tag.** `J` ist das Subjekt, ein Claim hat genau eines, und der Enum ist
geschlossen (`01 §2.1`). Eine Prämissenliste ist kein Subjekt.

**Verworfen — neues Feld.** Der Feldsatz aus `01 §2` ist der teuerste Ort der Spec: sechs
Invarianten und die Vektorgruppe C.14 (NV20–NV30, Zeile für Zeile) hängen daran. Ein Key 10
wäre Protokollversion 2 für etwas, wofür `v` bereits offen ist.

**Verworfen — die Prüfung in Layer 01.** Welche Prämisse zählt, ist Bedeutung. `01` ist
bedeutungsblind (A2); die Prüfung gehört zu dem Profil, das die Bedeutung setzt.

**Offen für die nächste Runde.** Welche Prämissen muss ein Claim nennen, damit die Nennung
nicht zur Zeremonie wird? Was gilt für einen abhängigen Claim, der keine nennt — folgenlos
nach `08 §2.2`, oder ein eigener Vermerk? Und trägt dieselbe Mechanik über `t_exp` hinaus,
also für jede Prämisse, deren Zustand sich ändern kann?

### D355 — Intervall-`now` zurückgestellt; der Befund ist die Asymmetrie darunter

**Die Frage.** Reicht als kleinere Variante ein Intervall statt eines Punktes, mit `LINKED`
bei Überlappung mit `t_exp`, wo der Verifizierer den dritten Ausgang über `temporal is None`
bereits kennt?

**Lesart zuerst.** Ein Intervall auf **`t`** wäre ein neues Feld und damit Protokollversion 2
(siehe D354, verworfene Alternative). Ein Intervall auf **`now`** kostet am Atom gar nichts —
`now` ist ein Parameter, kein Feld. Der Hinweis auf `temporal is None` zeigt auf die zweite
Lesart, und formal ist sie schön: `None` ist das Intervall von minus bis plus unendlich, jedes
heutige Verhalten wäre der entartete Fall.

**Beschluss: zurückgestellt.** Zwei Gründe. Erstens erzeugt es keine Kollision, sondern eine
Enthaltung — es verschiebt Fälle aus `ACTIVE`/`EXPIRED` nach `LINKED`, also in die sichere
Richtung, die bei fehlender Uhr ohnehin greift. Nach `08 §2.2` ist mehr Enthaltung genau die
Gegenrichtung zur Priorität. Zweitens ist es keine kleine Änderung, sondern deckt eine
Asymmetrie auf, die der Punktwert heute verbirgt.

**Der eigentliche Befund.** Überlappt das Intervall `t_exp`, zerfällt `_in_budget_set`
(`trust/groups.py:63`, heute eine Zeile `now <= claim.t_exp`) in zwei entgegengesetzte
konservative Richtungen:

| Menge | Frage | konservativ heißt | Unsicherheit |
|---|---|---|---|
| Kantensatz | gewährt der Vouch Vertrauen? | als abgelaufen behandeln | **raus** |
| Budget-Set | zählt er gegen `Σ n ≤ D`? | als nicht abgelaufen behandeln | **rein** |

Dieselbe Unsicherheit, derselbe Claim, dieselbe Funktion, entgegengesetzte Auflösung. Mit
einem Punkt-`now` fallen beide zusammen, und die Frage stellt sich nie. Die Asymmetrie ist
damit nicht Folge des Intervalls, sondern nur durch es sichtbar — sie ist die interessantere
Frage und wird als O60 geführt.

**Nebenbefund.** `trust/derive.py:39` und `trust/flow.py:30` nehmen `now: int`, nicht
`int | None`. Ein Gerät ohne Uhr bekommt keinen konservativen Trust-Wert, es bekommt keinen.
Das ist die harte Fassung von D350s zweitem Zeitregime: Trust ist nicht nur uhrgebunden,
sondern uhr-**pflichtig**, und zwar auf Typebene. `01` bleibt uhrenfrei berechenbar, `02a`
nicht.

**Verworfen — jetzt bauen.** Der Gewinn ist eine ehrlichere Enthaltung auf Geräten mit grober
Uhr. Der Preis ist eine normative Entscheidung über die Richtung in zwei Mengen, und die
gehört erst getroffen, wenn O60 beantwortet ist. In der Reihenfolge umgekehrt wäre es eine
Implementierung, die eine Spec-Frage nebenbei entscheidet.

### D356 — `time-regression-flagged` in den abhängigen Schichten

Aus D353. Ein neuer Zustand in `01` wirkt überall dort, wo eine Schicht Zustände aufzählt oder
erschöpfend verteilt. Drei Stellen, drei verschiedene Antworten.

**`02a §2.6` — in die Aufzählung.** Normativ folgt das bereits aus dem Satz darüber: ein Vouch
verlässt das Budget-Set ausschließlich durch `t_exp`. Eine rückwärts laufende Uhr ist kein
Lebenszyklus-Akt und gibt kein Budget frei — wörtlich die Begründung aus D135, dass der
Über-Commitment-Beweis auf Signaturen beruht und nicht auf Aktivität. Die Aufzählung wird
trotzdem nachgezogen, weil genau diese Differenz zwischen Satz und Aufzählung D135 gekostet hat
und der Abschnitt sie seither selbst als Warnung führt.

**`02-trust-flow.md` — bewusst unverändert.** Dort ist die Zugehörigkeit zum Budget-Set als
**Prädikat** formuliert und nicht als Aufzählung („nicht abgelaufen ist ein Prädikat, kein
Zustand"). Deshalb hat die Stelle D135 überstanden, und deshalb übersteht sie D353. Das steht
hier, damit ein späterer Lauf sie nicht aus Symmetriegefühl „vervollständigt" und dabei genau
den Fehler einbaut, gegen den die Formulierung gewählt wurde.

**`include_flagged` (D39) — unberührt.** Das ist ein **Autor**-Flag. `time-regression-flagged`
flaggt nach `01` Anhang B.1 den **Claim**; Vorgänger und Downstream bleiben unberührt. Die
Wirkung wäre ohnehin null, weil das Aktiv-Set `state == ACTIVE` verlangt und ein geflaggter
Claim dort nie ankommt.

**`03 §3.3.2` — `INDETERMINATE` mit eigenem Vermerk `OBLIGATION_TIME_REGRESSION`.** Bei einer
Zeitrückdatierung hat der Autor zwei unvereinbare Zeitbehauptungen signiert, und `obligation.t`
ist eine davon. Die Lage ist die dritte Spielart des bereits benannten Musters: bei `pending`
weiß der Verifizierer zu wenig, bei `equivocation_flagged` zu viel, hier widerspricht sich der
Autor. In allen drei Fällen wäre eine Aussage über die Schuld eine Behauptung ohne Deckung —
dieselbe Falschbeschuldigungsrichtung wie `02 §7`.

**Verworfen — `EXPIRED`.** Löschte die Schuld auf Grundlage genau der Zeitangabe, die soeben als
unzuverlässig erwiesen wurde. Der Schuldner profitierte von der eigenen kaputten Uhr; das ist
die gefährliche Richtung.

**Verworfen — weiter als `OPEN` führen.** Eine Schuldbehauptung auf ungedeckter Grundlage, und
damit dasselbe, was `03 §3.3.2` für die Gabelung bereits ausschließt.

**Verworfen — `ValueError`.** Der ist in `03 §3.3.2` für die falsche **Zuordnung** reserviert
(falsches Prädikat, falsches `N`, gar kein Claim). Hier liegt eine richtig zugeordnete, aber
unvollständige Lage vor, und dafür gibt es die Zustände.

**Nicht betroffen.** `verdict.py`, `membership.py`, `tally.py`, `chain.py` und `epoch.py` prüfen
sämtlich gegen `State.ACTIVE` und verteilen nicht erschöpfend; `credit.py` ist die einzige Stelle
mit `assert` auf die Restmenge und deshalb die einzige, die ohne diesen Eintrag gebrochen wäre.

### D357 — `t` in den Szenarien war Dekoration; die Welt wird umgetaktet, nicht die Erwartung

Der Lauf zu D353 hat `make check` an zwei bestehenden Szenarien rot gemacht: `s2` und `s3`. Das
Werkzeug hat gemeldet statt angepasst — richtig — und die Frage ins Register gegeben.

**Der Befund, unabhängig nachgerechnet.** Genau drei Stellen im gesamten Szenarienbestand
verletzen die Monotonie, und alle drei sind dieselbe: Anna signiert `accept-rules` mit `t = 1`,
dann `propose` mit `t = 2`, dann ihre `vote` wieder mit `t = 1`. In `s2` zweimal, weil das
Szenario zwei Welten aufsetzt, in `s3` einmal. Bruno und Chris tragen durchgehend `t = 1`,
liegen also im erlaubten Gleichstand und sind unberührt. Kein weiteres Szenario ist betroffen.
Die erste Messung des Supervisors meldete vier Dateien und war falsch: sie zählte über
`welt`-Schritte hinweg, und ein `welt`-Schritt setzt die Ketten zurück.

**Beschluss: die Szenariodaten werden umgetaktet, die `erwarte`-Blöcke bleiben unverändert.**
Annas Stimme bekommt ein `t` hinter ihrem eigenen Vorschlag. Gemessen: danach ist die Reihe
grün, ohne dass eine einzige Erwartung angefasst wurde. Das ist der Beleg dafür, dass die
Erwartungen richtig waren und die Welt falsch.

**Warum das kein Nachziehen ist.** Eine Erwartung nachzuziehen hieße, das Sollergebnis an ein
Istergebnis anzupassen. Hier wird eine **Eingabe** korrigiert, die eine Aussage trug, die vorher
bedeutungslos war und seit D353 einen Selbstwiderspruch bedeutet. Die Szenarien waren die
einzigen Stellen im Baum, an denen `t` frei gesetzt wurde — genau weil es folgenlos war. Dass
drei von ihnen dabei eine rückdatierte Stimme erzeugt haben, ist kein Zufall, sondern der
Normalfall bei einem Feld ohne Wirkung.

**Der eigentliche Befund liegt darüber.** Ein Feld, das nichts trägt, wird beliebig gefüllt, und
die beliebige Füllung wird erst sichtbar, wenn das Feld anfängt zu tragen. `08 §2.2` sagt, dass
ein Claim erst überprüfbar wird, wenn er kollidieren kann; die Umkehrung ist hier gemessen
worden. Jede künftige Verschärfung eines bisher wirkungslosen Feldes wird denselben Ausschlag
erzeugen, und der Ausschlag ist die gute Nachricht, nicht der Schaden.

**Verworfen — die Regel auf `vote@1` nicht anwenden.** Wäre eine Ausnahme genau für den Fall,
den D353 treffen will: eine Stimme, deren Zeitangabe vor dem Vorschlag liegt, auf den sie sich
bezieht. `04 §3.1` hält Governance uhrenfrei, und das bleibt so — die Monotonie braucht keine
Uhr, sie vergleicht zwei signierte Felder derselben Kette.

**Verworfen — die Szenarien als vor-D353-Artefakt einfrieren.** Ein Bestand, der die geltende
Spec verletzt und deshalb von der Prüfung ausgenommen wird, ist genau die stille Drift, gegen
die das Register gebaut ist.

### D358 — Ein Vektor muss den Zustand, den er belegt, im geteilten Korpus annehmen

Aus der Abnahme zu D353. NV32 sollte `time-regression-flagged` belegen und wurde nach Vorgabe
des Prompts auf `TV1` verkettet, in Bauform parallel zu TV2. Damit hat NV32 dasselbe
`(I, h_prev)` wie TV2 und ist dessen Equivocation-Geschwister. Gemessen im vollständigen
Vektorspeicher: NV32 ist `equivocation_flagged`, nicht `time_regression_flagged`, und **TV2
wechselt von `active` nach `equivocation_flagged`** — ein positiver Vektor, den niemand
angefasst hat.

Der Fehler stammt aus dem Prompt des Supervisors, nicht aus dem Lauf. Das Werkzeug hat die
Ursache zutreffend beschrieben und als Randnotiz geführt; die Einordnung als Defekt fehlte.
Dasselbe Muster wie in D352: der Bericht war inhaltlich richtig und in der Einordnung zu mild.

**Beschluss, normativ für Anhang C.** Ein Vektor, der einen Zustand belegt, **muss diesen
Zustand im vollständigen Vektorspeicher annehmen**, nicht nur in einem für ihn gebauten Store.
Anhang C ist der geteilte Anker der ganzen Spec-Reihe; ein Vektor, dessen Aussage nur unter
einer Teilmenge gilt, belegt nichts und verschiebt zugleich die Aussage seiner Nachbarn. Wo ein
neuer Vektor an eine bestehende Kette andockt, ist der Anker deshalb ein **kinderloses**
Kettenende, sofern nicht die Geschwisterschaft selbst der Gegenstand ist — wie bei NV3, der
Equivocation gegen TV1 zeigen soll und genau deswegen dort hängt.

**Reparatur, gemessen.** NV32 hängt an `TV6`, dem kinderlosen Ende von Alices Kette, mit
`t = 1700000409` gegen TV6s `t = 1700000410`. Danach ist TV2 wieder `active`, NV32 ist
`time_regression_flagged`, und es entsteht keine neue Geschwistergruppe.

**Was daran Abdeckung ist.** Der Kopplungstest über den Vektorspeicher wurde von keiner der
beiden Rücknahmeproben rot — weil `EQUIVOCATION_FLAGGED` vorher greift und NV32 dort nie in den
neuen Zweig läuft. Der Vektor war also im geteilten Korpus ungedeckt, und die Rücknahmeprobe
hat das sichtbar gemacht, ohne dass jemand danach gefragt hatte. Nach der Umhängung muss der
Kopplungstest NV32 tatsächlich als `time_regression_flagged` sehen; das ist ein eigener
Abnahmepunkt und kein Nebenprodukt.

**Verworfen — NV32 an TV1 lassen und nur im Test einen eigenen Store bauen.** Genau das tut der
Lauf heute, und genau deshalb ist der Defekt fast unsichtbar geblieben. Ein Vektor, der seinen
Zustand nur in einer eigens gebauten Umgebung annimmt, ist ein Test mit Vektor-Kostüm.

### D359 — Prüfregel 57 stand da und wurde nicht gelesen

Der Prompt zu D353 verlangte einen Test über den vollständigen Vektorspeicher, der `classify_all`
aufruft. Das Werkzeug hat gemeldet, dass die Rücknahmeprobe diesen Test nicht rot bekommen kann,
weil sie am Einschub in `verifier.py` ansetzt und der Test den Pfad in `index.py` nimmt — und hat
zu Recht nicht committet.

**Prüfregel 57 beantwortet das seit D278** und nennt beide Funktionen namentlich: wo zwei Pfade
gekoppelt geprüft werden, braucht jeder zusätzlich einen Träger, der den Wert behauptet. In
`00ah` war der Kopplungstest zwischen `classify` und `classify_all` grün, während beide Pfade
denselben falschen Zustand lieferten. Der Fall in `00bc` ist derselbe eine Ebene weiter: nicht
der Kopplungstest ohne Träger, sondern ein Träger für nur einen der beiden Pfade.

**Beschluss.** Der Volltest prüft beide Aufrufe auf demselben Store, und die Rücknahmeprobe wird
für jeden Einschub getrennt gefahren. Das ist **keine neue Regel**, sondern 57 angewandt. Beide
Proben treffen den Test jetzt; gemessen in `cbd61c7`.

**Der Befund ist der Ablauf, nicht die Regel.** Der Supervisor hat den Prompt geschrieben, ohne
`pruefregeln.md` zu öffnen, und die Einsicht anschließend neu hergeleitet — einschließlich der
Behauptung, der Kopplungstest sei „der falsche Ort", was 57 seit D278 genauer sagt. Prüfregel 38
verlangt, die Spec vor der Position zu lesen; Prüfregel 27 verlangt, jeden Verweis im Prompt zu
öffnen. Für die Prüfregeln selbst gab es keine solche Regel. Sie wird als **71** nachgezogen.

**Verworfen — eine neue Regel mit dem Inhalt von 57.** Zwei Nummern für dieselbe Aussage sind
schlimmer als eine: die zweite verdeckt, dass die erste gerissen wurde, und in drei Jahren ist
unklar, welche von beiden gilt. Genau der Zustand, gegen den das Register gebaut ist.

**Verworfen — 57 umformulieren oder erweitern.** Sie ist richtig, vollständig und trifft den Fall
wörtlich. Sie wurde nicht missverstanden, sondern nicht gelesen. Text zu ändern, der funktioniert
hat, verschiebt die Ursache auf die Regel statt auf den Ablauf.

**Was das über die Arbeitsteilung sagt.** Der Widerspruch kam vom Werkzeug, nicht vom Supervisor.
Die Anweisung, Rückfragen als Liste ans Ende zu melden statt unterwegs zu entscheiden, hat hier
zum zweiten Mal in dieser Sitzungsreihe einen Supervisor-Fehler gefangen — das erste Mal waren es
die roten Szenarien (D357). Beide Male hat das Werkzeug nicht committet und gefragt.
