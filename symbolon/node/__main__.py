"""Bedient einen Bestand, bis der Lauf unterbrochen wird (D476, D479 Beschluss 1)."""

from __future__ import annotations

import argparse
import time
from collections.abc import Callable

from symbolon.node.api import serve


def uhr_ab(start: int) -> Callable[[], int]:
    """Weltuhr: T plus die ganzen Sekunden seit dem Start, monoton (D479 Beschluss 1)."""
    begun = time.monotonic()

    def clock() -> int:
        return start + int(time.monotonic() - begun)

    return clock


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m symbolon.node")
    parser.add_argument("datei")
    parser.add_argument("--port", type=int, default=8470)
    parser.add_argument("--uhr-ab", type=int, default=None)
    args = parser.parse_args()
    clock = None if args.uhr_ab is None else uhr_ab(args.uhr_ab)
    try:
        serve(args.datei, port=args.port, clock=clock)
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
