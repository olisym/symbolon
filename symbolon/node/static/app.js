// Seite nach dem Klickmodell: links oben fest die Person, was ansteht und Widersprüche,
// darunter fünf Tabs mit dem Verein in Sätzen und den Abschnitten; rechts die Regie mit der
// Geschichte (D507 Beschluss 1 und 2, D506 Beschluss 1 und 2, D496 Beschluss 1 bis 3, D494 Beschluss 1 bis 6, D492 Beschluss 1 bis 5, D490 Beschluss 1 und 3, D489 Beschluss 3,
// D487 Beschluss 1 und 2, D482 Beschluss 3 bis 5, D481 Beschluss 3 und 5, D479 Beschluss 6).

import {
  ablauf,
  artInWorten,
  dekodierenV,
  genesisAnchor,
  lesen,
  pruefen,
  schluesselAnlegen,
  spitzeBestaetigen,
} from "./geraet.js";
import {
  VORHERSAGE,
  abweisungInWorten,
  aenderungen,
  antragTitel,
  antragZitate,
  auszaehlungInWorten,
  betrag,
  centAus,
  erfolgSatz,
  fassungSatz,
  frageInhalt,
  ganzeZahl,
  geschichte,
  hinweisSatzungGeaendert,
  kassenZeilen,
  mitgliedschaftInWorten,
  nameVon,
  personImSatz,
  regieReihenfolge,
  standZeile,
  tabTitel,
  tageAusKern,
  tilgungInWorten,
  verfassungsAenderungen,
  vertrauenSatz,
  wertInWorten,
  widerspruchOben,
  zeitpunktInWorten,
} from "./anzeige.js";


let handelnAls = "geraet";

// Der gewählte Tab überdauert ein Zeichnen, nicht ein Neuladen; beim ersten Laden „Im Verein“
// (D506 Beschluss 2).
let gewaehlterTab = "Im Verein";

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

function element(tag, klasse, text) {
  const node = document.createElement(tag);
  if (klasse) node.className = klasse;
  if (text !== undefined) node.textContent = text;
  return node;
}

function zeile(text, klasse) {
  return element("p", klasse, text);
}

function marke(text) {
  return element("div", "marke", text);
}

function knopf(text, tun, klasse = "neben") {
  const button = element("button", klasse, text);
  button.type = "button";
  button.addEventListener("click", tun);
  return button;
}

function knopfReihe(...knoepfe) {
  const reihe = element("div", "knoepfe");
  reihe.append(...knoepfe);
  return reihe;
}

// Kennungen nur hinter „Einzelheiten“ (D492 Beschluss 5).
function einzelheiten(zeilen) {
  const details = element("details", "einzelheiten");
  details.append(element("summary", null, "Einzelheiten"));
  for (const text of zeilen) details.append(zeile(text));
  return details;
}

function liste(texte) {
  const ul = element("ul");
  for (const text of texte) ul.append(element("li", null, text));
  return ul;
}

function aufzaehlung(namen) {
  if (namen.length === 0) return "niemand";
  if (namen.length === 1) return namen[0];
  return `${namen.slice(0, -1).join(", ")} und ${namen[namen.length - 1]}`;
}

async function antwortLesen(antwort) {
  const body = await antwort.json();
  if (!antwort.ok) {
    const error = new Error(typeof body === "string" ? body : "FEHLER");
    error.antwort = true;
    error.name = typeof body === "string" ? body : "FEHLER";
    throw error;
  }
  return body;
}

async function holen(path) {
  let antwort;
  try {
    antwort = await fetch(path);
  } catch (error) {
    error.netz = true;
    throw error;
  }
  return antwortLesen(antwort);
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
  return antwortLesen(antwort);
}

// Das Ergebnis einer Handlung überlebt das Neuzeichnen danach nur, wenn es dort gelesen
// wird: zeichnen() liest und löscht sie einmal (D486 Beschluss 2, D492 Beschluss 5).
let letzteMeldung = null;

function meldung(text, erfolg = false) {
  letzteMeldung = { text, erfolg };
}

function meldungKnoten() {
  const node = element("div");
  node.id = "meldung";
  if (letzteMeldung) {
    node.className = letzteMeldung.erfolg ? "meldung erfolg" : "meldung";
    node.textContent = letzteMeldung.text;
    letzteMeldung = null;
  }
  return node;
}

// Jeder Knopf, jede Auswahl und jedes Feld der Seite außer denen der offenen Frage
// (D487 Beschluss 1).
function interaktiveElemente() {
  const seite = document.querySelector("#seite");
  const frage = document.querySelector("#frage");
  return [...seite.querySelectorAll("button, select, input")].filter(
    (node) => !frage || !frage.contains(node),
  );
}

function sperren() {
  for (const node of interaktiveElemente()) node.disabled = true;
}

function entsperren() {
  for (const node of interaktiveElemente()) node.disabled = false;
}

// Die Frage steht an der Stelle von „Jetzt zu tun“, solange sie offen ist (D492 Beschluss 5).
function frageOeffnen(inhalt) {
  const frage = document.querySelector("#frage");
  const jetzt = document.querySelector("#jetzt");
  frage.replaceChildren(...inhalt);
  frage.hidden = false;
  if (jetzt) jetzt.hidden = true;
}

function frageSchliessen() {
  const frage = document.querySelector("#frage");
  const jetzt = document.querySelector("#jetzt");
  frage.hidden = true;
  frage.replaceChildren();
  if (jetzt) jetzt.hidden = false;
}

// Die Art aus p des dekodierten Kerns (D482 Beschluss 3, 01 §2.2).
function artAus(p) {
  let name = p.slice(p.lastIndexOf("/") + 1);
  if (name.endsWith("@1")) name = name.slice(0, -2);
  return name;
}

async function objekt(hash) {
  try {
    const gefunden = await holen(`/objects/${hash}`);
    const gelesen = dekodierenV(bytesFromHex(gefunden.data));
    return gelesen.name === "ACCEPT" ? gelesen.wert : null;
  } catch {
    return null;
  }
}

