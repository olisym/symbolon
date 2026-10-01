"""Trickle nach RFC 6206, Abschnitt 4.2, und die Zeiten nach der Bitrate (D611 Beschluss 1 und 2)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Zeiten:
    """Frist für den Link, Frist für eine Antwort ohne Fortschritt, kleinstes Intervall
    (D611 Beschluss 2)."""

    link: float
    antwort: float
    imin: float


def zeiten(bitrate: float | None) -> Zeiten:
    """Link, Antwort und ``imin``: ``72000/bitrate``, ``144000/bitrate``, ``72000/bitrate``.

    Nie unter 10, 15 und 10 Sekunden. Ohne Bitrate oder bei ``bitrate <= 0`` diese Untergrenzen;
    bei 1200 bit/s die Werte aus D610 (D611 Beschluss 2).
    """
    if bitrate is None or bitrate <= 0:
        return Zeiten(10.0, 15.0, 10.0)
    return Zeiten(
        max(10.0, 72000 / bitrate),
        max(15.0, 144000 / bitrate),
        max(10.0, 72000 / bitrate),
    )


class Trickle:
    """Ein Intervall, ein Zeitpunkt in der zweiten Hälfte, Unterdrückung ab ``k`` (D611 Beschluss 1).

    Abgelaufen verdoppelt es bis ``imin * 2**doppel``. Ein neuer eigener Stand beginnt ein
    Intervall mit ``imin``, wenn das laufende länger ist (RFC 6206, Abschnitt 4.2).
    """

    def __init__(self, imin: float, doppel: int, k: int, jetzt: float, zufall) -> None:
        if imin <= 0 or doppel < 0 or k < 1:
            raise ValueError("imin > 0, doppel >= 0 und k >= 1")
        self.imin = imin
        self.imax = imin * 2**doppel
        self.k = k
        self.zufall = zufall
        self._intervall(imin, jetzt)

    def _intervall(self, laenge: float, jetzt: float) -> None:
        """Neues Intervall: Zähler auf 0, Zeitpunkt in der zweiten Hälfte (RFC 6206, Abschnitt 4.2)."""
        self.laenge = laenge
        self.beginn = jetzt
        self.zeitpunkt = jetzt + self.zufall.uniform(laenge / 2, laenge)
        self.gehoert = 0
        self._gemeldet = False

    def gleich(self) -> None:
        """Ein gehörter gleicher Stand zählt für ``k`` (D611 Beschluss 1)."""
        self.gehoert += 1

    def neu(self, jetzt: float) -> None:
        """Beginnt bei ``jetzt`` ein Intervall mit ``imin``, wenn das laufende länger ist.

        Sonst nichts (RFC 6206, Abschnitt 4.2, D611 Beschluss 1).
        """
        if self.laenge > self.imin:
            self._intervall(self.imin, jetzt)

    def ankuendigen(self, jetzt: float) -> bool:
        """Einmal je Intervall, beim ersten Aufruf ab dem Zeitpunkt, und nur wenn ``gehoert < k``.

        Ist das Intervall abgelaufen, beginnt bei ``jetzt`` eines mit doppelter Länge, höchstens
        ``imax``. Wurde darin noch nicht gefragt und gilt ``gehoert < k``, holt dieser Aufruf
        die Ankündigung nach (RFC 6206, Abschnitt 4.2, D611 Beschluss 1, D623 Beschluss 1).
        """
        if jetzt >= self.beginn + self.laenge:
            nachholen = not self._gemeldet and self.gehoert < self.k
            self._intervall(min(2 * self.laenge, self.imax), jetzt)
            if nachholen:
                return True
        if self._gemeldet or jetzt < self.zeitpunkt:
            return False
        self._gemeldet = True
        return self.gehoert < self.k
