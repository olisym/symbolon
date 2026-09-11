# Offen

Die offene Liste. **Fortgeschrieben, nicht neu geschrieben** (D316 Beschluss 1). Ein Posten kommt
hinzu oder wird gestrichen; die anderen werden nicht angefasst.

**Nummern werden nie wiederverwendet.** Ein gestrichener Posten bleibt als Zeile stehen, mit dem
Registereintrag, der ihn geschlossen hat. Damit bleibt ein Verweis wie `offen O26` dauerhaft
lesbar.

**Die Schliessform.** Ein erledigter Posten behält seine Kopfzeile, bekommt den Zusatz
„erledigt" mit dem Registereintrag, der ihn geschlossen hat, und einen Rumpf von einer Zeile. Der
alte Text fällt weg; wer ihn braucht, findet ihn in der Historie.

Zählvorschrift: `grep -c '^### O' offen.md`. Sie zählt **Identitäten**, nicht offene Punkte:
erledigte Posten bleiben stehen, also steigt die Zahl monoton. Genau deshalb taugt sie als
Kaltzahl — sie kann nur durch eine verlorene Fortschreibung fallen (D318).

Ein Posten ist eine Vermutung über eine Lücke, keine Entscheidung. Entscheidungen stehen in
`07-decisions.md`.

---

## A — Anwendungsabschnitt

### O1 Es gibt kein Gruppen-Soll — erledigt (D327)

Verteilt Macht, gehört nicht ins Protokoll; kein neuer Mechanismus nötig. Die Umlage aus
bilateralen Zusagen ist die Antwort, kein Ersatz. Aus D312, entschieden in D327.

### O2 Es gibt keine Verwahrerrolle — erledigt (D327)

Konzentriert Macht über die Auszahlungsentscheidung. Ort: Policy, in einem eigenen Scope,
getrennt von `participants` (`00 §4.2`). Aus D312, entschieden in D327.

### O3 `OPEN` unterscheidet Verweigerung nicht von Partition

Das begrenzt, was Reputation aus Nichtleistung ableiten darf. Aus D312.

### O4 Gleicher Zustand bei allen Beobachtern ist eine Eigenschaft der Verteilung

Nicht von `settlement`. Das Protokoll erzwingt die Kopie nicht. Aus D312.

### O5 Preisblindheit trägt keine Versicherungsphase

`03 §3.1` ist die Stelle, an der die Spec eine Versicherungsphase nicht mehr trägt. Aus D312.

### O6 `settlement` prüft keine Mitgliedschaft

Eine Obligation eines Nichtmitglieds ist ebenso `OPEN` oder `SETTLED`. Aus D312.

### O7 Ohne `t_exp` bleibt eine Obligation ohne Ende offen

Ein Gläubiger-Timeout gibt es nicht. Aus D312.

### O8 `tools/szenario_absicherung.py` ist Wegwerfcode

Wird nicht fortgeschrieben. Jeder weitere Szenariolauf setzt auf `tools/sim/` auf.

---

## B — Verifikationsabschnitt

### O9 Anhang C ist gegen Generatordrift nur teilweise gesichert

Für C.1 gibt es einen Test mit getipptem Hex; für C.13 bis C.15 gibt es nichts, was den Spec-Text
an `vectors_01.json` bindet. Die andere Achse ist seit D295 geschlossen: Datei gegen Generator.

### O10 `UNPARSABLE_V` entsteht bei `ratify@1` nicht

D276.

### O11 `cbor_canon.decode` ist tolerant und bleibt es

### O12 `FOREIGN_LIFECYCLE` hat keinen Vektor und kann keinen bekommen

D263, D268. Auch vom Gitter unerreichbar, weil es einen Speicher braucht.

### O13 `EPOCH_FORK` hat keinen Produktivträger

D138, D176, D281.

### O14 `SUBGRANULAR_VOUCH.subject` ist ungeprüft

D173.

### O15 Sechs Zeilen mit wahrer Expiry-Inkohärenz

Die Zweitfassung wählt anders; beide Codes sind wahr, die Spec stellt frei, der Grund des
Unterschieds ist ungeklärt.