// Titel eines neuen Antrags aus dem Vorschlagsobjekt, auf das der Kern zeigt, und den
// Verfassungen, beide über /objects gelesen und streng dekodiert (D492 Beschluss 1 und 3).
async function neuerAntrag(vorschlagHash, view, namen) {
  if (!view) return { titel: null, zitate: [] };
  const vorschlag = await objekt(vorschlagHash);
  const ziel = vorschlag instanceof Map ? vorschlag.get(2n) : null;
  if (!(ziel instanceof Uint8Array)) return { titel: null, zitate: [] };
  const neu = await objekt(hex(ziel));
  const alt = await objekt(view.state.epoch.constitution_hash);
  const changes = verfassungsAenderungen(alt, neu);
  if (!changes) return { titel: null, zitate: [] };
  return { titel: antragTitel(changes, namen), zitate: antragZitate(changes) };
}

function einheitAus(bytes) {
  if (bytes === undefined) return null;
  if (!(bytes instanceof Uint8Array)) return undefined;
  try {
    return new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  } catch {
    return undefined;
  }
}

const SUBJEKT_ART = new Map([
  ["vouch", 1n],
  ["obligation", 1n],
  ["receipt", 2n],
]);

// Die Werte für den Satz der Absicht, aus dem dekodierten Kern und den Sichten; was nicht zu
// gewinnen ist, bleibt null, und dann gibt es keinen Satz (D492 Beschluss 1 und 2).
async function felderAus(art, kern, kontext) {
  const [tag, subjekt] = kern.get(2n);
  if (tag !== (SUBJEKT_ART.get(art) ?? 3n)) return {};
  const ziel = hex(subjekt);
  const scope = kern.has(5n) ? hex(kern.get(5n)) : null;
  const view = scope === null ? undefined : kontext.sichten.get(scope);
  const name = (schluessel) => personImSatz(kontext.namen, schluessel).name;
  const gelesen = kern.has(4n) ? dekodierenV(kern.get(4n)) : null;
  const v = gelesen && gelesen.name === "ACCEPT" ? gelesen.wert : null;

  if (art === "accept-rules") {
    return { geltend: view ? ziel === view.state.epoch.constitution_hash : null };
  }
  if (art === "propose") return neuerAntrag(ziel, view, kontext.namen);
  if (art === "vote" || art === "ratify") {
    const antrag = kontext.antraege.find((eintrag) => eintrag.proposal === ziel);
    const titel = antrag ? antragTitel(antrag.changes, kontext.namen) : null;
    const zitate = antrag ? antragZitate(antrag.changes) : [];
    if (art === "ratify") return { titel, zitate };
    const wahlWert = v instanceof Map ? v.get(0n) : undefined;
    const wahl = wahlWert === 1n ? "yes" : wahlWert === 0n ? "no" : null;
    const teilnehmer = view?.state?.constitution_obj?.participants ?? [];
    const einbringend = antrag ? personImSatz(kontext.namen, antrag.proposers[0]) : null;
    return {
      titel,
      zitate,
      name: einbringend ? einbringend.name : null,
      ohneName: einbringend ? einbringend.ohneName : false,
      wahl,
      teilnehmer: teilnehmer.includes(kontext.identitaet),
    };
  }
  if (art === "vouch") {
    const punkte = v instanceof Map && typeof v.get(0n) === "bigint" ? Number(v.get(0n)) : null;
    const ende = kern.get(7n);
    return {
      name: name(ziel),
      punkte,
      tage: typeof ende === "bigint" ? tageAusKern(kern.get(6n), ende) : null,
    };
  }
  if (art === "obligation") {
    let text = null;
    if (v instanceof Map && typeof v.get(0n) === "bigint") {
      const einheit = einheitAus(v.get(1n));
      if (einheit !== undefined) text = betrag(Number(v.get(0n)), einheit);
    }
    return { name: name(ziel), betrag: text };
  }
  if (art === "receipt") {
    const schuld = kontext.obligationen.find((eintrag) => eintrag.claim_id === ziel);
    return {
      name: schuld ? name(schuld.debtor) : null,
      betrag: schuld && schuld.amount !== null ? betrag(schuld.amount, schuld.unit) : null,
    };
  }
  return {};
}

// Die Frage vor dem Unterschreiben: Satz der Absicht, Folge, Warnungen, Einzelheiten; ohne
// Satz kein Unterschreiben (D492 Beschluss 1, 2 und 5, D471 Beschluss 2).
async function fragen(kern, prepared, kontext, autorPub) {
  const art = artAus(kern.get(3n));
  const felder = await felderAus(art, kern, kontext);
  kontext.felder = { art, ...felder };
  const inhalt = frageInhalt(art, felder, prepared);
  const anker = hex(await genesisAnchor(autorPub, crypto.subtle));
  const vorher = hex(kern.get(8n));

  const teile = [marke("Du unterschreibst"), element("div", "satz", inhalt.satz)];
  if (inhalt.unterschreiben) {
    for (const zitat of felder.zitate ?? []) teile.push(element("blockquote", null, zitat));
  }
  if (inhalt.folge.length > 0) {
    const folge = element("div", "folge");
    for (const text of inhalt.folge) folge.append(zeile(text));
    folge.append(zeile(VORHERSAGE, "leise"));
    teile.push(folge);
  }
  for (const text of inhalt.warnungen) teile.push(element("div", "warnung", text));
  const details = [
    `Art: ${artInWorten(kern.get(3n))} (${kern.get(3n)})`,
    `Subjekt: ${hex(kern.get(2n)[1])}`,
    `Vorgänger in der Kette: ${vorher === anker ? "der Anfang" : vorher}`,
    `Zeit: ${zeitpunktInWorten(kern.get(6n), kontext.jetzt)}`,
    `Kennung: ${prepared.claim_id}`,
  ];
  if (kern.has(5n)) details.splice(1, 0, `Scope: ${hex(kern.get(5n))}`);
  teile.push(einzelheiten(details));

  return new Promise((resolve) => {
    const warnt = inhalt.warnungen.length > 0;
    const nein = knopf(
      "Nicht unterschreiben",
      () => {
        frageSchliessen();
        resolve(false);
      },
      warnt || !inhalt.unterschreiben ? "haupt" : "neben",
    );
    const knoepfe = [];
    if (inhalt.unterschreiben) {
      knoepfe.push(
        knopf(
          "Unterschreiben",
          () => {
            frageSchliessen();
            resolve(true);
          },
          warnt ? "neben" : "haupt",
        ),
      );
    }
    knoepfe.push(nein);
    if (warnt) knoepfe.reverse();
    teile.push(knopfReihe(...knoepfe));
    frageOeffnen(teile);
  });
}

