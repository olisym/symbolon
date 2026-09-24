"""Prädikat-Grammatik (Anhang A), Scope-Auflösung und Bindungsregel (01 §2.2)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from symbolon.atom import Claim
from symbolon.errors import (
    BadScopeBinding,
    InvalidPredicate,
    MalformedCbor,
    ReservedCorePredicate,
    UnknownNamespace,
    VerifierError,
)

_CANONICAL_SCOPE = re.compile(r"^[0-9a-f]{64}$")
_NAME = re.compile(r"^[a-z0-9_-]+$")
_VERSION = re.compile(r"^[1-9][0-9]*$")
_CORE_PREDICATE = re.compile(r"^core/(revoke|supersede)@1$")
_NUC_PREDICATE = re.compile(
    r"^nuc:(?:[0-9a-f]{64}|(?![0-9a-f]{64}/)[a-z0-9_-]+)/[a-z0-9_-]+@[1-9][0-9]*$"
)


@dataclass(frozen=True, slots=True)
class ParsedPredicate:
    namespace: str
    name: str
    version: str
    scope_hex: str | None = None
    scope_alias: str | None = None


def parse_predicate(p: str) -> ParsedPredicate:
    """
    Grammatik aus Anhang A parsen.

    ``core/*`` gilt nur für die geschlossene Menge ``{revoke@1, supersede@1}``
    (01 §2.2, 01 §2.4 Invariante 4, D452). Prüft als erstes, ob p ein str ist,
    und wirft sonst MalformedCbor (D213).
    Raises VerifierError-Subklassen bei ungültiger Form.
    """
    if not isinstance(p, str):
        raise MalformedCbor()
    if p.startswith("core/"):
        if not _CORE_PREDICATE.match(p):
            raise ReservedCorePredicate()
        _, rest = p.split("/", 1)
        name, version = rest.split("@", 1)
        return ParsedPredicate(namespace="core", name=name, version=version)

    if p.startswith("nuc:"):
        if not _NUC_PREDICATE.match(p):
            raise InvalidPredicate()
        body = p[4:]
        scope_part, rest = body.split("/", 1)
        name, version = rest.split("@", 1)
        if _CANONICAL_SCOPE.match(scope_part):
            return ParsedPredicate(
                namespace="nuc",
                name=name,
                version=version,
                scope_hex=scope_part,
            )
        return ParsedPredicate(
            namespace="nuc",
            name=name,
            version=version,
            scope_alias=scope_part,
        )

    raise UnknownNamespace()


def resolve_scope(claim: Claim) -> bytes:
    """
    Aufgelösten Scope aus Claim bestimmen (01 §2.2).

    Raises BadScopeBinding wenn Bindungsregel verletzt.
    Raises ValueError wenn der Claim ein core/*-Claim ist (01 §2.3, D284).
    """
    parsed = parse_predicate(claim.p)

    if parsed.namespace == "core":
        raise ValueError("core/* claim has no scope")

    if parsed.scope_hex is not None:
        expected = bytes.fromhex(parsed.scope_hex)
        if claim.N is None or claim.N != expected:
            raise BadScopeBinding()
        return expected

    # Alias-Kodierung: N ist die einzige Scope-Quelle.
    if claim.N is None:
        raise BadScopeBinding()
    return claim.N


def is_core_predicate(claim: Claim) -> bool:
    """True gdw. p ein gültiges core/revoke@1 oder core/supersede@1 ist (01 §2.4)."""
    try:
        parsed = parse_predicate(claim.p)
        return parsed.namespace == "core"
    except VerifierError:
        return False


def is_nuc_name(claim: Claim, name: str) -> bool:
    """True gdw. p ein nuc:-Prädikat mit diesem Namen in Version 1 ist (01 §2.2, Anhang A, D181, D213)."""
    try:
        parsed = parse_predicate(claim.p)
    except VerifierError:
        return False
    return (
        parsed.namespace == "nuc"
        and parsed.name == name
        and parsed.version == "1"
    )


def check_scope_binding(claim: Claim) -> None:
    """Bindungsregel 01 §2.2 Regel 3 prüfen; wirft bei Verletzung."""
    parsed = parse_predicate(claim.p)
    if parsed.namespace == "nuc":
        resolve_scope(claim)
