# Nukleus-Fundament — Genesis · Verfassung · Schlüssel-Autorität — Spezifikation v1

Status: Entwurf · Protokollversion: 1 · Layer: Scope-Fundament (unter Governance, definiert `N`)

Diese Schicht definiert, **was ein Nukleus-Scope `N` eigentlich ist**, bevor Trust-Flow, Profile,
Governance und Enforcement darauf partitionieren. Sie schließt die Design-Forks **DF-0** (Scope-
Identität), **DF-3** (Verfassungs-/irrevocable-Schema) und liefert die Träger für **DF-2**
(Arbitrationsbindung) und **DF-4** (Schwellen). Sie führt **kein** Atom-Feld ein: Genesis und
Verfassung sind content-adressierte Objekte (wie die Verfassung schon in Atom-Spec §7.2), Rotation
ist ein Profil.

> **Numerierungshinweis.** Konzeptuell sitzt dieses Kapitel *zwischen* Atom (das `N` als opaken
> 32-Byte-Scope kennt, Atom-Spec §2.3) und Governance (das auf Mitgliedschaft baut). Es kann als
> `00-…` vorangestellt oder in `04-governance.md §1` gezogen werden. Bis zur Entscheidung: `00`.

---

## 1. Leitsätze (Geltungsrahmen)

- **F1 — Scope = Genesis-Hash, nicht Schlüssel (DF-0, entschieden).** Die stabile Scope-ID `N`
  ist der Hash eines **unveränderlichen Genesis-Objekts**, **nie** ein Signierschlüssel. Ein
  Nukleus behält seine Identität, während seine Schlüssel rotieren und seine Verfassung sich
  ändert. Das ist die einzige Wahl, die mit Schlüsselrotation **und** FROST-Re-Keying konsistent
  ist (§6).
- **F2 — Drei-Objekt-Modell.** Ein Nukleus besteht aus drei getrennten Objekten nach Lebensdauer:
  **Genesis** (unveränderlich, definiert `N`), **Verfassung** (versioniert, per Governance
  geändert), **Schlüssel-Nachfolge** (verkettet, per Rotation fortgeschrieben). Keines ist ein
  Atom-Feld.
- **F3 — Schlüssel ≠ Identität des Nukleus.** Wer *als* der Nukleus handeln darf, ist eine
  auflösbare Frage (`resolve_current_key`, §6.4), nicht eine feste Bytefolge. `grant-membership`
  und jeder andere Nukleus-Akt wird vom **aktuell autorisierten** Schlüssel signiert, nicht von
  „`I == N`" (§7).
- **F4 — Gewaltenteilung bei der Rotation (DF-0-Folgeentscheidung).** Der Schlüssel reicht sich im
  Normalfall selbst weiter (Key-Chain, billig, kein Quorum). Bei Verlust/Diebstahl entscheiden die
  **Mitglieder** per Governance-Akt. Der Konfliktfall (zwei konkurrierende Nachfolger) fällt
  mechanisch auf denselben Equivocation-Beweis wie jeder andere Fork zurück (§6.3).
- **F5 — Verfassung hat ein Minimal-Schema, bleibt sonst opak (DF-3).** Damit sicherheitskritische
  Policy (irrevocable Prädikate, Schwellen, Arbitration, Stimmmodus) **maschinenlesbar
  durchgesetzt** werden kann, definiert dieses Kapitel eine normative Teilstruktur des
  Verfassungsobjekts. Alles darüber hinaus bleibt uninterpretiert (A2).

---

## 2. Die drei Objekte

| Objekt | Lebensdauer | Adressierung | Ändert sich per |
|--------|-------------|--------------|-----------------|
| **Genesis** | unveränderlich | `N = H(genesis)` (§3) | nie |
| **Verfassung** | versioniert | Content-Hash, `accept-rules@1` zeigt darauf | Ratifizierung (`04 §4`) |
| **Schlüssel-Nachfolge** | fortlaufend | Kette von `rotate-key@1`-Claims ab Genesis-Key | Rotation / Governance (§6) |

Die drei sind bewusst entkoppelt: **`N` bleibt fix**, während Verfassung und Schlüssel wandern.
Das ist der ganze Punkt von DF-0.

---

## 3. Scope-Ableitung

```
DOM_NUC_GEN = "claim-atom/v1/nucleus-genesis"

N = SHA-256( DOM_NUC_GEN || cbor_deterministic(genesis_obj) )     ; 32 B
```

- Eigener Domänen-Separator, damit `N` **nie** mit dem Identity-Genesis-Anker (`DOM_ID_GEN`,
  Atom-Spec §4) oder einer `claim_id` kollidiert, selbst bei sonst gleichen Bytes.
- `genesis_obj` wird in **kanonischem CBOR** (Atom-Spec §3) kodiert — ohne Determinismus wäre `N`
  nicht reproduzierbar.
- Ein Verifizierer, der `genesis_obj` kennt, rechnet `N` selbst nach und prüft, dass jeder
  Claim mit Feld `N` tatsächlich zu **diesem** Genesis gehört. Kein Nachschlagen einer Autorität.

### 3.1 Worked Example (real gerechnet, geteilt mit `01` Anhang C)

Ein vollständig durchgerechnetes, **schema-valides** Beispiel-Nukleus. `N` und `constitution_hash`
hier sind **byte-identisch** mit den Test-Vektoren in Anhang C von `01-claim-atom.md` — die ganze
Spec-Reihe testet gegen *denselben* Anker. Reproduzierbar via kanonischem CBOR (RFC 8949).

Ed25519-Identitäten (Seeds `01×32` / `02×32`):
```
ALICE = 8a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c
BOB   = 8139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df60f5b8fc9b394
```

