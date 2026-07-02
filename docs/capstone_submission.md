# VietLearn Agent — Capstone submission draft

## Track

Agents for Good — Education.

## Problem

Vietnamese learners with limited English and uneven technical foundations struggle to complete international technology courses. Translation alone does not diagnose knowledge gaps, fit lessons into a time budget, or adapt after mistakes.

## Solution

VietLearn is a safe multi-agent learning assistant that diagnoses the learner, retrieves allowlisted course material, explains it in Vietnamese, evaluates understanding, and adapts the next lesson. The MVP supports Google's five-day AI Agents course with a strict limit of five days and 120 minutes per day.

## Agent design

- Learning Coach coordinates the workflow.
- Diagnostic Agent creates the learner profile.
- Tutor Agent retrieves grounded content and applies a Vietnamese teaching Skill.
- Evaluator Agent identifies misconceptions and recommends adaptation.
- Shared session state carries profile, lesson, and evaluation results.

## Course concepts demonstrated

1. Google ADK multi-agent system with specialist agents and shared state.
2. Read-only MCP server with allowlisted course resources.
3. Agent Skill using progressive disclosure, references, assets, and validation script.
4. Security policy, least privilege, prompt-injection detection, and deterministic guardrails.
5. Regression eval dataset, grounding/personalization checks, and structured traces.

## Safety and quality

Retrieved text is treated as untrusted data. MCP exposes no write or delete operation. Roadmaps and lesson duration are checked by code. Lessons require allowlisted source IDs, quiz difficulty is checked against the learner profile, and traces redact sensitive fields.

## Demonstration

The credential-free showcase runs diagnosis, five-day roadmap validation, course retrieval, content safety inspection, grounding and personalization evaluation, misconception detection, adaptive recommendation, and trace export.

```powershell
python scripts/demo_learning_flow.py
python -m pytest
```

## Limitations and next steps

The MVP contains one curated course catalog and local session state. Future work would add authenticated persistence, human-reviewed course ingestion, broader multilingual support, and longitudinal learning analytics.
