# Werkzeugschicht — Spezifikation v1

Status: Entwurf · Protokollversion: 1 · **Kein Layer**

Diese Datei trägt normativ, was bisher nur in Implementierungs-Prompts stand: die Autorschaft
(`tools/autor.py`), die Simulation (`tools/sim/`) und die Eigenschaftstests
(`tests/property/`). Sie führt **keinen** neuen Protokollmechanismus ein.

---

## 1. Einordnung — die dritte Spalte

Das Aufnahmekriterium aus `08 §3` fragt vor jedem neuen Mechanismus:

> Senkt er die Kosten dafür, festzustellen, wer was gesagt hat — oder verteilt er Macht?

Senken heißt Protokoll, verteilen heißt Policy. Es gibt einen dritten Fall: **keines von beidem**.
Ein Werkzeug erzeugt Claims überhaupt erst, oder es prüft, was das Paket rechnet. Es senkt keine
Feststellungskosten, weil ein Claim nach `01 §4` bereits selbstenthalten ist, und es verteilt keine
Macht, weil es nichts entscheidet.

Daraus folgt die Form dieser Datei:

- **Keine Zahl im Dateinamen, keine Golden Anchors, kein Layer.** Ein Werkzeug hat keine Anker,
  weil es keine Zahl erzeugt, die ein zweiter Implementierer treffen müsste.
- **Was hier steht, ist trotzdem normativ.** Die Schreibordnung aus §2.3 ist kein Stilvorschlag;
  ihre Verletzung erzeugt Selbst-Equivocation.
- **Nichts hier darf rechnen, was das Paket rechnet.** Eine zweite Kapazitätsformel, eine zweite
  Auszählung oder ein zweiter Kodierweg macht jede Aussage zirkulär.

Die Entscheidungen dieser Schicht stehen in D119 bis D129.

---

## 2. Autorschaft — `tools/autor.py`

Der Modulschnitt kommt aus D122: **Bau und Signatur** liegen im Paket (`build_signed`), weil
`core_bytes`, `DOM_SIG` und der Feldsatz zu `01` gehören und zwei Kodierwege driften. **Kettenspitze
und Schlüsselverwahrung** liegen im Werkzeug, weil sie Dauerhaftigkeit brauchen und nach `08 §3`
Betriebsfragen sind.

**Oberflächenregel.** Keine Operation gibt den Schlüssel oder die Spitze heraus. Es gibt genau eine:
gib mir einen signierten Claim zu diesem Inhalt. Überquert der Schlüssel die Grenze nie, ist ein
späterer entfernter Aufruf eine Transportfrage und kein Umbau.

**Ein Schreiber, ein Ort** (D123). Zwei gleichzeitige Schreiber auf derselben Kette verlangten eine
Einigung darüber, wer die Spitze fortschreibt; Geräte sind Endpunkte, nicht Kopien. Die Migration
auf ein anderes Gerät trägt Seed **und** Spitze; wer einen Sicherungsblob zweimal einspielt, hat
zwei Schreiber.

### 2.1 Die zwei Ports

Beide sind bewusst dumm. Sie tragen **keine** Protokollsemantik und rechnen insbesondere **nie**
`h_prev` (D127).

```
Rueckhalt:
  spitze_lesen()      -> bytes | None
  spitze_schreiben(h_prev)
  redo_lesen()        -> bytes | None
  redo_schreiben(signierte_bytes)
  redo_schliessen()

Ausgang:
  kennt(claim_id)     -> bool
  aufnehmen(claim)
```

`spitze_lesen` und `redo_lesen` liefern `None`, wenn nichts vorliegt. `redo_schliessen` auf einen
bereits geschlossenen Redo ist erlaubt und tut nichts.

Diese Naht ist die Antwort auf einen Einwand, der die Sache fast blockiert hätte: zwei
Implementierungen von Kettenfortführung und Signatur driften. Sie tun es nicht, wenn das Doppelte
`h_prev` gar nicht kennt. Was doppelt sein darf, ist der Rückhalt; die Fortführung existiert einmal.

