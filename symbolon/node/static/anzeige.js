// Anzeige: reine Funktionen ohne DOM, navigator und IndexedDB (D486 Beschluss 5).
// Was aus den Antworten des S-Node Worte macht: der Stand eines Antrags, die Änderungen einer
// Satzung, ein Betrag, die Zeilen der Kasse und die Wörter für Zustände, Warnungen und
// Abweisungen. Ein unbekannter Warnungs- oder Abweisungsname erscheint wörtlich (D486 Beschluss 3).
// Dazu die Titel der Anträge und die Sätze der Absicht, der Folge und der Meldung
// (D492 Beschluss 1 bis 3 und 5), die Wörter aus D494 Beschluss 5, die Geschichte der
// Demonstration (D494 Beschluss 3, D496 Beschluss 1, D509 Beschluss 1), Zeit relativ zur Uhr
// des S-Node (D496 Beschluss 2), die Beschriftung eines Tabs (D506 Beschluss 2 und 4), ob ein
// Widerspruch oben steht und was seine Karte sagt (D525 Beschluss 1 bis 3, D507 Beschluss 1).

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

// Der neue Wortlaut jedes Textfelds, als Zitat unter dem Titel (D492 Beschluss 3).
export function antragZitate(changes) {
  return changes.fields
    .filter((feld) => typeof feld.new === "string")
    .map((feld) => `„${feld.new}“`);
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

function vorhanden(felder, ...namen) {
  return namen.every((name) => felder[name] !== null && felder[name] !== undefined && felder[name] !== "");
}

// Der Satz der Absicht je Art; fehlt ein nötiger Wert, null (D492 Beschluss 1 und 2).
export function absichtSatz(art, felder) {
  switch (art) {
    case "accept-rules":
      if (typeof felder.geltend !== "boolean") return null;
      return felder.geltend
        ? "Du bestätigst die geltende Satzung des Vereins."
        : "Du bestätigst eine frühere Fassung der Satzung.";
    case "propose":
      if (!vorhanden(felder, "titel")) return null;
      return `Du beantragst: ${felder.titel}.`;
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

// Die Folge aus effect, „Danach:“ vor der ersten Zeile; ohne effect keine Zeile
// (D492 Beschluss 2, D490 Beschluss 2).
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
    if (effect.counts === false) {
      zeilen.push(
        felder.teilnehmer === false
          ? "Deine Stimme zählt nicht: Du stehst nicht auf der Mitgliederliste."
          : "Deine Stimme zählt nicht: Du hast schon abgestimmt. Auch deine erste Stimme zählt dann nicht mehr.",
      );
    }
  } else if (art === "propose") {
    zeilen.push(`Angenommen ist der Antrag mit ${effect.needed} von ${effect.n} Ja-Stimmen.`);
  } else if (art === "ratify") {
    zeilen.push(`${fassungSatz(effect.epoch)} Alle müssen die neue Satzung bestätigen.`);
  } else if (art === "accept-rules") {
    if (felder.geltend === true && effect.membership === "MEMBER") {
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
// keine Unterschrift (D492 Beschluss 1 und 5).
export function frageInhalt(art, felder, prepared) {
  const satz = absichtSatz(art, felder);
  const warnungen = (prepared.warnings ?? []).map(warnungInWorten);
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
