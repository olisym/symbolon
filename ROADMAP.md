# Roadmap

Ein Plan, keine Norm. Er darf sich ändern; jede Änderung bekommt einen Eintrag im Register mit
Begründung. Gesetzt mit D466, fortgeschrieben mit D664. Was gelöst und was offen ist, steht
ausführlicher in `LAGE.md`.

## 1. Richtung

Bis D465 war die Arbeit vor allem Selbstprüfung: Spec lesen, Code gegen die Spec lesen, Mutanten
messen, Lücken binden. Das Protokoll ist dadurch sorgfältig geworden und dabei unsichtbar geblieben.
Ab D466 ist der Maßstab eine Anwendung, die man bedienen und sehen kann. Sie zeigt Fehler, die keine
Mutationsmessung findet: einen umständlichen Ablauf, eine Regel, die im Gebrauch nichts taugt, eine
fehlende Zutat.

Die Anwendungen bauen auf den Bausteinen, die es gibt: Identität, Nukleus mit Verfassung,
`vouch@1`, `obligation@1` und `receipt@1`, Anklage und Verdikt, Abstimmung über Epochen,
Schlüsselrotation, Widerspruchserkennung. Keine Anwendung soll neues Protokoll brauchen
(`VISION §3`). Wo eine es doch braucht, ist das ein Befund und kommt ins Register. Welche Lücken
dabei schon absehbar sind, hat D661 gegen Fiske und Ostrom geprüft (O105).

## 2. Phase 0 — Neuausrichtung

**Erledigt** (D466, D467). Restack ist abgekoppelt, die Härtung ruht, diese Roadmap gilt, das erste
Szenario ist ein Verein. Der Bond ist ausgemustert (D467).

## 3. Phase 1 — Der Verein auf Papier

**Erledigt** (D468 bis D470). Ein Verein mit drei Abläufen, Mitglied werden, Antrag und
Abstimmung, Beitrag, und dem Moment, für den das Ganze da ist: ein Mitglied stimmt mit demselben
Schlüssel Ja und Nein, und alle sehen die Kollision mit beiden Unterschriften als Beweis
(`08 §2.2`). Geschrieben als `szenario-verein.md`; was es von Phase 2 verlangte, steht in
`szenario-verein §7`.

## 4. Phase 2 — S-Node, Version 0

**Erledigt** (D471 bis D478). Der Lebensraum der Claims (`VISION §5`): ein kleiner Dienst, der den
Bestand in SQLite hält, neue Claims prüft, den Zustand ausrechnet und eine lokale
HTTP-Schnittstelle anbietet. Ein Knoten ist keine Protokollfigur, sondern eine Identität, die einen
Dienst anbietet (`06 §2`).

## 5. Phase 3 — Oberfläche mit dem Verein

**Erledigt** (D479 bis D512). Im Browser, gegen den Knoten aus Phase 2: Schlüssel anlegen,
beitreten, Antrag stellen, abstimmen, Beitrag zahlen und quittieren, die Kollision sehen. Der
Schlüssel entsteht im Browser und verlässt ihn nicht.

## 6. Phase 4 — Simulation

**Erledigt** (D513 bis D554), dazu die Lücken zwischen Norm und Bau (D555 bis D581). Mehrere
Knoten, Personen mit eigenem Verhalten, Lüge und Versehen, mehrere Geräte einer Person mit eigenem
Schlüssel unter einer Wurzel (D529 bis D546), Sachanträge neben der Satzung (O96, D581). Jeder
Knoten zeigt denselben Zustand, sobald er dieselben Claims hat; wer sich widerspricht, fällt auf.

## 7. Phase 5 — Reticulum

**Im Lab erreicht** (D583 bis D638). Knoten gleichen sich über Reticulum ab, über einen Boten je
Knoten: Ankündigung nach Trickle, Abgleich nach Bereichen, Bündel, Rundruf an der Quelle (O97,
D617). Gemessen über einen simulierten Funkkanal mit 1200 bit/s und 5 % Verlust; ein Wahlgang
passt hindurch. Reticulum macht das Netz, der Bote trägt nur, was ein Verein weiss (D617).
Nebenbei: Wahlgänge und Patt (D594 bis D606).

**Ruht:** Funk über echte Hardware (T-Beams), bis sie da ist (D639). Offen bleibt der gehäuft
scheiternde Linkaufbau unter Verlust (O104).

## 8. Danach

### 8.1 Die Gründung — laufend

Drei gründen einen Verein gemeinsam am Tisch, alle drei sind Anker (O101, D640 bis D657). Vier
Schritte (D641 Beschluss 1):

1. Der Weg im Knoten. **Gebaut** (D641, D642), mit Vorlage, geschützten Feldern und Typen (D646,
   D648).
2. Die Bildschirme auf einem Knoten, mit Verwerfen. **Gebaut** und von Oli durchgespielt (D651 bis
   D655).
3. Der Scan mit Schlüssel und Adresse, der Knoten am Telefon. **Bestandsaufnahme gemessen**
   (D657); als Nächstes in diesem Strang.
4. Der Knoten hält nur eigene Scopes.

Danach die Verabredung zu zweit als zweite Vorlage (D640 Beschluss 3) und die Einladung aus der
Ferne (D654 Befund 5).

### 8.2 Die Lücken aus der Querprüfung

D661 hat sechs Stellen gefunden, die die Bausteine nicht abbilden (O105). Jede wird ein eigener
Strang; vor einer Position wird nachgeschlagen (D640). Die Reihenfolge:

1. **Geheime Wahl.** Als Nächstes, vor Schritt 3 der Gründung (D664). Sie betrifft den Verein
   unmittelbar, und das Feld ist seit Jahrzehnten erforscht.
2. Die übrigen fünf (Vertretung, Marktpreis und Tausch, verschachtelte Ebenen, Verzeihen,
   Schlichtung auf der Seite), wenn ein Szenario sie braucht oder Oli sie vorzieht.

### 8.3 Weitere Szenarien

Kandidaten sind die Food-Koop, ein freier Markt, eine Versicherung, ein Sicherheitsdienst. Was
davon kommt und in welcher Reihenfolge, ist offen. Den Bond gibt es nicht mehr; was er lösen
sollte, beantwortet jedes Szenario für sich (D467). Ein Markt prüft auch, ob Ansehen ohne zentrale
Bewertung unter Fremden trägt (D660 Befund 3).

## 9. Was ruht

- Lese- und Mutationsrunden über bestehenden Code, ausser eine Anwendung stolpert über einen Fehler.
- Der Nachzug der Rust-Fassung, weiter nach D409 Beschluss 3.
- Funk über echte Hardware, bis die T-Beams da sind (D639).
- Die Paketierung für `pip install` (D662 Beschluss 2); bis dahin trägt der Weg aus der README.
- Vertagte Posten in `offen.md` öffnet ein Szenario, das sie braucht, nicht der Kalender.
