# Prüfregeln

Die Regeln, nach denen in MaR geprüft wird. Sie sind aus Befunden entstanden, nicht aus
Prinzipien: jede steht hier, weil ihr Fehlen einmal einen Defekt durchgelassen hat. Wo eine
Regel aus einem Registereintrag stammt, ist er genannt.

Diese Datei ist der **einzige** Ort ihres Volltextes. Bis D144 standen sie verteilt über sechs
abgelöste `sitzungsstart-*.md`; ein `sitzungsstart` verweist auf diese Datei, er wiederholt sie
nicht.

Geordnet nach dem Zeitpunkt, an dem sie greifen. Die Nummern sind vergabestabil und stehen
deshalb nicht in ihrer Reihenfolge; wer eine Regel sucht, sucht den Zeitpunkt, nicht die Zahl.

---

## Beim Entwerfen

**1. Vor dem Schreiben rechnen.** Jede Zahl, die aus einer Regel folgt, wird gerechnet, bevor sie
geschrieben wird — nicht danach geprüft. Eine Eigenschaft so genau zu formulieren, dass eine
Maschine sie angreifen kann, ist selbst die Prüfung.

**2. Standprüfung.** Vor jedem Mechanismus zu Nebenläufigkeit, Ordnung oder Schwellen fragen,
unter welchem Namen das Problem außerhalb des Projekts gelöst ist. CALM und ein Raft-Befund haben
je einen eigenen Vorschlag widerlegt (D96, D102).

**15. Literaturprüfung vor der Entscheidung.** Bei jedem Fork, der außerhalb von MaR seit Jahren
bearbeitet wird, zuerst nachsehen, was dort gefunden wurde. D124 (did:plc, Keybase, CONIKS,
Nostr, SSB), D125 (TUF), D127 (Test-Doubles, ALICE, ARIES) sind so entschieden worden — und in
zwei Fällen billiger und schärfer, als eine eigene Analyse geworden wäre.

**32. Wo eine Prüfung sitzt, ist eine eigene Gabel.** Steht fest, dass geprüft werden soll, ist die
Stelle damit nicht entschieden. Die Gegenprobe wird an jeder plausiblen Stelle gebaut, und
verglichen werden die **erzeugten Aussagen**, nicht die Zahl der gefallenen Tests. In D200 kosteten
alle drei Varianten genau einen Test; die Wahl fiel erst, als die Vermerke nebeneinander lagen und
zwei Varianten `UNEVALUABLE` meldeten, wo `PASSED` gemessen war.

## Beim Definieren von Typen und Feldern

**3. Feldinventur.** Für jedes Feld eines Schemas benennen, welche Funktion es liest. Felder ohne
Leser sind zu streichen oder als deklarativ zu kennzeichnen (D114).

**4. Zugehörigkeitsliste am Datentyp.** Welche Felder eine Zugehörigkeit behaupten und wogegen sie
zu prüfen sind, wird bei der **Definition** des Typs aufgeschrieben (D112).

**10. Leserprüfung.** Trägt ein normativer Satz eine Pflicht an den *Autor* von Claims, wird bei
seiner Formulierung benannt, welche Funktion die Erfüllung liest. Gibt es keine, ist der Satz auf
SOLL zurückzunehmen oder mit einem Vermerk zu versehen (D119). Die Feldinventur fragt nach dem
Leser eines Feldes; diese Regel nach dem Leser einer Pflicht. `02 §6.2` hat zwei Layer
überdauert, weil seine einzige Wirkung war, dass ein wohlerzogener Autor etwas unterließ.

## Beim Formulieren normativen Textes

**9. Begründungsprüfung.** Ist eine Begründung an einen einzelnen Fehlermodus gebunden, und gibt
es einen zweiten? D77, D83, D87 und D91 sind alle aus Begründungen entstanden, die beim Wandern
still ihren Geltungsbereich verloren haben.

**11. Geschwisterformel.** Ein Verbot, das mit „an welcher Stelle auch immer" endet, fängt
Geschwister, die eine Aufzählung nicht kennt — billiger als eine vollständige Liste. Der Schnitt
in D122 nannte einen Helfer; das Verbot hat fünf gefunden.

**18. Aufzählung gegen Satz.** Steht in einer Spec eine Bedingung als Satz **und** als
ausgerechnete Aufzählung, gilt der Satz, und die Aufzählung wird als abgeleitet markiert (so in
`02a §2.6`). Aufzählungen verlieren beim Wandern still ihren Geltungsbereich — D77, D83, D87,
D91, D130, D135 sind alle diese Form. Ein allgemeiner Satz erbt den Geltungsbereich der
Aufzählung, die ihm vorausgeht; Prosabedingungen gehen abgeleiteten Aufzählungen vor.
Zusatz: dasselbe gilt für einen Satz, der einen älteren **ersetzt**. Wer eine Bedingung neu
formuliert, benennt zuerst den Geltungsbereich der alten und prüft ihn gegen den Code, der sie
umsetzt. In D165 wurde aus „die Kette von k ist an einem Punkt equivoziert" ein Satz über k
allein; der Code prüfte weiter jedes Kettenglied, und die Spec stand hinter ihm.

**20. Kostenaussage braucht Kostenmodell.** Ein Satz, der etwas „billig", „teuer" oder „ohnehin
unattraktiv" nennt, ist eine Aussage über Angriffskosten. Steht in der Spec kein Kostenmodell,
das ihn trägt, fällt der Satz — auch und gerade dann, wenn der Satz daneben bewiesen ist. Ein
bewiesener Nachbar macht eine unbelegte Behauptung nicht wahr, er macht sie nur schwerer
sichtbar (D139).

**21. Eine Kapazität ist eine Schranke, kein Ertrag.** Wer eine Kapazität in eine Bilanz
einsetzt, muss den Weg rechnen, den der Fluss zu ihr nimmt. `Σ C(h)` ist eine Obergrenze, kein
Aufkommen; `cap(p → h)` ist eine Ausgangsschranke, kein Beitrag, wenn `p` weniger empfängt.
D139, D141 und D142 sind dreimal dieselbe Verwechslung. Zusatz: ein Term, den die Spec als
redundant beweist, kann von keiner Rücknahmeprobe rot gefärbt werden — eine Probe, die ihn
treffen soll, ist falsch gebaut (D142).

