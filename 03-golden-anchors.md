# Golden Anchors Layer 03 — Profile II (Verdikt · Wert · Mitgliedschaft)

Normative Quelle: `03-profiles.md`; Register D55–D69, D77–D82.

Alle Werte in diesem Dokument sind **von Hand nachrechenbar**: kanonisches CBOR nach RFC 8949,
SHA-256, Ed25519 aus festen Seeds. Kein Wert stammt aus einem Programmlauf, der ihn selbst
erzeugt hat.

---

## 1. Maßstab: warum hier Negativvektoren stehen und keine Arithmetik

Layer 02 ließ sich über Zahlen prüfen — Flusswerte, Budgets, Rangvektoren, alle exakt und
rundungsfrei. Layer 03 rechnet nicht. Die Trennschärfe kommt hier aus drei anderen Quellen:

1. **Byte-exakte CBOR-Vektoren** für die `v`-Kodierungen (§5) und die vier Verstoßklassen der
   Kanonizität (§6). Von Hand nachrechenbar, byte-vergleichbar.
2. **Bestandsanker** (§2). `03` bindet an `constitution_hash` und `N` aus `00 §3.1`, statt neue
   Zahlen zu erfinden — dieselbe Disziplin wie in der ganzen Spec-Reihe.
3. **Konjunktionstabellen** (§7–§10). Jede Zeile ist ein Fall, den eine plausible
   Implementierung anders beantworten würde als eine korrekte.

**Das unbequeme zweite Profil aus D54 ist hier keine Parameterwahl, sondern eine zweite
Verfassung** — genauer: zwei. Das kanonische Beispiel trägt jeden Default, den es gibt, und
verdeckt damit fünf Entscheidungen vollständig (§3).

---

## 2. Bestandsanker — Profil A (kanonisch, unverändert)

Byte-identisch mit `00 §3.1` und `01` Anhang C. Hier nur nachgewiesen, nicht neu gerechnet.

```
constitution_A = {
  irrevocable_predicates: ["obligation@1"],
  thresholds:            { ordinary: [1,2], membership: [2,3], amendment: [3,4] },
  arbitration:           { arbitrators: [ALICE] }
}
constitution_hash_A = 890b21e7cd43fc4226938ce0b6eae1d00efa04ef9e6585c352dcf19ccad5ea7e
N_A                 = 65309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557
```

---

## 3. Die Gegenprofile

### 3.1 Identitäten

Ed25519 aus den Seeds `01×32`, `02×32`, `03×32`. ALICE und BOB sind die Bestandsidentitäten aus
`00 §3.1`; CAROL kommt neu dazu und wird für zwei Abweichungen gebraucht.

```
ALICE = 8a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c
BOB   = 8139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df60f5b8fc9b394
CAROL = ed4928c628d1c2c6eae90338905995612959273a5c63f93636c14614ac8737d1
```

### 3.2 Warum zwei Gegenprofile und nicht eines

Eine Verfassung kann nicht zugleich zu `irrevocable_predicates` **schweigen** und `vouch@1`
**nennen**. Die fünf Abweichungen brauchen daher zwei Objekte. Beide unterscheiden sich vom
kanonischen Genesis in **genau einem Feld** — `constitution_hash`. Wird ein Vektor rot, ist die
Ursache damit die Verfassung und nicht eines von acht gleichzeitig geänderten Feldern.

### 3.3 Profil B — nennt `vouch@1`, zwei Arbitratoren

