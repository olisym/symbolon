# Sitzungsstart: 00cw (MaR / symbolon), fortgeschrieben nach D613

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Repositorium **`symbolon`**, Gitea (`git.h.error13.de/oli/symbolon`,
LAN-only) und GitHub-Spiegel (`github.com/olisym/symbolon`). Lokaler Ordner bleibt
bewusst `~/mensch-als-republik`.

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, schreibst eng
gefasste Aufträge, führst die Abnahmen und schreibst die Registereinträge. Produktivcode schreibt
das Werkzeug.

**Supervisor-Zugriff:** Klon über den öffentlichen Spiegel, Commit-Hash vor jedem Lesen gegen den
geklonten `HEAD` prüfen. Der Spiegel übernimmt gelöschte Branches nicht sofort; ob ein Branch auf
Gitea noch existiert, entscheidet nicht der Spiegel.

## Die Richtung

Seit D466 ist der Maßstab eine Anwendung, die man bedienen und sehen kann (`ROADMAP.md`).

- Phase 0 bis 4: abgeschlossen (D466 bis D526). Mehrere Geräte einer Person, die Lücken zwischen
  Norm und Bau und O96 (Sachanträge) sind erledigt (D529 bis D581).
- **Phase 5: Reticulum, Strang O97** (D583). (1) Bestandsaufnahme, (2) der Bote, (3) das Lab auf
  einer Maschine: gebaut (D583 bis D592). (4) Verlust und Bandbreite nach Art von LoRa: läuft, mit
  einem geteilten Kanal im Userspace statt `netem` (D607); Trickle und Fristen nach Bitrate sind
  gebaut (D611, D612), als Nächstes das Bündel. (5) Funk über Olis T-Beams.
- **Governance nebenbei:** Wahlgänge mit Patt in Norm, Bibliothek und Knoten (O98 erledigt, D594
  bis D604). Die Seite sagt, wenn eine Abstimmung vorbei ist (D605, D606).
- **Danach, mit Oli verabredet (D606 Beschluss 3):** das Bündel mit QR-Code, die T-Beams, dann die
  Gründung eines Vereins als Bild und Bestandsaufnahme (Vorlagen, Feldtypen, O101).

## Stand

Am Ende von `00cv`: **1434 Tests**, darin der Selbsttest der Seite mit **241 Fällen**, Register
**D1–D613**, Prüfregeln **1–83**, `make check` grün, `main` beim Commit, der diesen Sitzungsstart
trägt. **35 Wurzel-Markdown-Dateien, alle gebunden**; `archiv/` steht bei 159 mit
`sitzungsstart-00cv.md`. `offen.md` führt **101 Posten**, davon **17 offen**: die 14 Wartestände,
O97, O100 und O101.

`rns 1.5.4` ist Teil von `dev` (D584 Beschluss 4). `make check` braucht es, wie es Node braucht.
Die Testreihe dauert jetzt sechs bis acht Minuten; die Tests mit Boten warten auf die erste
Ankündigung nach Trickle (D612 Befund 2).

## Was in dieser Sitzung geschah

- **D594 bis D597 — die Spaltung und ihr Ausweg.** Das zweite Bild (`--spaltung`): West und Ost
  entscheiden getrennt, Bruno und Dora stimmen auf beiden Seiten; vereint fallen beide Beschlüsse.
  Befund: danach ist die Fassung für alle gebunden, jedes weitere Ja unvereinbar. Ausweg eins: die
  Sperre als Absicht `device-end`, beide Brücken sperren (`--ausweg`, D596). Dazu recherchiert:
  accountable safety, Polygraph, ZLB, Tendermint, inactivity leak.
- **D595, D598 bis D604 — Wahlgänge.** Olis Einwand: eine Uhr aus den Claims. Daraus die Wahlgänge:
  ein Patt, am Bestand bewiesen, eröffnet den nächsten von selbst. Norm `04 §4.7`, Feld 4,
  Bedingung 8, `INV-04.12` und `INV-04.13`, `GV-92` bis `GV-103`; Bibliothek (`p41`), Knoten und
  Bild `--wahlgang` (`p42`). Befund dabei: die Absicht `ratify` nahm zwei Zeugen derselben Person
  (seit D542, D603 Befund 1). O98 erledigt.
- **D605, D606 — die Seite.** „Im Verein“ sagt, wenn eine Abstimmung vorbei ist (`p43`). Olis
  Durchlauf: der Tab hat keinen Zweck; neu O101 (was ein Mensch zuerst sieht), O99 erledigt.
