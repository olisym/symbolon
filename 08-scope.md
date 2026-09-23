# 08 — Zweck und Geltungsbereich

Dieses Dokument ist normativ für die Frage, **was in das Protokoll gehört und was nicht**. Es
beschreibt keinen Mechanismus. Es liefert das Kriterium, nach dem über die Aufnahme eines
Mechanismus entschieden wird, und die Begründungen, aus denen dieses Kriterium folgt.

Bei jedem Fork, bei dem eine Regel als Protokollbestandteil vorgeschlagen wird, ist Abschnitt 3
zu prüfen, bevor die Regel geschrieben wird.

---

## 1. Zweck

Menschliche und maschinelle Zusammenarbeit trägt Reibungskosten, die nicht aus der Sache
stammen, sondern aus der Unsicherheit über das Gegenüber: Prüfen, Absichern, Rückversichern,
Nachfassen. Diese Kosten fallen bei den Kooperationswilligen an, und sie sind für sie reiner
Verlust.

Das Protokoll senkt eine bestimmte, klar umrissene Sorte dieser Kosten: den Aufwand
festzustellen, **ob jemand anderswo etwas anderes erzählt hat**. Was dabei an Reibung
entfällt, bleibt bei den Beteiligten. Das ist der ganze Anspruch.

Das Protokoll entwirft kein politisches oder gesellschaftliches System. Es stellt die
Infrastruktur bereit, auf der Menschen eines vereinbaren können — und zwar so, dass die
Vereinbarung nachprüfbar ist, ohne dass jemand befragt werden muss, der über ihr steht.

---

## 2. Was das Protokoll leistet — und was nicht

### 2.1 Zurechenbarkeit, nicht Wahrheit

Das Protokoll ist bedeutungsblind. Es prüft nicht, ob ein Vouch verdient, eine Obligation
tatsächlich entstanden oder eine Aussage zutreffend ist. Eine falsche Aussage kann signiert
werden und ist dann protokollgültig.

Was das Protokoll erzwingt, ist **Zurechenbarkeit und Widerspruchsfreiheit**: jede Aussage hat
genau einen Urheber, und derselbe Urheber kann nicht zwei einander widersprechende Aussagen
gültig in der Welt halten.

Die Formulierung ist keine Bescheidenheit, sondern eine Schranke. Sobald das Protokoll
begänne, Aussagen gegen die Welt zu prüfen, wäre die Bedeutungsblindheit verloren — und mit
ihr die Eigenschaft, dass beliebige Inhalte über dieselbe Mechanik laufen können.

### 2.2 Widersprüche werden unbestreitbar, nicht unmöglich

Equivocation wird nicht verhindert. Unter Partition können zwei einander widersprechende
Zweige beliebig lange nebeneinander zirkulieren; genau deshalb gilt die Monotonie-Eigenschaft
der Ableitungsschicht, dass fehlendes Wissen ein Ergebnis nur senken und nie heben kann.

Was das Protokoll leistet: sobald zwei widersprechende Claims bei einem Beobachter
zusammentreffen, ist der Widerspruch **ein vom Urheber selbst signierter Beweis gegen ihn**.
Nicht bestreitbar, nicht abstreitbar, nicht auf ein Missverständnis schiebbar.

Daraus folgt eine Bedingung, die für die Priorisierung zählt: eine Aussage wird nicht dadurch
überprüfbar, dass sie signiert ist, sondern dadurch, dass sie mit anderem Signierten
**kollidieren kann**. Ein Claim, auf den nichts zeigt und der auf nichts zeigt, ist
unwiderlegbar und folgenlos. Die Kraft des Protokolls wächst mit dem Anteil des tatsächlichen
Zusammenlebens, der als verknüpfte Claims ausgedrückt wird — nicht mit der Anzahl der
Spezifikationsschichten.

### 2.3 Kein Konsens, kein objektiver Zustand

Es gibt keinen gemeinsamen Zustand und keine Instanz, die ihn feststellt. Jeder Beobachter
rechnet lokal aus dem, was er hat. Die Ergebnisse konvergieren, soweit das Wissen konvergiert.

In einem Punkt konvergieren sie nicht: über den Ablauf einer Frist dürfen zwei korrekte
Verifizierer dauerhaft uneins sein, weil sie verschiedene Uhren haben. Das ist der einzige
zugelassene Fall und wird ausdrücklich getragen.

Jede Erzwingung eines gemeinsamen Zustands verlangt eine globale Ressource. Eine globale
Ressource ist eine Machtstelle. Deshalb gibt es sie hier nicht.

### 2.4 Kosten verlagern sich, sie verschwinden nicht

Der Aufwand sinkt nicht gegen Null. Schlüsselverwaltung, Verfügbarkeit, Verbreitung und
Nachrechnen sind reale Lasten, und sie sind neu. Was entfällt, ist die eine Kostenart aus
Abschnitt 1. Sie ist groß genug, dass sich der Tausch lohnt; sie ist nicht alles.

---

