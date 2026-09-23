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

# Nachzug

## 14. Änderung: Linking zählt nur den unmittelbaren Vorgänger

- **Adresse:** 01 §6 / 01 Anhang B.1
- **Vorher:** Ein Claim galt als `linked`, wenn seine ganze Kette bis zum Genesis
  aufgelöst war (rekursiv bis zum Anker).
- **Jetzt:** Ein Claim ist `linked`, wenn sein `h_prev` der Genesis-Anker ist oder sein
  unmittelbarer Vorgänger lokal bekannt ist und vom selben Autor stammt. Der Zustand des
  Vorgängers (auch `pending`) wirkt nicht stromabwärts.
- **Grund:** D437: „Es zählt nur der unmittelbare Vorgänger … gleich welchen Zustand `P`
  selbst hat, auch `pending`.“ Die Zeile zu `linked` in Anhang B.1 wurde entsprechend auf
  „unmittelbarer Vorgänger bekannt & gültig“ geschärft.

## 15. Änderung: Eine Gruppe ohne Budget-Set-Mitglied verschwindet

- **Adresse:** 02 §3.1
- **Vorher:** Eine Gruppe `(I, J)` erschien auch dann mit `n_budget = 0`, wenn alle ihre
  Mitglieder abgelaufen waren.
- **Jetzt:** Eine Gruppe besteht nur, solange mindestens eines ihrer Mitglieder im
  Budget-Set liegt. Sind alle abgelaufen, gibt es keine Gruppe — keine `gruppe`-Zeile und
  kein `budget`-Beitrag des Autors.
- **Grund:** D396: „Eine Gruppe besteht, solange mindestens eines ihrer Mitglieder im
  Budget-Set liegt … Daraus folgt `n_budget ≥ 1` für jede Gruppe.“

## 16. Änderung: Vouches ausserhalb des Budget-Sets werden nicht gelesen

- **Adresse:** 02 §10 / 02 §11.4
- **Vorher:** `v` wurde an jedem Scope-Vouch gelesen und ein Vermerk auch an einem
  abgelaufenen Vouch gesetzt.
- **Jetzt:** Nur Vouches im Budget-Set werden gelesen und vermerkt; ein Vouch ausserhalb
  trägt keinen Vermerk und keinen Beitrag.
- **Grund:** D400: „Die Ableitung liest `v` … nur an Vouches im Budget-Set … ausserhalb
  trägt ein Vouch ohnehin nichts bei, und ein Vermerk über ihn beschriebe keine Wirkung.“

## 17. Änderung: `VOUCH_WITHOUT_TEXP` nur bei gültigem `n`

- **Adresse:** 02 §10
- **Vorher:** `VOUCH_WITHOUT_TEXP` wurde an jedem Vouch ohne `t_exp` gesetzt, auch wenn
  `v` unlesbar war.
- **Jetzt:** Scheitert das Lesen von `v`, trägt der Vouch allein den Vermerk seines
  Lesefehlers; `VOUCH_WITHOUT_TEXP` fällt nur an einem Vouch mit gültigem `n`.
- **Grund:** D400: „`VOUCH_WITHOUT_TEXP` fällt nur an einem Vouch mit gültigem `n` … er
  trägt allein den Vermerk seines Lesefehlers.“

## 18. Änderung: `VOUCH_WITHOUT_TEXP` behält seine Kante

- **Adresse:** 02 §10 / 02 §6.2
- **Vorher:** Ein Vouch ohne `t_exp` trug keine Kante (nur Budget, unbegrenzt).
- **Jetzt:** Ein Vouch ohne `t_exp` behält seine Kante, sofern er aktiv ist; er bindet
  Budget weiterhin unbegrenzt.
- **Grund:** Die Tabelle in §10 führt die Kante für `VOUCH_WITHOUT_TEXP` als
  „unverändert“, und der Absatz „Fehlendes `t_exp`: ein Vermerk ohne Wirkung“ sagt: „er
  trägt seine Kante, wenn er im Aktiv-Set liegt“. Die alte Lesart (Eintrag 6) folgte dem
  früheren §10-Satz „trägt nichts zum Fluss bei“; der heutige Text hat ihn ersetzt.

## 19. Änderung: ∞-Sentinel = max(Σ C(a), |E⁺|) + 1

- **Adresse:** 02 §4
- **Vorher:** `inf = Σ C(a) + 1` (saturierend).
- **Jetzt:** `inf = max(Σ C(a), |E⁺|) + 1`, geprüft auf Überlauf.
- **Grund:** D381 verlangt, dass ∞ beide Läufe übersteigt; im Einheitslauf begrenzt
  `|E⁺|` den Fluss, nicht `Σ C(a)`. Der Text nennt `max(Σ C(a), |E⁺|) + 1` als hinreichend
  und zusätzlich die Summe aller endlichen Kapazitäten `+1`; beide sind hinreichend,
  gewählt wurde die engere D381-Formel.

## 20. Änderung: Der Einheitslauf arbeitet auf E⁺

- **Adresse:** 02 §8
- **Vorher:** Der Einheitslauf gab jeder Vouch-Kante Kapazität 1, auch einer subgranularen
  Kante mit `cap = 0`.
