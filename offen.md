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

### O3 `OPEN` unterscheidet Verweigerung nicht von Partition — erledigt (D423)

Getragene Grenze in `08 §7`; `OPEN` ist kein negativer Ausgang (`05 §3`).

### O4 Gleicher Zustand bei allen Beobachtern ist eine Eigenschaft der Verteilung — erledigt (D423)

Bereits von `08 §2.3` getragen; kein Text geändert.

### O5 Preisblindheit trägt keine Versicherungsphase — erledigt (D423)

Prüftabelle `08 §3`: Wertschicht, wie D313 es schon entschieden hatte.

### O6 `settlement` prüft keine Mitgliedschaft — erledigt (D423)

Prüftabelle `08 §3` und `03 §5`: nicht Protokoll, `00 §4.2`.

### O7 Ohne `t_exp` bleibt eine Obligation ohne Ende offen — erledigt (D423)

Prüftabelle `08 §3`: Erlass ist `receipt@1`, Ausfall `accusation@1`, kein neuer Mechanismus.

### O8 `tools/szenario_absicherung.py` ist Wegwerfcode — erledigt (D423)

Entschieden in D312; die Datei bleibt im Baum, Szenarioläufe setzen auf `tools/sim/` auf.

---

## B — Verifikationsabschnitt

### O9 Anhang C ist gegen Generatordrift nur teilweise gesichert — erledigt (D414)

Ganz Anhang C gebunden, in beide Richtungen, mit dauerhafter Verfälschungsprobe.

### O10 `UNPARSABLE_V` entsteht bei `ratify@1` nicht

D276.

### O11 `cbor_canon.decode` ist tolerant und bleibt es

### O12 `FOREIGN_LIFECYCLE` hat keinen Vektor und kann keinen bekommen

D263, D268. Auch vom Gitter unerreichbar, weil es einen Speicher braucht.

### O13 `EPOCH_FORK` hat keinen Produktivträger

D138, D176, D281.

### O14 `SUBGRANULAR_VOUCH.subject` ist ungeprüft — erledigt (D427)

Geprüft, gemessen mit Rücknahmeprobe; der Gleichstand hängt an einer einzigen Stelle.

### O15 Sechs Zeilen mit wahrer Expiry-Inkohärenz — erledigt (D425)

Prüfreihenfolge der Go-Fassung, Anker vor Expiry, deterministisch; kein Befund nach Prüfregel 61.

### O16 N09 ist beobachtet, nicht durchgesetzt — erledigt (D428)

So beschlossen in D119, getragen in `02 §10`; kein Mangel, sondern ein Zustand.

### O17 N10 ist teilgemessen — erledigt (D428)

Seit D287 alle drei Erzeugungsstellen getragen; gemessen mit Rücknahmeprobe.

### O18 `RATIFY_WITH_EXPIRY` und der Zeugenpfad tragen die Weitergaberegel ungeprüft

D203.

### O19 Vergleiche gegen `dedupe_sort` sind für die Reihenfolge zirkulär

D196.

### O20 Vier `Finding`-Klassen, drei `dedupe_sort` — erledigt (D429)

Getrennt gelassen wie in D183; gegen Drift trägt die Ordnungsnorm aus `00 §10`.

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

### O26 `D >= C₀` ist ein SHOULD und wird nirgends geprüft — erledigt (D426)

Bleibt ungeprüft; Adressat ist die Gründung, nicht der Leser (`02 §8.1`).

### O27 `anchor_set` (`genesis[3]`) bleibt ungebunden — erledigt (D426)

Entschieden in D147; jetzt als Grenze in `02 §8.1` statt nur im Register.

### O28 `TrustParams.__post_init__` und `00 §4.0` prüfen dieselbe Wohlgeformtheit — erledigt (D426)

Entschieden in D147, nicht zusammengelegt; beide Fassungen gemessen deckungsgleich.

### O29 `genesis[4]` und die Auszählung

`GV-24` führt ein Genesis, dessen deklarierte Verfassung in der Auszählung nirgends vorkommt.

### O30 Der Beispielnukleus kann Epoche-1- von Epoche-2-Policy nicht unterscheiden

D169, D188.

### O31 Eine Schwelle für Autoritätslisten

Mit D166 zurückgestellt, für alle drei Listen zugleich oder gar nicht. Nach D236 tragen alle drei
dasselbe Bearer-Problem. Buchanan/Tullock (D326) liefert die theoretische Herleitung der
Kostenkurve hinter D235s Tabelle, ändert die Entscheidung nicht.

### O32 Darf ein Amendment ein deklariertes Prädikat weglassen? — erledigt (D424)

Ja, gemessen am Boden; getragen in `04 §8`, klargestellt in `00 §5.2`.

### O33 Ausgang 5 und Selbst-Equivocation — erledigt (D424)

Ort ist `01 §8`; kein Werkzeugausgang, Vermeidung hängt an O25.

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

### O43 Zwei Registerverweise zeigen ins Leere — erledigt (D417)

Sie zeigen in `03-golden-anchors.md`, nicht ins Leere; die Einträge bleiben, wie sie sind.

### O44 Die Einlese-Dateien behaupten, NV2 trage keine Drahtbytes — erledigt (D419)

Archiv beschreibt vergangene Läufe und wird nicht nachgezogen.

