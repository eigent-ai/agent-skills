---
name: humanizer
description: Detect and rewrite AI writing patterns to make content sound authentically human. Supports voice calibration from the author's own writing samples. Use when asked to humanize text, remove AI patterns, calibrate voice, audit content for AI detectability, or check if writing sounds like ChatGPT. Triggers: /humanize, /voice-calibrate, /audit-ai
---

## Overview

Detects and rewrites 29 AI writing patterns across content, language, style, and communication categories. Patterns include: significance inflation, vague attributions, copula avoidance, synonym cycling, em dash overuse, sycophantic tone, chatbot artifacts, and more. Also supports voice calibration from your own writing samples.

---

## /humanize

Full 29-pattern detection and rewrite. Analyzes the input for all AI-sounding patterns, rewrites the content, then runs a second-pass "obviously AI?" audit before returning the final version.

### Workflow

1. Receive the text to humanize and any brand voice notes.
2. Scan for all 29 patterns — flag each instance found.
3. Rewrite the text: fix flagged patterns, preserve the core argument and facts.
4. Run a second-pass audit: read the rewrite cold and ask "does any sentence still sound AI-generated?"
5. Return the final rewritten text with a brief summary of the main changes made.

### Example prompts

| Use case | Task prompt |
|---|---|
| Blog post | Humanize this blog post draft. Remove any AI-sounding patterns. Preserve the core argument but make it read like a person who actually has opinions wrote it. |
| LinkedIn | Rewrite this LinkedIn post. It currently sounds like ChatGPT wrote it. Cut the significance inflation, remove the em dashes, and make it direct. |
| Press release | Run the 29-pattern check on this press release. Flag every AI pattern you find, then rewrite it. The brand voice is confident and plain-spoken, not corporate. |

---

## /voice-calibrate

Accepts 2–3 writing samples from the target author, extracts their stylistic fingerprint (sentence rhythm, vocabulary, punctuation habits), then applies that fingerprint to any AI-generated text.

### Workflow

1. Receive 2–3 writing samples from the target author.
2. Analyze samples for: average sentence length, punctuation habits, vocabulary range, tonal register, structural patterns (how they open/close paragraphs), and idioms they favor.
3. Document the fingerprint as a short style profile.
4. Apply the fingerprint to the target AI text, rewriting to match the author's natural voice.
5. Return the rewritten text with the style profile so it can be reused in follow-up requests.

### Example prompts

| Use case | Task prompt |
|---|---|
| Newsletter | Here are 3 of my past newsletters [attached]. Use them to learn my voice, then rewrite this AI-drafted issue to match how I actually write. |
| CEO post | Calibrate to the CEO's voice using these 5 LinkedIn posts. Then rewrite this product announcement so it sounds like her, not our content team. |
| Personal brand | I want to post consistently on LinkedIn but don't have time to write from scratch. Learn my voice from these samples and rewrite these 5 AI drafts to match it. |

---

## /audit-ai

Scores text 0–100 for AI detectability across all 29 pattern categories. Highlights specific phrases most likely to trigger AI detectors and returns a prioritized fix list ranked by severity.

### Workflow

1. Receive the text to audit.
2. Score each of the 29 patterns 0–3 (0 = not present, 3 = severe).
3. Compute an overall AI detectability score (0–100, higher = more detectable).
4. Highlight the top phrases that are most suspicious.
5. Return the score, highlighted phrases, and a prioritized fix list (must-fix vs. nice-to-fix).

### Example prompts

| Use case | Task prompt |
|---|---|
| Pre-publish | Audit this article before we publish it. Give me an AI score, highlight the top 10 most suspicious phrases, and tell me which ones I absolutely must fix. |
| SEO content | Score these 5 blog posts for AI detectability. Rank them worst to best and give me a fix list for the 3 worst offenders. |
| Team workflow | Build me a pre-publish checklist based on the 29 patterns so our editors know what to review every time before anything goes live. |

---

## The 29 AI Writing Patterns

Organized into four categories:

**Content patterns:** significance inflation, vague attributions, unnecessary hedging, false balance, over-explaining obvious things, unsupported universal claims

**Language patterns:** copula avoidance ("utilizing" instead of "using"), synonym cycling (rotating synonyms to avoid repetition), em dash overuse, passive voice stacking, gerund chains, adverb padding

**Style patterns:** sycophantic openers, chatbot sign-off artifacts, hollow transitional phrases ("It's worth noting that…"), conclusion telegraphing ("In conclusion…"), bullet-point everything bias

**Communication patterns:** fence-sitting on opinions, corporate hedging language, artificial enthusiasm, filler affirmations ("Certainly!", "Great question!"), over-structured responses, meta-commentary about the writing itself