### O16 N09 ist beobachtet, nicht durchgesetzt

D119, D246.

### O17 N10 ist teilgemessen

D246.

### O18 `RATIFY_WITH_EXPIRY` und der Zeugenpfad tragen die Weitergaberegel ungeprüft

D203.

### O19 Vergleiche gegen `dedupe_sort` sind für die Reihenfolge zirkulär

D196.

### O20 Vier `Finding`-Klassen, drei `dedupe_sort`

D183, mit D207 berichtigt.

### O21 Die Eigenschaftstests zu `INV-04.7` und `INV-04.8` prüfen eine schwächere Aussage

Schwächer als sie scheinen. D117.

### O22 Dreifache Kantensumme in `test_deckenelastizitaet.py`

D142, nicht blockierend.

### O23 Die Sondierwelt in `test_benennung.py` erzeugt keine Vermerke

D173.

### O24 `disjoint_paths` bewegt sich nicht

Bleibt `1` in allen gemessenen Fällen.

### O25 Der Sicherungsblob mit Seed und Spitze

D120, beschrieben und ungebaut.

### O26 `D >= C₀` ist ein SHOULD und wird nirgends geprüft

`00 §4.0` und `02 §8`. D147.

### O27 `anchor_set` (`genesis[3]`) bleibt ungebunden

D147.

### O28 `TrustParams.__post_init__` und `00 §4.0` prüfen dieselbe Wohlgeformtheit zweimal

D147.

### O29 `genesis[4]` und die Auszählung

`GV-24` führt ein Genesis, dessen deklarierte Verfassung in der Auszählung nirgends vorkommt.

### O30 Der Beispielnukleus kann Epoche-1- von Epoche-2-Policy nicht unterscheiden

D169, D188.

### O31 Eine Schwelle für Autoritätslisten

Mit D166 zurückgestellt, für alle drei Listen zugleich oder gar nicht. Nach D236 tragen alle drei
dasselbe Bearer-Problem. Buchanan/Tullock (D326) liefert die theoretische Herleitung der
Kostenkurve hinter D235s Tabelle, ändert die Entscheidung nicht.

### O32 Darf ein Amendment ein deklariertes Prädikat weglassen?

Gehört an `04 §5`. D167.

### O33 Ausgang 5 und Selbst-Equivocation

Entschieden, aber der Ort ist offen. D127.

### O34 Meldung übersprungener Claims aus `store_laden`

Von D138 zurückgestellt.

### O35 Ein dritter Scope nur für Schlichtung

Fork, nicht entschieden.

### O36 `02d-purpose`

D56.

### O37 `VR-04.1`

D26.

### O38 Zeugenquorum für Fristen

D100.

### O39 Wie weit die Regierbarkeitsprüfung reicht

D200. Zurückgestellt — **nicht vorher aufmachen**.

### O40 Layer 05

Mit D237 ausdrücklich zurückgestellt.

### O41 Eine dritte Implementierung

Bleibt möglich (D311), aber sie prüft dieselbe Achse wie die Kampagne, und die hat nichts
geliefert. Erst wenn der Anwendungsabschnitt Fragen an `01` zurückwirft.

### O42 Tripel bleiben zurückgestellt

D305 Beschluss 4, solange Stufe 2 keinen Befund erzeugt hat.

---

## C — Werkzeug, Prozess, Hygiene

### O43 Zwei Registerverweise zeigen ins Leere

Zwei Registereinträge nennen Abschnitte in `03`, die es dort nicht gibt: einen mit der Nummer
5.1 und einen mit der Nummer 11. Bewusst nicht nachgezogen.

Die Nummern stehen hier absichtlich **nicht** in Verweisform. Ein Verweis, dessen ganze Aussage
ist, dass er ins Leere zeigt, meldet `check_specs` sonst als unbekannten Abschnitt — und genau
das ist beim ersten Lauf dieser Datei passiert. Ungeklärt bleibt, warum
`sitzungsstart-00ap.md` dieselben zwei Verweise in Verweisform trägt, ohne dass die Prüfung
anschlägt.

