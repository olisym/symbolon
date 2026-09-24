# Roadmap

Ein Plan, keine Norm. Er darf sich ändern; jede Änderung bekommt einen Eintrag im Register mit
Begründung. Gesetzt mit D466.

## 1. Richtung

Bis D465 war die Arbeit vor allem Selbstprüfung: Spec lesen, Code gegen die Spec lesen, Mutanten
messen, Lücken binden. Das Protokoll ist dadurch sorgfältig geworden und dabei unsichtbar geblieben.
Ab hier ist der Maßstab eine Anwendung, die man bedienen und sehen kann. Sie zeigt Fehler, die keine
Mutationsmessung findet: einen umständlichen Ablauf, eine Regel, die im Gebrauch nichts taugt, eine
fehlende Zutat.

Die Anwendungen bauen auf den Bausteinen, die es gibt: Identität, Nukleus mit Verfassung,
`vouch@1`, `obligation@1` und `receipt@1`, Anklage und Verdikt, Abstimmung über Epochen,
Schlüsselrotation, Widerspruchserkennung. Keine Anwendung soll neues Protokoll brauchen
(`VISION §3`). Wo eine es doch braucht, ist das ein Befund und kommt ins Register.

## 2. Phase 0 — Neuausrichtung

D466. Restack ist abgekoppelt, die Härtung ruht, diese Roadmap gilt, das erste Szenario ist ein
Verein. Offen aus dieser Phase: die Frage, ob es den Bond überhaupt geben soll (O88).

## 3. Phase 1 — Der Verein auf Papier

Ein Verein mit drei Abläufen:

- **Mitglied werden.** Eine Person legt einen Schlüssel an und tritt bei; ein Mitglied bürgt.
- **Antrag und Abstimmung.** Eine Satzungsänderung wird beantragt und abgestimmt; mit der Schwelle
  gilt die neue Satzung, und jede Maschine sieht dieselbe.
- **Beitrag.** Der Beitrag ist eine Obligation, die Quittung des Kassenwarts tilgt sie.

Dazu der Moment, für den das Ganze da ist: ein Mitglied stimmt mit demselben Schlüssel Ja und Nein,
und alle sehen die Kollision mit beiden Unterschriften als Beweis (`08 §2.2`).

Ergebnis: ein Szenario-Dokument. Welche Claims, wer unterschreibt was, was jeder Bildschirm zeigt,
was fehlt. Was fehlt, bekommt einen Registereintrag, bevor gebaut wird.

## 4. Phase 2 — S-Node, Version 0

Der Lebensraum der Claims (`VISION §5`). Ein Node ist keine Protokollfigur, sondern eine Identität,
die einen Dienst anbietet (`06 §2`). Version 0 ist ein kleiner Dienst auf Unix: er hält den Bestand,
prüft neue Claims, rechnet den Zustand aus und bietet eine lokale HTTP-Schnittstelle an. Endgeräte
sprechen mit ihrem S-Node wie ein Mailprogramm mit seinem Server. Maschinen haben eigene Schlüssel
und unterschreiben selbst.

## 5. Phase 3 — Oberfläche mit dem Verein

Im Browser, gegen den S-Node aus Phase 2: Nutzer anlegen, Verein gründen, beitreten, Antrag stellen,
abstimmen, Beitrag zahlen und quittieren, die Kollision sehen. Eine Person bedient, Skripte spielen
die übrigen.

## 6. Phase 4 — Simulation

Viele Personen mit eigenem Verhalten, mehrere S-Nodes, die Claims austauschen. Jeder Node zeigt
denselben Zustand, sobald er dieselben Claims hat; wer lügt, fällt auf.

## 7. Phase 5 — Reticulum

S-Nodes tauschen Claims über Reticulum und LXMF aus, am Ende auch über Funk. Reticulum
transportiert, Symbolon sagt, was die transportierten Aussagen bedeuten (`VISION §5`,
Referenzpfad RNS/LXMF).

## 8. Danach

Bewusst offen. Kandidaten sind die Food-Koop, ein freier Markt, eine Versicherung, ein
Sicherheitsdienst. Was davon kommt und in welcher Reihenfolge, entscheidet sich nach Phase 5.
Szenarien, die den Bond brauchen, warten auf O88.

## 9. Was ruht

- Lese- und Mutationsrunden über bestehenden Code, außer eine Anwendung stolpert über einen Fehler.
- Der Nachzug der Rust-Fassung, weiter nach D409 Beschluss 3.
- Vertagte Posten in `offen.md` öffnet ein Szenario, das sie braucht, nicht der Kalender.
