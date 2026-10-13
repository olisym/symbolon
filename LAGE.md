# Lage — was MaR heute ist, kann und nicht kann

Status: **Non-normativ.** Lagebild, keine Spezifikation. Stand: Register bis D657, Commit
`b29e6c5`, 13.10.2026.

Diese Datei beantwortet vier Fragen: Was ist gelöst, was ist offen, wie greifen die Teile
ineinander, und warum ist es so gebaut. Jede Aussage trägt einen Verweis, damit sie nachgeprüft
werden kann, statt geglaubt zu werden. Wo diese Datei und eine Spezifikation auseinanderlaufen,
gewinnt die Spezifikation, und diese Datei ist falsch (wie `VISION §7`).

Sie veraltet. Die Zeile oben sagt, bis wohin sie stimmt; was danach entschieden wurde, steht am
Ende von `07-decisions.md` und im neuesten `sitzungsstart-*.md`.

---

## 1. In einem Absatz

MaR ist ein Protokoll, mit dem Menschen Aussagen so unterschreiben, dass jeder sie selbst
nachrechnen kann, ohne eine Stelle in der Mitte. Es prüft nicht, ob eine Aussage wahr ist. Es
sorgt dafür, dass jede Aussage genau einen Urheber hat und dass derselbe Urheber nicht zwei
einander widersprechende Aussagen in der Welt halten kann, ohne dass der Widerspruch, sobald er
irgendwo zusammentrifft, als von ihm selbst unterschriebener Beweis gegen ihn vorliegt
(`08 §2.1`, `08 §2.2`). Darauf sitzen Bürgschaft, Mitgliedschaft, Schulden und Quittungen,
Streit und Urteil sowie Abstimmungen über Satzungen. Gebaut ist eine Referenzimplementierung in
Python mit einem Knoten, einer Seite im Browser und einem Boten, der Knoten über Reticulum
abgleicht, im Lab auch über simulierten Funk mit 1200 bit/s.

---

## 2. Was das Protokoll leistet, und was nicht

**Zurechenbarkeit, nicht Wahrheit** (`08 §2.1`). Das Protokoll ist bedeutungsblind. Eine
falsche Aussage kann unterschrieben werden und ist dann protokollgültig. Erzwungen werden nur
Urheberschaft und Widerspruchsfreiheit. Das ist eine Schranke, keine Bescheidenheit: ein
Protokoll, das Aussagen gegen die Welt prüft, braucht ein Orakel und verliert die Eigenschaft,
dass beliebige Inhalte über dieselbe Mechanik laufen.

**Überprüfbar wird eine Aussage durch Kollision, nicht durch Signatur** (`08 §2.2`). Ein Claim,
auf den nichts zeigt und der auf nichts zeigt, ist unwiderlegbar und folgenlos. Die Kraft des
Protokolls wächst mit dem Anteil des Zusammenlebens, der als verknüpfte Claims ausgedrückt wird.

**Kein Konsens, kein objektiver Zustand** (`08 §2.3`). Jeder Beobachter rechnet lokal aus dem,
was er hat. Die Ergebnisse stimmen überein, soweit das Wissen übereinstimmt. Eine Ausnahme ist
zugelassen: über den Ablauf einer Frist dürfen zwei korrekte Rechner uneins sein, weil sie
verschiedene Uhren haben. Ein erzwungener gemeinsamer Zustand bräuchte eine globale Ressource,
und eine globale Ressource ist eine Machtstelle.

**Nichts ist global** (`08 §5`). Normen gelten in Kreisen. Eine Person kann in beliebig vielen
Nuklei sein, jeder mit eigener Verfassung, und keiner erfährt vom anderen, wenn sie es ihm nicht
erzählt.

**Das Aufnahmekriterium** (`08 §3`). Für jeden neuen Mechanismus gilt eine Frage: Senkt er die
Kosten festzustellen, wer was gesagt hat, oder verteilt er Macht? Senken gehört ins Protokoll,
Verteilen in die Verfassung eines konkreten Nukleus. Schwellen, Losverfahren, Amtszeiten und
gewichtete Auszählung sind deshalb kein Protokoll.

