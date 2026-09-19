# Sitzungsstart: 00cc (MaR / symbolon), fortgeschrieben nach D422

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

Am Ende von `00cc`: **918 Tests**, Register **D1–D422**, Prüfregeln **1–77**, `make check` grün,
`main` beim Commit, der D422 und diesen Sitzungsstart trägt. **33 Wurzel-Markdown-
Dateien, alle gebunden** — neu ist `AGENTS.md` (D421); `archiv/` steht bei 139, und mit diesem
Sitzungsstart fällt `sitzungsstart-00cb.md` dazu. `offen.md` führt **75 Posten**, davon 44 offen;
O43 bis O49 sind in dieser Sitzung geschlossen worden, Sektion C ist leer.

**Stränge:** `main` und `00bo-hs` (kontaminiert, D374, wird nicht gelöscht). Dazu
`o70-uhrversatz-pin`, `o72-intervall-now`, `d410-zeitinvarianten` und `o9-anhang-c-bindung`,
alle gemergt und stehen gelassen. Diese Sitzung hat direkt auf `main` gearbeitet, ohne Lauf.

## Was in dieser Sitzung geschah

Eine Hygienerunde über Sektion C von `offen.md`, alle Änderungen als Splice des Supervisors.

### D417 und D418 — O43, O48, O49; Marken je Prüfgruppe

O43: die zwei Verweise zeigen in `03-golden-anchors.md`, nicht ins Leere; die Kurzform `03` ist
nicht injektiv. O48 getragen, weil die Grenze laut meldet. O49 gegenstandslos, solange `main`
grün ist: `check_specs` prüft die Zeilenlänge absolut, die Basiszahl ist in der Wurzel null.
D418 schreibt `HASH` und `BASIS` in `arbeitsweise.md §5`.

### D419 und D420 — O44, O45, O46; Drift an D325

O44 und O45: Archiv wird nicht nachgezogen. O46: `repomix.config.json` schliesst `.claude/**`
aus, gemessen mit repomix 1.18.0. Beim Lesen dafür gefunden und in D420 nachgezogen: die alte
Spiegel-URL in `arbeitsweise.md`, der Projektkopie-Abschnitt und Prüfregel 43, die beide noch
den Pflichtnachzug aus D224 beschrieben.

### D421 — O47: `AGENTS.md`

Die Prämisse war falsch: eine unversionierte `.cursorrules` lag seit Juli im Arbeitsbaum, von
Cursor gelesen, vom Register nie genannt, inhaltlich vor-Register. Ersetzt durch eine versionierte
`AGENTS.md`, gehärtet gegen den Einwand aus D218. **Jeder Prompt nennt ab jetzt `AGENTS.md` in
einer Zeile** und wiederholt die stehenden Regeln nicht. Die alte Datei liegt als
`/tmp/cursorrules-alt` beim Operator, bis der erste Lauf unter `AGENTS.md` sauber war.

### D422 — `ls` ist `eza`

Eine Messung ist an `ls -t` gescheitert; beim Operator ist `ls` `eza`, und `-t` heisst dort
etwas anderes. Steht jetzt in `arbeitsweise.md §5`.

## Werkzeugnotizen

- **Der nächste Cursor-Auftrag ist der erste unter `AGENTS.md`.** Im Bericht festhalten lassen,
  ob die Datei geladen war. Läuft ein Auftrag in Claude Code: `CLAUDE.md` mit `@AGENTS.md`
  (Stolperdraht aus D421).
- **Lieferungen:** in `/tmp`, Hashprüfung von Lieferung und Basis vor jeder Änderung, `rm` als
  letzter Job vor `== FERTIG ==` (`arbeitsweise.md §5`, D414, D418).
- **Splice-Anker enden am Zeilenende.** Ein Anker, der mitten in einer Zeile endet, hängt den
  Rest der Zeile an die Ersetzung; der Harness hat das in D419 zweimal als zu lange Zeile
  gefangen.
