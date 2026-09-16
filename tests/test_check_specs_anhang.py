"""Anhangsverweise in ``check_specs``: beide Zitatformen, Befunde, Auflösung (D401).

``check_specs`` liest auch Python-Dateien. Damit diese Testdatei selbst keinen
Befund erzeugt, werden Anhangsverweise hier zur Laufzeit aus Teilen zusammengesetzt
und stehen nie zusammenhängend im Quelltext.
"""

from __future__ import annotations

from tools.check_specs import check_section_refs, layer_headings


def _ref(name: str, appendix: str) -> str:
    return f"{name} {appendix}"


def _tick(name: str, appendix: str) -> str:
    return f"`{name}` {appendix}"


def _finding(ref: str, n: int) -> str:
    return f"verweist auf unbekannten Anhang: {ref} ({n}x)"


def test_anhang_aufgeloest() -> None:
    headings = {"01": frozenset({"A", "B", "C", "B.1", "B.2", "C.13"})}
    text = " ".join(
        [
            _ref("01", "Anhang B.2"),
            _ref("01", "B.2"),
            _tick("01", "Anhang B.2"),
            _ref("01", "Anhang A"),
        ]
    )
    n, problems = check_section_refs(text, headings)
    assert problems == []
    assert n == 4


def test_anhang_erfunden() -> None:
    headings = {"01": frozenset({"A", "B", "C", "B.1", "B.2", "C.13"})}
    text = " ".join(
        [
            _ref("01", "Anhang Z"),
            _ref("01", "Anhang Z.2"),
            _ref("01", "Z.2"),
        ]
    )
    n, problems = check_section_refs(text, headings)
    assert n == 3
    assert problems == [
        _finding(_ref("01", "Anhang Z"), 1),
        _finding(_ref("01", "Anhang Z.2"), 1),
        _finding(_ref("01", "Z.2"), 1),
    ]


def test_anhang_vollstaendige_nummer() -> None:
    text = _ref("01", "Anhang C.13")
    n, problems = check_section_refs(text, {"01": frozenset({"C.1"})})
    assert n == 1
    assert problems == [_finding(_ref("01", "Anhang C.13"), 1)]

    n, problems = check_section_refs(text, {"01": frozenset({"C.13"})})
    assert n == 1
    assert problems == []


def test_anhang_satzpunkt_gehoert_nicht_dazu() -> None:
    text = _ref("01", "Anhang B.2") + "."
    n, problems = check_section_refs(text, {"01": frozenset({"B.2"})})
    assert n == 1
    assert problems == []


def test_anhang_einzelbuchstabe_ohne_wort_nicht_erkannt() -> None:
    n, problems = check_section_refs(_ref("01", "B"), {"01": frozenset({"B"})})
    assert n == 0
    assert problems == []


def test_anhang_a_aus_01_mit_wort() -> None:
    n, problems = check_section_refs(_ref("01", "Anhang A"), layer_headings())
    assert n == 1
    assert problems == []


def test_anhang_buchstabe_als_wortanfang_nicht_erkannt() -> None:
    headings = {"01": frozenset({"A", "B", "C", "B.1", "B.2", "C.13"})}
    text = " ".join(
        [
            _ref("01", "Anhang Babel"),
            _ref("01", "B.2x"),
        ]
    )
    n, problems = check_section_refs(text, headings)
    assert n == 0
    assert problems == []
