# Sitzungsstart: 00ch (MaR / symbolon), fortgeschrieben nach D461

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

Am Ende von `00ch`: **1031 Tests**, Register **D1–D461**, Prüfregeln **1–83**, `make check` grün,
`main` beim Commit, der D461 und diesen Sitzungsstart trägt. **33 Wurzel-Markdown-Dateien, alle
gebunden**; `archiv/` steht bei 145 mit `sitzungsstart-00cg.md`. `offen.md` führt **85 Posten**,
davon **14 offen**. O83 bis O85 sind in dieser Sitzung entstanden und geschlossen.

**Stränge:** `main` und `00bo-hs` (kontaminiert, D374, wird nicht gelöscht). Gemergt und stehen
gelassen, neu in dieser Sitzung: `o83-lesen`, `o84-binden`, `o85-binden`.

**Rust-Fassung:** Isolat `~/mar-rs` auf `77f572d`, Anker `573db57` (D441). Sie hat den Text aus
D443, D450, D452 und D456 nicht gelesen. Ungeprüft ist, ob sie `core/revoke@2` annimmt, ob ein
fremder Lebenszyklus-Claim ihre Auswertung anhält und ob sie `v`-Schlüssel typgenau liest oder wie
Python aliasiert.

## Was in dieser Sitzung geschah

- **D456, D457:** `03` und `04` gegen die Norm gelesen. Kein fremder Claim hält dort eine
  Auswertung an. Gefunden: `cbor2` vergleicht `v`-Schlüssel mit Pythons Gleichheit (`false == 0`),
  und ein einzelnes Mitglied konnte damit die Epoche über Implementierungen spalten. Jetzt sind
  Schlüssel in `v` in jeder Tiefe nur Integer, `bstr` oder `tstr` (`02 §3.1`, `keys_admissible`).
  Dazu: Prädikat der Anklage, Tag-Tor für `EPOCH_PROPOSAL_UNAVAILABLE`, Zeugen mit 32 Byte,
  Vermerke aller Quittungen, `genesis[6]` typgenau, der Schiedsrichter als Partei als getragene
  Grenze.
- **D458:** Mutationsmessung über `03` und `04`, 148 Mutationen, 50 Lücken (nach D459), sieben
  davon mit Wirkung. Beim Lesen: `_is_valid_uint` nahm Negative an, `03 §1.3` widersprach `§6.1`,
  die Prüfung von `participants` stand zweimal im Code.
- **D459, D460:** alles gebunden. `participants_wellformed` in `policy.py` ist die einzige Prüfung.
  Nachmessung: nur noch äquivalente und laut Norm unerreichbare Mutanten.
- **D461:** Prüfregeln 82 (Scope-Verlust) und 83 (Lesen vor Messen), Sitzungsschluss.

## Werkzeugnotizen

- **Auftragsweg:** Aufträge liegen in `~/auftraege/`, erledigte werden vor dem nächsten Lauf nach
  `~/auftraege/erledigt/` verschoben. Der Lieferblock legt den Auftrag ab, legt den Branch an und
  schaltet um. Cursor bekommt den Inhalt als erste Nachricht in einem neuen Chat im Agent-Modus,
  mit „Führe diesen Auftrag aus. Es gilt AGENTS.md." davor. Den Branch pusht Oli vom Host, danach
  lese ich im Spiegel.
- **Mutationsläufe im Supervisor-Klon.** Die Skripte liegen nicht im Repositorium. Immer mit
  `PYTHONDONTWRITEBYTECODE=1` und geleertem `__pycache__` (Prüfregel 81). Erst gegen den engen
  Umfang der Schicht, jeder Überlebende dann gegen die volle Suite. Die volle Suite braucht rund
  36 Sekunden, ein Aufruf des Tool-Sandkastens bricht nach 300 Sekunden ab, also in Teilstücken.
- **Mutanten in Aufträgen als JSON, erzeugt, nicht getippt.** Der Auftrag `o85-binden` trug die
  exakten Ersetzungen, und das Werkzeug setzte sie per Textersetzung ein. Das hat getragen. Die
  Listen selbst gehen mit dem Sandkasten verloren (D461).
- **fish und Kommandosubstitution:** `"(cmd)"` in Anführungszeichen wird nicht ersetzt. Für einen
  sauberen Baum `test (git status --porcelain | count) -eq 0`, für den Basis-Commit den vollen
  Hash.
- **Ein Bericht kann einen unvollständigen Diff tragen.** Dann `git apply --recount`, notfalls die
  Datei von Hand setzen und über ihren Blob verankern (Prüfregel 59).
