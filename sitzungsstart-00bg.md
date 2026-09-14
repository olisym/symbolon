# Sitzungsstart: 00bg (MaR / symbolon), fortgeschrieben nach D365

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

Am Ende von `00bf`: **817 Tests**, Register **D1–D365**, Prüfregeln **1–74**, 61 Posten,
`make check` grün, `main` und `origin/main` gleichauf bei `56e5559`. **30 Wurzel-Markdown-
Dateien, alle gebunden**; `archiv/` stand bei 127, und mit diesem Sitzungsstart fällt
`sitzungsstart-00bf.md` dazu. Ein Branch.

`00bf` war eine Literatur- und Messrunde mit vier Registerköpfen: D363 (Befund zu O61), D364
(`t_exp`-lose Bürgschaften im Budget-Set) samt einer Korrektur an der eigenen Tabelle, D365
(Rücknahmeprobe je Mechanik) und Prüfregel 74. Dazu ein Prüffall. `symbolon/` ist unangetastet.

### Die Schichten

Unverändert seit `00ar` — siehe `arbeitsweise.md`, `pruefregeln.md`, `08-scope.md §3`.

### Der Bestand

Neu: `tests/trust/test_texp_los.py` (148 Zeilen, drei Prüffälle). Geändert: `07-decisions.md`,
`offen.md`, `pruefregeln.md`. Die Rücknahmeproben liefen und wurden zurückgenommen; nichts
davon ist im Baum.

**Ausserhalb des Repositoriums, bei Oli lokal:** `restack-faktensammlung.md`,
`restack-felder-englisch.md`, `prompt-log.py` und `prompt-log-restack.md` in `~/Downloads`.
Bewusst nicht im Baum. Wenn der Antrag vor dem 3. November nachgebessert wird, sind das die
Dateien dafür.

## Was in `00bf` entschieden wurde (D363–D365)

**D363 — Literaturbefund zu O61.** Statt O61 auf der billigeren Antwort zu schliessen, wurde
die Lücke aus D361 nachgelesen: die BRSKI-Entwürfe, die dort als ungelesene Vorarbeit stehen.
Drei Korrekturen an D361 folgen. Erstens die Fassung: D361 nennt keine Entwurfsnummer, und aus
dem Inhalt folgt Raytime -00 oder -01 — die Fassung -02 füllt die leeren Security
Considerations, ergänzt die Grenzen der Nutzung alter Token und den Vergleich zur Vorarbeit.
Zweitens ist BRSKI keine Vorarbeit, sondern eine **verworfene** Konstruktion: das „current
reasonable date" fehlt in RFC 8995 und schon in Entwurf -45, ersetzt durch eine binäre Regel
plus Nonce. Drittens ist Raytimes Zeitquelle **zentral** — der Authorization Server, und
verteilte Zeitquellen sind ausdrücklich nicht einschlägig.

Damit fallen zwei der drei Wege aus O61. Hinzu kommt ein vierter, den die Liste nicht kannte:
die untere Zeitschranke aus dem `t` empfangener signierter Claims nachziehen. Seine Hauptfrage
ist offen, denn D353 bindet nur **intra-Autor** und belastet die rückwärts laufende Uhr; ein
konsistent **vorlaufender** Autor kollidiert mit nichts und stellt trotzdem bei jedem Empfänger
die Schranke vor. D78 hat verwandte Wirkung zwischen Autoren bereits verworfen.

**D364 — ein Vouch ohne `t_exp` verlässt das Budget-Set nie.** Gemessen, nicht vermutet. Weg 3
aus O61 ist nicht zu bauen, er ist gebaut: `_in_budget_set` gibt bei fehlendem `t_exp`
unbedingt `True` zurück und fasst `now` nicht an, `build_groups` überspringt den Claim nicht,
und `test_vouch_without_texp.py` belegt, dass Gruppen und Kapazitäten mit und ohne `t_exp`
gleich sind. Inert ist der Vermerk, nicht die Bürgschaft.

Der schärfste Teil: **auch der Widerruf befreit nicht.** `REVOKED` steht nach D135 im
Budget-Set, und ohne `t_exp` gibt es keinen Ablauf — ein Autor, der sich mit `t_exp`-losen
Bürgschaften überbindet, bleibt dauerhaft `OVERCOMMITTED_AUTHOR`, alle seine Kanten fallen,
und nichts löst das je auf. In der Gegenprobe mit `t_exp` befreit ihn ebenfalls nicht der
Widerruf, sondern der Ablauf. Das ist D362s Mechanik ohne deren Selbstheilung.

