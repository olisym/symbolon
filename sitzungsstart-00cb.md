# Sitzungsstart: 00cb (MaR / symbolon), fortgeschrieben nach D416

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

Am Ende von `00cb`: **918 Tests**, Register **D1–D416**, Prüfregeln **1–77**, `make check` grün,
`main` bei `3c3f7f8`, darauf der Commit dieses Sitzungsstarts mit D416. **32 Wurzel-Markdown-
Dateien, alle gebunden**; `archiv/` steht bei 138, und mit diesem Sitzungsstart fällt
`sitzungsstart-00ca.md` dazu. `offen.md` führt **75 Posten**; O9 und O75 sind in dieser Sitzung
geschlossen, O74 und O75 eröffnet worden.

**Stränge:** `main` und `00bo-hs` (kontaminiert, D374, wird nicht gelöscht). Dazu
`o70-uhrversatz-pin`, `o72-intervall-now`, `d410-zeitinvarianten` und `o9-anhang-c-bindung`,
alle gemergt und stehen gelassen.

## Was in dieser Sitzung geschah

### D412 — die „Gabel F2" wird O74

Beim Prüfen des nächsten Schritts gegen `offen.md` fand sich die Gabel aus D354 („Verschachtelung
als Norm oder Schnittmenge bei der Auswertung") nicht auf der Liste. Sie lebte seit `00be` nur in
Sitzungsstarts, unter einem Namen, der mit `00 F2` kollidiert. Jetzt O74, Stolperdraht: das erste
Profil, das in `03 §1.3` einen Prämissen-Key deklariert. Die Vorbedingung aus D361 ist seit D404
erfüllt. Die Übertragung auf LoRa/Reticulum ist eine Richtung, kein Posten; ihre Anschlussliste
steht in D412, Sitzungsstarts zitieren D412.

### D413 und D414 — O9: Anhang C an `vectors_01.json` gebunden

`tests/test_anhang_c_bindung.py`, 7 Tests, bindet alle 41 Vektoren in beide Richtungen; was
`bytes` meint, entscheidet C.0 (D396). Die Verfälschungsproben stehen dauerhaft im Test. Vorab im
Klon gemessen, am Branch abgenommen, dazu sieben eigene Verfälschungen jenseits des ersten
Vorkommens. Zwei Schwächen, nicht blockierend, in D414. Die getippten TV1-Tests und `GOLDEN`
sind redundant und bleiben, bis ein Anlass sie berührt.

### D414 und D415 — Lieferregeln und README

Die Lieferregeln für Befehlsblöcke stehen jetzt in `arbeitsweise.md §5`, im selben Wortlaut, der
für die Supervisor-Anweisung geliefert wurde. Die README nennt keine wachsenden Zahlen mehr und
verweist auf `make check`, das Registerende und diesen Sitzungsstart; „formally verified" ist
gestrichen, die Layer-02-Fassungen sind nachgetragen.

### D416 — HS2 lief in opencode mit DeepSeek

Nachtrag zu D374 und D389, nach Auskunft des Operators. Das Werkzeug von HS1 ist nicht
festgehalten. „Werkzeugseitig unbelegt" bleibt der Befund.

## Werkzeugnotizen

- **Lieferungen:** in `/tmp`, Hashprüfung von Lieferung und Basis vor jeder Änderung, `rm` als
  letzter Job vor `== FERTIG ==`. Steht in `arbeitsweise.md §5` (D414).
- **Marken je Prüfgruppe:** `HASH` für Lieferungen, `BASIS` für Branch, Commit und Zieldateien.
  Anlass: ein Branch-Abbruch unter der Marke `HASH` wurde als Hashfehler gelesen. Noch nicht in
  `arbeitsweise.md`, nur für die Anweisung geliefert.
- **Merge und Push** als eigene Befehle ausserhalb des Blocks; der Lieferblock prüft danach den
  erwarteten `HEAD`. In dieser Sitzung wurde der Merge einmal vergessen, die `BASIS`-Prüfung hat
  gehalten.
- **Cursor am Host, frischer Thread je Auftrag.** Der Auftrag prüft im ersten Schritt die
  Commit-Meldung von `main`. Erledigte Aufträge liegen in `~/auftraege/erledigt/`.
- **`git --no-pager`** in allen Blöcken.
- **Der Supervisor-Klon ist flach.** Vollständig holen mit
  `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`. Für Messungen braucht es `cbor2`,
  `cryptography`, `pytest` und `hypothesis`. Vor jedem `checkout` die eigenen Entwürfe
  verwerfen (`git checkout -- .`), sonst bricht er ab.

**Prüfregel-Kandidaten, weiter nicht übernommen:**
- Einen Abschnitt ganz lesen, bevor man aus einem Satz darin schliesst (D392 → D394).
- An zwei Fällen Gemessenes nicht „durchgehend" nennen (D390 → D396).
- Eine Karte aus Wortsuche ist eine Vermutung; vor dem Schreiben den Wortlaut lesen (D397 → D398).
- Eine Flächenzeile, die vor dem Lesen des Codes geschrieben wird, ist eine Schätzung (D408).
- Der nächste Schritt eines Sitzungsstarts wird gegen `offen.md` und das Register-Ende geprüft,
  bevor er fortgeschrieben wird (D409).
- **Neu aus D412:** ein Strang, den ein Sitzungsstart über mehr als eine Sitzung trägt, hat eine
  O-Nummer oder einen Registereintrag, auf den er zeigt. Ergänzt den Kandidaten aus D409, der
  einen nie eingetragenen Posten nicht sieht.
- **Neu aus D415:** die englische Schale nennt keine Zahl, die mit der Arbeit wächst. Kandidat für
  `check_specs`, falls sie je wieder eine einführt.

## Offene Punkte, nach Grösse

**Merkposten Restack:** eingereicht am 10. September, Code `2026-11-0c4` (D349). Bewertet wird
nach der Frist am 3. November. **Mitte Oktober** den Antragstext gegen den Stand halten und
entscheiden, ob nachgebessert wird; die README ist seit D415 nachgezogen und wird mitgelesen. Wie
das Portal eine Aktualisierung abwickelt, ist nicht geklärt.

**O73** — der zweite Zeuge liest einen überholten Text. Stolperdraht, kein Lauf.

**O74** — Verschachtelung oder Schnittmenge. Stolperdraht, kein Lauf.

**Daneben:** O56 (PyPI-Name belegt).

**Ohne Frist:** die Übertragung auf unterbrochene Zustellung, geführt als Richtung in D412.

**Aus D408 getragen:** die Zahl der Auswertungen über ein Fenster hängt am Bestand und hat keine
Obergrenze; beisst es je, gehört die Grenze nach `02 §8` und nicht in die Rechenregel.

## Der nächste Schritt

Kein Bau steht an; geprüft gegen `offen.md` und das Register-Ende (D416). Ab Mitte Oktober: der
Restack-Antrag gegen den Stand. Bis dahin ist Stillstand ein gültiger Zustand. Wer vorher
arbeiten will, findet Hygieneposten ohne Anlass (O43, O48, O49) oder die Anwendungsfragen O3 bis
O7; beides ist Wahl, nicht Pflicht.
