# Sitzungsstart: 00cl (MaR / symbolon), fortgeschrieben nach D497

## Was das hier ist

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Repositorium **`symbolon`**, Gitea (`git.h.error13.de/oli/symbolon`,
LAN-only) und GitHub-Spiegel (`github.com/olisym/symbolon`). Lokaler Ordner bleibt
bewusst `~/mensch-als-republik`.

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, schreibst eng
gefasste Aufträge, führst die Abnahmen und schreibst die Registereinträge. Produktivcode schreibt
das Werkzeug.

**Supervisor-Zugriff:** Klon über den öffentlichen Spiegel, Commit-Hash vor jedem Lesen gegen den
geklonten `HEAD` prüfen. Der Spiegel liegt einen Commit vor diesem Stand, weil sich dieser
Sitzungsstart nicht mitzählt. Der Spiegel übernimmt gelöschte Branches nicht sofort; ob ein
Branch auf Gitea noch existiert, entscheidet nicht der Spiegel.

## Die Richtung

Seit D466 ist der Maßstab eine Anwendung, die man bedienen und sehen kann (`ROADMAP.md`).

- Phase 0 bis 2: abgeschlossen (D466 bis D478).
- Phase 3, Oberfläche mit dem Verein: **im Kern erreicht** (D496). Oli hat den Verein im Browser
  bedient, der Geschichte in der Regie gefolgt und Brunos Gabelung mit Beweis gesehen.
- Phase 4 und 5: Simulation mit mehreren S-Nodes, Reticulum.

## Stand

Am Ende von `00ck`: **1130 Tests**, im Selbsttest des Browsers **126 Fälle**, Register
**D1–D497**, Prüfregeln **1–83**, `make check` grün, `main` beim Commit, der diesen Sitzungsstart
trägt. **35 Wurzel-Markdown-Dateien, alle gebunden**; `archiv/` steht bei 148 mit
`sitzungsstart-00cj.md`. `offen.md` führt **89 Posten**, davon **13 offen**.

## Was in dieser Sitzung geschah

- **D479 bis D485:** Absichten (`POST /intent`, `/sim/intent`) mit Abweisungen und Warnungen, die
  Weltuhr `--uhr-ab`, das Adressbuch, das Gerät im Browser (Ed25519 in WebCrypto, Spitze in
  IndexedDB, Sperre zwischen Tabs, Vektoren aus Python), Aufgaben und Anträge als Lesepfade.
- **D486 bis D489:** die erste Oberfläche, Brunos Gabelung als Skript
  (`python -m tools.verein_gabel`), und was nach einer Gabelung bleibt (D489: kein Vergeben im
  Protokoll, der Weg zurück ist ein neuer Schlüssel; Literatur SSB und Cosmos knapp geprüft).
- **D490:** Olis Durchlauf zeigte eine Seite, die von den Daten her gebaut war. Ein Klickmodell
  (Design-Artefakt „Verein – Klickmodell“) wurde das Vorbild. Maßstab seitdem: eine Oberfläche wird
  an dem Satz gemessen, den ein Mensch nach dem Klick sagen kann. Vorbild außerhalb: Clear Signing
  (ERC-7730) und die Vorhersage der Folgen in Wallets.
- **D491 bis D497:** die Folge vor der Unterschrift (`effect`), die Seite nach dem Modell mit
  Sätzen der Absicht und der Folge (D492: kein Satz, keine Unterschrift), Titel der Anträge, das
  Ende nach einer Gabelung (`/tips`, `h_prev` nur als Spitze), die Geschichte in der Regie, Zeit
  relativ zur Uhr des S-Node.

## Neue Arbeitsweise aus dieser Sitzung

- **Werkstatt ist Claude Code.** Start in `~/mensch-als-republik`, erste Nachricht: „Lies
  ~/auftraege/<auftrag>.md und führe den Auftrag aus. Es gilt AGENTS.md.“
- **Der Bericht enthält keinen Diff** (D491, `AGENTS.md §5`): Commit-Hash, `git diff --stat`,
  `make check`, Rücknahmeproben, Meldungen, Rückfragen. Der Diff wird aus dem Spiegel gelesen,
  sobald Oli den Branch gepusht hat. Die Aufträge verlangen den Diff nicht mehr. Oli reicht den
  ganzen Bericht weiter; er will die Projekt-Anweisung dafür nicht selbst ändern.
