// Selbsttest: die Vektoren, die Entscheidungen des Ablaufs und die Anzeige
// (D481 Beschluss 1 und 4, D482 Beschluss 1 bis 4, D486 Beschluss 5, D487 Beschluss 2 und 4,
// D489 Beschluss 3, D492 Beschluss 1 bis 3, D494 Beschluss 3, 5 und 6, D496 Beschluss 1 bis 3,
// D498 Beschluss 1 und 2, 01 §4).

import {
  artInWorten,
  checkCore,
  claimId,
  dekodierenV,
  genesisAnchor,
  klaeren,
  neuerZustand,
  pruefen,
  signCore,
  verbuchen,
} from "./geraet.js";
import {
  KEIN_SATZ,
  absichtSatz,
  abweisungInWorten,
  aenderungen,
  antragTitel,
  betrag,
  fassungSatz,
  folgeZeilen,
  frageInhalt,
  geschichte,
  hinweisSatzungGeaendert,
  kassenZeilen,
  mitgliedschaftInWorten,
  personImSatz,
  regieReihenfolge,
  standZeile,
  tageAusKern,
  vertrauenSatz,
  warnungInWorten,
  wertInWorten,
  zeitpunktInWorten,
} from "./anzeige.js";

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

  pruefe(
    "mitgliedschaftInWorten: GRANT_ONLY (D487 Beschluss 2)",
    mitgliedschaftInWorten("GRANT_ONLY") ===
      "steht auf der Liste, hat die geltende Satzung noch nicht bestätigt",
    mitgliedschaftInWorten("GRANT_ONLY"),
  );
  pruefe(
    "mitgliedschaftInWorten: APPLICANT (D487 Beschluss 2)",
    mitgliedschaftInWorten("APPLICANT") === "hat bestätigt, steht nicht auf der Liste",
    mitgliedschaftInWorten("APPLICANT"),
  );
  pruefe(
    "abweisungInWorten: ALREADY_PARTICIPANT (D487 Beschluss 2)",
    abweisungInWorten("ALREADY_PARTICIPANT") === "Diese Person steht schon auf der Mitgliederliste.",
    abweisungInWorten("ALREADY_PARTICIPANT"),
  );
  pruefe(
    "abweisungInWorten: NOT_PARTICIPANT (D487 Beschluss 2)",
    abweisungInWorten("NOT_PARTICIPANT") === "Diese Person steht nicht auf der Mitgliederliste.",
    abweisungInWorten("NOT_PARTICIPANT"),
  );
  pruefe(
    "hinweisSatzungGeaendert: mindestens ein GRANT_ONLY (D487 Beschluss 2, szenario-verein §4)",
    hinweisSatzungGeaendert([
      ["a", { state: "MEMBER" }],
      ["b", { state: "GRANT_ONLY" }],
    ]) !== null,
    hinweisSatzungGeaendert([
      ["a", { state: "MEMBER" }],
      ["b", { state: "GRANT_ONLY" }],
    ]),
  );
  pruefe(
    "hinweisSatzungGeaendert: ein APPLICANT ohne GRANT_ONLY, kein Hinweis (D489 Beschluss 3)",
    hinweisSatzungGeaendert([
      ["a", { state: "MEMBER" }],
      ["b", { state: "APPLICANT" }],
    ]) === null,
    hinweisSatzungGeaendert([
      ["a", { state: "MEMBER" }],
      ["b", { state: "APPLICANT" }],
    ]),
  );
  pruefe(
    "hinweisSatzungGeaendert: kein GRANT_ONLY, kein Hinweis",
    hinweisSatzungGeaendert([["a", { state: "MEMBER" }]]) === null,
    hinweisSatzungGeaendert([["a", { state: "MEMBER" }]]),
  );

  pruefe(
    "wertInWorten: Wahl 1 einer Stimme als Ja (D487 Beschluss 4)",
    wertInWorten("nuc:aabb/vote@1", { "0": 1 }) === "Ja",
    wertInWorten("nuc:aabb/vote@1", { "0": 1 }),
  );
  pruefe(
    "wertInWorten: Wahl 0 einer Stimme als Nein (D487 Beschluss 4)",
    wertInWorten("nuc:aabb/vote@1", { "0": 0 }) === "Nein",
    wertInWorten("nuc:aabb/vote@1", { "0": 0 }),
  );
  pruefe(
    "wertInWorten: jeder andere Wert als JSON (D487 Beschluss 4)",
    wertInWorten("nuc:aabb/ratify@1", { "0": ["x"] }) === '{"0":["x"]}',
    wertInWorten("nuc:aabb/ratify@1", { "0": ["x"] }),
  );

  pruefe(
    "aenderungen: ein Wert, der kein Text ist, als JSON (D487 Beschluss 4)",
    JSON.stringify(
      aenderungen(
        { added: [], removed: [], fields: [{ field: "thresholds", old: null, new: { ordinary: [1, 2] } }] },
        new Map(),
      ),
    ) === JSON.stringify(['thresholds: – → {"ordinary":[1,2]}']),
    aenderungen(
      { added: [], removed: [], fields: [{ field: "thresholds", old: null, new: { ordinary: [1, 2] } }] },
      new Map(),
    ),
  );

  return results;
}

