"""Schnittstelle des S-Node (D476, 01 §4, 01 §6)."""

from __future__ import annotations

import json
import time
from collections.abc import Callable, Mapping
from dataclasses import fields, is_dataclass
from enum import Enum
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id, core_bytes, id_genesis_anchor, sign
from symbolon.errors import VerifierError
from symbolon.node.store import ObjectKind, SqliteStore
from symbolon.node.view import fork_evidence, scope_view

_LIMIT = 1048576
_HOST = "127.0.0.1"


def json_value(value: Any) -> Any:
    """JSON-Form jeder Antwort (D476 Beschluss 6)."""
    if isinstance(value, Enum):
        return json_value(value.value)
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, bytes):
        return value.hex()
    if is_dataclass(value) and not isinstance(value, type):
        return {item.name: json_value(getattr(value, item.name)) for item in fields(value)}
    if isinstance(value, (tuple, list)):
        return [json_value(item) for item in value]
    if isinstance(value, (set, frozenset)):
        try:
            ordered = sorted(value)
        except TypeError:
            ordered = sorted(value, key=repr)
        return [json_value(item) for item in ordered]
    if isinstance(value, Mapping):
        out: dict[str, Any] = {}
        for key, item in value.items():
            if isinstance(key, bytes):
                name = key.hex()
            elif isinstance(key, bool):
                name = "true" if key else "false"
            elif isinstance(key, int):
                name = str(key)
            elif isinstance(key, str):
                name = key
            else:
                name = repr(key)
            out[name] = json_value(item)
        return out
    return repr(value)


def _clock_default() -> int:
    return int(time.time())


def _hex(text: object, size: int | None = None) -> bytes:
    if not isinstance(text, str):
        raise ValueError("expected hex text")
    try:
        raw = bytes.fromhex(text)
    except ValueError as exc:
        raise ValueError("expected hex text") from exc
    if size is not None and len(raw) != size:
        raise ValueError(f"expected {size} bytes")
    return raw


def _require(body: Mapping[str, Any], key: str) -> Any:
    if key not in body:
        raise ValueError(f"missing field {key}")
    return body[key]


def _tips(store: SqliteStore, author: bytes) -> list[Claim]:
    own = [claim for claim in store.all_claims() if claim.I == author]
    pointed = {claim.h_prev for claim in own}
    return [claim for claim in own if claim_id(claim) not in pointed]


def _prepare(store: SqliteStore, body: Mapping[str, Any], clock: Callable[[], int]) -> Claim:
    """Vorbereiten (D476 Beschluss 2 und 3, 01 §4, 01 §6)."""
    author = _hex(_require(body, "I"), 32)
    predicate = _require(body, "p")
    if not isinstance(predicate, str):
        raise ValueError("p is not text")
    subject = _require(body, "J")
    if (
        not isinstance(subject, list)
        or len(subject) != 2
        or isinstance(subject[0], bool)
        or not isinstance(subject[0], int)
    ):
        raise ValueError("J is not a pair")
    payload = _hex(body["v"]) if "v" in body else None
    scope = _hex(body["N"], 32) if "N" in body else None
    expiry = body["t_exp"] if "t_exp" in body else None
    if expiry is not None and (isinstance(expiry, bool) or not isinstance(expiry, int)):
        raise ValueError("t_exp is not an integer")
    if "h_prev" in body:
        previous = _hex(body["h_prev"], 32)
    else:
        tips = _tips(store, author)
        if len(tips) > 1:
            raise _Forked()
        previous = id_genesis_anchor(author) if not tips else claim_id(tips[0])
    moment = clock()
    if isinstance(moment, bool) or not isinstance(moment, int):
        raise ValueError("clock is not an integer")
    known = store.get(previous)
    if known is not None and moment < known.t:
        moment = known.t
    return Claim(
        version=1,
        I=author,
        J=(subject[0], _hex(subject[1], 32)),
        p=predicate,
        t=moment,
        h_prev=previous,
        v=payload,
        N=scope,
        t_exp=expiry,
    )


def _submit(store: SqliteStore, core: bytes, sigma: bytes) -> bytes:
    """Kern und Signatur einliefern (D476 Beschluss 4, 01 §6)."""
    try:
        canonical = cbor_canon.is_canonical(core)
    except Exception as exc:
        raise ValueError("core is not canonical") from exc
    if not canonical:
        raise ValueError("core is not canonical")
    obj = cbor_canon.decode(core)
    if not isinstance(obj, dict) or any(type(key) is not int for key in obj):
        raise ValueError("core is not a map")
    obj[9] = sigma
    claim = store.submit_claim(cbor_canon.encode(obj))
    return claim_id(claim)


