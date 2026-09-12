# Prompt 00at — O55, Umbenennung `mensch_als_republik` → `symbolon`

## Modus

**Kein Prototyp.** D311 gilt hier nicht — das ist eine reguläre, dauerhafte Änderung nach D317
(Namensentscheidung) und D329/D330 (Nachbarposten geschlossen). Normale Sorgfalt, normale
Abnahme: Golden Numbers, ein Rücknahmeproben-Ersatz über die volle Testsuite (siehe unten),
vollständiger `git diff`.

Erfinde nichts still. Eine Entscheidung, die weder Spec noch Prompt hergibt: **triff sie,
markiere sie im Bericht als Befund, begründe sie.**

## Branch und Basis

Branch `00at-umbenennung`, abgezweigt vom Kopf von `main` (lies den tatsächlichen Kopf zu
Beginn, nenne ihn im Bericht). Ein Commit am Ende, kein Merge.

## Normative Grundlage

`07-decisions.md`: **D317** (Namensentscheidung: `symbolon`, Ausführung ist `O55`), **D329**
(Sprache — nicht betroffen von diesem Lauf), **D330** (mar-go-Repositorium — nicht betroffen).
`offen.md`: **O55**, **O56** (PyPI-Name belegt — irrelevant für diesen Lauf, betrifft nur eine
künftige Veröffentlichung).

**Korrektur zu O55 selbst (Prüfregel 27 — vor dem Bauen geprüft, nicht übernommen).** O55s
eigener Text nennt `LAYER_FILES` (`tools/check_specs.py`) als betroffen. Das ist falsch:
`LAYER_FILES` ist eine Zuordnung Layer-Präfix → Spec-Dateiname (`00-nucleus-genesis-
constitution.md` usw.) und hat mit dem Python-Paketnamen nichts zu tun. **`LAYER_FILES` bleibt
unverändert.** Diese Korrektur selbst braucht keinen eigenen Registereintrag — sie ist Teil
dieses Prompts und wird im Abnahme-Eintrag miterwähnt.

## Was gemessen wurde, bevor gebaut wird (Prüfregel 63)

Vorabmessung (Sandbox-Klon des Supervisors, gegen `main`):

- 102 `.py`-Dateien importieren `mensch_als_republik` (`grep -rl` über den ganzen Baum).
- Ausserhalb reiner Importe referenzieren `mensch_als_republik`/`mensch-als-republik` als Text:
  `arbeitsweise.md`, `README.md`, `sitzungsstart-00ar.md` (Repositoriumsname/-pfad, **nicht**
  Paketname — siehe Nicht-Ziele), sowie **`03-profiles.md`** (Layer-Datei!) und
  **`04-prompt.md`, `01a-policy-prompt.md`, `02a-maxflow-prompt.md`, `04a-korrektur-prompt.md`,
  `03-prompt.md`** (aktive, gebundene Prompt-Dateien) mit Codepfad-Zitaten wie
  `mensch_als_republik/profiles/` oder `mensch_als_republik/domains.py`.
- 77 Treffer liegen unter `archiv/` — historische, nicht mehr aktive Prompt-Dateien.
- `pyproject.toml` trägt kein `[build-system]` — das Projekt wird nicht editable installiert,
  `pytest` läuft über `pythonpath = ["."]`. Eine Paket-Neuinstallation ist **nicht** nötig.
- `Makefile` referenziert den Namen zweimal (Ruff-Ziel, `egg-info`-Aufräumzeile).

Prüfe das nach, bevor du beginnst — der Stand kann sich seit diesem Prompt geändert haben.

## Was gebaut wird

1. **Verzeichnis.** `git mv mensch_als_republik symbolon` (erhält Historie je Datei).

2. **Importe und Codereferenzen.** In allen `.py`-Dateien ausserhalb von `archiv/` und `go/`:
   `mensch_als_republik` als Python-Bezeichner (Import, `from X import Y`, vollqualifizierte
   Aufrufe) → `symbolon`. Das schliesst `symbolon/` selbst, `tests/`, `tools/` ein.

3. **`pyproject.toml`.** `name = "mensch-als-republik"` → `name = "symbolon"`. Sonst
   unverändert — `O56` (PyPI-Kollision) ist kein Hindernis für den lokalen Namen.

4. **`Makefile`.** Beide Vorkommen (`ruff check ...`, `egg-info`-Zeile) mitziehen.