// Titel, Sätze der Absicht und der Folge, wörtlich aus D492 Beschluss 2 und 3, und der
// strenge Dekoder für v (D492 Beschluss 1).
function saetzeFaelle() {
  const results = [];
  const gleich = (satz, got, want) =>
    results.push({ ok: JSON.stringify(got) === JSON.stringify(want), expect: satz, detail: JSON.stringify(got) });
  const namen = new Map([
    ["aa", "OLI"],
    ["bb", "BRUNO"],
  ]);
  const ohne = { added: [], removed: [], fields: [] };

  gleich("antragTitel: aufnehmen", antragTitel({ ...ohne, added: ["aa"] }, namen), "OLI aufnehmen");
  gleich("antragTitel: ausschließen", antragTitel({ ...ohne, removed: ["bb"] }, namen), "BRUNO ausschließen");
  gleich(
    "antragTitel: Feld ohne alten Wert",
    antragTitel({ ...ohne, fields: [{ field: "beitrag", old: null, new: "24 Euro" }] }, namen),
    "beitrag festlegen",
  );
  gleich(
    "antragTitel: Feld mit altem Wert",
    antragTitel({ ...ohne, fields: [{ field: "beitrag", old: "12 Euro", new: "24 Euro" }] }, namen),
    "beitrag ändern",
  );
  gleich(
    "antragTitel: mehreres",
    antragTitel({ ...ohne, added: ["aa"], fields: [{ field: "beitrag", old: null, new: "24 Euro" }] }, namen),
    "Satzung ändern",
  );

  gleich(
    "absichtSatz: accept-rules, geltende Fassung",
    absichtSatz("accept-rules", { geltend: true }),
    "Du bestätigst die geltende Satzung des Vereins.",
  );
  gleich(
    "absichtSatz: accept-rules, frühere Fassung",
    absichtSatz("accept-rules", { geltend: false }),
    "Du bestätigst eine frühere Fassung der Satzung.",
  );
  gleich(
    "absichtSatz: propose",
    absichtSatz("propose", { titel: "beitrag festlegen" }),
    "Du beantragst: beitrag festlegen.",
  );
  gleich(
    "absichtSatz: vote",
    absichtSatz("vote", { name: "ANNA", titel: "beitrag festlegen", wahl: "yes" }),
    "Du stimmst Ja zu ANNAs Antrag „beitrag festlegen“.",
  );
  gleich(
    "absichtSatz: ratify",
    absichtSatz("ratify", { titel: "beitrag festlegen" }),
    "Du stellst fest: Der Antrag „beitrag festlegen“ ist angenommen.",
  );
  gleich(
    "absichtSatz: vouch",
    absichtSatz("vouch", { name: "OLI", punkte: 50, tage: 365 }),
    "Du bürgst für OLI mit 50 Punkten für 365 Tage.",
  );
  gleich(
    "absichtSatz: obligation",
    absichtSatz("obligation", { betrag: "24,00 €", name: "KASSE" }),
    "Du verpflichtest dich, 24,00 € an KASSE zu zahlen.",
  );
  gleich(
    "absichtSatz: receipt",
    absichtSatz("receipt", { name: "DORA", betrag: "24,00 €" }),
    "Du bestätigst, dass DORA 24,00 € bezahlt hat.",
  );
  gleich(
    "absichtSatz: fehlt der Name, kein Satz",
    absichtSatz("vote", { name: null, titel: "beitrag festlegen", wahl: "yes" }),
    null,
  );

  const stimme = { no: 0, n: 4, needed: 3, passes: false, counts: true };
  gleich(
    "folgeZeilen: vote, es fehlt noch eine",
    folgeZeilen("vote", { ...stimme, yes: 2 }, { teilnehmer: true }),
    ["Danach: 2 von 3 nötigen Ja-Stimmen", "Es fehlt noch eine."],
  );
  gleich(
    "folgeZeilen: vote, es fehlen noch 2",
    folgeZeilen("vote", { ...stimme, yes: 1 }, { teilnehmer: true }),
    ["Danach: 1 von 3 nötigen Ja-Stimmen", "Es fehlen noch 2."],
  );
  gleich(
    "folgeZeilen: vote, passes",
    folgeZeilen("vote", { ...stimme, yes: 3, passes: true }, { teilnehmer: true }),
    [
      "Danach: 3 von 3 nötigen Ja-Stimmen",
      "Der Antrag ist dann angenommen; jemand muss den Beschluss noch feststellen.",
    ],
  );
  gleich(
    "folgeZeilen: vote, counts falsch, schon abgestimmt",
    folgeZeilen("vote", { ...stimme, yes: 1, counts: false }, { teilnehmer: true }),
    [
      "Danach: 1 von 3 nötigen Ja-Stimmen",
      "Es fehlen noch 2.",
      "Deine Stimme zählt nicht: Du hast schon abgestimmt. Auch deine erste Stimme zählt dann nicht mehr.",
    ],
  );
  gleich(
    "folgeZeilen: vote, counts falsch, nicht auf der Liste",
    folgeZeilen("vote", { ...stimme, yes: 1, counts: false }, { teilnehmer: false }),
    [
      "Danach: 1 von 3 nötigen Ja-Stimmen",
      "Es fehlen noch 2.",
      "Deine Stimme zählt nicht: Du stehst nicht auf der Mitgliederliste.",
    ],
  );
  gleich(
    "folgeZeilen: vouch unter D",
    folgeZeilen("vouch", { used: 50, D: 100 }, {}),
    ["Danach: Du hast 50 von 100 Punkten vergeben."],
  );
  gleich(
    "folgeZeilen: vouch über D",
    folgeZeilen("vouch", { used: 101, D: 100 }, {}),
    ["Danach: Du hast 101 von 100 Punkten vergeben.", "Dann zählt keine deiner Bürgschaften mehr."],
  );

  const lesen = (text) => {
    const gelesen = dekodierenV(bytesFromHex(text));
    return { name: gelesen.name, wahl: gelesen.wert instanceof Map ? String(gelesen.wert.get(0n)) : null };
  };
  gleich("dekodierenV: {0: 1} kanonisch", lesen("a10001"), { name: "ACCEPT", wahl: "1" });
  gleich("dekodierenV: {0: 1} nicht kürzest kodiert", lesen("a1001801"), { name: "NOT_CANONICAL", wahl: null });
  gleich("dekodierenV: Restbytes", lesen("a1000100"), { name: "MALFORMED", wahl: null });
  gleich("dekodierenV: Float", lesen("a100f93c00"), { name: "MALFORMED", wahl: null });

  return results;
}

