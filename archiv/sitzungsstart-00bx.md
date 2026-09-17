# Sitzungsstart: 00bx (MaR / symbolon), fortgeschrieben nach D401

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
Branches erscheinen am Spiegel erst nach dem Push vom Host.

## Stand

Am Ende von `00bx`: **882 Tests**, Register **D1–D401**, Prüfregeln **1–75** (unverändert),
`make check` grün, `main` bei `ed83792`. **32 Wurzel-Markdown-Dateien, alle gebunden**;
`archiv/` steht bei 134, und mit diesem Sitzungsstart fällt `sitzungsstart-00bw.md` dazu.
`offen.md` führt **69 Posten**; O64, O68 und O69 sind in dieser Sitzung erledigt.

**Zwei Stränge** wie bisher: `main` und `00bo-hs` (kontaminiert, D374, wird nicht gelöscht).

`check_specs` zählt in der Python-Zeile `161 Dateien, 411 Verweise` und prüft seit D401 auch
Anhangsverweise. Abschnittsverweise auf `02a` stehen ausserhalb von Register, `offen.md`, `archiv/`
und den Isolaten nirgends mehr.

## Was in dieser Sitzung geschah

### D398 — Zug 1 von O69: der Splice nach `02`

Die Abschnittskarte aus D397 trug in zehn von vierzehn Zeilen. Vier Abweichungen: `cut nach 02`
widersprach D375 (Oli: die Ausgabeform geht als K9 nach `02-golden-anchors.md`, dazu Anker 3c);
die Mengentabelle in `02 §3.1` wiederholte die D135-Klasse und ist jetzt zustandsbasiert;
Schritt 2 der Auswertungsreihenfolge hätte O68 durch Abschrift entschieden; ein Satz aus T-02.8
gilt nicht allgemein. Neu: `02 §11` (Rechenregeln, Parameterbereiche, Anfrage, Reihenfolge),
Sentinel-Kasten in `§4` mit Bedingung und Schranke nach D381, Filtersatz in `§8`. `02a` trägt
Kopfvermerk und je Abschnitt einen Verweis.

### D399 — O69 erledigt; der Containerlauf am Referenzrepo

Zug 2 war zwei Verweise, nicht sechs Dateien (die Liste in D397 kam aus einer Namenssuche mit
Hex-Hashes). Zug 3 hängte 37 Codestellen um und gab `TrustParams` eine Typprüfung. Zwei Fehler im
Auftrag, beide von mir: 409 statt 410 erwartete Verweise, und eine Rücknahmeprobe, deren Test die
Bereichsmeldung statt der Typmeldung traf. Das Werkzeug hat beides gemeldet, nicht angepasst.

### D400 — O68 erledigt

Gelesen wird das Budget-Set; `VOUCH_WITHOUT_TEXP` fällt nur bei gültigem `n`. Begründet über die
Wirkungsspalten in `02 §10`, nicht aus dem Code übernommen. Der Code blieb; drei Tests pinnen
jetzt die Vermerke (abgelaufen, widerrufen, Gegenprobe).

### D401 — O64 erledigt

`check_specs` prüft Anhangsverweise in beiden Zitatformen, gegen `## Anhang` und die
Unterabschnitte. 33 geprüfte Verweise, kein Befund. Die Vermutung aus O64, der Parser sammle nur
die zweite Ebene, traf nicht zu. Nachbesserung vor dem Merge: ein Buchstabe, dem ein Wort folgt,
ist kein Anhangsverweis.

## Werkzeuglauf: Container `mar-sym-box` (D399)

Implementierung am Referenzrepo läuft in opencode mit DeepSeek im Container, nicht in Cursor.

- Eigenes Datenvolume `mar-sym-data`, getrennt von `mar-rs-auth` des Isolats (D389 umgekehrt);
  `mar-sym-venv` über `/work/.venv`; Lauf mit Host-uid; Git-Identität per Umgebungsvariablen.
- Der Auftrag liegt in `~/Downloads` und wird nur lesend als `/auftrag.md` eingehängt, nie in
  die Wurzel (ungebunden wäre ein Befund).
