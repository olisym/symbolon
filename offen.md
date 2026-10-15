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

### O10 `UNPARSABLE_V` entsteht bei `ratify@1` nicht — erledigt (D432)

Entschieden: entsteht, wie bei `vote@1`; `04 §4.1`, `GV-54`. Der Code folgt im Messauftrag.

### O11 `cbor_canon.decode` ist tolerant und bleibt es — erledigt (D431)

Jeder Leser fremder `v`-Bytes prüft `is_canonical` im selben `try`; gemessen an allen drei.

### O12 `FOREIGN_LIFECYCLE` hat keinen Vektor und kann keinen bekommen — erledigt (D431)

Getragen in `01 §6` und NV12 (D263, D268); eine Grenze, keine Lücke.

### O13 `EPOCH_FORK` hat keinen Produktivträger — erledigt (D431)

Unerreichbar nach D176, getragen in `04 §4.4`; ein Test prüfte eine unmögliche Lage.

### O14 `SUBGRANULAR_VOUCH.subject` ist ungeprüft — erledigt (D427)

Geprüft, gemessen mit Rücknahmeprobe; der Gleichstand hängt an einer einzigen Stelle.

### O15 Sechs Zeilen mit wahrer Expiry-Inkohärenz — erledigt (D425)

Prüfreihenfolge der Go-Fassung, Anker vor Expiry, deterministisch; kein Befund nach Prüfregel 61.

### O16 N09 ist beobachtet, nicht durchgesetzt — erledigt (D428)

So beschlossen in D119, getragen in `02 §10`; kein Mangel, sondern ein Zustand.

### O17 N10 ist teilgemessen — erledigt (D428)

Seit D287 alle drei Erzeugungsstellen getragen; gemessen mit Rücknahmeprobe.

### O18 `RATIFY_WITH_EXPIRY` und der Zeugenpfad tragen die Weitergabe ungeprüft — erledigt (D435)

Zeugenpfad seit längerem gedeckt, `RATIFY_WITH_EXPIRY` mit dem Messauftrag.

### O19 Vergleiche gegen `dedupe_sort` sind für die Reihenfolge zirkulär — erledigt (D435)

Schlüssel in `00 §10` (D429); Prüfer für `02` und `04` gegen den ausgeschriebenen Schlüssel.

### O20 Vier `Finding`-Klassen, drei `dedupe_sort` — erledigt (D429)

Getrennt gelassen wie in D183; gegen Drift trägt die Ordnungsnorm aus `00 §10`.

### O21 Die Tests zu `INV-04.7` und `INV-04.8` prüfen eine schwächere Aussage — erledigt (D435)

Eigenschaftstests über zufällige Folgen; der Vorbehalt selbst war zu eng (D433, D434).

### O22 Dreifache Kantensumme in `test_deckenelastizitaet.py` — erledigt (D431)

Testcode, ohne Wirkung auf die Aussage; aufgeräumt wird, wenn die Datei ohnehin berührt wird.

### O23 Die Sondierwelt in `test_benennung.py` erzeugt keine Vermerke — erledigt (D435)

Zweite Probe über einer Welt mit Überziehung und Unterkorn; die erste bleibt.

### O24 `disjoint_paths` bewegt sich nicht — erledigt (D431)

Bewegt sich in TP-BOOT und TP-FAN; gemessen mit Rücknahmeprobe, drei rot.

### O25 Der Sicherungsblob mit Seed und Spitze

D120, beschrieben und ungebaut.

### O26 `D >= C₀` ist ein SHOULD und wird nirgends geprüft — erledigt (D426)

Bleibt ungeprüft; Adressat ist die Gründung, nicht der Leser (`02 §8.1`).

### O27 `anchor_set` (`genesis[3]`) bleibt ungebunden — erledigt (D426)

Entschieden in D147; jetzt als Grenze in `02 §8.1` statt nur im Register.

### O28 `TrustParams.__post_init__` und `00 §4.0` prüfen dieselbe Wohlgeformtheit — erledigt (D426)

Entschieden in D147, nicht zusammengelegt; beide Fassungen gemessen deckungsgleich.

### O29 `genesis[4]` und die Auszählung — erledigt (D430)

Seit D167 und D174 an Epoche 1 gebunden; gemessen mit Rücknahmeprobe, 21 rot.

### O30 Der Beispielnukleus kann Epoche-1- von Epoche-2-Policy nicht unterscheiden — erledigt (D435)

Der Prüfer sitzt in der Kettenwelt; der Beispielnukleus bleibt (D430).

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

### O41 Eine dritte Implementierung — erledigt (D437)