class _Forked(Exception):
    """Mehr als eine Spitze (D476 Beschluss 3)."""


class _PayloadTooLarge(Exception):
    """Rumpf über einem MiB (D476 Beschluss 5)."""


class _Missing(Exception):
    """Unbekannter Pfad, fehlender Genesis oder fehlender Seed."""


def _handler(store: SqliteStore, clock: Callable[[], int]) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, _format: str, *_args: object) -> None:
            return

        def do_GET(self) -> None:
            self._dispatch(False)

        def do_POST(self) -> None:
            self._dispatch(True)

        def _dispatch(self, post: bool) -> None:
            try:
                self._route(post)
            except _PayloadTooLarge:
                self._send(413, "payload too large")
            except _Forked:
                self._send(409, "more than one tip")
            except _Missing:
                self._send(404, "not found")
            except VerifierError as exc:
                self._send(400, type(exc).__name__)
            except ValueError as exc:
                self._send(400, str(exc))
            except Exception as exc:
                self._send(500, type(exc).__name__)

        def _route(self, post: bool) -> None:
            path = self.path.split("?", 1)[0]
            if not post and path == "/scopes":
                self._send(200, sorted(store.all_genesis()))
                return
            if not post and path.startswith("/scopes/"):
                scope = _hex(path[len("/scopes/") :], 32)
                if scope not in store.all_genesis():
                    raise _Missing()
                self._send(200, scope_view(store, scope, clock()))
                return
            if not post and path == "/forks":
                self._send(200, fork_evidence(store, clock()))
                return
            if post and path in {"/objects", "/claims", "/prepare", "/submit", "/sim/sign"}:
                body = self._json_body()
                if path == "/objects":
                    kind = ObjectKind(_require(body, "kind"))
                    digest = store.submit_object(kind, _hex(_require(body, "data")))
                    self._send(200, {"hash": digest})
                    return
                if path == "/claims":
                    claim = store.submit_claim(_hex(_require(body, "data")))
                    self._send(200, {"claim_id": claim_id(claim)})
                    return
                if path == "/prepare":
                    prepared = _prepare(store, body, clock)
                    self._send(200, _prepared_body(prepared))
                    return
                if path == "/submit":
                    cid = _submit(
                        store,
                        _hex(_require(body, "core")),
                        _hex(_require(body, "sigma"), 64),
                    )
                    self._send(200, {"claim_id": cid})
                    return
                seed = store.sim_seed(_hex(_require(body, "I"), 32))
                if seed is None:
                    raise _Missing()
                prepared = _prepare(
                    store, {key: value for key, value in body.items() if key != "h_prev"}, clock
                )
                sigma = sign(Ed25519PrivateKey.from_private_bytes(seed), prepared)
                cid = _submit(store, core_bytes(prepared), sigma)
                self._send(200, {"claim_id": cid})
                return
            raise _Missing()

        def _json_body(self) -> dict[str, Any]:
            raw = self._read()
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError("invalid json") from exc
            if not isinstance(obj, dict):
                raise ValueError("expected json object")
            return obj

        def _read(self) -> bytes:
            header = self.headers.get("Content-Length")
            if header is None:
                raise ValueError("missing field Content-Length")
            try:
                length = int(header)
            except ValueError as exc:
                raise ValueError("invalid Content-Length") from exc
            if length > _LIMIT:
                remaining = length
                while remaining:
                    chunk = self.rfile.read(min(remaining, 65536))
                    if not chunk:
                        break
                    remaining -= len(chunk)
                raise _PayloadTooLarge()
            return self.rfile.read(length)

        def _send(self, status: int, payload: object) -> None:
            encoded = json.dumps(json_value(payload)).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

    return Handler


def _prepared_body(claim: Claim) -> dict[str, object]:
    return {
        "core": core_bytes(claim),
        "claim_id": claim_id(claim),
        "h_prev": claim.h_prev,
        "t": claim.t,
    }


def serve(
    path: str | Path,
    port: int = 8470,
    clock: Callable[[], int] | None = None,
    bound: Callable[[HTTPServer], None] | None = None,
) -> None:
    """Öffnet den Bestand in diesem Faden und bedient 127.0.0.1 (D476 Beschluss 5)."""
    store = SqliteStore(path)
    server = HTTPServer((_HOST, port), _handler(store, clock or _clock_default))
    try:
        if bound is not None:
            bound(server)
        server.serve_forever()
    finally:
        server.server_close()
        store.close()
