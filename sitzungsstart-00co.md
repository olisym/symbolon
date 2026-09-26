# Sitzungsstart: 00cp (MaR / symbolon), fortgeschrieben nach D541

## Was das hier ist

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
- **Mehrere Geräte einer Person (O92): im Protokoll gelöst** (D529 bis D540). Offen ist, dass
  Knoten, Simulation und Karte es noch nicht kennen (O94).
- Phase 5: Reticulum.

## Stand

Am Ende von `00co`: **1181 Tests**, im Selbsttest des Browsers **165 Fälle**, Register
**D1–D541**, Prüfregeln **1–83**, `make check` grün, `main` beim Commit, der diesen Sitzungsstart
trägt. **35 Wurzel-Markdown-Dateien, alle gebunden**; `archiv/` steht bei 152 mit
`sitzungsstart-00cn.md`. `offen.md` führt **94 Posten**, davon **16 offen**.

## Was in dieser Sitzung geschah

- **D529 bis D534 — das Bild.** Eine **Wurzel** (Olis Hauptidentität, kalt auf einem Trezor)
  nimmt **Geräte** mit eigenem Schlüssel und eigener Kette auf, je Scope, mit Gegenzeichnung
  (`device-add@1`, `device-ack@1`). Die Wurzel wird nur für Aufnahme und Ende gebraucht; ein
  Zweitgerät schreibt ohne das Erstgerät. Das Wort „Ort“ aus D123 fällt weg: es legte zwei Rollen
  in eins. Literatur: KERI (Delegation), WhatsApp Multi-Device, Keyhive, Kleppmann/BEC, NIP-26/46.
- **Widerspruch je Wurzel am Inhalt.** Gleiche Wahl von zwei Geräten zählt einmal, verschiedene
  gar nicht, sichtbar, ohne Verlust der Kanten (Olis Satz: „ein Mensch kann nur ein Gerät
  gleichzeitig bedienen“). `min(claim_id)` trug nicht; jede der gleichen Stimmen darf zeugen (D530).
- **D532, D533 — das Kartenbild.** `device-end@1` ist die **Sperre**: sie wirkt sofort; was sie
  abschneidet, ist **bestritten, nicht bestraft** („eine Gabel ist ein Beweis, ein Bestreiten
  nicht“). Olis Einwand hat Weg C (Flag für die Wurzel) gekippt: 50 Jahre Ruf fielen sonst wegen
  eines gestohlenen Telefons. Eine bestrittene Stimme rechnet nur ein Schiedsrichter der Satzung
  zurück, und nur, wenn `verdict@1` dort unwiderruflich ist (D539). Ein Schiedsrichter kann ein
  FROST-Panel des Vereins sein.
- **D535 bis D540 — Text und Bau.** Normativ in `00 §5.2` (Boden), `01 §7.3` (Profile), `02 §2.1`
  (Zurechnung), `04 §3.1`, `§4.1`, `§4.4`. Gebaut in `p25-zurechnung`
  (`symbolon/trust/attribution.py`, Gruppen, Flags) und `p26-auszaehlung` (Auszählung und
  Feststellung je Wurzel, `DISPUTED_VOTE`). Beide Prototypen vorher im Klon, alle Proben dort
  gefahren; beide Prototypen fanden Fehler in meinem Text (D536, D539).
- **D541 — Sitzungsschluss.**

## Neue Arbeitsweise aus dieser Sitzung

- **Vor dem normativen Text der Prototyp, vor dem Auftrag der zweite.** Der Prototyp zum Text
  (D530, D531) prüft die Richtung; der zum Auftrag (D536, D539) prüft den Wortlaut. Beide Male
  fand der zweite etwas, das der erste nicht sehen konnte.
- **Oli entscheidet die Frage, die ihn betrifft; die übrigen entscheidet der Supervisor mit
  Position.** Eine Frage je Antwort. Olis Einwände waren zweimal der Wendepunkt (D529, D532).