**Die Rangfolge der Abwehr** (`08 §6`). Erstens Sichtbarkeit: ein bemerkter Regelverstoss hat
seinen Vorteil verloren. Zweitens Rückzug: Bürgen widerrufen, Kapazität versiegt, ohne
Strafinstanz. Drittens Durchsetzung für den Rest, und womit, sagt seit D467 das jeweilige
Szenario. Ausdrücklich nicht behauptet ist, dass Defektion für den einzelnen irrational sei;
behauptet ist, dass sie nicht verallgemeinerbar ist und mit der Sichtbarkeit ihren Vorteil
verliert.

---

## 3. Wie die Teile ineinandergreifen

### 3.1 Das Bild

```text
  Mensch            Mensch            Mensch
    |                 |                 |
  Seite im Browser (Schlüssel bleibt im Browser)        Werkzeug
    |                 |                 |
  Knoten  <--------> Knoten <--------> Knoten           Werkzeug
  (Bestand, Sicht)    |                 |
    |               Bote über Reticulum (Funk, WLAN, TCP)
    |
  ============================== Protokoll ==============================
    |
  04  Governance      Epochen, ein Loop: Vorschlag, Stimme, Auszählung
  03  Profile         Verdikt, Schuld und Quittung, Mitgliedschaft
  02  Trust-Flow      Bürgschaft als Fluss, Kapazität, Budget
  00  Nukleus         Genesis, Verfassung, Schlüssel des Nukleus
  01  Claim-Atom      ein Objekt, eine Signatur, eine Kette je Autor
  ------------------------------------------------------------------------
  05  Durchsetzung    Entwurf, zurückgestellt (O40)
  06  Dienste         Entwurf, nicht gebaut
  08  Zweck           was hinein darf und was nie
```

### 3.2 Die Schichten

**01 — das Claim-Atom.** Das einzige Primitiv. Ein Claim ist ein CBOR-Objekt mit zehn Feldern:
Autor `I` (Ed25519-Schlüssel), Subjekt `J`, Prädikat `p`, ein opaker Wert `v`, Scope `N`, Zeit
`t`, optionale Ablaufzeit `t_exp`, der Hash des vorigen Claims desselben Autors `h_prev` und die
Signatur (`01 §2`). Alle Verweise sind 32 Byte, die Signatur 64, ohne Kürzung, damit es über
LoRa passt. Jeder Autor führt eine Kette; eine Gabel in ihr ist der Widerspruchsbeweis (`01 §1`
A3). Alles Soziale ist ein Profil über diesem Atom und fügt nie ein Feld hinzu.

**00 — der Nukleus.** Eine Gemeinschaft ist der Hash eines unveränderlichen Genesis-Objekts,
nie ein Schlüssel (`00 §1` F1). Dazu kommen die versionierte Verfassung und die Kette der
Schlüssel des Nukleus. So behält ein Verein seine Identität, während Schlüssel rotieren und die
Satzung sich ändert.

**02 — Vertrauen als Fluss.** Eine Bürgschaft (`vouch@1`) ist eine Kante mit Gewicht `w`. Wie
viel Vertrauen von mir bei jemandem ankommt, ist ein maximaler Fluss durch dieses Netz
(`02 §4`). Jeder Knoten hat eine Kapazität `C(x)`, die nur von seiner Lage abhängt, also von
der Entfernung zum eigenen Ausgangspunkt (`02 §3`). Die Summe der Gewichte, die jemand vergibt,
ist höchstens 1 (`Σw ≤ 1`, D3): Bürgschaft ist knapp, also muss man auswählen. Jeder rechnet von
seinem eigenen Seed; es gibt keinen globalen Wert (`02 §1`).

**03 — Profile.** Drei Bündel sozialer Akte über demselben Atom (`03 §1`):
Anklage und Verdikt (ein Urteil bindet nur, wer sich der Schlichtung vorher unterworfen hat,
`03 §2`), Wert (Schuld als `obligation@1`, Tilgung als `receipt@1`, preisblind: Beträge werden
nie gelesen, `03 §3`) und Mitgliedschaft (gegenseitig: Person und Nukleus willigen beide ein,
`03 §4`).