**25. Die Begründung wird beim Beschluss geprüft, nicht beim Widerspruch.** Für jede Stelle, die
eine Begründung zitiert, wird gefragt, ob sie den Fall des Beschlusses regelt oder einen
benachbarten. D152 nannte einen Angriff, den der Einlesepfad ausschließt; D156 nannte einen
Paragraphen über fehlende Objekte für den Fall eines fehlenden Aufrufs. Beide Beschlüsse trugen,
beide Begründungen nicht, und beide fielen erst auf, als eine Messung widersprach. Eine ungeprüfte
Begründung sieht aus wie eine geprüfte (D158, D159, D160).

**36. Eine neue Behauptung wird danach eingeordnet, was sie hinzufügt: Erkennung oder Adresse.**
Gemessen wird das, indem die Welt falsch gemacht und die Rotmenge mit und ohne die neue Behauptung
verglichen wird. Sind beide gleich, kommt keine Erkennung hinzu, sondern eine bessere Auskunft.
Das ist ein zulässiger Zweck, aber ein anderer, und der Registereintrag sagt welchen. In D205 waren
die Rotmengen identisch — ein falsches `n` bricht ohnehin jeden Vertrauenswert; was die neuen
Behauptungen halten, ist die Übertragung der Ankertabelle in den Test.

**47. Ein Verweis und ein Code-Span werden beim Umbrechen wie ein Wort behandelt.**
`SECTION_REF` in `tools/check_specs.py` verlangt den Namen unmittelbar vor dem Paragraphenzeichen,
getrennt durch genau ein Leerzeichen. Ein Zeilenumbruch an dieser Stelle macht den Verweis nicht
falsch, sondern unsichtbar: er wird nicht mehr geprüft, und die Prüfung bleibt grün. Gemessen in
`00ab` an einem ungeglätteten Reflow: die gefundenen Verweise fallen in
`00-nucleus-genesis-constitution.md` von 67 auf 66 und in `06-services.md` von 44 auf 43. Fuer
Inline-Code-Spans dieselbe Lage in schwächerer Form: die Zeilen mit ungerader Backtick-Zahl in
`01-claim-atom.md` steigen von 38 auf 40. Wer Prosa umbricht, hält Name-Paragraph-Ziffer und jeden
Code-Span in einer Zeile (D239).

**54. Wer eine Form vorschreibt, benennt ihren tragenden Teil.**
Ein Prompt, der eine Codeform verlangt, bekommt die Form und nicht notwendig ihre Wirkung. In
`00ah` verlangte er `decode` und `is_canonical` im selben `try`; gebaut wurde genau das, und der
tragende Teil war ein anderer — dass der `except`-Zweig abbricht statt fortzufahren. Der Lauf traf
den Buchstaben und verfehlte den Satz. Wer eine Form vorschreibt, schreibt dazu, was sie leisten
soll, und formuliert das Abnahmekriterium an der Wirkung, nicht an der Silhouette (D276).

## Beim Prüfen von Code und Spec nebeneinander

**5. Ausgänge aufzählen.** Wo eine Invariante einen Zustandsübergang ausschließt, werden **alle**
Ausgänge aus dem Zustand aufgezählt — aus dem Code, nicht aus dem Gedächtnis (D117).

**8. Parallelenprüfung.** Zwei Stellen, die dasselbe tun, werden nebeneinandergelegt —
Eingangsbedingungen, Fehlertypen, Diagnosen. Sequenzielles Lesen findet Asymmetrien nicht.

**14. Zählregel.** Eine Aufzählung von Fundstellen wird **gegrept, nicht gelesen**. D119 nannte
zuerst einen Erzeuger, es waren drei. D127 nannte vier Kettenfortführungen, es waren fünf. D146
nannte einen Importeur von `_tally`, es waren zwei. Jedes Mal stimmte die Begründung und die Zahl
nicht.

**Ein Limit, das exakt erreicht wird, ist ein Nulltreffer.** Gibt `head -n` genau `n` Zeilen
zurück, sagt die Ausgabe nichts über das, was jenseits liegt — ein abgeschnittener Grep ist kein
Grep. Wer etwas verschiebt, greppt die Verwender, statt sie zu erinnern.

**16. Wirkungsprüfung.** Bevor einem Befund eine Folge zugeschrieben wird, wird der falsche Wert
**bis zu seinem Verbraucher** verfolgt. Bei D135 war `Σ n_budget` ausgerechnet, aber nicht
weiterverfolgt; der erste Wirkungsabsatz behauptete die Gegenrichtung, weil `derive.py` Schritt 5
geflaggte Autoren autorweit ausschließt und nicht gruppenweit. Die Wirkung liegt nie dort, wo die
Zahl entsteht.

**17. Prompt-Dateien sind normativer Text, solange Code auf sie zeigt.** Die Parallelenprüfung
gilt nicht nur für Layer-Dateien. `02a-maxflow-prompt.md` trug Befund und Widerlegung **neun
Zeilen** voneinander entfernt: eine Aufzählung, die `EQUIVOCATION_FLAGGED` wegließ, direkt über
dem Satz, ein Vouch verlasse das Budget-Set ausschließlich durch `t_exp`. Der Code folgte der
Aufzählung. Ein Verweis auf gelöschten Text ist normativer Text ohne Quelle.

