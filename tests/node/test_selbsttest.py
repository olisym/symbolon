"""Der Selbsttest der Seite läuft in ``make check`` (D549, D555).

Node lädt ``selbsttest.js`` als Modul und fährt ``run`` über ``vektoren.json`` mit
``globalThis.crypto.subtle``, wie die Seite im Browser. Fehlt Node, ist das ein Fehler, kein
übersprungener Test. Die Zahl der Fälle ist eine Golden Number: sie ändert sich nur mit einem
Auftrag, der sie nennt (D555 Beschluss 2).
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

_STATIC = Path(__file__).resolve().parents[2] / "symbolon" / "node" / "static"

_FAELLE = 380

_SKRIPT = """
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
const dir = process.argv[1];
const { run } = await import(pathToFileURL(dir + "/selbsttest.js").href);
const vectors = JSON.parse(readFileSync(dir + "/vektoren.json", "utf8"));
const results = await run(vectors, globalThis.crypto.subtle);
process.stdout.write(JSON.stringify(results));
"""


def test_selbsttest() -> None:
    """Jeder Fall des Selbsttests besteht (D555 Beschluss 1)."""
    node = shutil.which("node")
    assert node is not None, "Node fehlt; der Selbsttest der Seite braucht es (D555)"
    lauf = subprocess.run(
        [node, "--input-type=module", "-e", _SKRIPT, str(_STATIC)],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert lauf.returncode == 0, lauf.stderr
    ergebnisse = json.loads(lauf.stdout)
    assert len(ergebnisse) == _FAELLE, len(ergebnisse)
    rot = [f"{fall['expect']}: {fall['detail']}" for fall in ergebnisse if fall["ok"] is not True]
    assert rot == [], rot
