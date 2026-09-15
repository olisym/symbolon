# FRAGEN.md — Entscheidungen und offene Stellen

Jede Stelle, an der die Spec mehrdeutig, unvollständig oder widersprüchlich war und eine
Entscheidung nötig wurde, ist hier festgehalten. Format je Eintrag: Spec-Abschnitt, die
offene Frage, die gewählte Lesart, die verworfene Lesart und der Grund der Verwerfung.

---

## 1. Identitäten in der Ausgabe: Hex oder `labels`?

- **Spec:** `AUFTRAG.md` („Schnittstelle") und das Feld `labels` in `tp02.json`.
- **Frage:** Zeigt die Ausgabe `gruppe`/`kante`/`fluss`/`budget`/`schnitt` die Identitäten
  als rohe Hex-Schlüssel oder als die Namen aus `labels` (ALICE, BOB, …)?
- **Lesart:** **Hex-Schlüssel** (32 Byte, lowercase). `labels` ist nur eine Lesehilfe für
  den Menschen und fließt nicht in die Ausgabe ein. Grundlage: „Zeilen, Felder durch ein
  Leerzeichen getrennt, **Hex klein**", und die Sortiervorschriften sprechen von `claim_id`,
  `I`, `J`, `ziel`, `identity`, `adresse` — alles hex-förmige Werte. `befund <name>` und
  `profil <name>` sind die einzigen nicht-hex Felder, und die tragen ausdrücklich `<name>`.
- **Verworfen:** Namen aus `labels`. Sie wären zwar „lesbarer", aber die explizite
  Vorgabe „Hex klein" plus die Sortierung über hex-Werte macht Hex zur einzigen eindeutig
  deterministischen Wahl.

## 2. `schnitt`: welche Seite des minimalen Schnitts?

- **Spec:** `AUFTRAG.md` („schnitt nennt die Identitäten des minimalen Schnitts … Welche
  Seite gemeint ist, entscheide selbst"); `02-trust-flow.md` §4 (Min-Cut-Bound, „Grenze").
- **Frage:** Der minimale Schnitt zerlegt den Flussgraphen in Quell- und Senkenseite. Welche
  Identitäten werden gedruckt, und für welche Abfrage wird der Schnitt gerechnet?
- **Lesart:** Der Schnitt wird für die **`simultan`**-Abfrage (Multi-Sink über alle Ziele)
  gerechnet. Gedruckt wird die **Quellseite**: eine Identität `x` liegt auf der Quellseite,
  wenn ihr Eingangsknoten `x_in` von der Super-Quelle `S*` im Residualgraphen erreichbar ist
  (Standard-Charakterisierung der Quellseite über eine BFS im Residualnetz). Die Senkenseite
  ist das Komplement. Sortierung aufsteigend, leere Zeile erlaubt.
- **Verworfen:** (a) die **Grenze** (nur die Ehrlichen-Knoten, deren Budget- oder Vouch-Kante
  den Schnitt trägt, §4 „Grenze"). Sie ist semantisch reicher, aber die Aufforderung „Welche
  *Seite* gemeint ist" benennt ausdrücklich eine Seite, keine Kantenmenge. (b) Die Senkenseite
  (die abgeschnittenen Ziele) — die Quellseite ist die trust-tragende Menge und die
  natürlichere Antwort. **Hinweis:** Da ein Anker immer auf der Quellseite liegt, ist die
  Quellseite für diesen Vektorsatz nie leer; „eine leere Zeile ist erlaubt" ist eine
  allgemeine Format-Zusage (z. B. leerer Ankersatz).

## 3. Profil-Feld `t_exp` (Top-Level) wird nicht gebraucht

- **Spec:** `AUFTRAG.md` („`now`, `t_exp` — ganze Zahlen"); `02-trust-flow.md` §6.2.
- **Frage:** Wozu dient das Top-Level-Feld `t_exp` des Profils, wenn jeder Vouch sein eigenes
  `t_exp` trägt?
- **Lesart:** Es wird **nicht ausgewertet**. Alle Claims des Vektorsatzes tragen ihr eigenes
  `t_exp` (= 5000); `now` = 1000 kommt aus der Datei. Das Top-Level-`t_exp` ist die
  Policy-Maximallaufzeit aus §6.2, die nur griffe, wenn ein Vouch ohne eigenes `t_exp`
  vorläge — was hier nicht vorkommt.
- **Verworfen:** Das Top-Level-`t_exp` als Ersatz-Default für Vouches ohne `t_exp` zu setzen
  (und damit `VOUCH_WITHOUT_TEXP` zu unterdrücken). Verworfen, weil kein Claim ohne `t_exp`
  vorliegt und die Spec die Abwesenheit eines Feldes nicht über einen Profil-Default
  überschreibt; die Stelle ist als unbeobachtbar vermerkt.

## 4. `kante` schließt kapazitätslose (subgranulare) Kanten ein

- **Spec:** `02-trust-flow.md` §2 („Trägt kein Gruppenmitglied eine gültige Belegung …
  entsteht keine Kante"), §3.1/§10 (`SUBGRANULAR_VOUCH`).
- **Frage:** Erscheint eine Kante mit `cap = 0` (weil `n_kante·C(I) < D`) als `kante`-Zeile?
- **Lesart:** **Ja.** `kante` druckt jede Gruppe mit `n_kante ≥ 1` (eine gültige Belegung im
  Aktiv-Set), unabhängig davon, ob die Kapazität auf 0 fällt. Die Zeile trägt dann
  `cap = 0`, und es entsteht ein `SUBGRANULAR_VOUCH`-Vermerk. Die Basis-Kante existiert
  (§2), sie gehört nur nicht zu `E⁺` und trägt keinen Fluss.
- **Verworfen:** Nur `cap ≥ 1`-Kanten zu drucken. Verworfen, weil §2 die Kante an der
  gültigen Belegung festmacht, nicht an der Kapazität, und weil der Vermerk
  `SUBGRANULAR_VOUCH` genau für diese Fälle definiert ist (Profil E zeigt sie real).

## 5. Gruppe ohne gültige Belegung erzeugt keine Zeile

- **Spec:** `02-trust-flow.md` §3.1.
- **Frage:** Bildet eine `(I, J)`-Menge, deren sämtliche Vouches ein unlesbares/ungültiges
  `v` tragen, eine `gruppe`-Zeile?
- **Lesart:** **Nein.** Eine Gruppe wird nur geführt, wenn `n_budget ≥ 1` (mindestens ein
  Budget-Mitglied trägt ein gültiges `n`). `n_budget`/`n_kante` sind das Maximum über die
  gültigen Mitglieder.
- **Verworfen:** Gruppen mit `n_budget = 0` trotzdem zu drucken. Verworfen, weil §3.1 einen
  Vouch ohne gültige Belegung „keine Kante und keinen Budget-Beitrag" zuschreibt; eine leere
  Gruppe ist keine Gruppe. (Im Vektorsatz tritt der Fall nicht auf.)

## 6. `budget`-Summe = Summe der `n_budget`

- **Spec:** `02-trust-flow.md` §3.1 („`Σ_J n_budget ≤ D`"), `AUFTRAG.md` („budget <I>
  <summe> <verdikt>").
- **Frage:** Was ist `summe`?
- **Lesart:** `summe = Σ_J n_budget` über alle Gruppen des Autors im Budget-Set.
  `verdikt = over` gdw. `summe > D`. Das Budget-Set ist rein zeitlich definiert
  (`now ≤ t_exp`, fehlendes `t_exp` bindet unbegrenzt), unabhängig vom Lebenszyklus-Zustand
  (§3.1, D41): eingeschlossen sind also `pending`, `revoked`, `superseded` und flagged.
- **Verworfen:** `summe = Σ_J n_kante` (nur aktive Kanten). Verworfen, weil das Budget die
  **Haftung** über signierte, auch inaktive Vouches misst und die Spec ausdrücklich
  Aktiv-Set ⊆ Budget-Set trennt.

## 7. `include_flagged = True` (gegen den Spec-Default)

- **Spec:** `AUFTRAG.md` („Alle Abfragen laufen so, dass Vouches geflaggter oder
  über-committeter Autoren ihre Kante tragen … das Budget ist davon unberührt");
  `02-trust-flow.md` §8 („`include_flagged`, Default *nein*").
- **Frage:** Tragen Kanten über-committeter (oder equivocation-gefragter) Autoren Fluss?
- **Lesart:** **Ja** (`include_flagged = True`). Der AUFTRAG schreibt den vom Spec-Default
  abweichenden Fall vor. Die Budgetrechnung bleibt unberührt: ein über-committeter Autor
  erhält weiterhin `verdikt = over` und den Vermerk `OVERCOMMITTED_AUTHOR`, aber seine
  Kanten tragen mit ihrer normal berechneten Kapazität.
- **Verworfen:** Der Spec-Default (`include_flagged = False`, Kanten fallen aus). Verworfen,
  weil der AUFTRAG ausdrücklich „den anderen Fall" anordnet („der Mechanismus wird gemessen
  und nicht die Policy").

## 8. `VOUCH_WITHOUT_TEXP` feuert bei fehlendem `t_exp` des Vouch

- **Spec:** `02-trust-flow.md` §10, §6.2, §3.1.
- **Frage:** Wann genau entsteht der Vermerk `VOUCH_WITHOUT_TEXP`, und unterdrückt ein
  Policy-Default ihn?
- **Lesart:** Der Vermerk entsteht genau dann, wenn ein Vouch **kein** eigenes `t_exp` trägt
  (`texp == Nothing`). Ein Profil-/Policy-Default wird nicht als Ersatz herangezogen.
  Der Vouch behält seinen Budget-Beitrag („fehlendes `t_exp` bindet unbegrenzt", §3.1).
- **Verworfen:** Das Top-Level-`t_exp` als Default einzusetzen und den Vermerk zu
  unterdrücken. Verworfen, weil kein Claim des Satzes ohne `t_exp` ist (der Vermerk feuert
  real nie) und die Spec die Abwesenheit als unbefristete Bindung, nicht als Default-Aufruf
  beschreibt.

## 9. Quelle der Einzelabfrage ist `S*` (Ankerset), Senke `T_in`

- **Spec:** `02-trust-flow.md` §4 („trust(s → T) = maxflow(s_in → T_in)"), §6.3 (Ankerset).
- **Frage:** Für `fluss <ziel>` und `simultan` — woran hängt die Quelle?
- **Lesart:** Uniform ein Super-Source `S*` mit ∞-Kanten auf jedes `a_in` des Ankersets
  (hier stets ein Anker). Die interne Kante des Ankers `C(a)` liegt damit auf dem Pfad
  (§4: Voraussetzung des Beweises). Einzelabfrage: Senke = `T_in` des einen Ziels;
  `simultan`/`disjunkt`: Super-Senke `T*` mit ∞-Kanten von jedem Ziel-`g_in`.
- **Verworfen:** Quelle direkt an `a_out`. Verworfen — §4 zeigt explizit, dass dies den
  Min-Cut-Satz verletzt („drei Kanten … simultan 48 gegen Schranke 16").

## 10. `linked` wird nie als Endzustand gedruckt

- **Spec:** `01-claim-atom.md` Anhang B.1 (Zustände inkl. `linked`).
- **Frage:** Erscheint `linked` als `zustand`-Ausgabe?
- **Lesart:** **Nein.** `linked` ist ein Durchgangszustand; jeder verlinkte Claim endet in
  `active` oder einem neutralisierten Zustand (`expired`, `revoked`, `superseded`,
  `equivocation-flagged`, `time-regression-flagged`). Terminalszustände sind die acht Zeilen
  aus B.1 abzüglich `linked`; zusätzlich `malformed` für abgelehnte Claims.
- **Verworfen:** `linked` als eigenen Endzustand auszugeben. Verworfen, weil B.1 `linked`
  ausdrücklich als Übergang („weiter zu active/neutralisiert") beschreibt.

## 11. `malformed` und der `claim_id` abgelehnter Claims

- **Spec:** `01-claim-atom.md` Anhang B.1 („`malformed` ist kein Klassifikationsergebnis"),
  `AUFTRAG.md` („zustand je Claim des Profils").
- **Frage:** Was wird für einen strukturell abgelehnten Claim gedruckt, wenn dessen
  `claim_id` gar nicht berechenbar ist?
- **Lesart:** Abgelehnte Claims erhalten den Zustand `malformed`. Ist der Core dekodierbar
  und kanonisch re-serialisierbar (z. B. `BAD_SIGNATURE`), wird der `claim_id` aus dem
  kanonisierten Core berechnet und mit `malformed` gedruckt. Ist schon das CBOR nicht
  dekodierbar, existiert kein `claim_id`; die Zeile entfällt. **Im Vektorsatz kommt kein
  `malformed` vor** (alle acht Profile tragen ausschließlich kanonische, korrekt signierte
  Vouches); die Regel ist nur der Vollständigkeit halber implementiert.
- **Verworfen:** Einen Ersatz-`claim_id` (z. B. Hash der Rohbytes) zu erfinden. Verworfen,
  weil `claim_id` normativ als Inhaltsadresse des Cores definiert ist.

## 12. Kapazitäten des `disjunkt`-Laufs

- **Spec:** `02-trust-flow.md` §8 („Pfad-Disjunktheit … Einheitskapazitäten").
- **Frage:** Welche Kapazitäten trägt der disjunkte Lauf genau?
- **Lesart:** Anker-interne Kante `a_in → a_out = ∞` („Endpunkte werden nicht gespalten"),
  interne Kante jedes Nicht-Ankers `= 1`, jede Vouch-Kante `= 1`, Ziel-`g_in → T* = ∞`.
  Knoten- und Kantenmenge sind identisch mit dem normalen Lauf (`E⁺`, erreichbare Knoten);
  nur die Kapazitäten werden durch 1 ersetzt. Das liefert die Zahl knoten-disjunkter Pfade
  vom Ankerset zur Zielmenge.
- **Verworfen:** Auch die Anker-interne Kante auf 1 zu setzen. Verworfen — §8 sagt
  ausdrücklich, die Anker-Kante trage ∞, „sonst wäre die Zahl von einem einzelnen Anker aus
  trivial 1".

## 13. Sortierung der Ausgabezeilen

- **Spec:** `AUFTRAG.md` („sortiert nach …").
- **Frage:** Nach welcher Ordnung werden `zustand`, `gruppe`, `budget`, `kante`, `fluss`,
  `befund` sortiert?
- **Lesart:** Byte-lexikographisch über die Hex-Werte (`claim_id`, `I`, `J`, `ziel`,
  `adresse`), also numerisch über die rohen 32-Byte-Werte. `befund` sortiert nach
  `(name, adresse)`. `fluss` nach `ziel`.
- **Verworfen:** Sortierung über die `labels`-Namen. Verworfen, weil die Ausgabe Hex ist
  (Eintrag 1) und die Spec nach `claim_id`/`I`/`J` sortiert.

## 14. Scope-Partition ist trivial erfüllt

- **Spec:** `02-trust-flow.md` §2 („Es gibt einen Graphen pro N").
- **Frage:** Müssen Claims nach Scope gefiltert werden?
- **Lesart:** Jedes Profil enthält ausschließlich Vouches mit demselben `N` (= Profil-`scope`).
  Die Partition ist damit trivial; gefiltert wird nur auf `isVouch` (Prädikatname `vouch@1`,
  `J.tag == 1`). Eine zusätzliche Scope-Filterung wäre wirkungslos.
- **Verworfen:** Keine Filterung überhaupt. Verworfen — die Vouch-Erkennung bleibt nötig,
  weil Layer 2 nur `vouch@1`-Claims verarbeitet (der Vektorsatz enthält zwar nur Vouches,
  der Code ist aber allgemein gehalten).

## 15. `n_budget`/`n_kante` als Maximum über die Gruppenmitglieder

- **Spec:** `02-trust-flow.md` §3.1 („Maximum, nicht Summe").
- **Frage:** Wie werden mehrere Vouches derselben `(I, J, N)`-Gruppe aggregiert?
- **Lesart:** `n_budget = max n` über die Budget-Set-Mitglieder, `n_kante = max n` über die
  Aktiv-Set-Mitglieder (jeweils nur über gültig dekodierte `n`). „Maximum, nicht Summe"
  (§3.1). Aktiv-Set ⊆ Budget-Set ⇒ `n_kante ≤ n_budget`.
- **Verworfen:** Summe der `n`. Verworfen — die Spec schließt die Summe explizit aus (sonst
  wäre die Erneuerung eines Vouch ein Beweis gegen den Autor und zwei aktive Vouches trügen
  doppelte Kapazität).

## 16. Exakte Ganzzahl-Arithmetik für `C(x)` und `cap`

- **Spec:** `02-trust-flow.md` §3, §8.
- **Frage:** Wie wird der Decay `C(x) = ⌊C₀·γ^d⌋` exakt gerechnet?
- **Lesart:** `C(x) = (C₀ · γ_num^d) \`div\` γ_den^d` in `Integer`-Arithmetik — einmal am
  Ende gerundet, nie pro Schritt. `cap(I→J) = (n_kante · C(I)) \`div\` D`. Kein Float
  (der „harte" Blick bleibt ganzzahlig; `D ≥ C₀` und Abrunden erhalten das).
- **Verworfen:** Schrittweises Runden oder Float. Verworfen — §3 macht das Ergebnis sonst
  von der Auswertungsreihenfolge abhängig, und §8 zeigt das Doppelrundungs-Gegenbeispiel.

## 17. `SUBGRANULAR_VOUCH`-Adresse

- **Spec:** `02-trust-flow.md` §3.1, §10.
- **Frage:** Welcher `claim_id` adressiert den Vermerk, wenn mehrere Mitglieder `n = n_kante`
  tragen?
- **Lesart:** Die lexikographisch kleinste `claim_id` unter den Gruppenmitgliedern mit
  `n == n_kante` (§10: „bei Gleichstand die lexikographisch kleinste").
- **Verworfen:** Der erste (zeitliche) Träger. Verworfen — die Spec schreibt die
  lexikographisch kleinste `claim_id` vor (deterministisch, unabhängig von Ankunftsreihenfolge).

## 18. ∞-Sentinel für Flussgraph-Kanten

- **Spec:** `02-trust-flow.md` §4, §8 (Super-Source/Super-Senke mit ∞).
- **Frage:** Welcher Wert repräsentiert „∞"?
- **Lesart:** `10^18` (`Integer`). Sicher groß gegenüber jeder endlichen Kapazität des
  Vektorsatzes (alle `C ≤ 16`). Jede ∞-Kante mündet in eine endliche Kante (Anker-Budget bzw.
  Ziel-`in`), so dass der Sentinel nie als Flusswert erscheint.
- **Verworfen:** `maxBound :: Int` o. ä. Verworfen — `Integer` ist unbegrenzt, und ein
  versehentlich durchgereichter ∞-Wert wäre als absurd groß erkennbar, statt still zu
  überlaufen.

## 19. Equivocation/Time-Regression implementiert, im Vektorsatz nicht beobachtet

- **Spec:** `01-claim-atom.md` §4, §6, Anhang B.1.
- **Frage:** Treten `equivocation-flagged` oder `time-regression-flagged` im Vektorsatz auf?
- **Lesart:** Beide Zustände sind implementiert (Equivocation über `(I, h_prev)`-Gruppen,
  Time-Regression über `C.t < P.t` bei bekanntem Vorgänger). Im Vektorsatz tritt keiner auf:
  alle Claims sind `active`. Das ist konsistent mit dem Zweck des Satzes (Trust-Flow-Fälle,
  keine Equivocation-Fälle).
- **Verworfen:** Beide Prüfungen wegzulassen. Verworfen — Layer 1 verlangt die
  Zustandsklassifikation vollständig, auch wenn der Satz sie nicht ausreizt.
