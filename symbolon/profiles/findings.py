"""Profile-Findings: eigener Enum, kein Claim-Reject (03-profiles.md §6.1)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ProfileFinding(str, Enum):
    NON_CANONICAL_V = "NON_CANONICAL_V"
    UNPARSABLE_V = "UNPARSABLE_V"
    INVALID_V_TYPE = "INVALID_V_TYPE"
    SCOPE_MISMATCH = "SCOPE_MISMATCH"
    CONSTITUTION_UNAVAILABLE = "CONSTITUTION_UNAVAILABLE"
    EXPIRING_OBLIGATION = "EXPIRING_OBLIGATION"
    OBLIGATION_PENDING = "OBLIGATION_PENDING"
    OBLIGATION_AUTHOR_FLAGGED = "OBLIGATION_AUTHOR_FLAGGED"
    OBLIGATION_TIME_REGRESSION = "OBLIGATION_TIME_REGRESSION"
    PARTIAL_RECEIPT_UNSUPPORTED = "PARTIAL_RECEIPT_UNSUPPORTED"
    CONSTITUTION_VERSION_MISMATCH = "CONSTITUTION_VERSION_MISMATCH"
    UNAUTHORIZED_GRANT_AUTHOR = "UNAUTHORIZED_GRANT_AUTHOR"
    UNKNOWN_ACCUSATION = "UNKNOWN_ACCUSATION"
    INACTIVE_VERDICT = "INACTIVE_VERDICT"
    UNRESOLVED_ACCUSED = "UNRESOLVED_ACCUSED"


@dataclass(frozen=True, slots=True, order=True)
class Finding:
    """Vermerk mit Subjekt — in der Regel eine claim_id (03-profiles.md §6, D90)."""

    kind: ProfileFinding
    subject: bytes


def dedupe_sort(findings: list[Finding] | tuple[Finding, ...]) -> tuple[Finding, ...]:
    """Findings sortiert und dedupliziert (PR-INV-9)."""
    return tuple(sorted(set(findings)))