Nicht gebaut; die Lesung liegt aus den Layer-02-Fassungen vor, ihr Befund steht in `01 §6`.

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

### O52 Öffentliches Repository und Spiegel — entfällt (D466)

Der Spiegel besteht. Der Zweck, darüber Menschen zu finden, entfällt; Beteiligte werden simuliert.

### O53 Englische Schale — entfällt (D466)

Diente der Sichtbarkeit nach außen, die mit D466 kein Ziel mehr ist.

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

### O73 Der zweite Zeuge liest einen überholten Text — erledigt (D442)

`rs` auf `573db57` nachgezogen (D441); F1 und D439 tragen, F2 geht an O77.

### O74 Verschachtelung als Norm oder Schnittmenge bei der Auswertung

Aus D354, D361, eingetragen mit D412. Darf eine abhängige Aussage die Zeitgrenze ihrer Prämisse
überschreiten? Die Vorbedingung aus D361 ist seit D404 erfüllt. Stolperdraht: das erste Profil,
das in `03 §1.3` einen Prämissen-Key deklariert.

### O75 Die öffentliche README nennt Zahlen, die driften — erledigt (D415)

Keine wachsenden Zahlen mehr; Verweis auf `make check`, Registerende und Sitzungsstart.

### O76 `pending` und die Flags sind in keinem Vektorsatz belegt — erledigt (D439)

`ZF-02` (D438) belegt sie; Stufe A hat `rs` darauf gemessen, der Rest von F2 gehört zu O73.

### O77 Das Autor-Flag aus Equivocation steht nur im Code — erledigt (D444)

Normiert in `01 §4` und `02 §8` (D443), gebunden in `tests/trust/test_autor_flag.py`.

### O78 Die Fragenliste kennt nur eine Eintragsart — erledigt (D446)

Zwei Arten, Änderungen als Abschnitt 2 im Index (D445); `rs/FRAGEN.md` liegt im Baum.

### O79 Sieben Normen aus `02 §8` und `§10` sind ungebunden — erledigt (D449)

Gebunden in `tests/trust/test_bindung.py`, je mit Rücknahmeprobe (D448, D449).

### O80 `disjoint_paths` im Fenster und drei ungebundene Normen aus `02` — erledigt (D451)

Minimum über die Punkte in `flow.py`, gebunden in `test_fensterpunkte.py` und `test_bindung.py`.

### O81 Ein fremder Lebenszyklus-Claim hält jede Auswertung an — erledigt (D453)

Übergangen in `classify_all`, gebunden in `tests/test_nachtraeglich_ungueltig.py`.

### O82 `core/revoke@2`, `bool`-Schlüssel und sechs ungebundene Normen aus `01` — erledigt (D454)

Geschlossenes `core`, uint-Schlüssel, gebunden in `tests/test_bindung_01.py`.

### O83 Sechs Befunde aus dem Lesen von `03` und `04` — erledigt (D457)

`keys_admissible` in den drei `v`-Lesern; gebunden in `tests/test_v_schluessel.py`,
`tests/profiles/test_lesen_03.py` und `tests/governance/test_lesen_04.py`.

### O84 Sieben Lücken mit Wirkung, uint, eine Prüfung für `participants` — erledigt (D459)

`participants_wellformed` in `policy.py`; gebunden in `test_bindung_03.py`, `test_bindung_04.py`
und `test_policy.py`.

### O85 Die übrigen 36 Lücken aus `03` und `04` — erledigt (D460)

Gebunden in `test_bindung_03.py`, `test_bindung_04.py` und `test_v_schluessel.py`.

### O86 Genesis-Schlüssel und die Ordnung zweier Rotationen — erledigt (D463)

`genesis_scope` in `genesis.py`; gebunden in `tests/nucleus/test_lesen_keys.py`.

### O87 Rotationsbedingungen und drei Formprüfungen binden — erledigt (D465)

Gebunden in `tests/nucleus/test_bindung_keys.py`, Welten G1 bis G7 aus D464.

### O88 Den Bond recherchieren — erledigt (D467)

Das Wort ist ausgemustert, fünf Teilprobleme gehen an ihre Szenarien, nichts baut auf Verwahrung.

### O89 Ein Amtswechsel der Kasse ist eine Schlüsselübergabe

Die Quittung wird byteweise gegen den Gläubiger geprüft (`03 §3.3.2`); wer den Schlüssel der Kasse
einmal hatte, kann weiter quittieren. Aus D468 Beschluss 2. Öffnet mit einem Szenario, in dem das
Amt wechselt.