// Nach einer Gabelung: an welches Ende angeschlossen wird, jedes mit Art, Zeit und Wert
// (D492 Beschluss 4, D489 Beschluss 3).
async function endeWaehlen(pub, kontext) {
  const spitzen = await holen(`/tips/${pub}`);
  const name = nameVon(kontext.namen, pub);
  const teile = [
    marke("Die Kette hat zwei Enden"),
    element("div", "satz", `${name} hat zweimal an dieselbe Stelle der Kette unterschrieben.`),
    zeile("An welches Ende wird angeschlossen? Das setzt die Kette dort fort und gabelt nicht neu."),
  ];
  return new Promise((resolve) => {
    const reihe = element("div", "paar");
    const laden = spitzen.map(async (id) => {
      const claim = await holen(`/claims/${id}`);
      const karte = element("div", "ende");
      karte.append(
        element("div", "wert", wertInWorten(claim.p, claim.value)),
        zeile(artInWorten(claim.p)),
        zeile(`unterschrieben ${zeitpunktInWorten(claim.t, kontext.jetzt)}`, "leise"),
        einzelheiten([`Kennung: ${id}`]),
        knopf("An dieses Ende anschließen", () => {
          frageSchliessen();
          resolve(id);
        }),
      );
      return karte;
    });
    Promise.all(laden).then((karten) => {
      reihe.append(...karten);
      teile.push(
        reihe,
        knopfReihe(
          knopf(
            "Nicht unterschreiben",
            () => {
              frageSchliessen();
              resolve(null);
            },
            "haupt",
          ),
        ),
      );
      frageOeffnen(teile);
    });
  });
}

function mitVorgaenger(payload, vorgaenger) {
  return vorgaenger ? { ...payload, h_prev: vorgaenger } : payload;
}

// Eine Handlung über das Gerät oder über eine simulierte Person; beide sehen dieselbe Frage
// (D492 Beschluss 1 und 4, D486 Beschluss 3, D479 Beschluss 2).
function handelnFabrik(record, kontext) {
  const erfolg = () => erfolgSatz(kontext.felder?.art, kontext.felder ?? {});

  async function alsGeraet(art, parameter) {
    const ergebnis = await ablauf(crypto.subtle, {
      absicht: (tip) =>
        senden("/intent", mitVorgaenger({ art, I: hex(record.pub), ...parameter }, tip && hex(tip))),
      zeigen: (kern, prepared) => fragen(kern, prepared, kontext, record.pub),
      einliefern: (core, signature) => senden("/submit", { core, sigma: hex(signature) }),
    });
    if (ergebnis.name) meldung(abweisungInWorten(ergebnis.name));
    else if (ergebnis.schwebend) meldung("Eingeliefert; die Antwort des S-Node fehlt noch.");
    else if (ergebnis.ok) meldung(erfolg(), true);
    else if (ergebnis.abbruch) meldung("Nichts unterschrieben.");
    if (!ergebnis.halt) return false;
    frageOeffnen([
      marke("Das Gerät wartet"),
      element(
        "div",
        "satz",
        "Das Gerät weiß nicht sicher, wo seine Kette endet. Der S-Node schlägt ein Ende vor.",
      ),
      einzelheiten([`Vorgeschlagenes Ende: ${hex(ergebnis.halt)}`]),
      knopfReihe(
        knopf(
          "Dieses Ende bestätigen",
          async () => {
            await spitzeBestaetigen(ergebnis.halt);
            frageSchliessen();
            await zeichnen();
          },
          "haupt",
        ),
      ),
    ]);
    return true;
  }

  async function alsSimulierte(art, parameter) {
    const pub = handelnAls;
    let vorgaenger = null;
    let vorbereitet;
    try {
      vorbereitet = await senden("/intent", { I: pub, art, ...parameter });
    } catch (error) {
      if (!(error.antwort && error.name === "more than one tip")) throw error;
      vorgaenger = await endeWaehlen(pub, kontext);
      if (vorgaenger === null) {
        meldung("Nichts unterschrieben.");
        return false;
      }
      vorbereitet = await senden("/intent", mitVorgaenger({ I: pub, art, ...parameter }, vorgaenger));
    }
    const geprueft = pruefen(
      bytesFromHex(vorbereitet.core),
      bytesFromHex(pub),
      bytesFromHex(vorbereitet.h_prev),
    );
    if (geprueft.name !== "ACCEPT") {
      meldung(abweisungInWorten(geprueft.name));
      return false;
    }
    if (await fragen(geprueft.kern, vorbereitet, kontext, bytesFromHex(pub))) {
      await senden("/sim/intent", mitVorgaenger({ I: pub, art, ...parameter }, vorgaenger));
      meldung(erfolg(), true);
    } else {
      meldung("Nichts unterschrieben.");
    }
    return false;
  }

  // Wartet das Gerät auf eine bestätigte Spitze, bleibt die Frage stehen und die Seite wird
  // nicht neu gezeichnet.
  return async function handeln(art, parameter) {
    sperren();
    kontext.felder = null;
    let halten = false;
    try {
      halten = await (handelnAls === "geraet" ? alsGeraet : alsSimulierte)(art, parameter);
    } catch (error) {
      frageSchliessen();
      meldung(error.antwort ? abweisungInWorten(error.name) : "Der S-Node antwortet nicht.");
    } finally {
      entsperren();
    }
    if (!halten) await zeichnen();
  };
}

function wechseln(wert) {
  handelnAls = wert;
  void zeichnen();
}

// Die Geschichte über den Personen: je Schritt ein Haken, wenn er getan ist, und beim ersten
// offenen Schritt „Weiter als <Name>“ (D494 Beschluss 3).
function geschichteBereich(schritte) {
  const bereich = element("div", "geschichte");
  bereich.append(element("div", "marke", "Die Geschichte"));
  const ol = element("ol");
  for (const schritt of schritte) {
    const item = element("li", schritt.getan ? "getan" : "offen");
    item.append(element("span", "haken", schritt.getan ? "✓" : ""), element("span", null, schritt.text));
    if (schritt.weiter) {
      const name = schritt.eigene ? schritt.name ?? "du" : schritt.name;
      if (name) {
        item.append(
          knopf(`Weiter als ${name}`, () => wechseln(schritt.eigene ? "geraet" : schritt.person), "person weiter"),
        );
      }
    }
    ol.append(item);
  }
  bereich.append(ol);
  return bereich;
}