- **D607 bis D612 — Stufe 4.** Ein geteilter Funkkanal (`tools/funk.py`) statt `netem`, kein
  Root. Befund: bei 1200 bit/s bricht der Abgleich zusammen. Mein Kanal hatte zuerst ein Echo
  (D610 Befund 1). Ursache: Ankündigung in jedem Takt und feste Fristen. Gebaut (`p44`): Trickle
  nach RFC 6206 mit dem Stand als `app_data`, Fristen nach Bitrate, Sperrliste in jedem Takt,
  `--funk` im Lab. Befund: RNS ruft den Hörer mit Namen auf (D611 Befund 1).
- **D613 — Schluss der Sitzung.**

## Arbeitsweise, bestätigt

- **Prototyp vor dem Auftrag, Tests wörtlich im Auftrag, Rücknahmeproben vorher gegen diese
  Fassung**, der Prototyp fährt `make check` ganz. Tests eines Nachtrags gehen als Diff in den
  Auftrag, das Werkzeug wendet ihn mit `git apply` an.
- **Oli bekommt jeden Git-Befehl vollständig**, auch Merge, Push und das Löschen von Branches, je
  Schritt ein eigener Block mit Prüfungen vorher und der erwarteten Ausgabe. Er kopiert, er tippt
  nicht (00cu). Nach einem abgebrochenen Block zuerst lesen, nie blind wiederholen.
- **`main` vorher prüfen.** Ein Block, der auf `main` schreibt, prüft den Merge des Laufs mit ab;
  zweimal fing die Basisprüfung einen fehlenden Merge.
- **Ein Lauf, den kein Test fährt, fährt der Supervisor vor der Abnahme** (`main` von `tools.netz`,
  D589 Befund 4, D590).
- **Eine Abnahme der Seite braucht einen Durchlauf mit Oli** (D490); das Lab hat er gesehen.
- **Oli entscheidet, was er sieht, und wählt den nächsten Strang**; eine Frage je Antwort.
- **Kein Auftrag verlangt einen Push**, und die Deny-Regeln aus D592 verbieten ihn dem Werkzeug.
- **Das Werkzeug darf auch Cursor sein** (D606 Befund 1). Die Deny-Regeln aus D592 gelten dort
  nicht; die Abnahme liest ohnehin den Diff.
- **Last von unten aufbauen.** Nach zwei erfolglosen Anläufen am selben Symptom erst zwei, dann
  drei, dann fünf Geräte, mit einer Zählung je Paketart (D610).
- **Oli misst die Seite mit einem Satz:** was er als Anna denkt (D605, D606).


## Der nächste Schritt

**Das Bündel** (D610 Beschluss 2, D611 Beschluss 5, D612 Beschluss 2). Alles Fehlende in einem
CBOR-Paket, mit zlib komprimiert, gleich über Reticulum, als Datei und später als QR-Code. Gemessen
am Stand aus einem Funklauf: 14 Claims und 10 Objekte, 7,0 kB roh, 2,7 kB komprimiert; ein QR-Code
Version 40 fasst 2,95 kB. Entwurf, noch ohne Registereintrag:

- `symbolon/buendel.py`: schreiben und lesen, mit Kennung, Obergrenze beim Entpacken und dem
  formwidrigen Fall. Ohne Kennungen je Eintrag; der Empfänger rechnet sie selbst.
- Drahtpfad `paket` für den Boten: nach dem Vergleich der Bestände eine Anfrage für alles
  Fehlende, die Antwort ist ein Bündel. Danach im Lab bei 9600 und 1200 bit/s messen.
- `python -m tools.buendel` zum Schreiben und Lesen einer Datei über die HTTP-Schnittstelle des
  Knotens; der Empfänger liefert alles ein, der Knoten verwirft Bekanntes.
- Der QR-Code braucht eine Bibliothek zum Erzeugen und eine zum Lesen oder die Kamera des Browsers;
  das ist eine Entscheidung mit Oli.

Vorher gegen `offen.md` und das Register-Ende prüfen (D409).

## Die Demo starten

**Ein Knoten, die Geschichte der Aufnahme:**

```fish
cd ~/mensch-als-republik
and source .venv/bin/activate.fish
and python -m tools.verein_node ~/mar-daten/verein4.sqlite
and python -m symbolon.node ~/mar-daten/verein4.sqlite --uhr-ab 1000
```

Dann `http://127.0.0.1:8470/`. Ein frischer Bestand braucht eine neue Datei. In `verein3.sqlite`
ist die Geschichte durch.

**Sachanträge:** derselbe Ein-Knoten-Verein; der Ablauf aus D580 und D581 steht in der Abnahme zu
`p35-seite`: Sachantrag stellen, drei Ja, feststellen, Stand im Tab „Im Verein“, Satzungsantrag
mit `S`, zweites Ja nach Regel 3.

**Fünf Geräte, das Bild der Lüge:**

```fish
cd ~/mensch-als-republik
and source .venv/bin/activate.fish
and python -m tools.netz ~/mar-daten/netz2
```

