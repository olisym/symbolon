# Layer 04 — Golden Anchors

Erwartungswerte für die Implementierung der Governance-Schicht. Alle Zahlen sind exakte Integer
und vor dem Schreiben dieses Dokuments gerechnet, nicht danach.

---

## 1. Methode

**Zweifach verifiziert.** Die kanonische CBOR-Kodierung wurde eigenständig implementiert und
**gegen die vier Bestandsanker aus `00 §3.1` validiert**, bevor irgendein neuer Wert entstand:
`cbor(constitution)`, `constitution_hash = 890b21e7…`, `cbor(genesis)` und
`N = 65309fe2…` reproduzieren byte-identisch. Die Schwellenarithmetik ist zusätzlich in
Integer-Form und über `Fraction` gerechnet; beide Wege stimmen in jedem Fall überein.

**Kein Float, keine Division.** Jeder Vergleich zweier Verhältnisse läuft über Kreuzmultiplikation.

**Der Bestandsanker bleibt unberührt.** `65309fe2…` und `890b21e7…` sind nicht Teil dieses
Profils. Der Nukleus aus `00 §3.1` trägt kein `participants` und setzt `weight_mode = 1`; er ist
nach `04 §3.5` nicht auszählbar. Layer 04 bekommt deshalb ein eigenes Profil.

---

## 2. Profil D

### 2.1 Identitäten

Ed25519, Seeds `01×32` bis `05×32`. Die ersten drei sind Bestand.

```
ALICE = 8a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c
BOB   = 8139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df60f5b8fc9b394
CAROL = ed4928c628d1c2c6eae90338905995612959273a5c63f93636c14614ac8737d1
DAVE  = ca93ac1705187071d67b83c7ff0efe8108e8ec4530575d7726879333dbdabe7c
EVE   = 6e7a1cdd29b0b78fd13af4c5598feff4ef2a97166e3ca6f2e4fbfccd80505bf1
```

`participants` ist byteweise aufsteigend sortiert und duplikatfrei. Die Sortierung folgt **nicht**
der Namensreihenfolge:

```
P1 (Epoche 1, n = 4)  =  BOB, ALICE, DAVE, CAROL
                         8139…  8a88…  ca93…  ed49…

P2 (Epoche 2 und 3, n = 5)  =  EVE, BOB, ALICE, DAVE, CAROL
                               6e7a…  8139…  8a88…  ca93…  ed49…
```

Ein Vektor, der die Sortierung nach Namen statt nach Bytes vornimmt, erzeugt einen anderen
`constitution_hash` und damit eine andere Epoche. Das ist Absicht: die Reihenfolge ist Teil der
Identität. Dasselbe gilt für `irrevocable_predicates`, das hier in der Reihenfolge
`["obligation@1", "ratify@1", "vote@1"]` steht.

**`vote@1` und `ratify@1` stehen in `irrevocable_predicates` aller drei Verfassungen.** Ohne
diese Einträge wäre Profil D nach `04 §3.5` nicht auszählbar (`VOTE_REVOCABLE`,
`RATIFY_REVOCABLE`). Deshalb weichen alle Hashes dieses Profils von einer Fassung ab, die nur
`obligation@1` führt.

### 2.2 Die drei Verfassungen

```
C1 = {
  irrevocable_predicates: ["obligation@1", "ratify@1", "vote@1"],
  thresholds:             { ordinary: [1,2], membership: [2,3], amendment: [3,4] },
  arbitration:            { arbitrators: [ALICE] },
  participants:           [BOB, ALICE, DAVE, CAROL]
}

C2 = C1, aber participants = [EVE, BOB, ALICE, DAVE, CAROL]      (Aufnahme von EVE)

C3 = C2, aber arbitration = { arbitrators: [BOB, ALICE] }        (zweiter Arbitrator)
```

