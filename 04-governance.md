# Governance-Schicht — Spezifikation v1

Status: Entwurf · Protokollversion: 1 · Layer: Governance (über Trust-Flow und Profile)

Diese Schicht regelt, wie ein Nukleus seine eigenen Regeln ändert, ohne dass jemand befragt
werden muss, der über ihm steht. Sie fügt kein Atom-Feld hinzu. Vorschläge und Verfassungen sind
content-adressierte Objekte, auf die Claims zeigen; die Stimmen sind die Claims.

Zwei Sätze tragen die ganze Schicht:

> **Ein Nukleus lebt in Epochen.** Jede Epoche beginnt mit einer ratifizierten Verfassung; diese
> Verfassung sagt, wer stimmberechtigt ist und wie hoch die Schwelle liegt. Der Genesis ist
> Epoche 1.
>
> **Es gibt genau einen Loop.** Vorschlag, Stimme, Auszählung, Materialisierung. `§6` und `§7`
> sind Belegungen seiner Parameter, keine eigenen Verfahren.

Was diese Schicht **nicht** tut, steht in `08 §3`: sie verteilt keine Macht. Schwellen,
Mitgliederkreis, Amtsdauern und Losverfahren sind Verfassungsinhalt eines konkreten Nukleus, nicht
Protokoll.

---

## 1. Objekte und Epochen

### 1.1 Die drei Objekte

**Genesis (unveränderlich).** Definiert `N` als stabilen Scope, die Wurzelschlüssel, das initiale
Ankerset, den Hash der initialen Verfassung, die Änderungsklasse, den Gewichtungsmodus und den
Stimmmodus (`00 §4`). Der Genesis ändert sich nie; wer ihn ändern will, gründet einen anderen
Nukleus.

**Verfassung (versioniert).** Die inhaltlichen Regeln, content-adressiert. Sie trägt in dieser
Schicht zwei zusätzliche Felder gegenüber `00 §5`:

| Feld | Typ | Pflicht | Bedeutung |
|---|---|---|---|
| `participants` | array of bstr (32 B), sortiert, duplikatfrei | optional | Die stimmberechtigte Menge `P` der Epoche |
| `thresholds` | map text zu `[num, den]` | Pflicht | Schwellen je Klasse, exakte Integer |

`participants` ist **optional**, damit das kanonische Beispiel aus `00 §3.1` es weglässt und `N`
byte-identisch bleibt. Ein Nukleus ohne deklariertes `participants` ist nicht auszählbar (`§3.5`).

`P` wird **deklariert, nie abgeleitet.** Eine aus dem Bestand abgeleitete Menge wäre unter
Teilwissen unter-bekannt; ein zu kleiner Nenner macht jede Schwelle leichter erreichbar, und das
ist die Über-Ratifizierungsrichtung (D96).

**`irrevocable_predicates` MUSS `vote@1` und `ratify@1` enthalten.** Ohne den ersten greifen
Widerruf und Supersede nach `01 §5.4` auch auf Stimmen, die Stimmenmenge schrumpft, und die
Auszählung ist nicht mehr monoton — womit D96, D101 und D102 zugleich fallen. Ohne den zweiten kann
eine bereits etablierte Epoche wieder verschwinden, weil ihr einziger Beleg widerrufbar bleibt
(D107). Ein Nukleus ohne beide Deklarationen ist nicht auszählbar (`§3.5`).

**`propose@1` ist ausdrücklich nicht geschützt und wird nicht geprüft.** Eine Stimme zeigt auf den
`proposal_hash`, nie auf den `propose@1`-Claim; dieser dient allein der Auffindbarkeit. Sein
Zustand hat auf keine Auszählung Einfluss, und eine Aktivitätsprüfung auf ihn wäre ein Fehler.

Die Unwiderruflichkeit wird damit **nicht in dieser Schicht definiert**, sondern über den bereits
bestehenden Schutz aus D70/D72 erreicht. Es gibt keine zweite Lesart von „aktiv" neben
`classify()` und `classify_all()`; die Drift, gegen die `T-02.4` gebaut wurde, entsteht hier nicht.

Die Aufnahme von `vote@1` widerspricht D58 nicht. Die Negativliste dort nennt `vouch@1`, und das
Kriterium lautet, ob Fortbestehen die konservative Lesart ist. Eine Stimme gewährt keine
fortdauernde Autorität; sie ist ein einmaliger Akt an einem einzelnen Objekt (D97).

**Epoche (abgeleitet).** Kein Objekt, sondern eine Identität:

```
DOM_NUC_EPOCH = "claim-atom/v1/nucleus-epoch"

epoch_id = SHA-256( DOM_NUC_EPOCH || cbor_deterministic([N, i, constitution_hash]) )
```

`i` ist die Epochennummer, beginnend bei 1. Epoche 1 ist der Genesis:

```
epoch_id_1 = SHA-256( DOM_NUC_EPOCH || cbor_deterministic([N, 1, genesis[4]]) )
```

Die Identität hasht das **Ergebnis**, nie den Beleg (D99). Zwei Mitglieder, die dieselbe
Entscheidung unabhängig materialisieren, erzeugen damit zwei Claims über **dieselbe** Epoche und
keinen Widerspruch.

### 1.2 Was eine Epoche festlegt

Für die Dauer einer Epoche stehen fest: `P`, alle Schwellen, `irrevocable_predicates`, die
Arbitratorenliste — der gesamte Verfassungsinhalt. Eine Auszählung in Epoche `i` rechnet
ausschließlich gegen die Verfassung von `i`.

**Getragene Grenze.** Wer nach der Ratifizierung einer Epoche aufgenommen wird, stimmt erst in der
folgenden Epoche mit. Die Epochenverfassung ist ein Stand, kein Livewert.

---

## 2. Profile

Drei Prädikate. Alle drei sind `nuc:`-gescoped und tragen `N` als Pflichtfeld.

### 2.1 `nuc:N/propose@1`

| Feld | Belegung |
|---|---|
| `I` | ein Element von `P` der laufenden Epoche |
| `N` | `N` des Nukleus |
| `J` | `[object-hash, proposal_hash]` (Tag 3) |
| `v` | leer |

Führt einen Vorschlag ein. Erzeugt für sich keinen Zustand und verdrängt nichts.

### 2.2 `nuc:N/vote@1`

| Feld | Belegung |
|---|---|
| `I` | ein Element von `P` der laufenden Epoche |
| `N` | `N` des Nukleus |
| `J` | `[object-hash, proposal_hash]` (Tag 3) |
| `v` | `{0: choice}` |

`v` Key `0` ist **typ-normativ**: `choice` ist ein `uint`, `0` bedeutet Nein, `1` bedeutet Ja.
Andere Werte sind unbekannt und zählen weder als Ja noch als Nein; sie erzeugen den Vermerk
`UNKNOWN_VOTE_CHOICE`. Weitere Keys sind für spätere Durchgänge reserviert und werden ignoriert.

Es gibt **keinen dritten Wert** für Enthaltung. Wer sich nicht äußert, gibt keine Stimme ab; das
ist von einer Nein-Stimme in der Wirkung nicht unterschieden (`§3.2`), aber in der Diagnose (D94).

### 2.3 `nuc:N/ratify@1`

| Feld | Belegung |
|---|---|
| `I` | ein Element von `P` der laufenden Epoche |
| `N` | `N` des Nukleus |
| `J` | `[object-hash, proposal_hash]` (Tag 3) |
| `v` | `{0: [claim_id, ...]}` — die zählenden Ja-Stimmen |

Materialisiert eine gesättigte Entscheidung (`§4`). Die Zeugenmenge in `v` Key `0` ist ein
**austauschbarer Beleg**, kein Teil der Epochenidentität.

**Kanonizität von `v` (normativ).** `01 §7.1` setzt die Anforderung aus `01 §3` dort durch, wo `v`
gelesen wird. `vote@1` und `ratify@1` sind zwei solche Stellen: die auszählende Schicht dekodiert
`v` und prüft die Re-Serialisierung im selben Zug, in der Form aus Profile-II `§1.3`. Ein Verstoß
erzeugt den Vermerk `NON_CANONICAL_V` und lässt den defekten Teil wegfallen — **nie** einen Reject
und **nie** den Abwesend-Default. Bei `vote@1` zählt die Stimme dann weder als Ja noch als Nein,
wie bei einem unbekannten `choice`; bei `ratify@1` fällt die Zeugenmenge weg, die ohnehin
austauschbarer Beleg ist (D274).

