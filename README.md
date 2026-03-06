# Agent Skills

A collection of skills for AI coding agents when building Eigent. 

Skills follow the [Agent Skills](https://agentskills.io/) format.

## Available Skills

Skills are organized by category under `skills/{category}/{skill-name}`:

- **developer-tools**
- **ai-and-agent-systems**
- **productivity-and-knowledge-work**
- **personal-and-consumer-use-cases**
- **ecosystem-specific**

### Developer Tools

| Skill | Description | Author |
| --- | --- | --- |
| [`mintlify-docs-updater`](skills/developer-tools/mintlify-docs-updater/SKILL.md) | Maintain Mintlify documentation from uploaded Markdown files. Handles page placement under `docs/`, required frontmatter checks, and `docs/docs.json` navigation updates via `ingest_markdown_doc.py`. | Douglas Lai |

### AI and Agent Systems

| Skill | Description | Author |
| --- | --- | --- |
| [`eigent-design`](skills/ai-and-agent-systems/eigent-design/SKILL.md) | Plan new UIs or audit existing UIs. Covers UI/UX design, token compliance, interaction quality, and accessibility with `Design Guide` (pre-build spec) and `Design Review` (post-build checklist) modes. | Douglas Lai |

### Productivity and Knowledge Work

| Skill | Description | Author |
| --- | --- | --- |
| [`weekly-growth-tweet`](skills/productivity-and-knowledge-work/weekly-growth-tweet/SKILL.md) | Collect feature announcement posts from the Eigent #growth Slack channel (by Wendong Fan), filter for posts with the 1️⃣ emoji reaction, and generate a weekly summary tweet. Triggers: weekly tweet, growth channel summary, weekly update tweet, collect growth posts, Eigent weekly recap, summarize #growth, draft weekly tweet. | Waleed Alzarooni |

### Personal and Consumer Use Cases

| Skill | Description | Author |
| --- | --- | --- |
| _TBD_ | Category placeholder for future skills. | — |

### Ecosystem-Specific

| Skill | Description | Author |
| --- | --- | --- |
| [`eigent-server-sync`](skills/ecosystem-specific/eigent-server-sync/SKILL.md) | Transfer eigent server PRs to eigent_server. Use when syncing changes from eigent/server/ to eigent_server, when an eigent PR modifies server code that needs to be reflected in eigent_server, or when porting eigent server features. | Ahmed Awelkair |
| [`eigent-blog-update`](skills/ecosystem-specific/eigent-blog-update/SKILL.md) | Create, edit, and structure blog posts for Eigent. Handles blog content operations, frontmatter metadata, asset organization, and includes `generate_post.py` plus optional Git PR handoff. | Douglas Lai |
| [`eigent-usecase-update`](skills/ecosystem-specific/eigent-usecase-update/SKILL.md) | Create, edit, and manage usecase entries for Eigent. Covers usecase JSON authoring, media asset linkage, SEO metadata, and includes `generate_usecase.py` plus optional Git PR handoff. | Douglas Lai |

## Available Packages (ZIP)

- `eigent-design` - [Download ZIP](./packages/ai-and-agent-systems/eigent-design.zip)
- `mintlify-docs-updater` - [Download ZIP](./packages/developer-tools/mintlify-docs-updater.zip)
- `weekly-growth-tweet` - [Download ZIP](./packages/productivity-and-knowledge-work/weekly-growth-tweet.zip)
- `eigent-server-sync` - [Download ZIP](./packages/ecosystem-specific/eigent-server-sync.zip)
- `eigent-blog-update` - [Download ZIP](./packages/ecosystem-specific/eigent-blog-update.zip)
- `eigent-usecase-update` - [Download ZIP](./packages/ecosystem-specific/eigent-usecase-update.zip)

## Installation

Install the full skill pack (all categories) with:

```bash
npx skills add eigent-ai/agent-skills
```

After installation, skills are available under the category layout `skills/{developer-tools,ai-and-agent-systems,productivity-and-knowledge-work,personal-and-consumer-use-cases,ecosystem-specific}/{skill-name}/SKILL.md`.

## Usage

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

Examples:

- "Create a design guide for this new settings page."
- "Sync this eigent PR's server changes to eigent_server."
- "Ingest this Markdown file into Mintlify docs and update docs.json navigation."
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
