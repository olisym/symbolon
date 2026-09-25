# Sitzungsstart: 00ck (MaR / symbolon), fortgeschrieben nach D478

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

## Die Richtung

Seit D466 ist der Maßstab eine Anwendung, die man bedienen und sehen kann (`ROADMAP.md`). Die
Härtung ruht, außer eine Anwendung stolpert über einen Fehler (`ROADMAP.md §9`).

- Phase 0, Neuausrichtung: abgeschlossen (D466, D467).
- Phase 1, der Verein auf Papier: **abgeschlossen** (D468 bis D470, `szenario-verein.md`).
- Phase 2, S-Node Version 0: **abgeschlossen** (D471 bis D478).
- Phase 3, Oberfläche mit dem Verein: **als Nächstes** (`ROADMAP.md §5`).
- Phase 4 und 5: Simulation, Reticulum.

Oli hat den S-Node bei sich gestartet, den Verein angelegt und über `curl` abgefragt; es lief.

## Stand

Am Ende von `00cj`: **1087 Tests**, Register **D1–D478**, Prüfregeln **1–83**, `make check`
grün, `main` beim Commit, der diesen Sitzungsstart trägt. **35 Wurzel-Markdown-Dateien, alle
gebunden** (neu: `szenario-verein.md`); `archiv/` steht bei 147 mit `sitzungsstart-00ci.md`.
`offen.md` führt **89 Posten**, davon **13 offen** (neu: O89).

## Was in dieser Sitzung geschah

- **D468:** Der Verein auf Papier. Eine Laufgruppe auf dem Beispielnukleus, Gläubigerin der
  Beiträge ist eine eigene Identität KASSE, jedes Mitglied bestätigt nach jedem Epochenwechsel
  selbst, Bürgschaft und Aufnahme bleiben getrennt, der Regelbruch kostet Stimme, Epoche und
  Bürgschaftsgewicht.
- **D469:** Die Auszählung schweigt über Gabelungen; der S-Node zeigt sie.
- **D470:** Zwölf veraltete Stellen in `00`, `01`, `03` und `04` berichtigt.
- **D471:** Bauform des S-Node. Der S-Node bereitet vor, das Gerät mit dem Schlüssel zeigt an und
  unterschreibt und führt die Spitze seiner Kette. Heute ist das Gerät der Browser, am Ende ein
  Offline-Gerät nach Art eines Trezor. Bordmittel, SQLite, `symbolon/node/`.
- **D472:** Abnahme `p1-verein`: `tools/verein.py` prüft jede Zahl aus `szenario-verein.md`,
  die Hashes stehen in `szenario-verein §9`.
- **D473, D474, D475:** P2, Bestand und Sicht. Fremder Inhalt bricht die Sicht nicht mehr: ein
  Genesis, an dem die Auflösung scheitert, wird nicht angenommen; eine formwidrige Mitgliederliste
  ergibt einen Vermerk statt eines Absturzes.
- **D476, D477, D478:** P3, die Schnittstelle. Acht Pfade an `127.0.0.1`, ein Faden, jede Antwort
  schließt ihre Verbindung. `python -m tools.verein_node <datei>` legt den Verein an,
  `python -m symbolon.node <datei>` bedient ihn auf Port 8470.

## Der nächste Schritt: Phase 3, die Oberfläche

Im Browser, gegen den S-Node: Nutzer anlegen, beitreten, Antrag stellen, abstimmen, Beitrag
zahlen und quittieren, die Kollision sehen. Oli bedient, Skripte spielen die übrigen. Vorgehen:

1. Lesen: `szenario-verein §3` bis `szenario-verein §7` (was jeder Bildschirm zeigt), D471
   Beschluss 1 und 2, D476 Beschluss 2 und 5, `symbolon/node/api.py`.
2. **Die Absichten entwerfen.** Welche Handlungen der Browser anbietet und wie der S-Node daraus
   die Felder baut: `accept-rules@1`, `propose@1` samt Vorschlagsobjekt, `vote@1`, `ratify@1` mit
   den zählenden Ja-Stimmen aus `decide`, `vouch@1`, `obligation@1`, `receipt@1`. Ein Pfad je
   Absicht oder einer mit Art; die Antwort wie bei `/prepare`.
3. **Das Gerät im Browser.** Der Schlüssel als nicht exportierbarer WebCrypto-Schlüssel (Ed25519)
   in IndexedDB; die Spitze der eigenen Kette daneben; vor dem Unterschreiben prüft der Browser,
   dass `core` kanonisch ist, sein `I` trägt und seine Spitze als `h_prev` nennt (D471 Beschluss
   2). Offen ist, wie streng die Kanonizitätsprüfung ohne eigenen Kodierer sein kann.