**Wenn `v` sich nicht lesen lässt** (D276). Die Prüfung kennt **vier** Lagen, nicht zwei: `v` ist
abwesend; `v` ist vorhanden und nicht lesbar, weil die Dekodierung **oder** die Re-Serialisierung
scheitert oder das Ergebnis keine Map ist; `v` ist lesbar und nicht kanonisch; `v` ist lesbar und
kanonisch. Zur zweiten Lage gehört auch ein unzulässiger Map-Schlüssel nach Profile-II `§1.3`
(D456). Die zweite Lage ist eigens genannt, weil sie sonst als vierte durchgeht: `h'a2000101ff'`
dekodiert zu einer Map mit Key `0` und Wert `1` und lässt sich nicht re-serialisieren. Wer den
Fehler der Re-Serialisierung abfängt und danach weiterliest, zählt diese Stimme. Ihr Vermerk ist
`UNPARSABLE_V` und nicht `NON_CANONICAL_V`: an ihr ist die Kanonizität nicht entscheidbar, und
Profile-II `§1.3` benennt dieselbe Lage ebenso. Ein abwesendes `v` bleibt davon unberührt und
behält bei `vote@1` den Vermerk `UNKNOWN_VOTE_CHOICE`. Bei `ratify@1` trägt die zweite Lage
ebenfalls `UNPARSABLE_V` und verdrängt `UNSUPPORTED_RATIFICATION` (`§4.1`, D432).

**Lage 2 und Lage 3 überschneiden sich; die Kanonizität geht vor** (D277). Ein `v` kann zugleich
nicht kanonisch und keine Map sein — `h'1801'` etwa, die Zahl `1` in nicht-kürzester Form. Es ist
dann Lage 3 und trägt `NON_CANONICAL_V`, weil die Kanonizität vor der Form geprüft wird, wie in
Profile-II `§1.3`. `h'01'` dagegen ist kanonisch und keine Map: Lage 2, `UNPARSABLE_V`. Die
Aufzählung oben nennt Lage 2 zuerst, weil sie die unauffälligere ist, nicht weil sie zuerst
geprüft würde.

### 2.4 Das Vorschlagsobjekt

Content-adressiert, kein Claim:

```
DOM_NUC_PROPOSAL = "claim-atom/v1/nucleus-proposal"

proposal = {
  0 scope             : N
  1 predecessor       : epoch_id der Vorepoche
  2 constitution_hash : SHA-256(cbor_deterministic(constitution_neu))
}

proposal_hash = SHA-256( DOM_NUC_PROPOSAL || cbor_deterministic(proposal) )
```

Ein Vorschlag ist damit eine **vollständige Verfassungsversion**, nicht eine einzelne
Regeländerung. Das Verfassungsobjekt selbst reist neben dem Vorschlag; wer es nicht hat, kann den
Vorschlag nicht bewerten (`§3.5`).

Der eigene Domänen-Separator verhindert, dass ein `proposal_hash` je mit einem
`constitution_hash`, einer `claim_id` oder einem `epoch_id` kollidiert.

---

## 3. Der Kern-Loop

### 3.1 Welche Stimmen zählen

Eine `vote@1`-Stimme zählt für einen Vorschlag genau dann, wenn alle Bedingungen gelten:

1. `vote.N == scope`
2. `vote.J == (3, proposal_hash)`
3. `wurzel(vote)` nach `02 §2.1` ist Element von `P` — sonst Vermerk `NON_MEMBER_VOTE`
4. `vote.t_exp` ist nicht gesetzt — sonst Vermerk `VOTE_WITH_EXPIRY`
5. `vote.v[0]` ist `0` oder `1` — sonst Vermerk `UNKNOWN_VOTE_CHOICE`
6. Der Claim ist `ACTIVE` nach `classify_all` unter der scope-lokalen Policy (D91). Weil
   `vote@1` nach `§2.1` geschützt ist, führen Widerruf und Supersede hier nie aus `ACTIVE`
   heraus; die Bedingung schließt damit fehlenden Vorgänger, Equivocation und Ablauf aus, nicht
   den Widerruf.

Die Formprüfungen 4 und 5 stehen **vor** der Zustandsprüfung 6. Wirkung identisch, Diagnose
besser: eine abgelaufene Stimme mit gesetztem `t_exp` bekommt so `VOTE_WITH_EXPIRY`, statt lautlos
zu verschwinden (D94, D110).

Zu Bedingung 4: eine Stimme mit Ablaufdatum wäre eine Stimme, die durch Zeitablauf aus der Menge
verschwindet, und genau das darf nicht sein (D97). Sie wird deshalb **ungültig**, nicht still
umgedeutet. Ein Feld, dessen Wert wortlos ignoriert wird, ist die Stummheit, die D95 gekostet hat.

Die Zugehörigkeit des Vorschlags zur Epoche ist **keine Stimmbedingung**, sondern eine Eigenschaft
des Paares aus Epoche und Vorschlag. Sie wird einmal vorweg geprüft (`§3.5`), nicht je Stimme.

Der Ablauf aus Bedingung 5 bleibt trotzdem erreichbar, wenn ein Nukleus `t_exp` über eine
Policy-Maximallaufzeit erzwingt (`02 §6.2`). Ein solcher Nukleus kann keine Stimmen führen; das
ist eine Verfassungsfrage und keine Protokollfrage.

**Zusammengefasst wird je Wurzel** (`02 §2.1`). Ohne Geräte ist die Wurzel der Autor. Stimmen
verschiedener Geräte derselben Wurzel sind Stimmen dieser Wurzel.

**Zwei aktive Stimmen derselben Wurzel mit verschiedener Wahl zählen nicht** — weder die eine
noch die andere. Vermerk `AMBIGUOUS_VOTE`, Subjekt sind alle beteiligten `claim_id`. Die Parallele
ist `02 §2`: trägt kein Gruppenmitglied eine gültige Belegung, entsteht keine Kante. Zwischen zwei
Geräten ohne Verbindung sind Meinungsänderung und Lüge nicht zu unterscheiden; beide zählen nicht,
und beide sind sichtbar (D529 Beschluss 2).

**Mehrere aktive Stimmen derselben Wurzel mit gleicher Wahl zählen einmal** (D530). Die Wurzel
zählt als eine Stimme dieser Wahl, und **jede** dieser Stimmen ist ein gültiger Zeuge nach `§4.1`.
Ein Vermerk entsteht nicht; die Stimmen sagen dasselbe. Sie entstehen, wenn ein Mensch auf einem
Gerät abstimmt, ohne zu wissen, dass er es auf einem anderen schon getan hat.

> **Abgrenzung zu `03`, ausdrücklich.** `membership()` löst mehrere aktive `accept-rules` mit
> `min(claim_id)` auf. Das ist dort richtig, weil alle dasselbe sagen. Zwei Stimmen verschiedener
> Wahl sagen Verschiedenes. Wer das Muster aus `03` überträgt, erzeugt ein Ergebnis aus einer
> Aussage, die niemand gemacht hat (D101). Auch für gleiche Wahl trägt `min(claim_id)` nicht: eine
> Feststellung, die eine andere der gleichen Stimmen zitiert, fiele nach der Reihenfolge zweier
> Hashes (D530 Befund 2).

**Eine bestrittene Stimme zählt nicht** (D532). Hat die Wurzel das Gerät bei einem Endpunkt vor
der Stimme beendet (`02 §2.1`), ist die Stimme nicht zugerechnet; Vermerk `DISPUTED_VOTE`,
Subjekt ihre `claim_id`. Sie fällt vor der Zusammenfassung heraus und macht deshalb auch keine
andere Stimme derselben Wurzel mehrdeutig.

**Ein Verdikt rechnet sie wieder zu** (D533). Eine bestrittene Stimme zählt wie eine
zugerechnete, wenn der Bestand hält:

