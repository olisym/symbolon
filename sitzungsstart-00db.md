# Sitzungsstart: 00db (MaR / symbolon), fortgeschrieben nach D643

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
  einem geteilten Kanal im Userspace statt `netem` (D607). Gebaut: Trickle und Fristen nach
  Bitrate (D611, D612), das Bündel (D614 bis D616), der Abgleich nach Bereichen (D617, D618, O90
  erledigt) und die Zahl der Einträge in der Ankündigung (D619, D620). In `00cx`: der Rundruf
  gemessen und vertagt (D622, O103), der Stillstand behoben (D623 bis D626), die Streuung ohne
  Stillstand gemessen (D627). In `00cy`: die zweite Bestandsaufnahme zu Reticulum (D629), der
  einseitige Link gemessen und repariert (D630 bis D632), die Sendezeit je Gerät (D630), IFAC am
  Kanal (D633). In `00cz`: der Rundruf an der Quelle gemessen, gebaut und angenommen (D635 bis
  D638, O103 erledigt); ein Wahlgang kostet rund ein Drittel der Sendezeit. Stufe 4 ruht damit.
  (5) Funk über Olis T-Beams; die Hardware fehlt, und der Funk ist zurückgestellt (D639). Es
  bleibt nur das Band 869,4 bis 869,65 MHz mit 10 % (D630 Beschluss 3), mit IFAC am
  Funk-Interface (D629 Beschluss 1).
- **Governance nebenbei:** Wahlgänge mit Patt in Norm, Bibliothek und Knoten (O98 erledigt, D594
  bis D604). Die Seite sagt, wenn eine Abstimmung vorbei ist (D605, D606).
- **Die Gründung (O101, D640 bis D643):** Bestandsaufnahme gefahren; drei gründen gemeinsam am
  Tisch, alle drei sind Anker; der Schlüssel reist per Scan, die Einladung aus der Ferne kommt
  danach. Vier Schritte (D641 Beschluss 1): (1) der Weg im Knoten, gebaut (`POST /gruenden`,
  D641, D642); (2) die Bildschirme auf einem Knoten, **als Nächstes**; (3) der Scan mit Schlüssel
  und Adresse, dazu der Knoten am Telefon; (4) der Knoten hält nur eigene Scopes. Das zweite
  Beispiel ist die Verabredung zu zweit (D640 Beschluss 3). Der Verlust eines Schlüssels bleibt
  ein eigener Strang (D640 Beschluss 5). Kryptografische Werkzeuge nicht auf Vorrat. Die T-Beams,
  wenn die Hardware da ist. O102 ist entschieden: IFAC, als Regel des Betriebs (D629).
- **Grundsatz (D617 Beschluss 1):** Reticulum macht das Netz, der Bote trägt nur, was ein Verein
  weiss. Was Reticulum kann, baut MaR nicht nach.

## Stand

Am Ende von `00da`: **1582 Tests**, darin der Selbsttest der Seite mit **241 Fällen**, Register
**D1–D643**, Prüfregeln **1–83**, `make check` grün, `main` beim Commit, der diesen Sitzungsstart
trägt. **35 Wurzel-Markdown-Dateien, alle gebunden**; `archiv/` steht bei 164 mit
`sitzungsstart-00da.md`. `offen.md` führt **104 Posten**, davon **17 offen**: die 13 Wartestände,
O97, O100, O101 und O104.

`rns 1.5.4` ist Teil von `dev` (D584 Beschluss 4). `make check` braucht es, wie es Node braucht.
Die Testreihe dauert fünf bis neun Minuten; die Tests mit Boten warten auf die erste Ankündigung
nach Trickle (D612 Befund 2).

## Was in dieser Sitzung geschah

- **D640 — die Bestandsaufnahme.** Eine Gründung über die Schnittstelle auf einem frischen Knoten:
  nach Satzung und Genesis trägt alles, was die Seite kennt. Sie bricht davor ab: der leere Knoten
  ist eine Sackgasse, ein totgeborener Verein wird angenommen, die Seite kennt genau einen Verein,
  und wie ein Schlüssel von Mensch zu Mensch kommt, fehlt. Nachgeschlagen: Briar, Keybase und
  `@localfirst/auth`, Aragon, KERI, Dark Crystal. Oli: drei am Tisch, erst der Scan, das zweite
  Beispiel zu zweit. Die Leiter der kleinsten Einheiten (Befund 11).
