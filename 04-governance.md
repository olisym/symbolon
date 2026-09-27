# Governance-Schicht — Spezifikation v1

Status: Entwurf · Protokollversion: 1 · Layer: Governance (über Trust-Flow und Profile)

Diese Schicht regelt, wie ein Nukleus seine eigenen Regeln ändert, ohne dass jemand befragt
werden muss, der über ihm steht. Sie fügt kein Atom-Feld hinzu. Vorschläge, Sachanträge und
Verfassungen sind content-adressierte Objekte, auf die Claims zeigen; die Stimmen sind die Claims.

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

**Regelfelder und Sachfelder** (D565). Sechs Felder einer Verfassung sind **Regelfelder**:
`participants` und `thresholds` aus der Tabelle oben, `irrevocable_predicates`, `arbitration`,
`enforcement_policy` und `nucleus_keys` aus `00 §5`. Jedes andere Feld ist ein **Sachfeld**. Die
Liste ist Protokoll, nicht Verfassungsinhalt: ein Feld, das eine Auswertung liest, steht auf ihr,
und es aufzunehmen ändert dieses Dokument. Regelfelder ändert nur ein Vorschlag (`§2.4`), Sachfelder
auch ein Sachantrag (`§2.5`).

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
Arbitratorenliste, also alle Regelfelder. Eine Auszählung in Epoche `i` rechnet ausschließlich gegen
die Verfassung, mit der `i` beginnt; weil ein Sachantrag kein Regelfeld ändert, ist das dieselbe
Rechnung wie gegen jeden Stand von `i`. Sachfelder ändern sich innerhalb der Epoche durch
festgestellte Sachanträge, ohne eine neue Epoche zu etablieren (`§4.6`, D565).

**Getragene Grenze.** Wer nach der Ratifizierung einer Epoche aufgenommen wird, stimmt erst in der
folgenden Epoche mit. Die Epochenverfassung ist fest, kein Livewert.

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
| `v` | `{0: choice}` oder `{0: choice, 1: [claim_id, …]}` |

`v` Key `0` ist **typ-normativ**: `choice` ist ein `uint`, `0` bedeutet Nein, `1` bedeutet Ja.
Andere Werte sind unbekannt und zählen weder als Ja noch als Nein; sie erzeugen den Vermerk
`UNKNOWN_VOTE_CHOICE`.

`v` Key `1` ist optional: eine Liste von `claim_id` früherer Stimmen derselben Wurzel auf denselben
Vorschlag, die diese Stimme **ersetzt** (`§3.1`, D547). Jeder Eintrag ist ein Bytestring der Länge
32. Weitere Keys sind für spätere Durchgänge reserviert und werden ignoriert.

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
  3 motions           : [motion_hash, ...]            optional
}

proposal_hash = SHA-256( DOM_NUC_PROPOSAL || cbor_deterministic(proposal) )
```

Ein Vorschlag ist damit eine **vollständige Verfassungsversion**, nicht eine einzelne Änderung. Er
darf Regelfelder und Sachfelder ändern. Das Verfassungsobjekt selbst reist neben dem Vorschlag; wer
es nicht hat, kann den Vorschlag nicht bewerten (`§3.5`).

**Feld 3** ist die Liste `S` der Sachanträge dieser Epoche, auf denen der Vorschlag aufbaut (D564,
D565): Bytestrings der Länge 32, aufsteigend sortiert, duplikatfrei, nicht leer. Fehlt das Feld, ist
`S` leer; alle Vorschläge ohne Feld 3 behalten damit ihren `proposal_hash`. Eine leere Liste ist
formwidrig, weil sie dasselbe sagte wie das fehlende Feld, unter einem anderen Hash. Formwidrig ist
das Feld auch, wenn es keine Liste ist oder ein Eintrag die Form verfehlt. Wie `S` in die Auszählung
eingeht, sagen `§3.4`, `§3.5` und `§4.4`; wann ein Vorschlag mit `S` trägt, sagt `§4.1`.

Der eigene Domänen-Separator verhindert, dass ein `proposal_hash` je mit einem `constitution_hash`,
einer `claim_id`, einem `epoch_id` oder einem `motion_hash` kollidiert.

### 2.5 Das Sachantragsobjekt

Content-adressiert, kein Claim (D565):

```
DOM_NUC_MOTION = "claim-atom/v1/nucleus-motion"

motion = {
  0 scope       : N
  1 predecessor : epoch_id der Epoche, in der er gilt
  2 changes     : { feldname : [alt, neu], ... }
}