1. eine `accusation@1` `X` mit `X.N == scope` und `X.J == [claim-ref, claim_id(Stimme)]`, und
2. ein `verdict@1` `V` im Zustand `active`, ohne `t_exp`, mit `V.N == scope`,
   `V.J == [claim-ref, claim_id(X)]`, `V.I` in `arbitration.arbitrators` der **Verfassung dieser
   Epoche** und `v` Key `0 == 1`, und
3. `verdict@1` steht in `irrevocable_predicates` der Verfassung dieser Epoche.

Bedingung 3 ist der Schutz aus D105 und D107 für den Rückweg: ein widerrufbares Verdikt nähme
einer zählenden Stimme durch einen Widerruf die Wirkung, und das schliesst `INV-04.7` aus (D539).
Ob die Anklage `X` selbst noch aktiv ist, zählt nicht; sie zeigt nur, worüber geurteilt wurde.

Nur dieser Pfad zählt. Die Unterwerfung nach Profile-II `§2.4.1` ist widerruflich und wird gegen
`now` geprüft; eine Auszählung, die sie läse, änderte sich mit jedem Widerruf. Hat die Verfassung
keine Schiedsrichter, bleibt die Stimme bestritten: ob es eine Stelle für Kulanz gibt, entscheidet
die Satzung. Ein Schiedsrichter kann ein FROST-Panel sein (Profile-II `§2.2`); ein Gremium des
Vereins ist damit möglich, eine Abstimmung nach dieser Schicht nicht, denn ein Vorschlag ist immer
eine Verfassungsänderung (D534 Befund 3 und 4).

**Kanonizität von `v` in Bedingung 5** (D274). Ist `v` nicht kanonisch kodiert, wird sein Inhalt
gar nicht erst gelesen: Vermerk `NON_CANONICAL_V`, Subjekt die `claim_id` der Stimme, und die
Stimme zählt weder als Ja noch als Nein — an derselben Stelle und mit derselben Wirkung wie ein
unbekanntes `choice` (`§2.3`). Die Prüfung steht damit **vor** der Zusammenfassung nach Autor:
ein Autor mit einer kanonischen und einer nicht-kanonischen Stimme auf denselben Vorschlag
bekommt `NON_CANONICAL_V` und **nicht** `AMBIGUOUS_VOTE`, und seine kanonische Stimme zählt. Das
ist keine Ausnahme von der Regel darüber, sondern ihre Voraussetzung: zwei Stimmen sagen nur dann
Verschiedenes, wenn beide etwas sagen.

### 3.2 Die Auszählung

Sei `n = |P|`, sei `[num, den]` die anzuwendende Schwelle (`§3.4`), seien `Ja` und `Nein` die
Mengen der zählenden Stimmen je Wahl. Alles exakte Integer, keine Division:

```
durchgekommen:   |Ja| * den        >   num * n
gescheitert:     (n - |Nein|) * den   <=   num * n
```

Der Nenner ist `n`, nie `|Ja| + |Nein|`. Wer nicht abstimmt, senkt den Nenner nicht;
Nichtteilnahme wirkt wie Ablehnung. Die Schwelle gilt gegenüber den **Berechtigten**, nicht
gegenüber den Erschienenen.

Beide Mengen wachsen nur (D97), beide Bedingungen sind einmal wahr für immer wahr, und sie
schließen einander aus. Drei Ausnahmen sind benannt und getragen, alle mit sichtbarem Anlass: der
Zwilling einer gegabelten Stimme (D117, `§8`), die Sperre eines Geräts, die eine Stimme bestreitet
(D532), und das Verdikt, das sie wieder zurechnet (D533). Ein Vorschlag scheitert daran, dass
genug Berechtigte ihn ausdrücklich ablehnen — nicht daran, dass eine Frist abgelaufen ist.

### 3.3 Zustände

| Zustand | Bedingung |
|---|---|
| `PASSED` | `durchgekommen` |
| `FAILED` | `gescheitert` |
| `PENDING` | weder noch |
| `UNEVALUABLE` | die Auszählung kann nicht laufen (`§3.5`) |

`PASSED` und `FAILED` sind absorbierend, bis auf die drei Ausnahmen aus `§3.2`. `PENDING` ist die
Voreinstellung und bedeutet, dass weiteres Wissen das Ergebnis noch drehen kann.

Es gibt **kein Zeitfenster und keinen Abschluss**. Eine Abstimmung wird geschlossen, indem eine
Entscheidung materialisiert wird und damit die Epoche wechselt (`§4.3`), nicht indem ein Datum
vergeht. Die Begründung steht in D100: ein Stichtag verlangt Einigkeit darüber, welche Stimmen
davor abgegeben wurden, und die gibt es zwischen zwei Autoren nicht (`01 §5.3`).

### 3.4 Welche Schwelle gilt

Die Klasse wird aus dem **Unterschied** zwischen alter und neuer Verfassung abgeleitet, nicht vom
Vorschlagenden gewählt:

| Unterschied | Klasse |
|---|---|
| ausschließlich `participants` | `membership` |
| alles andere | `amendment` (Index aus `genesis[5]`) |

Die Klasse `ordinary` ist in v1 unbenutzt und für nicht-verfassungsbezogene Entscheidungen
reserviert; die Protokollschicht kennt keine.

**Die Reihenfolge der Klassen ist normativ** und bindet `genesis[5]` an einen Namen in
`thresholds`:

| Index | Klasse |
|---|---|
| `0` | `ordinary` |
| `1` | `membership` |
| `2` | `amendment` |

Fehlt der benannte Schlüssel in `thresholds`, ist der Vorschlag nicht auszählbar (`§3.5`). Ein
Index über `2` ist ebenfalls nicht auszählbar; er wird nicht auf `amendment` zurückgeführt.

**Selbstbezügliche Sperre.** Ändert ein Vorschlag die Schwelle der Klasse, die er selbst aufruft,
gilt das **Maximum** aus alter und neuer Schwelle:

```
angewandt = max( thresholds_alt[klasse], thresholds_neu[klasse] )

Vergleich zweier Ratios exakt:   num_a * den_n   gegen   num_n * den_a
```

Anheben verlangt damit die neue, höhere Schwelle; Senken verlangt die alte, höhere. Eine Fraktion
kann die Hürde nicht unter dem Niveau nehmen, das sie ohnehin überschreiten müsste. Das ist die
h-Regel für den binären Fall.

**Damit ist die Änderungsregel änderbar und trotzdem nicht kaperbar.** Der Satz aus der Vorfassung
— die Änderungsregel sei in v1 unveränderlich, wer sie ändern wolle, forke — entfällt.

### 3.5 Wann die Auszählung nicht läuft

`UNEVALUABLE`, jeweils mit Vermerk, in dieser Reihenfolge geprüft. Die Reihenfolge ist normativ:
sonst erzeugt dieselbe Lage je nach Umsetzung verschiedene Diagnosen.

**Ganz vorweg — die Scope-Zugehörigkeit.** Weicht `proposal.scope` von `epoch.scope` ab, ist das
ein **`ValueError`**, kein Vermerk: ein Vorschlagsobjekt eines fremden Nukleus ist ein
Aufruferfehler und keine Lage der Welt (D82, D92, D112). Dasselbe gilt in `§4.1`.

`Proposal` behauptet mit drei Feldern eine Zugehörigkeit, und alle drei werden geprüft: `scope`
gegen `epoch.scope`, `predecessor` gegen `epoch.epoch_id`, `constitution_hash` gegen das gereichte
Zielobjekt.

**Zuerst die Bindung des Genesis an den Scope** (D145). `decide` MUSS
`SHA-256(DOM_NUC_GEN ‖ cbor(genesis_obj)) == epoch.scope` nachrechnen, **bevor** es ein Feld des
Genesis liest, und bei Abweichung eine Ausnahme werfen statt einen Vermerk zu erzeugen. Die
Asymmetrie zu den Verfassungsobjekten weiter unten ist die aus `03 §1.2`: ein falsches Genesis
ist eine falsche Zuordnung, kein Teilwissen, und für eine falsche Zuordnung gibt es keine sichere
Voreinstellung. Ohne diese Prüfung wählt `genesis[5]` eine Schwellenklasse, die zu keinem Nukleus
gehört.

**Dann die Paarprüfung.**

