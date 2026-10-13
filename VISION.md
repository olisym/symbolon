# Mensch als Republik — Vision, Anwendungen & Grundannahmen

Status: **Non-normativ.** Kontext-Dokument, keine Spezifikation.

Dieses Dokument trägt das *Warum* und das *Wozu*: die Motivation, die Anwendungen und die bewusst
gemachten Grundannahmen. Es steht **außerhalb** der nummerierten Spec-Reihe und darf, was die
Specs nicht dürfen: Bedeutung tragen. Genau diese Trennung ist Programm. Die Spezifikationen
bleiben bedeutungsblind; hier lebt der Sinn daneben, nicht darin.

Was heute gelöst, gebaut und offen ist, steht in `LAGE.md`. Dieses Dokument sagt, wofür.

---

## 1. Was das ist

Ein **Substrat**, kein System. Ein Protokoll, auf dem Menschen freiwillig, föderiert und lokal
koordinieren, ohne Herrschaftsmonopol. Es erzwingt keine Ordnung; es macht **Aussagen**
**nachprüfbar und nicht-abstreitbar**, also wer was erklärt, zugesagt oder beschlossen hat, und
überlässt die Regeln den Menschen, die sich freiwillig auf sie einigen. Ob eine Aussage zu dem
passt, was jemand tatsächlich getan hat, kann es nicht prüfen; das bleibt eine Frage an Menschen
(§6, das Orakel-Problem).

Der Kern beweist nur eines: *Ich kenne ein Geheimnis und binde mich damit nachprüfbar an eine
Aussage, in einer Reihenfolge, die ich nicht nachträglich ändern kann.* Selbstbesitz ist hier
nicht als Regel geschrieben, sondern **strukturell verkörpert**: Niemand kann für dich signieren,
dir deine Identität nehmen oder deine Vergangenheit umschreiben.

Der entscheidende Unterschied zu jedem „System“: Ein Protokoll, das Regeln *erzwingt*, hat einen
Herrscher, und sei es einen algorithmischen. Dieses macht Regeln nur **sichtbar** und lässt
Menschen wählen. Das ist die Linie zwischen einem Substrat und einem System.

Der Name trägt das Bild. Ein *symbolon* war eine Münze oder Scherbe, die zwei Menschen
zerbrachen; Jahre später bewiesen die passenden Hälften die Übereinkunft, ohne Zeugen und ohne
Amt (D317). Überprüfbar ist hier eine Aussage nicht dadurch, dass sie unterschrieben ist, sondern
dadurch, dass sie mit anderem Unterschriebenen zusammenpassen oder kollidieren kann (`08 §2.2`).

## 2. Warum es ein freier Markt der Gesellschaftssysteme ist

Weil das Protokoll die Bedeutung von Regeln *nicht* kennt, kann darüber ein Markt konkurrierender
Ordnungen existieren. Ein Nukleus (eine Gemeinschaft) wählt seine Verfassung; ein anderer wählt
eine andere; ein Mensch tritt bei oder aus. Exit ist immer offen, die eigene Identität
unentziehbar, und eine neue Gründung braucht niemandes Zustimmung (D236). Gute Ordnungen setzen
sich durch, weil Menschen sie freiwillig wählen, nicht, weil eine Zentrale sie vorschreibt.
Sollte es ein „Naturrecht“ geben, würde es sich als das meistgewählte Regelwerk auf einem
wirklich freien Markt herauskristallisieren, nicht durch Dekret.

Dieselben Menschen können im selben Raum unter verschiedenen Verfassungen leben, von außen nicht
unterscheidbar (`08 §5`). Das ist kein Sonderfall, sondern der Normalfall: Normen gelten in
Kreisen, die sich an den Rändern berühren, ohne dass einer für die anderen entscheidet.

## 3. Was darauf wächst — Anwendungen

