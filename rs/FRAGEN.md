# Fragenliste — 00bv (Rust-Fassung Layer 02)

Jede Stelle, an der die Spec mehrdeutig, unvollständig oder widersprüchlich war
und eine Entscheidung nötig wurde. Reihenfolge ist die des Auffindens beim Bau.

## 1. Der ∞-Sentinel ist ein Wert, kein Literal

- **Adresse:** 02 §4
- **Frage:** Der Kasten „∞ ist ein Sentinel, kein Wert“ verlangt eine endliche Zahl,
  „die jeden erreichbaren Flusswert übersteigt“, und verweist für die Ausgestaltung auf
  `02a §2.8` — das bewusst zurückgehalten ist (STAND.md). Welche Zahl ist es?
- **Lesart:** `inf = Σ_{a ∈ Ankern} C(a) + 1`, je Profil zur Laufzeit gerechnet (u64,
  saturierend auf `u64::MAX`). Der Kasten selbst nennt die Schranke: „der Anker liegt auf
  jedem Pfad, also genügt die Summe der C(a) über die Anker“. Das `+1` macht das
  „übersteigt“ strikt; die Summe reicht zugleich für die `T*`-Kanten (jedes `C(t) ≤ C₀ =
  C(Anker)`).
- **Verworfen:** Ein festes Literal (z. B. `u64::MAX` oder `2⁶³`). Wird vom Kasten selbst
  verworfen: „ein festes Literal leistet das nicht, sobald C₀ gross genug ist“. Ebenso
  verworfen: ein `inf`-Wert, der nur `max_a C(a)` ist, weil er bei mehreren Ankern die
  Quellkanten nicht zuverlässig „übersteigt“.

## 2. `malformed` ist kein Klassifikationsergebnis, also keine `zustand`-Zeile

- **Adresse:** 01 Anhang B.1 / AUFTRAG
- **Frage:** `AUFTRAG` verlangt „`zustand` je Claim des Profils“. `01 Anhang B.1` (D278)
  sagt, `malformed` sei kein gehaltener Zustand — die Aufzählung führt acht Werte und nicht
  neun. Zählt ein strukturell ungültiger Claim zu „je Claim“?
- **Lesart:** Nur gehaltene (strukturell gültige) Claims erscheinen. Ein `malformed`-Claim
  wird verworfen und erzeugt keine `zustand`-Zeile, keinen Graphenbeitrag und keinen Vermerk
  in dieser Schicht. Die acht Zustände sind `pending`, `linked`, `active`, `revoked`,
  `superseded`, `expired`, `equivocation-flagged`, `time-regression-flagged`.
- **Verworfen:** Eine neunte Ausgabe „malformed“ je fehlerhaftem Claim. Widerspricht D278,
  wonach `malformed` die Verweigerung zu halten beschreibt und „nie entstehen kann“ als
  Klassifikationsergebnis.

## 3. Zustands-Vorrang: Widerruf/Supersede vor Ablauf

- **Adresse:** 02 §3.1 / 01 Anhang B.1
- **Frage:** Ein Claim kann zugleich widerrufen und (per `now > t_exp`) abgelaufen sein.
  Welcher Zustand wird gedruckt?
- **Lesart:** `revoked`/`superseded` gehen `expired` vor (Reihenfolge:
  equivocation → pending → time-regression → revoked → superseded → expired → active).
  D41 sagt ausdrücklich, ein widerrufener Claim erreiche „abgelaufen“ nie, „weil der
  Widerruf vorrangig ist“.
- **Verworfen:** `expired` vor `revoked`. Erzeugte genau den D41-Deadlock und verlöre die
  stärkere Diagnose „zurückgenommen“ zugunsten der schwächeren „abgelaufen“.

## 4. `linked` ist kein Endzustand

- **Adresse:** 01 Anhang B.1
- **Frage:** `linked` steht als Zeile der Zustandstabelle, aber sein Verhalten „weiter zu
  active/neutralisiert“ klingt transitiv. Kann ein Claim terminal `linked` bleiben?
