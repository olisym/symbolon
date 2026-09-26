# Szenario — der Verein

Phase 1 der Roadmap (`ROADMAP.md §3`), beschlossen mit D468. Ein kleiner Sportverein, eine
Laufgruppe mit vier Menschen: beitreten mit Bürgschaft, die Satzung ändern, den Beitrag zahlen und
quittieren. Dazu der Moment, für den das Ganze da ist: jemand erzählt zwei Leuten Verschiedenes,
und alle halten danach seinen eigenen Beweis in der Hand.

Dies ist **kein Spec-Layer.** Es beschreibt, welche Claims entstehen, wer sie unterschreibt, was
jeder Rechner daraus macht und was ein Bildschirm zeigt. Normativ sind die Layer, auf die es zeigt.
Was dabei fehlte oder umständlich war, steht in `§8` und im Register.

---

## 1. Warum auf dem Beispielnukleus

Der Verein beginnt nicht bei null. `example-nucleus.md` hat drei Gründer, zwei Scopes und die
Aufnahme einer Vierten, byte-genau gerechnet und von `tools/example_nucleus.py` gegen die
Implementierung geprüft. Der Verein übernimmt das unverändert (D468 Beschluss 1): dieselben
Identitäten, dieselben Hashes, dieselbe Aufnahme. Neu sind die Bürgschaft vor der Aufnahme, die
Satzungsänderung, der Beitrag und die Gabelung.

Die neuen Objekte rechnet `tools/verein.py` mit demselben Werkzeug und prüft dabei jeden Zustand
aus diesem Dokument (D472). Ihre Hashes stehen in `§9`, aus der Ausgabe des Laufs kopiert.

---

## 2. Wer beteiligt ist

**Menschen.** Anna, Bruno und Chris gründen die Laufgruppe. Dora kommt dazu. Chris ist
Kassenwartin.

| Name | Seed | öffentlicher Schlüssel | Rolle |
|---|---|---|---|
| ANNA | `0x11×32` | `d04ab232…` | Gründerin, Wurzel beider Scopes |
| BRUNO | `0x12×32` | `204040e3…` | Gründer, Wurzel beider Scopes |
| CHRIS | `0x13×32` | `66cd608b…` | Mitglied, Kassenwartin |
| DORA | `0x14×32` | `20828bf5…` | neu |
| KASSE | `0x15×32` | `d54207da194977dcf46adbfec2bc2e75b52d5a8a42184fedfdc00024f0e3e8da` | Gläubigerin der Beiträge |

Die ersten vier stehen vollständig in `example-nucleus §2`. KASSE ist neu (D468 Beschluss 2): eine
eigene Identität, deren Schlüssel Chris auf ihrem Gerät hält. Sie ist kein Mitglied und stimmt
nicht ab; sie quittiert.

**Zwei Scopes**, wie `00 §4.2` empfiehlt und `example-nucleus §3` und `example-nucleus §4` rechnen:

- **`N_gov`, der Verein.** Hier stehen die Satzung, die Mitgliederliste, die Stimmen. Er regiert
  genau eine Sache: sich selbst.
- **`N_res`, das Vereinsleben.** Hier stehen Bürgschaften, Beiträge, Quittungen. Keine Abstimmung,
  keine Mitgliederliste.

Auf dem Bildschirm heißt der erste „Verein“, der zweite „Konto und Vertrauen“. Wer beides sieht,
merkt nicht, dass es zwei Scopes sind; die Trennung zeigt sich erst, wenn sich der Verein spaltet
(`example-nucleus §6`).

**Stand zu Beginn.** Epoche 1, drei Mitglieder, alle Schwellen `[1,2]`. Im Vereinsleben bürgen Anna
und Bruno füreinander und für Chris, jede Bürgschaft mit `n = 50` (`example-nucleus §7`). Anna und
Bruno haben damit ihr ganzes Budget `D = 100` ausgegeben, Chris hat noch nichts ausgegeben.

