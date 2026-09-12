# Sitzungsstart: 00be (MaR / symbolon), fortgeschrieben nach D360–D361

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
`HEAD` prüfen. In `00bd` lag der Spiegel einen Commit **vor** dem im Sitzungsstart
genannten Stand, weil dieser sich selbst nicht mitzählt; das ist der Normalfall, kein Fehler.

## Stand

Am Ende von `00bd`: **811 Tests**, Register **D1–D361**, Prüfregeln **1–72**, 61 Posten,
`make check` grün, `main` und `origin/main` gleichauf bei `404ff1b`. **30 Wurzel-Markdown-
Dateien, alle gebunden**; `archiv/` stand nach dem Aufräumlauf auf 125, und mit diesem
Sitzungsstart fällt `sitzungsstart-00bd.md` dazu. Ein Branch.

`00bd` war eine reine Spec- und Aufräumrunde: kein Produktivcode, keine neuen Tests. Zwei
Registereinträge, eine Prüfregel, ein Posten, ein Aufräumlauf.

### Die Schichten

Unverändert seit `00ar` — siehe `arbeitsweise.md`, `pruefregeln.md`, `08-scope.md §3`.

### Der Bestand

Keine Änderung an `symbolon/`, keine an `tests/`. Verschoben wurden 16 ungebundene
Wurzeldateien nach `archiv/` (Prompts und Übergabedateien abgeschlossener Läufe, volle
Ähnlichkeit, null Einfügungen). Der Branch `szenario-h` war vollständig in `main` und ist
gelöscht.

**Ausserhalb des Repositoriums, bei Oli lokal:** `restack-faktensammlung.md`,
`restack-felder-englisch.md`, `prompt-log.py` und `prompt-log-restack.md` in `~/Downloads`.
Bewusst nicht im Baum. Wenn der Antrag vor dem 3. November nachgebessert wird, sind das die
Dateien dafür.

## Was in `00bd` entschieden wurde (D360, D361)

Ausgangspunkt war der nächste Schritt aus `00bc`: die Fork-Runde zu D354, also die Frage, ob
ein abhängiger Claim seine Prämisse nennen kann, damit eine Ablaufaussage ohne Uhr prüfbar wird.

**D360 (die Leseregeln zeigen nach innen).** Der Supervisor hat eine Fork-Position auf
Suchauszüge gestützt und als Befund gemeldet: zwei Lager, PKIX ohne Verschachtelung,
Capability-Systeme mit. Die Volltexte drehten den Hauptpunkt um. Verworfen wurde der erste
Reparaturvorschlag — den Geltungsbereich von Prüfregel 27 erweitern —, weil Prüfregel 38 das
seit D209 wörtlich sagt; das wäre D359 eine Ebene höher gewesen. Beschlossen wurde **Prüfregel
72** mit eng begrenztem Zuwachs: 27, 33 und 38 zeigen alle nach innen, und für eine externe
Quelle gibt es keinen zuständigen Abschnitt. 27, 33 und 38 bleiben im Wortlaut.

**D361 (Literaturbefund, und was an D354s Begründung fällt).** Vier Systeme und ein
IETF-Entwurf geprüft. Der gemeinsame Nenner: **keines vergleicht Zeit zwischen zwei signierten
Aussagen** — jede Zeitgrenze wird gegen eine Uhr zur Nutzungszeit geprüft. UCAN lässt
abweichende Perioden ausdrücklich zu, Biscuit kodiert Ablauf als Datalog-Check über eine
`time`-Fakt des Authorizers, RFC 5280 nennt das `notAfter` des Ausstellers nicht.
Verschachtelung ist bekannt und wird nirgends verlangt. Raytime ist die einzige Quelle zur
uhrlosen Lage und löst sie, indem es die Richtung umdreht — Verfügbarkeit vor Sicherheit,
Gegenrichtung zum Unter-Vertrauen aus `01 §5.3`.

Dazu die **Korrektur an D354**: die Verortung „`v` Key 1" hält nicht. Der Keyraum ist
prädikat-lokal (`03 §1.3`), Key 1 ist in `obligation@1` und `verdict@1` belegt, und `02a`
T-02.7 erlaubt Zusatz-Keys nur als **ungelesene**. Ein gelesener Prämissen-Key braucht eine
Zeile je Profil in `03 §1.3` und Vermerke in `03 §6.1`. Die Kernaussage „kein Feldsatz" bleibt
richtig, ihre Begründung nicht.

**Die Gabel selbst bleibt offen, und das ist der Beschluss.** Weder Verschachtelung noch
Prämissennennung erlauben einem uhrlosen Knoten, etwas zu **benutzen** — beide erlauben nur,
mehr abzulehnen. Die Frage hängt an einer Entscheidung eine Ebene höher, geführt als **O61**.
Die Vertagung kostet nichts: solange kein Profil einen Prämissen-Key deklariert, kann kein
Claim eine Verschachtelung verletzen.

**Nebenbefund, ungenutzt:** zwei `v`-Leser mit verschiedenen Verträgen.
`profiles/payload.py:read_v` gibt jede Map zurück, `trust/groups.py:_decode_weight` verlangt
Key 0, sobald `v` überhaupt gesetzt ist. Heute folgenlos; D354 würde den Grund schaffen.