// Rechts die Regie: die Geschichte, dann die eigene Identität und die übrigen nach Namen,
// Aktualisieren, der Selbsttest (D494 Beschluss 3 und 5, D492 Beschluss 5, D484 Beschluss 3).
// Ist jeder Schritt getan, steht die Geschichte nicht mehr da (D509 Beschluss 2).
function regieBereich(namen, simuliert, record, schritte) {
  const regie = element("aside", "regie");
  const ich = record ? hex(record.pub) : null;
  regie.append(
    element("div", "marke", "Regie"),
    zeile("Die Seite links zeigt, was die gewählte Person sieht, und handelt als sie."),
  );
  if (!schritte.every((schritt) => schritt.getan)) regie.append(geschichteBereich(schritte));
  regie.append(element("div", "marke", "Personen"));
  const geordnet = regieReihenfolge(
    [
      ...(ich ? [{ I: ich, name: namen.get(ich) ?? null }] : []),
      ...simuliert.filter((eintrag) => eintrag.I !== ich),
    ],
    ich,
  );
  const personen = [
    ...(ich ? [] : [{ wert: "geraet", text: "Ich" }]),
    ...geordnet.map((eintrag) =>
      eintrag.I === ich
        ? { wert: "geraet", text: `Ich · ${nameVon(namen, ich)}` }
        : { wert: eintrag.I, text: eintrag.name ?? kurz(eintrag.I) },
    ),
  ];
  const auswahl = element("div", "personen");
  for (const person of personen) {
    const button = knopf(person.text, () => wechseln(person.wert), "person");
    button.setAttribute("aria-pressed", String(person.wert === handelnAls));
    auswahl.append(button);
  }
  const link = element("a", null, "Selbsttest");
  link.href = "/app/selbsttest.html";
  regie.append(auswahl, knopf("Aktualisieren", () => void zeichnen(), "person"), link);
  return regie;
}

function anlegenFormular() {
  const abschnitt = element("section", "karte");
  const field = element("input");
  field.type = "text";
  field.maxLength = 64;
  const label = element("label", null, "Dein Name ");
  label.append(field);
  abschnitt.append(
    marke("Jetzt zu tun"),
    element("div", "satz", "Lege einen Schlüssel an. Er bleibt in diesem Browser."),
    label,
    knopfReihe(
      knopf(
        "Schlüssel anlegen",
        async () => {
          const gewaehlt = field.value.trim();
          if (!gewaehlt) {
            meldung("Ein Name fehlt.");
            await zeichnen();
            return;
          }
          const pub = await schluesselAnlegen(crypto.subtle);
          try {
            await senden("/names", { I: hex(pub), name: gewaehlt });
          } catch (error) {
            meldung(error.antwort ? abweisungInWorten(error.name) : "Der S-Node antwortet nicht.");
          }
          await zeichnen();
        },
        "haupt",
      ),
    ),
  );
  return abschnitt;
}

function mitgliedschaftVon(view, identitaet) {
  if (!view || !view.verein) return null;
  const gefunden = view.verein.membership.find(([subject]) => subject === identitaet);
  if (!gefunden) return "Steht nicht auf der Mitgliederliste.";
  const text = mitgliedschaftInWorten(gefunden[1].state);
  return `${text.charAt(0).toUpperCase()}${text.slice(1)}.`;
}

function kopfBereich(titel, info) {
  const kopf = element("header", "kopf");
  kopf.append(element("h1", null, titel));
  if (info) kopf.append(zeile(info, "leise"));
  return kopf;
}

function stimmenZeile(antrag, namen) {
  const ja = aufzaehlung(antrag.yes.map((p) => nameVon(namen, p)));
  const nein = aufzaehlung(antrag.no.map((p) => nameVon(namen, p)));
  return `Bisher Ja: ${ja}. Nein: ${nein}.`;
}

// Fehlt der eigenen Identität ein Name, ist das Eintragen die erste Aufgabe (D494 Beschluss 1).
function namenAufgabe(identitaet) {
  const block = element("div", "aufgabe");
  const field = element("input");
  field.type = "text";
  field.maxLength = 64;
  const label = element("label", null, "Dein Name ");
  label.append(field);
  block.append(
    element("div", "satz", "Trag deinen Namen ein."),
    knopfReihe(
      label,
      knopf(
        "Namen eintragen",
        async () => {
          const gewaehlt = field.value.trim();
          if (!gewaehlt) {
            meldung("Ein Name fehlt.");
          } else {
            try {
              await senden("/names", { I: identitaet, name: gewaehlt });
              meldung(`Dein Name ${gewaehlt} ist eingetragen.`, true);
            } catch (error) {
              meldung(error.antwort ? abweisungInWorten(error.name) : "Der S-Node antwortet nicht.");
            }
          }
          await zeichnen();
        },
        "haupt",
      ),
    ),
  );
  return block;
}