**Verfassungsobjekt** (Text-Keys, Minimal-Schema §5; Ratios als `[num, den]`, floatfrei):
```
constitution = {
  irrevocable_predicates: ["obligation@1"],
  thresholds:            { ordinary: [1,2], membership: [2,3], amendment: [3,4] },
  arbitration:           { arbitrators: [ALICE] }
}
cbor(constitution)      = a36a7468726573686f6c6473a3686f7264696e61727982010269616d656e646d
                          656e748203046a6d656d626572736869708202036b6172626974726174696f6e
                          a16b61726269747261746f72738158208a88e3dd7409f195fd52db2d3cba5d72
                          ca6709bf1d94121bf3748801b40f6f5c7669727265766f6361626c655f707265
                          64696361746573816c6f626c69676174696f6e4031
constitution_hash       = SHA-256(cbor(constitution))
                        = 890b21e7cd43fc4226938ce0b6eae1d00efa04ef9e6585c352dcf19ccad5ea7e
```

**Genesis-Objekt** (uint-Keys, Schema §4; `parent_scope` weggelassen ⇒ Top-Level-Nukleus):
```
genesis = {
  0 version           : 1
  1 root_keys         : [ALICE]
  2 key_mode          : 0            ; Einzelschlüssel
  3 anchor_set        : [ALICE]      ; Nukleus-Seed (Trust-Flow §6.3)
  4 constitution_hash : 890b21e7cd43fc42…
  5 amendment_rule    : 2            ; Schwellenklasse-Index (Policy)
  6 weight_mode       : 1            ; zweck-gescopt gewichtet (Gov §4)
  7 vote_mode         : 0            ; Komposition (Gov §3)
}
cbor(genesis)           = a80001018158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3
                          748801b40f6f5c0200038158208a88e3dd7409f195fd52db2d3cba5d72ca6709
                          bf1d94121bf3748801b40f6f5c045820890b21e7cd43fc4226938ce0b6eae1d0
                          0efa04ef9e6585c352dcf19ccad5ea7e050206010700
N = SHA-256(DOM_NUC_GEN ‖ cbor(genesis))
  = 65309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557
```

Ein Verifizierer, der `genesis` kennt, rechnet `N` selbst nach (oben) und prüft, dass jeder
Claim mit Feld `N == 65309fe2…` zu genau diesem Genesis gehört — ohne Autorität zu befragen.

---

## 4. Genesis-Objekt — normatives Schema

Kanonische CBOR-Map. Unveränderlich (jede Änderung erzeugt ein **anderes** `N` = einen anderen
Nukleus). Pflichtfelder:

| Key | Feld | Typ | Bedeutung |
|----:|------|-----|-----------|
| 0 | `version` | uint (=1) | Genesis-Format-Version. |
| 1 | `root_keys` | array[bytes32] | **Initial** autorisierte Signierschlüssel (§6.4). Ein Key **oder** ein FROST-Gruppenschlüssel. |
| 2 | `key_mode` | uint | `0` = Einzelschlüssel, `1` = FROST-Gruppenschlüssel. |
| 3 | `anchor_set` | array[bytes32] | Der **Nukleus-Seed** (Trust-Flow-Spec §6.3): das out-of-band etablierte Ankerset. |
| 4 | `constitution_hash` | bytes32 | Hash der Verfassung der **Epoche 1** (§5). Spätere Fassungen entstehen per Ratifizierung; welche gilt, ist Parameter der Auflösung und wird nicht aus dem Genesis gelesen (D167, Profile-II §1.2). |
| 5 | `amendment_rule` | uint | Schwellenklasse für Verfassungsänderung (§5, `04 §3.4`). `0` = `ordinary`, `1` = `membership`, `2` = `amendment` (D104). |
| 6 | `weight_mode` | uint | `0` = Kopfzahl, `1` = zweck-gescopt gewichtet (`04 §3.5`, D98). |
| 7 | `vote_mode` | uint | `0` = Komposition (Default), `1` = FROST-Opt-in (`04 §5`). Löst DR-015. |
| 8 | `parent_scope` | bytes32 (optional) | **Rein deklarativ.** Behauptete Zugehörigkeit oder Nachfolge; ohne mechanische Folge (§4.1, D114). |
| 9 | `trust_params` | map (optional) | `{0: C₀, 1: γ_num, 2: γ_den, 3: D}`, alle uint. Kalibrierung des Trust-Flow (Trust-Flow-Spec §8, D115). Fehlt der Key, sind die Parameter out-of-band. |

- `root_keys` trennt **Identität** (= `N`, aus dem *ganzen* Genesis) von **Autorität** (= die
  Schlüssel, die *innerhalb* stehen). Genau diese Trennung erlaubt Rotation ohne Identitätsverlust.
- `vote_mode`/`weight_mode`/`amendment_rule` im Genesis machen die Konsens-Parameter **vor** der
  ersten Abstimmung fest und prüfbar — kein „Modus-Wechsel mittendrin" ohne Amendment.
- Die Änderungsregel ist **nicht** unveränderlich, aber nicht kaperbar: die anzuwendende Schwelle
  ist das Maximum aus alter und neuer (Gov-Spec §3.4). Anheben verlangt die neue, Senken die alte.

**Schlüsseltypen (D462).** Jeder Map-Schlüssel des Genesis-Objekts ist ein uint, auch in
`trust_params`. Ein Objekt mit einem anderen Schlüssel, etwa `true`, `1.0` oder `-1`, ist kein
Genesis: ein Leser weist es ab wie eines, dessen Hash nicht `N` ist, und liest keinen seiner Werte.
Der Grund ist derselbe wie in `02 §3.1`. Unter anderen Schlüsseltypen hängt es an der Sprache des
Lesers, welcher Wert unter Key `1` steht, und der Gründer könnte die Schlüsselauflösung seines
Nukleus über Implementierungen spalten.

