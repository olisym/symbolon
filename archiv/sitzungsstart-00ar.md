# Sitzungsstart: 00ar (MaR)

## Was das hier ist

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Gitea unter `git.h.error13.de`, Arbeitsverzeichnis `~/mensch-als-republik`.
Seit `00ar` liegt die Go-Zweitimplementierung im selben Baum unter `go/` (vormals eigenes
Repositorium `~/mar-go`; dessen Gitea-Fortbestand ist offen, siehe unten). Seit `00ar`
zusätzlich öffentlich gespiegelt: `github.com/olisym/mensch-als-republik`, per Gitea-Push-
Mirror, bislang ohne spürbaren Sync-Verzug.

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Prompts und führst die Abnahmen. Du schreibst keinen
Produktivcode.

**Diese Datei ist kurz, seit D316.** Die stabile Disziplin steht in `arbeitsweise.md`, die
Prüfregeln 1 bis 64 im Volltext in `pruefregeln.md`, die offenen Posten in `offen.md`. Hier steht
nur der Stand, was zuletzt entschieden wurde, und der nächste Schritt.

**Diese Datei ist eine Hypothese, keine Messung.** Prüfregel 27 gilt auch für sie und für jeden
Posten, den sie nennt. Der Kopf wird gemessen, nicht abgeschrieben (Prüfregel 40).

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Ablesen, nicht schätzen. Vor der Testzahl `.hypothesis` und `__pycache__` löschen
(Prüfregel 19). Der Interpreter ist `.venv/bin/python`.

**Seit D322 lässt `repomix.config.json` `07-decisions.md` aus der gepackten Projektkopie aus**
(rund 218.000 Tokens gespart). Die Datei bleibt im Repository vollständig; `tools/register_index.py`
oder gezielte Auszüge ersetzen den Volltext im Kontext. `tools/stand.py` liest die Registerzahl
weiterhin direkt aus der Datei, unabhängig von der Packung.

Der Stand am Ende von `00ar`, gemessen: `5106491`, **797 Tests**, Register **D1–D325**,
Prüfregeln **1–64**, **58 Posten**, **drei Branches**. In der Wurzel liegen 31 Markdown-Dateien,
davon 30 gebunden (`00ar-always-bound-prompt.md` bleibt ungebunden bis zur nächsten Übergabe).

Die Ausgangslage war `6428a1f`, 320 Registereinträge, 32 Wurzeldateien, davon 29 gebunden.

### Die Schichten

- **00** Nukleus, Genesis, Verfassung. `00 §4.2` empfiehlt Governance und Substanz in getrennte
  Scopes — Obligationen gehören **nicht** in den Scope, dessen `participants` abgestimmt werden.
- **01** Atom, Verifier, **zwölf Reject-Codes**, **sieben** Klassifikationszustände. Anhang C
  trägt **sechzehn** Abschnitte. Seit D308 die Versionsausnahme.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II. `03 §3.1` Preisblindheit, `03 §3.2` Trägerwert extern, `03 §3.3` Kredit.
- **04** Governance. Ein Vorschlag besteht aus Scope, Vorgängerepoche und Verfassungshash.
- **08** Zweck und Geltungsbereich. `08 §3` trägt das Aufnahmekriterium und die Prüftabelle.
  **Achtung, Fund aus `00ar` (D324):** `08 §2.2` ist Equivocation, **nicht** die Anwendungs-
  bedingung „echte Menschen mit Anliegen" — diese steht in **D237**, unbeziffert (kein „vier").
  Über zwanzig alte Prompt-Dateien zitieren das falsch; sie bleiben unkorrigiert liegen (Altlast).

### Der Bestand

`tools/`: unverändert seit `00aq` — `autor.py`, `check_specs.py`, `check_tree.py`,
`example_nucleus.py`, `gitter.py`, `korpus.py`, `offen.py`, `paare.py`, `register_index.py`,
`splice_run.py`, `stand.py`, `szenario_absicherung.py`, `verdikt.py`, dazu `sim/`.
`check_specs.py` hat einen neuen `ALWAYS_BOUND`-Eintrag (`CONTRIBUTING.md`), sonst unverändert.

**Neu seit `00ar`:** `README.md` und `CONTRIBUTING.md` (Wurzel), `docs/METHOD.md`,
`repomix.config.json`. Alle drei Prosa-Dateien sind für ein englisches Publikum geschrieben,
nicht übersetzt — die Werkstatt bleibt deutsch. `go/` trägt die Go-Zweitimplementierung mit
erhaltener Historie (fünf Commits, blob-identisch zum vormaligen `~/mar-go` geprüft).

