# Sitzungsstart: 00bw (MaR / symbolon), fortgeschrieben nach D397

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

Am Ende von `00bw`: **859 Tests**, Register **D1–D397**, Prüfregeln **1–75** (unverändert),
`make check` grün, `main` bei `45adde4`. **32 Wurzel-Markdown-Dateien, alle gebunden**;
`archiv/` steht bei 133, und mit diesem Sitzungsstart fällt `sitzungsstart-00bv.md` dazu.
`offen.md` führt **69 Posten**; O65, O66 und O67 sind erledigt.

**Zwei Stränge** wie bisher: `main` und `00bo-hs` (kontaminiert, D374, wird nicht gelöscht).

Neun Commits, vier Registereinträge (D394–D397), ein Werkzeuglauf mit zwei Nachbesserungen.

## Was in dieser Sitzung geschah

### D394 — `02 §10` widersprach sich selbst, und D392 hatte es übersehen

Der Schlusssatz von `§10` zählte `VOUCH_WITHOUT_TEXP` zu den vier Vermerken, deren Claim nichts
zum Fluss beiträgt. Die Rust-Fassung hat genau das gebaut. D392 hatte nur den einleitenden Satz
gelesen und die Fassung einen Lesefehler geheissen. Das Ergebnis bleibt (D119 beschliesst den
Vermerk ohne Wirkung), die Begründung ist ersetzt. `§10` ist neu gefasst: Tabelle mit Subjekt,
Budget-Set, Kante und Grundlage; Quellenzuordnung und Reihenfolge korrigiert.

Nebenbei gemessen und als **O68** abgelegt: `build_groups` dekodiert nur Budget-Set-Mitglieder und
überspringt defektes `v` vor der `t_exp`-Prüfung. Welche Vouches einen Vermerk bekommen, steht
nirgends; bewusst nicht aus dem Code übernommen.

### D395 — selbsttragende Fragenlisten (O66)

`fragen-adressen.md` bleibt das Verzeichnis. Eine selbsttragende Liste meldet sich mit der Zeile
`Adressen: in der Liste.` an und wird aus sich gelesen; eine Vollständigkeitsprobe fängt nicht
angemeldete `FRAGEN*.md` ab. Index jetzt 81 Einträge, 110 Nennungen, 27 Adressen, Spalte `rs`.

Die Abnahme brauchte zwei Nachbesserungen. Vier von sieben Tests prüften nur den Exit-Code und
wären an jeder Indexabweichung rot geworden — sie sahen ihren Befund nicht. Und meine Rücknahmeprobe
nahm die Eingabe zurück statt der Reparatur. Die zweite Runde fand einen doppelten Träger derselben
Meldung.

### D396 — drei Nullstrukturen, verschiedene Ursachen (O65)

Gruppen mit `0 0` waren eine Textlücke: `02 §3.1` besteht jetzt darauf, dass eine Gruppe nur mit
einem Mitglied im Budget-Set existiert; die Out-Degree-Schranke setzt `n ≥ 1` voraus. Kanten mit
`cap 0` waren keine Lücke, sondern mein Auftrag (`inf` für unerreichbare Autoren setzte Kanten
voraus, die `E⁺` ausschliesst). Die `bytes`-Legende steht in `01 Anhang C.0` und hängt an der
eigenen `σ`-Zeile: mit ihr ist `bytes` der Core, ohne sie die Wire-Form. **D390 Befund 4 war an
zwei Vektoren gemessen und dann „durchgehend" genannt** — ab `C.13` ist `bytes` Wire-Form.

### D397 — `02a` wird als normativer Text aufgelöst (O69)

46 Registereinträge berühren `02a`-Stellen, 42 Dateien nennen den Namen, der Code zitiert 20-mal.
`02a` war nicht eingefroren, sondern viermal im Einzelfall nachgezogen (D135, D356, D369, D381) —
und genau das hat Lücken in beide Richtungen erzeugt: der Sentinel-Kasten in `02 §4` nennt eine
Schranke, die D381 nur in `02a §2.8` präzisiert hat.

**Oli hat Weg C entschieden:** ein normativer Text je Gegenstand, und das ist `02`. `02a` bleibt
in der Wurzel (101 Registerverweise über die Kurzform), bekommt Kopfvermerk und je Abschnitt einen
Verweis, Überschriften unverändert. Die Abschnittskarte steht in D397 Beschluss 3.

## Werkzeugnotizen

