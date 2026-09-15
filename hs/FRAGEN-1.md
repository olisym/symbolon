# FRAGEN.md

Entscheidungen an Stellen, an denen `spec/01-claim-atom.md` oder
`spec/02-trust-flow.md` mehrdeutig, unvollständig oder mit dem Auftrag
nicht wörtlich vereinbar sind. Kein Eintrag ist eine Rückfrage.

---

## 1. 02 §4 / Auftrag `schnitt` — welche Seite des Min-Cuts

**Offen:** Der Auftrag verlangt die Identitäten des minimalen Schnitts,
sagt aber nicht, ob Quellseite, Senkenseite oder die Knoten auf der
Schnittkante gemeint sind. `02` definiert den Satz, nicht die Ausgabeform.
`02a §3` ist zurückgehalten.

**Lesart:** Quellseite im Residuengraphen nach `maxFlowgraph`: BFS von `S*`
über Kanten mit Restkapazität `cap − flow` vorwärts und `flow` rückwärts.
Eine Identity erscheint, wenn ihr `in`- oder `out`-Knoten erreichbar ist.
`S*` und `T*` selbst werden nicht gedruckt. Die Menge kommt aus der
**simultanen** Abfrage, nicht aus einer Einzelabfrage und nicht aus
`disjunkt`.

**Verworfen:** Senkenseite (würden die Ziele die Schnittliste dominieren).
Verworfen, nur die Grenz-Identitäten mit einer Residuenkante auf die
andere Seite — `02` spricht vom Min-Cut als Kapazität, nicht als
Knotenliste; die Quellseite ist die übliche und die in `02a §3`
erwartete Lesart.

---

## 2. 02 §3 / §4 — Kodierung von ∞

**Offen:** Super-Source-Kanten `S* → a_in` und Multi-Sink-Kanten
`gᵢ_in → T*` tragen ∞. `fgl` rechnet über `Num b`; `Integer` hat kein ∞.

**Lesart:** `INF = 1 + Summe aller endlichen Kapazitäten` im jeweiligen
Graphen (interne Kanten + Vouch-Kanten, vor dem Einsetzen der INF-Kanten).
Eine INF-Kante bindet dann nie.

**Verworfen:** `maxBound` auf `Int` (überläuft und wäre ein eigener Solver).
Verworfen, `Double`/`MaxFlow2` (Auftrag verbietet das). Verworfen, ein
festes Literal wie `10^9` — bei großem `C0` könnte es binden.

---

## 3. Auftrag Ausgabe — Labels gegen Hex

**Offen:** Der Auftrag sagt „Hex klein“ und zugleich, Labels seien „zur
Lesbarkeit der Ausgabe“.

**Lesart:** Identitäten (`I`, `J`, Flussziele, Schnitt, `OVERCOMMITTED_AUTHOR`)
werden als Label gedruckt, falls der öffentliche Schlüssel in `labels`
steht, sonst als Kleinbuchstaben-Hex. `claim_id` und die übrigen Vermerk-
Adressen bleiben Hex. Sortierung der Rechenausgänge intern nach Rohbytes;
`fluss` und `schnitt` zusätzlich nach gedrucktem Namen, damit die Blöcke
stabil lesbar sind.

**Verworfen:** Überall Hex (dann sind die mitgelieferten Labels tot).
Verworfen, Sortierung nur nach Label-String intern in der Rechnung — die
Rechnung kennt keine Namen.

---

## 4. Auftrag `kante` — Kanten mit `cap = 0`

**Offen:** `02 §2` erzeugt keine Kante, wenn kein Gruppenmitglied eine
gültige Belegung trägt. Ob `cap = 0` bei gültigem `n_kante` (unerreichbarer
Autor oder Granularitätsboden) trotzdem als `kante`-Zeile erscheint, steht
nicht im Auftrag, der `inf` für unerreichbare Autoren verlangt.

