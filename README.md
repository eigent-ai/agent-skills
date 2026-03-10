# Agent Skills

A collection of skills for AI coding agents when building Eigent.

Skills follow the [Agent Skills](https://agentskills.io/) format.

## Available Skills

Skills are organized by category under `skills/{category}/{skill-name}`:

### Tier 1 — High Priority

#### AI & LLMs
_TBD — Category placeholder for future skills._

#### Coding Agents & IDEs

| Skill | Description |
| --- | --- |
| [`mintlify-docs-updater`](skills/coding-agents-and-ides/mintlify-docs-updater/SKILL.md) | Maintain Mintlify documentation from uploaded Markdown files. Handles page placement under `docs/`, required frontmatter checks, and `docs/docs.json` navigation updates via `ingest_markdown_doc.py`. |

#### Web & Frontend Development

| Skill | Description |
| --- | --- |
| [`eigent-design`](skills/web-and-frontend-development/eigent-design/SKILL.md) | Plan new UIs or audit existing UIs. Covers UI/UX design, token compliance, interaction quality, and accessibility with `Design Guide` (pre-build spec) and `Design Review` (post-build checklist) modes. |
| [`frontend-design`](skills/web-and-frontend-development/frontend-design/SKILL.md) | Create distinctive, production-grade frontend interfaces with high design quality. Generates creative, polished web components, pages, and applications that avoid generic AI aesthetics. |
| [`brand-guidelines`](skills/web-and-frontend-development/brand-guidelines/SKILL.md) | Apply Anthropic's official brand colors and typography to artifacts. Use when brand styling, visual formatting, or company design standards apply. |

#### DevOps & Cloud
_TBD — Category placeholder for future skills._

#### Browser & Automation
_TBD — Category placeholder for future skills._

#### Search & Research
_TBD — Category placeholder for future skills._

#### Marketing & Sales

| Skill | Description |
| --- | --- |
| [`weekly-growth-tweet`](skills/marketing-and-sales/weekly-growth-tweet/SKILL.md) | Collect feature announcement posts from the Eigent #growth Slack channel (by Wendong Fan), filter for posts with the 1️⃣ emoji reaction, and generate a weekly summary tweet. |
| [`eigent-blog-update`](skills/marketing-and-sales/eigent-blog-update/SKILL.md) | Create, edit, and structure blog posts for Eigent. Handles blog content operations, frontmatter metadata, asset organization, and includes `generate_post.py` plus optional Git PR handoff. |
| [`eigent-usecase-update`](skills/marketing-and-sales/eigent-usecase-update/SKILL.md) | Create, edit, and manage usecase entries for Eigent. Covers usecase JSON authoring, media asset linkage, SEO metadata, and includes `generate_usecase.py` plus optional Git PR handoff. |

#### Data & Analytics
_TBD — Category placeholder for future skills._

#### Image & Video Generation

| Skill | Description |
| --- | --- |
| [`algorithmic-art`](skills/image-and-video-generation/algorithmic-art/SKILL.md) | Create algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Generates generative art from algorithmic philosophies expressed as flow fields, particle systems, and noise fields. |
| [`canvas-design`](skills/image-and-video-generation/canvas-design/SKILL.md) | Create beautiful visual art in .png and .pdf documents using design philosophy. Generates posters, artwork, and static visual pieces with curated typography and intentional composition. |

#### Git & GitHub

| Skill | Description |
| --- | --- |
| [`eigent-server-sync`](skills/git-and-github/eigent-server-sync/SKILL.md) | Transfer eigent server PRs to eigent_server. Use when syncing changes from eigent/server/ to eigent_server, when an eigent PR modifies server code that needs to be reflected in eigent_server, or when porting eigent server features. |

### Tier 2 — Strong Supporting Pages

#### Productivity & Tasks
_TBD — Category placeholder for future skills._

#### PDF & Documents

| Skill | Description |
| --- | --- |
| [`docx`](skills/pdf-and-documents/docx/SKILL.md) | Create, read, edit, and manipulate Word documents (.docx files). Handles professional formatting, tracked changes, comments, tables of contents, and includes helper scripts for document operations. |

#### Speech & Transcription
_TBD — Category placeholder for future skills._

#### Communication
_TBD — Category placeholder for future skills._

#### Security & Passwords
_TBD — Category placeholder for future skills._

### Tier 3 — Niche but Valuable

#### CLI Utilities
_TBD — Category placeholder for future skills._

#### Notes & Knowledge Management
_TBD — Category placeholder for future skills._

#### Apple & Mobile Development
_TBD — Category placeholder for future skills._

#### Shopping & E-commerce
_TBD — Category placeholder for future skills._

#### Finance
_TBD — Category placeholder for future skills._

### Bonus / Future

#### Agent-to-Agent Protocols
_TBD — Category placeholder for future skills._

## Installation

### Quick Install (all agents)

```bash
npx @eigent-ai/agent-skills install
```

This auto-detects installed agents (Claude Code, Cursor, Windsurf, Codex, Copilot) and installs skills to each.

### Install specific skills only

```bash
npx @eigent-ai/agent-skills install eigent-design
npx @eigent-ai/agent-skills install eigent-design mintlify-docs-updater eigent-blog-update
```

Use `npx @eigent-ai/agent-skills list` to see all available skills.

### Install for a specific agent

```bash
npx @eigent-ai/agent-skills install -a claude-code
npx @eigent-ai/agent-skills install -a cursor eigent-design
```

### Install globally (user-level)

```bash
npx @eigent-ai/agent-skills install -g
```

### Via the Skills ecosystem

```bash
npx skills add eigent-ai/agent-skills
```

## Updating

Pull the latest skills from GitHub:

```bash
npx @eigent-ai/agent-skills update
```

The CLI tracks a content hash so it only writes when there are actual changes.

### Auto-update

Set up scheduled updates with a cron job:

```bash
npx @eigent-ai/agent-skills auto-update              # weekly (default)
npx @eigent-ai/agent-skills auto-update --interval daily
```

This prints the cron line to add to your crontab.

## CLI Reference

| Command | Description |
| --- | --- |
| `install [skill...]` | Install all skills (or specific skills) to detected agents |
| `update` | Fetch latest from GitHub and update |
| `uninstall [skill...]` | Remove all or specific installed skills |
| `list` | List available skills in this package |
| `status` | Show install status per agent |
| `auto-update` | Print cron setup for scheduled updates |
| `doctor` | Check which agents are detected |

**Flags:** `--agent, -a` (target agent), `--global, -g` (user-level), `--yes, -y` (skip prompts)

## Usage

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

Examples:

- "Create a design guide for this new settings page."
- "Sync this eigent PR's server changes to eigent_server."
- "Ingest this Markdown file into Mintlify docs and update docs.json navigation."
- "Create a new blog post for this feature launch."
- "Create or update a usecase JSON and prepare an optional PR."
- "Draft the weekly growth tweet from #growth channel posts."
- "Create a generative art piece with flow fields and particle systems."
- "Design a poster with bold typography and intentional composition."
- "Build a landing page with distinctive, production-grade design."
- "Create a Word document with tracked changes and comments."
- "Apply Anthropic brand colors to this component."

## Skill Structure

Each skill contains:

- `SKILL.md` - Instructions for the agent
- `scripts/` - Helper scripts for automation (optional)
- `references/` - Supporting documentation (optional)
- `assets/` - Templates or static resources used by the skill (optional)

## License

Apache License 2.0. See `LICENSE` for the full text.
