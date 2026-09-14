# Sitzungsstart: 00bf (MaR / symbolon), fortgeschrieben nach D362

## Was das hier ist

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Repositorium **`symbolon`**, Gitea (`git.h.error13.de/oli/symbolon`,
LAN-only) und GitHub-Spiegel (`github.com/olisym/symbolon`). Lokaler Ordner bleibt
bewusst `~/mensch-als-republik`. Tagline seit D335: *Symbolon: A Self-Verifying Trust
Layer for Local-First Networks*. Spec-Titel bleibt bewusst *Mensch als Republik* (D317).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Prompts, führst die Abnahmen. Schreibst keinen
Produktivcode.

**Supervisor-Zugriff:** Direkter Klon/Pull über den öffentlichen GitHub-Spiegel. Push-
Mirror, kann hinter Gitea zurückliegen — Commit-Hash vor jedem Lesen gegen den geklonten
`HEAD` prüfen. Der Spiegel liegt regelmässig einen Commit **vor** dem hier genannten Stand,
weil dieser Sitzungsstart sich selbst nicht mitzählt; das ist der Normalfall, kein Fehler.

## Stand

Am Ende von `00be`: **814 Tests**, Register **D1–D362**, Prüfregeln **1–72**, 61 Posten,
`make check` grün, `main` und `origin/main` gleichauf bei `bf8b94f`. **30 Wurzel-Markdown-
Dateien, alle gebunden**; `archiv/` stand bei 126, und mit diesem Sitzungsstart fällt
`sitzungsstart-00be.md` dazu. Ein Branch.

`00be` war eine Spec- und Prüffallrunde: ein Registereintrag, ein Vermerk in `02 §7`, ein
Querverweis an O60, drei neue Prüffälle. Keine Änderung an `symbolon/`.

### Die Schichten

Unverändert seit `00ar` — siehe `arbeitsweise.md`, `pruefregeln.md`, `08-scope.md §3`.

### Der Bestand

Neu: `tests/trust/test_zeitmonotonie.py` (107 Zeilen, drei Prüffälle). Geändert:
`07-decisions.md`, `02-trust-flow.md`, `offen.md`. `symbolon/` ist unangetastet — die
Rücknahmeprobe an `derive.py` wurde zurückgenommen und ist nicht im Baum.

**Ausserhalb des Repositoriums, bei Oli lokal:** `restack-faktensammlung.md`,
`restack-felder-englisch.md`, `prompt-log.py` und `prompt-log-restack.md` in `~/Downloads`.
Bewusst nicht im Baum. Wenn der Antrag vor dem 3. November nachgebessert wird, sind das die
Dateien dafür.

## Was in `00be` entschieden wurde (D362)

Ausgangspunkt waren die zwei Kandidaten aus `00bc`: O61 oder der Trust-Pfad aus `02a §2.6`.
Entschieden wurde für den Trust-Pfad, weil O61 vom selben Typ ist wie die Runde, die in `00bd`
zwei Supervisor-Fehler produziert hat — Fork-Arbeit ohne messbares Zwischenergebnis.

**D362 (der Trust-Wert ist nicht monoton in `now`).** Gemessen, nicht vermutet: bei Profil
TP-02 und einem Anker, der zwei Bürgschaften mit `n = 3` bei `D = 4` hält, springt der Wert
über drei Zeitpunkte von 0 auf 12 und zurück auf 0. Die Mechanik ist die von D118, aber auf
der Zeitachse: Σ `n_budget` ist 6 > 4, also `OVERCOMMITTED_AUTHOR`, und bei
`include_flagged = False` fällt **jede** Kante des Autors. Läuft die frühere Bürgschaft ab,
verlässt sie das Budget-Set — der einzige Austritt, den `02a §2.6` kennt —, das Flag
verschwindet, und die verbleibende Kante trägt wieder.

Drei Folgerungen, alle im Eintrag:

- `02 §7` führt `t_exp` als Abwehr 1 gegen Über-Vertrauen, als strukturelle harte Decke.
  Hier ist `t_exp` die **Ursache** des Anstiegs. Der Vermerk dazu steht jetzt dort.
- Bei `include_flagged = True` ist die Folge monoton fallend. Die Ankerwerte in
  `02-golden-anchors.md §3–§5` gelten bei `True` (`02a §3`) — der Ankersatz konnte das
  strukturell nicht sehen. Das ist die Erklärung für die Abdeckungslücke, nicht eine
  Entschuldigung dafür.
- Kein Defekt. Drei Entscheidungen erzeugen das Verhalten gemeinsam (`02a §2.6` mit D135,
  D40, `02a §2.10`), und keine ist falsch. Festgehalten wird die Folge.

Verworfen und im Register benannt: anteilig kappen statt Alles-oder-Nichts; den
Budget-Austritt über `t_exp` streichen; als Defekt behandeln und reparieren.

**Der Prüffall.** `tests/trust/test_zeitmonotonie.py`, drei Fälle: die Nicht-Monotonie beim
Default, die Monotonie bei `include_flagged = True`, und der Zwischenzustand
(`OVERCOMMITTED_AUTHOR` mit dem richtigen Subjekt beim ersten Zeitpunkt, weg beim zweiten).
Rücknahmeprobe nach Prüfregel 69: mit entfernter Flag-Anwendung in `derive.py` Schritt 5
fällt Fall 1 mit `assert 12 == 0`, Fall 2 und 3 bleiben grün. Damit ist belegt, dass der Test
genau den Pfad sieht, den er sehen soll.

## Der Ablauf, und wo der Fehler diesmal sass

