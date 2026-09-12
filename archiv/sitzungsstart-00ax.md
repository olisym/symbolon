# Sitzungsstart: 00ax (MaR / symbolon), fortgeschrieben nach D342–D344

## Was das hier ist

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Repositorium **`symbolon`**, Gitea (`git.h.error13.de/oli/symbolon`,
LAN-only) und GitHub-Spiegel (`github.com/olisym/symbolon`). Lokaler Ordner bleibt
bewusst `~/mensch-als-republik`. Tagline seit D335: *Symbolon: A Self-Verifying Trust
Layer for Local-First Networks*. Spec-Titel bleibt bewusst *Mensch als Republik* (D317).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Prompts, führst die Abnahmen. Schreibst keinen
Produktivcode.

**Supervisor-Zugriff:** Direkter Klon/Pull über den öffentlichen GitHub-Spiegel
(`github.com/olisym/symbolon`). Push-Mirror, kann hinter Gitea zurückliegen — Commit-Hash
vor jedem Lesen gegen den geklonten `HEAD` prüfen. Feature-Branches gehen nicht über den
Spiegel — bei einer Abnahme auf einem Branch braucht der Supervisor den vollständigen
`git diff`, nicht die Meldung darüber.

## Stand

Am Ende von `00ax`: **797 Tests** (unverändert seit `00au`), Register **D1–D344**,
Prüfregeln **1–66** (neu: 65, 66 — beide aus eigenen Fehlern dieser Sitzung),
**38 Wurzel-Markdown-Dateien**, `make check` grün (Exit 0, vollständig gelaufen).
Commit-Hash zu Sitzungsbeginn messen, nicht abtippen.

### Die Schichten

Unverändert seit `00ar` — siehe `arbeitsweise.md`, `pruefregeln.md`, `08-scope.md §3`.

### Der Bestand

`tools/sim/`: neu seit `00ax`: `szenario_f.py` (Wegwerf, gemergt, keine Löschung
geplant — Referenz für Governance-Szenarien). `szenario_d.py` in dieser Sitzung
repariert (ungenutzter Import `T_EXP`, seit `2351ee2` unbemerkt rot). Alles Übrige
unverändert; Szenario F kam ohne ein einziges neues Primitiv aus.

Acht ungebundene Wurzel-Prompt-Dateien (vier aus früheren Sitzungen, drei aus `00aw`,
plus `00ax-szenario-f-prompt.md`) — Kandidaten für einen Aufräumlauf, kein Zeitdruck.

## Was in `00ax` entschieden wurde (D342–D344)

**D342 (Szenario F, der eigentliche Fund).** Eine bereits materialisierte Folgeepoche
fällt bei einem Beobachter mit unvollständigem Wissen **zurück**, sobald eine bislang
unbekannte, rivalisierende Ja-Stimme desselben Autors eintrifft (`04 §4.4`). `ratify@1`
bleibt unwiderruflich, keine Epoche wird je widerrufen — `resolve_epoch` baut die Kette
bei jedem Aufruf vollständig neu aus Epoche 1, und ohne aktuell tragenden Übergang endet
sie wieder dort. Drei Stufen bei einem isolierten Beobachter: nur Vorschlag A bekannt →
Epoche 2, `PASSED`; Konfliktstimme trifft ein, Vorschlagsobjekt B fehlt →
`UNKNOWN_PROPOSAL`, Rückfall auf Epoche 1, `PENDING`; Vorschlagsobjekt B trifft nach →
`CONFLICTING_APPROVAL`, Ergebnis unverändert, nur die Diagnose wird präziser.
Kontrastprobe: fehlt das Vorschlagsobjekt dauerhaft, bleibt die Epoche dauerhaft bei 1
(`EPOCH_PROPOSAL_UNAVAILABLE`). Kein Implementierungsfehler — die Kehrseite derselben
Eigenschaft, die eine falsche Ratifizierung verhindert.

**D343 / Prüfregel 65 (Methodik).** Ein Splice-Assert muss den Erfolgszustand des ersten
Laufs verbrauchen, nicht nur den Anker prüfen; sonst gelingt der zweite Lauf ein zweites
Mal, gilt als nicht idempotent-sicher und der Harness verwirft beide.

