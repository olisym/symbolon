// Anzeige: reine Funktionen ohne DOM, navigator und IndexedDB (D486 Beschluss 5).
// Was aus den Antworten des S-Node Worte macht: der Stand eines Antrags, die Änderungen einer
// Satzung, ein Betrag, die Zeilen der Kasse und die Wörter für Zustände, Warnungen und
// Abweisungen. Ein unbekannter Warnungs- oder Abweisungsname erscheint wörtlich (D486 Beschluss 3).
// Dazu die Titel der Anträge und die Sätze der Absicht, der Folge und der Meldung
// (D492 Beschluss 1 bis 3 und 5), die Wörter aus D494 Beschluss 5, die Geschichte der
// Demonstration (D494 Beschluss 3, D496 Beschluss 1, D509 Beschluss 1), Zeit relativ zur Uhr
// des S-Node (D496 Beschluss 2), die Beschriftung eines Tabs (D506 Beschluss 2 und 4), ob ein
// Widerspruch oben steht und was seine Karte sagt (D525 Beschluss 1 bis 3, D507 Beschluss 1), und
// was die Seite über Stimmen einer Wurzel von mehreren Schlüsseln sagt (D542 Beschluss 6, D543),
// und über Stimmen, die still nicht zählen: ein zweites Ja, ein gesperrtes Gerät (D556).
// Die Gründung: Text und Betrag, die Schwellen als Sätze, der Stand und seine Sätze
// (D651 Beschluss 3 bis 5, D648 Beschluss 2 und 5, 04 §3.2). Gleiche Namen, die Regie ohne
// simulierte Personen, Sachfelder mit Typ (D654 Beschluss 2 bis 4).

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

// Namen als Aufzählung: „niemand“, einer, sonst mit Kommas und „und“ vor dem letzten; aus
// app.js hierher gezogen (D556 Beschluss 6).
export function aufzaehlung(namen) {
  if (namen.length === 0) return "niemand";
  if (namen.length === 1) return namen[0];
  return `${namen.slice(0, -1).join(", ")} und ${namen[namen.length - 1]}`;
}

// Name zu einem Schlüssel, sonst gekürzt (D479 Beschluss 5, D486 Beschluss 2).
export function nameVon(namen, schluessel) {
  const gefunden = namen.get(schluessel);
  if (gefunden) return gefunden;
  if (schluessel.length <= 12) return schluessel;
  return `${schluessel.slice(0, 6)}…${schluessel.slice(-6)}`;
}

// Schlüssel auf den Namen zum Anzeigen, in der Reihenfolge der Liste. Gleich heisst ohne
// Leerraum am Rand, in NFC und ohne Gross und Klein; kommt ein Name mehr als einmal vor,
// trägt jeder „Name (Kürzel)“ (D654 Beschluss 2, D492 Beschluss 5).
export function namenEindeutig(liste) {
  const abbildung = new Map();
  if (!Array.isArray(liste)) return abbildung;
  const eintraege = [];
  for (const eintrag of liste) {
    if (eintrag === null || typeof eintrag !== "object") continue;
    const name = eintrag.name;
    const schluessel = eintrag.I;
    if (typeof name !== "string" || typeof schluessel !== "string") continue;
    if (name.trim() === "") continue;
    eintraege.push({ schluessel, name, form: name.trim().normalize("NFC").toLowerCase() });
  }
  const zahlen = new Map();
  for (const eintrag of eintraege) zahlen.set(eintrag.form, (zahlen.get(eintrag.form) ?? 0) + 1);
  for (const eintrag of eintraege) {
    const gezeigt =
      zahlen.get(eintrag.form) > 1
        ? `${eintrag.name.trim()} (${nameVon(new Map(), eintrag.schluessel)})`
        : eintrag.name;
    abbildung.set(eintrag.schluessel, gezeigt);
  }
  return abbildung;
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
  ["CHANGE_VOTE", "Du hast schon anders abgestimmt. Diese Stimme ersetzt die frühere."],
  ["DEVICE_ENDED", "Dieses Gerät ist gesperrt. Die Stimme zählt nicht."],
  ["SAME_VOTE", "Du hast schon so abgestimmt. Die Stimme zählt einmal."],
]);

// Eine Warnung in Worten, aus den Sätzen in szenario-verein §3 und §5.1, CHANGE_VOTE aus
// D548 Beschluss 2, DEVICE_ENDED aus D556 Beschluss 3; eine unbekannte erscheint mit ihrem Namen
// (D486 Beschluss 3).
export function warnungInWorten(name) {
  return wortAus(WARNUNGEN, name);
}

// Die Warnung vor einem zweiten Ja: die anderen Anträge aus effect.conflict, mit Titeln aus
// felder.titelVon, wenn alle bekannt sind; je Antrag aus effect.falls ein Satz, dass er nicht mehr
// angenommen wäre (D556 Beschluss 2, 04 §4.4).
export function konfliktWarnung(effect, felder) {
  const andere = effect?.conflict ?? [];
  const titelVon = felder?.titelVon ?? {};
  const titel = (kennung) => (Object.hasOwn(titelVon, kennung) ? titelVon[kennung] : null);
  const bekannt = andere.length > 0 && andere.every((kennung) => typeof titel(kennung) === "string");
  let wem = andere.length === 1 ? "einem anderen Antrag" : "anderen Anträgen";
  if (bekannt) wem = aufzaehlung(andere.map((kennung) => `„${titel(kennung)}“`));
  const keine = andere.length === 1 ? "keine deiner beiden Zustimmungen" : "keine deiner Zustimmungen";
  const saetze = [
    `Du hast unter dieser Fassung der Satzung schon ${wem} zugestimmt.`,
    `Stimmst du hier Ja, zählt ${keine}, und das lässt sich nicht zurücknehmen, solange diese Fassung gilt.`,
  ];
  for (const kennung of effect?.falls ?? []) {
    const name = titel(kennung);
    saetze.push(
      typeof name === "string"
        ? `„${name}“ wäre dann nicht mehr angenommen.`
        : "Ein anderer Antrag wäre dann nicht mehr angenommen.",
    );
  }
  return saetze.join(" ");
}

