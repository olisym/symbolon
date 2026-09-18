# Sitzungsstart: 00bz (MaR / symbolon), fortgeschrieben nach D408

## Was das hier ist

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Repositorium **`symbolon`**, Gitea (`git.h.error13.de/oli/symbolon`,
LAN-only) und GitHub-Spiegel (`github.com/olisym/symbolon`). Lokaler Ordner bleibt
bewusst `~/mensch-als-republik`. Tagline seit D335: *Symbolon: A Self-Verifying Trust
Layer for Local-First Networks*. Spec-Titel bleibt bewusst *Mensch als Republik* (D317).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Aufträge, führst die Abnahmen. Schreibst keinen
Produktivcode.

**Supervisor-Zugriff:** Direkter Klon/Pull über den öffentlichen GitHub-Spiegel. Commit-Hash
vor jedem Lesen gegen den geklonten `HEAD` prüfen. Der Spiegel liegt regelmässig einen Commit
**vor** dem hier genannten Stand, weil dieser Sitzungsstart sich selbst nicht mitzählt.

## Stand

Am Ende von `00bz`: **898 Tests**, Register **D1–D408**, Prüfregeln **1–77**, `make check` grün,
`main` bei `3697063`. **32 Wurzel-Markdown-Dateien, alle gebunden**; `archiv/` steht bei 136, und
mit diesem Sitzungsstart fällt `sitzungsstart-00by.md` dazu. `offen.md` führt **72 Posten**; O71
und O72 sind in dieser Sitzung eröffnet beziehungsweise geschlossen worden.

**Stränge:** `main` und `00bo-hs` (kontaminiert, D374, wird nicht gelöscht). Dazu
`o70-uhrversatz-pin` und `o72-intervall-now`, beide gemergt und stehen gelassen.

## Was in dieser Sitzung geschah

Eine einzige Kette, von O71 bis zur Abnahme von O72.

### D406 — Intervall-`now`, exakt über die Bruchstellen

Der erste Vorschlag war, je Menge konservativ zu wählen: Kante gegen `hi`, Budget gegen `lo`.
Die Literaturrunde hat ihn als die **lockere** Form entlarvt — das ist die monotonicity-based
interval extension, und das Abhängigkeitsproblem der Intervallarithmetik sagt, warum sie zu weit
ist: `now` kommt zweimal vor, ist aber **ein** unbekannter Wert. Gemessen lieferte die Mischung 0,
wo an jedem Punkt des Fensters 6 oder 8 stand. Beschlossen ist die exakte Auswertung über die
Bruchstellen (`t_exp + 1` der Scope-Vouches im Fenster), Rückgabe als Minimum plus obere Schranke.
TrueTime steuerte die Form der einseitigen Prädikate bei, die credal/pignistic-Zweiteilung das
Argument für die zweite Zahl. Gesplict in `02 §3.1`, `§6.2`, `§11.1`, `§11.2`, `§11.4`.

### D407 — Prüfregeln 76 und 77

Der Befundtest (prüft die Meldung, die nur sein Befund erzeugt) und die Benennungsprobe (eine
Rücknahmeprobe belegt auch die Benennung). Beide standen mehrere Sitzungen als Kandidaten.

### Anker 5d, Profil `TP-UHR`

Eigenes Profil in `02-golden-anchors.md`: zwei disjunkte Pfade mit verschieden datierten
Abläufen, eine Bruchstelle bei 601, Fenster `[500, 700]` mit Minimum 6 und oberer Schranke 8.
Die vier Punktwerte sind gegen die Punktform gemessen, die Fensterzahlen abgeleitet — das steht
so im Anker, damit die Herkunft jeder Zahl später erkennbar bleibt.

### D408 — O72 gebaut und abgenommen

Erster Lauf mit Cursor am Host. Nur `symbolon/trust/flow.py` berührt, 885 → 898 Tests. Drei
Korrekturen am eigenen Text: die Flächenzeile in D406 war zu weit (nur `flow()` ändert sich,
`derive()` und `rank()` bleiben punktförmig), Anker 5d versprach eine Trennung für `cut` und
`disjoint_paths`, die er nicht leistet, und die Gleichstandsregel hing ungeprüft an `min()`.
Der letzte Punkt ist der Abnahmebefund: die Implementierung war richtig, aber eine Umstellung auf
die letzte Minimalstelle wäre grün geblieben. Nachgebessert mit demselben Profil und anderem Ziel.

## Werkzeugnotizen

