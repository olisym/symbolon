# Sitzungsstart: 00bl (MaR / symbolon), fortgeschrieben nach D370

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

Am Ende von `00bk`: **817 Tests**, Register **D1–D370**, Prüfregeln **1–75**, 62 Posten,
`make check` grün, `main` und `origin/main` gleichauf bei `8b98f56`. **30 Wurzel-Markdown-
Dateien, alle gebunden**; `archiv/` stand bei 128, und mit diesem Sitzungsstart fällt
`sitzungsstart-00bg.md` dazu. Ein Branch.

Die Sitzung umfasste fünf Runden: `00bg` (D366, Prüfregel 75), `00bh` (D367, Anker 5c, O62),
`00bi` (D368), `00bj` (D369), `00bk` (D370). Alle fünf sind Registerrunden; berührt wurden
in `symbolon/` nur zwei Kommentarzeilen.

### Die Schichten

Unverändert seit `00ar` — siehe `arbeitsweise.md`, `pruefregeln.md`, `08-scope.md §3`.

### Der Bestand

Geändert: `07-decisions.md`, `offen.md`, `pruefregeln.md`, `02-golden-anchors.md`,
`02-trust-flow.md`, `02a-maxflow-prompt.md`, `go/spec/STAND.md`,
`symbolon/trust/findings.py` (ein Kommentar), `symbolon/trust/graph.py` (ein Kommentar).
Keine neue Datei, kein Verhaltenswechsel — die 817 Tests waren über alle fünf Runden
unverändert grün.

**Ausserhalb des Repositoriums, bei Oli lokal:** `restack-faktensammlung.md`,
`restack-felder-englisch.md`, `prompt-log.py` und `prompt-log-restack.md` in `~/Downloads`.
Bewusst nicht im Baum. Wenn der Antrag vor dem 3. November nachgebessert wird, sind das die
Dateien dafür.

## Was in dieser Sitzung entschieden wurde (D366–D370)

**D366 und Prüfregel 75 — ein „nächster Schritt" ist Behauptung, keine Messung.** `00bg`s
Schlussabsatz charakterisierte den Codezustand zur Einhegung aus `02 §6.2`: der Autor sehe
beim Binden nichts, es gebe kein Reject und keine Warnung auf der Schreibseite. Diese Runde
übernahm den Satz als Prämisse. Zwei Lesedurchgänge widerlegten ihn:
`tools/example_nucleus.py`s `_Author.vouch()` verlangt `t_exp: int` bereits ohne Default, und
`symbolon/trust/__init__.py`s `__all__` exportiert `groups.py` nicht — die vermeintliche
Code-Lücke war eine Sichtbarkeitslücke. Regel 74 deckte davon nur den Prompt-Teil; Regel 75
erweitert es auf jede Codezustands-Behauptung im Sitzungsstart. Der eigentliche Befund lief
als Nachtrag unter D364: `02 §6.2` nennt jetzt die Unwiderruflichkeit,
`TrustFinding.VOUCH_WITHOUT_TEXP` trägt einen Verweis.

**D367 — die Messfläche vor der Zweitimplementierung, auch auf Layer 02.** Gemessen: die
gesamte Layer-02-Ankerfläche trug in jedem Vektor ein `t_exp`; §1 setzt es als Default. D364
stand damit ausschliesslich in Python-Prüffällen, und D256 Beschluss 3 schliesst die
Referenzausgabe als Erwartungsquelle aus. Beschlossen und gedruckt: **Anker 5c**, der
`t_exp`-lose Budget-Fall, abgeleitet aus `02a §2.6` und D135, mit der Referenz nur als
Gegenprobe. Zweiter Beschluss: eigener Anker für Layer 02 (D302). Dritter:
`go/spec/STAND.md` nachgezogen — der Satz „seit `79b73a2` unverändert" war falsch geworden,
der Blob ist intakt, der Anker wandert nicht.

**D368 — Umfang und Ankersatz.** Die Vermutung, die Gruppenbildung sei die billige Hälfte,
ist gemessen gefallen: `index.py` und `verifier.py` sind zusammen 525 Zeilen und
Voraussetzung **beider** Hälften, die Gruppenhälfte 308, die Solverhälfte 325 — davon 92
Zeilen Dinic. Beschlossen: gebaut werden `classify_all`, Gruppen- und Budgetstufe und der
Graphbau nach `02a §2.8`; der Max-Flow kommt aus einer Bibliothek. Ankersatz:
`01-claim-atom.md` und `02-trust-flow.md`, eigene `STAND.md`; `02-golden-anchors.md` und
`02a` werden zurückgehalten. Kein Vektorlauf für `superseded` und `expired` — anders als bei
D367 gibt es hier Abdeckung, nur keine Auflösung.

