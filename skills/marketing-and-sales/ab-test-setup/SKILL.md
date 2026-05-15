---
name: ab-test-setup
description: Design, analyze, and document A/B tests for conversion, onboarding, pricing, lifecycle, and product experiments. Use when the user asks for `/ab-test-setup`, experiment design, sample size, statistical significance, A/B test analysis, ICE-scored test backlogs, or avoiding common testing mistakes.
---

# A/B Test Setup

## Overview

Use this skill to guide the full experiment lifecycle: hypothesis, design, sample size, implementation, analysis, and playbook documentation. Keep tests focused, measurable, and resistant to common errors like peeking early or testing too many changes at once.

## Workflow

1. Define the business goal, user segment, current baseline, target metric, and guardrail metrics.
1. Write a specific hypothesis:
   - `If we change X for audience Y, metric Z will improve because...`
1. Design the test:
   - Control and variant.
   - Primary metric.
   - Secondary and guardrail metrics.
   - Traffic split, eligibility, exclusions, and duration.
1. Estimate sample size or minimum detectable effect when baseline traffic and conversion rates are available.
1. Create an implementation checklist:
   - Tracking, randomization, QA, exposure logging, analytics events, and rollback.
1. Define decision rules before launch:
   - Ship, revert, iterate, or continue testing.
1. Analyze results after the test reaches the agreed sample size.
1. Document what changed, what was learned, and follow-up experiments.

## Test Backlog Pattern

When building a backlog, score each idea with ICE:

- Impact: expected business or user benefit.
- Confidence: evidence quality.
- Effort: complexity and implementation cost.

Prioritize tests that combine high impact, credible evidence, and low operational risk.

## Example Prompts

- `I want to A/B test our signup CTA button. Current conversion rate is 3.2%, 8,000 visitors/month. Help me design the test, calculate the required sample size, and define what success looks like.`
- `Our A/B test just hit sample size. Here are the results [paste metrics]. Is this statistically significant? Should we ship the variant, revert, or keep testing?`
- `Build a prioritized A/B test backlog for our onboarding flow. Use ICE scoring. Sources to mine: our drop-off analytics, last month's support tickets, and these 3 heatmap observations.`
