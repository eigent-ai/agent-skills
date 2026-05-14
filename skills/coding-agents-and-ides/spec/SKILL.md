---
name: spec
description: Write a comprehensive product or engineering specification before implementation. Use when the user asks for `/spec`, PRDs, feature specs, API specs, refactor specs, acceptance criteria, user stories, edge cases, or open decision tracking before code is written.
---

# Spec

## Overview

Use this skill to turn a feature, API, refactor, or product idea into a clear specification that can feed planning and implementation. The output should reduce ambiguity before code is written.

## Workflow

1. Identify the problem, goal, users, constraints, and non-goals.
1. Capture the current behavior or system context when relevant.
1. Define user stories or use cases with acceptance criteria.
1. Specify functional requirements, edge cases, error states, permissions, and data handling.
1. Include API, UI, migration, observability, performance, or rollout requirements when applicable.
1. List open decisions and assumptions explicitly.
1. Keep the spec implementation-aware but avoid over-prescribing internal code structure unless required.

## Output Pattern

Use this structure by default:

1. Summary.
1. Problem statement.
1. Goals and non-goals.
1. Users and use cases.
1. Requirements.
1. Acceptance criteria.
1. Edge cases and risks.
1. Observability, rollout, and rollback notes.
1. Open questions.

## Example Prompts

- `/spec - Build a CSV export feature for our analytics dashboard. Users need to export filtered data with custom date ranges. Support up to 100k rows.`
- `/spec - Design a public webhooks API for our platform. Third-party apps need to subscribe to user events and receive payloads reliably with retry logic.`
- `/spec - Refactor our authentication flow to support SSO. We need to keep existing email/password working and add Google and GitHub OAuth without breaking current sessions.`
