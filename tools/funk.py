"""Geteilter Funkkanal: einer sendet zur Zeit, Sendezeit nach der Bitrate (D611 Beschluss 4).

Ein Paket geht an alle anderen Teilnehmer, nie an den Sender. Verlust je Empfänger mit festem
Samen. Die Sendezeit ist die Zahl der Bytes mal 8 geteilt durch die Bitrate (D607 Beschluss 1).
"""

from __future__ import annotations

import argparse
import queue
import random
import socket
import threading
import time


class Kanal:
    """Sendezeit, einer zur Zeit, Verlust mit Samen, nie an den Sender (D611 Beschluss 4)."""

    def __init__(self, bitrate: float, verlust: float, samen: int) -> None:
        if bitrate <= 0 or verlust < 0 or verlust >= 1:
            raise ValueError("bitrate > 0 und verlust in [0, 1)")
        self.bitrate = bitrate
        self.verlust = verlust
        self._zufall = random.Random(samen)
        self._ende = 0.0
        self.pakete = 0
        self.bytes = 0
        self.ankuendigungen = 0
        self.verloren = 0

    def senden(self, jetzt: float, daten: bytes) -> float:
        """Beginn ist ``max(jetzt, Ende des vorigen)``; Ende plus Bytes mal 8 durch die Bitrate.

        Zählt Pakete, Bytes und Ankündigungen (``daten[0] & 0b11 == 0b01``). Gibt das Ende zurück
        (D611 Beschluss 4).
        """
        beginn = max(jetzt, self._ende)
        ende = beginn + len(daten) * 8 / self.bitrate
        self._ende = ende
        self.pakete += 1
        self.bytes += len(daten)
        if daten and daten[0] & 0b11 == 0b01:
            self.ankuendigungen += 1
        return ende

    def empfaenger(self, von: int, anzahl: int) -> list[int]:
        """Jeder Index ausser ``von``, aufsteigend, ausser der Zufall liegt unter ``verlust``.

        Jeder Verlust zählt (D611 Beschluss 4, D610 Befund 1).
        """
        hoeren: list[int] = []
        for ziel in range(anzahl):
            if ziel == von:
                continue
            if self._zufall.random() < self.verlust:
                self.verloren += 1
            else:
                hoeren.append(ziel)
        return hoeren

    def bericht(self) -> str:
        """Eine Zeile mit Paketen, Bytes, Verlusten und Ankündigungen (D611 Beschluss 4)."""
        return (
            f"funk pakete={self.pakete} bytes={self.bytes} "
            f"verloren={self.verloren} ankuendigungen={self.ankuendigungen}"
        )


def main() -> None:
    """Je Eingang ein Teilnehmer; ein Paket geht nach seinem Ende an die Empfänger (D611 Beschluss 4).

    ``--eingaenge`` und ``--teilnehmer`` sind gleich viele Ports, sonst ein Fehler von argparse.
    Voreinstellung: 1200 bit/s, 5 % Verlust, Samen 0, Bericht alle 10 s.
    """
    parser = argparse.ArgumentParser(prog="python -m tools.funk")
    parser.add_argument("--eingaenge", type=int, nargs="+", required=True)
    parser.add_argument("--teilnehmer", type=int, nargs="+", required=True)
    parser.add_argument("--bitrate", type=float, default=1200)
    parser.add_argument("--verlust", type=float, default=0.05)
    parser.add_argument("--samen", type=int, default=0)
    parser.add_argument("--bericht", type=float, default=10)
    args = parser.parse_args()
    if len(args.eingaenge) != len(args.teilnehmer):
        parser.error("--eingaenge und --teilnehmer brauchen gleich viele Ports")
    kanal = Kanal(args.bitrate, args.verlust, args.samen)
    sperre = threading.Lock()
    angekommen: queue.Queue[tuple[float, int, bytes]] = queue.Queue()
    socken = []
    for index, port in enumerate(args.eingaenge):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("127.0.0.1", port))
        socken.append(sock)

        def empfangen(sock=sock, index=index) -> None:
            while True:
                daten = sock.recvfrom(65535)[0]
                angekommen.put((time.monotonic(), index, daten))

        threading.Thread(target=empfangen, daemon=True).start()
    ausgang = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def berichten() -> None:
        while True:
            time.sleep(args.bericht)
            with sperre:
                zeile = kanal.bericht()
            print(zeile, flush=True)

    threading.Thread(target=berichten, daemon=True).start()
    anzahl = len(args.teilnehmer)
    while True:
        jetzt, von, daten = angekommen.get()
        with sperre:
            ende = kanal.senden(jetzt, daten)
            ziele = kanal.empfaenger(von, anzahl)
        warten = ende - time.monotonic()
        if warten > 0:
            time.sleep(warten)
        for ziel in ziele:
            ausgang.sendto(daten, ("127.0.0.1", args.teilnehmer[ziel]))


if __name__ == "__main__":
    main()
