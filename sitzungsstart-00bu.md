# Sitzungsstart: 00bu (MaR / symbolon), fortgeschrieben nach D382

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

Am Ende von `00bu`: **831 Tests**, Register **D1–D382**, Prüfregeln **1–75** (unverändert),
`make check` grün, `main` und `origin/main` gleichauf bei `28cc796`. **30 Wurzel-Markdown-
Dateien, alle gebunden**; `archiv/` stand bei 131, und mit diesem Sitzungsstart fällt
`sitzungsstart-00bt.md` dazu. `offen.md` führt **63 Posten**; O63 trägt seit D381 die
Schliessform.

**Zwei Stränge**, nicht einer: `main` und `00bo-hs`. Letzterer trägt die erste
Haskell-Fassung, ist kontaminiert (D374) und wird **nicht gelöscht**.

Die Sitzung umfasste drei Runden: `00bu-a` (Doppellauf `FALL-02`, D380), `00bu-b` (D381,
O63 geschlossen), `00bu-c` (D382, Sprachwahl).

### Die Schichten

Unverändert seit `00ar` — siehe `arbeitsweise.md`, `pruefregeln.md`, `08-scope.md §3`.

### Der Bestand

Kein Zuwachs im Baum. Geändert: `02-trust-flow.md`, `02a-maxflow-prompt.md`,
`07-decisions.md`, `offen.md`. Nichts unter `symbolon/`, nichts unter `tests/`, nichts
unter `hs/`. **Keine Codeänderung in dieser Sitzung** — die 831 Tests sind dieselben wie
am Ende von `00bt`.

**Ausserhalb des Repositoriums:** `~/mar-hs2` — die zweite Haskell-Fassung, isoliert
gebaut, eigenes Git, dort auch ihre `FRAGEN.md`. Flüchtig: `/tmp/mar-hs1`, per
`git archive` aus `00bo-hs` ausgepackt, und `/tmp/fall02.json` samt der um `t_exp`
angereicherten Fassung `/tmp/fall02-hs1.json`.

## Was in dieser Sitzung entschieden wurde (D380, D381, D382)

**D380 — der Doppellauf, und die Vorhersage trifft in beiden Hälften.** `FALL-02` gegen
beide Haskell-Fassungen, Eingabe hashgleich zur Repositoriumsdatei
(`65abceb6…`). HS1 (`infOf xs = 1 + sum xs`, `Integer`) trifft alle drei Sprossen in jedem
Wert. HS2 (`inf = 1000000000000000000`, `Integer`) trifft R1 und R2 vollständig und weicht
auf R3 in genau einer Zahl ab: simultan `1000000000000000000` statt
`1152921504606846976`, Schnitt leer.

Der Ertrag liegt in dem, was **nicht** abwich: auf R3 sind die drei Einzelabfragen in
beiden Fassungen korrekt, der grösste Einzelfluss liegt unter dem Literal. Die
Kapazitätsleiter rechnet in beiden bis `2^62` fehlerfrei; die Divergenz sitzt allein in der
Darstellung von `∞`. Damit ist die Bedingung aus D377 Beschluss 2 wörtlich eingetreten.

**D381 — der Sentinel wird als Bedingung normiert, nicht als Formel.** Beim Nachlesen
verschob sich die Frage: D379s Kandidat ist kein Kandidat, sondern ein **Korollar**. `02 §4`
beweist, dass jeder Pfad einen ehrlichen Grenzknoten passiert, einschliesslich des Ankers
selbst — die Ankermenge ist damit selbst ein Schnitt. `02a §2.8` normiert dieselbe
Voraussetzung ein zweites Mal (`S* → a_in`, nicht `a_out`). Das in D379 als unbewiesen
abgelegte Argument war bereits zweimal aufgeschrieben.

Beide Formeln teilen denselben Mangel: sie stehen als **Realisierung** im Normtext. Deshalb
wird nicht getauscht, sondern die Ebene gewechselt. `INF` muss echt grösser sein als jeder
erreichbare Flusswert; die Referenz behält `sum(alle endlichen Kapazitäten) + 1`, eine
engere Realisierung ist zulässig und trägt ihre Begründung selbst. Folge, die den Posten
erst lösbar machte: **die drei in `FALL-02` gepinnten INF-Werte bleiben unverändert**, weil
die Referenz ihre Belegung behält. Der Stolperdraht aus D379 löst sich auf, statt umgangen
zu werden. `02 §4` bekommt zusätzlich den Kasten, der HS2 gefehlt hätte.