Dann die fünf gedruckten Adressen in je einem Tab und der gedruckte Ablauf. Ein frischer Anfang
braucht ein neues Verzeichnis. In `~/mar-daten/netz1` ist der Ablauf durch.

**Personen, die selbst handeln:** derselbe Befehl mit `--personen` (Bild a, fünf Geräte),
`--versehen` (Bild b, sechs Geräte, geteilter Schlüssel) oder `--geraete` (Bild c, sechs Geräte,
Zweitgeräte mit eigenem, aufgenommenem Schlüssel; D542), je mit neuem Verzeichnis. Nach etwa 12 oder
16 Sekunden ist der Lauf durch; dann die Tabs öffnen und nur ansehen. `--aufloesen` ist Bild (c)
mit Annas Warten und Brunos Auflösung (D551). Durch sind `netz-p1`, `netz-v1`, `netz-v2`,
`netz-g1`, `netz-a1`, `netz-v3`; im Ein-Knoten-Verein `verein5.sqlite`,
`verein6.sqlite` und `verein7.sqlite` (der Durchlauf zu den Sachanträgen, D581).

**Das Lab über Reticulum** (D588 bis D591): derselbe Befehl mit einer Geschichte und `--reticulum`
am Ende, je mit neuem Verzeichnis, etwa

```fish
cd ~/mensch-als-republik
and source .venv/bin/activate.fish
and test ! -e ~/mar-daten/lab2
and python -m tools.netz ~/mar-daten/lab2 --aufloesen --reticulum
```

Im Terminal „Gerät ← Nachbar: geholt=…“ und nach jedem Takt „gleicher Stand nach … s“; der ganze
Lauf in `verlauf.txt`. Beim Start kann RNS zwei `AttributeError` melden, beim Beenden gibt es Lärm
(D590 Befund 2 und 3). Durch ist `lab1`.

**Die Bilder dieser Sitzung**, je mit neuem Verzeichnis und `--reticulum` am Ende: `--spaltung`
(West und Ost, vereint fallen beide Beschlüsse, D594), `--ausweg` (danach sperren Bruno und Dora
ihr Zweitgerät, D596), `--wahlgang` (danach beantragt Anna neu, und es gilt ohne Sperre, D603).
Nach der Vereinigung sagt „Im Verein“, dass die Abstimmung vorbei ist (D605).

**Über simulierten Funk:** statt `--reticulum` am Ende `--funk`. Ein Kanal mit 9600 bit/s und 5 %
Verlust, je Gerät eine eigene RNS-Instanz; alle 10 s eine Zeile `funk pakete=… ankuendigungen=…`.
Ein Takt dauert Minuten (D611 Befund 3). Olis Verzeichnisse dieser Sitzung: `wahlgang1`,
`spalt2`, `spalt3`, `ausweg1`, `funk1`, soweit gefahren; ein neuer Lauf braucht ein neues.


## Werkzeugnotizen

- **Werkstatt ist Claude Code.** Start in `~/mensch-als-republik`, erste Nachricht: „Lies
  ~/auftraege/<auftrag>.md und führe den Auftrag aus. Es gilt AGENTS.md.“ Der Bericht enthält
  keinen Diff (D491); der Supervisor liest ihn aus dem Spiegel.
- **Registereinträge kommen als Anhang** `/tmp/dNNN.md` (D495); der Block prüft den Hash vorher
  und nachher. Lieferungen in `/tmp` mit festen Namen, `rm` als letzter Job. Oben im Block
  `== HASH ==` und `== BASIS ==`.
- **Blöcke, die nur Markdown ändern,** prüfen mit `make check-tree check-specs check-offen
  check-fragen` (D480). Den vollen Lauf fährt das Werkzeug vor dem Commit.
- **Abgelegte Aufträge:** `find ~/auftraege -maxdepth 1 -name '*.md' -exec mv -t
  ~/auftraege/erledigt/ {} +` verschiebt auch, wenn nichts da ist, ohne die Kette zu brechen.
- **JavaScript der Seite** im Klon mit Node prüfen: `run` aus `selbsttest.js` über
  `vektoren.json` mit `globalThis.crypto.subtle`. Den Stil prüft `test_stil.py`; geerbte
  Farbpaare sieht er nicht (D512), wer dunkle Werte ändert, misst sie nach.
- **Messungen im Supervisor-Klon** mit `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.`, `make PY=python3`
  für die Markdown-Prüfungen; Serverläufe mit `timeout`.
- **fish:** `"(cmd)"` in Anführungszeichen wird nicht ersetzt. `count` gibt bei null Zeilen den
  Status 1: nur als `test (… | count) -eq 0`, nie als nackte Pipe in der Kette. `test
  $pipestatus[1] -eq 0` hinter einer Pipe auf `tail`. Eine `for`-Schleife taugt in einer
  `and`-Kette nicht als Prüfung.