```
constitution_hash_1 = 8e7762ef9a8b9a414cbec44ad0b4658e3ae17d2663c6d3fc12af64a8ac78f3b0
constitution_hash_2 = 3ba90e8c98aca71654c2559ed4affde521e2860e228bf9ae57a07a3d1f92d2d0
constitution_hash_3 = 09c2441d09546d7546f043bb57be2349709fc9fca5db69d66245aa82fd505e86
```

`C1` nach `C2` unterscheidet sich ausschließlich in `participants` — Klasse **`membership`**,
Schwelle `[2,3]`. `C2` nach `C3` unterscheidet sich in `arbitration` — Klasse **`amendment`**,
Schwelle `[3,4]`. Die Klasse wird abgeleitet, nicht gewählt (`04 §3.4`).

### 2.3 Das Genesis-Objekt

```
genesis_D = {
  0 version           : 1
  1 root_keys         : [ALICE]
  2 key_mode          : 0
  3 anchor_set        : [ALICE]
  4 constitution_hash : 5e288ec9…
  5 amendment_rule    : 2
  6 weight_mode       : 0            ; Kopfzahl (D98)
  7 vote_mode         : 0            ; Epochenpfad
}

cbor(genesis_D) =
  a80001018158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c
  0200038158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c
  0458208e7762ef9a8b9a414cbec44ad0b4658e3ae17d2663c6d3fc12af64a8ac78f3b0
  050206000700

N_D = SHA-256(DOM_NUC_GEN || cbor(genesis_D))
    = a15c70c4829e7a296b5af56656e0a94b9ea9391096515c9cc592e18bd2d9f7ef
```

Gegenüber `00 §3.1` unterscheidet sich `genesis_D` in zwei Bytes des Endes — `06 00` statt
`06 01` — und im `constitution_hash`. Das ist ein nützlicher Vektor für sich: derselbe
Schlüsselsatz, ein anderer Gewichtungsmodus, ein anderer Nukleus.

---

## 3. Die Epochenkette

```
DOM_NUC_EPOCH    = "claim-atom/v1/nucleus-epoch"
DOM_NUC_PROPOSAL = "claim-atom/v1/nucleus-proposal"

epoch_id      = SHA-256( DOM_NUC_EPOCH    || cbor([N, i, constitution_hash]) )
proposal_hash = SHA-256( DOM_NUC_PROPOSAL || cbor({0: N, 1: predecessor, 2: constitution_hash}) )
```

```
epoch_id_1      = 56915063c07ce1e6b74e10712e8f17b9f381af359a3e12b9719e90a52483d724
                  ( [N_D, 1, constitution_hash_1] — der Genesis ist Epoche 1 )

proposal_hash_1 = 38edfd6b0ba90ade0b96746c21ead9e631c1dac883150a15ed923dd1aaf6db6b
                  ( predecessor = epoch_id_1, Ziel = constitution_hash_2 )

epoch_id_2      = 50a33beff78aae27f6ac8da621879a686055190eabcb7832867f9b7b00d5c182
                  ( [N_D, 2, constitution_hash_2] )

proposal_hash_2 = 8350006de0acc4089a347920748a70cc72068eb20e0995a8960d58e6581fd018
                  ( predecessor = epoch_id_2, Ziel = constitution_hash_3 )

epoch_id_3      = c052fd3b7c81d4d0a65adb892476a830666ae3ffebb928b355806c882fc9589a
                  ( [N_D, 3, constitution_hash_3] )
```

**Vektor `GV-1`.** Zwei `ratify@1`-Claims für `proposal_hash_1`, von verschiedenen Autoren, mit
verschiedenen Zeugenmengen. Beide liefern `epoch_id_2 = 380779c1…`. Kein Widerspruch, keine
zweite Epoche. Das ist D99 in einer Zahl.

**Vektor `GV-2`.** Ein `ratify@1` mit `v[0]` als Zeugenmenge, die einen zusätzlichen Claim
enthält, der **vorhanden ist, aber nicht zählt**. Der `epoch_id` ändert sich nicht; die
Ratifizierung scheitert an `04 §4.1` Bedingung 3, Vermerk `UNSUPPORTED_RATIFICATION`.

