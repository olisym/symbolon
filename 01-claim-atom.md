# Claim-Atom — Spezifikation v1

Status: Entwurf · Protokollversion: 1 · Layer: Identity/Claim (Konvergenzpunkt des Stacks)

Das Claim-Atom ist das einzige Primitiv der oberen Schichten. Bürgschaft, Regelannahme,
Verdikt, Wert-Transfer und Mitgliedschaft sind keine eigenen Objekte, sondern *Profile* —
Nutzungskonventionen über genau diesem Atom. Ein Profil fügt **niemals** ein Feld hinzu.

---

## 1. Leitsätze (Geltungsrahmen)

- **A1 — Selbstenthalten & transport-agnostisch.** Ein Claim ist ein in sich geschlossenes
  Objekt aus Bytes. Es trägt alles, was zur Verifikation nötig ist, und reist über **beliebige**
  Medien (Funk-Mesh, QR, Papier, …). Transport steht **nie** im Atom; die Bindung an ein
  konkretes Transportnetz (z. B. Reticulum/LXMF) ist ein separates **Transport-Profil**, kein
  Kern-Bestandteil.
- **A2 (geschärft) — Lebenszyklus, nicht Bedeutung.** Das Protokoll versteht den *Lebenszyklus
  von Claims und Keys* (Gültigkeit, Ordnung, Verkettung, Widerruf der eigenen Claims).
  Es versteht **niemals** die *Bedeutung von Aussagen*. Alles Soziale ist Policy und bleibt
  in der Interpretationsschicht.
- **A3 — Erkennen statt verhindern.** Kein globaler Konsens. Jede Identity führt einen
  hash-verketteten, append-only Log. Manipulation ist evident; Forks (Equivocation) sind
  kryptografisch beweisbar, werden aber nicht verhindert.
- **Ein-Signierer.** Jedes Atom hat genau einen Signierer. Mehrparteiigkeit ist entweder
  Krypto (FROST/Threshold kollabiert eine Gruppe zu *einer* Identity unter einem
  Gruppenschlüssel) oder Komposition (mehrere Atome + Interpretationsregel) — nie ein Feld.
- **v1-Sparsamkeit.** Keine Key-Rotation im Core, keine Delegation im Core (siehe §8).

> **Selektive Stille (non-normativ, gehört zur Bedeutung — siehe VISION.md §4).** Das Atom
> ist ein *Mechanismus*, kein Gebot zu signieren. Der Default ist **Schweigen**: Ein Claim
> entsteht nur, wenn der Einsatz es rechtfertigt, nicht bei jeder Alltagshandlung. Das
> Protokoll kann Schweigen nicht erzwingen (das wäre Bedeutung), aber diese Spezifikation
> hält fest, dass „kein Claim" der Normalzustand ist — sonst liest sich die Schicht wie
> Totalüberwachung, die sie nicht ist. Verankerung der Norm: `VISION.md`; hier steht sie nur,
> weil der Leser dem Mechanismus zuerst hier begegnet.

---

## 2. Feldsatz

| CBOR-Key | Feld     | Typ / Größe              | Pflicht | Bedeutung |
|---------:|----------|--------------------------|:-------:|-----------|
| 0        | `version`| uint (= 1)               | ja      | Formatversion. |
| 1        | `I`      | bytes[32]                | ja      | Signierer-Identity = Ed25519-Verify-Key. |
| 2        | `J`      | array `[tag, value]`     | ja      | Subjekt, polymorph (§2.1). |
| 3        | `p`      | text                     | ja      | Prädikat-ID, namensraum-qualifiziert + versioniert (§2.2, Anhang A). |
| 4        | `v`      | bytes                    | nein    | Opaker, prädikat-definierter Wert. Protokoll parst ihn nie. |
| 5        | `N`      | bytes[32]                | nein    | Scope = 32-Byte-Nukleus-Scope-ID. Strukturell erstklassig (§2.3). |
| 6        | `t`      | uint (Unix-Sekunden)     | ja      | Vom Autor behaupteter Zeitstempel. **Kein** Ordnungsprimitiv; monoton entlang der Autorenkette (§6). |
| 7        | `t_exp`  | uint (Unix-Sekunden)     | nein    | Lokale strukturelle Gültigkeitsdecke. Danach ist der Claim void (§5.3, §6). |
| 8        | `h_prev` | bytes[32]                | ja      | Hash des vorherigen Claims desselben Autors; Genesis = `SHA-256(DOM_ID_GEN ‖ I)` (§4). |
| 9        | `σ`      | bytes[64]                | ja*     | Ed25519-Signatur über das Preimage (§4). |

\* `σ` (Key 9) ist im *signierten* Objekt Pflicht und im *Signatur-Preimage* abwesend.

Alle Referenzen sind einheitlich 32 Byte (Ed25519-Key **oder** SHA-256-Hash), die Signatur
64 Byte. Das hält die Wire-Form kompakt — wichtig für LoRa. **Keine Truncation, nirgends**
(Scope-Sicherheit §2.4, Invariante 1).

### 2.1 `J` — Subjekt (polymorph)

`J = [tag: uint, value: bytes[32]]`. Der Tag ist ein **geschlossener** Enum; er ist Mechanismus,
weil der Verifizierer wissen *muss*, worauf der Claim zeigt:

| Tag  | Name         | `value` ist … |
|-----:|--------------|---------------|
| 1    | `identity`   | Ed25519-Verify-Key der referenzierten Identity. |
| 2    | `claim-ref`  | `claim_id` (SHA-256) eines konkreten Claims (§4). |
| 3    | `object-hash`| SHA-256 eines externen Objekts (z. B. Regeldokument, Datei). |

Mehr Typisierung wäre bereits Semantik und bleibt draußen. Ein **unbekannter Tag** ist
strukturell ungültig → Reject (§6, Anhang B): Der Verifizierer kann nicht raten, worauf ein
Claim zeigt.

### 2.2 `p` — Prädikat

Format: `<namespace>/<name>@<version>`, z. B. `nuc:hasenpfote/vouch@1`. Die vollständige
formale Grammatik steht in **Anhang A**; dieser Abschnitt bleibt normativ maßgeblich.

**Scope-Isolation (normativ, v1):**

1. **Kanonische Kodierung (empfohlen, interoperabel):**
   `namespace = nuc:<scope_id_hex>`, wobei `scope_id_hex` **exakt 64 Kleinbuchstaben-Hexziffern**
   (= 32-Byte-Scope-ID) sind, z. B. `nuc:a1b2…ff/vouch@1`.
2. **Alias-Kodierung (nicht interoperabel ohne `N`):**
   Ein Alias aus `[a-z0-9_-]+` (Anhang A) ist erlaubt, aber der **autoritative Scope** eines
   Claims lebt dann ausschließlich im Feld `N`. Zwei Nuklei mit identischem `p`-String
   (`nuc:custom/vouch@1`) kollidieren **nicht**, solange `N` unterschiedlich ist und Verifizierer
   `N` bindend auswerten. Ein Alias **MUSS** das kanonische Muster `^[0-9a-f]{64}$` **nicht**
   matchen (§2.4, Invariante 3) — sonst wäre die Kodierungs-Erkennung mehrdeutig.
3. **Bindungsregel:** Für jedes `nuc:…`-Profil **MUSS** `N` gesetzt sein und **MUSS** dem
   aufgelösten Scope entsprechen. Bei kanonischer Kodierung **MUSS**
   `N == bytes.fromhex(scope_id_hex)` gelten; bei Alias-Kodierung ist `N` die einzige Scope-Quelle.
   Diese Prüfung ist reine **Byte-Gleichheit** — das Atom bleibt blind für die *Herkunft* von `N`
   (§2.3).
4. **Evaluator-Partitionierung:** Trust-Flow, Profile und Governance partitionieren
   Claim-Mengen nach dem **aufgelösten Scope** (`resolve_scope(N)`), nicht nach dem
   rohen `p`-String allein (§2.4, Invariante 2).

- **Genau zwei gültige Namensräume in v1:** das geschlossene **`core`** und das offene
  **`nuc:<scope>`** (Anhang A). Ein Prädikat, dessen Namensraum **weder** `core` **noch** `nuc:`
  ist, ist **strukturell ungültig → Reject** (`UNKNOWN_NAMESPACE`, Anhang B). Das hält die
  Scope-Autorität einzig an `N` (§2.4, Invariante 2) und verhindert einen wildwachsenden
  Namensraum-Zoo neben `N`. Ein Prädikat mit `nuc:`-Präfix, das die Grammatik aus Anhang A
  **nicht** erfüllt, ist ebenfalls strukturell ungültig → Reject (`INVALID_PREDICATE`, Anhang B).
  Der Prädikat-Name ist **bedeutungs**-opak, nicht **form**-frei.
- Namensraum **`core`** ist protokoll-reserviert und **geschlossen**: genau `core/revoke@1` und
  `core/supersede@1` (§5). Jedes andere `core/*` ist strukturell ungültig → Reject (§2.4,
  Invariante 4).
- **Innerhalb `nuc:<scope>` ist der Prädikat-*Name* opak/Policy.** Das Protokoll behandelt ihn
  als undurchsichtigen Identifier; seine Bedeutung lebt vollständig in der Interpretationsschicht.
  Neue Profile (`vouch`, `accept-rules`, `validation`, `timestamp`, …) sind genau das: neue
  **Namen** unter `nuc:`, **kein** neuer Namensraum — deshalb wächst die Grammatik nie mit.

### 2.3 `N` — Scope (Atom bleibt blind für die Herleitung)

Optionaler 32-Byte-Verweis auf die Scope-ID eines Nukleus. **Strukturell** erstklassig: Der
Verifizierer partitioniert die Trust-Flow-Berechnung pro `N` (Vertrauen ist kontextgebunden).
`N` abwesend = kontextfreier Claim (z. B. ein reiner Identity-Announce oder ein `core/*`-Claim).

**Das Atom kennt die *Herleitung* von `N` nicht.** Dass `N` der Hash eines unveränderlichen
Nukleus-Genesis-Objekts ist — `N = SHA-256(DOM_NUC_GEN ‖ cbor(genesis_obj))` —, ist eine
**Governance-/Fundament-Definition** (siehe `00-nucleus-genesis-constitution.md §3`) und lebt
bewusst *nicht* hier. Für das Atom ist `N` ein opaker 32-Byte-Bezeichner; seine einzige atom-lokale
Regel ist die Byte-Gleichheit aus §2.2 Regel 3. So bleibt die Scope-ID stabil über FROST-Re-Keying
und Schlüsselrotation hinweg (der Grund, warum sie ein Objekt-Hash und **kein** Pubkey ist), ohne
dass das bedeutungsblinde Atom davon etwas wissen muss.

### 2.4 Scope-Sicherheit (normativ — sechs Invarianten)

Die Autorität eines Scopes hängt **einzig** an `N` (32 Byte, 256-bit-kollisionssicher). Es gibt
keinen globalen Namensraum, also nichts zu squatten, und kurze/ratbare Alias-Strings tragen
**null** Sicherheitsgewicht. Der reale Angriffsvektor ist nicht Krypto, sondern *menschliche
Verwechslung*. Die folgenden Invarianten machen die Auflösung wasserdicht:

1. **Keine Truncation.** Alle Referenzen (`I`, `N`, `claim_id`, `h_prev`) sind volle 32 Byte.
   Schließt Birthday-/Truncation-Kollisionen aus (die Begründung aus §4 als globale Invariante).
2. **`N` ist die einzige Autorität.** Partitionierung und Auflösung laufen immer über
   `resolve_scope(N)`, nie über den rohen `p`-String. Ein Homoglyph- oder Doppel-Alias kann
   keinen Scope kapern.
3. **64-Hex reserviert.** Aliase **MÜSSEN** `^[0-9a-f]{64}$` **nicht** matchen; dieses Muster
   ist kanonischer Kodierung vorbehalten.
4. **`core` ist geschlossen.** Verifizierer **MÜSSEN** jedes `core/*` außer `{revoke@1,
   supersede@1}` ablehnen. Fremd-adressierte Revokes sind über `R.I == C.I` (§5.1) ohnehin
   ungültig.
5. **Kanonische Re-Serialisierung ist Pflicht** (§3, §6). Dadurch ist `claim_id` eine echte
   Inhaltsadresse; es gibt keine CBOR-Malleability und kein „Grinding" mehrerer IDs für
   denselben logischen Claim (das würde Dedup und Equivocation-Erkennung vergiften).
6. **Alias-Display SHOULD auflösen.** Für sicherheitstragende Anzeige oder Cross-Nukleus-Aktion
   zeigt/handelt die Implementierung auf dem aufgelösten `N`, nicht auf dem Alias-String.

---

## 3. Kanonische Serialisierung

Signiert und gehasht wird **immer** eine deterministische CBOR-Kodierung (RFC 8949,
Core Deterministic Encoding). Ohne Determinismus bricht die Verifikation — das ist
keine Designwahl, sondern Pflicht.

Regeln:

1. Top-Level ist eine CBOR-**Map** mit **uint-Keys** (kompakter als Text-Keys).
2. Definite-Length only. Keine indefinite-length Items.
3. Integer in kürzester Form.
4. Map-Einträge in **aufsteigender** Key-Reihenfolge.
5. Optionale Felder, die abwesend sind, **lassen ihren Key weg** (kein `null`).
   Anwesend ⟺ Key vorhanden.
6. Keine doppelten Keys. Keine Floats im Atom (`v` ist opake Bytes).

