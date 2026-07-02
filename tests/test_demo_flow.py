"""Regression test for the credential-free showcase flow."""

from scripts.demo_learning_flow import run_demo


def test_demo_passes_all_quality_gates_and_adapts() -> None:
    result = run_demo()
    assert result["roadmap_valid"] is True
    assert all(result["quality_gates"].values())
    assert result["evaluation_result"]["misconceptions"] == ["API vs Tool"]
    assert len(result["trace"]) == 5
