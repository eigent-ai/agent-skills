# Agent Skills

A collection of skills for AI coding agents when building Eigent. 

Skills follow the [Agent Skills](https://agentskills.io/) format.

## Available Skills

Skills are organized by department under `skills/{department}/{skill-name}`:

- **engineering**
- **growth**
- **operation-finance**
- **product**

### Engineering

| Skill | Description | Author |
| --- | --- | --- |
| [`eigent-design`](skills/engineering/eigent-design/SKILL.md) | Plan new UIs or audit existing UIs. Covers UI/UX design, token compliance, interaction quality, and accessibility with `Design Guide` (pre-build spec) and `Design Review` (post-build checklist) modes. | Douglas Lai |
| [`eigent-server-sync`](skills/engineering/eigent-server-sync/SKILL.md) | Transfer eigent server PRs to eigent_server. Use when syncing changes from eigent/server/ to eigent_server, when an eigent PR modifies server code that needs to be reflected in eigent_server, or when porting eigent server features. | Ahmed Awelkair |

### Growth

| Skill | Description | Author |
| --- | --- | --- |
| [`eigent-blog-update`](skills/growth/eigent-blog-update/SKILL.md) | Create, edit, and structure blog posts for Eigent. Handles blog content operations, frontmatter metadata, asset organization, and includes `generate_post.py` plus optional Git PR handoff. | Douglas Lai |
| [`eigent-usecase-update`](skills/growth/eigent-usecase-update/SKILL.md) | Create, edit, and manage usecase entries for Eigent. Covers usecase JSON authoring, media asset linkage, SEO metadata, and includes `generate_usecase.py` plus optional Git PR handoff. | Douglas Lai |
| [`weekly-growth-tweet`](skills/growth/weekly-growth-tweet/SKILL.md) | Collect feature announcement posts from the Eigent #growth Slack channel (by Wendong Fan), filter for posts with the 1️⃣ emoji reaction, and generate a weekly summary tweet. Triggers: weekly tweet, growth channel summary, weekly update tweet, collect growth posts, Eigent weekly recap, summarize #growth, draft weekly tweet. | Waleed Alzarooni |

### Operation-Finance

| Skill | Description | Author |
| --- | --- | --- |
| _TBD_ | Department placeholder for future skills. | — |

### Product

| Skill | Description | Author |
| --- | --- | --- |
| _TBD_ | Department placeholder for future skills. | — |

## Available Packages (ZIP)

- `eigent-design` - [Download ZIP](./packages/eigent-design.zip)
- `eigent-server-sync` - [Download ZIP](./packages/eigent-server-sync.zip)
- `eigent-blog-update` - [Download ZIP](./packages/eigent-blog-update.zip)
- `eigent-usecase-update` - [Download ZIP](./packages/eigent-usecase-update.zip)
- `weekly-growth-tweet` - [Download ZIP](./packages/weekly-growth-tweet.zip)

## Installation

Install the full skill pack (all departments) with:

```bash
npx skills add eigent-ai/agent-skills
```

After installation, skills are available under the departmental layout `skills/{engineering,growth,operation-finance,product}/{skill-name}/SKILL.md`.

## Usage

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

Examples:

- "Create a design guide for this new settings page."
- "Sync this eigent PR's server changes to eigent_server."
- "Create a new blog post for this feature launch."
- "Create or update a usecase JSON and prepare an optional PR."
- "Draft the weekly growth tweet from #growth channel posts."

## Skill Structure

Each skill contains:

- `SKILL.md` - Instructions for the agent
- `scripts/` - Helper scripts for automation (optional)
- `references/` - Supporting documentation (optional)
- `assets/` - Templates or static resources used by the skill (optional)

## License

Apache License 2.0. See `LICENSE` for the full text.
