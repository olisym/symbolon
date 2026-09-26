# Sitzungsstart: 00cn (MaR / symbolon), fortgeschrieben nach D520

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
- **Phase 4, Simulation mit mehreren S-Nodes: erste Stufe erreicht** (D514 bis D519). Fünf
  Geräte gleichen ab; Brunos Lüge bleibt jedem Gerät allein verborgen und zeigt sich nach dem
  Abgleich auf allen. Oli hat den Ablauf durchgespielt: „Das hat sich richtig gut angefühlt.“
- Phase 5: Reticulum.

## Stand

Am Ende von `00cm`: **1148 Tests**, im Selbsttest des Browsers **154 Fälle**, Register
**D1–D520**, Prüfregeln **1–83**, `make check` grün, `main` beim Commit, der diesen Sitzungsstart
trägt. **35 Wurzel-Markdown-Dateien, alle gebunden**; `archiv/` steht bei 150 mit
`sitzungsstart-00cl.md`. `offen.md` führt **90 Posten**, davon **14 offen**.

## Was in dieser Sitzung geschah

- **D514, D515 — der Bestand räumt nach.** Nachgelesen: SSB/EBT passt nicht, weil ein Claim keine
  Sequenznummer trägt und MaR keine Reihenfolge verlangt; Negentropy passt der Form nach und ist
  als O90 für Phase 5 vertagt. Gemessen: ein fremder Widerruf hing an der Reihenfolge, weil
  `submit_claim` mit Store prüft; zwei Knoten wären nie gleich geworden. Jetzt entfernt der
  Bestand einen fremden `core/*`-Claim, sobald sein Ziel eintrifft (`01 §6` „nicht gehalten“).
  Über alle 720 Reihenfolgen ein Bestand.
- **D516, D517 — der Abgleich zweier Knoten.** Das Netz ist ein Werkzeug (`tools/abgleich.py`),
  die Knoten antworten nur, weil der Server einfädig ist und die SQLite-Verbindung an seinem
  Faden hängt. Routen unter `/peer/`, Schalter `getrennt` im Knoten. Eine Runde liest zuerst und
  liefert dann ein. Befund an mir: eine Rücknahmeprobe, die der Test in meiner Fassung nicht sah.
- **D518, D519 — fünf Geräte.** `python -m tools.netz <verzeichnis>` startet Annas, Brunos, Brunos
  Zweitgerät, Chris' und Doras Gerät und gleicht alle zwei Sekunden jedes Paar ab. Die Seite als
  Gerät: Name im Tab, Knopf zum Trennen, Hinweis „Es ist Neues angekommen“, keine Geschichte.
  Olis Durchlauf ohne Befund.
- **D520 — Sitzungsschluss.**

## Neue Arbeitsweise aus dieser Sitzung

- **Rücknahmeproben laufen vorher gegen die Tests des Auftrags** (D517). Der Supervisor baut die
  Python-Teile als Prototyp im Klon, schreibt die Tests so, wie der Auftrag sie verlangt, und
  fährt jede Probe dagegen. So ging `p21-netz` hinaus, und alle fünf Proben trafen.
- **Einen Ablauf für Oli selbst durchspielen**, bevor er ihn bekommt. Beim Durchdenken von D518
  fielen zwei Fallen auf: das Zweitgerät muss den Antrag kennen, bevor es getrennt wird, und
  Brunos Aufgaben dürfen nur auf einem Gerät erledigt werden. Der Lauf über die Schnittstelle vor
  Olis Durchlauf bestätigte das Bild.
- **Oli ist schnell und genau,** wenn der Ablauf gedruckt vor ihm liegt. Ein Ablauf je Bild im
  Terminal reicht für den ersten Durchlauf.

## Der nächste Schritt

Offen, Oli entscheidet. Drei Richtungen aus `ROADMAP.md §6` und dieser Sitzung:

1. **Personen mit eigenem Verhalten.** Die simulierten Personen handeln selbst nach einfachen
   Regeln, statt dass Oli jeden Klick tut; das Netz zeigt dann, was daraus wird.
2. **Die Knoten in Docker im Homelab** (Dockge, Proxmox, Pi), als Brücke zu Phase 5. D513 hat das
   hinter die Prozesse auf Olis Rechner gestellt; die sind jetzt da.
3. **Der Ablauf in der Seite** statt im Terminal, als Geschichte über Geräte. D518 hat das für den
   ersten Durchlauf verworfen.

Zuerst gegen `offen.md` und das Register-Ende prüfen (Kandidat aus D409).

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
- **Neu aus D518:** Ein Ablauf, den ein Mensch Schritt für Schritt bedient, wird vorher selbst
  gefahren; die Reihenfolge ist Teil des Bildes.

## Offene Punkte

**Die 14 offenen Posten** sind Wartestände. O31, O34 bis O40 und O42 sind vertagt, jeder mit
seiner Bedingung; nach D466 öffnet sie ein Szenario, das sie braucht. O25 (Sicherungsblob) ist ein
Bau ohne Anlass. O56 ist der PyPI-Name. O74 ist ein Stolperdraht. O89 (Amtswechsel der Kasse
ist Schlüsselübergabe) öffnet mit einem Szenario, in dem das Amt wechselt. O90 (Negentropy) öffnet
in Phase 5 oder wenn eine Messung die volle Liste zu gross findet.

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
