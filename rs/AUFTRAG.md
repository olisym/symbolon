# 00bv — Drittfassung Layer 02 in Rust

## Auftrag

Baue in Rust einen Trust-Flow-Rechner für das, was in `spec/02-trust-flow.md` beschrieben ist.

`spec/01-claim-atom.md` liegt daneben, weil Layer 02 darauf aufsetzt: Claims müssen dekodiert,
geprüft und in ihren Lebenszyklus-Zustand eingeordnet werden, bevor Layer 02 überhaupt beginnt.

Die Spec ist die einzige Quelle. Es gibt keine Referenzimplementierung zum Nachsehen und keine
weiteren Spec-Dateien. `spec/STAND.md` sagt, auf welchen Stand die Kopie eingefroren ist und was
bewusst fehlt.

## Umfang

Gebaut wird die Kette von den Claim-Bytes bis zum Fluss: Einordnung der Claims, Gruppenbildung,
Budgetprüfung, Kapazitäten und Distanzen, Aufbau des Flussgraphen, Abfrage.

Der Max-Flow-Algorithmus selbst wird **nicht** geschrieben. Er kommt aus `petgraph`, Funktion
`petgraph::algo::ford_fulkerson`, angewandt auf `Graph` — **nicht** auf `StableGraph`, und
**nicht** aus dem jüngeren `maximum_flow`-Modul. Die Signaturprüfung kommt aus `ed25519-dalek`,
der Hash aus `sha2`, die CBOR-Kodierung aus `ciborium`. Das ist nicht verhandelbar; erweist sich
eines davon beim Bau als untragfähig, halte an und melde es, statt auszuweichen.

**Der Kapazitätstyp ist `u64`, durchgehend.** Kein `u128`, kein `i128`, keine Bignum-Bibliothek,
auch nicht stellenweise. Läuft eine Rechnung über, ist das ein Ergebnis und kein Hindernis: halte
an, melde die Stelle und die beteiligten Werte. Der begrenzte Typ ist Teil dessen, was hier
gemessen wird.

Nicht gebaut werden PageRank, Enforcement, Governance und alles, was jenseits dieser beiden
Spec-Dateien liegt.

## Eingabe

Drei Dateien mit gleicher Struktur, zusammen zwanzig Profile:

- `vektoren/tp02.json` — acht Profile
- `vektoren/tz02.json` — neun Profile
- `vektoren/fall02.json` — drei Profile

Je Profil:

- `profil` — Name
- `params` — `C0`, `gamma_num`, `gamma_den`, `D`
- `now` — ganze Zahl
- `scope` — Hex
- `labels` — Name auf öffentlichen Schlüssel in Hex, zur Lesbarkeit der Ausgabe
- `claims` — die Wire-Bytes je Claim in Hex, in Bau-Reihenfolge
- `anchors`, `targets` — Hex

Die Dateien enthalten **keine** erwarteten Werte. Sie sind Eingabe, nicht Antwort. `C0` ist nicht
in allen Dateien gleich gross.

Alle Abfragen laufen so, dass Vouches geflaggter oder über-committeter Autoren ihre Kante
**tragen**. Die Spec nennt dafür einen abweichenden Vorgabewert; hier gilt der andere Fall, weil
der Mechanismus gemessen wird und nicht die Policy. Das Budget ist davon unberührt — Flags
ändern nie die Budgetrechnung.

## Schnittstelle

Ein ausführbares Programm. Es nimmt den Pfad einer der JSON-Dateien als Argument und schreibt auf
die Standardausgabe je Profil einen Block. Zeilen, Felder durch ein Leerzeichen getrennt, Hex
klein:

```
profil <name>
zustand <claim_id> <zustand>
gruppe <I> <J> <n_budget> <n_kante>
budget <I> <summe> <verdikt>
kante <I> <J> <d> <C> <cap>
inf <wert>
fluss <ziel> <wert>
simultan <wert>
disjunkt <wert>
schnitt <identity> ...
befund <name> <adresse>
```

- `zustand` je Claim des Profils, sortiert nach `claim_id`. Die Namen der Zustände werden
  `spec/01-claim-atom.md` entnommen, in der dort gedruckten Schreibweise.
- `gruppe` je Gruppe, sortiert nach `I`, dann `J`.
- `budget` je Autor mit mindestens einer Gruppe, sortiert. `verdikt` ist `ok` oder `over`.
- `kante` je Kante des Flussgraphen, sortiert. `d` und `C` sind die des Autors; für
  unerreichbare Autoren schreibe `inf` statt einer Zahl.