## Der nächste Schritt: O94, Geräte im Knoten, in der Simulation und auf der Karte

Ziel ist das Bild, an dem Oli die Änderung sieht: Bild (b) aus D523 mit Doras Zweitgerät als
**eigenem, aufgenommenem Schlüssel**. Erwartet: Dora stimmt zweimal Ja, die Stimme zählt einmal,
der Beschluss **hält**; die Karte sagt es. Dazu Bild (a) mit Brunos Lüge über zwei Geräte:
beide Stimmen zählen nicht, sichtbar, Bruno behält seine Kanten.

Zuerst gelesen werden: `symbolon/node/api.py` (`_budget_of`), `symbolon/node/view.py` (Karten,
`tally.yes`), `tools/ref_block.py`, `tools/netz.py`, `tools/personen.py`, D523 bis D526, D537
Befund 2, D539. Fragen, die vor dem Auftrag zu entscheiden sind: Wie nimmt ein Gerät in der
Simulation auf (die Wurzel als eigenes Gerät im Netz, oder Aufnahme vorab im Bestand)? Was sagt die
Karte bei gleicher Wahl zweimal, bei `DISPUTED_VOTE`? Die Seite braucht einen Durchlauf mit Oli
(D490). Vorher den Ablauf selbst über die Schnittstelle fahren (D518).

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
- **Das Werkzeug fährt Rücknahmeproben ohne Bytecode-Cache.** Zweimal zeigte ein veralteter
  `.pyc` eine Probe grün (D538, D540). Im Supervisor-Klon gilt `PYTHONDONTWRITEBYTECODE=1`
  ohnehin.
- **`tests/governance/fixtures.py`:** `fresh_p2()` liefert ALICE, BOB, CAROL, DAVE, EVE in dieser
  Reihenfolge. Eine Verfassung mit anderem Boden baut man dort ohne neue Epoche.
- **Ein laufender Auftrag bekommt einen Nachtrag, keinen neuen Auftrag,** wenn eine Rückfrage die
  Spec ändert: Arbeit parken (`git stash`), Spec auf `main`, Branch vorspulen, Arbeit zurück (D537).

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

## Offene Punkte

**Die 16 offenen Posten.** O94 ist der nächste Schritt. O93 (auflösende Stimme) öffnet danach; er
muss D97 beantworten und kann über einen belegten Key in `v` der Stimme gehen (D534 Befund 2). Die
übrigen sind Wartestände: O31, O34 bis O40 und O42 vertagt mit Bedingung; O25 (Sicherungsblob) ein
Bau ohne Anlass; O56 der PyPI-Name; O74 ein Stolperdraht; O89 (Amtswechsel der Kasse); O90
(Negentropy).

**Aus dieser Sitzung, ohne Auftrag:** Eine Bürgschaft **auf** einen Geräteschlüssel bleibt beim
Gerät (`02 §2`); ob das so bleibt, ist nicht gemessen (D535). Nur `vouch@1`, `vote@1` und
`ratify@1` rechnen Geräte der Wurzel zu; Obligationen und die übrigen Profile nach `I` (D534
Beschluss 2). Die Zurechnung geht je Anfrage die Kette entlang (D538 Befund 2). Der Beispielverein
führt `verdict@1` nicht im Boden; eine bestrittene Stimme bleibt dort bestritten (D539). Eine
Wurzel, die ihre eigene Aufnahme bestätigt, nimmt sich jede Aufnahme (D538 Befund 1).

**Aus `00cn`, ohne Auftrag, zu O94 gehörig:** Dass eine Feststellung nicht mehr trägt, sagt die
Seite nirgends (D525). Eine Stimme neben einem anderen Claim an derselben Stelle zählt auch nicht;
die Karte sagt dann nur „zweimal an dieselbe Stelle“ (D525). Dora sieht ihren Widerspruch, aber
nichts zu tun (D526). Der Antrag im Takt 2 prüft die Spitzen nicht (D522). Der Kopf von
`tools/netz.py` nennt fünf Geräte (D524).

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
