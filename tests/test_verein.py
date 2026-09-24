"""Verein — Dokument und Implementierung (szenario-verein.md)."""

from __future__ import annotations

from tools.verein import (
    build,
    check_ambiguous_sequence,
    check_amendment_class,
    check_amendment_table,
    check_anna_overcommit,
    check_anna_view,
    check_chris_view,
    check_chris_vouch_dora,
    check_dora_returns,
    check_epoch_3,
    check_exchange,
    check_exclusion,
    check_flagged_trust,
    check_membership_constitution_2,
    check_partial_receipt,
    check_settlement,
)


def test_anna_overcommit() -> None:
    check_anna_overcommit(build())


def test_chris_vouch_dora() -> None:
    check_chris_vouch_dora(build())


def test_membership_constitution_2() -> None:
    check_membership_constitution_2(build())


def test_amendment_class() -> None:
    check_amendment_class(build())


def test_amendment_table() -> None:
    check_amendment_table(build())


def test_epoch_3() -> None:
    check_epoch_3(build())


def test_ambiguous_sequence() -> None:
    check_ambiguous_sequence(build())


def test_anna_view() -> None:
    check_anna_view(build())


def test_chris_view() -> None:
    check_chris_view(build())


def test_exchange() -> None:
    check_exchange(build())


def test_dora_returns() -> None:
    check_dora_returns(build())


def test_flagged_trust() -> None:
    check_flagged_trust(build())


def test_exclusion() -> None:
    check_exclusion(build())


def test_settlement() -> None:
    check_settlement(build())


def test_partial_receipt() -> None:
    check_partial_receipt(build())
