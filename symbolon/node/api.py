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
from symbolon.governance.objects import Proposal
from symbolon.governance.tally import TallyState
from symbolon.index import classify_all
from symbolon.node.store import ObjectKind, SqliteStore
from symbolon.node.view import TaskView, fork_evidence, proposals_view, scope_view, tasks_view
from symbolon.policy import constitution_hash
from symbolon.predicates import is_nuc_name
from symbolon.trust.groups import build_groups
from symbolon.trust.params import resolve_trust_params

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


# Schlüssel der Verfassungstabellen, die set abweist (D479 Beschluss 3).
# irrevocable_predicates, thresholds, arbitration, enforcement_policy, nucleus_keys: 00 §5.
# participants, thresholds: 04 §1.1.
_RESERVED = frozenset(
    {
        "irrevocable_predicates",
        "thresholds",
        "arbitration",
        "enforcement_policy",
        "nucleus_keys",
        "participants",
    }
)

_ARTS = frozenset(
    {
        "accept-rules",
        "propose",
        "vote",
        "ratify",
        "vouch",
        "obligation",
        "receipt",
    }
)


class _Named(Exception):
    """Abweisung einer Absicht mit ihrem Namen (D479 Beschluss 4)."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.name = name


def _text(value: object, key: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{key} is not text")
    return value


def _whole(value: object, key: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{key} is not an integer")
    return value


def _scope_of(store: SqliteStore, raw: object) -> bytes:
    scope = _hex(raw, 32)
    if scope not in store.all_genesis():
        raise _Named("UNKNOWN_SCOPE")
    return scope


def _current(store: SqliteStore, scope: bytes, now: int):
    """Geltende Epoche und ihre Verfassung (D479 Beschluss 3, 04 §1.1)."""
    view = scope_view(store, scope, now)
    return view, view.state.epoch, view.state.constitution_obj


def _proposal_of(store: SqliteStore, raw: object) -> tuple[bytes, Proposal]:
    digest = _hex(raw, 32)
    found = store.all_proposals().get(digest)
    if found is None:
        raise _Named("UNKNOWN_PROPOSAL")
    return digest, found


def _require_current(store: SqliteStore, proposal: Proposal, now: int):
    view, epoch, _constitution = _current(store, proposal.scope, now)
    if proposal.predecessor != epoch.epoch_id:
        raise _Named("NOT_CURRENT")
    return view, epoch


def _budget_of(store: SqliteStore, scope: bytes, author: bytes, now: int) -> tuple[int, int]:
    """Summe aus Schritt 4 von derive, über build_groups (D479 Beschluss 4, 02 §3.1)."""
    genesis = store.all_genesis()[scope]
    params = resolve_trust_params(scope=scope, genesis_obj=genesis)
    groups, _findings = build_groups(
        store.all_claims(), classify_all(store, now), scope, params.D, now
    )
    total = 0
    for (who, _subject), group in groups.items():
        if who == author:
            total += group.n_budget
    return total, params.D


def _change(store: SqliteStore, scope: bytes, change: object, now: int) -> bytes:
    """Neue Verfassung und Vorschlag aus der geltenden Epoche (D479 Beschluss 3, 04 §1.1, 04 §2.4, 04 §3.5)."""
    if not isinstance(change, dict) or len(change) != 1 or not set(change) <= {"add", "remove", "set"}:
        raise _Named("INVALID_CHANGE")
    _view, epoch, constitution = _current(store, scope, now)
    if not isinstance(constitution, dict) or not isinstance(constitution.get("participants"), list):
        raise _Named("INVALID_CHANGE")
    updated = dict(constitution)
    if "add" in change:
        key = _hex(change["add"], 32)
        if key in updated["participants"]:
            raise _Named("ALREADY_PARTICIPANT")
        updated["participants"] = sorted([*updated["participants"], key])
    elif "remove" in change:
        key = _hex(change["remove"], 32)
        if key not in updated["participants"]:
            raise _Named("NOT_PARTICIPANT")
        remaining = [item for item in updated["participants"] if item != key]
        if not remaining:
            raise _Named("EMPTY_PARTICIPANTS")
        updated["participants"] = remaining
    else:
        spec = change["set"]
        if not isinstance(spec, dict) or set(spec) != {"field", "text"}:
            raise _Named("INVALID_CHANGE")
        field = _text(spec["field"], "field")
        text = _text(spec["text"], "text")
        if field in _RESERVED:
            raise _Named("RESERVED_FIELD")
        current = constitution.get(field)
        if current is not None and not isinstance(current, str):
            raise _Named("RESERVED_FIELD")
        updated[field] = text
    digest = constitution_hash(updated)
    store.submit_object(ObjectKind.CONSTITUTION, cbor_canon.encode(updated))
    proposal = Proposal(scope=scope, predecessor=epoch.epoch_id, constitution_hash=digest)
    store.submit_object(
        ObjectKind.PROPOSAL,
        cbor_canon.encode(
            {0: proposal.scope, 1: proposal.predecessor, 2: proposal.constitution_hash}
        ),
    )
    return proposal.proposal_hash


def _intent_body(
    store: SqliteStore, body: Mapping[str, Any], now: int
) -> tuple[dict[str, Any], list[str]]:
    """Ableitung einer Absicht auf den Rumpf von _prepare (D479 Beschluss 2, 04 §2.1, 04 §2.2, 04 §2.3)."""
    author = _hex(_require(body, "I"), 32)
    art = _text(_require(body, "art"), "art")
    if art not in _ARTS:
        raise _Named("UNKNOWN_ART")
    warnings: list[str] = []
    fields: dict[str, Any] = {"I": author.hex()}
    if "h_prev" in body:
        fields["h_prev"] = body["h_prev"]
    if art == "accept-rules":
        scope = _scope_of(store, _require(body, "scope"))
        if "constitution" in body:
            constitution = _hex(body["constitution"], 32)
        else:
            _view, epoch, _constitution = _current(store, scope, now)
            constitution = epoch.constitution_hash
        fields.update(p=f"nuc:{scope.hex()}/accept-rules@1", J=[3, constitution.hex()], N=scope.hex())
    elif art == "propose":
        scope = _scope_of(store, _require(body, "scope"))
        proposal = _change(store, scope, _require(body, "change"), now)
        fields.update(p=f"nuc:{scope.hex()}/propose@1", J=[3, proposal.hex()], N=scope.hex())
    elif art == "vote":
        digest, proposal = _proposal_of(store, _require(body, "proposal"))
        _require_current(store, proposal, now)
        choice = _text(_require(body, "choice"), "choice")
        if choice not in {"yes", "no"}:
            raise ValueError("choice is not yes or no")
        encoded = cbor_canon.encode({0: 1 if choice == "yes" else 0})
        fields.update(
            p=f"nuc:{proposal.scope.hex()}/vote@1",
            J=[3, digest.hex()],
            v=encoded.hex(),
            N=proposal.scope.hex(),
        )
        for claim in store.all_claims():
            if (
                claim.I == author
                and claim.N == proposal.scope
                and claim.J == (3, digest)
                and is_nuc_name(claim, "vote")
            ):
                warnings.append("ALREADY_VOTED")
                break
    elif art == "ratify":
        digest, proposal = _proposal_of(store, _require(body, "proposal"))
        view, _epoch = _require_current(store, proposal, now)
        tally = None
        if view.verein is not None:
            for key, result in view.verein.decisions:
                if key == digest:
                    tally = result
                    break
        if tally is None or tally.state is not TallyState.PASSED:
            raise _Named("NOT_PASSED")
        fields.update(
            p=f"nuc:{proposal.scope.hex()}/ratify@1",
            J=[3, digest.hex()],
            v=cbor_canon.encode({0: list(tally.yes)}).hex(),
            N=proposal.scope.hex(),
        )
    elif art == "vouch":
        scope = _scope_of(store, _require(body, "scope"))
        subject = _hex(_require(body, "subject"), 32)
        weight = _whole(_require(body, "n"), "n")
        expiry = _whole(_require(body, "t_exp"), "t_exp")
        total, limit = _budget_of(store, scope, author, now)
        if weight < 1 or weight > limit:
            raise _Named("INVALID_WEIGHT")
        if total + weight > limit:
            warnings.append("BUDGET_FULL")
        fields.update(
            p=f"nuc:{scope.hex()}/vouch@1",
            J=[1, subject.hex()],
            v=cbor_canon.encode({0: weight}).hex(),
            N=scope.hex(),
            t_exp=expiry,
        )
    elif art == "obligation":
        scope = _scope_of(store, _require(body, "scope"))
        creditor = _hex(_require(body, "creditor"), 32)
        amount = _whole(_require(body, "amount"), "amount")
        unit = _text(_require(body, "unit"), "unit").encode("utf-8")
        fields.update(
            p=f"nuc:{scope.hex()}/obligation@1",
            J=[1, creditor.hex()],
            v=cbor_canon.encode({0: amount, 1: unit}).hex(),
            N=scope.hex(),
        )
    else:
        digest = _hex(_require(body, "obligation"), 32)
        obligation = store.get(digest)
        if obligation is None or not is_nuc_name(obligation, "obligation") or obligation.N is None:
            raise _Named("UNKNOWN_OBLIGATION")
        if author != obligation.J[1]:
            raise _Named("NOT_CREDITOR")
        fields.update(
            p=f"nuc:{obligation.N.hex()}/receipt@1",
            J=[2, digest.hex()],
            N=obligation.N.hex(),
        )
    return fields, warnings


class _Forked(Exception):
    """Mehr als eine Spitze (D476 Beschluss 3)."""


class _PayloadTooLarge(Exception):
    """Rumpf über einem MiB (D476 Beschluss 5)."""


class _Missing(Exception):
    """Unbekannter Pfad, fehlender Genesis oder fehlender Seed."""


_STATIC = Path(__file__).resolve().parent / "static"
_APP_HEADERS = (
    ("Content-Security-Policy", "default-src 'self'; frame-ancestors 'none'"),
    ("X-Content-Type-Options", "nosniff"),
    ("Cache-Control", "no-store"),
)
_MEDIA = {
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".json": "application/json",
}


def _static_at_start() -> dict[str, Path]:
    """Namen, die beim Start in static/ liegen (D481 Beschluss 5)."""
    return {path.name: path for path in _STATIC.iterdir() if path.is_file()}


def _handler(
    store: SqliteStore, clock: Callable[[], int], files: Mapping[str, Path]
) -> type[BaseHTTPRequestHandler]:
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
            except _Named as exc:
                self._send(400, exc.name)
            except VerifierError as exc:
                self._send(400, type(exc).__name__)
            except ValueError as exc:
                self._send(400, str(exc))
            except Exception as exc:
                self._send(500, type(exc).__name__)

        def _send_file(self, file: Path) -> None:
            """Startseite und /app/ (D481 Beschluss 5, D477 Beschluss 1)."""
            payload = file.read_bytes()
            self.close_connection = True
            self.send_response(200)
            self.send_header("Content-Type", _MEDIA[file.suffix])
            self.send_header("Content-Length", str(len(payload)))
            for key, value in _APP_HEADERS:
                self.send_header(key, value)
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(payload)

        def _route(self, post: bool) -> None:
            path = self.path.split("?", 1)[0]
            if not post and path == "/":
                self._send_file(files["index.html"])
                return
            if not post and path.startswith("/app/"):
                found = files.get(path[len("/app/") :])
                if found is None:
                    raise _Missing()
                self._send_file(found)
                return
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
            if not post and path.startswith("/proposals/"):
                scope = _hex(path[len("/proposals/") :], 32)
                if scope not in store.all_genesis():
                    raise _Missing()
                self._send(200, proposals_view(store, scope, clock()))
                return
            if not post and path.startswith("/tasks/"):
                identity = _hex(path[len("/tasks/") :], 32)
                self._send(200, [_task_json(t) for t in tasks_view(store, identity, clock())])
                return
            if not post and path == "/names":
                self._send(200, _names(store))
                return
            if not post and path.startswith("/objects/"):
                found = store.object_at(_hex(path[len("/objects/") :], 32))
                if found is None:
                    raise _Missing()
                self._send(200, {"kind": found[0], "data": found[1]})
                return
            if post and path in {
                "/objects",
                "/claims",
                "/prepare",
                "/submit",
                "/sim/sign",
                "/intent",
                "/sim/intent",
                "/names",
            }:
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
                if path == "/intent":
                    fields, warnings = _intent_body(store, body, clock())
                    prepared = _prepare(store, fields, clock)
                    answered = _prepared_body(prepared)
                    answered["warnings"] = warnings
                    self._send(200, answered)
                    return
                if path == "/names":
                    name = _require(body, "name")
                    if not isinstance(name, str) or not 1 <= len(name) <= 64:
                        raise ValueError("name is not 1 to 64 characters")
                    store.add_name(_hex(_require(body, "I"), 32), name)
                    self._send(200, {})
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
                if path == "/sim/intent":
                    fields, warnings = _intent_body(
                        store,
                        {key: value for key, value in body.items() if key != "h_prev"},
                        clock(),
                    )
                    prepared = _prepare(store, fields, clock)
                    sigma = sign(Ed25519PrivateKey.from_private_bytes(seed), prepared)
                    cid = _submit(store, core_bytes(prepared), sigma)
                    self._send(200, {"claim_id": cid, "warnings": warnings})
                    return
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
            """Antwort und Schließen der Verbindung (D477 Beschluss 1)."""
            encoded = json.dumps(json_value(payload)).encode("utf-8")
            self.close_connection = True
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(encoded)

    return Handler


def _names(store: SqliteStore) -> list[dict[str, object]]:
    """Adressbuch: Schlüssel, Name, simuliert (D479 Beschluss 5, D471 Beschluss 3)."""
    named = store.all_names()
    simulated = store.sim_pubs()
    rows = []
    for pub in sorted(set(named) | simulated):
        rows.append({"I": pub, "name": named.get(pub), "simulated": pub in simulated})
    return rows


# Feldname, unter dem TaskView.detail je Art erscheint (D484 Beschluss 1).
_TASK_DETAIL_FIELD = {
    "CONFIRM_RULES": "constitution",
    "VOTE": "proposal",
    "RATIFY": "proposal",
    "CONTRIBUTION_OPEN": "obligation",
    "RECEIPT": "obligation",
}


def _task_json(task: TaskView) -> dict[str, object]:
    body: dict[str, object] = {"scope": task.scope, "art": task.art}
    body[_TASK_DETAIL_FIELD[task.art]] = task.detail
    return body


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
    server = HTTPServer(
        (_HOST, port), _handler(store, clock or _clock_default, _static_at_start())
    )
    try:
        if bound is not None:
            bound(server)
        server.serve_forever()
    finally:
        server.server_close()
        store.close()
