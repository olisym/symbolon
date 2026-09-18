# Sitzungsstart: 00ca (MaR / symbolon), fortgeschrieben nach D411

## Was das hier ist

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Repositorium **`symbolon`**, Gitea (`git.h.error13.de/oli/symbolon`,
LAN-only) und GitHub-Spiegel (`github.com/olisym/symbolon`). Lokaler Ordner bleibt
bewusst `~/mensch-als-republik`. Tagline seit D335: *Symbolon: A Self-Verifying Trust
Layer for Local-First Networks*. Spec-Titel bleibt bewusst *Mensch als Republik* (D317).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Aufträge, führst die Abnahmen. Schreibst keinen
Produktivcode.

**Supervisor-Zugriff:** Direkter Klon/Pull über den öffentlichen GitHub-Spiegel. Commit-Hash
vor jedem Lesen gegen den geklonten `HEAD` prüfen. Der Spiegel liegt regelmässig einen Commit
**vor** dem hier genannten Stand, weil dieser Sitzungsstart sich selbst nicht mitzählt.

## Stand

Am Ende von `00ca`: **911 Tests**, Register **D1–D411**, Prüfregeln **1–77**, `make check` grün,
`main` bei `03820d5`. **32 Wurzel-Markdown-Dateien, alle gebunden**; `archiv/` steht bei 137, und
mit diesem Sitzungsstart fällt `sitzungsstart-00bz.md` dazu. `offen.md` führt **73 Posten**; O62
ist in dieser Sitzung geschlossen, O73 eröffnet worden.

**Stränge:** `main` und `00bo-hs` (kontaminiert, D374, wird nicht gelöscht). Dazu
`o70-uhrversatz-pin`, `o72-intervall-now` und `d410-zeitinvarianten`, alle gemergt und stehen
gelassen.

## Was in dieser Sitzung geschah

### D409 — O62 geschlossen, O73 eröffnet

Der nächste Schritt aus `00bz` („O62 lesen, die Sprachfrage vorbereiten") war veraltet: die
Sprache steht seit D370 und D382, der Rust-Lauf ist seit D390 abgenommen, die Folgeposten O65 bis
O69 sind zu. Der Satz war aus `00by` ungeprüft mitgewandert. O62 ist geschlossen. O73 hält fest,
dass der Rust-Anker auf `15d091e` steht und seither sechs Änderungen an `02` (D394, D396, D398,
D400, D402, D406) und eine an `01` (D396) ungelesen sind. Dazu kommt die Frage, ob D368s
Zurückhaltung von `02a` nach D397 noch wirkt. Kein Lauf, solange der Stolperdraht nicht auslöst.

### D410 und D411 — Zeitaussagen in der Invariantentabelle

Der Posten „ungeklärt aus `00be`" ist erledigt. Invarianten bleiben in
`02-golden-anchors.md §8`; `02` bekommt keinen Abschnitt, weil Invarianten abgeleitet sind und
D397 nur Normen verschoben hat. Neu sind **INV-9** (bei `include_flagged = True` steigt der Wert
nie mit der Uhr; Prämisse: Gültigkeit hat nur eine obere Zeitgrenze) und **INV-10** (ein weiteres
Fenster senkt den Wert und hebt die Schranke; bei `True` fallen beide auf die Ränder). Beide
vorab im Supervisor-Klon gemessen, dann als `tests/trust/test_zeitinvarianten.py` gebaut,
13 Tests. Die Rücknahmeprobe trennt nur am D362-Szenario bei `False`; das Szenario muss im Test
bleiben.

## Werkzeugnotizen

- **Cursor am Host, frischer Thread je Auftrag.** In dieser Sitzung lief einmal der alte
  O72-Thread weiter und berichtete über den erledigten Auftrag. Ursache war ein nicht gelaufener
  Lieferblock: ohne Spec-Commit gab es keine Basis. Der Auftrag prüft jetzt im ersten Schritt die
  Commit-Meldung von `main`; das hätte den Lauf angehalten.
- **Erledigte Aufträge aus `~/auftraege/` wegschieben**, damit das Werkzeug sie nicht greift.
- **`git --no-pager diff`** in allen Blöcken, sonst wartet `less` auf eine Taste.
- **Das Werkzeug tippt Diffs gelegentlich ab**, statt sie zu kopieren (O72-Bericht, `tpuhr.py`).
  Die Abnahme liest den Branch im Spiegel, nie den Diff im Bericht.
- **Der Supervisor-Klon ist flach.** `git ls-remote origin 'refs/heads/*'` zeigt den wahren
  Stand; vollständig holen mit `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`. Für
  Messungen im Klon braucht es `cbor2`, `cryptography`, `pytest` und `hypothesis`.
- **Lieferungen laufen über `/tmp`**, als ein Block mit Hashprüfung von Lieferung und Basis,
  Marken `== NAME ==` und Schlussmarke `== FERTIG ==`.

**Prüfregel-Kandidaten, weiter nicht übernommen:**
- Einen Abschnitt ganz lesen, bevor man aus einem Satz darin schliesst (D392 → D394).
- An zwei Fällen Gemessenes nicht „durchgehend" nennen (D390 → D396).
- Eine Karte aus Wortsuche ist eine Vermutung; vor dem Schreiben den Wortlaut lesen (D397 → D398).
- Eine Flächenzeile, die vor dem Lesen des Codes geschrieben wird, ist eine Schätzung (D408).
- **Neu aus D409:** der nächste Schritt eines Sitzungsstarts wird gegen `offen.md` und das Ende
  des Registers geprüft, bevor er fortgeschrieben wird. Einmal begründet.

## Offene Punkte, nach Grösse

**Merkposten Restack:** eingereicht am 10. September, Code `2026-11-0c4` (D349). Bewertet wird
nach der Frist am 3. November. **Mitte Oktober** den Antragstext gegen den Stand halten und
entscheiden, ob nachgebessert wird. Wie das Portal eine Aktualisierung abwickelt, ist nicht
geklärt.

**O73** — der zweite Zeuge liest einen überholten Text. Stolperdraht, kein Lauf.

**Daneben:** D354 mit der Gabel F2. O56 (PyPI-Name belegt).

**Ohne Frist:** die Übertragung auf unterbrochene Zustellung (LoRa/Reticulum). Anschlusspunkte
D345, D346, D350, D353, D361, D362, D363, D404, D406.

**Aus D408 getragen:** die Zahl der Auswertungen über ein Fenster hängt am Bestand und hat keine
Obergrenze; beisst es je, gehört die Grenze nach `02 §8` und nicht in die Rechenregel.
`include_flagged = True` über ein Fenster ist seit D411 durch INV-10 gedeckt.

## Der nächste Schritt

Kein Bau steht an. Vor Mitte Oktober: `offen.md` durchsehen, ob ein Posten ohne Stolperdraht
reif ist, und D354 mit der Gabel F2 lesen. Ab Mitte Oktober: der Restack-Antrag gegen den Stand.
Vor dem Fortschreiben dieses Schritts gilt der Kandidat aus D409 — gegen `offen.md` und das
Register-Ende prüfen.