- **Das Bild:** acht Bildschirme als Standbild, `https://claude.ai/artifact/3ZmMDq9ZTQx1z1xa2rckSo`.
  Oli: gut so, der Scan ist die Geste.
- **D641, D642 — `p52-gruenden`.** `symbolon/node/gruendung.py` mit der Vorlage `verein`, dem
  Probelauf und der Route `POST /gruenden`; 28 Tests, zehn Proben, im ersten Durchgang angenommen.
  Zu dritt braucht ein Satzungsfeld alle drei Stimmen (D641 Befund 2).
- **D643 — Schluss.** Playwright läuft im Klon; die Seite ist zum ersten Mal gerendert gesehen.

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
- **Was automatisch laufen kann, läuft vorher** (D643 Beschluss 1): der Supervisor klickt die
  Seite mit Playwright durch, ein Context je Person, und liest die Bildschirmfotos. Oli bekommt
  einen Durchlauf erst, wenn die Frage ist, ob ein Mensch es benutzen kann.
- **Nachschlagen, bevor eine Position steht,** wo andere seit Jahren an derselben Frage arbeiten
  (D640); gelesen sind dann Auszüge, vor einem Normtext die Quelle ganz.
- **Kein Auftrag verlangt einen Push**, und die Deny-Regeln aus D592 verbieten ihn dem Werkzeug.
- **Das Werkzeug darf auch Cursor sein** (D606 Befund 1). Die Deny-Regeln aus D592 gelten dort
  nicht; die Abnahme liest ohnehin den Diff.
- **Last von unten aufbauen.** Nach zwei erfolglosen Anläufen am selben Symptom erst zwei, dann
  drei, dann fünf Geräte, mit einer Zählung je Paketart (D610).
- **Oli misst die Seite mit einem Satz:** was er als Anna denkt (D605, D606).
- **Ein Schritt am Boten wird über Funk gemessen, vor dem Auftrag und vor der Abnahme:**
  `--wahlgang --funk` bei 1200 bit/s, mit Zählung je Paketart im Kanal und einer Zeile je Abgleich
  (D617, D619). Ein Nutzen, den ein Schritt behauptet, wird vorher gemessen (D619 Befund 1).
- **`make check` des Prototyps zweimal, wenn ein Lab-Test einmal rot war,** und `main` daneben unter
  gleicher Last (D617 Befund 8).
- **Ein Lauf über Funk mit Wächter.** Ein Prozess fragt alle 10 s `/peer/bestand` und `/stand` jedes
  Geräts ab; so sieht man, wer zurückliegt und wie lange (D623). Diagnosezeilen je Anfrage (Grund,
  Dauer, Sendungen, Laufzeit) und je Ankündigung zeigen, warum (D623 Befund 2, D625).
- **Lange Messungen gehen als Messpaket an Claude Code in der Cloud** (D627 Beschluss 2): Auftrag,
  Diagnose-Patch und Skripte in `messung/`, mit `git add` vorgemerkt, dann
  `env CCR_FORCE_BUNDLE=1 claude --cloud "…"`; danach `messung/` wieder entfernen. Kein Commit, kein
  Push; der Auftrag schliesst `AGENTS.md` §5 ausdrücklich aus. Gedeutet wird im Supervisor-Chat.
- **Der Massstab eines Schritts am Boten ist die Lebendigkeit, nicht die Zeit** (D623 Beschluss 4).
  Die Zeiten streuen so stark, dass ein Lauf je Fassung nichts zeigt; ein Stillstand schon.
- **Vor einer Messung steht, was bei welchem Ergebnis geschieht** (D630). Rechnet die Regel hoch,
  nennt sie die Annahme der Hochrechnung (D630 Beschluss 4 und 6).
- **Ein seltener Fall wird für die Messung erzwungen** (D631): der Kanal verwarf jedes dritte
  `LRRTT`, so zeigte ein Lauf je Fassung den Unterschied zwischen `main` und Prototyp.
- **Eine Entscheidung für Oli nennt, was ein Mensch davon sieht, was sie kostet und wie fest sie
  ist** (`00cy`, O102); „(a) oder (b)“ ohne das war keine Grundlage.
- **Ein Auftrag, dessen Basis erst bei Oli entsteht,** prüft Branch, Commit-Nachricht und den Hash
  des Registers statt eines Commit-Hashes (D631, `p50`).
