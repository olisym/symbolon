# Sitzungsstart: 00bb (MaR / symbolon), fortgeschrieben nach D350–D352

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

Am Ende von `00bb`: **798 Tests**, Register **D1–D352**, Prüfregeln **1–68**, `make check`
grün, `main` und `origin/main` gleichauf bei `3c21795`. Wurzel-Markdown-Dateien und die
Ungebunden-Zahl werden gegrept, nicht abgetippt; mit diesem Sitzungsstart fällt
`sitzungsstart-00az.md` in die Ungebunden-Liste.

`00ba`/`00bb` waren eine Werkzeugsitzung: ein neuer Diagnoselauf (Szenario H), eine Zeile
Produktivcode repariert, ein Regressionstest, drei Registereinträge. Der Branch
`szenario-h` ist gemergt und kann beim nächsten Aufräumlauf weg.

### Die Schichten

Unverändert seit `00ar` — siehe `arbeitsweise.md`, `pruefregeln.md`, `08-scope.md §3`.

### Der Bestand

`tools/sim/` jetzt mit `szenario_h.py` (`00ba`). Keine neuen Primitive: Verzögerung,
Umordnung und Teilzustellung sind über die Reihenfolge der `zustellen`-Aufrufe und über
`nur=[...]` bereits ausdrückbar; `welt.py` blieb unangetastet.

**Ausserhalb des Repositoriums, bei Oli lokal:** `restack-faktensammlung.md`,
`restack-felder-englisch.md`, `prompt-log.py` und `prompt-log-restack.md` in `~/Downloads`.
Bewusst nicht im Baum. Wenn der Antrag vor dem 3. November nachgebessert wird, sind das die
Dateien dafür.

## Was in `00ba`/`00bb` entschieden wurde (D350–D352)

**D350 (`now` bekommt keine Quelle).** Drei Zeitgrössen erstmals nebeneinander benannt: `t`
(vom Autor behauptet, signiert, nach `01 §2` kein Ordnungsprimitiv, nirgends gegen eine Uhr
geprüft), `t_exp` (signiert, die einzige Stelle mit Wirkung), `now` (je Beobachter, nicht
signiert, in keinem Claim, in keinem Vermerk). Befund: `now` ist die einzige Grösse, die das
Ergebnis ändert und **nicht kollidieren kann** — sie steht damit ausserhalb von `08 §2.2`.
Zweiter Befund: zwei Zeitregime. Governance ist uhrenfrei und begründet so (`04 §3.1`
Bedingung 4, D97), Trust ist konstitutiv uhrgebunden (`02a §2.6`). Verworfen: Netzabfrage
nach Roughtime-Art, Uhrenabgleich unter Anwesenden (Marzullo, Berkeley, NTP), jede
Zeitautorität — alle setzen Erreichbarkeit voraus, dieselbe Gegenthese wie D348.

**D351 (Vermerk zeigte auf das falsche Subjekt).** Szenario H, Lauf 2 brachte erstmals
`UNSUPPORTED_RATIFICATION` und `VOTE_WITH_EXPIRY` gleichzeitig hervor. Beide trugen dieselben
drei Subjekte — die der Stimmen; die `claim_id` der Ratifizierung kam in keinem Vermerk vor.
Entschieden: Defekt, kein Verhalten. Repariert wird das Subjekt, nicht die Erwartung.

**D352 (Abnahme, und der Befund dahinter).** Die Reparatur war eine Zeile
(`subject=cid` → `subject=rid` im Zeugen-Zweig von `verify_ratification`) und seit D207
normativ entschieden: `04 §4.1` sagt, dass der Vermerk die Ratifizierung benennt, und D207
hat die Zeugenliste bereits als Feld ohne eigene Adresse eingeordnet. Der schwerere Befund:
**D207 hatte `epoch.py:140` namentlich als ungedeckten Pfad gemeldet** — „was fehlt, ist
nicht eine Regel, sondern Abdeckung" —, `00q` sollte Prüffälle anlegen, und der Defekt saß
danach genau dort und überlebte bis `00ba`. Ebenfalls festgehalten: zwei Einschränkungen von
Szenario H (Lauf 1/2 messen `resolve_epoch(now=X)`, nicht einen Teilnehmer mit verstellter
Uhr; Lauf 3 arbeitet in einem Scope ohne Nukleus und belegt damit `_is_temporally_valid`,
nicht den Trust-Pfad aus `02a §2.6`).

