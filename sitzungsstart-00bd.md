# Sitzungsstart: 00bd (MaR / symbolon), fortgeschrieben nach D353–D359

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
`HEAD` prüfen. Feature-Branches gehen nicht über den Spiegel; bei einer Abnahme auf einem
Branch braucht der Supervisor den vollständigen `git diff`, nicht die Meldung darüber.

## Stand

Am Ende von `00bc`: **811 Tests**, Register **D1–D359**, Prüfregeln **1–71**, `make check`
grün, `main` und `origin/main` gleichauf bei `3bed445`. 45 Wurzel-Markdown-Dateien, davon
30 gebunden und 15 ungebunden; mit diesem Sitzungsstart fällt `sitzungsstart-00bb.md`
dazu. Vier Branches.

`00bc` war die erste reine Spec-Runde seit längerem und hat sich zu einer vollen Kette
ausgewachsen: Fork-Analyse, sieben Registereinträge, normativer Text in vier Spec-Dateien,
ein Implementierungslauf mit Nachbesserung, ein neuer Vektor und drei Prüfregeln.

### Die Schichten

Unverändert seit `00ar` — siehe `arbeitsweise.md`, `pruefregeln.md`, `08-scope.md §3`.

### Der Bestand

Neu: Zustand `TIME_REGRESSION_FLAGGED` in `verifier.py` und `index.py`, Vermerk
`OBLIGATION_TIME_REGRESSION` in `profiles/`, Vektor **NV32** (Anhang C.16),
`tests/test_time_regression.py`. `tools/sim/scenarios/s2.json` und `s3.json` sind umgetaktet.

**Ausserhalb des Repositoriums, bei Oli lokal:** `restack-faktensammlung.md`,
`restack-felder-englisch.md`, `prompt-log.py` und `prompt-log-restack.md` in `~/Downloads`.
Bewusst nicht im Baum. Wenn der Antrag vor dem 3. November nachgebessert wird, sind das die
Dateien dafür.

## Was in `00bc` entschieden wurde (D353–D359)

Ausgangspunkt war die zweite Frage aus D350: kann `t` zur kollidierbaren Zeitaussage werden?

**D353 (`t` ist monoton entlang der Autorenkette).** Befund vorweg: `t` war nicht unbenutzt,
sondern **unverknüpft** — genau eine Auswertung, `01 §6` Punkt 7, claim-intern gegen `t_exp`.
Beschlossen: `C.t >= pred(C).t` bei lokal bekanntem Vorgänger, **kein Reject**, sondern der
Zustand `time-regression-flagged` nach dem Vorbild von `equivocation-flagged`, in
`BUDGET_STATES`. Die Regel stiftet keine Ordnung aus `t` — die Ordnung kommt weiter aus
`h_prev`, `t` wird gegen sie geprüft. Abgegrenzt gegen D78 (dort verworfen als Rangfolge
**zwischen** Autoren) und gegen das in D123 verworfene Widerspruchsfenster. `>=` statt `>`,
weil `t` sekundenaufgelöst ist. Golden Numbers: Alices Kette war bereits streng monoton
(+100/+100/+100/+110), Kosten am Vektorsatz null.

**D354 (der Fork, der noch offen ist).** Die Ablaufbewertung eines Beobachters ist
indexikalisch — „meine Uhr stand über X" ist wahr nur relativ zu einem Moment, und der
einzige Index dafür wäre eine Uhr. Zirkel. Ausweg: der abhängige Claim **nennt seine
Prämisse**, dann ist `B.t > V.t_exp` ein Widerspruch zwischen zwei signierten Zahlen — ohne
`now`, ohne Zeitquelle, auf einem Gerät ohne Uhr in einer Partition nachrechenbar. Verortet
in `02a`/`03` über `v` Key 1; `02a` T-02.7 hält Zusatz-Keys in `v` ausdrücklich für zulässig,
also kein Feldsatz, keine Protokollversion. **D353 vor D354 ist normativ**: ohne Monotonie
ist D354 durch Rückdatierung erledigt. Nachtrag zu D350: `VISION.md §5` nennt den Zeitdienst
bereits als Profil mit signierter Zeit-Attestierung und „kein neues Primitiv" — D350 schliesst
keine signierte Zeitaussage aus, nur Primitiv und Autorität.