### 4.0 `trust_params` — warum im Genesis

`D` steckt über `n/D` in jedem signierten Vouch. Läge es in der änderbaren Verfassung, würde ein
Amendment Bestandssignaturen still umbewerten; D35 verlangt deshalb Unveränderlichkeit über die
Lebensdauer eines Scopes, und unveränderlich ist nur das Genesis. `C₀` und `γ` reisen mit, weil ein
Nukleus, der die eine Hälfte der Kalibrierung festlegt und die andere nicht, keine reproduzierbare
Kapazität hat.

Wohlgeformt bei Anwesenheit: `C₀ >= 1`, `D >= 1`, `1 <= γ_num < γ_den`. SHOULD: `D >= C₀`
(Trust-Flow-Spec §8), damit stets `C(I)` bindet und nicht `D`.

Die harte Reichweite folgt: `r_max = ⌊log_{1/γ} C₀⌋`. Jenseits davon ist `⌊C₀γ^d⌋ = 0`, und kein
Vouch trägt mehr — die quantitative Fassung von „maximal lokal".

Das Protokoll fixiert **keinen Default**. Ein Reichweitenparameter verteilt Macht und ist damit
Verfassungsinhalt (`08 §3`); das Genesis ist nur der Ort der Festlegung, nicht der Ort der Wahl.

### 4.1 `parent_scope` ist eine Behauptung, keine Beziehung

Das Feld wird von **keiner** Funktion dieser Referenzimplementierung gelesen. Es begründet keine
Autorität, keine Übertragung, keinen Vorrang und keine Sichtbarkeit über Scope-Grenzen hinweg —
`02 §2` ist unverändert bindend: es gibt einen Graphen je `N`, und Vertrauen aus einem Scope
fließt nicht in einen anderen.

Was es leistet: Es **behauptet** eine Zugehörigkeit oder eine Nachfolge, prüfbar über die
Genesis-Kette, bewertet vom Leser. Das Protokoll erzwingt Zurechenbarkeit, nicht Wahrheit
(`08 §2.1`).

Daraus folgt ausdrücklich: **mehrere Nuklei dürfen dieselbe Elternschaft behaupten**, und keiner
kann einen anderen daran hindern. Spaltet sich eine Gemeinschaft, berufen sich beide Hälften auf
denselben Vorgänger; welche als Fortsetzung gilt, entscheiden die Beteiligten und nicht ein
Register. Das Protokoll bildet den Streit ab, statt ihn zu entscheiden.

Es gibt **keine Stilllegungsmarkierung** und soll keine geben. Ein Nukleus, in dem niemand mehr
signiert, ist stillgelegt; das erkennt jeder Beobachter an seinem eigenen Bestand. Eine Markierung
wäre eine globale Aussage über etwas, das nur lokal beobachtbar ist.

### 4.2 Empfehlung: Governance und Substanz in getrennte Scopes

Keine Prüfung, eine Empfehlung — und die folgenreichste Entscheidung bei der Gründung.

Vouches, Obligationen und Quittungen gehören **nicht** in den Scope, dessen `participants`
abgestimmt werden. Ein Governance-Scope regiert genau eine Sache: sich selbst. Die Substanz lebt
in einem eigenen Scope, der keine `participants` deklariert und damit nicht auszählbar ist — er
braucht auch keine, denn Bürgen, sich verpflichten und quittieren sind zweiseitige Akte ohne
Kollektivbeschluss.

**Der Schnitt entscheidet, was eine Trennung später kostet.** Liegt die Substanz im
Governance-Scope, kostet ein Zerwürfnis die gesamte gescopte Geschichte. Liegt sie daneben, kostet
es das Regelwerk — die Vertrauenskanten und Kreditbeziehungen tragen ein anderes `N` und bleiben
unberührt, egal wie fest der Governance-Scope steckt.

Der Preis der Trennung: ein Scope ohne Governance hat **unveränderliche Arbitratoren**, weil
`03 §2.4` sie aus der Verfassung des eigenen Scopes nimmt. Wer beides will — änderbare Regeln und
unangreifbare Substanz — braucht drei Scopes oder muss einen der beiden Nachteile tragen.

---

## 5. Verfassungs-Minimal-Schema (DF-3)

Die Verfassung ist ein content-adressiertes, **versioniertes** Objekt. Ihr **Großteil bleibt
opak/Policy** (A2). Aber fünf Felder sind **normativ** und **MÜSSEN** von Verifizierern honoriert
werden, weil an ihnen Sicherheit hängt:

| Feld | Typ | Zweck | Schließt |
|------|-----|-------|----------|
| `irrevocable_predicates` | array[text] | Prädikate, deren `core/revoke`/`core/supersede` **ignoriert** werden (Atom-Spec §5.4). Profilnamen ohne Scope-Präfix. `obligation@1`, `rotate-key@1` und `rotate-ack@1` gelten auch ungenannt (§5.2); trust-gewährende Prädikate werden verworfen (Atom-Spec §5.4.3 b). | **P-1 / DR-030** |
| `thresholds` | map{text→ratio} | Quorum je Schwellenklasse (`ordinary`, `membership`, `amendment`, …). | DR-012 |
| `arbitration` | map | Zuständige Schiedsrichter / Klausel (§5.1). | **E-1 / DR-029** |
| `enforcement_policy` | map (optional) | Cure-Kurve, terminale Fehler (Enf-Spec §4, §8). | DR-022 |
| `nucleus_keys` | array[bytes32] (optional) | Die per Governance gesetzten autorisierten Schlüssel (§5.4, §6.2). Fehlt das Feld, gilt `genesis.root_keys`. | **DF-0 / D150** |

