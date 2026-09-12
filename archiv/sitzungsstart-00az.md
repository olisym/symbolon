# Sitzungsstart: 00az (MaR / symbolon), fortgeschrieben nach D347–D349

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

Am Ende von `00az`: **797 Tests** (unverändert seit `00au`), Register **D1–D349**,
Prüfregeln **1–68** (neu: 68), `make check` grün. Wurzel-Markdown-Dateien und die
Ungebunden-Zahl werden gegrept, nicht abgetippt — mit diesem Sitzungsstart fällt
`sitzungsstart-00ay.md` in die Ungebunden-Liste.

`00az` war eine reine Papiersitzung: kein Werkzeuglauf, keine Codeänderung, drei
Registereinträge und ein Splice. Der Commit-Hash zu Sitzungsbeginn wird gemessen.

### Die Schichten

Unverändert seit `00ar` — siehe `arbeitsweise.md`, `pruefregeln.md`, `08-scope.md §3`.

### Der Bestand

`tools/sim/` unverändert seit `00ay` (`szenario_g.py` zuletzt hinzugekommen).

**Ausserhalb des Repositoriums, bei Oli lokal:** `restack-faktensammlung.md` (Rohmaterial
je Formularfeld), `restack-felder-englisch.md` (die eingereichten Feldtexte),
`prompt-log.py` und `prompt-log-restack.md` in `~/Downloads`. Bewusst nicht im Baum. Wenn
der Antrag vor dem 3. November nachgebessert wird, sind das die Dateien dafür.

## Was in `00az` entschieden wurde (D347–D349, Prüfregel 68)

**D347 (Budget und Offenlegung).** 15.000 € beantragt: 230 h zu 60 €/h plus Sachkosten.
Der Satz ist hoch gewählt, weil ein niedrigerer dieselbe Summe in eine höhere, im Antrag
schriftlich fixierte Stundenzahl übersetzt. Die KI-Nutzung wird vollständig offengelegt.
Verworfen: eine schriftliche Vorabklärung beim Rentenversicherungsträger — die Betragsfrage
war ohne Anfrage entscheidbar.

**D348 (programmierbare Kryptographie geprüft, nicht aufgenommen).** 0xPARC, Teil 1.
Entgegengesetzte Richtung zu `08 §2.2`: dort wird eine Aussage unbestreitbar gemacht, hier
gründet Überprüfbarkeit darauf, dass Aussagen kollidieren können. „Hallucinated Servers"
ist die Gegenthese zu D312 und hält nicht, weil MPC/FHE kollektive Verfügbarkeit
voraussetzen — unter Partition nicht gegeben (D336–D342). Nebenbefund: der Text räumt
selbst ein, dass auch die stärkste Konstruktion den Fork nicht verhindern kann; das stützt
D234–D236 aus fremder Richtung.

**D349 (O57 eingereicht, plus der Fund der Sitzung).** Restack-Antrag am 10.9.2026
eingereicht, Code `2026-11-0c4`. Die Bewertung beginnt erst nach dem 3. November, und bis
dahin zählt die zuletzt vollständige Fassung — eine Nachbesserung bleibt möglich. Der
methodische Befund stammt aus dem Kuratieren des beigefügten Prompt-Logs: zwei Prüfläufe
mit verschiedenen Werkzeugen fanden je etwas, was der andere übersah. Die Mustersuche fand
die Stellen mit ihren Schlagwörtern, das vollständige Lesen fand einen Abschnitt, der
keines davon trug.

**Prüfregel 68.** Eine Prüfung auf Abwesenheit braucht einen zweiten Lauf mit anderem
Fehlermodus. Ohne Treffer zu bleiben belegt nur, dass die eigene Konstruktion nichts
gefunden hat.

**Muster dieser Sitzung.** Zweimal hat eine Prüfung auf einem Ausschnitt gearbeitet und
deshalb danebengegriffen: einmal verlor ein gefiltertes Suchergebnis den Kontext und ordnete
eine Fundstelle dem falschen Kanal zu, einmal lag die gesuchte Stelle jenseits der
110-Zeichen-Grenze einer Übersicht. Beides fiel erst auf, als dieselbe Frage gegen den
vollen Text lief.

Zwei Werkzeugnotizen:

- `tools/stand.py` **braucht ein Argument**: einen Pfad auf eine Datei mit der
  pytest-Ausgabe. Also erst `make check > /tmp/mar-check.txt 2>&1`, dann
  `python tools/stand.py /tmp/mar-check.txt`.
- **Fish bricht eine Zeile ab, wenn ein Wildcard keinen Treffer hat** — `ls *.zip *.json`
  scheitert vollständig, sobald kein JSON existiert, und die ganze `and`-Kette steht. In
  `00az` gerissen. Wildcards, die leer sein dürfen, gehören in einen eigenen Job.

## Offene Punkte, nach Grösse

**Ohne Frist, aber inhaltlich das grösste:** die Übertragung des Rechenschaftsmodells auf
unterbrochene, unzuverlässige Zustellung (LoRa/Reticulum), wo weder „jetzt" noch
Zustellreihenfolge garantiert sind. Anschlusspunkte im Register: D345 (Rückfall ohne
Partition und ohne Gabelung) und D346 (Zurückhalten kostet nichts und legt genau eine
Ja-Stimme still).

**Ohne Dringlichkeit:** O56 (PyPI-Name `symbolon` belegt). Ungebundene Wurzel-Dateien —
Aufräumlauf; der kann jetzt drei Sitzungsstarts löschen statt zwei, die Zahl wird gegrept.

**Nicht mehr offen:** O57 ist mit D349 geschlossen.

**Ungeklärt aus `00az`:** keine offene Frage aus dieser Runde übrig.

## Der nächste Schritt

**Das LoRa/Reticulum-Szenario.** Es ist die nächste inhaltliche Ecke, es steht im
eingereichten Antrag als die kommende Phase, und wenn es vor Ende Oktober Befunde liefert,
können die in die letzte Antragsfassung nachgezogen werden. Kein Zwang dazu — der Antrag
steht auch ohne.

Der Aufräumlauf kann jederzeit dazwischen; er kostet wenig und braucht keine
Vorentscheidung.