**D369 — `02a §4` trug die von D42 verworfene Belegung.** Beim Lesen von `graph.py` vor der
Beauftragung gefunden: der Kommentar dort nannte sich eine Abweichung von K5, obwohl K5 `1`
sagt und der Code ihr folgt. `02a §4` stand in der Vouch-Spalte auf `INF` — die
D32-Belegung, die D42 ausdrücklich verworfen hat. Nachgezogen, Kommentar auf D42 umgestellt,
kein Verhaltenswechsel.

**D370 — Haskell.** Klarstellung zu D256: dessen Begründung lautet „nicht selbst schreiben",
nicht „muss Standardbibliothek sein" — eine etablierte Fremdbibliothek für die Signatur
genügt. Das Max-Flow-Kriterium wurde **nicht** gelockert: Eigenbau misst nichts, eine
Float-Bibliothek bringt eine fremde Divergenzklasse. Gemessen wurde die Bibliothekslage;
Rusts einzige ganzzahlgenerische Bibliothek steht unter GPL-3, die übrigen rechnen in `f64`,
Go hat keine etablierte, JGraphT nimmt `double`. Haskell gewinnt auf drei Punkten: `Integer`
als Standardtyp erledigt das Überlaufkriterium der Kapazitätsleiter, BSD-3 erspart die
Lizenzanalyse, und Reinheit stellt jede `now`- und Speicherabhängigkeit in den Typ.
Rückfallweg benannt: OCaml mit `ocamlgraph` und Zarith.

## Der Ablauf, und wo die Fehler diesmal sassen

Kein Werkzeuglauf in dieser Sitzung — fünf Splices, alle vom Supervisor geschrieben. Die
Fehler sassen entsprechend alle dort, und alle fielen vor dem Merge:

1. `00bg`s erster Prompt verwies für den Registertext auf eine „Registervorlage im
   Sitzungsprotokoll", die es nicht gibt. Das Werkzeug hat angehalten und nachgefragt, statt
   den Wortlaut zu erfinden — Prüfregel 27, richtig angewandt. Vermerkt in D366.
2. `00bg`s erster Splice liess `02-trust-flow.md` mit einem ausgefransten Absatz zurück
   (31-Zeichen-Rest). `check_specs.py` sieht das nicht, es prüft nur die Obergrenze. Im Diff
   gefunden, korrigierter Splice.
3. `00bh`s erste Ankertabelle war für `now = 10**6` falsch: dort laufen auch die Nachbarn
   mit dem Default `t_exp = 5000` ab. Geschrieben aus der Form der Aussage statt aus den
   Werten — die D366-Klasse, gefangen von der Gegenprobe. Der Anker trägt seither ein fernes
   `t_exp` für die Nachbarn.
4. `00bh`s zweite Fassung beschriftete die Vergleichszeilen als „Anker 5", obwohl sie diesen
   Aufbau wiedergeben. Eine Zweitfassung hätte daraus einen Scheinbefund gemacht. Im Diff
   gefunden.
5. Die Position zum Umfang von O62 — „Gruppenbildung ist die billige Hälfte" — war falsch
   und ist in `00bi` von der Messung gekippt worden, nicht von einem Argument.

Gemeinsamer Nenner wie in `00bf`: der erzählende Teil, geschrieben nach der Messung. Die
Messungen selbst waren jedes Mal richtig. Neu ist, dass diesmal jeder dieser Fehler von einem
bereits vorhandenen Instrument gefangen wurde — Gegenprobe, Diff-Lektüre, Idempotenzsperre.
Eine weitere Regel dafür wäre Zeremonie.

## Werkzeugnotizen

- **Der Supervisor-Sandbox veraltet innerhalb einer Sitzung.** Zweimal lief ein Trockenlauf
  rot, weil der geklonte Baum eine Runde zurückstand und `check_specs.py` die fehlende
  D-Nummer meldete. Vor jedem Trockenlauf `git fetch` und `git reset --hard origin/main`,
  nicht nur beim Sitzungsbeginn.
- **`build_groups` hat fünf Parameter**, nicht drei: `(claims, classifications, scope, D,
  now)`. `classify_all` nimmt den **Store**, nicht die Claim-Liste, und liegt in
  `symbolon/index.py`, nicht in `verifier.py`. Beides hat in `00bh` je einen Fehlversuch
  gekostet.