```
constitution_B = {
  thresholds:            { ordinary: [1,2], membership: [2,3], amendment: [3,4] },
  arbitration:           { arbitrators: [ALICE, BOB] },
  irrevocable_predicates: ["vouch@1"]
}
cbor(constitution_B) = a36a7468726573686f6c6473a3686f7264696e61727982010269616d656e646d
                       656e748203046a6d656d626572736869708202036b6172626974726174696f6e
                       a16b61726269747261746f72738258208a88e3dd7409f195fd52db2d3cba5d72
                       ca6709bf1d94121bf3748801b40f6f5c58208139770ea87d175f56a35466c34c
                       7ecccb8d8a91b4ee37a25df60f5b8fc9b3947669727265766f6361626c655f70
                       7265646963617465738167766f7563684031
constitution_hash_B  = 9053909b466d60dd8d97947db67513af01a1ddeb32c6fa48dd3f584a4d74f026

genesis_B = { …wie 00 §3.1, nur 4 constitution_hash: 9053909b… }
cbor(genesis_B)      = a80001018158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3
                       748801b40f6f5c0200038158208a88e3dd7409f195fd52db2d3cba5d72ca6709
                       bf1d94121bf3748801b40f6f5c0458209053909b466d60dd8d97947db67513af
                       01a1ddeb32c6fa48dd3f584a4d74f026050206010700
N_B                  = 7ce9653872a4143b85ff00d8d8af4ebc7dcb5da19d8d9907a423b477534bbb0c
```

Profil B trägt **zwei** Abweichungen in einem Objekt und ist damit der dichteste Vektor der
Datei: `["vouch@1"]` ist zugleich die unsichere Deklaration (D58) **und** der schärfste Fall von
D70 — eine Verfassung, die ein anderes Prädikat nennt und `obligation@1` weglässt. Genau der
Fall, für den der Boden erfunden wurde.

### 3.4 Profil C — schweigt

```
constitution_C = {
  thresholds:  { ordinary: [1,2], membership: [2,3], amendment: [3,4] },
  arbitration: { arbitrators: [ALICE] }
}
cbor(constitution_C) = a26a7468726573686f6c6473a3686f7264696e61727982010269616d656e646d
                       656e748203046a6d656d626572736869708202036b6172626974726174696f6e
                       a16b61726269747261746f72738158208a88e3dd7409f195fd52db2d3cba5d72
                       ca6709bf1d94121bf3748801b40f6f5c
constitution_hash_C  = f306b62560cbf3c5253a4a0dc0ca5744fe815cfa100b924b0ff9202873e25e08

cbor(genesis_C)      = a80001018158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3
                       748801b40f6f5c0200038158208a88e3dd7409f195fd52db2d3cba5d72ca6709
                       bf1d94121bf3748801b40f6f5c045820f306b62560cbf3c5253a4a0dc0ca5744
                       fe815cfa100b924b0ff9202873e25e08050206010700
N_C                  = dffbe29a24c55594f387ea8d33fb5f0534424a3dfe828f9b0d91a4e072ad0069
```

Die CBOR-Map hat **zwei** Einträge statt drei (`a2` statt `a3`) — das Schweigen ist am ersten
Byte ablesbar.

### 3.5 Was jede Abweichung trennt

| # | Abweichung | Profil | prüft | ohne sie |
|---|---|---|---|---|
| 1 | Verfassung schweigt zu `irrevocable_predicates` | C | D70, Boden | Schweigen wäre nicht vom Nennen unterschieden |
| 2 | Verfassung nennt `vouch@1` | B | D58 + D70 | unsichere Deklaration bliebe wirksam, Boden verschwände still |
| 3 | zwei Arbitratoren, Verdikt von einem **Dritten** | B | D67, Pfad (i) ggü. (ii) | Pfad (ii) würde nie geprüft |
| 4 | `accept-rules` auf einen anderen `constitution_hash` | B | D61 | Versionsbindung wäre wirkungslos |
| 5 | `grant-membership` von einem Schlüssel außerhalb `authorized_keys` | B | D62 | Autorisierung wäre wirkungslos |

Abweichung 4 zeigt auf `890b21e7…` — den **kanonischen** Hash. Der „falsche" Hash ist damit
selbst ein Bestandsanker und keine erfundene Zahl. Abweichungen 4 und 5 sind claim-seitig und
brauchen kein eigenes Verfassungsobjekt.

**Keiner dieser fünf Fälle ist unter Profil A sichtbar.**

---

## 4. Policy-Auflösung (D57, D70, D71, D82)

`resolve_policy(scope=…, genesis_obj=…, constitution_hash=…, constitution_obj=…)`.