### 5.1 `arbitration` (Träger für DF-2)

```
arbitration = {
  arbitrators:  [bytes32],     ; Identities, die im Scope urteilen dürfen
  clause_hash?: bytes32,       ; optional: Verweis auf eine ausführlichere Schlichtungsordnung
}
```

Ein `verdict@1` **bindet** nur, wenn sein Autor entweder (i) in `arbitration.arbitrators` steht,
**oder** (ii) beide Parteien vorab per `submit-arbitration@1` (Profile-II §2.4) auf ihn
gezeigt haben. Fehlt beides, ist das Verdikt **attributed_opinion** ohne Statuswechsel
(Enforcement-Spec §3, geänderte Fassung — siehe DF-2). Das ist die maschinenlesbare Antwort
auf E-1.

### 5.2 Sicherheits-Default: ein Boden, keine Rückfallebene

`obligation@1`, `rotate-key@1` und `rotate-ack@1` sind **immer** irrevocable
(Protokoll-Default, Profile-II §3.3.3 und §6.1). `irrevocable_predicates` kann die Menge nur
**erweitern**, nie verkleinern — gemessen am Boden, nicht an der Vorgängerfassung. Ein Amendment
darf ein früher deklariertes Prädikat weglassen (`04 §8`, D424):

```
wirksame Menge  =  { "obligation@1", "rotate-key@1", "rotate-ack@1" }
                   ∪  irrevocable_predicates  ∖  unsicher (Atom-Spec §5.4.3 b)
```

Die beiden Rotationsprädikate stehen aus einem eigenen Grund darin (D153): wäre eine Ack
widerrufbar, könnte der Nachfolger seine Zustimmung zurücknehmen und die Autorität spränge auf
den Vorgänger zurück — genau die Lage, die D125 unter „letzter gewinnt" verworfen hat, nur von
der anderen Seite erreicht.


Damit gilt der Schutz in drei Fällen gleichermaßen: die Verfassung schweigt; sie nennt
`obligation@1`; sie nennt **andere** Prädikate und lässt `obligation@1` weg. Eine
Formulierung, in der der Default nur bei Schweigen greift, wäre durch das bloße Nennen einer
beliebigen anderen Zeile aushebelbar gewesen — genau das Schulden-Lösch-Loch, das dieser
Abschnitt schließen soll, nur mit einem Zwischenschritt.

**Unsichere Deklarationen fallen heraus, ohne die übrigen zu entwerten.** Nennt eine Verfassung
`vouch@1`, bleibt der Rest der Liste wirksam; der unsichere Eintrag wird verworfen und
vermerkt (`UNSAFE_IRREVOCABLE_PREDICATE`, Atom-Spec §5.4.3 b). Ein Alles-oder-nichts wäre
schlechter: eine einzelne Fehldeklaration nähme dem Nukleus auch den Schuldenschutz.

### 5.3 Lebenszyklus

Verfassungsupdate ⇒ neues Objekt ⇒ neuer Hash. Welche Fassung gilt, entscheidet ein `ratify@1`
über die Schwelle der Klasse (`04 §4`). Die `accept-rules@1` eines Mitglieds auf den neuen Hash
entscheidet über seine eigene Mitgliedschaft, nicht über das Zustandekommen (`04 §7.1`, D470).
**`N` bleibt fix**, weil `N` aus dem *Genesis*, nicht aus der Verfassung abgeleitet ist.

### 5.4 `nucleus_keys` — Träger der Governance-Rotation (D150)

```
nucleus_keys = [bytes32]     ; die autorisierten Schlüssel des Nukleus
```

Fehlt das Feld, gilt `genesis.root_keys`. Ist es gesetzt, **ersetzt** es den Anker der Key-Chain
(§6.4 Schritt 1) vollständig: die Ketten werden ab den hier genannten Schlüsseln neu aufgebaut,
und ein `rotate-key@1` eines nicht mehr genannten Schlüssels verliert seine Wurzel und wirkt
nicht — unabhängig davon, wann er signiert wurde. Damit ist der Notfallpfad (§6.2) uhrfrei
rechenbar, ohne dass je verglichen werden müsste, ob ein Claim vor oder nach einer Epoche liegt.

Der Ort ist die Verfassung und nicht das Vorschlagsobjekt, weil `arbitration.arbitrators` dort
bereits eine Autoritätsliste derselben Bauform führt, weil eine Verfassungsänderung schon die
`amendment`-Schwelle trägt, die §6.2 verlangt, und weil ein viertes Feld im Vorschlagsobjekt die
Kodierung von `proposal_hash` änderte (D150).

**`nucleus_keys = []` bedeutet: kein autorisierter Schlüssel.** Nukleus-Akte sind dann nicht
autorisiert. Das ist die sichere Richtung, dieselbe wie in §6.4 und §9; die Gegenrichtung ließe
eine Governance, die absetzen will, ins Leere laufen. Der Preis ist, dass eine Verfassung den
Nukleus per Amendment handlungsunfähig machen kann. Das ist ausdrückbar und wird nicht verhindert.

**Wohlgeformtheit: der defekte Eintrag fällt weg, das Feld nicht (D163).** Wohlgeformt ist ein
Eintrag, der `bytes` der Länge 32 ist. Ein formwidriger Eintrag wird verworfen und vermerkt
(`MALFORMED_NUCLEUS_KEY`, ein Vermerk je Verfassung, Subjekt der `constitution_hash`); die übrigen
bleiben wirksam. Duplikate fallen wortlos zusammen, weil `nucleus_keys` eine Menge bezeichnet und
keine Auszählungsgrundlage ist — anders als `participants` in Gov-Spec §1.1, wo ein zu kleiner
Nenner jede Schwelle senkt. Eine Sortierpflicht gibt es aus demselben Grund nicht.

