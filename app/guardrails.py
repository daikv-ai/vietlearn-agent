"""Deterministic safety checks for VietLearn outputs and retrieved content."""

from __future__ import annotations

import re
from typing import Any


_INJECTION_PATTERNS = (
    re.compile(r"ignore (all |any )?(previous|prior) instructions", re.IGNORECASE),
    re.compile(r"bỏ qua (mọi |tất cả )?(chỉ dẫn|hướng dẫn|quy tắc)", re.IGNORECASE),
    re.compile(r"(reveal|show|print|đọc|tiết lộ).{0,30}(api[_ -]?key|secret|password)", re.IGNORECASE),
)


def validate_roadmap(
    roadmap: list[dict[str, Any]],
    max_minutes: int,
) -> dict[str, Any]:
    """Require exactly Days 1-5 and enforce the daily time budget."""
    errors: list[dict[str, Any]] = []
    days = [item.get("day") for item in roadmap if isinstance(item, dict)]

    if days != [1, 2, 3, 4, 5]:
        errors.append(
            {
                "code": "INVALID_ROADMAP_DAYS",
                "message": "Lộ trình phải gồm đúng Ngày 1 đến Ngày 5.",
            }
        )

    for item in roadmap:
        if not isinstance(item, dict):
            errors.append({"code": "INVALID_DAY_ITEM", "message": "Ngày học không hợp lệ."})
            continue
        minutes = item.get("minutes")
        if not isinstance(minutes, int) or minutes < 0 or minutes > max_minutes:
            errors.append(
                {
                    "code": "TIME_BUDGET_EXCEEDED",
                    "day": item.get("day"),
                    "message": f"Thời lượng mỗi ngày phải từ 0 đến {max_minutes} phút.",
                }
            )

    return {"valid": not errors, "errors": errors}


def inspect_retrieved_content(content: str) -> dict[str, Any]:
    """Flag instructions embedded in untrusted retrieved course content."""
    matches = [pattern.pattern for pattern in _INJECTION_PATTERNS if pattern.search(content)]
    return {
        "allowed": not matches,
        "event": "prompt_injection_detected" if matches else None,
        "matched_patterns": matches,
    }