Wichtig: **Keine dieser Anwendungen soll neues Protokoll brauchen.** Alle sind Kompositionen aus
den bestehenden Bausteinen: Identität, Nukleus mit Verfassung, Bürgschaft (`vouch@1`), Schuld und
Quittung (`obligation@1`, `receipt@1`), Anklage und Verdikt, Abstimmung über Epochen und
Trust-Flow. Braucht eine Anwendung doch etwas Neues, ist das ein Befund und kommt ins Register
(`ROADMAP §1`). Das ist eine **Annahme**, geprüft bisher an einer Anwendung, dem Verein. Stellen,
an denen sie absehbar nicht trägt, sind benannt: eine geheime Wahl gibt es nicht, weil jede Stimme
unterschrieben ist; Preise und Tausch brauchen eine Wertschicht, die es nicht gibt (`08 §3`).

Seit D467 gibt es keinen Bond mehr: kein Mechanismus baut auf einer Stelle, die fremden Wert
verwahrt oder einzieht. Was der Bond lösen sollte, beantwortet jedes Szenario für sich.

- **Der Verein.** Die erste Anwendung, und gebaut: drei gründen am Tisch, Mitglieder treten bei,
  Satzung und Sachanträge werden abgestimmt, der Beitrag ist eine Schuld, die Quittung der Kasse
  tilgt sie, und eine Doppelstimme ist für alle als Beweis sichtbar (`szenario-verein.md`, D468
  bis D655). Er ist das Modell jeder Gruppe, die sich auf Regeln einigt und zielgerichtet handelt.
- **Risikoteilung statt Versicherungskonzern.** Eine kleine Gruppe teilt Risiken unter sich, wie
  ein Broodfonds mit 20 bis 50 Personen (D467). Klein ist sie nicht aus technischen Gründen,
  sondern weil Menschen, die einander kennen, Missbrauch selbst bemerken. Größere Risiken tragen
  viele solcher Gruppen gemeinsam, nicht eine große; wie sie sich zusammenschließen, ist offen
  (`04 §7`). Ob es einen gemeinsamen Topf gibt, wer ihn verwahrt und wer die Fälle prüft,
  entscheidet das Versicherungsszenario. Das Protokoll stellt
  nicht fest, ob ein Fall eingetreten ist; das tun Menschen, deren Aussagen zurechenbar sind
  (`08 §2.1`).
- **Schlichtung als Dienst.** Schiedsstellen konkurrieren. Ein Urteil bindet nur, wer sich der
  Schlichtung vorher unterworfen hat (`03 §2`). Auch ohne Bindung trägt es: wer ein Urteil
  missachtet, verliert Bürgen, wie bei den Händlern des Law Merchant (D333). Die Wahl des Forums
  ist Teil des Marktes.
- **Schutz ohne Gewaltmonopol.** Das Protokoll tut nie Physisches. Es kann ein mehrfach
  unterschriebenes **Mandat** tragen; *Menschen*, konkurrierende Schutzgemeinschaften, handeln
  darauf, und jede prüft die Legitimität selbst. Rein defensiv; Angriff ist nie legitim. Diese
  Anwendung ist die am wenigsten durchdachte und braucht ein eigenes Szenario (`05 §7`).
- **Ansehen, kein Konto.** Vertrauen wirkt als Leitwert, nicht als Währung (`08 §4`): es ist
  nicht übertragbar, nicht ansparbar und kein Stimmgewicht. Durch gutes Verhalten wächst keine
  Zahl; wer ehrlich ist, bleibt jemand, für den andere bürgen, und wer Vertrauen bricht, verliert
  seine Bürgen (D10, D18). Gehört-werden ist unbegrenzt, Torwächterschaft knapp (D25). Es gibt
  kein Reputations-Monopol: jeder rechnet von seinem eigenen Ausgangspunkt. Bewertungen gibt es
  trotzdem, als unterschriebene Meinung eines Menschen über einen anderen; jeder Leser gewichtet
  sie über sein eigenes Netz, und eine Bewertung von gefälschten Identitäten erreicht ihn nicht
  (`05 §5`, `02 §4`). Ob das unter Fremden so gut trägt wie ein Marktplatz mit zentraler
  Bewertung, ist ungemessen; das prüft ein Szenario mit einem Markt.