**27. Ein Verweis im Prompt wird aufgeschlagen.** Bevor ein Zeiger auf eine Spec-Stelle in einen
Prompt geht, wird die Stelle gelesen und geprüft, ob sie die Aussage trägt — auch und gerade
dann, wenn der Zeiger aus dem eigenen Register stammt. `04-golden-anchors.md §8` hat vier
Stationen durchlaufen: D170 nannte es als bessere Stelle, D171 ließ es stehen, der `00c`-Prompt
zitierte es, das Werkzeug führte es aus. Keine Station hat die Datei aufgeschlagen; §8 ist die
Invariantentabelle und sagt zu Vermerken nichts. Regel 22 trägt den Fall nicht — ein
Abschnittsverweis ist kein Bezeichner: er lässt sich nicht aus der Quelle übernehmen, sondern
nur gegen sie prüfen (D173).

**38. Eine Position wird erst bezogen, nachdem der zuständige Abschnitt aufgeschlagen ist.**
Prüfregel 27 verlangt das Aufschlagen vor dem Prompt, Prüfregel 33 das Danebenlegen des Spec-Satzes.
Beide greifen zu spät: entschieden wird, wenn eine Position auf eine Gabel bezogen wird, und das
geschieht davor. Wer eine Lage für ungeklärt hält, schlägt zuerst nach, wer sie schon geklärt hat —
`tools/register_index.py` nennt die Einträge zu einem Abschnitt. In der Sitzung zu D207 wurden drei
von vier Positionen zurückgenommen, jede davon gegen eine Entscheidung, die es bereits gab (D209).

**52. Wer ungebundenes Verhalten sucht, misst am Code und nicht am Register.**
Die Frage „welcher Registereintrag beschließt Verhalten und taucht in keinem Test auf" liefert in
`00ah` 47 Kandidaten und damit kein Signal; die Frage „welcher Vermerks- oder Verdiktcode im
Produktivcode taucht in keinem Test auf" liefert vier, von denen zwei benannt waren und zwei
nicht. Der Grund ist mechanisch: D-Nummern stehen selten im Code, Codes stehen immer dort. Ein
Suchmuster, das über das Register läuft, misst die Dokumentation; nur eines, das über die
Bezeichner im Produktivcode läuft, misst den Bestand (D278).

## Beim Ändern von Reihenfolgen und Stufen

**6. Monotonie stufenweise.** Eine Monotonieaussage gilt zunächst nur für die letzte Stufe. Jede
Stufe davor wird einzeln geprüft (D118).

**7. Abhängigkeitssatz bei Reihenfolgeänderungen.** Wird eine Reihenfolge geändert, wird für jede
Größe, die in der alten nebenbei entstand, benannt, woher sie in der neuen kommt (D113).

## Beim Schreiben eines Prompts

**22. Ein Bezeichner im Prompt ist ein Zitat.** Namen, Signaturen und Argumentlisten, die in
einen Prompt gehen, werden aus der Quelle übernommen, nicht aus dem Gelesenen rekonstruiert. In
D145 stand `passed()` im Prompt, weil der Rumpf der Funktion gelesen und ihre `def`-Zeile ergänzt
worden war; sie heißt `reached()`. Regel 14 trägt diesen Fall nicht — er ist keine Aufzählung,
sondern eine einzelne Angabe, und **gelesen** und **vollständig gelesen** sehen bei einem
Funktionsrumpf gleich aus.

**24. Ein Nicht-Ziel, das eine beschlossene Norm verletzt, ist keines.** Vor jedem „keine
Änderung an X" im Prompt wird geprüft, ob eine Norm desselben Laufs X zwangsläufig bewegt. Steht
die Normänderung im selben Prompt wie das Verbot, sie nachzuziehen, hat das Werkzeug keinen
erfüllbaren Weg — und der einzige verbleibende ist der stille Umbau, den das Nicht-Ziel
verhindern sollte (D157, D160).

**28. Ein Abnahmekriterium behauptet einen Weltzustand.** Bevor ein Kriterium in einen Prompt
geht, wird nicht nur gefragt, ob die erwartete Aussage stimmen soll, sondern ob der Zustand, in
dem sie geprüft würde, überhaupt konstruierbar ist. Der Prüfgriff ist, ihn vor dem Schreiben zu
bauen: welche Claims, welche Objekte, welche Verfassung. Vier der neun Testfälle aus `00d`
behaupteten unmögliche Lagen — ein Objekt, das für den Übergang bekannt und für das Ergebnis
unbekannt ist; zwei Objekte unter einem Schlüssel; eine Rückwirkung, die überlappende
Teilnehmermengen ausschließen; der Widerruf eines Prädikats, das die Verfassung zwingend schützt.
Alle vier lasen sich schlüssig und alle vier waren vor dem Lauf entschieden.
Und: die Welt, die im Prompt steht, ist Feld für Feld die Welt, die gemessen wurde. In `00j` war
sie in der Designrunde richtig gebaut und ging beim Abschreiben verloren — die Feldliste nannte
Schwellen, Schlichter, `participants` und `nucleus_keys` und ließ `irrevocable_predicates` weg,
ohne die nach `04 §3.5` keine Auszählung evaluierbar ist. Konstruieren ist die eine Hälfte,
vollständig übertragen die andere.

**29. Ein Grep-Kriterium verbietet Namen.** Ein Abnahmekriterium der Form „`grep X` liefert null"
trifft nicht nur den Zustand, den es verbieten soll, sondern jede Zeichenkette, die `X` enthält. In
`00e` verlangte das Kriterium für `_is_nuc_name` null Treffer; ein Test namens
`test_is_nuc_name_...` hätte es rot gemacht, ohne dass etwas falsch gewesen wäre. Das Werkzeug hat
die Testnamen deshalb danach ausgerichtet und es gemeldet. Ein Kriterium, das die Namensgebung
lenkt, misst nicht mehr. Ein Grep-Kriterium wird so eng gefasst, dass nur der verbotene Zustand
hineinfällt: `def _is_nuc_name` statt `_is_nuc_name`.

