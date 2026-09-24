# Dienste-Schicht — Spezifikation v1

Status: Entwurf · Protokollversion: 1 · Layer: Dienste (Komposition über allen anderen)

Diese Schicht führt **fast keinen neuen Mechanismus** ein. Ein *Dienst* ist keine neue Entität,
sondern eine **Identity, die ein Verhalten über Zeit verspricht** — Validierung, Zeit-Bezeugung,
später Storage. Das ist die erste Schicht, die über *Liveness* spricht (Verfügbarkeit, korrektes
Verhalten über Zeit), wo alle vorherigen nur *Ein-Schuss-Aussagen* kannten. Genau daran hängt die
einzige wirklich neue normative Regel dieser Schicht: der **mechanische Falsch-Validierungs-Slash**
(§4). Alles andere ist Komposition aus Primitiven, die wir schon haben (Profil, Bond, Verdikt,
Obligation/Receipt, Enforcement).

Der Kern-Satz:

> **Ein Dienst macht ein Verhaltensversprechen; das Protokoll slasht nur, was *beweisbar* gebrochen
> ist.** Objektiv falsches Verhalten (eine nachweislich falsche Validierung, Equivocation) schlitzt
> **mechanisch**. Bloße Nicht-Verfügbarkeit (Liveness) trägt allein die **Reputation** — kein
> Bond-Slash ohne Beweis.

---

## 1. Leitsätze (Geltungsrahmen)

- **S1 — Dienst = Komposition, kein Atom-Feld.** `service-announce`, `timestamp`, `validation`
  sind **Profile** über dem Atom (Atom-Spec §7), bewertet unter `nuc:<N>`. Mieten, SLA, Staking
  sind Kompositionen aus `obligation`/`receipt` (Profile-II §3.3), Bond (Trust-Flow §6.1), Verdikt
  (Profile-II §2.2) und Enforcement (Enf-Spec). Diese Schicht ist **normativ-leicht**: sie schreibt
  nur dort neue Regeln, wo eine **neue Verifizierer-Pflicht** entsteht (§4, §9).
- **S2 — Dreiteiliges Fehlermodell (das Herzstück).** Dienst-Fehlverhalten zerfällt in drei
  Klassen mit *unterschiedlicher* Beweisbarkeit (§3): **objektiv-mechanisch** (Validierung),
  **gemischt** (Zeit), **Liveness-sozial** (Storage/Relay). Die Klasse bestimmt, *ob* und *wie*
  geslasht wird — exakt die objektiv/subjektiv-Linie aus Profile-II §2.3, auf Dienste angewandt.
- **S3 — Kein Dienst ist Autorität oder Orakel.** Jede Dienst-Attestierung ist ein Claim,
  **trust-gewichtet aus Sicht des Beobachters** (Trust-Flow-Spec), **nie** eine globale Wahrheit
  oder globale Ordnung. Ein Zeitdienst liefert keine kanonische Zeit; ein Validierungs-Node ist
  keine Instanz, die *entscheidet* — er *bezeugt*, und Bezeugung ist überprüfbar. Das bewahrt das
  Nicht-Monopol (VISION §1, §3).
- **S4 — Bewährtes adaptieren, nicht einbacken.** Wo etablierte Algorithmen ein Teilproblem lösen,
  werden sie **referenziert**, nicht ins Atom gezogen (§8): **Roughtime** (witnessed time +
  Inkonsistenz-Meldung) für den Zeitdienst, **NTS** (RFC 8915) für Transport-Auth, die
  **PoR/PoRep/PoSt-Klasse** für den vertagten Storage-Dienst. Das Atom bleibt
  algorithmus-agnostisch; ein Dienst-Profil *wrappt* einen externen Beweis, es *ersetzt* ihn nicht.

---

## 2. Node = Identity + `service-announce` (kein neues Objekt)

**Ein „Node" ist keine Protokoll-Entität.** Es ist eine Ed25519-Identity (Atom-Spec §1), die einen
Dienst ankündigt. „Node" ist Betriebs-Vokabular (der Lebensraum, in dem Atome existieren,
VISION §5), nicht Protokoll-Vokabular.

### 2.1 `nuc:<N>/service-announce@1`