- **Lesart:** `linked` ist transitiv (Kette bis zum Genesis aufgelöst) und geht immer in
  `active` oder einen neutralisierten Zustand über; als Endzustand tritt es nicht auf. Es
  bleibt aber Teil der achtwertigen Aufzählung (D278), daher im Enum geführt.
- **Verworfen:** `linked` als terminalen Zustand auszugeben. Ein gelinkter Claim ist nach
  den Regeln von §6 entweder aktiv, zeitlich ungültig, widerrufen, superseded oder
  geflaggt; ein Restfall „nur gelinkt“ existiert nicht.

## 5. `include_flagged` — geflaggte und über-committete Autoren tragen ihre Kante

- **Adresse:** AUFTRAG / 02 §8
- **Frage:** `02 §8` nennt als Vorgabe `include_flagged = False` (geflaggte Autoren tragen
  keinen Fluss). `AUFTRAG` legt fest: „hier gilt der andere Fall“. Was genau trägt dann?
- **Lesart:** Eine Vouch-Kante trägt genau dann, wenn ihr Zustand `active` oder
  `equivocation-flagged` ist (bei gültigem `n` und vorhandenem `t_exp`). Über-Commitment
  lässt Kanten **nicht** ausfallen (die D118-Regel wird nicht aktiviert). Die
  Budgetrechnung bleibt davon unberührt. `time-regression-flagged` bleibt strukturell
  „nicht trust-nutzbar“ (§6) — das ist kein Policy-Knopf und wird von `include_flagged`
  nicht eingeschaltet.
- **Verworfen:** Die Spec-Vorgabe `include_flagged = False` (Kanten geflaggter und
  über-committeter Autoren ausfallen lassen). Verworfen, weil der Auftrag ausdrücklich den
  anderen Fall verlangt, „weil der Mechanismus gemessen wird und nicht die Policy“.

## 6. `VOUCH_WITHOUT_TEXP`: keine Kante, aber Budgetbindung

- **Adresse:** 02 §10 / 02 §6.2
- **Frage:** `§10` zählt `VOUCH_WITHOUT_TEXP` zu den vier „Dekodier-Vermerken“ und sagt,
  ein solcher Claim „trägt nichts zum Fluss bei“. `§6.2` sagt zugleich, ein Vouch ohne
  `t_exp` „bindet Budget unbefristet“. Trägt er eine Kante und/oder Budget?
- **Lesart:** Ein Vouch ohne `t_exp` trägt **keine Kante** (kein `n_kante`-Beitrag, kein
  Graphen-Eintrag), trägt aber **Budget** (`n_budget` zählt, und zwar unbefristet, weil
  ohne `t_exp` nie ablaufend). Das ist konsistent: `§10` spricht vom Fluss, `§6.2` vom
  Budget; ein fehlendes `t_exp` entwertet das Vertrauen, entwertet aber nicht die
  Über-Commitment-Grundlage (die auf Signaturen beruht).
- **Verworfen:** (a) `VOUCH_WITHOUT_TEXP` als reine Kennzeichnung ohne Wirkung — verworfen,
  weil er dann nicht unter die vier „trägt nichts zum Fluss bei“-Vermerke gehörte. (b) Auch
  die Budgetbindung zu streichen — verworfen, weil `§6.2` sie ausdrücklich verlangt
  („unwiderruflich, REVOKED bleibt im Budget-Set“).

## 7. Budget-Set ist rein zeitlich, nicht lebenszyklusgebunden

- **Adresse:** 02 §3.1
- **Frage:** Gehören `pending`-, `revoked`-, `superseded`-, `equivocation-flagged`- und
  `time-regression-flagged`-Vouches ins Budget-Set?