- **Freier Markt der Währungen.** Jeder kann eine Recheneinheit erstellen, wie jeder eine
  Identität erstellen kann: eine `obligation@1` mit eigener Einheit, wertlos, bis jemand sie
  annimmt (`03 §3`, D467). Das Protokoll ist preisblind; Wert entsteht am Markt. Währung ist
  Schmiermittel für Koordination, nicht Selbstzweck der Vermehrung.
- **Dienste als Markt.** Lebensraum für Claims, Zeitbezeugung, Schlichtung: jeder Dienst ist eine
  Identität, die ein Verhalten über Zeit verspricht, selbst betrieben oder gemietet (`06 §2`).
  Wie ein Dienst glaubwürdig wird, ohne dass jemand Pfand verwahrt, ist offen.
- **Bodennutzung (geparkt).** Notiz für die Zukunft: **Nutzungsrecht statt Eigentum**, ein freier
  Markt um das zeitlich begrenzte Recht, Land zu bewirtschaften, statt absoluten Bodeneigentums.

## 4. Grundannahmen

Diese Annahmen sind bewusst gemacht und gehören offengelegt. Sie prägen das Design, sind aber
*Annahmen*, keine bewiesenen Tatsachen.

- **Kooperative Mehrheit, Defektion ist parasitär.** Die große Mehrheit will in Ruhe
  zusammenleben und wirtschaften. Defektion setzt eine regeltreue Mehrheit voraus und funktioniert
  nur, solange sie unbemerkt bleibt (`08 §6`). Das System muss Defektion handhaben, ohne die
  Mehrheit zu gängeln. Es braucht dafür keine feste Quote von „Guten“ und „Bösen“; viele schummeln
  ein wenig, wenige viel, und dieselbe Rangfolge der Abwehr gilt für beide (D658 Befund 2).
- **Mit der Natur des Menschen, nicht gegen sie.** Menschen setzen sich ein, wo es lokal spürbar
  wirkt und Ansehen bringt: dazugehören, anerkannt werden, eine Aufgabe haben (D645). Das Tun ist
  die Hauptfläche; Alltägliches fällt leicht, Grundlegendes schwer; Schweigen soll nicht lähmen
  (D645 Beschluss 3). Die Oberfläche lockt nicht: keine Serien, Abzeichen, roten Punkte oder
  endlosen Listen, die Menschen zurückholen sollen. Man kommt, wenn es etwas zu tun gibt, und geht
  wieder.
- **Selektive Stille.** Das Atom ist ein Mechanismus, kein Gebot zu signieren. Der Normalzustand
  ist **kein Claim**: unterschrieben wird, wo der Einsatz es rechtfertigt, nicht bei jeder
  Alltagshandlung. Für ein Brötchen braucht niemand einen Vertrag. Das Protokoll kann Schweigen
  nicht erzwingen, weil das Bedeutung wäre (`01 §1`), aber hier steht die Norm: MaR macht
  sichtbar, was ein Mensch **erklärt**, nicht was er **tut**. Was niemand unterschreibt, sieht
  niemand. Das ist die Linie zur Überwachung, und sie hat einen Preis: wer schweigt, bleibt
  unwiderlegbar (`08 §2.2`).
- **Legibilität ist der eigentliche Hebel.** Der Mehrwert gegenüber bestehenden Ordnungen ist
  nicht Zwang, sondern **Sichtbarkeit**: Widerspruch wird beweisbar und nicht-abstreitbar.
  Rückzug als gewaltfreies Mittel funktioniert nur, wenn erkennbar ist, wer was zugesagt und wer
  sich widersprochen hat. In heutigen Ordnungen ist das oft nicht so; plausible Abstreitbarkeit
  ist dort die Schutzschicht verdeckter Defektion. Das ist die Lücke, die dieses Protokoll
  schließt, für alle, die es benutzen.
