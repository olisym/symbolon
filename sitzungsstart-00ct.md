# Sitzungsstart: 00ct (MaR / symbolon), fortgeschrieben nach D576

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

- Phase 0 bis 4: abgeschlossen (D466 bis D526).
- **Mehrere Geräte einer Person:** gelöst und gebaut (O92, O94, D529 bis D546).
- **Lücken zwischen Norm und Bau** (D555): alle drei Stufen erledigt (D555 bis D563).
- **O96, mehrere Anträge nebeneinander:** Norm, Golden Anchors und Governance-Code stehen (D567 bis
  D573); die Wörter der Seite sind entschieden (D575). Es fehlen der Knoten und die Seite.
- Phase 5: Reticulum.

## Stand

Am Ende von `00cs`: **1264 Tests**, darin der Selbsttest der Seite mit **222 Fällen**, Register
**D1–D576**, Prüfregeln **1–83**, `make check` grün, `main` beim Commit, der diesen Sitzungsstart
trägt. **35 Wurzel-Markdown-Dateien, alle gebunden**; `archiv/` steht bei 156 mit
`sitzungsstart-00cs.md`. `offen.md` führt **96 Posten**, davon **15 offen**: 14 Wartestände mit
Bedingung und O96.

## Was in dieser Sitzung geschah

- **D567 — der Normtext zu Sachanträgen.** `04 §1.1` Regelfelder, `§2.4` Feld 3 (`S`), `§2.5` das
  Objekt `motion`, `§3.4` Klasse `ordinary` und die Klasse eines Vorschlags gegen den Stand aus `S`,
  `§3.5` die neuen Prüfungen, `§4.1` Bedingung 7, `§4.4` die drei Regeln mit B1 bis B5 in einer
  Rechnung, `§4.6` der Stand einer Epoche; `03 §4`: `accept-rules` bindet an den Epochenbeginn.
- **D568 — Golden Anchors `GV-59` bis `GV-91`, `INV-04.9` bis `INV-04.11`.** Die Vektoren stehen in
  Epoche 1, weil nur dort `membership` und `amendment` verschieden viele Ja brauchen. Zwei falsche
  Kurzhashes in der Anchor-Datei korrigiert.
- **D569, D570 — `p32-sachantraege`:** Objekte, Formprüfung, Auszählung, die drei Regeln, Klasse,
  Bedingung 7. Ohne Nachtrag abgenommen. Befund an meinem Auftrag: `GV-68` sah seine Regel nicht,
  vor dem Auftrag gefunden.
- **D571 bis D573 — `p33-fassung` mit Nachtrag `p33b-scope`:** Kette mit Sachanträgen, Stand,
  Invarianten erschöpfend. Nachtrag: ein Objekt mit fremdem `scope` brachte die Kette zum Werfen,
  jetzt übergangen; zwei bare Verweise, einer aus meinem Testkopf. Der Bericht nannte `make check`
  grün, weil `make` ein Alias mit `-j4` war und `| tail` den Status verschluckte; `AGENTS.md §4`
  sagt jetzt, grün heisst Exit-Status 0 von `make`.
- **D574 — Nachtrag zu D467:** `08` trug den Bond an drei Stellen ohne Vorbehalt, gefunden in einem
  anderen Gespräch, im Spiegel nachgeprüft, mit vollständiger Suche über das Repositorium.
- **D575 — die Wörter.** Oli: Satzungsantrag, Sachantrag, Beschluss, „die 3. Fassung der Satzung“,
  Stand. Die Norm sagt jetzt „Stand“ statt „Fassung“ (`resolve_stand`, `stand_obj`); der Code heisst
  noch `resolve_fassung`.
- **D576 — Schluss der Sitzung.**

## Arbeitsweise, bestätigt

- **Prototyp vor dem Auftrag, Tests wörtlich im Auftrag, Rücknahmeproben vorher gegen diese
  Fassung.** Neu: der Prototyp fährt die Prüfungen von `make check` ganz, auch `check_specs` über
  die Python-Dateien (D572 Befund 4), und ein Vektor für eine Ausnahme braucht einen Fall, den die
  Regel ohne die Ausnahme träfe (D569 Befund 1).
- **Ein Nachtrag auf demselben Branch** trägt Registereintrag und Spec-Satz auf dem Branch; der
  Merge bleibt ein Vorspulen (D572).