| Lage | Vermerk |
|---|---|
| `proposal.predecessor != epoch.epoch_id` | `STALE_EPOCH_VOTE`, Subjekt `proposal_hash` |

Ein nicht zusammengehöriges Paar aus Epoche und Vorschlag ist kein Stimmenproblem, und es darf
nicht davon abhängen, ob überhaupt jemand abgestimmt hat: stünde die Prüfung in der Stimmschleife,
liefe eine Auszählung über ein unpassendes Paar **ohne** Stimmen glatt durch und meldete `PENDING`.

**Dann die Objektidentitäten, vor jedem Zugriff auf ihren Inhalt.**

| Lage | Vermerk |
|---|---|
| Verfassung der Epoche fehlt oder ihr Hash passt nicht zu `epoch.constitution_hash` | `CONSTITUTION_UNAVAILABLE` |
| neues Verfassungsobjekt fehlt oder sein Hash passt nicht zu `proposal.constitution_hash` | `PROPOSAL_CONSTITUTION_UNAVAILABLE` |

**Dann der Inhalt.**

| Lage | Vermerk |
|---|---|
| `participants` nicht deklariert | `PARTICIPANTS_UNDECLARED` |
| `participants` formwidrig: kein Array, leer, Eintrag nicht 32 B, unsortiert, Duplikate | `MALFORMED_PARTICIPANTS` |
| `irrevocable_predicates` führt `vote@1` nicht | `VOTE_REVOCABLE` |
| `irrevocable_predicates` führt `ratify@1` nicht | `RATIFY_REVOCABLE` |
| `genesis[6]` ist nicht der uint `0` (Gewichtungsmodus nicht Kopfzahl) | `UNSUPPORTED_WEIGHT_MODE` |
| `genesis[5] > 2`, Schwellenklasse fehlt, oder Schwelle nicht wohlgeformt | `MALFORMED_THRESHOLD` |

**Das Subjekt benennt das Objekt, das die Prüfung zurückweist** (D198). Bei den Zeilen über den
Inhalt einer Verfassung ist das ihr Hash, bei `STALE_EPOCH_VOTE` der `proposal_hash`. Zwei Fälle
sind nicht offensichtlich und werden deshalb ausgeschrieben. Liegt der Fehler in `genesis[5]` oder
`genesis[6]`, ist das Subjekt der **Scope**: der Scope ist der Hash des Genesis und damit die
einzige Adresse, unter der ein Beobachter es holen kann. Und wird die Schwelle in beiden
Verfassungen geprüft, benennt das Subjekt die **zurückgewiesene** — bei der Zielverfassung also
`proposal.constitution_hash`, nicht `epoch.constitution_hash`. Ein Vermerk, der auf ein heiles
Objekt zeigt, schickt den Beobachter an die falsche Stelle, und das ist schlechter als gar keine
Adresse: einer fehlenden folgt er nicht. `findings` ist sortiert und dedupliziert, in der Ordnung
aus `00 §10` (D429).

**Eine leere `participants`-Liste ist formwidrig.** Sie ist sortiert und duplikatfrei und käme
sonst durch; mit `n = 0` wäre jeder Vorschlag sofort `FAILED`, und die Diagnose sagte „abgelehnt",
wo „niemand konnte abstimmen" gemeint ist.

**Wohlgeformtheit einer Schwelle** (D108). Sei `[num, den]` die Schwelle der **angewandten**
Klasse, in beiden Verfassungen geprüft:

```
den >= 1     0 <= num <= den     2 * num >= den
```

Geprüft wird auf den **Rohwerten** beider Verfassungen, bevor irgendeine Umwandlung stattfindet.
Eine Schwelle mit Textwerten muss `MALFORMED_THRESHOLD` ergeben und darf den Aufruf nicht
abreißen (D112).

Die Klasse wird für diese Prüfung gebraucht und **einmal** bestimmt, vor der Validierung. Die
Ableitung der Klasse und die Ermittlung der angewandten Schwelle sind zwei getrennte Schritte;
keiner von beiden wird wiederholt (D113).

Die letzte Bedingung ist die tragende. Seien `A` und `B` disjunkte Ja-Mengen, die beide
durchkommen; dann gilt `|A| * den > num * n` und `|B| * den > num * n`, und mit `|A| + |B| <= n`:

```
n * den   >=   (|A| + |B|) * den   >   2 * num * n        ->        den > 2 * num
```

Zwei disjunkte Ja-Mengen sind also genau dann unmöglich, wenn `2 * num >= den`. Die Grenze ist
nicht strikt — `[1,2]` bleibt zulässig, `[1,3]` nicht. Ohne diese Bedingung fällt D102: zwei
rivalisierende Nachfolger derselben Epoche könnten beide durchkommen, ohne dass jemand doppelt
gestimmt hat.

Die übrigen Bedingungen sind nicht bloß Hygiene: bei `num < 0` vergleicht `reached(0, n, num, den)`
den Ausdruck `0 > num * n` und ist **wahr** — ein Vorschlag wäre `PASSED`, ohne dass eine einzige
Stimme abgegeben wurde.

Geprüft wird ausschließlich die **angewandte** Klasse, nie der gesamte `thresholds`-Eintrag: eine
Verfassung soll nicht daran scheitern, dass ein in v1 unbenutzter Eintrag unglücklich gesetzt ist.

`UNEVALUABLE` ist **nie** `PASSED`. Kein Teilwissen führt zu einer Ratifizierung.

Zur letzten Zeile: `00 §4` Key 6 lässt `weight_mode = 1` weiterhin zu, aber v1 wertet es nicht
aus (D98). Ein Nukleus, der es setzt, bekommt kein Ergebnis statt eines falschen. Verglichen wird
typgenau: ein `false` ist nicht der uint `0` (D456).

---

## 4. Materialisierung und Epochenwechsel

### 4.1 Prüfung eines `ratify@1`

Ein `ratify@1`-Claim etabliert die Folgeepoche genau dann, wenn:

0. `proposal.scope == epoch.scope`, sonst **`ValueError`** (D112). Die Auszählung gehört zu
   **dieser** Epoche und **diesem** Vorschlag. Weicht `tally.epoch_id`
   von `epoch.epoch_id` oder `tally.proposal_hash` von `proposal.proposal_hash` ab, ist das ein
   **`ValueError`**, kein Vermerk: ein fehlzugeordnetes Objekt ist ein Aufruferfehler und keine
   Lage der Welt (D82, D92, D109). Ist `tally.state` gleich `UNEVALUABLE`, entsteht keine Epoche;
   Vermerk `TALLY_UNEVALUABLE` — „ich konnte nicht auswerten", nicht „die Behauptung stimmt nicht".
1. `ratify.N == scope`, `ratify.J == (3, proposal_hash)`, `wurzel(ratify)` nach `02 §2.1` ist
   Element von `P`
2. der Claim ist `ACTIVE`
3. jede `claim_id` in `v[0]` bezeichnet eine Stimme, die nach `§3.1` zählt, mit `choice == 1`
4. keine zwei bezeichnen Stimmen derselben Wurzel
5. die Anzahl der Wurzeln überschreitet die Schwelle nach `§3.2` und `§3.4`
6. die Zielverfassung ist **regierbar**: `participants` ist deklariert und wohlgeformt nach
   `§3.5`, und `irrevocable_predicates` führt `vote@1` und `ratify@1`

Trifft eine Bedingung nicht zu, etabliert der Claim keine Epoche. Er ist deshalb kein Angriff und
kein Protokollverstoß, sondern eine Behauptung, die sich nicht bestätigt.

Zwei Vermerke, weil die Diagnose verschieden ist (D94, D106):

| Lage | Vermerk |
|---|---|
| eine zitierte `claim_id` ist lokal nicht vorhanden | `UNKNOWN_WITNESS_VOTE` |
| ein zitierter Eintrag ist überhaupt keine `claim_id` | `UNSUPPORTED_RATIFICATION` |
| alles Übrige — der Claim ist da und trägt nicht | `UNSUPPORTED_RATIFICATION` |

Die Wirkung ist in allen drei Fällen dieselbe: keine Epoche. Im ersten Fall weiß der Beobachter,
welche `claim_id` er holen muss; in den beiden anderen weiß er, dass Holen nichts nützt.