- **Transparenz gegen verdeckte Machtkonzentration.** Eine nicht-abstreitbare, nicht-löschbare
  Folge unterschriebener Entscheidungen ist die erste Abwehr gegen *verdeckten* Missbrauch an
  Koordinationspositionen. Macht, die sich nicht verstecken kann, lässt sich schwerer kapern.
- **Ziel-Gleichgewicht.** Ehrliches Verhalten soll die naheliegende Strategie sein, weil
  Defektion auffällt, sobald sie mit Unterschriebenem kollidiert, und Rückzug kostet: Bürgen
  widerrufen, Kapazität versiegt, ohne dass eine Strafinstanz entscheidet (`08 §6`). Ehrlich:
  das ist ein *Gleichgewichts-Argument*, keine Garantie. Behauptet ist nicht, dass Defektion für
  den Einzelnen irrational sei, sondern dass sie nicht verallgemeinerbar ist und mit der
  Sichtbarkeit ihren Vorteil verliert. Unter extremen Machtasymmetrien kann es kippen (§6).

## 5. Wo es läuft — Lebensraum und Knoten

Jedes Atom braucht einen **Lebensraum**, um zu existieren, so wie ein Mensch einen. Dieser
Lebensraum ist ein **Knoten**. Seit Phase 2 gibt es ihn: ein kleines Programm, das den Bestand
hält, neue Claims prüft, den Zustand ausrechnet und eine Seite im Browser anbietet; der Schlüssel
bleibt im Gerät des Menschen (D471, D657). Ein Knoten ist keine Protokollfigur, sondern eine
Identität, die einen Dienst anbietet (`06 §2`).

- **Selbstbestimmte Identität verlangt selbst-gehosteten Speicher und Compute.** Jeder Mensch
  besitzt ein digitales Identitäts- und Datenset, das unter eigener Kontrolle stehen sollte. Das
  braucht eigenen Speicher und damit einen eigenen Rechner.
- **Ein Server zu Hause.** So wie früher der eigene Rechner liegt heute ein kleiner eigener
  Server nahe; lokale KI verstärkt das, aber der Bedarf besteht schon jetzt.
- **Freier Markt der Knoten-Hoster.** Wer nicht selbst hosten will, mietet Lebensraum. Der eigene
  Knoten ist nicht umsonst, aber Souveränität und Wohlstand, der in der eigenen Gemeinschaft
  bleibt, machen ihn seinen Preis wert.
- **Grund-Knoten = Unix.** Kein Neuerfinden eines Betriebssystems, sondern ein bewährtes,
  komponierbares Fundament: *„those who do not know Unix are doomed to reinvent it. Poorly.“* Der
  Knoten bleibt im Geist des Protokolls: **schlank, beherrschbar, skalierbar**. Er läuft heute auf
  einem Rechner und, in ersten Versuchen, auf einem Telefon (D657).
- **Das Netz darunter ist Reticulum.** Reticulum macht das Netz: Identitäten, Pfade, Links,
  Sendezeit, über Funk, WLAN oder Internet. Der Bote trägt nur, was ein Verein weiss, und baut
  nichts nach, was Reticulum kann (D617). Ein Wahlgang passt über einen Funkkanal mit 1200 bit/s
  (D635). Das Atom selbst ist transport-agnostisch und reist über beliebige Medien (`01 §1`).
- **Die Uhr ist lokal.** `now` ist die Zeit des Prüfenden: die eigene Uhr **oder** ein
  Zeitdienst, dem er vertraut. Ein Zeitdienst ist ausdrückbar als Profil, eine unterschriebene
  Bezeugung „ich sah das zu meiner Zeit T“, ohne neues Primitiv (`06 §5`). Ist keine Uhr da,
  kann ein Knoten weiter belasten, aber kein Vertrauen gewähren (D404); mit grober Uhr rechnet er
  über ein Intervall (D406).

*Zu Substrate und Polkadot (Randnotiz):* Der Name verführt, aber die Architektur passt schlecht.
Substrate erzeugt globalen Konsens und geteilte Sicherheit, genau das, was dieses Protokoll
bewusst verweigert (`08 §2.3`). Als kontrastierendes Zweitexperiment denkbar, nicht als
Referenzpfad. Der Referenzpfad ist die schlanke Implementierung über Reticulum.

