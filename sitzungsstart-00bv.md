# Sitzungsstart: 00bv (MaR / symbolon), fortgeschrieben nach D393

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

Am Ende von `00bv`: **852 Tests**, Register **D1–D393**, Prüfregeln **1–75** (unverändert),
`make check` grün, `main` und `origin/main` gleichauf bei `7e9c89a`. **32 Wurzel-Markdown-
Dateien, alle gebunden**; `archiv/` steht bei 132, und mit diesem Sitzungsstart fällt
`sitzungsstart-00bu.md` dazu. `offen.md` führt **67 Posten**.

**Zwei Stränge** wie bisher: `main` und `00bo-hs` (kontaminiert, D374, wird nicht gelöscht).

Fünfzehn Commits, elf Registereinträge (D383–D393), zwei Werkzeugläufe.

### Der Bestand — neu in dieser Sitzung

Unter `rs/`: `spec/01-claim-atom.md`, `spec/02-trust-flow.md`, `spec/STAND.md`, `AUFTRAG.md`,
`FRAGEN.md`. Unter `hs/`: `FRAGEN-1.md`, `FRAGEN-2.md`, `FRAGEN-STAND.md`. In der Wurzel:
`fragen-adressen.md`, `fragen-index.md`. Dazu `tools/check_fragen.py`, `tools/ref_block.py`
und ihre Tests. `arbeitsweise.md` hat einen elften Abschnitt.

**Ausserhalb des Repositoriums:** `~/mar-rs` — die Rust-Fassung, eigenes Git, Commit
`e7fd0fc`, gebaut in einem Container ohne Sicht auf das Hauptrepo. `~/mar-hs2` unverändert.
`~/mar-rs-box/Dockerfile` und die Volumes `mar-rs-auth`, `mar-rs-cargo`.

## Was in dieser Sitzung geschah

### Die Vorbedingung, die keiner auf dem Zettel hatte (D384–D387)

D374 Beschluss 4 verlangt eine gegliederte Fragenliste **vor** dem Start einer dritten
Fassung. Der Posten lag, weil zwei der drei Listen gar nicht im Baum waren: HS1 nur in
`00bo-hs`, HS2 nur in `~/mar-hs2`. Das wichtigste Ergebnis der bisherigen Arbeit war nicht
mitversioniert.

D384 holt beide nach `hs/`, unverändert, mit dem Vermerk daneben statt darin. D385 ordnet
nicht durch Umschreiben, sondern über einen Index — Belege bleiben Belege. D386 korrigiert
D385 einen Commit später: die geplanten Extraktionsregeln tragen nicht, weil bei `go` zehn
von zweiundzwanzig Titeln keine Stelle nennen und fünf davon ausgerechnet den dichtesten
Punkt betreffen. Die Zuordnung ist Urteilsarbeit und steht in `fragen-adressen.md`, alle 68
Einträge. D387 legt Matrixform und Betriebsart fest: geprüft, nicht bei jedem Lauf
geschrieben.

Sichtbar wurde dabei, dass **dreizehn der 68 Einträge auf `AUFTRAG` zeigen** — jede vierte
bis fünfte Frage der Layer-02-Fassungen entstand an meinen Aufträgen, nicht am Normtext.

### Die Kontaminationsprobe (D389)

Vor der Beauftragung geprüft, ob das Werkzeugmodell das Projekt kennt. **Cursor kannte den
Aufbau der zurückgehaltenen Ankerdatei**, die Existenz von `03-` und `04-golden-anchors.md`
und Einzelheiten beider Haskell-Läufe — aus früheren Sitzungen, nicht aus dem Dateisystem.
Damit ist D374s „Isolat ohne Pfad nach aussen" nur die Dateiseite; werkzeugseitig ist HS2
unbelegt (die Gegenprobe an ihrer Fragenliste schlägt allerdings nicht an).