- **Supervisor-Klon:** `cbor2 cryptography pytest hypothesis` per `pip --break-system-packages`.
  Vollständig holen mit `git fetch origin '+refs/heads/*:refs/remotes/origin/*' --prune`.
- **`check_specs`** liest ein `§` hinter einer Registernummer als Verweis ohne Datei. Überschriften
  im Register höchstens 100 Zeichen.
- **Rücknahmeproben vor dem Auftrag:** Die Python-Teile im Klon als Prototyp bauen, die Tests in
  der Fassung des Auftrags schreiben, jede verlangte Probe dagegen fahren, den Prototyp verwerfen
  (D517, D518).
- **Einen Ablauf für Oli** vorher über die Schnittstelle fahren (`/sim/intent`, `/getrennt`), mit
  dem echten Startbefehl im Hintergrund über `setsid timeout`. Zweimal fand das eine Falle, die
  kein Test sah (D518).
- **Rust-Fassung:** Isolat `~/mar-rs` auf `77f572d`, Anker `573db57`, ruht (D409 Beschluss 3).
- **Das Werkzeug fährt Rücknahmeproben ohne Bytecode-Cache.** Zweimal zeigte ein veralteter
  `.pyc` eine Probe grün (D538, D540). Im Supervisor-Klon gilt `PYTHONDONTWRITEBYTECODE=1`
  ohnehin.
- **`tests/governance/fixtures.py`:** `fresh_p2()` liefert ALICE, BOB, CAROL, DAVE, EVE in dieser
  Reihenfolge. Eine Verfassung mit anderem Boden baut man dort ohne neue Epoche.
- **Ein laufender Auftrag bekommt einen Nachtrag, keinen neuen Auftrag,** wenn eine Rückfrage die
  Spec ändert: Arbeit parken (`git stash`), Spec auf `main`, Branch vorspulen, Arbeit zurück (D537).
- **Ein Nachtrag auf demselben Branch** trägt seinen Registereintrag auf dem Branch, nicht auf
  `main`: dann bleibt die Historie linear und der Merge ein Vorspulen (D544, D545).
- **Der Selbsttest läuft in `make check`** (`tests/node/test_selbsttest.py`, D555). Ein Auftrag,
  der Fälle hinzufügt, nennt die neue Zahl `_FAELLE`; ohne Node ist `make check` rot.
- **Rote Fälle des Selbsttests benennen:** ein Node-Skript nach dem Muster aus
  `tests/node/test_selbsttest.py`, das `expect` der Fälle mit `ok` falsch druckt; so zeigt eine
  Rücknahmeprobe den Fall, nicht nur den einen Python-Test (D580).
- **Der Prototyp einer Seite** wird im Klon mit dem echten Knoten im Hintergrund gefahren
  (`python3 -m tools.verein_node`, dann `setsid timeout … python3 -m symbolon.node`), die Absicht
  über `/intent` wie die Seite, danach `/sim/intent`. So fand D580 Befund 2.
- **Merge als eigener Befehl vor dem Registerblock.** Die Basisprüfung des Blocks fängt einen
  vergessenen Merge ab (der Block prüft `HEAD` gegen den Commit des Laufs).
- **RNS im Supervisor-Klon:** `pip install --break-system-packages rns`. Mehrere Knoten mit Boten
  laufen dort als Prozesse; die Geschichten über ein Skript in einer Datei mit `setsid timeout -s
  INT`, sonst hängt der Aufruf.
- **`pkill -f` trifft die eigene Shell**, wenn das Muster in der Befehlszeile des Aufrufs steht;
  Muster als `'[r]nsbote'` schreiben oder den Aufruf in eine Skriptdatei legen (D584).
- **Eine RNS-Instanz ist bereit**, wenn `@rns/<instance_name>` in `/proc/net/unix` steht; nie mit
  einem RNS-Programm prüfen (D589 Befund 1).
- **Diagnose am Boten:** eine Zeile beim Ablauf einer Frist mit Pfad, Status der Quittung und
  Laufzeit des Links; `loglevel = 6` in der Konfiguration der Instanz zeigt den Aufbau der Links
  (D591).
- **`.claude/settings.local.json` in Olis Klon** trägt seine Freigaben und die Deny-Regeln aus D592;
  sie ist über Olis globale Ignore-Liste ausgeblendet. Nie überschreiben; ändern nur mit einem
  Block, der das JSON einliest und eine Sicherung anlegt.