- **Blöcke, die nur Markdown ändern,** prüfen mit `make check-tree check-specs check-offen
  check-fragen` (D480). Den vollen Lauf fährt das Werkzeug vor dem Commit und der Supervisor im
  Klon auf dem Stand des Merges.
- **Registereinträge kommen als Anhang** `/tmp/dNNN.md` (D495). Der Block prüft den Hash des
  Anhangs und den des Registers vorher, hängt an und prüft den Hash nachher. Die ganze Datei nur,
  wenn ein älterer Eintrag geändert wird.
- **Lieferungen liegen in `/tmp` mit festen Namen,** `rm` als letzter Job. Keine Suche in anderen
  Verzeichnissen.
- **Oben im Block die Marken** `== HASH ==` und `== BASIS ==`; bricht der Block dort ab, ist
  nichts geändert.

## Der nächste Schritt

1. **Kleiner Auftrag:** die Dauer einer Bürgschaft auf den nächsten ganzen Tag gerundet statt
   abgerundet (D497).
2. **Dann mit Oli entscheiden:** Phase 4 (mehrere S-Nodes, die Tabelle aus
   `szenario-verein §5.2` im Betrieb, D479 Befund 3) oder ein weiterer Schritt an der Seite. Offen
   an der Seite: ob eine Bürgschaft Vertrauen weitergibt, als Folgezeile (D495); der Zugang vom
   Telefon über `adb reverse` oder TLS (D481 Befund 3); Chrome ist ungeprüft (D484).

Oli ist kein Programmierer. Er will die Demo sehen und bedienen; Erklärungen ohne Jargon, am
Alltag verankert. Was er beim Bedienen nicht versteht, ist ein Befund an der Seite, nicht an ihm.

## Die Demo starten

```fish
cd ~/mensch-als-republik
and source .venv/bin/activate.fish
and python -m tools.verein_node ~/mar-daten/verein3.sqlite
and python -m symbolon.node ~/mar-daten/verein3.sqlite --uhr-ab 1000
```

Dann `http://127.0.0.1:8470/`. Die Gabelung im zweiten Terminal mit
`python -m tools.verein_gabel`, wenn genau ein Antrag offen ist. Ein frischer Bestand braucht
eine neue Datei; der Schlüssel im Browser bleibt.

## Werkzeugnotizen

- **Nachtrag auf demselben Branch.** Findet die Prüfung einen Mangel, kommt erst ein
  Registereintrag auf `main`, dann ein Nachtrag auf den Auftrags-Branch; das Werkzeug liest den
  Eintrag mit `git show main:07-decisions.md`. Gemergt wird danach mit `--no-ff`, der Lieferblock
  prüft `HEAD^2`.
- **Ein Lieferblock wechselt selbst auf `main`,** nachdem er den sauberen Baum geprüft hat.
- **Rücknahmeproben selbst nachfahren**, in der Sache, und wenigstens eine eigene bauen, die der
  Bericht nicht hatte. Bleibt eine eigene Probe grün, ist das eine Lücke im Test, festzuhalten
  (D488, D493, D495).
- **JavaScript der Seite** im Klon mit Node prüfen: `run` aus `selbsttest.js` über
  `vektoren.json` mit `globalThis.crypto.subtle`.
- **Messungen im Supervisor-Klon** mit `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.`; Serverläufe mit
  `timeout`. Vor `git checkout` eines Branches lokale Änderungen an `07-decisions.md` verwerfen.
- **fish:** `"(cmd)"` in Anführungszeichen wird nicht ersetzt. `test (git status --porcelain |
  count) -eq 0` für einen sauberen Baum. `test $pipestatus[1] -eq 0` hinter einer Pipe auf `tail`.
  Eine `for`-Schleife liefert den Status des letzten Befehls ihres letzten Durchlaufs; in einer
  `and`-Kette taugt sie nicht als Prüfung.
- **Supervisor-Klon:** `cbor2 cryptography pytest hypothesis` per `pip --break-system-packages`.
  Vollständig holen mit `git fetch origin '+refs/heads/*:refs/remotes/origin/*' --prune`.
