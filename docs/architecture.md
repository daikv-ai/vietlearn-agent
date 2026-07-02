# VietLearn Agent Architecture

## Responsibilities

### Learning Coach

Coordinates the learning session, delegates tasks, and maintains the overall workflow.

### Diagnostic Agent

Scores the entry test, detects missing profile fields, and records knowledge gaps.

### Tutor Agent

Retrieves the current lesson, applies the Vietnamese explanation skill, and produces grounded teaching content.

### Evaluator Agent

Creates and scores quizzes, records misconceptions, and recommends how the next lesson should adapt.

## Context Strategy

### Static context

- mission and role boundaries;
- hard rules;
- short learner profile;
- tool schemas.

### Dynamic context

- current lesson;
- relevant glossary entries;
- latest quiz result;
- current misconception list.

## Trust Boundaries

- Course resources are untrusted input.
- MCP has no write or delete tools.
- The learner profile must not contain secrets.
- Policy checks run before any persisted roadmap is replaced.
- Tool calls and evaluation outcomes are logged without sensitive content.
