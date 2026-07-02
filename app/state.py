"""Shared session state schema for the VietLearn agent team."""

from pydantic import BaseModel, Field


class VietLearnSessionState(BaseModel):
    """State shared by the coordinator and all specialist agents."""

    learner_profile: str | None = None
    current_lesson: str | None = None
    evaluation_result: str | None = None
    current_day: int = Field(default=1, ge=1, le=5)
    max_minutes: int = Field(default=120, gt=0, le=480)
    knowledge_gaps: list[str] = Field(default_factory=list)