- **Merge und Push** als eigene Befehle ausserhalb des Blocks.
- **Cursor am Host, frischer Thread je Auftrag.** Der Auftrag prüft im ersten Schritt die
  Commit-Meldung von `main`. Erledigte Aufträge liegen in `~/auftraege/erledigt/`; dort liegt
  bisher einer, die älteren stehen in `archiv/`.
- **`git --no-pager`** in allen Blöcken.
- **Der Supervisor-Klon ist flach.** Vollständig holen mit
  `git fetch origin '+refs/heads/*:refs/remotes/origin/*'` oder `git fetch --unshallow`. Vor
  jedem `checkout` die eigenen Entwürfe verwerfen (`git checkout -- .`).

**Prüfregel-Kandidaten, weiter nicht übernommen:**
- Einen Abschnitt ganz lesen, bevor man aus einem Satz darin schliesst (D392 → D394).
- An zwei Fällen Gemessenes nicht „durchgehend" nennen (D390 → D396).
- Eine Karte aus Wortsuche ist eine Vermutung; vor dem Schreiben den Wortlaut lesen (D397 → D398).
- Eine Flächenzeile, die vor dem Lesen des Codes geschrieben wird, ist eine Schätzung (D408).
- Der nächste Schritt eines Sitzungsstarts wird gegen `offen.md` und das Register-Ende geprüft,
  bevor er fortgeschrieben wird (D409).
- Ein Strang, den ein Sitzungsstart über mehr als eine Sitzung trägt, hat eine O-Nummer oder
  einen Registereintrag, auf den er zeigt (D412).
- Die englische Schale nennt keine Zahl, die mit der Arbeit wächst (D415).
- **Neu aus D421:** die Prämisse eines Postens wird gemessen, bevor er entschieden wird. O47
  stand seit D218 auf „es gibt keine", und es gab eine.
- **Neu aus D420:** eine Beschreibung, die eine Zahl aus einem anderen Eintrag wiederholt,
  veraltet mit ihm; ein Verweis statt der Zahl.

## Offene Punkte, nach Grösse

**Merkposten Restack:** eingereicht am 10. September, Code `2026-11-0c4` (D349). Bewertet wird
nach der Frist am 3. November. **Mitte Oktober** den Antragstext gegen den Stand halten und
entscheiden, ob nachgebessert wird; README (D415) und `AGENTS.md` (D421) werden mitgelesen. Wie
das Portal eine Aktualisierung abwickelt, ist nicht geklärt.

**O73** — der zweite Zeuge liest einen überholten Text. Stolperdraht, kein Lauf.

**O74** — Verschachtelung oder Schnittmenge. Stolperdraht, kein Lauf.

**Daneben:** O56 (PyPI-Name belegt).

**Stolperdrähte aus dieser Sitzung:** O48 (der erste absichtliche Listenpunktverweis in
Unterabschnittsform), O49 (ein Splice ausserhalb der Wurzel oder auf rotem `main`), D421
(der erste Auftrag in Claude Code).

**Ohne Frist:** die Übertragung auf unterbrochene Zustellung, geführt als Richtung in D412.

**Aus D408 getragen:** die Zahl der Auswertungen über ein Fenster hängt am Bestand und hat keine
Obergrenze; beisst es je, gehört die Grenze nach `02 §8` und nicht in die Rechenregel.

## Der nächste Schritt

Kein Bau steht an; geprüft gegen `offen.md` und das Register-Ende (D422). Ab Mitte Oktober: der
Restack-Antrag gegen den Stand. Bis dahin ist Stillstand ein gültiger Zustand. Sektion C ist
leer; wer vorher arbeiten will, findet die Anwendungsfragen O3 bis O7 oder die Posten in den
Sektionen dazwischen, die diese Sitzung nicht angesehen hat. Beides ist Wahl, nicht Pflicht.