// „Jetzt zu tun“: die Aufgaben der Person in Sätzen, jede mit ihrem Knopf (D494 Beschluss 1,
// D492 Beschluss 5, D484 Beschluss 1).
function jetztBereich(tasks, kontext, handeln) {
  const bereich = element("section", "karte jetzt");
  bereich.id = "jetzt";
  bereich.append(marke("Jetzt zu tun"));
  const { namen, antraege, obligationen } = kontext;
  const ohneName = handelnAls === "geraet" && !namen.get(kontext.identitaet);
  if (ohneName) bereich.append(namenAufgabe(kontext.identitaet));
  if (tasks.length === 0 && !ohneName) {
    bereich.append(zeile("Nichts. Sobald etwas ansteht, steht es hier."));
    return bereich;
  }
  for (const aufgabe of tasks) {
    const block = element("div", "aufgabe");
    if (aufgabe.art === "CONFIRM_RULES") {
      block.append(
        element("div", "satz", "Die Satzung hat sich geändert. Bestätige die geltende Fassung."),
        zeile("Wer nicht neu bestätigt, bleibt stimmberechtigt, ist aber an die neue Fassung nicht gebunden."),
        knopfReihe(
          knopf("Satzung bestätigen …", () =>
            handeln("accept-rules", { scope: aufgabe.scope, constitution: aufgabe.constitution }),
            "haupt",
          ),
        ),
      );
    } else if (aufgabe.art === "VOTE" || aufgabe.art === "RATIFY") {
      const antrag = antraege.find((eintrag) => eintrag.proposal === aufgabe.proposal);
      if (!antrag) continue;
      const titel = antragTitel(antrag.changes, namen);
      const wer = aufzaehlung(antrag.proposers.map((p) => nameVon(namen, p)));
      block.append(element("div", "satz", `${wer} beantragt: ${titel}`));
      for (const zitat of antragZitate(antrag.changes)) {
        block.append(zeile("Neu in der Satzung stünde:"), element("blockquote", null, zitat));
      }
      block.append(zeile(stimmenZeile(antrag, namen)));
      if (aufgabe.art === "VOTE") {
        if (antrag.needed !== null) {
          block.append(zeile(`Angenommen ist der Antrag mit ${antrag.needed} von ${antrag.n} Ja-Stimmen.`));
        }
        block.append(
          knopfReihe(
            knopf("Ja …", () => handeln("vote", { proposal: antrag.proposal, choice: "yes" }), "haupt"),
            knopf("Nein …", () => handeln("vote", { proposal: antrag.proposal, choice: "no" })),
          ),
        );
      } else {
        block.append(
          zeile("Der Antrag ist angenommen. Jemand muss den Beschluss noch feststellen."),
          knopfReihe(
            knopf("Beschluss feststellen …", () => handeln("ratify", { proposal: antrag.proposal }), "haupt"),
          ),
        );
      }
    } else if (aufgabe.art === "CONTRIBUTION_OPEN" || aufgabe.art === "RECEIPT") {
      const schuld = obligationen.find((eintrag) => eintrag.claim_id === aufgabe.obligation);
      if (!schuld) continue;
      const summe = betrag(schuld.amount, schuld.unit);
      const glaeubiger = schuld.creditor === null ? "–" : nameVon(namen, schuld.creditor);
      if (aufgabe.art === "CONTRIBUTION_OPEN") {
        block.append(
          element("div", "satz", `Dein Beitrag von ${summe} an ${glaeubiger} ist offen.`),
          zeile(`Er bleibt offen, bis ${glaeubiger} quittiert.`),
        );
      } else {
        block.append(
          element("div", "satz", `${nameVon(namen, schuld.debtor)} hat zugesagt, ${summe} zu zahlen.`),
          zeile("Ist das Geld da, quittierst du."),
          knopfReihe(
            knopf("Quittieren …", () => handeln("receipt", { obligation: schuld.claim_id }), "haupt"),
          ),
        );
      }
    }
    bereich.append(block);
  }
  return bereich;
}

// Eine Widerspruchskarte je Gabelung, dazu ob sie oben steht (D507 Beschluss 1, D492 Beschluss 5,
// szenario-verein §5.2, 02 §8).
async function widerspruchKarten(forks, kontext) {
  const karten = [];
  for (const gruppe of forks) {
    const name = nameVon(kontext.namen, gruppe.I);
    const claims = await Promise.all(gruppe.claims.map(([cid]) => holen(`/claims/${cid}`)));
    const stimmen = claims.every((claim) => claim.p.endsWith("/vote@1"));
    const werte = claims.map((claim) => wertInWorten(claim.p, claim.value));
    const karte = element("section", "karte widerspruch");
    karte.append(marke("Widerspruch"));
    const punkte = [];
    if (stimmen && werte.includes("Ja") && werte.includes("Nein")) {
      const antrag = kontext.antraege.find((eintrag) => eintrag.proposal === claims[0].J[1]);
      const worum = antrag ? `zum Antrag „${antragTitel(antrag.changes, kontext.namen)}“` : "zu einem Antrag";
      karte.append(element("div", "satz", `${name} hat ${worum} Ja und Nein zugleich unterschrieben.`));
      punkte.push("Keine der beiden Stimmen zählt.");
    } else {
      karte.append(element("div", "satz", `${name} hat zweimal an dieselbe Stelle der Kette unterschrieben.`));
    }
    punkte.push(
      `${name}s Bürgschaften zählen ab jetzt nicht mehr. Wer nur über ${name} verbürgt war, ist es nicht mehr.`,
    );
    karte.append(liste(punkte));
    const paar = element("div", "paar");
    claims.forEach((claim, index) => {
      const seite = element("div", "ende");
      seite.append(
        element("div", "wert", stimmen ? werte[index] : artInWorten(claim.p)),
        zeile(`unterschrieben ${zeitpunktInWorten(claim.t, kontext.jetzt)}`, "leise"),
      );
      paar.append(seite);
    });
    karte.append(
      paar,
      zeile(`Beide stehen an derselben Stelle in ${name}s Kette. Das ist ein Beweis, den jeder nachprüfen kann.`),
      einzelheiten([
        ...gruppe.claims.map(([cid]) => `Kennung: ${cid}`),
        `Gemeinsamer Vorgänger: ${gruppe.h_prev}`,
      ]),
    );
    karten.push({ karte, oben: widerspruchOben(claims, kontext.antraege) });
  }
  return karten;
}

// Der Verein in Sätzen, ohne eigene Marke: der Tab nennt den Bereich (D507 Beschluss 2,
// D492 Beschluss 5, D487 Beschluss 2).
function vereinGerade(view, kontext) {
  const bereich = element("section", "gerade");
  if (!view || !view.verein) {
    bereich.append(zeile("Kein Verein."));
    return bereich;
  }
  const { namen, antraege, obligationen } = kontext;
  const saetze = [fassungSatz(view.state.epoch.index)];
  const mitglieder = view.verein.membership;
  saetze.push(`Auf der Mitgliederliste: ${aufzaehlung(mitglieder.map(([s]) => nameVon(namen, s)))}.`);
  const bestaetigt = mitglieder.filter(([, ergebnis]) => ergebnis.state === "MEMBER").length;
  saetze.push(
    bestaetigt === mitglieder.length
      ? "Alle haben die geltende Satzung bestätigt."
      : `${bestaetigt} von ${mitglieder.length} haben die geltende Satzung bestätigt.`,
  );
  const hinweis = hinweisSatzungGeaendert(mitglieder);
  if (hinweis) saetze.push(hinweis);
  for (const [feld, wert] of Object.entries(view.state.constitution_obj ?? {})) {
    if (typeof wert === "string") saetze.push(`In der Satzung steht zu ${feld}: „${wert}“`);
  }
  const offen = antraege.filter((antrag) => antrag.state === "PENDING");
  const angenommen = antraege.filter((antrag) => antrag.state === "PASSED");
  if (offen.length === 0 && angenommen.length === 0) saetze.push("Keine offenen Anträge.");
  for (const antrag of offen) {
    saetze.push(`Offener Antrag: „${antragTitel(antrag.changes, namen)}“, ${standZeile(antrag)}.`);
  }
  for (const antrag of angenommen) {
    saetze.push(`„${antragTitel(antrag.changes, namen)}“ ist angenommen, aber noch nicht festgestellt.`);
  }
  const offeneBeitraege = obligationen.filter((schuld) => schuld.state === "OPEN").length;
  if (offeneBeitraege > 0) {
    saetze.push(offeneBeitraege === 1 ? "Ein Beitrag ist offen." : `${offeneBeitraege} Beiträge sind offen.`);
  }
  bereich.append(liste(saetze));
  return bereich;
}

