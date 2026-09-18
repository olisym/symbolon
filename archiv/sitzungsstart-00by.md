# Sitzungsstart: 00by (MaR / symbolon), fortgeschrieben nach D405

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

Am Ende von `00by`: **885 Tests**, Register **D1–D405**, Prüfregeln **1–75** (unverändert),
`make check` grün, `main` bei `7e316f2`. **32 Wurzel-Markdown-Dateien, alle gebunden**;
`archiv/` steht bei 135, und mit diesem Sitzungsstart fällt `sitzungsstart-00bx.md` dazu.
`offen.md` führt **71 Posten**; O60, O61 und O70 sind in dieser Sitzung erledigt, O70 und O71
sind neu hinzugekommen.

**Zwei Stränge** wie bisher: `main` und `00bo-hs` (kontaminiert, D374, wird nicht gelöscht).
Dazu `o70-uhrversatz-pin`, gemergt und stehen gelassen.

`check_specs` zählt in der Python-Zeile `162 Dateien, 424 Verweise`.

## Was in dieser Sitzung geschah

### D402 — O60 erledigt: zwei Prädikate für Über-Commitment

Die Gegenläufigkeit aus O60 ist harmlos: bei einem Intervall `now ∈ [lo, hi]` heisst konservativ
für die Kante `hi ≤ t_exp` und für das Budget `lo ≤ t_exp`, aus dem ersten folgt das zweite, also
bleibt `Aktiv-Set ⊆ Budget-Set`. Der Konflikt sitzt im Budget-Set selbst: der lokale Vermerk will
„rein" (Unter-Vertrauen), der slashbare Beweis will „raus" (nie eine Verletzung erfinden).
Gemessen: bei nachlaufender Uhr fällt `OVERCOMMITTED_AUTHOR` gegen eine Autorin, deren
Bürgschaften nach ihren signierten Zahlen nacheinander liefen. Beschlossen sind zwei Prädikate —
der Vermerk bleibt `now`-basiert und lokal, der Beweis wird signaturbasiert mit gemeinsamem
Geltungspunkt `max tᵢ ≤ min t_expᵢ`. Gesplict in `02 §3.1`, `§7`, `§10`, `03 §2.3`, `§3.3.4`.

### D403 — `LINKED` ist im Trust-Pfad unerreichbar

`LINKED` entsteht nur im Zweig `temporal is None`, also nur bei `now = None`; `derive()` verlangt
`now: int`. Die Aufzählung in `02 §3.1` ist damit erschöpfend, anders als bei D135. Die Lücke
liegt im Prädikat: ohne `now` ist „nicht abgelaufen" weder wahr noch falsch. Gemessen wurde, dass
die naive Durchreichung von `now = None` die Richtung umkehrt — der uhrlose Knoten sähe **mehr**
als der mit Uhr. Keine Norm gesetzt; die zwei Sätze gehören zu O61.

### D404 — O61 erledigt: uhrlos wird belastet, nicht gewährt

Der tragende Grund ist neu: `02 §8` macht die Budgetregel zum Default und erlaubt nur lockerer
oder strenger, nicht aus. Also gilt `02 §6.2` überall, also trägt jeder Vouch `t_exp`, also ist
der uhrlose Wert strukturell 0 — positiv wird er nur über Bürgschaften, die die Pflicht verletzen
und nach D364 die schlechtesten sind. Eine Fähigkeit, die den Verstoß prämiert, wird nicht gebaut.
Was uhrlos geht, ist benannt: Signaturprüfung, Verkettung, Equivocation und seit D402 der
Über-Commitment-Beweis. Der reale Fall ist der Knoten mit grober Uhr, und der läuft als O71.

### D405 — O70 erledigt: der Uhrversatz-Fall ist gepinnt

Containerlauf, `tests/trust/test_uhrversatz.py`, drei Fälle, `symbolon/` unberührt. Der Befund
der Abnahme ist der wertvollere Teil: die erste Fassung bestand die Rücknahmeprobe nur zur Hälfte,
weil ein Fall nur behauptete, dass ein Wert zurückkommt — „geflaggt, Flag ignoriert" und „gar
nicht geflaggt" waren für ihn ununterscheidbar.

## Werkzeugnotizen