**04 — Governance.** Ein Nukleus lebt in Epochen; jede beginnt mit einer ratifizierten
Verfassung. Es gibt genau einen Loop: Vorschlag, Stimme, Auszählung, Materialisierung (`04`,
Einleitung). Dazu gehören Sachanträge neben der Satzung (O96, D581), Wahlgänge und Patt (D600
bis D604) und geschützte Sachfelder mit eigener Schwelle (D646).

**05 und 06** sind Entwürfe. `05` ordnet die Antworten auf Regelbruch in Stufen,
`06` beschreibt Dienste wie Zeitbezeugung. Beide tragen noch Sätze über Bonds unter Vorbehalt
(D467 Beschluss 5). Im Code gibt es keinen Bond und keine Reputationszahl.

**08 — der Zweck.** Was hinein darf, was nie, und welche Grenzen bewusst getragen werden.

### 3.3 Das Werkzeug

Was Menschen bedienen, ist nicht Protokoll, sondern Werkzeug (`08 §3`, Tabelle).

- **Der Knoten** (`symbolon/node/`): hält den Bestand in SQLite, prüft eingelieferte Claims,
  rechnet die Sicht als reine Funktion und bietet eine HTTP-Schnittstelle an (D471 bis D478).
  Ein Knoten ist keine Protokollfigur, sondern eine Identität, die einen Dienst anbietet.
- **Die Seite** (`symbolon/node/static/`): Schlüssel anlegen, Verein gründen, beitreten,
  Antrag stellen, abstimmen, Beitrag und Quittung, die Kollision sehen (D479 bis D512, D651).
  Der Schlüssel entsteht im Browser und verlässt ihn nicht (D657 Befund 1).
- **Der Bote** (`symbolon/bote/`): gleicht Knoten über Reticulum ab. Reticulum macht das Netz
  (Identitäten, Pfade, Links, Sendezeit), der Bote trägt nur, was ein Verein weiss (D617
  Beschluss 1). Darin: Ankündigung nach Trickle (D611), Abgleich nach Bereichen (D617, O90),
  Bündel (D614) und Rundruf an der Quelle (D636).
- **Mehrere Geräte einer Person**: eine Wurzel, je Gerät ein eigener Schlüssel, delegiert je
  Scope; ein Widerspruch zählt je Wurzel (D529 bis D546).
- **Das Lab** (`tools/netz.py`): fünf bis sechs Geräte auf einer Maschine, mit Personen, die
  selbst handeln, über Reticulum oder einen simulierten Funkkanal (D518 bis D554, D607).

### 3.4 Wo der Code liegt

| Schicht | Module |
|---|---|
| 01 | `atom.py`, `cbor_canon.py`, `verifier.py`, `predicates.py`, `keys.py` |
| 00 | `genesis.py`, `resolve.py` |
| 02 | `trust/` (Graph, Fluss, Dinic, Ableitung, Relaxation) |
| 03 | `profiles/` (Verdikt, Kredit, Mitgliedschaft) |
| 04 | `governance/` (Kette, Epoche, Auszählung) |
| Werkzeug | `node/`, `bote/`, `buendel.py`, `tools/` |

---

## 4. Was gelöst ist

„Gelöst“ heisst: normiert, gebaut und getestet. Wo nur die Spec steht, sagt es die Spalte.