Kein Defekt: D135, D119 und `02a §2.6` erzeugen es gemeinsam, keine ist für sich falsch.
Verworfen und benannt: `REVOKED` aus `BUDGET_STATES` nehmen (die Prämie auf den
Lebenszyklus-Akt, die D135 ausschliesst); die Pflicht aus `02 §6.2` zum Reject härten (die
Entscheidung, die D119 anders getroffen hat); als Defekt behandeln.

**D365 und Prüfregel 74 — eine Mutation je Mechanik.** Der Prüffall zu D364 trägt zwei
Mechaniken, der Prompt verlangte eine Mutation. Unter der `t_exp`-Mutation blieb der Fall zum
Widerruf grün und sah robust aus: er vergleicht zwei Läufe, die symmetrisch mitwandern. Erst
die zweite Mutation an `BUDGET_STATES` liess ihn fallen. Ein Test, der nichts sehen kann, ist
von einem, der nichts zu sehen findet, an der Farbe nicht zu unterscheiden.

## Der Ablauf, und wo die Fehler diesmal sassen

Das Werkzeug hat wieder sauber geliefert: Auftrag eingehalten, Werte abgeleitet, die
Rücknahmeprobe korrekt gefahren und **einschliesslich des grün gebliebenen Falls** berichtet.
Alle drei Defekte der Runde stammen aus dem Supervisor-Text.

1. D363 schlug im Schlussabsatz einen Prüffall mit zwei Beobachtern vor. `derive()` ist eine
   reine Funktion — der Fall misst nichts, was `test_zeitmonotonie.py` nicht schon misst.
   Zurückgenommen in D364.
2. D364s Tabelle war gegen den Messcode falsch beschriftet, und der Schlussabsatz verwies auf
   die falschen Zeilen. Korrigiert in derselben Sitzung.
3. Im Prompt fehlte die zweite Mutation. Daraus D365 und Regel 74.

Der gemeinsame Nenner: alle drei stehen im **erzählenden** Teil, der nach der Messung
geschrieben wird. Die Messungen selbst waren jedes Mal richtig. Kein Linter und kein Test sieht
diese Klasse — dieselbe Bauform wie der Fehlverweis `01 §5.3` und die falsche Prompt-Begründung
aus `00be`. Regel 74 deckt davon nur den Prompt-Teil ab.

## Werkzeugnotizen

- **`git --no-pager` gehört vor das Subkommando**, nicht ans Ende. Seit dem 10. September gilt
  für alle Ausgaben in Blöcken `git --no-pager diff` / `log` / `show`, damit die Kette ohne
  Tastendruck durchläuft. `git diff --nopager` kennt git nicht und würde in einer `and`-Kette
  alles Folgende abwürgen. Die Regel lebte bis `00bf` nur im Verlauf und fiel prompt heraus.
- **Der repomix-Nachzug ist gestrichen, nicht überfällig.** Seit dem Spiegel-Zugriff ist er
  kein Pflichtschritt mehr (Token-Ökonomie 2 der Dauer-Anweisung); die Werkzeugnotiz in `00bf`
  hat ihn trotzdem zwei Runden als offenen Posten mitgeschleppt. Repomix bleibt ein optionales
  Werkzeug für Token-Diagnosen. Der Absatz unter „Shell-Disziplin" in der Dauer-Anweisung
  widerspricht dem noch und kann nur von Oli geändert werden.
- **Ein wiederverwendetes `Identity`-Objekt über zwei Stores hinweg erzeugt `PENDING`.** Die
  Kette läuft im Objekt weiter; landen die späteren Claims in einem Store ohne ihre Vorgänger,
  stehen sie auf `PENDING` — **im Budget-Set, aber ohne Kante**. Das ergibt stillschweigend
  0 statt des erwarteten Werts und sieht aus wie ein Befund. In `00bf` ist genau das passiert
  und wurde erst beim Nachprüfen der eigenen Konstruktion sichtbar. Frische Identitäten je
  Szenario. Gleicher Name in zwei getrennten Stores ist unkritisch; im selben Store gibt er
  `EQUIVOCATION_FLAGGED`.
- **`stand.py` braucht einen Pfad** auf eine Datei mit der pytest-Ausgabe und gibt ohne
  Argument stumm 1 zurück. Aufruf: `make check > /tmp/check.txt 2>&1`, dann
  `python tools/stand.py /tmp/check.txt`. **Keine Pipe dahinter** — `tail` schluckt den roten
  Status. `stand.py` meldet den Hash des letzten **Commits**, nicht den Zustand danach, und
  zählt Zeilen von `git branch -a`: drei Zeilen heisst ein Branch.
