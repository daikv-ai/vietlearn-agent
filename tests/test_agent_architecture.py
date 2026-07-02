"""Architecture tests for the VietLearn ADK multi-agent system."""

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.skill_toolset import SkillToolset

from app.agent import (
    diagnostic_agent,
    evaluator_agent,
    root_agent,
    tutor_agent,
)


def test_root_agent_has_three_specialized_sub_agents() -> None:
    assert [agent.name for agent in root_agent.sub_agents] == [
        "diagnostic_agent",
        "tutor_agent",
        "evaluator_agent",
    ]


def test_agent_names_are_unique() -> None:
    names = [root_agent.name, *(agent.name for agent in root_agent.sub_agents)]

    assert len(names) == len(set(names))


def test_specialists_write_to_distinct_session_state_keys() -> None:
    assert diagnostic_agent.output_key == "learner_profile"
    assert tutor_agent.output_key == "current_lesson"
    assert evaluator_agent.output_key == "evaluation_result"


def test_tutor_uses_skill_toolset() -> None:
    assert len(tutor_agent.tools) == 1
    assert isinstance(tutor_agent.tools[0], SkillToolset)

    skill_toolset = tutor_agent.tools[0]
    assert set(skill_toolset._skills) == {"vietnamese-course-explainer"}


def test_explainer_skill_can_access_only_read_only_course_mcp_tools() -> None:
    skill_toolset = tutor_agent.tools[0]

    assert len(skill_toolset._provided_toolsets) == 1
    course_toolset = skill_toolset._provided_toolsets[0]
    assert isinstance(course_toolset, McpToolset)
    assert course_toolset.tool_filter == ["search_materials", "get_lesson"]


def test_skill_resources_are_packaged_for_progressive_disclosure() -> None:
    skill = tutor_agent.tools[0]._skills["vietnamese-course-explainer"]

    assert "glossary.md" in skill.resources.references
    assert "trigger_cases.json" in skill.resources.references
    assert "lesson_template.md" in skill.resources.assets
    assert "validate_lesson.py" in skill.resources.scripts


def test_root_instruction_enforces_delegation_order() -> None:
    instruction = str(root_agent.instruction)

    assert "diagnostic_agent" in instruction
    assert "tutor_agent" in instruction
    assert "evaluator_agent" in instruction
    assert instruction.index("diagnostic_agent") < instruction.index("tutor_agent")
    assert instruction.index("tutor_agent") < instruction.index("evaluator_agent")


def test_runtime_guardrails_are_available_to_responsible_agents() -> None:
    assert [tool.__name__ for tool in root_agent.tools] == ["validate_roadmap"]
    skill_toolset = tutor_agent.tools[0]
    assert "inspect_retrieved_content" in skill_toolset.tool_filter


def test_security_policy_is_attached_to_coordinator_and_tutor() -> None:
    assert "untrusted data" in str(root_agent.instruction)
    assert "untrusted data" in str(tutor_agent.instruction)
    assert "search_materials" in str(tutor_agent.instruction)