**Ein gesetztes Feld fällt nie auf `genesis.root_keys` zurück (D163).** Sind alle Einträge
formwidrig, oder ist der Wert gar keine Liste, ist der Anker die leere Menge. Die Gegenrichtung
wäre die Absetzungs-Umgehung: ein einziges formwidriges Byte holte die abgesetzten Wurzelschlüssel
zurück, und die Deklaration höbe durch ihre eigene Fehlerhaftigkeit den Schutz auf, den sie setzt.

---

## 6. Schlüssel-Autorität & Rotation (DF-0-Folgeentscheidung: „Beides")

Zwei Pfade, wie in F4 festgelegt.

### 6.1 Normalpfad — Key-Chain (`rotate-key@1`)

Ein **Profil**, kein `core` (Frozen-Primitive-Check §8): Rotation macht eine Aussage über *wer als
der Nukleus handeln darf* — soziale Autorität, kein selbst-bezüglicher Lebenszyklus im Sinne von
Atom-Spec §5.1. Fällt damit korrekt durch den `core`-Aufnahmetest.

| `nuc:N/rotate-key@1` | Belegung |
|----------------------|----------|
| `I` | der **aktuell autorisierte** Schlüssel `K_{n-1}` |
| `J` | `[identity, K_n]` — der Nachfolgeschlüssel |
| `N` | der Scope |
| `v` | optional: `{ effective?, note? }` |

**Kettenregel (Nachfolge, autor-verkettet):**
```
R_1 ist gültig  ⟺  R_1.I ∈ genesis.root_keys
R_n ist gültig  ⟺  R_n.I == (der von R_{n-1} benannte K_{n-1})
```
Die Nachfolge ist damit eine Kette über **Autorschaft**: jeder Schlüssel benennt genau seinen
Nachfolger. Ordnung kommt aus dieser Kette, **nie** aus Wall-Clock `t` (Atom-Spec §5.3).

**Gegenzeichnung (D125).** Ein `rotate-key@1` allein wirkt nicht. Eine Rotation ist
**vollständig**, wenn `K_n` sie gegenzeichnet. Eine unvollständige Rotation ist wirkungslos: kein
Zustand, kein eigener Vermerk, sie zählt nicht. Es bindet der **erste vollständige** Rotate.

Die Gegenzeichnung ist ein eigenes Profil `nuc:N/rotate-ack@1` mit vierteiliger Belegung (D152):

```
R_n wirkt  ⟺  R_n ist nach der Kettenregel gültig
              UND es existiert ein Claim ack mit

              ack.p  == nuc:N/rotate-ack@1
              ack.J  == [claim-ref, claim_id(R_n)]
              ack.I  == R_n.J.value    und   R_n.J.tag == identity
              ack.N  == R_n.N
```

Alle vier Bedingungen tragen. Ein eigenes Prädikat ist nötig, weil „irgendein Claim, der die
`claim_id` nennt" auch ein `core/revoke@1` von `K_n` erfüllte — eine Rücknahme als Zustimmung.
`ack.N == R_n.N` ist nicht redundant: `01 §2.2` Regel 3 erzwingt nur, dass `N` gesetzt und
selbstkonsistent ist, nicht dass zwei Claims denselben Scope teilen (dieselbe Begründung wie die
dritte Bedingung in D63).

Beide Signaturen sind selbstenthalten und reisen zusammen; die Regel braucht **weder Uhr noch
globale Ordnung**. Sie schließt drei Fälle, die die Kettenregel offen ließ: die einseitige
Einsetzung eines Dritten, den Rotate auf einen Schlüssel, dessen Halter nichts davon weiß, und den
Vertipper. Ein Altschlüssel bekommt die Kette dadurch nicht zurück — wirkt der erste vollständige
Rotate, ist `K_{n-1}` nicht mehr autorisiert, und ein späterer Rotate von ihm ist kein Akt eines
autorisierten Schlüssels mehr.

**Rotate und Ack sind irrevocable** (Protokoll-Default, §5.2, D153). Ohne das könnte `K_n` die
eigene Zustimmung zurücknehmen und die Autorität spränge zum Vorgänger zurück.

**„Erster" heißt: erster in der Kette von `K_{n-1}`, nicht erster nach Empfang (D154).** Signiert
`K_{n-1}` nacheinander zwei Rotationen auf verschiedene Nachfolger mit **verschiedener** `h_prev`,
ist das keine Equivocation (§6.3 verlangt dieselbe `h_prev`), und beide sind gültig. Bindend ist
die frühere in `K_{n-1}`s eigener Kette. Daraus folgt ausdrücklich: **trifft deren Gegenzeichnung
erst später ein, springt der aufgelöste Kopf zurück**, und Akte des zwischenzeitlichen Kopfes
verlieren rückwirkend ihre Autorisierung. Das ist dieselbe Klasse wie nachträglich entdeckte
Equivocation — mehr Wissen revidiert einen Zustand (Detect-not-Prevent, `01 §1` Axiom A3). Die
Alternative, nach Empfangsreihenfolge zu ordnen, wäre schlechter: zwei Leser mit demselben
Claim-Bestand kämen zu verschiedenen Ergebnissen.


### 6.2 Notfallpfad — Governance-Rotation

Ist `K_{n-1}` **verloren** (kann keinen `rotate-key` mehr signieren) oder die Kette **umstritten**
(§6.3), installieren die **Mitglieder** einen neuen Schlüssel per Governance-Akt: eine
Verfassungsänderung, deren `nucleus_keys` (§5.4) den neuen autorisierten Schlüssel deklariert,
ratifiziert über die **`amendment`-Schwelle** (hoch, gegen Routine-Capture). Kein neues Primitiv
und kein neues Feld im Vorschlagsobjekt — reiner Governance-Loop (Gov-Spec §2), und die Schwelle
ergibt sich, weil eine Verfassungsänderung sie ohnehin trägt (D150).

