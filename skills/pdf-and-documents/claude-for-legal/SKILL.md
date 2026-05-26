---
name: claude-for-legal
description: Full legal plugin suite for commercial contract review, privacy/DPA analysis, and AI governance vendor reviews. Use when the user invokes /commercial-legal:review, /privacy-legal:dpa-review, /ai-governance-legal:vendor-ai-review, renewal tracking, DSAR responses, or EU AI Act triage.
metadata:
  source-repo: https://github.com/anthropics/claude-for-legal
---

# Claude for Legal

100+ skills across 13 practice-area plugins. Each plugin learns your playbook via cold-start interview and writes a practice profile every skill reads from.

## Source Repository

- **GitHub:** [anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal)
- **Install upstream:** `/plugin install commercial-legal@claude-for-legal` (Claude Code) or `npx skills add anthropics/claude-for-legal`

Verified citations via CourtListener, Trellis, and Westlaw (via Thomson Reuters CoCounsel plugin).

---

## `/commercial-legal:review`

Reviews vendor MSAs, NDAs, and SaaS agreements against your negotiation playbook. Tracks amendment history, flags renewal deadlines, routes escalations with draft asks.

**Example prompts:**
- Review this vendor MSA [paste] — we're the customer. Check liability cap (must be 2x fees), data processing, IP ownership, termination for convenience. Draft redlines for every deviation.
- `/commercial-legal:renewal-tracker` — contracts with cancel-by deadlines in next 90 days. Current terms, last accepted deviations, recommended action: renew/renegotiate/terminate.
- `/commercial-legal:amendment-history` — renegotiating with [vendor]. Full amendment history [paste base + amendments]: what changed at each step and what we gave up.

---

## `/privacy-legal:dpa-review`

Reviews Data Processing Agreements as controller or processor. Checks GDPR Article 28 requirements, flags missing mandatory provisions, redlines deviations from standard DPA template.

**Companion skills:** DPIA generation, DSAR drafting, regulation gap analysis.

**Example prompts:**
- Review this DPA [paste] — we are the controller. Check Article 28 mandatory clauses, flag missing provisions, redline liability/audit shifts away from us.
- `/privacy-legal:dsar-response` — DSAR from [name] on [date]. Draft acknowledgment letter and fulfillment steps within GDPR 30-day window.
- `/privacy-legal:reg-gap-analysis` — compare privacy policy [paste] against latest GDPR and CCPA. Gaps prioritised by regulatory risk with redraft recommendations.

---

## `/ai-governance-legal:vendor-ai-review`

Reviews AI vendor contracts for governance risks — EU AI Act classification, data usage rights, model training opt-outs, liability for AI outputs, audit provisions.

**Companion skills:** AI Impact Assessments, internal AI usage policy drafts.

**Example prompts:**
- CRM vendor updated terms with AI features [paste]. New AI provisions? Training on our data? Conflicts with AI governance policy?
- `/ai-governance-legal:use-case-triage` — deploying AI for [use case]. EU AI Act classification: prohibited/high-risk/limited-risk/minimal-risk? Compliance steps before deployment?
- `/ai-governance-legal:policy-starter` — draft internal AI usage policy for 200-person B2B SaaS. Cover approved tools, prohibited uses, data handling, employee obligations, review cadence.

---

## Practice Profile Setup

On first use, run cold-start interview for the relevant practice area:
1. Organisation type and size
2. Standard templates and non-negotiables
3. Escalation paths and approvers
4. Jurisdiction and regulatory scope

Save the profile for consistent future reviews.

---

## Guardrails

- Decision support only — not legal advice.
- Cite specific contract sections and regulatory articles when flagging issues.
- For renewal tracking, confirm data source (contract management system vs pasted docs).
- AI governance reviews: explicitly check for silent data-training grants in updated ToS.