## Der Ablauf, der teurer war als das Ergebnis

Beide Supervisor-Fehler dieser Runde hat der **Operator** gestoppt, nicht der Supervisor.
Zuerst die Nachfrage, ob die Literatur wirklich gelesen sei — daraus D360. Dann die Anweisung,
vor den Registereinträgen vollständig zu lesen; die Nachprüfung fand, dass der Eintrag, der
Prüfregel 72 begründet, selbst überbehauptete, was gelesen worden war. Und im ersten Diff stand
ein Zähl-Drift: „Vier Systeme" über einer Liste von fünf Quellen. Drei Anläufe bis zum
sauberen Splice.

Die Lehre steht in D360 und in Prüfregel 72 und wird hier nicht wiederholt. Was hier steht,
ist der Rest: das vollständige Lesen des Diffs hat wieder etwas gefunden, das kein Linter
sieht, und der Trockenlauf gegen eine Kopie hat jede der drei Fassungen vorab bestätigt.

## Werkzeugnotizen

- **`stand.py` braucht einen Pfad** auf eine Datei mit der pytest-Ausgabe und gibt ohne
  Argument stumm 1 zurück. Aufruf: `make check > /tmp/check.txt 2>&1`, dann
  `python tools/stand.py /tmp/check.txt`. **Keine Pipe dahinter** — `tail` schluckt den
  roten Status, und die Schlussmarke erscheint trotzdem.
- **`stand.py` zählt Zeilen von `git branch -a`**, also Remote-Refs mit. Die „vier Branches"
  im Sitzungsstart zu `00bd` waren `main`, `szenario-h`, `origin/HEAD` und `origin/main` —
  es gab nie einen Rückstand von vier Feature-Branches. Jetzt sind es drei Zeilen und ein
  Branch.
- **`git rev-parse --short` verträgt nur eine Revision**, weil `--short` `--verify` impliziert.
  Zwei Argumente ergeben „Benötigte einen einzelnen Commit" — sieht nach einem Push-Fehler aus
  und ist keiner.
- **`splice_run.py` verlangt einen sauberen Baum.** Wird ein Defekt im Diff gefunden, ist der
  Weg `git checkout --` auf die betroffenen Dateien und ein korrigierter Splice, nicht ein
  zweiter Splice obendrauf.
- **Der repomix-Nachzug der Projektkopie steht für diese Runde noch aus.** Kopfzeile aus den
  Kaltzahlen: `404ff1b`, 811 Tests, 361 Registerköpfe, 72 Prüfregeln, 61 Posten, 3 Branches.

## Offene Punkte, nach Grösse

**Das grösste:** O61 — soll ein uhrloser Knoten überhaupt Vertrauen gewähren können? `01 §5.3`
beantwortet die Lage heute kohärent mit Unter-Vertrauen, aber damit kann ein Knoten ohne Uhr
nichts gewähren. Drei Wege: signierte Zeit-Attestierung (`VISION.md §5`, D350), Wechsel auf die
Verfügbarkeitsseite nach Raytime, oder Scopes ohne `t_exp`. D354 hängt daran und ist ohne diese
Vorentscheidung nur ratbar.

**Daneben:** D354 selbst, mit der Gabel F2 (Verschachtelung als Norm gegen Schnittmenge bei der
Auswertung). O60 — die Budget-/Kantensatz-Asymmetrie, Vorbedingung für jede Fassung mit
unscharfer Zeit; Raytime liefert dafür Namen, Form und die Persistenzpflicht. Der Trust-Pfad aus
`02a §2.6` als eigener Lauf mit eigener Frage, offen seit `00bb`. O56 (PyPI-Name `symbolon`
belegt). O57 (Restack, eingereicht am 10. September, Frist für Nachbesserung 3. November).

**Ohne Frist:** die Übertragung auf unterbrochene Zustellung (LoRa/Reticulum). Anschlusspunkte
D345, D346, D350, D353, jetzt D361 — und die Erkenntnis, dass die Literatur für den uhrlosen
Fall nichts Fertiges hergibt.

**Ungeklärt aus `00bd`:** keine offene Frage aus dieser Runde übrig, ausser der bewusst
vertagten Gabel F2.

## Der nächste Schritt

Zwei Kandidaten, und die Reihenfolge ist eine Entscheidung.

**O61** ist die inhaltlich grössere Frage und blockiert D354. Sie ist aber vom selben Typ wie
die Runde, die gerade zwei Supervisor-Fehler produziert hat: Fork-Arbeit ohne messbares
Zwischenergebnis, bei der nur das Lesen vor dem Irrtum schützt. Wenn sie drankommt, dann mit
Prüfregel 72 von Anfang an und mit `VISION.md §5` sowie D350 vorher aufgeschlagen.

**Der Trust-Pfad aus `02a §2.6`** ist der andere: ein Lauf mit eigener Frage, messbarem
Abnahmekriterium und einem Werkzeug, das mitprüft. Er steht seit `00bb` offen, und Szenario H
hat ihn nicht beantwortet.

Nach drei Anläufen an einem Registereintrag spricht einiges dafür, zuerst etwas zu fahren, das
ein Werkzeug rot werden lassen kann.