- **Lesart:** Budget-Zugehörigkeit prüft allein `t_exp` gegen `now` (fehlendes `t_exp`
  bindet unbegrenzt), unabhängig vom Lebenszyklus-Zustand und von Flags. Alle strukturell
  gültigen, nicht per `t_exp` abgelaufenen Vouches tragen `n_budget` bei — pending,
  widerrufen, superseded und geflaggt eingeschlossen. Das folgt aus „Über-Commitment beruht
  auf Signaturen, nicht auf Aktivität“ und „die Budgetrechnung ist von Flags unberührt“.
- **Verworfen:** Budget an den Zustand `active` zu koppeln. Öffnete die Umgehung, einen
  Vorgänger zurückzuhalten (alle Vouches blieben pending und budgetfrei), und widerspricht
  „pending bindet Budget“.

## 8. Sortierung der Ausgabe ist Byte-Lexikografisch

- **Adresse:** AUFTRAG
- **Frage:** `AUFTRAG` verlangt Sortierung nach `claim_id`, `I`/`J`, `ziel`, `name`/`adresse`,
  ohne die Ordnung zu benennen.
- **Lesart:** Alle 32-Byte-Identifier werden als Bytefolgen lexikografisch aufsteigend
  geordnet (identisch zur aufsteigenden Kleinbuchstaben-Hex-Darstellung). `kante` nach
  `(I, J)`, `fluss` nach `ziel`, `befund` nach Vermerk-Name, dann Adresse (Bytes).
- **Verworfen:** Sortierung nach Einfüge-/Bau-Reihenfolge. Nicht deterministisch gegenüber
  der Eingabe und mit „sortiert“ unvereinbar.

## 9. `petgraph::ford_fulkerson` rechnet in `usize`

- **Adresse:** WERKZEUG
- **Frage:** Der Auftrag verlangt Kapazitätstyp `u64` durchgehend; `petgraph` 0.6.5
  `ford_fulkerson` operiert intern auf `usize`.
- **Lesart:** Auf der Zielplattform (64-bit) ist `usize == u64`, daher bleibt die
  Kapazität bitgleich `u64`; die Kantengewichte sind `u64`, die Rückgabe wird als `u64`
  geführt. Kein Wechsel des Kapazitätstyps. `ford_fulkerson` liefert `(MaxFlow,
  Vec<Fluss je Kante>)`; der quellseitige Min-Cut wird aus dem Residualgraphen (BFS von der
  Super-Quelle, vorwärts `cap − flow > 0`, rückwärts `flow > 0`) selbst bestimmt.
- **Verworfen:** Ein Wechsel auf `usize` im eigenen Code oder auf `maximum_flow`
  (petgraph ≥ 0.7). Beides ist im Auftrag ausdrücklich ausgeschlossen.

## 10. Exaktes `⌊C₀·γ^d⌋` in reiner `u64`-Arithmetik

- **Adresse:** 02 §3 / AUFTRAG
- **Frage:** „Einmal am Ende abgerundet, nicht pro Schritt“ verlangt das exakte
  `⌊C₀·γ_num^d/γ_den^d⌋`; `u128`/`i128` sind verboten, und die Zwischenprodukte
  `C₀·γ_num^d` können `u64` sprengen. Wie rechnet man ohne Überlauf und ohne
  Schritt-Rundung?
- **Lesart:** Für `γ_num = 1` (alle drei Eingabedateien): `C(x) = C₀ / γ_den^d`, exakt
  per wiederholter Ganzzahldivision — gültig wegen
  `⌊a/(b·c)⌋ = ⌊⌊a/b⌋/c⌋` für positive Ganzzahlen. Für allgemeines `γ_num` wird eine
  exakte Bruchform `(num, den)` mit GCD-Reduktion geführt und nur am Ende gerundet; fällt
  der Bruch unter 1, ist das Ergebnis 0. Die Kantenkapazität `⌊n·C/D⌋` nutzt die Zerlegung
  `n·(C/D) + (n·(C%D))/D`, damit `n·C` mit `C = 2⁶², n = 4` nicht überläuft.
