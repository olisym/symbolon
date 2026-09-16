"""Testaufbau: signierte Vouch-/Lifecycle-Claims ohne Systemuhr, deterministisch aus Labels."""

from __future__ import annotations

import hashlib

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id
from symbolon.verifier import InMemoryStore
from tools.autor import Autor, SpeicherRueckhalt, StoreAusgang

# Normative Seeds aus 00 §3.1 / 03-golden-anchors.md §3.1 — eine Definition (D88).
SEED_ALICE = bytes([0x01] * 32)
SEED_BOB = bytes([0x02] * 32)
SEED_CAROL = bytes([0x03] * 32)


def scope_id(label: str) -> bytes:
    return hashlib.sha256(b"scope:" + label.encode()).digest()


class Identity:
    """Eine Autorenkette: jeder Aufruf hängt an, h_prev wird intern fortgeführt."""

    def __init__(self, label: str, *, seed: bytes | None = None) -> None:
        if seed is None:
            seed = hashlib.sha256(b"identity:" + label.encode()).digest()
        self.label = label
        self._autor = Autor(seed, SpeicherRueckhalt(), StoreAusgang(InMemoryStore()))
        self.pub = self._autor.pub
        self._autor.wiederaufnehmen()

    def _append(
        self,
        *,
        J: tuple[int, bytes],
        p: str,
        t: int,
        v: bytes | None = None,
        N: bytes | None = None,
        t_exp: int | None = None,
    ) -> Claim:
        return self._autor.signieren(J=J, p=p, t=t, v=v, N=N, t_exp=t_exp)

    def vouch(
        self,
        subject: "Identity",
        *,
        n: int | None,
        scope: bytes,
        t: int,
        t_exp: int | None = None,
        extra: dict[int, object] | None = None,
    ) -> Claim:
        """n=None => v abwesend (Default n=D, 02 §3.1)."""
        if n is None:
            v = None
        else:
            payload: dict[int, object] = {0: n}
            if extra:
                payload.update(extra)
            v = cbor_canon.encode(payload)
        return self.vouch_raw(subject, v=v, scope=scope, t=t, t_exp=t_exp)

    def vouch_raw(
        self,
        subject: "Identity",
        *,
        v: bytes | None,
        scope: bytes,
        t: int,
        t_exp: int | None = None,
    ) -> Claim:
        p = f"nuc:{scope.hex()}/vouch@1"
        return self._append(J=(1, subject.pub), p=p, t=t, v=v, N=scope, t_exp=t_exp)

    def claim(
        self,
        *,
        p: str,
        J: tuple[int, bytes],
        t: int,
        v: bytes | None = None,
        N: bytes | None = None,
        t_exp: int | None = None,
    ) -> Claim:
        """Generischer Anhänger für Prädikate jenseits von vouch@1."""
        return self._append(J=J, p=p, t=t, v=v, N=N, t_exp=t_exp)

    def revoke(self, target: Claim, *, t: int) -> Claim:
        return self._append(J=(2, claim_id(target)), p="core/revoke@1", t=t)

    def supersede(self, target: Claim, *, t: int) -> Claim:
        return self._append(J=(2, claim_id(target)), p="core/supersede@1", t=t)


def store_with(*claims: Claim) -> InMemoryStore:
    store = InMemoryStore()
    for c in claims:
        store.add(c)
    return store
