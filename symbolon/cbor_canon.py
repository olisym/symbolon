"""Kanonische CBOR-Enkodierung und Re-Serialisierungs-Check (01 §3)."""

from __future__ import annotations

import cbor2


def encode(obj: object) -> bytes:
    """Deterministische CBOR-Kodierung (RFC 8949 Core Deterministic Encoding)."""
    return cbor2.dumps(obj, canonical=True)


def decode(data: bytes) -> object:
    """CBOR dekodieren."""
    return cbor2.loads(data)


def reserialize(data: bytes) -> bytes:
    """Empfangene Bytes dekodieren und kanonisch re-enkodieren."""
    return encode(decode(data))


def is_canonical(data: bytes) -> bool:
    """True gdw. data bereits kanonisch kodiert ist."""
    return data == reserialize(data)


def keys_admissible(data: bytes) -> bool:
    """Jeder Map-Schlüssel ist ungetaggter Integer, bstr oder tstr (02 §3.1).

    Geht über die Bytes, nicht über das dekodierte ``dict``. Defekte Bytes dürfen
    eine Ausnahme werfen.
    """
    _ok, _end = _walk(data, 0)
    return _ok


def _header(data: bytes, i: int) -> tuple[int, int, int]:
    if i >= len(data):
        raise ValueError("truncated cbor")
    byte = data[i]
    return byte >> 5, byte & 0x1F, i + 1


def _argument(data: bytes, i: int, info: int) -> tuple[int, int]:
    if info < 24:
        return info, i
    width = {24: 1, 25: 2, 26: 4, 27: 8}.get(info)
    if width is None:
        raise ValueError("reserved additional info")
    end = i + width
    if end > len(data):
        raise ValueError("truncated cbor")
    return int.from_bytes(data[i:end], "big"), end


def _key_at(data: bytes, i: int) -> tuple[bool, int]:
    if i >= len(data):
        raise ValueError("truncated cbor")
    major = data[i] >> 5
    ok, end = _walk(data, i)
    return major in (0, 1, 2, 3) and ok, end


def _walk(data: bytes, i: int) -> tuple[bool, int]:
    major, info, i = _header(data, i)
    if info == 31:
        if major == 2:
            return _indefinite_chunks(data, i, 2)
        if major == 3:
            return _indefinite_chunks(data, i, 3)
        if major == 4:
            return _indefinite_array(data, i)
        if major == 5:
            return _indefinite_map(data, i)
        raise ValueError("invalid indefinite length")
    if major in (0, 1):
        _value, i = _argument(data, i, info)
        return True, i
    if major in (2, 3):
        length, i = _argument(data, i, info)
        end = i + length
        if end > len(data):
            raise ValueError("truncated cbor")
        return True, end
    if major == 4:
        count, i = _argument(data, i, info)
        ok = True
        for _ in range(count):
            item_ok, i = _walk(data, i)
            ok = ok and item_ok
        return ok, i
    if major == 5:
        count, i = _argument(data, i, info)
        ok = True
        for _ in range(count):
            key_ok, i = _key_at(data, i)
            value_ok, i = _walk(data, i)
            ok = ok and key_ok and value_ok
        return ok, i
    if major == 6:
        _tag, i = _argument(data, i, info)
        return _walk(data, i)
    if major == 7:
        if info < 24:
            return True, i
        width = {24: 1, 25: 2, 26: 4, 27: 8}.get(info)
        if width is None:
            raise ValueError("reserved simple value")
        end = i + width
        if end > len(data):
            raise ValueError("truncated cbor")
        return True, end
    raise ValueError("invalid major type")


def _indefinite_chunks(data: bytes, i: int, major: int) -> tuple[bool, int]:
    while True:
        if i >= len(data):
            raise ValueError("truncated cbor")
        if data[i] == 0xFF:
            return True, i + 1
        chunk_major, info, j = _header(data, i)
        if chunk_major != major or info == 31:
            raise ValueError("invalid indefinite chunk")
        length, j = _argument(data, j, info)
        j += length
        if j > len(data):
            raise ValueError("truncated cbor")
        i = j


def _indefinite_array(data: bytes, i: int) -> tuple[bool, int]:
    ok = True
    while True:
        if i >= len(data):
            raise ValueError("truncated cbor")
        if data[i] == 0xFF:
            return ok, i + 1
        item_ok, i = _walk(data, i)
        ok = ok and item_ok


def _indefinite_map(data: bytes, i: int) -> tuple[bool, int]:
    ok = True
    while True:
        if i >= len(data):
            raise ValueError("truncated cbor")
        if data[i] == 0xFF:
            return ok, i + 1
        key_ok, i = _key_at(data, i)
        value_ok, i = _walk(data, i)
        ok = ok and key_ok and value_ok