---

## 3. Mitglied werden

Dora will mitlaufen. Chris kennt sie und bürgt für sie. Anna beantragt die Aufnahme, Bruno ist
dagegen, Chris dafür.

| # | Wer unterschreibt | Scope | Claim | Inhalt |
|---|---|---|---|---|
| V1 | CHRIS | `N_res` | `vouch@1` | `J = [1, DORA]`, `v = {0: 50}` |
| V2 | ANNA | `N_gov` | `propose@1` | Aufnahme, Vorschlag aus `example-nucleus §5` |
| V3 | ANNA | `N_gov` | `vote@1` | Ja |
| V4 | BRUNO | `N_gov` | `vote@1` | Nein |
| V5 | CHRIS | `N_gov` | `vote@1` | Ja |
| V6 | ANNA | `N_gov` | `ratify@1` | Zeugen V3 und V5 |
| V7 | DORA | `N_gov` | `accept-rules@1` | auf `constitution_hash_2` |
| V8–V10 | ANNA, BRUNO, CHRIS | `N_gov` | `accept-rules@1` | auf `constitution_hash_2` |

V2 bis V7 sind `example-nucleus §7` Nummer 4 bis 9. V1 und V8 bis V10 sind neu.

**Warum Chris bürgt und nicht Anna.** Die Schranke `Σ n ≤ D` gilt je Bürge (`02 §3.1`). Anna steht
bei 100 von 100. Jede weitere Bürgschaft, auch mit `n = 1`, brächte sie auf 101, und dann fielen
**alle** ihre Bürgschaften aus, nicht nur die neue (`OVERCOMMITTED_AUTHOR`, `example-nucleus §8.1`).
Wer bürgen will, muss vorher eine bestehende Bürgschaft verkleinern. Chris hat Budget frei.

Nach V1 steht Dora in Distanz 2 zum Anker: `C(DORA) = ⌊100 · (1/2)²⌋ = 25`. Die Kante von Chris
trägt `⌊C(CHRIS) · n / D⌋ = ⌊50 · 50 / 100⌋ = 25`.

**Die Abstimmung.** Klasse `membership`, weil sich die Satzungen nur in der Mitgliederliste
unterscheiden (`04 §3.4`). Bei `n = 3` und `[1,2]` genügen zwei Ja: nach V3 und V4 steht es
`PENDING`, nach V5 `PASSED`. V6 schreibt das fest; jeder Rechner, der V3 bis V6 und die beiden
Satzungen hat, kommt auf Epoche 2 (`04 §4.5`).

**Was jeder Rechner danach rechnet.** Stimmberechtigt sind vier (`participants`). Gebunden an die
geltende Satzung ist zunächst niemand: Doras Annahme fehlt noch, und die Annahmen der drei anderen
zeigen auf die alte Fassung. Nach V7 ist Dora `MEMBER`, nach V8 bis V10 auch die übrigen
(`04 §6.1`, `04 §6.3`).

**Was die Bildschirme zeigen.**

- Anna, Bruno, Chris, beim Antrag: „Dora möchte aufgenommen werden. Chris bürgt für sie.“ Die
  Bürgschaft steht neben dem Antrag, obwohl sie in einem anderen Scope liegt; das Protokoll
  verknüpft beides nicht, der Bildschirm tut es (D468 Beschluss 4).
- Alle, während der Abstimmung: „1 Ja, 1 Nein, 2 von 3 nötig.“
- Dora, nach V6: „Du bist aufgenommen. Bestätige die Satzung, um Mitglied zu sein.“
- Anna, Bruno, Chris, nach V6: „Die Mitgliederliste hat sich geändert. Bestätige die Satzung neu.“
  Das ist eine Aufgabe, keine Warnung. Abstimmen können sie auch ohne sie (D468 Beschluss 3).
- Anna, wenn sie für Dora bürgen will: „Dein Budget ist voll. Verkleinere zuerst eine Bürgschaft.“

