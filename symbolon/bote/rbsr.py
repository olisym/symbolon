"""Abgleich nach Bereichen: Form, Parameter und Ablauf (D617 Beschluss 2, 3 und 4)."""

from __future__ import annotations

import hashlib
from bisect import bisect_left
from collections import deque

from symbolon import cbor_canon

ART_OBJEKT = 0
ART_CLAIM = 1
SKIP = 0
FP = 1
IDS = 2
FEHLT = 3
TEILUNG = 4
LISTE = 3
FP_LAENGE = 16
RAHMEN = 380
ANFRAGE = 190
RUNDEN = 64

_SCHLUESSEL = 33
_Bereich = tuple[bytes, bytes | None]
_Teil = tuple[bytes | None, int, object]


class Formwidrig(ValueError):
    """Eine Nachricht hat nicht die Form aus D617 Beschluss 2."""


def schluessel(claims: list[bytes], objekte: list[bytes]) -> list[bytes]:
    """Objekte vor Claims, die Art als Byte vor der Kennung (D617 Beschluss 2)."""
    eintraege = [bytes([ART_OBJEKT]) + objekt for objekt in objekte]
    eintraege.extend(bytes([ART_CLAIM]) + claim for claim in claims)
    eintraege.sort()
    return eintraege


def fingerabdruck(schluessel: list[bytes]) -> bytes:
    """SHA-256 über die Anzahl und die Schlüssel, die ersten 16 Byte (D617 Beschluss 2)."""
    digest = hashlib.sha256(len(schluessel).to_bytes(8, "big"))
    for eintrag in schluessel:
        digest.update(eintrag)
    return digest.digest()[:FP_LAENGE]


def kodieren(teile: list[_Teil]) -> bytes:
    """Kanonisches CBOR einer nicht leeren Teileliste (D617 Beschluss 2)."""
    return cbor_canon.encode([[grenze, modus, inhalt] for grenze, modus, inhalt in teile])


def lesen(roh: object, *, vom_boten: bool) -> list[_Teil]:
    """Jede Regel aus D617 Beschluss 2. Ein Fehler beim Kanon-Prüfen ist Formwidrig."""
    if type(roh) is not bytes or not roh or len(roh) > RAHMEN:
        raise Formwidrig()
    try:
        kanonisch = cbor_canon.is_canonical(roh)
    except Exception as exc:
        raise Formwidrig() from exc
    if not kanonisch:
        raise Formwidrig()
    wert = cbor_canon.decode(roh)
    if not isinstance(wert, list) or not wert:
        raise Formwidrig()
    teile: list[_Teil] = []
    unter = b""
    vorher: bytes | None = None
    for index, teil in enumerate(wert):
        if not isinstance(teil, list) or len(teil) != 3:
            raise Formwidrig()
        grenze, modus, inhalt = teil
        if grenze is None:
            if index != len(wert) - 1:
                raise Formwidrig()
        elif type(grenze) is not bytes or not 1 <= len(grenze) <= _SCHLUESSEL:
            raise Formwidrig()
        elif vorher is not None and grenze <= vorher:
            raise Formwidrig()
        teile.append((grenze, _modus(modus), _inhalt(modus, inhalt, unter, grenze, vom_boten)))
        vorher = grenze if grenze is not None else vorher
        unter = grenze if grenze is not None else unter
    return teile


def antworten(schluessel: list[bytes], nachricht: list[_Teil]) -> list[_Teil]:
    """Zustandslos, Teil für Teil; ``FEHLT`` bis zum Rahmen (D617 Beschluss 4)."""
    keys = sorted(schluessel)
    antwort: list[_Teil] = []
    unter = b""
    for ober, modus, inhalt in nachricht:
        if not _beantworten(antwort, keys, unter, ober, modus, inhalt):
            break
        if ober is None:
            break
        unter = ober
    return antwort


class Abgleich:
    """Warteschlange offener Bereiche; je Runde höchstens ``ANFRAGE`` Byte (D617 Beschluss 4)."""

    def __init__(self, schluessel: list[bytes]) -> None:
        self._keys = sorted(schluessel)
        self._haben = set(self._keys)
        self._offen: deque[_Bereich] = deque([(b"", None)])
        self.fehlt: set[bytes] = set()
        self.runden = 0
        self._unterwegs: list[_Bereich] = []

    def naechste(self) -> bytes | None:
        """Die nächste Anfrage, ``None`` nach ``RUNDEN`` oder ohne offene Bereiche."""
        if self.runden >= RUNDEN or not self._offen:
            return None
        teile, unterwegs = _anfrage(self._keys, self._offen)
        if not teile:
            return None
        self._unterwegs = unterwegs
        self.runden += 1
        return kodieren(teile)

    def auswerten(self, teile: list[_Teil]) -> None:
        """Schliesst, was die Antwort trägt; Unbeantwortetes bleibt offen (D617 Beschluss 4)."""
        pos: bytes | None = b""
        neu: list[_Bereich] = []
        for ober, modus, inhalt in teile:
            if pos is None:
                break
            _aufnehmen(self, pos, ober, modus, inhalt, neu)
            pos = ober
        if pos is not None:
            for unter, ober in self._unterwegs:
                if ober is not None and ober <= pos:
                    continue
                neu.append((pos, ober) if unter < pos else (unter, ober))
        for bereich in reversed(neu):
            self._offen.appendleft(bereich)


