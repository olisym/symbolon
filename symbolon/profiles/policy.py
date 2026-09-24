"""Policy-Auflösung aus Genesis und Verfassung (03-profiles.md §1.2, D82/D84/D90, D167, D168)."""

from __future__ import annotations

from dataclasses import dataclass

from symbolon.genesis import genesis_scope
from symbolon.policy import NucleusPolicy, constitution_hash as hash_constitution
from symbolon.profiles.findings import Finding, ProfileFinding, dedupe_sort


@dataclass(frozen=True, slots=True)
class PolicyResolution:
    """Ergebnis von ``resolve_policy``: Policy plus Auflösungsbefunde (03-profiles.md §1.2)."""

    policy: NucleusPolicy
    findings: tuple[Finding, ...]


def resolve_policy(
    *,
    scope: bytes,
    genesis_obj: dict,
    constitution_hash: bytes,
    constitution_obj: dict | None = None,
) -> PolicyResolution:
    """Rechnet Scope und constitution_hash nach; Sicherheits-Default bei Teilwissen.

    Siehe 03-profiles.md §1.2 und 03-prompt.md §4. ``UNSAFE_IRREVOCABLE_PREDICATE``
    entsteht im Konstruktor von ``NucleusPolicy`` (D84), nicht hier.
    ``genesis_obj[4]`` wird nicht gelesen (D168). Hash-Abweichung ist ValueError (D167).
    """
    computed_scope = genesis_scope(genesis_obj)
    if scope != computed_scope:
        raise ValueError("genesis_obj does not match scope")

    if constitution_obj is None:
        return PolicyResolution(
            policy=NucleusPolicy(scope, declared=frozenset()),
            findings=dedupe_sort(
                [
                    Finding(
                        kind=ProfileFinding.CONSTITUTION_UNAVAILABLE,
                        subject=constitution_hash,
                    )
                ]
            ),
        )

    if hash_constitution(constitution_obj) != constitution_hash:
        raise ValueError("constitution_obj does not match constitution_hash")

    raw = constitution_obj.get("irrevocable_predicates", [])
    return PolicyResolution(
        policy=NucleusPolicy(scope, declared=raw),
        findings=(),
    )
