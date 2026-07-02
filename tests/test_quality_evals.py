"""Tests for structured offline quality evaluations."""

from evals.quality import evaluate_grounding, evaluate_personalization


def test_grounded_lesson_passes() -> None:
    result = evaluate_grounding(
        {"source_ids": ["day-3-skills"]},
        allowed_source_ids={"day-3-skills"},
    )
    assert result["passed"] is True


def test_unknown_or_missing_source_fails_grounding() -> None:
    result = evaluate_grounding(
        {"source_ids": ["invented-source"]},
        allowed_source_ids={"day-3-skills"},
    )
    assert result["passed"] is False
    assert result["unknown_source_ids"] == ["invented-source"]


def test_quiz_matched_to_beginner_passes() -> None:
    result = evaluate_personalization(
        {"quiz_difficulty": "beginner"},
        {"technical_level": "beginner"},
    )
    assert result["passed"] is True


def test_quiz_too_hard_for_beginner_fails() -> None:
    result = evaluate_personalization(
        {"quiz_difficulty": "advanced"},
        {"technical_level": "beginner"},
    )
    assert result["passed"] is False
