---
name: seo-audit
description: Audit technical, on-page, and AI-search SEO for pages, sites, and content. Use when the user asks for `/seo-audit`, `/ai-seo`, SEO review, keyword targeting, heading structure, metadata, internal linking, content gaps, AEO, GEO, LLMO, or competitor SEO comparisons.
---

# SEO Audit

## Overview

Use this skill to evaluate how well a page or site can be discovered, understood, and cited by search engines and AI answer engines. Focus on prioritized fixes that connect directly to ranking, crawlability, conversion intent, or answer eligibility.

## Workflow

1. Identify the target page, keyword or query set, business goal, and audience.
1. Inspect the available page content, rendered HTML, metadata, and site structure.
1. Audit core on-page SEO:
   - Title, meta description, H1/H2 structure, URL, canonical, alt text, schema, and internal links.
   - Keyword intent alignment, content depth, duplication, and missing sections.
1. Audit technical risk where access permits:
   - Indexability, robots directives, performance signals, mobile rendering, broken links, redirects, and structured data validity.
1. For AI-search optimization, check whether the page provides concise answerable claims, clear entity relationships, sourceable facts, comparison language, and trustworthy proof.
1. Compare competitors when supplied and identify missing topics, formats, keywords, and proof points.
1. Deliver a prioritized fix list with expected impact, effort, and concrete edits.

## Output Pattern

Use this structure unless the user requests another format:

1. Summary of the strongest opportunities.
1. Critical fixes.
1. On-page recommendations.
1. Technical recommendations.
1. AI-search recommendations.
1. Content gap opportunities.
1. Suggested title, meta description, headings, and internal links when useful.

## Example Prompts

- `Run an SEO audit on this landing page [paste content]. Check keyword density, heading structure, meta description, and internal linking. Give me a prioritized fix list.`
- `Run /ai-seo on our homepage. We want to rank in AI-generated answers for "best project management tool for remote teams". What needs to change?`
- `Compare our blog content against these 3 competitor URLs. What topics are they ranking for that we're missing? Give me a content gap report.`
