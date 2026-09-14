# Sitzungsstart: 00bs (MaR / symbolon), fortgeschrieben nach D377

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

Am Ende von `00bs`: **820 Tests**, Register **D1–D377**, Prüfregeln **1–75** (unverändert),
62 Posten, `make check` grün, `main` und `origin/main` gleichauf bei `ecc00d5`. **30
Wurzel-Markdown-Dateien, alle gebunden**; `archiv/` stand bei 129, und mit diesem
Sitzungsstart fällt `sitzungsstart-00bl.md` dazu.

**Zwei Stränge**, nicht einer: `main` und `00bo-hs`. Letzterer trägt die erste
Haskell-Fassung, ist kontaminiert (siehe unten) und wird **nicht gelöscht** — seine
Fragenliste hat D374 getragen und liegt sonst nirgends.

Die Sitzung umfasste sieben Runden: `00bm` (D371, Ankerkopie), `00bn` (Vektorsatz TP-02),
`00bo` (D372, Auftrag, beide Haskell-Läufe), `00bp` (D373, D374), `00bq` (D375),
`00br` (TZ-02), `00bs` (D376, D377).

### Die Schichten

Unverändert seit `00ar` — siehe `arbeitsweise.md`, `pruefregeln.md`, `08-scope.md §3`.

### Der Bestand

Neu im Baum: `hs/` (Ankerkopie, Auftrag, Vektorsatz), `tests/trust/tz02.py`,
`tools/export_tp02.py`, `tools/export_tz02.py`, `tests/vectors/vectors_02_tp02.json`,
`tests/vectors/vectors_02_tz02.json`, zwei Vergleichstests. Geändert: `07-decisions.md`,
`offen.md`, `02-trust-flow.md` (ein Absatz in `§4`), `go/spec/STAND.md` (eine Zeile),
`tests/trust/test_groups.py` (Aufbau ausgelagert), `.gitignore`.

**Ausserhalb des Repositoriums:** `~/mar-hs2` — die zweite Haskell-Fassung, isoliert
gebaut, eigenes Git. Nicht im Baum und soll es nicht sein. Dort liegt auch ihre
`FRAGEN.md` mit 19 Einträgen.

## Was in dieser Sitzung entschieden wurde (D371–D377)

**D371 — Ort, Commit und Textform des Layer-02-Ankers.** `hs/spec/` mit
`01-claim-atom.md`, `02-trust-flow.md` und einer `STAND.md`, die den Ankercommit und beide
Blob-Hashes trägt, beides aus dem Baum abgeleitet statt getippt. Der benannte Commit ist
der Kopf zum Zeitpunkt der Kopie, nicht der spätere Auftragscommit — sonst wäre die Kopie
dazwischen nicht eingefroren. Die Textform nennt ausdrücklich, was zurückgehalten ist,
damit eine spätere Fassung das Fehlen nicht als Versehen nachreicht.

**D372 — die Messfläche.** Gestufte Ausgabe je Profil: Zustand, Gruppe, Budget, Kante,
dann Fluss, simultan, disjunkt, Schnitt, zuletzt die Vermerke. Grund ist D368 Beschluss 2.
Geprüft wurde, ob die Stufen Begriffe des Ankersatzes sind: `Budget-Set`, `n_budget`,
`n_kante`, `Distanz` und `Fluss` stehen in `02`, `lassifik` kommt null Mal vor — die erste
Stufe holt ihren Namen aus `01`. Das Flag wird im Auftrag gesetzt, weil die Ankerwerte beim
anderen Wert gelten als der Vorgabewert im Text. Die Schnittseite bleibt offen gelassen,
mit Vorhersage.

**D373 — der Ankersatz zitiert seine eigene Prüfdatei.** `02-trust-flow.md` nennt
`02-golden-anchors.md` viermal namentlich und druckt Ankerwerte mit: simultan 4 für A, E
und F, für F zusätzlich Summe 10. Das Leck wird **ausgewiesen, nicht gestopft** — ein
normativer Text, dem man die Belege nimmt, ist schlechter geworden, um besser gemessen zu
werden. Wer eine Fassung gegen die Anker hält, darf diese Werte nicht als unabhängige
Bestätigung lesen.

**D374 — der Doppellauf.** Zwei Haskell-Fassungen, beide treffen über alle acht Profile
jeden Flusswert, jede Budgetsumme, jede Befundadresse. Der Ertrag lag **nicht** in den
Ausgaben, sondern in den Fragenlisten: ein Lesefehler an `01` Anhang B.1 (`malformed` ist
kein Klassifikationsergebnis, die zweite Fassung zitiert den Satz und druckt den Zustand
trotzdem), die `∞`-Kodierung als ungemessene Lücke, und ein Defekt im eigenen Vektorsatz.
Beschlossen: `t_exp` fliegt aus dem Satz; zwei Achsen (zwei Modelle messen Lesbarkeit, zwei
Sprachen messen Zahlbereich); die Fragenliste wird vor einer dritten Fassung gegliedert.