- **Je Auftrag Container und opencode-Sitzung neu starten**, im **Build**-Modus. Eine
  Nachbesserung zum selben Auftrag darf in der offenen Sitzung laufen.
- Die Zugriffsanfrage auf `/` mit „Allow once" beantworten.
- Branch auf dem Host anlegen, Push vom Host, Abnahme am Spiegel. Merge als fast-forward.

Startbefehl und erste Nachricht stehen in `00bx` mehrfach im Verlauf; der Branchblock prüft den
Basis-Hash, der Pushblock `git status` und `git log` gegen den Branchpunkt.

## Werkzeugnotizen

- **Rücknahmeproben gegen die ganze Testdatei laufen lassen**, nicht nur gegen die neuen Tests.
  Erst dann sieht man, was bestehende Tests schon abdeckten (D400: beide Proben trafen je einen
  alten Test mit).
- **Erwartete Zahlen im Auftrag über den ganzen Auftrag probefahren**, nicht nur über Teil A.
  Eine neue Testdatei ändert Datei- und Verweiszahl.
- **`check_specs` liest auch Python-Dateien.** Erfundene Verweise in Tests zur Laufzeit
  zusammensetzen.
- **Register und Sitzungsstart sind von der Abschnittsprüfung ausgenommen.** Wer Verweise zählt,
  zählt ohne sie (D401 wäre sonst mit 55 statt 35 gerechnet).
- **Splice-Kopfzeilen in `offen.md`**: der Zusatz „erledigt" kann die Zeilengrenze sprengen
  (O69 nennt deshalb die Kurzform).
- Unverändert: `git checkout main` vor jedem Merge; `cbor2`, `cryptography`, `pytest`,
  `hypothesis` im Sandbox nachinstallieren; Splices im Supervisor-Klon probefahren; der Klon wird
  nach einer Probe zurückgesetzt.

**Prüfregel-Kandidaten, nicht übernommen:**
- Ein Befundtest prüft die Meldung, die nur sein Befund erzeugt — **zweimal** in zwei Sitzungen
  (D395, D399), das zweite Mal im Auftrag. Reif für eine Regel.
- Einen Abschnitt ganz lesen, bevor man aus einem Satz darin schliesst (D392 → D394).
- An zwei Fällen Gemessenes nicht „durchgehend" nennen (D390 → D396).
- Eine Karte aus Wortsuche ist eine Vermutung; vor dem Schreiben den Wortlaut lesen (D397 → D398).

## Offene Punkte, nach Grösse

**O61** — soll ein uhrloser Knoten Vertrauen gewähren können? Das grösste inhaltliche Thema,
unverändert seit `00bl`.

**O60** — Budget-Set und Kantensatz lösen Zeitunsicherheit in entgegengesetzte Richtungen.
Nach D398 und D400 gegen `02 §3.1` und `02 §11` neu zu lesen.

**Daneben:** D354 mit der Gabel F2. O56 (PyPI-Name belegt).

**Merkposten Restack:** eingereicht am 10. September, Code `2026-11-0c4` (D349). Bewertet wird
nach der Frist am 3. November; bis dahin zählt die zuletzt vollständige Fassung. **Mitte Oktober**
den Antragstext gegen den Stand halten und entscheiden, ob nachgebessert wird. Wie das Portal eine
Aktualisierung abwickelt, ist nicht geklärt.

**Ungeklärt aus `00be`:** die Invariantentabelle kennt keine Zeitaussage. Die Invarianten stehen
weiter nur in `02-golden-anchors.md §8`; `02` hat seit D398 keinen Invariantenabschnitt bekommen.

**Ohne Frist:** die Übertragung auf unterbrochene Zustellung (LoRa/Reticulum).
Anschlusspunkte D345, D346, D350, D353, D361, D362, D363.

## Der nächste Schritt

**O60 lesen**, gegen `02 §3.1` (Mengentabelle nach D398), `02 §7` und `02 §11.4`. Erst den
Posten und die dort genannten Registereinträge vollständig, dann Position. O60 ist die kleinere
Vorstufe zu O61: beide handeln davon, was fehlende oder unsichere Zeit mit Budget und Kante macht.
