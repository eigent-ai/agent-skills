---
name: weekly-growth-tweet
description: |
  Collects feature announcement posts from the Eigent #growth Slack channel by Wendong Fan, filters for posts with the 1️⃣ (Keycap: 1) emoji reaction, and generates a weekly summary tweet. TRIGGERS: "weekly tweet", "growth channel summary", "weekly update tweet", "collect growth posts", "Eigent weekly recap", "summarize #growth", "draft weekly tweet".
license: Apache-2.0
metadata:
  author: Waleed Alzarooni
  version: "1.0"
---

# Weekly Growth Tweet Skill

Collect feature announcement posts from Slack's Eigent **#growth** channel (posted by **Wendong Fan**) from the past week, then synthesize them into a polished weekly summary tweet for Twitter/X.

## When to Use This Skill

- User asks for a weekly tweet or recap of Eigent updates
- User wants to summarize recent #growth channel posts
- User asks to draft a Twitter/X post based on Slack announcements
- User mentions collecting Wendong Fan's posts from #growth

## Workflow

### Step 1: Open Slack and Navigate to #growth

1. Navigate to **Slack** in the browser (https://app.slack.com)
2. Locate and open the **#growth** channel in the Eigent workspace
3. If not already logged in, prompt the user to log in first

### Step 2: Collect Posts from the Past Week

Scroll through the #growth channel and identify posts that meet **all** of the following criteria:

**Author filter:**
- Posted by **Wendong Fan**

**Format filter — Feature Announcement Style:**
Posts should follow this general structure:
- A **headline** describing the feature or improvement (e.g., "Eigent Now Lets You...")
- A **shoutout** to the contributor(s) (e.g., "Shoutout to @username for...")
- A **bullet list** of key capabilities or changes (using dashes or bullet points)
- A **closing line** thanking the contributor and/or linking to the PR
- A **link** to the GitHub PR (github.com/eigent-ai/eigent/pull/...)

Example matching post:
```
Eigent Now Lets You Open Agent Folders Directly in Your IDE!
Shoutout to @eureka928 for this nice quality-of-life improvement!

With this PR, you can now:
- One-Click Access: Open any agent's project folder directly in VS Code or Cursor from the Folder view
- Choose Your Editor: Pick your preferred IDE in Settings - we'll remember it

It makes jumping into agent code so much faster, thanks @eureka928 for making the dev experience a bit smoother!

Check it out: github.com/eigent-ai/eigent/pull/1159
```

**Reaction filter:**
- Post must have a reaction using the **1️⃣ (Keycap: 1)** emoji
- Look for the reaction bar below the post content
- This emoji indicates the post has been marked/approved for inclusion in the weekly summary

**Time filter:**
- Only collect posts from the **past 7 days** relative to the current date

### Step 3: Extract Key Information from Each Post

For each qualifying post, extract:
- **Feature name / headline** — the main improvement or addition
- **Category** — classify into one of: Enterprise Infrastructure & Security, Data Handling & Knowledge, Developer Experience, Community & Localization, Agent Capabilities, UI/UX Improvements, or create a new category if needed
- **Key capabilities** — the bullet points describing what's new
- **Contributor(s)** — GitHub username(s) mentioned (via @mentions)
- **PR link** — the GitHub pull request URL

### Step 4: Draft the Weekly Summary Tweet

Compose the tweet following this **exact style and tone** template:

```
Eigent weekly update ([Date Range])

[1-2 sentence hook about building in public or the week's theme]

[Category 1]
• [Feature]: [Brief description] (via [contributor]).
• [Feature]: [Brief description] (via [contributor]).

[Category 2]
• [Feature]: [Brief description] (via [contributor]).

[Category 3]
• [Feature]: [Brief description] (via [contributor]).

[Closing line thanking contributors]
```

**Style rules:**
- **Tone**: Professional but warm, community-focused, builder-oriented
- **Opening**: Always start with "Eigent weekly update ([date range])" followed by a thematic hook
- **Categories**: Group features into logical categories with bold headers
- **Bullet format**: Use "•" bullets, keep each to one line, include contributor attribution as "(via [github_username])"
- **Closing**: End with a thank-you to contributors — genuine and appreciative
- **Length**: Aim for a tweet thread or long-form tweet (280–1000 characters depending on volume)
- **Voice**: "Building in public" ethos — transparent, grateful, forward-looking

**Reference tweet for tone:**
```
Eigent weekly update (Feb 2–6)

Building in public means solving real-world problems. The latest Eigent updates focus heavily on enterprise readiness and developer experience.

Enterprise Infrastructure & Security
• Proxy Support: Full HTTP/SOCKS support. Configure network proxies directly in Settings (via bittoby).
• Observability: Built-in OpenTelemetry integration to track agent performance, costs, and error traces (via bytecraftii).
• Per-Agent Models: Optimize costs by assigning specific models to specific workers (via MkDev11).

Data Handling & Knowledge
• Local Knowledge: Built-in RAG capabilities allow agents to query internal documents securely using a local vector database (via MkDev11).
• Spreadsheet Integration: Browser agents can now read/write directly to Excel/Google Sheets for data-heavy workflows (via fengju0213).

Developer Experience
• IDE Integration: Open agent projects directly in VS Code or Cursor with one click (via eureka928).
• Native Windows App: Improved frame and system theme integration for Windows users (via glowsenior).
• Lint & Format: Full ESLint/Prettier setup for a cleaner codebase (via 4pmtong).

Community & Localization
• Portuguese Docs (via Caiodiv)
• Japanese Docs (via eltociear)
• Themes: Light, Dark, and Transparent modes now available (via cbum-dev).

A huge thank you to every contributor who submitted a PR, fixed a bug, or improved a doc.
```

### Step 5: Present Output

1. Show the user the collected posts (titles + contributors + PR links) as a summary table
2. Present the draft tweet for review
3. Ask the user if they want to adjust categories, wording, or emphasis before finalizing

## Browser Interaction Notes

- Use `read_page` and `find` tools to locate posts in the Slack message list
- Slack messages are typically rendered in a scrollable message pane; scroll up to load older messages within the week
- Reactions appear as small emoji icons below each message — look for the "1️⃣" keycap emoji specifically
- Post author can be identified by the display name above each message
- If the channel has many messages, use date dividers in Slack to efficiently navigate to the target week
- Use `get_page_text` to extract message content when needed

## Edge Cases

- **No qualifying posts found**: Inform the user that no posts by Wendong Fan with the 1️⃣ reaction were found in the past week
- **Few posts (1-2)**: Still draft a tweet but note it's a lighter week; adjust the hook accordingly
- **Many posts (10+)**: Group aggressively into categories; consider suggesting a tweet thread instead of a single tweet
- **Missing PR links**: Note which features are missing links and ask the user if they want to add them
- **Ambiguous categories**: Default to the closest match and let the user re-categorize in review

## Keywords

weekly tweet, growth channel, Slack summary, Eigent weekly update, #growth, Wendong Fan, feature announcements, weekly recap, Twitter post, X post, building in public