Es gibt zwei Rückhalte — Speicher und Dateien — und **einen** Testsatz, der über beide läuft.

### 2.2 Der Zustand und die Wiederaufnahme

`wiederaufnehmen()` leitet den Zustand aus Rückhalt und Ausgang ab. **Die Reihenfolge ist normativ:
erst der Redo, dann die Spitze** (D127).

```
1. Redo offen?
     Claim aus den Bytes rekonstruieren
     traegt er ein fremdes I  -> ANGEHALTEN
     kennt der Ausgang ihn nicht -> aufnehmen
     Spitze := claim_id, Redo schliessen -> FORTGESETZT
2. Spitze leer                 -> GENESIS, h_prev = id_genesis_anchor(I)
3. Spitze gesetzt, Ausgang kennt sie nicht -> ANGEHALTEN
4. sonst                       -> NORMAL, h_prev = Spitze
```

**Warum Redo zuerst.** Der Zustand hat drei unabhängige Bits — Spitze gesetzt, Redo offen, Claim der
Spitze bekannt. Die Lage „Spitze leer, Redo offen" entsteht beim Absturz während des allerersten
Claims. Prüfte man die Spitze zuerst, führe sie in den Genesis-Ausgang und baute einen **zweiten**
Genesis-Claim mit neuem `t` — Selbst-Equivocation, genau der Fehler, den die Ordnung verhindern
soll. Die Reihenfolge beseitigt die Lage, statt einen weiteren Ausgang zu brauchen.

Wirft die Rekonstruktion des eigenen Redo, ist das ein Programmierfehler (D92) und **kein**
Reject-Code: eigene Bytes sind keine Lage der Welt.

**Der Halt ist eine Ableitung, kein Gedächtnis** (D128). Ein Halt aus Ausgang 3 heilt, sobald der
fehlende Claim nachgeliefert ist — die Aussage betrifft den Ausgang und nicht die Kette. Ein offener
fremder Redo heilt nicht, weil sich diese Lage nicht von selbst ändert. Beides ist dieselbe Regel.

**Nicht erfasst: zwei eigene Claims auf dieselbe Spitze.** Der doppelt eingespielte Sicherungsblob
erzeugt den Fork in zwei **getrennten** Stores, von denen keiner beide Zweige sieht. Der Fall ist
durch eine Startprüfung nicht erreichbar, sondern erst bei der Vereinigung. Dort erkennt ihn jeder
Leser als Equivocation nach `01 §4`; die Grenze trägt `01 §8` (Ein-Schreiber-Annahme). Das
Werkzeug bekommt keinen Ausgang dafür: nach der zweiten Signatur verhindert ein Halt nichts mehr
(D162, D424). Vermeiden lässt er sich nur im Betrieb, also beim Sicherungsblob (O25).

### 2.3 `signieren` — die Schreibordnung

Vier Schreibvorgänge, in genau dieser Reihenfolge (D120):

```
0. bauen und signieren        (schreibt nichts)
1. Redo schreiben
2. aussenden
3. Spitze schreiben
4. Redo schliessen
```

Die Alternativen tragen nicht:

| Ordnung | Absturz dazwischen | Folge |
|---|---|---|
| signieren, dann persistieren | Spitze veraltet | Equivocation auf demselben `h_prev` |
| Spitze zuerst, dann signieren | Spitze zeigt ins Leere | Nachfolger bleiben `pending`, unheilbar |
| **die Ordnung oben** | Redo liegt vor | Wiederaufnahme erzeugt denselben Claim |

Sie trägt, weil Ed25519 deterministisch signiert (RFC 8032): aus denselben Core-Bytes entsteht
dieselbe Signatur, also derselbe Claim, byteweise. Die Wiederaufnahme ist **idempotent** und nicht
bloß möglich — der Unterschied zwischen einer Rettung und einer Gabelung.

**Der Redo-Eintrag trägt die signierten Claim-Bytes, nicht die Core-Bytes** (D127). Die Signatur ist
eine deterministische reine Funktion des Cores, also ist bei atomarem Schreiben beides gleich
sicher;
die Absturzordnung betrifft die **Spitze**. Der Gewinn ist ein vermiedener zweiter Dekodierweg.
Nebenertrag: `t` bleibt beim Fortsetzen zwingend unverändert, weil es aus den Bytes kommt und nicht
neu gesetzt werden **kann**.