// Ein Abschnitt steht in seinem Tab offen, mit dem erklärenden Satz, ohne Einklappen
// (D506 Beschluss 2).
function abschnittOffen(titel, satz) {
  const abschnitt = element("section", "abschnitt");
  abschnitt.append(element("h2", null, titel));
  if (satz) abschnitt.append(zeile(satz, "leise"));
  return abschnitt;
}

// Jede Auswahl einer Person beginnt leer mit „Person wählen …“ (D494 Beschluss 2).
function personAuswahl() {
  const auswahl = element("select");
  const leer = element("option", null, "Person wählen …");
  leer.value = "";
  auswahl.append(leer);
  return auswahl;
}

// Ein Knopf, der erst handelt, wenn in jeder seiner Auswahlen eine Person gewählt ist
// (D494 Beschluss 2).
function knopfMitAuswahl(text, auswahlen, tun) {
  const button = knopf(text, () => {
    if (auswahlen.every((auswahl) => auswahl.value !== "")) tun();
  });
  const pruefen = () => {
    button.disabled = !auswahlen.every((auswahl) => auswahl.value !== "");
  };
  for (const auswahl of auswahlen) auswahl.addEventListener("change", pruefen);
  pruefen();
  return button;
}

function auswahlNamen(namenListe, ausser = new Set()) {
  const auswahl = personAuswahl();
  for (const eintrag of namenListe) {
    if (ausser.has(eintrag.I)) continue;
    const option = element("option", null, eintrag.name ?? kurz(eintrag.I));
    option.value = eintrag.I;
    auswahl.append(option);
  }
  return auswahl;
}

// Die Formulare für Anträge nur für Handelnde auf der Liste (D494 Beschluss 2, 04 §2.1).
function neuerAntragFormular(gov, view, namenListe, namen, identitaet, handeln) {
  const form = element("div", "formular");
  const teilnehmer = new Set(view?.state?.constitution_obj?.participants ?? []);
  if (!teilnehmer.has(identitaet)) {
    form.append(zeile("Anträge stellen kann nur, wer auf der Mitgliederliste steht."));
    return form;
  }
  const aufnehmen = auswahlNamen(namenListe, teilnehmer);
  const ausschliessen = personAuswahl();
  for (const schluessel of teilnehmer) {
    const option = element("option", null, nameVon(namen, schluessel));
    option.value = schluessel;
    ausschliessen.append(option);
  }
  const feldName = element("input");
  feldName.placeholder = "Feld, z. B. beitrag";
  const feldText = element("input");
  feldText.placeholder = "Text";
  form.append(
    zeile("Neuer Antrag:"),
    knopfReihe(
      aufnehmen,
      knopfMitAuswahl("Aufnehmen beantragen …", [aufnehmen], () =>
        handeln("propose", { scope: gov, change: { add: aufnehmen.value } }),
      ),
    ),
    knopfReihe(
      ausschliessen,
      knopfMitAuswahl("Ausschluss beantragen …", [ausschliessen], () =>
        handeln("propose", { scope: gov, change: { remove: ausschliessen.value } }),
      ),
    ),
    knopfReihe(
      feldName,
      feldText,
      knopf("Satzungstext beantragen …", () =>
        handeln("propose", {
          scope: gov,
          change: { set: { field: feldName.value, text: feldText.value } },
        }),
      ),
    ),
  );
  return form;
}

function antraegeAbschnitt(antraege, gov, view, namenListe, namen, identitaet, handeln) {
  const abschnitt = abschnittOffen(
    "Anträge",
    "Eine Änderung der Satzung gilt, wenn genug Ja-Stimmen da sind und jemand den Beschluss " +
      "feststellt. Eine Stimme lässt sich nicht zurücknehmen.",
  );
  if (gov === null) {
    abschnitt.append(zeile("Kein Verein."));
    return abschnitt;
  }
  if (antraege.length === 0) abschnitt.append(zeile("Keine Anträge."));
  for (const antrag of antraege) {
    const karte = element("div", "karte antrag");
    const wer = aufzaehlung(antrag.proposers.map((p) => nameVon(namen, p)));
    karte.append(element("div", "satz", `${wer} beantragt: ${antragTitel(antrag.changes, namen)}`));
    for (const zitat of antragZitate(antrag.changes)) karte.append(element("blockquote", null, zitat));
    karte.append(zeile(`${auszaehlungInWorten(antrag.state)}: ${standZeile(antrag)}`));
    karte.append(zeile(stimmenZeile(antrag, namen)));
    for (const person of antrag.ambiguous) {
      karte.append(
        zeile(`${nameVon(namen, person)} hat zweimal abgestimmt. Eine zweite Stimme macht beide ungültig.`),
      );
    }
    if (antragZitate(antrag.changes).length === 0 && antrag.changes.fields.length > 0) {
      for (const text of aenderungen(antrag.changes, namen)) karte.append(zeile(text));
    }
    if (antrag.state === "PENDING") {
      karte.append(
        knopfReihe(
          knopf("Ja …", () => handeln("vote", { proposal: antrag.proposal, choice: "yes" })),
          knopf("Nein …", () => handeln("vote", { proposal: antrag.proposal, choice: "no" })),
        ),
      );
    }
    if (antrag.state === "PASSED") {
      karte.append(
        knopfReihe(knopf("Beschluss feststellen …", () => handeln("ratify", { proposal: antrag.proposal }))),
      );
    }
    abschnitt.append(karte);
  }
  abschnitt.append(neuerAntragFormular(gov, view, namenListe, namen, identitaet, handeln));
  return abschnitt;
}

