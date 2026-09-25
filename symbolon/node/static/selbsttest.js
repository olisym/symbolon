// Selbsttest: die Vektoren, die Entscheidungen des Ablaufs und die Anzeige
// (D481 Beschluss 1 und 4, D482 Beschluss 1 bis 4, D486 Beschluss 5, 01 §4).

import {
  artInWorten,
  checkCore,
  claimId,
  genesisAnchor,
  klaeren,
  neuerZustand,
  pruefen,
  signCore,
  verbuchen,
} from "./geraet.js";
import { betrag, kassenZeilen, standZeile, warnungInWorten } from "./anzeige.js";

function bytesFromHex(text) {
  const out = new Uint8Array(text.length / 2);
  for (let index = 0; index < out.length; index += 1) {
    out[index] = Number.parseInt(text.slice(index * 2, index * 2 + 2), 16);
  }
  return out;
}

function hex(bytes) {
  return [...bytes].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

function marke(byte) {
  return new Uint8Array(32).fill(byte);
}

// Eine Spitze in Worten, damit auch das Fehlen vergleichbar ist.
function zeigt(wert) {
  return wert ? hex(wert) : "nichts";
}

async function vektorFaelle(vectors, subtle) {
  const key = await subtle.importKey(
    "pkcs8",
    bytesFromHex(vectors.key.pkcs8),
    { name: "Ed25519" },
    false,
    ["sign"],
  );
  const results = [];
  for (const fall of vectors.cases) {
    const core = bytesFromHex(fall.core);
    const author = bytesFromHex(fall.I);
    const tip = bytesFromHex(fall.tip);
    const got = checkCore(core, author, tip);
    let ok = got === fall.expect;
    let detail = got;
    if (ok && fall.expect === "ACCEPT") {
      const id = hex(await claimId(core, subtle));
      const anchor = hex(await genesisAnchor(author, subtle));
      const signature = hex(await signCore(core, key, subtle));
      ok = id === fall.claim_id && anchor === fall.anchor && signature === fall.sigma;
      if (!ok) detail = `Kennung ${id} Anker ${anchor} Unterschrift ${signature}`;
    }
    results.push({ ok, expect: fall.expect, detail });
  }
  return results;
}

// Die Sätze aus D482 Beschluss 1 bis 4, je Satz ein Fall; sie hängen an keiner Rechnung
// aus Python und stehen deshalb hier und nicht in vektoren.json.
async function funktionsFaelle(vectors, subtle) {
  const results = [];
  const pruefe = (satz, ok, detail) => results.push({ ok, expect: satz, detail });
  const pub = marke(0x01);
  const anker = await genesisAnchor(pub, subtle);
  const alt = marke(0x11);
  const schwebend = marke(0x22);
  const fremd = marke(0x33);

  const frisch = neuerZustand(pub, anker);
  pruefe(
    "neuerZustand: Spitze ist der Anker, nichts schwebt",
    zeigt(frisch.tip) === zeigt(anker) && frisch.pending === null,
    `Spitze ${zeigt(frisch.tip)}, schwebend ${zeigt(frisch.pending)}`,
  );

  const vorgerueckt = klaeren({ pub, tip: alt, pending: schwebend }, schwebend);
  pruefe(
    "klaeren: das Schwebende ist der Vorschlag und wird Spitze",
    vorgerueckt.halt === null &&
      zeigt(vorgerueckt.zustand.tip) === zeigt(schwebend) &&
      vorgerueckt.zustand.pending === null,
    `Spitze ${zeigt(vorgerueckt.zustand.tip)}, schwebend ${zeigt(vorgerueckt.zustand.pending)}`,
  );

  const verworfen = klaeren({ pub, tip: alt, pending: schwebend }, alt);
  pruefe(
    "klaeren: die Spitze ist der Vorschlag, das Schwebende wird verworfen",
    verworfen.halt === null &&
      zeigt(verworfen.zustand.tip) === zeigt(alt) &&
      verworfen.zustand.pending === null,
    `Spitze ${zeigt(verworfen.zustand.tip)}, schwebend ${zeigt(verworfen.zustand.pending)}`,
  );

  const dritter = klaeren({ pub, tip: alt, pending: schwebend }, fremd);
  pruefe(
    "klaeren: ein dritter Vorschlag hält an",
    zeigt(dritter.halt) === zeigt(fremd) &&
      zeigt(dritter.zustand.tip) === zeigt(alt) &&
      zeigt(dritter.zustand.pending) === zeigt(schwebend),
    `Halt ${zeigt(dritter.halt)}, Spitze ${zeigt(dritter.zustand.tip)}`,
  );

  const ohneSpitze = klaeren({ pub, tip: null, pending: null }, anker);
  pruefe(
    "klaeren: ohne Spitze hält auch der Genesis-Anker an",
    zeigt(ohneSpitze.halt) === zeigt(anker) && ohneSpitze.zustand.tip === null,
    `Halt ${zeigt(ohneSpitze.halt)}, Spitze ${zeigt(ohneSpitze.zustand.tip)}`,
  );

  const ruhig = klaeren({ pub, tip: alt, pending: null }, fremd);
  pruefe(
    "klaeren: ohne Schwebendes und mit Spitze unverändert",
    ruhig.halt === null &&
      zeigt(ruhig.zustand.tip) === zeigt(alt) &&
      ruhig.zustand.pending === null,
    `Halt ${zeigt(ruhig.halt)}, Spitze ${zeigt(ruhig.zustand.tip)}`,
  );

  const gleich = verbuchen({ pub, tip: alt, pending: null }, schwebend, schwebend);
  pruefe(
    "verbuchen: gleiche Antwort, die Kennung wird Spitze",
    zeigt(gleich.tip) === zeigt(schwebend) && gleich.pending === null,
    `Spitze ${zeigt(gleich.tip)}, schwebend ${zeigt(gleich.pending)}`,
  );

  const abweichend = verbuchen({ pub, tip: alt, pending: null }, schwebend, fremd);
  pruefe(
    "verbuchen: abweichende Antwort, die Kennung schwebt",
    zeigt(abweichend.tip) === zeigt(alt) && zeigt(abweichend.pending) === zeigt(schwebend),
    `Spitze ${zeigt(abweichend.tip)}, schwebend ${zeigt(abweichend.pending)}`,
  );

  const ohneAntwort = verbuchen({ pub, tip: alt, pending: null }, schwebend, null);
  pruefe(
    "verbuchen: ohne Antwort schwebt die Kennung",
    zeigt(ohneAntwort.tip) === zeigt(alt) && zeigt(ohneAntwort.pending) === zeigt(schwebend),
    `Spitze ${zeigt(ohneAntwort.tip)}, schwebend ${zeigt(ohneAntwort.pending)}`,
  );

  const angenommen = vectors.cases.find((fall) => fall.expect === "ACCEPT");
  const kernFall = pruefen(
    bytesFromHex(angenommen.core),
    bytesFromHex(angenommen.I),
    bytesFromHex(angenommen.tip),
  );
  pruefe(
    "pruefen: ACCEPT gibt den dekodierten Kern",
    kernFall.name === checkCore(
      bytesFromHex(angenommen.core),
      bytesFromHex(angenommen.I),
      bytesFromHex(angenommen.tip),
    ) &&
      kernFall.name === "ACCEPT" &&
      kernFall.kern instanceof Map &&
      hex(kernFall.kern.get(1n)) === angenommen.I &&
      hex(kernFall.kern.get(8n)) === angenommen.tip,
    `${kernFall.name}, Kern ${kernFall.kern === null ? "fehlt" : "da"}`,
  );

  const abgewiesen = vectors.cases.find((fall) => fall.expect !== "ACCEPT");
  const nameFall = pruefen(
    bytesFromHex(abgewiesen.core),
    bytesFromHex(abgewiesen.I),
    bytesFromHex(abgewiesen.tip),
  );
  pruefe(
    "pruefen: eine Abweisung trägt den Namen aus checkCore und keinen Kern",
    nameFall.name === abgewiesen.expect && nameFall.kern === null,
    `${nameFall.name}, Kern ${nameFall.kern === null ? "fehlt" : "da"}`,
  );

  const arten = [
    ["accept-rules", "Satzung annehmen"],
    ["propose", "Antrag stellen"],
    ["vote", "Abstimmen"],
    ["ratify", "Beschluss feststellen"],
    ["vouch", "Bürgen"],
    ["obligation", "Schuld eintragen"],
    ["receipt", "Zahlung quittieren"],
  ];
  for (const [name, wort] of arten) {
    const p = `nuc:${hex(marke(0xab))}/${name}@1`;
    pruefe(`artInWorten: ${name}`, artInWorten(p) === wort, artInWorten(p));
  }
  pruefe(
    "artInWorten: eine unbekannte Art wörtlich",
    artInWorten("core/revoke@1") === "core/revoke@1",
    artInWorten("core/revoke@1"),
  );

  return results;
}

// Die Sätze aus szenario-verein.md für die Anzeige, mindestens einer je genanntem Satz
// (D486 Beschluss 5).
function anzeigeFaelle() {
  const results = [];
  const pruefe = (satz, ok, detail) => results.push({ ok, expect: satz, detail });

  pruefe(
    "standZeile: 1 Ja, 1 Nein, 2 von 3 nötig (szenario-verein §3)",
    standZeile({ yes: ["a"], no: ["b"], needed: 2, n: 3 }) === "1 Ja, 1 Nein, 2 von 3 nötig",
    standZeile({ yes: ["a"], no: ["b"], needed: 2, n: 3 }),
  );
  pruefe(
    "standZeile: 2 Ja, 0 Nein, 3 von 4 nötig (szenario-verein §4)",
    standZeile({ yes: ["a", "b"], no: [], needed: 3, n: 4 }) === "2 Ja, 0 Nein, 3 von 4 nötig",
    standZeile({ yes: ["a", "b"], no: [], needed: 3, n: 4 }),
  );
  pruefe(
    "betrag: 2400 EUR-Cent als 24,00 € (szenario-verein §6)",
    betrag(2400, "EUR-Cent") === "24,00 €",
    betrag(2400, "EUR-Cent"),
  );

  const kasse = "kk";
  const fremd = "xx";
  const zeilen = kassenZeilen(
    ["unterschrieben", "quittiert", "fehlt"],
    [
      { debtor: "unterschrieben", creditor: kasse, state: "OPEN" },
      { debtor: "quittiert", creditor: kasse, state: "SETTLED" },
      { debtor: "fehlt", creditor: fremd, state: "OPEN" },
    ],
    kasse,
  );
  const zustand = new Map(zeilen.map((zeile) => [zeile.teilnehmer, zeile.zustand]));
  pruefe(
    "kassenZeilen: unterschrieben (szenario-verein §6)",
    zustand.get("unterschrieben") === "unterschrieben",
    zustand.get("unterschrieben"),
  );
  pruefe(
    "kassenZeilen: quittiert (szenario-verein §6)",
    zustand.get("quittiert") === "quittiert",
    zustand.get("quittiert"),
  );
  pruefe(
    "kassenZeilen: eine Obligation an einen anderen Gläubiger zählt nicht, fehlt (szenario-verein §6)",
    zustand.get("fehlt") === "fehlt",
    zustand.get("fehlt"),
  );

  pruefe(
    "warnungInWorten: ein unbekannter Name wörtlich",
    warnungInWorten("UNBEKANNT") === "UNBEKANNT",
    warnungInWorten("UNBEKANNT"),
  );

  return results;
}

export async function run(vectors, subtle) {
  const results = await vektorFaelle(vectors, subtle);
  results.push(...(await funktionsFaelle(vectors, subtle)));
  results.push(...anzeigeFaelle());
  return results;
}

async function seite() {
  const ausgabe = document.querySelector("#ausgabe");
  const antwort = await fetch("/app/vektoren.json");
  const vectors = await antwort.json();
  const results = await run(vectors, crypto.subtle);
  const passed = results.filter((item) => item.ok).length;
  ausgabe.textContent = `${passed} von ${results.length} bestanden`;
  for (const item of results) {
    if (item.ok) continue;
    const line = document.createElement("p");
    line.textContent = `${item.expect}: ${item.detail}`;
    ausgabe.append(line);
  }
}

if (typeof document !== "undefined") void seite();