**Die Eingabe ist genau ein Item (normativ).** Die empfangenen Bytes sind die Kodierung **eines**
CBOR-Items und enthalten nichts darüber hinaus. Eine Folge mit Restbytes ist keine Kodierung eines
Claims — auch dann nicht, wenn die Restbytes selbst ein gültiger Claim sind — und wird abgelehnt
(`MALFORMED_CBOR`, Anhang B). Der Satz entscheidet mehr als einen Code: ohne ihn bliebe offen, ob
ein Verifizierer den angehängten zweiten Claim verarbeiten darf, und die Antwort „nicht-kanonisch"
verwirft ihn stillschweigend.

**Durchsetzung (normativ):** Ein Verifizierer, der Bytes empfängt, **MUSS** die dekodierte Map —
alle Felder einschließlich `σ` — neu kanonisch serialisieren und mit den empfangenen Bytes
**byte-genau** vergleichen. Bei Abweichung → Reject (`NON_CANONICAL_ENCODING`, Anhang B). Ohne
diesen Check ist die Kodierung mehrdeutig und `claim_id` faktisch vom Autor frei wählbar
(§2.4, Invariante 5).

> **Verglichen wird die Map, nicht der Core.** Der Core ist die Map ohne `σ` (§4) und kommt in den
> empfangenen Bytes nie für sich vor: er ist das signierte und das adressierte Objekt, nicht das
> Soll der Wire-Form. Ein Vergleich des Cores gegen die empfangenen Bytes wäre für jeden
> signierten Claim falsch. Die Kanonizität des Cores folgt aus der der Map, weil `σ` den höchsten
> Key trägt und sein Wegfall die Kodierung der übrigen Einträge unberührt lässt.

---

## 4. Domänen-Separation, Signatur, Claim-ID & Verkettung

**Core** = die deterministische CBOR-Map aller Felder **außer** `σ` (Keys 0–8). Das ist das
signierte *und* das adressierte Objekt; `σ` steht nie im Core.

**Domänen-Separatoren** (verhindern, dass eine Signatur oder ein Hash je über Protokoll- oder
Zweckgrenzen wiederverwendet werden kann):

```
DOM_SIG    = "claim-atom/v1/sig"
DOM_CID    = "claim-atom/v1/cid"
DOM_ID_GEN = "claim-atom/v1/id-genesis"
```

> `DOM_NUC_GEN = "claim-atom/v1/nucleus-genesis"` gehört **nicht** hierher — es ist der Separator
> für die Nukleus-Scope-ID und lebt in `00-nucleus-genesis-constitution.md §3` (§2.3). Das Atom
> definiert nur die drei obigen.

**Berechnung:**

```
bytes    = cbor_deterministic(core)
claim_id = SHA-256( DOM_CID ‖ bytes )                ; 32 B, Inhaltsadresse
σ        = Ed25519-Sign( sk_I, DOM_SIG ‖ bytes )     ; 64 B, im Claim, nie im Core
```

`claim_id` adressiert den **Inhalt** und ist **signatur-unabhängig** — es hasht nur den Core,
nicht `σ`. `σ` beweist getrennt die **Urheberschaft** der Bytes. Verifikation:
`Ed25519-Verify(I, DOM_SIG ‖ bytes, σ)`.

> **Offline-selbstenthalten (A1).** Weil `I` der volle 32-Byte-Ed25519-Verify-Key ist, trägt der
> Core sein eigenes Verifikationsmaterial — ein Claim ist ohne Nachschlagen prüfbar (Papier/QR).
> Preis ist Größe: 32 statt 16 Byte je Identity-Referenz. Die kompaktere Alternative (ein
> 16-Byte-Truncation-Hash + separat mitgeführter Pubkey) wurde bewusst verworfen: sie knüpft
> Offline-Prüfung an eine Nachschlage-Vorbedingung und öffnet einen 128-bit-Truncation-
> Kollisionsspielraum — bei einem sicherheitstragenden Identitätsverweis nicht akzeptabel
> (§2.4, Invariante 1).

**Verkettung.** `h_prev` ist die `claim_id` des unmittelbar vorhergehenden Claims *desselben
Autors*. Der erste Claim einer Identity (Genesis) setzt einen **identity-gebundenen Anker**:

```
h_prev_genesis = SHA-256( DOM_ID_GEN ‖ I )
```

Das bindet selbst den Genesis an die Identity — keine Cross-Identity-Verwechslung und kein über
alle Identities identischer Null-Anker. Jede Identity bildet damit genau **einen** linearen,
hash-verketteten Log.

> **`h_prev = 32×0x00` ist verboten (harter Reject).** Der Null-Vektor ist **kein** gültiger
> Genesis-Anker und **kein** gültiger Vorgänger. Ein Claim mit `h_prev = 32×0x00` wird abgelehnt
> (`INVALID_GENESIS_ANCHOR`, Anhang B), **nicht** als *pending* gehalten. Das sperrt naive
> Implementierungen aus, die einen Null-Genesis nachbauen. Negativer Vektor: **NV1** (Anhang C).

**Equivocation.** Existieren zwei strukturell gültige Claims `C1 ≠ C2` (verschiedene `claim_id`)
mit gleichem `(I, h_prev)`, dann hat der Autor seinen Log geforkt. Das ungeordnete Paar
`{C1, C2}` ist ein selbstenthaltener, kryptografischer Equivocation-Beweis gegen `I`. Beide
bleiben gespeichert; nichts wird gelöscht. Equivocation invalidiert strukturell gültige
Downstream-Claims **nicht** rückwirkend — sie **flaggt den Autor** (Zustand
`equivocation-flagged`, Anhang B). Die *Konsequenz* (z. B. Slashing) ist Sache der
ökonomischen/Policy-Schicht. Positiver Beweis-Vektor: **NV3** (Anhang C, teilt `(I, h_prev)`
mit TV1).

> **Warum das die Schlüssel-Diebstahl-Frage automatisch löst (DF-0).** Ein gestohlener Schlüssel,
> der zwei konkurrierende Nachfolger signiert (etwa zwei `rotate-key@1`, §8), erzeugt exakt diese
> Equivocation — ein selbst-validierender Beweis. Die Entscheidung, welcher Zweig gilt, fällt
> dadurch **zwangsläufig an die Mitglieder** (Governance-Akt), ohne dass der Core dafür ein
> Sonder-Primitiv braucht.

### 4.1 Die Ordnung der `claim_id` benennt, sie entscheidet nicht

Zwei verschiedene Claims haben verschiedene `claim_id`s, und 32-Byte-Zeichenketten sind total
geordnet. Diese Ordnung ist ein Nebenprodukt des Hashes: sie sagt nichts über Zeit, Rang, Nähe
zum Anker oder Autorität, und sie ist **mahlbar** — wer einen Schlüssel hält, erzeugt Claims,
bis seiner der kleinere ist.

**Benennen (erlaubt).** Muss eine Ableitung aus mehreren Claims, die eine Regel gleich erfüllen,
einen **benennen** — als `subject` eines Vermerks oder als Beleg in einem Ergebnis —, so ist es
der mit der kleinsten `claim_id`, ausgewählt **nach** der inhaltlichen Filterung. Zulässig ist
das genau dann, wenn die **Vertauschungsprobe** hält:

> Ersetzt man den benannten Claim durch einen beliebigen anderen aus derselben
> Kandidatenmenge, ist das Ergebnis der Ableitung **byte-gleich** — das benannte Feld
> ausgenommen.

Kein Kandidat wird dabei verworfen; alle bleiben gespeichert und lesbar (§1 A3). Die Benennung
ist eine **Anzeige** über einem mehrwertigen Zustand, nicht seine Auflösung. Genau deshalb ist
die Mahlbarkeit hier folgenlos: wer mahlt, gewinnt einen Namen und kein Ergebnis.

**Entscheiden (verboten).** Hält die Vertauschungsprobe nicht, so wählt die Ordnung aus, was
**gilt** — welcher Schlüssel autorisiert, welche Stimme zählt, welcher Zweig eines geforkten
Logs der echte ist. Eine **abgeleitete** Ordnung darf das nie: nicht der Hash, nicht die
Kodierungslänge, nicht die Ankunftszeit. Entscheiden darf allein eine **deklarierte** Ordnung —
die Verfassung (`00 §5.4`) oder ein Governance-Akt (`00 §6.2`). Gibt es keine, fällt die Aussage
weg; die Kandidaten bleiben gespeichert und werden gemeldet.

> **Die Probe ersetzt kein Urteil über Bedeutung und verlangt keines (§1 A2).** Ob mehrere
> `accept-rules` dasselbe sagen (`04 §3.1`, D101), ist die *Begründung* dafür, dass die
> Vertauschungsprobe dort hält — nicht die Prüfung selbst. Die Prüfung ist mechanisch: sie
> vergleicht Ergebnisbytes, nicht Aussagen.

---

## 5. Der gesegnete Kern: `core/revoke` & `core/supersede`

Diese zwei Prädikate sind die einzige Stelle, an der das Protokoll einem Prädikat eine
kanonische Bedeutung gibt. Das ist **kein** Bruch von A2, weil ihre *gesamte* Bedeutung
im Lebenszyklus der **eigenen** Claims des Autors aufgeht — exakt das, was A2 dem Protokoll
zuspricht.

**Geschlossenes Aufnahmekriterium für `core`:** Gesegnet wird ausschließlich eine Operation,
deren vollständige Bedeutung im selbst-bezüglichen Lebenszyklus aufgeht — strukturell prüfbar
ohne Weltwissen. Genau zwei Operationen bestehen diesen Test. `vouch`, `verdict`, `membership`
u. a. machen Aussagen mit *sozialem Wert* und fallen durch — sie können sich nicht in `core`
schmuggeln.

### 5.1 Selbst- vs. fremd-bezüglich

- **Selbst-bezüglich** (`R.I == C.I`, wobei `R.J = [claim-ref, C.claim_id]`): rein strukturell
  prüfbar (gleicher Schlüssel, gültige Kette). Das ist Lebenszyklus → **verstanden**.
