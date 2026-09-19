# Arbeitsweise

Diese Datei trägt die stabile Disziplin: Rollen, Arbeitsbogen, Shell, Messvorschriften,
Splices, Zitiergrammatik. Sie wird selten angefasst und muss nicht in jede Sitzung.

Sie ersetzt `pruefregeln.md` nicht. Dort stehen die Regeln 1 bis 64 im Volltext, geordnet
entlang des Arbeitsbogens. Diese Datei sagt, **wann** man dorthin greift.

Was sich je Sitzung ändert, steht in `sitzungsstart-*.md`. Was offen ist, steht in `offen.md`.

---

## 1. Rollen und Kanäle

- **Oli**: Operator. Entscheidet, führt alle Shell-Befehle aus, tippt nichts selbst in Dateien.
- **Der Supervisor** (Chatfenster): prüft gegen die Spec, rechnet Golden Numbers mit, schreibt
  Registereinträge, Prompts und Abnahmen. Schreibt **keinen** Produktivcode.
- **Das Werkzeug** (Cursor / Claude Code): führt aus. Implementierung, Tests, Refactorings,
  Messungen, Diagnoseläufe.
- **Gitea** ist die geteilte Wahrheit. Die Kanäle reden über Commits.

**Der Bericht des Werkzeugs ist nie die Abnahme** (Prüfregel 56). Geprüft wird der Diff, nicht
die Meldung darüber. Das gilt auch für den eigenen Bericht.

**Rückfragen des Werkzeugs gehen an den Supervisor**, nicht ins Implementiererfenster. Sie sind
Kandidaten für Spec-Lücken.

### Arbeitsteilung (D316 Beschluss 2)

Das Werkzeug misst, läuft, liest Diffs vor und macht mechanische Refactorings. Der Supervisor
bekommt **Zahlen und Befunde, keine Dateiinhalte**. Eine Datei wird nur gelesen, wenn eine
benannte Entscheidung von ihrem Inhalt abhängt — dann aber vollständig, und vor dem Prompt.

Das ändert die **Messung**, nicht die Abnahme. Die Abnahme bleibt beim Supervisor und bleibt am
Diff.

Der öffentliche Spiegel (`github.com/olisym/symbolon`, D317) wird direkt geklont oder
gepullt, wenn eine Entscheidung von einem Dateiinhalt abhängt — der Supervisor tut das selbst.
Vor dem Lesen steht ein Hash-Abgleich: der geklonte `HEAD` muss den gemeldeten Commit tragen,
sonst wird neu gepullt, nicht gelesen (D325). Repomix bleibt ein optionales Diagnosewerkzeug,
kein Pflichtschritt mehr.

---

## 2. Der Arbeitsbogen

1. Ziel in einem Satz. Bei Implementierung: Abnahmekriterium messbar.
2. **Modulcode vor Prompt** — alle betroffenen Quellen lesen, bevor ein Prompt entsteht.
3. Forks benennen, Position beziehen, Golden Numbers rechnen. Registereintrag **vor** dem Prompt.
4. Prompt schreiben, Lauf abwarten, Diff lesen, Abnahme.
5. Merge. Defekte werden vor dem Merge auf demselben Branch behoben.

**Der Vergleichspunkt eines Laufs ist der Prompt-Commit**, nicht der Branchpunkt der Spec-Reihe.

`python3 tools/register_index.py "04 §4.1"` nennt die Registereinträge, die einen Abschnitt
entschieden haben. Das ist Prüfregel 38 in ausführbarer Form und der billigste erste Griff,
bevor eine Position bezogen wird.

### Prompt-Regeln

Jeder Prompt enthält: Branch und Basis-Commit, normative Grundlage, den Auftrag, **ausdrückliche
Nicht-Ziele**, abgeleitete Abnahmekriterien, den Abschluss (ein Commit, kein Merge).

- Kein stiller Scope-Zuwachs. Was nicht im Prompt steht, wird gemeldet, nicht gebaut.
- **Golden Numbers gehören nicht in den Prompt**, sondern in die Abnahme.
- Erwartete Werte werden **abgeleitet**, nicht getippt. Eine getippte Menge veraltet still.
- Eine **Rücknahmeprobe** dort, wo ein Regressionstest entsteht. Ein Regressionstest, der die
  Regression nicht sieht, ist keiner.
- Widerspricht eine Messung dem Prompt: **melden, nicht anpassen.**
- Der Abschluss verlangt den **vollständigen** `git diff` gegen den Branchpunkt.

---