`GV-2` und `GV-30` sind das Paar: derselbe Ausgang, zwei Diagnosen. Ein Lauf, der beide auf
denselben Vermerk abbildet, ist rot (D106).

---

## 4. Schwellenarithmetik

```
durchgekommen:   |Ja| * den          >   num * n
gescheitert:     (n - |Nein|) * den   <=  num * n
```

### 4.1 Die Kante des strikten Größer

Epoche 1, `n = 4`, Klasse `amendment`, `[3,4]`:

| Vektor | Ja | Nein | Rechnung | Zustand |
|---|---|---|---|---|
| `GV-3` | 3 | 0 | `3*4 = 12` gegen `3*4 = 12` | `PENDING` |
| `GV-4` | 4 | 0 | `4*4 = 16` gegen `12` | `PASSED` |

`GV-3` ist der wichtigste Vektor dieses Dokuments. Ein `>=` statt `>` macht aus drei von vier
Stimmen eine Verfassungsänderung. Der Unterschied ist ein Zeichen im Quelltext.

### 4.2 Scheitern ohne vollständige Beteiligung

Epoche 1, `n = 4`, `[3,4]`:

| Vektor | Ja | Nein | Rechnung | Zustand |
|---|---|---|---|---|
| `GV-5` | 0 | 2 | `(4-2)*4 = 8` gegen `12` | `FAILED` |
| `GV-6` | 1 | 2 | `(4-2)*4 = 8` gegen `12` | `FAILED` |

Zwei Mitglieder haben sich noch gar nicht geäußert, und der Vorschlag ist trotzdem endgültig
erledigt: das erreichbare Ja ist zu klein. Ohne die zweite Ungleichung bliebe er auf `PENDING`
hängen, bis jemand eine Frist erfindet.

### 4.3 Die Aufnahme (Epoche 1, Klasse `membership`)

`n = 4`, `[2,3]`, Ziel `constitution_hash_2`:

| Vektor | Ja | Rechnung | Zustand |
|---|---|---|---|
| `GV-7` | 2 | `2*3 = 6` gegen `2*4 = 8` | `PENDING` |
| `GV-8` | 3 | `3*3 = 9` gegen `8` | `PASSED` |

Die Aufnahme von EVE kostet drei von vier Stimmen. Dieselbe Aufnahme unter der
Änderungsschwelle hätte alle vier gekostet — das ist der Grund für die Klassenableitung aus
`04 §3.4`.

**EVE ist nach `GV-8` noch kein Mitglied.** Sie steht in `participants` von `C2`, aber
`membership()` verlangt zusätzlich ihre aktive `accept-rules@1` auf `constitution_hash_2`. Ohne
sie lautet der Zustand `GRANT_ONLY` (`04 §6.1`, D60).

### 4.4 Die Änderung (Epoche 2, Klasse `amendment`)

`n = 5`, `[3,4]`, Ziel `constitution_hash_3`:

| Vektor | Ja | Rechnung | Zustand |
|---|---|---|---|
| `GV-9`  | 3 | `3*4 = 12` gegen `3*5 = 15` | `PENDING` |
| `GV-10` | 4 | `4*4 = 16` gegen `15` | `PASSED` |

---

## 5. Die Maximum-Regel

Alle Fälle in Epoche 2, `n = 5`. `angewandt = max(alt, neu)`, Vergleich über
`num_a * den_n` gegen `num_n * den_a`.

### 5.1 Senken — der tragende Fall

Ein Vorschlag setzt `thresholds.amendment` von `[3,4]` auf `[1,2]`. Der Zielwert ist nach D108
zulässig: `2*1 = 2` erreicht `den = 2`, die Grenze ist nicht strikt.

```
max([3,4], [1,2]):   3*2 = 6   >=   1*4 = 4   ->   angewandt = [3,4]
```