- **`check_specs`** liest ein `§` hinter einer Registernummer als Verweis ohne Datei. Docstrings
  nennen Auftragspunkte deshalb als „Abschnitt 3.6 Punkt N“. Überschriften im Register höchstens
  100 Zeichen.
- **Rust-Fassung:** Isolat `~/mar-rs` auf `77f572d`, Anker `573db57`, ruht (D409 Beschluss 3).

## Prüfregel-Kandidaten, weiter nicht übernommen

- An zwei Fällen Gemessenes nicht „durchgehend“ nennen (D390 → D396).
- Eine Karte aus Wortsuche ist eine Vermutung; vor dem Schreiben den Wortlaut lesen (D397 → D398).
- Eine Flächenzeile vor dem Lesen des Codes ist eine Schätzung (D408).
- Der nächste Schritt eines Sitzungsstarts wird gegen `offen.md` und das Register-Ende geprüft
  (D409).
- Ein Strang über mehr als eine Sitzung hat eine O-Nummer oder einen Registereintrag (D412).
- Eine Beschreibung, die eine Zahl aus einem anderen Eintrag wiederholt, veraltet mit ihm (D420).
- Ein Vergleichs-`diff` wird nicht mit `head` gekürzt (D440).
- Eine Bedingung, an die ein vertagter Posten geknüpft ist, wird gegen alle Einträge seit ihrer
  Setzung geprüft (D437).
- Ein Auftrag, der eine frühere Schnittstelle für gültig erklärt, übernimmt die Befunde über sie
  (D447).
- Ein Vektor im Register wird aus der Messausgabe kopiert, nicht abgeschrieben (D457).
- Eine Lücke, deren Normspalte auf einen Satz zeigt, wird gegen dessen Wortlaut geprüft (D459).
- Eine Rücknahmeprobe zählt nur, wenn der Test an der Sache scheitert (D463).
- Eine Welt baut jede Identität frisch (D464).
- Nimmt Code fremden Inhalt an, nennt der Auftrag die Lage, dass dieser Inhalt formwidrig ist
  (D474).
- Ein Lader nennt jedes Objekt, das seine Welt braucht; ein Werkzeug ist wiederholbar (D477).
- Eine Rücknahmeprobe, die an einer vorgelagerten Zusicherung scheitert, zeigt nicht, dass der
  Test die Sache sieht (D478).
- **Neu aus D489:** Wer „das ist die Regel“ sagt, trennt die Regel des Protokolls von der Wahl
  einer Implementierung.
- **Neu aus D490:** Eine Oberfläche wird an dem Satz gemessen, den ein Mensch nach dem Klick sagen
  kann; eine Abnahme der Seite braucht einen Durchlauf mit Oli.
- **Neu aus D494:** Die Abnahme einer Seite liest auch, was sie zeigt und verbirgt, also die
  Stilregeln, nicht nur die Logik.
- **Neu aus D496:** Was ein Mensch eintippt, bindet keine Rechnung an seine Schreibweise.

## Offene Punkte

**Die 13 offenen Posten** sind Wartestände. O31, O34 bis O40 und O42 sind vertagt, jeder mit
seiner Bedingung; nach D466 öffnet sie ein Szenario, das sie braucht. O25 (Sicherungsblob) ist ein
Bau ohne Anlass. O56 ist der PyPI-Name. O74 ist ein Stolperdraht. O89 (Amtswechsel der Kasse
ist Schlüsselübergabe) öffnet mit einem Szenario, in dem das Amt wechselt.

**Aus D408 getragen:** Die Zahl der Auswertungen über ein Fenster hat keine Obergrenze. Beisst es
je, gehört die Grenze nach `02 §8`.

**Aus der Aussprache mit Oli, für später:** eigene Währung als Kreditgeld über `unit_ref`
(`03 §3.3`), Olis Versicherungsbild mit kleinem Topf und verteilter Verwahrung, Signaturen mit
Schlüsselpreisgabe nur in Sonderfällen (D467), eine Stimme, die sich innerhalb einer
Abstimmungsfrist ändern lässt (D487 Befund 3), und der Weg zurück nach einer Gabelung mit neuem
Schlüssel als eigenes Szenario (D489). Kandidaten nach Phase 5.
