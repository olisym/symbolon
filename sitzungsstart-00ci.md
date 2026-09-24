# Sitzungsstart: 00cj (MaR / symbolon), fortgeschrieben nach D467

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
Sitzungsstart nicht mitzählt.

## Die Richtung seit dieser Sitzung

Mit D466 hat sich der Modus geändert. Die Härtung ruht; der Maßstab ist eine Anwendung, die man
bedienen und sehen kann. Es gilt `ROADMAP.md`:

- Phase 0, Neuausrichtung: **abgeschlossen** (D466, D467).
- Phase 1, der Verein auf Papier: **als Nächstes** (`ROADMAP.md §3`).
- Phase 2 bis 5: S-Node als Lebensraum, Oberfläche, Simulation, Reticulum.

Restack ist kein Auslöser mehr, die Frist steht in Olis Kalender. Die „vier Menschen“ gibt es
nicht, und über das Repositorium sollen keine gefunden werden; Beteiligte werden simuliert. O52
und O53 sind deshalb entfallen.

## Stand

Am Ende von `00ci`: **1050 Tests**, Register **D1–D467**, Prüfregeln **1–83**, `make check` grün,
`main` beim Commit, der diesen Sitzungsstart trägt. **34 Wurzel-Markdown-Dateien, alle gebunden**
(neu: `ROADMAP.md`); `archiv/` steht bei 146 mit `sitzungsstart-00ch.md`. `offen.md` führt **88
Posten**, davon **12 offen**.

## Was in dieser Sitzung geschah

- **D462, D463:** `keys.py` und `resolve.py` gegen `00 §6` und `04 §5` gelesen. Genesis-Schlüssel
  sind jetzt uint in jeder Tiefe (`genesis_scope` in `genesis.py`, fünf Leser), die Ordnung zweier
  Rotationen läuft über die Vorgängerrelation aus `01 §6`, zwei überholte Stand-Absätze ersetzt.
- **D464, D465:** Mutationsmessung über `keys.py`, `resolve.py`, `genesis.py`. 200 Mutanten,
  sieben Lücken in 13 Mutanten, gebunden in `tests/nucleus/test_bindung_keys.py`. Die übrigen
  Überlebenden sind Deklaration, unerreichbar oder äquivalent.
- **D466:** Neuausrichtung. Restack abgekoppelt, Härtung ruht, `ROADMAP.md`, der Verein zuerst.
- **D467:** Das Wort „Bond“ ist ausgemustert. Darunter lagen fünf Probleme: Identitäten teuer
  machen, ein Geschäft absichern, Regelbruch bestrafen, Risiken teilen, Dienstleister glaubwürdig
  machen. Nichts baut auf Verwahrung; keine Protokolländerung ohne Szenario; Wahrheit und
  Durchsetzung sind Anwendungsfragen (`08 §2.1`). Betroffene Texte tragen einen Vorbehalt.

## Aus der Aussprache mit Oli, für später

- **Eigene Währung.** Jeder darf eine Recheneinheit herausgeben, wertlos, bis jemand sie annimmt
  (`VISION §3`, `03 §3.3` mit `unit_ref`). Sie ist Kreditgeld im strengen Sinn: eine Forderung
  gegen den Ausgeber. Ein Handelsplatz mit gemeinsamem globalem Zustand wie Uniswap ist im
  Protokoll nicht abbildbar (`08 §5`); Anbieter, die Kurse als Claims stellen, sind es. Kandidat für
  ein Szenario nach Phase 5.
- **Olis Versicherungsbild.** Der Beitrag ist weg, Auszahlungen sind für Mitglieder nicht
  einsehbar, bekannt ist nur, dass genug da ist, ein Überschuss fließt zurück. Das bringt einen
  kleinen Topf mit verteilter Verwahrung zurück. Offen bis zum Versicherungsszenario.
- **Signaturen mit Schlüsselpreisgabe** (Poettering und Stebila; Ruffing, Kate, Schröder) nur in
  Sonderfällen: Anwender lesen keine Konsequenzen.

## Der nächste Schritt: Phase 1, der Verein auf Papier

Ergebnis ist ein Szenario-Dokument, noch kein Code. Vorgehen:

1. Lesen, worauf der Verein baut: Mitgliedschaft (`03 §4`), Stimme, Zählung und Epochen
   (`04 §2.2`, `04 §3`, `04 §4`), Obligation und Quittung (`03 §3.3`), Widerspruch (`01 §4`,
   `08 §2.2`). Wortlaut vor Position.
2. Die drei Abläufe als Folge von Claims aufschreiben: beitreten mit Bürgschaft, Antrag und
   Abstimmung über die Satzung, Beitrag mit Quittung. Dazu die doppelte Stimme.
3. Für jeden Schritt: wer unterschreibt, was jeder Knoten danach rechnet, was ein Bildschirm zeigt.
4. Was fehlt oder umständlich ist, wird ein Registereintrag, bevor etwas gebaut wird.

Oli ist kein Programmierer und will die Demo sehen und bedienen. Erklärungen ohne Jargon, die
Szenarien in seinem Alltag verankert.

## Werkzeugnotizen

- **Auftragsweg:** Aufträge liegen in `~/auftraege/`, erledigte in `~/auftraege/erledigt/`. Cursor
  bekommt den Inhalt als erste Nachricht in einem neuen Chat im Agent-Modus, mit „Führe diesen
  Auftrag aus. Es gilt AGENTS.md.“ davor. Oli pusht den Branch vom Host, gelesen wird im Spiegel.
- **Lieferungen:** in `/tmp`, Hashprüfung von Lieferung und Basis vor jeder Änderung, `rm` als
  letzter Job vor `== FERTIG ==`. Merge und Push als eigene Befehle.
- **Rücknahmeproben selbst nachfahren**, in der Sache: den Mutanten als Textersetzung einsetzen
  oder das Modulattribut ersetzen, nicht Importe entfernen (D463).
- **Mutationsläufe im Supervisor-Klon** mit `PYTHONDONTWRITEBYTECODE=1`, im Vordergrund in
  Teilstücken unter 280 Sekunden. Hintergrundläufe überleben das Ende eines Aufrufs nicht und
  hinterlassen die Datei mutiert. Der AST-Mutator liegt nicht im Repositorium.
- **fish:** `"(cmd)"` in Anführungszeichen wird nicht ersetzt. `test (git status --porcelain |
  count) -eq 0` für einen sauberen Baum. `test $pipestatus[1] -eq 0` hinter einer Pipe auf `tail`.
- **Supervisor-Klon:** `cbor2 cryptography pytest hypothesis` per `pip --break-system-packages`,
  Aufruf mit `PYTHONPATH=.`. Vollständig holen mit
  `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`.
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
- **Neu aus D463:** Eine Rücknahmeprobe zählt nur, wenn der Test an der Sache scheitert.
- **Neu aus D464:** Eine Welt baut jede Identität frisch.

## Offene Punkte

**Die 12 offenen Posten** sind Wartestände. O31, O34 bis O40 und O42 sind vertagt, jeder mit
seiner Bedingung; nach D466 öffnet sie ein Szenario, das sie braucht. O25 (Sicherungsblob) ist ein
Bau ohne Anlass. O56 ist der PyPI-Name. O74 ist ein Stolperdraht.

**Aus D408 getragen:** Die Zahl der Auswertungen über ein Fenster hat keine Obergrenze. Beisst es
je, gehört die Grenze nach `02 §8`.
