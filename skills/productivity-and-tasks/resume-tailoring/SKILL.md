---
name: resume-tailoring
description: Tailor a resume to a job description with ATS keyword optimization, gap analysis, and rewritten bullets — zero fabrication. Use when the user wants /tailor for a single role, /batch for multiple JDs, career pivot reframing, or interview prep questions from a tailored application.
metadata:
  source-repo: https://github.com/varunr89/resume-tailoring-skill
---

# Resume Tailoring

AI-powered resume tailoring — gap analysis, ATS keywords, bullet reordering and rewriting. Every change grounded in existing content; no fabrication.

## Source Repository

- **GitHub:** [varunr89/resume-tailoring-skill](https://github.com/varunr89/resume-tailoring-skill)
- **Install upstream:** `npx skills add varunr89/resume-tailoring-skill`

---

## `/tailor`

Paste (or point to) resume + job description.

**Workflow:**
1. Parse the JD — required skills, seniority signals, keywords ATS will scan.
2. Map existing experience to requirements.
3. Rewrite bullets to lead with most relevant impact (action → scope → result).
4. Inject missing keywords only where honestly supported by existing experience.
5. Output tailored resume + gap analysis report.

**Gap analysis report includes:**
- Requirements fully covered
- Partial matches needing stronger framing
- Genuine gaps to address in cover letter or upskilling
- Suggested talking points for interviews

**Example prompts:**
- Tailor my resume [paste] for this job description [paste]. Emphasize relevant experience, add missing keywords, flag gaps for my cover letter.
- I'm applying for Staff Engineer. Elevate framing from IC execution to technical leadership, system thinking, cross-team impact.
- Moving from data analyst to PM — reframe analytical work as product thinking; note transferable skills and gaps.

---

## `/batch`

Processes 3–5 job descriptions in one run — uniquely tailored variant per JD.

**Output:**
- One tailored resume per role
- Diff summary per variant (what changed and why)
- Optional: best-fit role ranking and largest-gap role

**Example prompts:**
- Base resume [paste] + 4 job descriptions [paste all 4]. Generate tailored variants with diff summary per version.
- Run batch on 3 PM roles. After tailoring, tell me which fits best and which has the largest gap.
- After tailoring [resume + JD], generate 10 likely interview questions with suggested talking points.

---

## Output Formats

Deliver in the format requested:
- Markdown (default)
- DOCX (use docx skill if available)
- PDF (use pdf skill if available)

---

## Guardrails

**Zero fabrication policy:**
- Never invent employers, titles, dates, metrics, or skills not in the source resume.
- Reframe and emphasize — do not fabricate.
- When a JD keyword has no honest match, flag it in the gap analysis instead of inserting it.
- Preserve the user's voice; avoid generic corporate filler.