- **Eine Frage aus dem Sitzungsstart wird an der Einheit der Kosten gemessen,** bevor zwischen den
  dort genannten Wegen gewählt wird; D634 fragte nach zwei Wegen, der dritte trug (D635 Befund 3).
- **Der Prototyp entsteht in der Form des Auftrags** und fährt denselben Lauf über Funk, den der
  Supervisor vor der Abnahme auf dem Branch wiederholt (D636 Befund 3, D637 Befund 3).
- **Zahlen für Oli werden bis zum selben Schnitt gezählt** wie die Zahlen daneben (D635 Befund 8).


## Der nächste Schritt

**Schritt 2 der Gründung: die Bildschirme auf einem Knoten (D641 Beschluss 1, D643 Beschluss 3
und 4).** Heute zeigt der leere Knoten nach dem Schlüssel „Kein Verein.“ und die Geschichte der
Demonstration.

- Zuerst ganz lesen: `symbolon/node/static/app.js`, `anzeige.js`, `geraet.js`, `selbsttest.js`,
  `style.css`; `tests/node/test_selbsttest.py` und `test_stil.py`; D494 und D556 zu den Wortregeln
  der Seite; das Bild (acht Bildschirme) und D643 Beschluss 3.
- Dann der Prototyp im Klon gegen den echten Knoten: gründen aus der Vorlage mit Mitgründern aus
  dem Adressbuch, `/gruenden` und die eigene `accept-rules` in einem Zug, Brunos Bildschirm ohne
  Einladenden, „In Gründung“ und „Der Verein besteht“, die Geschichte nur mit simulierten
  Personen. Felder als Text.
- Mit drei Contexts in Playwright durchklicken und die Bildschirmfotos lesen, bevor der Auftrag
  hinausgeht. Der Auftrag nennt die neue Zahl `_FAELLE`.
- Danach Olis Durchlauf in drei Containern oder Profilen (D490, D643 Beschluss 2).

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
Ein Takt dauert Minuten (D611 Befund 3). Olis Verzeichnisse aus `00cw`: `wahlgang1`, `spalt2`,
`spalt3`, `ausweg1`, `funk1`, soweit gefahren; ein neuer Lauf braucht ein neues. Gemessen wird bei
1200 bit/s: ein kleines Skript setzt `tools.netz.FUNK_BITRATE = 1200` und ruft `main` mit
`--wahlgang --funk` (so im Messpaket aus D627).


**Der Rundruf im Lab:** jede Geschichte mit `--reticulum` oder `--funk` zeigt seit D636 Zeilen
der Form „Gerät ← Nachbar: rundruf geholt=1 abgewiesen={}“; ein Holen kommt nur noch, wo ein
Rundruf fehlte.

**Eine Gründung über die Schnittstelle** (D641): auf einem frischen Knoten `POST /gruenden` mit
`vorlage` „verein“, `gruender` (drei Schlüssel als Hex) und `felder` (`name`, `sitz`, `zweck`,
dazu `beitrag`); danach je Gründer `accept-rules`. Die Seite kann es noch nicht.

## Werkzeugnotizen

- **Playwright im Supervisor-Klon:** `pip install --break-system-packages playwright`, dann
  `python3 -m playwright install firefox`. Je Person `browser.new_context(viewport=…)`; der Knoten
  startet davor in einem eigenen Aufruf. `page.on("pageerror", …)` sammelt Fehler der Seite.
- **Für Olis Durchlauf mit mehreren Personen:** Firefox Multi-Account Containers, ein Container
  je Person; mit unserer Seite noch nicht ausprobiert (D643).
- **Ein Prototyp mit neuen Dateien** braucht `git add` vor `check-tree`, sonst ist das Ziel rot.
- **Der Auftrag liegt ausserhalb des Repositoriums** in `~/auftraege`, die Tests als Diff
  daneben; der Block legt beide ab und schiebt Älteres nach `erledigt/`.

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
- **Ein Lauf im Hintergrund überlebt das Ende eines Zuges nicht** (f2 in `00cx`). Jeder Lauf beginnt
  und endet im selben Zug: rund 10 Minuten für `--wahlgang --funk` bis zum ersten Urteil.
- **Vor jedem Lauf aufräumen.** Zweimal belegten die Knoten eines noch laufenden Laufs die Ports,
  der neue lief ohne Takt 0 (d2, f1). Das Startskript ruft zuerst das Aufräumskript.