**31. Der Vergleichspunkt eines Laufs ist der Prompt-Commit.** Ein Abnahmekriterium über einen
Diff nennt den Commit, auf dem der Prompt liegt, nicht den Registercommit darunter. Der Prompt ist
selbst eine Datei im Wurzelverzeichnis und erscheint sonst in genau dem Diff, den er beschreibt.
In `00k` setzte der Supervisor `32c55c9` als Basis, obwohl der Prompt auf `2a02104` lag, und maß
das Kriterium „genau fünf Dateien" gegen sechs; das Werkzeug hat es gemeldet und nichts
nachgezogen. Die Regel stand seit langem in der dauerhaften Anweisung und in jedem Sitzungsstart,
war aber nicht nummeriert — und was hier nicht steht, wird beim Schreiben eines Prompts nicht
geprüft. Dieselbe Begründung wie bei den Nummern 8 und 9 in D144.

**33. Der Prompt wird gegen den Spec-Satz gelesen, den er umsetzt.** Prüfregel 27 verlangt, dass
ein Verweis die behauptete Aussage trägt. Das genügt nicht: der Verweis kann stimmen und die
Anweisung daneben liegen. In `00m` zitierte der Prompt `04 §4.1` richtig und schrieb den
ValueError-Wächter trotzdem hinter die Bedingungen 1 bis 5, wo die Spec ihn an keine Bedingung
knüpft. Das Werkzeug hat den Prompt korrekt umgesetzt, und der Defekt wurde erst in der Abnahme
sichtbar. Wo ein Prompt eine Reihenfolge oder einen Ort festlegt, wird der Spec-Satz danebengelegt,
nicht nur aufgeschlagen.

**37. Die Basis eines Laufs ist der Commit, der den Prompt enthält.**
Ein Prompt, der geschrieben wird, bevor er committet ist, kann seine eigene Basis nicht nennen; wer
den Registercommit darunter einträgt, lässt den Lauf an einem Punkt verzweigen, an dem der Prompt
noch nicht existiert. Die Abnahme bleibt davon oft unberührt, der Merge nicht: ein Fast-Forward
setzt voraus, dass die Zielspitze der Branchpunkt ist, und das ist bei dieser Reihenfolge nie
gegeben. Deshalb wird der Prompt zuerst committet und die Basis danach eingetragen. In `00q` fiel
es erst beim Merge auf (D208).

**41. Die Vorabvariante ist Erwartungsquelle, nicht Vorbild.**
Eine vollständig gebaute Variante liefert die Zahlen, gegen die abgenommen wird — sie bindet das
Werkzeug nicht. Weicht der Lauf ab, wird die Abweichung zuerst gegen den **Prompt** geprüft und
erst danach gegen die Variante; deckt der Prompt das ab, was das Werkzeug gebaut hat, ist die
Variante der Fehler und nicht der Lauf. In `00t` zählte die Variante alle Python-Befunde als
einen, der Prompt verlangte die Zählung je Datei, und die vier Zeilen Abweichung waren die
Reparatur (D217).

**50. Ein Modell des Codes trägt nur die Zusicherungen, die es nachbildet.**
Wer eine Erwartung an einem nachgebauten Modell rechnet statt am Code, darf daraus keine Aussage
über Mengen ableiten, die das Modell nicht kennt. Gemessen in `00ac`: ein Modell von
`resolve_scope` mit drei Fällen sagte einen roten Test voraus; der Lauf färbte vier, weil drei der
achtzehn Tests in `tests/test_predicates.py` über die Klassifikation in `parse_predicate`
behaupten und nicht über die Auflösung. Die Richtung der Aussage war richtig, ihre Zahl nicht. Ein
Kriterium aus einem Modell wird als untere Schranke formuliert — dieser Test wird rot —, nie als
vollständige Menge. Ergänzt Prüfregel 28: die Weltlage vor dem Kriterium umfasst auch die Tests,
die das Modell nicht kennt.

**63. Vor einem Prompt, der etwas bauen lässt, wird gemessen, ob es das schon gibt.**
Ein Prompt beschreibt, was entstehen soll; ein Werkzeug baut, was der Prompt verlangt. Keiner von
beiden sieht nach, ob der Bestand die Sache bereits trägt — der Prompt nicht, weil er die Frage
nicht stellt, das Werkzeug nicht, weil stiller Scope-Zuwachs verboten ist. In `00an` verlangte der
Prompt vier Beteiligte mit getrennten Verzeichnissen, einen dateibasierten Ausgang und einen Leser
dazu; all das lag unter `tools/sim/`, samt Inbox-Konvention, deklarativen Szenarien und Tests. Das
Werkzeug fand den Rahmen, benannte ihn und baute trotzdem neu, weil der Prompt es so verlangte
(D312). Der Griff davor ist nicht Prüfregel 38, die auf die Spec zeigt, sondern ein Blick in den
Baum: welches Verzeichnis trägt schon etwas, das so heisst wie der Auftrag.

**64. Eine Regel, die eine Menge ausdünnt, wird auf ihren zweiten Lauf geprüft, bevor sie in einen
Prompt geht.**
Ein Filter, der Elemente über Verweise anderer Elemente hält, kann im ersten Durchgang mehr binden
als im zweiten: fällt eine Quelle selbst heraus, verliert ihr Ziel die Bindung. Das Ergebnis ist
ein Aufräumen, das beim nächsten Mal wieder etwas findet, und eine gemeldete Zahl, die nichts
bedeutet. Die Regel gehört deshalb auf gebundene Quellen eingeschränkt und bis zum Fixpunkt
gerechnet. In `00ao` hielt eine ungebundene Nachlaufdatei eine Abnahmedatei; die Fassung im Prompt
band 28 Dateien im ersten und 27 im zweiten Durchgang, und das Werkzeug schloss die Lücke von
selbst (D315). Gegenstück zu Prüfregel 62: dort wird eine Menge zu leer, hier zu voll.

## Beim Bauen und Lesen von Tests

**12. Zwei Läufe, eine Variable.** Um zu zeigen, dass ein Mechanismus erreicht wird oder
wirkungslos ist, zwei Läufe über derselben Menge vergleichen, die sich in genau einer Größe
unterscheiden. Eine Bedingung zu prüfen, die auch andere Ursachen erfüllen könnten, ist schwächer
— und liest sich gleich.