**Die Mutantenkampagne steht unverändert über beide Stufen.** `gitter.py` liefert 2511
Einzelmutanten, `paare.py` 16958 Paarmutanten. Über 19469 Mutanten hat sie keinen einzigen Befund
aus einem Verdikt-Unterschied getragen. Layer 01 ist damit ausgelesen — unverändert seit `00aq`.

## Was zuletzt entschieden wurde

- **D321** — O58 ausgeführt: `mar-go` per `filter-repo` + Merge zu `go/`, nicht per `subtree`.
  Fünf Commits erhalten, blob-geprüft. Offen bleibt, was mit dem eigenständigen Gitea-
  Repositorium `mar-go` geschieht (archivieren, umbenennen, stilllegen — nicht entschieden).
- **D322** — Repomix schließt `07-decisions.md` aus der Projektkopie aus. Register bleibt
  vollständig im Repository; nur die gepackte Kopie schrumpft.
- **D323** — O57 neu gemessen: NGI Zero (Commons Fund) ist beendet, Nachfolger „Open Internet
  Stack" mit `Restack` als beste Passung. Nächste Frist **3. November 2026**. O52 und O53
  bleiben Voraussetzung für einen Antrag.
- **D324** — Zitierfehler gefunden: `08 §2.2` wurde über zwanzig Mal fälschlich als Quelle für
  „vier Menschen mit Anliegen" zitiert. Echte Quelle ist D237, unbeziffert. README und
  CONTRIBUTING korrigiert; alte Prompt-Dateien bleiben unkorrigiert (Altlast, kein Posten wert).
- **O52 ausgeführt** — Gitea-Push-Mirror auf `github.com/olisym/mensch-als-republik`, sofort
  synchron beim ersten beobachteten Push.
- **O53 ausgeführt** — `README.md`, `CONTRIBUTING.md`, `docs/METHOD.md` geschrieben, abgenommen,
  gemergt. Ton bewusst warm statt transaktional (Nutzerentscheidung): kein Verweis auf den
  Förderantrag als Grund der Veröffentlichung.
- **Aufräumen (D316 nachgeholt)** — drei ungebundene Wurzeldateien nach `archiv/` verschoben
  (`00aq-nachtrag-prompt.md`, `00aq-werkzeuge-prompt.md`, `sitzungsstart-00ap.md`). Mit dieser
  Übergabe zusätzlich: `sitzungsstart-00aq.md` archiviert, diese Datei tritt an ihre Stelle.
- **D325** — nach Abschluss der Öffnung: direkter Klon/Pull des öffentlichen Spiegels ersetzt
  Repomix als Standardweg, mit HEAD-Hash-Abgleich vor jedem Lesen. `arbeitsweise.md` und
  `README.md` (Erklärung der flachen Prompt-/Golden-Anchor-Struktur) entsprechend angepasst.
  **Diese Übergabedatei wurde danach noch einmal nachgezogen** — der Kopf oben ist der
  wirkliche Endstand, nicht der Stand vor D325.

## Der nächste Schritt

**Szenario A tatsächlich laufen lassen.** Branch `00an-szenario-a` und Prompt
`00an-szenario-a-prompt.md` stehen seit vor `00ar`, noch ungelaufen — die Vorarbeit aus `00ar`
war Öffnung, nicht Forschung. Zwei-Phasen-Vergleich: Fonds mit Verwahrer gegen Obligation ohne.
Scenario-Modus gilt (D311): Szenario-Code ist Wegwerfware, nur Befunde gehen ins Register, keine
Golden Numbers oder Rücknahmeproben für Prototypen.

**Danach, nicht davor:** Entwurf der Restack-Bewerbung (O57), gestützt auf die Befunde aus
Szenario A statt nur auf Architektur. Frist 3. November 2026 — reichlich Vorlauf bei jetzigem
Start.

**Nebenbei, niedrige Dringlichkeit:** Stufe B als Spec-Arbeit (D313), die drei Befunde ohne Ort
aus D312 (O1–O3) durch `08 §3` schicken, die Entscheidung über das `mar-go`-Repositorium bei
Gitea (aus D321 offen), O54 (normative Sprache) und O55 (Umbenennung `symbolon`) — beide jetzt
technisch entsperrt, da die Öffnung erledigt ist, aber keins zeitkritisch.

**Die Anwendung mit echten Menschen bleibt zurückgestellt.** D237 verlangt ein echtes
gemeinsames Anliegen, nicht Neugier an der Technik. Sichtbarkeit — jetzt öffentlich auf GitHub —
ist der Mechanismus, über den das entstehen könnte, nicht ein Termin, den man setzt.