## 3. Das Aufnahmekriterium

> **Test:** Senkt der Mechanismus die Kosten dafür, festzustellen, wer was gesagt hat — oder
> verteilt er Macht?
>
> Senken: Protokoll. Verteilen: Policy.

Ein Mechanismus, der Macht verteilt, wird nicht deshalb zum Protokollbestandteil, weil er gut
begründet ist oder weil er sich sauber implementieren lässt. Er gehört in die Verfassung eines
konkreten Nukleus, wo er geändert werden kann, ohne dass jemand das Protokoll wechseln muss.

Anwendung auf den Bestand:

| Gegenstand | Wirkung | Ort |
| --- | --- | --- |
| Kette, Signatur, Equivocation-Ausschluss | senkt Prüfkosten | Protokoll |
| Trust-Flow, Budget, Kapazitätsschranken | begrenzt Torwächterschaft | Protokoll |
| Mitgliedschafts-, Tilgungs- und Verdikt-Zustände | machen Zustände feststellbar | Protokoll |
| Epochenkette und Änderungsverfahren | ersetzen eine Autorität für Regeländerungen | Protokoll |
| Slashing, soweit downside-only | macht Ausfall teuer, ohne Aufbau zu erlauben | Protokoll, eng |
| Gewichtete Auszählung | verteilt Macht | Policy, in v1 nicht vorhanden |
| Losverfahren, Amtszeiten, Appeal-Pfade | verteilen Macht | Policy |
| Schwellenwerte, Arbitratorenlisten, Ressourcengrenzen | verteilen Macht | Policy |
| Werkzeug: Schlüssel halten, Claims bauen, Empfangenes einlesen | erzeugt Claims, senkt nichts | Werkzeug, weder Protokoll noch Policy |
| Ort der Schreibautorität, Geräte als Endpunkte | Betrieb | Werkzeug (D123) |
| Gruppen-Soll (Anspruch einer Gruppe gegen einen Beitragspflichtigen) | verteilt Macht (wer zählt zur Gruppe, wessen Nichtzustimmung bindet); Umlage aus bilateralen Obligationen reicht bereits | kein neuer Mechanismus nötig (O1, D327) |
| Verwahrerrolle (Sammelstelle mit Auszahlungspflicht) | konzentriert Macht über die Auszahlungsentscheidung | Policy, eigener Scope (O2, D327), `00 §4.2` |
| Prädikat für den Versicherungsfall | macht einen Zustand feststellbar | Protokoll, bereits vorhanden: `accusation@1` (D67, D327) |
| Prämie und Deckungssumme einer Versicherung | Preisbildung, `03 §3.1` | Wertschicht, nicht vorhanden (O5, D313, D423) |
| Mitgliedschaftsprüfung in `settlement` | bestimmte, wer Gläubiger sein darf, und koppelte die Substanz an den Governance-Scope | nicht Protokoll; ein Werkzeug darf beim Lesen filtern (O6, D423), `00 §4.2` |
| Gläubiger-Timeout (Obligation endet ohne `t_exp` des Schuldners) | Erlass trägt `receipt@1`, Ausfall `accusation@1`; ein Zustand „überfällig" läse aus Ausbleiben Absicht (§7) | kein neuer Mechanismus nötig (O7, D423) |

Die Prüftabelle ist bei jedem neuen Mechanismus fortzuschreiben. Ein Eintrag in der rechten
Spalte "Protokoll" verlangt eine Begründung in der mittleren.

**Wohin vertagt wird.** Mehrere Schichten schieben Offenes an „die Anwendungsschicht" (`03 §3.4`
atomarer Tausch, `06 §8` Prüfung externer Beweise, `01` A1 Transportbindung). Das ist **kein**
Empfänger, sondern mindestens zwei: ein **Werkzeug**, das Claims erzeugt und einliest, und eine
**Wertschicht**, die es nicht gibt. Keine der drei Vertagungen fällt an das Werkzeug. Wer künftig
vertagt, benennt den Empfänger — sonst wächst die erste Schicht, die gebaut wird, um fremde
Verpflichtungen.

---

## 4. Vertrauen ist kein Zahlungsmittel

Vertrauen wirkt in diesem Protokoll als **Flussverstärker**: es entscheidet, wie viel über eine
Kante getragen werden kann. Es ist damit ein Leitwert, keine Währung.

Der Unterschied ist normativ, nicht sprachlich:

- Vertrauen ist **nicht übertragbar**. Es fließt entlang tatsächlicher Kanten und lässt sich
  nicht abtreten.
- Vertrauen ist **nicht akkumulierbar**. Es wird nicht ausgegeben und nicht gespart; es begrenzt.
- Vertrauen ist **kein Stimmgewicht**. Ein Stimmgewicht wäre eine handelbare Größe, sobald
  jemand bemerkt, dass es sich lohnt.

