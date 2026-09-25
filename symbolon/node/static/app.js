// Seite: eine Seite, drei Lesepfade, sieben Abschnitte (D486 Beschluss 2 bis 4, D479 Beschluss 2
// bis 6, D482 Beschluss 3 bis 5, D471 Beschluss 3, D481 Beschluss 5).

import {
  ablauf,
  artInWorten,
  genesisAnchor,
  lesen,
  pruefen,
  schluesselAnlegen,
  spitzeBestaetigen,
} from "./geraet.js";
import {
  aenderungen,
  auszaehlungInWorten,
  abweisungInWorten,
  betrag,
  kassenZeilen,
  mitgliedschaftInWorten,
  nameVon,
  standZeile,
  tilgungInWorten,
  warnungInWorten,
} from "./anzeige.js";

const MONATE = [
  "Januar",
  "Februar",
  "März",
  "April",
  "Mai",
  "Juni",
  "Juli",
  "August",
  "September",
  "Oktober",
  "November",
  "Dezember",
];

let handelnAls = "geraet";

function hex(bytes) {
  return [...bytes].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

function bytesFromHex(text) {
  const out = new Uint8Array(text.length / 2);
  for (let index = 0; index < out.length; index += 1) {
    out[index] = Number.parseInt(text.slice(index * 2, index * 2 + 2), 16);
  }
  return out;
}

function kurz(text) {
  if (text.length <= 12) return text;
  return `${text.slice(0, 6)}…${text.slice(-6)}`;
}

function zeitInWorten(seconds) {
  const moment = new Date(Number(seconds) * 1000);
  const stunde = String(moment.getHours()).padStart(2, "0");
  const minute = String(moment.getMinutes()).padStart(2, "0");
  const monat = MONATE[moment.getMonth()];
  return `${moment.getDate()}. ${monat} ${moment.getFullYear()}, ${stunde}:${minute} Uhr`;
}

function zeile(text) {
  const node = document.createElement("p");
  node.textContent = text;
  return node;
}

function ueberschrift(text) {
  const node = document.createElement("h2");
  node.textContent = text;
  return node;
}

function knopf(text, tun) {
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = text;
  button.addEventListener("click", tun);
  return button;
}

async function holen(path) {
  let antwort;
  try {
    antwort = await fetch(path);
  } catch (error) {
    error.netz = true;
    throw error;
  }
  const body = await antwort.json();
  if (!antwort.ok) {
    const error = new Error(typeof body === "string" ? body : "FEHLER");
    error.antwort = true;
    error.name = typeof body === "string" ? body : "FEHLER";
    throw error;
  }
  return body;
}

async function senden(path, payload) {
  let antwort;
  try {
    antwort = await fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  } catch (error) {
    error.netz = true;
    throw error;
  }
  const body = await antwort.json();
  if (!antwort.ok) {
    const error = new Error(typeof body === "string" ? body : "FEHLER");
    error.antwort = true;
    error.name = typeof body === "string" ? body : "FEHLER";
    throw error;
  }
  return body;
}

function meldungKnoten() {
  return document.querySelector("#meldung");
}

// Das Ergebnis einer Handlung überlebt das Neuzeichnen danach nur, wenn es dort gelesen
// wird: zeichnen() liest und löscht sie einmal (D486 Beschluss 2, D483 zweite Rückfrage).
let letzteMeldung = null;

function meldung(text) {
  letzteMeldung = text;
}

// Kern und Warnungen anzeigen, Unterschreiben oder Abbrechen (D486 Beschluss 2 und 3,
// D471 Beschluss 2).
async function vorschau(kern, warnungen, autorPub) {
  const dialog = document.querySelector("#dialog");
  const anker = hex(await genesisAnchor(autorPub, crypto.subtle));
  dialog.replaceChildren();
  dialog.append(zeile(`Art: ${artInWorten(kern.get(3n))}`));
  const scope = kern.get(5n);
  if (scope) dialog.append(zeile(`Scope: ${kurz(hex(scope))}`));
  const vorher = hex(kern.get(8n));
  dialog.append(zeile(`Vorgänger: ${vorher === anker ? "der Anfang" : kurz(vorher)}`));
  dialog.append(zeile(`Zeit: ${zeitInWorten(kern.get(6n))}`));
  for (const warnung of warnungen) dialog.append(zeile(warnungInWorten(warnung)));
  dialog.hidden = false;
  return new Promise((resolve) => {
    dialog.append(
      knopf("Unterschreiben", () => {
        dialog.hidden = true;
        resolve(true);
      }),
      knopf("Abbrechen", () => {
        dialog.hidden = true;
        resolve(false);
      }),
    );
  });
}

// Eine Handlung über das Gerät oder über eine simulierte Person, zwei Schritte bei der
// simulierten (D486 Beschluss 3, D479 Beschluss 2).
function handelnFabrik(record) {
  return async function handeln(art, felder) {
    try {
      if (handelnAls === "geraet") {
        const ergebnis = await ablauf(crypto.subtle, {
          absicht: (tip) => {
            const payload = { art, I: hex(record.pub), ...felder };
            if (tip) payload.h_prev = hex(tip);
            return senden("/intent", payload);
          },
          zeigen: (kern, warnungen) => vorschau(kern, warnungen, record.pub),
          einliefern: (core, signature) => senden("/submit", { core, sigma: hex(signature) }),
        });
        if (ergebnis.name) meldung(abweisungInWorten(ergebnis.name));
        else if (ergebnis.schwebend) meldung("Wartet auf Antwort");
        else if (ergebnis.ok) meldung("Eingetragen");
        else if (ergebnis.abbruch) meldung("Abgebrochen");
        if (ergebnis.halt) {
          meldungKnoten().replaceChildren(
            zeile(`Spitze: ${kurz(hex(ergebnis.halt))}`),
            knopf("Diese Spitze bestätigen", async () => {
              await spitzeBestaetigen(ergebnis.halt);
              await zeichnen();
            }),
          );
          return;
        }
      } else {
        const pub = handelnAls;
        const vorbereitet = await senden("/intent", { I: pub, art, ...felder });
        const geprueft = pruefen(
          bytesFromHex(vorbereitet.core),
          bytesFromHex(pub),
          bytesFromHex(vorbereitet.h_prev),
        );
        const weiter = await vorschau(geprueft.kern, vorbereitet.warnings, bytesFromHex(pub));
        if (weiter) {
          await senden("/sim/intent", { I: pub, art, ...felder });
          meldung("Eingetragen");
        } else {
          meldung("Abgebrochen");
        }
      }
    } catch (error) {
      meldung(error.antwort ? abweisungInWorten(error.name) : "keine Antwort");
    }
    await zeichnen();
  };
}

function kopf(namen, simuliert) {
  const abschnitt = document.createElement("section");
  const auswahl = document.createElement("select");
  const ich = document.createElement("option");
  ich.value = "geraet";
  ich.textContent = "Ich";
  auswahl.append(ich);
  for (const eintrag of simuliert) {
    const option = document.createElement("option");
    option.value = eintrag.I;
    option.textContent = eintrag.name ?? kurz(eintrag.I);
    auswahl.append(option);
  }
  auswahl.value = handelnAls;
  auswahl.addEventListener("change", () => {
    handelnAls = auswahl.value;
    void zeichnen();
  });
  const label = document.createElement("label");
  label.append(document.createTextNode("Handeln als "), auswahl);
  abschnitt.append(label, knopf("Aktualisieren", () => void zeichnen()));
  return abschnitt;
}

function anlegenFormular() {
  const abschnitt = document.createElement("section");
  const field = document.createElement("input");
  field.type = "text";
  field.maxLength = 64;
  const label = document.createElement("label");
  label.append(document.createTextNode("Name "), field);
  abschnitt.append(
    label,
    knopf("Schlüssel anlegen", async () => {
      const gewaehlt = field.value.trim();
      if (!gewaehlt) {
        meldung("Ein Name fehlt");
        return;
      }
      const pub = await schluesselAnlegen(crypto.subtle);
      try {
        await senden("/names", { I: hex(pub), name: gewaehlt });
      } catch (error) {
        meldung(error.antwort ? error.name : "keine Antwort");
        return;
      }
      await zeichnen();
    }),
  );
  return abschnitt;
}

function aufgabenAbschnitt(tasks, handeln) {
  const abschnitt = document.createElement("section");
  abschnitt.append(ueberschrift("Aufgaben"));
  if (tasks.length === 0) abschnitt.append(zeile("Keine Aufgaben."));
  for (const aufgabe of tasks) {
    const zeileEl = document.createElement("p");
    zeileEl.append(document.createTextNode(`${kurz(aufgabe.scope)}: `));
    if (aufgabe.art === "CONFIRM_RULES") {
      zeileEl.append(
        document.createTextNode("Die Satzung hat sich geändert. "),
        knopf("Satzung bestätigen", () =>
          handeln("accept-rules", { scope: aufgabe.scope, constitution: aufgabe.constitution }),
        ),
      );
    } else if (aufgabe.art === "VOTE") {
      zeileEl.append(
        document.createTextNode("Abstimmen. "),
        knopf("Ja", () => handeln("vote", { proposal: aufgabe.proposal, choice: "yes" })),
        knopf("Nein", () => handeln("vote", { proposal: aufgabe.proposal, choice: "no" })),
      );
    } else if (aufgabe.art === "RATIFY") {
      zeileEl.append(
        document.createTextNode("Angenommen. "),
        knopf("Beschluss feststellen", () => handeln("ratify", { proposal: aufgabe.proposal })),
      );
    } else if (aufgabe.art === "CONTRIBUTION_OPEN") {
      zeileEl.append(document.createTextNode("Dein Beitrag ist offen."));
    } else if (aufgabe.art === "RECEIPT") {
      zeileEl.append(
        document.createTextNode("Eine Zahlung wartet. "),
        knopf("Quittieren", () => handeln("receipt", { obligation: aufgabe.obligation })),
      );
    }
    abschnitt.append(zeileEl);
  }
  return abschnitt;
}

function vereinAbschnitt(view, namen) {
  const abschnitt = document.createElement("section");
  abschnitt.append(ueberschrift("Verein"));
  if (view === null) {
    abschnitt.append(zeile("Kein Verein."));
    return abschnitt;
  }
  abschnitt.append(zeile(`Epoche ${view.state.epoch.index}`));
  const liste = document.createElement("ul");
  for (const [subject, ergebnis] of view.verein.membership) {
    const item = document.createElement("li");
    item.textContent = `${nameVon(namen, subject)}: ${mitgliedschaftInWorten(ergebnis.state)}`;
    liste.append(item);
  }
  abschnitt.append(liste);
  const konstitution = view.state.constitution_obj ?? {};
  for (const [feld, wert] of Object.entries(konstitution)) {
    if (typeof wert === "string") abschnitt.append(zeile(`${feld}: ${wert}`));
  }
  return abschnitt;
}

function neuerAntragFormular(gov, view, namenListe, namen, handeln) {
  const form = document.createElement("div");
  const teilnehmer = new Set(view?.state?.constitution_obj?.participants ?? []);

  const aufnehmenAuswahl = document.createElement("select");
  for (const eintrag of namenListe) {
    if (teilnehmer.has(eintrag.I)) continue;
    const option = document.createElement("option");
    option.value = eintrag.I;
    option.textContent = eintrag.name ?? kurz(eintrag.I);
    aufnehmenAuswahl.append(option);
  }
  form.append(
    aufnehmenAuswahl,
    knopf("Aufnehmen", () =>
      handeln("propose", { scope: gov, change: { add: aufnehmenAuswahl.value } }),
    ),
  );

  const ausschliessenAuswahl = document.createElement("select");
  for (const schluessel of teilnehmer) {
    const option = document.createElement("option");
    option.value = schluessel;
    option.textContent = nameVon(namen, schluessel);
    ausschliessenAuswahl.append(option);
  }
  form.append(
    ausschliessenAuswahl,
    knopf("Ausschließen", () =>
      handeln("propose", { scope: gov, change: { remove: ausschliessenAuswahl.value } }),
    ),
  );

  const feldName = document.createElement("input");
  feldName.placeholder = "Feld";
  const feldText = document.createElement("input");
  feldText.placeholder = "Text";
  form.append(
    feldName,
    feldText,
    knopf("Setzen", () =>
      handeln("propose", {
        scope: gov,
        change: { set: { field: feldName.value, text: feldText.value } },
      }),
    ),
  );
  return form;
}

function antraegeAbschnitt(antraege, gov, view, namenListe, namen, handeln) {
  const abschnitt = document.createElement("section");
  abschnitt.append(ueberschrift("Anträge"));
  if (gov === null) {
    abschnitt.append(zeile("Kein Verein."));
    return abschnitt;
  }
  for (const antrag of antraege) {
    const karte = document.createElement("div");
    karte.append(zeile(`Antrag ${kurz(antrag.proposal)}`));
    karte.append(
      zeile(
        `Eingebracht von ${antrag.proposers.map((p) => nameVon(namen, p)).join(", ")}`,
      ),
    );
    karte.append(zeile(auszaehlungInWorten(antrag.state)));
    karte.append(zeile(standZeile(antrag)));
    for (const text of aenderungen(antrag.changes, namen)) karte.append(zeile(text));
    if (antrag.state === "PENDING") {
      karte.append(
        knopf("Ja", () => handeln("vote", { proposal: antrag.proposal, choice: "yes" })),
        knopf("Nein", () => handeln("vote", { proposal: antrag.proposal, choice: "no" })),
      );
    }
    if (antrag.state === "PASSED") {
      karte.append(
        knopf("Beschluss feststellen", () => handeln("ratify", { proposal: antrag.proposal })),
      );
    }
    abschnitt.append(karte);
  }
  abschnitt.append(neuerAntragFormular(gov, view, namenListe, namen, handeln));
  return abschnitt;
}

function vertrauenAbschnitt(view, res, namenListe, namen, jetzt, handeln) {
  const abschnitt = document.createElement("section");
  abschnitt.append(ueberschrift("Vertrauen"));
  if (res === null || !view.vereinsleben) {
    abschnitt.append(zeile("Kein Vereinsleben."));
    return abschnitt;
  }
  const bfs = view.vereinsleben.derivation.bfs;
  const tabelle = document.createElement("table");
  const kopfzeile = document.createElement("tr");
  for (const text of ["Name", "Abstand", "Gewicht"]) {
    const zelle = document.createElement("th");
    zelle.textContent = text;
    kopfzeile.append(zelle);
  }
  tabelle.append(kopfzeile);
  for (const schluessel of Object.keys(bfs.distance).sort()) {
    const reihe = document.createElement("tr");
    for (const wert of [
      nameVon(namen, schluessel),
      bfs.distance[schluessel],
      bfs.node_capacity[schluessel],
    ]) {
      const zelle = document.createElement("td");
      zelle.textContent = wert;
      reihe.append(zelle);
    }
    tabelle.append(reihe);
  }
  abschnitt.append(tabelle);

  const personAuswahl = document.createElement("select");
  for (const eintrag of namenListe) {
    const option = document.createElement("option");
    option.value = eintrag.I;
    option.textContent = eintrag.name ?? kurz(eintrag.I);
    personAuswahl.append(option);
  }
  const gewichtFeld = document.createElement("input");
  gewichtFeld.type = "number";
  gewichtFeld.min = "1";
  gewichtFeld.value = "1";
  const tageFeld = document.createElement("input");
  tageFeld.type = "number";
  tageFeld.min = "1";
  tageFeld.value = "365";
  abschnitt.append(
    document.createElement("hr"),
    personAuswahl,
    gewichtFeld,
    tageFeld,
    knopf("Bürgen", () =>
      handeln("vouch", {
        scope: res,
        subject: personAuswahl.value,
        n: Number(gewichtFeld.value),
        t_exp: jetzt + Number(tageFeld.value) * 86400,
      }),
    ),
  );
  return abschnitt;
}

function beitraegeAbschnitt(obligationen, res, namenListe, namen, handeln) {
  const abschnitt = document.createElement("section");
  abschnitt.append(ueberschrift("Beiträge"));
  if (res === null) {
    abschnitt.append(zeile("Kein Vereinsleben."));
    return abschnitt;
  }
  for (const o of obligationen) {
    const glaeubiger = o.creditor === null ? "–" : nameVon(namen, o.creditor);
    abschnitt.append(
      zeile(
        `${nameVon(namen, o.debtor)} an ${glaeubiger}: ${betrag(o.amount, o.unit)} — ` +
          tilgungInWorten(o.state),
      ),
    );
  }
  const glaeubigerAuswahl = document.createElement("select");
  for (const eintrag of namenListe) {
    const option = document.createElement("option");
    option.value = eintrag.I;
    option.textContent = eintrag.name ?? kurz(eintrag.I);
    glaeubigerAuswahl.append(option);
  }
  const euroFeld = document.createElement("input");
  euroFeld.type = "number";
  euroFeld.min = "0";
  euroFeld.step = "0.01";
  abschnitt.append(
    document.createElement("hr"),
    glaeubigerAuswahl,
    euroFeld,
    knopf("Beitrag unterschreiben", () =>
      handeln("obligation", {
        scope: res,
        creditor: glaeubigerAuswahl.value,
        amount: Math.round(Number(euroFeld.value) * 100),
        unit: "EUR-Cent",
      }),
    ),
  );
  return abschnitt;
}

function kasseAbschnitt(view, obligationen, namenListe, namen, handeln) {
  const abschnitt = document.createElement("section");
  abschnitt.append(ueberschrift("Kasse"));
  const auswahl = document.createElement("select");
  for (const eintrag of namenListe) {
    const option = document.createElement("option");
    option.value = eintrag.I;
    option.textContent = eintrag.name ?? kurz(eintrag.I);
    if (eintrag.name === "KASSE") option.selected = true;
    auswahl.append(option);
  }
  abschnitt.append(auswahl);
  const teilnehmer = view?.state?.constitution_obj?.participants ?? [];
  const liste = document.createElement("ul");
  const zeichneListe = () => {
    liste.replaceChildren();
    for (const eintrag of kassenZeilen(teilnehmer, obligationen, auswahl.value)) {
      const item = document.createElement("li");
      item.append(
        document.createTextNode(`${nameVon(namen, eintrag.teilnehmer)}: ${eintrag.zustand}`),
      );
      const offene = eintrag.obligationen.find((o) => o.state === "OPEN");
      if (offene && handelnAls === auswahl.value) {
        item.append(
          document.createTextNode(" "),
          knopf("Quittieren", () => handeln("receipt", { obligation: offene.claim_id })),
        );
      }
      liste.append(item);
    }
  };
  auswahl.addEventListener("change", zeichneListe);
  zeichneListe();
  abschnitt.append(liste);
  return abschnitt;
}

async function widersprueAbschnitt(forks, namen) {
  const abschnitt = document.createElement("section");
  abschnitt.append(ueberschrift("Widersprüche"));
  if (forks.length === 0) abschnitt.append(zeile("Keine Widersprüche."));
  for (const gruppe of forks) {
    const name = nameVon(namen, gruppe.I);
    abschnitt.append(zeile(`Dieselbe Stelle in ${name}s Kette:`));
    const reihe = document.createElement("div");
    for (const [cid] of gruppe.claims) {
      const claim = await holen(`/claims/${cid}`);
      const karte = document.createElement("div");
      karte.append(
        zeile(`Art: ${artInWorten(claim.p)}`),
        zeile(`Zeit: ${zeitInWorten(claim.t)}`),
        zeile(`Wert: ${claim.value === null ? "–" : JSON.stringify(claim.value)}`),
      );
      reihe.append(karte);
    }
    abschnitt.append(reihe);
  }
  return abschnitt;
}

function findeScope(sichten, teil) {
  for (const [scope, view] of sichten) {
    if (view[teil]) return scope;
  }
  return null;
}

async function zeichnen() {
  const seite = document.querySelector("#seite");
  seite.replaceChildren();
  document.querySelector("#dialog").hidden = true;
  meldungKnoten().replaceChildren();
  if (letzteMeldung) {
    meldungKnoten().append(zeile(letzteMeldung));
    letzteMeldung = null;
  }

  const namenListe = await holen("/names");
  const namen = new Map(namenListe.map((eintrag) => [eintrag.I, eintrag.name]));
  const simuliert = namenListe.filter((eintrag) => eintrag.simulated);

  seite.append(kopf(namen, simuliert));

  const record = await lesen();
  if (handelnAls === "geraet" && !record) {
    seite.append(anlegenFormular());
    return;
  }

  const scopes = await holen("/scopes");
  const sichten = new Map();
  for (const scope of scopes) sichten.set(scope, await holen(`/scopes/${scope}`));
  const gov = findeScope(sichten, "verein");
  const res = findeScope(sichten, "vereinsleben");

  const jetzt = await holen("/now");
  const handelndeIdentitaet = handelnAls === "geraet" ? hex(record.pub) : handelnAls;
  const tasks = await holen(`/tasks/${handelndeIdentitaet}`);
  const antraege = gov === null ? [] : await holen(`/proposals/${gov}`);
  const obligationen = res === null ? [] : await holen(`/obligations/${res}`);
  const forks = await holen("/forks");

  const handeln = handelnFabrik(record);

  seite.append(aufgabenAbschnitt(tasks, handeln));
  seite.append(vereinAbschnitt(gov === null ? null : sichten.get(gov), namen));
  seite.append(
    antraegeAbschnitt(antraege, gov, gov === null ? null : sichten.get(gov), namenListe, namen, handeln),
  );
  seite.append(
    vertrauenAbschnitt(res === null ? null : sichten.get(res), res, namenListe, namen, jetzt, handeln),
  );
  seite.append(beitraegeAbschnitt(obligationen, res, namenListe, namen, handeln));
  seite.append(
    kasseAbschnitt(gov === null ? null : sichten.get(gov), obligationen, namenListe, namen, handeln),
  );
  seite.append(await widersprueAbschnitt(forks, namen));
}

void zeichnen();