**Lesart:** Jede Gruppe mit `n_kante > 0` erzeugt eine `kante`-Zeile, auch
bei `cap = 0`. Unerreichbare Autoren: `d` und `C` als `inf`. Genau das
macht `inf` in der Zeile beobachtbar.

**Verworfen:** Nur `E+` (`cap ≥ 1`) zu drucken — dann gäbe es kein `inf`.

---

## 5. 02 §8 `include_flagged` — welche Zustände Kanten tragen

**Offen:** Default ist *nein*; der Auftrag setzt *ja*. Die Spec nennt
`equivocation-flagged` und Über-Commitment. `time-regression-flagged`,
`pending`, `revoked`, `superseded`, `expired` erwähnt sie dort nicht.

**Lesart:** Kanten aus `active` **und** `equivocation-flagged` (beide
Fork-Geschwister). Über-Commitment entfernt keine Kante. `time-regression-flagged`
trägt **keine** Kante (01 §6: nicht für trust-gewährende Zwecke).
`pending` trägt keine Kante (02 §2). Widerruf, Supersede, Ablauf tragen
keine Kante.

**Verworfen:** Alle gehaltenen Vouches als Kante (über-Vertrauen bei
Widerruf). Verworfen, Equivocation-Claims selbst wegzulassen — dann hätte
der Knopf `include_flagged` für Equivocation keine Wirkung auf genau die
Claims, die den Beweis tragen, und Downstream-Claims auf anderen
`(I, h_prev)` wären die einzige Restwirkung.

---

## 6. 02 §3.1 Budget-Set und geflaggte Claims

**Offen:** Das Budget-Set ist „nicht abgelaufen“, inkl. widerrufen,
supersediert, pending. Equivocation und Zeitregression fehlen in der
Tabelle.

**Lesart:** Zugehörigkeit ist das Prädikat `now ≤ t_exp` (fehlendes `t_exp`
bindet unbegrenzt), unabhängig vom Lebenszyklus-Zustand. Geflaggte Vouches
binden Budget, sofern `n` lesbar ist.

**Verworfen:** Budget an `active` zu knüpfen (D41 / D372: das wäre der
Deadlock, den der Auftrag ausdrücklich nicht wiederholen soll).

---

## 7. 02 §10 — `VOUCH_WITHOUT_TEXP` und der Satz „trägt nichts bei“

**Offen:** Die vier „ersten Lagen“ inkl. `VOUCH_WITHOUT_TEXP` „tragen nichts
zum Fluss bei“. `02 §6.2` sagt zugleich, fehlendes `t_exp` binde Budget
unbefristet.

**Lesart:** `VOUCH_WITHOUT_TEXP` ist ein Vermerk und **kein** Skip. Unlesbares
oder ungültiges `n` (`UNPARSABLE_VOUCH_PAYLOAD`, `NON_CANONICAL_V`,
`INVALID_VOUCH_WEIGHT`) skippt Kante und Budget. Fehlt nur `t_exp`, bleibt
der Vouch Teilnehmer.

**Verworfen:** Den Satz wörtlich auf alle vier anzuwenden — das striche
§6.2 und machte den Vermerk zur heimlichen Void-Regel.

---

## 8. 02 §10 — Reihenfolge der `v`-Prüfung

**Offen:** Rundlauf-Exception → `UNPARSABLE`; abweichende Bytes →
`NON_CANONICAL_V`; danach Wert. Indefinite-length steht in beiden Sätzen.

**Lesart:** `decode → normalize (last-wins) → encode`. Scheitert das
Dekodieren (inkl. Restbytes), ist `v` unlesbar. Liefert der Rundlauf andere
Bytes, ist `v` nicht kanonisch — auch bei doppeltem Key 0. Erst danach
Map/Key-0/`uint`/`[1, D]`. Negative Integers unter Key 0 gelten als
unlesbar, nicht als ungültiges Gewicht.