function vertrauenAbschnitt(view, res, namenListe, namen, jetzt, handeln) {
  const abschnitt = abschnittOffen(
    "Vertrauen",
    "Wer für wen bürgt. Jeder Bürge hat ein festes Budget; wer es überzieht, dessen " +
      "Bürgschaften fallen alle aus.",
  );
  if (res === null || !view || !view.vereinsleben) {
    abschnitt.append(zeile("Kein Vereinsleben."));
    return abschnitt;
  }
  // Ein Satz je Person statt der Tabelle (D494 Beschluss 5).
  const bfs = view.vereinsleben.derivation.bfs;
  const schluessel = new Set([...namenListe.map((eintrag) => eintrag.I), ...Object.keys(bfs.distance)]);
  const personen = regieReihenfolge(
    [...schluessel].map((I) => ({ I, name: namen.get(I) ?? null })),
    null,
  );
  abschnitt.append(
    liste(personen.map((person) => vertrauenSatz(nameVon(namen, person.I), bfs.distance[person.I]))),
  );

  const person = auswahlNamen(namenListe);
  const gewicht = element("input");
  gewicht.type = "number";
  gewicht.min = "1";
  gewicht.value = "50";
  const tage = element("input");
  tage.type = "number";
  tage.min = "1";
  tage.value = "365";
  const labelGewicht = element("label", null, "Punkte ");
  labelGewicht.append(gewicht);
  const labelTage = element("label", null, "Tage ");
  labelTage.append(tage);
  abschnitt.append(
    knopfReihe(
      person,
      labelGewicht,
      labelTage,
      // Punkte und Tage nur ganz; Werte unter 1 benennt der S-Node (D501 Beschluss 2).
      knopfMitAuswahl("Bürgen …", [person], async () => {
        const punkte = ganzeZahl(gewicht.value);
        const dauer = ganzeZahl(tage.value);
        if (punkte === null || dauer === null) {
          meldung("Punkte und Tage gehen nur in ganzen Zahlen.");
          await zeichnen();
          return;
        }
        await handeln("vouch", {
          scope: res,
          subject: person.value,
          n: punkte,
          t_exp: jetzt + dauer * 86400,
        });
      }),
    ),
  );
  return abschnitt;
}

function beitraegeAbschnitt(obligationen, res, namenListe, namen, handeln) {
  const abschnitt = abschnittOffen(
    "Beiträge",
    "Wer wem was schuldet. Die Schuld unterschreibt der Schuldner selbst, die Quittung der Empfänger.",
  );
  if (res === null) {
    abschnitt.append(zeile("Kein Vereinsleben."));
    return abschnitt;
  }
  for (const schuld of obligationen) {
    const glaeubiger = schuld.creditor === null ? "–" : nameVon(namen, schuld.creditor);
    abschnitt.append(
      zeile(
        `${nameVon(namen, schuld.debtor)} an ${glaeubiger}: ${betrag(schuld.amount, schuld.unit)} — ` +
          tilgungInWorten(schuld.state),
      ),
    );
  }
  const glaeubiger = auswahlNamen(namenListe);
  const euro = element("input");
  euro.type = "number";
  euro.min = "0";
  euro.step = "0.01";
  const label = element("label", null, "Euro ");
  label.append(euro);
  abschnitt.append(
    knopfReihe(
      glaeubiger,
      label,
      // Cent aus dem Text, nicht aus einer Gleitkommazahl (D503 Beschluss 1 und 2).
      knopfMitAuswahl("Beitrag zusagen …", [glaeubiger], async () => {
        const cent = centAus(euro.value);
        if (cent === null) {
          meldung("Der Betrag geht nur in Euro mit höchstens zwei Stellen nach dem Komma.");
          await zeichnen();
          return;
        }
        await handeln("obligation", {
          scope: res,
          creditor: glaeubiger.value,
          amount: cent,
          unit: "EUR-Cent",
        });
      }),
    ),
  );
  return abschnitt;
}

function kasseAbschnitt(view, obligationen, namenListe, namen, identitaet, handeln) {
  const abschnitt = abschnittOffen(
    "Kasse",
    "Für einen Empfänger: wer zugesagt hat, wer quittiert ist, wer fehlt.",
  );
  const auswahl = auswahlNamen(namenListe);
  abschnitt.append(auswahl);
  const teilnehmer = view?.state?.constitution_obj?.participants ?? [];
  const ul = element("ul");
  const zeichneListe = () => {
    ul.replaceChildren();
    if (auswahl.value === "") return;
    for (const eintrag of kassenZeilen(teilnehmer, obligationen, auswahl.value)) {
      const item = element("li", null, `${nameVon(namen, eintrag.teilnehmer)}: ${eintrag.zustand}`);
      const offene = eintrag.obligationen.find((schuld) => schuld.state === "OPEN");
      if (offene && identitaet === auswahl.value) {
        item.append(
          document.createTextNode(" "),
          knopf("Quittieren …", () => handeln("receipt", { obligation: offene.claim_id })),
        );
      }
      ul.append(item);
    }
  };
  auswahl.addEventListener("change", zeichneListe);
  zeichneListe();
  abschnitt.append(ul);
  return abschnitt;
}

function mitgliederAbschnitt(view, namen) {
  const abschnitt = abschnittOffen(
    "Mitglieder",
    "Wer auf der Mitgliederliste steht und wer die geltende Satzung bestätigt hat. Abstimmen " +
      "darf jeder auf der Liste; gebunden ist nur, wer bestätigt hat.",
  );
  if (!view || !view.verein) {
    abschnitt.append(zeile("Kein Verein."));
    return abschnitt;
  }
  abschnitt.append(
    liste(
      view.verein.membership.map(
        ([subject, ergebnis]) => `${nameVon(namen, subject)}: ${mitgliedschaftInWorten(ergebnis.state)}`,
      ),
    ),
  );
  return abschnitt;
}

