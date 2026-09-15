# Stand dieser Spec-Kopie

Diese Kopie ist der eingefrorene Anker für die Rust-Fassung von Layer 02 — die dritte Fassung
dieses Layers nach zwei Haskell-Fassungen (D367, D368, D371, D382, D383). Sie ist keine
Arbeitskopie. Wer sie verschiebt, braucht einen Registereintrag.

- Quelle: das Hauptrepositorium dieses Projekts; die Adresse steht bewusst nicht hier
- Commit: `15d091e`
- Datei: `01-claim-atom.md`, Blob: `41016c8a5c8fb87cb113f85e70b1501eda5defa8`
- Datei: `02-trust-flow.md`, Blob: `2de75f7f357c47777bb5e61ebc0d25e6515185cc`

Die Blobs werden geprüft mit `git hash-object spec/01-claim-atom.md` und
`git hash-object spec/02-trust-flow.md`; die Vergleichswerte stehen oben. Im Hauptrepo liefert
`git show 15d091e:02-trust-flow.md` dieselben Bytes.

Der benannte Commit wandert nicht mit. Der Text in der Wurzel des Hauptrepos läuft weiter; diese
Kopie tut es nicht. Sie nachzuziehen ist ein Registerakt, kein Nachzug nebenbei.

## Was hier bewusst fehlt

`02-golden-anchors.md` und `02a-maxflow-prompt.md` sind **zurückgehalten**. Die Ankerdatei trägt
die Antworten, und der Prompt-Anhang nimmt genau die Mehrdeutigkeiten vorweg, deren Auffinden der
Zweck dieser Fassung ist. Das Fehlen ist kein Versehen und wird nicht nachgereicht.

Der Kasten zu `∞` in `02 §4` verweist für die Ausgestaltung auf `02a §2.8`. Auch dieser Verweis
führt bewusst ins Leere; die Bedingung, die zu erfüllen ist, steht vollständig im Kasten selbst.

Wer eine Stelle für mehrdeutig hält, entscheidet sie nach bestem Verständnis, hält die
Entscheidung fest und schreibt die Stelle in die Fragenliste. Die Fragenliste ist Ergebnis, nicht
Nebenprodukt.

## Nicht derselbe Text, den die Haskell-Fassungen gelesen haben

`hs/spec/` steht auf `764f0da`. `01-claim-atom.md` ist seither unverändert; `02-trust-flow.md`
trägt hier zwei Kästen in `§4`, die dort fehlen:

- **Die Schranke ist eine Kapazität, keine Knotenmenge** (D375). `Grenze` ist nicht der minimale
  Schnitt, und eine leere Schnittmenge ist kein fehlender Engpass.
- **`∞` ist ein Sentinel, kein Wert** (D381), mit Herleitung und einer hinreichenden Schranke.

Das ist gewollt: geprüft wird der heutige Normtext, nicht ein überholter. Es heisst aber, dass
ein Vergleich der drei Läufe an diesen beiden Stellen keine drei unabhängigen Zeugen hat. Wer
die Läufe nebeneinanderstellt, führt das mit.

## Der Umfang

Layer 01 als Voraussetzung, Layer 02 als Gegenstand. Gebaut werden die Zustandsklassifikation,
die Gruppen- und Budgetstufe und der Graphbau. Der Max-Flow kommt aus einer Bibliothek und wird
nicht selbst geschrieben; normativ ist die Konstruktion des Graphen, nicht der Solver.

Eine Fassung mit anderem Umfang braucht einen eigenen Anker.