| Feld   | Belegung |
|--------|----------|
| `I`    | der Betreiber (Node-Identity) |
| `J`    | `[object-hash, H(service_descriptor)]` — der content-adressierte Dienst-Deskriptor |
| `v`    | optional, opak (z. B. kurzer Typ-Tag / Endpoint-Hint) |
| `N`    | **Pflicht** — der Nukleus-Kontext, den der Dienst bedient |
| `t_exp`| optional — befristetes Angebot (lokale Gültigkeitsdecke, Atom-Spec §6) |

- **Deskriptor** (externes Objekt, per Hash referenziert — Muster aus Atom-Spec §7.2): trägt
  `type` (`validation`/`time`/…), Bedingungen, optional `bond_ref` (§7). Das Atom parst ihn nie.
- **Lebenszyklus:** Dienst einstellen = `core/revoke@1` auf den Announce (selbst-bezüglich,
  verstanden). Angebot ändern = `core/supersede@1` auf neuen Deskriptor.

### 2.2 Mieten ist selbst ein Dienst (rekursiv)

Selbst-gehostet **oder gemietet** (VISION §5) fällt ohne Sondermechanik heraus:

- Ein Hoster betreibt einen Dienst vom `type: hosting` (Compute/Storage-Lebensraum), angekündigt
  per `service-announce`.
- Der Mieter **konsumiert** ihn über `obligation@1`/`receipt@1` (Profile-II §3.3) — normaler
  gegenseitiger Kredit.
- Der Mieter fährt seinen **eigenen** Dienst unter **eigener** Identity auf dem gemieteten
  Lebensraum. Identität und Autorität bleiben beim Mieter; der Hoster liefert nur das Substrat.

**Ehrlicher Preis:** eine Ebene Verschachtelung (ein Dienst läuft auf einem gemieteten Dienst).
Das ist kein Sonderfall, sondern dasselbe radiale Muster eine Stufe tiefer — offen benannt (§11).

---

## 3. Das Fehlermodell (S2 konkret)

Der **Auslösertyp bestimmt die Beweisklasse** — und die Klasse bestimmt die Enforcement-Antwort
(Enf-Spec §3, gestufter Einstieg).

| Dienst | Fehler | Beweisklasse | Antwort |
|--------|--------|--------------|---------|
| **Validierung** | falsche Attestierung (behauptet gültig, ist malformed — oder umgekehrt) | **objektiv, selbst-validierend** | **mechanischer Slash** (§4, VR-06.1) — kein Verdikt |
| **Zeit** | Equivocation des eigenen Schlüssels | **objektiv** (Atom-Spec §4) | mechanischer Slash |
| **Zeit** | „falsche" Zeit attestiert | **subjektiv/oracle** | nur **Verdikt** + Vorab-Bindung (§5, Profile-II §2.4) |
| **Storage/Relay** | Nicht-Auslieferung / Ausfall | **Liveness, subjektiv** | **kein** Bond-Slash; Reputation-Decay (§6, VR-06.4) |

Der Glücksfall: **Validierung ist mechanisch**, weil strukturelle Gültigkeit von *jedem*
nachrechenbar ist (Atom-Spec §6). Das macht den wichtigsten Dienst dieser Schicht beweisbar —
und genau das ist die eine neue Regel, die `06` beisteuert.

---

## 4. Validierungs-Node & der mechanische Falsch-Validierungs-Slash (VR-06.1)