function findeScope(sichten, teil) {
  for (const [scope, view] of sichten) {
    if (view[teil]) return scope;
  }
  return null;
}

async function zeichnenInhalt() {
  const seite = document.querySelector("#seite");
  const namenListe = await holen("/names");
  const namen = new Map(namenListe.map((eintrag) => [eintrag.I, eintrag.name]));
  const simuliert = namenListe.filter((eintrag) => eintrag.simulated);
  const record = await lesen();
  const ich = record ? hex(record.pub) : null;

  const scopes = await holen("/scopes");
  const sichten = new Map();
  for (const scope of scopes) sichten.set(scope, await holen(`/scopes/${scope}`));
  const gov = findeScope(sichten, "verein");
  const res = findeScope(sichten, "vereinsleben");
  const govView = gov === null ? null : sichten.get(gov);
  const resView = res === null ? null : sichten.get(res);
  const antraege = gov === null ? [] : await holen(`/proposals/${gov}`);
  const obligationen = res === null ? [] : await holen(`/obligations/${res}`);
  const forks = await holen("/forks");

  const eigeneMitgliedschaft = govView?.verein?.membership.find(([subject]) => subject === ich);
  const schritte = geschichte({
    ich,
    namen,
    kanten: resView?.vereinsleben?.derivation.bfs.edges ?? [],
    antraege,
    liste: govView?.state?.constitution_obj?.participants ?? [],
    satzung: govView?.state?.constitution_obj ?? null,
    mitgliedschaft: eigeneMitgliedschaft ? eigeneMitgliedschaft[1].state : null,
    gabelungen: forks.map((gruppe) => gruppe.I),
    obligationen,
  });

  const links = element("div", "links");
  const regie = regieBereich(namen, simuliert, record, schritte);

  if (handelnAls === "geraet" && !record) {
    links.append(kopfBereich("Du hast noch keinen Schlüssel"), meldungKnoten(), anlegenFormular());
    seite.replaceChildren(links, regie);
    return;
  }

  const jetzt = await holen("/now");
  const identitaet = handelnAls === "geraet" ? ich : handelnAls;
  const tasks = await holen(`/tasks/${identitaet}`);

  const kontext = { namen, sichten, antraege, obligationen, identitaet, jetzt, felder: null };
  const handeln = handelnFabrik(record, kontext);

  const frage = element("section", "karte frage");
  frage.id = "frage";
  frage.hidden = true;

  // Ein Widerspruch steht oben, solange über den Antrag abgestimmt wird, sonst im Tab „Im
  // Verein“ unter den Sätzen (D507 Beschluss 1).
  const widersprueche = await widerspruchKarten(forks, kontext);
  const oben = widersprueche.filter((eintrag) => eintrag.oben).map((eintrag) => eintrag.karte);
  const unten = widersprueche.filter((eintrag) => !eintrag.oben).map((eintrag) => eintrag.karte);

  // Fünf Tabs unter dem festen Kopf, in der Reihenfolge aus D506 Beschluss 2; die Zählungen
  // sind dieselben wie in „Im Verein gerade“, und nur der gewählte Tab wird gebaut.
  const tabs = [
    ["Im Verein", 0, () => [vereinGerade(govView, kontext), ...unten]],
    [
      "Anträge",
      antraege.filter((antrag) => antrag.state === "PENDING").length,
      () => [antraegeAbschnitt(antraege, gov, govView, namenListe, namen, identitaet, handeln)],
    ],
    ["Vertrauen", 0, () => [vertrauenAbschnitt(resView, res, namenListe, namen, jetzt, handeln)]],
    [
      "Beiträge und Kasse",
      obligationen.filter((schuld) => schuld.state === "OPEN").length,
      () => [
        beitraegeAbschnitt(obligationen, res, namenListe, namen, handeln),
        kasseAbschnitt(govView, obligationen, namenListe, namen, identitaet, handeln),
      ],
    ],
    ["Mitglieder", 0, () => [mitgliederAbschnitt(govView, namen)]],
  ];
  // Der Inhalt des gewählten Tabs steht in einem Element mit role="tabpanel"; jeder Tab
  // verweist mit aria-controls darauf, das Element mit aria-labelledby auf den gewählten Tab
  // (D507 Beschluss 2).
  const leiste = element("div", "tabs");
  leiste.setAttribute("role", "tablist");
  const inhalt = element("div");
  inhalt.id = "tabinhalt";
  inhalt.setAttribute("role", "tabpanel");
  tabs.forEach(([name, offen, bauen], index) => {
    const tab = knopf(
      tabTitel(name, offen),
      () => {
        gewaehlterTab = name;
        void zeichnen();
      },
      "tab",
    );
    tab.id = `tab-${index}`;
    tab.setAttribute("role", "tab");
    tab.setAttribute("aria-selected", String(name === gewaehlterTab));
    tab.setAttribute("aria-controls", inhalt.id);
    leiste.append(tab);
    if (name === gewaehlterTab) {
      inhalt.setAttribute("aria-labelledby", tab.id);
      inhalt.append(...bauen());
    }
  });

  // Kopf, Meldung, Frage und „Jetzt zu tun“ stehen immer oben, nie in einem Tab (D506
  // Beschluss 1); ein Widerspruch nur bei offener Abstimmung (D507 Beschluss 1). Die Seite nennt sich erst „Du bist <Name>“, wenn der Name eingetragen
  // ist (D494 Beschluss 1).
  const titel = namen.get(identitaet) ? `Du bist ${namen.get(identitaet)}` : "Dein Name fehlt noch";
  links.append(
    kopfBereich(titel, mitgliedschaftVon(govView, identitaet)),
    meldungKnoten(),
    frage,
    jetztBereich(tasks, kontext, handeln),
    ...oben,
    leiste,
    inhalt,
  );
  seite.replaceChildren(links, regie);
}

// Scheitert das Laden, erscheint statt einer leeren Seite ein Satz mit einem Knopf, der es
// erneut versucht (D487 Beschluss 4).
async function zeichnen() {
  const seite = document.querySelector("#seite");
  try {
    await zeichnenInhalt();
  } catch {
    const links = element("div", "links");
    links.append(
      zeile("Der S-Node antwortet nicht."),
      knopfReihe(knopf("Aktualisieren", () => void zeichnen(), "haupt")),
    );
    seite.replaceChildren(links);
  }
}

void zeichnen();