**13. Neustart als Annahme.** Modelliert ein Test einen Neustart, wird gefragt, ob dieselbe
Ursache auch **ohne** Neustart eintreten kann. Wenn ja, ist der Weiterlauf ein eigener Vektor und
keine Variante. Die Absturzaufzählung in D128 konnte B-1 strukturell nicht sehen, weil jeder
ihrer Läufe nach dem Bruch ein frisches Objekt baute.

**30. Eine Variantenwelt braucht eine Nullprobe.** Wer eine Welt baut, um darin genau ein Feld zu
verändern, baut sie zuerst mit **unverändertem** Feld und weist nach, dass sie die Referenzwelt
reproduziert — bei Claims claim-ID-genau. Ohne diese Nullprobe misst die Variantenmessung den
Bauapparat und nicht die Variante. In `00k` hat sie im ersten Messwert gefangen, dass beide Welten
aus denselben `Identity`-Objekten gebaut waren: `Identity` führt `h_prev` intern fort, die zweite
Welt zeigte auf Vorgänger, die in ihrem eigenen Speicher nicht liegen, ihre Stimmen waren nicht
`ACTIVE`, und der daraus gelesene Befund war ein Artefakt des Baus.

**35. Eine Grenze auf zwei Schichten braucht auf jeder einen Wächter.** Wird ein Verhalten von zwei
Stellen zugleich erzwungen, hält ein Prüffall auf der äusseren die innere nicht: die Probe an der
inneren Stelle bleibt grün, weil die äussere das Ergebnis ohnehin verwirft. In D203 blieb der
Kettentest grün, als die Weitergabe auf den tragenden Pfad von `§4.1` gelegt wurde, weil
`resolve_epoch` dessen Vermerke gar nicht liest. Wer eine Grenze prüft, misst zuerst, wie viele
Stellen sie halten.

**45. Eine Probe darf den Produktivcode nicht formen.**
Entsteht Code, den nur die Rücknahmeprobe braucht, ist die Probe falsch konstruiert und nicht der
Code unvollständig. In `00y` kam eine Abfrage auf die Zahl der Regex-Gruppen in `check_specs.py`
hinzu, weil die Probe eine Gruppe entfernte; im Produktivpfad war die Abfrage konstant wahr. Die
Probe ließ sich stattdessen bauen, indem das Trennzeichen der Gruppe durch ein nie vorkommendes
ersetzt wurde — Gruppe bleibt, matcht nie, Befund feuert.

**57. Wo zwei Pfade gekoppelt geprüft werden, braucht jeder zusätzlich einen Träger.**
Ein Test, der zwei Erzeugerpfade gegeneinander hält, bindet die Übereinstimmung und nicht den
Wert. In `00ah` blieb der Kopplungstest zwischen `classify` und `classify_all` grün, während beide
Pfade denselben falschen Zustand lieferten; er war die ganze Zeit da und hat `SUPERSEDED` nie
gesichert. Neben die Kopplung gehört je Pfad ein Träger, der den Wert behauptet (D278).

## Bei Rücknahmeproben und Mutanten

**23. Die Rücknahmeprobe setzt an der ungeschützten Seite an.** Behauptet ein Test die
Übereinstimmung zweier Orte, sind die Orte selten gleich bewacht. Wer für die Probe den Ort
anfasst, an dem schon ein anderer Test hängt, bekommt Rot aus fremder Ursache — die Probe sieht
bestätigt aus und beweist nichts. Vor jeder Probe steht daher die Frage: **was außer dem
geprüften Test könnte hier noch rot werden?** Die Antwort muss „nichts" sein. In D147 wurde
`genesis_res[9]` verändert; das ändert den Hash und schlug beim Bestandsanker `N_res` an, bevor
`resolve_trust_params` überhaupt lief. Die ungeschützte Seite war das `TrustParams`-Literal, das
an keinem Hash hängt. Unterschied zum Zusatz in Regel 21: dort ist die Probe **unmöglich**, hier
ist sie **zweideutig**.

**34. Eine Rücknahmeprobe, die eine Prüfung entfernt, belegt nicht ihren Ort.** Wer eine Prüfung an
eine bestimmte Stelle setzt, nimmt sie in der Probe nicht heraus, sondern **verschiebt** sie an die
verworfene Stelle. In `00m` fielen bei entfernter Prüfung beide Fälle rot, bei verschobener nur der
neue — und erst das zeigte, dass der ältere die Stelle nie gehalten hat. Dieselbe Begründung wie
bei Prüfregel 23: die Probe muss die unbewachte Seite treffen.

**49. Eine Rücknahmeprobe neutralisiert die Träger einer Pflicht geschlossen.**
Wer eine Pflicht mit der Rücknahmeprobe misst, bestimmt zuerst die vollständige Menge ihrer
Träger und neutralisiert sie zusammen. Bleibt eine von mehreren gleichwertigen Stellen stehen,
zeigt ein grüner Lauf nur, dass die neutralisierte Stelle für die bestehenden Tests unsichtbar
ist — nicht, dass die Pflicht ungeprüft ist; ein Test über einen anderen Einstiegspunkt bekommt
dieselbe Ausnahme von einer der übrigen. Vier Module rechnen die Genesis-Bindung byte-gleich
nach, drei weitere werfen wortgleich zur Policy-Bindung; nach einer Einzelprobe heißt eine Pflicht
darum unbestimmt und nicht ungeprüft. Bleibt bei geschlossener Neutralisierung ein Test rot, ist
sie geprüft, auch wenn keine Einzelstelle für sich rot zu faerben war. Umgekehrt zu Prüfregel
41: eine ausbleibende Abweichung ist erst dann ein Befund, wenn ein paralleler Träger
ausgeschlossen ist (D245).