const ABWEISUNGEN = new Map([
  ["NOT_CURRENT", "Der Antrag gilt nicht mehr für die aktuelle Epoche."],
  ["NOT_PASSED", "Der Antrag ist noch nicht angenommen."],
  ["ALREADY_PARTICIPANT", "Diese Person steht schon auf der Mitgliederliste."],
  ["NOT_PARTICIPANT", "Diese Person steht nicht auf der Mitgliederliste."],
  ["INVALID_WEIGHT", "Das Gewicht liegt außerhalb der erlaubten Spanne."],
  ["NOT_CREDITOR", "Nur der Gläubiger kann quittieren."],
  ["NOT_A_TIP", "An dieser Stelle endet die Kette nicht. Angeschlossen wird nur an ein Ende."],
  [
    "more than one tip",
    "Die Kette hat zwei Enden, weil zweimal an dieselbe Stelle unterschrieben wurde. " +
      "Gewählt werden muss, an welches Ende angeschlossen wird.",
  ],
  [
    "INCOHERENT_EXPIRY",
    "Die Dauer ist zu kurz: das Ende muss nach der Unterschrift liegen. Gib mindestens 1 Tag ein.",
  ],
  ["INVALID_VALUE", "Ein Wert hat nicht die Form, die die Vorlage des Vereins verlangt."],
  ["MISSING_FIELD", "Name, Sitz und Zweck braucht jeder Verein. Eines davon fehlt."],
  ["TOO_FEW_FOUNDERS", "Ein Verein braucht mindestens drei Gründer."],
  ["NOT_FOUNDING", "Dieser Verein besteht schon. Verwerfen lässt sich nur eine Gründung."],
]);

// Eine Abweisung in Worten, aus D479 Beschluss 4, dazu NOT_A_TIP und die Abweisung wegen
// mehrerer Spitzen (D492 Beschluss 4, D476 Beschluss 3) und INCOHERENT_EXPIRY (D500 Beschluss 2);
// eine unbekannte erscheint mit ihrem Namen (D486 Beschluss 3).
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

// Ob eine Gabelung eine Doppelstimme ist: jeder Claim eine vote@1-Stimme, alle mit J == [3, h]
// auf denselben Antrag h; die Werte spielen keine Rolle (D525 Beschluss 1). claims wie aus
// GET /claims: p, value und J.
function doppelstimme(claims) {
  if (claims.length === 0) return false;
  const antrag = claims[0].J[1];
  return claims.every(
    (claim) => claim.p.endsWith("/vote@1") && claim.J[0] === 3 && claim.J[1] === antrag,
  );
}

// Ob die Karte einer Gabelung oben steht: genau dann, wenn die Gabelung eine Doppelstimme ist und
// ihr Antrag unter den Anträgen der Seite im Stand PENDING steht (D525 Beschluss 2, ändert
// D507 Beschluss 1).
export function widerspruchOben(claims, antraege) {
  if (!doppelstimme(claims)) return false;
  const antrag = antraege.find((eintrag) => eintrag.proposal === claims[0].J[1]);
  return antrag !== undefined && antrag.state === "PENDING";
}

// Die Überschrift der Karte einer Gabelung und ob keine der Stimmen zählt: eine Doppelstimme mit
// gleichen Werten „zweimal {Wert}“, sonst mit nur Ja und Nein „zugleich“, sonst „zweimal
// verschieden“, alle drei zaehltNicht; sonst „zweimal an dieselbe Stelle der Kette“
// (D526 Beschluss 3, D525 Beschluss 3, 04 §3.1 Bedingung 6).
export function widerspruchSatz(name, claims, antraege, namen) {
  if (!doppelstimme(claims)) {
    return { satz: `${name} hat zweimal an dieselbe Stelle der Kette unterschrieben.`, zaehltNicht: false };
  }
  const antrag = antraege.find((eintrag) => eintrag.proposal === claims[0].J[1]);
  const worum = antrag ? `zum Antrag „${antragTitel(antrag.changes, namen)}“` : "zu einem Antrag";
  const werte = claims.map((claim) => wertInWorten(claim.p, claim.value));
  let was = "zweimal verschieden";
  if (werte.every((wert) => wert === werte[0])) was = `zweimal ${werte[0]}`;
  else if (werte.every((wert) => wert === "Ja" || wert === "Nein")) was = "Ja und Nein zugleich";
  return { satz: `${name} hat ${worum} ${was} unterschrieben.`, zaehltNicht: true };
}

// Die Punkte zu Feststellungen, die nicht tragen, weil sie sich auf eine Stimme der Gabelung
// stützen: je Feststellung, deren Zeugenliste unter value["0"] eine der ids nennt, ein Punkt mit
// dem Namen ihres I, in der Reihenfolge der Feststellungen; feststellungen wie aus GET /claims
// (D559 Beschluss 1 und 2).
export function feststellungPunkte(ids, feststellungen, namen) {
  const punkte = [];
  for (const claim of feststellungen) {
    const zeugen = claim.value?.["0"];
    if (!Array.isArray(zeugen)) continue;
    if (!zeugen.some((zeuge) => typeof zeuge === "string" && ids.includes(zeuge))) continue;
    punkte.push(`${nameVon(namen, claim.I)}s Feststellung stützt sich auf diese Stimme und trägt deshalb nicht.`);
  }
  return punkte;
}

// Die Punkte zu Stimmen in einer Gabelung, die keine Doppelstimme ist: je Antrag ihrer vote@1-Claims
// mit J[0] == 3 ein Punkt, in der Reihenfolge des ersten Auftretens, Einzahl oder Mehrzahl, ohne
// bekannten Antrag „zu einem Antrag“; für eine Doppelstimme keiner (D559 Beschluss 3, 04 §3.1
// Bedingung 6).
export function stimmenPunkte(claims, antraege, namen) {
  if (doppelstimme(claims)) return [];
  const zahl = new Map();
  for (const claim of claims) {
    if (!claim.p.endsWith("/vote@1") || claim.J[0] !== 3) continue;
    zahl.set(claim.J[1], (zahl.get(claim.J[1]) ?? 0) + 1);
  }
  return [...zahl].map(([kennung, anzahl]) => {
    const antrag = antraege.find((eintrag) => eintrag.proposal === kennung);
    const worum = antrag ? `zum Antrag „${antragTitel(antrag.changes, namen)}“` : "zu einem Antrag";
    return anzahl === 1 ? `Die Stimme ${worum} zählt nicht.` : `Die Stimmen ${worum} zählen nicht.`;
  });
}