**`claim_id` ist die Hochwassermarke.** Die Wiederaufnahme fragt den Ausgang, ob er den
rekonstruierten Claim kennt. Kein „erledigt"-Flag, kein zusätzlicher Zustand — der Claim ist
inhaltsadressiert, und Präsenz ist die Prüfung. ARIES erkauft dieselbe Idempotenz über den
LSN-Vergleich; hier ist sie geschenkt.

### 2.4 `gabeln`

`gabeln` signiert über die aktuelle Spitze und sendet aus, **schreibt aber weder Redo noch Spitze**
und rückt die Spitze nicht vor (D129).

Der Grund trägt die Operation allein: schriebe `gabeln` einen Redo, machte ein späteres
`wiederaufnehmen` den absichtlichen Fork zur **echten Spitze** — der Zwilling würde still zum
Hauptzweig. Schriebe es die Spitze, wäre es kein Fork, sondern ein gewöhnlicher Anhang. Es bleibt
nur, den dauerhaften Zustand gar nicht zu berühren, und das ist auch die richtige Aussage über die
Sache: ein absichtlicher Fork steht **neben** der Kette, er ist nicht etwas, das die Kette tut.

`gabeln` existiert für die Simulation (S5) und die Eigenschaftstests (P-3b) und für nichts sonst. Es
ist eine **eigene benannte Operation** und kein Bool-Argument an `signieren`: der gefährlichste
Zustand der Kette darf kein Default-Argument sein.

### 2.5 Der Halt

**Anhalten und nicht warnen.** Weiterschreiben ist in jedem der Haltefälle genau der Fehler, den die
Prüfung erkannt hat.

Der Halt gilt auch für die **abgefangene Ausnahme** (D128). Bricht ein Schreibvorgang ab und fängt
der Aufrufer die Ausnahme, ist der Zustand des Objekts derselbe wie nach einem Absturz — nur läuft
der Prozess weiter. Ohne Halt baute der nächste Aufruf einen zweiten Claim auf dasselbe `h_prev`.
Das Objekt setzt daher `ANGEHALTEN`, räumt die Spitze und wirft **unverändert weiter**.

Die Klausel fängt `BaseException` und nicht `Exception`: `KeyboardInterrupt` und `SystemExit` erben
nicht von `Exception`, und in einem bedienten Werkzeug ist Strg-C während des Signierens der
wahrscheinlichste Abbruch überhaupt. Sie schluckt nichts und ist damit die anerkannte Ausnahme von
der Regel gegen weite `except`-Klauseln; die Regel selbst bleibt unangetastet.

Der Halt gilt einheitlich für alle vier Schreibvorgänge. Bricht der letzte ab, ist die Lage sachlich
unbedenklich, und der Halt kostet dort ein `wiederaufnehmen` und nichts sonst. Eine
Fallunterscheidung nach Schritt wäre eine Behauptung darüber, was der abgebrochene Schritt bereits
bewirkt hat — und die kann das Objekt nicht prüfen.

Der Halt klebt am **Objekt**, nicht am Rückhalt: `wiederaufnehmen` nimmt die Kette auf demselben
Objekt wieder auf. Das ist der vorgesehene Weg nach einem behandelten `OSError`.

### 2.6 Der Datei-Rückhalt und seine Voraussetzungen

Zwei Dateien im Verzeichnis: `spitze` (Hex, ASCII) und `redo` (rohe Bytes). Jeder Schreibvorgang
geht über eine Temporärdatei im **selben** Verzeichnis, `fsync` auf den Dateideskriptor,
`os.replace` auf den Zielnamen, `fsync` auf den Verzeichnisdeskriptor.

