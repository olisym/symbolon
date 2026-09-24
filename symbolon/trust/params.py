"""Trust-Flow-Parameter (02 §11.2) und Herleitung aus dem Genesis (02 §8.1, D147)."""

from __future__ import annotations

from dataclasses import dataclass

from symbolon.genesis import genesis_scope


@dataclass(frozen=True, slots=True)
class TrustParams:
    """γ = gamma_num/gamma_den, C(d) = ⌊C0 · γ^d⌋ (einmal am Ende gerundet, 02 §3)."""

    C0: int
    gamma_num: int
    gamma_den: int
    D: int

    def __post_init__(self) -> None:
        if type(self.C0) is not int:
            raise ValueError("C0 must be int")
        if type(self.gamma_num) is not int:
            raise ValueError("gamma_num must be int")
        if type(self.gamma_den) is not int:
            raise ValueError("gamma_den must be int")
        if type(self.D) is not int:
            raise ValueError("D must be int")
        if self.C0 <= 0:
            raise ValueError("C0 must be > 0")
        if not (0 < self.gamma_num < self.gamma_den):
            raise ValueError("gamma_num must satisfy 0 < gamma_num < gamma_den")
        if self.D < 1:
            raise ValueError("D must be >= 1")


def resolve_trust_params(
    *,
    scope: bytes,
    genesis_obj: dict,
    out_of_band: TrustParams | None = None,
) -> TrustParams:
    """Kalibrierung aus Genesis oder out-of-band (02-trust-flow.md §8.1, D147)."""
    if (
        genesis_scope(genesis_obj)
        != scope
    ):
        raise ValueError("genesis_obj does not match scope")
    if 9 in genesis_obj:
        raw = genesis_obj[9]
        if not isinstance(raw, dict):
            raise ValueError("genesis_obj key 9 is malformed")
        try:
            c0, gamma_num, gamma_den, d = raw[0], raw[1], raw[2], raw[3]
        except KeyError:
            raise ValueError("genesis_obj key 9 is malformed") from None
        if not (
            type(c0) is int
            and type(gamma_num) is int
            and type(gamma_den) is int
            and type(d) is int
        ):
            raise ValueError("genesis_obj key 9 is malformed")
        derived = TrustParams(C0=c0, gamma_num=gamma_num, gamma_den=gamma_den, D=d)
        if out_of_band is None:
            return derived
        if derived != out_of_band:
            raise ValueError("out_of_band does not match genesis trust_params")
        return derived
    if out_of_band is None:
        raise ValueError("genesis_obj missing trust_params and no out_of_band")
    return out_of_band