| Problem | Antwort | Wo |
|---|---|---|
| Wer hat das gesagt, und wurde es verändert? | Ed25519-Signatur, Hashkette je Autor | `01 §4` |
| Jemand sagt zweimal Verschiedenes | Gabel in der eigenen Kette ist ein selbst unterschriebener Beweis | `08 §2.2`, `01 §4` |
| Doppelstimme zum selben Antrag | jedes Paar von Stimmen derselben Wurzel; Auflösung durch eine Stimme, die die früheren nennt | D525, D547 |
| Gefälschte Identitäten in Masse (Sybil) | Fluss in die Sybil-Region ist durch die Kapazität der ehrlichen Grenzknoten beschränkt | `02 §4` |
| Vertrauen horten, kaufen, vererben | Kapazität ist positional; kein Guthaben, keine Belohnung, nicht übertragbar | `02 §1`, D10, D18, `08 §4` |
| Ansehen wird zu Macht | Zuhören unbegrenzt, Torwächterschaft im eigenen Budget | D25 |
| Regeln ändern ohne Instanz darüber | Epochen und ein Loop | `04` |
| Zwei konkurrierende neue Satzungen | arithmetisch unmöglich, solange die Schwelle über der Hälfte liegt | D102, D108, D176 |
| Netz zerfällt in Teile | fehlendes Wissen senkt ein Ergebnis, hebt es nie; Spaltung und Vereinigung vorgeführt | `08 §2.2`, D336 bis D346, D594 |
| Knoten ohne Uhr | er kann belasten, aber kein Vertrauen gewähren | D404 |
| Knoten mit grober Uhr | Intervall-`now` über die Bruchstellen | D406, D408 |
| Schlüssel des Nukleus wechseln | Rotation mit Gegenzeichnung des Nachfolgers | `00 §6`, D125 |
| Mehrere Geräte, ein Mensch | Wurzel und Geräteschlüssel, Sperre eines Geräts | D529 bis D546 |
| Schuld und Tilgung | `obligation@1` und `receipt@1`, preisblind | `03 §3` |
| Streit und Urteil | Anklage, Verdikt; bindend nur nach Unterwerfung, die Reputationsschiene trägt auch ohne | `03 §2`, D333 |
| Ein feindliches Mitglied blockiert | kein Ausschlussmechanismus; Exit durch neue Gründung, Grenze benannt | D236 |
| Einen Verein gründen | drei gründen gemeinsam, alle sind Anker; Vorlage mit Schutz und Typen | D640 bis D655 |
| Ohne Internet | Bote über Reticulum; ein Wahlgang kostet über Funk rund ein Drittel der Sendezeit | D617, D635, D636 |
| Mithören im Funk | IFAC am Interface, als Regel des Betriebs | D629 |

---

## 5. Was verworfen wurde, und warum

Diese Vorschläge kommen erfahrungsgemäss gut begründet zurück (`08 §4`). Hier stehen sie mit
dem Grund, aus dem sie nicht hineinkommen.

- **Ein Ruf-Konto, das mit gutem Verhalten wächst.** Es wäre ein Guthaben, und ein Guthaben ist
  ein Puffer gegen Sanktion: erst sammeln, dann verbrennen (D18). Belohnt würde ausserdem, für
  sichere Kandidaten zu bürgen statt für Neue (D18).
- **Brücken- oder Vermittlungsprämien, anteilige Kapazitätsteilung.** Was übertragbar wird,
  wird gekauft, und was gekauft wird, ist Torwächterschaft (D8, D9, D25).
- **Stimmgewicht nach Ruf oder Einsatz.** Ein Stimmgewicht ist eine handelbare Grösse, sobald
  jemand bemerkt, dass es sich lohnt (`08 §4`). Ausgezählt wird nach Kopfzahl (D98).
- **Bond, Pfand, Slashing, Treuhand.** Darunter lagen fünf verschiedene Probleme. Gefährlich ist
  die verwahrende Stelle in der Mitte, das Pooling und der Einsatz, der Einfluss kauft. Nichts
  baut auf Verwahrung (D467).
- **Signaturen, die bei Widerspruch den Schlüssel preisgeben.** Sie passen technisch, machen aber
  einen ehrlichen Fehler wie ein doppelt signierendes Backup zur Katastrophe (D467 Beschluss 3).
- **Ein Ausschlussverfahren mit Stimmverbot.** Es kippt den Minderheitenschutz: eine knappe
  Mehrheit macht sich zur Supermajorität, indem sie Gegner zu Betroffenen erklärt (D236).
- **Globaler Konsens, eine gemeinsame Kette.** Ein erzwungener gemeinsamer Zustand ist eine
  Machtstelle (`08 §2.3`); Substrate und ähnliche bauen genau das (`VISION §5`).
- **Eine Reputationszahl als Durchsetzung.** `05` beschreibt eine Beta-Reputation je Beobachter.
  Sie ist zurückgestellt, weil sie ein ungelöstes Moral-Licensing-Problem trägt: wer genug
  Ansehen hat, leistet sich einen Fehltritt (D237). Ohne beobachtete Verstösse wäre jede
  Festlegung Spekulation.
