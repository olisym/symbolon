// Gerät: Dekodieren, Prüfen, Schlüssel, die Entscheidungen des Ablaufs
// (D481 Beschluss 2 bis 4, D482 Beschluss 1 bis 5, D479 Beschluss 6, 01 §2, 01 §3, 01 §4).

const DOM_SIG = new TextEncoder().encode("claim-atom/v1/sig");
const DOM_CID = new TextEncoder().encode("claim-atom/v1/cid");
const DOM_ID_GEN = new TextEncoder().encode("claim-atom/v1/id-genesis");
const LOCK = "geraet";
const REQUIRED = [0n, 1n, 2n, 3n, 6n, 8n];

function malformed() {
  const error = new Error("MALFORMED");
  error.malformed = true;
  return error;
}

function same(left, right) {
  if (left.length !== right.length) return false;
  for (let index = 0; index < left.length; index += 1) {
    if (left[index] !== right[index]) return false;
  }
  return true;
}

function concat(parts) {
  const length = parts.reduce((sum, part) => sum + part.length, 0);
  const out = new Uint8Array(length);
  let offset = 0;
  for (const part of parts) {
    out.set(part, offset);
    offset += part.length;
  }
  return out;
}

function compareBytes(left, right) {
  const length = Math.min(left.length, right.length);
  for (let index = 0; index < length; index += 1) {
    if (left[index] !== right[index]) return left[index] - right[index];
  }
  return left.length - right.length;
}

function head(major, length) {
  const prefix = major << 5;
  if (length < 24) return Uint8Array.of(prefix | length);
  if (length < 256) return Uint8Array.of(prefix | 24, length);
  if (length < 65536) return Uint8Array.of(prefix | 25, length >> 8, length & 0xff);
  const out = new Uint8Array(5);
  out[0] = prefix | 26;
  new DataView(out.buffer).setUint32(1, length);
  return out;
}

function encodeUint(value) {
  if (value < 0n || value >= 2n ** 64n) throw malformed();
  if (value < 24n) return Uint8Array.of(Number(value));
  if (value < 256n) return Uint8Array.of(24, Number(value));
  if (value < 65536n) return Uint8Array.of(25, Number(value >> 8n), Number(value & 0xffn));
  if (value < 2n ** 32n) {
    const out = new Uint8Array(5);
    out[0] = 26;
    new DataView(out.buffer).setUint32(1, Number(value));
    return out;
  }
  const out = new Uint8Array(9);
  out[0] = 27;
  const view = new DataView(out.buffer);
  view.setUint32(1, Number(value >> 32n));
  view.setUint32(5, Number(value & 0xffffffffn));
  return out;
}

function encodeBytes(major, bytes) {
  return concat([head(major, bytes.length), bytes]);
}

function encode(value) {
  if (typeof value === "bigint") return encodeUint(value);
  if (value instanceof Uint8Array) return encodeBytes(2, value);
  if (typeof value === "string") return encodeBytes(3, new TextEncoder().encode(value));
  if (Array.isArray(value)) {
    return concat([head(4, value.length), ...value.map((item) => encode(item))]);
  }
  if (value instanceof Map) {
    const entries = [...value.entries()].map(([key, item]) => [encode(key), encode(item)]);
    entries.sort((left, right) => compareBytes(left[0], right[0]));
    return concat([
      head(5, entries.length),
      ...entries.map(([key, item]) => concat([key, item])),
    ]);
  }
  throw malformed();
}

function readArgument(bytes, index, info) {
  if (info < 24) return [BigInt(info), index];
  const width = { 24: 1, 25: 2, 26: 4, 27: 8 }[info];
  if (width === undefined) throw malformed();
  if (index + width > bytes.length) throw malformed();
  let value = 0n;
  for (let step = 0; step < width; step += 1) {
    value = (value << 8n) + BigInt(bytes[index + step]);
  }
  return [value, index + width];
}

function keyMark(key) {
  if (typeof key === "bigint") return `i:${key}`;
  if (typeof key === "string") return `s:${key}`;
  if (key instanceof Uint8Array) return `b:${[...key].join(",")}`;
  throw malformed();
}

