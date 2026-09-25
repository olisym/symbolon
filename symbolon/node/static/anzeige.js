// Anzeige: reine Funktionen ohne DOM, navigator und IndexedDB (D486 Beschluss 5).
// Was aus den Antworten des S-Node Worte macht: der Stand eines Antrags, die Änderungen einer
// Satzung, ein Betrag, die Zeilen der Kasse und die Wörter für Zustände, Warnungen und
// Abweisungen. Ein unbekannter Warnungs- oder Abweisungsname erscheint wörtlich (D486 Beschluss 3).

// Stand eines Antrags in Worten, aus yes, no, needed, n von GET /proposals (D486 Beschluss 2,
// szenario-verein §3, szenario-verein §4).
export function standZeile(antrag) {
  const ja = antrag.yes.length;
  const nein = antrag.no.length;
  if (antrag.needed === null || antrag.n === null) {
    return `${ja} Ja, ${nein} Nein`;
  }
  return `${ja} Ja, ${nein} Nein, ${antrag.needed} von ${antrag.n} nötig`;
}

// Name zu einem Schlüssel, sonst gekürzt (D479 Beschluss 5, D486 Beschluss 2).
export function nameVon(namen, schluessel) {
  const gefunden = namen.get(schluessel);
  if (gefunden) return gefunden;
  if (schluessel.length <= 12) return schluessel;
  return `${schluessel.slice(0, 6)}…${schluessel.slice(-6)}`;
}

// Ein Feldwert in Worten: Text wörtlich, sonst als JSON (D487 Beschluss 4).
function feldWert(wert) {
  if (wert === null || wert === undefined) return "–";
  if (typeof wert === "string") return wert;
  return JSON.stringify(wert);
}

// Änderungen zwischen geltender und vorgeschlagener Satzung in Worten (D486 Beschluss 2,
// D487 Beschluss 4, aus GET /proposals: changes.added, changes.removed, changes.fields).
export function aenderungen(changes, namen) {
  const zeilen = [];
  for (const schluessel of changes.added) {
    zeilen.push(`${nameVon(namen, schluessel)} aufgenommen`);
  }
  for (const schluessel of changes.removed) {
    zeilen.push(`${nameVon(namen, schluessel)} ausgeschlossen`);
  }
  for (const feld of changes.fields) {
    zeilen.push(`${feld.field}: ${feldWert(feld.old)} → ${feldWert(feld.new)}`);
  }
  return zeilen;
}

// Ein Betrag in Worten: EUR-Cent als Euro mit Komma, jede andere Einheit wörtlich neben der
// Zahl (D486 Beschluss 2, szenario-verein §6).
export function betrag(amount, unit) {
  if (amount === null || amount === undefined) return "–";
  if (unit === "EUR-Cent") {
    const euro = Math.trunc(amount / 100);
    const cent = String(amount % 100).padStart(2, "0");
    return `${euro},${cent} €`;
  }
  if (unit === null || unit === undefined) return `${amount}`;
  return `${amount} ${unit}`;
}

// Die Zeilen der Kasse: unterschrieben, quittiert oder fehlt, je Teilnehmer, nur für
// Obligationen an diesen Gläubiger (D486 Beschluss 2 und 4, szenario-verein §6).
export function kassenZeilen(teilnehmer, obligationen, glaeubiger) {
  return teilnehmer.map((person) => {
    const eigene = obligationen.filter(
      (o) => o.debtor === person && o.creditor === glaeubiger,
    );
    let zustand = "fehlt";
    if (eigene.some((o) => o.state === "SETTLED")) zustand = "quittiert";
    else if (eigene.length > 0) zustand = "unterschrieben";
    return { teilnehmer: person, zustand, obligationen: eigene };
  });
}

function wortAus(worte, wert) {
  return worte.get(wert) ?? wert;
}