- **Jetzt:** Der Einheitslauf belegt nur Kanten aus `E⁺` (`cap ≥ 1`) mit Kapazität 1;
  subgranulare Kanten werden ausgeschlossen.
- **Grund:** D42: „Beide Läufe arbeiten auf demselben Kantensatz `E⁺` … mit 1 auf jeder
  Vouch-Kante wäre eine Kante mit `cap = 0` sonst von einer vollwertigen nicht zu
  unterscheiden.“

## 21. Änderung: `SUBGRANULAR_VOUCH` nur für erreichte Autoren

- **Adresse:** 02 §10
- **Vorher:** `SUBGRANULAR_VOUCH` wurde an jeder Kante mit `cap = 0` gesetzt, auch wenn der
  Autor unerreichbar war.
- **Jetzt:** Der Vermerk fällt nur an einer Kante, deren Autor die Breitensuche erreicht
  hat; ein unerreichbarer Autor mit `C = 0` ist der strukturelle Fall und kein Vermerk.
- **Grund:** D439: „Der Vermerk setzt einen erreichten Autor voraus … Für einen
  unerreichbaren Autor ist `C = 0` der strukturelle Fall aus §3 und kein Vermerk.“

## 22. Änderung: Überlauf wird gemeldet statt saturiert

- **Adresse:** AUFTRAG
- **Vorher:** Der ∞-Sentinel und die allgemeine `C(x)`-Bruchrechnung saturierten auf
  `u64::MAX`.
- **Jetzt:** Jede Rechnung, die `u64` sprengt, hält das Programm an und meldet Stelle und
  beteiligte Werte (geprüfte Addition und Multiplikation). Keine Saturierung, kein
  Abfangen.
- **Grund:** AUFTRAG verlangt, einen Überlauf zu melden statt abzufangen; der Nachzug hebt
  die Saturierung ausdrücklich auf („Keine Saturierung, nirgends. Kein Abfangen eines
  Überlaufs.“).

## 23. Änderung: Überlappende Anker und Ziele werden zurückgewiesen

- **Adresse:** 02 §11.3
- **Vorher:** Überlappende Anker/Ziele wurden nicht geprüft; die Auswertung rechnete einen
  Wert.
- **Jetzt:** Überschneiden sich Anker und Ziele, weist das Programm die Anfrage zurück
  (Fehlermeldung, kein Block).
- **Grund:** §11.3: „Anker und Ziele einer Anfrage sind disjunkt. Überschneiden sie sich …
  weist die Auswertung die Anfrage zurück, statt einen Wert zu liefern.“

## 24. Änderung: Parameter ausserhalb der Bereiche → keine Auswertung

- **Adresse:** 02 §11.2
- **Vorher:** Parameter wurden nicht auf ihren Bereich geprüft.
- **Jetzt:** Liegen `C₀`, `γ_num`, `γ_den` oder `D` ausserhalb `C₀ ≥ 1`,
  `0 < γ_num < γ_den`, `D ≥ 1`, wird die Anfrage zurückgewiesen.
- **Grund:** §11.2: „Ausserhalb dieser Bereiche gibt es keine Auswertung.“

## Einträge 1 bis 13

- 1: beantwortet (02 §4) — D381 nennt die Belegung `max(Σ C(a), |E⁺|) + 1` ausdrücklich.
- 2: beantwortet (01 Anhang B.1) — D278 steht unverändert: `malformed` bleibt kein Klassifikationsergebnis.
- 3: beantwortet (02 §3.1) — D41 bleibt: der Widerruf ist vorrangig vor dem Ablauf.
- 4: beantwortet (01 Anhang B.1) — „weiter zu active/neutralisiert“ bleibt; nur die Linked-Bedingung wurde durch D437 geschärft.
- 5: beantwortet (AUFTRAG) — der Auftrag verlangt weiterhin den anderen Fall (`include_flagged` wirkt nicht).
- 6: beantwortet (02 §10) — der heutige Text entscheidet anders: ohne `t_exp` bleibt die Kante, nur das Budget bindet unbegrenzt.
- 7: beantwortet (02 §3.1) — die Tabelle nennt `equivocation-flagged` und `time-regression-flagged` jetzt ausdrücklich im Budget-Set.
- 8: beantwortet (02 §11.1) — „Deterministisch … wo die Reihenfolge … berühren kann, wird vorher sortiert.“
- 9: beantwortet (WERKZEUG) — `ford_fulkerson` in `usize`; auf 64-bit bitgleich `u64`, keine Änderung.
- 10: beantwortet (02 §11.1) — „keine Gleitkomma- und keine Bruchrechnung … `C(x)` wird einmal am Ende gerundet.“
- 11: beantwortet (01 §6) — der vorgängerunabhängige Konjunkt bleibt benannt.
- 12: beantwortet (02 §3.1) — „`n_kante` = max n über Aktiv-Set, `n_budget` = max n über Budget-Set.“
- 13: beantwortet (01 Anhang C.0) — D396 klärt, was `bytes` trägt (eigene σ-Zeile ⇒ Core, sonst Wire-Form).
