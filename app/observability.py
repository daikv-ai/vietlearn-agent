"""Minimal structured tracing with secret redaction."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


_SENSITIVE_KEYS = {"api_key", "authorization", "password", "secret", "token"}


def _redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if key.casefold() in _SENSITIVE_KEYS else _redact(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redact(item) for item in value]
    return value


class TraceRecorder:
    """Collect structured events belonging to one learner request."""

    def __init__(self, trace_id: str | None = None) -> None:
        self.trace_id = trace_id or uuid4().hex
        self.events: list[dict[str, Any]] = []

    def record(
        self,
        agent_name: str,
        action: str,
        status: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.events.append(
            {
                "trace_id": self.trace_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "agent_name": agent_name,
                "action": action,
                "status": status,
                "details": _redact(details or {}),
            }
        )

    def export(self) -> list[dict[str, Any]]:
        return list(self.events)
