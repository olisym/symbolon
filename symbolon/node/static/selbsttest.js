// Selbsttest gegen die Vektoren (D481 Beschluss 1, 01 §4).

import { checkCore, claimId, genesisAnchor, signCore } from "./geraet.js";

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

export async function run(vectors, subtle) {
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