`constitution_hash` ist seit D167 Parameter; `genesis_obj[4]` wird nicht gelesen. In den Vektoren
unten ist es der Hash der **erwarteten** Verfassung, nicht der des übergebenen Objekts.

| ID | Eingabe | wirksame Menge | Vermerke |
|---|---|---|---|
| `P-A` | Profil A vollständig | `{device-ack@1, device-add@1, device-end@1, obligation@1, rotate-ack@1, rotate-key@1}` | — |
| `P-B` | Profil B vollständig | `{device-ack@1, device-add@1, device-end@1, obligation@1, rotate-ack@1, rotate-key@1}` | — · `policy.warnings` trägt `UNSAFE_IRREVOCABLE_PREDICATE(vouch@1)` |
| `P-C` | Profil C vollständig | `{device-ack@1, device-add@1, device-end@1, obligation@1, rotate-ack@1, rotate-key@1}` | — |
| `P-D` | Genesis A, Hash A, `constitution_obj=None` | `{device-ack@1, device-add@1, device-end@1, obligation@1, rotate-ack@1, rotate-key@1}` | `CONSTITUTION_UNAVAILABLE` |
| `P-E` | Genesis A, Hash A, Verfassung **B** | — | `ValueError` (D167) |
| `P-F` | Genesis B, `scope = N_A` | — | `ValueError` |
| `P-G` | Genesis A **ohne Key `4`**, `scope` daraus gerechnet, Verfassung A | `{device-ack@1, device-add@1, device-end@1, obligation@1, rotate-ack@1, rotate-key@1}` | — (D168) |
| `P-H` | Genesis A, Hash **B**, `constitution_obj=None` | `{device-ack@1, device-add@1, device-end@1, obligation@1, rotate-ack@1, rotate-key@1}` | `CONSTITUTION_UNAVAILABLE`, Subjekt Hash **B** (D167) |

**`P-B` ist der Kernvektor.** Er ist der einzige, der D58 und D70 gleichzeitig stellt: die
deklarierte Menge ist `{vouch@1}`, das Ergebnis ist der Boden. Eine Implementierung, die
nur filtert, liefert `{}`; eine, die nur den Boden setzt, liefert ihn zuzüglich `vouch@1`.

Der Boden ist seit D535 sechselementig: `obligation@1`, `rotate-key@1`, `rotate-ack@1`,
`device-add@1`, `device-ack@1`, `device-end@1`. Die Werte oben sind entsprechend nachgezogen (D157
für die Rotation, D537 für die Geräte) — nicht, um einen Test grün zu bekommen, sondern weil die
Norm sich geändert hat.
Beide sind hier rot, und zwar in verschiedene Richtungen.

**`P-A`, `P-C` und `P-D` liefern dasselbe Ergebnis und sind trotzdem drei Vektoren.** Sie
unterscheiden sich in den Vermerken, und der Betreiber muss „die Verfassung sagt es",
„die Verfassung schweigt" und „ich habe die Verfassung nicht" auseinanderhalten können.

**`P-G` liefert seit D168 dasselbe wie `P-A` und ist trotzdem ein eigener Vektor.** Er sagt nicht
„die Verfassung sagt es", sondern „das Genesis ist unvollständig und der Auflöser stört sich nicht
daran". `resolve_policy` prüft, was es liest, und `genesis[4]` liest es nicht mehr. Ohne diesen
Vektor prüft die Aussage niemand.

**`P-H` ist der Vektor, ohne den D167 ungeprüft bliebe.** In `P-D` sind der übergebene
`constitution_hash` und `genesis[4]` **derselbe Wert**; der Vektor kann deshalb nicht sehen,
welchem von beiden die Auflösung folgt, und bliebe grün, wenn sie dem Genesis folgte. `P-H`
trennt die zwei Größen und ist damit die einzige Stelle, an der der Epochenschritt aus `§1.2`
gemessen wird. Ein Vektor, dessen beide Eingänge zufällig gleich sind, misst keinen von beiden.

