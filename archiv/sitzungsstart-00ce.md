# Sitzungsstart: 00ce (MaR / symbolon), fortgeschrieben nach D440

## Was das hier ist

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Repositorium **`symbolon`**, Gitea (`git.h.error13.de/oli/symbolon`,
LAN-only) und GitHub-Spiegel (`github.com/olisym/symbolon`). Lokaler Ordner bleibt
bewusst `~/mensch-als-republik`. Tagline seit D335: *Symbolon: A Self-Verifying Trust
Layer for Local-First Networks*. Spec-Titel bleibt bewusst *Mensch als Republik* (D317).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Aufträge, führst die Abnahmen. Schreibst keinen
Produktivcode.

**Supervisor-Zugriff:** Direkter Klon/Pull über den öffentlichen GitHub-Spiegel. Commit-Hash
vor jedem Lesen gegen den geklonten `HEAD` prüfen. Der Spiegel liegt regelmässig einen Commit
**vor** dem hier genannten Stand, weil dieser Sitzungsstart sich selbst nicht mitzählt.

## Stand

Am Ende von `00ce`: **935 Tests**, Register **D1–D440**, Prüfregeln **1–79**, `make check` grün,
`main` beim Commit, der D440 und diesen Sitzungsstart trägt. **33 Wurzel-Markdown-Dateien, alle
gebunden**; `archiv/` steht bei 142 mit `sitzungsstart-00cd.md`. `offen.md` führt **76 Posten**,
davon **15 offen**; O41 und O76 sind in dieser Sitzung geschlossen, O76 ist in ihr entstanden.

**Stränge:** `main` und `00bo-hs` (kontaminiert, D374, wird nicht gelöscht). Gemergt und stehen
gelassen, neu in dieser Sitzung: `o76-zf02`, `d439-subgranular`.

## Was in dieser Sitzung geschah

- **D437:** O41 geschlossen. Die Bedingung war seit D353 erfüllt (D424 hatte nur die Befunde aus
  D312 durchgesehen), und die unabhängige Lesung von `01` lag aus den Layer-02-Fassungen vor. Sie
  hat eine Textlücke gefunden: `rs` las `linked` transitiv, die Referenz nur am unmittelbaren
  Vorgänger. Normiert in `01 §6` und `Anhang B.1`. Neu O76.
- **D438:** der Vektorsatz `ZF-02` mit drei Profilen (Lücke, Gabel, Rückdatierung) und
  handgerechneten Golden Numbers; die Messung in zwei Stufen, damit der Ankernachzug die alte
  Lesart nicht überschreibt, bevor sie gemessen ist.
- **D439:** Abnahme `ZF-02`; **Stufe A** gemessen: die unveränderte Rust-Fassung
  (`~/mar-rs/target/release/trustflow02`, Anker `15d091e`) rechnet F1 transitiv, D437 war also
  eine Reparatur. F2 weicht am alten Aktiv-Set von `02 §3.1` ab (O73). Neuer Befund:
  `SUBGRANULAR_VOUCH` am unerreichbaren Autor; normiert in `02 §10`, dass der Vermerk einen
  erreichten Autor voraussetzt. O76 erledigt.
- **D440:** Abnahme des Bindungstests für D439, Sitzungsschluss.

## Werkzeugnotizen

- **`AGENTS.md` trägt weiter.** Zwei Läufe in Cursor, je ein frischer Chat, Auftragstext als erste
  Nachricht eingefügt, vorher `git switch` auf den Auftrags-Branch. Beide Diffs ohne
  Scope-Abweichung.
- **Aufträge liegen ausserhalb des Repos** in `~/auftraege/`. Der Auftrag prüft im ersten Schritt
  die Commit-Meldung seiner Basis.
- **Messen im Supervisor-Klon** hat in dieser Sitzung drei Rücknahmeproben ohne Auftrag geleistet.
  Umgebung: `python3 -m venv --system-site-packages .venv`, dann `.venv/bin/pip install ruff cbor2
  cryptography pytest hypothesis`; damit läuft `make check` im Klon wie beim Operator.
- **Der Supervisor-Klon ist flach.** Vollständig holen mit
  `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`. Vor jedem Pull eigene Entwürfe
  verwerfen.