**D375 — der Schnitt ist eine Kapazität, keine Knotenmenge.** Die Referenz liefert für A
und F je CAROL und für B die leere Menge; beide Fassungen liefern alle quellseitig
erreichbaren Identitäten. `02a §3` normiert die Form, `02 §4` kannte nur die Schranke und
daneben den Begriff `Grenze` — zwei verschiedene Mengen, und der Text sagte nirgends, dass
sie es sind. `§4` hat den Absatz jetzt. Enthält zugleich die Korrektur an D374, dessen
Abnahmesatz die Übereinstimmung unzulässig auf die Referenz ausdehnte.

**D376 — TZ-02.** Neun Profile aus Anker 5, 5b und 5c, achtzehn Werte unabhängig
nachgerechnet und alle getroffen. `revoked`, `superseded` und `expired` sind zum ersten Mal
beobachtbar. Vorbehalt: in Z7 bis Z9 läuft das Mesh ab, die **Flusswerte** dieser drei
Profile haben deshalb keine Ankerdeckung — zwischen Fassungen vergleichbar, gegen die Anker
nicht prüfbar.

**D377 — das Überlaufkriterium wird gemessen, bevor es eine Sprache auswählt.** Ein
Kapazitätsprofil mit grossem `C₀` trennt die beiden `∞`-Kodierungen: das feste Literal
bindet irgendwann, die mitwachsende Summe sprengt einen 64-Bit-Typ. Ausdrücklich als
**Falltest** geführt, nicht als Anker — er misst nicht den Text, sondern ob eine Fassung
eine Entscheidung robust getroffen hat, die der Text ihr überlässt.

## Der Ablauf, und wo die Fehler diesmal sassen

Zwei Werkzeugläufe im Repo (`00bn`, `00br`), beide ohne Defekt in der Abnahme. Zwei
Haskell-Läufe ausserhalb. Die Fehler sassen wieder überwiegend beim Supervisor:

1. **Der erste Haskell-Lauf lief im Repo-Kontext.** Belegt, nicht vermutet: seine
   Fragenliste begründet mit „D41 / D372", und D372 steht in keiner Datei unter `hs/`. Der
   Zahlenvergleich hätte das nie gezeigt — beide Fassungen treffen jede Ankerzahl, und eine
   korrekte unabhängige Fassung sieht aus wie eine abgeschriebene.
2. **Der Verdacht auf Kontamination beim zweiten Lauf war falsch** und fiel auf den
   Ankersatz zurück (D373). Der erste Reflex, „Treffer auf ganzer Linie wäre das schlechte
   Zeichen", behandelte Korrektheit als verdächtig und war in die bequeme Richtung falsch.
3. **D374 behauptete Übereinstimmung mit der Referenz für die Schnittmengen**, die nie
   gegen die Referenz geprüft waren. Vier Runden auf `main`, gefunden bei der Vorbereitung
   einer anderen Runde. D366-Klasse an einer Stelle, die Prüfregel 75 nicht abdeckt.
4. **Ein Branch zweigte vom falschen Kopf ab**, weil die Ausgangslage in Prosa fixiert war
   statt in der Kette. Repariert per Cherry-pick.
5. **`python3` statt `.venv/bin/python`**, obwohl Zeile 1 des Makefiles es seit jeher sagt.

Gemeinsamer Nenner mit `00bl`: der erzählende Teil nach der Messung. Neu und wichtiger:
**zweimal hat nicht das gebaute Instrument gefunden, sondern die beiläufige Lektüre.** Der
Schnitt-Befund kam aus einem Blick in `test_anchors.py` während der Vorbereitung von TZ-02,
nicht aus der gestuften Ausgabe, für die ein ganzer Registereintrag aufgewendet wurde.
Daraus folgt kein neues Instrument, sondern eine Reihenfolge: **der Abgleich gegen die
Referenzzusicherungen in `tests/` gehört vor den Abgleich der Fassungen untereinander.**

## Werkzeugnotizen

- **Jeder Python-Aufruf im Repo läuft über `.venv/bin/python`.** Makefile Zeile 1.
  `python3` findet `cryptography` nicht.
- **`git switch main` gehört als erster Job in die Kette**, nicht in die Prosa davor. Sonst
  zweigt der Lauf-Branch von dem ab, wo der letzte Zug endete.
- **`splice_run.py` verlangt den Baum vollständig sauber**, auch bei `M`-Dateien, nicht nur
  bei untracked. `.gitignore`-Änderungen also vorher committen.