**Nicht hier geprüft:** die Prädikat-Normalisierung selbst (Boden, Negativliste, `core`-Filter).
Sie liegt im Konstruktor von `NucleusPolicy` in Layer 01 und ist durch die Vektoren `P-1` bis
`P-6` aus `01a-policy-prompt.md §5.1` abgedeckt. Diese Datei prüft ausschließlich die
**Auflösung** aus Genesis und Verfassung.

---

## 5. `v`-Kodierungen (D55)

Format wie TV1 (`v = h'a1001864'`). Zwei Referenzwerte, damit die 32-Byte-Felder reproduzierbar
sind und nicht aus der Luft kommen:

```
unit_ref   = SHA-256("mar/example/unit-of-account/Stunde")
           = e3151c99703d8a9723d0e33a1b32234db31826d710f12e3d1b80c6318e859291
reason_ref = SHA-256("mar/example/verdict-reason/nichtlieferung")
           = 974a63cba3658a639ebd25c469e33365d805c5fd3f55d6859c80a8c4c79d55b4
```

| ID | Profil | Inhalt | `v` (hex) |
|---|---|---|---|
| `TV-O1` | `obligation@1` | `{0: 4711, 1: unit_ref}` | `a200191267015820e3151c99703d8a9723d0e33a1b32234db31826d710f12e3d1b80c6318e859291` |
| `TV-R1` | `receipt@1` | `{0: 1750}` | `a1001906d6` |
| `TV-V1` | `verdict@1` | `{0: 3, 1: reason_ref}` | `a20003015820974a63cba3658a639ebd25c469e33365d805c5fd3f55d6859c80a8c4c79d55b4` |

Die Beträge sind absichtlich krumm. `4711` und `1750` sind keine Vielfachen einer runden Zahl
und stehen in keinem Verhältnis zueinander — es gibt in dieser Schicht keine Rechnung, in der
sie ein Verhältnis haben dürften, und ein Testlauf, der eines herstellt, hat einen Fehler.
`outcome = 3` ist bewusst weder `0` noch `1`, damit kein Werkzeug es für einen Wahrheitswert
hält.

**Positive Gegenprobe für die Tilgung:**

| ID | `receipt.v` | tilgt? |
|---|---|---|
| `TV-R0` | abwesend | **ja** |
| `TV-R2` | `a10701` = `{7: 1}` — nur ein opaker Key | **ja** |
| `TV-R1` | `a1001906d6` = `{0: 1750}` | **nein**, `PARTIAL_RECEIPT_UNSUPPORTED` |

`TV-R2` ist der Vektor gegen die strikte Lesart. Eine Implementierung, die „`v` muss leer oder
abwesend sein" verlangt, ist hier rot — geprüft wird Key `0`, nicht die Map als Ganzes.

**Typverstoß:**

| ID | `obligation.v` | Antwort |
|---|---|---|
| `TV-T1` | `a1006434373131` = `{0: "4711"}` | `INVALID_V_TYPE`, kein Reject |

---

## 6. Kanonizität von `v` (D77)

Dieselben vier Verstoßklassen wie in `02c-canon-v`, hier auf `receipt@1` angewandt, weil das
Ergebnis dort **nicht** folgenlos ist.

| ID | `receipt.v` (hex) | dekodiert zu | kanonisch | Antwort |
|---|---|---|---|---|
| `CV-1` | `a100190064` | `{0: 100}` | nein | `NON_CANONICAL_V` + `PARTIAL_RECEIPT_UNSUPPORTED`, tilgt nicht |
| `CV-2` | `bf001864ff` | `{0: 100}` | nein | dito |
| `CV-3` | `a20901001864` | `{9: 1, 0: 100}` | nein | dito |
| `CV-4` | `a2001864001865` | `{0: 101}` | nein | dito |
| `CV-5` | `a1001864` | `{0: 100}` | **ja** | nur `PARTIAL_RECEIPT_UNSUPPORTED` |
| `CV-6` | `a1` | — | — | `UNPARSABLE_V`, tilgt nicht, **keine Exception** |