**Die zweite Zeile stand bis D207 nicht in der Tabelle.** Ein Eintrag, der keine `claim_id` ist,
ist kein Claim, der da wäre und nicht trüge; die dritte Zeile trifft ihn nicht. Er fällt trotzdem
auf `UNSUPPORTED_RATIFICATION`, weil das Kriterium dieser Tabelle die Auskunft an den Beobachter
ist und nicht die Ursache: Holen nützt nichts, weil es nichts zu holen gibt. Das Subjekt ist die
`claim_id` des `ratify@1` — die Zeugenliste ist ein Feld und hat keine eigene Adresse, wie
`genesis[5]` und `genesis[6]` in `§3.5`.

**Nicht-kanonisches `v`** (D274). Ist `v` nicht kanonisch kodiert, fällt die Zeugenmenge weg,
und der Claim etabliert keine Epoche. Der Vermerk ist `NON_CANONICAL_V` und **nicht**
`UNSUPPORTED_RATIFICATION`: das Kriterium dieser Tabelle ist die Auskunft an den Beobachter, und
die Auskunft „das `v` ist nicht kanonisch" enthält „er trägt nicht" bereits und nennt zusätzlich
den Grund. Das Subjekt ist die `claim_id` des `ratify@1`, aus demselben Grund wie in der zweiten
Zeile — die Zeugenliste ist ein Feld und hat keine eigene Adresse.

**Nicht lesbares `v`** (D432). Liegt `v` in der zweiten Lage aus `§2.3`, fällt die Zeugenmenge
ebenso weg, und der Vermerk ist `UNPARSABLE_V`, nicht `UNSUPPORTED_RATIFICATION` — aus demselben
Grund wie beim nicht-kanonischen `v`, mit demselben Subjekt. Ein abwesendes `v` und eine lesbare
Map ohne Zeugenliste unter Key `0` bleiben bei `UNSUPPORTED_RATIFICATION`: dort ist nichts
unlesbar, der Claim trägt nur nicht.

**Bedingung 6 — die Zielverfassung muss regieren können** (D200).

| Lage in der Zielverfassung | Vermerk, Subjekt `proposal.constitution_hash` |
|---|---|
| `participants` nicht deklariert | `PARTICIPANTS_UNDECLARED` |
| `participants` formwidrig nach `§3.5` | `MALFORMED_PARTICIPANTS` |
| `irrevocable_predicates` führt `vote@1` nicht | `VOTE_REVOCABLE` |
| `irrevocable_predicates` führt `ratify@1` nicht | `RATIFY_REVOCABLE` |

Es sind dieselben vier Lagen wie in `§3.5`, dort an der Verfassung der Epoche gemessen, hier an
der Zielverfassung. Das Subjekt benennt nach D198 das zurückgewiesene Objekt, also die
Zielverfassung; die Verfassung der Epoche ist in dieser Lage heil.

**Warum hier und nicht in `§3.5`.** Die Regierbarkeit des Ziels wird für die Auszählung nicht
gebraucht — Klasse und angewandte Schwelle stehen ohne sie fest. Stünde die Prüfung in `§3.5`,
meldete die Auszählung `UNEVALUABLE`, obwohl sie ausgewertet hat: gemessen an der Welt aus D197
drei Ja-Stimmen von drei Mitgliedern gegen die Schwelle `[1,2]`, also `PASSED`. Eine Auszählung,
die `UNEVALUABLE` sagt, wo sie `PASSED` meint, ist eine falsche Adresse, und dafür gilt dieselbe
Begründung wie in D198: einer falschen folgt der Beobachter.

**Warum zuletzt.** Trägt der `ratify@1` schon nach 1 bis 5 nicht, ist der Zustand der
Zielverfassung ohne Belang; ein Vermerk über sie verdeckte dann den Defekt am Claim. Die
Reihenfolge ist aus demselben Grund normativ wie die in `§3.5`.

**Das Zielobjekt gehört zur Auszählung.** Ist `tally.state` nicht `UNEVALUABLE` und trägt das
gereichte Zielobjekt nicht den Hash `proposal.constitution_hash`, ist das ein **`ValueError`** wie
in Bedingung 0: ein fehlzugeordnetes Objekt ist ein Aufruferfehler und keine Lage der Welt. Ohne
diese Bindung prüfte Bedingung 6 eine andere Verfassung als die, über die abgestimmt wurde.

**Was Bedingung 6 nicht leistet.** Sie sperrt die Sackgasse, in der die Zielverfassung nie eine
Auszählung tragen kann. Die `thresholds` der Zielverfassung prüft sie nicht — das tut `§3.5`
bereits, aber nur für die angewandte Klasse, nicht für die Klasse, die ein späterer Übergang
brauchen wird. Eine Zielverfassung ohne `thresholds` der Klasse `membership` bleibt also ein
zulässiges Ziel und sperrt erst den übernächsten Übergang, und zwar nur den einer Klasse. Ob
`§4.1` das mitprüfen soll, ist offen und in D200 benannt.

**Entsteht keine Epoche, trägt das Ergebnis die Vermerke der Auszählung mit** (D203). Sie werden
additiv angehängt, in derselben Form wie bei `TALLY_UNEVALUABLE` (D194): der eigene Vermerk bleibt
stehen, die Verarbeitung ändert sich nicht, `dedupe_sort` führt zusammen. Das gilt für **jeden**
Pfad ohne Folgeepoche, also auch für `UNSUPPORTED_RATIFICATION`, `UNKNOWN_WITNESS_VOTE`,
`RATIFY_WITH_EXPIRY` und Bedingung 6.

Der Grund ist die Adresse. `UNSUPPORTED_RATIFICATION` sagt, dass diese Ratifizierung nicht trägt;
es sagt nicht, warum die Zählung zu kurz ist. Gemessen an vier Teilnehmern mit Schwelle `[2,3]`,
zwei gültigen Ja und einem Ja von jemandem ausserhalb von `participants`: die Auszählung steht auf
`PENDING` und führt `NON_MEMBER_VOTE` mit der `claim_id` der fremden Stimme, die Ratifizierung
zitiert die beiden gültigen und erreicht die Schwelle nicht. Ohne die Weitergabe erfährt der
Beobachter nur die `claim_id` des `ratify@1` — die einzige Stelle, an der nichts zu holen ist.

**Entsteht eine Epoche, werden sie nicht weitergegeben.** Der Übergang hat getragen; was in seiner
Auszählung vermerkt wurde, beantwortet nicht die Frage, die `§4.5` stellt. Diese Grenze ist die aus
`§4.5` und wird hier nicht verschoben.

Die Prüfung ist **offline und vollständig lokal**: wer den Vorschlag, das neue Verfassungsobjekt
und die zitierten Stimmen hat, rechnet das Ergebnis nach, ohne jemanden zu fragen und ohne eine
Uhr zu lesen.

### 4.2 Die Folgeepoche

```
i_neu             = i + 1
constitution_neu  = das Objekt zu proposal[2]
epoch_id_neu      = SHA-256( DOM_NUC_EPOCH || cbor_deterministic([N, i_neu, proposal[2]]) )
```

Zwei `ratify@1`-Claims für denselben Vorschlag ergeben denselben `epoch_id_neu`. Sie sind zwei
Belege für dieselbe Tatsache.

### 4.3 Was der Wechsel erledigt

Mit der Etablierung von `i+1` sind alle Stimmen und alle Vorschläge, deren `predecessor` auf `i`
zeigt, gegenstandslos. Ein Vorschlag, der in `i` nicht durchkam, muss in `i+1` neu eingebracht
werden und behauptet sich dort gegen den geänderten Status quo.

### 4.4 Höchstens ein Ja je Mitglied je Epoche

Ein Mitglied darf in einer Epoche höchstens einen Vorschlag mit `choice == 1` bedenken. Zwei
aktive Ja-Stimmen derselben Wurzel (`02 §2.1`) auf **verschiedene** Vorschläge derselben Epoche
zählen beide nicht; Vermerk `CONFLICTING_APPROVAL`, Subjekt sind alle beteiligten `claim_id`.
Eine bestrittene Stimme zählt dabei nicht mit.