5. **Aktive Spec- und Prompt-Dateien, Codepfad-Zitate.** In `03-profiles.md` (Layer-Datei —
   **normale Sorgfalt, keine stille Bedeutungsänderung**, nur der Pfad ändert sich, der Satz
   drumherum bleibt), `04-prompt.md`, `01a-policy-prompt.md`, `02a-maxflow-prompt.md`,
   `04a-korrektur-prompt.md`, `03-prompt.md`: `mensch_als_republik/...`-Pfadzitate auf
   `symbolon/...` ziehen. Prüfe jede Fundstelle einzeln (Prüfregel 27) — es sind Codepfade,
   keine Fliesstext-Erwähnungen des Projektnamens.

6. **`README.md`.** Die Zeile, die `mensch_als_republik/`, `tests/`, `tools/` als
   Verzeichnisse der Referenzimplementierung nennt, auf `symbolon/` ziehen. Die Reponame-Sätze
   (Repositoriumsname, Klon-URL) **nicht** anfassen — das ist Nicht-Ziel 2.

## Die Prüfung

- `grep -rln "mensch_als_republik" --include="*.py" .` ausserhalb von `archiv/` und `go/`:
  **leer**.
- `grep -rn "mensch_als_republik" 03-profiles.md 04-prompt.md 01a-policy-prompt.md
  02a-maxflow-prompt.md 04a-korrektur-prompt.md 03-prompt.md README.md`: **leer**.
- `test -d symbolon && test ! -d mensch_als_republik`.
- `git diff --stat -- archiv/ go/ 07-decisions.md`: **leer** — keine dieser drei darf sich
  ändern.
- Volle Testsuite unverändert in der Zahl: **797 bestanden**, nicht mehr, nicht weniger (eine
  reine Umbenennung ändert kein Verhalten). Das ist der Rücknahmeproben-Ersatz für diesen Lauf:
  ein abweichender Wert ist der Befund, keine Zahl wird nachgezogen, um 797 zu erzwingen.
- `python tools/check_specs.py`: weiterhin sauber, Register unverändert (dieser Lauf schreibt
  nicht in `07-decisions.md`).

## Nicht-Ziele

1. **`archiv/`, `07-decisions.md`, `go/` bleiben unangetastet.** Historische Prompt-Dateien
   beschreiben einen vergangenen Stand korrekt — sie umzuschreiben wäre Geschichtsfälschung
   (vgl. D324: alte Prompt-Dateien bleiben mit bekannten Fehlern liegen, aus demselben Grund).
   `go/spec/STAND.md` ist ein eingefrorener Anker (D290, D294, D302) und hängt an Commit- und
   Blob-Hashes des **Hauptrepositoriums**, nicht am Paketnamen — trotzdem: nicht anfassen, das
   ist ausdrücklich nicht Teil dieses Auftrags.
2. **Kein Server-Vorgang.** Die Umbenennung des Gitea- und GitHub-Repositoriums (`git.h.error13.de`,
   `github.com/olisym/...`) läuft separat, ausserhalb von Git, durch Oli. Dieser Lauf ändert
   keine Remote-URLs, keine `arbeitsweise.md`-Sätze über den Klon-Pfad, keine
   `sitzungsstart-00ar.md`. Wenn der Server-Umzug ansteht, ist das ein eigener, späterer Schritt.
3. **`O56` wird nicht bearbeitet.** Kein PyPI-Ausweichname, keine Veröffentlichung.
4. **Kein `[build-system]` und keine `pip install`-Änderung.** Das Projekt bleibt, wie es ist:
   `pythonpath`-basiert, nicht editable installiert.
5. **Kein Merge, kein Push nach `main`.**

## Abschluss

Ein Commit auf `00at-umbenennung`. `git add` mit expliziten Pfaden (kein `-A`).

Melde:

1. Die Ergebnisse der Prüfungen von oben, mit Zahlen (Testanzahl, `check_specs.py`-Ausgabe
   gekürzt, die drei Grep-Proben).
2. Jede Stelle, an der du auf eine mehrdeutige Fundstelle gestossen bist (Fliesstext vs.
   Codepfad) und wie du entschieden hast.
3. Ob `git diff --stat -- archiv/ go/ 07-decisions.md` tatsächlich leer war.
4. Den vollständigen `git diff` gegen den Branchpunkt (wird lang — das ist normal bei einer
   Umbenennung über ~100 Dateien; keine Kürzung, das bleibt Abnahmegrundlage).

Wenn eine Fundstelle nicht eindeutig Codepfad oder Fliesstext ist, ist der benannte Abbruch mit
Begründung das bessere Ergebnis als eine geratene Entscheidung.
