"""Tests for deterministic validation bundled with the explainer skill."""

from pathlib import Path
import sys


SKILL_SCRIPT_DIR = (
    Path(__file__).parents[1]
    / ".agents"
    / "skills"
    / "vietnamese-course-explainer"
    / "scripts"
)
sys.path.insert(0, str(SKILL_SCRIPT_DIR))

from validate_lesson import validate_lesson  # noqa: E402


def make_valid_lesson() -> dict:
    """Return a minimal valid lesson for deterministic tests."""
    return {
        "day": 3,
        "title": "Agent Skills",
        "objectives": ["Giải thích progressive disclosure"],
        "sections": [
            {"name": "Giải thích", "minutes": 35, "content": "Nội dung"},
            {"name": "Ví dụ", "minutes": 30, "content": "Ví dụ"},
            {"name": "Thực hành", "minutes": 40, "content": "Bài tập"},
            {"name": "Quiz", "minutes": 15, "content": "Kiểm tra"},
        ],
        "glossary": [{"term": "Skill", "meaning": "Quy trình chuyên môn"}],
        "quiz": [{"question": "Skill dùng để làm gì?", "answer": "Đóng gói cách làm"}],
        "completion_criteria": ["Trả lời đúng ít nhất 80% quiz"],
    }


def test_valid_lesson_passes_all_checks() -> None:
    result = validate_lesson(make_valid_lesson(), max_minutes=120)

    assert result == {"valid": True, "total_minutes": 120, "errors": []}


def test_lesson_over_time_budget_is_rejected() -> None:
    lesson = make_valid_lesson()
    lesson["sections"][0]["minutes"] = 50

    result = validate_lesson(lesson, max_minutes=120)

    assert result["valid"] is False
    assert result["total_minutes"] == 135
    assert any(error["code"] == "TIME_BUDGET_EXCEEDED" for error in result["errors"])


def test_day_six_is_rejected() -> None:
    lesson = make_valid_lesson()
    lesson["day"] = 6

    result = validate_lesson(lesson, max_minutes=120)

    assert result["valid"] is False
    assert any(error["code"] == "INVALID_DAY" for error in result["errors"])


def test_missing_quiz_is_rejected() -> None:
    lesson = make_valid_lesson()
    lesson["quiz"] = []

    result = validate_lesson(lesson, max_minutes=120)

    assert result["valid"] is False
    assert any(error["code"] == "QUIZ_REQUIRED" for error in result["errors"])


def test_missing_required_field_is_rejected() -> None:
    lesson = make_valid_lesson()
    del lesson["objectives"]

    result = validate_lesson(lesson, max_minutes=120)

    assert result["valid"] is False
    assert any(error["code"] == "MISSING_FIELD" for error in result["errors"])