Nein-Stimmen sind unbeschränkt. Gegen mehrere Vorschläge gleichzeitig zu sein ist kohärent; zwei
verschiedene Dokumente gleichzeitig als das geltende zu benennen ist es nicht.

**Diese Regel ist sicherheitstragend, nicht ordnungspolitisch.** Aus ihr folgt, dass zwei
rivalisierende Nachfolger derselben Epoche arithmetisch unmöglich sind. Der Beweis läuft über
dieselbe Schranke wie in `§3.5` — `2 * num >= den` — und zerfällt in zwei Fälle.

**Disjunkte Ja-Mengen** sind bereits durch `§3.5` ausgeschlossen; die Rechnung steht dort.

**Überschneidende Ja-Mengen** schlägt diese Regel. Seien `A` und `B` die Ja-Mengen zweier
Vorschläge derselben Epoche, beide durchgekommen, und sei `S` ihr Schnitt. Nach `§3.5` ist `S`
nicht leer. Jeder Autor in `S` hat zwei aktive Ja-Stimmen auf verschiedene Vorschläge derselben
Epoche; `CONFLICTING_APPROVAL` entfernt ihn aus **beiden** Mengen. Für den Rest von `A` gilt
`|A| - |S| <= n - |B|`, und aus `|B| * den > num * n` folgt `n - |B| < n * (den - num) / den`.
Damit dieser Rest die Schwelle noch erreicht, müsste `den - num > num` gelten, also
`den > 2 * num` — ausgeschlossen. Beide Reste fallen unter die Schwelle.

Nicht „bei einer Schwelle über der Hälfte": die Schranke ist `2 * num >= den`, also **ab** der
Hälfte. Bei `num / den = 1/2` trägt die Aussage trotzdem, weil `durchgekommen` in `§3.2` strikt
vergleicht und `|Ja| * 2 > n` eine echte Mehrheit verlangt.

Ohne diese Regel entstünde genau das Split Brain, das Raft bei nebenläufigen
Konfigurationswechseln beschreibt (D102).

Niemand muss Nein zu A sagen, um Ja zu B sagen zu können, und ein Ja zu A wird B **nicht** als
Nein angerechnet.

**Wenn die Epoche einer fremden Ja-Stimme nicht auflösbar ist.** Die Zugehörigkeit eines
Vorschlags zu einer Epoche steht in `proposal[1]`; ist das Vorschlagsobjekt lokal unbekannt, kann
sie nicht bestimmt werden. Eine aktive Ja-Stimme auf einen unbekannten Vorschlag gilt dann als
**möglicherweise epochengleich** und blockiert die andere Ja-Stimme desselben Autors; Vermerk
`UNKNOWN_PROPOSAL`, Subjekt die `claim_id` der unauflösbaren Stimme.

Die Richtung ist erzwungen, nicht gewählt: die Gegenannahme lässt bei Teilwissen zwei Nachfolger
derselben Epoche entstehen, und das ist die Über-Ratifizierungsrichtung. Geheilt wird der Fall,
indem jemand das Vorschlagsobjekt nachreicht — es ist content-adressiert und damit nicht
fälschbar (D103).

**Die Aussetzung ist nicht epochenlokal.** Eine Auszählung in `i` prüft sämtliche aktiven
Ja-Stimmen eines Autors und kann bei einem unbekannten Vorschlag gerade nicht feststellen, zu
welcher Epoche er gehört. Eine Stimme, die in Wahrheit zu `i+1` gehört, schlägt deshalb auf die
Auszählung in `i` durch. Der Autor ist nicht für eine Epoche ausgesetzt, sondern für jede, die
eine Kettenauflösung nach `§4.5` noch braucht — und das schließt bereits erreichte Epochen ein
(D178).

**Eine Stimme mit nicht-kanonischem `v` ist keine Ja-Stimme** (D274). Sie löst deshalb keinen
Ausschluss nach dieser Regel aus, weder für sich noch für die andere Ja-Stimme ihres Autors;
Vermerk `NON_CANONICAL_V`, Subjekt ihre `claim_id`. Der Vermerk entsteht auch dann, wenn die
Stimme auf einen anderen Vorschlag zeigt als den ausgezählten: er hängt am Lesen von `v` und
nicht am Vorschlag. Das ist die Gegenrichtung zu `UNKNOWN_PROPOSAL` und nur scheinbar
inkonsistent — dort ist die Stimme eine gültige Ja-Stimme mit unbestimmter Epoche, hier ist sie
keine Ja-Stimme.

### 4.5 Die Kette

`§4.1` bis `§4.4` prüfen **einen** Übergang. Welche Epoche gilt, ergibt sich daraus erst, wenn
alle Übergänge nacheinander gelaufen sind. Das leistet `resolve_epoch` (D174):

```
resolve_epoch(store, scope, genesis_obj, known_constitutions, known_proposals, now)
    ->  (epoch, constitution_obj, findings)
```

**Start** ist Epoche 1 nach `§1.1`: `index = 1`, `constitution_hash = genesis[4]`, `N = scope`.
Der übergebene `scope` wird gegen `genesis_obj` geprüft; eine Abweichung ist ein Aufruferfehler
und MUSS werfen, nicht vermerken — dieselbe Asymmetrie wie in `§3.5`.

**Schritt.** Zu einer Epoche `i` sucht die Kette alle aktiven `ratify@1`, deren Vorschlag
`predecessor == epoch_id(i)` trägt, und prüft jede nach `§4.1`. Trägt genau eine, ist `i+1`
erreicht und der Schritt wiederholt sich. Trägt keine, endet die Kette bei `i`.

**Beschaffung.** Verfassungs- und Vorschlagsobjekte kommen als Abbildung vom Hash auf das Objekt.
Jeder Zugriff wird gegen den Schlüssel geprüft: ein Eintrag, dessen Objekt nicht auf seinen
Schlüssel hasht, gilt als **unbekannt**. Der Aufrufer kontrolliert den Inhalt fremder Objekte
nicht; deshalb Vermerk und nicht Ausnahme. Dieselbe Prüfung gilt für `known_proposals` in `§3`
(D175).

**Vermerke.** Die Kette beantwortet, welche Epoche gilt; ihre Vermerke sagen, warum sie dort endet —
nicht, was in einer überholten Epoche geschah. Sie gibt daher ausschließlich die Vermerke der
Prüfungen nach `§4.1` weiter, die auf die **erreichte** Epoche zeigen. Vermerke der Auszählungen
nach `§3` holt sie sich nicht selbst; sie erreichen den Aufrufer nur, soweit `§4.1` sie an ein
Ergebnis **ohne** Folgeepoche angehängt hat (D194, D203). Was in einer Auszählung vermerkt wurde,
deren Übergang getragen hat, fällt damit weg — es beantwortet nicht, warum die Kette dort endet, wo
sie endet. Diese Verwerfung leistet der Neuaufbau der Liste in jedem Schleifenschritt; sie ist keine
Zeile, die man streichen könnte. Ist die Verfassung der erreichten Epoche unbekannt, bleibt das
Ergebnisfeld leer; ein eigener Vermerk wäre dieselbe Auskunft ein zweites Mal.

**Das leere Feld ist nur an Epoche 1 erreichbar.** Die Verfassung von `i+1` ist zugleich das
Zielobjekt des Übergangs von `i` nach `i+1`; fehlt sie, ist die Auszählung nach `§3.5` nicht
auswertbar und der Übergang trägt nicht. Ab Epoche 2 ist das Objekt also notwendig bekannt, sonst
wäre die Epoche nicht erreicht. Nur an Epoche 1 nennt das Genesis einen Hash, dessen Objekt fehlen
darf (D179).

**Ist das Vorschlagsobjekt einer sonst tragenden Ratifizierung unbekannt**, lautet der Vermerk
`EPOCH_PROPOSAL_UNAVAILABLE`, Subjekt der `proposal_hash`. `UNKNOWN_PROPOSAL` aus `§4.4` trägt
hier nicht: dort ist das Subjekt die `claim_id` einer Stimme, hier ein Objekthash, und derselbe
Vermerkstyp mit verschiedenem Subjekttyp ist die falsche Kollision aus D172.

