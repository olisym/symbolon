# Stand dieser Spec-Kopie

Diese Kopie ist der eingefrorene Anker für die Rust-Fassung von Layer 02. Sie ist keine
Arbeitskopie. Wer sie verschiebt, braucht einen Registereintrag.

- Quelle: das Hauptrepositorium dieses Projekts; die Adresse steht bewusst nicht hier
- Commit: `573db57`
- Datei: `01-claim-atom.md`, Blob: `e90e4ed63837e0b40aa639b99c7bb007772e038d`
- Datei: `02-trust-flow.md`, Blob: `2ba6ed826a6fb822c9795e12e6a768e3d7b5986d`

Die Blobs werden geprüft mit `git hash-object spec/01-claim-atom.md` und
`git hash-object spec/02-trust-flow.md`; die Vergleichswerte stehen oben. Im Hauptrepo liefert
`git show 573db57:02-trust-flow.md` dieselben Bytes.

Der benannte Commit wandert nicht mit. Der Text in der Wurzel des Hauptrepos läuft weiter; diese
Kopie tut es nicht. Sie nachzuziehen ist ein Registerakt, kein Nachzug nebenbei.

## Vorheriger Anker

Die Fassung wurde auf `15d091e` gebaut (D368). Dieser Anker ist nachgezogen, nicht ersetzt: Der
Code aus dem ersten Lauf und seine Fragenliste bleiben Beleg dafür, was damals gelesen wurde. Die
Kopie auf `15d091e` ist in der Historie dieses Verzeichnisses erhalten.

## Was hier bewusst fehlt

`02-golden-anchors.md` und `02a-maxflow-prompt.md` sind **zurückgehalten**. Die Ankerdatei trägt
die Antworten. Der Implementierungsauftrag nimmt Mehrdeutigkeiten vorweg, deren Auffinden der
Zweck dieser Fassung ist. Das Fehlen ist kein Versehen und wird nicht nachgereicht.

`02 §11` nennt `02a` als Herkunft seiner Normen. Was dort normativ war, steht seither in `§11`,
und nur `§11` gilt. Die Verschiebung ist gewollt: geprüft wird der heutige Normtext, auch wenn er
damit mehr sagt als der Text, den der erste Lauf gelesen hat.

Wer eine Stelle für mehrdeutig hält, entscheidet sie nach bestem Verständnis, hält die
Entscheidung fest und schreibt die Stelle in die Fragenliste. Die Fragenliste ist Ergebnis, nicht
Nebenprodukt.

## Der Umfang

Layer 01 als Voraussetzung, Layer 02 als Gegenstand. Gebaut werden die Zustandsklassifikation,
die Gruppen- und Budgetstufe und der Graphbau. Der Max-Flow kommt aus einer Bibliothek und wird
nicht selbst geschrieben; normativ ist die Konstruktion des Graphen, nicht der Solver.

Eine Fassung mit anderem Umfang braucht einen eigenen Anker.