4. **Die Seite kommt vom S-Node**, vom selben Ursprung (D476 Beschluss 5): statische Dateien aus
   dem Paket, keine externen Skripte.
5. Registereintrag vor dem Auftrag, dann Aufträge in kleinen Schritten.

Oli ist kein Programmierer und will die Demo sehen und bedienen. Erklärungen ohne Jargon, die
Szenarien in seinem Alltag verankert.

## Werkzeugnotizen

- **Auftragsweg:** Aufträge liegen in `~/auftraege/`, erledigte in `~/auftraege/erledigt/`. Cursor
  bekommt den Inhalt als erste Nachricht in einem neuen Chat im Agent-Modus, mit „Führe diesen
  Auftrag aus. Es gilt AGENTS.md.“ davor. Oli pusht den Branch vom Host, gelesen wird im Spiegel.
- **Nachtrag auf demselben Branch.** Findet die Prüfung einen Mangel, kommt erst ein
  Registereintrag auf `main`, dann ein Nachtrag auf den Auftrags-Branch; das Werkzeug liest den
  Eintrag mit `git show main:07-decisions.md`. Gemergt wird danach mit `--no-ff`, der Lieferblock
  prüft `HEAD^1` und `HEAD^2`.
- **Ein Lieferblock wechselt selbst auf `main`,** nachdem er den sauberen Baum geprüft hat; Oli
  steht nach einem Auftrag oft noch auf dessen Branch.
- **Lieferungen:** in `/tmp`, Hashprüfung von Lieferung und Basis vor jeder Änderung, `rm` als
  letzter Job vor `== FERTIG ==`. Merge, Push und Branch-Löschung als eigene Befehle.
- **Rücknahmeproben selbst nachfahren**, in der Sache. Trifft eine Probe des Berichts eine
  vorgelagerte Zusicherung statt der Sache, die vorgelagerte Zusicherung für die Probe
  herausnehmen (D478).
- **Messungen im Supervisor-Klon** mit `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.`; Serverläufe mit
  `timeout`. Vor `git checkout` eines Branches lokale Änderungen an `07-decisions.md` verwerfen,
  sonst bricht der Wechsel ab.
- **fish:** `"(cmd)"` in Anführungszeichen wird nicht ersetzt. `test (git status --porcelain |
  count) -eq 0` für einen sauberen Baum. `test $pipestatus[1] -eq 0` hinter einer Pipe auf `tail`.
  Ein `for` über ein Glob ohne Treffer läuft leer und bricht die Kette nicht.
- **Supervisor-Klon:** `cbor2 cryptography pytest hypothesis` per `pip --break-system-packages`.
  Vollständig holen mit `git fetch origin '+refs/heads/*:refs/remotes/origin/*' --prune`.
- **`check_specs`** liest ein `§` hinter einer Registernummer als Verweis ohne Datei. Docstrings
  nennen Auftragspunkte deshalb als „Abschnitt 3.6 Punkt N“.
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
- **Neu aus D474:** Nimmt Code fremden Inhalt an, nennt der Auftrag die Lage, dass dieser Inhalt
  formwidrig ist; sonst baut das Werkzeug den Gutfall.
- **Neu aus D477:** Ein Lader nennt jedes Objekt, das seine Welt braucht, nicht nur die neuen;
  ein Werkzeug ist wiederholbar.
- **Neu aus D478:** Eine Rücknahmeprobe, die an einer vorgelagerten Zusicherung scheitert, zeigt
  nicht, dass der Test die Sache sieht.

## Offene Punkte

**Die 13 offenen Posten** sind Wartestände. O31, O34 bis O40 und O42 sind vertagt, jeder mit
seiner Bedingung; nach D466 öffnet sie ein Szenario, das sie braucht. O25 (Sicherungsblob) ist ein
Bau ohne Anlass. O56 ist der PyPI-Name. O74 ist ein Stolperdraht. **O89** (Amtswechsel der Kasse
ist Schlüsselübergabe) öffnet mit einem Szenario, in dem das Amt wechselt.

**Aus D408 getragen:** Die Zahl der Auswertungen über ein Fenster hat keine Obergrenze. Beisst es
je, gehört die Grenze nach `02 §8`.

**Aus der Aussprache mit Oli, für später:** eigene Währung als Kreditgeld über `unit_ref`
(`03 §3.3`), Olis Versicherungsbild mit kleinem Topf und verteilter Verwahrung, Signaturen mit
Schlüsselpreisgabe nur in Sonderfällen (D467). Kandidaten nach Phase 5.
