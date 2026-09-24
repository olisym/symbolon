# Sitzungsstart: 00cg (MaR / symbolon), fortgeschrieben nach D455

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

Am Ende von `00cg`: **971 Tests**, Register **D1–D455**, Prüfregeln **1–81**, `make check` grün,
`main` beim Commit, der D455 und diesen Sitzungsstart trägt. **33 Wurzel-Markdown-Dateien, alle
gebunden**; `archiv/` steht bei 144 mit `sitzungsstart-00cf.md`. `offen.md` führt **82 Posten**,
davon **14 offen**. O79 bis O82 sind in dieser Sitzung entstanden und geschlossen.

**Stränge:** `main` und `00bo-hs` (kontaminiert, D374, wird nicht gelöscht). Gemergt und stehen
gelassen, neu in dieser Sitzung: `o79-bindung`, `o80-fenster`, `o81-uebergehen`, `o82-schliessen`.

**Rust-Fassung:** Isolat `~/mar-rs` auf `77f572d`, Anker `573db57` (D441). Sie hat den Text aus
D443, D450 und D452 nicht gelesen. Ungeprüft ist, ob sie `core/revoke@2` annimmt und ob ein fremder
Lebenszyklus-Claim ihre Auswertung anhält.

## Was in dieser Sitzung geschah

- **D448, D449:** Bindungsmessung über `02 §8` und `§10`, 41 Mutationen, sieben ungebunden, darunter
  die Knotendisjunktheit. Gebunden in `tests/trust/test_bindung.py`.
- **D450, D451:** zweiter Teil über `§3`, `§4`, `§5`, `§8.1` und `§11`, 44 Mutationen. Drei
  Bindungslücken und eine Normlücke: `disjoint_paths` im Fenster ist jetzt ein eigenes Minimum über
  die Punkte (`02 §11.1`), weil es eine Gate-Grösse ist.
- **D452, D453:** Messung über `01`, 53 Mutationen. Beim Lesen gefunden: Ein fremder
  Lebenszyklus-Claim legte `classify_all` und damit jede Auswertung auf dem Knoten still. Jetzt ist
  ein nachträglich ungültiger Claim nicht gehalten (`01 §6`, `02 §11.4`).
- **D454:** `core` wird gegen `{revoke@1, supersede@1}` geprüft, Map-Schlüssel sind uint, sechs
  Bindungen aus `01`.
- **D455:** Prüfregel 81, Sitzungsschluss.

## Werkzeugnotizen

- **Mutationsläufe im Supervisor-Klon.** Die Skripte liegen nicht im Repositorium. Immer mit
  `PYTHONDONTWRITEBYTECODE=1` und geleertem `__pycache__` (Prüfregel 81). Der schnelle Umfang, alle
  Wurzeltests und `tests/trust`, braucht rund 19 Sekunden, die volle Suite rund 50. Ein Aufruf des
  Tool-Sandkastens bricht nach 300 Sekunden ab, und ein Hintergrundprozess stirbt mit ihm. Längere
  Läufe also in Teilstücken.
- **Ein Bericht kann einen unvollständigen Diff tragen.** In D453 fehlten im letzten Hunk die
  Kontextzeilen. Dann `git apply --recount`, notfalls die Datei von Hand setzen und über ihren Blob
  verankern (Prüfregel 59).
- **Der Rust-Lauf im Isolat**, falls er wieder gebraucht wird:
  `docker run --rm -it -v ~/mar-rs:/work -v mar-rs-auth:/root/.local/share/opencode
  -v mar-rs-cargo:/usr/local/cargo/registry mar-rs-box opencode`. Darin eine neue Sitzung im
  Build-Modus. Bauen ohne Modell: dieselben Mounts ohne `-it`, Befehl `cargo build --release -q`.
- **Vergleich mit der Referenz:** `trustflow02 <vektordatei>` gegen `tools/ref_block.py`, beide
  ohne die `inf`-Zeile, dann `diff` ungekürzt.
- **`AGENTS.md` trägt weiter.** Vier Läufe in Cursor, je ein frischer Chat. Jeder meldete eine
  Abweichung von meiner Rücknahmetabelle, statt anzupassen, und jede war berechtigt.
