"""Deterministically validate a structured VietLearn lesson."""

from __future__ import annotations

from typing import Any


REQUIRED_FIELDS = (
    "day",
    "title",
    "objectives",
    "sections",
    "glossary",
    "quiz",
    "completion_criteria",
)


def validate_lesson(lesson: dict[str, Any], max_minutes: int) -> dict[str, Any]:
    """Validate required structure, course day, quiz, and time budget.

    Args:
        lesson: Structured lesson following the bundled lesson template.
        max_minutes: Maximum total minutes allowed for the learning day.

    Returns:
        A structured validation result with all detected errors.
    """
    errors: list[dict[str, str]] = []

    for field in REQUIRED_FIELDS:
        if field not in lesson:
            errors.append(
                {
                    "code": "MISSING_FIELD",
                    "message": f"Thiếu trường bắt buộc: {field}.",
                }
            )

    day = lesson.get("day")
    if not isinstance(day, int) or not 1 <= day <= 5:
        errors.append(
            {
                "code": "INVALID_DAY",
                "message": "Ngày học phải là số nguyên từ 1 đến 5.",
            }
        )

    total_minutes = 0
    sections = lesson.get("sections", [])
    if isinstance(sections, list):
        for section in sections:
            minutes = section.get("minutes", 0) if isinstance(section, dict) else 0
            if isinstance(minutes, int) and minutes >= 0:
                total_minutes += minutes
            else:
                errors.append(
                    {
                        "code": "INVALID_DURATION",
                        "message": "Mỗi section phải có số phút nguyên không âm.",
                    }
                )

    if total_minutes > max_minutes:
        errors.append(
            {
                "code": "TIME_BUDGET_EXCEEDED",
                "message": (
                    f"Bài học có {total_minutes} phút, vượt ngân sách "
                    f"{max_minutes} phút."
                ),
            }
        )

    quiz = lesson.get("quiz")
    if not isinstance(quiz, list) or not quiz:
        errors.append(
            {
                "code": "QUIZ_REQUIRED",
                "message": "Bài học phải có ít nhất một câu quiz.",
            }
        )

    return {
        "valid": not errors,
        "total_minutes": total_minutes,
        "errors": errors,
    }