motion_hash = SHA-256( DOM_NUC_MOTION || cbor_deterministic(motion) )
```

Ein Sachantrag ändert Sachfelder der Epoche, in der er gestellt wird, ohne eine neue Epoche zu
etablieren. `alt` und `neu` sind je `[]` für „das Feld fehlt“ oder `[w]` für den Wert `w`; so bleibt
ein fehlendes Feld von einem Feld mit dem Wert `null` unterscheidbar. `alt` ist die
**Vorbedingung**: ein Sachantrag wirkt nur dort, wo jedes seiner Felder diesen Wert hat (`§4.6`).
Eine **Vorbedingung** im Sinn von `§4.4` ist ein Paar aus Feldname und `alt`; ein Sachantrag mit
drei Feldern führt drei. Zusammengehöriges bündelt die Antragstellerin in einem Sachantrag; er wirkt
ganz oder gar nicht (D558).

**Gleichheit von Werten.** Zwei Werte sind gleich, wenn ihre deterministische Kodierung byte-gleich
ist. Die Gleichheit einer Programmiersprache gilt nicht: `1`, `1.0` und `true` sind drei
verschiedene Werte.

**Formwidrig** ist ein Sachantrag, wenn er Schlüssel außer `0`, `1` und `2` führt, `scope` oder
`predecessor` kein Bytestring der Länge 32 ist, `changes` keine Map oder leer ist, ein Feldname kein
Text oder ein Regelfeld ist (`§1.1`), ein Wert keine Liste aus genau zwei Einträgen ist, `alt` oder
`neu` keine Liste der Länge 0 oder 1 ist, oder `alt` und `neu` gleich sind.

- Ein unbekannter Schlüssel ist formwidrig und wird nicht ignoriert: ein späterer Durchgang, der
  dort eine Bedingung einführt, würde sonst von älteren Knoten mit anderer Bedeutung ausgezählt.
- `alt` gleich `neu` ist formwidrig, weil ein Feld, das sich nicht ändert, eine Bedingung ohne
  Änderung wäre und trotzdem jede andere Änderung desselben Felds sperrte (`§4.4`, Regel 2). Ob
  solche Bedingungen gebraucht werden, zeigt der Gebrauch; zulassen lässt sich später, was heute
  formwidrig ist, umgekehrt nicht.

Ein formwidriger Sachantrag ist nicht auszählbar (`§3.5`) und kommt nie durch. Die Form hängt am
Objekt allein, alle Beobachter sehen also dasselbe.

**Welches Objekt ein Claim nennt.** `propose@1`, `vote@1` und `ratify@1` nennen einen Sachantrag wie
einen Vorschlag, mit `J == (3, h)`. Ob `h` einen Vorschlag oder einen Sachantrag nennt, entscheidet
das Objekt: es ist ein Vorschlag, wenn es unter `DOM_NUC_PROPOSAL` auf `h` hasht, ein Sachantrag,
wenn unter `DOM_NUC_MOTION`, sonst unbekannt (`§4.5`, Beschaffung). Die Unterscheidung liegt im
Objekt, nicht im Prädikat; zwei Prädikate wären zwei Stellen, an denen der Schutz aus `§1.1` gelten
muss (D565).

Wo `§3` und `§4` einen Vorschlag auszählen oder feststellen, gilt dasselbe für einen Sachantrag, mit
`motion_hash` an der Stelle von `proposal_hash`. Die Abweichungen stehen in `§3.4`, `§3.5`, `§4.1`
und `§4.4`. Das Register nennt einen Vorschlag auch Regeländerung (D564).

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

**Eine Stimme kann frühere Stimmen derselben Wurzel ersetzen** (D547). Seien die Stimmen einer
Wurzel auf einen Vorschlag die, die nach den Bedingungen 1 bis 6 zählen können und nicht
bestritten sind. Vor der Zusammenfassung fällt jede dieser Stimmen heraus, die von einer anderen
von ihnen in `v` Key `1` genannt wird. Die beiden Regeln darüber gelten für das, was übrig bleibt.
Die genannte Stimme bleibt im Bestand und `ACTIVE`. Sie wird nicht widerrufen, sondern überholt; die
Nennung beweist, dass die neue Stimme nach ihr entstand, ohne Uhr.

- Ein Name, der auf keine solche Stimme zeigt, bleibt ohne Wirkung und ohne Vermerk: eine fremde
  Wurzel, ein anderer Vorschlag, eine Stimme, die nach den Bedingungen oben nicht zählen kann,
  oder eine lokal unbekannte. Eine Stimme, die später eintrifft, ist bei ihrem Eintreffen schon
  ersetzt.
- Zwei Stimmen, die einander nicht nennen, bleiben beide; zwei ersetzende Stimmen zweier Geräte
  mit verschiedener Wahl zählen deshalb nicht, wie jede Doppelstimme.
- Ist Key `1` formwidrig — keine Liste, oder ein Eintrag ist kein Bytestring der Länge 32 —, zählt
  die Stimme, als fehlte Key `1`; Vermerk `MALFORMED_REPLACES`, Subjekt ihre `claim_id`.

**Warum das mit D97 verträglich ist.** Die Menge der Stimmen wächst weiter nur, nichts wird
widerrufen, und keine Uhr wirkt. Eine ersetzende Stimme zählt für ihre Wurzel nie weniger als
dieselbe Stimme ohne Nennung: zählt die Wurzel ohne Nennung eine Wahl, zählt sie mit Nennung
dieselbe. Die Nennung öffnet damit keinen Weg abwärts, den die zweite Stimme nicht schon hat; sie
macht aus einer Meinungsänderung, die beide Stimmen lähmt, eine, die gilt. Wer ein zweites Mal
verschieden stimmt, ohne die erste Stimme zu nennen, lähmt beide wie bisher.

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
schließen einander aus. Die Ausnahmen sind benannt und getragen, alle mit sichtbarem Anlass: der
Zwilling einer gegabelten Stimme (D117, `§8`), eine weitere Stimme derselben Wurzel auf denselben
Vorschlag (`§3.1`, `§8`), eine Stimme, die eine andere ersetzt (`§3.1`, D547), ein Ja derselben
Wurzel, das nach `§4.4` mit ihr unvereinbar ist, die Sperre eines Geräts, die eine Stimme bestreitet
(D532), und das Verdikt, das sie wieder zurechnet (D533). Ein Vorschlag scheitert daran, dass
genug Berechtigte ihn ausdrücklich ablehnen — nicht daran, dass eine Frist abgelaufen ist.

### 3.3 Zustände

| Zustand | Bedingung |
|---|---|
| `PASSED` | `durchgekommen` |
| `FAILED` | `gescheitert` |
| `PENDING` | weder noch |
| `UNEVALUABLE` | die Auszählung kann nicht laufen (`§3.5`) |

`PASSED` und `FAILED` sind absorbierend, bis auf die Ausnahmen aus `§3.2`. `PENDING` ist die
Voreinstellung und bedeutet, dass weiteres Wissen das Ergebnis noch drehen kann.

Es gibt **kein Zeitfenster und keinen Abschluss**. Eine Abstimmung wird geschlossen, indem eine
Entscheidung materialisiert wird und damit die Epoche wechselt (`§4.3`), nicht indem ein Datum
vergeht. Die Begründung steht in D100: ein Stichtag verlangt Einigkeit darüber, welche Stimmen
davor abgegeben wurden, und die gibt es zwischen zwei Autoren nicht (`01 §5.3`).

### 3.4 Welche Schwelle gilt

Die Klasse wird aus der Art des Antrags und dem **Unterschied** zwischen alter und neuer Verfassung
abgeleitet, nicht vom Vorschlagenden gewählt:

| Antrag | Klasse |
|---|---|
| ein Sachantrag (`§2.5`) | `ordinary` |
| ein Vorschlag, Unterschied ausschließlich in `participants` | `membership` |
| ein Vorschlag, alles andere | `amendment` (Index aus `genesis[5]`) |

**Die alte Verfassung eines Vorschlags ist der Stand aus der Verfassung der Epoche und `S`**
(D567): die Verfassung, mit der die Epoche beginnt, nach Anwendung der Sachanträge in `S` wie in
`§4.6`. Gemessen an der Verfassung, mit der die Epoche beginnt, wäre jede Aufnahme nach einem
Sachbeschluss eine Änderung der Klasse `amendment`, denn die neue Verfassung trüge den Sachbeschluss
und die alte nicht. Trägt der Vorschlag, ist dieser Stand der, mit dem die Epoche endet (`§4.4`,
B5); vorher ist er der, den der Vorschlag voraussetzt. Ohne `S` ist er die Verfassung der Epoche.

`ordinary` ist die Klasse der Sachanträge (D565). Die Protokollschicht kennt keine weitere
nicht-verfassungsbezogene Entscheidung.

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

Ein Sachantrag ändert keine Schwelle; die Sperre betrifft ihn nicht.

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
Zielobjekt. Ein Sachantrag behauptet sie mit zwei, `scope` und `predecessor`; ein Zielobjekt hat er
nicht, und `PROPOSAL_CONSTITUTION_UNAVAILABLE` entfällt für ihn.

**Bei einem Sachantrag steht davor seine Form** (D567). Ist er nach `§2.5` formwidrig, ist die
Auszählung `UNEVALUABLE` mit Vermerk `MALFORMED_MOTION`, Subjekt sein `motion_hash`, noch vor der
Scope-Prüfung: ohne die Form sind `scope` und `predecessor` nicht lesbar.

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

**Dann die Form von `S`**, bei einem Vorschlag mit Feld 3:

| Lage | Vermerk |
|---|---|
| Feld 3 formwidrig nach `§2.4` | `MALFORMED_PROPOSAL`, Subjekt `proposal_hash` |

**Dann die Objektidentitäten, vor jedem Zugriff auf ihren Inhalt.**

| Lage | Vermerk |
|---|---|
| Verfassung der Epoche fehlt oder ihr Hash passt nicht zu `epoch.constitution_hash` | `CONSTITUTION_UNAVAILABLE` |
| neues Verfassungsobjekt fehlt oder sein Hash passt nicht zu `proposal.constitution_hash` | `PROPOSAL_CONSTITUTION_UNAVAILABLE` |
| ein Eintrag in `S` ist lokal unbekannt | `MOTION_UNAVAILABLE`, Subjekt der Eintrag |

**Dann die Sachanträge in `S`**, vor dem Inhalt, weil die Klasse den Stand aus `S` braucht
(`§3.4`):

| Lage | Vermerk |
|---|---|
| ein Eintrag ist ein Vorschlag, nicht ein Sachantrag | `MALFORMED_PROPOSAL`, Subjekt `proposal_hash` |
| ein Sachantrag in `S` ist formwidrig nach `§2.5` | `MALFORMED_MOTION`, Subjekt sein `motion_hash` |
| ein Sachantrag in `S` hat anderen `scope` oder `predecessor` als der Vorschlag | `MALFORMED_PROPOSAL`, Subjekt `proposal_hash` |
| zwei Sachanträge in `S` teilen eine Vorbedingung | `MALFORMED_PROPOSAL`, Subjekt `proposal_hash` |

Die letzte Zeile, weil der Stand aus `S` dann nicht eindeutig ist (`§4.4`, B4) und der Vorschlag
nie tragen könnte: nach B3 kommen die beiden nicht zugleich durch, nach B5 braucht er beide. Der
formwidrige Sachantrag in `S` wird nach D198 selbst benannt; er ist das Objekt, das die Prüfung
zurückweist.

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

Geprüft wird auf den **Rohwerten** beider Verfassungen, bevor irgendeine Umwandlung stattfindet. Bei
einem Sachantrag gibt es nur eine: geprüft wird `ordinary` in der Verfassung der Epoche.
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
gestimmt hat. Auf derselben Bedingung stehen die Beweise B1 bis B3 in `§4.4`.

Die übrigen Bedingungen sind nicht bloß Hygiene: bei `num < 0` vergleicht `reached(0, n, num, den)`
den Ausdruck `0 > num * n` und ist **wahr** — ein Vorschlag wäre `PASSED`, ohne dass eine einzige
Stimme abgegeben wurde.

Geprüft wird ausschließlich die **angewandte** Klasse, nie der gesamte `thresholds`-Eintrag: eine
Verfassung soll nicht daran scheitern, dass ein Eintrag, den dieser Antrag nicht braucht,
unglücklich gesetzt ist.

`UNEVALUABLE` ist **nie** `PASSED`. Kein Teilwissen führt zu einer Ratifizierung.

Zur letzten Zeile: `00 §4` Key 6 lässt `weight_mode = 1` weiterhin zu, aber v1 wertet es nicht
aus (D98). Ein Nukleus, der es setzt, bekommt kein Ergebnis statt eines falschen. Verglichen wird
typgenau: ein `false` ist nicht der uint `0` (D456).

---

## 4. Materialisierung und Epochenwechsel

### 4.1 Prüfung eines `ratify@1`

Ein `ratify@1` auf einen Vorschlag etabliert die Folgeepoche; einer auf einen Sachantrag **stellt
ihn fest** und nimmt ihn damit in den Stand der Epoche auf (`§4.6`). Beides genau dann, wenn:

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
6. bei einem Vorschlag: die Zielverfassung ist **regierbar**: `participants` ist deklariert und
   wohlgeformt nach `§3.5`, und `irrevocable_predicates` führt `vote@1` und `ratify@1`
7. bei einem Vorschlag: **jeder Sachantrag in `S` ist festgestellt**, ein `ratify@1` auf ihn trägt
   nach dieser Prüfung

Bei einem Sachantrag entfallen 6 und 7: er hat keine Zielverfassung und kein `S`. Die Prüfung eines
Sachantrags hängt an keiner anderen Feststellung, die Prüfung nach 7 endet also.

Ist der Sachantrag nach `§2.5` formwidrig, ist seine Auszählung `UNEVALUABLE` (`§3.5`), und der
Claim endet mit `TALLY_UNEVALUABLE`. `scope` und `predecessor` des Objekts werden dabei nicht
gelesen, aus demselben Grund wie in `§3.5`: ohne die Form sind sie nicht lesbar (D570).

Trifft eine Bedingung nicht zu, etabliert der Claim keine Epoche und stellt nichts fest. Er ist
deshalb kein Angriff und kein Protokollverstoß, sondern eine Behauptung, die sich nicht bestätigt.

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

**Warum nach 1 bis 5.** Trägt der `ratify@1` schon nach 1 bis 5 nicht, ist der Zustand der
Zielverfassung ohne Belang; ein Vermerk über sie verdeckte dann den Defekt am Claim. Die Reihenfolge
ist aus demselben Grund normativ wie die in `§3.5`.

**Bedingung 7 — was der Vorschlag voraussetzt, muss festgestellt sein** (D564, B5 in `§4.4`).

| Lage | Vermerk |
|---|---|
| ein Sachantrag in `S` ist nicht festgestellt | `MOTION_UNRATIFIED`, Subjekt sein `motion_hash` |

Die Klasse des Vorschlags ist gegen den Stand aus `S` bestimmt (`§3.4`). Trüge er, ohne dass `S`
festgestellt ist, setzte er eine Sachänderung mit der Schwelle seiner Klasse in Kraft, über die als
Sachantrag nie entschieden wurde. Das Subjekt ist der Sachantrag: die Auskunft an den Beobachter
ist, welche Feststellung er holen muss. Die Bedingung steht nach 6, weil sie wie 6 nicht am Claim
hängt, und 6 behält die Nummer, unter der D200 sie führt.

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
`RATIFY_WITH_EXPIRY` und die Bedingungen 6 und 7, und ebenso für eine Feststellung eines
Sachantrags, die nicht trägt.

Der Grund ist die Adresse. `UNSUPPORTED_RATIFICATION` sagt, dass diese Ratifizierung nicht trägt;
es sagt nicht, warum die Zählung zu kurz ist. Gemessen an vier Teilnehmern mit Schwelle `[2,3]`,
zwei gültigen Ja und einem Ja von jemandem ausserhalb von `participants`: die Auszählung steht auf
`PENDING` und führt `NON_MEMBER_VOTE` mit der `claim_id` der fremden Stimme, die Ratifizierung
zitiert die beiden gültigen und erreicht die Schwelle nicht. Ohne die Weitergabe erfährt der
Beobachter nur die `claim_id` des `ratify@1` — die einzige Stelle, an der nichts zu holen ist.

**Entsteht eine Epoche, werden sie nicht weitergegeben.** Der Übergang hat getragen; was in seiner
Auszählung vermerkt wurde, beantwortet nicht die Frage, die `§4.5` stellt. Diese Grenze ist die aus
`§4.5` und wird hier nicht verschoben.

Die Prüfung ist **offline und vollständig lokal**: wer den Vorschlag, das neue Verfassungsobjekt,
die zitierten Stimmen und bei `S` die Sachanträge mit ihren Feststellungen hat, rechnet das Ergebnis
nach, ohne jemanden zu fragen und ohne eine Uhr zu lesen.

### 4.2 Die Folgeepoche

```
i_neu             = i + 1
constitution_neu  = das Objekt zu proposal[2]
epoch_id_neu      = SHA-256( DOM_NUC_EPOCH || cbor_deterministic([N, i_neu, proposal[2]]) )
```

Zwei `ratify@1`-Claims für denselben Vorschlag ergeben denselben `epoch_id_neu`. Sie sind zwei
Belege für dieselbe Tatsache. Zwei für denselben Sachantrag stellen ihn einmal fest.

### 4.3 Was der Wechsel erledigt

Mit der Etablierung von `i+1` sind alle Stimmen, Vorschläge und Sachanträge, deren `predecessor` auf
`i` zeigt, gegenstandslos. Ein Antrag, der in `i` nicht durchkam, muss in `i+1` neu eingebracht
werden und behauptet sich dort gegen den geänderten Status quo.

Der Stand von `i` endet mit ihr. Weiter gilt, was die Verfassung von `i+1` enthält: die
festgestellten Sachanträge sind dann genau die in `S` (`§4.4`, B5), und wieweit die neue Verfassung
sie übernimmt, sagt ihr Unterschied zum Stand aus `S`, der ihre Klasse bestimmt (`§3.4`).

### 4.4 Ja-Stimmen, die einander ausschließen

Ein Mitglied darf in einer Epoche `g` mit `choice == 1` bedenken (D564 Beschluss 3):

1. höchstens **einen Vorschlag** von `g`;
2. je **Vorbedingung** (`§2.5`) höchstens einen Sachantrag von `g`, der sie führt;
3. **nicht zugleich** einen Vorschlag `G` von `g` und einen Sachantrag von `g`, der nicht in `S` von
   `G` steht.

Zwei aktive Ja-Stimmen derselben Wurzel (`02 §2.1`) auf verschiedene Objekte, die zusammen eine
dieser Regeln verletzen, sind **unvereinbar** und zählen beide nicht; Vermerk
`CONFLICTING_APPROVAL`, Subjekt sind alle beteiligten `claim_id`. Eine bestrittene Stimme zählt
dabei nicht mit. Jedes andere Paar ist vereinbar, darunter zwei Ja auf Sachanträge mit verschiedenen
Vorbedingungen und ein Ja auf einen Vorschlag neben einem Ja auf einen Sachantrag in seinem `S`.

- Die Epoche eines Objekts ist sein `predecessor`. Objekte verschiedener Epochen sind stets
  vereinbar.
- Zwei Vorbedingungen sind gleich, wenn Feldname und `alt` nach `§2.5` gleich sind. `[]` ist eine
  Vorbedingung wie jede andere: zwei Sachanträge, die dasselbe fehlende Feld anlegen, teilen sie.
- Ein formwidriger Sachantrag (`§2.5`) kommt bei keinem Beobachter durch; ein Ja auf ihn ist mit
  jedem vereinbar.
- Ist Feld 3 eines Vorschlags formwidrig, gilt für Regel 3 `S` als leer. Der Vorschlag kommt ohnehin
  nicht durch (`§3.5`), und die leere Liste ist die vorsichtige Lesart.

**Ein Vermerk für alle drei Regeln** (D567). Wirkung und Urheber sind dieselben: zwei Ja derselben
Wurzel, die nicht beide gelten können, und beide fallen. Welche Regel greift, lesen Beobachter und
Seite aus den beiden Objekten. Ein eigener Vermerk je Regel wäre eine Aufzählung mehr, der
`INV-04.7` und jede Anzeige folgen müssten, ohne dass ein Beobachter danach anders handelte.

**Eine ersetzte Ja-Stimme zählt für diese Regeln weiter** (D547). Sie bleibt `ACTIVE`, und die
Beweise unten rechnen mit allen aktiven Ja-Stimmen; sie für ersetzte zu lockern bräuchte einen
eigenen. Wer sein Ja auf einen anderen Antrag derselben Epoche verlegen will, kann das deshalb nicht
durch Ersetzen.

Nein-Stimmen sind unbeschränkt. Gegen mehrere Anträge gleichzeitig zu sein ist kohärent; zwei
verschiedene Dokumente gleichzeitig als das geltende zu benennen ist es nicht.

**Diese Regeln sind sicherheitstragend, nicht ordnungspolitisch.** Aus ihnen folgt, dass zwei
rivalisierende Nachfolger derselben Epoche arithmetisch unmöglich sind und dass der Stand einer
Epoche nicht von einer Reihenfolge abhängt. Alle Beweise laufen über dieselbe Schranke wie in
`§3.5`, `2 * num >= den`, und über eine gemeinsame Rechnung.

**Die Rechnung.** Sei `n = |P|` der Epoche. Kommt ein Antrag mit zählender Ja-Menge `A` durch, gilt
`|A| * den > num * n`, und mit `2 * num >= den` folgt `2 * |A| > n`: `A` enthält mehr als die Hälfte
von `P`. Das gilt für jede Klasse, deren Schwelle `§3.5` durchlässt, und alle Anträge einer Epoche
zählen gegen dasselbe `P`, denn `participants` ist ein Regelfeld (`§1.2`). Zwei durchgekommene
Anträge derselben Epoche haben deshalb, gleich welcher Klasse, ein Mitglied, dessen Ja in beiden
zählt. Verletzen diese beiden Ja eine der Regeln, zählt keines von ihnen; der Widerspruch zeigt,
dass die beiden Anträge nicht beide durchgekommen sein können.

- **B1. Höchstens ein Vorschlag von `g` kommt durch.** Die Rechnung mit Regel 1. Das ist der
  bisherige Beweis dieses Abschnitts in kürzerer Form (D102).
- **B2. Ein Vorschlag `G` von `g` und ein Sachantrag von `g`, der nicht in `S` von `G` steht, kommen
  nicht beide durch.** Die Rechnung mit Regel 3.
- **B3. Zwei Sachanträge von `g` mit einer gemeinsamen Vorbedingung kommen nicht beide durch.** Die
  Rechnung mit Regel 2.
- **B4. Der Stand hängt nur von der Menge der festgestellten Sachanträge ab** (`§4.6`). Festgestellt
  heißt durchgekommen (`§4.1`, Bedingung 5). Sind in einem Zwischenstand zwei noch nicht angewandte
  festgestellte Sachanträge zugleich anwendbar, berühren sie verschiedene Felder: ein gemeinsames
  Feld hätte in diesem Zwischenstand einen Wert, beide führten ihn als Vorbedingung, und nach B3
  wäre nur einer durchgekommen. Zwei Sachanträge auf verschiedenen Feldern vertauschen, und jeder
  bleibt anwendbar, wenn der andere angewandt ist. Jeder wird höchstens einmal angewandt, das
  Verfahren endet also. Ein endendes Verfahren, dessen Schritte von jedem Zwischenstand aus wieder
  zusammenlaufen, hat genau ein Ergebnis (Newmans Lemma); die Wahl der Reihenfolge ist gleichgültig.
- **B5. Ein Vorschlag trägt nur, wenn jeder Sachantrag in `S` festgestellt ist** (`§4.1`, Bedingung
  7). Fällt eine solche Feststellung, weil eine ihrer Stimmen nach `INV-04.7` wegfällt, fällt der
  Vorschlag mit, abwärts wie in `§8`. Mit B2 folgt: trägt `G`, sind die festgestellten Sachanträge
  von `g` genau die in `S`. Jeder festgestellte ist durchgekommen und steht nach B2 in `S`; jeder in
  `S` ist nach B5 festgestellt. Der Stand, gegen den `§3.4` die Klasse von `G` bestimmt, ist damit
  der Stand, mit dem `g` endet.

Alle Beweise sprechen über einen Bestand. Zwei Beobachter, von denen jeder nur eine von zwei
unvereinbaren Stimmen kennt, können verschiedene Anträge `PASSED` sehen; treffen ihre Bestände
zusammen, fallen beide, abwärts und mit dem Namen des Autors (`§8`, `INV-04.8`). Das gilt seit D102
für Regel 1 und hier für alle drei.

Nicht „bei einer Schwelle über der Hälfte“: die Schranke ist `2 * num >= den`, also **ab** der
Hälfte. Bei `num / den = 1/2` tragen die Aussagen trotzdem, weil `durchgekommen` in `§3.2` strikt
vergleicht und `|Ja| * 2 > n` eine echte Mehrheit verlangt.

Ohne Regel 1 entstünde genau das Split Brain, das Raft bei nebenläufigen Konfigurationswechseln
beschreibt (D102).

Niemand muss Nein zu A sagen, um Ja zu B sagen zu können, und ein Ja zu A wird B **nicht** als Nein
angerechnet.

**Wenn das Objekt einer fremden Ja-Stimme nicht auflösbar ist.** Epoche, Art und Vorbedingungen
eines Antrags stehen in seinem Objekt; ist es lokal unbekannt, kann keine davon bestimmt werden.
Eine aktive Ja-Stimme auf ein unbekanntes Objekt gilt dann als **möglicherweise unvereinbar** mit
jeder anderen Ja-Stimme desselben Autors und blockiert sie; Vermerk `UNKNOWN_PROPOSAL`, Subjekt die
`claim_id` der unauflösbaren Stimme.

Die Richtung ist erzwungen, nicht gewählt: die Gegenannahme lässt bei Teilwissen zwei Nachfolger
derselben Epoche entstehen, und das ist die Über-Ratifizierungsrichtung. Geheilt wird der Fall,
indem jemand das Objekt nachreicht — es ist content-adressiert und damit nicht fälschbar (D103).

**Die Aussetzung ist nicht epochenlokal.** Eine Auszählung in `i` prüft sämtliche aktiven Ja-Stimmen
eines Autors und kann bei einem unbekannten Objekt gerade nicht feststellen, zu welcher Epoche es
gehört. Eine Stimme, die in Wahrheit zu `i+1` gehört, schlägt deshalb auf die Auszählung in `i`
durch. Der Autor ist nicht für eine Epoche ausgesetzt, sondern für jede, die eine Kettenauflösung
nach `§4.5` noch braucht — und das schließt bereits erreichte Epochen ein (D178).

**Eine Stimme mit nicht-kanonischem `v` ist keine Ja-Stimme** (D274). Sie löst deshalb keinen
Ausschluss nach diesen Regeln aus, weder für sich noch für eine andere Ja-Stimme ihres Autors;
Vermerk `NON_CANONICAL_V`, Subjekt ihre `claim_id`. Der Vermerk entsteht auch dann, wenn die Stimme
auf ein anderes Objekt zeigt als das ausgezählte: er hängt am Lesen von `v` und nicht am Antrag. Das
ist die Gegenrichtung zu `UNKNOWN_PROPOSAL` und nur scheinbar inkonsistent — dort ist die Stimme
eine gültige Ja-Stimme mit unbestimmter Epoche, hier ist sie keine Ja-Stimme.

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

**Schritt.** Zu einer Epoche `i` sucht die Kette alle aktiven `ratify@1`, deren Objekt ein Vorschlag
von `i` ist, und prüft jede nach `§4.1`. Trägt genau eine, ist `i+1` erreicht und der Schritt
wiederholt sich. Trägt keine, endet die Kette bei `i`. Feststellungen von Sachanträgen führen zu
keiner Epoche; sie bilden den Stand (`§4.6`) und gehen in die Kette nur über Bedingung 7 ein. Der
Schritt prüft deshalb vor den Vorschlägen die Feststellungen aller Sachanträge von `i` nach `§4.1`;
die festgestellten sind die Menge, gegen die Bedingung 7 prüft. Deren Vermerke gehören nicht zum
Ergebnis der Kette, sondern zu `resolve_stand` (`§4.6`, D570).

**Welche Objekte zu `i` gehören** (D571, D572). Ein Vorschlag oder Sachantrag gehört zu `i`, wenn
sein `scope` der Scope der Kette und sein `predecessor` der `epoch_id` von `i` ist. Ein Sachantrag,
dessen Objekt keine Map ist, nennt keine Epoche und gehört zu keiner. Ein Objekt mit fremdem `scope`
wird übergangen, ohne Vermerk: ausgezählt wäre es nach `§3.5` ein Aufruferfehler, und ein signiertes
`ratify@1` auf ein solches Objekt dürfte die Kette nicht zum Werfen bringen.

**Beschaffung.** Verfassungsobjekte kommen als Abbildung vom Hash auf das Objekt, Vorschlags- und
Sachantragsobjekte als eine zweite. Jeder Zugriff wird gegen den Schlüssel geprüft: ein Eintrag,
dessen Objekt nicht auf seinen Schlüssel hasht, gilt als **unbekannt**. In der zweiten Abbildung
entscheidet der Domänen-Separator, unter dem ein Objekt auf seinen Schlüssel hasht, ob es ein
Vorschlag oder ein Sachantrag ist (`§2.5`). Der Aufrufer kontrolliert den Inhalt fremder Objekte
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

**Ist das Objekt einer sonst tragenden Ratifizierung unbekannt**, lautet der Vermerk
`EPOCH_PROPOSAL_UNAVAILABLE`, Subjekt der Hash unter `J`. Ob das Objekt ein Vorschlag oder ein
Sachantrag wäre, ist gerade nicht bestimmbar. `UNKNOWN_PROPOSAL` aus `§4.4` trägt
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

### 4.6 Der Stand einer Epoche

Der **Stand** einer Epoche `g` ist die Verfassung, mit der `g` beginnt, nach Anwendung ihrer
festgestellten Sachanträge (D564 Beschluss 2). Festgestellt ist ein Sachantrag von `g`, wenn ein
`ratify@1` auf ihn nach `§4.1` trägt.

**Anwenden.** Ein Zwischenstand ist eine Verfassung; der Wert eines Felds ist `[]`, wenn es fehlt,
sonst `[w]`. Ein Sachantrag ist in einem Zwischenstand anwendbar, wenn er noch nicht angewandt ist
und jedes seiner Felder dort den Wert `alt` hat (Gleichheit nach `§2.5`). Angewandt setzt er jedes
seiner Felder auf `neu`: `[w]` setzt den Wert `w`, `[]` entfernt das Feld. Solange ein
festgestellter Sachantrag anwendbar ist, wird einer angewandt, gleich welcher, jeder höchstens
einmal. Das Ergebnis ist der Stand. Nach B4 (`§4.4`) hängt er nicht von der Wahl ab. Eine
Reihenfolge hat der Stand nicht, und keine Rechnung darf eine voraussetzen.

**Ein festgestellter Sachantrag, dessen Vorbedingung nicht eintritt,** bleibt ohne Wirkung und
bleibt festgestellt. Er ist kein Fehler und trägt keinen Vermerk: ein später festgestellter
Sachantrag kann seine Vorbedingung herstellen, und dann wird er angewandt. Dass sie nie eintritt,
lässt sich innerhalb der Epoche nicht feststellen; mit ihrem Ende wird er gegenstandslos (`§4.3`).
Welche festgestellten Sachanträge angewandt sind, gehört deshalb zum Ergebnis.

**Der Stand wächst.** Kommt ein festgestellter Sachantrag hinzu, bleibt jeder bisher angewandte
angewandt: die bisherige Folge von Anwendungen ist weiter zulässig, und nach B4 ist das Ergebnis
jeder zulässigen Folge dasselbe. Der Stand schrumpft nur, wenn eine Feststellung fällt, und das
nur aus den Gründen, aus denen nach `INV-04.8` eine Epoche fällt.

**Der Stand ist keine Epoche** (D565 Beschluss 3). Er hat keinen `epoch_id`, und eine Annahme
nach `03 §4` bindet weiter an die Verfassung, mit der die Epoche beginnt: wer sie annimmt, nimmt das
Verfahren an, mit dem ihre Sachfelder sich ändern. Ein festgestellter Sachantrag verlangt keine neue
Annahme. Eine Kette über Zwischenstände der Sachanträge ist verworfen: je nach Reihenfolge der
Feststellungen entstünden verschiedene Kennungen, und zwei Beobachter sähen zeitweise eine Gabel
(D564).

**Die Schnittstelle.**

```
resolve_stand(store, epoch, genesis_obj, constitution_obj, known_proposals, now)
    ->  (stand_obj, applied, findings)
