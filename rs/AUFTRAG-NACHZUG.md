# Nachzug der Rust-Fassung auf den heutigen Spec-Text

## Lage

In diesem Verzeichnis liegt deine Fassung eines Trust-Flow-Rechners. Sie ist nach `AUFTRAG.md`
gebaut, gegen die Spec-Kopie in `spec/`, und ihre Fragenliste steht in `FRAGEN.md`.

Die Spec-Kopie ist seither nachgezogen worden. `spec/STAND.md` nennt den neuen Stand. Der Text
von `spec/01-claim-atom.md` und `spec/02-trust-flow.md` hat sich geändert.

`AUFTRAG.md` gilt weiter: Umfang, Bibliotheken, Kapazitätstyp `u64`, Eingabeformat,
Schnittstelle, Ausgabeform, Nicht-Ziele. Dieser Auftrag ändert davon nur, was unten steht.

## Auftrag

Bring die Fassung in Übereinstimmung mit dem heutigen Text von `spec/`. Die Spec ist die einzige
Quelle. Es gibt keine Referenzimplementierung, keine weiteren Spec-Dateien und keine Liste der
Änderungen. Welche Stellen sich geändert haben und ob dein Code sie trifft, findest du selbst
heraus.

Wo der heutige Text deiner früheren Lesart widerspricht, folgt der Code dem Text. Hältst du die
frühere Lesart dennoch für richtig, bekommt der Zweifel einen Frage-Eintrag. Der Code folgt
trotzdem dem Text.

## Eingabe

Zu den drei Dateien aus `AUFTRAG.md` kommt eine vierte:

- `vektoren/zf02.json` — drei Profile, gleiche Struktur

Alle vier Dateien enthalten keine erwarteten Werte. Alle Abfragen laufen weiter so, dass Vouches
geflaggter oder über-committeter Autoren ihre Kante tragen.

## Ein Punkt aus dem ersten Lauf

Dein Eintrag 1 in `FRAGEN.md` nennt im Nebensatz, der Sentinel werde saturierend auf `u64::MAX`
gerechnet. `AUFTRAG.md` verlangt, einen Überlauf zu melden statt abzufangen. Ersetze die
Saturierung: Läuft eine Rechnung über, hält das Programm an und meldet Stelle und Werte.

## Die Fragenliste

`FRAGEN.md` wird fortgeschrieben, nicht neu begonnen. Die bisherigen Einträge 1 bis 13 bleiben
**unverändert**, kein Wort darin wird angefasst. Darunter entsteht ein neuer Abschnitt
`# Nachzug`, dessen Einträge ab 14 weiterzählen. Er kennt drei Arten.

**Fragen**, in der Form aus `AUFTRAG.md`, mit Pflichtadresse:

```
## <n>. <Titel>

- **Adresse:** <kanonisch>
- **Frage:** die Frage, die der Text offenlässt
- **Lesart:** die Lesart, für die entschieden wurde
- **Verworfen:** die verworfene Lesart, und warum
```

**Änderungen.** Je Änderung am Verhalten des Programms ein eigener Eintrag. Eine Änderung, die
zwei Stellen der Spec folgt, bekommt einen Eintrag mit beiden Adressen. Zwei Änderungen, die
derselben Stelle folgen, bekommen zwei Einträge.

```
## <n>. Änderung: <Titel>

- **Adresse:** <kanonisch>
- **Vorher:** was das Programm tat
- **Jetzt:** was es tut
- **Grund:** was an der Adresse die Änderung verlangt, in eigenen Worten
```

Kannst du für eine Änderung keine Adresse nennen, ist das kein Grund, sie wegzulassen. Schreib
den Eintrag mit `**Adresse:** keine` und begründe im Feld `Grund`, warum sie nötig war.
Refaktorierungen ohne Wirkung auf die Ausgabe brauchen keinen Eintrag.

**Die alten Einträge.** Am Ende des Abschnitts eine Liste `## Einträge 1 bis 13`, je alter
Eintrag eine Zeile:

```
- <n>: beantwortet (<Adresse>) | offen | widerlegt — ein Satz
```

`beantwortet` heisst, der heutige Text entscheidet die Frage, und die Adresse nennt, wo.
`widerlegt` heisst, die Frage beruhte auf einer falschen Beobachtung.

Jede Abweichung von einer Spec-Angabe bekommt einen eigenen Eintrag. Ein Nebensatz in einem
anderen Eintrag zählt nicht als Meldung.

Die Adressform aus `AUFTRAG.md` gilt unverändert.

## Nicht-Ziele

- Alles aus `AUFTRAG.md`, unverändert.
- Keine Änderung an den Einträgen 1 bis 13 von `FRAGEN.md`.
- Keine Änderung an `spec/`, an `vektoren/`, an `AUFTRAG.md` und an dieser Datei.
- Kein Umbau ohne Anlass im Text. Was nur schöner würde, bleibt, wie es ist.
- Keine Saturierung, nirgends. Kein Abfangen eines Überlaufs.
- Keine Anpassung der Ausgabe an vermutete Erwartungen.
- Kein Entfernen von Ausgabezeilen, Tests oder Prüfungen, das nicht eine Änderung mit eigenem
  Eintrag ist. Ein ungefragtes Entfernen ist wie ein ungefragter Zuwachs zu melden.

## Abschluss

Ein Commit in diesem Verzeichnis. Kein Merge.

Der Bericht nennt:

- den vollständigen `git diff` gegen den Commit vor diesem Lauf, ungekürzt;
- die Zahl der eigenen Tests vorher und nachher;
- die Zahl der neuen Einträge in `FRAGEN.md`, getrennt nach Fragen und Änderungen;
- die Zeilen der Liste `Einträge 1 bis 13`;
- die vollständige Ausgabe des Programms über alle vier Eingabedateien, ungekürzt.
