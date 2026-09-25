# Sitzungsstart: 00cm (MaR / symbolon), fortgeschrieben nach D513

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
- Phase 3, Oberfläche mit dem Verein: abgeschlossen (D496 bis D512). Oli bedient den Verein im
  Browser, mit Tabs, Geschichte, Hell und Dunkel.
- **Phase 4, Simulation mit mehreren S-Nodes: beginnt jetzt.** Oli hat zugestimmt.
- Phase 5: Reticulum.

## Stand

Am Ende von `00cl`: **1134 Tests**, im Selbsttest des Browsers **154 Fälle**, Register
**D1–D513**, Prüfregeln **1–83**, `make check` grün, `main` beim Commit, der diesen Sitzungsstart
trägt. **35 Wurzel-Markdown-Dateien, alle gebunden**; `archiv/` steht bei 149 mit
`sitzungsstart-00ck.md`. `offen.md` führt **89 Posten**, davon **13 offen**.

## Was in dieser Sitzung geschah

- **D498 bis D505 — Eingaben, die stimmen.** Die Dauer einer Bürgschaft wird aufgerundet (D498).
  Ein Kern mit `t_exp` nicht nach `t` wird in `_prepare` mit `INCOHERENT_EXPIRY` abgewiesen, vor
  der Unterschrift (D499, D500). Punkte und Tage nur ganz (D501). Euro werden als Cent aus dem Text
  gelesen, nicht über eine Gleitkommazahl: `19.99` mal 100 ist dort 1998,9999… (D503).
- **D506 bis D508 — Tabs.** Oben fest Kopf, Meldung, Frage, „Jetzt zu tun“; darunter fünf Tabs mit
  Zählern. Ein Widerspruch steht oben nur, solange über den Antrag abgestimmt wird, sonst im Tab
  „Im Verein“ (D507).
- **D509, D510 — die Geschichte.** Zweites Kapitel „Der Beitrag“ nach `szenario-verein §6`; ist
  alles getan, verschwindet die Geschichte, und die Personen rücken nach oben.
- **D511, D512 — Hell und Dunkel.** 30 Farbvariablen, dunkel nach `prefers-color-scheme`, jedes
  Paar über 4,5 zu 1. `tests/node/test_stil.py` hält fest, dass keine feste Farbe zurückkommt.
- **D513 — Sitzungsschluss**, Phase 4 beschlossen.

## Neue Arbeitsweise aus dieser Sitzung

- **Claude Code je Auftrag frisch starten** (neues Fenster oder `/clear`). Ein Werkzeug, das über
  mehrere Aufträge läuft, liest Dateien aus dem Gedächtnis statt neu (D504 Befund 2). Die Aufträge
  verlangen das Lesen ausdrücklich.
- **Eine Oberfläche wird mit Olis Durchlauf abgenommen**, vor dem Merge. Oli prüft gern und
  schnell; ein Durchlauf fand in dieser Sitzung drei Befunde, die kein Test sah.
- **Eigene Rücknahmeprobe gegen den naheliegenden Fehler.** Dreimal blieb eine eigene Probe grün,
  und die Lücke lag jedes Mal in den Fällen, die der Supervisor im Beschluss genannt hatte
  (D501 Befund 1, D504 Befund 1, D512 Befund). Die Fälle eines Beschlusses decken jede Rechenstelle
  ab (etwa eine Nachkommastelle) und jeden Weg zur Stelle (etwa jede Route vor `_prepare`).
- **Ein Nachtrag** folgt dem Muster aus `00ck`: Registereintrag auf `main`, dann ein Auftrag
  `<branch>-nachtrag.md` auf demselben Branch, gemergt mit `--no-ff`.
- **Der Merge-Befehl prüft zuerst, dass `main` ausgecheckt ist.** Ohne das lief einmal ein Merge
  eines Branches in sich selbst, still wegen `-q`.

## Der nächste Schritt: Phase 4

Besprochen mit Oli, noch ohne Registereintrag:

1. **Zuerst nachlesen**, wie andere Knoten mit signierten, verketteten Logs abgleichen: Secure
   Scuttlebutt (Replikation, EBT), Nostr NIP-77 (Negentropy, bereichsbasierter Mengenabgleich),
   dazu was Szenario D bis F unter Partition gefunden haben (D336 bis D342).
2. **Dann der Abgleich als Beschluss:** jeder Knoten fragt seine Nachbarn, was ihm fehlt, holt es
   und prüft jeden Claim beim Eintreffen selbst (`structural_check`). Zu messen vor dem Beschluss:
   in welcher Reihenfolge Objekte und Claims ankommen müssen (`_check_foreign_lifecycle`) und ob
   ein Claim ohne bekannten Vorgänger angenommen wird.
3. **Wie die Knoten laufen, in Stufen:** zuerst mehrere Prozesse auf Olis Rechner, eigene Datei und
   eigener Port, ein Befehl startet alle; ein Schalter „getrennt“ im Knoten statt echter
   Netztrennung; erst danach Docker auf Maschinen im Homelab (Dockge, Proxmox, Pi) als Brücke zu
   Phase 5. Grund: in dieser Phase ändert sich der Code ständig, und jedes Abbild neu zu bauen
   bremst.
4. **Das Bild für Oli:** BRUNO stimmt Ja an einem Knoten und Nein an einem anderen; jeder Knoten
   allein sieht nichts, nach dem Abgleich sehen beide den Widerspruch. `szenario-verein §7`: eine
   Kette je Identität, KASSE lebt auf genau einem Gerät.

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
eine neue Datei; der Schlüssel im Browser bleibt. In `verein3.sqlite` ist die Geschichte durch.

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
- **Neu aus D501, D504, D512:** Die Fälle eines Beschlusses decken jede Rechenstelle und jeden Weg
  zur Stelle ab; der Supervisor prüft sie mit einer eigenen Probe gegen den naheliegenden Fehler,
  bevor der Auftrag hinausgeht.
- **Neu aus D503:** Wer ein Muster auf einen neuen Gegenstand überträgt, misst es dort; was für
  ganze Zahlen hält, bricht an Gleitkommazahlen.
- **Neu aus D512:** Ein Test, der Paare aus einer Datei liest, sieht nur, was die Datei
  ausdrücklich paart.

## Offene Punkte

**Die 13 offenen Posten** sind Wartestände. O31, O34 bis O40 und O42 sind vertagt, jeder mit
seiner Bedingung; nach D466 öffnet sie ein Szenario, das sie braucht. O25 (Sicherungsblob) ist ein
Bau ohne Anlass. O56 ist der PyPI-Name. O74 ist ein Stolperdraht. O89 (Amtswechsel der Kasse
ist Schlüsselübergabe) öffnet mit einem Szenario, in dem das Amt wechselt.

**Kleine Befunde an der Seite, ohne Auftrag:** eine Eingabe geht nach einer Meldung verloren
(D502); nach dem Beschluss heißt es „zu einem Antrag“ statt des Titels (D507 Befund 2); der
Stiltest sieht geerbte Farben nicht (D512). Dazu aus `00ck`: ob eine Bürgschaft Vertrauen
weitergibt, als Folgezeile (D495); der Zugang vom Telefon (D481 Befund 3); Chrome ungeprüft
(D484).

**Aus D408 getragen:** Die Zahl der Auswertungen über ein Fenster hat keine Obergrenze. Beisst es
je, gehört die Grenze nach `02 §8`.

**Aus der Aussprache mit Oli, für später:** eigene Währung als Kreditgeld über `unit_ref`
(`03 §3.3`), Olis Versicherungsbild mit kleinem Topf und verteilter Verwahrung, Signaturen mit
Schlüsselpreisgabe nur in Sonderfällen (D467), eine Stimme, die sich innerhalb einer
Abstimmungsfrist ändern lässt (D487 Befund 3), und der Weg zurück nach einer Gabelung mit neuem
Schlüssel als eigenes Szenario (D489). Kandidaten nach Phase 5. Ob ein Beitrag von 0 Cent
sinnvoll ist, fragt `03 §3.3` (D503).