**Prüfregel-Kandidat aus D352, Nummer noch offen.** Ein als ungedeckt gemeldeter Pfad ist
erst geschlossen, wenn ein Test ihn rot werden lässt. Meldung, Registereintrag und Vorsatz
decken nichts ab; nur der Test tut es. Wortlaut steht ausformuliert in D352.

**Muster dieser Sitzung.** Der Werkzeugbericht war inhaltlich korrekt und in der Einordnung
falsch — er führte den Defekt als „zusätzlicher Ist-Wert (nicht widersprochen)". Sichtbar
wurde er nur durch den Abgleich der berichteten Vermerkmenge gegen den gelesenen Code.
Zwischenzeitlich stand der Verdacht im Raum, die Ausgabe sei nachgebaut statt gemessen; ein
eigener Lauf hat ihn widerlegt, bevor daraus eine Folgerung wurde. Beides gehört zusammen:
der Bericht ist nicht die Wahrheit, und der Verdacht gegen den Bericht ist es auch nicht.

Vier Werkzeugnotizen:

- **`tools/check_specs.py` ist nicht ausführbar** — `.venv/bin/python tools/check_specs.py`,
  nicht `tools/check_specs.py`. In `00ba` gerissen.
- **Nacktes `python` scheitert an `cryptography`**, während `make check` grün bleibt: das
  Makefile setzt `PY := .venv/bin/python`. Der Traceback sieht nach Codefehler aus und ist
  keiner. In `00bb` einmal in die Irre geführt.
- `tools/stand.py` **braucht ein Argument**: erst `make check > /tmp/mar-check.txt 2>&1`,
  dann `python tools/stand.py /tmp/mar-check.txt`.
- **Fish bricht eine Zeile ab, wenn ein Wildcard keinen Treffer hat.** Wildcards, die leer
  sein dürfen, gehören in einen eigenen Job.

## Offene Punkte, nach Grösse

**Das grösste, und der nächste Schritt:** der zweite Satz aus D350 — kann `t` zur
kollidierbaren Zeitaussage werden? `t` ist signiert und wird heute nirgends ausgewertet. Wer
auf Ablauf handelt, gibt dabei ohnehin einen Claim mit eigenem `t` ab; seine Ablaufbewertung
ist implizit bereits signiert. Überführbar wäre nicht die falsche Uhr, sondern die
Unvereinbarkeit der eigenen Behauptungen — Bauform Equivocation. Das ist Spec-Arbeit mit
Forks und Registereinträgen, kein Werkzeuglauf.

**Daneben, kleiner:** der Trust-Pfad aus `02a §2.6` als eigener Lauf mit eigener Frage
(Szenario H beantwortet ihn nicht, siehe D352). Die Prüfregel zu D352 setzen —
`pruefregeln.md` ist thematisch gegliedert und die Herkunftsliste steht am Dateiende, der
Einfüge-Splice braucht einen passenden Anker. Der Aufräumlauf, jetzt mit mehr ungebundenen
Wurzel-Dateien und dem gemergten Branch `szenario-h`. O56 (PyPI-Name `symbolon` belegt).

**Ohne Frist, aber weiter offen:** die Übertragung auf unterbrochene Zustellung
(LoRa/Reticulum) als Ganzes. Die Vorfrage ist mit D350 geklärt — es fehlt kein
Zustellprimitiv und keine Uhrenquelle. Anschlusspunkte: D345, D346, D350.

**Ungeklärt aus `00bb`:** keine offene Frage aus dieser Runde übrig.

## Der nächste Schritt

Die Fork-Runde zu `t`. Drei Fragen, in der Reihenfolge ihrer Härte: Was genau behauptet ein
Beobachter, wenn er sagt „dieser Claim ist abgelaufen"? Kann diese Behauptung zu einem
signierten, kollidierbaren Claim werden? Und reicht als kleinere Variante ein Intervall statt
eines Punktes — `LINKED` bei Überlappung mit `t_exp` —, wo der Verifier den dritten Ausgang
über `temporal is None` bereits kennt?

Der Aufräumlauf kann jederzeit dazwischen; er kostet wenig und braucht keine Vorentscheidung.