**„Sonst tragend" heißt: vorab nicht widerlegt** (D456). Gemeint sind die Teile von Bedingung 1
aus `§4.1`, die ohne das Vorschlagsobjekt prüfbar sind: `ratify.N == scope`, `ratify.J` trägt
Tag 3, und `ratify.I` ist Element von `P`. Die letzte Prüfung braucht eine bekannte Verfassung der
Epoche mit wohlgeformtem `participants`; fehlt sie, entsteht der Vermerk trotzdem, denn unbekannt
heißt auch hier möglicherweise einschlägig. Ohne diese Vorbedingung hängt jede Identität beliebig
viele Vermerke an die erreichte Epoche, je einen für ein signiertes `ratify@1` auf einen erfundenen
Hash.

Der Vermerk erscheint an der **erreichten** Epoche, obwohl die Epochenzugehörigkeit des fehlenden
Vorschlags gerade unbestimmt ist — sie steht in `proposal[1]`, und genau dieses Objekt fehlt. Die
Richtung ist dieselbe wie in `§4.4`: unbekannt heißt möglicherweise einschlägig, nicht
möglicherweise fremd. Die Gegenannahme würde den Vermerk still fallen lassen, sobald die Kette
weiterläuft, und damit die Auskunft verlieren, dass ein Objekt fehlt (D179).

**Terminierung.** Jeder Übergang braucht mindestens ein `ratify@1`, dessen `J` auf einen Vorschlag
mit `predecessor == epoch_id(i)` zeigt. Beide Felder sind fest, also passt jeder Claim zu genau
einer Epoche; und da `epoch_id` den streng wachsenden Index mithasht, ist jede Epoche der Kette
verschieden. Die Zahl der Schritte ist damit durch die Zahl der `ratify@1` im Speicher begrenzt.
Eine Zyklusprüfung ist **nicht** vorzusehen — anders als bei der Rotationskette in `00 §6.4`, die
autorverkettet ist und zyklisch werden kann.

**Zwei tragende Ratifizierungen auf verschiedene Nachfolger** sind nach `§4.4` unmöglich. Der
Ausgang ist gleichwohl zu definieren: kein Kopf ab `i`, Ergebnis ist `i`, Vermerk `EPOCH_FORK` je
`epoch_id` der beiden Nachfolger (D176). Das ist die Form, die Tendermint für den erkannten Fork
wählt — anhalten und Beweis erzeugen statt wählen — und sie hat wie dort **keinen erreichbaren
Produktivfall**. Ein Test darauf ist ausdrücklich nicht zu bauen; er prüfte eine unmögliche Lage.

---

## 5. Der Nukleus-Akt

Ein Nukleus-Akt ist eine Handlung, die dem Nukleus selbst zugerechnet wird und nicht einem
Menschen. `00 §7` zählt sie auf: `grant-membership@1`, das Verdikt eines Panels, die
Föderationsstimme, die Ratifizierung, `rotate-key@1`.

Es gibt **zwei Pfade**, und `00 §4` Key 7 wählt zwischen ihnen. Beide Pfade waren bisher an drei
Stellen verschieden formuliert; die folgende Zuordnung ist die normative:

| `vote_mode` | Pfad | Autorisierung | Normiert in |
|---|---|---|---|
| `0` | Epochenpfad | die Verfassung der Epoche trägt die Wirkung; jedes Mitglied darf materialisieren | `04 §4` |
| `1` | Schlüsselpfad | `akt.I` ist Element von `resolve_current_key(akt.N)` | `00 §7`, umgesetzt in `03 §4` |

`03 §4` implementiert damit den **Schlüsselpfad**: sein Parameter `authorized_keys` ist die Menge,
die `resolve_authorized_keys` aus dem Anker und den Rotationsketten bildet (`00 §6.4`).
`resolve_current_key` ist darin der Schritt, der je Anker den geltenden Kopf bestimmt — nicht die
ganze Auflösung. Das war nie ausgeschrieben und ist der Grund, aus dem `03 §5` eine Lücke melden
musste.

Beide sind seit `00a` und `00b` gebaut (D160, D161). `resolve_authorized_keys` bekommt den
`constitution_hash` von außen; `§4.5` normiert die Kette, die ihn herleitet, und `resolve_state`
verkettet beides (D183). Wer die Primitive selbst verkettet und eine veraltete Verfassung übergibt,
bekommt ein veraltetes Ergebnis. Bis D462 stand hier, der Anschluss sei nicht gebaut.

---

## 6. Mitgliedschaft

### 6.1 Im Epochenpfad

Mitgliedschaft ist weiterhin die Konjunktion aus fremder Aufnahme und eigener Annahme (D60). Nur
die Herkunft der Aufnahme ändert sich: sie ist kein Claim, sondern ein Eintrag im
Verfassungsobjekt, das der `constitution_hash` adressiert.

```
MEMBER  gdw.  subject ist Element von constitution.participants
        und   eine aktive accept-rules@1 des subject auf genau diesen constitution_hash
```

Beide Konjunkte zeigen damit auf **dasselbe** content-adressierte Objekt. Die vier Zustände aus
`03 §4` bleiben unverändert: fehlt die Annahme, ist der Zustand `GRANT_ONLY`; fehlt die Aufnahme,
`APPLICANT`.

Die eigene Annahme ist keine Formalie. Sie verhindert, dass eine Mehrheit jemandem eine
Mitgliedschaft samt Pflichten zuschreibt, die er nicht eingegangen ist.

### 6.2 Anschluss an `03`

`membership()` bekommt einen zusätzlichen optionalen Parameter:

```
constitution_obj: dict | None = None
```

Ist er gesetzt, prüft die Funktion zuerst `constitution_hash(constitution_obj)` gegen den bereits
vorhandenen Parameter `constitution_hash` und wirft bei Abweichung `ValueError` (D111). Danach
gilt `subject in constitution_obj["participants"]` als zweite Aufnahmequelle neben einer aktiven
`grant-membership@1`. Die `accept-rules`-Strecke bleibt unverändert.

Die Teilnehmerliste wird **nicht** getrennt gereicht. Beide Konjunkte der Mitgliedschaft zeigen so
auf dasselbe content-adressierte Objekt; eine Liste aus einer anderen Epoche kann nicht mit dem
Hash dieser verbunden werden.

Kein neues Prädikat, kein neuer Zustand, keine zweite Mitgliedschaftsfunktion. Zwei Funktionen,
die dasselbe tun, waren die Fehlerform der `03`-Abnahme (D92).

### 6.3 Zwei Fragen, nicht eine

`participants` und Mitgliedschaft beantworten **verschiedene** Fragen. Die Liste bestimmt, **wer
entscheidet** (`§2.1`, `§3.1`); die Annahme bestimmt, **wer gebunden ist** (`§6.1`, D60).

Nach einer Ratifizierung zeigen alle bestehenden `accept-rules@1` auf den **vorigen**
`constitution_hash`, und `03 §4` zählt sie für die neue Version gar nicht. Jedes Mitglied ist
damit `GRANT_ONLY`, bis es die neue Fassung annimmt. **Die Stimmberechtigung bleibt davon
unberührt.**

Das ist beabsichtigt. Verlangte die Stimmberechtigung `MEMBER`, könnte eine Ratifizierung den
Nukleus einfrieren: niemand dürfte abstimmen, bis alle angenommen haben, und wer nie annimmt,
blockierte dauerhaft. Wer eine Änderung ablehnt, behält so die Mittel, sie rückgängig zu machen
(D116).

### 6.4 Aufnahme als Verfassungsänderung

Eine Aufnahme ist damit ein Vorschlag, dessen neue Verfassung sich von der alten ausschließlich in
`participants` unterscheidet — Klasse `membership` nach `§3.4`. Es gibt in v1 kein eigenes
Aufnahmeverfahren.

---

## 7. Verfassungsänderung und Föderation als Belegungen

### 7.1 Verfassungsänderung

Der Loop aus `§3` mit Klasse `amendment` und der selbstbezüglichen Sperre aus `§3.4`. Kein eigener
Mechanismus, keine eigene Prosa. Die Ratifizierung ist `ratify@1`; die Re-Akzeptanz der Mitglieder
ist ihre `accept-rules@1` auf den neuen Hash und entscheidet über ihre eigene Mitgliedschaft in
der Folgeepoche (`§6.1`), nicht über das Zustandekommen der Änderung.

