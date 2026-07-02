"""Run a deterministic end-to-end VietLearn showcase without an API key."""

from __future__ import annotations

import json
import sys

from app.guardrails import inspect_retrieved_content, validate_roadmap
from app.observability import TraceRecorder
from evals.quality import evaluate_grounding, evaluate_personalization
from mcp_server.course_server import get_lesson


def run_demo() -> dict:
    trace = TraceRecorder(trace_id="vietlearn-demo")
    profile = {
        "technical_level": "beginner",
        "english_level": "low",
        "max_minutes": 120,
        "knowledge_gaps": ["API vs Tool"],
    }
    trace.record("diagnostic_agent", "create_learner_profile", "success")

    roadmap = [{"day": day, "minutes": 120} for day in range(1, 6)]
    roadmap_check = validate_roadmap(roadmap, max_minutes=profile["max_minutes"])
    trace.record("learning_coach", "validate_roadmap", "success", roadmap_check)

    source = get_lesson(day=4)["lesson"]
    content_check = inspect_retrieved_content(source["summary"])
    trace.record("tutor_agent", "inspect_retrieved_content", "success", content_check)

    lesson = {
        "day": source["day"],
        "title": source["title"],
        "quiz_difficulty": "beginner",
        "source_ids": ["course-day-4"],
    }
    grounding = evaluate_grounding(lesson, {"course-day-4"})
    personalization = evaluate_personalization(lesson, profile)
    trace.record("tutor_agent", "evaluate_lesson", "success")

    evaluation_result = {
        "score": 0.6,
        "misconceptions": ["API vs Tool"],
        "next_action": "Dạy lại bằng ví dụ nhà hàng và cho bài phân loại ngắn.",
    }
    trace.record("evaluator_agent", "recommend_adaptation", "success")

    return {
        "learner_profile": profile,
        "roadmap_valid": roadmap_check["valid"],
        "lesson": lesson,
        "quality_gates": {
            "content_safe": content_check["allowed"],
            "grounded": grounding["passed"],
            "personalized": personalization["passed"],
        },
        "evaluation_result": evaluation_result,
        "trace": trace.export(),
    }


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(run_demo(), ensure_ascii=False, indent=2))