Ein Validierungs-Node bezeugt, dass ein Claim strukturell gültig ist (oder nicht) — nützlich für
Peers, die den Ziel-Claim (noch) nicht selbst geprüft haben. Das ist ein **Confidence-Signal**
(Atom-Spec §6, „Validierungs-Nodes orthogonal"), **kein** intrinsischer Atom-Zustand.

### 4.1 `nuc:<N>/validation@1`

| Feld | Belegung |
|------|----------|
| `I`  | der Validierungs-Node |
| `J`  | `[claim-ref, ziel.claim_id]` — der attestierte Claim |
| `v`  | opak: Ergebnis (Vorschlag: CBOR `{0: 1}` = strukturell gültig, `{0: 0}` = ungültig, + optional geprüfte Checks) |
| `N`  | **Pflicht** — der Kontext |

### 4.2 Die neue Verifizierer-Regel (normativ)

> **VR-06.1 — Falsch-Validierung ist mechanisch slashbar.** Gegeben eine `validation@1`-Attestierung
> `A` von Node `V` über Ziel `C` mit Ergebnis `R`, **und die Bytes von `C`**: Wenn `recompute(C)`
> (die strukturelle Prüfung aus Atom-Spec §6) dem behaupteten `R` **widerspricht**, dann ist das
> Paar `{A, C}` ein **selbst-validierender Falsch-Validierungs-Beweis** gegen `V`. Der Dienst-Bond
> (§7) schlitzt **mechanisch** in der ökonomischen Schicht — **ohne Verdikt**, in derselben Klasse
> wie Equivocation (Atom-Spec §4).

- **Beide Richtungen prüfbar:** „gültig" behauptet über ein malformtes `C` **oder** „ungültig"
  behauptet über ein gültiges `C` — beides ist ein Widerspruch, den jeder Verifizierer selbst
  feststellt.
- **Harte Voraussetzung (ehrlich):** Der Beweis braucht **`C`s Bytes**. Liegen sie nicht vor, ist
  `A` bloß eine unüberprüfbare Behauptung → **nur trust-gewichtet** (kein mechanischer Slash). Das
  ist die konsequente „Abwesenheit von Evidenz ist keine Evidenz"-Linie (Trust-Flow §7.3).
- **Propagation:** Der Beweis reist als **Fakt** (Enf-Spec §5, objektive Klasse), nicht als
  attribuierte Meinung — es ist Mathematik, kein Diffamierungsvektor.

---

## 5. Zeitdienst — witnessed-at, kein Ordnungs-Orakel (Fork 5)

Das Atom ist zeitquellen-agnostisch: `now` ist die lokale, subjektive Verifizierer-Zeit
(Atom-Spec §6). Der Zeitdienst liefert dazu ein **komposables Confidence-Signal** — er *bezeugt*
einen Claim in der Zeit, er *ordnet* nicht.

### 5.1 `nuc:<N>/timestamp@1`

| Feld | Belegung |
|------|----------|
| `I`  | der Zeitdienst |
| `J`  | `[claim-ref, ziel.claim_id]` — das bezeugte Objekt |
| `t`  | **die bezeugte lokale Zeit** — „ich sah `ziel` zu meiner Zeit `t`". Kein Extra-Feld nötig. |
| `v`  | optional (z. B. Quelle/Präzision, Roughtime-Proof-Ref) |
| `N`  | **Pflicht** — der Kontext |

Der ehrliche Trick: Das Feld `t` (vom Autor behaupteter Zeitstempel, Atom-Spec §2) *ist* die
bezeugte Zeit. `timestamp@1` verleiht ihm soziale Bedeutung („bezeugt"), ohne dem Atom eine neue
Semantik aufzuzwingen.

### 5.2 Normative Leitplanke (VR-06.3)

> **VR-06.3 — Eine Zeit-Attestierung ist kein globales Ordnungs-Orakel.** `timestamp@1` ist
> **trust-gewichtete Evidenz** aus Sicht des Beobachters, **nie** eine kanonische oder globale Zeit.
> Ordnung kommt **weiterhin** ausschließlich aus der Autorenkette (`h_prev`, Atom-Spec §5.3); ein
> `timestamp@1` **darf** die Kettenordnung **nicht** überschreiben. Sonst käme Wall-Clock durch die
> Hintertür zurück (der Fehler, den Atom-Spec §5.3 bewusst ausschließt).

- **Nutzen:** verankert einen *konkreten* Claim gegenüber einem vertrauten Dienst in der Zeit —
  hilft dem `t_exp`-Anchoring aus Atom-Spec §6, ohne globale Ordnung zu behaupten. Mehrere
  unabhängige Zeit-Attestierungen erhöhen die Confidence (wie mehrere Zeugen), bleiben aber je
  einzeln trust-gewichtet.

### 5.3 Fehler des Zeitdienstes (VR-06.2)

> **VR-06.2 — Zeit-Equivocation mechanisch, Falsch-Zeit nur per Verdikt.** Signiert der Zeitdienst
> zwei widersprüchliche Attestierungen auf gleichem `(I, h_prev)` → **Equivocation** (Atom-Spec §4),
> mechanischer Slash. Eine *nachweislich falsche* bezeugte Zeit ist dagegen **oracle-abhängig** →
> nur **Verdikt** mit Vorab-Bindung (Profile-II §2.4). Ehrlich: Der Zeitdienst ist überwiegend
> **reputationsgetragen**, nicht mechanisch fixierbar — genau wie Roughtimes „Inkonsistenz-Meldung"
> ein soziales Überführen ist, kein Konsens.

---

## 6. SLA & Liveness — rein sozial (Fork 3, VR-06.4)

> **VR-06.4 — Liveness ist nie *mechanisch* slashbar.** Bloße Nicht-Verfügbarkeit löst **keinen**
> Bond-Slash aus. Sie trägt allein den **Reputation-Decay** (Trust-Flow §7: versiegender Fluss,
> ausbleibende frische Evidenz). Bond-Slash bleibt **beweisbaren** Fehlern vorbehalten (VR-06.1,
> Equivocation) **oder** einem **Verdikt** über eine gebrochene SLA-Obligation.

**SLA = Komposition, kein neuer Mechanismus:**

- Ein Verfügbarkeits-Versprechen ist eine `obligation@1` (Profile-II §3.3) des Dienstes — „ich
  liefere Dienst X bis `t_exp` / im Zeitraum Y".
- Bruch ist **subjektiv** (hat er geliefert?) → **verdikt-slashbar nur bei Vorab-Bindung**
  (Arbitration in der Verfassung oder ad-hoc, `00 §5.1`, Profile-II §2.4). Ohne Bindung: bloß
  eine signierte Meinung, Wirkung allein über Reputation.
- Optionaler Dienst-Bond (§7) erhöht den Einsatz — verdikt-slashbar bei erwiesenem SLA-Bruch.

So bleibt „Verfügbarkeit" ein **Markt**-Signal (Reputation, freie Anbieterwahl), kein
Protokoll-Zwang — konsistent mit „detect-not-prevent" und dem freien Dienst-Markt (VISION §3).

---

## 7. Staking — Dienst-Bond (downside-only)

**Unter Vorbehalt (D467).** Die Glaubwürdigkeit eines Dienstes trägt bis dahin seine Reputation. Das
Wort „Bond“ ist ausgemustert: darunter lagen fünf verschiedene Probleme, die je ihr Szenario
beantwortet. Kein Mechanismus baut auf einer Stelle auf, die fremden Wert verwahrt oder einzieht.
Der Text hier bleibt, bis ein Szenario ihn anfasst.

Ein Dienst-Bond ist ein `bond_ref` im Deskriptor (§2.1) und folgt **exakt** der Bond-Semantik aus
Trust-Flow §6.1:

- **Downside-only.** Der Bond hebt **keine** Kapazität und **kein** Stimmgewicht — er macht den
  Dienst **slashbar** unter Beweis (VR-06.1 / Equivocation) oder Verdikt (SLA-Bruch). Costly
  Signal, kein Privileg.
- **Geldblind.** Ein reicher Betreiber kauft sich **kein** höheres Standing; er riskiert nur mehr.
  Der ehrliche Betreiber verliert nie (Trust-Flow §6.1, ehrlicher Residual).
- Eine Nukleus-Policy **MAY** für Hochrisiko-Dienste verlangen, dass nur **gebondete** Dienste
  zählen (ein Filter, kein Multiplikator).

---

## 8. Adaptierte Fremd-Algorithmen (S4 explizit)

Referenziert, **nicht** eingebacken — das Atom bleibt algorithmus-agnostisch, ein Dienst-Profil
wrappt einen externen Beweis:

- **Roughtime** (`draft-ietf-ntp-roughtime`, IETF NTP-WG, Intended Status *Experimental*). Zwei
  Eigenschaften passen exakt: (1) sichere *grobe* Zeit für Clients ohne jede Zeitvorstellung —
  unser Offline-/Bootstrap-Fall; (2) ein Format, mit dem Clients **Inkonsistenzen zwischen
  Zeitservern melden**. Diese Meldung ist strukturell unser Überführen eines Dienstes: ein Server,
  der widersprüchlich signiert, ist nachweisbar — genau VR-06.2. Der `timestamp@1`-`v` **MAY** eine
  Roughtime-Antwort/Merkle-Proof-Referenz tragen. **Als *work in progress* zitiert**, nicht als
  Normreferenz — der Draft ist experimentell.
- **NTS — Network Time Security** (RFC 8915). Transport-Authentisierung für Zeitabruf; relevant,
  wenn ein Zeitdienst über ein authentifiziertes Netz statt reiner Attestierung arbeitet. Transport-
  Profil-Sache (Atom-Spec §1, A1), nicht Kern.
- **Proof-of-Retrievability-Klasse** — PoR (Juels & Kaliski, 2007), sowie **PoRep/PoSt**
  (Proof of Replication / Proof of Spacetime, Filecoin-Linie). Das ist die Algorithmen-Klasse, die
  ein **künftiger** Storage-Dienst (§11, vertagt) wrappen würde, um „ich halte und liefere `C`"
  *beweisbar* statt bloß reputationsgetragen zu machen. In v1 **nicht** spezifiziert.

Prinzip (normativ): Ein externer Beweis wird über `v` oder ein `object-hash` **referenziert** und
von der **Policy/Anwendungsschicht** geprüft — das Atom validiert ihn nie (Atom-Spec §7.2, Muster
Cashu/externes Token, Profile-II §3.2).

---

## 9. Verifizierer-Regeln dieser Schicht (Zusammenfassung, normativ)

| Regel | Inhalt |
|-------|--------|
| **VR-06.1** | Falsche `validation@1` gegen bekannten Ziel-`C` ⇒ `{A, C}` selbst-validierender Beweis ⇒ **mechanischer** Dienst-Bond-Slash (kein Verdikt). Braucht `C`s Bytes; sonst trust-gewichtet. |
| **VR-06.2** | Zeit-Equivocation ⇒ mechanisch (Atom-Spec §4). Nachweislich falsche Zeit ⇒ **nur** Verdikt + Vorab-Bindung. |
| **VR-06.3** | `timestamp@1` ist trust-gewichtete Evidenz, **nie** globale Ordnung; überschreibt die Autorenkette (Atom-Spec §5.3) **nicht**. |
| **VR-06.4** | Liveness/Nicht-Verfügbarkeit ist **nie** mechanisch slashbar — nur Reputation-Decay, oder Verdikt bei gebundener SLA. |

Alle vier sind **Auswertungs**-Regeln über bestehenden Feldern; keine ändert Core, Serialisierung,
Signatur oder Validität eines Atoms.

---

## 10. Frozen-Primitive-Konformität (Nachweis)

Diese Schicht fügt **kein** Atom-Feld hinzu:

- **`service-announce@1`, `timestamp@1`, `validation@1`** sind Profile über bestehenden Feldern
  (`I`, `J ∈ {claim-ref, object-hash}`, `v`, `N`, `t`, `h_prev`). Keiner besteht den
  `core`-Aufnahmetest (alle machen **soziale** Aussagen mit Wert) — sie bleiben korrekt außerhalb
  von `core`, konsistent mit der Ablehnung von `vouch`/`verdict`/`membership` (Atom-Spec §5).
- **Namensraum:** alle Dienst-Prädikate leben unter **`nuc:<N>`** — kein neuer Namensraum, **keine
  Grammatik-Änderung** an Atom-Spec Anhang A. Die Scope-Autorität bleibt einzig an `N` (Atom-Spec
  §2.4, Invariante 2). Dienst-„Typ" ist der Prädikatname, nicht ein Namensraum-Präfix.
- **Mieten, SLA, Staking** sind Kompositionen aus `obligation`/`receipt`, Bond, Verdikt,
  Enforcement — bestehende Mechanik.
- **VR-06.1–06.4** sind Verifizierer-/Policy-Regeln, keine Formatänderung. Der mechanische Slash
  nutzt dieselbe ökonomische Schicht wie Equivocation.
- **Externe Beweise** (Roughtime, PoR) werden **referenziert**, nie im Atom validiert.

Ergebnis: rein additiv über Profile + content-adressierte Objekte + Verifizierer-Regeln. Das
radiale Prinzip bleibt intakt.

---

## 11. Bewusst getragene Grenzen & Designentscheidungen

- **Falsch-Validierungs-Slash braucht die Ziel-Bytes** (§4.2). Ohne `C` ist eine falsche
  Attestierung nur trust-gewichtet — mechanisch überführbar wird sie erst, wenn `C` propagiert.
  Das ist die konsequente „keine Evidenz aus Abwesenheit"-Linie, kein Schlupfloch.
- **Der Zeitdienst bleibt überwiegend reputationsgetragen.** Nur Equivocation ist mechanisch;
  „falsche Zeit" ist oracle-abhängig (VR-06.2). Roughtime mildert das (Inkonsistenz-Meldung),
  löst es nicht — dasselbe irreduzible Orakel-Problem wie überall (VISION §6).
- **Storage/Relay ist in v1 nur reputations-getragen benannt**, der beweisbare Teil (PoR/PoRep/PoSt)
  ist **vertagt** auf eine eigene Spec — er verdient die volle Sorgfalt der Filecoin-Klasse und
  gehört nicht halb hineingestreut.
- **Directory/Naming-Dienst vertagt.** Alias→`N`-Auflösung (Atom-Spec §2.4, Inv. 6) berührt die
  Squatting-Frage und bekommt eine eigene Behandlung, nicht hier.
- **Miet-Verschachtelung** (§2.2): ein Dienst auf einem gemieteten Dienst ist eine Ebene
  Indirektion. Bewusst getragen — es ist dasselbe radiale Muster, keine Sondermechanik.
- **Mieten trägt eine Annahme über den Hoster (D123).** „Identität und Autorität bleiben beim
  Mieter" (§2.2) gilt auf Protokollebene und ist auf Betriebsebene unbelegt: wer die Maschine
  betreibt, hat Zugriff auf den Speicher, in dem der Schlüssel liegt. Für **Dienste** ist das
  tragbar — eine falsche Attestierung ist über VR-06.1 mechanisch überführbar. Für die
  **persönliche Schreibautorität** ist es nicht tragbar: mit dem Schlüssel gehen Obligationen im
  Namen des Mieters, und der Beweis zeigt auf ihn. Ein gemieteter Ort taugt für Dienste, nicht
  für die eigene Kette.
- **`validation@1`-Ergebnis-Kodierung** (`v`) ist eine *vorgeschlagene* Form (`{0:1}`); die konkrete
  Check-Granularität ist ein Policy-Knopf. Das Atom parst `v` nie.
## Anhang — Test-Vektoren (real gerechnet, geteiltes Nukleus `N = 6530…5557`)

Fortsetzung des Beispiel-Nukleus aus `00 §3.1` / `01 Anhang C`. Neuer Akteur **CAROL** (Seed
`03×32`) betreibt einen Node mit Validierungs- und Zeitdienst. Reproduzierbar via kanonischem
CBOR + Ed25519; Signaturen verifiziert, `claim_id = SHA-256(DOM_CID ‖ bytes)`.

```
CAROL (I)            = ed4928c628d1c2c6eae90338905995612959273a5c63f93636c14614ac8737d1
h_prev_genesis(CAROL)= 8f66a5c0bb83f38b2d0e64dd069a5b9654d7e3aee3b18290b413c4653f890e2b
N                    = 65309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557
TV1.claim_id (aus 01)= f95d430e40df736cbdffd7bf82af4f77e0c7af8692565f3b2a151c2c1ae8660c
NV1.claim_id (aus 01)= 9b25020fee7da6832416f8bcb61e4a05329776d051a4da282db7e973eb96c453      ; malformed (h_prev=32×0x00)

descriptor           = { type:"validation", checks:"structural-only" }
cbor(descriptor)     = a264747970656a76616c69646174696f6e66636865636b736f7374727563747572616c2d6f6e6c79
DESC (object-hash)   = a06526bcec1a7334b059f0f36fcfce786d7102da2c25470d7d0655078820ab44
```

### SV1 — `service-announce@1` (CAROL kündigt Validierungsdienst an; Genesis der CAROL-Kette)

```
core = { 0:1, 1:CAROL, 2:[object-hash, DESC], 3:"nuc:6530…5557/service-announce@1",
         5:N, 6:1700000400, 8:h_prev_genesis(CAROL) }

bytes    = a70001015820ed4928c628d1c2c6eae90338905995612959273a5c63f93636c1
           4614ac8737d10282035820a06526bcec1a7334b059f0f36fcfce786d7102da2c
           25470d7d0655078820ab440378576e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f736572766963652d616e6e6f75
           6e6365403105582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703
           ab13fb6c7d2f5557061a6553f2900858208f66a5c0bb83f38b2d0e64dd069a5b
           9654d7e3aee3b18290b413c4653f890e2b
claim_id = 2f4ba01a6f7ec63d1eabc9220b21b1ec75c02d0cd58939e3b9da28e101964c52
σ        = 1560ed26185ca00e4c773a3341f5c87551958d14f2fd225291a845172995f835
           f3aa7eb086b055f9a2e665183180d0e34b88d9b2976948d8f150a568b0e12308
```

### SV2 — `timestamp@1` (witnessed-at: CAROL bezeugt TV1 zu ihrer lokalen Zeit `t`)

`t = 1700000500` **ist** die bezeugte Zeit — kein separates Feld nötig; `J` zeigt auf das
bezeugte Objekt. Keine globale Ordnung (VR-06.3).

```
core = { 0:1, 1:CAROL, 2:[claim-ref, TV1.claim_id], 3:"nuc:6530…5557/timestamp@1",
         5:N, 6:1700000500, 8:SV1.claim_id }

bytes    = a70001015820ed4928c628d1c2c6eae90338905995612959273a5c63f93636c1
           4614ac8737d10282025820f95d430e40df736cbdffd7bf82af4f77e0c7af8692
           565f3b2a151c2c1ae8660c0378506e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f74696d657374616d7040310558
           2065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f55
           57061a6553f2f40858202f4ba01a6f7ec63d1eabc9220b21b1ec75c02d0cd589
           39e3b9da28e101964c52
claim_id = f9741473aeedc0b2a43ee1031c8bea1335e67bdfa12ac47c3f6e2b150cab2d54
σ        = 7fa1a434cdf15da4618f28bbf5a8debc001b831fd8feb39ffb21c95381b3377e
           9abe4cd761c6b3cc8dd80543bc434b8a6d80a1e1ec83e28645cf543bfbef3d04
```

### SV3 — `validation@1` (WAHR: CAROL attestiert TV1 als strukturell gültig)

`v = h'a10001'` = CBOR `{0:1}` → Ergebnis „strukturell gültig". TV1 ist tatsächlich gültig →
korrekte Attestierung, kein Slash.

```
core = { 0:1, 1:CAROL, 2:[claim-ref, TV1.claim_id], 3:"nuc:6530…5557/validation@1",
         4:h'a10001', 5:N, 6:1700000600, 8:SV2.claim_id }

bytes    = a80001015820ed4928c628d1c2c6eae90338905995612959273a5c63f93636c1
           4614ac8737d10282025820f95d430e40df736cbdffd7bf82af4f77e0c7af8692
           565f3b2a151c2c1ae8660c0378516e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f76616c69646174696f6e403104
           43a1000105582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab
           13fb6c7d2f5557061a6553f358085820f9741473aeedc0b2a43ee1031c8bea13
           35e67bdfa12ac47c3f6e2b150cab2d54
claim_id = c1266a602985e4114b6a51f9c1aaec21fed1992e7602a9f004186fed1ce40d42
σ        = 64105651b5a213e2dc926b5ff9ed6b296dd34be4a94ef486770bac85ae1a6d21
           7fd2e8f96b2b147ba8ca822401683e198a2fb3594cc123be642333bc0ecca003
```

### NV06 — `validation@1` (FALSCH: attestiert das malformte NV1 als gültig → mechanischer Slash)

Gleiches `v` („gültig"), aber Ziel NV1 hat `h_prev = 32×0x00` → `INVALID_GENESIS_ANCHOR`.
Das Paar `{NV06, NV1}` ist ein **selbst-validierender Falsch-Validierungs-Beweis** (VR-06.1):
jeder Verifizierer mit NV1s Bytes rechnet nach und überführt CAROL **mechanisch**, ohne Verdikt.

```
core = { 0:1, 1:CAROL, 2:[claim-ref, NV1.claim_id], 3:"nuc:6530…5557/validation@1",
         4:h'a10001', 5:N, 6:1700000700, 8:SV3.claim_id }

bytes    = a80001015820ed4928c628d1c2c6eae90338905995612959273a5c63f93636c1
           4614ac8737d102820258209b25020fee7da6832416f8bcb61e4a05329776d051
           a4da282db7e973eb96c4530378516e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f76616c69646174696f6e403104
           43a1000105582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab
           13fb6c7d2f5557061a6553f3bc085820c1266a602985e4114b6a51f9c1aaec21
           fed1992e7602a9f004186fed1ce40d42
claim_id = 62060b515e3ac586ad6e7822a7313f1aa4ed8568053ba0af6a8299fb5d7fbb11
σ        = 383b19de7d48d5f6717c2a9f6bfeb59a37fcd83669d04c2a94c3b9130222cbb2
           bb5d28fd5b718a3387494c0e186051573ee2b8ce7ba0877dc0faae17d60a340c
erwartet = {NV06, NV1} ist self-contained Beweis; CAROLs Dienst-Bond schlitzt mechanisch
           (ökonomische Schicht, wie Equivocation). Ohne NV1s Bytes: nur trust-gewichtet.
```