function decodeItem(bytes, index) {
  if (index >= bytes.length) throw malformed();
  const major = bytes[index] >> 5;
  const info = bytes[index] & 0x1f;
  index += 1;
  if (info === 31 || major === 1 || major === 6 || major === 7) throw malformed();
  if (major === 0) return readArgument(bytes, index, info);
  if (major === 2 || major === 3) {
    const [length, start] = readArgument(bytes, index, info);
    const size = Number(length);
    if (start + size > bytes.length) throw malformed();
    const slice = bytes.slice(start, start + size);
    if (major === 2) return [slice, start + size];
    let text;
    try {
      text = new TextDecoder("utf-8", { fatal: true }).decode(slice);
    } catch {
      throw malformed();
    }
    return [text, start + size];
  }
  if (major === 4) {
    const [count, start] = readArgument(bytes, index, info);
    const items = [];
    index = start;
    for (let step = 0n; step < count; step += 1n) {
      const [item, next] = decodeItem(bytes, index);
      items.push(item);
      index = next;
    }
    return [items, index];
  }
  if (major === 5) {
    const [count, start] = readArgument(bytes, index, info);
    const map = new Map();
    index = start;
    for (let step = 0n; step < count; step += 1n) {
      const [key, afterKey] = decodeItem(bytes, index);
      const [item, next] = decodeItem(bytes, afterKey);
      const mark = keyMark(key);
      if (map.has(mark)) throw malformed();
      map.set(mark, [key, item]);
      index = next;
    }
    const ordered = new Map();
    for (const [key, item] of map.values()) ordered.set(key, item);
    return [ordered, index];
  }
  throw malformed();
}

function isBytes(value, length) {
  return value instanceof Uint8Array && (length === undefined || value.length === length);
}

function schema(value) {
  if (!(value instanceof Map)) return "SCHEMA";
  for (const key of value.keys()) {
    if (typeof key !== "bigint" || key < 0n || key > 8n) return "SCHEMA";
  }
  for (const key of REQUIRED) {
    if (!value.has(key)) return "SCHEMA";
  }
  if (typeof value.get(0n) !== "bigint") return "SCHEMA";
  if (!isBytes(value.get(1n), 32)) return "SCHEMA";
  const subject = value.get(2n);
  if (!Array.isArray(subject) || subject.length !== 2) return "SCHEMA";
  if (typeof subject[0] !== "bigint" || !isBytes(subject[1], 32)) return "SCHEMA";
  if (typeof value.get(3n) !== "string") return "SCHEMA";
  if (value.has(4n) && !isBytes(value.get(4n))) return "SCHEMA";
  if (value.has(5n) && !isBytes(value.get(5n), 32)) return "SCHEMA";
  if (typeof value.get(6n) !== "bigint") return "SCHEMA";
  if (value.has(7n) && typeof value.get(7n) !== "bigint") return "SCHEMA";
  if (!isBytes(value.get(8n), 32)) return "SCHEMA";
  return null;
}

function abgewiesen(name) {
  return { name, kern: null };
}

// Prüfung mit dem dekodierten Kern, damit das Gerät zeigt, was es unterschreibt
// (D482 Beschluss 3, D481 Beschluss 2, 01 §2, 01 §3).
export function pruefen(core, I, tip) {
  let value;
  try {
    const [decoded, end] = decodeItem(core, 0);
    if (end !== core.length) return abgewiesen("MALFORMED");
    value = decoded;
  } catch (error) {
    if (error && error.malformed) return abgewiesen("MALFORMED");
    throw error;
  }
  if (!same(encode(value), core)) return abgewiesen("NOT_CANONICAL");
  if (schema(value)) return abgewiesen("SCHEMA");
  if (value.get(0n) !== 1n) return abgewiesen("WRONG_VERSION");
  if (!same(value.get(1n), I)) return abgewiesen("WRONG_AUTHOR");
  if (!same(value.get(8n), tip)) return abgewiesen("WRONG_PREDECESSOR");
  return { name: "ACCEPT", kern: value };
}

export function checkCore(core, author, tip) {
  return pruefen(core, author, tip).name;
}

const ARTEN = new Map([
  ["accept-rules", "Satzung annehmen"],
  ["propose", "Antrag stellen"],
  ["vote", "Abstimmen"],
  ["ratify", "Beschluss feststellen"],
  ["vouch", "Bürgen"],
  ["obligation", "Schuld eintragen"],
  ["receipt", "Zahlung quittieren"],
]);

// Die Art folgt aus p, eine unbekannte Art erscheint wörtlich (D482 Beschluss 3, 01 §2.2).
export function artInWorten(p) {
  let name = p.slice(p.lastIndexOf("/") + 1);
  if (name.endsWith("@1")) name = name.slice(0, -2);
  return ARTEN.get(name) ?? p;
}

async function digest(subtle, domain, payload) {
  const hash = await subtle.digest("SHA-256", concat([domain, payload]));
  return new Uint8Array(hash);
}

export function claimId(core, subtle) {
  return digest(subtle, DOM_CID, core);
}