- **Fremd-bezüglich** („Alice erklärt Bobs Claim für ungültig"): erfordert soziale Befugnis.
  Das ist in Wahrheit ein **Verdikt/Sanktion** → reine Policy, opak, **nicht** Core.

### 5.2 `core/revoke@1`

`J = [claim-ref, ziel.claim_id]`, `ziel.I == revoke.I`. Markiert den eigenen Ziel-Claim
in der Default-Sicht als **inaktiv**. Löscht oder versteckt nichts — sowohl der Claim als
auch sein Widerruf bleiben sichtbar (das ist selbst soziale Information und von A3 ohnehin
verlangt). Positiver Vektor: **TV3** (Anhang C).

### 5.3 `core/supersede@1`

`J = [claim-ref, ziel.claim_id]`, `ziel.I == supersede.I`. Ersetzt den eigenen Ziel-Claim;
der supersedierende Claim repräsentiert fortan die lebende Version. **Ordnung kommt aus der
Autorenkette (`h_prev`), nie aus Wall-Clock `t`** — über eine partitionierbare Mesh ist
`t` als globale Ordnung wertlos.

> **Lifecycle-Claims tragen kein `t_exp` (Monotonie, normativ).** `core/revoke@1` und
> `core/supersede@1` **SHOULD** kein `t_exp` setzen; ein Verifizierer **MUSS** ein `t_exp` auf
> einem `core/*`-Claim **ignorieren**. Grund: Ein ablaufender Widerruf würde in einer Partition
> das widerrufene Vertrauen *wiederbeleben* → **Über-Vertrauen**, exakt die eine gefährliche
> Richtung (Trust-Flow §7). Lifecycle ist **monoton**: einmal wirksam gesehen, permanent
> wirksam. Positiver Vektor: **TV5** (Anhang C) — ein `core/revoke@1` mit gesetztem `t_exp`,
> der jenseits von `t_exp` weiter `active` ist. Das Ignorieren schließt die Feld-Konsistenz aus
> §6 Punkt 7 ein: `t ≥ t_exp` ist auf einem `core/*`-Claim **kein** Reject.

### 5.4 Default-Sicht & Policy-Override

- **Weicher Default:** Claims sind durch ihre Autoren widerrufbar/supersedierbar.
- **Opt-out:** Eine Nukleus-Policy erklärt bestimmte Prädikate für *irrevocable*; Verifizierer
  unter dieser Policy ignorieren `revoke`/`supersede`, die auf solche Prädikate zielen.
  (Beispiel: `obligation@1`, damit ein Schuldner seine Schuld nicht per Selbst-Widerruf löscht
  — Profile-II §3.3.3.)

`revoke`/`supersede` sind selbst Claims in der Autorenkette — sie sind also geordnet und
gegen Equivocation geschützt wie alles andere.

#### 5.4.1 Woher die Policy kommt (normativ)

Der Verifizierer **wählt** die Policy nicht; sie wird aus dem Claim aufgelöst:

```
C.N  →  Genesis-Objekt  →  constitution_hash  →  Verfassungsobjekt
                                              →  irrevocable_predicates   (00 §5)
```

Jede Stufe ist content-adressiert und lokal nachrechenbar — kein Nachschlagen bei einer
Autorität, keine Netzwerkabhängigkeit. Ein Claim ohne `N` (also jeder `core/*`-Claim) fällt
unter keine Policy.

**Fehlt das Verfassungsobjekt lokal** (Partition, noch nicht synchronisiert), gilt der
Sicherheits-Default aus `00 §5.2`. Die Offline-Berechenbarkeit aus §6 bleibt damit erhalten:
die Zustandsmaschine braucht das Objekt nicht, um zu einem Ergebnis zu kommen — nur um ein
vollständigeres zu bekommen.

#### 5.4.2 Prädikat-Abgleich

`irrevocable_predicates` enthält **Profilnamen ohne Scope-Präfix** (`"obligation@1"`). Ein
Claim `C` fällt darunter gdw.:

```
C.p beginnt mit "nuc:"  und  der Teil nach dem letzten "/" ist in irrevocable_predicates
```

`core/*` kann **nie** irrevocable sein: `core/revoke@1` und `core/supersede@1` *sind* der
Lebenszyklus; ein Widerruf, der sich selbst gegen Widerruf immunisiert, ist keine Aussage,
sondern ein Fixpunkt. Ein Eintrag `"revoke@1"` oder `"supersede@1"` wird ignoriert.

#### 5.4.3 Zwei Grenzen der Irrevocability (normativ)

**(a) Irrevocability schlägt die Uhr nicht.** Ein irrevocabler Claim mit `t_exp` läuft ab wie
jeder andere. Der Opt-out schützt gegen den **nachträglichen Willen** des Autors, nicht gegen
den bei Ausstellung vorprogrammierten Verfall. Wer eine unbefristete Bindung will, stellt
keinen `t_exp` aus; wer eine befristete annimmt, sieht die Frist vor der Gegenleistung
(Profile-II §3.3.1).

**(b) Trust-gewährende Prädikate dürfen nicht irrevocable sein.** Irrevocable darf nur ein
Prädikat sein, dessen **Fortbestehen** die konservative Lesart ist.

| Prädikat | Fortbestehen bedeutet | konservativ? |
|---|---|---|
| `obligation@1` | die Schuld bleibt stehen | ja |
| `vouch@1` | das Vertrauen bleibt stehen | **nein** — Trust-Flow §7, die eine gefährliche Richtung |

> **Normativ:** Steht ein trust-gewährendes Prädikat in `irrevocable_predicates`, ist die
> Deklaration **unwirksam** — Widerrufe wirken weiterhin. Die Policy trägt den Vermerk
> `UNSAFE_IRREVOCABLE_PREDICATE`. In v1 ist `vouch@1` das einzige Prädikat dieser Klasse;
> die Liste wächst mit jedem künftigen Prädikat, das Kapazität, Gewicht oder Zugang verleiht.

Ohne (b) wäre ein Widerruf permanent und strukturell wirkungslos statt nur partitionsbedingt
verspätet — schlimmer als jeder Fall, gegen den `t_exp` gebaut wurde.

---

## 6. Verifizierer-Pflichten & Zustandsmodell

Ein Claim durchläuft eine **Zustandsmaschine**, deren *sämtliche intrinsischen Zustände ein
einzelnes Gerät offline aus den gehaltenen Bytes plus seiner lokalen Zeit berechnen kann* — ohne
Weltwissen, ohne einen externen Dienst. Diese Offline-Berechenbarkeit ist die tragende
Eigenschaft; sie *erzeugt* die Partitionstoleranz. Die vollständige Fehlerklassen- und
Übergangstabelle steht in **Anhang B**; hier die normative Kurzfassung.

**Strukturell gültig** gdw.:

1. `version` wird unterstützt;
2. die empfangenen Bytes sind **kanonisch** kodiert (§3: Re-Serialisierung byte-gleich, über die
   Map einschließlich `σ`), dekodierbar, ohne doppelte Keys, und tragen den Feldsatz aus §2:
   jedes Pflichtfeld vorhanden, kein Key außerhalb der Tabelle, Typen und Längen wie dort
   angegeben;
3. `J.tag` ist im geschlossenen Enum (§2.1);
4. `p` beginnt mit `core/` **oder** `nuc:` (sonst `UNKNOWN_NAMESPACE`, §2.2); bei
   `nuc:…`-Prädikat: die Form erfüllt die Grammatik aus Anhang A (sonst `INVALID_PREDICATE`) und
   die Bindungsregel §2.2 Regel 3 (sonst `BAD_SCOPE_BINDING`); bei `core/*` gilt jede der drei
   Bedingungen für sich: Prädikat ∈ `{revoke@1, supersede@1}` (sonst `RESERVED_CORE_PREDICATE`,
   §2.4 Invariante 4), `J.tag == claim-ref` (sonst `MALFORMED_CBOR`) und, **sofern der Ziel-Claim
   lokal bekannt ist**, `ziel.I == C.I` (sonst `FOREIGN_LIFECYCLE`);
5. `Ed25519-Verify(C.I, DOM_SIG ‖ bytes, C.σ)` ist wahr;
6. `h_prev ≠ 32×0x00` (§4); ist `h_prev == SHA-256(DOM_ID_GEN ‖ C.I)`, ist `C` ein
   **Genesis**-Claim;
7. falls `t` **und** `t_exp` vorhanden und `p` kein `core/*`: `t < t_exp` (reine
   Feld-Konsistenz — ein Claim, der behauptet, vor seiner eigenen Erstellung abzulaufen, ist
   inkohärent; **kein** Wall-Clock nötig). Auf `core/*` entfällt die Prüfung mit dem Feld (§5.3).

**Selbstenthaltene Gültigkeit (normativ).** Die Punkte 1 bis 7 sind bis auf einen Konjunkt aus den
empfangenen Bytes allein entscheidbar — ohne Uhr, ohne Speicher, ohne Netz. Der eine Konjunkt ist
`ziel.I == C.I` in Punkt 4, und er greift nur, sofern der Ziel-Claim lokal bekannt ist. Ein Claim
heißt **selbstenthalten gültig**, wenn die Punkte 1 bis 7 ohne diesen Konjunkt erfüllt sind. Der
Begriff verlangt nichts, er benennt: er ist der Prüfumfang eines Geräts ohne Speicher (A1) und
damit der Bezugspunkt für Fassungen, die nur diesen Teil bauen. Wissen kann das Urteil nur
**verengen** — ein selbstenthalten gültiger Claim kann strukturell ungültig werden, sobald sein
Ziel bekannt ist; der umgekehrte Weg existiert nicht. Zeitliche Gültigkeit, `pending` und `linked`
liegen außerhalb: sie brauchen Uhr beziehungsweise Speicher, und keines von beiden ist ein Reject
(Anhang B.3).

**Zeit — `now` ist bewusst lokal und subjektiv (normativ).** Die Gültigkeitsprüfung gegen `t_exp`
lautet: falls `t_exp` vorhanden, gilt `C` als *zeitlich gültig* gdw. `now ≤ t_exp`, wobei `now`
die **lokale Zeitquelle des Verifizierers** ist (eigene Uhr **oder** ein Zeitdienst, dem er
vertraut — siehe VISION.md §5). `t_exp` ist **keine Ordnungs-**, sondern eine **lokale
Gültigkeitsaussage**. Konsequenzen:

- **Zwei Verifizierer dürfen legitim uneins sein**, ob ein Claim abgelaufen ist. Das ist kein
  Bug. Die **sichere Richtung** ist stets **Unter-Vertrauen**: Im Zweifel den Claim *nicht* für
  trust-gewährende Zwecke heranziehen.
- **Offline-Fall (keine Zeitquelle).** Ist keine vertraute Zeitquelle verfügbar, ist die
  `t_exp`-Gültigkeit lokal **unentscheidbar** → der Claim wird für trust-gewährende Zwecke
  **nicht** herangezogen (Unter-Vertrauen). Nicht-zeitkritische Verarbeitung (z. B. Verkettung,
  Offline-Pooling, Vorberechnung, die online nur noch validiert werden muss) läuft davon
  unberührt weiter.

**Zeit — `t` ist monoton entlang der Autorenkette (normativ).** Bis hierher wird `t` nur
claim-intern geprüft (Punkt 7). Zusätzlich gilt für jeden Claim `C` mit **lokal bekanntem**
Vorgänger `P`, also `C.h_prev == P.claim_id`:

```
C.t >= P.t
```

Ist die Bedingung verletzt, ist `C` **time-regression-flagged** (Anhang B.1): gehalten,
gespeichert, nicht für trust-gewährende Zwecke heranzuziehen. **Kein Reject** — die Prüfung
braucht den Vorgänger und läge damit außerhalb der selbstenthaltenen Gültigkeit oben, die genau
einen vorgängerabhängigen Konjunkt kennt und ihn als die Ausnahme benennt. Das Vorbild ist
`equivocation-flagged`: speicherabhängig, Zustand statt Fehler.

Die Regel stiftet **keine** Ordnung aus `t`. Die Ordnung kommt weiterhin ausschließlich aus
`h_prev` (§5.3); `t` wird gegen sie geprüft. Insbesondere entsteht keine Rangfolge zwischen zwei
Autoren — verschiedene Autoren teilen keine Kette, und zwischen ihnen bleibt `t` wirkungslos.

Anders als `now` ist `t` signiert. Damit ist die Zeitbehauptung eines Autors gegen seine eigenen
früheren Behauptungen prüfbar, ohne dass ein Verifizierer eine Uhr, eine Zeitquelle oder
Erreichbarkeit braucht, und eine rückwärts laufende oder rückdatierte Uhr belastet ausschließlich
den Signierer. Das ist die Bauform aus `08 §2.2`: nicht verhindern, sondern unbestreitbar machen.

Drei Abgrenzungen:

- **Gilt auch für `core/*`.** Der Ausnahmegrund aus §5.3 ist die Monotonie des Lebenszyklus und
  trägt hier nicht; ein Widerruf mit rückwärts laufendem `t` ist derselbe Selbstwiderspruch wie
  jeder andere Claim.
- **Gleichstand ist erlaubt** (`>=`, nicht `>`). `t` ist sekundenaufgelöst, und zwei Claims
  desselben Autors in derselben Sekunde sind legitim. Strenge Monotonie bände die Claim-Rate an
  die Uhrenauflösung.
- **Ohne bekannten Vorgänger wird nicht geprüft.** Dann gilt `pending` (unten). Wissen verengt
  das Urteil, es kehrt es nicht um.

Stellung in der Zustandsmaschine: geprüft, **nachdem** der Vorgänger bekannt ist, und **bevor**
Widerruf und Supersede ausgewertet werden. Die Wirkung ist dieselbe — beide führen aus `active`
heraus —, die Diagnose ist besser: „der Autor widerspricht sich selbst" ist die stärkere Auskunft
als „der Claim wurde zurückgenommen". Dieselbe Erwägung trägt in `04 §3.1` die Reihenfolge der
Bedingungen 4 und 5.

**Aktiv** (Default-Sicht) gdw. strukturell gültig, zeitlich gültig, **verlinkt** (Vorgänger
bekannt & gültig) **und**:

- kein strukturell gültiger `core/revoke@1`-Claim `R` mit `R.I == C.I` und
  `R.J == [claim-ref, C.claim_id]` existiert, **und**
- `C` nicht durch einen strukturell gültigen `core/supersede@1`-Claim desselben Autors
  ersetzt ist.

**Unter einer Policy** (§5.4) entfallen beide Bedingungen für Claims, deren Prädikat irrevocable
ist: ein `revoke`/`supersede` auf ein solches Ziel wird bei der Zustandsbestimmung **ignoriert**.
Der Widerruf selbst bleibt gültig, gespeichert und sichtbar (§5.2) — er ist soziale Information
und wird nicht versteckt; er hat nur keine Wirkung auf den Zustand seines Ziels. Die zeitliche
Gültigkeit bleibt unberührt (§5.4.3 a).

**Pending statt Reject (kritische Klärung).** Ist `C` strukturell gültig, aber sein `h_prev`
referenziert einen **noch unbekannten** Vorgänger (Partial-Sync über Gossip), dann ist `C`
**pending** — es wird **gehalten**, nicht abgelehnt. Das folgt derselben „sichere Richtung"-Logik
wie Trust-Flow §7: Fehlende Vorgänger senken nur, was ich weiß; sie machen einen Claim nicht zu
Müll. Sobald der Vorgänger eintrifft, wird `C` **linked** und (falls nicht neutralisiert)
**active**.

**Idempotenz.** `claim_id` ist inhaltsadressiert; ein doppelt empfangener Claim (Gossip-Replay)
ist ein **idempotenter No-op**, kein Fehler.

Eine Nukleus-Policy MAY die Aktiv-Sicht überschreiben (§5.4). **Alles jenseits davon** —
was ein Vouch wert ist, ob Mitgliedschaft ratifiziert ist — ist Policy und liegt außerhalb
dieser Spezifikation.

> **Validierungs-Nodes sind orthogonal, kein Atom-Zustand.** Die Attestierung eines (gestakten)
> Validierungs-Nodes ist *externe Korroboration* = zusätzliche Claims = ein Profil höherer
> Schicht (ein **Confidence-Signal** für Policy/Trust-Flow). Sie **gatet** die intrinsische
> Zustandsleiter **nicht**. Die intrinsischen Zustände sind endlich (Anhang B); darüber gibt es
> unbegrenzt viele Confidence-Tiers via Attestierung. Sobald ein *intrinsischer* Zustand einen
> externen Dienst *bräuchte*, verlöre das Atom seine Offline-/Partitions-Eigenschaft — deshalb
> die strikte Trennung.

---

## 7. Profile (erste Ableitungen)

Ein Profil legt fest: welches `p`, welcher `J`-Typ, was in `v`, ob `N` Pflicht — plus die
Interpretation (Policy). Es fügt **kein Feld** hinzu. Das ist das radiale Prinzip konkret.

### 7.1 Bürgschaft — `nuc:<N>/vouch@1`

| Feld   | Belegung |
|--------|----------|
| `I`    | der Bürge |
| `J`    | `[identity, verbürgte_identity]` |
| `v`    | kanonische CBOR-Map mit `0: n`, `n : uint`, `1 ≤ n ≤ D` — das Vouch-Gewicht (Trust-Flow-Spec §3.1). **Abwesend ⇒ `n = D`, also `w = 1`.** Weitere Keys sind zulässig und für das Atom opak. |
| `N`    | **Pflicht** — Vertrauen ist kontextgebunden |
| `t_exp`| optional im Atom; in Scopes mit Budgetregel **Pflicht**, oder die Policy setzt eine Maximallaufzeit als Default (Trust-Flow-Spec §6.2) |

> `n` ist ein **uint**, kein Bruch. `w = n/D` mit scope-festem `D` (Trust-Flow-Spec §8) hält
> die gesamte harte Sicht ganzzahlig; ein `weight ∈ [0,1]` als Float verstieße gegen §3
> Regel 6. Geprüft wird **Key `0`**, nicht die Map als Ganzes. Reservierte Keys: `0` = `n`
> (normativ), `1` = Zweck-Tag (Trust-Flow-Spec §2), `2` = `bond_ref` (Trust-Flow-Spec §6.1).
> Referenzvektor TV1 trägt `v = h'a1001864'` = `{0: 100}` — bei `D = 100` der Default `w = 1`.

**Zu den Keys `1` und `2`.** Key `2` ist **typ-fest**: `2 : bstr`, Länge 32, nie dereferenziert.
Er trägt in v1 keine Wirkung und keinen Testvektor; festgelegt ist nur der Typ, damit die
Durchsetzungs- und die Profilschicht denselben Slot nicht verschieden belegen.

Key `1` bleibt **unkodiert**. Er ist Trust-Flow-Semantik, nicht Profil-Semantik: sobald ein
Zweck-Tag existiert, brauchen `trust()` und `rank()` einen `purpose`-Parameter, das Kantengewicht
muss über der **gefilterten** Teilmenge maximiert werden — sonst erbt ein Probe-Vouch für einen
Zweck das Gewicht eines vollen Vouch für einen anderen —, und das Budget muss über **alle**
Zwecke laufen, sonst kauft ein Autor durch Zweck-Splitting neues Budget. Das ist ein eigener
Durchgang und nicht der Nebeneffekt einer Kodierungszeile.

**Kanonizität von `v` prüft die lesende Schicht.** §3 verlangt kanonisches CBOR, aber der
Re-Serialisierungs-Check aus §6 Regel 2 deckt nur den **Core** ab; `v` ist darin eine `bstr`,
deren Inhalt uninterpretiert bleibt. Das Atom liest `v` nicht und wird es nicht tun — eine
Prüfung hier bräche die Bedeutungsblindheit. Durchgesetzt wird die Anforderung dort, wo `v`
gelesen wird: Trust-Flow-Spec §3.1 für Key `0`, Profile-II §1.3 für die Profil-Keys. Ein
Verstoß erzeugt dort einen Vermerk und lässt den defekten Teil wegfallen — **nie** einen Reject
und **nie** den Abwesend-Default.

- **Lebenszyklus:** Rücknahme via `core/revoke@1` (`J = [claim-ref, vouch.claim_id]`).
  Selbst-bezüglich → verstanden → in **jeder** Default-Sicht inaktiv. (Genau das schließt
  das Missbrauchs-Szenario: zieht Alice ihren Vouch für Bob zurück, verleiht er nirgends
  mehr Vertrauen — die Korrektheit hängt nicht an der Sorgfalt einzelner Implementierer.)
- **Interpretation (Policy, außerhalb Protokoll):** Kante im Trust-Graph; speist den
  personalisierten PageRank vom eigenen Seed; Bond & Slashing leben in der ökonomischen
  Schicht; eine inaktive (zurückgezogene) Kante trägt 0 Fluss bei.

Referenz-Vektor: **TV1** (Genesis-Vouch Alice → Bob, Anhang C).

### 7.2 Regelannahme — `nuc:<N>/accept-rules@1`

| Feld | Belegung |
|------|----------|
| `I`  | das Mitglied |
| `J`  | `[object-hash, H(Verfassungsobjekt vR)]` |
| `v`  | optional (z. B. Versionskennung), opak |
| `N`  | **Pflicht** — der Nukleus, den die Verfassung regiert |

- **Lebenszyklus:** Verfassungsupdate ⇒ neues Objekt ⇒ neuer Hash. Das Mitglied stellt
  `accept-rules@1` für den neuen Hash aus **und** supersediert (`core/supersede@1`,
  `J = [claim-ref, alte_annahme.claim_id]`) die vorige Annahme. Ordnung via eigene Kette,
  nie Wall-Clock.
- **Kollektive Ratifizierung — zwei Wege, beide außerhalb des Atoms:**
  1. *Komposition:* N Einzel-Annahmen + Interpretationsregel „ab t-of-n gilt ratifiziert".
  2. *FROST:* der Nukleus-Gruppenschlüssel co-signiert **eine** Ratifizierungs-Annahme.
- **Interpretation (Policy):** Mitgliedschaft / Konsens-Stufe 1.

Referenz-Vektoren: **TV2** (Alice, verkettet auf TV1) und **TV4** (Bob, Genesis; Anhang C).

---

## 8. Bewusst getragene v1-Grenzen

- **Ein-Schreiber-Annahme.** Eine Identity = ein logischer Schreiber = eine Kette. Mehrere
  Geräte mit demselben Schlüssel forken die eigene Kette ⇒ Selbst-Equivocation. Multi-Device
  erfordert daher eines von: (a) alle Signaturen über *ein* Gerät routen, (b) jedes Gerät als
  *eigene* Identity, oder (c) FROST über die Geräte. Reale operative Einschränkung, kein Bug —
  der Preis für triviale Tamper-Evidence ohne Konsens. Sauberer Fix später via Delegation
  (Sub-Keys), bewusst vertagt.
- **Key-Rotation: nicht im Core, aber ausdrückbar (DF-0).** Der Core kennt keine Rotation. Der
  **Normalfall** ist ein verkettetes `rotate-key@1`-**Profil** (Interpretationsschicht, **kein**
  `core`): Der alte Schlüssel signiert als letzten Akt seiner Kette einen Verweis auf den neuen.
  **Verlust/Diebstahl** löst ein **Governance-Akt** (`00 §6.2`). Ein gestohlener Schlüssel, der zwei
  Nachfolger signiert, erzeugt automatisch eine **Equivocation** (§4) — die Wahl des gültigen Zweigs
  fällt damit zwangsläufig an die Mitglieder. Kein neues Atom-Feld nötig.
- **Keine Delegation im Core.** „Schlüssel A signiert für Identity B" schmuggelt Scope-Semantik
  ein; bleibt in der Interpretationsschicht, bis sich zeigt, dass Verifikation ohne sie nicht geht.
- **Oracle-Problem & physische Durchsetzung** liegen außerhalb des Atoms. Das Protokoll
  garantiert *Non-Repudiation* und *Record-Integrität* — nie die *Wahrheit* einer Behauptung
  und nie die *Durchsetzung* eines Verdikts.
- **Seed-Set.** Die gesamte Sybil-Resistenz steht und fällt mit der Integrität des initialen,
  out-of-band etablierten Ankersets. Das ist die wertbildende Entscheidung des Systems,
  kein technisches Detail.

---

## 9. Versionierung

`version` (Key 0) sitzt im Core und damit unter `σ`. Eine **inkompatible** Änderung erhöht
`version` **und** die Domänen-Separatoren (`claim-atom/v2/sig` usw.) — dadurch kollidiert eine
Signatur oder ein `claim_id` **nie** über Versionsgrenzen, selbst bei sonst gleichen Bytes.

Neue **Prädikate** brauchen dagegen **keinen** Version-Bump — sie sind Profile (§7) und ändern
weder Core noch Serialisierung, Signatur oder Validität. Genau das ist die radiale Einheit:
das Format wächst nicht, nur die Menge der Konventionen darüber.

---

## Anhang A — Prädikat-Grammatik (normativ)

Ergänzt §2.2; bei Konflikt gilt §2.2. ABNF (RFC 5234), gefolgt von äquivalenten Regexen.

```abnf
predicate    = namespace "/" name "@" version
namespace    = core-ns / nuc-ns
core-ns      = "core"
nuc-ns       = "nuc:" scope
scope        = canonical-scope / alias-scope
canonical-scope = 64HEXLOW            ; exakt 64 Kleinbuchstaben-Hex = 32-Byte-Scope-ID
alias-scope  = 1*aliaschar            ; MUSS NICHT canonical-scope matchen (§2.4, Inv. 3)
name         = 1*namechar
version      = nonzero *DIGIT         ; keine führende Null (kürzeste Form, §3)

HEXLOW       = DIGIT / %x61-66        ; 0-9 a-f
aliaschar    = %x61-7A / DIGIT / "-" / "_"   ; a-z 0-9 - _
namechar     = %x61-7A / DIGIT / "-" / "_"   ; a-z 0-9 - _
nonzero      = %x31-39                ; 1-9
```

Äquivalente Regexe (implementierungsfreundlich):

```
canonical scope : ^[0-9a-f]{64}$
alias scope     : ^(?![0-9a-f]{64}$)[a-z0-9_-]+$      ; negativer Lookahead sperrt 64-Hex
name            : ^[a-z0-9_-]+$
version         : ^[1-9][0-9]*$
core predicate  : ^core/(revoke|supersede)@[1-9][0-9]*$   ; v1: nur @1 aktiv (§2.2)
nuc predicate   : ^nuc:(?:[0-9a-f]{64}|(?![0-9a-f]{64}/)[a-z0-9_-]+)/[a-z0-9_-]+@[1-9][0-9]*$
```

Bindung an `N`: siehe §2.2 Regel 3 und §2.4 Invarianten 2–3. Die Grammatik prüft **Form**;
die **Autorität** prüft immer `N`.

Ein `nuc:`-Prädikat, das diese Grammatik verletzt, ist `INVALID_PREDICATE` (Anhang B.2). Ein
String ohne `core/`- und ohne `nuc:`-Präfix ist `UNKNOWN_NAMESPACE`; ein `core/*` außerhalb der
beiden gesegneten Prädikate ist `RESERVED_CORE_PREDICATE`.

---

## Anhang B — Verifizierer-Verhalten & Zustandsmaschine (normativ)

### B.1 Intrinsische Zustände (endlich, offline berechenbar)

Alle Zustände sind aus den gehaltenen Bytes + lokaler Zeit ohne Weltwissen bestimmbar.

| Zustand | Bedingung | Verhalten |
|---------|-----------|-----------|
| `malformed` | Signatur/CBOR/Kanonizität/`J`-Tag/Bindungsregel verletzt (§6.1–4) | **Reject**, nicht speichern |
| `pending` | strukturell gültig, aber `h_prev`-Vorgänger unbekannt (Partial-Sync) | **halten**, auf Vorgänger warten |
| `linked` | Vorgänger bekannt & gültig, Kette konsistent | weiter zu active/neutralisiert |
| `active` | linked, zeitlich gültig, nicht revoked/superseded | **Default-Sicht** |
| `revoked` | linked, gültiger selbst-bezüglicher `core/revoke@1` existiert **und** `C.p` ist nicht irrevocable unter der Policy (§5.4) | gültig, **inaktiv** |
| `superseded` | linked, durch eigenen `core/supersede@1` ersetzt **und** `C.p` ist nicht irrevocable unter der Policy (§5.4) | gültig, **inaktiv** |
| `expired` | linked, `t_exp` vorhanden und `now > t_exp` (lokal!) | lokal **inaktiv**; andernorts evtl. active |
| `equivocation-flagged` | zweiter gültiger Claim mit gleichem `(I, h_prev)`, andere `claim_id` | **beide speichern**, Autor flaggen; Downstream nicht rückwirkend invalide |
| `time-regression-flagged` | linked, Vorgänger `P` bekannt und `C.t < P.t` (§6) | **speichern**, Claim flaggen; `P` und Downstream unberührt |

**`malformed` ist kein Klassifikationsergebnis** (D278). Die übrigen acht Zeilen beschreiben
einen gehaltenen Claim; `malformed` beschreibt die Verweigerung, ihn zu halten. Eine Fassung, die
die Klassifikation als Aufzählung führt, führt darin acht Werte und nicht neun — der neunte kann
nie entstehen, weil der Claim, der ihn trüge, nicht gespeichert wird. Woran es lag, sagen die
Reject-Codes aus `§6`, nicht ein Zustand.

`expired` ist der einzige Zustand mit legitim **verifizierer-relativer** Belegung (§6, `now`
lokal). Alle anderen sind über Verifizierer hinweg deterministisch gegeben denselben Bytes
**und derselben Policy**. Zwei Verifizierer mit verschiedenen Verfassungsobjekten für dasselbe
`N` sind kein legitimer Zustand, sondern ein Synchronisationsdefekt: `N` ist der Hash des
Genesis, und der Genesis fixiert `constitution_hash`. Wer eine andere Verfassung hält, hält
eine andere Version — und die Ratifizierung, die sie gültig macht, ist selbst prüfbar
(`00 §5.3`).

### B.2 Fehlerklassen (Reject-Gründe)

| Code | Auslöser |
|------|----------|
| `UNSUPPORTED_VERSION` | `version` nicht unterstützt |
| `NON_CANONICAL_ENCODING` | Re-Serialisierung ≠ empfangene Bytes (§3); dazu zählt dekodierbare indefinite-length (BV3) |
| `MALFORMED_CBOR` | nicht dekodierbar (auch: unabgeschlossene indefinite-length, Break in Wertposition, Restbytes hinter dem Item) / doppelte Keys / Nicht-uint-Schlüssel / falscher Feldtyp, fehlendes Pflichtfeld, Key außerhalb der Feldtabelle oder falsche Byte- bzw. Array-Länge (§2) / `J.tag ≠ claim-ref` bei `core/*` (§6 Punkt 4) |
| `UNKNOWN_J_TAG` | `J.tag` ∉ `{1,2,3}` (§2.1) |
| `UNKNOWN_NAMESPACE` | `p` beginnt weder mit `core/` noch mit `nuc:` (§2.2) |
| `INVALID_PREDICATE` | `p` beginnt mit `nuc:`, erfüllt aber die Grammatik aus Anhang A nicht |
| `BAD_SCOPE_BINDING` | `nuc:…` ohne `N`, oder `N ≠ bytes.fromhex(scope)` bei kanonischer Kodierung (§2.2 R3) |
| `RESERVED_CORE_PREDICATE` | `core/*` ∉ `{revoke@1, supersede@1}` (§2.4 Inv. 4) |
| `FOREIGN_LIFECYCLE` | `core/revoke`/`supersede` mit `ziel.I ≠ C.I` bei lokal bekanntem Ziel-Claim (§5.1) |
| `BAD_SIGNATURE` | Ed25519-Verifikation schlägt fehl |
| `INVALID_GENESIS_ANCHOR` | `h_prev == 32×0x00` (§4) |
| `INCOHERENT_EXPIRY` | `t` und `t_exp` vorhanden und `t ≥ t_exp`; nicht auf `core/*` (§5.3) |

**Vorrang bei mehreren Mängeln (normativ).** Trägt eine Bytefolge mehrere Mängel, entscheidet
nicht die Prüfreihenfolge, sondern der Inhalt der Aussage. `NON_CANONICAL_ENCODING` behauptet, es
gebe eine kanonische Kodierung desselben Inhalts, die gültig wäre. Trägt der dekodierte Inhalt
einen Mangel, den keine Kodierung behebt, ist der Code `MALFORMED_CBOR` — gleichgültig, an welchem
Schritt eine Implementierung ihn findet (BV2). Solche Mängel sind: die oberste Ebene ist keine Map
(§3 Regel 1, C.15), ein Schlüssel ist kein uint, ein Key kommt doppelt vor, ein Pflichtfeld fehlt,
ein Key steht außerhalb der Feldtabelle, ein Feld trägt den falschen Typ oder die falsche Länge
(§2). Die Aufzählung ist abschließend: was nicht in ihr steht, hebt `NON_CANONICAL_ENCODING` nicht
auf. Eine Prüfreihenfolge wird damit nicht normiert; die Aufzählungen in §6 sind Konjunktionen,
keine Folgen.

**Der Code ist ein Grund, kein Zustand (normativ).** B.1 kennt genau einen Reject-Zustand,
`malformed`. Die Codes dieser Tabelle benennen, woran er hängt; über den Zustand entscheiden sie
nicht. Deshalb wird **keine Gesamtordnung** der Klassen normiert: tragen mehrere Codes eine wahre
Aussage über dieselbe Bytefolge, ist die Wahl der Implementierung überlassen. Verboten ist allein
der falsche Satz — ein Code, dessen Aussage die Bytefolge nicht trägt. Die Vektoren in Anhang C
binden die Wahl nur, soweit sie sie stellen: C.10 trägt acht Claims mit je genau einem Mangel,
und der einzige Vektor mit zwei Mängeln ist BV2, den der Vorrang entscheidet und keine
Reihenfolge.

**Die Feldtabelle gilt je Version (normativ).** Der Feldsatz aus §2 ist der von `version` 1. Wird
eine Version nicht unterstützt, ist der Code `UNSUPPORTED_VERSION`; Pflichtfelder, Keys und Längen
werden dann nicht mehr gegen §2 geprüft. Eine fremde Version darf einen anderen Feldsatz tragen,
und `MALFORMED_CBOR` behauptete dort einen Mangel, den erst die v1-Tabelle setzt. Das gilt ebenso
für jeden Code, dessen Aussage eine Feldbedeutung aus §2 voraussetzt: unter einer nicht
unterstützten Version trägt die Bytefolge ihn nicht, weil erst die v1-Tabelle den Feldern ihre
Bedeutung gibt. Strukturelle Mängel bleiben unberührt, weil sie an keiner Version hängen (D308).
Die Ausnahme setzt voraus, dass `version` als uint lesbar ist; fehlt das Feld oder trägt es einen
anderen Typ, liegt keine fremde Version vor, sondern ein Mangel der v1-Tabelle.

### B.3 Nicht-Fehler (bewusst kein Reject)

- **Gossip-Replay**: identische `claim_id` erneut empfangen → **idempotenter No-op**.
- **Unbekannter Vorgänger**: → `pending` (nicht Reject), siehe B.1.
- **`t_exp` auf `core/*`**: → **ignorieren** (Monotonie §5.3), Claim ansonsten normal behandeln;
  auch `t ≥ t_exp` löst dort keinen Reject aus (§6 Punkt 7).
- **Lokaler Ablauf abweichend von anderen Verifizierern**: legitim, kein Fehler (§6, `now`).

---

## Anhang C — Test-Vektoren (real gerechnet, schema-valide, geteilt mit `00`)

Alle Werte sind **reproduzierbar** aus festen Ed25519-Seeds und kanonischem CBOR (RFC 8949,
`cbor2 canonical=True`). Hex durchgängig lowercase. Signaturen gegen `DOM_SIG ‖ bytes`
verifiziert; `claim_id = SHA-256(DOM_CID ‖ bytes)`. Das Beispiel-Nukleus (`N`, Genesis,
Verfassung) ist **schema-valide zu `00 §4/§5`** und **identisch** mit dem Worked-Example in
`00-nucleus-genesis-constitution.md §3.1` — die gesamte Spec-Reihe teilt damit *einen* Anker.

Davon ausgenommen ist die Gruppe der **Byte-Vektoren `BV1`–`BV3` (C.8)**: rohe Bytefolgen ohne
Schlüsselmaterial, die kein gültiger Claim sein können. Sie sind nicht schema-valide und nicht
aus Seeds gerechnet — sie legen fest, **welchen Code** eine Implementierung liefern muss, nicht
über welchen Schritt sie dorthin gelangt.

### C.0 Gemeinsame Parameter

```
DOM_SIG    = "claim-atom/v1/sig"
DOM_CID    = "claim-atom/v1/cid"
DOM_ID_GEN = "claim-atom/v1/id-genesis"
DOM_NUC_GEN= "claim-atom/v1/nucleus-genesis"        ; Nukleus-Scope-Separator (Def. 00 §3)

alice_seed = 01×32   ; Ed25519-Privatkey-Seed (32 Byte 0x01)
bob_seed   = 02×32

ALICE (I)  = 8a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c
BOB   (I)  = 8139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df60f5b8fc9b394

; Beispiel-Nukleus — schema-valide, siehe 00 §3.1 (dort mit Objekt-Feldern ausgeschrieben)
constitution_hash (CONST) = 890b21e7cd43fc4226938ce0b6eae1d00efa04ef9e6585c352dcf19ccad5ea7e
N                         = 65309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557

h_prev_genesis(ALICE) = SHA-256(DOM_ID_GEN ‖ ALICE)
                      = 62db0b05f44c17e2dfe7f371d631845fdd5858dd94c37d327a28f73b25625430
h_prev_genesis(BOB)   = SHA-256(DOM_ID_GEN ‖ BOB)
                      = d507038f3b07c8642b65e9b3cf559204d9ad7aa0a3faee674d4284a5d9e43abe
```

### C.1 TV1 — Genesis-Vouch (Alice → Bob), `v` und `t_exp` gesetzt

```
core = { 0:1, 1:ALICE, 2:[1, BOB], 3:"nuc:6530…5557/vouch@1",
         4:h'a1001864', 5:N, 6:1700000000, 7:1735689600, 8:h_prev_genesis(ALICE) }

bytes    = a900010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f5557061a6553f100071a6774858008582062db0b05f44c17e2dfe7f371d631
           845fdd5858dd94c37d327a28f73b25625430
claim_id = f95d430e40df736cbdffd7bf82af4f77e0c7af8692565f3b2a151c2c1ae8660c
σ        = ef3b6674898a1f037bdb58dc485926b4f0de01ef995d6cbf7d6387c4dd33679f
           63da403f2f2d1c4bb39513484dee2c74387ec904bbab0aa22b8bdb376fb1c401
```

### C.2 TV2 — accept-rules (Alice), verkettet auf TV1, kein `v`, kein `t_exp`

```
core = { 0:1, 1:ALICE, 2:[3, CONST], 3:"nuc:6530…5557/accept-rules@1",
         5:N, 6:1700000100, 8:TV1.claim_id }

bytes    = a700010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c0282035820890b21e7cd43fc4226938ce0b6eae1d00efa04ef9e
           6585c352dcf19ccad5ea7e0378536e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f6163636570742d72756c657340
           3105582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c
           7d2f5557061a6553f164085820f95d430e40df736cbdffd7bf82af4f77e0c7af
           8692565f3b2a151c2c1ae8660c
claim_id = 29b66881810bbbf1e254e061c35395e15da6c064327c2d33dfa6aa29d47dc2a6
σ        = 33220d6b1b744a76181311d9e724f5e43ab55608037bef5835f14c061d3fe0fd
           d13b8a54f94a118f698c591a85b06b29bd6dbdbdbdcd63ad3fcf6c278d851207
```

### C.3 TV3 — `core/revoke@1` (Alice widerruft TV1), kein `N`, kein `t_exp` (monoton)

```
core = { 0:1, 1:ALICE, 2:[2, TV1.claim_id], 3:"core/revoke@1",
         6:1700000200, 8:TV2.claim_id }

bytes    = a600010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c0282025820f95d430e40df736cbdffd7bf82af4f77e0c7af8692
           565f3b2a151c2c1ae8660c036d636f72652f7265766f6b654031061a6553f1c8
           08582029b66881810bbbf1e254e061c35395e15da6c064327c2d33dfa6aa29d4
           7dc2a6
claim_id = 8e76a2a9ee6677e6959bf9868dc6d162e5ff7e464a6bb4c6b839f89713e54629
σ        = 88388a4ad5f22d618dafef8a3bd877cd33f0e8899efdab3808cbd194adefb04f
           10123a0b34b3ab29a4f127b419ddde98e86c19417a2538bd31de22ba37df6006
```

Wirkung: TV1 wird in jeder Default-Sicht `revoked` (inaktiv), bleibt aber gespeichert (§5.2).

### C.4 TV4 — accept-rules (Bob, Genesis; zweiter Autor)

```
core = { 0:1, 1:BOB, 2:[3, CONST], 3:"nuc:6530…5557/accept-rules@1",
         5:N, 6:1700000050, 8:h_prev_genesis(BOB) }

bytes    = a700010158208139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df6
           0f5b8fc9b3940282035820890b21e7cd43fc4226938ce0b6eae1d00efa04ef9e
           6585c352dcf19ccad5ea7e0378536e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f6163636570742d72756c657340
           3105582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c
           7d2f5557061a6553f132085820d507038f3b07c8642b65e9b3cf559204d9ad7a
           a0a3faee674d4284a5d9e43abe
claim_id = 0bd77591da5e480a8c9a573382d14407a1770e0a7f6d2d09776b630fbd7ca01c
σ        = 87ac5f22c62b87a105eb6b18dd80e0ca014cdfd6c602128be2dd917f35265cbf
           0933001dc891120b9a02a807e5608e29eb622e49252bcc933caf2c9f31f44c05
```

### C.5 NV1 — negativ: `h_prev = 32×0x00` → `INVALID_GENESIS_ANCHOR`

Signatur ist **gültig**; der Claim wird **allein wegen `h_prev`** abgelehnt (§4). Er wird
**nicht** als `pending` gehalten.

```
core = { 0:1, 1:ALICE, 2:[1, BOB], 3:"nuc:6530…5557/vouch@1",
         5:N, 6:1700000300, 8:00…00 (32×0x00) }

bytes    = a700010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f756368403105582065309f
           e233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557061a65
           53f22c0858200000000000000000000000000000000000000000000000000000
           000000000000
claim_id = 9b25020fee7da6832416f8bcb61e4a05329776d051a4da282db7e973eb96c453
σ        = 08fb042eae35833c6412cbcc18d73aeb2c9f45fb82a7e24a73351164fc1c0a3e
           c1dc13fb6288cb827d6c10d62afe2d8c17dc945867b14401bf2e99d8684cde07
erwartet = Reject: INVALID_GENESIS_ANCHOR
```

### C.6 NV3 — negativ: Equivocation gegen TV1 (gleiches `(I, h_prev)`)

Alice signiert einen **zweiten** Genesis-Claim auf demselben `h_prev` wie TV1 (nur `t`
differiert) → andere `claim_id`. Das Paar `{TV1, NV3}` **ist** der Equivocation-Beweis (§4).

```
core = { 0:1, 1:ALICE, 2:[1, BOB], 3:"nuc:6530…5557/vouch@1",
         5:N, 6:1700000001, 8:h_prev_genesis(ALICE) }   ; selbes h_prev wie TV1

claim_id = e14ebd82eb172672a4a3ccbc330fef64fecd86e4664f72eab538855c9cef5c8b
σ        = 959245d77a82c6099905ff781e61c917e7a1de4687a4bb8e84504b5191060ef9
           a81203a06e71a51144a66e886db3f62ba9fcd19171adb3f25b2288c4ef9fa403
erwartet = beide Claims speichern; Autor ALICE als equivocation-flagged markieren;
           Konsequenz (Slash) = ökonomische/Policy-Schicht (05)
```

### C.7 NV2 — negativ: nicht-kanonisch kodierte TV1-Map → `NON_CANONICAL_ENCODING`

Dieselbe signierte Map wie TV1, einschließlich `σ`, aber mit **unsortierten Map-Keys** kodiert.
Der Verifizierer dekodiert, re-serialisiert kanonisch und vergleicht — Mismatch → Reject. Der
Vektor trägt genau diesen einen Mangel: die kanonische Kodierung desselben Inhalts ist TV1 und
wäre gültig, und nur deshalb ist `NON_CANONICAL_ENCODING` über ihn eine wahre Aussage (B.2,
Vorrang).

```
nicht-kanonisch (Key-Reihenfolge 8,6,5,3,2,1,0,7,4,9):
           aa08582062db0b05f44c17e2dfe7f371d631845fdd5858dd94c37d327a28f73b
           25625430061a6553f10005582065309fe233da30fda061d7c5ef002b6b80e426
           82cd54d703ab13fb6c7d2f555703784c6e75633a363533303966653233336461
           3330666461303631643763356566303032623662383065343236383263643534
           64373033616231336662366337643266353535372f766f756368403102820158
           208139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df60f5b8fc9b3
           940158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801
           b40f6f5c0001071a677485800444a1001864095840ef3b6674898a1f037bdb58
           dc485926b4f0de01ef995d6cbf7d6387c4dd33679f63da403f2f2d1c4bb39513
           484dee2c74387ec904bbab0aa22b8bdb376fb1c401

received == canonical            : false     → Reject
reserialize(received) == canonical: true     → dieselbe Map, nur nicht-kanonisch kodiert
erwartet = Reject: NON_CANONICAL_ENCODING
```

### C.8 BV1–BV3 — Byte-Vektoren (kein Schlüsselmaterial, keine Claims)

Die drei Bytefolgen sind kein gültiger Claim und können keiner werden. Sie prüfen den
**Fehlerkanal** des Verifizierers: welchen Code er liefert, unabhängig davon, an welchem Schritt
seiner Prüfreihenfolge er ihn findet. Eine Implementierung mit anderer CBOR-Bibliothek erreicht
denselben Reject möglicherweise früher oder später — der Code muss derselbe sein.

#### BV1 — Break-Sentinel in Wertposition → `MALFORMED_CBOR`

```
           a100ff

; Map {0: <break>}. Dekodiert; die Schlüsselprüfung (uint) passiert der Vektor,
; weil das Sentinel im Wert steht. Die Re-Serialisierung kann den Wert nicht
; kodieren und wirft.
erwartet = Reject: MALFORMED_CBOR
```

Der Vektor gehört zu D130: der Rundlauf steht im selben `try` wie das Dekodieren, und was von dort
kommt, ist unlesbar. Eine Implementierung, die den Rundlauf ungeschützt aufruft, liefert hier
**keinen** Reject-Code, sondern einen Bibliotheksfehler — das ist der Defekt, den BV1 fängt.

#### BV2 — indefinite-length **und** Nicht-uint-Schlüssel → `MALFORMED_CBOR`

```
           bf616100ff

; Indefinite-length-Map {"a": 0}. Dekodiert, ist nicht kanonisch, und hat einen
; text-Schlüssel.
erwartet = Reject: MALFORMED_CBOR
```

Der Grund ist der **Schlüsseltyp**, nicht die Längenform. Eine Implementierung, die zuerst auf
Kanonizität prüft, antwortet `NON_CANONICAL_ENCODING` und behauptet damit, es gebe eine kanonische
Kodierung desselben Inhalts, die gültig wäre — die gibt es nicht, ein `str`-Schlüssel bleibt in
jeder Kodierung ungültig. Der Vektor prüft die Vorrangregel aus `Anhang B.2`, nicht eine
Prüfreihenfolge: an welchem Schritt eine Fassung den Mangel findet, bleibt ihr überlassen.

#### BV3 — indefinite-length als **einziger** Mangel → `NON_CANONICAL_ENCODING`

Derselbe logische Inhalt wie TV1 — sortierte uint-Schlüssel, gültige Feldtypen, gute Signatur —
allein die Längenform der äußeren Map ist indefinite.

```
           bf00010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3
           748801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a
           91b4ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364
           61333066646130363164376335656630303262366238306534323638326364
           353464373033616231336662366337643266353535372f766f756368403104
           44a100186405582065309fe233da30fda061d7c5ef002b6b80e42682cd54d7
           03ab13fb6c7d2f5557061a6553f100071a6774858008582062db0b05f44c17
           e2dfe7f371d631845fdd5858dd94c37d327a28f73b25625430095840ef3b66
           74898a1f037bdb58dc485926b4f0de01ef995d6cbf7d6387c4dd33679f63da
           403f2f2d1c4bb39513484dee2c74387ec904bbab0aa22b8bdb376fb1c401ff

dekodiert zu TV1.signed_map    : true
received == canonical          : false    (310 Byte statt 309)
reserialize(received) == TV1.signed_bytes : true
erwartet = Reject: NON_CANONICAL_ENCODING
```

BV3 trennt, was `Anhang B.2` vor D130 zusammenwarf. Eine dekodierbare indefinite-length-Kodierung
ist der Musterfall von `NON_CANONICAL_ENCODING`: es gibt eine kanonische Kodierung desselben
Inhalts, und sie ist eine andere. Unter `MALFORMED_CBOR` fällt die Längenform nur, wenn sie
**unabgeschlossen** ist — und das deckt „nicht dekodierbar" bereits ab.

### C.9 TV5 — `core/revoke@1` mit gesetztem `t_exp` (Wiederholung auf TV1, verkettet auf TV3)

```
core = { 0:1, 1:ALICE, 2:[2, TV1.claim_id], 3:"core/revoke@1",
         6:1700000300, 7:1700000400, 8:TV3.claim_id }

bytes    = a700010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3
           748801b40f6f5c0282025820f95d430e40df736cbdffd7bf82af4f77e0c7af
           8692565f3b2a151c2c1ae8660c036d636f72652f7265766f6b654031061a65
           53f22c071a6553f2900858208e76a2a9ee6677e6959bf9868dc6d162e5ff7e
           464a6bb4c6b839f89713e54629
claim_id = 8b19196274b2a8ac08e9a34337de5f445e6efd19fb75155eb187b069f5fd8022
σ        = 61522c987609f25a18292abb53df78a5a7ee5027d3ad09b28e6d7adfbb06cd68
           e1c586fbebbc91f27c87ca513ddb4fa833ead9f979e229d7730c7132ab083d0d
```


Wirkung: keine. TV1 ist durch TV3 bereits widerrufen; TV5 wiederholt den Widerruf und ist
selbst bei einem `now` jenseits seines `t_exp` weiterhin `active` (§5.3, Anhang B.3).

### C.10 NV4–NV11 — negative Vektoren für den Fehlerkanal

Acht Claims, jeder mit genau einem Mangel. Alle übrigen Felder sind die Grundwerte von TV1
ohne `t_exp`, korrekt signiert. Sie prüfen denselben Fehlerkanal wie C.8: welchen Code eine
Implementierung liefern muss, unabhängig davon, an welcher Stelle ihrer Prüfreihenfolge sie
ihn findet.

#### NV4 — `version` 2 → `UNSUPPORTED_VERSION`

Verletzt Punkt 1 von §6: `version` wird nicht unterstützt.

```
core = { 0:2, 1:ALICE, 2:[1, BOB], 3:"nuc:6530…5557/vouch@1",
         4:h'a1001864', 5:N, 6:1700000401, 8:h_prev_genesis(ALICE) }

bytes    = a800020158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f5557061a6553f29108582062db0b05f44c17e2dfe7f371d631845fdd5858dd
           94c37d327a28f73b25625430
claim_id = 382810f6d71a1767c96e678a05519da48713a556f0277f8a97732b9d9714bf09
σ        = b73db1e3037bb602e2eb7c79c268f552dc5d51132f88fdd4bf9c3df509e6aacf
           b969429bd48ee179c7057dbd6192c58dd65407d876d238136271c60f920e3f0c
erwartet = Reject: UNSUPPORTED_VERSION
```

#### NV5 — `J.tag` 4 → `UNKNOWN_J_TAG`

Verletzt Punkt 3 von §6: `J.tag` liegt nicht im geschlossenen Enum `{1,2,3}`.

```
core = { 0:1, 1:ALICE, 2:[4, BOB], 3:"nuc:6530…5557/vouch@1",
         4:h'a1001864', 5:N, 6:1700000402, 8:h_prev_genesis(ALICE) }

bytes    = a800010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820458208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f5557061a6553f29208582062db0b05f44c17e2dfe7f371d631845fdd5858dd
           94c37d327a28f73b25625430
claim_id = 341cd38cebb06e8b9b2b33c10def16530df4576862c5dc92d98dc9fecadd8a7d
σ        = 53bbc9430388716ab18063f91200025cd79319ae553782eace0f3022a393c15c
           e4677816d4899f606c988c7940add80ddc15ce9e6e582fe19da20aa1044a270f
erwartet = Reject: UNKNOWN_J_TAG
```

#### NV6 — Namensraum `foo` → `UNKNOWN_NAMESPACE`

Verletzt Punkt 4 von §6: der Namensraum von `p` ist weder `core` noch `nuc:`.

```
core = { 0:1, 1:ALICE, 2:[1, BOB], 3:"foo/vouch@1",
         4:h'a1001864', 6:1700000403, 8:h_prev_genesis(ALICE) }

bytes    = a700010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b394036b666f6f2f766f75636840310444a1001864061a
           6553f29308582062db0b05f44c17e2dfe7f371d631845fdd5858dd94c37d327a
           28f73b25625430
claim_id = e9a3dbb5903dba124c2c746e4a8a2180454fba7527ac406e57af40bfd8c9824a
σ        = 0576a0be4bcbb1fc32912b1a9e62e4b1b90e633f0345e33d3ae5fa16f00dc514
           74ff68a38bcce79acf899fd08db629d8fe75ef7d81b76d7e2bf14ae4f87e420e
erwartet = Reject: UNKNOWN_NAMESPACE
```

#### NV7 — `N` entspricht dem kanonischen Scope nicht → `BAD_SCOPE_BINDING`

Verletzt Punkt 4 von §6, Bindungsregel §2.2 Regel 3: `N` ist gesetzt und ungleich
`bytes.fromhex(scope)`.

```
core = { 0:1, 1:ALICE, 2:[1, BOB], 3:"nuc:6530…5557/vouch@1",
         4:h'a1001864', 5:32×0x11, 6:1700000404, 8:h_prev_genesis(ALICE) }

bytes    = a800010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           0558201111111111111111111111111111111111111111111111111111111111
           111111061a6553f29408582062db0b05f44c17e2dfe7f371d631845fdd5858dd
           94c37d327a28f73b25625430
claim_id = 0c9b903b704dd4f996522cef13f96bfa2fb9f553196579981ba58d39801c3099
σ        = 9275a4193d9bec8f9cfe9aab8929a54f7c6cbc77678e7a51fa1dfa9637f4ab2d
           902fe71388c9646a84c74e2e380c5ca54c2e21d765767505c91ae16416a15e04
erwartet = Reject: BAD_SCOPE_BINDING
```

#### NV8 — Alias-Kodierung ohne `N` → `BAD_SCOPE_BINDING`

Verletzt Punkt 4 von §6, Bindungsregel §2.2 Regel 3: bei Alias-Kodierung fehlt `N`.

```
core = { 0:1, 1:ALICE, 2:[1, BOB], 3:"nuc:beispiel-alias/vouch@1",
         4:h'a1001864', 6:1700000405, 8:h_prev_genesis(ALICE) }

bytes    = a700010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403781a6e75633a626569737069656c2d616c696173
           2f766f75636840310444a1001864061a6553f29508582062db0b05f44c17e2df
           e7f371d631845fdd5858dd94c37d327a28f73b25625430
claim_id = 52c26cea614c8460f859a6e0756eb8cbb6e3cf7b8409547f3f41e5d727af60b5
σ        = 17f1a3ded18d913034e6e607b9a93e0d297729f5faaf901556f77bb5ed69b52a
           cbb1d3a827839cb63e58abda199248b29f06f1008189c4a25d5d17881ba95b04
erwartet = Reject: BAD_SCOPE_BINDING
```

#### NV9 — `core/rotate@1` → `RESERVED_CORE_PREDICATE`

Verletzt Punkt 4 von §6: `core/*` liegt nicht in `{revoke@1, supersede@1}`.

```
core = { 0:1, 1:ALICE, 2:[2, TV1.claim_id], 3:"core/rotate@1",
         6:1700000406, 8:h_prev_genesis(ALICE) }

bytes    = a600010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c0282025820f95d430e40df736cbdffd7bf82af4f77e0c7af8692
           565f3b2a151c2c1ae8660c036d636f72652f726f746174654031061a6553f296
           08582062db0b05f44c17e2dfe7f371d631845fdd5858dd94c37d327a28f73b25
           625430
claim_id = 614aab79e4bea65dd486b46f95a4d1f50ad03205f92aac14e454b4446fd71969
σ        = f899d194336b2456e11cbe7ad7012cbe7a4d9cef68b604ea93701f194d6a6f35
           13330a1a402a93f256680cccb92749db8c786ff2c64daeed9d371857ab7aab0e
erwartet = Reject: RESERVED_CORE_PREDICATE
```

#### NV10 — Signatur von BOB, `I` bleibt ALICE → `BAD_SIGNATURE`

Verletzt Punkt 5 von §6: `Ed25519-Verify` gegen `C.I` schlägt fehl.

```
core = { 0:1, 1:ALICE, 2:[1, BOB], 3:"nuc:6530…5557/vouch@1",
         4:h'a1001864', 5:N, 6:1700000407, 8:h_prev_genesis(ALICE) }

bytes    = a800010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f5557061a6553f29708582062db0b05f44c17e2dfe7f371d631845fdd5858dd
           94c37d327a28f73b25625430
claim_id = f4541adfc37c1d42b880cee040c1018772f47020736bc02ed3d4b21fed7b611b
σ        = b5147f2d004b03e9c46d33db57bfe3e37af585b875357fac2f3b8bd2f2433a05
           ad88ffe76ca55ed747feba8ead186de324baf7b3b1bafda67bf8a41c6a494106
erwartet = Reject: BAD_SIGNATURE
```

#### NV11 — `t_exp` gleich `t` → `INCOHERENT_EXPIRY`

Verletzt Punkt 7 von §6: `t < t_exp` gilt nicht, die Gleichheit liegt auf der Grenze.

```
core = { 0:1, 1:ALICE, 2:[1, BOB], 3:"nuc:6530…5557/vouch@1",
         4:h'a1001864', 5:N, 6:1700000408, 7:1700000408, 8:h_prev_genesis(ALICE) }

bytes    = a900010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f5557061a6553f298071a6553f29808582062db0b05f44c17e2dfe7f371d631
           845fdd5858dd94c37d327a28f73b25625430
claim_id = 32dd820ac291f75319369563f9eb10fe30de77607cb24cbb5a6778798a57ff3c
σ        = 5ee6ea5ec53776d0e804b2b7640cd87dbb84b22486b3f3510b85f3d6dc9f381a
           e6d313a10ce6f9af4d6f650458477110ccc7ca36c68dc087aeed26dc00e14308
erwartet = Reject: INCOHERENT_EXPIRY
```

### C.11 TV6 und NV12 — `t_exp` auf `core/*` und falscher `J.tag`

#### TV6 — `core/revoke@1` mit `t ≥ t_exp`

Auf `core/*` bleibt `t_exp` ohne Wirkung. Deshalb ist auch `t ≥ t_exp` kein
Reject (§5.3). TV6 trägt `t = 1700000410` und `t_exp = 1700000405` und gilt.

```
core = { 0:1, 1:ALICE, 2:[2, TV1.claim_id], 3:"core/revoke@1",
         6:1700000410, 7:1700000405, 8:TV5.claim_id }

bytes    = a700010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c0282025820f95d430e40df736cbdffd7bf82af4f77e0c7af8692
           565f3b2a151c2c1ae8660c036d636f72652f7265766f6b654031061a6553f29a
           071a6553f2950858208b19196274b2a8ac08e9a34337de5f445e6efd19fb7515
           5eb187b069f5fd8022
claim_id = 990b870c9e1c92d7fc442c70cdfe3b2d06d04ca41c522c6efe9e0834902d952e
σ        = 77e2d66ddf07a87414030be860efd0e97020ddc3f11d53e184ba27d40f7610de
           6a2420816325aa5d2f7a75ee8670006b27e213bbb7ad69dc09f25daacb596008
```

#### NV12 — `J.tag` 1 → `MALFORMED_CBOR`

Der Tag ist `1` statt `claim-ref`. Das verletzt die Form, die §6 Punkt 4 für
`core/*` verlangt. Ohne bekannten Ziel-Claim kann `FOREIGN_LIFECYCLE` nichts
behaupten; der Code ist `MALFORMED_CBOR`.

```
core = { 0:1, 1:ALICE, 2:[1, ALICE], 3:"core/revoke@1",
         6:1700000409, 8:h_prev_genesis(ALICE) }

bytes    = a600010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d
           94121bf3748801b40f6f5c036d636f72652f7265766f6b654031061a6553f299
           08582062db0b05f44c17e2dfe7f371d631845fdd5858dd94c37d327a28f73b25
           625430
claim_id = 8d253635ff9d59cca68fa760c589a3393551053a4ea08a5c78ce936d7541bddc
σ        = 9fac85e00bccce34144f33e885bdfe60b8d9d4a4d298de74d30dd99198b0f1fd
           80c2df73397c417e4aa7ec2aea22865d76185fba1bac5d0566f51113df4ba306
erwartet = Reject: MALFORMED_CBOR
```

### C.12 NV13 — Formverstoß unter nuc:

Der Name ist `VOUCH` statt `vouch`. Das verletzt die Form, die Anhang A für
`nuc:…` verlangt. `UNKNOWN_NAMESPACE` behauptet, der Namensraum sei unbekannt;
er ist `nuc:`. Der Code ist `INVALID_PREDICATE`.

```
core = { 0:1, 1:ALICE, 2:[1, BOB], 3:"nuc:6530…5557/VOUCH@1",
         4:h'a1001864', 5:N, 6:1700000411, 8:h_prev_genesis(ALICE) }

bytes    = a800010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f564f55434840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f5557061a6553f29b08582062db0b05f44c17e2dfe7f371d631845fdd5858dd
           94c37d327a28f73b25625430
claim_id = ffc2ae3df57e3c6753037fd601a8aa5d6cd67bb2d6a9bc31073084024b1595ff
σ        = 9e7548f45283682ee306cf8ae5ec3c2b043286d355eb0225a692a2475346c659
           c14c2b2d97497aa421b9f4b737b0c2f9c6be1e6e3d959e00d712debeda9d4c08
erwartet = Reject: INVALID_PREDICATE
```

### C.13 NV14–NV19 — Feldsatz, doppelte Keys, Version und Arity

Fünf der sechs tragen genau einen Mangel. NV18 trägt zwei und prüft deshalb — wie
BV2 in C.8 — den **Vorrang**, nicht eine Prüfreihenfolge.

#### NV14 — Key außerhalb der Tabelle → `MALFORMED_CBOR`

Der Core trägt Key 20. Der Autor hat den erweiterten Core mitsigniert, damit
`BAD_SIGNATURE` keine wahre Aussage über die Folge ist. Der Code ist
`MALFORMED_CBOR`.

```
bytes    = ab00010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f5557061a6553f100071a6774858008582062db0b05f44c17e2dfe7f371d631
           845fdd5858dd94c37d327a28f73b25625430095840c51adab69faff250c4d6e8
           8234fc71f9648b3916ad23cf2c2007f856696facbc81fdf7b14425ed131d5310
           b3fbb052b933daff11437c42c3439b7204132d0b081401
erwartet = Reject: MALFORMED_CBOR
```

#### NV15 — `t` ist CBOR `true` → `MALFORMED_CBOR`

Key 6 trägt `h'f5'` statt eines uint. `01 §2` verlangt uint. Der Code ist
`MALFORMED_CBOR`.

```
bytes    = aa00010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f555706f5071a6774858008582062db0b05f44c17e2dfe7f371d631845fdd58
           58dd94c37d327a28f73b2562543009584008df55af7c463bd19c8aae8b502b47
           4a841a4230f7730fcd4ea486fbd10b1a322e31ac8d969eb4216ad20dc718fb7e
           18980a8d65cfe22e02f71b5afd65978d09
erwartet = Reject: MALFORMED_CBOR
```

#### NV16 — `t` ist negativ → `MALFORMED_CBOR`

Key 6 trägt die Zahl -5 (Major 1). `01 §2` verlangt uint. Der Code ist
`MALFORMED_CBOR`.

```
bytes    = aa00010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f55570624071a6774858008582062db0b05f44c17e2dfe7f371d631845fdd58
           58dd94c37d327a28f73b25625430095840c59e71efa56d1d9471870e1bf3c015
           13371bd8e388cfc384825d6578a69f3032cfdbf8c7fe21882903aced162fbeb1
           cfe1be6051437c33c551361a30b988b500
erwartet = Reject: MALFORMED_CBOR
```

#### NV17 — doppelter Map-Key → `MALFORMED_CBOR`

Key 6 kommt zweimal vor. Der Mangel liegt in der dekodierten Semantik; keine
Kodierung behebt ihn. `NON_CANONICAL_ENCODING` behauptete das Gegenteil. Der
Code ist `MALFORMED_CBOR`.

```
bytes    = ab00010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f5557061a6553f100061a6553f101071a6774858008582062db0b05f44c17e2
           dfe7f371d631845fdd5858dd94c37d327a28f73b25625430095840ef3b667489
           8a1f037bdb58dc485926b4f0de01ef995d6cbf7d6387c4dd33679f63da403f2f
           2d1c4bb39513484dee2c74387ec904bbab0aa22b8bdb376fb1c401
erwartet = Reject: MALFORMED_CBOR
```

#### NV18 — `version` 2 ohne `t` → `UNSUPPORTED_VERSION`

Die Folge trägt zwei Mängel: eine nicht unterstützte Version und ein fehlendes
Pflichtfeld der v1-Tabelle. `MALFORMED_CBOR` behauptete einen Mangel, den erst
die v1-Tabelle setzt. Der Code ist `UNSUPPORTED_VERSION`.

```
bytes    = a900020158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f5557071a6774858008582062db0b05f44c17e2dfe7f371d631845fdd5858dd
           94c37d327a28f73b25625430095840e339410a8372c04d160d8170d5125f1ca1
           795bd692ad0fc4ed0408ba56a7d0c8837654d899928c7c779038fab8aeaad4bd
           1ba28c58b72ebc129b4c148c98a306
erwartet = Reject: UNSUPPORTED_VERSION
```

#### NV19 — Restbytes hinter dem Item → `MALFORMED_CBOR`

Hinter dem vollständigen TV1-Item steht ein Byte `h'00'`. Die Folge ist keine
Kodierung eines Claims. `NON_CANONICAL_ENCODING` setzte voraus, dass sie eine
Kodierung desselben Inhalts ist. Der Code ist `MALFORMED_CBOR`.

```
bytes    = aa00010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f5557061a6553f100071a6774858008582062db0b05f44c17e2dfe7f371d631
           845fdd5858dd94c37d327a28f73b25625430095840ef3b6674898a1f037bdb58
           dc485926b4f0de01ef995d6cbf7d6387c4dd33679f63da403f2f2d1c4bb39513
           484dee2c74387ec904bbab0aa22b8bdb376fb1c40100
erwartet = Reject: MALFORMED_CBOR
```

### C.14 NV20–NV30 — Feldtabelle, Zeile für Zeile

Jeder der elf verletzt genau eine Zeile der Feldtabelle aus §2 oder den
Pflichtfeldsatz. Im Übrigen ist jeder kanonisch kodiert und über seinen
eigenen Core signiert.

#### NV20 — `version` ist CBOR `true` → `MALFORMED_CBOR`

Key 0 trägt `h'f5'` statt 1. `01 §2` verlangt uint. Der Code ist
`MALFORMED_CBOR`.

```
bytes    = aa00f50158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f5557061a6553f100071a6774858008582062db0b05f44c17e2dfe7f371d631
           845fdd5858dd94c37d327a28f73b25625430095840c5d394e8074abe2f69d4d6
           b07142fd7fdd028d1e68178ba555dd7740282bbfd6db552802b9c031ed49d916
           c72861c03bbf90fa6e4c3c310a7e6cb0ef49137802
erwartet = Reject: MALFORMED_CBOR
```

#### NV21 — `I` mit 31 Byte → `MALFORMED_CBOR`

Key 1 trägt die ersten 31 Byte seines TV1-Wertes. `01 §2` verlangt
`bytes[32]`. `BAD_SIGNATURE` behauptete eine falsche Signatur; gemessen ist
eine Feldlänge außerhalb der Tabelle. Der Code ist `MALFORMED_CBOR`.

```
bytes    = aa000101581f8a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4ee
           37a25df60f5b8fc9b39403784c6e75633a363533303966653233336461333066
           6461303631643763356566303032623662383065343236383263643534643730
           33616231336662366337643266353535372f766f75636840310444a100186405
           582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f
           5557061a6553f100071a6774858008582062db0b05f44c17e2dfe7f371d63184
           5fdd5858dd94c37d327a28f73b256254300958403ed31085fbee05a92526403d
           10171fb40a71c6f67fab94a5c70b447af0efa7c0009403d30bfa446f7cd7a518
           5a25d24fc401f3ab491266c4515060af2752f203
erwartet = Reject: MALFORMED_CBOR
```

#### NV22 — `J` mit drei Elementen → `MALFORMED_CBOR`

Key 2 trägt `[1, BOB_PUB, BOB_PUB]`. `01 §2` verlangt ein Array der Länge
zwei. Der Code ist `MALFORMED_CBOR`.

```
bytes    = aa00010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02830158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39458208139770ea87d175f56a35466c34c7ecccb8d8a
           91b4ee37a25df60f5b8fc9b39403784c6e75633a363533303966653233336461
           3330666461303631643763356566303032623662383065343236383263643534
           64373033616231336662366337643266353535372f766f75636840310444a100
           186405582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb
           6c7d2f5557061a6553f100071a6774858008582062db0b05f44c17e2dfe7f371
           d631845fdd5858dd94c37d327a28f73b256254300958408244711ecd09d009ad
           c8592b30d6b4dd2d3fc0e7ccc04d6ee988b4a88ed6abcbfe6f6827002bde0c01
           c80edab3b775bc5920cc8983ede726272d772750279403
erwartet = Reject: MALFORMED_CBOR
```

#### NV23 — `J.tag` ist CBOR `true` → `MALFORMED_CBOR`

Key 2 trägt `[true, BOB_PUB]`. `01 §2` verlangt `tag: uint`. Der Code ist
`MALFORMED_CBOR`.

```
bytes    = aa00010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c0282f558208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f5557061a6553f100071a6774858008582062db0b05f44c17e2dfe7f371d631
           845fdd5858dd94c37d327a28f73b25625430095840c39bc319fe1bddb3703166
           2f2a545c278b3ce3850b013875c0316a23b2b116d69356a644be4ab258116536
           35f00cf37125a231c4caaa01880dc51c608c31420e
erwartet = Reject: MALFORMED_CBOR
```

#### NV24 — `p` ist die Zahl 1 → `MALFORMED_CBOR`

Key 3 trägt die Zahl 1 statt einer Zeichenfolge. `01 §2` verlangt text. Der
Code ist `MALFORMED_CBOR`.

```
bytes    = aa00010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403010444a100186405582065309fe233da30fda061
           d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557061a6553f100071a6774
           858008582062db0b05f44c17e2dfe7f371d631845fdd5858dd94c37d327a28f7
           3b256254300958406d76e4dcf37d6803d63373172bec0fb203b2d819592346cf
           d9daaef1dcdce0562ce2908bd1d0797164f96dd1d5622dd86adf87a6d194252e
           0a04a3050e458109
erwartet = Reject: MALFORMED_CBOR
```

#### NV25 — `v` ist die Zahl 1 → `MALFORMED_CBOR`

Key 4 trägt die Zahl 1 statt einer Bytefolge. `01 §2` verlangt bytes. Der
Code ist `MALFORMED_CBOR`.

```
bytes    = aa00010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f7563684031040105582065
           309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f555706
           1a6553f100071a6774858008582062db0b05f44c17e2dfe7f371d631845fdd58
           58dd94c37d327a28f73b25625430095840a5b5842f0a02f9de9fd3be693b7bd7
           a7267d30d1669cae0af0527cff2ea598a8aa0ca0ba87132970545af2d5d786f9
           1e66cc5fb80bee27fbca9092b038874d0b
erwartet = Reject: MALFORMED_CBOR
```

#### NV26 — `N` mit 31 Byte → `MALFORMED_CBOR`

Key 5 trägt die ersten 31 Byte seines TV1-Wertes. `01 §2` verlangt
`bytes[32]`. Der Code ist `MALFORMED_CBOR`.

```
bytes    = aa00010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05581f65309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f55061a6553f100071a6774858008582062db0b05f44c17e2dfe7f371d63184
           5fdd5858dd94c37d327a28f73b25625430095840f2f5f675ad44a8c27a06c124
           336bb65650990e728cae6b22bc87255f2f16f3f83c86516a70199034e5bb4035
           0474bc9dcbcbfa1768f1a79e1fefbc28c9b30106
erwartet = Reject: MALFORMED_CBOR
```

#### NV27 — `t_exp` ist CBOR `true` → `MALFORMED_CBOR`

Key 7 trägt `h'f5'` statt eines uint. `01 §2` verlangt uint. Der Code ist
`MALFORMED_CBOR`.

```
bytes    = aa00010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f5557061a6553f10007f508582062db0b05f44c17e2dfe7f371d631845fdd58
           58dd94c37d327a28f73b256254300958408084f47ad19b2e1e812cc9f89ae78d
           239279721f4458c677c0b0acd0f73cf16c13d4a8279c895ceaa0dac6c9ab198a
           54be6e6e4f68a0a3e89dc0bc65a1826f04
erwartet = Reject: MALFORMED_CBOR
```

#### NV28 — `h_prev` mit 31 Byte → `MALFORMED_CBOR`

Key 8 trägt die ersten 31 Byte seines TV1-Wertes. `01 §2` verlangt
`bytes[32]`. Der Code ist `MALFORMED_CBOR`.

```
bytes    = aa00010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f5557061a6553f100071a6774858008581f62db0b05f44c17e2dfe7f371d631
           845fdd5858dd94c37d327a28f73b25625409584087aa837420146e531345a3e0
           a9bac1edc8583aa4946c54cc8182beb15ebb6a93b9cbf926ceb6fb6d818ba082
           0b8885721bf0c7a55af5e4fc43511998f0fe8a05
erwartet = Reject: MALFORMED_CBOR
```

#### NV29 — `σ` mit 63 Byte → `MALFORMED_CBOR`

Der Core ist der von TV1. Key 9 trägt die ersten 63 Byte der Signatur.
`01 §2` verlangt `bytes[64]`. `BAD_SIGNATURE` behauptete eine falsche
Signatur; gemessen ist eine Feldlänge außerhalb der Tabelle. Der Code ist
`MALFORMED_CBOR`.

```
bytes    = aa00010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f5557061a6553f100071a6774858008582062db0b05f44c17e2dfe7f371d631
           845fdd5858dd94c37d327a28f73b2562543009583fef3b6674898a1f037bdb58
           dc485926b4f0de01ef995d6cbf7d6387c4dd33679f63da403f2f2d1c4bb39513
           484dee2c74387ec904bbab0aa22b8bdb376fb1c4
erwartet = Reject: MALFORMED_CBOR
```

#### NV30 — Key 3 fehlt → `MALFORMED_CBOR`

Das Pflichtfeld `p` fehlt. `01 §2` verlangt Key 3. Der Code ist
`MALFORMED_CBOR`.

```
bytes    = a900010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b3940444a100186405582065309fe233da30fda061d7c5
           ef002b6b80e42682cd54d703ab13fb6c7d2f5557061a6553f100071a67748580
           08582062db0b05f44c17e2dfe7f371d631845fdd5858dd94c37d327a28f73b25
           6254300958400e49e5cc1fbbbc6ee184be8665c26d4cb4d7219d03da2cd904cb
           58843ecb775aed7c334db5c7d1da3113f5632e00826a389b96abe9bff4eb409a
           8165607ba70e
erwartet = Reject: MALFORMED_CBOR
```

### C.15 NV31 — die Drahtform ist kein Map

`01 §3` Regel 1 verlangt, dass die oberste Ebene eine CBOR-Map mit uint-Keys ist. NV31 verletzt
genau diese Regel und sonst keine: er trägt die zehn Werte von TV1 in aufsteigender
Key-Reihenfolge als CBOR-Array, ist im Übrigen kanonisch kodiert, und die Signatur in der letzten
Position ist die von TV1 und über dessen Core gültig.

Der Vektor fragt, ob eine Implementierung die Felder über ihre Keys liest oder über ihre Position.
Wer sie über die Position liest, baut aus diesen 299 Byte TV1 zurück, findet die Signatur gültig
und akzeptiert einen Claim, den `01 §3` nicht kennt — mit derselben `claim_id` wie TV1. Das ist
dieselbe Bauart wie NV22 (§C.14): eine Drahtform, die auf dem Weg zum Preimage zurechtgeschnitten
wird und deshalb an der Signatur nicht scheitert.

Der Code ist `MALFORMED_CBOR` und nicht `NON_CANONICAL_ENCODING`. Die Bytes sind kanonisches
CBOR; ihre Re-Serialisierung ist byte-gleich. `NON_CANONICAL_ENCODING` wäre eine falsche Aussage
über sie (D262). Kanonizität ist in `01 §3` an der Claim-Map erklärt — was keine Map ist, ist kein
Claim, dessen Kodierung sich beurteilen ließe.

#### NV31 — zehn TV1-Werte als Array statt als Map → `MALFORMED_CBOR`

```
bytes    = 8a0158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801
           b40f6f5c820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a2
           5df60f5b8fc9b394784c6e75633a363533303966653233336461333066646130
           3631643763356566303032623662383065343236383263643534643730336162
           31336662366337643266353535372f766f756368403144a1001864582065309f
           e233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f55571a6553
           f1001a67748580582062db0b05f44c17e2dfe7f371d631845fdd5858dd94c37d
           327a28f73b256254305840ef3b6674898a1f037bdb58dc485926b4f0de01ef99
           5d6cbf7d6387c4dd33679f63da403f2f2d1c4bb39513484dee2c74387ec904bb
           ab0aa22b8bdb376fb1c401
erwartet = Reject: MALFORMED_CBOR
```

### C.16 NV32 — Zeitrückdatierung gegen den eigenen Vorgänger

Alice kettet auf **TV6**, das Ende ihrer Kette, und trägt ein `t` eine Sekunde **vor** dem `t`
ihres eigenen Vorgängers. Strukturell ist der Claim einwandfrei: Signatur gültig, Vorgänger
bekannt und gültig, kein Feld verletzt einen der sieben Punkte aus §6. Der einzige Mangel ist
die Zeitaussage gegen die eigene Kette — und weil die Prüfung den Vorgänger braucht, ist sie
kein Reject, sondern ein Zustand (§6, Anhang B.1).

Der Anker ist **TV6 und nicht TV1**. An TV1 trüge NV32 dasselbe `(I, h_prev)` wie TV2 und wäre
dessen Equivocation-Geschwister; im vollständigen Vektorspeicher wäre NV32 dann
`equivocation-flagged` statt `time-regression-flagged`, und TV2 wechselte mit ihm aus `active`
heraus. Der Vektor belegte damit nichts und verschöbe zugleich die Aussage seines Nachbarn.
Gemessen, behoben, als Regel festgehalten in D358: ein Vektor muss den Zustand, den er belegt,
im vollständigen Speicher annehmen. TV6 ist kinderlos und deshalb der richtige Andockpunkt.

Was der Vektor **nicht** belegt: nichts über `now` und nichts über `t_exp`. Die Monotonie
vergleicht zwei signierte Felder derselben Kette und braucht keine Uhr; `now` bleibt lokal,
subjektiv und außerhalb jeder Kollision (D350).

```
core = { 0:1, 1:ALICE, 2:[3, CONST], 3:"nuc:6530…5557/accept-rules@1",
         5:N, 6:1700000409, 8:TV6.claim_id }   ; TV6 trägt t = 1700000410

claim_id = 1555e8a53354051b92b58bb1febeab2a48752f75475e8b09b746e5e56c3d700c
σ        = c53836a733d325eb44cc70c29c59037a79813b933f0be26a5f01ec3f90c97435
           6fd03a2194b4bcb30dd81b7e876d07dac2e077a8e16022877c58bc621bf7b301
erwartet = speichern; Claim als time-regression-flagged markieren; nicht
           trust-nutzbar; TV6 und Downstream unberührt; kein Reject-Code
```

## Änderungshistorie ggü. Vorentwurf (v1-Konsolidierung)

- **Genesis-`h_prev` vereinheitlicht** auf `SHA-256(DOM_ID_GEN ‖ I)` (Feldtabelle, §4, §6);
  `32×0x00` ist harter Reject (`INVALID_GENESIS_ANCHOR`, NV1). Drei widersprüchliche
  Definitionen entfernt.
- **`DOM_GENESIS` → `DOM_ID_GEN`** umbenannt (klare Abgrenzung zum Nukleus-Scope-Separator
  `DOM_NUC_GEN`, Def. `00 §3`).
- **`N` auf DF-0 gebracht:** 32-Byte-Scope-ID, Herleitung in `00` (§2.3); Atom prüft nur
  Byte-Gleichheit.
- **Scope-Sicherheit** als sechs normative Invarianten konsolidiert (§2.4).
- **Prädikat-Grammatik** formalisiert (Anhang A); Alias `[a-z0-9_-]+`, 64-Hex kanonisch
  reserviert, Version ohne führende Null.
- **`now`/`t_exp`-Widerspruch aufgelöst:** `now` lokal/subjektiv, `t_exp` lokale Gültigkeit,
  legitime Uneinigkeit, sichere Richtung = Unter-Vertrauen; Offline-Fall definiert (§6).
- **Zustandsmodell & Fehlerbehandlung** als Zustandsmaschine mit Fehlerklassen (§6, Anhang B);
  `pending` statt Reject bei unbekanntem Vorgänger; Replay idempotent; Re-Serialisierung Pflicht.
- **Lifecycle-Claims monoton:** `core/revoke`/`supersede` ohne `t_exp` (§5.3).
- **§8 Key-Rotation** auf DF-0 angeglichen (`rotate-key@1`-Profil / Governance-Akt;
  Diebstahl ⇒ Equivocation).
- **Selektive Stille** als non-normativer §1-Leitsatz mit VISION-Verweis.
- **Namensraum geglättet:** genau `core` + `nuc:` gültig; alles andere Reject
  (`UNKNOWN_NAMESPACE`); Prosa an Anhang-A-Grammatik angeglichen (§2.2, §6, Anhang B).
- **Test-Vektoren** real gerechnet (TV1–TV4, NV1–NV3; Anhang C); Beispiel-Nukleus
  jetzt schema-valide (00 §4/§5) und byte-identisch mit 00 §3.1 geteilt.