// Der Satz zu Stimmen einer Wurzel von mehreren Schlüsseln, gruppe wie aus GET /geraetestimmen:
// wählen die zählenden Stimmen verschieden, eine Karte mit ihren Punkten, dazu, solange sie oben
// steht, dass eine neue Stimme sie ersetzt; wählen erst zählende und ersetzte zusammen
// verschieden, der Satz der Auflösung ohne Karte; sonst der Satz der gleichen Wahl. Die Zahl der
// Geräte ist die Zahl verschiedener Schlüssel über zählende und ersetzte Stimmen, zwei bis vier
// ausgeschrieben; „Keine der beiden“ nur bei genau zwei Stimmen (D542 Beschluss 6, D543 Beschluss
// 1 und 2, D551 Beschluss 4 und 5, D552 Beschluss 2). Steht die Wurzel beim Antrag der Gruppe
// unter conflicting und wählen die zählenden Stimmen nicht verschieden, kein Satz: sie zählen
// nicht (D556 Beschluss 4).
export function geraeteSatz(name, gruppe, namen, antraege) {
  const titel = antragTitel(gruppe.changes, namen);
  const alle = [...gruppe.stimmen, ...gruppe.ersetzt];
  const geraete = new Set(alle.map(([, schluessel]) => schluessel)).size;
  const zahl = { 2: "zwei", 3: "drei", 4: "vier" }[geraete] ?? String(geraete);
  const werte = new Set(gruppe.stimmen.map(([, , wahl]) => wahl));
  const antrag = (antraege ?? []).find((eintrag) => eintrag.proposal === gruppe.proposal);
  if (werte.size <= 1 && (antrag?.conflicting ?? []).includes(gruppe.root)) {
    return { karte: false, satz: null, punkte: [] };
  }
  if (werte.size > 1) {
    const punkte = [
      gruppe.stimmen.length === 2 ? "Keine der beiden Stimmen zählt." : "Keine dieser Stimmen zählt.",
      `${name}s Bürgschaften zählen weiter.`,
    ];
    if (geraeteOben(gruppe, antraege)) {
      punkte.push(`Eine neue Stimme von ${name} ersetzt ${gruppe.stimmen.length === 2 ? "beide" : "alle"}.`);
    }
    return {
      karte: true,
      satz: `${name} hat zum Antrag „${titel}“ auf ${zahl} Geräten Ja und Nein unterschrieben.`,
      punkte,
    };
  }
  const wahl = werte.has(1) ? "Ja" : "Nein";
  if (new Set(alle.map(([, , wert]) => wert)).size > 1) {
    const ersetzt =
      gruppe.stimmen.length === 1
        ? `das mit einer neuen Stimme ersetzt. Sie zählt: ${wahl}.`
        : `das mit neuen Stimmen ersetzt. Sie zählen einmal: ${wahl}.`;
    return {
      karte: false,
      satz: `${name} hat zum Antrag „${titel}“ auf ${zahl} Geräten verschieden gestimmt und ${ersetzt}`,
      punkte: [],
    };
  }
  return {
    karte: false,
    satz: `${name} hat zum Antrag „${titel}“ auf ${zahl} Geräten ${wahl} gestimmt. Das zählt einmal.`,
    punkte: [],
  };
}

// Die Karte einer Wurzel, die mehreren Anträgen derselben Fassung zugestimmt hat, titel die Titel
// der Anträge der Seite, die sie unter conflicting nennen; einer allein, wenn das andere Ja ersetzt
// ist (D556 Beschluss 4, 04 §4.4).
export function zustimmungSatz(name, titel) {
  const weiter = `${name}s Bürgschaften zählen weiter.`;
  if (titel.length === 1) {
    return {
      satz: `${name} hat „${titel[0]}“ und einem weiteren Antrag zugestimmt.`,
      punkte: [`Die Zustimmung zu „${titel[0]}“ zählt nicht.`, weiter],
    };
  }
  const zahl = { 2: "zwei", 3: "drei", 4: "vier" }[titel.length] ?? String(titel.length);
  return {
    satz: `${name} hat ${zahl} Anträgen zugestimmt: ${aufzaehlung(titel.map((eintrag) => `„${eintrag}“`))}.`,
    punkte: [titel.length === 2 ? "Keine der beiden Zustimmungen zählt." : "Keine dieser Zustimmungen zählt.", weiter],
  };
}

// Der Satz zu einer Stimme unter DISPUTED_VOTE: ein gesperrtes Gerät (D556 Beschluss 5, 04 §3.1).
export function gesperrtSatz(name, titel) {
  return `Eine Stimme von ${name} zum Antrag „${titel}“ zählt nicht: das Gerät ist gesperrt.`;
}

// Ein Antrag der laufenden Abstimmung: current ist nicht falsch (04 §4.7, D605 Beschluss 2).
export function laufend(antrag) {
  return antrag.current !== false;
}

// Steht ein Satzungsantrag ausserhalb der laufenden Abstimmung, der Satz; ohne Liste keiner
// (04 §4.7, D605 Beschluss 3).
export function abstimmungVorbeiSatz(antraege) {
  const vorbei = (antraege ?? []).some((antrag) => antrag.kind === "proposal" && !laufend(antrag));
  if (!vorbei) return null;
  return (
    "Die bisherige Abstimmung über eine neue Fassung ist vorbei: keiner ihrer Anträge kann noch " +
    "durchkommen. Ein neuer Antrag kann es."
  );
}

// Die Zeile auf der Karte eines Antrags ausserhalb der laufenden Abstimmung (04 §4.7,
// D605 Beschluss 3).
export const ANTRAG_VORBEI = "Kann nicht mehr durchkommen. Ein neuer Antrag kann es.";

// Gruppen, deren Antrag auf der Seite steht und läuft, in der Reihenfolge der Gruppen; ohne
// Gruppen keine (04 §4.7, D605 Beschluss 4).
export function laufendeGruppen(gruppen, antraege) {
  const kennungen = new Set((antraege ?? []).filter(laufend).map((antrag) => antrag.proposal));
  return (gruppen ?? []).filter((gruppe) => kennungen.has(gruppe.proposal));
}

// Ob die Karte einer Gruppe aus GET /geraetestimmen oben steht: genau dann, wenn ihr Antrag unter
// den Anträgen der Seite steht, in jedem Zustand; bis zur Feststellung wirkt eine neue Stimme
// (D551 Beschluss 4, ändert D542 Beschluss 6).
export function geraeteOben(gruppe, antraege) {
  return antraege.some((eintrag) => eintrag.proposal === gruppe.proposal);
}

// Titel eines Antrags aus changes: genau eine Änderung benennt ihn, jede andere Zahl heißt
// „Satzung ändern“ (D492 Beschluss 3).
export function antragTitel(changes, namen) {
  const anzahl = changes.added.length + changes.removed.length + changes.fields.length;
  if (anzahl !== 1) return "Satzung ändern";
  if (changes.added.length === 1) return `${nameVon(namen, changes.added[0])} aufnehmen`;
  if (changes.removed.length === 1) return `${nameVon(namen, changes.removed[0])} ausschließen`;
  const feld = changes.fields[0];
  if (feld.old === null || feld.old === undefined) return `${feld.field} festlegen`;
  return `${feld.field} ändern`;
}

// Die Marke über einer Antragskarte aus kind von GET /proposals oder GET /antragstitel (D580
// Beschluss 1, D575 Beschluss 1).
export function antragMarke(kind) {
  return kind === "motion" ? "Sachantrag" : "Satzungsantrag";
}

// Der neue Wortlaut jedes Textfelds, als Zitat unter dem Titel. Der Beitrag in Worten, jedes
// andere Feld wörtlich (D492 Beschluss 3, D654 Beschluss 4).
export function antragZitate(changes) {
  if (!Array.isArray(changes?.fields)) return [];
  return changes.fields
    .filter((feld) => typeof feld?.new === "string")
    .map((feld) => `„${feld.field === "beitrag" ? beitragInWorten(feld.new) : feld.new}“`);
}

