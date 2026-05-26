---
name: open-design
description: Generate web, mobile, and desktop prototypes, slides, dashboards, and editorial layouts from a single prompt using brand-grade design systems. Use when the user wants /web-prototype, /mobile-app, or /dashboard interactive HTML previews exportable to HTML, PDF, PPTX, or MP4 without Figma.
metadata:
  source-repo: https://github.com/nexu-io/open-design
---

# Open Design

Local-first, open-source design system for rapid prototyping across web, mobile, and dashboards.

## Source Repository

- **GitHub:** [nexu-io/open-design](https://github.com/nexu-io/open-design)
- **Install upstream:** `npx skills add nexu-io/open-design`

Runs on Claude Code, Cursor, Codex, Gemini CLI, and Copilot. Outputs sandboxed HTML preview with export to HTML, PDF, PPTX, or MP4.

---

## `/web-prototype`

Generates a fully interactive web prototype from a text description — clickable HTML with real layout, components, and design system tokens. No Figma required.

**Workflow:**
1. Clarify product type, primary user flows, and aesthetic (minimal SaaS, dark theme, etc.).
2. Build sandboxed HTML with navigation between key views.
3. Apply design tokens for spacing, color, and typography.
4. Offer export format (HTML, PDF, PPTX, MP4).

**Example prompts:**
- Build a B2B invoicing tool prototype — dashboard, invoice list with status badges, create-invoice modal. Clean minimal SaaS aesthetic.
- Generate a landing page for an AI meeting notes product — hero with CTA, 3-feature grid, social proof, pricing table. Dark theme.
- Prototype an internal HR leave request portal — employee form, manager approve/reject queue. Simple and functional.

---

## `/mobile-app`

Generates pixel-accurate mobile app screens for iOS or Android — navigation, components, interaction states, spacing.

**Example prompts:**
- Design a habit tracker — today view with checkboxes, streak counter, weekly stats chart, settings. iOS style, clean and minimal.
- Generate a 4-screen onboarding flow for a food delivery app — welcome, location permission, cuisine picker, home feed. Bold, colorful.
- Design notification settings for a fintech app — toggle alert types, quiet hours, push vs email. Android Material 3.

---

## `/dashboard`

Generates data dashboard layouts — grid layouts, charts, KPI cards, tables, filters — as sandboxed HTML preview.

**Example prompts:**
- Build a SaaS analytics dashboard — MRR trend, churn KPI, active users by plan, top features, recent signups table.
- Design an ops monitoring dashboard — server uptime, error rate by endpoint, p95 latency, active deployments, incident log. Dark mode, high-density.
- Create an executive KPI dashboard — revenue vs target, burn rate, headcount by team, NPS trend, top 3 OKR progress bars. Boardroom-ready.

---

## Guardrails

- Confirm target platform (web/mobile/dashboard) before generating.
- Use realistic placeholder data — not lorem ipsum labels on charts.
- Keep prototypes focused on the requested flows; avoid over-scoping.
- Note export dependencies (PDF/PPTX/MP4) if tooling is unavailable.