- **Gibt der Auto-Modus kein Urteil**, startet Oli `env CLAUDE_CODE_AUTO_MODE_SERVER=0 claude`.
- **fish:** `"(cmd)"` in Anführungszeichen wird nicht ersetzt; im Block zu D592 selbst noch einmal
  so geschrieben und vor der Ausführung nicht bemerkt. `test (… | count) -eq 0` statt `test -z`.

- **Aufträge mit Boten dauern.** Die Testreihe sechs bis acht Minuten, eine Rücknahmeprobe mit
  Boten bis zu einer Minute. Nach einer Probe `rnsd`, `tools.funk` und `symbolon.bote` beenden.
- **Der Kanal im Supervisor-Klon:** `tools/funk.py` mit einem Eingang je Teilnehmer; RNS sendet
  über `UDPInterface` aus einem neuen Socket je Paket (D610 Befund 1). Zum Messen zählt man im
  Kanal die Paketart aus dem ersten Byte und bei Daten den Kontext aus Byte 18.
- **RNS ruft Rückrufe mit Namen auf** (`Transport.py`, D611 Befund 1); ein Fehler darin wird still
  verschluckt.
- **`check_specs`** liest `§` in „RFC 6206 §4.2“ als baren Verweis; „Abschnitt 4.2“ schreiben.
- **Lange Läufe im Klon** in den Hintergrund legen und in Abständen unter 300 s nachsehen; ein
  einzelner Aufruf darf nicht länger laufen.

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
- Wer „das ist die Regel“ sagt, trennt die Regel des Protokolls von der Wahl einer
  Implementierung (D489).
- Eine Oberfläche wird an dem Satz gemessen, den ein Mensch nach dem Klick sagen kann; eine
  Abnahme der Seite braucht einen Durchlauf mit Oli (D490).
- Die Abnahme einer Seite liest auch, was sie zeigt und verbirgt, also die Stilregeln (D494).
- Was ein Mensch eintippt, bindet keine Rechnung an seine Schreibweise (D496).
- Die Fälle eines Beschlusses decken jede Rechenstelle und jeden Weg zur Stelle ab; der
  Supervisor prüft sie mit einer eigenen Probe gegen den naheliegenden Fehler, bevor der Auftrag
  hinausgeht (D501, D504, D512). **Geschärft aus D517:** eine Rücknahmeprobe, die ein Auftrag
  verlangt, fährt der Supervisor gegen den Test in der Fassung des Auftrags, nicht nur gegen die
  Implementierung.
- Aus D503: Wer ein Muster auf einen neuen Gegenstand überträgt, misst es dort; was für
  ganze Zahlen hält, bricht an Gleitkommazahlen.
- Aus D512: Ein Test, der Paare aus einer Datei liest, sieht nur, was die Datei
  ausdrücklich paart.
- **Neu aus D514:** Ein Weg, den ein Beschluss verworfen hat, wird im Code gesucht, bevor darauf
  gebaut wird; D473 hatte den Store beim Einlesen nicht ausgeschlossen, und der Code nahm ihn.
- Aus D518: Ein Ablauf, den ein Mensch Schritt für Schritt bedient, wird vorher selbst
  gefahren; die Reihenfolge ist Teil des Bildes.
- **Neu aus D527:** Ein neuer Posten in `offen.md` wird vorher gegen das Register gesucht, mit den
  Wörtern der Frage und den Namen, die er nennen will (schärft D514).
- **Neu aus D527:** Ein Hash in einem Block wird aus dem Spiegel kopiert, nie aus einem Kurzhash
  ergänzt (Schwester von D457). Einmal ergänzt, brach der Block an der Basis ab.
- **Neu aus D526:** Nimmt Code fremden Inhalt an, nennt der Auftrag den formwidrigen Fall (D474);
  diesmal fehlte er, und das Werkzeug fand die Lücke.
- **Neu aus D537:** Wer eine aufgezählte Menge der Spec ändert, sucht jede Aufzählung derselben
  Menge, Golden Anchors und Tests eingeschlossen (Schwester von D420). Übersehen hatte ich die
  Anker P-A bis P-H.
- **Neu aus D536:** Wirkt eine Regel an zwei Stellen, nimmt die Rücknahmeprobe sie an der Quelle
  zurück; an einer Stelle zurückgenommen, greift die andere, und die Probe bleibt grün.
- **Neu aus D539:** Ein Test an einer Schwelle prüft selbst, dass die richtige und die falsche
  Zählung auf verschiedenen Seiten der Schwelle liegen.
- **Neu aus D534, D539:** Eine Norm, die ein Ergebnis zurücknehmen kann, wird gegen die
  Invarianten gelesen, die es festhalten (`INV-04.7`); dort fehlte das widerrufbare Verdikt.