**53. Die Überdeckung geht der Mutation voraus.**
Ein Mutant an einer Stelle, die kein Test erreicht, überlebt immer und sagt nichts. Ein Lauf mit
`coverage` trennt die Menge vorab in „nie erreicht" und „erreicht"; nur die zweite Klasse braucht
Mutanten, und der Befund der ersten steht schon fest. In `00ai` fielen so von 37 Erzeugerstellen
19 als überlebende Mutanten an, davon 16 nie erreicht — die teure Messung war nur für die
restlichen drei nötig. Umgekehrt gilt die Grenze: erreicht heißt nicht gebunden, und dafür bleibt
die Mutation das einzige Mittel (D280).

**60. Eine Rücknahmeprobe wird an ihrem roten Test abgenommen, nicht an ihrer Anzahl.**
Rot heißt nur, dass irgendein Test die Neutralisierung bemerkt hat. Soll die Probe eine benannte
Entscheidung halten, muss der rote Test derjenige sein, der sie trägt; jeder andere ist ein
Nachbartor, und eine Zahl im Bericht kann den Unterschied nicht zeigen. Der Prompt verlangt darum
den Namen. Dazu die Bedingung an einen Fall, der zwei Tore trennen soll: er muss das vordere Tor
passieren und hinter dem hinteren ein anderes Ergebnis erzeugen; beides wird gemessen, bevor er in
einen Prompt geht. In `00ak` machte das entfernte Hexziffern-Tor genau einen Test rot, und es war
der falsche — die gespiegelte Konvention aus D293 hing an keinem Test (D296). Gegenstück zu
Prüfregel 53 in der Gegenrichtung: dort wird der Träger an seiner Zielzeile gemessen statt an
seinem Grün, hier die Probe an ihrem roten Test statt an ihrer Zahl.

**62. Eine Rücknahmeprobe darf die Menge nicht leeren, über die ihr roter Test quantifiziert.**
Ein Test der Form "für jedes Element dieser Menge gilt" ist wahr, sobald die Menge leer ist. Nimmt
die Probe genau das weg, was die Menge füllt, wird der Test nicht rot, sondern stumm, und ein
Bericht, der nur grün meldet, kann den Unterschied nicht zeigen. Vor jeder Probe wird darum
gefragt, welcher Test die Nichtleere trägt; dieser ist der erwartete rote. In `00al` sollte eine
Probe die Familie C kanonisch neu kodieren und den Bauart-Test rot machen; die Aufnahme verwarf die
kanonischen Bytes als Saatbytes, die Familie wurde leer, und der Test blieb über der leeren Menge
wahr (D304). Zusatz zu Prüfregel 60: dort geht es um den Namen des roten Tests, hier darum, dass er
überhaupt rot werden kann.


## Beim Messen

**19. Kalte Messung.** Ein grüner Testlauf auf der Arbeitskopie ist keine Aussage über den
Commit. Zustand außerhalb von git — `.hypothesis/`, `__pycache__`, warme Caches — wird vor jeder
Behauptung über `main` gelöscht. `make check-all` führt `check_tree.py` und hat damit ein Tor
gegen vergessene **Dateien**; gegen vergessene **Zustände** gibt es keines. Genau darin lag D137.

**26. Ein Hashtest hat ein Verfallsdatum.** Der Abgleich einer Projektkopie gegen das Repo gilt
für den Commit, an dem er gemacht wurde, und für keinen späteren. Jeder Merge, der eine Datei
anfasst, entwertet ihn — die Kopie sieht danach unverändert lesbar aus, und nichts wird rot. Vor
jeder Zählung, die in einen Prompt geht, wird gefragt: hat seit dem Abgleich ein Lauf diese Datei
berührt? In D169 hat der Supervisor `_policy(` in einer Kopie von vor dem `00b`-Merge gezählt und
sechs Aufrufstellen genannt, wo zehn standen; die vier fehlenden hatte `00b` selbst angelegt.

**43. Zwischen Merge und Nachzug ist die Projektkopie kalter Kaffee.**
Die Kopie wird nach jedem Push nachgezogen, nicht nach jeder Sitzung (D224). Wer davor eine Zahl
aus der Kopie nennt, sagt dazu, dass sie hinter `main` liegt — sonst ist es eine Behauptung über
einen Baum, den es so nicht gibt. Von Hand nachgepatchte Kopien sind der schlechteste Fall: sie
sehen aktuell aus. In `00u` lief `tools/check_specs.py` vier Merges lang in der Rekonstruktion
des Supervisors statt in der Fassung des Werkzeugs.

**44. Abgeleitete Zahlen werden gerechnet, nicht aus der eigenen Tabelle nachgezählt.**
Ein Abnahmekriterium, das eine Anzahl nennt, leitet sie aus der Messung ab, die dem Prompt
zugrunde liegt. In `00y` nannte Prompt D sieben betroffene Testdateien, während die eigene
Tabelle darüber neun listete, und eine Probe fünf statt sechs. Die Messung lag vor; gezählt wurde
im Kopf. Das Werkzeug hat beide Abweichungen gemeldet und die Tabelle umgesetzt — richtig, aber
ein Kriterium, das der Auftrag verletzt, ist kein Kriterium.

**46. Zeilennummern und Zeilenzahlen aus der Projektkopie sind um eins zu hoch.**
Jeder Dateikörper im repomix-Archiv beginnt mit einem Zeilenumbruch hinter dem Dateitag; wer ihn
aufteilt, zählt eine Leerzeile mit. In `00z` trugen fünf Zeilenangaben eines Prompts und beide
Splice-Trockenläufe denselben Versatz. Er fällt in jeder Differenz heraus — der Zuwachs stimmt,
die Stelle nicht — und bleibt darum lange unentdeckt. Vor jeder absoluten Zeilenangabe die
führende Leerzeile abziehen. Im Prompt bleibt der Ankertext maßgeblich; die Nummer ist ein
Hinweis, keine Adresse.

**48. Eine abgeleitete `numstat`-Erwartung zieht die randgleichen Zeilen ab.**
Git zieht Zeilen, die am oberen oder unteren Rand eines Blocks unverändert bleiben, nicht in den
Hunk. Wer je Block die vollständige Alt-Menge als Löschung und die vollständige Neu-Menge als
Einfügung rechnet, erwartet systematisch zu viel: für den Lauf zu D238 stand +179 -82 gegen
gemessene +147 -50, und die Differenz von 32 auf beiden Seiten war genau die Zahl der randgleichen
Zeilen. Ohne den Abzug sieht eine Abweichung, die nichts bedeutet, aus wie ein Befund. Das ergänzt
Prüfregel 41 um einen Fall, in dem die Abweichung vor der Bewertung gerechnet werden kann (D244).