**D355 (Intervall-`now` zurückgestellt).** Es erzeugt Enthaltung statt Kollision, also die
Gegenrichtung zu `08 §2.2`. Der Fund darunter ist wertvoller und wird als **O60** geführt:
mit unscharfer Zeit zerfällt `_in_budget_set` in zwei entgegengesetzte konservative
Richtungen — Kantensatz „als abgelaufen behandeln", Budget-Set „als nicht abgelaufen
behandeln". Punkt-`now` lässt beide zusammenfallen und verdeckt die Frage. Nebenbefund:
`trust/derive.py:39` und `flow.py:30` nehmen `now: int`, nicht `int | None` — Trust ist
uhr-**pflichtig** auf Typebene.

**D356 (abhängige Schichten).** Drei Stellen, drei Antworten: `02a §2.6` nimmt den Zustand in
die Aufzählung (D135-Begründung: der Über-Commitment-Beweis beruht auf Signaturen, nicht auf
Aktivität); `02-trust-flow.md` bleibt **bewusst unverändert**, weil die Zugehörigkeit dort als
Prädikat formuliert ist und deshalb D135 überstanden hat; `03 §3.3.2` bekommt `INDETERMINATE`
mit eigenem Vermerk. `credit.py` war die einzige erschöpfende Zustandsverteilung im Baum.

**D357 (`t` in den Szenarien war Dekoration).** Der Lauf machte `s2` und `s3` rot. Genau drei
Stellen, alle dieselbe: Annas `vote` mit `t = 1` nach ihrem `propose` mit `t = 2`. Die Welt
wird umgetaktet, die `erwarte`-Blöcke nicht — danach grün, ohne dass eine Erwartung bewegt
wurde. Der Befund darüber: ein Feld ohne Wirkung wird beliebig gefüllt, und die beliebige
Füllung wird erst sichtbar, wenn das Feld zu tragen beginnt.

**D358 (Vektor-Verankerung).** NV32 hing nach Prompt-Vorgabe an TV1 und war damit
Equivocation-Geschwister von TV2 — im vollständigen Speicher `equivocation-flagged` statt
`time-regression-flagged`, und TV2 kippte aus `active` heraus. Normativ für Anhang C: ein
Vektor muss den Zustand, den er belegt, im **vollständigen** Speicher annehmen; Andockpunkt
ist ein kinderloses Kettenende, ausser die Geschwisterschaft ist der Gegenstand (NV3). NV32
hängt jetzt an TV6.

**D359 (Prüfregel 57 stand da und wurde nicht gelesen).** Der Prompt verlangte einen Volltest,
der nur `classify_all` prüft; die Rücknahmeprobe konnte ihn nicht rot bekommen. Prüfregel 57
beantwortet das seit D278 und nennt beide Funktionen namentlich. Verworfen: eine neue Regel
mit demselben Inhalt, und 57 umzuformulieren — sie wurde nicht missverstanden, sondern nicht
gelesen. Daraus **Prüfregel 71**.

**Prüfregeln 69–71.** 69 (aus D352): ein als ungedeckt gemeldeter Pfad ist erst geschlossen,
wenn ein Test ihn rot werden lässt. 70 (aus D358): ein Vektor muss seinen Zustand im
vollständigen Speicher annehmen. 71 (aus D359): vor einem Prompt wird der einschlägige
Abschnitt der Prüfregeln gelesen.