## 3. Der Prototypmodus (D311 Beschluss 1)

Szenarioskripte sind **Wegwerfcode**. Für sie gelten **nicht**: Registerpflicht für den Code,
Golden Numbers, Rücknahmeproben, Zweitimplementierung, Abnahme gegen erwartete Zahlen.

Es gelten **weiter**: die Spec als normative Wahrheit, das Register als oberste Instanz, die
Zitiergrammatik, und dass eine Messung eine Position ändern können muss.

Ins Register wandert aus einem Prototyplauf ausschliesslich der **Befund**: die Stelle, an der die
Spec keine Antwort hatte, eine falsche gab, oder eine erzwang, die ein Zentrum voraussetzt.

Die Abnahme prüft im Prototypmodus **nicht den Code gegen den Bericht**, sondern die **Befunde
gegen die Spec**.

Der Rahmen ist `tools/sim/`: getrennte Beobachter, getrennte Uhren und Schlüssel, ein Verzeichnis
je Teilnehmer mit Inbox, deklarative Szenarien in JSON mit den Schritten `claim`, `zustellen`,
`uhr`, `zeige` und `erwarte`. **Jeder weitere Szenariolauf setzt darauf auf** (Prüfregel 63).

---

## 4. Risiko-Tiers

**Tier 1 — irreversibel oder Historie berührend. Ein Befehl, Erwartung vorher fixieren.**
`git push`, force-push, Merge nach `main`, Branch- oder Dateilöschung, `git add -A`,
vollständige Ersetzung einer Spec-Datei ohne Hash-Abgleich.

**Tier 2 — reversibel, lokal. Bündeln.** Commits auf einem Lauf-Branch, Schreiben im
Arbeitsverzeichnis. Git ist der Rollback.

**Tier 3 — read-only. Immer bündeln, keine Zeremonie.** `git log`, `git show`, `grep`, `sed -n`,
`sha256sum`, Diagnoseläufe.

Im Zweifel eine Stufe tiefer. Eskalation braucht konkreten Grund.

---

## 5. Shell

Fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`. Kein Heredoc.

- **Nie `and` innerhalb einer Pipe.** `sha256sum -c` am Pipe-Ende und eine Pipe auf `tail`, `cat`,
  `tee` oder `grep -q` sind die nützlichen Ausnahmen.
- **Sichtbar und geprüft zugleich geht über `tee`.** `make check 2>&1 | tee /tmp/x.txt | tail -6`,
  danach `grep -q '^789 passed' /tmp/x.txt`.
- **Jeder Block trägt Marken.** Vor jedem Abschnitt ein `echo "== NAME =="`, am Ende ein
  `echo "== FERTIG =="`. Fehlt die Schlussmarke, ist die Kette abgebrochen — unabhängig davon,
  ob die letzte sichtbare Zeile erfolgreich aussieht. Jede Prüfgruppe trägt eine eigene Marke:
  `HASH` vor den Lieferungen, `BASIS` vor Branch, Commit und Zieldateien. Die Marken stehen mit
  `and` in der Kette, damit sie mit ihr abbrechen; ein `echo` scheitert nicht von selbst (D418).
- **Keine Ausgabe heisst: der Block ist nicht gelaufen.**
- **Lieferungen über `/tmp`.** Oli legt gelieferte Dateien in `/tmp` ab. Der Lieferblock prüft
  zuerst den Hash jeder Lieferung und den Basisstand der Zieldatei, erst dann wird ersetzt.
  Letzter Job vor `== FERTIG ==` ist `rm` der gelieferten Dateien, in der `and`-Kette: bricht der
  Block ab, bleiben sie für den zweiten Anlauf liegen. Eine liegengebliebene Altversion lässt den
  Browser die neue als `name (1).md` ablegen (D414).
- **`git --no-pager`** vor `diff`, `log` und `show`, sonst wartet `less` auf eine Taste.
- **Abbruch einplanen.** Prüfungen stehen vor jeder Änderung (Hash, Branch, Basis-Commit,
  Basis-Hash der Zieldatei), damit eine gescheiterte Prüfung nichts halb Geändertes hinterlässt.
  `git push` und der Merge nach `main` stehen als eigener Befehl ausserhalb des Blocks.
- **Nur ausgeben, was die Rückantwort braucht.** Erfolgreiche Zwischenschritte schweigen,
  Zählungen und Prüfsummen erscheinen als eine Zeile. `git diff` für die Abnahme bleibt
  vollständig.
- **`string`-Kommandos in einer `and`-Kette sind eine Falle.** `string trim`, `string match` und
  `string replace` liefern Status 1, wenn sie nichts zu tun hatten. Kommandosubstitution entfernt
  Whitespace bereits selbst.
- **`set -l` und verschachtelte Kommandosubstitution gehören nicht in einen Copy-Block.**
- **Glob-Argumente quoten.** Ein Glob ohne Treffer bricht die Kette, auch vor einem `rm -f`. Zum
  Aufräumen `find /tmp -maxdepth 1 -name 'splice-*.py' -delete`.
- **`grep` ohne `-E` kennt kein `|` als Alternative.** **`grep -c` liefert bei null Treffern
  Status 1**; eine Zählzeile, die null ergeben *darf*, geht auf `| cat`.
- **`diff a b > datei` bricht die Kette**, weil `diff` bei Unterschieden Status 1 liefert.
- **Kommandosubstitution in doppelten Anführungszeichen wird in fish nicht ausgeführt.** Der Weg,
  der trägt: die Zahlen mit `printf` und Kommandosubstitution **außerhalb** von
  Anführungszeichen in eine Datei schreiben, dann `--header-text "$(cat /tmp/stand.txt)"`.
- **Ein Fragment aus einem Antwortabsatz gehört nicht in den Block.** Der Block wird vor dem
  Absenden von hinten gelesen.
- **Eine lange Ausgabe passt nicht in jedes Konsolenfenster.** Diagnoseskripte **aggregieren** und
  schreiben die volle Liste in eine Datei; ein `| cut -c1-150` verhindert den Umbruch.
- **`go` liegt nicht im `PATH`.** Die Toolchain steht unter `~/sdk/go/bin/go`.
- **Die Werkzeuge unter `tools/` laufen nur als Modul.** `python -m tools.gitter`.
- **`.venv/bin/python -m pytest -q`, nie bares `pytest`.** `/usr/bin/python` trägt kein
  pytest; die Zeile `python -m pytest` scheitert mit `No module named pytest`. `make check`
  und `make check-all` wählen den Interpreter selbst.
- **Im Merge-Block steht `git push` vor `git branch -d`** (Prüfregel 58).
- **`git add` mit expliziten Pfaden, nie `-A`.** Neue Dateien vor `make check` adden, sonst danach.
- **Neue Dateien kommen nach dem Splice, nicht davor.** `splice_run.py` verlangt einen sauberen
  Arbeitsbaum und scheitert schon an einer unverfolgten Datei.
- **Hash-Test als erster Job** bei jeder gelieferten Datei. Bei Ersetzungen zusätzlich
  `git diff --quiet`. Mehrere Hashes prüft ein `printf` mit wiederholtem Format, Ausgabe in
  `sha256sum -c`.
- **Spec-Dateien, Prompts und Skripte als Download**, nicht als Copy-Block. **Eine Datei, die
  erzeugt und nicht ausgeliefert wurde, existiert für Oli nicht.**

---

## 6. Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt. Eine **Ersetzung** ist eine Löschung
  plus eine Einfügung; nach Prüfregel 48 werden die randgleichen Zeilen abgezogen.
- **`grep -c '^+'` auf einen unified diff zählt die `+++`-Kopfzeile mit.**
- **Ein eigener Print-Separator ist keine Messung.**
- **Aus einer Zeilennummer folgt kein Abschnitt.**
- **Zwei Messungen desselben Gegenstands gehören gegeneinander gehalten**, bevor die zweite eine
  Entscheidung trägt.
- **Zählungen werden gegrept, nicht geschätzt.**

### Zählvorschriften

- Registerköpfe: `grep -c '^### D' 07-decisions.md`
- Prüfregeln: `grep -cE '^\*\*[0-9]+\.' pruefregeln.md`
- Offene Posten: `grep -c '^### O' offen.md`
- Branches: `git branch -a | wc -l` — die Zahl schliesst `origin/main` und `origin/HEAD` ein, drei
  heisst also ein lokaler Branch.
- Vor der Testzahl `.hypothesis` und `__pycache__` löschen (Prüfregel 19).

### Die Projektkopie

Optional seit D325, gezogen nur für eine Diagnose (D420). Der Kopf trägt die Kaltzahlen aus
D318 im `--header-text`. **Das `-o` gehört dazu**, sonst landet `repomix-output.xml` im
Arbeitsbaum. Ob der Header in der Datei steht, sagt erst ein `grep` auf `user_provided_header`.

Aus `/tmp/mar-context.xml` lässt sich der ganze Baum rekonstruieren — geschnitten am `file`-Tag,
die Newline hinter dem öffnenden und vor dem schliessenden Tag gehören nicht zum Inhalt. **Das
Auspackskript hängt jeder Datei eine Schluss-Newline an.** Jede Zeilenangabe aus der Kopie ist um
eins verschoben (Prüfregel 46).

**Der Blob-Hash aus dem Diff ist der Anker der Rekonstruktion.** `git hash-object` auf die
nachgebaute Datei gegen die `index`-Zeile des Diffs.

### Wann welche Regel greift

**27** vor jedem Verweis, **33** für den Satz daneben, **38** vor der Position, **40** vor jeder
Erwartung an einen Kopfstand, **41** vor jeder Bewertung einer Abweichung gegen den Prompt, **43**
vor jeder Zahl aus der Kopie, **44** vor jeder abgeleiteten Anzahl, **46** vor jeder Zeilenangabe,
**49** vor jeder Rücknahmeprobe, **51** vor jedem Prüfer, der eine Menge misst, **59** vor jeder
rekonstruierten Fassung, **60** vor jeder Meldung über eine Probe, **61** vor jeder Bewertung
einer Abweichung zwischen zwei Fassungen, **62** vor jeder Probe, die eine Menge verkleinert,
**63** vor jedem Prompt, der etwas bauen lässt, **64** vor jeder Regel, die eine Menge ausdünnt.

---

## 7. Splices

Ein Splice ist ein Skript mit `assert`, dass der Anker genau einmal vorkommt. Gefahren mit
`.venv/bin/python tools/splice_run.py /tmp/splice-*.py` (D225). **Die Meldung `AssertionError`
gefolgt von `zweiter Lauf gescheitert` ist die Erfolgsmeldung.**

- **Das Skript liegt in `/tmp`.** `ROOT = Path.cwd()`, nicht `Path(__file__).parent`.
- **Das Skript wird erzeugt, nicht getippt.** Der Anker wird aus der Zieldatei **gelesen**.
- **Ein Skript mit mehreren Paaren rechnet erst alles und schreibt dann.**
- **Der Assert prüft das Ergebnis, nicht den eingesetzten Text** (Prüfregel 42). Der belastbare
  Assert misst jede Zeile der neuen Fassung, die in der alten nicht vorkommt.
- **Das Anhängen an das Dateiende wird über `rstrip` normalisiert** und ist damit unabhängig
  davon, wie die Zieldatei endet; deshalb lässt sich der Zielhash vorher rechnen.
- **Ein Zielhash-Assert vor dem Schreiben ersetzt den Quellhash.** Weicht die Datei ab, schreibt
  das Skript nicht.
- **`alt.count("### D")` ist nicht die Zählvorschrift.** Zeilenweise mit `startswith`.
- **Ein Nachtrag an einen bestehenden Eintrag erhöht die Registerzahl nicht.**
- **Dreifache Anführungszeichen im Einschubtext beenden den Python-String.**
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

---

## 8. Zitiergrammatik und Bindung

Seit D232 gibt es keinen offenen Teil. Vier Teile: der Dateiname mit oder ohne `.md`; die Kurzform
`NN`/`NNx` über `LAYER_FILES`; die Bereichsform `NAME §A–§B` (D228, kein Leerraum um den Strich);
die Anhangsnummer als Großbuchstabe mit Punkt vor der Ziffernfolge (D230). Dazu die
Backtick-Toleranz (D231). Alles andere in `.py` ist ein Befund (D227); in `.md` bleibt der bare
Verweis zulässig.

**Ein Verweis auf einen Abschnitt derselben Datei braucht die Dateinamensform** (D301).

**Prüfregel 47:** ein Verweis und ein Inline-Code-Span werden nicht über die Zeilengrenze
getrennt.

**Die Grenze, die bleibt:** die Prüfung sichert, dass das Ziel **existiert**, nicht dass es
**stimmt** (D229, D233). Daraus folgt D250: ein Anhang wird **angehängt, nicht eingeschoben**.

### Bindung (D314)

Eine Wurzeldatei ist gebunden, wenn sie in `LAYER_FILES` oder `ALWAYS_BOUND` steht, oder wenn eine
Python-Datei oder eine **andere gebundene** Wurzeldatei sie als `NAME §X` nennt. Eine blosse
namentliche Nennung bindet nicht. `check_specs` meldet die Zahlen am Ende und **schlägt dabei
nicht fehl**.

**Verweise mit Paragraphen auf archivierte Dateien sind ein Befund** — der Zitiername ist
unbekannt, sobald die Datei die Wurzel verlässt. Wer eine Archivdatei erwähnt, nennt sie ohne
Abschnitt.

### Form

- **Prosa bricht bei 100 Zeichen; Tabellenzeilen und Codeblöcke sind ausgenommen** (D222). Für
  Python gibt es **keine** Zeilenlängenregel (D205). **Zeichen zählen, nicht Bytes** — `awk
  length` zählt Bytes.
- Keine Escapes in Spec-Dateien; Bytes als `h'ff'`. Gilt auch für Prompt-Dateien im
  Wurzelverzeichnis — `check_specs.py` prüft sie mit.
- **Eine Regex, die in einen Prompt oder eine Spec-Datei soll, geht nicht.** Regexänderungen
  werden in Prosa beauftragt.

---

## 9. Abhängigkeiten

Minimal: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis`, `ruff`. Kein `float`,
kein `fractions` im Produktivcode. `now` ist immer Parameter.
---