- **`pkill -f` traf die eigene Shell fünfmal in `00cx`,** jedes Mal, weil ein Pfad wie
  `symbolon/bote/…` in derselben Befehlszeile stand wie der Aufruf des Aufräumskripts (auch über
  ein Startskript, das aufräumt). Aufräumen und Starten nur in Aufrufen ohne solchen Pfad.
- **Das Messpaket aus D627** (`lauf.sh`, `stopp.sh`, `mess.py`, `waechter.py`, `auswert.py`,
  `diag.patch`, `AUFTRAG.md`) ist die Vorlage für die nächste Messung; der Patch muss zur Basis
  passen.
- **Das Messpaket aus D630** kam als `messung.tar.gz`: der Kanal schreibt eine Zeile je Paket
  (Sender, Art aus `daten[0] & 0b11`, Ziel aus Byte 2 bis 17, Kontext aus Byte 18, wer es hörte,
  Sendezeit, Stau), der Bote Zeilen je Link über Haken an `RNS.Link` (`validate_request`,
  `rtt_packet`, `handle_request`, `link_closed`). `auswert.py` verbindet beides über die Kennung
  des Links. Es liegt in keinem Repositorium; die nächste Messung baut es neu.
- **Mit IFAC ist der Kopf maskiert:** Art, Ziel und Kontext liest der Kanal dann nicht, und
  `Kanal.senden` zählt die Ankündigungen falsch (D633 Befund 5).
- **Ein Start im Hintergrund** geht im Supervisor-Klon nur als eigener Aufruf, mit `< /dev/null`
  und `timeout 10` davor; im selben Aufruf mit anderem hängt er bis zum Zeitlimit (`00cy`).
- **`pgrep -f` mit `symbolon` im Muster** findet die eigene Shell, wenn sie in
  `/home/claude/symbolon` wechselt; ein Rest von einem Prozess ist dann keiner.
- **Zwei Fassungen nebeneinander** über `git worktree add /tmp/<name> <commit>`, den Patch je Baum
  mit einem kleinen Skript; danach `git worktree remove --force`.
- **`ruff` fehlt im frischen Supervisor-Klon;** `pip install --break-system-packages ruff`, dann
  `python3 -m ruff check symbolon tests tools` statt des Ziels `check-lint`.
- **IFAC in der Konfiguration eines Interfaces:** `network_name`, `passphrase`, `ifac_size = 64`
  (Bit; 8 Byte wie am RNode). Das gilt für jedes Interface, auch `UDPInterface` (D633).

- **`rns` im Supervisor-Klon festlegen:** `pip install --break-system-packages 'rns==1.5.4'`; ohne
  Version kam 1.5.6 (`00cz`).
- **`make PY=python3 check` scheitert im Klon am Lint-Ziel** (`.venv/bin/ruff`). Stattdessen
  `make PY=python3 test`, `python3 -m ruff check symbolon tests tools` und die vier
  Markdown-Ziele einzeln.
- **Die Ausgabe von `make` in eine Datei, den Status aus `$?`.** Hinter `| tail` stand in `00cz`
  einmal ein rotes `check-specs`, und die letzte Zeile sah grün aus (D573).
- **Das Messpaket aus D635** liegt in keinem Repositorium: der Kanal schreibt je Paket Zeit,
  Sender, Länge, Art, Ziel und Kontext; der Bote je Anfrage die Kennung des Links und den Pfad;
  die Auswertung ordnet jedes Paket an eine Link-Kennung der letzten Anfrage auf diesem Link zu.
  Geschnitten wird am fünften „gleicher Stand“ (Takte 0 bis 4).
- **Ein Lauf über Funk im Klon** braucht drei Aufrufe: starten (allein), in Abständen unter 300 s
  nachsehen, auswerten. Im selben Aufruf mit anderem hing der Start wieder; ein Lauf über das
  Zugende hinaus war wieder verloren (`00cz`, je zum zweiten Mal).
- **Testdaten für eine Grösse im Bündel** müssen sich nicht packen lassen; 400 gleiche Bytes
  wurden zu 48 (`00cz`).
- **Der Knoten antwortet beim Einliefern** mit `claim_id` und `hash`; `/stand` antwortet dem
  Verhalten nach auch, wenn der Knoten getrennt ist, `/peer/bestand` nicht (D636 Befund 2).