**Verworfen:** Last-wins stillschweigend als kanonisch zu akzeptieren
(02 §3.1, Absatz zum doppelten Schlüssel). Verworfen, indefinite `v` als
`NON_CANONICAL_V`, wenn der Decoder mit Nothing abbricht — das ist der
Exception-Zweig, also `UNPARSABLE_VOUCH_PAYLOAD`.

---

## 9. 01 §6 / B.1 — `FOREIGN_LIFECYCLE` nach dem Einzelparse

**Offen:** Der Konjunkt `ziel.I == C.I` braucht den Ziel-Claim. Beim
Einzelparse ist er oft noch unbekannt.

**Lesart:** Zuerst alle Drähte parsen, Duplikate nach `claim_id`
wegwerfen, dann Acts droppen, deren Ziel lokal bekannt und fremd-`I` ist.
Diese Bytes erscheinen nicht unter `zustand`.

**Verworfen:** Fremd-Acts zu halten und zu ignorieren (dann wäre der
Reject-Code tot). Verworfen, sie als `malformed` zu drucken — `malformed`
ist kein gehaltener Zustand (D278).

---

## 10. 01 §6 — wirkt ein `pending` Revoke

**Offen:** „ein gültiger selbst-bezüglicher `core/revoke@1` existiert“.
Gültig ist strukturell; pending ist gehalten.

**Lesart:** Jeder gehaltene selbst-bezügliche Revoke/Supersede wirkt, auch
wenn der Act selbst `pending` oder geflaggt ist. Unter-Vertrauen: ein
gesehener Widerruf deaktiviert.

**Verworfen:** Nur `active` Acts wirken — ein pending Widerruf ließe
Vertrauen stehen, obwohl der Act bereits signiert vorliegt.

---

## 11. 01 B.1 — Vorrang Equivocation gegen Widerruf und Ablauf

**Offen:** Ein Claim kann forken und widerrufen sein. Die Tabelle gibt
acht Zustände, keine Kombination.

**Lesart:** Equivocation zuerst (beide Geschwister), dann pending, dann
Zeitregression, dann revoke, dann supersede, dann expired, sonst active.
Gleichstand `C.t >= P.t` ist erlaubt (01 §6).

**Verworfen:** Widerruf über Equivocation (die Diagnose „der Autor hat
geforkt“ ginge verloren). Verworfen, expired über revoke (02 §3.1 / D41).

---

## 12. 01 §6 `linked` — transitiver Vorgänger

**Offen:** `pending`, wenn `h_prev` unbekannt ist. Ist `C` linked, wenn `P`
bekannt, `P` aber selbst pending ist?

**Lesart:** Nur der unmittelbare `h_prev` zählt. Ist er im Speicher, ist
`C` linked (und dann zeitgeprüft). Keine transitive Genesis-Forderung.

**Verworfen:** Die ganze Kette bis Genesis zu verlangen — das steht nicht
im Satz, und Partial-Sync würde ganze Suffixe auf pending setzen, obwohl
der unmittelbare Vorgänger da ist.

---

## 13. 01 B.2 — Prüfreihenfolge der Reject-Codes

**Offen:** Keine Gesamtordnung; verboten ist nur der falsche Satz.

**Lesart:** Nicht-Map / Restbytes / Nicht-uint-Key / doppelter Key →
`MALFORMED_CBOR`. Lesbares `version ≠ 1` → `UNSUPPORTED_VERSION` ohne
Feldtabelle. Sonst Re-Serialisierung, bei Abweichung
`NON_CANONICAL_ENCODING` (BV3: dekodierbare indefinite äußere Map).
Danach v1-Feldtabelle, Bindung, Signatur, Null-`h_prev`, `t < t_exp`.

**Verworfen:** Kanonizität vor dem Schlüsseltyp (BV2 verlangt
`MALFORMED_CBOR` bei text-Key, auch indefinite).

---

## 14. 01 §3 — indefinite-length im eigenen Decoder