### O45 Die Anhangsform-Datei trägt fünf um eins zu hohe Zeilenangaben — erledigt (D419)

Archiv, nicht berichtigt; D232 hat das für diese Datei entschieden.

### O46 `.claude/settings.local.json` landet in der Projektkopie — erledigt (D419)

`repomix.config.json` schliesst `.claude/**` aus.

### O47 Es gibt keine Kontextdatei für das Werkzeug — erledigt (D421)

Es gab eine, unversioniert; ersetzt durch `AGENTS.md`.

### O48 Die Verweisprüfung unterscheidet Listenpunkte nicht von Unterabschnitten — erledigt (D417)

Getragen: die Grenze meldet laut, nicht still. Stolperdraht in D417.

### O49 Der Harness vergleicht Zeilenzahlen, er identifiziert Zeilen nicht — erledigt (D417)

Gegenstandslos bei grünem `main`. Stolperdraht in D417.

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

### O60 Budget-Set und Kantensatz lösen Zeitunsicherheit gegenläufig — erledigt (D402)

Gegenläufigkeit harmlos; getrennt sind lokaler Vermerk und signierter Beweis (`02 §3.1`).

### O61 Soll ein uhrloser Knoten Vertrauen gewähren können? — erledigt (D404)

Nein; uhrlos kann ein Knoten belasten, nicht gewähren (`02 §6.2`, D402, D404).

### O62 Zweitimplementierung für Layer 02 — erledigt (D409)

Drei Fassungen, Fluss- und Zustandshälfte gelesen; der Überhang geht an O73.

### O63 Der INF-Sentinel hängt am Bestand, nicht an der Kalibrierung — erledigt (D381)

`02a §2.8` normiert die Bedingung statt der Formel; die Referenzbelegung und die gepinnten Werte
bleiben unverändert.

### O64 Anhangsverweise werden nicht auf Existenz geprüft — erledigt (D401)

`check_specs` prüft beide Zitatformen gegen die Anhangsüberschriften (Werkzeuglauf nach D401).

### O65 Was eine Gruppe ohne wirksame Vouches ist, steht nirgends — erledigt (D396)

Gruppe besteht nur mit einem Mitglied im Budget-Set; `cap 0` war Auftrag; Legende in `C.0`.

### O66 Selbstgetragene Adressen erscheinen in keinem Index — erledigt (D395)

Selbsttragende Listen werden angemeldet und aus sich gelesen, mit Vollständigkeitsprobe.

### O67 `02 §10` nennt zu jedem Vermerk das Subjekt und zu keinem die Wirkung — erledigt (D394)

Neu gefasst mit Wirkungsspalte; der Widerspruch im Schlusssatz ist aufgelöst.


### O68 Welche Vouches überhaupt einen Vermerk bekommen, steht nirgends — erledigt (D400)

Gelesen wird das Budget-Set; `VOUCH_WITHOUT_TEXP` nur bei gültigem `n` (`02 §10`, `02 §11.4`).

### O69 `02a` trägt überholte Stellen, und niemand hat sie gezählt — erledigt (D399)

`02a` ist historisch; Normen in `02 §11` und K9, Verweise in Spec und Code umgehängt (D397, D398).

### O70 Der Uhrversatz-Fall aus D402 ist ungepinnt — erledigt (D405)

Drei Fälle in `tests/trust/test_uhrversatz.py`; der Beweis bleibt ungebaut (D403).

### O71 Intervall-`now` für den Knoten mit grober Uhr — erledigt (D406)

Parameter, exakt über die Bruchstellen, Minimum plus obere Schranke; die Umsetzung läuft als O72.

### O72 Intervall-`now` ist normiert, aber nicht gebaut — erledigt (D408)

Gebaut auf `o72-intervall-now`, gemergt als `8f8b460`; nur `flow.py` berührt, `derive()` und
`rank()` blieben punktförmig. Die Bruchstellen kommen aus den Scope-Vouches. Nicht gemessen
blieb `include_flagged = True` über ein Fenster; die Kostenfrage aus D406 bleibt ohne
Obergrenze.

### O73 Der zweite Zeuge liest einen überholten Text

Aus D409. Der Rust-Anker steht auf `15d091e`; seither ist `02-trust-flow.md` in sechs Commits
geändert (D394, D396, D398, D400, D402, D406) und `01-claim-atom.md` in einem (D396), darunter der
ganze `§11`. Keine Fassung hat das gelesen. Vor dem nächsten Auftrag offen: D368 hält `02a`
zurück, dessen Normstoff seit D397 in `02 §11` steht — die Diät wirkt nicht mehr wie beschlossen.
Stolperdraht: der erste Befund, der an einer dieser Änderungen hängt und ohne zweiten Zeugen
entschieden werden müsste.

### O74 Verschachtelung als Norm oder Schnittmenge bei der Auswertung

Aus D354, D361, eingetragen mit D412. Darf eine abhängige Aussage die Zeitgrenze ihrer Prämisse
überschreiten? Die Vorbedingung aus D361 ist seit D404 erfüllt. Stolperdraht: das erste Profil,
das in `03 §1.3` einen Prämissen-Key deklariert.

### O75 Die öffentliche README nennt Zahlen, die driften — erledigt (D415)

Keine wachsenden Zahlen mehr; Verweis auf `make check`, Registerende und Sitzungsstart.