**Getragene Grenze.** Der Rückhalt setzt drei Persistenzeigenschaften voraus — atomares
`os.replace`, `fsync` der Datei vor dem Rename, `fsync` des Verzeichnisses danach — und **prüft sie
nicht**. Die Literatur ist hier eindeutig: ALICE (OSDI '14) fand 60 Crash-Vulnerabilities in elf
ausgereiften Anwendungen, weil die Persistenzeigenschaften zwischen verbreiteten Linux-Dateisystemen
weit auseinandergehen; insbesondere garantiert ein `fsync` auf eine Datei nicht, dass ihr
Verzeichniseintrag persistiert ist. Ohne ein Werkzeug dieser Klasse ist die Annahme argumentierbar
und nicht prüfbar. Sie wird benannt statt behauptet.

**Prüfbar ist dagegen die Zustandsmaschine.** Die Absturzpunkte liegen in der Reihenfolge der
Operationen, nicht im Rückhalt. Ein Rückhalt, der beim k-ten Schreibvorgang wirft, aufgezählt über
alle k, prüft sie erschöpfend — im Speicher, deterministisch, ohne Dateisystem. Referenz für jeden
gestörten Lauf ist der ungestörte Lauf derselben Eingabe.

---

## 3. Simulation — `tools/sim/`

### 3.1 Bauform

```
tools/sim/
  welt.py         Teilnehmer, Verzeichnisse, Zustellung
  szenario.py     Szenariodatei lesen und ausfuehren
  anzeige.py      Tabellen
  scenarios/*.json
```

Je Teilnehmer ein Verzeichnis unter einem Weltpfad:

```
<welt>/anna/
  key.bin         32 Byte Seed
  now             Unix-Sekunden, als Text
  spitze          Kettenspitze, Hex          (aus 2.6, erst ab dem ersten Claim)
  redo            offener Redo-Eintrag       (nur waehrend eines Schreibvorgangs)
  inbox/<claim_id_hex>.cbor
```

**Claims sind einzelne Dateien.** Der Dateiname ist die `claim_id` in Hex, der Inhalt sind die
kanonischen Bytes. Ein Claim ist nach `01 §4` offline selbstenthalten und trägt seinen eigenen
Verify-Key — die Simulation behandelt ihn deshalb wie einen Gegenstand, den man kopieren,
verschicken oder ausdrucken kann.

Der Teilnehmer **ist** der `Ausgang` seines Autors: die Inbox beantwortet `kennt`, und `aufnehmen`
legt eine Datei an. Ein zweiter Weg, der Claim-Dateien anlegt, darf nicht entstehen.

**`kennt` antwortet aus dem Inhalt, nicht aus dem Dateinamen (D132, D138).** Der Name
`<claim_id_hex>.cbor` lokalisiert die Datei; die Antwort verlangt darüber hinaus, dass `read_claim`
auf ihren Bytes einen Claim liefert und dessen `claim_id` der gefragten gleicht. Der Grund liegt
nicht in der Inbox, sondern bei ihrem Verbraucher: `kennt` ist der Port, den `wiederaufnehmen`
befragt, um zu entscheiden, ob die gespeicherte Spitze vorliegt (§2.2). Ein falsches „kenne ich"
aus einem Dateinamen ließe die Kette über einen Vorgänger fortschreiben, den niemand hält — ein
Absender könnte sie stören, ohne eine Signatur zu fälschen.

Ebenso lädt `store_laden` über `read_claim` und überspringt, was als Reject-Code zurückkommt. Der
Store wird dabei nicht durchgereicht: er wäre während des Ladens halbfertig und bände
`FOREIGN_LIFECYCLE` an die Sortierung der Dateinamen (D138).

**Zustellung ist ein Befehl**, nie automatisch, und läuft **nicht** über den `Ausgang`: sie kopiert
rohe Bytes, ohne zu dekodieren. Zustellung ist keine Autorschaft. Nichts synchronisiert von selbst.

`now` wird aus der Datei gelesen und ist Parameter, nie Systemuhr.

### 3.2 Szenariodatei

JSON, stdlib, keine neue Abhängigkeit. Eine Liste von Schritten; jeder Schritt hat eine Art und
Argumente:

`welt` · `genesis` · `claim` · `zustellen` · `uhr` · `zeige` · `erwarte`

**`erwarte` ist Pflicht, nicht Zierde.** Jeder Schritt, der etwas zeigt, führt seine erwartete
Belegung mit; weicht der Lauf ab, bricht das Szenario mit einem Fehler ab. Ein Szenario ohne
Erwartungen ist eine Vorführung und kein Nachweis. Die `erwarte`-Blöcke sind die Anker dieser
Schicht.

Der Schritt `claim` trägt das optionale Feld **`kette_fortschreiben`**, Voreinstellung `true`. Auf
`false` wird der Claim gegabelt (§2.4). Das Feld bleibt im Schema, obwohl es aus der
Python-Oberfläche verschwunden ist: die Grenze liegt zwischen **Datei und Aufrufkonvention**. Ein
Szenarioautor, der `false` schreibt, hat es getippt; ein Programmierer, der ein Argument wegläßt,
hätte es nicht.

### 3.3 Die sechs Szenarien

S1 Gründung · S2 Der Dritte entscheidet · S3 Partition · S4 Überzeichnung · S5 Equivocation ·
S6 Uhrenstreit.

Sie sind Vorführungen mit Beweislast, keine Testfälle im engeren Sinn: sie zeigen, dass getrennte
Beobachter mit unterschiedlichem Wissen und unterschiedlichen Uhren **verschieden** rechnen dürfen,
ohne dass einer von ihnen falsch liegt.

---

## 4. Eigenschaftstests — `tests/property/`

**Geprüft werden Zusagen, die im Text stehen** — nicht, ob der Code tut, was er tut. Jede
Eigenschaft nennt die Stelle, die sie behauptet, und trägt ihre Vorbehalte ausdrücklich.

**Ein Fuzzer findet nur, was jemand aufgeschrieben hat.** Keiner der Befunde D114 bis D118 wäre so
entstanden; sie kamen aus Durchgängen, nicht aus Läufen. Diese Prüfungen ersetzen die Durchgänge
nicht, sie sichern das bereits Formulierte.

`hypothesis` steht unter `dev`, nicht im Paket. Die Hausregel „nur `cbor2` und `cryptography`"
betrifft das Paket; `pytest` steht dort ebenfalls.

### 4.1 Der Generator

`welten.py` beschreibt eine Welt: 3 bis 6 Identitäten mit Seeds aus dem Beispielnukleus, ein
Ankerset von ein bis zwei Identitäten, `C₀` und `D` aus `{16, 100}`, `γ` aus `{1/2, 2/3}`, 0 bis 12
Vouches mit `n` aus `1…D` ohne Selbstbezug, `t_exp` je Vouch gewichtet `4 : 4 : 1` als abwesend,
künftig oder vergangen, optional Stimmen auf **einen** Vorschlag im Governance-Scope, und einen
Zustellplan.

Zwei Schalter, **einzeln** setzbar, weil die Vorbehalte an ihnen hängen; Voreinstellung `False`:

```
erlaube_ueberzeichnung    Sigma n je Autor darf D ueberschreiten
erlaube_equivocation      zwei Claims mit demselben h_prev
```

### 4.2 Die Eigenschaften

**P-1 — Reihenfolgeunabhängigkeit.** Derselbe Claim-Bestand in beliebiger Einfügereihenfolge liefert
byte-identische Ergebnisse, für `derive`, `trust`, `decide` und `classify_all`. Ohne Vorbehalte.

Das ist die Eigenschaft mit dem höchsten Risiko: Max-Flow-Lösungen sind **nicht eindeutig** — der
Wert ist es, die Flusszerlegung nicht. Hängt irgendwo eine Auswahl an der Zerlegung statt am Wert,
oder eine Iteration an der Einfügereihenfolge, ist das Ergebnis reihenfolgeabhängig. Verglichen wird
**byteweise**, nicht feldweise.

**P-2 — Monotonie in Wissen.** Eine Teilmenge liefert nie höheres Vertrauen als der volle Bestand
(`02 §7`). Beide Vorbehalte sind zwingend: `erlaube_ueberzeichnung = False`, weil die Budgetprüfung
`Σ n ≤ D` nicht monoton ist (D118, kleinstes Gegenbeispiel zwei Vouches mit `n = 51` bei `D = 100`),
und `erlaube_equivocation = False`, weil ein eintreffender Zwilling einem zählenden Claim die
Wirkung entzieht (D117). Ohne sie ist die Eigenschaft **falsch**, und ein roter Lauf wäre kein
Befund, sondern eine falsch aufgeschriebene Zusage.

**P-3 — Die Vorbehalte positiv.** Was P-2 ausschließt, wird eigens geprüft, sonst prüft P-2 nur den
bequemen Bereich. P-3a: mit Überzeichnung existieren Welten, in denen eine Teilmenge **höheres**
Vertrauen liefert. P-3b: mit Equivocation entfernt ein zusätzlicher Claim eine zählende Stimme und
ein erreichtes `PASSED` fällt auf `PENDING` zurück. Beides sind **erwartete** Verletzungen; ein
Lauf, der keine findet, ist der Befund.

**P-4 — Konvergenz.** Haben am Ende alle Beobachter denselben Bestand und dieselbe Uhr, rechnen sie
dasselbe. Gleiche Uhr ist Bedingung, nicht Vorbehalt: über `t_exp` dürfen zwei korrekte
Verifizierer dauerhaft uneins sein (`01 §6`, D72), und das ist der einzige zugelassene Fall.

**P-5 — Die sichere Richtung der Auszählung.** Teilwissen erzeugt nie `PASSED`, wo Vollwissen es
nicht tut (`INV-04.3`). Vorbehalt: `erlaube_equivocation = False` (D117).

**P-6 — Zeitgrenze.** Ein Claim ist zeitlich gültig **gdw. `now ≤ t_exp`** (`01 §6`), geprüft
beiderseits der Grenze mit `now = t_exp` als ausdrücklich erzeugtem Fall.

Gefundene Gegenbeispiele werden **mitgeliefert** — als geschrumpfte Belegung im Kommentar oder als
eigener Vektor. Ein Gegenbeispiel, das nur im Lauf existierte, ist verloren.

Läufe bleiben klein: `max_examples` so, dass die Suite schnell bleibt. Ein langsamer Test wird
abgeschaltet, und ein abgeschalteter Test ist keiner.

---

## 5. Der Beispielnukleus

`tools/example_nucleus.py` rechnet die Objekte aus `example-nucleus.md` über **denselben** Kodierweg
wie das Paket. Er ist die Brücke zwischen den Golden Anchors der Layer und dem laufenden Code: was
dort steht, ist anderswo normativ, und dieses Werkzeug prüft nur, dass es auch entsteht.

---

## 6. Was diese Schicht nicht darf

- **Nichts rechnen, was das Paket rechnet.** Keine zweite Kapazitätsformel, keine zweite
  Auszählung, kein zweiter Kodierweg.
- **Keine Kettenfortführung außerhalb von `tools/autor.py`.** Sie hat fünfmal existiert; das ist die
  Klasse von Fehlern, die D122 beschreibt — ein vergessenes Feld erzeugt keinen defekten Claim,
  sondern einen in sich stimmigen mit anderer `claim_id` und korrekter Signatur über genau das, was
  dasteht.
- **Keine Systemuhr.** `now` ist überall Parameter.
- **Keine neue Abhängigkeit** außer `hypothesis` unter `dev`.
- **Keine Golden Anchors.** Wo eine Zahl gebraucht wird, ist die Referenz ein zweiter Lauf über
  derselben Eingabe, der sich in genau einer Größe unterscheidet.

---

## 7. Offene Punkte

- **Übersprungene Claims aus `store_laden`** werden nicht gemeldet (O34, D138).
- **Der Sicherungsblob** mit Seed und Spitze (D120) ist beschrieben und nicht gebaut.
- **B-4:** die Zwillingsbuchführung im Generator zieht kein Budget ab. Wirksam nur bei
  `erlaube_ueberzeichnung = False` **und** `erlaube_equivocation = True`, was heute keine
  Eigenschaft benutzt. Wer eine schreibt, repariert es zuerst.