## 10. Die Übergabe

Jede Sitzung endet mit einer Übergabedatei und beginnt mit ihr (D320).

### Die Datei

`sitzungsstart-NNNN.md` im Wurzelverzeichnis. Sie heisst nach der Sitzung, die sie **schreibt**,
nicht nach der, die sie startet. Die Suffixe laufen `00a` bis `00z`, dann `00aa` fort; die
jüngste ist die mit dem längeren Namensteil, bei gleicher Länge die alphabetisch spätere.

Sie trägt den Stand **vor** ihrer eigenen Übergabe. Der Commit, mit dem sie eingecheckt wird,
steht nicht mehr darin. Wer den Kopf abschreibt statt ihn zu messen, liegt um einen Commit
daneben.

Inhalt: Rolle in zwei Sätzen, der Stand mit den sechs Kaltzahlen, die Schichten, der Bestand,
was zuletzt entschieden wurde, der nächste Schritt. Zielgrösse unter siebzig Zeilen. Alles
Weitere steht in `arbeitsweise.md`, `offen.md` und `pruefregeln.md`.

### Am Sitzungsende

Der Supervisor schreibt die Datei und liefert sie als Download. Sie kommt in die Wurzel und wird
committet; der Commit trägt den Präfix der schreibenden Sitzung. Im selben Commit wandert eine
ältere Übergabedatei nach `archiv/`.

