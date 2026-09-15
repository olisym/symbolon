# Sitzungsstart: 00bt (MaR / symbolon), fortgeschrieben nach D379

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

Am Ende von `00bt`: **831 Tests**, Register **D1–D379**, Prüfregeln **1–75** (unverändert),
**63 Posten**, `make check` grün, `main` und `origin/main` gleichauf bei `e416413`. **30
Wurzel-Markdown-Dateien, alle gebunden**; `archiv/` stand bei 130, und mit diesem
Sitzungsstart fällt `sitzungsstart-00bs.md` dazu.

**Zwei Stränge**, nicht einer: `main` und `00bo-hs`. Letzterer trägt die erste
Haskell-Fassung, ist kontaminiert (D374) und wird **nicht gelöscht**.

Die Sitzung umfasste vier Runden: `00bt-a` (D378, Profilentwurf), `00bt-b` (Werkzeuglauf
`FALL-02`), `00bt-c` (Abnahme und Merge), `00bt-d` (D379, O63).

### Die Schichten

Unverändert seit `00ar` — siehe `arbeitsweise.md`, `pruefregeln.md`, `08-scope.md §3`.

### Der Bestand

Neu im Baum: `tests/trust/fall02.py`, `tests/trust/test_fall02.py`,
`tests/trust/test_vectors_fall02.py`, `tools/export_fall02.py`,
`tests/vectors/vectors_02_fall02.json`. Geändert: `07-decisions.md`, `offen.md`.
Nichts unter `symbolon/`, nichts unter `hs/`, keine Ankerdatei berührt.

**Ausserhalb des Repositoriums:** `~/mar-hs2` — die zweite Haskell-Fassung, isoliert
gebaut, eigenes Git. Dort auch ihre `FRAGEN.md` mit 19 Einträgen.

## Was in dieser Sitzung entschieden wurde (D378, D379)

**D378 — der Falltest bekommt sein Profil, und die Schwelle teilt sich in zwei.** `FALL-02`:
ein Graph, drei Kapazitäten. Kette ALICE nach BOB nach CAROL mit je n=4, dann ein Fächer
CAROL nach g1 mit n=2 und nach g2, g3 mit je n=1 — Budgetsumme bei CAROL genau D, **null
Befunde**, kein `include_flagged`. Variante A wäre der naheliegende Aufbau gewesen und ist
der falsche: sie ist überzeichnet, ihre Ankerwerte entstehen nur mit gesetztem Flag, und
ohne Flag liefert sie Wert 0 und leeren Schnitt — gemessen, nicht vermutet.

Die drei Sprossen, alle achtzehn Werte gegen die Referenz gerechnet:

| Sprosse | C0 | value | INF | int64 | festes Literal 10^18 |
| --- | --- | --- | --- | --- | --- |
| R1 | 1152921504606846976 | 288230376151711744 | 4467570830351532033 | trägt | richtig |
| R2 | 3458764513820540928 | 864691128455135232 | 13402712491054596097 | überläuft | richtig |
| R3 | 4611686018427387904 | 1152921504606846976 | 17870283321406128129 | überläuft | klippt |

Überall `disjoint_paths` 1, Schnitt CAROL, Befundliste leer. Der eigentliche Ertrag ist R2:
dort rechnet die Abkürzung der zweiten Haskell-Fassung **richtig** und der Normtext ist in
int64 **nicht implementierbar**. D374s Satz, die naheliegende Wahl sei die brüchige, gilt
erst oberhalb der zweiten Schwelle.

**D379 — INF hängt am Bestand, nicht an der Kalibrierung.** `02a §2.8` summiert über alle
Knoten und Kanten; für die drei in D378 gerechneten Aufbauten sind das 29, 31 und 35 Achtel
von C0 bei sechs bis sieben Identitäten. Damit ist die Frage, ob INF in einen begrenzten
Typ passt, nicht aus den Parametern zu beantworten. Der Eintrag skizziert eine engere
Schranke — der Fluss passiert in jedem Fall die internen Ankerkanten, also genügt die Summe
der C(0) über die Anker, im Einheitslauf die Kantenzahl —, beweist sie **nicht** und legt
sie als **O63** ab. Keine Textänderung an `02a` in dieser Sitzung, weil `FALL-02` drei
INF-Werte pinnt und Eingabe eines laufenden Vergleichs ist.

