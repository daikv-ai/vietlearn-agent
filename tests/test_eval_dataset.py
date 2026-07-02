"""Schema checks for the regression evaluation dataset."""

import json
from pathlib import Path


def test_eval_cases_have_unique_ids_and_required_fields() -> None:
    path = Path(__file__).parents[1] / "evals" / "cases.json"
    cases = json.loads(path.read_text(encoding="utf-8"))
    ids = [case["id"] for case in cases]
    assert len(cases) >= 5
    assert len(ids) == len(set(ids))
    assert all("category" in case and "input" in case for case in cases)


def test_eval_dataset_covers_capstone_quality_dimensions() -> None:
    path = Path(__file__).parents[1] / "evals" / "cases.json"
    cases = json.loads(path.read_text(encoding="utf-8"))
    categories = {case["category"] for case in cases}
    assert {"constraint", "quality", "grounding", "safety", "adaptation"} <= categories
