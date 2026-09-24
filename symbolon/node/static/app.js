// Seite: Schlüssel anlegen und die Satzung bestätigen (D479 Beschluss 6, D481 Beschluss 3 und 4).

import {
  ablauf,
  genesisAnchor,
  lesen,
  schluesselAnlegen,
  spitzeBestaetigen,
} from "./geraet.js";

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

function hex(bytes) {
  return [...bytes].map((byte) => byte.toString(16).padStart(2, "0")).join("");
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

function knopf(text, tun) {
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = text;
  button.addEventListener("click", tun);
  return button;
}

async function namenFuer(pub) {
  const antwort = await fetch("/names");
  const rows = await antwort.json();
  const found = rows.find((row) => row.I === hex(pub));
  return found ? found.name : "";
}

async function vereinScope() {
  const scopes = await (await fetch("/scopes")).json();
  for (const scope of scopes) {
    const view = await (await fetch(`/scopes/${scope}`)).json();
    if (view.verein) return scope;
  }
  return null;
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

function meldung(name) {
  return zeile(name);
}

async function zeichnen() {
  const seite = document.querySelector("#seite");
  seite.replaceChildren();
  const record = await lesen();
  if (!record) {
    const field = document.createElement("input");
    field.type = "text";
    field.maxLength = 64;
    const label = document.createElement("label");
    label.append(document.createTextNode("Name "), field);
    seite.append(
      label,
      knopf("Schlüssel anlegen", async () => {
        const pub = await schluesselAnlegen(crypto.subtle);
        try {
          await senden("/names", { I: hex(pub), name: field.value });
        } catch (error) {
          seite.append(meldung(error.antwort ? error.name : "keine Antwort"));
          return;
        }
        await zeichnen();
      }),
    );
    return;
  }
  const name = await namenFuer(record.pub);
  seite.append(zeile(`${name} ${kurz(hex(record.pub))}`));
  seite.append(knopf("Satzung des Vereins bestätigen", () => satzung(seite, record.pub)));
}

async function satzung(seite, pub) {
  let scope;
  try {
    scope = await vereinScope();
  } catch (error) {
    seite.append(meldung(error.antwort ? error.name : "keine Antwort"));
    return;
  }
  if (!scope) {
    seite.append(meldung("Kein Verein"));
    return;
  }
  let ergebnis;
  try {
    ergebnis = await ablauf(crypto.subtle, {
      absicht: (tip) => {
        const payload = { art: "accept-rules", scope, I: hex(pub) };
        if (tip) payload.h_prev = hex(tip);
        return senden("/intent", payload);
      },
      zeigen: async (prepared) => {
        const anfang = hex(await genesisAnchor(pub, crypto.subtle));
        seite.append(zeile("Art: Satzung annehmen"));
        seite.append(zeile(`Scope: ${kurz(scope)}`));
        const vorgaenger = prepared.h_prev === anfang ? "der Anfang" : kurz(prepared.h_prev);
        seite.append(zeile(`Vorgänger: ${vorgaenger}`));
        seite.append(zeile(`Zeit: ${zeitInWorten(prepared.t)}`));
        return new Promise((resolve) => {
          seite.append(knopf("Unterschreiben", () => resolve(true)));
        });
      },
      einliefern: (core, signature) => senden("/submit", { core, sigma: hex(signature) }),
    });
  } catch (error) {
    seite.append(meldung(error.antwort ? error.name : "keine Antwort"));
    return;
  }
  if (!ergebnis) return;
  if (ergebnis.name) seite.append(meldung(ergebnis.name));
  if (ergebnis.anfang) {
    seite.append(zeile(`Anfang: ${kurz(hex(ergebnis.anfang))}`));
    seite.append(
      knopf("Anfang bestätigen", async () => {
        await spitzeBestaetigen(ergebnis.anfang);
        await satzung(seite, pub);
      }),
    );
  }
  if (ergebnis.halt) {
    seite.append(zeile(`Spitze: ${kurz(hex(ergebnis.halt))}`));
    seite.append(
      knopf("Diese Spitze bestätigen", async () => {
        await spitzeBestaetigen(ergebnis.halt);
      }),
    );
  }
  if (ergebnis.schwebend) seite.append(zeile("Wartet auf Antwort"));
  if (ergebnis.abweichung) seite.append(zeile("Die Kennung weicht ab"));
  if (ergebnis.ok) seite.append(zeile("Eingetragen"));
}

void zeichnen();