- **Ein Bericht kommt oft vor dem Push.** Vor dem Lesen `git ls-remote origin` gegen den
  gemeldeten Commit prüfen. Liegt er nicht vor, nach Prüfregel 59 aus dem Diff nachbauen.
- **Supervisor-Klon:** `.venv` mit `--system-site-packages`, darin `ruff cbor2 cryptography
  pytest hypothesis`. Vollständig holen mit
  `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`. Für Probe-Commits im Klon eine lokale
  Git-Identität setzen.
- **Lieferungen:** in `/tmp`, Hashprüfung von Lieferung und Basis vor jeder Änderung, `rm` als
  letzter Job vor `== FERTIG ==`. Merge und Push als eigene Befehle. Legt ein Block einen Branch
  für einen Werkzeuglauf an, schaltet er auch auf ihn um.

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
  In `00cg` wieder gerissen: Die Bilanz in D455 übernahm zuerst die zwölf Lücken aus D451, die nur
  `02` zählten.
- Ein Lauf, der ungefragt etwas entfernt, ist Scope-Verlust und gehört in den Bericht wie ein
  Zuwachs (D435).
- Ein Vergleichs-`diff` wird nicht mit `head` gekürzt (D440).
- Eine Bedingung, an die ein vertagter Posten geknüpft ist, wird gegen alle Einträge seit ihrer
  Setzung geprüft (D437).
- Ein Auftrag, der eine frühere Schnittstelle für gültig erklärt, übernimmt die Befunde über sie;
  vorher die Einträge lesen, die den alten Auftrag zitieren (D447).
- **Neu aus D455:** Wer eine Ausnahme in einer Auswertung über den ganzen Bestand wirft, fragt, wer
  sie auslösen kann und was dann anhält (D452).
- **Neu aus D455:** Eine Mutationsmessung ersetzt das Lesen gegen die Norm nicht; sie findet nur
  ungebundenen richtigen Code (D452).

## Offene Punkte

**Die 14 offenen Posten** sind Wartestände:
- O31, O34 bis O40 und O42 sind bewusst vertagt, jeder mit seiner Bedingung.
- O25 ist ein Bau ohne Anlass.
- O52 und O53 gehören zur Öffnung.
- O56 ist der PyPI-Name.
- O74 ist ein Stolperdraht.

**Merkposten Restack:** eingereicht am 10. September, Code `2026-11-0c4` (D349), Frist
3. November. Mitte Oktober nur prüfen, ob der Antrag den Stand grob falsch beschreibt. Seit `00cg`
kommt eine Frage hinzu: ob er eine Eigenschaft behauptet, die der Angriff aus D452 bis dahin
widerlegt hätte.

**Aus D408 getragen:** Die Zahl der Auswertungen über ein Fenster hängt am Bestand und hat keine
Obergrenze. Beisst es je, gehört die Grenze nach `02 §8`.

**Aus D444 getragen, erweitert:** Ein Nachzug der Rust-Fassung auf den Text aus D443, D450 und D452
wird erst beauftragt, wenn eine Entscheidung an ihm hängt (D409 Beschluss 3).

## Der nächste Schritt

Kein Posten verlangt einen. Geprüft gegen `offen.md` und das Register-Ende: Die 14 offenen Posten
haben Bedingungen, die nicht erfüllt sind, und D455 hinterlässt keinen Folgeauftrag.

Wenn gearbeitet wird, dann in dieser Reihenfolge der Lohnenswertigkeit:

1. **`03` und `04` lesen, dann messen.** Profile und Governance stehen auf `classify_all` und
   bekamen in D452 nur die eine Anpassung in `keys.py`. Die Erfahrung aus `01` ist, dass das Lesen
   gegen die Norm die Defekte findet und die Mutation die Lücken. Zuerst also das Lesen, mit der
   Frage aus D452: Welche Ausnahme kann ein fremder Claim auslösen, und was hält sie an? Danach die
   Messung nach Prüfregel 81.
2. **Mitte Oktober:** der Restack-Abgleich.

Stillstand bleibt ein gültiger Zustand.