**Offen:** Der Decoder muss BV3 dekodieren können, sonst wäre die einzige
Antwort `MALFORMED_CBOR`.

**Lesart:** Indefinite Arrays/Maps/Bytes/Text werden gelesen und definite
re-kodiert. Break in Wertposition (BV1) bleibt undekodierbar →
`MALFORMED_CBOR`.

**Verworfen:** Indefinite grundsätzlich abzulehnen (BV3 ununterscheidbar
von Müll).

---

## 15. 02 §2 Zweck-Filter und Bond

**Offen:** Zweck-Tag in `v` Key 1; Bond Key 2. Die Eingabe hat keinen
Zweck-Parameter.

**Lesart:** Kein Zweck-Filter, kein Bond-Filter. Key 0 allein bestimmt `n`.
Weitere Keys sind unschädlich.

**Verworfen:** Untypisierte vs. typisierte Kanten zu unterscheiden — ohne
Anfrage-Zweck wäre jede Wahl eine Erfindung.

---

## 16. 02 §2 Scope

**Offen:** Ein Graph pro `N`. Das Profil liefert ein `scope`.

**Lesart:** Nur Vouches mit `N` gleich diesem Scope und `J.tag = identity`.
Andere gehaltene Claims erscheinen nur unter `zustand`.

**Verworfen:** Alias-`p` ohne `N`-Vergleich (01 §2.4: `N` ist die Autorität).

---

## 17. 02 §8 Disjunkt-Lauf

**Offen:** Einheitskapazitäten auf internen und Vouch-Kanten; Anker-interne
∞; Senke weiter `T_in`. Ob Kanten mit Original-`cap = 0` auf 1 gehen, fehlt.

**Lesart:** Derselbe Graph wie die harte Sicht, aber nur Kanten, die dort
`cap ≥ 1` hatten, werden 1. Anker-interne Kanten ∞ (`INF` wie Eintrag 2).
Nicht-Anker intern 1, falls `C(x) ≥ 1`, sonst 0.

**Verworfen:** Null-Kanten auf 1 zu heben (erzeugt Pfade, die `E+` nicht
kennt). Verworfen, Endpunkte wirklich ungespalten zu lassen — `02 §8`
sagt, die interne Anker-Kante trägt ∞, nicht, dass `in`/`out` entfallen.

---

## 18. 02 §3 BFS-Start

**Offen:** Distanz vom Ankerset. Sind Anker ohne ausgehende Vouch-Kante
bei `d = 0`?

**Lesart:** Jeder Anker startet bei `d = 0`, `C = C0`, unabhängig von
Kanten. BFS nur über `cap ≥ 1`.

**Verworfen:** Anker erst nach einer Kante einzusetzen — dann wäre `C0`
totes Gewicht.

---

## 19. Auftrag Datei-Feld `t_exp`

**Offen:** Jedes Profil trägt `now` und `t_exp`. Claims tragen eigenes
`t_exp`.

**Lesart:** Ausgewertet wird nur Claim-`t_exp` gegen Datei-`now`. Das
Profil-Feld `t_exp` ist ungenutzt (Konstruktionshint der Vektoren, keine
Default-Laufzeit). Keine Uhr.

**Verworfen:** Fehlendes Claim-`t_exp` durch das Dateifeld zu ersetzen
(das wäre eine Policy-Default-Laufzeit, die 02 §6.2 erlaubt, der Vektorsatz
aber nicht als Policy deklariert).

---

## 20. 01 §5.4 Policy / irrevocable

**Offen:** Ohne Verfassungsobjekt gilt der Sicherheits-Default.

**Lesart:** Keine Verfassung in der Eingabe → alle Prädikate widerrufbar.
`core/*` ohne `N` fällt unter keine Policy.

**Verworfen:** Irgendein Prädikat irrevocable zu setzen (kein Genesis in
der Datei).

---

## 21. 02 §10 `SUBGRANULAR_VOUCH` bei Unerreichbarkeit