- **Die Rust-Fassung läuft direkt auf dem Host**: `trustflow02 <vektordatei>`, Vergleich mit
  `diff` gegen `tools/ref_block.py`, die `inf`-Zeile ausserhalb (D391 Beschluss 4).
- **Lieferungen:** in `/tmp`, Hashprüfung von Lieferung und Basis vor jeder Änderung, `rm` als
  letzter Job vor `== FERTIG ==`. Merge und Push als eigene Befehle.

**Prüfregel-Kandidaten, weiter nicht übernommen:**
- Einen Abschnitt ganz lesen, bevor man aus einem Satz darin schliesst (D392 → D394).
- An zwei Fällen Gemessenes nicht „durchgehend" nennen (D390 → D396).
- Eine Karte aus Wortsuche ist eine Vermutung; vor dem Schreiben den Wortlaut lesen (D397 → D398).
- Eine Flächenzeile, die vor dem Lesen des Codes geschrieben wird, ist eine Schätzung (D408).
- Der nächste Schritt eines Sitzungsstarts wird gegen `offen.md` und das Register-Ende geprüft
  (D409).
- Ein Strang, den ein Sitzungsstart über mehr als eine Sitzung trägt, hat eine O-Nummer oder
  einen Registereintrag (D412).
- Die englische Schale nennt keine Zahl, die mit der Arbeit wächst (D415).
- Eine Beschreibung, die eine Zahl aus einem anderen Eintrag wiederholt, veraltet mit ihm (D420).
- Ein Lauf, der ungefragt etwas entfernt, ist Scope-Verlust und gehört in den Bericht wie ein
  Zuwachs (D435).
- **Neu aus D440:** ein Vergleichs-`diff` wird nicht mit `head` gekürzt; die Regel für `git diff`
  gilt für jeden Diff, der Messgrundlage ist.
- **Neu, bemerkt in D437:** eine Bedingung, an die ein vertagter Posten geknüpft ist, wird gegen
  alle Einträge seit ihrer Setzung geprüft, nicht gegen die eine Runde, die gerade ansteht.

## Offene Punkte

**Die 15 offenen Posten** sind fast alle Wartestände: O31, O34 bis O40 und O42 bewusst vertagt,
jeder mit seiner Bedingung; O25 ein Bau ohne Anlass; O52, O53 zur Öffnung; O56 (PyPI-Name); O73 und
O74 Stolperdrähte. **O73 hat jetzt einen Anlass**, siehe unten.

**Merkposten Restack:** eingereicht am 10. September, Code `2026-11-0c4` (D349), Frist
3. November. Mitte Oktober nur prüfen, ob der Antrag den Stand grob falsch beschreibt.

**Aus D408 getragen:** die Zahl der Auswertungen über ein Fenster hängt am Bestand und hat keine
Obergrenze; beisst es je, gehört die Grenze nach `02 §8`.

## Der nächste Schritt

**Stufe B, O73: die Rust-Fassung liest den heutigen Text.** Erst eine Entscheidung, dann ein Lauf.

1. **Die Frage aus O73 entscheiden.** D368 hält `02a` von der Rust-Fassung zurück; der Normstoff
   von `02a` steht seit D397 in `02 §11`. Ein Nachzug gibt ihr damit, was die Diät zurückhalten
   sollte. Zu lesen vorher: D368, D389, D390, `rs/AUFTRAG.md`, `rs/spec/STAND.md`, O73.
2. **Ankernachzug und Lauf** im Isolat (`mar-rs-box`, `~/mar-rs`), dann alle vier Vektorsätze
   (`TP-02`, `TZ-02`, `FALL-02`, `ZF-02`) gegen `ref_block`.

**Die Erwartung, vor dem Lauf fixiert:** in `ZF-02` stimmen F1 und F2 mit der Referenz überein
(b3 `active`, Fluss 3; keine Kante an f1 und f2), und die neun `SUBGRANULAR_VOUCH` aus Stufe A
verschwinden. Weicht eines davon ab, ist der Text nach D437, D398 oder D439 nicht so lesbar, wie
er gemeint ist. Die schwächste Stelle ist D439 Beschluss 1, an einer einzigen Fassung entschieden.

Stillstand bleibt ein gültiger Zustand.