- **Neu aus D544, D545, geschärft aus D537:** Wer einen Satz ändert, sucht jede Stelle, die
  denselben Sachverhalt ausspricht, auch in anderer Form: eine Warnung und ihre Folgezeile, eine
  Regel und die Reihenfolge ihrer Prüfungen. Beide Nachträge zu `p27` kamen aus meinem Wortlaut.
- **Neu aus D548:** Ein Eigenschaftstest, den jede Regel einer Klasse von selbst erfüllt, schützt
  nicht; die Rücknahmeprobe zeigt es, wenn sie gegen ihn grün bleibt.
- **Neu aus D547, D548:** Eine neue Regel an einer Stelle der Auszählung wird an jeder Stelle
  gesucht, die dieselbe Menge selbst rechnet (Sicht, Vorschau, Karte); die Gruppierung aus D542
  hätte den aufgelösten Widerspruch weiter gezeigt.
- **Neu aus D556:** Ein Wortlaut, den Oli bestätigen soll, wird vorher gegen die Wortregeln der
  Seite gelesen; „Epoche“ war seit D494 „Fassung der Satzung“.
- **Neu aus D552:** Eine Meldung, die ein Bild nur einmal auslöst, braucht einen eigenen Test; das
  Bild sieht nicht, ob sie einmal oder jedes Mal käme.
- **Neu aus D555:** Eine Zählung als Golden Number schützt vor einer verschwundenen Gruppe von
  Fällen, die ein Test „alle grün“ nicht sieht.
- **Neu aus D557:** Eine Rücknahmeprobe nimmt die benannte Wirkung zurück, nicht eine benachbarte;
  sonst wird sie am falschen Test rot.
- **Neu aus D562:** Ein Befund wird dort im Code gesucht, wo sein Bild entsteht, bevor eine
  Reparatur entworfen wird; D502 nannte sein Bild im Titel, und D561 reparierte einen anderen Weg
  (schärft D514).
- **Zweimal verletzt, zur Übernahme vorgeschlagen (D557, D560):** Eine Rücknahmeprobe nimmt die
  benannte Wirkung zurück, nicht eine benachbarte. In D559 änderte K6 den Schlüssel der Zählung und
  damit die Titelsuche.
- **Neu aus D564 Befund 3:** Eine Aussage über Nebenläufigkeit wird an zwei Beobachtern geprüft, die
  dieselben Feststellungen in verschiedener Reihenfolge sehen.
- **Neu aus D569:** Ein Vektor für eine Ausnahme braucht einen Fall, den die Regel ohne die
  Ausnahme träfe; sonst bleibt die Rücknahmeprobe grün (Schwester von D548).
- **Neu aus D572:** Der Prototyp eines Auftrags fährt die Prüfungen von `make check` ganz, nicht nur
  die Tests.
- **Neu aus D572, zum dritten Mal verletzt:** Nimmt Code fremden Inhalt an, nennt der Auftrag den
  formwidrigen Fall (D474, D526).
- **Neu aus D573, zur Übernahme vorgeschlagen:** Grün ist ein Exit-Status, keine Ausgabezeile; eine
  gekürzte Ausgabe trägt nur, wenn der Status des gekürzten Befehls geprüft wird.
- **Neu aus D574, zur Übernahme vorgeschlagen:** Wer einen Begriff ausmustert, sucht jede Datei, die
  ihn trägt, über das ganze Repositorium (Schwester von D537).
- **Neu aus D575:** Ein neuer Begriff der Norm wird vorher im ganzen Repositorium und auf der Seite
  gesucht.
- **Neu aus D570:** Ein Hash in einem Block wird aus dem Spiegel kopiert; auch ich habe einmal einen
  Kurzhash ergänzt und es vor der Ausführung bemerkt (Schwester von D527).
- **Neu aus D578:** Wer eine Lücke mit einem Wert kodiert, prüft, ob dieser Wert im Format
  vorkommen kann (`None` für „Feld 3 fehlt“, aber CBOR kennt `null`).
- **Zum dritten Mal belegt, zur Übernahme vorgeschlagen (D582):** einen Ablauf vor dem Durchlauf
  selbst über die Schnittstelle fahren (D518, D580 Befund 2); wer eine Menge der Kette an einer
  zweiten Stelle rechnet, sucht jede solche Stelle (D547, D548, D577 Befund 1); einen Hash im Block
  nie aus einem Kurzhash ergänzen (D527, D570, D582).
- **Aus D577 Befund 2:** Wird eine Rücknahmeprobe vor der erwarteten Stelle rot, wird gelesen,
  warum; dort war es die Norm selbst (`UNKNOWN_PROPOSAL`), nicht ein Fehler des Tests.
- **Neu aus D587:** Eine Rücknahmeprobe nimmt die Wirkung in jeder Form zurück, in der man sie bauen
  kann, nicht nur in der Form des eigenen Prototyps; im `elif` des Werkzeugs sah der Test den Fehler
  nicht.
