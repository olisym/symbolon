"""Bedient einen Bestand, bis der Lauf unterbrochen wird (D476)."""

from __future__ import annotations

import argparse

from symbolon.node.api import serve


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m symbolon.node")
    parser.add_argument("datei")
    parser.add_argument("--port", type=int, default=8470)
    args = parser.parse_args()
    try:
        serve(args.datei, port=args.port)
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