```

`epoch` und `constitution_obj` sind das Ergebnis von `resolve_epoch` (`§4.5`); `genesis_obj` braucht
die Auszählung (`§3.5`, D570). Ist `constitution_obj` leer, ist auch `stand_obj` leer. `applied`
ist die aufsteigend sortierte Liste der `motion_hash` der angewandten Sachanträge. `findings` sind
die Vermerke der Prüfungen nach `§4.1` an Feststellungen von Sachanträgen dieser Epoche, die nicht
tragen, in der Form aus `§4.5`: ist ein Sachantrag festgestellt, fallen die Vermerke seiner übrigen
Feststellungen weg. Ein unbekanntes Objekt unter einer Feststellung meldet schon die Kette
(`EPOCH_PROPOSAL_UNAVAILABLE`); hier erscheint es nicht ein zweites Mal.

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

Nach der Ratifizierung eines Vorschlags zeigen alle bestehenden `accept-rules@1` auf den **vorigen**
`constitution_hash`, und `03 §4` zählt sie für die neue Version gar nicht. Jedes Mitglied ist damit
`GRANT_ONLY`, bis es die neue Verfassung annimmt. **Die Stimmberechtigung bleibt davon unberührt.**
Ein festgestellter Sachantrag ändert keinen Hash, auf den eine Annahme zeigt (`§4.6`).

Das ist beabsichtigt. Verlangte die Stimmberechtigung `MEMBER`, könnte eine Ratifizierung den
Nukleus einfrieren: niemand dürfte abstimmen, bis alle angenommen haben, und wer nie annimmt,
blockierte dauerhaft. Wer eine Änderung ablehnt, behält so die Mittel, sie rückgängig zu machen
(D116).

### 6.4 Aufnahme als Verfassungsänderung

Eine Aufnahme ist damit ein Vorschlag, dessen neue Verfassung sich vom Stand aus der
Verfassung der Epoche und `S` ausschließlich in `participants` unterscheidet — Klasse `membership`
nach `§3.4`. Es gibt in v1 kein eigenes Aufnahmeverfahren. Aufnahmen laufen deshalb nacheinander:
unter einer Epoche kommt höchstens ein Vorschlag durch (`§4.4`, B1; D564 Beschluss 1).

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

- **Ein Vorschlag ist ein Bündel, ein Sachantrag auch.** Wer nur die Arbitratorenliste ändern will,
  reicht eine vollständige Verfassungsversion ein; Regelfelder ändert nur ein Vorschlag. Sachfelder
  ändern auch Sachanträge, nebeneinander und je ganz oder gar nicht. Das Mischen, vor dem D101
  warnt, macht die Vorbedingung sicher: zwei Änderungen desselben Felds aus demselben Wert schließen
  einander aus (`§4.4`, Regel 2), ein Vorschlag nennt in `S`, worauf er aufbaut (Regel 3), und die
  Stand hängt von keiner Reihenfolge ab (`§4.6`). Eine Teilannahme gibt es nicht; wer zwei Felder
  zusammen ändern will, bündelt sie (D564).

- **Regeländerungen laufen nacheinander, Aufnahmen eingeschlossen.** Unter einer Epoche kommt
  höchstens ein Vorschlag durch (`§4.4`, B1). Mehrere Aufnahmen nebeneinander brauchten einen
  Nenner, der mitläuft, und der bricht die Rechnung aus `§4.4` (D564 Befund 2 und 3). Wer mehrere
  Personen zugleich aufnehmen will, nimmt sie in einem Vorschlag auf.

- **Ein Ja auf einen Vorschlag legt fest, welchen Sachanträgen man noch zustimmen kann.** Ein Ja auf
  einen Sachantrag derselben Epoche, der nicht in `S` steht, nimmt beiden Ja die Wirkung (`§4.4`,
  Regel 3), auch wenn es später kommt; ein erreichtes `PASSED` kann dadurch fallen wie durch jede
  unvereinbare Stimme. Wer einen Vorschlag unterstützt, stimmt neuen Sachanträgen erst in der
  Folgeepoche zu.

- **Zwischen zwei Sachanträgen auf dasselbe Feld gibt es keine Stichfrage.** Wer zwischen zwei neuen
  Werten für dasselbe Feld wählen will, stimmt einem zu; ein zweites Ja nimmt beiden die Wirkung
  (`§4.4`, Regel 2). Kommt keiner durch, bleibt der Wert. Eine Stichfrage bräuchte einen eigenen
  Beweis (D564 Beschluss 3).

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

- **Eine Stimme lässt sich nicht zurücknehmen, aber ersetzen.** Ohne Frist gibt es kein Fenster,
  nach dem es gleichgültig wäre; ohne Unwiderruflichkeit gibt es keine Monotonie (D97). Wer seine
  Meinung ändert und ein zweites Mal abstimmt, ohne die erste Stimme zu nennen, nimmt beiden die
  Wirkung: auf denselben Vorschlag nach `§3.1`, als Ja, das mit dem ersten unvereinbar ist, nach
  `§4.4` (D470). Nennt die zweite Stimme die erste, ersetzt sie sie auf demselben Vorschlag
  (`§3.1`, D547); ein erreichtes `PASSED` kann dadurch fallen wie durch die bloße zweite Stimme,
  nicht öfter.

- **Eine Sperre kann eine Stimme bestreiten, auch nach einer Feststellung.** Beendet eine Wurzel
  ein Gerät vor einer Stimme, zählt die Stimme nicht mehr, und eine darauf gestützte Epoche fällt
  wie in D117. Wer so eine bereute Stimme zurückzieht, tut es sichtbar, mit seinem Namen am Ende,
  und der Verein kann darüber urteilen (`§3.1`). Ohne Frist ist „vor der Auszählung“ kein
  Zeitpunkt (D532).

- **Agenda-Macht bleibt, ist aber klein.** Der Vorschlagende wählt den Inhalt. Er wählt weder die
  Wählerschaft noch einen Kantenschnitt noch einen Zweckkontext; all das ist mit dem Snapshot
  entfallen (D96). Wer vorschlagen darf, begrenzt die Verfassung, nicht das Protokoll.

- **Ein zurückgehaltenes Objekt kann ein Mitglied vorübergehend aussetzen.** Wer eine Ja-Stimme auf
  einen Vorschlag oder Sachantrag abgibt, dessen Objekt nie verbreitet wird, zählt in dieser Epoche
  nirgends mit (`§4.4`). Das ist die sichere Richtung und heilt, sobald jemand das Objekt
  nachreicht; verhindern kann das Mitglied es nicht.

- **Eine Verfassungsänderung entzieht allen still den `MEMBER`-Status.** Bis jede und jeder die neue
  Verfassung angenommen hat, liefert `membership()` `GRANT_ONLY`; alles, was auf `MEMBER` prüft,
  hört so lange auf zu wirken. Kein Fehler, aber eine Rechnung, die vor der ersten Änderung bekannt
  sein muss (D116, `§6.3`). Ein festgestellter Sachantrag tut das nicht (`§4.6`).

- **Ein Equivocierender kann eine Epoche kippen — einmal, abwärts, und mit Beweis.** Zwei
  widersprechende Stimmen desselben Autors, an verschiedene Beobachter geschickt, lassen einen
  Beobachter `PASSED` sehen, bevor er den Zwilling kennt. Trifft dieser ein, fällt die Stimme weg
  und eine darauf gestützte Epoche mit ihr. Die Richtung ist stets abwärts, es entsteht nie etwas;
  und der Vorgang hinterlässt einen vom Urheber selbst signierten Beweis, dessen Folgen Layer 05
  regelt (D117).

- **Ein Amendment kann Schutz zurücknehmen.** Lässt eine neue Verfassung ein Prädikat aus
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