**D382 — die dritte Fassung wird in Rust gebaut.** `petgraph` trägt ganzzahligen Max-Flow:
`ford_fulkerson` ist generisch über `PositiveMeasure`, implementiert für `u8` bis `usize`,
Lizenz MIT oder Apache-2.0; seit 0.8 daneben ein `maximum_flow`-Modul mit Dinic. Dazu
`ed25519-dalek` 3.0.0 (BSD-3-Clause), `sha2` (MIT/Apache) und drei gepflegte CBOR-Crates mit
deterministischer Kodierung. Damit sind alle vier Kriterien aus D370 **gleichzeitig**
erfüllt, einschliesslich des begrenzten Standardtyps aus D374 Beschluss 3 — Typkriterium und
Bibliothekslage zogen bisher gegeneinander und tun es nicht mehr. D380 Beschluss 2 wird
dadurch gegenstandslos, bevor er gewirkt hat.

Der unangenehme Teil: `ford_fulkerson` kam mit petgraph 0.6.5 am **6. Mai 2024**, lange vor
D370. Die Lage hat sich nicht geändert; der Literaturcheck hat die meistgenutzte
Graphbibliothek der Sprache nicht erfasst. Prüfregel 15 war richtig und wurde formal
befolgt — ein Check sagt über die nicht getroffenen Ergebnisse einer Suche nichts aus.

Beschluss 2: `u64` als Kapazitätstyp. Beschluss 3: die neue Ankerkopie **vor** dem Auftrag.

## Der Ablauf, und wo die Fehler diesmal sassen

Kein Werkzeuglauf; die Sitzung bestand aus Messungen, Registerarbeit und einer Websuche.
Neu und bewährt: **Splices werden vor der Lieferung im Supervisor-Klon probegefahren**,
samt `check_specs.py`. Das hat bei D381 und D382 Zeilenlängenfehler abgefangen, bevor sie
bei dir ankamen — bei D380 gab es diesen Probelauf noch nicht, und genau dort ist einer
durchgerutscht.

Die Fehler:

1. **Eine Prüfausgabe auf `tail` gekürzt, und `tail` schnitt die Befundzeile ab.**
   `check_specs.py` meldete `1 Datei(en) mit Befund`, die Zeile mit dem Befund lag darüber.
   Richtige Kürzung dort ist `grep -v "  ok  "`, nicht `tail`.
2. **`tools/check_specs.py` ohne `.venv/bin/python` aufgerufen** — die Datei ist nicht
   ausführbar, die Kette brach, Schlussmarke fehlte.
3. **Eine Registerüberschrift mit 103 Zeichen** gegen die 100er-Grenze aus D222.
4. **`08-scope.md §3` falsch verortet**: das ist das Aufnahmekriterium für Mechanismen,
   nicht der Zuschnitt des Ankersatzes. Der steht in D368 Beschluss 3.
5. **D380 rechnet HS2 zu weit zu Gute.** Dort steht, der Text lasse die Darstellung offen;
   das gilt für `§4`, nicht für `02a §2.8`, das die Formel festlegte. D381 trägt die
   Korrektur: die Lücke lag zwischen zwei Layern, nicht im Normtext.

Gemeinsamer Nenner wie in `00bt`: nicht das Messen, sondern das Übertragen und Verorten des
Gemessenen. Die Gewohnheit aus `00bt` gilt weiter — **was einmal gelesen wurde, wird beim
Zitieren erneut aufgeschlagen.** Sie hat bei D381 gegriffen und bei Punkt 4 gefehlt.

## Werkzeugnotizen

- **`cabal run -- DATEI` deutet die Datei als Skript-Target.** Es braucht den Namen der
  Executable: `cabal run mar-hs2 -- DATEI`, `cabal run trust-flow -- DATEI`.
- **HS1 liest `FALL-02` nicht unverändert**: `FileProfile` verlangt `t_exp`, das D374
  Beschluss 2 aus dem Exporter entfernt hat. `Main.hs` bindet es an `_unusedFileTExp` und
  verwertet es nicht. Die Anreicherung ist zulässig, wenn sie durch Rückrechnen auf den
  Originalhash als einzige Änderung nachgewiesen wird.