| Vektor | Ja | angewandte Schwelle | Rechnung | Zustand |
|---|---|---|---|---|
| `GV-11` | 3 | `[3,4]` | `3*4 = 12` gegen `15` | `PENDING` |
| `GV-12` | 3 | `[1,2]` (Gegenbild ohne Regel) | `3*2 = 6` gegen `5` | `PASSED` |

**Das ist die Anti-Capture-Eigenschaft in zwei Zahlen.** Drei von fünf Mitgliedern können die
Änderungsschwelle nicht auf die Hälfte senken, obwohl drei von fünf nach der *neuen* Schwelle
eine Mehrheit wären. `GV-12` ist der Vektor, der grün werden muss, wenn die Regel fehlt — er
gehört als Gegenbild in die Testsuite, nicht nur als Kommentar.

### 5.2 Anheben

Ein Vorschlag setzt `thresholds.amendment` von `[1,2]` auf `[4,5]`.

```
max([1,2], [4,5]):   1*5 = 5   <   4*2 = 8   ->   angewandt = [4,5]
```

| Vektor | Ja | angewandte Schwelle | Rechnung | Zustand |
|---|---|---|---|---|
| `GV-13` | 4 | `[4,5]` | `4*5 = 20` gegen `4*5 = 20` | `PENDING` |
| `GV-14` | 4 | `[1,2]` (Gegenbild ohne Regel) | `4*2 = 8` gegen `5` | `PASSED` |

`GV-13` trifft zugleich die Kante aus `4.1`: bei `[4,5]` und `n = 5` verlangt das strikte Größer
Einstimmigkeit. Eine Minderheit kann der Mehrheit keine strengere Regel auferlegen.

Die Ausgangsschwelle `[1,2]` in `5.2` gehört zu keiner der drei Verfassungen aus `2.2`; der
Vektor prüft die Regel, nicht die Kette.

### 5.3 Formwidrige Schwellen (D108)

Alle in Epoche 2, `n = 5`, Klasse `amendment`. Erwartung durchgehend `UNEVALUABLE` mit
`MALFORMED_THRESHOLD` — **nie** ein Ergebnis.

| Vektor | Zielschwelle | Verletzte Bedingung | Was ohne die Prüfung geschähe |
|---|---|---|---|
| `GV-35` | `[1,3]` | `2*num >= den` | zwei Vorschläge mit je 2 von 5 Ja, ohne Überschneidung — D102 fällt |
| `GV-36` | `[2,5]` | `2*num >= den` | dasselbe, knapp unterhalb der Grenze |
| `GV-37` | `[-1,2]` | `0 <= num` | `0 > -1 * 5` ist wahr: `PASSED` ohne eine einzige Stimme |
| `GV-38` | `[5,4]` | `num <= den` | dauerhaft unerreichbar, ohne Diagnose |
| `GV-39` | `[1,0]` | `den >= 1` | dauerhaft `FAILED`, ohne Diagnose |

`GV-37` ist der schärfste: er wird ohne die Prüfung nicht bloß falsch, sondern liefert eine
ratifizierte Verfassung aus einem leeren Store.

**`[1,2]` ist zulässig** und muss es bleiben. Bei `n = 5` verlangt es drei Ja; zwei disjunkte
Dreiermengen passen nicht in fünf Mitglieder. Ein Vektor, der `[1,2]` zurückweist, ist rot.

Die Prüfung betrifft nur die **angewandte** Klasse. Die Verfassung aus `00 §3.1` führt
`ordinary: [1,2]` — zulässig, und in v1 ohnehin unbenutzt.

---

## 6. Ausschluss rivalisierender Nachfolger

Epoche 2, `n = 5`, Klasse `amendment`, `[3,4]`.

```
nötige Ja je Vorschlag:                     4
zwei Vorschläge verlangen zusammen:         8 Ja-Stimmen
verfügbare Mitglieder:                      5
Mitglieder mit zwei Ja, mindestens:         8 - 5 = 3
```

