---
name: legal-work-plugin
description: In-house legal workflows for contract review against playbooks, NDA triage with GREEN/YELLOW/RED ratings, compliance briefings, and vendor checks. Use when the user invokes /review-contract, /triage-nda, /legal-risk-assessment, or /vendor-check for organisation-standard legal analysis.
metadata:
  source-repo: https://github.com/anthropics/knowledge-work-plugins
---

# Legal Work Plugin

Anthropic's knowledge work plugin suite — legal plugin for in-house counsel workflows.

## Source Repository

- **GitHub:** [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)
- **Install upstream:** `npx skills add anthropics/knowledge-work-plugins`

Connects to Slack, Box, Egnyte, Jira, and Microsoft 365 when configured.

---

## `/review-contract`

Reviews incoming contracts against the organisation's negotiation playbook.

**Workflow:**
1. Load or ask for the negotiation playbook (standard terms, liability caps, IP, termination, etc.).
2. Compare each clause to playbook standards.
3. Flag deviations by severity.
4. Classify each issue: **blocker** / **negotiate** / **accept**.
5. Draft redline language for blockers in house style.
6. Produce business impact summary alongside legal analysis.

**Pair with `/legal-risk-assessment`** for scored output and escalation recommendation.

**Example prompts:**
- Review this vendor MSA [paste]. Flag playbook deviations. Classify as blocker/negotiate/accept; draft redlines for blockers.
- Review-contract then legal-risk-assessment — severity breakdown (critical/high/medium/low) and escalation: can legal sign off or needs CFO?
- `/vendor-check [vendor name]` — status of existing agreements, renewals, open issues, prior accepted deviations.

---

## `/triage-nda`

Rapid first-pass NDA screening before lawyer review.

**Output:**
- **GREEN** — sign as-is
- **YELLOW** — negotiate specific clauses
- **RED** — escalate to counsel

Includes key reason, routing recommendation, and clauses that triggered the flag.

**Example prompts:**
- Triage this NDA from a new partner [paste]. GREEN/YELLOW/RED? What triggered the rating?
- Batch triage 5 NDAs [paste sequentially]. Rating per NDA; flag only those needing human review. Output as table.
- Triage NDA then brief — signing with [company] tomorrow. Triage + 5-minute briefing on conversation watchpoints.

---

## Playbook Setup

If no playbook exists, run a quick intake:
- Standard liability cap formula
- Acceptable indemnification scope
- IP ownership defaults
- Termination rights
- Data processing requirements
- Non-compete / non-solicit policy

Store answers for consistent future reviews.

---

## Guardrails

- Decision support only — not a substitute for licensed counsel.
- When playbook conflicts with user's stated priorities, ask which takes precedence.
- For RED NDAs, always list specific clauses and suggested fallback language.
- Batch triage: use a consistent table format for quick scanning.
