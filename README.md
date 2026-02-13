# Agent Skills

A collection of skills for AI coding agents when building Eigent. 

Skills follow the [Agent Skills](https://agentskills.io/) format.

## Available Skills

1. **ui-ux-design** (`skills/eigent-design/SKILL.md`)
   - **Use when:** You need to plan a new UI (design guide) or audit an existing UI (design review).
   - **Category covered:** UI/UX design, token compliance, interaction quality, accessibility.
   - **Feature:** Two modes: `Design Guide` (pre-build spec) and `Design Review` (post-build checklist with severity).
   - **How it works:** Reads design references and outputs a structured markdown guide/review with concrete tokens, states, and fixes.
   - **Result:** Implementation-ready design specs or actionable UI review findings.

2. **eigent-blog** (`skills/eigent-blog-update/SKILL.md`)
   - **Use when:** You need to create, edit, or structure blog posts for Eigent.
   - **Category covered:** Blog content operations, frontmatter metadata, blog asset organization.
   - **Feature:** Includes `generate_post.py` template generation, frontmatter/directory rules, and optional Git PR handoff.
   - **How it works:** Generates or validates post structure (`.md/.mdx`), required metadata, asset paths, and can optionally guide branch/commit/PR flow.
   - **Result:** Publish-ready blog posts with consistent formatting and SEO-friendly metadata, with optional PR ready for review.

3. **eigent-usecases** (`skills/eigent-usecase-update/SKILL.md`)
   - **Use when:** You need to create, edit, or manage usecase entries for Eigent.
   - **Category covered:** Usecase JSON authoring, media asset linkage, SEO metadata.
   - **Feature:** Includes `generate_usecase.py`, updated JSON/template schema (`uploadDate`, replay URL, media paths), and optional Git PR handoff.
   - **How it works:** Builds valid usecase JSON with required fields and maps image/video assets in `public/gallery/`, then can optionally guide branch/commit/PR flow.
   - **Result:** Valid, display-ready usecase entries with consistent structure and discoverability, with optional PR ready for review.

## Available Packages (ZIP)

- `ui-ux-design` - [Download ZIP](./packages/eigent-design.zip)
- `eigent-blog` - [Download ZIP](./packages/eigent-blog-update.zip)
- `eigent-usecases` - [Download ZIP](./packages/eigent-usecase-update.zip)

## Installation

```bash
npx skills add eigent-ai/agent-skills
```

## Usage

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

Examples:

- "Create a design guide for this new settings page."
- "Create a new blog post for this feature launch."
- "Create or update a usecase JSON and prepare an optional PR."

## Skill Structure

Each skill contains:

- `SKILL.md` - Instructions for the agent
- `scripts/` - Helper scripts for automation (optional)
- `references/` - Supporting documentation (optional)
- `assets/` - Templates or static resources used by the skill (optional)

## License

Apache License 2.0. See `LICENSE` for the full text.
