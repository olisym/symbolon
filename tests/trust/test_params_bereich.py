"""TrustParams: Typpruefung und Bereichsgrenzen (02 §11.2, D398 Beschluss 3)."""

from __future__ import annotations

import pytest

from symbolon.trust import TrustParams

from .tp02 import PARAMS

FIELDS = ("C0", "gamma_num", "gamma_den", "D")


def _params(**overrides: object) -> TrustParams:
    base: dict[str, object] = {
        "C0": PARAMS.C0,
        "gamma_num": PARAMS.gamma_num,
        "gamma_den": PARAMS.gamma_den,
        "D": PARAMS.D,
    }
    base.update(overrides)
    return TrustParams(**base)


@pytest.mark.parametrize("field", FIELDS)
def test_type_float_abgelehnt(field: str) -> None:
    with pytest.raises(ValueError, match=field):
        _params(**{field: float(getattr(PARAMS, field))})


@pytest.mark.parametrize("field", FIELDS)
def test_type_bool_abgelehnt(field: str) -> None:
    with pytest.raises(ValueError, match=field):
        _params(**{field: True})


def test_c0_null_abgelehnt() -> None:
    with pytest.raises(ValueError, match="C0 must be > 0"):
        _params(C0=0)


def test_gamma_num_null_abgelehnt() -> None:
    with pytest.raises(ValueError, match="gamma_num must satisfy 0 < gamma_num < gamma_den"):
        _params(gamma_num=0)


def test_gamma_num_gleich_gamma_den_abgelehnt() -> None:
    with pytest.raises(ValueError, match="gamma_num must satisfy 0 < gamma_num < gamma_den"):
        _params(gamma_num=PARAMS.gamma_den)


def test_d_null_abgelehnt() -> None:
    with pytest.raises(ValueError, match="D must be >= 1"):
        _params(D=0)


def test_rand_gueltig() -> None:
    params = TrustParams(C0=1, gamma_num=1, gamma_den=2, D=1)
    assert params.C0 == 1
    assert params.gamma_num == 1
    assert params.gamma_den == 2
    assert params.D == 1