### O90 Negentropy für den Abgleich über knappe Strecken — erledigt (D618)

Abgleich nach Bereichen (RBSR) im Boten, jede Nachricht ein Paket (D617, D618).

### O91 Mehrere Geräte einer Person ohne geteilten Schlüssel — erledigt (D527)

Seit D123 entschieden: ein Schreiber, ein Ort; Geräte unterschreiben die Anfrage, nicht den Claim.

### O92 Mehrere Geräte einer Person: D123 neu bewerten — erledigt (D540)

Wurzel und Geräteschlüssel je Scope, Zurechnung in `02 §2.1`, Auszählung je Wurzel (D529–D540).

### O93 Eine Stimme, die zwei widersprüchliche Stimmen derselben Wurzel auflöst — erledigt (D549)

Eine Stimme ersetzt, was sie in `v` Key `1` nennt; die Seite nennt frühere Stimmen (D547–D549).

### O94 Geräte im Knoten, in der Simulation und auf der Karte — erledigt (D546)

Bild (c) unter `--geraete`, Sicht je Wurzel, Stimmen einer Wurzel von mehreren Schlüsseln (D542
bis D546).

### O95 Das Folgebild: Bruno löst seinen Widerspruch auf — erledigt (D554)

Bild unter `--aufloesen`: Anna wartet, Bruno ersetzt beide Stimmen, die Seite sagt es (D551–D554).

### O96 Mehrere Anträge nebeneinander: unabhängige Änderungen unter einer Fassung — erledigt (D581)

Sachanträge neben Satzungsanträgen, drei Regeln, Stand; Norm, Knoten und Seite (D564–D581).

### O97 Phase 5: S-Nodes gleichen sich über Reticulum ab

Die Knoten gleichen sich heute nicht selbst ab; ein Werkzeug fährt die Runde (D516). Phase 5 lässt
sie über Reticulum abgleichen, zuerst in einem Lab auf einer Maschine, dann mit Verlust nach Art von
LoRa, dann über Funk (`ROADMAP §7`). Stufen und Lücken L1 bis L10 in D583. O90 gehört dazu.

### O98 Nach einer Spaltung mit Brücken ist die Fassung gebunden — erledigt (D604)

Sperre als Absicht (D596), Wahlgänge mit Patt in Norm, Bibliothek und Knoten (D598–D603).

### O99 Die Seite zeigt keinen Wahlgang und kein Patt — erledigt (D606)

„Im Verein“ sagt, wenn eine Abstimmung vorbei ist; der Verlauf wandert nach O101 (D605, D606).

### O100 Das Patt kostet Zeit

Der geltende Wahlgang wird bei jedem durchgekommenen Vorschlag und in jeder Aufgabenliste neu
gerechnet, und das Patt klassifiziert den Bestand je Wahlgang und je Vorschlag. Die Testreihe wurde
merklich langsamer (D601 Befund 4, D604 Befund 1); auf einem Telefon oder über LoRa ungemessen.

### O101 Die Seite hat kein Konzept dafür, was ein Mensch zuerst sieht

Olis Durchlauf zu D605: „Im Verein“ ist eine gewachsene Liste ohne Zweck. Eine Fassungsnummer ohne
Inhalt, die Mitgliederliste doppelt, „Alle haben bestätigt“ ohne Bezug; die Bestätigung gehört zur
Ansicht der Satzung. Offen: was „Im Verein“ ist (Lage, Neuigkeiten), der Tab „Verlauf“ (D605),
Ansichten je Grösse des Bildschirms, und wie ein Mensch ankommt, der nichts weiss; das beginnt mit
Gründung und Beitritt (D606).

### O102 Vertraulichkeit im Funk — erledigt (D629)

IFAC am Funk-Interface mit zufälliger Passphrase, als Regel des Betriebs, nicht der Norm (D628,
D629).

### O103 Rundruf auf knappem Funk — erledigt (D638)

Der Bote sendet eigene neue Einträge einmal als Rundruf; ein Drittel der Sendezeit (D635 bis D638).

### O104 Anfragen über den Link scheitern unter Verlust

Bei 1200 bit/s und 5 % Verlust scheiterte im Lab jede sechste Anfrage, jede nach mindestens 60 s,
eine nach 250 s; auch gelungene brauchten oft 80 s (D623 Befund 4). Die Zeit bis zum gleichen Stand
hängt daran. Zuerst messen, woran (Aufbau des Links, Wiederholung, Frist), dann die T-Beams.
Gemessen in D630: jede Anfrage, die an der Antwortfrist scheitert, liegt auf einem Link, dessen
`LRRTT` verloren ging. Repariert: ein Link ohne Antwort wird neu aufgebaut (D631, D632). Offen
bleiben die gehäuft scheiternden Aufbauten (D627 Befund 3, D630 Befund 2).

