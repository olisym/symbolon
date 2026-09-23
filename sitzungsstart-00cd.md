# Sitzungsstart: 00cd (MaR / symbolon), fortgeschrieben nach D436

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

Am Ende von `00cd`: **926 Tests**, Register **D1–D436**, Prüfregeln **1–79**, `make check` grün,
`main` beim Commit, der D436 und diesen Sitzungsstart trägt. **33 Wurzel-Markdown-Dateien, alle
gebunden**; `archiv/` steht bei 140, und mit diesem Sitzungsstart fällt `sitzungsstart-00cc.md`
dazu. `offen.md` führt **75 Posten**, davon **16 offen**; 28 sind in dieser Sitzung geschlossen
worden. Sektion A ist leer, von Sektion B stehen nur noch die bewusst vertagten Posten und O25.

**Stränge:** `main` und `00bo-hs` (kontaminiert, D374, wird nicht gelöscht). Dazu die gemergten
und stehen gelassenen `o70-uhrversatz-pin`, `o72-intervall-now`, `d410-zeitinvarianten`,
`o9-anhang-c-bindung` und neu `00cd-messauftrag`.

## Was in dieser Sitzung geschah

Eine Triage über die offene Liste, Cluster für Cluster, fast alles als Splice des Supervisors;
gemessen wurde meist im eigenen Klon mit Rücknahmeproben, statt einen Lauf zu beauftragen.

- **D423, D424:** Sektion A — die Anwendungsbefunde aus D312 durch das Aufnahmekriterium `08 §3`.
  `OPEN` ist kein negativer Ausgang (`05 §3`, `08 §7`); ein Amendment darf ein deklariertes
  irrevocables Prädikat weglassen, gemessen am Boden (`00 §5.2`, `04 §8`).
- **D425 bis D431:** Sektion B. Von 23 triagierten Posten war mehr als die Hälfte überholt oder
  schon entschieden. Neu normiert: der Sortierschlüssel der Vermerke (`00 §10`, D429). Gefunden:
  die Policy-Epoche in `resolve_state` war ungeprüft (D430).
- **D432:** O10 entschieden — `UNPARSABLE_V` auch bei `ratify@1`, `GV-54`. Dazu der Messauftrag,
  sechs Teile, der erste Lauf unter `AGENTS.md`.
- **D433, D434:** `INV-04.7` und `INV-04.8` waren zweimal falsch gefasst — erst zu eng (zweite
  Stimme und Zweit-Ja entwerten ebenfalls, nicht nur Equivocation), dann zu weit (die
  Urheberregel liess den Widerruf wieder zu). Der Vorbehalt steht jetzt in
  `04-golden-anchors.md §8`: nur der eigene Autor, nur durch einen Zwilling oder eine weitere
  Stimme.
- **D435:** Abnahme des Branches nach zwei Nachläufen, Merge fast-forward.
- **D436:** Prüfregeln 78 und 79.

## Werkzeugnotizen

- **`AGENTS.md` trägt.** Dreimal geladen und befolgt. Eine Grauzone gesehen: der erste Nachlauf
  hat Generator-Schritte gestrichen, die der Auftrag nicht zu streichen verlangte (D434, D435).
  Nächste Aufträge nennen bei Umbauten ausdrücklich, was bleibt.
- **Aufträge liegen ausserhalb des Repos** in `~/auftraege/`, erledigte in `~/auftraege/erledigt/`.
  Der Auftrag prüft im ersten Schritt die Commit-Meldung seines Branches.
- **Messen im Supervisor-Klon lohnt sich.** Eine Rücknahmeprobe dort kostet einen Befehl und hat in
  dieser Sitzung vier Posten ohne Auftrag geschlossen. Umgebung: `pip install
  --break-system-packages cbor2 cryptography pytest hypothesis`, dann `PYTHONPATH=$PWD`; das Paket
  lässt sich wegen des flachen Layouts nicht installieren.
- **Der Supervisor-Klon ist flach.** Vollständig holen mit
  `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`. Vor jedem Pull oder Checkout eigene
  Entwürfe verwerfen, sonst bricht der Pull ab und der nächste Splice sitzt auf altem Stand.
- **Lieferungen:** in `/tmp`, Hashprüfung von Lieferung und Basis vor jeder Änderung, `rm` als
  letzter Job vor `== FERTIG ==`. Splice-Anker enden am Zeilenende. Merge und Push als eigene
  Befehle. `git --no-pager` in allen Blöcken.
- **Kopfzeilen in `offen.md`** laufen mit „— erledigt (Dnnn)" leicht über 100 Zeichen; dann wird
  der Titel gekürzt und das im Eintrag vermerkt.

**Prüfregel-Kandidaten, weiter nicht übernommen:**
- Einen Abschnitt ganz lesen, bevor man aus einem Satz darin schliesst (D392 → D394).
- An zwei Fällen Gemessenes nicht „durchgehend" nennen (D390 → D396).
- Eine Karte aus Wortsuche ist eine Vermutung; vor dem Schreiben den Wortlaut lesen (D397 → D398).
- Eine Flächenzeile, die vor dem Lesen des Codes geschrieben wird, ist eine Schätzung (D408).
- Der nächste Schritt eines Sitzungsstarts wird gegen `offen.md` und das Register-Ende geprüft
  (D409).
- Ein Strang, den ein Sitzungsstart über mehr als eine Sitzung trägt, hat eine O-Nummer oder
  einen Registereintrag (D412).
- Die englische Schale nennt keine Zahl, die mit der Arbeit wächst (D415).
- Eine Beschreibung, die eine Zahl aus einem anderen Eintrag wiederholt, veraltet mit ihm (D420).
- **Neu aus D435:** ein Lauf, der ungefragt etwas entfernt, ist Scope-Verlust und gehört in den
  Bericht wie ein Zuwachs.

## Offene Punkte

**Die 16 offenen Posten** sind fast alle Wartestände: O31, O34 bis O42 bewusst vertagt, jeder mit
seiner Bedingung; O25 ein Bau ohne Anlass (daran hängt seit D424 auch die Vermeidung von
Ausgang 5); O52, O53 zur Öffnung; O56 (PyPI-Name); O73 und O74 Stolperdrähte.

**Merkposten Restack:** eingereicht am 10. September, Code `2026-11-0c4` (D349), Frist
3. November. Der Operator baut das Projekt nicht darum herum; Mitte Oktober wird nur geprüft, ob
der Antrag den Stand grob falsch beschreibt, und ob sich eine Aktualisierung lohnt. Wie das Portal
sie abwickelt, ist nicht geklärt.

**Aus D408 getragen:** die Zahl der Auswertungen über ein Fenster hängt am Bestand und hat keine
Obergrenze; beisst es je, gehört die Grenze nach `02 §8`.

## Der nächste Schritt

Aus der offenen Liste ist nichts mehr billig zu holen; geprüft gegen `offen.md` und das
Register-Ende (D436). Die nächste Arbeit mit Substanz ist eine Wahl, keine Pflicht: eine der
vertagten Bedingungen prüfen (O41 wartet auf Fragen an `01`, O42 auf einen Befund aus Stufe 2),
die Übertragung auf unterbrochene Zustellung (Richtung aus D412), oder O52/O53 für eine Öffnung.
Stillstand ist ein gültiger Zustand.