- **Cursor am Host statt Container.** Die Isolation aus D389 ist die Antwort auf die Fremdfassung,
  nicht auf das Referenzrepo; hier soll das Werkzeug die Spec lesen. Erhalten bleiben: frischer
  Thread je Auftrag (das Plus, kein Fortsetzen), Auftrag in `~/auftraege/`, **nie** in der
  Repo-Wurzel, Branch und Push am Host, kein Merge durch das Werkzeug. Gewonnen: `ruff` läuft am
  Host mit. Vor dem Start prüfen, ob threadübergreifende Memories aktiv sind; Regeldateien
  (`.cursor/rules`, `AGENTS.md`) hat das Repo keine.
- **Der Supervisor-Klon ist flach.** `git fetch origin` zieht dort die Branch-Refs nicht mit.
  `git ls-remote origin 'refs/heads/*'` zeigt den wahren Stand; sonst wird zweimal ein fehlender
  Push gemeldet, der längst da war. Vollständig holen mit
  `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`.
- **Lieferungen laufen über `/tmp`, immer**, als ein zusammenhängender Block: Hashprüfung der
  Lieferung und der Basisdateien, Splice oder `cp`, voller `git diff`, `make check`, Commit, Push.
  Marken `== NAME ==` und `== FERTIG ==` in der `and`-Kette; fehlt die Schlussmarke, ist die Kette
  gebrochen.
- **Der Splice-Harness fängt die Zeilenlänge.** Bei D407 wäre die Herkunftszeile auf 110 Zeichen
  gelaufen; der Trockenlauf hat es gemeldet, nicht der Host.
- **Erwartungen werden gezählt, nicht geschätzt.** Bei D406 habe ich `+178` angekündigt, es waren
  143 — die Datei lag vor mir. Der Trockenlauf liefert die Zahl; sie gehört vor den Block.

**Prüfregel-Kandidaten, weiter nicht übernommen:**
- Einen Abschnitt ganz lesen, bevor man aus einem Satz darin schliesst (D392 → D394).
- An zwei Fällen Gemessenes nicht „durchgehend" nennen (D390 → D396).
- Eine Karte aus Wortsuche ist eine Vermutung; vor dem Schreiben den Wortlaut lesen (D397 → D398).
- **Neu aus D408:** eine Flächenzeile, die vor dem Lesen des Codes geschrieben wird, ist eine
  Schätzung und wird als solche gekennzeichnet. Einmal begründet, noch keine Regel.

## Offene Punkte, nach Grösse

**O62** — Zweitimplementierung für Layer 02. Umfang steht (D368), Sprache offen, Prüfregel 15
verlangt den Literaturcheck vor der Wahl. Hier wird der Container wieder zwingend: eine
Fremdfassung, die die Referenz sieht, ist kein zweiter Zeuge (D389).

**Daneben:** D354 mit der Gabel F2. O56 (PyPI-Name belegt).

**Merkposten Restack:** eingereicht am 10. September, Code `2026-11-0c4` (D349). Bewertet wird
nach der Frist am 3. November. **Mitte Oktober** den Antragstext gegen den Stand halten und
entscheiden, ob nachgebessert wird. Wie das Portal eine Aktualisierung abwickelt, ist nicht
geklärt.

**Ungeklärt aus `00be`:** die Invariantentabelle kennt keine Zeitaussage. Die Invarianten stehen
weiter nur in `02-golden-anchors.md §8`; `02` hat seit D398 keinen Invariantenabschnitt bekommen.
Mit D406 ist eine Zeitaussage dazugekommen, die dort fehlt.

**Ohne Frist:** die Übertragung auf unterbrochene Zustellung (LoRa/Reticulum). Anschlusspunkte
D345, D346, D350, D353, D361, D362, D363, D404, jetzt auch D406.

**Aus D408 getragen:** `include_flagged = True` über ein Fenster ist nicht gemessen. Die Zahl der
Auswertungen hängt am Bestand und hat keine Obergrenze; beisst es je, gehört die Grenze nach
`02 §8` und nicht in die Rechenregel.

## Der nächste Schritt

**O62 lesen und die Sprachfrage vorbereiten.** Zuerst D368 (Umfang) und Prüfregel 15, dann der
Literaturcheck, erst danach die Wahl. Der Containerablauf aus `werkzeuge.md` gilt dort
unverändert; was in dieser Sitzung über Cursor gelernt wurde, gilt für das Referenzrepo und
nicht für die Fremdfassung.