- **Neu aus D586:** Verlangt ein Auftrag „ohne Antwort → X“, stellt ein Test die fehlende Antwort
  her; der Bau verliess sich auf die Bibliothek, und die schloss die Anfrage nie ab.
- **Neu aus D589:** Eine Probe der Bereitschaft darf den Zustand nicht herstellen, den sie prüft.
- **Zum zweiten Mal belegt (D390, D590 Befund 1):** Eine Ursache, die in zwei Läufen „nicht mehr
  gesehen“ wurde, ist nicht bestätigt; D589 Befund 2 war falsch.
- **Neu aus D585 bis D591:** Ein Fehler in einer fremden Bibliothek wird im Quelltext der
  Bibliothek nachgelesen, bevor ein Test angepasst oder eine Umgehung gebaut wird (zwei Wettläufe
  in RNS, D586 Befund 3, D590 Befund 2).

- **Neu aus D610:** Ein Messwerkzeug wird gegen die Wirklichkeit geprüft, bevor seine Zahlen
  gelten; mein Kanal gab jedem Sender seine Pakete zurück, und zwei Registereinträge standen auf
  verfälschten Zahlen.
- **Neu aus D599, D601:** Eine Position wird vor dem Normtext an einem Prototyp gemessen; die
  Messung änderte das Patt von den zählenden auf die gebundenen Ja (D600).
- **Neu aus D603 Befund 2:** Ein Test, dessen Wächter an einer Aufgabe hängt, verliert ihn, wenn
  die Aufgabe entfällt; die Probe hat dann keinen Gegenstand mehr.
- **Neu aus D611 Befund 1, Schwester von D586 Befund 3:** Wer einer fremden Bibliothek einen
  Rückruf gibt, liest nach, wie sie ihn aufruft.
- **Neu aus D605, D606:** Eine richtige Aussage auf der Seite genügt nicht; sie muss dort stehen, wo
  ein Mensch hinsieht (Olis Anna-Satz).

## Offene Punkte

**17 offene Posten:** O97 (Phase 5, läuft), O100 (das Patt kostet Zeit), O101 (was ein Mensch
zuerst sieht) und 14 Wartestände: O31, O34 bis O40 und O42 vertagt mit Bedingung; O25
(Sicherungsblob) ein Bau ohne Anlass; O56 der PyPI-Name; O74 ein Stolperdraht; O89 (Amtswechsel der
Kasse); O90 (Negentropy, gehört zu O97).

**Aus `00cv`, ohne Auftrag:** Die Absicht `device-end` hat keine Folge und keine Warnung, die
Seite keinen Knopf (D596). Nach einer Spaltung mit Doppelstimmen bindet ein Ja auf einen
Sachantrag über Wahlgänge hinweg (`04 §8`, D600); Wahlgänge für Sachanträge sind nicht
durchgerechnet. Der Tab „Verlauf“ und der Zweck von „Im Verein“ (O101). Olis Feldtypen für die
Satzung, statt Freitext (Gründung, 00cv). Vor den T-Beams die Grenzen der Sendezeit auf 868 MHz
nach ETSI nachlesen; RNS kennt `airtime_limit_short` und `airtime_limit_long` (D609). Im Hörer des
Boten eine Bedingung, die nie eintritt (D612 Befund 1); im Docstring von `main` in `tools/netz.py`
eine Zeile über 100 Zeichen (D604 Befund 2). Die Zeile zu DORA in Olis Bild (D605 Befund 1).

**Aus O97, ohne Auftrag:** L2 (Entdeckung über Announces; der Bote fragt seine Nachbarn
nacheinander), L3 (Transportadresse und Identität), L4 und L5 (Grösse, der ganze Bestand je Runde;
O90), L6 (was eine knappe Runde zuerst schickt; `02 §7` will Widerrufe zuerst), L8 (Flut: keine
Stelle der Spec), L9 (Uhren), L10 (Aufnahme im Netz). LXMF oder rohe Links: Position rohe Links
(D583). Der eine Lauf von `--aufloesen`, in dem Anna sofort feststellte (D588 Befund 1). Warum
Pakete über die gemeinsame Instanz verloren gehen (D591 Befund 1); zwei Wettläufe in RNS (D586
Befund 3, D590 Befund 2), ob Oli sie meldet. `rnsd` läuft weiter, wenn `boten` nach seinem Start
scheitert; ein Lab mit einem Gerät hätte kein `--nachbar` (D590 Befund 4). Lärm beim Beenden
(D590 Befund 3). Ein Link, der nicht aktiv wird, wird nicht abgebaut (D586 Beschluss 4). L8 ist
mit Trickle gelöst (D611); L4 und L5 gemessen: je Holen die ganze Liste und je Eintrag eine Anfrage
(D609, D610). Der Bote fragt einen Nachbarn, der hinter ihm liegt, vergeblich, bis die Pause
wächst; der Stand sagt nicht, wer voraus ist (D611).