**`CV-6` ist der Abnahmevektor**, nicht der interessanteste: `is_canonical` dekodiert selbst und
wirft bei undekodierbarer Eingabe. Eine Prüfung vor dem Dekodieren verwandelt einen Vermerk in
eine durchschlagende Exception.

**`CV-1` bis `CV-4` tilgen aus zwei Gründen nicht** — der Payload ist unlesbar *und* er trägt
(oder könnte tragen) Key `0`. Beide Vermerke erscheinen. Eine Implementierung, die bei
`NON_CANONICAL_V` abbricht und `PARTIAL_RECEIPT_UNSUPPORTED` unterschlägt, ist rot: die
Wirkung stimmt, die Diagnose nicht, und der Betreiber liest daraus eine andere Ursache.

---

## 7. Mitgliedschaft (D60, D61, D62)

`membership(store, subject=BOB, scope=…, constitution_hash=…, now=…, authorized_keys=…)`.
Grundlage ist Profil A, sofern nicht anders vermerkt; `authorized_keys = {ALICE}`.

| ID | `accept-rules` (BOB) | `grant-membership` (→ BOB) | Zustand | Vermerke |
|---|---|---|---|---|
| `MB-1` | aktiv, auf `890b21e7…` | aktiv, von ALICE | `MEMBER` | — |
| `MB-2` | aktiv | fehlt | `APPLICANT` | — |
| `MB-3` | fehlt | aktiv, von ALICE | `GRANT_ONLY` | — |
| `MB-4` | fehlt | fehlt | `NONE` | — |
| `MB-5` | aktiv, dann **widerrufen** | aktiv, von ALICE | `GRANT_ONLY` | — |
| `MB-6` | aktiv | aktiv, dann **widerrufen** | `APPLICANT` | — |
| `MB-7` | aktiv, auf `f306b625…` (Profil C) | aktiv, von ALICE | `GRANT_ONLY` | `CONSTITUTION_VERSION_MISMATCH` |
| `MB-8` | aktiv | aktiv, von **CAROL** | `APPLICANT` | `UNAUTHORIZED_GRANT_AUTHOR` |
| `MB-9` | aktiv, aber `N = N_B` | aktiv, von ALICE | `GRANT_ONLY` | `SCOPE_MISMATCH` |

**`MB-5` und `MB-6` sind das Paar, für das es vier Zustände gibt.** `MB-5` ist der Austritt (X
widerruft die Annahme), `MB-6` der Ausschluss (N widerruft den Grant). Mit einem Wahrheitswert
sind beide `False`; `05 §1` Stufe 4 muss sie unterscheiden können.

**`MB-7` und `MB-8` sind die Gegenprofil-Abweichungen 4 und 5.** Beide erzeugen denselben
Effekt — der betroffene Claim zählt gar nicht —, aber verschiedene Vermerke.

**Getragene Grenze, hier festgehalten:** `MB-2` und `MB-6` liefern beide `APPLICANT` und sind im
Ergebnis **nicht** unterscheidbar; ebenso `MB-3` und `MB-5`. Die Zustandsmaschine sagt „inaktiv",
nicht „warum". Wer die Historie braucht, liest den Store. Das ist Absicht (`03 §1.1`) und kein
fehlender Zustand.

---

## 8. Tilgung (D63, D64, D65, D79)

`settlement(store, obligation=O, scope=N_A, now=…, policy=P-A)`. Gläubiger ist BOB, Schuldner
ALICE, sofern nicht anders vermerkt.