## Der Ablauf, und wo die Fehler diesmal sassen

Ein Werkzeuglauf, ohne Defekt in der Abnahme: der gelieferte Diff wurde im
Supervisor-Sandbox aus dem Diff **neu gebaut und ausgeführt**, die Vektordatei unabhängig
erzeugt und gegen die gelieferten Hexwerte gehalten. Die Fehler sassen sämtlich beim
Supervisor, und vier von fünf sind Übertragungsfehler an Stellen, die vorher korrekt
gelesen worden waren:

1. **Der Sitzungsstart wurde gegen das Register gestellt.** Die Behauptung, D377 sei in
   seiner zweiten Hälfte widerlegt, war falsch: D377 nennt den `Integer`-Vorbehalt selbst,
   die Zusammenfassung verkürzt ihn. Prüfregel 38, an der eigenen Datei.
2. **Der Haskell-Quelltext wurde falsch gelesen.** Die Zeile mit `anchorSet -> 0` steht
   unter `UnitMode`, nicht unter `CapMode`; HS1 belegt die interne Ankerkante im Flusslauf
   mit C(0) wie die Referenz. Der daraus gebastelte Verdacht auf eine ungemessene
   Abweichung war ein Phantom. Nachgemessen: in `A'` bindet C(0) tatsächlich, simultan 16
   bei C0 16 — gäbe es die Abweichung, hätte D374 sie an diesem Profil gesehen.
3. **Splice-Anker in `ae`/`ue` getippt**, obwohl die Zieldatei Umlaute trägt. Der Assert hat
   es gefangen.
4. **Der erste Splice war nicht atomar** — er schrieb das Register und brach dann an
   `offen.md` ab. Auf der Kopie folgenlos, auf dem Baum wäre eine halbe Änderung
   liegengeblieben. Seitdem: beide Dateien prüfen, dann beide schreiben.
5. **Ein Pfad in Prosa korrigiert und im Shell-Block stehen gelassen.**

Gemeinsamer Nenner: nicht das Messen, sondern das Übertragen des Gemessenen. Daraus folgt
kein neues Instrument, sondern eine Gewohnheit — **was einmal gelesen wurde, wird beim
Zitieren erneut aufgeschlagen, nicht aus dem Gedächtnis wiedergegeben.**

## Werkzeugnotizen

- **Der Spiegel trägt `00bo-hs` nicht**, nur `main`. Die erste Haskell-Fassung ist für den
  Supervisor nicht lesbar; sie muss über den Operator geholt werden.
- **Im Supervisor-Sandbox gibt es kein `.venv`.** Dort `python3` mit
  `PYTHONPATH=<repowurzel>`; `pip install pytest cbor2 cryptography --break-system-packages`,
  `hypothesis` fehlt, deshalb `--ignore=tests/property`. Im Repo gilt unverändert: **jeder
  Aufruf über `.venv/bin/python`**, Makefile Zeile 1.
- **`tools/stand.py` hat in dieser Sitzung nichts ausgegeben** — kein Fehler, keine Zeile,
  Kette lief weiter. Ungeklärt. Die Kaltzahlen kamen aus `check_specs.py`, `offen.py` und
  `pytest`.
- **`grep --include=*.hs` braucht in fish Anführungszeichen** (`--include="*.hs"`), sonst
  bricht die Glob-Expansion den Aufruf ab.
- Splices: Anker dienen als Nachweis der erwarteten Fassung, **angehängt wird am
  Dateiende** — das umgeht das Raten innerer Zeilenumbrüche.