Ungewöhnlich für diese Reihe: das Werkzeug hat sauber geliefert. Es hat den Auftrag
eingehalten, die Werte abgeleitet statt abgetippt, die Rücknahmeprobe korrekt ausgeführt und
berichtet, und den INV-3-Befund als **Meldung** behandelt statt als Bauauftrag — genau so,
wie es die Prompt-Regel verlangt.

Der einzige Defekt im Diff stammte aus dem **Prompt**. Dort stand als Vorbedingung
`PARAMS.D >= 3`, mit der Begründung, `2n > D` sei bei `n <= D` sonst nicht erfüllbar. Das ist
falsch: bei `n = D // 2 + 1` gelten beide Bedingungen für jedes `D >= 1`. Das Werkzeug hat die
Zeile korrekt übernommen, dreimal, samt Begründung. Ersetzt wurde sie durch die tatsächliche
Vorbedingung der Konstruktion — `expected_mid > 0`, einmal in `_szenario()`.

Zwei Dinge, die daran hängen. Erstens: eine falsche Begründung im Prompt wird zu einer
falschen Begründung im Baum, und kein Linter sieht sie. Zweitens: gefunden wurde sie beim
Nachrechnen der Vorbedingung für D=1 bis 8, nicht beim Lesen. Lesen allein hätte gereicht, um
den Satz zu sehen, aber nicht, um ihn als falsch zu erkennen.

## Werkzeugnotizen

- **`stand.py` braucht einen Pfad** auf eine Datei mit der pytest-Ausgabe und gibt ohne
  Argument stumm 1 zurück. Aufruf: `make check > /tmp/check.txt 2>&1`, dann
  `python tools/stand.py /tmp/check.txt`. **Keine Pipe dahinter** — `tail` schluckt den
  roten Status. In `00be` wurde bewusst die Umleitung statt `tee` benutzt, weil am selben
  Block ein Merge hing.
- **`stand.py` meldet den Hash des letzten Commits, nicht den Zustand danach.** Im
  Merge-Block von `00be` stand `26fce87` über einer Ausgabe, die den noch nicht committeten
  Korrekturstand mass. Kein Fehler, aber beim Abschreiben in die Kaltzahlen eine Falle.
- **`stand.py` zählt Zeilen von `git branch -a`**, also Remote-Refs mit. Drei Zeilen heisst
  ein Branch.
- **`splice_run.py` verlangt einen sauberen Baum.** Wird ein Defekt im Diff gefunden, ist der
  Weg `git checkout --` auf die betroffenen Dateien und ein korrigierter Splice, nicht ein
  zweiter Splice obendrauf. In `00be` lief die Korrektur stattdessen als eigener Splice auf
  dem schon committeten Lauf-Branch — das geht, weil der Baum dabei sauber war.
- **Ein Splice-Skript darf mehrfach vorkommende Blöcke entfernen**, muss die Zahl dann aber
  hart prüfen (`count != 3` ist ein Abbruch). Die Zielmuster-Wache aus Prüfregel 65 bleibt
  davon unberührt.
- **Der repomix-Nachzug der Projektkopie steht weiterhin aus**, jetzt zwei Runden.
  Kopfzeile aus den Kaltzahlen: `bf8b94f`, 814 Tests, 362 Registerköpfe, 72 Prüfregeln,
  61 Posten, 3 Branches.

## Offene Punkte, nach Grösse

**Das grösste:** O61 — soll ein uhrloser Knoten überhaupt Vertrauen gewähren können? `01 §5.3`
beantwortet die Lage heute kohärent mit Unter-Vertrauen, aber damit kann ein Knoten ohne Uhr
nichts gewähren. Drei Wege: signierte Zeit-Attestierung (`VISION.md §5`, D350), Wechsel auf die
Verfügbarkeitsseite nach Raytime, oder Scopes ohne `t_exp`. D354 hängt daran. **D362 schärft
die Frage:** ein Knoten ohne verlässliche Uhr ist nicht bloss vorsichtiger als die anderen,
sein Ergebnis ist unbestimmt — es kann in beide Richtungen abweichen.

**Daneben:** O60, die Budget-/Kantensatz-Asymmetrie, jetzt mit einer gemessenen Zahl statt
einer Vermutung; die Richtungsfrage bleibt, aber sie wird nicht erst bei unscharfer Zeit
scharf. D354 selbst mit der Gabel F2 (Verschachtelung als Norm gegen Schnittmenge bei der
Auswertung). O56 (PyPI-Name `symbolon` belegt). O57 (Restack, eingereicht am 10. September,
Frist für Nachbesserung 3. November).

**Ohne Frist:** die Übertragung auf unterbrochene Zustellung (LoRa/Reticulum). Anschlusspunkte
D345, D346, D350, D353, D361, jetzt D362.

**Ungeklärt aus `00be`:** die Invariantentabelle `02a §7` kennt keine Zeitaussage. INV-3
spricht über das Entfernen von Kanten. Ob D362 dort eine Zeile braucht — und ob sie die
Nicht-Monotonie festschreibt oder nur die Richtung, in der sie auftreten darf —, ist nicht
entschieden. Kein O-Posten, weil noch nicht klar ist, ob es eine Frage oder nur eine
Redaktionsaufgabe ist.

## Der nächste Schritt

**O61** ist jetzt der klare Kandidat. Die Runde, die ihn verdrängt hat, ist abgeschlossen, und
sie hat ihm eine Zahl mitgebracht: Uhrversatz erzeugt nicht Unter-Vertrauen, sondern
Unbestimmtheit. Wenn O61 drankommt, dann mit Prüfregel 72 von Anfang an und mit `VISION.md §5`,
D350 und D362 vorher aufgeschlagen.

Zwei kleinere Züge, falls eine Runde mit messbarem Ergebnis vorgezogen werden soll: die
INV-3-Frage oben, und der repomix-Nachzug, der jetzt zwei Runden hinterherhinkt.
