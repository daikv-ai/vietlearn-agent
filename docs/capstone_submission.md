# VietLearn Agent — Kaggle Writeup

## Basic details

**Title:** VietLearn Agent: Adaptive Tech Learning for Vietnamese Learners

**Subtitle:** A safe multi-agent tutor that turns English technology courses into personalized Vietnamese learning journeys.

**Track:** Agents for Good

## Project description

### The problem

Many Vietnamese learners cannot fully benefit from international technology courses because the material assumes both English fluency and prior technical knowledge. Translation alone is not enough: it does not diagnose missing foundations, fit lessons into a limited schedule, verify understanding, or adapt after mistakes.

### The solution

VietLearn Agent is a safe, adaptive learning system that converts an English technology course into a structured Vietnamese learning journey. The learner first completes a diagnostic assessment. VietLearn then builds a profile, retrieves allowlisted course material, teaches one grounded lesson at the appropriate difficulty, evaluates the learner's answers, and uses detected misconceptions to adapt the next lesson.

The MVP is grounded in Google's 5-Day AI Agents: Intensive Vibe Coding Course. It enforces a strict five-day roadmap and a maximum of 120 minutes per day for the target learner.

### Multi-agent architecture

VietLearn is implemented with Google Agent Development Kit (ADK):

- **Learning Coach** coordinates the workflow and validates the roadmap.
- **Diagnostic Agent** identifies the learner's English level, technical level, time budget, and knowledge gaps.
- **Tutor Agent** retrieves grounded course content and applies the Vietnamese Course Explainer Skill.
- **Evaluator Agent** scores quiz answers, records misconceptions, and recommends the next adaptation.
- **Shared session state** carries the learner profile, current lesson, and evaluation result between agents.

### Course concepts demonstrated

1. **ADK multi-agent system:** a coordinator, three specialist agents, explicit responsibilities, and shared state.
2. **MCP server:** a local read-only server exposes only `search_materials` and `get_lesson`; arbitrary file access, writes, and deletes are unavailable.
3. **Agent Skill:** progressive disclosure packages instructions, references, a lesson template, and a deterministic validation script.
4. **Security:** least-privilege tools, untrusted-content policy, prompt-injection detection, secret redaction, and explicit confirmation before overwriting progress.
5. **Evaluation and observability:** deterministic guardrails, grounding and personalization evals, a regression dataset, and structured traces with a shared `trace_id`.

### Safety and quality gates

Hard constraints are checked by code rather than left to prompting alone. A roadmap must contain exactly Days 1–5. Daily duration cannot exceed the learner's budget. Retrieved text is inspected before use. Lessons cite allowlisted source IDs, and quiz difficulty is compared with the diagnosed learner level. Trace fields recursively redact API keys, passwords, secrets, and tokens.

The repository contains 39 automated tests covering agent architecture, read-only MCP behavior, Skill packaging, time and day limits, indirect prompt injection, grounding, personalization, trace redaction, and the complete credential-free showcase flow.

### Demonstration

The deterministic showcase makes the safety and evaluation path reproducible without external credentials. It runs:

1. learner diagnosis;
2. five-day roadmap validation;
3. allowlisted course retrieval;
4. retrieved-content inspection;
5. grounding and personalization checks;
6. misconception detection;
7. adaptive recommendation;
8. structured trace export.

```powershell
python scripts/demo_learning_flow.py
python -m pytest
```

### Impact

VietLearn demonstrates a reusable pattern for making international technical education more accessible: language adaptation combined with diagnosis, grounded retrieval, active assessment, and controlled personalization. The same architecture can later support additional courses and languages without granting the tutor unrestricted access to external systems.

### Limitations and next steps

The MVP uses one curated course catalog and local session state. The ADK application and tools run locally; live Gemini execution depends on project-level API access. Future work includes authenticated persistence, human-reviewed course ingestion, longitudinal learning analytics, additional Vietnamese technology courses, and learner-facing web/mobile interfaces.

## Project links

- Source code: https://github.com/daikv-ai/vietlearn-agent
- Architecture: https://github.com/daikv-ai/vietlearn-agent/blob/main/docs/architecture.md
- Agent Skill: https://github.com/daikv-ai/vietlearn-agent/tree/main/.agents/skills/vietnamese-course-explainer
- Eval dataset: https://github.com/daikv-ai/vietlearn-agent/blob/main/evals/cases.json

## Media files

- Card image: `docs/assets/vietlearn-thumbnail-560x280.png`
- Demo image: `docs/assets/demo-quality-gates.png`
- Test image: `docs/assets/test-results.png`