### Am Sitzungsanfang

In den Kontext gehen **zwei** Dinge: die dauerhafte Anweisung und die jüngste Übergabedatei.
Sonst nichts. Die anderen Dateien liegen im Repositorium und werden geholt, wenn eine
Entscheidung an ihnen hängt.

Der erste Zug ist die Kaltmessung. Die Übergabedatei ist eine Hypothese; ihre Zahlen werden
gemessen, nicht geglaubt (Prüfregel 40).

### Das Archiv

Gebunden wird nur die jüngste Übergabedatei. Jede ältere erscheint in der Bindungsmeldung von
`check_specs.py` als ungebunden — das ist kein Mangel, sondern der Auftrag, sie wegzuräumen.
Eine archivierte Datei wird ohne Abschnitt zitiert; der Zitiername ist unbekannt, sobald sie die
Wurzel verlässt (D314).

### Die Grenze

Es gibt kein Verfahren, das erzwingt, dass die Datei geschrieben wird. Fällt sie aus, startet
die nächste Sitzung blind. Mechanisch schliessen lässt sich das nicht, weil eine Sitzung im
Repositorium kein Gegenstand ist.

---

## 11. Die Fragenlisten

Jede Zweitfassung führt eine Fragenliste: jede Stelle, an der der Text mehrdeutig, unvollständig
oder widersprüchlich war, mit der gewählten und der verworfenen Lesart. Sie ist das Ergebnis der
Fassung, nicht ihr Nebenprodukt. Drei liegen vor — `go/FRAGEN.md` zu Layer 01, `hs/FRAGEN-1.md`
und `hs/FRAGEN-2.md` zu Layer 02 —, die Rust-Liste folgt.

Die Listen bleiben unverändert, wie sie geschrieben wurden (D384 Beschluss 1). Die Ordnung
entsteht daneben: `fragen-adressen §1` ordnet jedem Eintrag seine Stelle zu, und daraus wird
`fragen-index §1` erzeugt, sortiert nach Adresse, mit einer Spalte je Fassung (D385, D386).

Neue Fragenlisten tragen die Adresse als Pflichtfeld je Eintrag; für sie entfällt die Zuordnung.
