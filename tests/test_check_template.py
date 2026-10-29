"""Tests for scripts/check_template.py. Stdlib + pytest only."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from check_template import check_file, check_text, detect_template

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = REPO_ROOT / "examples" / "bottlers-nepal-terai-initiation-example.md"

COMPLETE = """# Initiation Report — Example

## 1. Thesis in one paragraph
One paragraph of thesis.

## 2. Business
What it sells.

## 3. Industry
Market context.

## 4. Financials
A table of figures.

## 5. Valuation
Method fit discussion.

## 6. Risks
First risk.

## 7. What would change this thesis
Bull and bear triggers.

## 8. Open questions / unverified items
Everything not verified.
"""


def test_flags_missing_section():
    text = "## 1. Thesis in one paragraph\nThesis.\n\n## 2. Business\nSells.\n"
    missing, _empty = check_text(text, "initiation")
    assert "Industry" in missing
    assert "Financials" in missing
    assert "Valuation" in missing
    assert "Thesis in one paragraph" not in missing
    assert "Business" not in missing


def test_flags_empty_section():
    text = COMPLETE.replace(
        "## 3. Industry\nMarket context.\n", "## 3. Industry\n"
    )
    missing, empty = check_text(text, "initiation")
    assert missing == []
    assert empty == ["Industry"]


def test_passes_complete_example():
    missing, empty = check_text(COMPLETE, "initiation")
    assert missing == []
    assert empty == []


def test_no_false_positive_on_new_filled_example():
    assert EXAMPLE.exists()
    chosen, missing, empty = check_file(EXAMPLE, "initiation")
    assert chosen == "initiation"
    assert missing == []
    assert empty == []


def test_auto_detect_finds_initiation_example():
    text = EXAMPLE.read_text(encoding="utf-8")
    assert detect_template(text) == "initiation"


def test_deterministic_repeat_runs():
    first = check_file(EXAMPLE, "initiation")
    second = check_file(EXAMPLE, "initiation")
    assert first == second