function hexVon(bytes) {
  return [...bytes].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

function gleich(links, rechts) {
  if (typeof links !== typeof rechts) return false;
  if (links instanceof Uint8Array || rechts instanceof Uint8Array) {
    return links instanceof Uint8Array && rechts instanceof Uint8Array && hexVon(links) === hexVon(rechts);
  }
  if (Array.isArray(links) || Array.isArray(rechts)) {
    return (
      Array.isArray(links) &&
      Array.isArray(rechts) &&
      links.length === rechts.length &&
      links.every((wert, index) => gleich(wert, rechts[index]))
    );
  }
  if (links instanceof Map || rechts instanceof Map) {
    if (!(links instanceof Map && rechts instanceof Map) || links.size !== rechts.size) return false;
    for (const [schluessel, wert] of links) {
      if (!rechts.has(schluessel) || !gleich(wert, rechts.get(schluessel))) return false;
    }
    return true;
  }
  return links === rechts;
}

function feldAlsText(wert) {
  if (wert === undefined) return null;
  return typeof wert === "string" ? wert : "(kein Text)";
}

// Unterschiede zweier dekodierter Verfassungen in der Form von changes aus GET /proposals,
// für einen Antrag, den /proposals noch nicht führt, weil sein propose@1 erst unterschrieben
// wird (D492 Beschluss 1 und 3, D484 Beschluss 2). null, wenn eine keine Verfassung ist.
export function verfassungsAenderungen(alt, neu) {
  if (!(alt instanceof Map) || !(neu instanceof Map)) return null;
  const liste = (verfassung) => {
    const wert = verfassung.get("participants") ?? [];
    return Array.isArray(wert) ? wert.filter((item) => item instanceof Uint8Array).map(hexVon) : [];
  };
  const vorher = new Set(liste(alt));
  const nachher = new Set(liste(neu));
  const schluessel = [...new Set([...alt.keys(), ...neu.keys()])]
    .filter((key) => typeof key === "string" && key !== "participants")
    .sort();
  return {
    added: [...nachher].filter((key) => !vorher.has(key)).sort(),
    removed: [...vorher].filter((key) => !nachher.has(key)).sort(),
    fields: schluessel
      .filter((key) => !gleich(alt.get(key), neu.get(key)))
      .map((key) => ({ field: key, old: feldAlsText(alt.get(key)), new: feldAlsText(neu.get(key)) })),
  };
}

// „1 Punkt“, sonst „<n> Punkten“ (D494 Beschluss 6, D493).
function punkteInWorten(punkte) {
  return punkte === 1 ? "1 Punkt" : `${punkte} Punkten`;
}

// „1 Tag“, sonst „<d> Tage“ (D496 Beschluss 2).
function tageInWorten(tage) {
  return tage === 1 ? "1 Tag" : `${tage} Tage`;
}

// Die Dauer einer Bürgschaft in ganzen Tagen, aufgerundet: t_exp minus t des dekodierten Kerns
// (D498 Beschluss 1, D496 Beschluss 2).
export function tageAusKern(t, tExp) {
  return Math.ceil((Number(tExp) - Number(t)) / 86400);
}

// Eine Eingabe als ganze Zahl: Number des Texts, wenn das ganz ist, sonst null
// (D501 Beschluss 2).
export function ganzeZahl(text) {
  const zahl = Number(text);
  return Number.isInteger(zahl) ? zahl : null;
}

// Cent aus dem Text des Felds „Euro“: Ziffern, wahlweise ein Punkt und ein oder zwei Ziffern,
// aus den Ziffern gerechnet und nicht über eine Gleitkommazahl; sonst null (D503 Beschluss 1).
export function centAus(text) {
  const teile = /^([0-9]+)(?:\.([0-9]{1,2}))?$/.exec(text);
  if (teile === null) return null;
  return Number(teile[1]) * 100 + Number((teile[2] ?? "").padEnd(2, "0"));
}

// Ein Zeitpunkt als Abstand zur Uhr des S-Node aus GET /now, nie als Kalenderdatum
// (D496 Beschluss 2, D495 Befund 1).
export function zeitpunktInWorten(t, jetzt) {
  const sekunden = Number(jetzt) - Number(t);
  if (sekunden < 60) return "gerade eben";
  if (sekunden < 3600) {
    const minuten = Math.floor(sekunden / 60);
    return minuten === 1 ? "vor 1 Minute" : `vor ${minuten} Minuten`;
  }
  if (sekunden < 86400) {
    const stunden = Math.floor(sekunden / 3600);
    return stunden === 1 ? "vor 1 Stunde" : `vor ${stunden} Stunden`;
  }
  const tage = Math.floor(sekunden / 86400);
  return tage === 1 ? "vor 1 Tag" : `vor ${tage} Tagen`;
}

// Der Name einer Person im Satz der Absicht; fehlt er im Adressbuch, „eine Person ohne Namen“
// mit dem gekürzten Schlüssel, und die Unterschrift bleibt möglich (D494 Beschluss 6, D493).
export function personImSatz(namen, schluessel) {
  const name = namen.get(schluessel);
  if (name) return { name, ohneName: false };
  return { name: `eine Person ohne Namen (${nameVon(new Map(), schluessel)})`, ohneName: true };
}

// Unicode-Klasse Cc: die Steuerzeichen C0 und C1 (D651 Beschluss 3, D649 Befund 5).
const _STEUER = /[\u0000-\u001F\u007F-\u009F]/;

// Kein Text ergibt null; sonst Leerraum am Rand weg, dann NFC. Leer oder mit einem Steuerzeichen
// ergibt null (D651 Beschluss 3, D648 Beschluss 2).
export function textFeld(eingabe) {
  if (typeof eingabe !== "string") return null;
  const text = eingabe.trim().normalize("NFC");
  if (text === "" || _STEUER.test(text)) return null;
  return text;
}

// Euro als 0 oder ohne führende Null, höchstens sieben Stellen, wahlweise Komma oder Punkt und
// eine oder zwei Ziffern; nur 0 bis 9. Null ergibt null. Sonst „24,00 EUR im Jahr“
// (D651 Beschluss 3, D648 Beschluss 2, D496).
export function betragText(eingabe, faelligkeit) {
  if (faelligkeit !== "Monat" && faelligkeit !== "Jahr") return null;
  if (typeof eingabe !== "string") return null;
  const treffer = /^(0|[1-9][0-9]{0,6})(?:[.,]([0-9]{1,2}))?$/.exec(eingabe.trim());
  if (treffer === null) return null;
  const cent = (treffer[2] ?? "").padEnd(2, "0");
  if (treffer[1] === "0" && cent === "00") return null;
  return `${treffer[1]},${cent} EUR im ${faelligkeit}`;
}

// Genau die Form aus D648 Beschluss 2, grösser als null (D651 Beschluss 3).
export function betragLesen(text) {
  if (typeof text !== "string") return null;
  const treffer = /^(0|[1-9][0-9]{0,6}),([0-9]{2}) EUR im (Monat|Jahr)$/.exec(text);
  if (treffer === null) return null;
  const cent = Number(treffer[1]) * 100 + Number(treffer[2]);
  if (cent === 0) return null;
  return { cent, faelligkeit: treffer[3] };
}

// Lesbar als „24,00 € im Jahr“ über betrag; sonst der Text roh, und „–“, wenn es kein Text ist
// (D651 Beschluss 4, D648 Beschluss 2).
export function beitragInWorten(text) {
  if (typeof text !== "string") return "–";
  const gelesen = betragLesen(text);
  if (gelesen === null) return text;
  return `${betrag(gelesen.cent, "EUR-Cent")} im ${gelesen.faelligkeit}`;
}

// Die festen Schwellen in Worten (D651 Beschluss 5, D648 Beschluss 5).
export function schwelleInWorten(paar) {
  if (paar[0] === 1 && paar[1] === 2) return "mehr als die Hälfte";
  if (paar[0] === 2 && paar[1] === 3) return "mehr als zwei Drittel";
  return `mehr als ${paar[0]} von ${paar[1]} Teilen`;
}

// „Name“, „Sitz“, „Zweck“, „Beitrag“; jedes andere Feld in den Anführungszeichen der Seite
// (D654 Beschluss 4).
export function sachfeldName(feld) {
  if (feld === "name") return "Name";
  if (feld === "sitz") return "Sitz";
  if (feld === "zweck") return "Zweck";
  if (feld === "beitrag") return "Beitrag";
  return `„${feld}“`;
}

// Der Eintrag aus GET /vorlagen, dessen Name und Fassung als „name@fassung“ genau
// ``satzung.vorlage`` gleichen; sonst null (D654 Beschluss 4, D648 Beschluss 3).
export function vorlageDerSatzung(satzung, vorlagen) {
  if (satzung === null || typeof satzung !== "object") return null;
  if (vorlagen === null || typeof vorlagen !== "object") return null;
  const genannt = satzung.vorlage;
  if (typeof genannt !== "string") return null;
  for (const [name, eintrag] of Object.entries(vorlagen)) {
    if (eintrag === null || typeof eintrag !== "object") continue;
    if (`${name}@${eintrag.fassung}` === genannt) return eintrag;
  }
  return null;
}

// Text über textFeld, Betrag über betragText, jeder andere Typ null
// (D654 Beschluss 4, D648 Beschluss 2).
export function sachwert(typ, eingabe, faelligkeit) {
  if (typ === "text") return textFeld(eingabe);
  if (typ === "betrag") return betragText(eingabe, faelligkeit);
  return null;
}

// Geschützt zählt amendment, sonst ordinary. Keine Liste heisst kein Schutz. Ohne lesbare
// Schwelle der zählenden Klasse null (D654 Beschluss 4, D646 Beschluss 2, D652 Beschluss 2).
export function sachfeldSatz(feld, satzung, n) {
  if (satzung === null || typeof satzung !== "object") return null;
  const thresholds = satzung.thresholds;
  if (thresholds === null || typeof thresholds !== "object") return null;
  const liste = satzung.protected_fields;
  const geschuetzt = liste != null && Array.isArray(liste) && liste.includes(feld);
  const paar = geschuetzt ? thresholds.amendment : thresholds.ordinary;
  const k = noetigeStimmen(paar, n);
  if (k === null) return null;
  const schwelle = schwelleInWorten(paar);
  const zahl = k < n ? String(k) : "alle";
  const name = sachfeldName(feld);
  if (geschuetzt) {
    return (
      `${name} ist geschützt: Ein Antrag darauf braucht ${schwelle}, wie eine Änderung der Satzung. ` +
      `Bei ${n} Mitgliedern sind das ${zahl}.`
    );
  }
  return `Ein Antrag auf ${name} braucht ${schwelle}. Bei ${n} Mitgliedern sind das ${zahl}.`;
}

// Lokal ist localhost, 127.0.0.1 und jeder Name auf „.localhost“. Das Beispiel ist der erste
// der Namen bruno, chris, anna, der nicht die eigene Adresse ist (D654 Beschluss 3).
export function regieHinweis(hostname, port) {
  const fern =
    "Dieses Fenster ist eine Person. Eine weitere braucht ein eigenes Gerät oder ein eigenes Profil im Browser.";
  const lokal =
    hostname === "localhost" || hostname === "127.0.0.1" ||
    (typeof hostname === "string" && hostname.endsWith(".localhost"));
  if (!lokal) return fern;
  const beispiel = ["bruno", "chris", "anna"].find((name) => `${name}.localhost` !== hostname);
  const mitPort = typeof port === "string" && port !== "" ? `:${port}` : "";
  return (
    "Dieses Fenster ist eine Person. Eine weitere bekommt einen eigenen Tab unter eigener Adresse, etwa " +
    `http://${beispiel}.localhost${mitPort}/.`
  );
}

// Die kleinste Zahl k mit k * den > num * n, oder null bei fremder Form. Gerechnet ohne
// Schleife, damit jede Eingabe endet (04 §3.2, D651 Beschluss 5, D652 Beschluss 2).
export function noetigeStimmen(paar, n) {
  if (!Array.isArray(paar) || paar.length !== 2) return null;
  const [num, den] = paar;
  if (!Number.isInteger(num) || !Number.isInteger(den) || !Number.isInteger(n)) return null;
  if (n <= 0) return null;
  if (!(num >= 0 && num < den)) return null;
  return Math.floor((num * n) / den) + 1;
}

// Drei Sätze, fest membership, ordinary, amendment, oder die leere Liste, wenn eine Art nicht
// lesbar ist. Steht k nicht unter n, endet der Satz mit „sind das alle.“
// (D651 Beschluss 5, D652 Beschluss 2, D641 Befund 2).
export function schwellenSaetze(thresholds, n) {
  if (typeof thresholds !== "object" || thresholds === null) return [];
  const arten = [
    ["membership", "Aufnehmen und ausschließen", true],
    ["ordinary", "Sitz und Beitrag ändern", false],
    ["amendment", "Name, Zweck und alles Übrige der Satzung ändern", false],
  ];
  const saetze = [];
  for (const [art, anfang, mussJa] of arten) {
    const k = noetigeStimmen(thresholds[art], n);
    if (k === null) return [];
    const schwelle = schwelleInWorten(thresholds[art]);
    const zahl = k < n ? String(k) : "alle";
    const kern = mussJa ? `${schwelle} muss Ja sagen` : schwelle;
    saetze.push(`${anfang}: ${kern}. Bei ${n} Mitgliedern sind das ${zahl}.`);
  }
  return saetze;
}

// name, sitz, zweck, beitrag, nur Textwerte; der Beitrag über beitragInWorten
// (D651 Beschluss 4).
export function satzungZeilen(stand) {
  if (stand === null || stand === undefined || typeof stand !== "object") return [];
  const felder = [
    ["name", "Name"],
    ["sitz", "Sitz"],
    ["zweck", "Zweck"],
    ["beitrag", "Beitrag"],
  ];
  const zeilen = [];
  for (const [feld, label] of felder) {
    const wert = stand[feld];
    if (typeof wert !== "string") continue;
    const gezeigt = feld === "beitrag" ? beitragInWorten(wert) : wert;
    zeilen.push(`${label}: ${gezeigt}`);
  }
  return zeilen;
}

// null ohne Verein oder wenn die Fassung nicht die erste ist (D651 Beschluss 4).
export function gruendungStand(view) {
  if (!view?.verein || view.state?.epoch?.index !== 1) return null;
  const membership = view.verein.membership;
  const gruender = membership.map(([wer]) => wer);
  const bestaetigt = membership.filter(([, ergebnis]) => ergebnis.state === "MEMBER").map(([wer]) => wer);
  const offen = membership.filter(([, ergebnis]) => ergebnis.state !== "MEMBER").map(([wer]) => wer);
  return {
    gruender,
    bestaetigt,
    offen,
    besteht: membership.every(([, ergebnis]) => ergebnis.state === "MEMBER"),
  };
}

// Eine sortierte Kopie, deutsch (D651 Beschluss 4).
export function nachNamen(namen) {
  return [...namen].sort((links, rechts) => links.localeCompare(rechts, "de"));
}

function reiheDerGruendung(schluessel, namen, ich) {
  const dabei = ich !== null && ich !== undefined && schluessel.includes(ich);
  const uebrige = nachNamen(
    schluessel.filter((wer) => wer !== ich).map((wer) => nameVon(namen, wer)),
  );
  return aufzaehlung(dabei ? ["du", ...uebrige] : uebrige);
}

// Die eigene Identität heisst „du“ und steht vorn, die übrigen nach nachNamen; ein Schlüssel
// ohne Namen steht gekürzt (D651 Beschluss 4, D652 Beschluss 3, D492 Beschluss 5, D605).
export function gruendungSatz(stand, namen, ich = null) {
  if (stand.besteht) return "Der Verein besteht. Alle Gründer haben die Satzung bestätigt.";
  const bestaetigt = reiheDerGruendung(stand.bestaetigt, namen, ich);
  const offen = reiheDerGruendung(stand.offen, namen, ich);
  return `Der Verein ist in Gründung. Bestätigt: ${bestaetigt}. Noch offen: ${offen}.`;
}

function vorhanden(felder, ...namen) {
  return namen.every((name) => felder[name] !== null && felder[name] !== undefined && felder[name] !== "");
}

// Der Satz der Absicht je Art; fehlt ein nötiger Wert, null (D492 Beschluss 1 und 2).
export function absichtSatz(art, felder) {
  switch (art) {
    case "accept-rules":
      if (typeof felder.geltend !== "boolean") return null;
      // In der Gründung der Satz mit Verein und den übrigen Gründern (D651 Beschluss 5).
      if (felder.geltend && felder.gruendung) {
        const { verein, andere } = felder.gruendung;
        return (
          `Du gründest mit ${aufzaehlung(andere)} den Verein „${verein}“ ` +
          "und bestätigst seine Satzung."
        );
      }
      return felder.geltend
        ? "Du bestätigst die geltende Satzung des Vereins."
        : "Du bestätigst eine frühere Fassung der Satzung.";
    case "propose":
      // Die Art des Antrags gehört zum Satz; ohne sie kein Satz (D580 Beschluss 1).
      if (!vorhanden(felder, "titel") || typeof felder.sachantrag !== "boolean") return null;
      return `Du stellst einen ${antragMarke(felder.sachantrag ? "motion" : "proposal")}: ${felder.titel}.`;
    case "vote": {
      if (!vorhanden(felder, "name", "titel", "wahl")) return null;
      const wahl = { yes: "Ja", no: "Nein" }[felder.wahl];
      if (!wahl) return null;
      if (felder.ohneName) {
        return `Du stimmst ${wahl} zum Antrag „${felder.titel}“ ${felder.name.replace(/^eine /, "einer ")}.`;
      }
      return `Du stimmst ${wahl} zu ${felder.name}s Antrag „${felder.titel}“.`;
    }
    case "ratify":
      if (!vorhanden(felder, "titel")) return null;
      return `Du stellst fest: Der Antrag „${felder.titel}“ ist angenommen.`;
    case "vouch":
      if (!vorhanden(felder, "name", "punkte", "tage")) return null;
      return `Du bürgst für ${felder.name} mit ${punkteInWorten(felder.punkte)} für ${tageInWorten(felder.tage)}.`;
    case "obligation":
      if (!vorhanden(felder, "betrag", "name")) return null;
      return `Du verpflichtest dich, ${felder.betrag} an ${felder.name} zu zahlen.`;
    case "receipt":
      if (!vorhanden(felder, "name", "betrag")) return null;
      return `Du bestätigst, dass ${felder.name} ${felder.betrag} bezahlt hat.`;
    default:
      return null;
  }
}

// Was nach einer Handlung geschieht, aus ihrem Ausgang, wie ihn ablauf gibt, oder { fehler: true }:
// „halten“, solange das Gerät auf eine bestätigte Spitze wartet; „zeichnen“ bei ok, schwebend und
// fehlt; sonst „melden“, und die Seite bleibt mit ihren Auswahlen und Feldern stehen
// (D561 Beschluss 3, D502).
export function nachHandlung(ausgang) {
  if (ausgang.halt) return "halten";
  if (ausgang.ok || ausgang.schwebend || ausgang.fehlt) return "zeichnen";
  return "melden";
}

// Die Folge aus effect, „Danach:“ vor der ersten Zeile; ohne effect keine Zeile
// (D492 Beschluss 2, D490 Beschluss 2). Bei einer Stimme gleiche Wahl aus effect.same, die
// Teilnahme der Wurzel aus effect.participant, nur wo das fehlt aus felder (D544 Beschluss 1);
// bei counts falsch zuerst die Teilnahme, dann gleiche Wahl (D545 Beschluss 1); ersetzt die
// Stimme eine frühere, sagt eine Zeile das (D548 Beschluss 2). Nach der Teilnahme das gesperrte
// Gerät aus effect.ended, dann ein anderes Ja aus effect.conflict (D556 Beschluss 6). Bleibt kein
// Grund, zählt die Stimme nicht, ohne einen zu nennen (D561 Beschluss 2).
export function folgeZeilen(art, effect, felder) {
  if (!effect) return [];
  const zeilen = [];
  if (art === "vote") {
    if (effect.needed !== null && effect.needed !== undefined) {
      zeilen.push(`${effect.yes} von ${effect.needed} nötigen Ja-Stimmen`);
      const fehlen = effect.needed - effect.yes;
      if (effect.passes) {
        zeilen.push("Der Antrag ist dann angenommen; jemand muss den Beschluss noch feststellen.");
      } else if (fehlen === 1) {
        zeilen.push("Es fehlt noch eine.");
      } else {
        zeilen.push(`Es fehlen noch ${fehlen}.`);
      }
    }
    const teilnehmer = effect.participant !== undefined ? effect.participant : felder.teilnehmer;
    // Die neue Stimme ersetzt die frühere (D548 Beschluss 2).
    if (effect.counts === true && effect.replaces === true) {
      zeilen.push("Deine frühere Stimme zählt dann nicht mehr.");
    }
    if (effect.counts === false) {
      if (teilnehmer === false) {
        zeilen.push("Deine Stimme zählt nicht: Du stehst nicht auf der Mitgliederliste.");
      } else if (effect.ended === true) {
        zeilen.push("Deine Stimme zählt nicht: Dieses Gerät ist gesperrt.");
      } else if ((effect.conflict ?? []).length > 0) {
        zeilen.push("Deine Stimme zählt nicht: Du hast schon einem anderen Antrag zugestimmt.");
      } else if (effect.same === true) {
        zeilen.push("Deine Stimme zählt einmal: Du hast schon so abgestimmt.");
      } else {
        zeilen.push("Deine Stimme zählt nicht.");
      }
    }
  } else if (art === "propose") {
    zeilen.push(`Angenommen ist der Antrag mit ${effect.needed} von ${effect.n} Ja-Stimmen.`);
  } else if (art === "ratify") {
    // Ein Sachbeschluss lässt die Fassung stehen (D580 Beschluss 1, 04 §4.6).
    if (felder.sachantrag === true) {
      zeilen.push(`Der Beschluss gilt. Die Satzung bleibt in der ${effect.epoch}. Fassung; niemand muss neu bestätigen.`);
    } else {
      zeilen.push(`${fassungSatz(effect.epoch)} Alle müssen die neue Satzung bestätigen.`);
    }
  } else if (art === "accept-rules") {
    // In der Gründung die zwei Zeilen aus fehlen und alle (D651 Beschluss 5).
    if (felder.geltend === true && effect.membership === "MEMBER" && felder.gruendung) {
      const fehlen = felder.gruendung.fehlen;
      if (fehlen.length === 0) zeilen.push("Der Verein besteht.");
      else if (fehlen.length === 1) {
        zeilen.push(`Der Verein besteht, sobald auch ${fehlen[0]} bestätigt hat.`);
      } else {
        zeilen.push(`Der Verein besteht, sobald auch ${aufzaehlung(fehlen)} bestätigt haben.`);
      }
      zeilen.push(
        `Für immer fest steht, wer gegründet hat: ${aufzaehlung(felder.gruendung.alle)}. ` +
          "Satzung und Mitgliederliste ändert ihr später per Abstimmung.",
      );
    } else if (felder.geltend === true && effect.membership === "MEMBER") {
      zeilen.push("Du bist Mitglied.");
    } else if (felder.geltend === true && effect.membership === "APPLICANT") {
      zeilen.push("Du hast die Satzung bestätigt, stehst aber nicht auf der Mitgliederliste.");
    } else {
      zeilen.push("Deine Mitgliedschaft ändert sich nicht.");
    }
  } else if (art === "vouch") {
    zeilen.push(`Du hast ${effect.used} von ${effect.D} Punkten vergeben.`);
    if (effect.used > effect.D) zeilen.push("Dann zählt keine deiner Bürgschaften mehr.");
  } else if (art === "obligation") {
    if (effect.settlement === "OPEN" && vorhanden(felder, "name")) {
      zeilen.push(`Der Beitrag ist offen, bis ${felder.name} quittiert.`);
    }
  } else if (art === "receipt") {
    if (effect.settlement === "SETTLED") zeilen.push("Der Beitrag ist bezahlt.");
  }
  if (zeilen.length > 0) zeilen[0] = `Danach: ${zeilen[0]}`;
  return zeilen;
}

// Unter der Folge, sobald andere gleichzeitig handeln können (D492 Beschluss 2, D490 Beschluss 2).
export const VORHERSAGE =
  "Das ist eine Vorhersage. Handelt jemand anderes gleichzeitig, kann es anders kommen.";

// Steht statt des Satzes, wenn die Seite ihn nicht bauen kann (D492 Beschluss 1).
export const KEIN_SATZ = "Die Seite kann nicht lesen, was du unterschreiben würdest.";

// Was die Frage vor dem Unterschreiben zeigt und ob sie Unterschreiben anbietet: ohne Satz
// keine Unterschrift (D492 Beschluss 1 und 5). CONFLICTING_APPROVAL mit konfliktWarnung
// (D556 Beschluss 2).
export function frageInhalt(art, felder, prepared) {
  const satz = absichtSatz(art, felder);
  const warnungen = (prepared.warnings ?? []).map((name) =>
    name === "CONFLICTING_APPROVAL" ? konfliktWarnung(prepared.effect, felder) : warnungInWorten(name),
  );
  if (satz === null) {
    return { satz: KEIN_SATZ, folge: [], warnungen, unterschreiben: false };
  }
  return { satz, folge: folgeZeilen(art, prepared.effect, felder), warnungen, unterschreiben: true };
}

// Der Satz der Meldung nach dem Eintragen (D492 Beschluss 5).
export function erfolgSatz(art, felder) {
  switch (art) {
    case "accept-rules":
      return "Deine Bestätigung der Satzung ist eingetragen.";
    case "propose":
      return vorhanden(felder, "titel")
        ? `Dein Antrag „${felder.titel}“ ist eingetragen.`
        : "Dein Antrag ist eingetragen.";
    case "vote":
      return felder.wahl === "no"
        ? "Deine Nein-Stimme ist eingetragen."
        : "Deine Ja-Stimme ist eingetragen.";
    case "ratify":
      return "Die Feststellung des Beschlusses ist eingetragen.";
    case "vouch":
      return vorhanden(felder, "name")
        ? `Deine Bürgschaft für ${felder.name} ist eingetragen.`
        : "Deine Bürgschaft ist eingetragen.";
    case "obligation":
      return "Deine Zusage, den Beitrag zu zahlen, ist eingetragen.";
    case "receipt":
      return "Deine Quittung ist eingetragen.";
    default:
      return "Eingetragen.";
  }
}

// Die Fassung der Satzung statt der Epoche (D494 Beschluss 5).
export function fassungSatz(index) {
  return `Es gilt die ${index}. Fassung der Satzung.`;
}

// Der Stand im Tab „Im Verein“, stand wie ScopeView.stand: die Fassung, die Zahl der angewandten
// Sachbeschlüsse und je Textfeld des Stands ein Satz (D580 Beschluss 1, D575 Beschluss 1, 04 §4.6).
export function standSaetze(index, stand) {
  const saetze = [fassungSatz(index)];
  const angewandt = stand?.applied?.length ?? 0;
  if (angewandt === 1) saetze.push("Dazu gilt 1 Sachbeschluss.");
  else if (angewandt > 1) saetze.push(`Dazu gelten ${angewandt} Sachbeschlüsse.`);
  for (const [feld, wert] of Object.entries(stand?.stand_obj ?? {})) {
    // vorlage bekommt keinen Satz; der Beitrag in Worten (D651 Beschluss 4).
    if (feld === "vorlage" || typeof wert !== "string") continue;
    const gezeigt = feld === "beitrag" ? beitragInWorten(wert) : wert;
    saetze.push(`Es gilt zu ${feld}: „${gezeigt}“`);
  }
  return saetze;
}

// Die Beschriftung eines Tabs: „ · <n> offen“ hinter dem Namen, wenn n nicht null ist; bei null
// nur der Name (D506 Beschluss 2 und 4).
export function tabTitel(name, offen) {
  return offen === 0 ? name : `${name} · ${offen} offen`;
}

// Ein Satz je Person im Vertrauen, aus dem Abstand zum Anker (D494 Beschluss 5, 02 §3).
export function vertrauenSatz(name, abstand) {
  if (abstand === null || abstand === undefined) return `${name} ist nicht verbürgt.`;
  if (abstand === 0) return `${name} ist Anker des Vereins.`;
  if (abstand === 1) return `${name} ist verbürgt, einen Schritt vom Anker entfernt.`;
  return `${name} ist verbürgt, ${abstand} Schritte vom Anker entfernt.`;
}

// Die Regie zeigt zuerst die eigene Identität, dann die übrigen nach Namen; wer keinen Namen
// hat, steht danach, nach Schlüssel (D494 Beschluss 5).
export function regieReihenfolge(personen, ich) {
  const eigene = personen.filter((person) => person.I === ich);
  const andere = personen.filter((person) => person.I !== ich);
  andere.sort((links, rechts) => {
    if (links.name && rechts.name) return links.name.localeCompare(rechts.name, "de");
    if (links.name) return -1;
    if (rechts.name) return 1;
    return links.I < rechts.I ? -1 : 1;
  });
  return [...eigene, ...andere];
}

// Die Geschichte der Demonstration: jeder Schritt mit der handelnden Person und ob er getan ist,
// aus den Sichten. Sie kennt die Personen des Szenarios bei ihren Namen; sie ist Werkzeug der
// Demonstration wie die Regie, keine Rechnung des Vereins (D494 Beschluss 3, D496 Beschluss 1,
// D509 Beschluss 1, D484 Beschluss 3).
//
// zustand: ich (eigener Schlüssel oder null), namen (Map Schlüssel → Name, aus /names),
// kanten (Kanten der Ableitung im Vereinsleben, je { author, subject }), antraege (aus
// /proposals), liste (participants der geltenden Epoche), satzung (constitution_obj der
// geltenden Epoche), mitgliedschaft (Zustand der eigenen Identität oder null), gabelungen
// (Autoren aus /forks), obligationen (aus /obligations, je { debtor, creditor, state }).
export function geschichte(zustand) {
  const { ich, namen, kanten, antraege, liste, satzung, mitgliedschaft, gabelungen, obligationen } = zustand;
  const schluesselVon = (name) => {
    for (const [schluessel, eintrag] of namen) if (eintrag === name) return schluessel;
    return null;
  };
  const anna = schluesselVon("ANNA");
  const bruno = schluesselVon("BRUNO");
  const chris = schluesselVon("CHRIS");
  const dora = schluesselVon("DORA");
  const kasse = schluesselVon("KASSE");
  const aufgenommen = ich !== null && liste.includes(ich);
  const aufnahme = antraege.find(
    (antrag) => ich !== null && antrag.proposers.includes(anna) && antrag.changes.added.includes(ich),
  );
  const stimmende = [anna, chris, dora];
  const nochNicht = stimmende.filter((person) => !aufnahme || !aufnahme.yes.includes(person));
  // Ein Antrag ANNAs, der ein Textfeld setzt, oder ein Textfeld der geltenden Satzung, gleich
  // welches (D496 Beschluss 1).
  const textBeantragt = antraege.some(
    (antrag) =>
      antrag.proposers.includes(anna) && antrag.changes.fields.some((feld) => typeof feld.new === "string"),
  );
  const textInSatzung = Object.values(satzung ?? {}).some((wert) => typeof wert === "string");
  // „Du sagst der KASSE deinen Beitrag zu“, getan, „sobald eine Obligation mit dir als Schuldner
  // und der KASSE als Gläubiger besteht, gleich mit welchem Betrag“; „Die KASSE quittiert“,
  // getan, „sobald eine solche Obligation im Stand SETTLED steht“ (D509 Beschluss 1).
  const beitraege = obligationen.filter(
    (schuld) => ich !== null && kasse !== null && schuld.debtor === ich && schuld.creditor === kasse,
  );

  const schritte = [
    {
      text: "Du trägst deinen Namen ein",
      person: ich,
      eigene: true,
      getan: ich !== null && Boolean(namen.get(ich)),
    },
    {
      text: "CHRIS bürgt für dich",
      person: chris,
      getan: ich !== null && kanten.some((kante) => kante.author === chris && kante.subject === ich),
    },
    { text: "ANNA beantragt deine Aufnahme", person: anna, getan: aufgenommen || Boolean(aufnahme) },
    {
      text: "ANNA, CHRIS und DORA stimmen Ja",
      person: nochNicht[0] ?? anna,
      getan: aufgenommen || (Boolean(aufnahme) && nochNicht.length === 0),
    },
    { text: "ANNA stellt den Beschluss fest", person: anna, getan: aufgenommen },
    { text: "Du bestätigst die Satzung", person: ich, eigene: true, getan: mitgliedschaft === "MEMBER" },
    {
      text: "ANNA beantragt einen Satzungstext, etwa den Beitrag",
      person: anna,
      getan: textBeantragt || textInSatzung,
    },
    {
      text: "BRUNO widerspricht sich, im Terminal mit python -m tools.verein_gabel",
      person: bruno,
      getan: bruno !== null && gabelungen.includes(bruno),
    },
    {
      text: "Du sagst der KASSE deinen Beitrag zu",
      person: ich,
      eigene: true,
      getan: beitraege.length > 0,
    },
    {
      text: "Die KASSE quittiert",
      person: kasse,
      getan: beitraege.some((schuld) => schuld.state === "SETTLED"),
    },
  ];
  const erster = schritte.findIndex((schritt) => !schritt.getan);
  return schritte.map((schritt, index) => ({
    eigene: false,
    ...schritt,
    name: schritt.person === null ? null : namen.get(schritt.person) ?? null,
    weiter: index === erster,
  }));
}
