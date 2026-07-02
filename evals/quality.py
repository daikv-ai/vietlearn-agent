"""Structured offline evaluations for grounding and personalization."""

from __future__ import annotations

from typing import Any


_LEVEL_RANK = {"beginner": 1, "intermediate": 2, "advanced": 3}


def evaluate_grounding(
    lesson: dict[str, Any],
    allowed_source_ids: set[str],
) -> dict[str, Any]:
    """Check that a lesson cites only retrieved, allowlisted course sources."""
    source_ids = lesson.get("source_ids", [])
    valid_shape = isinstance(source_ids, list) and bool(source_ids)
    unknown = sorted(set(source_ids) - allowed_source_ids) if valid_shape else []
    passed = valid_shape and not unknown
    return {
        "passed": passed,
        "unknown_source_ids": unknown,
        "reason": "grounded" if passed else "missing_or_unknown_sources",
    }


def evaluate_personalization(
    lesson: dict[str, Any],
    learner_profile: dict[str, Any],
) -> dict[str, Any]:
    """Check quiz difficulty against the diagnosed learner level."""
    learner_level = learner_profile.get("technical_level")
    quiz_level = lesson.get("quiz_difficulty")
    learner_rank = _LEVEL_RANK.get(learner_level)
    quiz_rank = _LEVEL_RANK.get(quiz_level)
    passed = learner_rank is not None and quiz_rank is not None and quiz_rank <= learner_rank
    return {
        "passed": passed,
        "learner_level": learner_level,
        "quiz_difficulty": quiz_level,
        "reason": "level_matched" if passed else "quiz_too_hard_or_level_missing",
    }
