# Sitzungsstart: 00cq (MaR / symbolon), fortgeschrieben nach D550

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
- **Mehrere Geräte einer Person:** im Protokoll gelöst (O92, D529 bis D540), in Knoten, Simulation
  und Karte gebaut und von Oli durchlaufen (O94, D542 bis D546).
- **Eine Stimme ersetzt, was sie nennt:** O93 gelöst (D547 bis D549), D97 beantwortet.
- Phase 5: Reticulum.

## Stand

Am Ende von `00cp`: **1203 Tests**, im Selbsttest des Browsers **180 Fälle**, Register
**D1–D550**, Prüfregeln **1–83**, `make check` grün, `main` beim Commit, der diesen Sitzungsstart
trägt. **35 Wurzel-Markdown-Dateien, alle gebunden**; `archiv/` steht bei 153 mit
`sitzungsstart-00co.md`. `offen.md` führt **94 Posten**, davon **14 offen**, alle Wartestände mit
Bedingung.

## Was in dieser Sitzung geschah

- **D542 bis D546 — O94, Bild (c).** `--geraete`: die Zweitgeräte tragen einen eigenen, von der
  Wurzel aufgenommenen Schlüssel; die Wurzel liegt warm auf dem Erstgerät (D542 Beschluss 2, weil
  `accept-rules@1` und `receipt@1` nach `I` rechnen). Dora stimmt zweimal Ja und zählt einmal, der
  Beschluss hält; Bruno stimmt auf zwei Geräten verschieden, keine Stimme zählt, er behält seine
  Kanten. Die Sicht rechnet je Wurzel; eine neue Quelle `/geraetestimmen` zeigt Stimmen einer
  Wurzel von mehreren Schlüsseln dauerhaft, über die Epoche hinaus (D542 Befund 4: am Antrag wäre
  es nie zu sehen gewesen). Gebaut in `p27-geraete` mit zwei Nachträgen aus meinem Wortlaut (D544,
  D545). Oli hat alle sechs Tabs durchlaufen: „leicht abzulesen“, überall dasselbe (D546).
- **D547 bis D549 — O93, die ersetzende Stimme.** `v` Key `1` nennt frühere Stimmen derselben
  Wurzel; was genannt ist, zählt nicht mehr. Oli wählte B (ersetzen immer) statt A (nur nach
  Widerspruch). Die Antwort auf D97: eine nennende Stimme zählt nie weniger als dieselbe ohne
  Nennung, gemessen an 2468 Zwischenständen; sie öffnet keinen Weg abwärts, den die bloße zweite
  Stimme nicht schon hat, und die Frist aus D487 wird nicht gebraucht. Die Seite nennt jede
  frühere Stimme, die ihr Bestand kennt (Olis Ja): ein zweiter Klick ist ein Stimmwechsel
  (`CHANGE_VOTE`). Gebaut in `p28-ersetzen`, ohne Nachtrag.
- **D550 — Sitzungsschluss.**

## Arbeitsweise, bestätigt

- **Prototyp vor dem Text, Prototyp vor dem Auftrag** (aus `00co`) hat wieder getragen: der zweite
  Prototyp zu O93 fand die Gruppierung aus D542, die sonst den aufgelösten Widerspruch weiter
  gezeigt hätte.
- **Oli entscheidet, was er sieht und wie es sich anfühlt** (Ort eines Satzes, A oder B, ob die
  Seite nennt); die übrigen Fragen entscheidet der Supervisor mit Position. Eine Frage je Antwort.
- **Die Tests stehen wörtlich im Auftrag**, das Werkzeug übernimmt sie; der Supervisor fährt die
  Rücknahmeproben vorher gegen genau diese Fassung. Das Werkzeug hat die Dateien aus dem Auftrag
  gezogen statt abzutippen.

## Der nächste Schritt: das Folgebild, Bruno löst seinen Widerspruch auf

In Bild (c) ist der Antrag festgestellt, bevor Bruno seinen Widerspruch sieht; er kann ihn dort
nicht mehr auflösen (D549). Ziel ist ein Bild, in dem er es kann: Brunos Zweitgerät stimmt Nein,
ohne das Ja zu kennen; nach dem Abgleich sieht Bruno die Karte, stimmt auf einem Gerät neu, die
Stimme nennt beide, und die Karte verschwindet; der Antrag zählt ihn mit der neuen Wahl.

