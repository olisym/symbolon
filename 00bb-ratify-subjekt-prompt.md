# 00bb — Reparatur: `UNSUPPORTED_RATIFICATION` zeigt auf das falsche Subjekt

## Branch und Basis

Weiter auf `szenario-h`, Basis-Commit `ab3153e38f1bbc2f0c399e4ce3e9e26510e66ebf`
(`00ba: Szenario H misst die zwei Zeitregime`). Kein neuer Branch, kein Merge — der Defekt wird
vor dem Merge auf demselben Branch behoben.

## Normative Grundlage

- `08 §2.2`: eine Aussage, die kollidieren koennen soll, muss benennen, wovon sie handelt.
- `04 §3` und D94: ein Vermerk traegt ein Subjekt, in der Regel eine `claim_id`.
- `D351`: das gemessene Verhalten ist ein Defekt, kein Verhalten. Repariert wird das Subjekt,
  nicht die Erwartung.

## Der Befund, den du reproduzieren wirst

`.venv/bin/python -m tools.sim.szenario_h`, Lauf 2, jede Uhrlage, jeder Beobachter:

```
UNSUPPORTED_RATIFICATION subject=317a8a8b652f40d4
UNSUPPORTED_RATIFICATION subject=c54c234fd749c161
UNSUPPORTED_RATIFICATION subject=dcf9907a01a6b2a3
VOTE_WITH_EXPIRY subject=317a8a8b652f40d4
VOTE_WITH_EXPIRY subject=c54c234fd749c161
VOTE_WITH_EXPIRY subject=dcf9907a01a6b2a3
```

Die drei Subjekte sind die `claim_id` der drei Stimmen. Die `claim_id` der einzigen Ratifizierung
ist `5a05e8f9ff11a97c` und kommt in keinem Vermerk vor.

Erwartbar aus dem Code sind vier Vermerke: ein `UNSUPPORTED_RATIFICATION` mit
`claim_id(ratify_a)`, drei `VOTE_WITH_EXPIRY` mit den `claim_id` der Stimmen.

Bereits geprueft und als Ursache ausgeschlossen: `resolve_epoch` in
`symbolon/governance/chain.py` filtert die Kandidaten ueber `is_nuc_name(claim, "ratify")`;
`_unsupported` in `symbolon/governance/epoch.py` setzt genau ein Finding mit `claim_id(ratify)`;
`dedupe_sort` in `symbolon/governance/findings.py` ist `tuple(sorted(set(...)))`.

## Auftrag

1. Ursache finden. Der Pfad zwischen `decide` und `verify_ratification` ist der ungepruefte Teil.
2. Reparieren, sodass der Vermerk den beanstandeten Claim benennt und genau einmal erscheint.
3. Einen Regressionstest anlegen, der die Lage aus Lauf 2 herstellt — Ratifizierung scheitert,
   waehrend Tally-Vermerke anfallen — und Art **und** Subjekt jedes Vermerks prueft.

Die erwartete Menge im Test wird **abgeleitet**, nicht getippt: aus `claim_id(ratify)` und den
`claim_id` der Stimmen des Testaufbaus, nicht aus einer Hex-Konstante.

**Ruecknahmeprobe.** Nimm die Reparatur zurueck und bestaetige, dass der neue Test rot wird.
Berichte das Ergebnis beider Laeufe. Danach die Reparatur wiederherstellen.

## Ausdrueckliche Nicht-Ziele

- **Keine Aenderung an `tools/sim/szenario_h.py`.** Es ist der Zeuge. Seine Ausgabe muss sich
  durch die Reparatur aendern; das ist der Beleg, nicht der Fehler.
- Keine Aenderung an bestehenden Golden Anchors. Wenn ein bestehender Anchor durch die Reparatur
  faellt, ist das zu **melden**, nicht auszugleichen.
- Kein Nachziehen bestehender Tests auf das neue Verhalten ohne Meldung. Faellt ein Test,
  berichte ihn namentlich, bevor du ihn anfasst.
- Keine Spec-Aenderung, kein Registereintrag, keine Umbenennung von Finding-Arten.
- Keine Aufraeumarbeiten im beruehrten Modul.

## Abnahmekriterien

1. Lauf 2 von Szenario H zeigt je Beobachter genau vier Vermerke: einmal
   `UNSUPPORTED_RATIFICATION` mit dem Subjekt der Ratifizierung, dreimal `VOTE_WITH_EXPIRY` mit
   den Subjekten der Stimmen.
2. Der neue Regressionstest prueft Art und Subjekt, mit abgeleiteten Erwartungen.
3. Die Ruecknahmeprobe ist berichtet: Test rot ohne Reparatur, gruen mit.
4. `make check` gruen. Die Testzahl steigt um die Zahl der neuen Tests; die Differenz zu 797 wird
   genannt und begruendet.
5. Faellt ein bestehender Test oder Anchor, steht er namentlich im Bericht.

## Wenn eine Messung dem Prompt widerspricht

Melden, nicht anpassen. Erweist sich das Verhalten wider Erwarten als beabsichtigt und irgendwo
normativ gedeckt, halte an und nenne die Fundstelle, statt zu reparieren.

## Abschluss

Ein Commit auf `szenario-h`, kein Merge. Zurueck kommt der vollstaendige
`git --no-pager diff ab3153e`, die Vermerkzeilen aus Lauf 2 nach der Reparatur, das Ergebnis der
Ruecknahmeprobe und die letzten Zeilen von `make check`.