### 6.3 Präzedenz & umstrittene Rotation (der Diebstahlfall)

- **Governance schlägt Key-Chain.** Nennt die Verfassung der jüngsten ratifizierten Epoche ein
  Feld `nucleus_keys`, **ersetzt** diese Menge den Anker der Key-Chain (§5.4, §6.4 Schritt 1); die
  Ketten werden ab ihr neu aufgebaut. Es wird kein Effektivpunkt verglichen — die Epoche *ist* der
  Zustand. Begründung: die Mitglieder sind die letzte Autorität; der Schlüssel ist ihr Delegat.
- **Doppel-Nachfolger = Equivocation.** Signiert `K_{n-1}` zwei verschiedene Nachfolger, haben beide
  `I == K_{n-1}` und dieselbe `h_prev` in `K_{n-1}`s eigener Kette ⇒ **Equivocation-Beweis nach
  Atom-Spec §4**, ohne neue Mechanik. Der Verifizierer sieht eine *umstrittene* Autorität und
  behandelt Nukleus-Akte beider konkurrierender Schlüssel als **unaufgelöst**, bis die
  Governance-Rotation (§6.2) entscheidet **oder** das Mitglied per Exit/Fork ausweicht
  (Gov-Spec §6).
- Das ist genau der Grund für „Beides": ein **gestohlener** Schlüssel produziert einen zweiten
  Nachfolger → Equivocation → die Entscheidung fällt zwangsläufig an die Mitglieder, nicht an den
  Dieb.

### 6.4 `resolve_current_key(N)` — der autoritative Auflösungsalgorithmus

```
1.  Anker A bestimmen. Die Verfassung der jüngsten ratifizierten Epoche (Gov-Spec §1.1)
    wird übergeben, nicht aus der Epochenkette hergeleitet (D161). Drei Lagen:
    a) Sie liegt vor und nennt ein Feld nucleus_keys (§5.4): A ist die Menge ihrer
       wohlgeformten Einträge, auch wenn diese leer ist (D163).
    b) Sie liegt vor und nennt kein Feld nucleus_keys: A = genesis.root_keys aus dem
       Objekt, dessen Hash == N.
    c) Sie liegt lokal nicht vor: A = genesis.root_keys, mit Vermerk
       CONSTITUTION_UNAVAILABLE (D164). Das ist die unsichere Richtung, nie still.
2.  Für jedes k aus A der Kette der vollständigen Rotationen (§6.1) ab k folgen, bis zu
    dem Schlüssel, der keinen vollständigen Nachfolger hat. Dieser Schlüssel ist der
    Kopf der Kette von k.
3.  Hat k irgendeinen Claim im Zustand EQUIVOCATION_FLAGGED — an beliebiger Stelle
    seiner Autorenkette, nicht nur an einer Rotation (D162) —, liefert k keinen Kopf;
    Nukleus-Akte beider konkurrierender Schlüssel gelten als nicht autorisiert
    (Detect-not-Prevent, `01 §1` Axiom A3). Dasselbe gilt für jeden Schlüssel, den
    Schritt 2 auf der Kette erreicht, nicht nur für k selbst (D165). Eine Änderung
    von nucleus_keys löst den Fall nicht auf, indem sie denselben Schlüssel erneut
    nennt, sondern einen anderen.
4.  Rückgabe ist die Vereinigung der Köpfe aller k aus A.
```
Der Rückgabewert ist die Menge der aktuell autorisierten Schlüssel. Jeder Verifizierer rechnet das
lokal über seinen bekannten Claim-Teilgraphen (Partitionstoleranz wie Trust-Flow-Spec §7).

**Es wird nichts maximiert (D149).** Mehrere Elemente in `A` sind mehrere **parallele** Ketten,
keine konkurrierenden: jede Rotation ersetzt den Schlüssel ihres **eigenen** Autors, und Konkurrenz
innerhalb einer Wurzel ist Equivocation, die Layer 01 seit jeher führt. Der frühere Wortlaut „folge
der längsten Kette" ist damit gegenstandslos.

**Ein defektes Kettenglied blockiert nichts (D154).** Eine ungültige oder eine unvollständige
Rotation ist schlicht kein Nachfolger; der Kopf bleibt beim letzten vollständigen Glied. Der
bekannte Betriebsschaden der TUF-Referenzimplementierung — eine ungültige Version blockierte alle
folgenden dauerhaft — setzt eine lückenlos versionsnummerierte Kette voraus; diese Kette ist
autorverkettet und hat die Voraussetzung nicht.

**Das Ergebnis ist unter Wissenszuwachs nicht monoton (D154).** Trifft die Gegenzeichnung einer
früheren Rotation nach der einer späteren ein, springt der Kopf zurück. Das ist dieselbe Klasse
wie nachträglich entdeckte Equivocation und die sichere Richtung.

**Was als Kettenglied zählt (D155).** Rotate und Ack müssen `ACTIVE` sein; `EXPIRED` zählt bei
diesen beiden Prädikaten wie `ACTIVE`, weil eine ablaufende Rotation die Autorität zurückspringen
ließe — dieselbe Monotonie-Begründung, aus der `01 §5.3` das `t_exp` von `core/*` ignoriert. Sind
zwei vollständige Rotationen desselben Autors mangels Zwischenglied nicht vergleichbar, liefert
die Wurzel keinen Kopf. Die Ordnung folgt derselben Vorgängerrelation wie die Klassifikation
(`01 §6`): ein Glied zählt, wenn es bekannt, vom selben Autor und gehalten ist. Ein nachträglich
ungültiger Claim oder ein Vorgänger eines anderen Autors ist für die Ordnung ein fehlendes
Zwischenglied (D462). Trifft der Lauf einen bereits besuchten Schlüssel, ebenso: eine zyklische
Kette ist keine Nachfolge.