- **Der Rust-Lauf im Isolat**, falls er wieder gebraucht wird:
  `docker run --rm -it -v ~/mar-rs:/work -v mar-rs-auth:/root/.local/share/opencode
  -v mar-rs-cargo:/usr/local/cargo/registry mar-rs-box opencode`. Darin eine neue Sitzung im
  Build-Modus. Bauen ohne Modell: dieselben Mounts ohne `-it`, Befehl `cargo build --release -q`.
- **Vergleich mit der Referenz:** `trustflow02 <vektordatei>` gegen `tools/ref_block.py`, beide
  ohne die `inf`-Zeile, dann `diff` ungekürzt.
- **Supervisor-Klon:** `cbor2 cryptography pytest hypothesis` per `pip --break-system-packages`.
  Vollständig holen mit `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`.
- **Lieferungen:** in `/tmp`, Hashprüfung von Lieferung und Basis vor jeder Änderung, `rm` als
  letzter Job vor `== FERTIG ==`. Merge und Push als eigene Befehle.

**Prüfregel-Kandidaten, weiter nicht übernommen:**
- An zwei Fällen Gemessenes nicht „durchgehend" nennen (D390 → D396).
- Eine Karte aus Wortsuche ist eine Vermutung; vor dem Schreiben den Wortlaut lesen (D397 → D398).
- Eine Flächenzeile, die vor dem Lesen des Codes geschrieben wird, ist eine Schätzung (D408).
- Der nächste Schritt eines Sitzungsstarts wird gegen `offen.md` und das Register-Ende geprüft
  (D409).
- Ein Strang, den ein Sitzungsstart über mehr als eine Sitzung trägt, hat eine O-Nummer oder
  einen Registereintrag (D412).
- Die englische Schale nennt keine Zahl, die mit der Arbeit wächst (D415).
- Eine Beschreibung, die eine Zahl aus einem anderen Eintrag wiederholt, veraltet mit ihm (D420).
- Ein Vergleichs-`diff` wird nicht mit `head` gekürzt (D440).
- Eine Bedingung, an die ein vertagter Posten geknüpft ist, wird gegen alle Einträge seit ihrer
  Setzung geprüft (D437).
- Ein Auftrag, der eine frühere Schnittstelle für gültig erklärt, übernimmt die Befunde über sie;
  vorher die Einträge lesen, die den alten Auftrag zitieren (D447).
- **Neu aus D457:** Ein Vektor im Register wird aus der Messausgabe kopiert, nicht abgeschrieben.
- **Neu aus D459:** Eine Lücke, deren Normspalte auf einen Satz zeigt, wird gegen dessen Wortlaut
  geprüft, bevor sie in einen Auftrag geht.

## Offene Punkte

**Die 14 offenen Posten** sind Wartestände:
- O31, O34 bis O40 und O42 sind bewusst vertagt, jeder mit seiner Bedingung.
- O25 ist ein Bau ohne Anlass.
- O52 und O53 gehören zur Öffnung.
- O56 ist der PyPI-Name.
- O74 ist ein Stolperdraht.

**Merkposten Restack:** eingereicht am 10. September, Code `2026-11-0c4` (D349), Frist
3. November. Mitte Oktober prüfen, ob der Antrag den Stand grob falsch beschreibt und ob er eine
Eigenschaft behauptet, die D452 oder D456 widerlegt hätten: dass kein fremder Claim eine Auswertung
anhalten kann, oder dass zwei Implementierungen aus denselben Bytes dasselbe lesen. Der Antragstext
liegt nicht im Repositorium; Oli bringt ihn mit.

**Aus D408 getragen:** Die Zahl der Auswertungen über ein Fenster hängt am Bestand und hat keine
Obergrenze. Beisst es je, gehört die Grenze nach `02 §8`.

**Aus D444 getragen, erweitert:** Ein Nachzug der Rust-Fassung auf den Text aus D443, D450, D452 und
D456 wird erst beauftragt, wenn eine Entscheidung an ihm hängt (D409 Beschluss 3).

## Der nächste Schritt

Kein Posten verlangt einen. Geprüft gegen `offen.md` und das Register-Ende: Die 14 offenen Posten
haben Bedingungen, die nicht erfüllt sind, und D461 hinterlässt keinen Folgeauftrag.

Wenn gearbeitet wird, dann in dieser Reihenfolge der Lohnenswertigkeit:

1. **`keys.py` und `resolve.py` lesen, dann messen.** Die Schlüsselauflösung aus `00 §6.4` und der
   Nukleus-Akt aus `04 §5` sind der letzte Code, der weder gelesen noch gemessen ist. Nach
   Prüfregel 83 zuerst das Lesen gegen `00 §6` und `04 §5`, mit der Frage, wer eine Ausnahme oder
   eine Abweichung auslösen kann. Danach die Messung.
2. **Mitte Oktober:** der Restack-Abgleich.

Stillstand bleibt ein gültiger Zustand.