- **Ein Splice, der neue Dateien anlegt, verträgt sich nicht mit `splice_run.py`** — aber
  sequentiell im selben Block mit Commit dazwischen geht es (in `00bm` und `00bo` so
  gemacht).
- **`grep` ohne Treffer gibt Exit 1** und bricht die `and`-Kette. Mit `or echo ...`
  abfangen oder in eine Datei schreiben und `tail`-en.
- **Backslash-Zeilenfortsetzungen überleben das Kopieren nicht** und laufen zu einer Zeile
  zusammen. Fish braucht sie nicht.
- **Der Supervisor-Sandbox veraltet innerhalb einer Sitzung.** Vor jedem Trockenlauf
  `git fetch` und `git reset --hard origin/main`.
- **Im Supervisor-Sandbox fehlen die Abhängigkeiten.**
  `pip install pytest cbor2 cryptography --break-system-packages`; `hypothesis` fehlt,
  deshalb dort `--ignore=tests/property`.
- **Die Vektordateien heissen `vectors_02_tp02.json` und `vectors_02_tz02.json`**, die
  Fixtures `tp02.py` und `tz02.py`, die Exporter `export_tp02.py` und `export_tz02.py`.
- **Ausgabe kürzen, aber nie den Diff.** Bei grossen Diffs: in eine Datei schreiben,
  `--stat` zurückschicken und gezielt den relevanten Teil nachziehen.

## Offene Punkte, nach Grösse

**O62 — die Layer-02-Zweitfassung.** Flusshälfte bestätigt (D374, unter Abzug von D373),
Zustandshälfte durch TZ-02 vorbereitet aber noch von keiner Fassung gelesen. Die Reihenfolge
steht in D377: erst der **Falltest** zum Kapazitätsbereich, dann die **Sprachwahl**, dann
eine **neue Ankerkopie**, die `TZ-02` und den `§4`-Absatz aus D375 mitführt. `hs/spec/`
steht auf `764f0da` und trägt beides nicht.

Der Sprach-Fork ist schwieriger als er aussieht: D374 Beschluss 3 will einen begrenzten
Standardtyp, D370 hat gemessen, dass genau dort die Bibliothekslage dünn ist — Rusts
einzige ganzzahlgenerische Max-Flow-Bibliothek unter GPL-3, keine etablierte in Go,
`double` in JGraphT. Die Kriterien ziehen gegeneinander; der Falltest entscheidet, welches
nachgibt.

**Ebenfalls aus D374 offen:** die Gliederung der Fragenliste nach Spec-Abschnitt. Zwei frei
nummerierte Listen gegeneinanderzuhalten war Handarbeit; bei drei Fassungen skaliert das
nicht.

**O61** bleibt das grösste inhaltliche, unverändert seit `00bl`.

**Daneben:** O60 (Budget-/Kantensatz-Asymmetrie). D354 mit der Gabel F2. O56 (PyPI-Name
`symbolon` belegt). O57 (Restack, Frist für Nachbesserung **3. November**).

**Nicht gemessen:** ob `02a` weitere Stellen trägt, die eine spätere Entscheidung überholt
hat. D369 fand eine zufällig. Ein systematischer Abgleich ist nicht gelaufen und wäre eine
eigene Runde wert — `tools/register_index.py` kennt die Verweise schon.

**Nicht gemessen:** Distanzen, Kapazitäten und Flusswerte von `TZ-02` für Z1 bis Z6. Die
Grundlage dafür gibt es, sie ist ungenutzt geblieben.

**Ungeklärt aus `00be`:** die Invariantentabelle `02a §7` kennt keine Zeitaussage. Ob D362
dort eine Zeile braucht, ist weiterhin nicht entschieden und weiterhin kein O-Posten.

**Ohne Frist:** die Übertragung auf unterbrochene Zustellung (LoRa/Reticulum).
Anschlusspunkte D345, D346, D350, D353, D361, D362, D363.

## Der nächste Schritt

**Der Falltest aus D377.** Ein Werkzeuglauf im Repo: ein eigener kleiner Vektorsatz mit
Variante-A-Aufbau und grossem `C₀` als Zweierpotenz, ausdrücklich als Falltest benannt,
neben `TP-02` und `TZ-02`. Die Erwartung folgt aus der Formel — `trust(ALICE → gᵢ)` ist
`⌊C₀·γ²⌋` und die Kante trägt denselben Wert —, es entsteht also keine neue Ankerzeile.

Danach gegen beide vorliegenden Haskell-Fassungen laufen lassen: die zweite liegt in
`~/mar-hs2` und ist in einer Minute gestartet, die erste auf `00bo-hs`. Erwartet wird, dass
die zweite falsch rechnet, sobald eine echte Kapazität ihr festes Literal überholt. Trifft
das ein, ist die `∞`-Lücke belegt und die Sprachwahl bekommt ihr Gewicht.