**Vektor `GV-15`.** Zwei Vorschläge auf `epoch_id_2`, jeder mit vier Ja. Nach `04 §4.4` zählen
die Ja-Stimmen der drei doppelt stimmenden Mitglieder bei **keinem** von beiden; Vermerk
`CONFLICTING_APPROVAL`. Beide Zählungen landen bei einem Ja und damit auf `PENDING`. Es entsteht
keine Epoche 3, kein Fork und keine Auflösungsregel.

Damit ist D102 an einer Zahl geprüft: nicht „der erste gewinnt", sondern „der Fall tritt nicht
ein".

---

## 7. Ausschlussfälle mit Vermerk

Alle in Epoche 2 gegen `proposal_hash_2`, Erwartung jeweils: der Zustand bleibt `PENDING`, der
Vermerk erscheint, und die Stimme zählt nicht.

| Vektor | Lage | Vermerk |
|---|---|---|
| `GV-16` | zwei aktive Stimmen desselben Autors auf denselben Vorschlag | `AMBIGUOUS_VOTE` |
| `GV-17` | Stimme eines Schlüssels, der nicht in `participants` steht | `NON_MEMBER_VOTE` |
| `GV-18` | Stimme auf einen Vorschlag mit `predecessor = epoch_id_1` | `STALE_EPOCH_VOTE` |
| `GV-19` | `vote.v[0] = 2` | `UNKNOWN_VOTE_CHOICE` |
| `GV-20` | `vote.N != N_D` | `SCOPE_MISMATCH` |
| `GV-21` | Verfassungsobjekt zu `constitution_hash_2` lokal unbekannt | `CONSTITUTION_UNAVAILABLE`, Zustand `UNEVALUABLE` |
| `GV-22` | Verfassung ohne `participants` | `PARTICIPANTS_UNDECLARED`, Zustand `UNEVALUABLE` |
| `GV-23` | `participants` unsortiert oder mit Duplikat | `MALFORMED_PARTICIPANTS`, Zustand `UNEVALUABLE` |
| `GV-24` | eigenes Genesis mit `[6] = 1`, Epoche auf **dessen** Scope (D145) | `UNSUPPORTED_WEIGHT_MODE`, Zustand `UNEVALUABLE` |
| `GV-25` | aktive Ja-Stimme auf einen lokal unbekannten Vorschlag; derselbe Autor hat ein zweites Ja | `UNKNOWN_PROPOSAL`, beide Ja zählen nicht |
| `GV-26` | `vote.t_exp` gesetzt | `VOTE_WITH_EXPIRY`, die Stimme zählt nicht |
| `GV-27` | Verfassung ohne `vote@1` in `irrevocable_predicates` | `VOTE_REVOCABLE`, Zustand `UNEVALUABLE` |
| `GV-28` | ein widerrufener `vote@1` in einer Verfassung **mit** `vote@1` als irrevocable | kein Vermerk, die Stimme zählt weiter |
| `GV-29` | eigenes Genesis mit `[5] = 3`, Epoche auf **dessen** Scope (D145) | `MALFORMED_THRESHOLD`, Zustand `UNEVALUABLE` |
| `GV-30` | `ratify@1` zitiert eine `claim_id`, die im Store fehlt | `UNKNOWN_WITNESS_VOTE`, keine Epoche |
| `GV-31` | Verfassung ohne `ratify@1` in `irrevocable_predicates` | `RATIFY_REVOCABLE`, Zustand `UNEVALUABLE` |
| `GV-32` | widerrufener `ratify@1` in einer Verfassung **mit** `ratify@1` als irrevocable | kein Vermerk, die Epoche steht weiter |
| `GV-33` | `ratify.t_exp` gesetzt | `RATIFY_WITH_EXPIRY`, keine Epoche |
| `GV-34` | widerrufener `propose@1` bei unveränderten Stimmen | kein Vermerk, das Ergebnis ändert sich nicht |
| `GV-40` | `participants` ist ein leeres Array | `MALFORMED_PARTICIPANTS`, Zustand `UNEVALUABLE` |
| `GV-41` | `proposal.predecessor` zeigt auf eine andere Epoche, **kein** Stimmclaim im Store | `STALE_EPOCH_VOTE` mit `proposal_hash` als Subjekt, Zustand `UNEVALUABLE` — **nicht** `PENDING` |
| `GV-42` | Verfassungsobjekt vorhanden, Hash passt nicht zu `epoch.constitution_hash` | `CONSTITUTION_UNAVAILABLE`; keine Prüfung liest vorher seinen Inhalt |
| `GV-43` | `verify_ratification` mit `tally.state = UNEVALUABLE` | `TALLY_UNEVALUABLE`, keine Epoche |
| `GV-44` | `verify_ratification` mit einer Auszählung zu einem **anderen** Vorschlag oder einer **anderen** Epoche | `ValueError` (D109) — kein Vermerk |
| `GV-45` | `membership()` mit `constitution_obj`, dessen Hash nicht zum Parameter passt | `ValueError` (D111) |
| `GV-46` | `proposal.scope` gehört zu einem anderen Nukleus, `predecessor` passt | `ValueError` (D112) — in `decide` **und** in `verify_ratification` |
| `GV-47` | `thresholds[klasse]` trägt Textwerte statt Integer | `MALFORMED_THRESHOLD`, Zustand `UNEVALUABLE` — kein Abbruch |
| `GV-48` | `vote.v` nicht kanonisch kodiert, `v[0]` wäre `1` | `NON_CANONICAL_V`, die Stimme zählt nicht |
| `GV-49` | derselbe Autor mit einer kanonischen und einer nicht-kanonischen Ja-Stimme auf denselben Vorschlag | `NON_CANONICAL_V`, **kein** `AMBIGUOUS_VOTE`, die kanonische Stimme zählt |
| `GV-50` | nicht-kanonisches Zweit-Ja desselben Autors auf einen **anderen** Vorschlag derselben Epoche | `NON_CANONICAL_V`, **kein** `CONFLICTING_APPROVAL`, das erste Ja zählt |
| `GV-51` | `ratify.v` nicht kanonisch kodiert, Zeugenmenge sonst tragend | `NON_CANONICAL_V`, keine Epoche |
| `GV-52` | `vote.v = h'a2000101ff'` — dekodiert zu Key `0`, Wert `1`, re-serialisiert nicht | `UNPARSABLE_V`, die Stimme zählt nicht |
| `GV-53` | dieselbe Kodierung als Zweit-Ja desselben Autors auf einen **anderen** Vorschlag derselben Epoche | `UNPARSABLE_V`, **kein** `CONFLICTING_APPROVAL`, das erste Ja zählt |
| `GV-54` | `ratify.v = h'a2000101ff'`, Auszählung sonst tragend | `UNPARSABLE_V`, **kein** `UNSUPPORTED_RATIFICATION`, keine Epoche |

