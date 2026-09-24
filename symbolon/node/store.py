"""Bestand in einer SQLite-Datei (D473, D476, 01 §6, 00 §3, 00 §5, 04 §2.4)."""

from __future__ import annotations

import sqlite3
from enum import Enum
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_from_bytes, claim_id, signed_bytes
from symbolon.genesis import genesis_scope
from symbolon.governance.objects import Proposal
from symbolon.policy import constitution_hash
from symbolon.resolve import resolve_state
from symbolon.trust.params import resolve_trust_params
from symbolon.verifier import InMemoryStore, structural_check


class ObjectKind(str, Enum):
    """Art eines Objekts: Genesis, Verfassung oder Vorschlag (D473 Beschluss 1)."""

    GENESIS = "genesis"
    CONSTITUTION = "constitution"
    PROPOSAL = "proposal"


class SqliteStore:
    """Bestand in einer SQLite-Datei (D473)."""

    def __init__(self, path: str | Path) -> None:
        self._db = sqlite3.connect(path)
        self._db.executescript(
            """
            CREATE TABLE IF NOT EXISTS claims (
                claim_id BLOB PRIMARY KEY,
                data BLOB NOT NULL,
                I BLOB NOT NULL,
                h_prev BLOB NOT NULL
            );
            CREATE INDEX IF NOT EXISTS claims_author_hprev ON claims (I, h_prev);
            CREATE TABLE IF NOT EXISTS objects (
                hash BLOB PRIMARY KEY,
                kind TEXT NOT NULL,
                data BLOB NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sim_keys (
                pub BLOB PRIMARY KEY,
                seed BLOB NOT NULL
            );
            CREATE TABLE IF NOT EXISTS names (
                pub BLOB PRIMARY KEY,
                name TEXT NOT NULL
            );
            """
        )
        self._db.commit()

    def close(self) -> None:
        self._db.close()

    def get(self, cid: bytes) -> Claim | None:
        row = self._db.execute(
            "SELECT data FROM claims WHERE claim_id = ?", (cid,)
        ).fetchone()
        if row is None:
            return None
        return claim_from_bytes(row[0])

    def by_author_hprev(self, I: bytes, h_prev: bytes) -> list[Claim]:
        rows = self._db.execute(
            "SELECT data FROM claims WHERE I = ? AND h_prev = ? ORDER BY rowid",
            (I, h_prev),
        ).fetchall()
        return [claim_from_bytes(row[0]) for row in rows]

    def add(self, claim: Claim) -> None:
        self.submit_claim(signed_bytes(claim))

    def all_claims(self) -> list[Claim]:
        rows = self._db.execute(
            "SELECT data FROM claims ORDER BY rowid"
        ).fetchall()
        return [claim_from_bytes(row[0]) for row in rows]

    def submit_claim(self, data: bytes) -> Claim:
        """Liefert einen Claim ein (01 §6, D473 Beschluss 1)."""
        claim = structural_check(data, self)
        cid = claim_id(claim)
        if self.get(cid) is None:
            self._db.execute(
                "INSERT INTO claims (claim_id, data, I, h_prev) VALUES (?, ?, ?, ?)",
                (cid, data, claim.I, claim.h_prev),
            )
            self._db.commit()
        return claim

    def submit_object(self, kind: ObjectKind, data: bytes) -> bytes:
        """Liefert ein Objekt ein und gibt seinen Hash zurück (D473 Beschluss 1, D474 Beschluss 1)."""
        try:
            canonical = cbor_canon.is_canonical(data)
        except Exception as exc:
            raise ValueError("object bytes are not canonical") from exc
        if not canonical:
            raise ValueError("object bytes are not canonical")
        obj = cbor_canon.decode(data)
        if kind is ObjectKind.GENESIS:
            if not isinstance(obj, dict):
                raise ValueError("genesis object is not a map")
            digest = genesis_scope(obj)
            resolve_state(
                InMemoryStore(),
                scope=digest,
                genesis_obj=obj,
                known_constitutions={},
                known_proposals={},
                now=0,
            )
            if 9 in obj:
                resolve_trust_params(scope=digest, genesis_obj=obj)
        elif kind is ObjectKind.CONSTITUTION:
            if not isinstance(obj, dict):
                raise ValueError("constitution object is not a map")
            digest = constitution_hash(obj)
        elif kind is ObjectKind.PROPOSAL:
            if not isinstance(obj, dict) or any(type(key) is not int for key in obj):
                raise ValueError("proposal object is not a map of uint keys")
            if set(obj) != {0, 1, 2}:
                raise ValueError("proposal object keys are not 0, 1, 2")
            fields: list[bytes] = []
            for key in (0, 1, 2):
                value = obj[key]
                if not isinstance(value, bytes) or len(value) != 32:
                    raise ValueError("proposal field is not 32 bytes")
                fields.append(value)
            digest = Proposal(
                scope=fields[0],
                predecessor=fields[1],
                constitution_hash=fields[2],
            ).proposal_hash
        else:
            raise ValueError("unknown object kind")
        row = self._db.execute(
            "SELECT 1 FROM objects WHERE hash = ?", (digest,)
        ).fetchone()
        if row is None:
            self._db.execute(
                "INSERT INTO objects (hash, kind, data) VALUES (?, ?, ?)",
                (digest, kind.value, data),
            )
            self._db.commit()
        return digest

    def _rows(self, kind: ObjectKind) -> list[tuple[bytes, bytes]]:
        return self._db.execute(
            "SELECT hash, data FROM objects WHERE kind = ? ORDER BY hash",
            (kind.value,),
        ).fetchall()

    def all_genesis(self) -> dict[bytes, dict]:
        """Alle Genesis-Objekte, Abbildung vom Hash auf das Objekt (D473)."""
        return {row[0]: cbor_canon.decode(row[1]) for row in self._rows(ObjectKind.GENESIS)}

    def all_constitutions(self) -> dict[bytes, dict]:
        """Alle Verfassungen, Abbildung vom Hash auf das Objekt (D473)."""
        return {
            row[0]: cbor_canon.decode(row[1])
            for row in self._rows(ObjectKind.CONSTITUTION)
        }

    def all_proposals(self) -> dict[bytes, Proposal]:
        """Alle Vorschläge, Abbildung vom Hash auf das Proposal (D473, 04 §2.4)."""
        found: dict[bytes, Proposal] = {}
        for digest, data in self._rows(ObjectKind.PROPOSAL):
            obj = cbor_canon.decode(data)
            found[digest] = Proposal(
                scope=obj[0], predecessor=obj[1], constitution_hash=obj[2]
            )
        return found

    def add_sim_key(self, seed: bytes) -> bytes:
        """Trägt einen simulierten Schlüssel ein und gibt den öffentlichen zurück (D476 Beschluss 4, D477 Beschluss 2)."""
        pub = Ed25519PrivateKey.from_private_bytes(seed).public_key().public_bytes_raw()
        row = self._db.execute(
            "SELECT pub FROM sim_keys WHERE seed = ?", (seed,)
        ).fetchone()
        if row is not None:
            return row[0]
        self._db.execute(
            "INSERT INTO sim_keys (pub, seed) VALUES (?, ?)",
            (pub, seed),
        )
        self._db.commit()
        return pub

    def sim_seed(self, pub: bytes) -> bytes | None:
        """Liest den Seed zu einem öffentlichen Schlüssel, oder None (D476 Beschluss 4)."""
        row = self._db.execute(
            "SELECT seed FROM sim_keys WHERE pub = ?", (pub,)
        ).fetchone()
        if row is None:
            return None
        return row[0]

    def sim_pubs(self) -> set[bytes]:
        """Öffentliche Schlüssel der simulierten Personen (D471 Beschluss 3, D479 Beschluss 5)."""
        rows = self._db.execute("SELECT pub FROM sim_keys").fetchall()
        return {row[0] for row in rows}

    def add_name(self, pub: bytes, name: str) -> None:
        """Setzt den Namen eines Schlüssels, auch wiederholt (D479 Beschluss 5)."""
        self._db.execute(
            "INSERT INTO names (pub, name) VALUES (?, ?) "
            "ON CONFLICT(pub) DO UPDATE SET name = excluded.name",
            (pub, name),
        )
        self._db.commit()

    def all_names(self) -> dict[bytes, str]:
        """Namen des Adressbuchs, Abbildung vom Schlüssel auf den Namen (D479 Beschluss 5)."""
        rows = self._db.execute("SELECT pub, name FROM names").fetchall()
        return {row[0]: row[1] for row in rows}

    def object_at(self, digest: bytes) -> tuple[str, bytes] | None:
        """Art und Bytes eines Objekts, oder None (D479 Beschluss 5)."""
        row = self._db.execute(
            "SELECT kind, data FROM objects WHERE hash = ?", (digest,)
        ).fetchone()
        if row is None:
            return None
        return row[0], row[1]