| ID | Lage | Zustand | Vermerke |
|---|---|---|---|
| `SE-1` | `O` aktiv, `R` von BOB, `v` abwesend | `SETTLED` | — |
| `SE-2` | `O` aktiv, keine Quittung | `OPEN` | — |
| `SE-3` | `R` trägt `TV-R1` (`{0: 1750}`) | `OPEN` | `PARTIAL_RECEIPT_UNSUPPORTED` |
| `SE-4` | `R` von **ALICE** (dem Schuldner) | `OPEN` | — |
| `SE-5` | `R.N = N_B` | `OPEN` | `SCOPE_MISMATCH` |
| `SE-6` | `O.J.tag = claim-ref` statt `identity` | `OPEN` | — |
| `SE-7` | `R` aktiv, dann von BOB **widerrufen** | `OPEN` | — |
| `SE-8` | `O` mit `t_exp`, `now > t_exp` | `EXPIRED` | `EXPIRING_OBLIGATION` |
| `SE-9` | `O` `pending` (Vorgänger unbekannt) | `INDETERMINATE` | `OBLIGATION_PENDING` |
| `SE-10` | Schuldner hat gegabelt, `O` `equivocation_flagged` | `INDETERMINATE` | `OBLIGATION_AUTHOR_FLAGGED` |
| `SE-11` | `O` aktiv, ALICE widerruft `O` | `OPEN` | — |
| `SE-12` | wie `SE-11`, aber `scope = N_B`, `policy = P-B` | `OPEN` | — |
| `SE-13` | `O` **aktiv** mit `t_exp` in der Zukunft | `OPEN` | `EXPIRING_OBLIGATION` |

**`SE-11` ist der Kernvektor der ganzen Schicht.** Ohne Policy wäre `O` widerrufen und die
Schuld verschwunden; unter der Policy bleibt sie stehen. Das ist das Schulden-Lösch-Loch, und
dieser eine Vektor ist der Grund, warum Layer 01 für `01a-policy` aufgetaut wurde.

**`SE-12` ist derselbe Vektor unter Profil B** — einer Verfassung, die `obligation@1` **nicht**
nennt und stattdessen `vouch@1` deklariert. Das Ergebnis muss identisch sein. Eine
Implementierung, die den Boden aus D70 nur bei Schweigen setzt, ist hier rot und bei `SE-11`
grün.

**`SE-7` hält die Nicht-Monotonie fest** (D64): die Quittung ist widerrufbar, die Schuld lebt
wieder auf. Getragen, nicht repariert.

**`SE-4` und `SE-6` prüfen die zweite Bedingung aus D63** von beiden Seiten: einmal stimmt der
Autor der Quittung nicht, einmal ist die Obligation gar nicht auf eine Identität ausgestellt.

**Nicht als Vektor, sondern als `assert`** (D75): `O` im Zustand `revoked` oder `superseded` ist
unter jeder Policy unerreichbar, weil der Boden aus D70 unbedingt gilt; `linked` ist es, weil es
nur bei `now is None` entsteht und `now` hier immer ein `int` ist. Die Unmöglichkeit wird
zugesichert, die Semantik nicht getestet.

---

## 9. Verdikt-Status (D67, D78)

Grundlage ist **Profil B**: `arbitrators = [ALICE, BOB]`, `scope = N_B`. Ankläger ist ALICE,
Beschuldigter BOB, Schiedsrichter CAROL — ein Dritter, damit Pfad (i) fällt und Pfad (ii)
tragen muss.