- Ankerwerte in `test_anchors.py` laufen sämtlich mit `include_flagged=True`. Wer ein Profil
  aus `TP-02` nachbaut, erbt das stillschweigend.
- **Ausgabe kürzen, aber nie den Diff.**

## Offene Punkte, nach Grösse

**O62 — die Layer-02-Zweitfassung.** Flusshälfte bestätigt (D374, unter Abzug von D373),
Zustandshälfte durch `TZ-02` vorbereitet und weiterhin von keiner Fassung gelesen. Die
Reihenfolge aus D377 ist um einen Schritt fortgeschritten: der **Falltest steht** (D378),
offen sind der **Lauf**, dann die **Sprachwahl**, dann eine **neue Ankerkopie**, die
`TZ-02` und den `§4`-Absatz aus D375 mitführt. `hs/spec/` steht auf `764f0da` und trägt
beides nicht.

Der Sprach-Fork bleibt schwierig: D374 Beschluss 3 will einen begrenzten Standardtyp, D370
hat gemessen, dass dort die Bibliothekslage dünn ist. **D379 verschiebt das Gewicht**: ist
die engere Schranke haltbar, kostet der begrenzte Typ weniger als D377 annahm.

**O63 — der INF-Sentinel** (neu, aus D379). Erst der Lauf, dann dieser Posten; die
Reihenfolge ist Teil des Beschlusses.

**Ebenfalls aus D374 offen:** die Gliederung der Fragenliste nach Spec-Abschnitt.

**O61** bleibt das grösste inhaltliche, unverändert seit `00bl`.

**Daneben:** O60 (Budget-/Kantensatz-Asymmetrie). D354 mit der Gabel F2. O56 (PyPI-Name
`symbolon` belegt). O57 (Restack, Frist für Nachbesserung **3. November**).

**Nicht gemessen:** ob `02a` weitere Stellen trägt, die eine spätere Entscheidung überholt
hat. D369 fand eine zufällig; ein systematischer Abgleich ist nicht gelaufen —
`tools/register_index.py` kennt die Verweise schon.

**Nicht gemessen:** Distanzen, Kapazitäten und Flusswerte von `TZ-02` für Z1 bis Z6.

**Ungeklärt aus `00be`:** die Invariantentabelle `02a §7` kennt keine Zeitaussage. Ob D362
dort eine Zeile braucht, ist weiterhin nicht entschieden und weiterhin kein O-Posten.

**Ohne Frist:** die Übertragung auf unterbrochene Zustellung (LoRa/Reticulum).
Anschlusspunkte D345, D346, D350, D353, D361, D362, D363.

## Der nächste Schritt

**`FALL-02` gegen beide vorliegenden Haskell-Fassungen.** Eingabe ist
`tests/vectors/vectors_02_fall02.json`, unverändert, in derselben JSON-Form wie `TP-02` —
beide Fassungen sollten sie ohne Anpassung lesen. Die zweite liegt in `~/mar-hs2` und ist in
einer Minute gestartet, die erste auf `00bo-hs`.

**Vorhersage, vor dem Lauf fixiert:**

- **HS1** (`infOf xs = 1 + sum xs`, `Integer`) trifft alle drei Sprossen.
- **HS2** (`inf = 1000000000000000000`, `Integer`) trifft R1 und R2 und rechnet auf **R3
  falsch**: Flusswert 1000000000000000000 statt 1152921504606846976, und der Schnitt wird
  **leer** statt CAROL, weil die bindende Kante dann die Quellkante ist.

Trifft das ein, ist die `∞`-Lücke belegt und die Sprachwahl bekommt ihr Gewicht. Trifft es
nicht ein, ist die Vorhersage falsch und nicht der Falltest — **melden, nicht anpassen.**

Vor dem Vergleich der Fassungen untereinander steht der Abgleich gegen die
Referenzzusicherungen in `tests/` (Reihenfolge aus `00bs`).