- `inf` nennt den Zahlwert, mit dem du unbeschränkte Kanten im Flussgraphen belegst. Führst du
  keinen solchen Wert, schreibe `inf keiner`. Diese Zeile misst deine Belegung, nicht dein
  Ergebnis; sie wird gegen keine Erwartung gehalten.
- `fluss` je Ziel einzeln, sortiert. `simultan` ist die Abfrage über alle Ziele gemeinsam,
  `disjunkt` dieselbe Abfrage mit Einheitskapazitäten.
- `schnitt` nennt den **quellseitigen** minimalen Schnitt: die im Residualgraphen von der
  Super-Quelle erreichbaren Knoten bestimmen ihn eindeutig. Gedruckt werden die Identitäten,
  deren **interne Kante** im Schnitt liegt, sortiert nach Bytes. Besteht der Schnitt
  ausschliesslich aus Vouch-Kanten, bleibt die Zeile leer — das ist kein Fehler, sondern die
  Aussage, dass hier keine Person bindet, sondern eine Beziehung. Der Schnitt wird für die
  `simultan`-Abfrage gerechnet.
- `befund` je Vermerk, sortiert nach Name, dann Adresse. Namen und Adressen stehen in
  `spec/02-trust-flow.md`.

**Die Reihenfolge der Blöcke ist eine Ausgabeordnung, keine Rechenvorschrift.** Sie sagt nichts
darüber, in welcher Reihenfolge gerechnet wird, und nichts darüber, ob eine Stufe von der
vorigen abhängt. Wie du intern schneidest, ist deine Sache; nur die Ausgänge müssen stimmen.

## Der Vektorsatz ist unvollständig

Er enthält zwanzig Profile als Eingabe. Erwartete Werte sind absichtlich zurückgehalten und
werden nicht nachgereicht. Aus dem Fehlen eines Beispiels folgt nichts: eine Bedingung der Spec
ist nicht deshalb unwichtig, weil kein gerechneter Fall dazu vorliegt.

## Was mitzuliefern ist: die Fragenliste

Neben dem Code entsteht `FRAGEN.md`. Darin steht jede Stelle, an der die Spec mehrdeutig,
unvollständig oder widersprüchlich war und eine Entscheidung nötig wurde. Je Eintrag:

```
## <n>. <Titel>

- **Adresse:** <kanonisch>
- **Frage:** die Frage, die der Text offenlässt
- **Lesart:** die Lesart, für die entschieden wurde
- **Verworfen:** die verworfene Lesart, und warum
```

Die **Adresse** ist Pflicht und hat die Form `<Quelle> <Stelle>`:

- Quelle ist `01` oder `02` für die beiden Spec-Dateien, `AUFTRAG`, wenn allein diese Datei die
  Frage aufwirft, oder `WERKZEUG`, wenn sie an Sprache oder Bibliothek hängt.
- Stelle ist `§N`, `§N.M` oder `Anhang X.N` — für `AUFTRAG` und `WERKZEUG` entfällt sie.
- Mehrere Stellen mit ` / ` getrennt, die engste zuerst: `02 §3.1 / 02 §10`.

Diese Datei ist nicht Beiwerk, sondern das wichtigste Ergebnis dieser Arbeit. Eine Stelle, an der
geraten wurde, ohne dass sie hier steht, ist verloren. Lieber ein Eintrag zu viel.

Es wird nicht zurückgefragt und nicht auf eine Antwort gewartet. Es wird entschieden, gebaut und
der Eintrag geschrieben.

## Nicht-Ziele

- Kein eigener Max-Flow, kein eigenes Ed25519, kein eigenes SHA-256, kein eigener CBOR-Decoder.
- Kein Wechsel des Kapazitätstyps, auch nicht an einer einzelnen Stelle, auch nicht als
  Zwischenrechnung.
- Keine Netzwerk-, Datei- oder Zeitzugriffe ausser dem Lesen der Eingabedatei. `now` kommt aus
  der Datei, nie aus einer Uhr.
- Kein Zugriff auf Verzeichnisse ausserhalb dieses Arbeitsverzeichnisses.
- Keine Vollständigkeitsannahme über den Vektorsatz.
- Keine Anpassung der Ausgabe an vermutete Erwartungen. Wenn eine Rechnung ein Ergebnis liefert,
  das unplausibel wirkt, ist das Ergebnis zu drucken und der Zweifel in `FRAGEN.md` zu notieren.

## Abschluss

Ein Commit in diesem Verzeichnis. Kein Merge. Der Bericht nennt: die gebauten Dateien, die Zahl
der eigenen Tests, die Zahl der Einträge in `FRAGEN.md`, die verwendeten Versionen von
`petgraph`, `ed25519-dalek`, `sha2` und `ciborium`, und die vollständige Ausgabe des Programms
über alle drei Eingabedateien.