---

## 4. Die Satzung ändert sich

Die Laufgruppe braucht Geld für Startgebühren. Anna beantragt, einen Jahresbeitrag in die Satzung
aufzunehmen.

Die neue Fassung `constitution_3` ist `constitution_2` mit einem zusätzlichen Feld `beitrag`, einem
Text: „24 Euro im Jahr, fällig im Januar, an die Kasse“. Das Feld ist opak (`00 §5`); kein Rechner
liest es. Es steht dort, damit jeder, der die Satzung annimmt, weiß, wozu er Ja sagt.

| # | Wer unterschreibt | Scope | Claim | Inhalt |
|---|---|---|---|---|
| V11 | ANNA | `N_gov` | `propose@1` | Vorgänger Epoche 2, Ziel `constitution_3` |
| V12–V14 | Mitglieder | `N_gov` | `vote@1` | je Ja oder Nein |
| V15 | ein Mitglied | `N_gov` | `ratify@1` | Zeugen die zählenden Ja |
| V16–V19 | alle vier | `N_gov` | `accept-rules@1` | auf `constitution_3` |

**Die Rechnung.** Klasse `amendment`, weil sich mehr als die Mitgliederliste ändert. Die Schwelle
ist das Maximum aus alter und neuer, hier beide `[1,2]` (`04 §3.4`). Mit vier Berechtigten:

```
n = 4,  [num, den] = [1, 2]

durchgekommen:   |Ja| · 2  >  4            ->   |Ja| >= 3
gescheitert:     (4 − |Nein|) · 2  <=  4   ->   |Nein| >= 2
```

| Ja | Nein | Zustand |
|---|---|---|
| 2 | 0 | `PENDING` |
| 2 | 1 | `PENDING` |
| 2 | 2 | **`FAILED`** — endgültig, nicht offen |
| 3 | 0 oder 1 | **`PASSED`** |

Ein Gleichstand von zwei zu zwei ist gescheitert. Der Nenner ist die Zahl der Berechtigten, nicht
die der Abstimmenden (`04 §3.2`): wer nicht abstimmt, wirkt wie ein Nein, und bei vier Mitgliedern
braucht jede Änderung drei.

**Was die Bildschirme zeigen.** Den Antrag mit beiden Fassungen nebeneinander und dem Unterschied
hervorgehoben; den Stand „2 Ja, 0 Nein, 3 von 4 nötig“; nach der Ratifizierung bei allen vieren die
Aufgabe „Die Satzung hat sich geändert: neuer Beitrag. Bestätigen?“. Wer nicht bestätigt, ist an
die neue Fassung nicht gebunden und bleibt stimmberechtigt (`04 §6.3`).

---

## 5. Die Doppelstimme

Dora ist in dieser Woche nicht erreichbar und stimmt nicht ab. Anna und Chris sagen Ja. Es kommt
also auf Bruno an.

### 5.1 Nacheinander

Bruno stimmt Ja und besinnt sich, am nächsten Tag stimmt er Nein. Beide Stimmen hängen
nacheinander in seiner Kette. Das Nein nennt das Ja in `v` Key `1`, wie jede Stimme, die die Seite
unterschreibt (D548), und ersetzt es: Bruno zählt als Nein, sein Ja ist weg, der Antrag steht bei
`PENDING`. Nennt die zweite Stimme die erste nicht, zählt die Auszählung **keine** von beiden und
vermerkt `AMBIGUOUS_VOTE` mit beiden `claim_id` (`04 §3.1`); auch dann steht der Antrag bei
`PENDING`.

Das ist kein Betrug, sondern eine Meinungsänderung. Zurücknehmen lässt sich eine Stimme nicht
(`04 §8`); ersetzen schon (`04 §3.1`, D547). Der Bildschirm sagt es vorher, bei der zweiten
Stimme: „Du hast schon anders abgestimmt. Diese Stimme ersetzt die frühere.“ und in der Folge
„Deine frühere Stimme zählt dann nicht mehr.“