- **`splice_run.py` verlangt einen sauberen Baum.** Wird ein Defekt im Diff gefunden, ist der
  Weg `git checkout --` auf die betroffenen Dateien und ein korrigierter Splice, nicht ein
  zweiter obendrauf. In `00bf` zweimal so gelaufen, beide Male richtig.
- **Im Supervisor-Sandbox fehlen die Abhängigkeiten.** Vor dem ersten Diagnoselauf
  `pip install pytest cbor2 cryptography --break-system-packages`. Ohne sie scheitert schon das
  Einsammeln der Tests an `symbolon/cbor_canon.py`.

## Offene Punkte, nach Grösse

**Das grösste bleibt O61** — soll ein uhrloser Knoten Vertrauen gewähren können? Nach D363 und
D364 steht die Frage anders als in `offen.md` ursprünglich notiert: die signierte
Zeit-Attestierung löst sie nicht, Raytime setzt eine Autorität voraus, die es nach D350 nicht
geben soll, Weg 3 ist bereits gebaut und braucht Einhegung statt Bau, und der vierte Weg hat
eine offene Hauptfrage gegen D78. Prüfregel 72 ist für O61 bezahlt; wer ihn eröffnen will,
braucht nach Regel 73 zusätzlich die BRSKI-Fassungsfrage und die Persistenzfrage.

**Daneben:** O60, die Budget-/Kantensatz-Asymmetrie. D354 mit der Gabel F2. O56 (PyPI-Name
`symbolon` belegt). O57 (Restack, eingereicht am 10. September, Frist für Nachbesserung
3. November).

**Ohne Frist:** die Übertragung auf unterbrochene Zustellung (LoRa/Reticulum). Anschlusspunkte
D345, D346, D350, D353, D361, D362, jetzt D363.

**Ungeklärt aus `00be`:** die Invariantentabelle `02a §7` kennt keine Zeitaussage. Ob D362 dort
eine Zeile braucht — und ob sie die Nicht-Monotonie festschreibt oder nur die Richtung, in der
sie auftreten darf —, ist nicht entschieden. Mit D364 ist zusätzliches Material da, aber es ist
weiterhin kein O-Posten.

## Der nächste Schritt

**Die Einhegung aus `02 §6.2`.** Sie ist der einzige offene Punkt, an dessen Ende etwas im Code
steht statt nur im Register, und das ist nach vier Runden ohne Bewegung im Bestand das
Ausschlaggebende. Die Lage ist ungewöhnlich günstig: der Schaden ist in D364 beziffert, und die
Norm sieht die Abhilfe bereits vor — `02 §6.2` verlangt in Scopes mit Budgetregel `t_exp`
**oder** eine Policy-Maximallaufzeit als Default. D119 hält fest, dass das Verfassungsschema
kein Feld dafür hat. Das ist die Lücke.

Zwei Befunde aus der Vorprüfung liegen schon vor:

- `VOUCH_WITHOUT_TEXP` fällt ausschliesslich in `symbolon/trust/groups.py`, also **beim
  Auswertenden**. Der Autor, der sich gerade unwiderruflich bindet, sieht nichts. Kein Reject,
  keine Warnung auf der Schreibseite.
- `02 §6.2` formuliert die Maximallaufzeit als gleichrangige Alternative zum MUSS, nicht als
  Ausnahme. Der Weg ist normativ offen.

Vor einem Vorschlag zu klären: ob das Verfassungsschema ein Feld aufnehmen kann, ohne `§8` und
den schweigenden Nukleus zu berühren. Das ernsthafte Gegenargument gegen die ganze Runde steht
in D364 selbst — es ist kein Defekt, und die Lähmung ist die Folge eines Normverstosses; Folgen
von Normverstössen muss man nicht abfedern. Was dagegen spricht, ist die Unwiderruflichkeit
ohne jede Warnung auf der Seite dessen, den es trifft.

Zwei kleinere Züge, falls eine kurze Runde vorgezogen werden soll: die INV-3-Frage oben, und
die Abgrenzung des vierten Wegs gegen D78 — letztere allerdings Fork-Arbeit ohne messbares
Zwischenergebnis, also der Typ, der in `00bd` und `00bf` die Fehler produziert hat.