Meine erste Probe war als Detektor untauglich — ich fragte nach Werten, die berechenbar
sind, und zitierte im selben Zug D374s Satz, dass eine korrekte Fassung wie eine
abgeschriebene aussieht. Der brauchbare Detektor sind **neun Registernummern, die nur in
`02-golden-anchors.md` stehen**: D19, D24, D31, D32, D36, D39, D44, D135, D256. D367 fällt
aus, weil er in `rs/spec/STAND.md` steht.

DeepSeek V4 Pro war sauber. Der Ankersatz nannte allerdings die Repo-Adressen — in der
Datei, die das Zurückhalten begründet. D389 Beschluss 3 entfernt sie; die Arbeitskopie wurde
neu aufgesetzt, weil ein Fix per Commit die Historie nicht erreicht.

### Die dritte Fassung (D383, D388, D390)

Rust, `petgraph::algo::ford_fulkerson` auf `Graph`, `u64` ohne Ausweichen, drei Vektorsätze
statt einem, vorgegebene Schnittseite, neue `inf`-Zeile. Gebaut im Container.

**Acht von acht Profilen aus `TP-02` treffen die Ankerwerte**, ohne dass die Fassung die
Ankerdatei je gesehen hat. `FALL-02` deckt sich mit HS1 in allen drei Sprossen.

Zwei stille Anpassungen sind zu vermerken: Saturierung auf `u64::MAX` entgegen dem
Nicht-Ziel, und eine Korrektur der Spec-Bytes aus `Anhang C` für die eigenen Tests. Beide
standen in Nebensätzen anderer Einträge. D390 Beschluss 2 verlangt künftig für jede
Abweichung von einer Spec-Angabe einen eigenen Eintrag.

### Der Zeilenvergleich (D391–D393)

`tools/ref_block.py` druckt die Referenz in der Blockform der Aufträge. Er ist **kein
Orakel** (D391 Beschluss 2): weicht eine Fassung ab, ist zu klären, wer die Spec besser
liest.

`TZ-02` liefert **eine echte Divergenz**: die Rust-Fassung entzieht einem Vouch ohne `t_exp`
die Kante, die Referenz vermerkt und rechnet weiter. Wirkung bis ins Ergebnis (`simultan` 3
gegen 2 in `Z8`). Der Text entscheidet gegen die Rust-Fassung — `§3.1`, `§6.2` und der
einleitende Satz von `§10` sagen alle dasselbe. Die Lücke ist trotzdem echt: `§10` nennt zu
jedem Vermerk das Subjekt und zu keinem die Wirkung. Das ist O67.

`TP-02` und `FALL-02` decken sich vollständig. Und die `inf`-Zeilen trennen sich dabei um
fast den Faktor vier, ohne dass eine Ergebniszeile abweicht: **D381 ist damit gemessen, nicht
mehr nur argumentiert.** Nebenbefund: die Referenzformel liegt bei `R3` rund `2^59` unter
`u64::MAX` — eine weitere Sprosse bräche sie in einem begrenzten Typ.

## Werkzeugnotizen

- **Das Werkzeug lässt den Branch ausgecheckt zurück.** `git checkout main` gehört vor jeden
  Merge-Block, sonst läuft der Merge gegen sich selbst und `git branch -d` scheitert.
- **Splices werden im Supervisor-Klon probegefahren**, samt `check_specs.py` und `offen.py`.
  Hat in dieser Sitzung zwei Fehler abgefangen, bevor sie ankamen.
- **Ein erfundenes Beispiel in Zitatform gehört nicht in Spec-Text.** Ein O-Entwurf nannte
  eine absichtlich ungültige Adresse zur Erläuterung; `check_specs.py` las sie als echten
  Verweis und meldete sie. Prüfregel-Kandidat.
- **`check_specs.py` prüft Abschnitte auf Existenz, Anhänge nicht.** Gemessen: eine erfundene
  Paragraphennummer fällt auf, ein erfundener Anhang nicht (O64).