Zuerst gelesen werden: `tools/personen.py` (`takt`, `absichten`, `TRENNUNG`, `ANTRAG_TAKT`),
`tools/netz.py` (`GERAETE_GERAETE`, `ZUSEHEN_GERAETE`), die Widerspruchskarte in `app.js`
(`geraeteKarten`) und `geraeteSatz` in `anzeige.js`, D523, D542, D548. Fragen vor dem Auftrag:
Wann stellt Anna fest, damit Bruno vorher auflösen kann (eine Feststellung erst nach dem Abgleich,
oder ein Antrag, der ohne Bruno nicht durchkommt)? Was sagt die Karte als dritten Punkt („Eine neue
Stimme von BRUNO ersetzt beide.“)? Bleibt Bild (c) wie es ist, und das Folgebild wird ein vierter
Schalter? Vorher den Ablauf selbst über die Schnittstelle fahren (D518), dann Olis Durchlauf (D490).

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
16 Sekunden ist der Lauf durch; dann die Tabs öffnen und nur ansehen. Durch sind `netz-p1`,
`netz-v1`, `netz-v2`, `netz-g1`.

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
- **Der Selbsttest läuft nicht in `make check`.** Das Werkzeug zählt ihn mit einem Skript im
  Scratchpad; ein eigener Auftrag, wenn es wieder gebraucht wird (D549).

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

## Offene Punkte

**Die 14 offenen Posten sind Wartestände.** O31, O34 bis O40 und O42 vertagt mit Bedingung; O25
(Sicherungsblob) ein Bau ohne Anlass; O56 der PyPI-Name; O74 ein Stolperdraht; O89 (Amtswechsel der
Kasse); O90 (Negentropy).

**Aus dieser Sitzung, ohne Auftrag:** das Folgebild (oben). Der Selbsttest in `make check` (D549).
Die kalte Wurzel und die übrigen Profile nach `I` (D534 Beschluss 2, D542 Beschluss 2). Die
Aufnahme eines Geräts als Handlung im Netz (D542 Beschluss 3). `DISPUTED_VOTE` ohne Satz auf der
Seite (D542). Die Gruppierung sieht `CONFLICTING_APPROVAL` nicht, und die Absicht behandelt ein
gesperrtes Gerät wie seine Wurzel (D543, schwächste Stelle). `04 §4.4`: ein ersetztes Ja blockiert
weiter ein Ja auf einen anderen Antrag derselben Epoche; lockern bräuchte einen eigenen Beweis (D547
Beschluss 4). Knoten verschiedener Fassung sehen bei Key `1` verschiedene Epochen, bis beide die
Regel haben; wer die Rust-Fassung weckt, übernimmt sie (D547 Befund 6). `szenario-verein §9` sagt,
zwei Geräte einer Identität gabelten sich selbst; seit D529 gilt das nur für einen geteilten
Schlüssel (D548 Befund 5). In `folgeZeilen` ist ein Zweig von der Absicht aus nicht mehr erreichbar
(D548 Befund 4).

**Aus `00co`, weiter ohne Auftrag:** Eine Bürgschaft **auf** einen Geräteschlüssel bleibt beim
Gerät (D535). Die Zurechnung geht je Anfrage die Kette entlang (D538 Befund 2). Der Beispielverein
führt `verdict@1` nicht im Boden (D539). Eine Wurzel, die ihre eigene Aufnahme bestätigt, nimmt sich
jede Aufnahme (D538 Befund 1).

**Aus `00cn`:** Dass eine Feststellung nicht mehr trägt, sagt die Seite nirgends (D525). Eine
Stimme neben einem anderen Claim an derselben Stelle zählt auch nicht; die Karte sagt dann nur
„zweimal an dieselbe Stelle“ (D525). Der Antrag im Takt 2 prüft die Spitzen nicht (D522).

**Kleine Befunde an der Seite:** eine Eingabe geht nach einer Meldung verloren (D502); nach dem
Beschluss heißt es „zu einem Antrag“ statt des Titels (D507 Befund 2, für Gabelkarten); der
Stiltest sieht geerbte Farben nicht (D512); ob eine Bürgschaft Vertrauen weitergibt, als Folgezeile
(D495); der Zugang vom Telefon (D481 Befund 3); Chrome ungeprüft (D484).

**Aus dem Netz:** ein zweites Strg-C beim Beenden von `tools.netz` druckt einen Traceback (D519).
Die Uhr jedes Knotens beginnt bei jedem Start bei 1000 (D518). Das Werkzeug glaubt dem Nachbarn,
dass Bytes zur angefragten `claim_id` gehören (D516, Phase 5).

**Aus D408:** Die Zahl der Auswertungen über ein Fenster hat keine Obergrenze; beisst es je, gehört
die Grenze nach `02 §8`.

**Aus der Aussprache mit Oli, für später:** eigene Währung als Kreditgeld über `unit_ref`
(`03 §3.3`), Olis Versicherungsbild mit kleinem Topf und verteilter Verwahrung, Signaturen mit
Schlüsselpreisgabe nur in Sonderfällen (D467), der Weg zurück nach einer Gabelung mit neuem
Schlüssel als eigenes Szenario (D489). Kandidaten nach Phase 5. Ob ein Beitrag von 0 Cent sinnvoll
ist, fragt `03 §3.3` (D503). Die Stimme, die sich ändern lässt (D487 Befund 3), ist mit D547 gelöst.
