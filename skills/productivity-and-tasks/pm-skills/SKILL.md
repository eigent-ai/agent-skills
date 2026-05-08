---
name: pm-skills
description: Product management workflows covering the full work lifecycle — discovery, strategy, execution, launch, and growth. Write PRDs, plan OKRs, and structure meeting notes. Useful beyond PMs — applicable to any knowledge worker managing projects, stakeholders, or strategy. Triggers: /write-prd, /plan-okrs, /meeting-notes
author: phuryn (github.com/phuryn/pm-skills)
---

## Overview

65 skills and 36 chained workflows covering the full PM work lifecycle. The three core skills below cover the most common PM artifacts: requirements, goal-setting, and meeting capture. Each produces a structured, shareable output ready to hand off to stakeholders or a team.

---

## /write-prd

Drafts a full product requirements document from a brief description. Includes problem statement, user stories, assumptions, edge cases, acceptance criteria, and open questions.

### Workflow

1. Gather: feature name, the problem it solves, primary users, and any known constraints.
2. Write the problem statement — one paragraph, no solution language yet.
3. Draft user stories: "As a [role], I want [action] so that [outcome]." Cover the primary flow and at least 2 edge cases.
4. List assumptions (what must be true for this to work) and open questions (what needs a decision).
5. Write acceptance criteria for each user story — specific, testable, binary pass/fail.
6. Return the full PRD in a structured format ready to paste into Notion, Confluence, or a doc.

### Example prompts

| Use case | Task prompt |
|---|---|
| New feature | Write a PRD for a notification preferences center. Users need granular control over email, push, and in-app alerts by category. Include edge cases for users on multiple devices. |
| Internal tool | Write a PRD for an internal expense reporting tool. Finance team needs to approve, reject, and request more info. Current process is email-based and takes 2 weeks. |
| API product | Write a PRD for a public API rate limiting dashboard. Developers need to monitor usage, set alerts, and upgrade their plan without contacting sales. |

---

## /plan-okrs

Generates a full OKR set from a goal or initiative — key results with measurable targets, leading indicators, and a tracking cadence. Also reviews existing OKRs for clarity and measurability.

### Workflow

1. Understand the objective: what outcome are we driving toward and over what timeframe?
2. Draft 3–5 key results — each must be quantitative, have a baseline and a target, and be achievable in the timeframe.
3. For each key result, identify a leading indicator (an early signal that you're on track) and a tracking cadence (weekly/bi-weekly check-in metric).
4. If reviewing existing OKRs: flag key results that are vague, unmeasurable, or don't ladder to the objective. Rewrite the weakest ones.
5. Return the full OKR set in a format ready for planning docs or OKR tools.

### Example prompts

| Use case | Task prompt |
|---|---|
| Quarterly planning | Write OKRs for our growth team next quarter. Goal: improve activation rate for new signups. We currently have a 22% 7-day activation rate and want to reach 35%. |
| OKR review | Review these OKRs and tell me which key results are too vague, which are unmeasurable, and rewrite the weakest three. |
| Team alignment | We have 4 team OKRs but they don't ladder up to the company goal of expanding into enterprise. Rewrite them so the connection is clear. |

---

## /meeting-notes

Turns a raw meeting transcript or bullet-point notes into structured output: decisions made, action items with owners, open questions, and a short summary for stakeholders who weren't there.

### Workflow

1. Receive the transcript or raw notes (paste or attach).
2. Extract decisions — concrete choices that were made and won't be revisited.
3. Extract action items — each with a clear owner and, if mentioned, a due date.
4. Extract open questions — things raised but not resolved, that need a follow-up.
5. Write a 3–5 sentence summary suitable for sharing with stakeholders who weren't in the meeting.
6. Return the structured output in this order: Summary → Decisions → Action Items → Open Questions.

### Example prompts

| Use case | Task prompt |
|---|---|
| Transcript | Here's the transcript from our roadmap planning meeting. Extract all decisions, action items with owners, and anything that needs a follow-up before next week. |
| Rough notes | I jotted down these notes during the design review. Turn them into a clean meeting summary I can share with the team and stakeholders. |
| Standup digest | Here are this week's daily standup notes. Summarize what each person worked on, what's blocked, and what shipped. Flag anything that needs my attention. |
