"""Trust-Findings: eigene Enum, kein Claim-Reject (02 §10)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TrustFinding(str, Enum):
    OVERCOMMITTED_AUTHOR = "OVERCOMMITTED_AUTHOR"
    SUBGRANULAR_VOUCH = "SUBGRANULAR_VOUCH"
    INVALID_VOUCH_WEIGHT = "INVALID_VOUCH_WEIGHT"
    UNPARSABLE_VOUCH_PAYLOAD = "UNPARSABLE_VOUCH_PAYLOAD"
    NON_CANONICAL_V = "NON_CANONICAL_V"
    # unbefristet bindend, auch Widerruf befreit nie (02 §6.2, D364)
    VOUCH_WITHOUT_TEXP = "VOUCH_WITHOUT_TEXP"


@dataclass(frozen=True, slots=True, order=True)
class Finding:
    kind: TrustFinding
    subject: bytes