**51. Ein Prüfer, der eine Menge misst, wird zuerst an einem vorhandenen Element geeicht.**
Wer ein Skript baut, das erwartete Werte im Text sucht, prüft es zunächst gegen ein Element, das
im Bestand schon steht. Die Rücknahmeprobe reicht dafür nicht: sie zeigt, dass der Prüfer
reagiert, nicht dass er das Richtige misst. Gemessen in `00ad`: ein Diagnoseskript für Anhang C
meldete gegen den Vorzustand pflichtgemäß null Treffer und gegen den Zielzustand ebenfalls null
für die Bytes — weil es die signierten Bytes suchte, der Anhang aber nach dem Muster von C.1 den
Core und die Signatur getrennt führt. Ein Probelauf gegen TV1 hätte das im ersten Zug gezeigt und
einen Umlauf gespart. Ergänzt Prüfregel 49: eine Probe sichert die Richtung, nicht den Maßstab.

**67. Eine Szenariokonstruktion trägt keine Bedingung, die die Frage nicht verlangt.**
Gabelung, Partition und Teilwissen sind bequeme Aufbauhilfen; sie erlauben mehrere Fälle in
einer Welt. Wer sie aus Bequemlichkeit einbaut, bindet den Befund an sie, und wer ihn in
einem Jahr liest, hält die Bedingung für notwendig. Vor der Abnahme wird die bequeme
Bedingung gestrichen und der Fall ohne sie nachgebaut; hält der Befund auch dann, ist er
stärker und gehört in dieser Fassung ins Register. In `00ay` gerissen: drei
Konfliktstimmen hingen per `claim_gabeln` an einer Spitze, weil sonst die Vorgänger
fehlten, und der Rückfall las sich als Folge einer Equivokation. Ohne Gabelung und mit
Vollzustellung an alle trat er unverändert ein (D345).

**68. Eine Prüfung auf Abwesenheit braucht einen zweiten Lauf mit anderem Fehlermodus.**
Eine Prüfung auf Anwesenheit ist mit dem ersten Treffer fertig. Eine auf Abwesenheit ist
es nie: bleibt sie ohne Treffer, belegt das nur, dass ihre eigene Konstruktion nichts
gefunden hat. Eine Suche über benannte Begriffe ist blind gegenüber allem, was ohne diese
Begriffe auskommt, und ein Ausschnitt als Grundlage erbt die Grenzen seines Zuschnitts.
Wer Abwesenheit zusichert, lässt deshalb einen zweiten Lauf mit anderem Fehlermodus
darüber — zweimal dasselbe Verfahren ist keine zweite Prüfung. In `00az` beim Kuratieren
des Antrags-Logs gerissen: die Mustersuche fand die Stellen, die ihre Schlagwörter
enthielten, und übersah einen Abschnitt, der keines davon trug; erst ein vollständiges
Lesen durch ein zweites Werkzeug fand ihn (D349).

## Beim Fahren von Blöcken und Splices

**39. Eine Ausgabe ist keine Bedingung.**
In einer `and`-Kette entscheidet der Rückgabewert, nicht der gedruckte Text. `git branch
--show-current`, `git log` und `grep -c` liefern Status 0, auch wenn sie das Falsche zeigen; wer
einen Zustand sichern will, braucht `test`, `--is-ancestor`, `--quiet` oder `-c` mit Vergleich. In
`00r` galt eine Branchausgabe als Prüfung, und der Lauf-Commit landete auf `main` (D211).

**40. Der erwartete Kopf des nächsten Blocks wird abgeleitet, nicht erinnert.**
Was ein Block hinterlässt, steht im Block, nicht im zuletzt gesehenen Hash. Ein Block, der
committet und nicht pusht, lässt `main` und `origin/main` auseinanderlaufen; ein Block, der einen
Branch anlegt, lässt `main` stehen; ein Übergabe-Commit hebt den Kopf über den Stand, auf dem die
eigene Kopie steht. Wer im nächsten Zug `test (git rev-parse HEAD ...) = <hash>` schreibt, ohne
diesen Zustand gemessen zu haben, hält die Kette auf einer Zahl an, die nie galt — und der
Operator zahlt einen Zug für einen Fehler, der keiner war. Liegt kein gemessener Hash vor, wird
die **Beziehung** geprüft: `git rev-parse main` gegen `impl/00x^`, `--is-ancestor`, oder
`origin/main` statt `main`. In `00s` zweimal gerissen (D214).

**42. Der Assert eines Splices prüft das Ergebnis, nicht den eingesetzten Text.**
Ein Splice, der eine Länge, eine Anzahl oder eine Form zusichert, misst sie an der Datei, wie sie
nach dem Schreiben aussieht — nicht am Block, den er einsetzt. Der Unterschied ist nicht
theoretisch: eine Ersetzung mitten in einem Absatz kann jede Zusicherung des eingesetzten Textes
erfüllen und die Zeile daneben auf das Doppelte der Grenze bringen (D223).

**55. Ein Anzahl-Assert in einem Splice wird abgelesen, nicht gerechnet.**
Ein Assert auf eine erwartete Anzahl fängt mehr als eine Anwesenheitsprüfung (Prüfregel 42), aber
nur, wenn die Zahl stimmt. In `00ah` sind drei von vier Anzahl-Asserts beim ersten Lauf gefallen,
jedes Mal, weil die Zahl im Kopf gerechnet statt im Wegwerfbaum gemessen war. Jeder Fehlschlag
kostet einen Durchlauf und ist der billigste vermeidbare Fehler der Sitzung. Die Zahl wird vor dem
Schreiben des Skripts im ausgepackten Baum gegriffen.

