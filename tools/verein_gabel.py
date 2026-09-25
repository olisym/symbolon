"""Brunos Gabelung über die Schnittstelle des S-Node (D488 Beschluss 2, szenario-verein §5.2)."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from symbolon.atom import claim_from_bytes, sign
from tools.verein import build
from tools.verein_node import _seed


class GabelFehler(Exception):
    """Abbruch mit einem Satz, bevor oder statt eingeliefert wird (D488 Beschluss 2)."""


def _call(base: str, method: str, path: str, payload: object = None) -> object:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(base + path, data=data, method=method)
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        raise GabelFehler(
            f"Der S-Node weist {method} {path} ab: {exc.code} {exc.read().decode(errors='replace')}."
        ) from exc
    except (urllib.error.URLError, OSError) as exc:
        raise GabelFehler(f"Der S-Node unter {base} ist nicht erreichbar.") from exc


def _antrag_waehlen(base: str, scope: bytes, antrag: bytes | None) -> bytes:
    """Der einzige Antrag auf PENDING oder der genannte (D488 Beschluss 2, D484 Beschluss 2)."""
    rows = _call(base, "GET", f"/proposals/{scope.hex()}")
    pending = [row["proposal"] for row in rows if row["state"] == "PENDING"]
    if antrag is not None:
        if antrag.hex() not in pending:
            genannt = ", ".join(pending) or "keiner"
            raise GabelFehler(
                f"Der Antrag {antrag.hex()} steht nicht auf PENDING; auf PENDING: {genannt}."
            )
        return antrag
    if not pending:
        raise GabelFehler("Kein Antrag steht auf PENDING.")
    if len(pending) > 1:
        raise GabelFehler(
            f"Mehrere Anträge stehen auf PENDING, einer ist mit --antrag zu nennen: "
            f"{', '.join(pending)}."
        )
    return bytes.fromhex(pending[0])


def gabeln(base: str, antrag: bytes | None = None) -> tuple[bytes, bytes]:
    """Ja und Nein Brunos auf dasselbe h_prev, beide eingeliefert (D488 Beschluss 2, 01 §4).

    Beide Kerne werden über ``POST /intent`` vorbereitet, bevor einer eingeliefert wird; sonst
    schlüge der S-Node für den zweiten den ersten als Vorgänger vor (D476 Beschluss 3).
    Gibt die ``claim_id`` von Ja und Nein zurück.
    """
    world = build()
    bruno = world.bruno.pub
    digest = _antrag_waehlen(base, world.ex.N_gov, antrag)
    prepared = [
        _call(
            base,
            "POST",
            "/intent",
            {"I": bruno.hex(), "art": "vote", "proposal": digest.hex(), "choice": choice},
        )
        for choice in ("yes", "no")
    ]
    if prepared[0]["h_prev"] != prepared[1]["h_prev"]:
        raise GabelFehler("Die beiden Kerne tragen nicht dasselbe h_prev; nichts eingeliefert.")
    sk = Ed25519PrivateKey.from_private_bytes(_seed(world.bruno))
    ids: list[bytes] = []
    for answer in prepared:
        core = bytes.fromhex(answer["core"])
        sigma = sign(sk, claim_from_bytes(core))
        submitted = _call(base, "POST", "/submit", {"core": core.hex(), "sigma": sigma.hex()})
        ids.append(bytes.fromhex(submitted["claim_id"]))
    return ids[0], ids[1]


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m tools.verein_gabel")
    parser.add_argument("--port", type=int, default=8470)
    parser.add_argument("--antrag", default=None)
    args = parser.parse_args()
    base = f"http://127.0.0.1:{args.port}"
    try:
        antrag = None if args.antrag is None else bytes.fromhex(args.antrag)
    except ValueError:
        print(f"verein_gabel: --antrag ist kein Hex: {args.antrag}.", file=sys.stderr)
        return 2
    try:
        ja, nein = gabeln(base, antrag)
    except GabelFehler as exc:
        print(f"verein_gabel: {exc}", file=sys.stderr)
        return 1
    print(ja.hex())
    print(nein.hex())
    print(f"Die Oberfläche unter {base}/ zeigt die Gabelung im Abschnitt „Widersprüche“.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