- **Ein Befundtest prüft die Meldung, nicht den Exit-Code.** Sonst wird er an jeder Nebenwirkung
  der Verfälschung rot und sieht seinen eigenen Befund nie.
- **Eine Rücknahmeprobe neutralisiert den Prüfpfad**, nicht die Eingabe. Meldet das Werkzeug
  „Test blieb grün", ist das ein Haltesignal.
- **`check_specs.py` misst Zeilenlänge in Zeichen, prüft Tabellenzeilen nicht.** `awk length`
  zählt anders. Überschriften im Register werden geprüft.
- **Umbruch neuer Registerblöcke maschinell**, Tabellen- und Kopfzeilen dabei auslassen. Handumbruch
  kaskadiert.
- **Der Supervisor-Klon wird nach einer Probe zurückgesetzt** (`git checkout -- .`), sonst
  scheitert der nächste Pull.
- Unverändert: `git checkout main` vor jedem Merge; `cbor2`, `pynacl`, `pytest`, `hypothesis` im
  Sandbox nachinstallieren; Splices im Supervisor-Klon probefahren.

**Prüfregel-Kandidaten, nicht übernommen:** einen Abschnitt ganz lesen, bevor man aus einem Satz
darin schliesst (D392 → D394); an zwei Fällen Gemessenes nicht „durchgehend" nennen (D390 → D396);
die beiden Testnotizen oben.

## Offene Punkte, nach Grösse

**O69 — der Umbau nach D397.** Laufend, drei Züge offen (siehe nächster Schritt).

**O61** bleibt das grösste inhaltliche, unverändert seit `00bl`.

**O68 — welche Vouches einen Vermerk bekommen.** Wird nach O69 gegen `02` entschieden, nicht gegen
`02a §2.10`.

**O64 — Anhangsverweise ungeprüft.** `check_specs.py` prüft Abschnitte, Anhänge nicht.

**Daneben:** O60 (Budget-/Kantensatz-Asymmetrie). D354 mit der Gabel F2. O56 (PyPI-Name belegt).
**O57 (Restack, Frist 3. November)** — die einzige Frist im Bestand.

**Ungeklärt aus `00be`:** die Invariantentabelle `02a §7` kennt keine Zeitaussage. Nach D397 ist
die Frage gegen die Invariantenstelle zu stellen, die in `02` entsteht.

**Ohne Frist:** die Übertragung auf unterbrochene Zustellung (LoRa/Reticulum).
Anschlusspunkte D345, D346, D350, D353, D361, D362, D363.

## Der nächste Schritt

**D397 Beschluss 4, Zug 1: der Splice nach `02`.** Vorher jede Zeile der Abschnittskarte im
Wortlaut gegen `02` nachlesen — die Karte ist eine Wortsuche, das ist ihre schwächste Stelle.
Inhalt des Splice:

- ein neuer Abschnitt in `02` für Auswertungsreihenfolge (`02a §2.10`), Rechenregeln (`§0`:
  ganzzahlig, `now` als Parameter, Determinismus einschliesslich `cut` und Vermerken), `cut`
  quellseitig samt leerem `cut` (`§3`), den Fehlerfall Anker ∩ Ziele (`§2.8`), vollständige
  Parameterbereiche (`§2.1`);
- im Sentinel-Kasten `02 §4` die Schranke nach D381 (`max(Σ C(0), |E⁺|) + 1`) und der Verweis auf
  `02a §2.8` ersetzt;
- in `02 §3.1` die zwei Sätze aus `02a §2.6` (Aktiv-Set ausdrücklich `ACTIVE`, `MALFORMED` in
  keiner Menge) und der Satz aus `02a §4`, dass der Filter für den Einheitslauf sicherheitsrelevant
  ist;
- im selben Commit `02a`: Kopfvermerk und je verschobenem Abschnitt ein Verweis auf die `02`-Stelle,
  Überschriften unverändert. `02 §10` verweist danach nicht mehr auf `02a`.

Danach Zug 2 (Spec-Dateien `02-golden-anchors.md`, `02b-*`, `06`, `01`, `01a`, `pruefregeln.md`)
und Zug 3 (Werkzeuglauf für Code, Tests, Werkzeuge nach einer aus dem Splice abgeleiteten
Umhängetabelle). Abschluss per `grep`: kein `02a §` ausserhalb von Register, `offen.md`, `archiv/`
und den Isolaten unter `go/`, `hs/`, `rs/`.