export function genesisAnchor(author, subtle) {
  return digest(subtle, DOM_ID_GEN, author);
}

export function signCore(core, key, subtle) {
  return subtle.sign({ name: "Ed25519" }, key, concat([DOM_SIG, core])).then(
    (signature) => new Uint8Array(signature),
  );
}

// Ein frischer Schlüssel beginnt an seinem Anker (D482 Beschluss 1 und 5, 01 §4).
export function neuerZustand(pub, anker) {
  return { pub, tip: anker, pending: null };
}

// Eine schwebende oder fehlende Spitze am Vorschlag des S-Node klären
// (D481 Beschluss 4, D482 Beschluss 1, D471 Beschluss 2).
export function klaeren(zustand, vorschlag) {
  const { tip, pending } = zustand;
  if (pending && same(pending, vorschlag)) {
    return { zustand: { ...zustand, tip: pending, pending: null }, halt: null };
  }
  if (pending && tip && same(tip, vorschlag)) {
    return { zustand: { ...zustand, pending: null }, halt: null };
  }
  if (pending || !tip) return { zustand, halt: vorschlag };
  return { zustand, halt: null };
}

// Die Antwort auf das Einliefern verbuchen (D482 Beschluss 2, D481 Beschluss 4).
export function verbuchen(zustand, id, antwortId) {
  if (antwortId && same(id, antwortId)) return { ...zustand, tip: id, pending: null };
  return { ...zustand, pending: id };
}

function memory() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("geraet", 1);
    request.onupgradeneeded = () => {
      request.result.createObjectStore("zustand");
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

function mitSpeicher(mode, nutzen) {
  return memory().then(
    (base) =>
      new Promise((resolve, reject) => {
        const transaction = base.transaction("zustand", mode);
        const request = nutzen(transaction.objectStore("zustand"));
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
        transaction.oncomplete = () => base.close();
      }),
  );
}

export function lesen() {
  return mitSpeicher("readonly", (store) => store.get("selbst")).then((record) => record ?? null);
}

function schreiben(record) {
  return mitSpeicher("readwrite", (store) => store.put(record, "selbst")).then(() => undefined);
}

export function schluesselAnlegen(subtle) {
  return navigator.locks.request(LOCK, async () => {
    const vorhanden = await lesen();
    if (vorhanden) return vorhanden.pub;
    const pair = await subtle.generateKey({ name: "Ed25519" }, false, ["sign"]);
    const pub = new Uint8Array(await subtle.exportKey("raw", pair.publicKey));
    const anker = await genesisAnchor(pub, subtle);
    await schreiben({
      ...neuerZustand(pub, anker),
      privateKey: pair.privateKey,
      publicKey: pair.publicKey,
    });
    return pub;
  });
}

export function spitzeBestaetigen(tip) {
  return navigator.locks.request(LOCK, async () => {
    const record = await lesen();
    record.tip = tip;
    record.pending = null;
    await schreiben(record);
  });
}

function hexToBytes(text) {
  const out = new Uint8Array(text.length / 2);
  for (let index = 0; index < out.length; index += 1) {
    out[index] = Number.parseInt(text.slice(index * 2, index * 2 + 2), 16);
  }
  return out;
}

export function ablauf(subtle, { absicht, zeigen, einliefern }) {
  return navigator.locks.request(LOCK, async () => {
    const record = await lesen();
    if (!record) return { fehlt: true };
    let zustand = { pub: record.pub, tip: record.tip, pending: record.pending };
    if (zustand.pending || !zustand.tip) {
      const vorschlag = hexToBytes((await absicht(null)).h_prev);
      const geklaert = klaeren(zustand, vorschlag);
      if (geklaert.halt) return { halt: geklaert.halt };
      zustand = geklaert.zustand;
      await schreiben({ ...record, ...zustand });
    }
    const prepared = await absicht(zustand.tip);
    const core = hexToBytes(prepared.core);
    const { name, kern } = pruefen(core, zustand.pub, zustand.tip);
    if (name !== "ACCEPT") return { name };
    if (!(await zeigen(kern))) return { abbruch: true };
    const signature = await signCore(core, record.privateKey, subtle);
    const id = await claimId(core, subtle);
    let antwort = null;
    try {
      antwort = await einliefern(prepared.core, signature);
    } catch (error) {
      if (error && error.antwort) return { name: error.name };
    }
    zustand = verbuchen(zustand, id, antwort ? hexToBytes(antwort.claim_id) : null);
    await schreiben({ ...record, ...zustand });
    return zustand.pending ? { schwebend: true } : { ok: true };
  });
}