### 7.2 Föderation

Eine Föderation ist ein Nukleus, dessen Mitglieder Nuklei sind: eigener Genesis `N_fed`, eigene,
kleinere Verfassung, derselbe Loop.

Ein Nukleus ist allerdings **kein Graphknoten** — Knoten sind Ed25519-Schlüssel (`02 §2`), ein
Nukleus ist ein Genesis-Hash. Für eine Kopfzahl-Auszählung ist das gleichgültig: `participants`
einer Föderationsverfassung führt je Kind **einen benannten Schlüssel**, mit dem dieses Kind in
dieser Föderation spricht. Er ist von den `nucleus_keys` des Kindes und deren Rotation entkoppelt;
die Föderation löst nichts auf, sondern vergleicht byte-weise wie jede Stimmbedingung (`§3.1`).
Die Föderationsstimme ist deshalb **kein Nukleus-Akt** (D235): sie fällt im fremden Scope `N_fed`,
und `resolve_current_key(N_fed)` nennt die Schlüssel der Föderation, nicht die des Kindes.

**Der Preis steht offen.** Verliert ein Kind diesen Schlüssel, verliert es seine Stimme, bis
`participants` geändert ist; wer ihn behält, obwohl er im Kind-Scope längst abgelöst wurde, stimmt
weiter. Beides folgt aus derselben Bauform wie `arbitration.arbitrators` in `03 §2.4` und ist mit
D235 getragen, nicht übersehen.

**Der Appeal-Pfad ist Opt-in, nicht eingebaut.** Ein Verdikt aus dem Föderations-Scope ist im
Kind-Scope scope-fremd und bindet dort nicht (D81, D92). Es bindet genau dann, wenn die Verfassung
des Kindes das Föderationspanel in `arbitration.arbitrators` führt. Das ist die freiwillige Form
und die einzige, die mit `03` ausdrückbar ist. Die Vorfassung behauptete einen eingebauten Pfad;
das war nicht einlösbar.

Alles Weitere zur Föderation — Losverfahren für Versammlungen, Repräsentationsfairness, Rechtsweg
über mehrere Ebenen — ist Verfassungsinhalt nach `08 §3` und nicht Gegenstand dieser Schicht.

---

## 8. Bewusst getragene Grenzen

- **Ein Vorschlag ist ein Bündel.** Wer nur die Arbitratorenliste ändern will, reicht eine
  vollständige Verfassungsversion ein. Der feinere Weg — Änderungen je Feld mit unabhängiger
  Geltung — bringt Parallelität, erlaubt aber die Teilannahme eines Pakets und braucht eine
  Zerlegung, die niemand gerechnet hat. Grob gebündelt und fein zerlegt sind beide sicher;
  gefährlich ist das Mischen (D101).

- **Vorschläge scheitern oder kommen durch; sie laufen nicht ab.** In einer Epoche, in der nichts
  durchgeht, hängt ein Vorschlag unbegrenzt. Eine Entscheidung bildet damit gesetzte Zustimmung ab
  und nicht, wer an einem bestimmten Tag besser mobilisiert hat.

- **Eine hohe Schwelle bei lauer Beteiligung macht die Verfassung faktisch unveränderlich.** Der
  Nenner ist `|P|`, nicht die Zahl der Abstimmenden. Die Schwelle ist gegen realistische
  Beteiligung zu wählen; das gehört in `example-nucleus.md`, nicht ins Protokoll.

- **Ein feindlicher Eintrag blockiert seine eigene Entfernung.** Wer in `participants` steht,
  stimmt über jede Änderung mit, die ihn herausnähme; der Nenner bleibt `|P|`, und gescheitert ist
  einmal wahr für immer wahr (`§3.2`). Bei Schwelle `1/2` sind dafür `n/2` solcher Einträge nötig,
  bei `2/3` nur `n/3`, bei `3/4` ein Viertel — je strenger die Schwelle, desto leichter die
  Blockade. Ein Stimmverbot des Betroffenen wäre der bekannte Ausweg; er ist mit D236 verworfen,
  weil er den Minderheitenschutz genau dort aufhebt, wo er gebraucht wird. Der Weg bleibt der neue
  Kontext: ein Genesis braucht niemandes Zustimmung.

- **Eine Stimme lässt sich nicht zurücknehmen.** Ohne Frist gibt es kein Fenster, nach dem es
  gleichgültig wäre; ohne Unwiderruflichkeit gibt es keine Monotonie (D97). Wer seine Meinung
  ändert und ein zweites Mal abstimmt, nimmt beiden Stimmen die Wirkung: auf denselben Vorschlag
  nach `§3.1`, als zweites Ja auf einen anderen derselben Epoche nach `§4.4` (D470).

- **Eine Sperre kann eine Stimme bestreiten, auch nach einer Feststellung.** Beendet eine Wurzel
  ein Gerät vor einer Stimme, zählt die Stimme nicht mehr, und eine darauf gestützte Epoche fällt
  wie in D117. Wer so eine bereute Stimme zurückzieht, tut es sichtbar, mit seinem Namen am Ende,
  und der Verein kann darüber urteilen (`§3.1`). Ohne Frist ist „vor der Auszählung“ kein
  Zeitpunkt (D532).

- **Agenda-Macht bleibt, ist aber klein.** Der Vorschlagende wählt den Inhalt. Er wählt weder die
  Wählerschaft noch einen Kantenschnitt noch einen Zweckkontext; all das ist mit dem Snapshot
  entfallen (D96). Wer vorschlagen darf, begrenzt die Verfassung, nicht das Protokoll.

- **Ein zurückgehaltenes Vorschlagsobjekt kann ein Mitglied vorübergehend aussetzen.** Wer eine
  Ja-Stimme auf einen Vorschlag abgibt, dessen Objekt nie verbreitet wird, zählt in dieser Epoche
  nirgends mit (`§4.4`). Das ist die sichere Richtung und heilt, sobald jemand das Objekt
  nachreicht; verhindern kann das Mitglied es nicht.

- **Eine Verfassungsänderung entzieht allen still den `MEMBER`-Status.** Bis jede und jeder die
  neue Fassung angenommen hat, liefert `membership()` `GRANT_ONLY`; alles, was auf `MEMBER` prüft,
  hört so lange auf zu wirken. Kein Fehler, aber eine Rechnung, die vor der ersten Änderung
  bekannt sein muss (D116, `§6.3`).

- **Ein Equivocierender kann eine Epoche kippen — einmal, abwärts, und mit Beweis.** Zwei
  widersprechende Stimmen desselben Autors, an verschiedene Beobachter geschickt, lassen einen
  Beobachter `PASSED` sehen, bevor er den Zwilling kennt. Trifft dieser ein, fällt die Stimme weg
  und eine darauf gestützte Epoche mit ihr. Die Richtung ist stets abwärts, es entsteht nie etwas;
  und der Vorgang hinterlässt einen vom Urheber selbst signierten Beweis, dessen Folgen Layer 05
  regelt (D117).

- **Ein Amendment kann Schutz zurücknehmen.** Lässt eine neue Fassung ein Prädikat aus
  `irrevocable_predicates` weg, wirkt ein Widerruf darauf ab ihr — auch einer, der während des
  Schutzes signiert wurde und bis dahin wirkungslos im Store lag. Erlaubt, weil über den Boden
  (`00 §5.2`) hinaus die Menge Policy ist und Policy änderbar sein muss (`08 §3`). Sichtbar ist die
  Änderung vor jedem `accept-rules@1` am Vergleich der beiden Verfassungsobjekte; das Ventil ist
  die `amendment`-Schwelle und Austritt (D424).

- **Kein Rechtsweg gegen die eigene Mehrheit.** Wer in `P` überstimmt wird, hat innerhalb des
  Nukleus keine Instanz über sich. Das Ventil ist Austritt und, wenn die Verfassung es vorsieht,
  das Föderationspanel (`§7.2`).

- **Vertagt und ausdrücklich nicht in v1:** gewichtete Auszählung (D98), Zweck-Tag am Vouch
  (D56, `02d`), Kettenbindung von Ämtern nach VR-04.1 (D26), das Zeugenquorum für Fristen (D100).
