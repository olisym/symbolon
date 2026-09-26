# Sitzungsstart: 00co (MaR / symbolon), fortgeschrieben nach D528

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

- Phase 0 bis 3: abgeschlossen (D466 bis D512).
- **Phase 4, Simulation mit mehreren S-Nodes: erreicht** (D514 bis D526). Personen handeln
  selbst nach Regeln. Bild (a): Bruno lügt, und nach dem nächsten Abgleich sieht es jedes Gerät.
  Bild (b): Dora vertut sich auf einem Zweitgerät mit ihrem Schlüssel, das Netz sieht bei ihr
  dasselbe wie bei Bruno, der Beschluss fällt, und die Karte sagt warum.
- **Offen vor Phase 5: mehrere Geräte einer Person** (O92). Oli findet D123 nicht befriedigend.
- Phase 5: Reticulum.

## Stand

Am Ende von `00cn`: **1154 Tests**, im Selbsttest des Browsers **165 Fälle**, Register
**D1–D528**, Prüfregeln **1–83**, `make check` grün, `main` beim Commit, der diesen Sitzungsstart
trägt. **35 Wurzel-Markdown-Dateien, alle gebunden**; `archiv/` steht bei 151 mit
`sitzungsstart-00cm.md`. `offen.md` führt **92 Posten**, davon **15 offen**.

## Was in dieser Sitzung geschah

- **D521, D522 — Personen mit eigenem Verhalten, Bild (a).** `tools/personen.py` handelt über die
  bestehenden Routen nach einer Tabelle von Regeln; je Takt erst handeln, dann abgleichen. Gemessen
  vor dem Auftrag: die Lüge braucht keine Trennung, jede Lücke zwischen zwei Abgleichen genügt; eine
  Trennung kann sie sogar verhindern. Olis Satz: „Jede Lücke zwischen zwei Abgleichen ist eine
  Trennung. Bruno nutzt sie, und nach dem nächsten Abgleich sieht es jedes Gerät.“
- **D523, D524 — Bild (b), Doras Versehen.** Ein sechstes Gerät trägt DORAs Schlüssel, Dora handelt
  dort einen Takt später, getrennt nach Plan. Gemessen: mit fester Uhr gleiche Bytes und keine
  Gabel; mit der Wanduhr zwei Gabeln, und der Beschluss fällt, weil nach `04 §3.1` keine Stimme
  einer Gabelung zählt. Olis Satz: „Dora hat sich nur vertan, Bruno hat gelogen. Das Netz sieht bei
  beiden dasselbe: keiner von beiden zählt mehr, und der Beschluss fällt.“
- **D525, D526 — die Karte.** Jedes Paar von Stimmen zum selben Antrag ist eine Doppelstimme: oben,
  solange der Antrag offen ist, mit dem Antrag im Satz und „Keine der beiden Stimmen zählt.“; bei
  fremden Werten „zweimal verschieden“. Olis Durchlauf: „das passt so“.
- **D527 — O91 war ein Fehler von mir.** Die Frage nach mehreren Geräten stand seit D123 entschieden
  im Register; ich hatte sie als offen angelegt. Autobase nachgeholt, bestätigt D123 und D124.
- **D528 — Sitzungsschluss.** Oli hält D123 für unpraktisch und will die Frage neu aufrollen: O92.

## Neue Arbeitsweise aus dieser Sitzung

- **Den Prototyp über den echten Startbefehl fahren, nicht nur im Test.** Der Lauf mit der Wanduhr
  hat in D523 das Bild erst gezeigt (feste Uhr: keine Gabel). Den Endstand eines solchen Laufs liest
  der Supervisor über die Schnittstelle, wenn der Bericht ihn nicht abfragt (D524).
- **Die Seite liest Oli, und was er fragt, ist ein Befund.** „Ist das so gewollt?“ zu zwei Orten der
  Karten führte zu D525; die Regel aus D507 war für Ja und Nein gedacht.

## Der nächste Schritt: O92, mehrere Geräte einer Person, neu bewerten

Olis Einwand gegen D123: Ein Zweitgerät, das sein Erstgerät erreichen muss, ist kaum mehr wert als
das Erstgerät. Oli will die Frage tief und unter neuen Suchbegriffen nachlesen und die bisherigen
Beschlüsse nicht als fest behandeln. Zuerst gelesen werden: `01 §8`, D123, D124, D471 Beschluss 2,
D489 Befund 2 und Beschluss 2, D523, D527. Nicht noch einmal gesucht wird, was dort schon steht:
did:plc, Keybase, CONIKS, Nostr NIP-41, Secure Scuttlebutt (Fusion IDs, ICN 2019), Cosmos,
Matrix Cross-Signing, Autobase.

Leitfragen, jede mit der Entscheidung, die sie ändern kann:

1. **Wer ist der Ort?** D123 sagt nicht, dass der Ort das Erstgerät sein muss. Ein S-Node im
   Homelab wäre immer erreichbar, im Netz; über Funk in Phase 5 nicht. Trägt Olis Einwand gegen
   den Ort überhaupt, oder nur gegen das Erstgerät als Ort? Ändert: D123, oder nur seine Lesart.
2. **Muss eine Kette eine Kette sein?** Kann die Geschichte eines Schlüssels ein DAG mit mehreren
   Köpfen sein, die sich wieder vereinen, und als Widerspruch gilt nur, was sich inhaltlich
   ausschliesst? Ändert: `01 §4`, D43, D469, `04 §3.1` Bedingung 6.