- **Eine Zeile über 100 Zeichen im Registeranhang** findet `check_specs` erst nach dem Anhängen;
  den Anhang im Klon an das Register hängen und die vier Markdown-Ziele fahren, bevor er hinausgeht.

## Prüfregel-Kandidaten, weiter nicht übernommen

- **Zum zweiten Mal belegt (D637, D642 Befund 4):** Sagt ein Auftrag, was bei einer Ausnahme
  geschieht, nennt er jede Stelle, an der sie auftreten kann.
- **Neu aus D641 Befund 1:** Wer zwei Objekte aus denselben Angaben baut, prüft, ob zwei Aufrufe
  mit verschiedener Absicht dasselbe Objekt ergeben.
- **Neu aus D641 Befund 2:** Eine Schwelle aus einem Bild wird an der kleinsten Gruppe gemessen,
  bevor sie in eine Vorlage geht; zwei Drittel sind zu dritt alle.
- **Neu aus D640 Beschluss 4:** Eine Aussage aus einem früheren Gespräch, die nicht im Register
  steht, wird beim Wiederaufgreifen gegen die Norm geprüft; „ein Genesis mit Lücken“ war falsch.

- **Neu aus D637:** Sagt ein Auftrag, was bei einer Ausnahme geschieht, nennt er jede Stelle, an
  der sie auftreten kann (Schwester von D586).
- **Neu aus D635 Befund 5:** Ein Prototyp, der auf einen Zustand einer fremden Bibliothek baut
  (ein bekannter Schlüssel), wird ab dem kalten Start gemessen.
- **Neu aus D635 Befund 8:** Zahlen aus einem Lauf werden alle bis zum selben Schnitt gezählt.
- **Neu aus `00cz`, Prüfregel 27 verletzt:** ein Verweis im Entwurf zu D636 zeigte auf den falschen
  Beschluss (D615 Beschluss 2); vor der Lieferung beim Öffnen bemerkt.
- **Zum zweiten Mal belegt (D573, `00cz`):** Grün ist ein Exit-Status, keine Ausgabezeile.

- **Neu aus D629:** Eine Eigenschaft einer fremden Bibliothek, die nur im Quelltext steht und nicht
  in ihrer Dokumentation, wird als solche benannt; sie kann sich ohne Ankündigung ändern.
- **Neu aus D630:** Eine Entscheidungsregel, die eine Messung hochrechnet, nennt die Annahme der
  Hochrechnung, bevor gemessen wird.
- **Neu aus D630:** Ein Beschluss, der einen früheren wieder öffnet, sagt das; D629 Beschluss 4
  öffnete D627 Beschluss 1, ohne ihn zu nennen.
- **Neu aus `00cy`:** Eine Vermutung über eine fremde Bibliothek wird zu Ende gelesen, bevor sie
  ausgesprochen wird; „eine verlorene kleine Antwort bleibt unbemerkt“ war falsch, weil der Status
  einer Anfrage als Paket `SENT` bleibt.
- **Neu aus `00cy`:** Eine Zahl in einem Registereintrag wird gegen die Ausgabe nachgerechnet;
  „71 kamen an“ waren 68.
- **Neu aus D623:** Ein Befund, der einer Fassung einen Fehler zuschreibt, wird gegen dieselbe
  Messung auf `main` geprüft; der Stillstand von (a) in D622 kam aus `main` selbst.
- **Neu aus D623, D625:** Ein Lauf, dessen Prozesse mit einem anderen überlappen, zählt nicht; vor
  der Auswertung prüfen, dass Takt 0 überhaupt lief.
- **Neu aus D625:** Eine Frist, die an einem Ort bemessen wurde (lokal), wird am neuen Ort gemessen,
  bevor sie dort gilt (Schwester von D503).
- **Neu aus D628:** Eine Aussage über eine fremde Bibliothek („`GROUP` statt `SINGLE`“) wird im
  Quelltext geprüft, bevor sie Oli zur Entscheidung vorgelegt wird (schärft D585 bis D591).
- **Zum dritten Mal belegt, aus `00cx`:** ein Hash im Block wird aus dem Spiegel kopiert, nie
  ergänzt; im Block zu D623 noch einmal ergänzt und erst in der Antwort bemerkt.

