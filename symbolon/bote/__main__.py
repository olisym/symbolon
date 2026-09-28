"""Start des Boten: ``python -m symbolon.bote`` (D584 Beschluss 4, D585 Beschluss 1)."""

from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> None:
    """Zuerst die Adresse, dann der Bote; ``RNS`` erst nach dem Parsen (D584 Beschluss 4)."""
    parser = argparse.ArgumentParser(prog="python -m symbolon.bote")
    parser.add_argument("knoten", nargs="?", help="URL des eigenen Knotens")
    parser.add_argument("--identitaet", required=True, metavar="DATEI")
    parser.add_argument("--rns", metavar="VERZEICHNIS")
    parser.add_argument(
        "--nachbar", action="extend", nargs="+", type=bytes.fromhex, default=[], metavar="HEX"
    )
    parser.add_argument("--takt", type=float, default=2.0, metavar="SEKUNDEN")
    parser.add_argument("--nur-adresse", action="store_true")
    args = parser.parse_args(argv)
    try:
        from symbolon.bote.reticulum import adresse, identitaet, laufen

        ident = identitaet(args.identitaet)
        print(f"adresse {adresse(ident).hex()}", flush=True)
        if args.nur_adresse:
            return
        if args.knoten is None or args.rns is None:
            parser.error("knoten und --rns sind verlangt")
        laufen(
            args.knoten,
            args.rns,
            ident,
            args.nachbar,
            args.takt,
            lambda zeile: print(zeile, flush=True),
        )
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
