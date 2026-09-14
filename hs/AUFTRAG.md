# 00bo — Zweitimplementierung Layer 02 in Haskell

## Auftrag

Baue in Haskell einen Trust-Flow-Rechner für das, was in `spec/02-trust-flow.md` beschrieben ist.

`spec/01-claim-atom.md` liegt daneben, weil Layer 02 darauf aufsetzt: Claims müssen dekodiert,
geprüft und in ihren Lebenszyklus-Zustand eingeordnet werden, bevor Layer 02 überhaupt beginnt.

Die Spec ist die einzige Quelle. Es gibt keine Referenzimplementierung zum Nachsehen und keine
weiteren Spec-Dateien. `spec/STAND.md` sagt, auf welchen Stand die Kopie eingefroren ist.

## Umfang

Gebaut wird die Kette von den Claim-Bytes bis zum Fluss: Einordnung der Claims, Gruppenbildung,
Budgetprüfung, Kapazitäten und Distanzen, Aufbau des Flussgraphen, Abfrage.

Der Max-Flow-Algorithmus selbst wird **nicht** geschrieben. Er kommt aus `fgl`, Modul
`Data.Graph.Inductive.Query.MaxFlow` — **nicht** `MaxFlow2`, das ist auf `Double`
festverdrahtet, und dieser Solver rechnet ganzzahlig. Die Signaturprüfung kommt aus `crypton`,
**nicht** aus dem gleichnamigen Paket `ed25519`. Beides ist nicht verhandelbar; erweist sich
`fgl` beim Bau als untragfähig, halte an und melde es, statt auszuweichen.

Nicht gebaut werden PageRank, Enforcement, Governance und alles, was jenseits dieser beiden
Spec-Dateien liegt.

## Eingabe

`vektoren/tp02.json`, acht Profile. Je Profil:

- `profil` — Name
- `params` — `C0`, `gamma_num`, `gamma_den`, `D`
- `now`, `t_exp` — ganze Zahlen
- `scope` — Hex
- `labels` — Name auf öffentlichen Schlüssel in Hex, zur Lesbarkeit der Ausgabe
- `claims` — die Wire-Bytes je Claim in Hex, in Bau-Reihenfolge
- `anchors`, `targets` — Hex

Die Datei enthält **keine** erwarteten Werte. Sie ist Eingabe, nicht Antwort.

Alle Abfragen laufen so, dass Vouches geflaggter oder über-committeter Autoren ihre Kante
**tragen**. Die Spec nennt dafür einen abweichenden Vorgabewert; hier gilt der andere Fall, weil
der Mechanismus gemessen wird und nicht die Policy. Das Budget ist davon unberührt — Flags
ändern nie die Budgetrechnung.

## Schnittstelle

Ein ausführbares Programm. Es nimmt den Pfad der JSON-Datei als Argument und schreibt auf die
Standardausgabe je Profil einen Block. Zeilen, Felder durch ein Leerzeichen getrennt, Hex klein:

```
profil <name>
zustand <claim_id> <zustand>
gruppe <I> <J> <n_budget> <n_kante>
budget <I> <summe> <verdikt>
kante <I> <J> <d> <C> <cap>
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
- `fluss` je Ziel einzeln, sortiert. `simultan` ist die Abfrage über alle Ziele gemeinsam,
  `disjunkt` dieselbe Abfrage mit Einheitskapazitäten.
- `schnitt` nennt die Identitäten des minimalen Schnitts, sortiert; eine leere Zeile ist
  erlaubt. Welche Seite gemeint ist, entscheide selbst und schreibe die Entscheidung in
  `FRAGEN.md`.
- `befund` je Vermerk, sortiert nach Name, dann Adresse. Namen und Adressen stehen in
  `spec/02-trust-flow.md`.

**Die Reihenfolge der Blöcke ist eine Ausgabeordnung, keine Rechenvorschrift.** Sie sagt nichts
darüber, in welcher Reihenfolge gerechnet wird, und nichts darüber, ob eine Stufe von der
vorigen abhängt. Wie du intern schneidest, ist deine Sache; nur die Ausgänge müssen stimmen.

## Der Vektorsatz ist unvollständig

Er enthält acht Profile als Eingabe. Erwartete Werte sind absichtlich zurückgehalten und werden
nicht nachgereicht. Aus dem Fehlen eines Beispiels folgt nichts: eine Bedingung der Spec ist
nicht deshalb unwichtig, weil kein gerechneter Fall dazu vorliegt.

## Was mitzuliefern ist: die Fragenliste

Neben dem Code entsteht `FRAGEN.md`. Darin steht jede Stelle, an der die Spec mehrdeutig,
unvollständig oder widersprüchlich war und eine Entscheidung nötig wurde. Je Eintrag:

- der Abschnitt der Spec
- die Frage, die der Text offenlässt
- die Lesart, für die entschieden wurde
- die verworfene Lesart, und warum sie verworfen wurde

Diese Datei ist nicht Beiwerk, sondern das wichtigste Ergebnis dieser Arbeit. Eine Stelle, an der
geraten wurde, ohne dass sie hier steht, ist verloren. Lieber ein Eintrag zu viel.

Es wird nicht zurückgefragt und nicht auf eine Antwort gewartet. Es wird entschieden, gebaut und
der Eintrag geschrieben.

## Nicht-Ziele

- Kein eigener Max-Flow, kein eigener Ed25519, kein eigenes SHA-256.
- Keine Netzwerk-, Datei- oder Zeitzugriffe ausser dem Lesen der Eingabedatei. `now` kommt aus
  der Datei, nie aus einer Uhr.
- Kein Zugriff auf Verzeichnisse ausserhalb dieses Arbeitsverzeichnisses.
- Keine Vollständigkeitsannahme über den Vektorsatz.
- Keine Anpassung der Ausgabe an vermutete Erwartungen. Wenn eine Rechnung ein Ergebnis liefert,
  das unplausibel wirkt, ist das Ergebnis zu drucken und der Zweifel in `FRAGEN.md` zu notieren.

## Abschluss

Ein Commit in diesem Verzeichnis. Kein Merge. Der Bericht nennt: die gebauten Dateien, die Zahl
der eigenen Tests, die Zahl der Einträge in `FRAGEN.md`, die verwendeten Paketversionen von `fgl`
und `crypton`, und die vollständige Ausgabe des Programms über alle acht Profile.