### 5.2 Die Gabelung

Bruno will es sich mit niemandem verderben. Er schickt Anna ein Ja und Chris ein Nein, beide
unterschrieben mit seinem Schlüssel und beide auf denselben Vorgänger in seiner Kette. Genau das
ist der Fall, gegen den das Protokoll gebaut ist: jemand erzählt anderswo etwas anderes
(`08 §1`).

| Zeitpunkt | Annas Rechner | Chris' Rechner |
|---|---|---|
| Bruno hat geschickt | Ja: Anna, Chris, Bruno. **3 Ja, `PASSED`** | Ja: Anna, Chris. Nein: Bruno. `PENDING` |
| Anna ratifiziert | Epoche 3, neue Satzung gilt | Ratifizierung zitiert eine unbekannte Stimme: `UNKNOWN_WITNESS_VOTE`, Epoche 2 |
| beide tauschen aus | beide Stimmen Brunos `equivocation-flagged`, 2 Ja, `PENDING`, **zurück auf Epoche 2** | dasselbe |

Nach dem Austausch rechnen beide dasselbe, und es gilt wieder die alte Satzung. Annas
Ratifizierung stützt sich auf eine Stimme, die nicht mehr zählt, und trägt nicht
(`UNSUPPORTED_RATIFICATION`, `04 §4.1`). Die Richtung ist immer abwärts: durch eine Lüge entsteht
nichts, es fällt höchstens etwas weg (`04 §8`).

Zurück bleibt das Paar aus Brunos beiden Stimmen. Beide tragen seine Unterschrift und denselben
Vorgänger; wer sie hat, kann es jedem zeigen, und niemand muss Bruno glauben oder nicht glauben
(`01 §4`, `08 §2.2`).

**Wie es weitergeht.** Sobald Dora wieder da ist und Ja sagt, sind es drei saubere Ja. Jemand
ratifiziert neu mit den Stimmen von Anna, Chris und Dora, und Epoche 3 gilt für alle. Annas erste
Ratifizierung bleibt liegen, unwiderruflich und wirkungslos. Hatte Anna die neue Satzung schon
angenommen, als ihr Rechner Epoche 3 zeigte, wird diese Annahme in dem Moment wieder wirksam.

**Was die Bildschirme zeigen.** Das ist der Moment der Demo:

- Anna, nach dem Austausch: „Die neue Satzung gilt nicht mehr. Bruno hat widersprüchlich
  abgestimmt.“ Darunter beide Stimmen nebeneinander, mit Zeit, Inhalt und dem Vermerk „dieselbe
  Stelle in Brunos Kette“.
- Chris: dasselbe, und dazu die Stimme, die sie selbst nie bekommen hatte.
- Bruno: „Deine beiden Stimmen sind bei allen angekommen.“
- Alle: „Epoche 2. Für den Beitrag fehlt eine Ja-Stimme.“

Die Auszählung selbst schweigt über die Gabelung: Bedingung 6 aus `04 §3.1` lässt die geflaggten
Stimmen ohne Vermerk fallen. Den Beweis liest der Bildschirm aus dem Zustand der Claims, eine
Schicht tiefer (D469).

### 5.3 Was aus der Lüge folgt

Das Protokoll stellt den Beweis fest. Was daraus folgt, entscheidet der Verein (D467 Beschluss 4).
Drei Dinge geschehen, eines davon von selbst.

**Von selbst: Bruno kann nicht mehr bürgen.** Ein Autor mit einem Gabelungsbeweis ist geflaggt,
gleich in welchem Scope (`02 §8`); bei der Voreinstellung tragen seine Bürgschaften keine Kante
mehr. Die Gabelung im Verein nimmt ihm damit das Gewicht im Vereinsleben. Chris bleibt über Anna in
Distanz 1, Dora über Chris in Distanz 2. Der Flag geht nicht weg: der Beweis bleibt im Bestand.

