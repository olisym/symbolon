# AGENTS.md — stehende Regeln für das ausführende Werkzeug

Diese Datei gilt für jedes Werkzeug, das in diesem Repositorium einen Auftrag ausführt (D421). Sie
trägt Verfahren, keine Norm und keinen Auftrag.

## 1. Geltung

- **Was gebaut wird, steht allein im Auftrag.** Diese Datei erweitert keinen Auftrag, sie
  beschränkt nur, wie er ausgeführt wird. Was der Auftrag nicht nennt, wird nicht gebaut.
- **Der Auftrag geht vor.** Widerspricht er dieser Datei, gilt der Auftrag, und der Widerspruch
  steht im Bericht.
- **Die normative Wahrheit** steht in den Layer-Dateien und in `07-decisions.md`. Sie wird
  zitiert, nicht ausgelegt. Eine Lücke oder ein Widerspruch dort ist ein Befund, keine Einladung.

## 2. Vor der ersten Änderung

- Branch und Basis-Commit aus dem Auftrag prüfen. Weichen sie ab: abbrechen und melden.
- Jede Datei, die der Auftrag nennt, ganz lesen, bevor eine davon geändert wird.

## 3. Während des Laufs

- **Melden, nicht anpassen.** Widerspricht eine Messung dem Auftrag oder der Spec, wird das
  gemeldet. Kein Golden Anchor, kein Vektor und keine bestehende Erwartung wird nachgezogen, um
  einen Test grün zu bekommen.
- **Kein stiller Scope-Zuwachs.** Die Nicht-Ziele des Auftrags sind verbindlich. Was nötig
  scheint und nicht beauftragt ist, steht im Bericht, nicht im Diff. Das gilt auch für
  Hilfsfunktionen, Parameter und Abkürzungen, die weder Spec noch Auftrag nennt.
- **Erwartete Werte werden abgeleitet, nicht getippt** — aus Signaturen, Vektordateien und
  Spec-Tabellen. Eine getippte Menge veraltet still.
- **Rücknahmeprobe.** Wo ein Regressionstest entsteht: die Reparatur zurücknehmen, bestätigen,
  dass der Test rot wird, die Reparatur wiederherstellen. Ein Regressionstest, der die Regression
  nicht sieht, ist keiner.
- **Rückfragen werden nicht unterwegs entschieden.** Sie stehen als Liste am Ende des Berichts.
  Blockiert eine den Lauf, wird abgebrochen und gemeldet.
- Docstrings nennen den Abschnitt, auf dem der Code beruht, in der Form `NN §X.Y`.

## 4. Prüfen

- Vor dem Commit läuft `make check` und ist grün. Tests laufen als `python -m pytest -q` im
  Projekt-Interpreter, nie als bares `pytest`.
- `git add` mit expliziten Pfaden, nie `-A`. Neue Dateien werden vor `make check` hinzugefügt.
- In Markdown-Dateien: Prosa bricht bei 100 Zeichen, Umlaute ausgeschrieben, keine Escapes, Bytes
  als `h'ff'`.

## 5. Abschluss

- **Ein Commit auf dem Auftrags-Branch. Kein Merge, kein Push.**
- Der Bericht enthält den **vollständigen** `git diff` gegen den Basis-Commit, nicht `--numstat`
  und keine Zusammenfassung; das Ergebnis von `make check`; jede Meldung aus §3; jede Stelle, an
  der dem Auftrag nicht zu folgen war.
- Der Bericht ist nicht die Abnahme. Geprüft wird der Diff.

## 6. Diese Datei

- Sie ändert sich nur mit einem Eintrag in `07-decisions.md`.
- Sie nennt keine Einzelheit der Implementierung. Auch ein Zeugenlauf, der unabhängig vom
  bestehenden Code bleiben muss, liest sie (D389).