const MITGLIEDSCHAFT = new Map([
  ["MEMBER", "Mitglied"],
  ["APPLICANT", "hat bestätigt, steht nicht auf der Liste"],
  ["GRANT_ONLY", "steht auf der Liste, hat die geltende Satzung noch nicht bestätigt"],
  ["NONE", "Kein Mitglied"],
]);

// Zustand der Mitgliedschaft in Worten (D487 Beschluss 2, 04 §6.1, 04 §6.3).
export function mitgliedschaftInWorten(zustand) {
  return wortAus(MITGLIEDSCHAFT, zustand);
}

// Ist mindestens ein Teilnehmer GRANT_ONLY, sagt der Verein, dass sich die Satzung
// geändert hat (D487 Beschluss 2, szenario-verein §4, 04 §6.3).
export function hinweisSatzungGeaendert(mitgliedschaften) {
  const geaendert = mitgliedschaften.some(([, ergebnis]) => ergebnis.state === "GRANT_ONLY");
  if (!geaendert) return null;
  return (
    "Die Satzung hat sich geändert. Wer sie nicht neu bestätigt, bleibt " +
    "stimmberechtigt, ist aber an die neue Fassung nicht gebunden."
  );
}

const AUSZAEHLUNG = new Map([
  ["PASSED", "Angenommen"],
  ["FAILED", "Abgelehnt"],
  ["PENDING", "Offen"],
  ["UNEVALUABLE", "Nicht auszählbar"],
]);

// Zustand der Auszählung in Worten (D486 Beschluss 2, 04 §3.3).
export function auszaehlungInWorten(zustand) {
  return wortAus(AUSZAEHLUNG, zustand);
}

const TILGUNG = new Map([
  ["SETTLED", "Bezahlt"],
  ["OPEN", "Offen"],
  ["EXPIRED", "Abgelaufen"],
  ["INDETERMINATE", "Unklar"],
]);

// Zustand der Tilgung in Worten (D486 Beschluss 2, 03 §3.3.2).
export function tilgungInWorten(zustand) {
  return wortAus(TILGUNG, zustand);
}

const WARNUNGEN = new Map([
  ["BUDGET_FULL", "Dein Budget ist voll. Verkleinere zuerst eine Bürgschaft."],
  ["ALREADY_VOTED", "Du hast schon abgestimmt. Eine zweite Stimme macht beide ungültig."],
]);

// Eine Warnung in Worten, aus den Sätzen in szenario-verein §3 und §5.1; eine unbekannte
// erscheint mit ihrem Namen (D486 Beschluss 3).
export function warnungInWorten(name) {
  return wortAus(WARNUNGEN, name);
}

const ABWEISUNGEN = new Map([
  ["NOT_CURRENT", "Der Antrag gilt nicht mehr für die aktuelle Epoche."],
  ["NOT_PASSED", "Der Antrag ist noch nicht angenommen."],
  ["ALREADY_PARTICIPANT", "Diese Person steht schon auf der Mitgliederliste."],
  ["NOT_PARTICIPANT", "Diese Person steht nicht auf der Mitgliederliste."],
  ["INVALID_WEIGHT", "Das Gewicht liegt außerhalb der erlaubten Spanne."],
  ["NOT_CREDITOR", "Nur der Gläubiger kann quittieren."],
]);

// Eine Abweisung in Worten, aus D479 Beschluss 4; eine unbekannte erscheint mit ihrem Namen
// (D486 Beschluss 3).
export function abweisungInWorten(name) {
  return wortAus(ABWEISUNGEN, name);
}

// Der Wert eines Claims in Worten: eine Wahl aus vote@1 als „Ja“ oder „Nein“, sonst wie
// bisher als JSON (D487 Beschluss 4, aus GET /claims: p und value).
export function wertInWorten(p, value) {
  if (p.endsWith("/vote@1") && value && typeof value === "object" && !Array.isArray(value)) {
    if (value["0"] === 1) return "Ja";
    if (value["0"] === 0) return "Nein";
  }
  return value === null || value === undefined ? "–" : JSON.stringify(value);
}