- **`git archive 00bo-hs hs | tar -x -C /tmp/…` statt Checkout** — kein Worktree-Eintrag,
  kein Aufräumbedarf, Arbeitsbaum unberührt.
- **`git --no-pager diff`** in Blöcken, sonst hängt die Ausgabe im Pager.
- **Der Spiegel trägt `00bo-hs` nicht**, nur `main`.
- **Im Supervisor-Sandbox gibt es kein `.venv`.** Dort `python3`; im Repo gilt unverändert:
  jeder Aufruf über `.venv/bin/python`.
- **Ausgabe kürzen, aber nie den Diff** — und bei Prüfwerkzeugen nicht mit `tail`.
- Splices: Anker als Nachweis der erwarteten Fassung, **alle Anker prüfen, dann alle
  Dateien schreiben**. Anhängen am Dateiende umgeht das Raten innerer Zeilenumbrüche;
  Ersetzungen in der Dateimitte brauchen `count(anker) == 1`.
- Ankerwerte in `test_anchors.py` laufen sämtlich mit `include_flagged=True`.

## Offene Punkte, nach Grösse

**O62 — die Layer-02-Zweitfassung.** Flusshälfte bestätigt (D374, unter Abzug von D373),
Zustandshälfte durch `TZ-02` vorbereitet und weiterhin **von keiner Fassung gelesen**. Der
Lauf ist durch (D380), die Sprache gewählt (D382). Offen sind die **neue Ankerkopie** und
danach der **Auftrag**.

**O61** bleibt das grösste inhaltliche, unverändert seit `00bl`.

**Ebenfalls aus D374 offen:** die Gliederung der Fragenliste nach Spec-Abschnitt.

**Daneben:** O60 (Budget-/Kantensatz-Asymmetrie). D354 mit der Gabel F2. O56 (PyPI-Name
`symbolon` belegt). O57 (Restack, Frist für Nachbesserung **3. November**).

**Nicht gemessen:** ob `02a` weitere Stellen trägt, die eine spätere Entscheidung überholt
hat. `tools/register_index.py` kennt die Verweise schon.

**Nicht gemessen:** Distanzen, Kapazitäten und Flusswerte von `TZ-02` für Z1 bis Z6.

**Nicht gemessen:** dass die beiden CBOR-Kanonisierungsregeln bei uint-Keys zusammenfallen,
ist argumentiert (D382) und nicht an Testvektoren nachgewiesen.

**Ungeklärt aus `00be`:** die Invariantentabelle `02a §7` kennt keine Zeitaussage. Ob D362
dort eine Zeile braucht, ist weiterhin nicht entschieden und weiterhin kein O-Posten.

**Ohne Frist:** die Übertragung auf unterbrochene Zustellung (LoRa/Reticulum).
Anschlusspunkte D345, D346, D350, D353, D361, D362, D363.

## Der nächste Schritt

**Die Ankerkopie für die Rust-Fassung**, nach dem Zuschnitt aus D368 Beschluss 3 und dem
Herstellungsmuster aus D371 — beides ist vor dem Anlegen im Wortlaut zu lesen. Die Kopie
trägt `01-claim-atom.md` und `02-trust-flow.md`, eingefroren auf den Commit der
Beauftragung, plus eigene `STAND.md` nach dem Muster aus D302. Zurückgehalten werden
`02-golden-anchors.md` und `02a-maxflow-prompt.md`.

**Eigenes Verzeichnis, keine geteilte Kopie** (Operatorentscheid in dieser Sitzung): die
drei Fassungen bleiben so unabhängig wie möglich. Der Preis ist eine dritte Kopie, die
still veralten kann — `hs/spec/` hat genau das vorgeführt.

**Zu bedenken, vor dem Anlegen:** die Bedingung für den `∞`-Sentinel aus D381 steht in
`02a §2.8` und damit in der **zurückgehaltenen** Datei; nur der Kasten in `02 §4` liegt im
Ankersatz. Das ist so gewollt — ob die Fassung die Schranke selbst findet, ist die Messung.
Es heisst aber, dass `FALL-02` gegen sie **nicht dasselbe misst** wie gegen HS1 und HS2,
deren Ankersatz den Kasten nicht enthielt. Wer die drei Läufe nebeneinanderstellt, muss das
mitführen.

Danach der Auftrag für die dritte Fassung.
