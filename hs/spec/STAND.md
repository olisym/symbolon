# Stand dieser Spec-Kopie

Diese Kopie ist der eingefrorene Anker für die dritte Implementierung: Layer 02 in Haskell
(D367, D368, D370, D371). Sie ist keine Arbeitskopie. Wer sie verschiebt, braucht einen
Registereintrag.

- Quelle: `git.h.error13.de/oli/symbolon`, gespiegelt auf `github.com/olisym/symbolon`
- Commit: `764f0da`
- Datei: `01-claim-atom.md`, Blob: `41016c8a5c8fb87cb113f85e70b1501eda5defa8`
- Datei: `02-trust-flow.md`, Blob: `c16d1316516dc065abb6f613ef5d10843f01c1d6`

Die Blobs werden geprüft mit `git hash-object spec/01-claim-atom.md` und
`git hash-object spec/02-trust-flow.md`; die Vergleichswerte stehen oben. Im Hauptrepo liefert
`git show 764f0da:02-trust-flow.md` dieselben Bytes.

Der benannte Commit wandert nicht mit. Der Text in der Wurzel des Hauptrepos läuft weiter; diese
Kopie tut es nicht. Sie nachzuziehen ist ein Registerakt, kein Nachzug nebenbei.

## Was hier bewusst fehlt

`02-golden-anchors.md` und `02a-maxflow-prompt.md` sind **zurückgehalten**. Die Ankerdatei trägt
die Antworten, und der Prompt-Anhang nimmt genau die Mehrdeutigkeiten vorweg, deren Auffinden der
Zweck dieser Fassung ist. Das Fehlen ist kein Versehen und wird nicht nachgereicht.

Wer eine Stelle für mehrdeutig hält, entscheidet sie nach bestem Verständnis, hält die
Entscheidung fest und schreibt die Stelle in die Fragenliste. Die Fragenliste ist Ergebnis, nicht
Nebenprodukt.

## Der Umfang

Layer 01 als Voraussetzung, Layer 02 als Gegenstand. Gebaut werden die Zustandsklassifikation,
die Gruppen- und Budgetstufe und der Graphbau. Der Max-Flow kommt aus einer Bibliothek und wird
nicht selbst geschrieben; normativ ist die Konstruktion des Graphen, nicht der Solver.

Eine Fassung mit anderem Umfang braucht einen eigenen Anker.