- **Invarianten erschöpfend, wo der Raum klein ist** (D571 Beschluss 3); zehn Stichproben sehen eine
  Regel nicht sicher.
- **Oli entscheidet, was er sieht** (die Wörter, D575); die übrigen Fragen entscheidet der
  Supervisor mit Position. Eine Frage je Antwort.
- **Beweis vor Code** für jede Änderung an `04 §4.4`.
- **Kein Auftrag verlangt einen Push** (D570 Befund 1). Oli pusht Branch und `main`.

## Der nächste Schritt: der Knoten für Sachanträge

Der Knoten kann heute keinen Sachantrag speichern und keinen Vorschlag mit Feld 3 annehmen
(`symbolon/node/store.py` verlangt die Schlüssel 0, 1, 2). Zu lesen vorher:
`symbolon/node/store.py`, `api.py`, `view.py` ganz (rund 2000 Zeilen), `04 §2.4`, `§2.5`, `§4.5`,
`§4.6`, D569 Beschluss 2, D575.

- **Zuerst die Umbenennung** `resolve_fassung` → `resolve_stand`, `FassungResolution` →
  `StandResolution`, `fassung_obj` → `stand_obj`, `tests/governance/test_fassung.py` →
  `test_stand.py` (D575 Beschluss 3), im selben Auftrag wie der Knoten oder davor.
- **Speicher:** eine Objektart für Sachanträge; Vorschläge mit Feld 3. Formwidrige Objekte: was der
  Knoten annimmt und was er ablehnt, nennt der Auftrag (Kandidat aus D474, D526, D572).
- **Schnittstelle:** Sachantrag anlegen (Feld, alter Wert aus dem Stand, neuer Wert), Stimme und
  Feststellung wie beim Vorschlag; der Satzungsantrag nennt `S`. `view.py` liefert den Stand
  (`resolve_stand`) statt der Verfassung der Epoche, wo die Seite Sachfelder zeigt.
- **Danach die Seite** mit den Wörtern aus D575; die Warnung vor einem Ja auf einen Satzungsantrag,
  der einen Sachantrag auslässt (Regel 3), und vor einem zweiten Ja auf dasselbe Feld (Regel 2).

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
`netz-g1`, `netz-a1`, `netz-v3`; im Ein-Knoten-Verein `verein5.sqlite` und `verein6.sqlite`.

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
- **Merge als eigener Befehl vor dem Registerblock.** Die Basisprüfung des Blocks fängt einen
  vergessenen Merge ab (der Block prüft `HEAD` gegen den Commit des Laufs).

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

## Offene Punkte

**15 offene Posten.** O96 ist der laufende Strang. Die übrigen 14 sind Wartestände: O31, O34 bis
O40 und O42 vertagt mit Bedingung; O25 (Sicherungsblob) ein Bau ohne Anlass; O56 der PyPI-Name;
O74 ein Stolperdraht; O89 (Amtswechsel der Kasse); O90 (Negentropy).

**Aus O96:** der Knoten und die Seite (oben). Weiter ohne Auftrag: die Stichfrage des doppelten Ja
je Feld (D564 Beschluss 3); Mengen als Sachfelder (D565 Beschluss 4); ob Aufnahmen neben
Sachfragen später laufen können (D564 Beschluss 1); `classify_all` läuft je Schritt der Kette
zweimal (D572 Befund 3); Key `2` einer Bürgschaft bleibt als `bond_ref` reserviert (D574).

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
Die Uhr jedes Knotens beginnt bei jedem Start bei 1000 (D518). Das Werkzeug glaubt dem Nachbarn,
dass Bytes zur angefragten `claim_id` gehören (D516, Phase 5).

**Aus D408:** Die Zahl der Auswertungen über ein Fenster hat keine Obergrenze; beisst es je, gehört
die Grenze nach `02 §8`.

**Aus der Aussprache mit Oli, für später:** eigene Währung als Kreditgeld über `unit_ref`
(`03 §3.3`), Olis Versicherungsbild mit kleinem Topf und verteilter Verwahrung, Signaturen mit
Schlüsselpreisgabe nur in Sonderfällen (D467), der Weg zurück nach einer Gabelung mit neuem
Schlüssel als eigenes Szenario (D489). Kandidaten nach Phase 5. Ob ein Beitrag von 0 Cent sinnvoll
ist, fragt `03 §3.3` (D503).