- **`git --no-pager` gehört vor das Subkommando.** Gilt unverändert.
- **Im Supervisor-Sandbox fehlen die Abhängigkeiten.** `pip install pytest cbor2 cryptography
  --break-system-packages`. `hypothesis` fehlt ebenfalls — deshalb dort
  `python -m pytest -q --ignore=tests/property` (803 statt 817 Tests); das ist der bekannte
  Unterschied zu `make check`, kein Befund.
- **Ein Splice, der neue Dateien anlegt, verträgt sich nicht mit `splice_run.py`** im selben
  Zug: der Harness bricht bei untracked files ab. Ankerkopie und Splice gehören in getrennte
  Runden.
- **Der Sitzungsstart-Tausch muss committet sein, bevor ein Lauf-Branch entsteht.** In `00bg`
  lag er gestaged auf `main`, wanderte mit auf den Branch und liess `splice_run.py`
  abbrechen.

## Offene Punkte, nach Grösse

**O62 — die Layer-02-Zweitfassung.** Umfang, Ankersatz und Sprache stehen (D368, D370).
Offen sind zwei Schritte in dieser Reihenfolge: erst die **Ankerkopie** — `01-claim-atom.md`
und `02-trust-flow.md` auf den dann aktuellen Commit, eigene `STAND.md` nach dem Muster aus
D302, Blob-Hashes prüfbar mit `git hash-object` —, dann der **Auftrag**. Der Auftrag lässt
sich nicht vorher schreiben: er muss den Ankercommit benennen, und den gibt es erst mit der
Kopie.

In den Auftrag gehören: die beiden Fallen aus D370 (`Data.Graph.Inductive.Query.MaxFlow`,
nicht `MaxFlow2`; `crypton`, nicht `ed25519`), das Zurückhalten der Vektoren nach dem Muster
von `go/AUFTRAG.md`, die Fragenliste als Pflichtlieferung, und das Verfahren aus D368
Beschluss 2 — eine Abweichung an Anker 5b, 5 oder 5c wird erst zwischen Zustandsstufe und
Gruppierung lokalisiert, bevor sie als Spec-Befund geführt wird.

**O61** bleibt das grösste inhaltliche. Nach D363 und D364 unverändert: die signierte
Zeit-Attestierung löst ihn nicht, Raytime setzt eine Autorität voraus, Weg 3 ist gebaut und
braucht Einhegung, der vierte Weg hat eine offene Hauptfrage gegen D78. Die Einhegung aus
`02 §6.2` ist **nicht** erledigt — `00bg` hat nur ihren Sichtbarkeitsteil geschlossen; der
Policy-Maximallaufzeit-Zweig hängt weiter an O61.

**Daneben:** O60 (Budget-/Kantensatz-Asymmetrie). D354 mit der Gabel F2. O56 (PyPI-Name
`symbolon` belegt). O57 (Restack, eingereicht 10. September, Frist für Nachbesserung
**3. November**).

**Nicht geschlossen, bewusst:** `superseded` und `expired` haben in `01` Anhang C keinen
gedruckten Vektor (D368 Beschluss 2). Abgedeckt sind sie aggregat über Anker 5b, 5 und 5c.

**Nicht gemessen:** ob `02a` weitere Stellen trägt, die eine spätere Entscheidung überholt
hat. D369 fand eine, und zwar zufällig bei der Vorbereitung. Ein systematischer Abgleich von
`02a` gegen das Register ist nicht gelaufen und wäre eine eigene Runde wert — er ist billig,
weil `tools/register_index.py` die Verweise schon kennt.

**Ohne Frist:** die Übertragung auf unterbrochene Zustellung (LoRa/Reticulum).
Anschlusspunkte D345, D346, D350, D353, D361, D362, D363.

**Ungeklärt aus `00be`:** die Invariantentabelle `02a §7` kennt keine Zeitaussage. Ob D362
dort eine Zeile braucht, ist weiterhin nicht entschieden und weiterhin kein O-Posten.

## Der nächste Schritt

**Die Ankerkopie für O62.** Sie ist der einzige offene Punkt, der ohne weitere Entscheidung
ausführbar ist: Umfang, Ankersatz und Sprache stehen im Register, und die Kopie ist eine
Dateioperation mit Hash-Prüfung, kein Lauf. Danach der Auftrag, in derselben oder der
nächsten Runde.

Zwei kleinere Züge, falls eine kurze Runde vorgezogen werden soll: der systematische
`02a`-Abgleich gegen das Register (oben), und die INV-3-Frage aus `00be`. Der erste hat ein
messbares Zwischenergebnis, der zweite nicht — nach dem Muster der letzten Sitzungen ist das
der Unterschied, der zählt.