def _modus(modus: object) -> int:
    if type(modus) is not int or modus not in (SKIP, FP, IDS, FEHLT):
        raise Formwidrig()
    return modus


def _inhalt(
    modus: int, inhalt: object, unter: bytes, ober: bytes | None, vom_boten: bool
) -> object:
    if modus == SKIP:
        if inhalt is not None:
            raise Formwidrig()
        return None
    if modus == FP:
        if type(inhalt) is not bytes or len(inhalt) != FP_LAENGE:
            raise Formwidrig()
        return inhalt
    if modus == FEHLT and vom_boten:
        raise Formwidrig()
    if modus not in (IDS, FEHLT):
        raise Formwidrig()
    return _liste(inhalt, unter, ober)


def _liste(inhalt: object, unter: bytes, ober: bytes | None) -> list[bytes]:
    if not isinstance(inhalt, list):
        raise Formwidrig()
    vorher: bytes | None = None
    erg: list[bytes] = []
    for key in inhalt:
        if (
            type(key) is not bytes
            or len(key) != _SCHLUESSEL
            or key[0] not in (ART_OBJEKT, ART_CLAIM)
        ):
            raise Formwidrig()
        if vorher is not None and key <= vorher:
            raise Formwidrig()
        if key < unter or (ober is not None and key >= ober):
            raise Formwidrig()
        vorher = key
        erg.append(key)
    return erg


def _schnitt(keys: list[bytes], unter: bytes, ober: bytes | None) -> list[bytes]:
    anfang = bisect_left(keys, unter)
    ende = len(keys) if ober is None else bisect_left(keys, ober)
    return keys[anfang:ende]


def _grenze(links: bytes, rechts: bytes) -> bytes:
    """Kürzester Präfix von ``rechts``, der grösser ist als ``links`` (D617 Beschluss 4)."""
    stelle = 0
    while links[stelle] == rechts[stelle]:
        stelle += 1
    return rechts[: stelle + 1]


def _gruppen(keys: list[bytes], teilung: int) -> list[list[bytes]]:
    if not keys:
        return []
    anzahl = min(teilung, len(keys))
    basis, rest = divmod(len(keys), anzahl)
    gruppen: list[list[bytes]] = []
    cursor = 0
    for index in range(anzahl):
        groesse = basis + (1 if index < rest else 0)
        gruppen.append(keys[cursor : cursor + groesse])
        cursor += groesse
    return gruppen


def _teilen(
    keys: list[bytes], ober: bytes | None, teilung: int, liste: int
) -> list[_Teil]:
    """Gleiche Anzahl; bis ``liste`` Schlüssel als ``IDS``, sonst ``FP`` (D617 Beschluss 4)."""
    if not keys:
        return [(ober, IDS, [])]
    gruppen = _gruppen(keys, teilung)
    teile: list[_Teil] = []
    for index, gruppe in enumerate(gruppen):
        if index + 1 == len(gruppen):
            bound: bytes | None = ober
        else:
            bound = _grenze(gruppe[-1], gruppen[index + 1][0])
        if len(gruppe) <= liste:
            teile.append((bound, IDS, gruppe))
        else:
            teile.append((bound, FP, fingerabdruck(gruppe)))
    return teile


def _passt(bisher: list[_Teil], neu: list[_Teil]) -> bool:
    return len(kodieren(bisher + neu)) <= RAHMEN


def _anfuegen(antwort: list[_Teil], teile: list[_Teil]) -> bool:
    if _passt(antwort, teile):
        antwort.extend(teile)
        return True
    return False


def _prefix(antwort: list[_Teil], teile: list[_Teil]) -> None:
    for teil in teile:
        if not _passt(antwort, [teil]):
            return
        antwort.append(teil)


def _substanz(teile: list[_Teil]) -> bool:
    return any(modus != SKIP for _grenze, modus, _inhalt in teile)