### O105 Was die Bausteine nicht abbilden

Querprüfung gegen Fiskes vier Formen und Ostroms Bauprinzipien (D661). Sechs Lücken, je ein
Strang, wenn ein Szenario ihn braucht; vorher wird nachgeschlagen (D640):

1. **Vertretung nach aussen**, ein Vorstand, der für die Gruppe spricht (D645 Befund 4); dazu
   Delegation im Kern (`01 §1`) und Stimmvollmacht.
2. **Geheime Wahl.** Jede Stimme ist ein unterschriebener Claim.
3. **Marktpreis und Tausch.** Die Wertschicht fehlt (`08 §3`), der atomare Tausch ist vertagt
   (`03 §3.4`).
4. **Verschachtelte Ebenen.** Föderation normiert (`04 §7`), ungebaut; auch empirisch das am
   schwächsten gestützte Prinzip.
5. **Verzeihen und Vergessen.** Ohne Layer 05 kein Ort, an dem Altes weniger zählt (`05 §4`).
6. **Schlichtung auf der Seite.** In der Bibliothek gebaut (`03 §2`), für Menschen nicht
   erreichbar.

### O106 Geheime Abstimmung

Jede Stimme ist ein unterschriebener Claim (O105 Punkt 2). Richtung nach D666: eine Mischrunde
unter den Teilnehmenden ergibt eine Liste frischer Schlüssel, mit denen nach `04 §3` abgestimmt
wird; das Atom bleibt. Gebaut: die Zählregel in `04 §9` und in der Bibliothek (D669, D671,
D672), die Vorlage `verein` mit `ballot-ack@1` und `ballot@1` (D674), Wahl und Liste im Knoten
(D677), der Ablauf ohne Mischrunde mit dem Wahlschlüssel im Knoten (D679) und die Seite mit dem
Tab „Wahlen“, den Schritten unter „Jetzt zu tun“ und einer Frage vor jeder Stimme (D683). Offene
und geheime Stimmen in derselben Epoche treffen sich nicht, denn die Wahl ist kein Antrag (D667
Beschluss 2). Offen: die Mischrunde zwischen Knoten, ein Satzungsantrag für Vereine, die vor D673
gegründet wurden, und was die Vorstandswahl füllt (O105 Punkt 1).

### O107 Beteiligung: wer nie abstimmt

Der Nenner ist `|P|`, Schweigen wirkt wie Ablehnung (D100). Mit festen Schwellen in der Vorlage
(D648 Beschluss 5) steht ein Verein still, sobald mehr als ein Drittel nie abstimmt: keine
Satzungsänderung mehr, Wahlen ohne Ende (D686 Befund 1 und 2). Position nach D686: Enthaltung als
ausdrückliche Stimme, die den Nenner senkt; ruhen durch Beschluss mit `membership`, zurück durch
ein eigenes Lebenszeichen. Offen: wann eine Rückkehr wirkt, ohne eine laufende Abstimmung zu
kippen, die Kennung der Regel in der Satzung, Enthaltung in Wahl und Patt (D686 Befund 5).
Nachgeschlagen in D687: der Nenner sinkt in einer Abstimmung nur, und jeder kann selbst ruhen.
Gerechnet in D689: nur eine Wurzel ohne zählende Stimme darf den Nenner verlassen; wer ruht,
stimmt nicht; die Ruhenden stehen in der Satzung, selbst ruhen gilt bis zur eigenen Rückkehr,
und zurück ist man, wenn ein Antrag das aufnimmt. Offen: die Kennung der Liste in der Satzung,
Enthaltung und Ruhen in Wahl und Patt, eine blockierte Rückkehr (D689 Befund 3).
Im Prototyp (D690): es kippt nur der zweite Claim eines Mitglieds, und nur nach offen; eine
Stimme, die die eigene Ruhe nennt, ist ein Lebenszeichen; die Liste braucht `threshold_class`.
Wahl und Patt in D691: Enthaltung je Wahlgang, auch geheim; in der geheimen Wahl zählt nur die
Liste in der Satzung, selbst ruhen wirkt dort nicht. Offen: mehrere Geräte einer Wurzel.
Rivalen und Kennung in D692; der Normtext in D693 (`participation@1`, `BV-1` bis `BV-43`).
Nächster Schritt: der Auftrag `p63-beteiligung`, danach die Seite.