- **Vertrauen ohne Uhr.** Es trüge nur über Bürgschaften, die die Pflicht zur Ablaufzeit
  verletzen, und prämierte damit den Verstoss (D404).

---

## 6. Was offen ist

### 6.1 Der laufende Strang

- **Gründung, Schritt 3:** der Scan mit Schlüssel und Adresse, der Knoten am Telefon. Gemessen
  ist: der Knoten läuft in Termux, der Scan geht über die Kamera-App, Multicast ist dort
  gesperrt, eine gezielte Verbindung trägt im Klon, am Telefon über WLAN noch nicht (D657).
- **Gründung, Schritt 4:** der Knoten hält nur eigene Scopes (D641 Beschluss 1).
- **Einladung aus der Ferne:** Olis Gedanke, einer unterschreibt die Absicht und lädt ein
  (D654 Befund 5). Kein Beschluss.
- **Die Verabredung zu zweit** als zweite Vorlage (D640 Beschluss 3).

### 6.2 Benannte Lücken mit Posten

- **O101:** die Seite hat kein Konzept dafür, was ein Mensch zuerst sieht.
- **O104:** Linkaufbau über verlustbehafteten Funk scheitert gehäuft.
- **O100:** das Patt kostet Rechenzeit; auf Telefon und LoRa ungemessen.
- **O89:** ein Amtswechsel der Kasse ist eine Schlüsselübergabe; wer den Schlüssel hatte, kann
  weiter quittieren.
- **O40:** Layer 05 ist zurückgestellt (D237).
- **O35, O31, O74, O25** und weitere Wartestände: siehe `offen.md`.

### 6.3 Benannt, ohne Posten

- **Verlust des Schlüssels einer Person:** ein eigener Strang (D640 Beschluss 5).
- **Funk über echte Hardware:** die T-Beams fehlen, der Funk ruht (D639).
- **Die Szenarien nach dem Verein:** Food-Koop, freier Markt, Versicherung, Sicherheitsdienst
  (`ROADMAP §8`). Jedes beantwortet für sich, was früher der Bond lösen sollte (D467).
- **Austritt mit offenen Pflichten:** der Rückzug wirkt nur, solange jemand bleiben will. Wer
  geht, dem ist er gleich; im Verein der Kassenwart, der mit offenen Pflichten austritt. Kandidat
  für das Vereinsszenario, aus der Durchsicht vom 13.10.2026.
- **Ankerprüfung beim Beitritt aus der Ferne:** am Tisch löst der Scan, woher eine Eingeladene
  weiss, dass sie dem echten Verein beitritt. Aus der Ferne ist das offen. Kandidat zur Einladung,
  aus derselben Durchsicht.

### 6.4 Der grösste offene Punkt ist kein technischer

Es gibt keine Menschen mit einem echten gemeinsamen Anliegen, die MaR benutzen. Alles ist gegen
sich selbst geprüft, mit Zweitimplementierungen in Go, Haskell und Rust als bestem Ersatz für
einen zweiten Blick (D237). Seit D466 ist der Massstab eine Anwendung, die man bedienen und sehen
kann; sie zeigt Fehler, die keine Messung findet.

---

## 7. Getragene Grenzen

Was MaR ausdrücklich nicht liefert, aus `08 §7` und dem Register:

- **Keine Wahrheit über die Welt.** Ob etwas wirklich geschah, sagen Menschen, deren Aussagen
  zurechenbar sind und kollidieren können (`08 §2.1`, D467 Beschluss 4).
- **Keine Verhinderung von Täuschung.** Nur ihre Unbestreitbarkeit nach dem Zusammentreffen.
- **Keine Einigkeit über Fristablauf** zwischen Rechnern mit verschiedenen Uhren.
- **Keine Unterscheidung von Verweigerung und Ausbleiben.** „Offen“ heisst: nicht gezahlt, nicht
  quittiert oder nicht zugestellt.
- **Kein Schutz gegen echte Menschen, die sich absprechen.** Die Sybil-Schranke gilt gegen
  gefälschte Identitäten, nicht gegen Kollusion (D20).
