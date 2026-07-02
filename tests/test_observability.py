"""Tests for safe structured tracing."""

from app.observability import TraceRecorder


def test_events_in_one_trace_share_trace_id() -> None:
    recorder = TraceRecorder(trace_id="request-123")
    recorder.record("learning_coach", "delegate", "success")
    recorder.record("tutor_agent", "get_lesson", "success")
    assert {event["trace_id"] for event in recorder.export()} == {"request-123"}


def test_sensitive_fields_are_redacted_recursively() -> None:
    recorder = TraceRecorder(trace_id="request-123")
    recorder.record(
        "tutor_agent",
        "call_model",
        "success",
        {"api_key": "real-key", "nested": {"password": "real-password"}},
    )
    details = recorder.export()[0]["details"]
    assert details["api_key"] == "[REDACTED]"
    assert details["nested"]["password"] == "[REDACTED]"