def _geteilt(
    antwort: list[_Teil],
    keys: list[bytes],
    unter: bytes,
    ober: bytes | None,
    teilung: int,
    liste: int,
) -> bool:
    """Passt der Teil nicht, endet die Antwort; nur ``SKIP`` heisst knapp (D617 Beschluss 4)."""
    teile = _teilen(_schnitt(keys, unter, ober), ober, teilung, liste)
    if _anfuegen(antwort, teile):
        return True
    erstes_passt = bool(teile) and _passt(antwort, teile[:1])
    if _substanz(antwort) or erstes_passt:
        _prefix(antwort, teile)
        return False
    knapp = _teilen(_schnitt(keys, unter, ober), ober, 2, 1)
    if _anfuegen(antwort, knapp):
        return True
    _prefix(antwort, knapp)
    return False


def _fehlt_teile(
    missing: list[bytes], anzahl: int, eigene: list[bytes], ober: bytes | None
) -> list[_Teil]:
    """``FEHLT`` bis zum Trenner, der Rest des Bereichs als ``FP`` (D617 Beschluss 4)."""
    genommen = missing[:anzahl]
    if anzahl == len(missing):
        return [(ober, FEHLT, genommen)]
    letzte = genommen[-1]
    naechster = eigene[eigene.index(letzte) + 1]
    bound = _grenze(letzte, naechster)
    rest = [key for key in eigene if key >= bound]
    return [(bound, FEHLT, genommen), (ober, FP, fingerabdruck(rest))]


def _auf_ids(
    antwort: list[_Teil],
    keys: list[bytes],
    unter: bytes,
    ober: bytes | None,
    ihre: object,
) -> bool:
    eigene = _schnitt(keys, unter, ober)
    fremd = set(ihre) if isinstance(ihre, list) else set()
    missing = [key for key in eigene if key not in fremd]
    if not missing:
        return _anfuegen(antwort, [(ober, SKIP, None)])
    for anzahl in range(len(missing), 0, -1):
        teile = _fehlt_teile(missing, anzahl, eigene, ober)
        if _passt(antwort, teile):
            antwort.extend(teile)
            return True
    return _geteilt(antwort, keys, unter, ober, TEILUNG, LISTE)


def _beantworten(
    antwort: list[_Teil],
    keys: list[bytes],
    unter: bytes,
    ober: bytes | None,
    modus: int,
    inhalt: object,
) -> bool:
    if modus == SKIP:
        return _anfuegen(antwort, [(ober, SKIP, None)])
    if modus == FP:
        if fingerabdruck(_schnitt(keys, unter, ober)) == inhalt:
            return _anfuegen(antwort, [(ober, SKIP, None)])
        return _geteilt(antwort, keys, unter, ober, TEILUNG, LISTE)
    if modus == IDS:
        return _auf_ids(antwort, keys, unter, ober, inhalt)
    raise Formwidrig()


def _anfrage(
    keys: list[bytes], offen: deque[_Bereich]
) -> tuple[list[_Teil], list[_Bereich]]:
    """So viele Bereiche, wie in ``ANFRAGE`` passen; Lücken als ``SKIP`` (D617 Beschluss 4)."""
    teile: list[_Teil] = []
    unterwegs: list[_Bereich] = []
    cursor = b""
    for unter, ober in offen:
        vorschlag = list(teile)
        if unter != cursor:
            vorschlag.append((unter, SKIP, None))
        bereich = _schnitt(keys, unter, ober)
        if len(bereich) <= LISTE:
            vorschlag.append((ober, IDS, bereich))
        else:
            vorschlag.append((ober, FP, fingerabdruck(bereich)))
        if teile and len(kodieren(vorschlag)) > ANFRAGE:
            break
        teile = vorschlag
        unterwegs.append((unter, ober))
        if ober is None:
            break
        cursor = ober
    for _bereich in unterwegs:
        offen.popleft()
    return teile, unterwegs


def _aufnehmen(
    abgleich: Abgleich,
    unter: bytes,
    ober: bytes | None,
    modus: int,
    inhalt: object,
    neu: list[_Bereich],
) -> None:
    if modus == SKIP:
        return
    if modus == FP:
        if fingerabdruck(_schnitt(abgleich._keys, unter, ober)) != inhalt:
            neu.append((unter, ober))
        return
    if modus == IDS and isinstance(inhalt, list):
        for key in inhalt:
            if key not in abgleich._haben:
                abgleich.fehlt.add(key)
        return
    if modus == FEHLT and isinstance(inhalt, list):
        for key in inhalt:
            if key not in abgleich._haben:
                abgleich.fehlt.add(key)
