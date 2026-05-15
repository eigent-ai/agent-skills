---
name: review
description: Perform a direct five-axis code review across correctness, security, performance, readability, and maintainability. Use when the user asks for `/review`, PR review, security review, pre-merge review, production readiness review, or blocking issue assessment.
---

# Review

## Overview

Use this skill for code-review work. Prioritize bugs, behavioral regressions, security risks, performance issues, and missing tests. Findings come first, ordered by severity, with concrete file and line references whenever possible.

## Workflow

1. Inspect the requested diff, files, branch, or pull request context.
1. Review across five axes:
   - Correctness.
   - Security.
   - Performance.
   - Readability.
   - Maintainability.
1. Check whether tests cover the changed behavior and important failure modes.
1. Keep feedback specific and actionable; avoid broad style commentary unless it affects maintainability or correctness.
1. Flag issues by severity:
   - Blocking: should not ship.
   - High: likely bug, security issue, or serious regression.
   - Medium: meaningful risk or missing coverage.
   - Low: small maintainability or clarity improvement.
1. If no issues are found, say so clearly and mention residual test gaps or assumptions.

## Output Pattern

1. Findings first, ordered by severity.
1. Open questions or assumptions.
1. Brief change summary only after findings.
1. Tests or verification reviewed.

## Example Prompts

- `/review - Review this pull request. Flag anything that affects security, performance, or will be hard to maintain in 6 months. Be direct about blocking issues.`
- `/review - Audit this API endpoint handler for security issues. Check for injection risks, missing auth checks, improper error handling, and data exposure.`
- `/review - This is going to production tomorrow. Do a final review focused only on breaking changes, regressions, and anything that could cause an incident.`