### O44 Die Einlese-Dateien behaupten, NV2 trage keine Drahtbytes

Seit D291 falsch, bewusst nicht nachgezogen; sie liegen im Archiv.

### O45 Die Anhangsform-Datei trägt fünf um eins zu hohe Zeilenangaben

D232. Sie liegt im Archiv, der Posten bleibt.

### O46 `.claude/settings.local.json` landet in der Projektkopie

Obwohl git sie ignoriert.

### O47 Es gibt keine Kontextdatei für das Werkzeug

D218. Mit D316 rückt der Posten näher: `arbeitsweise.md` ist ein Kandidat, aber sie ist für den
Supervisor geschrieben, nicht für das Werkzeug.

### O48 Die Verweisprüfung kann Listenpunkte nicht von Unterabschnitten unterscheiden

D209.

### O49 Der Harness vergleicht Zeilenzahlen, er identifiziert Zeilen nicht

D226.

### O50 `ALWAYS_BOUND` nennt Wurzeldateien namentlich — erledigt (D318)

`latest_handoff` bindet die jüngste Übergabedatei zur Laufzeit; die beiden Einstiegsdateien
stehen namentlich in der Liste.

---

## D — Öffnung

### O51 Lizenz — erledigt (D319)

Apache-2.0 für den Code, CC-BY-4.0 für Spec, Register und Prüfregeln.

### O52 Öffentliches Repository und Spiegel

Gitea bleibt primär, GitHub wird Spiegel. Sichtbarkeit ist die einzige Möglichkeit, die vier
Menschen aus `08 §2.2` zu finden.

### O53 Englische Schale

README, LICENSE, CONTRIBUTING und ein Dokument zur Methode auf Englisch. Neu geschrieben, nicht
übersetzt. Die Werkstatt bleibt deutsch.

### O54 Normative Sprache der Layer-Dateien — erledigt (D329)

Deutsch bleibt normativ für Layer-Dateien, Register und Prüfregeln. Die englischen Dateien
sind keine Übersetzungen, sondern eigenständiger Text — keine Drift-Gefahr, weil keine
Übersetzungsbeziehung besteht.

### O55 Umbenennung auf `symbolon` — erledigt (D331)

Verzeichnis, Paketname, Importe, Gitea-Name ausgeführt. `LAYER_FILES` war nie betroffen
(Korrektur im Prompt); GitHub-Spiegel und Go-Anker bewusst unverändert.

### O56 Der PyPI-Name `symbolon` ist belegt

Ein 0.1.0-Paket fremden Fachs. Weicher Blocker, erst relevant bei einer Veröffentlichung.
Ausweichnamen: `symbolon-protocol`, `mar`.

### O57 Förderantrag — erledigt (D349)

Am 10. September 2026 bei Restack eingereicht, Code `2026-11-0c4`, 15.000 €.

### O58 Die Implementierungen liegen in zwei Repositorien — erledigt (D321, D330)

Nach `go/` gemergt (D321, fünf Commits erhalten, blob-geprüft). Das verwaiste Gitea-
Repositorium `mar-go` wird archiviert, nicht umbenannt oder gelöscht (D330).

### O59 Vouchsafe als Antwort auf die Vertrauensentzug-Frage aus D313 — erledigt, verneint (D328)

Falsche Passung: löst Capability-Widerruf, nicht wirtschaftliche Durchsetzung. Die
D313-Frage ist stattdessen durch den gemessenen Lauf 00as beantwortet. Aus D326.

### O60 Budget-Set und Kantensatz lösen Zeitunsicherheit in entgegengesetzte Richtungen

Aus D355. Konservativ heißt für den Kantensatz „als abgelaufen behandeln" und für das
Budget-Set „als nicht abgelaufen behandeln" — dieselbe Unsicherheit, entgegengesetzte
Auflösung, beide in `_in_budget_set` (`trust/groups.py:63`). Ein Punkt-`now` lässt beide
zusammenfallen; die Frage ist heute nicht gestellt, nicht beantwortet. Vorbedingung für jede
Fassung mit unscharfer Zeit.