**58. Im Merge-Block steht `git push` vor `git branch -d`.**
`git branch -d` prüft die Zusammenführung gegen den Upstream. Ein lokal gemergter Branch gilt als
unzusammengeführt, solange `main` nicht gepusht ist, und der Löschbefehl scheitert mitten in der
Kette. Die Reihenfolge ist damit nicht Geschmack, sondern Bedingung.

**65. Der zweite Lauf eines Splices muss scheitern, nicht nur der erste gelingen.**
Ein Assert, der nur die Eingangsbedingung des ersten Laufs prüft (der Anker kommt einmal vor),
bleibt nach dem Einsetzen unverändert wahr, wenn der Anker selbst nicht verbraucht wird — der
zweite Lauf des Harnesses (`splice_run.py`) gelingt dann ein zweites Mal, gilt als nicht
idempotent-sicher und wird verworfen, samt der eigentlich richtigen ersten Anwendung. Der Assert
prüft deshalb zusätzlich auf das Zielmuster, das erst nach dem ersten Lauf existiert (z. B. die
neue Überschrift), oder verbraucht den Anker selbst. In `00ax` beim Schreiben von D342 gerissen
(D343).

**66. An einem Gate wird die Ausgabe nicht gekürzt.**
Vor jedem Tier-1-Zug (Merge, `git push`, Branch- oder Dateilöschung) steht ein prüfender
Lauf — `make check`, ein Testlauf, ein Linter. Wird dessen Ausgabe in derselben `and`-Kette
durch eine Pipe gekürzt (`| tail`, `| head`, `| grep`), entscheidet der Status des letzten
Pipeglieds, nicht der des Prüflaufs; `tail` gelingt praktisch immer, und das Gate ist blind.
Entweder läuft der Prüfbefehl an dieser Stelle ungekürzt, oder sein Status wird ausdrücklich
geprüft (`$pipestatus[1]`), oder er steht in einem eigenen Block, dessen Ergebnis vor dem
Tier-1-Zug gelesen wird. Die Kürzungsdisziplin aus `arbeitsweise.md` gilt für Diagnose, nicht
für Gates. In `00ax` gerissen: ein roter `make check` wurde gemergt und gepusht, und derselbe
Mechanismus hatte seit `00aw` einen Lint-Fehler verdeckt (D344).

## Bei der Abnahme und beim Merge

**56. Ein Bericht ohne den Diff ist keine Lieferung.**
Ein Werkzeugbericht, der den Diff als geliefert bezeichnet, ohne ihn zu enthalten, wird nicht als
Lieferung behandelt und nicht abgenommen; der Diff wird nachgefordert. In `00ah` enthielt der
nachgeforderte Diff den Defekt, den der Bericht nicht sah. Das ist kein Formalismus, sondern der
Grundsatz aus der dauerhaften Anweisung in seiner engsten Form: geprüft wird der Diff, nicht die
Meldung darüber.

**59. Eine aus einem Diff rekonstruierte Fassung wird über Quellhashes verankert.**
Wer einen gelieferten Diff im ausgepackten Baum nachbaut, um gegen die Fassung statt gegen ihre
Beschreibung zu messen, hat zwei Fehlerquellen: den Diff und die Rekonstruktion. Ein
`sha256sum -c` über vier bis sechs Quelldateien schließt die zweite und geht als zweiter Job in
denselben Block wie der Hash-Test der gelieferten Dateien. Der Archivhash der Projektkopie taugt
dafür nicht, und der `--header-text` kann eine Sitzung alt sein.

---

**61. Eine Abweichung zwischen zwei Fassungen ist erst ein Befund, wenn die Spec den Punkt
festlegt.**
Ein Vergleich Zeile für Zeile behandelt jede Ausgabe als bestimmt. Wo der Text eine Wahl
ausdrücklich freistellt, meldet er Freiheit als Uneinigkeit, und zwar bei jedem Lauf aufs Neue, bis
jemand die Meldung für Rauschen hält. Vor der Bewertung steht deshalb die Frage, ob beide Ausgaben
einen wahren Satz über dieselbe Eingabe tragen; erst wenn einer von beiden falsch ist, liegt ein
Befund vor. In `00ak` meldete der erste Lauf der Kampagne zwölf Zeilen und enthielt keinen Befund:
`01 §B.2` stellt die Wahl unter mehreren wahren Codes frei (D299). Der billige erste Griff ist
Prüfregel 38 — und wo `tools/register_index.py` schweigt, weil der Verweis auf einen Anhang zeigt,
wird gegrept statt geschlossen.

## Herkunft der Nummern

Die Regeln 1–7 stammen aus `sitzungsstart-05.md`, 10–12 aus `sitzungsstart-anwendung.md`, 13–15
aus `sitzungsstart-einlesepfad.md`, 16–18 aus `sitzungsstart-buchfuehrung.md`, 19 aus
`sitzungsstart-kollision.md`, 20 aus `sitzungsstart-decke.md`, 21 aus D142, 22 aus D146, 23 aus
D148, 24 und 25 aus D160, 26 aus D169, 27 aus D173, 28 aus D179, 29 aus D184,
30 aus D192, 31 aus D196, 32 aus D200, 33 und 34 aus D201, 35 aus D203, 36 aus D205,
37 aus D208, 38 aus D209, 39 aus D211, 40 aus D214, 41 aus D217, 42 aus D223, 43 aus D224,
44 und 45 aus D229, 46 aus D232, 47 aus D239, 48 aus D244, 49 aus D245, 50 aus D254, 51 aus D257,
52 bis 59 aus D282, 60 aus D296, 61 aus D299, 62 aus D304, 63 aus D312, 64 aus D315,
65 aus D343, 66 aus D344, 67 aus D345, 68 aus D349.

Die Nummern **8** und **9** wurden in D144 vergeben. Parallelenprüfung und Begründungsprüfung
liefen bis dahin unnummeriert als „die beiden älteren" mit; ohne Nummer waren sie in Prompts
nicht zitierbar.