**Wenn die anderen wollen: Ausschluss.** Ein Antrag mit einer Mitgliederliste ohne Bruno, Klasse
`membership`, bei `n = 4` drei Ja nötig. Anna, Chris und Dora genügen; Bruno darf mitstimmen, aber
mit einem Nein nichts aufhalten, dafür bräuchte er zwei. Danach ist er nicht mehr stimmberechtigt.

**Was bleibt.** Bruno ist Wurzel und Anker beider Scopes und Schlichter im Vereinsleben. Das steht
im Genesis und in der Satzung von `N_res`, und beides ist nicht änderbar (`example-nucleus §6`).
Im Verein lässt es sich ändern, im Vereinsleben nicht; wer ihn dort loswerden will, gründet ein
neues Vereinsleben. Das ist der Preis der Trennung. Für die Schlichter ist er in O35 geführt;
für Wurzel und Anker gibt es keinen Ausweg außer dem neuen Scope.

---

## 6. Der Beitrag

Die Satzung mit Beitrag gilt. Dora zahlt ihre 24 Euro in bar an Chris. Das Geld bewegt sich
außerhalb des Protokolls; im Protokoll bewegen sich zwei Unterschriften.

| # | Wer unterschreibt | Scope | Claim | Inhalt |
|---|---|---|---|---|
| V20 | DORA | `N_res` | `obligation@1` | `J = [1, KASSE]`, `v = {0: 2400, 1: h'4555522d43656e74'}` |
| V21 | KASSE (Chris' Gerät) | `N_res` | `receipt@1` | `J = [2, cid(V20)]`, kein `v` |

`v` Key `1` ist die Einheit, die Bytes von „EUR-Cent“. Kein Rechner liest Betrag oder Einheit
(`03 §3.1`); sie stehen für die Menschen da.

**Was jeder Rechner rechnet** (`03 §3.3.2`). Nach V20 ist Doras Beitrag `OPEN`, nach V21
`SETTLED`. Die Obligation kann Dora nicht zurückziehen: `obligation@1` ist immer unwiderruflich
(`00 §5.2`). Die Quittung kann Chris zurückziehen, dann lebt die Schuld wieder auf; der Widerruf
bleibt dabei sichtbar (`03 §5`).

**Drei Fälle, die der Bildschirm unterscheiden muss.**

- **Teilzahlung.** Zahlt Dora 12 Euro und quittiert Chris mit `v = {0: 1200}`, bleibt der Beitrag
  `OPEN`, mit dem Vermerk `PARTIAL_RECEIPT_UNSUPPORTED`. Eine Quittung mit Betrag tilgt nie. Zwei
  halbe Beiträge sind zwei Obligationen zu 1200.
- **Keine Obligation.** Unterschreibt ein Mitglied nie, gibt es nichts Offenes. Der Verein kann
  niemandem eine Schuld zuschreiben; die Obligation unterschreibt der Schuldner selbst
  (`03 §3.3.1`, `08 §3` Zeile Gruppen-Soll). Die Kasse sieht, wer für dieses Jahr unterschrieben
  hat und wer nicht.
- **Unterschrieben, nicht bezahlt.** `OPEN` sagt nicht, ob nicht gezahlt, nicht quittiert oder nur
  noch nicht zugestellt wurde (`08 §7`). Ein Zustand „überfällig“ existiert nicht. Wer Nichtzahlung
  behauptet, tut es mit `accusation@1` und unter seinem Namen (`05 §3`).

**Was die Bildschirme zeigen.**

- Dora: „Beitrag 2026: 24 € an die Kasse. Unterschreiben?“, danach „offen“, danach „bezahlt, von
  der Kasse quittiert“.
- Chris, als Kasse: eine Liste der Mitglieder mit drei Spalten, unterschrieben, quittiert, fehlt.
  „Quittieren“ ist ein Knopf ohne Betragsfeld.

---

## 7. Was der S-Node leisten muss

Für Phase 2 (`ROADMAP.md §4`). Nicht Protokoll, sondern die Anforderungen, die dieses Szenario an
den Rechner stellt, der die Claims hält.

- **Beide Scopes gemeinsam führen** und für jeden `resolve_state` rechnen (`04 §4.5`), dazu
  `membership()` mit dem Verfassungsobjekt der erreichten Epoche (`04 §6.2`), `trust()` im
  Vereinsleben und `settlement()` für jede Obligation.
- **Über die Scopes hinweg anzeigen, nicht rechnen.** Die Bürgschaft neben dem Antrag (`§3`), die
  Mitgliederliste neben der Beitragsliste (`§6`). Keine Rechnung verknüpft die Scopes.
- **Gabelungsbeweise zeigen.** Die Auszählung vermerkt sie nicht (D469). Der S-Node liest
  `equivocation-flagged` aus dem Zustand der Claims und zeigt das Paar, in jedem Scope, in dem der
  Autor vorkommt.
- **Aufgaben führen.** Offene Bestätigungen nach jedem Epochenwechsel, offene Beiträge, fehlende
  Obligationen.
- **Warnen, bevor unterschrieben wird.** Budget voll (`§3`), zweite Stimme (`§5.1`), Betrag in der
  Quittung (`§6`).
- **Eine Kette je Identität.** Jede Identität hat genau eine Kette über alle Scopes. Unterschreibt
  sie von zwei Geräten, gabelt sie sich selbst (`01 §8`). KASSE lebt deshalb auf genau einem Gerät,
  dem von Chris.

---

## 8. Was fehlt

Keiner der drei Abläufe braucht neues Protokoll. Gefunden wurde:

- **Ein Amtswechsel der Kasse ist eine Schlüsselübergabe.** Die Quittung wird byteweise gegen den
  Gläubiger geprüft (`03 §3.3.2`). Gibt Chris das Amt ab, muss sie den Schlüssel weitergeben, und
  wer ihn einmal hatte, kann weiter quittieren. Offen als O89 (D468 Beschluss 2).
- **Jede Aufnahme verlangt vier neue Unterschriften.** Getragen, weil die Annahme eine eigene
  Einwilligung ist; der Bildschirm macht daraus eine Aufgabe (D468 Beschluss 3).
- **Die Auszählung schweigt über Gabelungen.** Getragen, der S-Node zeigt sie (D469).
- **Sätze in `00`, `01`, `03` und `04`, die nicht mehr stimmen,** wurden beim Lesen gefunden und
  berichtigt (D470).

---

## 9. Die gerechneten Objekte

Ausgabe von `python -m tools.verein` am Commit `2d70cca`, kopiert, nicht abgeschrieben (D472).

```
constitution_3  1675cd589aabf17567cadbf3bf5b5742dfbd9f089aa8e01726908a20755016fb
proposal_3      6747ee5cfa15f66ddecaadc340ea304ea96a171c751505442b70093df0572b14
epoch_3         c68caa1b9fb24a2958f2ead77a4c85088e5e69d90bddc14f7b22fefd865c4887
constitution_4  a3533705454f0fafc65400a4c43b515a2dac659d0345a345f34d18fa7f4b7d47
proposal_4      c22fe60ed5336899b18cef8f9f5fc327b4124fad86431893e3231629ad2be446
KASSE           d54207da194977dcf46adbfec2bc2e75b52d5a8a42184fedfdc00024f0e3e8da
```

`constitution_3` ist die Satzung mit Beitrag aus `§4`, `proposal_3` ihr Antrag auf Epoche 2,
`epoch_3` die Epoche, die er öffnet. `constitution_4` und `proposal_4` sind der Ausschluss aus
`§5.3`. Die Claims `V1` bis `V21` tragen keine festen Hashes: ihre Zeitstempel sind Parameter der
Welt, nicht Teil des Szenarios.