| ID | Verdikt von | `accusation.J` | Unterwerfungen auf CAROL | Status | Vermerke |
|---|---|---|---|---|---|
| `VS-1` | ALICE | `[identity, BOB]` | keine | `BINDING` | — |
| `VS-2` | CAROL | `[identity, BOB]` | keine | `ATTRIBUTED_OPINION` | — |
| `VS-3` | CAROL | `[identity, BOB]` | ALICE **und** BOB, aktiv | `BINDING` | — |
| `VS-4` | CAROL | `[claim-ref, X]`, `X.I = BOB` | ALICE **und** BOB, aktiv | `BINDING` | — |
| `VS-5` | CAROL | `[identity, BOB]` | nur ALICE | `ATTRIBUTED_OPINION` | — |
| `VS-6` | CAROL | `[identity, BOB]` | beide, BOBs **widerrufen** | `ATTRIBUTED_OPINION` | — |
| `VS-7` | CAROL | `[identity, BOB]` | beide, aber `N = N_A` | `ATTRIBUTED_OPINION` | `SCOPE_MISMATCH` |
| `VS-8` | CAROL | `[claim-ref, X]`, `X` unbekannt | beide, aktiv | `ATTRIBUTED_OPINION` | `UNRESOLVED_ACCUSED` |
| `VS-9` | CAROL | `[identity, BOB]` | beide, aktiv; **Verdikt widerrufen** | `ATTRIBUTED_OPINION` | `INACTIVE_VERDICT` |
| `VS-10` | CAROL | `[identity, BOB]`, Anklage **widerrufen** | beide, aktiv | `BINDING` | — |
| `VS-11` | CAROL | `verdict.J.tag = identity` | beide, aktiv | `ATTRIBUTED_OPINION` | `UNKNOWN_ACCUSATION` |
| `VS-12` | CAROL | Anklage mit `N = N_A` | beide, aktiv | `ATTRIBUTED_OPINION` | `SCOPE_MISMATCH` |
| `VS-13` | ALICE | `[identity, BOB]` | keine · **`verdict.N = N_A`** | `ValueError` | — |
| `VS-14` | ALICE | `[identity, BOB]` | keine · **`verdict.p` ist `accusation@1`** | `ValueError` | — |

**`VS-1` gegen `VS-3` ist die Pfadtrennung.** Bei `VS-1` bindet der Pfad über die Verfassung,
und die Unterwerfungen sind irrelevant; bei `VS-3` ist es umgekehrt. Unter Profil A — ein
Arbitrator, ALICE — wäre `VS-3` nicht konstruierbar, ohne den Schiedsrichter zu wechseln.

**`VS-3` gegen `VS-4` ist die Parteiform** aus D67 (b): einmal steht der Beschuldigte direkt in
`J`, einmal muss er über den Autor des bestrittenen Claims aufgelöst werden.

**`VS-6` ist der D78-Vektor.** Er ist der einzige, der „vorab" von „aktiv zum
Bewertungszeitpunkt" unterscheidet: die Unterwerfung *gab* es, sie ist nur nicht mehr aktiv. Wer
„vorab" als „irgendwann einmal ausgestellt" liest, ist hier grün und damit falsch.

**`VS-13` und `VS-14` sind die Eingangsprüfung** (`03 §1.4`, `§2.4.2`). Ohne sie bindet ein
Verdikt aus Nukleus B einen Streit in Nukleus A, sobald sein Autor in beiden Arbitratorenlisten
steht — bei `VS-13` steht ALICE in beiden. Der Fall ist nicht exotisch: ein anerkannter
Schiedsrichter sitzt typischerweise in mehreren Nuklei.

**`VS-12` gegen `VS-11` trennt zwei Diagnosen mit gleicher Wirkung.** Eine Anklage aus fremdem
Scope ist **bekannt** und zählt nur nicht; `UNKNOWN_ACCUSATION` schickte den Betreiber in die
Partitionsecke, während das Objekt vor ihm liegt.

**`VS-10` hält fest, dass der Zustand der Anklage irrelevant ist.** Sie wird nur gelesen, um die
Parteien zu bestimmen; wer die Parteien *waren*, ändert sich durch einen Widerruf nicht.

---

## 10. Scope-Gleichheit (D81)

Drei Vektoren, einer je Beziehung. Alle bereits oben enthalten, hier zusammengezogen, weil sie
eine gemeinsame Regel prüfen und gemeinsam veralten würden:

| Beziehung | Vektor | Ohne die Regel |
|---|---|---|
| `receipt` ↔ `obligation` | `SE-5` | eine Identität in B quittiert eine Schuld aus A |
| `submit-arbitration` ↔ `verdict` | `VS-7` | eine Unterwerfung in A bindet einen Streit in B |
| `accept-rules` ↔ `grant-membership` | `MB-9` | eine Annahme in B begründet Mitgliedschaft in A |

`01 §2.2` Regel 3 erzwingt nur, dass `N` gesetzt und selbstkonsistent ist. Ohne `03 §1.4` ist
keiner der drei Fälle ein Fehler.