- **fish:** `$` in doppelten Anführungszeichen ist Interpolation — Regex mit `$` gehört in
  einfache. `diff … >datei` mit `or echo` hält die Kette am Leben, wenn ein Unterschied
  erlaubt ist.
- **Der Container:** `mar-rs-box` mit drei Mounts — `~/mar-rs` nach `/work`, Volume
  `mar-rs-auth` nach `/root/.local/share/opencode`, Volume `mar-rs-cargo` nach
  `/usr/local/cargo/registry`. Dockerfile in `~/mar-rs-box`.
- **Im Supervisor-Sandbox fehlen `cbor2` und `pynacl`** — `pip install --break-system-packages`
  vor dem ersten Referenzaufruf. Kein `.venv` dort; im Repo gilt unverändert `.venv/bin/python`.
- **Ausgabe kürzen, aber nie den Diff** — und bei Prüfwerkzeugen `grep -v "  ok  "` statt
  `tail`, sonst schneidet die Kürzung die Befundzeile ab.

## Offene Punkte, nach Grösse

**O61** bleibt das grösste inhaltliche, unverändert seit `00bl`.

**O67 — die Wirkungsspalte in `02 §10`.** Braucht `02a §2.3` im Wortlaut, bevor die drei
Dekodierfälle beschrieben werden können. Direkter Ertrag des Rust-Laufs.

**O65 — Strukturen ohne Wirkung.** Gruppen mit `0 0`, Budgetzeilen mit Summe null, Kanten mit
`cap 0`: die Rust-Fassung druckt sie, die Referenz filtert sie. Dieselbe Frage an drei
Zeilenarten. Dazu die fehlende Legende für `bytes` in `01 Anhang C`.

**O66 — selbstgetragene Adressen im Index.** `check_fragen.py` liest nur
`fragen-adressen.md`; `rs/FRAGEN.md` trägt seine Adressen selbst und steht in keiner
Indexzeile. Einfacher Werkzeugzug.

**O64 — Anhangsverweise ungeprüft.** Betrifft jede Spec-Datei, nicht nur die Zuordnung.

**Daneben:** O60 (Budget-/Kantensatz-Asymmetrie). D354 mit der Gabel F2. O56 (PyPI-Name
belegt). **O57 (Restack, Frist 3. November)** — die einzige Frist im Bestand.

**Nicht gemessen:** ob `02a` weitere Stellen trägt, die eine spätere Entscheidung überholt
hat. `tools/register_index.py` kennt die Verweise schon.

**Ungeklärt aus `00be`:** die Invariantentabelle `02a §7` kennt keine Zeitaussage. Ob D362
dort eine Zeile braucht, ist weiterhin nicht entschieden und weiterhin kein O-Posten.

**Ohne Frist:** die Übertragung auf unterbrochene Zustellung (LoRa/Reticulum).
Anschlusspunkte D345, D346, D350, D353, D361, D362, D363.

## Der nächste Schritt

**O67**, weil es der einzige offene Posten ist, den der Lauf selbst erzeugt hat, und weil
der Befund frisch ist. Zuerst `02a §2.3` im Wortlaut lesen — ohne diese Stelle lassen sich
die drei Dekodierfälle nicht beschreiben, und der Eintrag würde raten.

Danach O66 und O65, beide klein. O65 braucht vor der Entscheidung eine Antwort darauf,
warum die Referenz den `E⁺`-Filter dort setzt, wo sie ihn setzt.

**Zu bedenken:** eine vierte Fassung ist nicht beschlossen. Wenn sie kommt, gilt D390
Beschluss 2 (eigener Eintrag je Abweichung), D389 Beschluss 4 (Container), und die
Überlegung aus dieser Sitzung, ob eine knappe `AGENTS.md` die Abschlusspflichten im Kontext
hält — sie wurde bewusst **nicht** auf Vorrat gebaut.
