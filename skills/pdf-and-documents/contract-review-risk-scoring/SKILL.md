---
name: contract-review-risk-scoring
description: Review contracts with clause-by-clause risk scoring, market benchmarks, negotiability ratings, and redline suggestions. Use when the user pastes an NDA, SaaS/MSA, M&A LOI, or payment agreement and wants a Contract Safety Score, CUAD-based risk breakdown, or /review as [position] analysis.
metadata:
  source-repo: https://github.com/evolsb/claude-legal-skill
---

# Contract Review & Risk Scoring

Focused contract review built on CUAD (41 risk categories), ContractEval benchmarks, and LegalBench.

## Source Repository

- **GitHub:** [evolsb/claude-legal-skill](https://github.com/evolsb/claude-legal-skill)
- **Install upstream:** `npx skills add evolsb/claude-legal-skill`

Covers NDAs, SaaS/MSA, M&A, payment agreements, and finder/broker agreements.

---

## `/review [contract] as [your position]`

Core skill. Reads the full contract, maps clauses against CUAD's 41 risk categories, assigns severity (low / medium / high / critical), benchmarks key terms against market norms, and outputs a prioritised fix list with concrete redline language. Finishes with an overall **Contract Safety Score**.

**Workflow:**
1. Confirm document type and user's position (customer, vendor, receiving party, acquirer, etc.).
2. Parse and enumerate all material clauses.
3. Score each clause against CUAD risk categories.
4. Benchmark flagged terms vs market norms.
5. Assign negotiability rating per issue (easy / moderate / hard).
6. Draft specific redline language for top issues.
7. Output Contract Safety Score (0–100) with summary.

**Output structure:**
```
## Contract Safety Score: [score]/100

## Critical Issues (fix before signing)
## High / Medium / Low Issues
## Market Benchmark Comparison
## Recommended Redlines (prioritised)
## Negotiation Strategy Notes
```

---

## Example Prompts

- Review this NDA [paste] — I'm the receiving party. Flag unusual confidentiality scope, one-sided carve-outs, non-compete buried in obligations. Contract Safety Score + top 3 redlines.
- Review this SaaS subscription agreement [paste] — I'm the customer. Check liability caps, data ownership, unilateral change clauses, auto-renewal. Compare to market norms.
- Review this LOI [paste] — I'm the acquirer. Flag provisions locking us in early, limiting diligence rights, or unusual exclusivity. Score overall risk; critical issues first.

---

## Guardrails

- This is decision support, not legal advice. Include a disclaimer when delivering output.
- Do not skip boilerplate — buried risk often lives in definitions and general provisions.
- When contract text is incomplete, state what cannot be assessed.
- Prefer specific redline language over vague "negotiate this" notes.