`GV-24` ist mit dem Bestandsnukleus aus `00 §3.1` unmittelbar prüfbar: `N = 65309fe2…` setzt
`weight_mode = 1` und liefert damit `UNEVALUABLE`, nie ein Ergebnis. Derselbe Nukleus trifft auch
`GV-27`: seine Verfassung führt nur `obligation@1`.

`GV-28` ist der Vektor gegen die naheliegende Fehlimplementierung. Wer `classify_all` ohne die
scope-lokale Policy aufruft, bekommt für die widerrufene Stimme `REVOKED` und zählt sie nicht —
die Auszählung schrumpft, und `INV-04.1` fällt. Der Vektor ist grün nur mit korrekt gereichter
Policy (D91).

---

## 8. Invarianten

| Kennung | Aussage |
|---|---|
| `INV-04.1` | `PASSED` und `FAILED` sind absorbierend: mehr Stimmen ändern einen erreichten Zustand nie. |
| `INV-04.2` | `PASSED` und `FAILED` schließen einander aus, für jedes `n`, `num`, `den`, `Ja`, `Nein`. |
| `INV-04.3` | Kein Teilwissen führt zu `PASSED`. Fehlt ein Objekt, ist der Zustand `UNEVALUABLE`. |
| `INV-04.4` | Zwei `ratify@1` für denselben Vorschlag liefern denselben `epoch_id`. |
| `INV-04.5` | Die Auszählung liest keine Uhr. `t` wird nie ausgewertet; `t_exp` einer Stimme nur auf Anwesenheit, nie auf seinen Wert. |
| `INV-04.7` | Die Menge der zählenden Stimmen wächst monoton: kein zusätzlicher Claim im Store entfernt je eine bereits zählende Stimme. **Vorbehalt:** gilt, solange kein Mitglied equivociert (D117). |
| `INV-04.8` | Eine einmal etablierte Epoche bleibt etabliert: kein zusätzlicher Claim im Store nimmt einem gültigen `ratify@1` seine Wirkung. **Vorbehalt:** derselbe (D117). |
| `INV-04.6` | Bei `num/den > 1/2` gibt es zu einer Epoche höchstens einen Vorschlag im Zustand `PASSED`. |

