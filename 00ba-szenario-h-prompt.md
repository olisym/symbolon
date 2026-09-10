# 00ba — Szenario H: die zwei Zeitregime unter divergenten Uhren

## Branch und Basis

Branch `szenario-h`, Basis-Commit `535dddd0ce09419835daf7e8f89e643f2d51820b`
(`D350: now bekommt keine Quelle, zeitliche Rechenschaft ueber t`).

## Normative Grundlage

- `01 §2`, Feld 6: `t` ist ein vom Autor behaupteter Zeitstempel und **kein** Ordnungsprimitiv.
- `04 §3.1`, Bedingung 4: eine Stimme mit gesetztem `t_exp` zaehlt nicht, Vermerk
  `VOTE_WITH_EXPIRY`. Begruendung D97. Entsprechend `RATIFY_WITH_EXPIRY` fuer die Ratifizierung.
- `04 §3.1`, Schlussabsatz: eine Verfassung, die `t_exp` ueber eine Policy-Maximallaufzeit
  erzwingt (`02 §6.2`), kann keine Stimmen fuehren. Diese Aussage ist bisher **behauptet, nicht
  gemessen**.
- `02a §2.6`: der Budget-Austritt laeuft ueber `t_exp`; der Trust-Pfad ist damit uhrgebunden.
- `D350`: `now` bekommt keine Quelle. Szenario H misst den Ist-Zustand, bevor an einem der
  beiden Zeitregime etwas geaendert wird.

## Auftrag

Neue Datei `tools/sim/szenario_h.py`, aufgebaut nach dem Muster von `tools/sim/szenario_g.py`:
`main()` mit `tempfile.TemporaryDirectory()`, ein `_aufbau`, ein `_beobachte`, je Lauf eine
Funktion, am Ende ein `_befunde`, das die Ist-Werte **immer** druckt und danach je Erwartung
`bestaetigt` oder `widerlegt` ausgibt.

Vier Teilnehmer, Namen wie in `szenario_g.py`. Drei Uhrlagen, die in allen drei Laeufen
dieselben sind:

- **vor**: `now` deutlich nach allen `t_exp` des Laufs,
- **zurueck**: `now` deutlich vor allen `t_exp` des Laufs,
- **ohne**: `now=None` wird an die Auswertung durchgereicht.

`Teilnehmer.read_now()` liefert immer einen Wert; die Lage **ohne** entsteht dadurch, dass
`szenario_h.py` in seinem eigenen `_beobachte` `now=None` uebergibt, nicht durch einen Eingriff
in `welt.py`.

### Lauf 1 — Governance bei identischem Wissen und drei Uhren

Gerade Epochenkette ohne Konflikt, Vollzustellung an alle vier, kein Claim mit `t_exp`.
Danach `resolve_epoch` je Beobachter unter seiner Uhrlage.

Erwartung: alle vier stehen auf **derselben** Epoche mit **demselben** `constitution_hash` und
derselben Vermerkmenge.

Die Erwartung wird **abgeleitet, nicht getippt**: geprueft wird die Gleichheit der vier
Beobachterzeilen untereinander, nicht die Uebereinstimmung mit einer im Quelltext stehenden
Epochennummer. Die tatsaechliche Epochennummer wird gedruckt.

### Lauf 2 — dieselbe Kette, aber mit `t_exp` auf den Stimmen

Aufbau wie Lauf 1, aber jede `vote@1` traegt ein `t_exp`. Uhrlagen unveraendert.

Erwartung: bei **allen** Beobachtern erscheint `VOTE_WITH_EXPIRY` je Stimme, keine Epoche
entsteht ueber die Genesis hinaus, und das Ergebnis ist zwischen den drei Uhrlagen identisch —
die Stimme faellt an der Formpruefung, nicht am Ablauf.

Das ist der zweite Fehlermodus zu Lauf 1 nach Pruefregel 68: Lauf 1 prueft, dass die Uhr nicht
durchschlaegt, Lauf 2 stellt die Lage her, in der `t_exp` tatsaechlich im Governance-Pfad
auftaucht.

`t_exp` wird in diesem Lauf **direkt beim Signieren gesetzt**. Die Policy-Maximallaufzeit aus
`02 §6.2` wird nicht nachgebaut. Ob sie im Code ueberhaupt erzwingbar ist, ist eine offene
Frage — sie wird im Abschlussbericht **gemeldet**, nicht beantwortet und nicht gebaut.

### Lauf 3 — Trust unter denselben drei Uhren

Eine Trust-Kante beziehungsweise ein Claim mit `t_exp`, dessen Klassifikation ueber
`classify_all` beziehungsweise den Verifier laeuft. Identische Inbox bei allen vier, dieselben
drei Uhrlagen.

Erwartung: die Klassifikation **divergiert** — `State.ACTIVE` bei **zurueck**, `State.EXPIRED`
bei **vor**, `State.LINKED` bei **ohne** —, und zwar auf identischem Claim-Satz.

Zweite Stufe im selben Lauf: derselbe Claim wird einem vierten Beobachter erst zugestellt,
nachdem dessen `now` bereits nach `t_exp` liegt. Erwartung: die Nachlieferung heilt nicht, der
Claim kommt an und ist `EXPIRED`. Gedruckt wird, ob irgendein Vermerk zwischen "nie erhalten"
und "zu spaet erhalten" unterscheidet.

## Ausdrueckliche Nicht-Ziele

- **Kein Eingriff in `tools/sim/welt.py`.** Kein Delay-, Reorder- oder Verlust-Primitiv.
  Verzoegerung und Teilzustellung sind ueber die Reihenfolge der `zustellen`-Aufrufe und ueber
  `nur=[...]` bereits ausdrueckbar.
- Keine Aenderung an `szenario_g.py` oder an einem anderen bestehenden Szenario.
- Keine Aenderung an `symbolon/verifier.py`, `symbolon/governance/tally.py`,
  `symbolon/governance/epoch.py`, `symbolon/trust/` oder `symbolon/profiles/`.
- Keine Spec-Aenderung, kein Registereintrag.
- Kein neuer Test in `tests/`. Szenario H ist ein Diagnoselauf wie G, kein Testfall.
- Keine Golden Anchors anfassen.

## Abnahmekriterien

1. `python -m tools.sim.szenario_h` laeuft durch und druckt drei Laeufe und einen Befundblock.
2. Jede Erwartung erscheint im Befundblock als `bestaetigt` oder `widerlegt`, in beiden Faellen
   **mit den gedruckten Ist-Werten davor**.
3. Lauf 1 vergleicht die Beobachter untereinander. Im Quelltext steht keine erwartete
   Epochennummer.
4. Lauf 3 druckt je Uhrlage den `State`-Namen aus.
5. `make check` bleibt gruen, Testzahl unveraendert bei 797.
6. `tools/check_specs.py` bleibt gruen, auch fuer diese Prompt-Datei.

## Wenn eine Messung dem Prompt widerspricht

Melden, nicht anpassen. Weicht ein Lauf von der hier notierten Erwartung ab, bleibt der Code so,
dass die Abweichung sichtbar wird, und der Abschlussbericht nennt sie. Insbesondere Lauf 3: falls
die Klassifikation **nicht** divergiert, ist das der interessantere Befund und wird nicht
weggebaut.

## Abschluss

Ein Commit auf `szenario-h`, kein Merge. Zurueck kommt der **vollstaendige** `git diff` gegen den
Branchpunkt `535dddd`, nicht `--numstat`, plus die vollstaendige Ausgabe von
`python -m tools.sim.szenario_h` und die letzten Zeilen von `make check`.
