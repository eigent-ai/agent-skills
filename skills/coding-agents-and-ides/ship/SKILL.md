---
name: ship
description: Plan launch readiness, staged rollouts, production monitoring, rollback, communications, and post-launch validation. Use when the user asks for `/ship`, pre-launch checklists, release readiness, staged rollout plans, feature flags, deployment monitoring, or rollback planning.
---

# Ship

## Overview

Use this skill to prepare a feature or change for production. The goal is to make launch decisions explicit: what ships, how it rolls out, what is monitored, when to stop, and how to recover.

## Workflow

1. Identify the release scope, owner, timeline, users affected, dependencies, and risk level.
1. Build a pre-launch checklist:
   - Tests, migrations, feature flags, documentation, support readiness, analytics, alerts, and runbooks.
1. Define rollout strategy:
   - Internal, beta, percentage rollout, region/account cohorts, or all-at-once when low risk.
1. Specify success metrics and guardrails:
   - Product metrics, reliability metrics, error rates, latency, revenue, support volume, and user feedback.
1. Create rollback and mitigation steps:
   - Flag disablement, revert path, data repair, comms, and owner escalation.
1. Plan launch communications for affected teams and users.
1. After launch, compare live metrics against expected ranges and decide whether to continue, pause, expand, or roll back.

## Output Pattern

- Release summary.
- Pre-launch checklist.
- Rollout stages and entry/exit criteria.
- Monitoring plan.
- Rollback plan.
- Communications plan.
- Post-launch validation steps.

## Example Prompts

- `/ship - We're deploying the new payments flow tomorrow. Walk me through the pre-launch checklist, what to monitor in the first hour, and our rollback plan if error rates spike.`
- `/ship - Plan a staged rollout for our new recommendation engine. Start at 5% traffic, define success metrics, and set the criteria for each expansion step to 100%.`
- `/ship - We shipped 3 hours ago. Here are the current metrics [paste]. Is anything outside normal range? Should we roll back or keep going?`
