"""Trickle nach RFC 6206 und die Zeiten nach der Bitrate (D611 Beschluss 1 und 2)."""

from __future__ import annotations

import pytest

from symbolon.bote.kern import ankuendigung, ankuendigung_aus
from symbolon.bote.trickle import Trickle, Zeiten, zeiten


class _Mitte:
    """Ein Zufall, der immer die Mitte zieht; so liegt der Zeitpunkt bei drei Vierteln."""

    def uniform(self, unten: float, oben: float) -> float:
        return (unten + oben) / 2


def test_einmal_je_intervall() -> None:
    """Angekündigt wird einmal, zum Zeitpunkt in der zweiten Hälfte (RFC 6206, Abschnitt 4.2)."""
    t = Trickle(10.0, 3, 2, 0.0, _Mitte())
    assert [t.ankuendigen(x) for x in (0.0, 7.4, 7.5, 8.0, 9.9)] == [False, False, True, False, False]
    # Das zweite Intervall beginnt bei 10 mit 20 s, der Zeitpunkt liegt bei 25.
    assert [t.ankuendigen(x) for x in (10.0, 24.9, 25.0, 29.0)] == [False, False, True, False]


def test_verdoppeln_bis_imax() -> None:
    """Jedes abgelaufene Intervall verdoppelt, bis ``imin * 2**doppel`` (RFC 6206, Abschnitt 4.2)."""
    t = Trickle(10.0, 2, 2, 0.0, _Mitte())
    laengen = []
    jetzt = 0.0
    for _ in range(5):
        jetzt = t.beginn + t.laenge
        t.ankuendigen(jetzt)
        laengen.append(t.laenge)
    assert laengen == [20.0, 40.0, 40.0, 40.0, 40.0]
    assert t.imax == 40.0


def test_k_unterdrueckt() -> None:
    """Wer im Intervall ``k`` gleiche Stände gehört hat, schweigt."""
    t = Trickle(10.0, 3, 2, 0.0, _Mitte())
    t.gleich()
    t.gleich()
    assert t.ankuendigen(7.5) is False
    u = Trickle(10.0, 3, 2, 0.0, _Mitte())
    u.gleich()
    assert u.ankuendigen(7.5) is True


def test_neu_setzt_zurueck() -> None:
    """Ein neuer eigener Stand beginnt ein Intervall mit ``imin``, wenn das laufende länger ist."""
    t = Trickle(10.0, 3, 2, 0.0, _Mitte())
    t.ankuendigen(10.0)
    t.ankuendigen(30.0)
    assert t.laenge == 40.0
    t.neu(31.0)
    assert (t.laenge, t.beginn, t.zeitpunkt) == (10.0, 31.0, 38.5)
    assert t.ankuendigen(38.5) is True


def test_neu_bei_imin_nichts() -> None:
    """Ist das laufende Intervall schon ``imin``, ändert ein neuer Stand nichts (RFC 6206, Abschnitt 4.2)."""
    t = Trickle(10.0, 3, 2, 0.0, _Mitte())
    t.gleich()
    t.neu(3.0)
    assert (t.laenge, t.beginn, t.zeitpunkt, t.gehoert) == (10.0, 0.0, 7.5, 1)


@pytest.mark.parametrize(("imin", "doppel", "k"), [(0.0, 3, 2), (10.0, -1, 2), (10.0, 3, 0)])
def test_werte(imin, doppel, k) -> None:
    with pytest.raises(ValueError):
        Trickle(imin, doppel, k, 0.0, _Mitte())


@pytest.mark.parametrize(
    ("bitrate", "erwartet"),
    [
        (1200, Zeiten(60.0, 120.0, 60.0)),
        (2400, Zeiten(30.0, 60.0, 30.0)),
        (20000, Zeiten(10.0, 15.0, 10.0)),
        (None, Zeiten(10.0, 15.0, 10.0)),
        (0, Zeiten(10.0, 15.0, 10.0)),
    ],
)
def test_zeiten(bitrate, erwartet) -> None:
    """Bei 1200 bit/s die Werte aus D610, nie unter 10, 15 und 10 s (D611 Beschluss 2)."""
    assert zeiten(bitrate) == erwartet


@pytest.mark.parametrize(
    ("app_data", "erwartet"),
    [
        (bytes(range(32)) + bytes([0, 0, 1, 2]), (bytes(range(32)), 258)),
        (bytes(36), (bytes(32), 0)),
        (bytes(32) + b"\xff" * 4, (bytes(32), 2**32 - 1)),
        (bytes(range(32)), None),
        (None, None),
        (b"", None),
        (bytes(35), None),
        (bytes(37), None),
        ("00" * 36, None),
        (bytearray(36), None),
    ],
)
def test_ankuendigung_aus(app_data, erwartet) -> None:
    """Nur genau 36 Bytes sind eine Ankündigung, die alte Form mit 32 nicht; alles andere ist
    formwidrig und macht keinen Nachbarn fällig (D619 Beschluss 1)."""
    assert ankuendigung_aus(app_data) == erwartet


def test_ankuendigung() -> None:
    """Hin und zurück; eine Zahl über vier Byte wird gekappt (D619 Beschluss 1)."""
    stand = bytes(range(32))
    assert ankuendigung(stand, 258) == stand + bytes([0, 0, 1, 2])
    assert ankuendigung_aus(ankuendigung(stand, 7)) == (stand, 7)
    assert ankuendigung_aus(ankuendigung(stand, 2**40)) == (stand, 2**32 - 1)
