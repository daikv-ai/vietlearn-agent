"""Tests for the read-only VietLearn course MCP server."""

import inspect

import pytest

from mcp_server.course_server import (
    EXPOSED_TOOL_NAMES,
    get_lesson,
    load_catalog,
    search_materials,
)


def test_catalog_contains_exactly_five_ordered_lessons() -> None:
    """The MVP course must contain exactly Days 1 through 5."""
    catalog = load_catalog()

    assert [lesson["day"] for lesson in catalog["lessons"]] == [1, 2, 3, 4, 5]


def test_get_lesson_returns_structured_lesson() -> None:
    """A valid day returns the matching grounded lesson."""
    result = get_lesson(day=2)

    assert result["ok"] is True
    assert result["lesson"]["day"] == 2
    assert "MCP" in result["lesson"]["concepts"]


def test_get_lesson_rejects_day_outside_course() -> None:
    """The server must not silently substitute or invent another day."""
    result = get_lesson(day=8)

    assert result == {
        "ok": False,
        "error": {
            "code": "LESSON_NOT_FOUND",
            "message": "Không tìm thấy bài học Ngày 8. Khóa học chỉ có Ngày 1 đến Ngày 5.",
        },
    }


def test_search_is_case_insensitive_and_grounded() -> None:
    """Concept search should work without depending on capitalization."""
    result = search_materials(concept="mcp")

    assert result["ok"] is True
    assert [lesson["day"] for lesson in result["lessons"]] == [2]


def test_search_can_filter_by_day_and_level() -> None:
    """Search filters should narrow results without inventing content."""
    result = search_materials(day=4, level="BEGINNER")

    assert result["ok"] is True
    assert [lesson["day"] for lesson in result["lessons"]] == [4]


def test_search_returns_empty_list_when_no_material_matches() -> None:
    """No match is a valid grounded result and must not trigger hallucination."""
    result = search_materials(concept="quantum gardening")

    assert result == {"ok": True, "count": 0, "lessons": []}


def test_mcp_surface_is_read_only_and_has_no_path_argument() -> None:
    """The public MCP surface must not expose writes or arbitrary file access."""
    assert EXPOSED_TOOL_NAMES == ("search_materials", "get_lesson")

    for function in (search_materials, get_lesson):
        assert "path" not in inspect.signature(function).parameters
        assert "file" not in inspect.signature(function).parameters


@pytest.mark.parametrize("day", [0, -1, 6, 100])
def test_invalid_day_never_returns_another_lesson(day: int) -> None:
    """Invalid input must never be coerced into a valid lesson."""
    result = get_lesson(day=day)

    assert result["ok"] is False
    assert result["error"]["code"] == "LESSON_NOT_FOUND"