// Die Geschichte, die Wörter aus D494 Beschluss 5 und die Punkte aus D494 Beschluss 6.
function fuehrungFaelle() {
  const results = [];
  const gleich = (satz, got, want) =>
    results.push({ ok: JSON.stringify(got) === JSON.stringify(want), expect: satz, detail: JSON.stringify(got) });

  const ich = "01";
  const [anna, bruno, chris, dora] = ["aa", "bb", "cc", "dd"];
  const szenario = [
    [anna, "ANNA"],
    [bruno, "BRUNO"],
    [chris, "CHRIS"],
    [dora, "DORA"],
  ];
  const leer = {
    ich,
    namen: new Map(szenario),
    kanten: [],
    antraege: [],
    liste: [anna, bruno, chris, dora],
    satzung: {},
    mitgliedschaft: null,
    gabelungen: [],
  };
  const voll = {
    ...leer,
    namen: new Map([[ich, "OLI"], ...szenario]),
    kanten: [{ author: chris, subject: ich }],
    antraege: [
      {
        proposers: [anna],
        yes: [],
        changes: { added: [], removed: [], fields: [{ field: "beitrag", old: null, new: "24 Euro" }] },
      },
    ],
    liste: [anna, bruno, chris, dora, ich],
    mitgliedschaft: "MEMBER",
    gabelungen: [bruno],
  };
  const offen = geschichte(leer);
  const getan = geschichte(voll);
  offen.forEach((schritt, index) => {
    gleich(`geschichte: offen, ${schritt.text}`, schritt.getan, false);
    gleich(`geschichte: getan, ${getan[index].text}`, getan[index].getan, true);
  });
  gleich(
    "geschichte: erster offener Schritt ist der Name, als du",
    offen.filter((schritt) => schritt.weiter).map((schritt) => [schritt.text, schritt.eigene]),
    [["Du trägst deinen Namen ein", true]],
  );
  const verbuergt = geschichte({ ...leer, namen: voll.namen, kanten: [{ author: chris, subject: ich }] });
  gleich(
    "geschichte: nach Name und Bürgschaft ist ANNA dran",
    verbuergt.filter((schritt) => schritt.weiter).map((schritt) => [schritt.text, schritt.person, schritt.name]),
    [["ANNA beantragt deine Aufnahme", anna, "ANNA"]],
  );
  const vonAnna = geschichte({ ...leer, namen: voll.namen, kanten: [{ author: anna, subject: ich }] });
  gleich("geschichte: eine Bürgschaft von ANNA ist nicht die von CHRIS", vonAnna[1].getan, false);
  const aufnahme = {
    proposers: [anna],
    yes: [anna],
    changes: { added: [ich], removed: [], fields: [] },
  };
  const abgestimmt = geschichte({ ...leer, namen: voll.namen, antraege: [aufnahme] });
  gleich(
    "geschichte: nach ANNAs Ja stimmt CHRIS",
    [abgestimmt[2].getan, abgestimmt[3].getan, abgestimmt[3].name],
    [true, false, "CHRIS"],
  );

  gleich("vertrauenSatz: Abstand 0", vertrauenSatz("ANNA", 0), "ANNA ist Anker des Vereins.");
  gleich(
    "vertrauenSatz: Abstand 1",
    vertrauenSatz("CHRIS", 1),
    "CHRIS ist verbürgt, einen Schritt vom Anker entfernt.",
  );
  gleich("vertrauenSatz: Abstand 2", vertrauenSatz("DORA", 2), "DORA ist verbürgt, 2 Schritte vom Anker entfernt.");
  gleich("vertrauenSatz: ohne Abstand", vertrauenSatz("OLI", undefined), "OLI ist nicht verbürgt.");
  gleich("fassungSatz", fassungSatz(2), "Es gilt die 2. Fassung der Satzung.");
  gleich(
    "regieReihenfolge: zuerst die eigene, dann nach Namen",
    regieReihenfolge(
      [
        { I: "cc", name: "CHRIS" },
        { I: "01", name: "OLI" },
        { I: "aa", name: "ANNA" },
      ],
      "01",
    ).map((person) => person.name),
    ["OLI", "ANNA", "CHRIS"],
  );

  const mitSatz = frageInhalt("propose", { titel: "beitrag festlegen" }, { warnings: [], effect: { needed: 3, n: 4 } });
  gleich(
    "frageInhalt: mit Satz wird Unterschreiben angeboten",
    [mitSatz.satz, mitSatz.unterschreiben],
    ["Du beantragst: beitrag festlegen.", true],
  );
  const ohneSatz = frageInhalt("propose", {}, { warnings: [], effect: { needed: 3, n: 4 } });
  gleich(
    "frageInhalt: ohne Satz kein Unterschreiben",
    [ohneSatz.satz, ohneSatz.unterschreiben, ohneSatz.folge],
    [KEIN_SATZ, false, []],
  );
  gleich(
    "absichtSatz: eine Stimme ohne lesbare Wahl",
    absichtSatz("vote", { name: "ANNA", titel: "beitrag festlegen", wahl: null }),
    null,
  );
  gleich(
    "absichtSatz: 1 Punkt in der Einzahl",
    absichtSatz("vouch", { name: "OLI", punkte: 1, tage: 365 }),
    "Du bürgst für OLI mit 1 Punkt für 365 Tage.",
  );
  const unbenannt = personImSatz(new Map(), "93fdd4aaaaaaaaaaaaaaaa315267");
  gleich(
    "absichtSatz: Einbringende ohne Namen",
    absichtSatz("vote", { ...unbenannt, titel: "beitrag festlegen", wahl: "yes" }),
    "Du stimmst Ja zum Antrag „beitrag festlegen“ einer Person ohne Namen (93fdd4…315267).",
  );

  return results;
}