**D344 / Prüfregel 66 (Methodik, der teuerste Fehler der Sitzung).** `make check 2>&1 |
tail -8` in einer `and`-Kette gibt den Status von `tail` zurück, nicht von `make`. Ein
roter `make check` wurde deshalb gemergt, gepusht und der Branch gelöscht. Derselbe
Mechanismus hatte seit `00aw` einen Lint-Fehler verdeckt. An einem Gate wird nicht
gekürzt.

**Muster dieser Sitzung, unbedingt lesen.** Vier der fünf Fehler kamen daher, dass ich
Regeln nicht befolgt habe, die im Projekt **bereits standen** (Prüfregel 39; Hash-Test
als erster Job; venv-Aktivierung). Der fünfte: eine geänderte Datei nicht neu
präsentiert, dadurch zwei Leerläufe gegen eine veraltete Fassung. Konkret für die
nächste Sitzung:

- Vor jedem `python`-Aufruf im Repo: `source .venv/bin/activate.fish`.
- Splice-Skripte liegen außerhalb des Repos: `ROOT = Path.cwd()`, nie `Path(__file__)`.
- Jede gelieferte Datei bekommt einen **Hash-Test als ersten Job** im Block — und nach
  jeder Änderung wird sie **neu präsentiert**, sonst läuft Oli gegen die alte Fassung.
- Gate und der davon abhängige Tier-1-Zug nie in derselben Kette.
- Neue Register-/Regeltexte vor der Lieferung auf die 100-Zeichen-Grenze prüfen (D222);
  auch die Herkunftszeile in `pruefregeln.md` wächst mit und muss umbrochen werden.

## Offene Punkte, nach Grösse

**Mit Frist:** O57, Restack-Förderantrag. Frist **3. November 2026, 12:00 CET** — noch
knapp zwei Monate. Faktensammlung liegt vor, inhaltlich jetzt gut bestückt: Szenario C
(D333), LoRa/Partition ehrlich und bösartig (D336–D341), Governance unter Partition
(D342). Blockiert unverändert auf **zwei Dingen, die nur Oli lösen kann**: Klärung mit
dem Rentenversicherungsträger (Hinzuverdienstgrenze → Budgetzahl) und die eigene
AI-disclosure-Entscheidung. Beides braucht Vorlauf, besonders die Rentenklärung —
sinnvoll, das jetzt anzustossen, unabhängig davon, woran im Repositorium gerade
gearbeitet wird.

**Ohne Dringlichkeit:** O56 (PyPI-Name `symbolon` belegt). Acht ungebundene
Wurzel-Prompt-Dateien — Aufräumlauf.

**Ungeklärt aus `00ax`:** keine offene Frage aus dieser Runde übrig.

## Der nächste Schritt

**Vorentschieden: Szenario G — Rückfall über mehrere Epochen.** D342 zeigt den Rückfall
auf einer einstufigen Kette (1→2). Offene Anschlussfrage: greift derselbe Mechanismus
auch über mehrere Stufen (Kette 1→2→3, Konfliktstimme trifft die Abstimmung zu Epoche 2),
und wie weit fällt die Kette dann zurück — auf 2 oder bis auf 1? Zweite Teilfrage im
selben Aufbau: kann ein Beobachter durch **selektive** Zustellung dauerhaft auf einer
anderen Epoche gehalten werden als alle übrigen, ohne dass irgendwo ein Vermerk
entsteht, der das sichtbar macht? Das ist die Governance-Entsprechung zu D340/D341
(bösartiger Fall) und die letzte offene Ecke der Partitionsreihe.

Danach, in dieser Reihenfolge: **O57 fertigstellen**, sobald Rentenklärung und
AI-disclosure stehen — mit D342 als drittem unabhängig nachgebautem Befund neben
Szenario C und der LoRa-Reihe. Der Aufräumlauf kann jederzeit dazwischen, er kostet
wenig und schrumpft `check_specs.py`s wachsende Liste.