3. **Kann ein Widerspruch über Geräteschlüssel hinweg entstehen?** D123 verwirft Ketten je Gerät,
   weil dann Equivocation frei wäre. Das gilt nur, wenn Widersprüche je Kette erkannt werden. Werden
   sie je Identität erkannt (zwei Geräte derselben Person stimmen verschieden), kollidieren die
   Aussagen wieder. Ändert: D123s Begründung, `02 §8`.
4. **Was kostet jede Antwort?** Nach D124 bezahlt jede Rettung der Identität mit Ordnung. Der
   Maßstab bleibt `08 §2.2`: Aussagen kollidieren, kein globaler Konsens, Prüfung offline.

Suchbegriffe, neu gegenüber der Liste oben:

- Kleppmann und Howard, „Byzantine Eventual Consistency“ (2020), und Kleppmann, „Making CRDTs
  Byzantine Fault Tolerant“ (2022): Hash-DAG statt Kette, gleichzeitige Einträge eines Autors
  erlaubt.
- KERI (Key Event Receipt Infrastructure): „duplicity detection“, „delegated identifiers“,
  „pre-rotation“, Zeugen und Wächter.
- Ink & Switch, „Keyhive“ und „Beelay“: Geräte, Gruppen und Delegation in local-first Software.
- Willow und Meadowcap, Earthstar: Fähigkeiten, die an Geräteschlüssel delegiert werden.
- p2panda: Schlüssel je Gerät und Gruppen von Schlüsseln.
- MLS (RFC 9420) und WhatsApp Multi-Device: Gerät als eigenes Blatt, Identitätsschlüssel
  beglaubigt Geräteschlüssel.
- Nostr NIP-46 („remote signing“, „bunker“): die Form des Orts aus D123 in der Praxis; NIP-26 und
  warum es nicht empfohlen wird.
- AT Protocol: der PDS als Ort, der den Signierschlüssel hält, und die Clients als Endpunkte.

Arbeitsform: erst gegen das Register suchen (Kandidat aus D514, geschärft in D527), dann die
Quellen je Leitfrage lesen, Zitate unter 15 Wörtern, Befunde mit Quelle in einen Registereintrag.
Erst danach ein Vorschlag, und der wird wie in D521 an einem Prototyp gemessen, bevor er normativ
wird.

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

**Personen, die selbst handeln:** derselbe Befehl mit `--personen` (Bild a, fünf Geräte) oder
`--versehen` (Bild b, sechs Geräte), je mit neuem Verzeichnis. Nach etwa 12 oder 16 Sekunden ist
der Lauf durch; dann die Tabs öffnen und nur ansehen. Durch sind `netz-p1`, `netz-v1`, `netz-v2`.

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

## Offene Punkte

**Die 15 offenen Posten.** O92 ist der nächste Schritt. Die übrigen sind Wartestände. O31, O34 bis
O40 und O42 sind vertagt, jeder mit seiner Bedingung; nach D466 öffnet sie ein Szenario, das sie
braucht. O25 (Sicherungsblob) ist ein Bau ohne Anlass. O56 ist der PyPI-Name. O74 ist ein
Stolperdraht. O89 (Amtswechsel der Kasse ist Schlüsselübergabe) öffnet mit einem Szenario, in dem
das Amt wechselt. O90 (Negentropy) öffnet in Phase 5 oder wenn eine Messung die volle Liste zu
gross findet.

**Aus dieser Sitzung, ohne Auftrag:** Dass eine Feststellung nicht mehr trägt, sagt die Seite
nirgends (D525). Eine Stimme neben einem anderen Claim an derselben Stelle zählt auch nicht; die
Karte sagt dann nur „zweimal an dieselbe Stelle“ (D525). Dora sieht ihren Widerspruch, aber nichts
zu tun (D526). Der Antrag im Takt 2 prüft die Spitzen nicht (D522). Der Kopf von `tools/netz.py`
nennt fünf Geräte (D524).

**Kleine Befunde an der Seite, ohne Auftrag:** eine Eingabe geht nach einer Meldung verloren
(D502); nach dem Beschluss heißt es „zu einem Antrag“ statt des Titels (D507 Befund 2); der
Stiltest sieht geerbte Farben nicht (D512). Dazu aus `00ck`: ob eine Bürgschaft Vertrauen
weitergibt, als Folgezeile (D495); der Zugang vom Telefon (D481 Befund 3); Chrome ungeprüft
(D484).

**Aus dem Netz, ohne Auftrag:** ein zweites Strg-C beim Beenden von `tools.netz` druckt einen
Traceback, ohne dass ein Knoten übrig bleibt (D519). Die Uhr jedes Knotens beginnt bei jedem Start
bei 1000 (D518). Das Werkzeug glaubt dem Nachbarn, dass Bytes zur angefragten `claim_id` gehören;
ein lügender Nachbar kann eine Runde endlos wiederholen lassen (D516, Phase 5).

**Aus D408 getragen:** Die Zahl der Auswertungen über ein Fenster hat keine Obergrenze. Beisst es
je, gehört die Grenze nach `02 §8`.

**Aus der Aussprache mit Oli, für später:** eigene Währung als Kreditgeld über `unit_ref`
(`03 §3.3`), Olis Versicherungsbild mit kleinem Topf und verteilter Verwahrung, Signaturen mit
Schlüsselpreisgabe nur in Sonderfällen (D467), eine Stimme, die sich innerhalb einer
Abstimmungsfrist ändern lässt (D487 Befund 3), und der Weg zurück nach einer Gabelung mit neuem
Schlüssel als eigenes Szenario (D489). Kandidaten nach Phase 5. Ob ein Beitrag von 0 Cent
sinnvoll ist, fragt `03 §3.3` (D503).
