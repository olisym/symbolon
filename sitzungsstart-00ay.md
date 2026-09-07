# Sitzungsstart: 00ay (MaR / symbolon), fortgeschrieben nach D345–D346

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
Bewährt in `00ay`: statt den Branch nachzuziehen, die Welt mit eigenem Treiber neu bauen
und selbst fahren — das war die Abnahme, die etwas gefunden hat.

## Stand

Am Ende von `00ay`: **797 Tests** (unverändert seit `00au`), Register **D1–D346**,
Prüfregeln **1–67** (neu: 67), **39 Wurzel-Markdown-Dateien**, `make check` grün
(ungekürzt gelaufen, Exit 0). Commit-Hash zu Sitzungsbeginn messen, nicht abtippen.

Historien-Schönheitsfehler: die beiden Szenario-Commits (`0f619db`, `28069c6`) tragen
`00ax:` im Betreff, stammen aber aus `00ay`. Nicht korrigiert, nur vermerkt.

### Die Schichten

Unverändert seit `00ar` — siehe `arbeitsweise.md`, `pruefregeln.md`, `08-scope.md §3`.

### Der Bestand

`tools/sim/`: neu seit `00ay`: `szenario_g.py` (Wegwerf, gemergt, keine Löschung
geplant — drei Läufe, Referenz für Ketten- und Zustellungsfragen). Alles Übrige
unverändert; Szenario G kam wie F ohne ein einziges neues Primitiv aus.

**Korrektur zum Handoff aus `00ax`:** `00ax-szenario-f-prompt.md` existiert nicht und hat
nie existiert — weder im Baum noch in der Historie. Gebunden ist immer nur der jüngste
Sitzungsstart: mit `sitzungsstart-00ay.md` fiel `sitzungsstart-00ax.md` in die
Ungebunden-Liste, die damit neun Einträge zählt (sieben Prompt-Dateien plus die beiden
älteren Sitzungsstarts). Der Aufräumlauf kann beide alten Sitzungsstarts löschen; die
Zahl wird gegrept, nicht abgetippt.

## Was in `00ay` entschieden wurde (D345–D346, Prüfregel 67)

**D345 (Szenario G, der Hauptfund).** Vier Aussagen über die Epochenkette 1→2→3:
(1) Der Rückfall endet am Bruchpunkt, nicht an der Wurzel — eine rivalisierende Ja-Stimme
auf Sprosse 1 wirft auf Epoche 1, dieselbe Stimme auf Sprosse 2 lässt auf Epoche 2 stehen.
(2) Der Rückfall braucht weder Partition noch Gabelung: gerade Autorenkette, eine einzige
Konfliktstimme, Vollzustellung — alle Beobachter landen identisch. (3) Die überholte obere
Sprosse hinterlässt keinen Vermerk; `04 §4.5` verwirft die Vermerke getragener Übergänge
in jedem Schleifenschritt. (4) Ein zurückgehaltenes `ratify@1` hält einen Beobachter
dauerhaft auf einer früheren Epoche, bei leerer Vermerkliste auf **allen** Seiten —
sichtbar nur im Quervergleich zweier Beobachter.

**D346 (die schärfere Ecke).** Eine aktive Ja-Stimme auf ein Vorschlagsobjekt, das der
Autor nie herausgibt, setzt ihn nach `04 §4.4` in jeder Auszählung aus, die eine
Kettenauflösung noch braucht (D178) — bei allen Beobachtern gleichzeitig, unbefristet,
heilbar nur durch ihn selbst. Keine Sperrminorität über die Schwelle, sondern die
dauerhafte Stilllegung genau einer Ja-Stimme zum Preis von null. Anschluss an D234–D236:
ein feindlicher Eintrag muss nicht blockieren, es genügt zu schweigen.

**Prüfregel 67 (Methodik, der Fund der Abnahme).** Eine Szenariokonstruktion trägt keine
Bedingung, die die Frage nicht verlangt. Die erste Fassung von Szenario G hängte drei
Konfliktstimmen per `claim_gabeln` an eine Spitze — bequem, aber der Befund las sich als
Folge einer Equivokation. Der unabhängige Nachbau ohne Gabelung, mit Vollzustellung an
alle, war der einzige Grund, dass D345 in der starken Fassung im Register steht.

**Muster dieser Sitzung.** Der Bericht des Werkzeugs war beide Male sachlich richtig und
alle Erwartungen bestätigt — gefunden wurde trotzdem etwas, und zwar nur durch den
eigenen Nachbau. Der Bericht ist nicht die Abnahme, auch wenn er stimmt.

Zwei Werkzeugnotizen für die nächste Sitzung:

- `tools/stand.py` **braucht ein Argument**: einen Pfad auf eine Datei mit der
  pytest-Ausgabe. Ohne Argument steigt es mit Exit 1 und ohne Zeile aus. Also erst
  `make check > /tmp/mar-check.txt 2>&1`, dann `python tools/stand.py /tmp/mar-check.txt`.
- In `00ay` selbst gerissen: `python tools/stand.py 2>&1 | tail -8` in einer `and`-Kette
  hat den Ausfall verschluckt (Status von `tail`). Prüfregel 66 nennt das Gate; derselbe
  Mechanismus trifft jede Diagnose, deren Ausbleiben man sonst nicht bemerkt.

## Offene Punkte, nach Grösse

**Mit Frist:** O57, Restack-Förderantrag. Frist **3. November 2026, 12:00 CET**. Die
Faktensammlung ist inhaltlich fertig bestückt: Szenario C (D333), LoRa/Partition ehrlich
und bösartig (D336–D341), Governance unter Partition (D342), Kette und Zustellung
(D345/D346). Blockiert unverändert auf **zwei Dingen, die nur Oli lösen kann**: Klärung
mit dem Rentenversicherungsträger (Hinzuverdienstgrenze → Budgetzahl) und die eigene
AI-disclosure-Entscheidung. Die Rentenklärung braucht Vorlauf und läuft besser parallel
zur Repositoriumsarbeit als danach.

**Ohne Dringlichkeit:** O56 (PyPI-Name `symbolon` belegt). Ungebundene Wurzel-Dateien —
Aufräumlauf.

**Ungeklärt aus `00ay`:** keine offene Frage aus dieser Runde übrig. Die Partitionsreihe
(D336–D342, D345, D346) ist geschlossen.

## Der nächste Schritt

**O57.** Die Szenarioarbeit hat geliefert, was der Antrag an Substanz braucht; weitere
Läufe verbessern ihn nicht mehr, die beiden Blocker schon. Zuerst die Rentenklärung
anstossen, dann die AI-disclosure-Entscheidung treffen, dann die Formularsätze selbst
schreiben — die Faktensammlung ist Rohmaterial, keine Prosa, und das soll so bleiben.

Der Aufräumlauf (die ungebundenen Wurzel-Dateien, schrumpft die wachsende Liste in
`check_specs.py`) kann jederzeit dazwischen; er kostet wenig und braucht keine
Vorentscheidung.

Falls doch wieder Szenarioarbeit ansteht, ist die nächste offene Ecke nicht Governance,
sondern die Übertragung des Rechenschaftsmodells auf unterbrochene, unzuverlässige
Zustellung (LoRa/Reticulum), wo weder „jetzt" noch Zustellreihenfolge garantiert sind —
dieselbe Frage, die in der Faktensammlung als nächste technische Phase steht.