**Stand (D161, D163, D183, D462).** Schritt 1 ist seit `00b` gebaut, und ein vorgefundenes
`nucleus_keys` wird nach §5.4 ausgewertet. Die Verfassung der geltenden Epoche leitet
`resolve_state` aus der Epochenkette her (`04 §4.5`) und bildet daraus `authorized_keys`.
`membership` aus `03 §4` behält den Parameter (D183): wer ihn selbst füllt, trägt die Aktualität,
und eine veraltete Menge gibt ein veraltetes Ergebnis. Bis D462 stand hier, dass `nucleus_keys`
nicht ausgewertet werde; das war seit `00b` überholt.

**Jede Spaltung entwertet, nicht nur die an einer Rotation (D162).** Der Diebstahl zeigt sich
zuerst an gewöhnlichen Akten und erst spät an einer doppelten Rotation; eine Regel, die nur
Rotationen ansieht, deckt den auffälligen Angreifer und lässt den geduldigen durch. Der Preis ist,
dass ein Client, der einmal zwei Claims auf dieselbe Spitze schreibt, die Autorität seines Nukleus
kostet — mit demselben Ausweg §6.2, den auch der Diebstahl hat.

### 6.5 FROST-Re-Keying

In `key_mode = 1` ist der autorisierte „Schlüssel" ein **Gruppen**schlüssel. Mitgliederwechsel ⇒
neuer Gruppenschlüssel ⇒ derselbe `rotate-key@1`: der **alte** Gruppenschlüssel co-signiert (per
FROST) die Rotation auf den **neuen**. Scheitert die Schwellen-Signatur (zu viele Mitglieder weg),
greift der Notfallpfad §6.2. **`N` bleibt in allen Fällen fix** — das war die Kernanforderung, an
der Variante A (Pubkey = Scope) gescheitert wäre.

**Die Gegenzeichnung aus §6.1 gilt hier unverändert:** der **neue** Gruppenschlüssel zeichnet die
Rotation gegen. Ohne diesen Satz nähme `key_mode = 1` sich still von D125 aus, und die Bauform der
Rotation wäre in den zwei Modi verschieden.

---

## 7. Auswirkung auf `grant-membership` & Nukleus-Akte

**Geänderte Autorisierungsregel** (ersetzt „`I == N`"): Ein Nukleus-Akt (`grant-membership@1`,
`verdict@1` eines Panels, Ratifizierung, `rotate-key@1`) ist autorisiert gdw.:

```
akt.I ∈ resolve_current_key(akt.N)
```

- `∈` ist Mengenzugehörigkeit und für jede Mächtigkeit definiert. **`key_mode` unterscheidet die
  Signaturform, nicht die Zahl der autorisierten Schlüssel.** Für `key_mode = 0` ist das eine
  gewöhnliche Ed25519-Signatur, für `key_mode = 1` eine FROST-Gruppensignatur unter dem aktuellen
  Gruppenschlüssel; in beiden Fällen trägt der Akt **eine** Signatur.
- **Bei mehreren autorisierten Schlüsseln genügt einer (D166).** `root_keys` ist eine Liste — der
  Beispiel-Nukleus in `example-nucleus.md` hat zwei (D149) —, und jeder von ihnen darf allein
  handeln. Dasselbe gilt für `nucleus_keys` (§5.4) und für `arbitration.arbitrators` (§5.1): drei
  Autoritätslisten, dieselbe Regel. **Eine Schwelle trägt in v1 keine von ihnen.** Wer `k`-von-`n`
  will, hat zwei Wege, die es schon gibt: `key_mode = 1` mit FROST (§6.5) auf der Signaturebene,
  oder den Governance-Pfad gegen `thresholds` (`04 §3`). Ein dritter Weg wäre ein
  Verfassungsknopf nach §5 und kein Protokolldefault — und er wäre für alle drei Listen zugleich
  zu entscheiden, nicht für eine.
- `akt.N` MUSS gesetzt sein und zum aufgelösten Scope passen (Atom-Spec §2.2, Bindungsregel).
- **Die Föderationsstimme gehört nicht dazu (D235).** Sie ist der einzige Akt in einem fremden
  Scope: `akt.N` wäre nach der Bindungsregel `N_fed`, und `resolve_current_key(N_fed)` nennt die
  Schlüssel der Föderation, nicht die des stimmenden Kindes. Ihre Autorisierung läuft über
  `participants` der Föderationsverfassung (Gov-Spec §3.1), byte-weise und ohne Auflösung.

Das ist die konkrete Code-Konsequenz von DF-0: die heutige Prüfung `atom.I == scope` in
`parse_grant_membership` wird zu `atom.I ∈ resolve_current_key(scope)`.

---

## 8. Frozen-Primitive-Konformität (Nachweis)

Dieses Kapitel fügt **kein** Atom-Feld hinzu. Prüfung Punkt für Punkt:

- **Genesis & Verfassung** sind content-adressierte externe Objekte, referenziert per Hash
  (`accept-rules@1.J = [object-hash, …]`) — exakt das Muster aus Atom-Spec §7.2. Kein neues Feld.
- **`rotate-key@1`** ist ein Profil über bestehenden Feldern (`I`, `J=[identity,…]`, `N`, `v`).
  Es besteht den `core`-Aufnahmetest **nicht** (es macht eine Autoritäts-Aussage, keinen
  selbst-bezüglichen Lifecycle) und bleibt daher korrekt außerhalb von `core` — konsistent mit
  der Ablehnung von `vouch`/`verdict`/`membership` in Atom-Spec §5.