## 6. Ehrliche Grenzen — warum das keine Utopie ist

Ein Vorhaben wird nicht dadurch als Utopie entlarvt, dass es Grenzen hat, sondern dadurch, dass es
sie verschweigt. Diese hier sind bewusst getragen; die vollständige Liste steht in `08 §7`.

- **Das Orakel-Problem.** Das Protokoll kann die physische Welt nicht bezeugen. „Ist X wirklich
  passiert?“ braucht ein menschliches Urteil, getragen von Menschen, deren Aussagen zurechenbar
  sind und kollidieren können (D467 Beschluss 4). Das ist in bestehenden Ordnungen nicht besser
  gelöst, aber es ist ehrlich, es nicht zu verstecken. Die Strategie: so viel wie möglich
  *beobachtbar machen* (Quittung, Sensor, Nähe im Funknetz), nur den Rest bezeugen.
- **Rückzug diszipliniert, solange jemand bleiben will.** Wo die einmalige Beute den Wert des
  Bleibens übersteigt, wirkt Rückzug nicht: der Exit-Scam, im Verein der Kassenwart, der mit
  offenen Pflichten austritt. Den Bond als Antwort gibt es nicht mehr (D467). Was bleibt: der
  Schaden eines Unterwanderers ist auf das Vertrauen begrenzt, das ihm zugeflossen ist, und eine
  offene Schuld bleibt für alle sichtbar. Wie ein Verein das Endspiel absichert, ist offen
  (`LAGE §6`).
- **Echte Menschen, die sich absprechen.** Die Schranke gegen gefälschte Identitäten schützt
  nicht gegen echte Menschen, die sich abstimmen; das ist die Grenze der ganzen Klasse (D20).
- **Der irreduzible physische Rest.** Gegen eine hinreichend große, fehlgeleitete Koalition hilft
  kein Protokoll; das ist das politische Restrisiko *jeder* Ordnung, auch der staatlichen.
  Selbst-Verifizierbarkeit, lokale Gewichtung und Exit *begrenzen* es, eliminieren es nicht.
- **Bootstrapping.** Am Anfang gibt es keine Bürgen, keine Schlichter, keine gewachsenen Gruppen.
  Das System startet dicht und lokal und wächst, ein Substrat, das neben bestehender Ordnung
  keimt, kein Urknall-Ersatz. Bis heute benutzt es keine echte Gruppe (D237).
- **Korreliertes Risiko.** Risikoteilung löst Systemrisiko (alle melden gleichzeitig einen
  Schaden) nicht von selbst; es braucht einen Ausgleich zwischen Gruppen.
- **Wer es nicht benutzen will, den erreicht es nicht.** Wer heute von plausibler Abstreitbarkeit
  lebt, hat keinen Grund, seine Entscheidungen unterschrieben in eine Kette zu legen. MaR wirkt
  dort, wo Menschen es wählen, und wächst von unten, nicht durch Einführung von oben.

## 7. Verhältnis zu den Spezifikationen

Dieses Dokument ist **non-normativ**. Es begründet und motiviert, es schreibt nichts vor. Die
normative Wahrheit liegt in den Layer-Dateien `00` bis `06` und in `08`, die Entscheidungen und
ihre Gründe in `07-decisions.md`. Wenn dieses Dokument und eine Spezifikation je in Konflikt
geraten, gewinnt die Spezifikation, und dieses Dokument ist zu korrigieren.

Eine Ausnahme ist ausdrücklich gewollt: Wo eine Spezifikation eine Norm der Bedeutung hierher
verweist, wie `01 §1` die selektive Stille, steht sie hier (§4). Die Ethik und die Anwendungen
leben bewusst *neben* dem Protokoll, damit das Protokoll blind bleiben kann. Das ist kein Mangel
an Überzeugung, sondern ihre Bedingung: Nur ein bedeutungsblindes Substrat trägt einen freien
Markt der Gesellschaftssysteme.
