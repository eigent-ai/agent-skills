---
name: last30days
description: Research what people have discussed in the last 30 days across high-signal public platforms. Use when the user asks for `/last30days`, recent trend research, competitive intelligence, market pulse briefs, or engagement-ranked synthesis from Reddit, Hacker News, GitHub, X, YouTube, Polymarket, and similar sources.
---

# Last30Days

## Overview

Use this skill to produce a grounded brief on a topic using only recent public discussion and engagement signals. Prioritize sources from the last 30 days, rank findings by real engagement, and merge duplicate stories before synthesizing.

## Workflow

1. Clarify the topic, audience, and output format when they are not obvious.
1. Search relevant public platforms for the last 30 days:
   - Reddit, Hacker News, GitHub, X, YouTube, and Polymarket when relevant.
   - Topic-specific communities, handles, hashtags, repos, and keywords.
1. Capture engagement context such as upvotes, comments, stars, views, reposts, or prediction odds.
1. De-duplicate repeated stories across platforms and keep the strongest source links.
1. Rank findings by engagement and relevance, not by editorial placement.
1. Produce a concise brief with:
   - Executive summary.
   - Top themes and ranked evidence.
   - Notable disagreements or weak signals.
   - Source links and dates.
   - Practical implications for the user's decision.
1. If the user asks for `--emit=html`, produce a formatted HTML brief.
1. If the user asks for ELI5 after a run, rewrite the same findings in plain language without changing the evidence.

## Example Prompts

- `/last30days new claude code agent skills github trending` - find what skills are gaining traction this week across HN, Reddit, and GitHub.
- `/last30days Notion vs Obsidian knowledge management 2026` - summarize what people are actually saying across Reddit and X, ranked by engagement.
- `/last30days AI writing tools market sentiment --emit=html` - synthesize discussion from HN, X, and Polymarket into a shareable brief.