**Muster dieser Sitzung.** Beide Supervisor-Fehler wurden vom **Werkzeug** gefangen, nicht vom
Supervisor: die roten Szenarien und der einpfadige Volltest. Beide Male hat es nicht committet
und gefragt. Die Anweisung, Rückfragen als Liste zu melden statt unterwegs zu entscheiden, ist
der teuerste Satz im Prompt-Format und hat sich zweimal bezahlt gemacht. Umgekehrt hat das
vollständige Lesen des Diffs dreimal etwas gefunden, das kein Linter sieht: zwei literale
Backslashes vor typografischen Anführungszeichen und zwei Zähl-Drifts in `03` („davon gibt es
zwei", „In beiden Fällen").

Vier Werkzeugnotizen:

- **`check_specs.py` prüft Prompt-Dateien mit.** Eine Prompt-Datei, die D-Nummern zitiert, die
  auf dem Branch noch fehlen, macht `make check` rot. Prompt-Commits gehören deshalb auf
  `main`, bevor der Branch abzweigt — oder `main` muss vorher in den Branch.
- **`welt`-Schritte in Szenarien setzen die Ketten zurück.** Wer über sie hinweg vergleicht,
  erzeugt Scheinverstösse; in `00bc` einmal passiert und erst beim zweiten Hinsehen gemerkt.
- **`test_verdikt.py` parametrisiert über den Saatkorpus.** Jeder neue Vektor erzeugt zwei
  zusätzliche collected items. Differenzen in der Testzahl zuerst dort suchen.
- **Der Diff wird nie gekürzt** — das ist keine Zeremonie, sondern hat in dieser Sitzung drei
  Defekte gefunden, von denen keiner durch einen Linter gegangen wäre.

## Offene Punkte, nach Grösse

**Das grösste, und der nächste Schritt:** D354 ausarbeiten. Drei Fragen: Welche Prämissen muss
ein Claim nennen, damit die Nennung nicht zur Zeremonie wird? Was gilt für einen abhängigen
Claim, der keine nennt — folgenlos nach `08 §2.2`, oder ein eigener Vermerk? Und trägt dieselbe
Mechanik über `t_exp` hinaus, also für jede Prämisse, deren Zustand sich ändern kann? Das ist
Spec-Arbeit mit Forks und Registereinträgen, kein Werkzeuglauf.

**Daneben, kleiner:** O60 — die Budget-/Kantensatz-Asymmetrie, Vorbedingung für jede Fassung
mit unscharfer Zeit. Der Trust-Pfad aus `02a §2.6` als eigener Lauf mit eigener Frage (steht
seit `00bb` offen, Szenario H beantwortet ihn nicht). Der Aufräumlauf, jetzt mit 15 ungebundenen
Wurzeldateien, darunter zwei aus dieser Sitzung, und vier Branches. O56 (PyPI-Name `symbolon`
belegt). O57 (Restack, Frist 3. November).

**Ohne Frist, aber weiter offen:** die Übertragung auf unterbrochene Zustellung
(LoRa/Reticulum). Anschlusspunkte: D345, D346, D350, jetzt D353 — die Monotonie ist die erste
Zeitprüfung im Baum, die ohne Uhr und ohne Erreichbarkeit auskommt und damit auf einem
LoRa-Knoten vollständig durchführbar ist.

**Ungeklärt aus `00bc`:** keine offene Frage aus dieser Runde übrig.

## Der nächste Schritt

Die Fork-Runde zu D354. Vorher lohnt ein Blick auf `02a` T-02.7 und auf die `v`-Behandlung in
`03`, weil dort entschieden wird, ob eine Prämissenliste in Key 1 wirklich ohne Feldsatzänderung
trägt — D354 behauptet es auf Grundlage eines Testfalls, nicht auf Grundlage des ganzen Pfades.
Prüfregel 71 zuerst: `pruefregeln.md`, Abschnitte „Beim Schreiben eines Prompts" und „Beim
Definieren von Typen und Feldern".

Der Aufräumlauf kann jederzeit dazwischen; er kostet wenig und braucht keine Vorentscheidung.