- **Neu aus D615 Befund 1:** Ein Auftrag nennt auch den Grenzfall einer Ausgabe (die gekürzte
  Datei), nicht nur den formwidrigen Eingang (Schwester von D474).
- **Neu aus D615 Befund 2:** Ein Test, der eine Lesart nahelegt (`Formwidrig` ist ein `ValueError`),
  wird so gebaut; was gefangen wird, sagt der Auftrag ausdrücklich.
- **Neu aus D617:** Eine Zahl im Docstring eines Tests wird gemessen, nicht aus einem früheren
  Prototyp übernommen; „neun Runden“ waren fünf (Schwester von D457).
- **Neu aus D618 Befund 2:** Eine Abweichung, die die Form erlaubt, bleibt eine Abweichung vom
  Wortlaut des Beschlusses; die Abnahme schreibt sie ins Register.
- **Neu aus D619 Befund 1:** Ein Schritt, dessen Nutzen ich begründet habe, wird gemessen, bevor er
  gebaut wird; die Anregung durch den Nachbarn fiel weg.
- **Neu aus D620 Befund 3:** Ein Prüfkriterium per `grep` ist so eng wie die Sache.
- **Neu aus `00cw`:** Eine Annahme über Sicherheit (der Inhalt sei verschlüsselt) wird gegen Spec
  und Code geprüft, bevor auf ihr gebaut wird.

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

**17 offene Posten:** O97 (Phase 5, ruht bis zu den T-Beams), O100 (das Patt kostet Zeit), O101
(was ein Mensch zuerst sieht), O104 (Anfragen über den Link scheitern unter Verlust; der einseitige
Link ist repariert, offen sind die gehäuft scheiternden Aufbauten) und 13 Wartestände: O31, O34 bis
O40 und O42 vertagt mit Bedingung; O25 (Sicherungsblob) ein Bau ohne Anlass; O56 der PyPI-Name; O74
ein Stolperdraht; O89 (Amtswechsel der Kasse).

**Aus `00da`, ohne Auftrag:** Die Seite nimmt den ersten Verein nach Hash, und `/peer/objects`
nimmt jedes Genesis an (D640 Befund 8; Schritt 4). Genesis vor der Satzung lässt eine blinde
Bestätigung zu (D640 Befund 5). Schwellen und Schiedsleute weist die Schnittstelle als
`RESERVED_FIELD` ab (D640 Befund 6). Ein Gründer muss kein gültiger Schlüssel sein; eine
formwidrige Vorlage kann Status 500 liefern (D642 Befund 4 und 5). Der Probelauf prüft
`epoch_findings` nicht (D642 Befund 2). Die Feldtypen, Kandidat CDDL, nicht nachgeschlagen (D641
Beschluss 6). `00 §6.1` zu `rotate-key@1` lesen, bevor zum Schlüsselverlust eine Position steht
(D640 Beschluss 5). Ob ein Scope ohne eingetragene Schiedsleute zulässig ist, und Schuld und
Quittung zu zweit ohne Verein daneben (D640 Befund 11). NFC-Tags mit eigenem Schlüssel und der
Versuch mit Termux (D641 Beschluss 7). Verdeckte Wahl und Los (D640 Beschluss 6). Die Mindestzahl
beim nicht eingetragenen Verein und die geschichtlichen Beispiele sind nicht nachgeschlagen.

**Aus `00cz`, ohne Auftrag:** Rundruf und IFAC zusammen und der Rundruf unter Kollisionen, beides
mit den T-Beams (D636 Beschluss 7). Ein wiederholt abgespielter Rundruf zählt gegen die Grenze
seines Absenders. Dass der Hörer das Nachholen ruft, prüft kein Test. Ein Eintrag über 384 Byte im
Bündel geht nie als Rundruf (zwei je Wahlgang). Weniger Runden im Abgleich bleibt der kleinere
Hebel (D636 Beschluss 6). Im Lauf auf dem Branch 14 statt 15 Rundrufe, nicht untersucht (D637
Befund 3). In `kern.py` und `reticulum.py` drei ältere Zeilen über 100 Zeichen.