- **Lieferungen laufen über `/tmp`, immer.** Ein zusammenhängender Block je Lieferung: Basis- und
  Zielhashes per `printf` in `/tmp/mar-basis.sha` und `/tmp/mar-neu.sha`, `sha256sum -c` als
  Abbruchbedingung, dann `cp /tmp/<datei> .`, Prüfung, Commit, Push. Kein Aufteilen in Blöcke,
  die Klicks oder Tippen erfordern.
- **Vor dem `cp` gehört `git status --short` in den Block.** In dieser Sitzung hat er gezeigt,
  dass ein Commit der Vorrunde nie gelaufen war: `e0d76df` trägt deshalb D403 und D404 unter der
  D404-Nachricht. Wer D403 sucht, findet ihn dort.
- **Der Containerlauf deckt `make check` nicht ab**, wenn im Container nur `pytest` lief. `ruff`
  läuft erst am Host; lange Docstring-Zeilen fallen dort auf, nicht im Lauf.
- Unverändert: je Auftrag Container und opencode-Sitzung neu, Build-Modus, Auftrag nur lesend als
  `/auftrag.md` eingehängt, Branch am Host, Push am Host, Abnahme am Spiegel, Merge als
  fast-forward. Rücknahmeproben gegen die ganze Testdatei. `check_specs` liest auch Python-Dateien;
  Verweiszahlen im Auftrag nicht vorgeben, wenn sie an Docstrings hängen, die erst im Lauf
  entstehen.
- Supervisor-Klon: `cbor2`, `cryptography`, `pytest`, `hypothesis` nachinstallieren. Nach einer
  Probe zurücksetzen — und vorher prüfen, ob die Kopie der letzten Lieferung noch in den Outputs
  liegt, sonst ist ein `git checkout -- .` teuer.

**Prüfregel-Kandidaten, nicht übernommen:**
- **Reif, jetzt zum zweiten Mal begründet:** ein Befundtest prüft die Meldung, die nur sein Befund
  erzeugt (D395, D399).
- **Neu aus D405:** ein Test, den seine eigene Rücknahmeprobe nicht rot bekommt, prüft nicht, was
  sein Name sagt. Die Probe belegt auch die Benennung, nicht nur den Regressionsschutz.
- Einen Abschnitt ganz lesen, bevor man aus einem Satz darin schliesst (D392 → D394).
- An zwei Fällen Gemessenes nicht „durchgehend" nennen (D390 → D396).
- Eine Karte aus Wortsuche ist eine Vermutung; vor dem Schreiben den Wortlaut lesen (D397 → D398).

## Offene Punkte, nach Grösse

**O71** — Intervall-`now` für den Knoten mit grober oder driftender Uhr. Seit D404 der
Hauptstrang: die Vorbedingung (O60) ist beantwortet, D355 hat die Konstruktion skizziert. Zu
klären sind Herkunft des Intervalls, Parameter oder Verifizierer-Zustand, und was eine Auswertung
zurückgibt, deren Anfrage im Intervall kippt.

**O62** — Zweitimplementierung für Layer 02. Umfang steht (D368), Sprache offen, Prüfregel 15
verlangt den Literaturcheck vor der Wahl.

**Daneben:** D354 mit der Gabel F2. O56 (PyPI-Name belegt).

**Merkposten Restack:** eingereicht am 10. September, Code `2026-11-0c4` (D349). Bewertet wird
nach der Frist am 3. November. **Mitte Oktober** den Antragstext gegen den Stand halten und
entscheiden, ob nachgebessert wird. Wie das Portal eine Aktualisierung abwickelt, ist nicht
geklärt.

**Ungeklärt aus `00be`:** die Invariantentabelle kennt keine Zeitaussage. Die Invarianten stehen
weiter nur in `02-golden-anchors.md §8`; `02` hat seit D398 keinen Invariantenabschnitt bekommen.

**Ohne Frist:** die Übertragung auf unterbrochene Zustellung (LoRa/Reticulum). Anschlusspunkte
D345, D346, D350, D353, D361, D362, D363, jetzt auch D404.

## Der nächste Schritt

**O71 lesen und Position beziehen**, gegen D355 (der zurückgestellte Beschluss), `02 §3.1` mit den
beiden Prädikaten aus D402, `01 §6` und den Nebenbefund aus D355 zu `derive()` und `flow()`. Die
Richtungsfrage ist entschieden; offen ist die Bauform. Erst den Posten und die genannten
Registereinträge vollständig, dann Position.