---

## 11. Abgeleitete Invarianten (als Tests zu implementieren)

| ID | Aussage |
|---|---|
| `PR-INV-1` | Für **jede** Eingabe enthält `resolve_policy(...).policy.irrevocable` den Eintrag `"obligation@1"` (D70). |
| `PR-INV-2` | `policy.irrevocable ∩ TRUST_GRANTING = ∅` (D58). |
| `PR-INV-3` | Kein Element von `policy.irrevocable` bezeichnet ein `core`-Prädikat (D71). |
| `PR-INV-4` | Jede der vier Funktionen wirft `ValueError`, wenn `policy.scope ≠ scope` (D73) — geprüft **bevor** der Store gelesen wird. |
| `PR-INV-5` | `settlement()` ist ohne `policy` nicht aufrufbar (`TypeError`), `membership()` und `verdict_status()` sind es (D80). |
| `PR-INV-6` | `MEMBER` ⟹ beide `claim_id` gesetzt; jeder andere Zustand ⟹ mindestens eine `None`. |
| `PR-INV-7` | `SETTLED` ⟹ Quittungs-`claim_id` gesetzt **und** `receipt.v` trägt keinen Key `0`. |
| `PR-INV-8` | `BINDING` ⟹ das Verdikt ist aktiv (D67 + `INACTIVE_VERDICT`). |
| `PR-INV-9` | `findings` ist in allen vier Ergebnistypen sortiert und dedupliziert. |
| `PR-INV-10` | `classify_all` ist in `profiles/` **dasselbe Funktionsobjekt** wie in `trust/` — Identitätsvergleich, wie `PR-INV-4` in `02b` für `derive()`. |
| `PR-INV-11` | Kopplung mit Policy, **scope-lokal**: für `c` mit `nuc:`-Prädikat und `c.N != policy.scope` gilt `classify_all(store, now, policy)[claim_id(c)] == classify(c, store, now, None)`, für alle übrigen `== classify(c, store, now, policy)`. Die Erweiterung von `T-02.4` um den Parameter. |
| `PR-INV-12` | `classify_all(store, now, policy)` wirft **nie**, gleich wie viele Nuklei der Store trägt. Zu prüfen an einem Store, der Claims aus `N_A`, `N_B` und `N_C` gemischt enthält. |
| `PR-INV-13` | Jede Funktion, die einen Claim als Argument nimmt, wirft `ValueError` bei falschem Prädikat, falschem `N` oder fehlendem Store-Eintrag — geprüft für `settlement()` und `verdict_status()` in derselben Form (`03 §1.4`). |

`PR-INV-1` ist als Eigenschaftstest über alle drei Profile plus die fehlende Verfassung zu
führen, nicht als vierter Einzelvektor: der Boden gilt unbedingt, und „unbedingt" ist eine
Aussage über alle Eingaben.

---

## 12. Forkstand

Entschieden und in dieser Datei verankert: **D55–D69, D77–D82**.

Offen, außerhalb dieser Datei:

- **Zweiter Durchgang `05 §3`** — Vokabular `BINDING`/`ATTRIBUTED_OPINION` und der Satz, dass
  ein nicht bindendes Verdikt keinen Statuswechsel auslöst, unabhängig von der Severity (D68).
  `03` definiert das Vokabular selbst, damit es nicht auf Text zeigt, den es nicht gibt.
- **`00 §5.1`** zieht auf „aktiv zum Bewertungszeitpunkt" nach (D78).
- **`05 §2`** verweist auf „Profile-II §7.1" — das ist `01 §7.1`. Alter Tippfehler.
- **`02d-purpose`** (Zweck-Tag, D56). `00a-rotate-key` ist gebaut (D160), aber ohne Aufrufer in
  dieser Schicht: `authorized_keys` bleibt Parameter.
- **`example-nucleus.md`** mit `D = 100`, `C₀ ≤ 100`, niedrigem `k_slash`. Mit `03` dringender
  geworden, weil `unit_ref` und die Irrevocable-Markierung dort landen.