**Aus `00cy`, ohne Auftrag:** Von 107 Linkanfragen kamen 11 nicht an, mehr als 5 % Verlust erwarten
lassen (D630 Befund 2). Nach zwei neuen Links bleiben der dritten Anfrage rund 30 s; eine kürzere
Zustellfrist für frische Links wartet auf einen Anlass (D631 Beschluss 3, D632 Befund 3). Ob Oli
das unquittierte `LRRTT` bei Reticulum meldet (D631 Beschluss 4). `Kanal.senden` zählt mit IFAC die
Ankündigungen falsch (D633 Befund 5). Die Anleitung zu den T-Beams braucht die drei Zeilen für IFAC
und `airtime_limit_long = 10` (D630 Beschluss 3, D633 Beschluss 2). Der simulierte Kanal war zu 61
bis 71 % belegt und kennt keine Kollisionen (D630 Beschluss 5). Ein Wechsel der Passphrase macht ein
Gerät, das ihn verpasst, am Funk taub; der Rückweg ist ein anderes Interface (D629 Befund 4).

**Aus `00cx`, ohne Auftrag:** Im Docstring von `Trickle.ankuendigen` meint „darin“ das abgelaufene
Intervall (D624 Befund 2). Ein Gerät lag in einzelnen Läufen 100 bis 190 s länger zurück als die
übrigen (D624, D626, D627; die Fälle an der Antwortfrist erklärt D630). `AGENTS.md` §5
verlangt einen Commit auch von einem Messauftrag (D627 Befund 4). Der simulierte Kanal modelliert
weder Halbduplex noch Kollisionen (D627 Beschluss 1).

**Aus `00cw`, ohne Auftrag:** `_auf_ids` in `rbsr.py` rechnet bei Tausenden fehlender Einträge in
einem Bereich quadratisch; im Docstring von `holen` steht der Verweis auf D615 Beschluss 2 am
falschen Satz (D618 Befund 3). Grosse Differenzen bleiben die schwache Stelle des Abgleichs (D617
Befund 8). `test_boten_sperren` einmal rot unter Last, Ursache nicht bestätigt (D617 Befund 8). Der
Pfad `bestand` dient nur noch Diagnose und Tests (D617 Beschluss 5). Die Zeiten bis zum gleichen
Stand streuen zwischen Läufen stark (384 s bis 667 s auf derselben Fassung).

**Aus `00cv`, ohne Auftrag:** Die Absicht `device-end` hat keine Folge und keine Warnung, die
Seite keinen Knopf (D596). Nach einer Spaltung mit Doppelstimmen bindet ein Ja auf einen
Sachantrag über Wahlgänge hinweg (`04 §8`, D600); Wahlgänge für Sachanträge sind nicht
durchgerechnet. Der Tab „Verlauf“ und der Zweck von „Im Verein“ (O101). Olis Feldtypen für die
Satzung, statt Freitext (Gründung, 00cv). Vor den T-Beams die Grenzen der Sendezeit auf 868 MHz
nach ETSI nachlesen; RNS kennt `airtime_limit_short` und `airtime_limit_long` (D609). Im Hörer des
Boten eine Bedingung, die nie eintritt (D612 Befund 1); im Docstring von `main` in `tools/netz.py`
eine Zeile über 100 Zeichen (D604 Befund 2). Die Zeile zu DORA in Olis Bild (D605 Befund 1).

**Aus O97, ohne Auftrag:** L2 (Entdeckung über Announces; der Bote fragt seine Nachbarn
nacheinander), L3 (Transportadresse und Identität), L6 (was eine knappe Runde zuerst schickt; `02
§7` will Widerrufe zuerst), L8 (Flut: keine Stelle der Spec), L9 (Uhren), L10 (Aufnahme im Netz).
LXMF oder rohe Links: Position rohe Links (D583). Der eine Lauf von `--aufloesen`, in dem Anna
sofort feststellte (D588 Befund 1). Warum Pakete über die gemeinsame Instanz verloren gehen (D591
Befund 1); zwei Wettläufe in RNS (D586 Befund 3, D590 Befund 2), ob Oli sie meldet. `rnsd` läuft
weiter, wenn `boten` nach seinem Start scheitert; ein Lab mit einem Gerät hätte kein `--nachbar`
(D590 Befund 4). Lärm beim Beenden (D590 Befund 3). Ein Link, der nicht aktiv wird, wird nicht
abgebaut (D586 Beschluss 4). L8 ist mit Trickle gelöst (D611), L4 und L5 mit Bündel und Abgleich
nach Bereichen (D614, D617); wer voraus ist, sagt die Zahl in der Ankündigung (D619).

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