- **Governance-Rotation** ist ein gewöhnlicher `propose`/`vote`-Loop; die Auszählung ist bestehende
  Governance-Mechanik.
- **Equivocation umstrittener Rotation** nutzt `Atom.is_equivocation_pair` unverändert.
- **Verfassungs-Schema** lebt im *Objekt hinter dem Hash*, nicht im Atom; das Atom sieht weiterhin
  nur einen opaken 32-Byte-`object-hash`.

Ergebnis: Das Fundament wächst rein additiv über Profile und content-adressierte Objekte. Das
radiale Prinzip bleibt intakt.

---

## 9. Bewusst getragene Grenzen & Designentscheidungen

- **Genesis-Bootstrapping bleibt der wertbildende Akt (DR-026).** `N`, `root_keys` und `anchor_set`
  entstehen out-of-band. Die gesamte Sybil- und Autoritätssicherheit steht und fällt mit der
  Integrität dieser Gründungszeremonie — kein Protokollmechanismus kann eine vergiftete Gründung
  intern erkennen. Bewusst akzeptiert; eine Multi-Party-Seed-Zeremonie ist Policy, kein v1-Core.
- **Die Änderungsregel ist änderbar, aber nicht kaperbar** (`04 §3.4`). `genesis[5]` wählt die
  Klasse und bleibt fest; die Schwelle der Klasse steht in der Verfassung, und ihre Änderung trägt
  das Maximum aus alter und neuer Schwelle. Die Vorfassung — unveränderlich, wer ändern wolle,
  forke — ist mit `04 §3.4` entfallen (D470).
- **Governance-Rotation als Capture-Vektor.** Der Notfallpfad §6.2 könnte theoretisch von einer
  Mehrheit missbraucht werden, um einen legitimen Schlüsselhalter zu enteignen. Mitigation: hohe
  (`amendment`-)Schwelle + der Halter kann per Exit/Fork ausweichen (er behält seine *eigene*
  Identität, Profile-II §4). Residual bewusst getragen — es ist dieselbe irreduzible „Mehrheit kann
  irren"-Grenze wie in Enforcement-Spec §7.
- **Unaufgelöste Autorität unter Partition (§6.4 Schritt 3).** Solange eine umstrittene Rotation
  nicht per Governance aufgelöst ist, sind Nukleus-Akte ab dem Fork *nicht autorisiert* — die
  sichere Richtung (lieber kein gültiger Akt als ein falsch autorisierter), konsistent mit dem
  „Unter-Vertrauen"-Prinzip aus Trust-Flow-Spec §7.
- **Keine Schwelle auf Autoritätslisten (D166).** Ein einzelner kompromittierter Schlüssel aus
  `root_keys`, `nucleus_keys` oder `arbitration.arbitrators` kann allein handeln. TUF entscheidet
  an derselben Stelle anders — jede Rolle trägt `keys` **und** `threshold` —, und die Begründung
  dort ist genau der Diebstahlfall aus §6.3. Getragen, weil kein Nukleus die Frage stellt
  (`08 §2.2`) und weil FROST (§6.5) und der Governance-Pfad den absichtlichen Fall abdecken.
  Nicht getragen als erledigt: die Frage steht offen für alle drei Listen zugleich.
- **Schema-Minimalismus (DF-3).** Nur fünf Verfassungsfelder sind normativ; alles andere bleibt
  opak. Das ist ein *bewusster, begrenzter* Bruch der „Verfassung = reiner opaker Hash"-Linie — der
  minimal nötige, um P-1/E-1 maschinenlesbar zu schließen, ohne die Interpretationsschicht ins
  Protokoll zu ziehen.

---

## 10. Vermerke und ihre Subjekte

Die Auflösung der Schlüssel-Autorität wirft für schadhafte Eingaben keine Ausnahmen; sie legt
Vermerke ab und rechnet weiter. `NucleusFinding` ist ein eigener Enum und kein Reject-Code des
Atoms — diese Schicht weist keinen Claim zurück, sie sagt nur, unter welchem Vorbehalt ihre
Antwort steht. `findings` ist sortiert und dedupliziert.

**Was sortiert heisst (D429).** Aufsteigend nach `kind`, als ASCII-Zeichenfolge verglichen, dann
nach `subject` byteweise; gleiche Paare fallen zusammen. Die Ordnung gilt für die Vermerke aller
Schichten (`02 §10`, `03 §6`, `04 §3.5`). Sie trägt keine Bedeutung — sie macht zwei Antworten
über denselben Bestand byte-vergleichbar.

| Vermerk | Subjekt |
|---|---|
| `CONSTITUTION_UNAVAILABLE` | der übergebene `constitution_hash` (D164) |
| `MALFORMED_NUCLEUS_KEY` | der übergebene `constitution_hash` (D163) |

Beide Subjekte sind derselbe Wert, und das ist kein Versehen: das zurückgewiesene Objekt ist in
beiden Lagen die Verfassung. Einmal, weil sie lokal nicht vorliegt (§6.4, Schritt 1 c); einmal,
weil ein Eintrag ihres Feldes `nucleus_keys` formwidrig ist (§5.4). Ein formwidriger Eintrag hat
keine eigene Adresse, benannt wird deshalb gröber die Verfassung, die ihn führt — dieselbe Regel
wie in `04 §3.5`. Daraus folgt die Zusammenziehung aus D163: mehrere formwidrige Einträge ergeben
**einen** Vermerk, und die Anzahl ist keine Aussage dieser Schicht.

Das Subjekt ist nie ein Leerwert. Weder der berechnete Hash eines Objekts, das gar nicht
vorliegt, noch `b""` steht je darin.