// Der Schritt zum Satzungstext, die Satzung bei GRANT_ONLY, die Tage der Bürgschaft und die
// Abstände zur Uhr des S-Node an ihren Grenzen (D496 Beschluss 1 bis 3, D495).
function feinschliffFaelle() {
  const results = [];
  const gleich = (satz, got, want) =>
    results.push({ ok: JSON.stringify(got) === JSON.stringify(want), expect: satz, detail: JSON.stringify(got) });

  const ich = "01";
  const anna = "aa";
  const namen = new Map([
    [ich, "OLI"],
    [anna, "ANNA"],
    ["bb", "BRUNO"],
    ["cc", "CHRIS"],
    ["dd", "DORA"],
  ]);
  const leer = {
    ich,
    namen,
    kanten: [],
    antraege: [],
    liste: [anna, "bb", "cc", "dd"],
    satzung: {},
    mitgliedschaft: null,
    gabelungen: [],
  };
  const text = "ANNA beantragt einen Satzungstext, etwa den Beitrag";
  const schritt = (zustand, name) => geschichte(zustand).find((eintrag) => eintrag.text === name);
  gleich("geschichte: Satzungstext offen", schritt(leer, text).getan, false);
  gleich(
    "geschichte: Satzungstext getan über einen Antrag mit anders benanntem Feld",
    schritt(
      {
        ...leer,
        antraege: [
          {
            proposers: [anna],
            yes: [],
            changes: { added: [], removed: [], fields: [{ field: "Beitrag", old: null, new: "24" }] },
          },
        ],
      },
      text,
    ).getan,
    true,
  );
  gleich(
    "geschichte: Satzungstext getan über ein Textfeld der Satzung",
    schritt({ ...leer, satzung: { zweck: "Laufen am Sonntag" } }, text).getan,
    true,
  );
  gleich(
    "geschichte: Du bestätigst die Satzung offen bei GRANT_ONLY",
    schritt({ ...leer, mitgliedschaft: "GRANT_ONLY" }, "Du bestätigst die Satzung").getan,
    false,
  );

  gleich(
    "absichtSatz: Bürgschaft für 1 Tag",
    absichtSatz("vouch", { name: "OLI", punkte: 50, tage: 1 }),
    "Du bürgst für OLI mit 50 Punkten für 1 Tag.",
  );
  gleich(
    "absichtSatz: Bürgschaft für 365 Tage",
    absichtSatz("vouch", { name: "OLI", punkte: 50, tage: 365 }),
    "Du bürgst für OLI mit 50 Punkten für 365 Tage.",
  );

  const jetzt = 1000000;
  gleich("zeitpunktInWorten: 59 Sekunden", zeitpunktInWorten(jetzt - 59, jetzt), "gerade eben");
  gleich("zeitpunktInWorten: 60 Sekunden", zeitpunktInWorten(jetzt - 60, jetzt), "vor 1 Minute");
  gleich("zeitpunktInWorten: eine Stunde", zeitpunktInWorten(jetzt - 3600, jetzt), "vor 1 Stunde");
  gleich("zeitpunktInWorten: ein Tag", zeitpunktInWorten(jetzt - 86400, jetzt), "vor 1 Tag");
  gleich("zeitpunktInWorten: zwei Tage", zeitpunktInWorten(jetzt - 172800, jetzt), "vor 2 Tagen");

  // Die Tage einer Bürgschaft aufgerundet, an den Grenzen aus D498 Beschluss 2.
  const tag = 86400;
  const jahr = 1000 + 365 * tag;
  gleich("tageAusKern: genau 365 Tage", tageAusKern(1000, jahr), 365);
  gleich("tageAusKern: 365 Tage weniger drei Sekunden, als BigInt", tageAusKern(1003n, BigInt(jahr)), 365);
  gleich("tageAusKern: eine Sekunde", tageAusKern(1000, 1001), 1);
  gleich("tageAusKern: ein Tag und eine Sekunde", tageAusKern(1000, 1000 + tag + 1), 2);

  return results;
}

export async function run(vectors, subtle) {
  const results = await vektorFaelle(vectors, subtle);
  results.push(...(await funktionsFaelle(vectors, subtle)));
  results.push(...anzeigeFaelle());
  results.push(...saetzeFaelle());
  results.push(...fuehrungFaelle());
  results.push(...feinschliffFaelle());
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