- **Verworfen:** Iteratives Abrunden pro Schritt (verletzt die Norm und macht das Ergebnis
  abhängig von der Auswertungsreihenfolge); `u128` als Zwischenrechnung (im Auftrag
  verboten).

## 11. `FOREIGN_LIFECYCLE` ist ein vorgängerunabhängiger Sonderfall

- **Adresse:** 01 §6 / 01 §5.1
- **Frage:** Die Selbstenthaltene-Gültigkeit kennt genau einen speicherabhängigen Konjunkt:
  `ziel.I == C.I` bei `core/*`. Er kann erst nach dem Einlesen aller Claims geprüft werden.
  Wie wird er behandelt?
- **Lesart:** Nach dem Einlesen werden `core/revoke@1`/`core/supersede@1` verworfen, deren
  Ziel lokal bekannt ist und einem anderen Autor gehört (`FOREIGN_LIFECYCLE`). Ist das Ziel
  unbekannt, bleibt der Claim selbstenthalten gültig. Die Wirkung (revoked/superseded)
  entfaltet ein Lifecycle-Claim nur, wenn `ziel.I == C.I`.
- **Verworfen:** Die Fremd-Prüfung ganz wegzulassen (dann revoke/supersede auf fremde
  Ziele still zu ignorieren statt den Lifecycle-Claim zu verwerfen). Verworfen, weil §6
  Punkt 4 den Reject ausdrücklich fordert.

## 12. Ein superseded Mitglied tötet die Gruppe nicht

- **Adresse:** 02 §3.1
- **Frage:** Trägt eine Gruppe `(I, J)` mit mehreren Mitgliedern noch eine Kante, wenn nur
  *eines* davon superseded/revoked ist?
- **Lesart:** `n_kante = max n` über dem Aktiv-Set, `n_budget = max n` über dem Budget-Set.
  Ein superseded/revoked Mitglied verlässt das Aktiv-Set, bleibt aber im Budget-Set. Ein
  verbleibendes aktives Mitglied erhält die Kante; das Maximum „nicht die Summe“ bestimmt
  die Belegung. (In `tz02` Z3 tritt genau dieser Fall auf: zwei `CAROL→g1`-Vouches, einer
  superseded — die Kante bleibt mit `n_kante = 2` bestehen.)
- **Verworfen:** Die Kante zu streichen, sobald irgendein Mitglied neutralisiert ist.
  Verworfen, weil die Aggregation je Gruppe definiert ist und nur das Aktiv-Set zählt;
  eine Rücknahme einer einzelnen Erneuerung würde sonst eine weiterhin aktive Beziehung
  löschen.

## 13. In `Anhang C` tragen mehrere Byte-Vektoren eine inkonsistente Map-Größe

- **Adresse:** 01 Anhang C.5 / 01 Anhang C.10
- **Frage:** Die `bytes`-Zeilen von NV1, NV4, NV5 (und weiteren negativen Vektoren) tragen
  einen Map-Header mit der Kern-Schlüsselzahl (z. B. `a8`), enthalten aber zusätzlich `σ`
  (Schlüssel 9) — die Folge hat also einen Eintrag mehr, als der Header angibt. Welcher
  Header ist verbindlich?
- **Lesart:** Für die eigenen Tests wurde der Header auf die tatsächliche Eintragszahl
  korrigiert (die Signatur deckt ohnehin nur den Core, der vom äußeren Header unberührt
  bleibt). Auf den gebauten Rechner hat das keine Wirkung: seine Eingabe sind die 20
  Profile aus `vektoren/`, nicht die Vektoren aus `Anhang C`.
- **Verworfen:** Die `bytes`-Zeile wörtlich zu übernehmen und den Mehr-Eintrag als
  Restbytes (`MALFORMED_CBOR`) zu werten. Verworfen, weil das den gemeinten Mangel des
  jeweiligen Vektors (Version, `J.tag`, Genesis-Anker) überdeckt hätte und die Signatur
  über dem Core beweist, dass `σ` zur Folge gehört.