`INV-04.2` und `INV-04.6` sind als Eigenschaftstests über einem Bereich zu prüfen, nicht an
Einzelvektoren: `n` von 1 bis 12, `[num,den]` über allen gekürzten Brüchen mit `den <= 8` und
`1/2 <= num/den < 1`, alle Belegungen von `Ja` und `Nein` mit `Ja + Nein <= n`.

`INV-04.5` ist negativ zu prüfen: ein Lauf mit zwei verschiedenen `now`-Werten muss byte-identische
Ergebnisse liefern.

**Zum Vorbehalt.** Equivocation ist der dritte Ausgang aus `ACTIVE` neben Widerruf und Ablauf, und
der einzige, gegen den `is_irrevocable` nicht schützt — er soll es nicht, denn ein solcher Schutz
schützte den Doppelzüngigen. Trifft der Zwilling einer zählenden Stimme ein, fällt sie weg; ein
erreichtes `PASSED` kann dadurch auf `PENDING` zurückkippen und eine materialisierte Epoche
verfallen. Die Richtung ist stets abwärts, und der Vorgang hinterlässt einen selbst signierten
Beweis (D117). Ein Eigenschaftstest zu `INV-04.7` und `INV-04.8` muss Equivocation deshalb
ausschließen — oder sie gezielt erzeugen und den Rückfall als **erwartet** prüfen.

`INV-04.8` ist `INV-04.7` eine Ebene höher: die Stimmenmenge zu sichern nützt nichts, wenn die
Materialisierung darüber zurückgenommen werden kann (D107). `GV-34` prüft die Gegenrichtung —
`propose@1` wird von der Auszählung nie gelesen, also darf sein Zustand nichts ändern.

`INV-04.7` ist die Invariante, auf der D96, D101 und D102 gemeinsam stehen. Sie ist über zufällige
Claim-Folgen zu prüfen: Store schrittweise füllen, nach jedem Schritt auszählen, und sicherstellen,
dass die Menge der zählenden `claim_id` nie kleiner wird.

---

## 9. Was hier nicht steht

- **Keine Gewichte.** `weight_mode = 1` ist nicht ausgewertet (D98); es gibt keine Trust-Flow-Zahl
  in diesem Dokument.
- **Keine Signaturvektoren.** Die Claims selbst folgen `01` Anhang C; dieses Profil liefert die
  Objekte und die Arithmetik, nicht die Atome.
- **Kein `resolve_current_key`.** Alle Vektoren laufen über `vote_mode = 0`. Die Funktion
  existiert seit `00a` (D160), wird von dieser Schicht aber nicht aufgerufen.
- **Keine Föderationszahlen.** `04 §7.2` ist eine Belegung desselben Loops; ein zweites Profil auf
  Föderationsebene bringt keine neue Arithmetik.