Vorschläge, die diese drei Eigenschaften aufweichen, sind bereits mehrfach geprüft und
verworfen worden — Kapazitätsbelohnung für erfolgreiches Bürgen, Brücken- und
Betweenness-Prämien, anteilige Kapazitätsteilung. Sie kehren erfahrungsgemäß gut begründet
zurück. Das Kriterium bleibt: was übertragbar wird, wird gekauft, und was gekauft wird, ist
Torwächterschaft (D25).

---

## 5. Warum nichts global ist

Verhalten gilt lokal als angemessen. Es gibt Kreise, innerhalb derer eine Norm selbstverständlich
ist, und diese Kreise berühren sich an den Rändern und beeinflussen einander, ohne dass eine
von ihnen für die anderen entscheidet.

Daraus folgt die Scope-Architektur nicht als technischer Kompromiss, sondern als Abbildung:
**es gibt keine globale Norm, die zu erzwingen wäre.** Ein Protokoll, das eine erzwingt, bildet
die Wirklichkeit falsch ab, bevor es irgendetwas leistet.

Die Anschauung dazu: dieselben Menschen, derselbe Raum, verschiedene Verfassungen — von außen
nicht unterscheidbar. Eine Person kann in beliebig vielen Nuklei Mitglied sein, jeder mit
eigener Verfassung, eigener Arbitratorenliste, eigenem Budget, und kein Nukleus erfährt davon,
solange sie es ihm nicht erzählt. Das ist kein Sonderfall, sondern der Normalfall.

Zwei Abgrenzungen dazu:

1. Verschiedene Verfassungen für **verschiedene** Scopes sind gewollt. Verschiedene Verfassungen
   für **denselben** Scope sind ein Synchronisationsdefekt und bleiben es (D72).
2. Berühren sich zwei Kreise in einer Person, die sich in beiden zu Unvereinbarem verpflichtet,
   löst das Protokoll den Konflikt **nicht**. Es macht ihn unbestreitbar, weil beide Bindungen
   signiert in derselben Kette stehen. Der Rand zwischen zwei Kreisen ist die Kette einer Person.

Auch die Trennung von Mitgliedschaft und Ressourcenzugang folgt hieraus (D13): Zugehörigkeit
und Anspruch sind verschiedene Aussagen und werden getrennt erklärt.

---

## 6. Regeltreue und Defektion

Jedes System trägt auf der Annahme, dass die meisten Beteiligten sich an die Regeln halten.
Defektion ist parasitär: sie setzt eine regeltreue Mehrheit voraus und funktioniert nur,
solange sie unbemerkt bleibt. Niemand zieht in eine Nachbarschaft, in der alle stehlen.

Daraus folgt die Rangfolge der Abwehr:

1. **Sichtbarkeit** ist die eigentliche Leistung. Ein bemerkter Regelverstoß hat seinen Vorteil
   bereits verloren.
2. **Rückzug** ist die primäre Sanktion, und er ist endogen: Bürgen widerrufen, Kapazität
   versiegt, der Fluss erreicht den Betreffenden nicht mehr. Dafür braucht es keine
   Strafinstanz, sondern nur die Ableitungsschicht.
3. **Durchsetzung** deckt allein den Rest — den Schaden, der entstanden ist, bevor der Rückzug
   greifen konnte. Dafür sind Bonds da, und nur dafür sind sie downside-only (D40).

Es ist ausdrücklich **nicht** behauptet, dass Defektion für den einzelnen Defektor irrational
sei. Ihr Gewinn ist konzentriert, ihr Schaden verteilt; das ist der Grund, aus dem es sie gibt.
Behauptet wird, dass sie nicht verallgemeinerbar ist und dass ihr Vorteil mit der Sichtbarkeit
verschwindet.

---

## 7. Getragene Grenzen

Was dieses Protokoll ausdrücklich nicht liefert:

- **Keine Wahrheit über die Welt.** Nur Zurechenbarkeit und Widerspruchsfreiheit (2.1).
- **Keine Verhinderung von Täuschung.** Nur ihre Unbestreitbarkeit nach dem Zusammentreffen (2.2).
- **Keine Einigkeit über Fristablauf.** Zwei korrekte Verifizierer dürfen uneins sein (2.3).
- **Keine Unterscheidung von Verweigerung und Ausbleiben.** `OPEN` heißt „aktiv, keine passende
  Quittung" (`03 §3.3.2`) und deckt drei Lagen: nicht gezahlt, nicht quittiert, nicht zugestellt.
  Wer daraus auf Unwilligkeit schließt, verwechselt Partition mit Absicht (D423).
- **Keine Deckung.** Ein Bond ist eine Zusage, kein Treuhandkonto. Ausfall wird sichtbar und
  teuer; unmöglich wird er nicht.
- **Keine Wiedergutmachung ohne Beteiligte.** Alles, was das Protokoll tut, setzt voraus, dass
  jemand hinschaut und daraufhin handelt.

Diese Liste ist Teil der Zweckbestimmung. Ein Mechanismus, der eine dieser Grenzen aufheben
will, ändert den Zweck und ist entsprechend zu behandeln.