- **Kein Ausschluss gegen den Willen einer Sperrminorität.** Die Antwort ist Exit (D236).
- **Keine Wiedergutmachung ohne Beteiligte.** Alles setzt voraus, dass jemand hinschaut und
  handelt.
- **Was nicht unterschrieben wird, sieht MaR nicht.** Wer auf der Arbeit nur so tut, als würde
  er arbeiten, unterschreibt nichts darüber. Das ist der Unterschied zu Überwachung: sichtbar
  wird, was jemand erklärt, nicht was er tut (`08 §2.1`).

---

## 8. Abgrenzung, soweit im Register belegt

Ein vollständiger Vergleich mit verwandten Projekten steht aus. Belegt sind diese Kontraste:

- **Blockchains und Substrate:** globaler Konsens und geteilte Sicherheit, genau das, was MaR
  verweigert (`VISION §5`, `08 §2.3`).
- **Bisq, Cashu, Fedimint, Ethereum-Staking:** Pfand und Verwahrung, mit den drei Gefahren aus
  D467.
- **MLS, Stellar, Mastodon, Hive:** wie Systeme ohne Zentrale jemanden entfernen, und dass
  keines alle vier Bedingungen von MaR zugleich hält (D236).
- **Briar und Keybase:** Schlüsseltausch am Tisch und Einladung aus der Ferne, als Vorbild für
  die Gründung (D640).
- **Reticulum:** das Netz darunter; MaR baut nichts davon nach (D617).
- **Law Merchant, Diamantenhändler:** Durchsetzung über Reputation statt über erzwingbare
  Bindung, mit derselben Struktur wie die Reputationsschiene (D333).

---

## 9. Wörter

| Wort | Bedeutung | Wo |
|---|---|---|
| Claim, Atom | eine unterschriebene Aussage; das einzige Primitiv | `01` |
| Prädikat | was die Aussage ist, etwa `vouch@1` oder `vote@1` | `01 §2` |
| Profil | eine Konvention über das Atom, ohne neues Feld | `01`, `03` |
| Kette | die Folge der Claims eines Autors, verknüpft über `h_prev` | `01 §4` |
| Gabel, Equivocation | zwei Claims eines Autors mit demselben Vorgänger; der Widerspruchsbeweis | `01 §4` |
| Nukleus, Scope | eine Gemeinschaft, benannt durch den Hash ihres Genesis | `00` |
| Genesis | das unveränderliche Gründungsobjekt | `00 §4` |
| Verfassung, Satzung | die geltenden Regeln eines Nukleus, versioniert | `00 §5` |
| Epoche | die Zeit unter einer ratifizierten Verfassung | `04` |
| Vouch, Bürgschaft | eine Kante im Vertrauensnetz mit Gewicht `w` | `02` |
| Kapazität `C(x)` | wie viel über einen Knoten fliessen kann; nur von der Lage abhängig | `02 §3` |
| Seed | der Ausgangspunkt, von dem jeder sein Vertrauen rechnet | `02 §1` |
| Wurzel | die Identität einer Person über ihren Geräten | D529 |
| Knoten | das Programm, das den Bestand hält und die Sicht rechnet | D471 |
| Bote | das Programm, das Knoten über Reticulum abgleicht | D584 |
| Vorlage | eine Satzung mit festen Feldern, Typen und Schwellen | D641, D648 |
| Sachantrag | eine Änderung eines Felds neben der Satzung | D581 |
| Wahlgang, Patt | eine weitere Runde, wenn zwei Vorschläge gleichauf liegen | D600 |
| Vermerk | ein Befund, den die Auswertung ablegt, statt abzubrechen | `02 §10` |

---

## 10. Wo der Stand steht

- Entscheidungen: `07-decisions.md`, mit Begründung und Verworfenem.
- Offene Posten: `offen.md`.
- Der Plan: `ROADMAP.md`.
- Das Warum und die Anwendungen: `VISION.md`.
- Der Verlauf der Arbeit: der neueste `sitzungsstart-*.md`.
- Die Zahlen (Tests, Einträge, Posten): `make check`, das Ende des Registers und der
  Sitzungsstart. Diese Datei nennt bewusst keine (D415).