**Aus O96, weiter ohne Auftrag:** die Stichfrage des doppelten Ja je Feld (D564 Beschluss 3); Mengen
als Sachfelder (D565 Beschluss 4); ob Aufnahmen neben Sachfragen später laufen können (D564
Beschluss 1); `classify_all` läuft je Schritt der Kette zweimal (D572 Befund 3); Key `2` einer
Bürgschaft bleibt als `bond_ref` reserviert (D574).

**Aus `00ct`, ohne Auftrag (D581):** Der Typhinweis von `_vorgaenger` nennt nur `Proposal`; der
Docstring von `antragstitel` und der Kopfkommentar von `anzeige.js` nennen die Sachanträge nicht;
`verfassungsAenderungen` hat in `app.js` keinen Aufrufer mehr; die Geschichte der Demonstration
sagt „ANNA beantragt einen Satzungstext“, der Knopf heisst „Als Satzungsantrag …“. Ein Sachantrag
kann über die Seite kein Feld entfernen (`null`); die Schnittstelle kann es.

**Aus `00cr`, ohne Auftrag:** Die Kopfkommentare von `anzeige.js` und `selbsttest.js` nennen D559
und D561 nicht (D562 Bericht). Eine Feststellung, die selbst in einer Gabel steht, bekommt keinen
Satz; die Seite sieht nur Feststellungen aus `epoch_findings` der geltenden Kette (D559).

**Aus `00cq`, weiter ohne Auftrag:** Die Suche nach anderen Zustimmungen wiederholt die Filter von
`decide`; den Weg über ein Verdikt prüft kein Test (D556, D539). Bei einem Antrag ohne Zeile in
`proposals_view` sagt die Warnung allgemein „anderen Anträgen“ (D557 Beschluss 2). Annas Wartezeile
schlägt Namen ohne Rückfall nach (D553 Befund 1). Die Karte mit dem dritten Punkt steht nur einen
Takt oben (D554 Befund 2). Das gesperrte Gerät zeigt kein Bild (D556).

**Aus `00cp`, weiter ohne Auftrag:** Die kalte Wurzel und die übrigen Profile nach `I` (D534
Beschluss 2, D542 Beschluss 2). Die Aufnahme eines Geräts als Handlung im Netz (D542 Beschluss 3,
Phase 5). `04 §4.4`: ein ersetztes Ja blockiert weiter ein Ja auf einen anderen Antrag derselben
Epoche (D547 Beschluss 4); in O96 gilt das für Regel 1 weiter. Knoten verschiedener Fassung sehen
bei Key `1` verschiedene Epochen (D547 Befund 6).

**Aus `00co`, weiter ohne Auftrag:** Eine Bürgschaft **auf** einen Geräteschlüssel bleibt beim
Gerät (D535). Die Zurechnung geht je Anfrage die Kette entlang (D538 Befund 2). Der Beispielverein
führt `verdict@1` nicht im Boden (D539). Eine Wurzel, die ihre eigene Aufnahme bestätigt, nimmt sich
jede Aufnahme (D538 Befund 1).

**Aus `00cn`:** Der Antrag im Takt 2 prüft die Spitzen nicht (D522).

**Kleine Befunde an der Seite:** der Stiltest sieht geerbte Farben nicht (D512); ob eine Bürgschaft
Vertrauen weitergibt, als Folgezeile (D495); der Zugang vom Telefon (D481 Befund 3); Chrome
ungeprüft (D484).

**Aus dem Netz:** ein zweites Strg-C beim Beenden von `tools.netz` druckt einen Traceback (D519).
Die Uhr jedes Knotens beginnt bei jedem Start bei 1000 (D518, L9). Fremde Bytes zur angefragten
`claim_id` verfälschen den Bestand nicht, eine Runde konvergiert dann nur nie (D516, D583 L7).

**Aus D408:** Die Zahl der Auswertungen über ein Fenster hat keine Obergrenze; beisst es je, gehört
die Grenze nach `02 §8`.

**Aus der Aussprache mit Oli, für später:** eigene Währung als Kreditgeld über `unit_ref`
(`03 §3.3`), Olis Versicherungsbild mit kleinem Topf und verteilter Verwahrung, Signaturen mit
Schlüsselpreisgabe nur in Sonderfällen (D467), der Weg zurück nach einer Gabelung mit neuem
Schlüssel als eigenes Szenario (D489). Kandidaten nach Phase 5. Ob ein Beitrag von 0 Cent sinnvoll
ist, fragt `03 §3.3` (D503).