**Offen:** Vermerk, wenn `⌊n_kante · C / D⌋` auf 0 fällt. Unerreichbar ist
`C = 0`.

**Lesart:** Der Vermerk gilt auch für unerreichbare Autoren mit
`n_kante > 0`. Träger: kleinste `claim_id` unter den Aktiv-Mitgliedern mit
`n = n_kante`.

**Verworfen:** Nur Granularitätsboden bei `C ≥ 1` — die Formel unterscheidet
das nicht.

---

## 22. Auftrag `gruppe` ohne Aktiv-Mitglieder

**Offen:** `n_kante` ist max n im Aktiv-Set. Das Aktiv-Set kann leer sein.

**Lesart:** Gruppe existiert, sobald das Budget-Set nicht leer ist.
Leeres Aktiv-Set → `n_kante = 0`, keine `kante`-Zeile.

**Verworfen:** Solche Gruppen zu unterschlagen — das Budget wäre dann
unsichtbar.

---

## 23. 02 §4 Quelle bei Super-Source

**Offen:** Einzelabfrage ist `maxflow(s_in → T_in)`. Das Ankerset hängt
`S*` vor `a_in`.

**Lesart:** Immer `S*` als Quelle, Senke `T_in` (einzeln) bzw. `T*`
(simultan/disjunkt). Die interne Ankerkante liegt auf jedem Pfad.

**Verworfen:** Einzelnen Anker an `a_out` zu hängen (02 §4: Satz bei
Über-Commitment falsch). Zweifel, falls ein Ziel selbst Anker ist:
`S* → T_in` wäre INF. Die acht Profile tun das nicht.

---

## 24. fgl-Kantenmenge

**Offen:** `mkGraph` mit parallelen Kanten und `Integer`.

**Lesart:** Eine Kante je `(u, v)`; Kapazität `Integer`. Modul
`Data.Graph.Inductive.Query.MaxFlow`, nicht `MaxFlow2`.

**Verworfen:** Eigener Edmonds-Karp (Auftrag). Verworfen, Flusswerte an
vermutete Anker zu drehen.

---

## 25. 01 Anhang A Alias-Scope

**Offen:** Lookahead `^(?![0-9a-f]{64}$)`. Ein 64-Hex-String, der ein
Großbuchstaben-A enthält, ist weder kanonisch noch Alias.

**Lesart:** Kanonisch nur `[0-9a-f]{64}`. Alias nur, wenn die Länge
**nicht** 64 ist und `[a-z0-9_-]+` gilt. Länge 64 mit einem unzulässigen
Zeichen → `INVALID_PREDICATE`.

**Verworfen:** 64er Strings grundsätzlich als kanonisch zu lesen.

---

## 26. Ausgabeprofil-Trennung

**Offen:** Der Auftrag nennt keine Leerzeile zwischen Blöcken.

**Lesart:** Eine Leerzeile zwischen Profilen, damit acht Blöcke
untereinander lesbar bleiben. Innerhalb eines Blocks keine Leerzeilen.
`schnitt` ohne Identitäten ist die Zeile `schnitt`.

**Verworfen:** Alles in einem Strom ohne Trennung (nicht verboten, aber
die Blockgrenze wäre nur `profil` ).

---

## 27. Zweifel an plausiblen Zahlen

**Offen:** Der Vektorsatz trägt keine erwarteten Flusswerte. Variante A
ist über-committet (`include_flagged = True`, Kanten bleiben). E0 hat
unerreichbare Ziele.

**Lesart:** Die gedruckten `fluss`/`simultan`/`disjunkt` werden nicht
nachträglich angepasst. Wirkt ein Wert tot (0 gegen eine Kette, die
optisch durchgeht), steht das hier: ohne `02-golden-anchors.md` ist
„unplausibel“ nicht entscheidbar; gedruckt wird, was Graph und `fgl`
liefern.

**Verworfen:** Ankerwerte aus Erinnerung an Python-Läufe einzusetzen.
