# Durchsetzungsschicht — Spezifikation v1

Status: Entwurf · Protokollversion: 1 · Layer: Durchsetzung (schließt den Loop über allen anderen)

Diese Schicht führt **fast keinen neuen Mechanismus** ein. Sie ist die *Choreografie* — der
Lebenszyklus, der die Auslöser und Antworten der unteren Schichten (Equivocation-Beweis,
Bond-Slash, `t_exp`, Trust-Entzug, Verdikt, föderierter Appeal) zu einem geschlossenen Kreis
verkettet. Governance war die Voraussetzung: man muss wissen, *welche* Regeln gelten, bevor man
ihren Bruch ahndet.

Vier Prinzipien tragen die Schicht:

- **Verhältnismäßig durch Einstiegspunkt**, nicht durch Zwangsreihenfolge (§3).
- **Bidirektional durch Cure** — jede Stufe unter dem Physischen ist umkehrbar (§4).
- **Zwei Propagationsklassen** — Fakten vs. attribuierte Meinungen, gegen Diffamierung (§5).
- **Individuelle Haftung, eine Sprunghöhe** — keine Sippenhaft (§6).

---

## 1. Die fünf Stufen

Severity steigt nach oben. Jede Stufe nutzt ein **bestehendes** Primitiv.

| Stufe | Mechanismus (bestehend) | Cure |
|------:|-------------------------|------|
| 1 · **Reputationsverlust** | Beta-Reputation / Subjective-Logic-Update, **lokal je Beobachter** | Zeit (λ-Zerfall) + frische positive Evidenz |
| 2 · **Vertrauensentzug** | Bürgen widerrufen (`core/revoke`) oder Vouches laufen ab (`t_exp`); `t_s`-Fluss versiegt | Vertrauen neu verdienen (frische Vouches) |
| 3 · **Bond-Slash** | Slash des Bonds hinter Vouch/Obligation (mechanisch bei Equivocation, per Verdikt bei subjektiv) | Restitution + signierte Anerkennung |
| 4 · **Ausschluss** | Nukleus widerruft `grant-membership`; Abschneiden von Diensten (Versicherung, Schlichtung, Handel/Kredit) | Wiederaufnahme = neues `grant-membership` + `accept-rules` nach Restitution/Zeit |
| 5 · **Physische Abwehr** | portables, bond-bewehrtes **Mandat** (Governance-Akt); **Menschen** handeln | — (kein Cure im Protokoll; Mandat gegen-adjudizierbar) |

Keiner dieser Punkte ist ein neues Atom-Feld. Das Mandat ist Komposition (§7).

---

## 2. Reputation & Trust als Stufen 1–2 (Selbstheilung eingebaut)

Stufe 1 ist eine reine *Neubewertung* im Kopf jedes Beobachters (kein globaler Akt). Stufe 2
lässt den zweck-gescopten `t_s`-Fluss zum Akteur versiegen — teils automatisch (`t_exp`), teils
durch aktive Widerrufe der Bürgen (der Missbrauchsfall aus Profile-II §7.1). Beide sind schon
gebaut; die Durchsetzungsschicht *ordnet* sie nur als erste, weichste Antworten ein.

---

## 3. Gestufter Einstieg (E1)

Der **Auslösertyp bestimmt den Einstiegspunkt** — dann wird nur weiter eskaliert, solange der
Akteur nicht kuriert/nachkommt. Keine Zwangskletterei durch sinnlose weiche Sprossen.

| Auslöser | Einstieg |
|----------|----------|
| Norm-Reibung / einzelner negativer Ausgang | Stufe 1 |
| Subjektiver Vorwurf (oracle-abhängig) → **braucht Verdikt** | Stufe 2, per Verdikt-Severity höher |
| **Equivocation** (selbst-validierend, Profile-II §2.3) | **direkt Stufe 3** (mechanischer Slash, kein Verdikt) |

Verhältnismäßigkeit entsteht so durch den *Einstiegspunkt*, nicht durch eine starre Reihenfolge.

**`OPEN` ist kein negativer Ausgang (D423).** Eine offene Obligation sagt nicht, ob nicht gezahlt,
nicht quittiert oder nur nicht zugestellt wurde (`08 §7`). Nichtleistung ist ein subjektiver
Vorwurf und tritt über `accusation@1` ein, also in der zweiten Zeile dieser Tabelle.

---

## 4. Cure & Rückfälligkeit (E2 — rehabilitativ mit steigenden Kosten)

Jede Stufe unter dem Physischen hat einen **definierten Cure**, der die Eskalation anhält und
umkehren kann — die Leiter ist **bidirektional**, keine Einweg-Ratsche. Das ist die strukturelle
Form von „positives Verhalten wird belohnt".

Cure-Typen: **Restitution** (geslashten Betrag/Schuld erfüllen), **signierte Anerkennung**, oder
**Zeit + frische positive Evidenz** (Trust-Flow §7).

**Gegen Gaming (defektieren, billig kurieren, wiederholen):**
- Die Beta-Reputation mit Vergessensfaktor `λ` akkumuliert Rückfälle und klingt nur langsam ab ⇒
  **Cure-Kosten steigen mit Rückfälligkeit** (ein akkumulierter, langsam zerfallender
  Reputations-Schuldstand).
