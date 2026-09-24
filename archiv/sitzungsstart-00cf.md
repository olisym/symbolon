# Sitzungsstart: 00cf (MaR / symbolon), fortgeschrieben nach D447

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

Am Ende von `00cf`: **942 Tests**, Register **D1–D447**, Prüfregeln **1–80**, `make check` grün,
`main` beim Commit, der D447 und diesen Sitzungsstart trägt. **33 Wurzel-Markdown-Dateien, alle
gebunden**; `archiv/` steht bei 143 mit `sitzungsstart-00ce.md`. `offen.md` führt **78 Posten**,
davon **14 offen**. O73 ist in dieser Sitzung geschlossen; O77 und O78 sind in ihr entstanden
und geschlossen.

**Stränge:** `main` und `00bo-hs` (kontaminiert, D374, wird nicht gelöscht). Gemergt und stehen
gelassen, neu in dieser Sitzung: `o77-autorflag`, `o78-fragen`.

**Rust-Fassung:** Isolat `~/mar-rs` auf `77f572d`, Anker `573db57` (D441). Sie hat den Text aus
D443 (`01 §4`, `02 §8`, `§10`, `§11.4`) nicht gelesen.

## Was in dieser Sitzung geschah

- **D441:** Stufe B von O73. Die Diät ist neu gefasst: Der Ankersatz enthält `§11`,
  zurückgehalten bleiben die Ankerdatei und `02a`. Gewählt ist ein Nachzug statt eines Neubaus,
  der Detektor aus D389 ist neu abgeleitet.
- **D442:** Abnahme des Nachzugs. F1 und D439 tragen. F2 weicht weiter ab, weil `02 §8`
  `equivocation-flagged` als Eigenschaft eines Autors gebrauchte. Acht Kanten mit `cap 0` gehen
  auf den Auftrag zurück, der D396 Beschluss 2 übergangen hat. O73 ist erledigt, O77 und O78 sind
  neu.
- **D443:** Das Autor-Flag ist in `02 §8` normiert, `01 §4` trennt Autor und Zustand. D442 ist
  berichtigt: Die Definition stand schon in `01`. Beide Wirkungen waren ungebunden.
- **D444:** Abnahme `o77-autorflag`, drei Tests mit drei Rücknahmeproben. O77 ist erledigt.
- **D445, D446:** `check_fragen` kennt Änderungseinträge, der Index führt sie als Abschnitt 2.
  `rs/FRAGEN.md` liegt im Baum. O78 ist erledigt.
- **D447:** Prüfregel 80, Sitzungsschluss.

## Werkzeugnotizen

- **Der Rust-Lauf im Isolat**, falls er wieder gebraucht wird:
  `docker run --rm -it -v ~/mar-rs:/work -v mar-rs-auth:/root/.local/share/opencode
  -v mar-rs-cargo:/usr/local/cargo/registry mar-rs-box opencode`. Darin eine neue Sitzung im
  Build-Modus; eine alte fortzusetzen wäre eine Abkürzung am Text vorbei. Bauen ohne Modell:
  dieselben Mounts ohne `-it`, Befehl `cargo build --release -q`.
- **Vergleich mit der Referenz:** `trustflow02 <vektordatei>` gegen `tools/ref_block.py`, beide
  ohne die `inf`-Zeile, dann `diff` ungekürzt.
- **`AGENTS.md` trägt weiter.** Zwei Läufe in Cursor, je ein frischer Chat, beide Diffs ohne
  Scope-Abweichung. Aufträge liegen in `~/auftraege/`.
- **Ein Bericht kommt oft vor dem Push.** Vor dem Lesen `git ls-remote origin` gegen den
  gemeldeten Commit prüfen. Liegt er nicht vor, entweder den Push abwarten oder nach Prüfregel 59
  aus dem Diff nachbauen und über den Blob der Indexzeile verankern (so in D444).
- **Supervisor-Klon:** `.venv` mit `--system-site-packages`, darin `ruff cbor2 cryptography
  pytest hypothesis`. Vollständig holen mit
  `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`.
  Vor jedem Pull eigene Entwürfe sichern, nicht verwerfen: In `00cf` ging einmal ein nicht
  gelieferter Stand über `stash drop` verloren und musste aus den Lieferungen zurückgeholt werden.
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
  In `00cf` zweimal gerissen: O73 zählte die Commits falsch (D441), und die Stand-Zeilen
  zählten O73 als offen (D447).
- Ein Lauf, der ungefragt etwas entfernt, ist Scope-Verlust und gehört in den Bericht wie ein
  Zuwachs (D435).
- Ein Vergleichs-`diff` wird nicht mit `head` gekürzt (D440).
- Eine Bedingung, an die ein vertagter Posten geknüpft ist, wird gegen alle Einträge seit ihrer
  Setzung geprüft (D437).
- **Neu aus D447:** Ein Auftrag, der eine frühere Schnittstelle für gültig erklärt, übernimmt die
  Befunde über sie; vorher die Einträge lesen, die den alten Auftrag zitieren.

## Offene Punkte

**Die 14 offenen Posten** sind Wartestände:
- O31, O34 bis O40 und O42 sind bewusst vertagt, jeder mit seiner Bedingung.
- O25 ist ein Bau ohne Anlass.
- O52 und O53 gehören zur Öffnung.
- O56 ist der PyPI-Name.
- O74 ist ein Stolperdraht.

**Merkposten Restack:** eingereicht am 10. September, Code `2026-11-0c4` (D349), Frist
3. November. Mitte Oktober nur prüfen, ob der Antrag den Stand grob falsch beschreibt.

**Aus D408 getragen:** Die Zahl der Auswertungen über ein Fenster hängt am Bestand und hat keine
Obergrenze. Beisst es je, gehört die Grenze nach `02 §8`.

**Aus D444 getragen:** Ein Nachzug der Rust-Fassung auf den Text aus D443 wird erst beauftragt,
wenn eine Entscheidung an ihm hängt (D409 Beschluss 3). Der Stolperdraht ist der aus O73.

## Der nächste Schritt

Kein Posten verlangt einen. Geprüft gegen `offen.md` und das Register-Ende: Die 14 offenen
Posten haben Bedingungen, die nicht erfüllt sind, und D447 hinterlässt keinen Folgeauftrag.

Wenn gearbeitet wird, dann in dieser Reihenfolge der Lohnenswertigkeit:

1. **Die Bindungslücke als Muster.** D443 fand zwei Wirkungen, die kein Test sah, obwohl ein
   Vektorsatz eigens für sie gebaut war. Eine Rücknahmeprobe je Zeile von `02 §10` und je Punkt
   von `02 §8` misst, wie viele Normen der Schicht ungebunden sind. Zuerst die Messung, dann ein
   Posten.
2. **Mitte Oktober:** der Restack-Abgleich.

Stillstand bleibt ein gültiger Zustand.
