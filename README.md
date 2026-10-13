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
| [`skill-creator`](skills/coding-agents-and-ides/skill-creator/SKILL.md) | Create, modify, and evaluate skills. Covers authoring `SKILL.md` files, bundling scripts and references, running evals, and benchmarking skill performance. |
| [`mcp-builder`](skills/coding-agents-and-ides/mcp-builder/SKILL.md) | Build MCP (Model Context Protocol) servers in Python (FastMCP) or Node/TypeScript. Includes planning workflows, MCP best-practices references, evaluation scripts (`evaluation.py`, `connections.py`), and language-specific implementation guides. |
| [`spec`](skills/coding-agents-and-ides/spec/SKILL.md) | Write comprehensive product and engineering specs before implementation. Covers problem statements, user stories, acceptance criteria, edge cases, rollout notes, and open decisions. |
| [`review`](skills/coding-agents-and-ides/review/SKILL.md) | Perform five-axis code reviews across correctness, security, performance, readability, and maintainability. Leads with severity-ranked findings and concrete fixes. |
| [`ship`](skills/coding-agents-and-ides/ship/SKILL.md) | Prepare releases for production with launch checklists, staged rollout criteria, monitoring plans, rollback paths, communications, and post-launch validation. |

#### Web & Frontend Development

| Skill | Source | Description |
| --- | --- | --- |
| [`frontend-design`](skills/web-and-frontend-development/frontend-design/SKILL.md) | — | Create distinctive, production-grade frontend interfaces with high design quality. Generates creative, polished web components, pages, and applications that avoid generic AI aesthetics. |
| [`brand-guidelines`](skills/web-and-frontend-development/brand-guidelines/SKILL.md) | — | Apply Anthropic's official brand colors and typography to artifacts. Use when brand styling, visual formatting, or company design standards apply. |
| [`web-artifacts-builder`](skills/web-and-frontend-development/web-artifacts-builder/SKILL.md) | — | Build elaborate, multi-component claude.ai HTML artifacts using React, Tailwind CSS, and shadcn/ui. Includes project scaffolding and single-file bundling scripts. |
| [`theme-factory`](skills/web-and-frontend-development/theme-factory/SKILL.md) | — | Apply professional color and font themes to artifacts like slides, docs, reports, and landing pages. Includes 10 curated themes with a visual showcase PDF. |
| [`excalidraw`](skills/web-and-frontend-development/excalidraw/SKILL.md) | — | Generate architecture and system diagrams as `.excalidraw` files from codebase analysis. Covers valid Excalidraw JSON, element IDs, labels, arrows, and styling rules so diagrams open correctly in Excalidraw. |
| [`open-design`](skills/web-and-frontend-development/open-design/SKILL.md) | [nexu-io/open-design](https://github.com/nexu-io/open-design) | Generate web, mobile, and dashboard prototypes from a prompt using brand-grade design systems. Outputs sandboxed HTML previews exportable to HTML, PDF, PPTX, or MP4. |

#### DevOps & Cloud
_TBD — Category placeholder for future skills._

#### Browser & Automation

| Skill | Description |
| --- | --- |
| [`webapp-testing`](skills/browser-and-automation/webapp-testing/SKILL.md) | Test local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing screenshots, and viewing browser logs with server lifecycle helpers. |

#### Search & Research

| Skill | Description |
| --- | --- |
| [`last30days`](skills/search-and-research/last30days/SKILL.md) | Research recent public discussion across Reddit, Hacker News, GitHub, X, YouTube, Polymarket, and similar sources, then synthesize engagement-ranked findings into a grounded brief. |

#### Marketing & Sales

| Skill | Source | Description |
| --- | --- | --- |
| [`instagram-posting`](skills/marketing-and-sales/instagram-posting/SKILL.md) | — | Post images or video to an already logged-in Instagram session via browser automation. Includes a script to pick the correct crop aspect ratio before upload. |
| [`copywriting`](skills/marketing-and-sales/copywriting/SKILL.md) | — | Write marketing copy for landing pages, launches, ads, campaigns, and email sequences using product context and direct-response frameworks where useful. |
| [`seo-audit`](skills/marketing-and-sales/seo-audit/SKILL.md) | — | Audit technical, on-page, and AI-search SEO, including metadata, page structure, keyword intent, internal links, content gaps, and AEO/GEO/LLMO readiness. |
| [`marketing-ideas`](skills/marketing-and-sales/marketing-ideas/SKILL.md) | — | Generate practical SaaS and product marketing ideas across organic, paid, community, partnerships, product-led growth, retention, and launch channels. |
| [`ab-test-setup`](skills/marketing-and-sales/ab-test-setup/SKILL.md) | — | Design, analyze, and document A/B tests, including hypotheses, sample size, implementation checks, decision rules, and ICE-scored experiment backlogs. |
| [`humanizer`](skills/marketing-and-sales/humanizer/SKILL.md) | [blader/humanizer](https://github.com/blader/humanizer) | Detect and rewrite AI writing patterns to make content sound authentically human, with optional voice calibration from writing samples. |

#### Data & Analytics

| Skill | Description |
| --- | --- |
| [`ml-failure-audit`](skills/data-and-analytics/ml-failure-audit/SKILL.md) | Audit ML CI failures, experiment regressions, training run failures, golden metric failures, and telemetry-backed ML claims. Classifies failures across model, correctness, data/config, runtime, metric-policy, observability, and unsupported-claim categories with evidence-backed recommendations. |

#### Image & Video Generation

| Skill | Source | Description |
| --- | --- | --- |
| [`algorithmic-art`](skills/image-and-video-generation/algorithmic-art/SKILL.md) | — | Create algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Generates generative art from algorithmic philosophies expressed as flow fields, particle systems, and noise fields. |
| [`canvas-design`](skills/image-and-video-generation/canvas-design/SKILL.md) | — | Create beautiful visual art in .png and .pdf documents using design philosophy. Generates posters, artwork, and static visual pieces with curated typography and intentional composition. |
| [`slack-gif-creator`](skills/image-and-video-generation/slack-gif-creator/SKILL.md) | — | Create animated GIFs optimized for Slack with proper dimensions, frame rates, and file sizes. Includes PIL-based utilities for frame composition, easing, and validation. |
| [`instagram-reel-editor`](skills/image-and-video-generation/instagram-reel-editor/SKILL.md) | — | Turn raw travel-style footage folders into cinematic Instagram Reels (9:16) with grading, cuts, overlays, and music. Includes Python helpers to scan clips and build the final MP4. |
| [`remotion`](skills/image-and-video-generation/remotion/SKILL.md) | [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | Make videos programmatically with React using Remotion. Produces product demos, tutorials, social clips, Manim-style animations, and branded pipelines with voiceover and FFmpeg. |

#### Git & GitHub

| Skill | Source | Description |
| --- | --- | --- |
| [`changelog-generator`](skills/git-and-github/changelog-generator/SKILL.md) | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | Transform git commit history into polished changelogs and release notes. Groups changes by type, filters internal noise, and outputs Keep a Changelog formatted entries or app store notes. |

### Tier 2 — Strong Supporting Pages

#### Productivity & Tasks

| Skill | Source | Description |
| --- | --- | --- |
| [`pm-skills`](skills/productivity-and-tasks/pm-skills/SKILL.md) | [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | Product management workflows for PRDs, OKRs, and meeting notes. Covers discovery, strategy, execution, launch, and growth workflows for knowledge workers. |
| [`resume-tailoring`](skills/productivity-and-tasks/resume-tailoring/SKILL.md) | [varunr89/resume-tailoring-skill](https://github.com/varunr89/resume-tailoring-skill) | Tailor resumes to job descriptions with ATS keyword optimization, gap analysis, and rewritten bullets. Supports single-role and batch tailoring with zero fabrication. |

#### PDF & Documents

| Skill | Source | Description |
| --- | --- | --- |
| [`pdf`](skills/pdf-and-documents/pdf/SKILL.md) | — | Work with PDF files: extract text/tables, merge/split, rotate pages, add watermarks, fill forms, encrypt/decrypt, extract images, and OCR scanned PDFs. |
| [`docx`](skills/pdf-and-documents/docx/SKILL.md) | — | Create, read, edit, and manipulate Word documents (.docx). Covers document creation, tracked changes, comments, find-and-replace, tables of contents, and professional formatting. |
| [`xlsx`](skills/pdf-and-documents/xlsx/SKILL.md) | — | Work with spreadsheet files (.xlsx, .xlsm, .csv, .tsv): create, edit, format, compute formulas, clean messy data, and convert between tabular formats. |
| [`pptx`](skills/pdf-and-documents/pptx/SKILL.md) | — | Create, read, edit, and manipulate PowerPoint presentations (.pptx). Covers slide decks, pitch decks, templates, layouts, speaker notes, thumbnails, and content extraction. |
| [`doc-coauthoring`](skills/pdf-and-documents/doc-coauthoring/SKILL.md) | — | Guide users through structured co-authoring of documentation, proposals, technical specs, and decision docs via context gathering, iterative refinement, and reader testing. |
| [`contract-review-risk-scoring`](skills/pdf-and-documents/contract-review-risk-scoring/SKILL.md) | [evolsb/claude-legal-skill](https://github.com/evolsb/claude-legal-skill) | Review contracts with CUAD-based clause-by-clause risk scoring, market benchmarks, negotiability ratings, redline suggestions, and an overall Contract Safety Score. |
| [`legal-work-plugin`](skills/pdf-and-documents/legal-work-plugin/SKILL.md) | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | In-house legal workflows for playbook-based contract review, NDA triage (GREEN/YELLOW/RED), compliance briefings, and vendor agreement checks. |
| [`claude-for-legal`](skills/pdf-and-documents/claude-for-legal/SKILL.md) | [anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal) | Full legal plugin suite for commercial contract review, privacy/DPA analysis, DSAR responses, and AI governance vendor reviews with EU AI Act triage. |

#### Speech & Transcription
_TBD — Category placeholder for future skills._

#### Communication

| Skill | Description |
| --- | --- |
| [`internal-comms`](skills/communication/internal-comms/SKILL.md) | Write internal communications including 3P updates, company newsletters, FAQ responses, status reports, and leadership updates using company-standard formats. |

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
npx @eigent-ai/agent-skills install mintlify-docs-updater
npx @eigent-ai/agent-skills install mintlify-docs-updater webapp-testing
```

Use `npx @eigent-ai/agent-skills list` to see all available skills.

### Install for a specific agent

```bash
npx @eigent-ai/agent-skills install -a claude-code
npx @eigent-ai/agent-skills install -a cursor mintlify-docs-updater
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

- "Create a distinctive settings page interface for this product."
- "Ingest this Markdown file into Mintlify docs and update docs.json navigation."
- "Create a generative art piece with flow fields and particle systems."
- "Design a poster with bold typography and intentional composition."
- "Build a landing page with distinctive, production-grade design."
- "Create a Word document with tracked changes and comments."
- "Apply Anthropic brand colors to this component."
- "Make me a GIF of a spinning logo for Slack."
- "Write a 3P update for this week's sprint."
- "Build a complex multi-component artifact with shadcn/ui."
- "Test my local web app with Playwright and capture screenshots."
- "Apply the Ocean Depths theme to my slide deck."
- "Help me co-author a technical design doc."
- "Edit this folder of travel clips into an Instagram Reel with music."
- "Post this video to Instagram with this caption and hashtags."
- "Generate an architecture diagram as an excalidraw file for this repo."
- "Help me build an MCP server in TypeScript that wraps our internal API."
- "Audit this ML CI failure and decide whether it is a real training regression or a gate/policy issue."
- "/last30days AI writing tools market sentiment --emit=html."
- "Write a 3-email launch sequence for our new pricing plan."
- "Run an SEO audit on this landing page and give me a prioritized fix list."
- "Generate marketing ideas for a B2B SaaS tool with a $5k/month budget."
- "Help me design an A/B test for our signup CTA button."
- "/spec - Design a public webhooks API with retries and reliable delivery."
- "/review - Audit this API endpoint handler for security issues."
- "/ship - Plan a staged rollout for our new recommendation engine."
- "Humanize this blog post so it doesn't sound like AI wrote it."
- "Write a PRD for a notification preferences center."
- "Generate a changelog for commits between v1.4.0 and v1.5.0."
- "Tailor my resume for this job description."
- "Build a web prototype for a B2B invoicing tool."
- "Create a 30-second product demo video with Remotion."
- "Review this NDA as the receiving party and give me a Contract Safety Score."

## Skill Structure

Each skill contains:

- `SKILL.md` - Instructions for the agent
- `scripts/` - Helper scripts for automation (optional)
- `references/` - Supporting documentation (optional)
- `assets/` - Templates or static resources used by the skill (optional)

## License

Apache License 2.0. See `LICENSE` for the full text.