- Die Policy darf einzelne Fehler als **terminal** (nicht kurierbar) markieren.

Ohne Rückweg erzeugt das System permanente Ausgestoßene, die sich zu gegnerischen Nuklei formieren
(die Clan-Dynamik) — deshalb ist der Cure kein Weichspüler, sondern Stabilitäts-Design.

---

## 5. Propagation & Schutz gegen Waffenwirkung (E3)

Ein verbreiteter „Schuld-Beweis" ist auch ein Diffamierungsvektor. Zwei Klassen trennen das sauber:

- **Objektive, selbst-validierende Beweise** (Equivocation) reisen als **Fakten**: jeder
  verifiziert unabhängig, Prioritäts-Propagation wie Widerrufe. Kein Diffamierungsrisiko — es ist
  Mathematik.
- **Subjektive Verdikte** reisen als **attribuierte Meinungen**, deren Gewicht das Vertrauen des
  *Beobachters in den Schiedsrichter* ist — **nie** eine globale Score-Änderung. Ein Verdikt von Z
  zählt für mich nur, insofern ich Z gewichte. Das ist die strukturelle Abwehr gegen
  Diffamierung-per-Broadcast und bewahrt das Nicht-Monopol.

**Anklage-Stake:** `accusation@1` stakt die Reputation des Anklägers (plus optional einen Bond) —
eine böswillige Anklage ist **selbst** ein Fehler und richtet die Leiter gegen den Ankläger. Das
verteuert Missbrauch der Durchsetzung selbst.

---

## 6. Haftungsreichweite (E4 — strikt individuell, eine Sprunghöhe)

Hat `V` für `J` **mit Bond** gebürgt und `J` defektiert, dann slasht `V`s Bond mit — das ist `V`s
skin in the game (Trust-Flow §6.1). Aber:

- **nur** der direkt bürgende `V` mit **explizitem** Bond haftet,
- **gedeckelt** durch den Bond-Betrag,
- **keine** transitive/kollektive Haftung darüber hinaus.

Das hält Bürgen verantwortlich (sorgfältiges Vouchen), verhindert aber Sippenhaft-Kaskaden.

---

## 7. Stufe 5 & die Übergabe ans Physische (E5, aus C2)

Das Protokoll tut **nie** Physisches. Es produziert ein **portables, selbst-verifizierbares,
bond-bewehrtes, mehrfach-signiertes Mandat** — ein hochschwelliger Nukleus-/Föderations-Akt
(Verdikt + Schwellen-Cosignaturen, Governance §3; **Komposition, kein neues Primitiv**) — plus die
freigegebenen Bonds plus den propagierten Beweis.

*Menschen* — konkurrierende Schutzgemeinschaften — handeln darauf; **jeder Durchsetzer prüft die
Legitimität unabhängig** (Nicht-Monopol; keiner ist die Quelle der Wahrheit).

**Zwei eingebaute Bremsen vor Stufe 5:**
1. Der **föderierte Appeal** (Governance §7) muss durchlaufen sein.
2. Das Mandat ist **gegen-adjudizierbar** (es kann selbst angefochten werden).

**Ehrlicher Residual (nicht wegbügelbar):** Das Protokoll kann eine *fälschlich mobilisierende
Mehrheitskoalition* nicht verhindern — das ist das irreduzible politische Risiko **jeder** Ordnung,
auch der staatlichen. Appeal, Selbst-Verifizierbarkeit und lokale Gewichtung **begrenzen** es, sie
eliminieren es nicht. Die Executive-Säule wird dezentral beantwortet als *föderierter, jederzeit
kündbarer Pool* von Abwehrbereitschaft — nicht als Monopol.

---

## 8. Bewusst getragene Grenzen & Designentscheidungen

- **Trigger→Einstieg-Mapping** (§3) ist die konkrete Instanziierung von E1; die Schwellen für
  „Verdikt-Severity → höhere Stufe" sind Policy, in der Verfassung deklariert.
- **Cure-Kostenfunktion** (§4) — „steigt mit λ-Schuldstand" ist eine gewählte Form; die konkrete
  Kurve ist ein Policy-Knopf. Terminale Fehler sind ein Policy-Opt-in.
- **Das Mandat ist kein neues Primitiv** — es ist ein Governance-Akt (§7). Falls ein expliziter
  Wrapper gewünscht ist, `fed:N/enforcement-mandate@1` mit `J = [claim-ref, verdict]`, aber die
  Autorisierung bleibt die Schwellen-Komposition aus Governance §3.
- **Der irreduzible Residual** (§7) ist die ehrliche Grenze: Kryptografie koordiniert, beweist,
  bindet und eskaliert bis Stufe 4 — den physischen Vollzug tut unvertretbar der Mensch, und gegen
  eine hinreichend große fehlgeleitete Koalition hilft kein Protokoll.
- **Kein Cure auf Stufe 5** im Protokoll — die einzige Rückbindung dort ist die Gegen-Adjudikation,
  die den Fall wieder in die unteren, kurierbaren Stufen zurückholen kann.
