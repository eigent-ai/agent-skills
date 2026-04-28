# AGENTS.md

This file provides guidance to AI coding agents (Codex, Claude Code, Cursor, Copilot, etc.) when working with this repository.

## Repository Overview

This repository contains reusable AI agent skills for Eigent workflows.  
Each skill is defined in a `SKILL.md` file and may include helper scripts, references, and assets.  
Packaged ZIP artifacts for one-click download are stored in `packages/`.

## Category Structure

Skills and packages are organized into tiered categories:

### Tier 1 — High Priority
- `ai-and-llms`
- `coding-agents-and-ides`
- `web-and-frontend-development`
- `devops-and-cloud`
- `browser-and-automation`
- `search-and-research`
- `marketing-and-sales`
- `data-and-analytics`
- `image-and-video-generation`
- `git-and-github`

### Tier 2 — Strong Supporting
- `productivity-and-tasks`
- `pdf-and-documents`
- `speech-and-transcription`
- `communication`
- `security-and-passwords`

### Tier 3 — Niche but Valuable
- `cli-utilities`
- `notes-and-knowledge-management`
- `apple-and-mobile-development`
- `shopping-and-ecommerce`
- `finance`

### Bonus / Future
- `agent-to-agent-protocols`

## Current Skill Layout

```text
skills/
  web-and-frontend-development/
    frontend-design/
      SKILL.md
    brand-guidelines/
      SKILL.md
    web-artifacts-builder/
      SKILL.md
      scripts/
    theme-factory/
      SKILL.md
      themes/
    excalidraw/
      SKILL.md
      references/
  coding-agents-and-ides/
    mintlify-docs-updater/
      SKILL.md
      scripts/
      references/
    skill-creator/
      SKILL.md
      scripts/
      references/
    mcp-builder/
      SKILL.md
      scripts/
      references/
      LICENSE.txt
  browser-and-automation/
    webapp-testing/
      SKILL.md
      scripts/
      examples/
  image-and-video-generation/
    algorithmic-art/
      SKILL.md
      templates/
    canvas-design/
      SKILL.md
      canvas-fonts/
    instagram-reel-editor/
      SKILL.md
      scripts/
      references/
    slack-gif-creator/
      SKILL.md
      core/
  marketing-and-sales/
    instagram-posting/
      SKILL.md
      scripts/
  pdf-and-documents/
    pdf/
      SKILL.md
      scripts/
    docx/
      SKILL.md
      scripts/
    xlsx/
      SKILL.md
      scripts/
    pptx/
      SKILL.md
      scripts/
    doc-coauthoring/
      SKILL.md
  communication/
    internal-comms/
      SKILL.md
      examples/
packages/
  web-and-frontend-development/frontend-design.zip
  web-and-frontend-development/brand-guidelines.zip
  web-and-frontend-development/web-artifacts-builder.zip
  web-and-frontend-development/theme-factory.zip
  web-and-frontend-development/excalidraw.zip
  coding-agents-and-ides/mintlify-docs-updater.zip
  coding-agents-and-ides/skill-creator.zip
  coding-agents-and-ides/mcp-builder.zip
  browser-and-automation/webapp-testing.zip
  image-and-video-generation/algorithmic-art.zip
  image-and-video-generation/canvas-design.zip
  image-and-video-generation/instagram-reel-editor.zip
  image-and-video-generation/slack-gif-creator.zip
  marketing-and-sales/instagram-posting.zip
  pdf-and-documents/pdf.zip
  pdf-and-documents/docx.zip
  pdf-and-documents/xlsx.zip
  pdf-and-documents/pptx.zip
  pdf-and-documents/doc-coauthoring.zip
  communication/internal-comms.zip
```

## Creating or Updating a Skill

### Directory Structure

```text
skills/
  {category}/
    {skill-name}/
      SKILL.md              # Required: skill definition
      scripts/              # Optional: helper automation scripts
      references/           # Optional: supporting docs
      assets/               # Optional: templates/static resources
packages/
  {category}/{skill-name}.zip  # Distribution artifact for one-click download
```

### Naming Conventions

- Skill directory: `kebab-case` (for example: `mintlify-docs-updater`)
- Skill file: always `SKILL.md` (uppercase)
- Scripts: use clear task-oriented names (existing scripts use `snake_case.py`)
- Category directory: `kebab-case` (for example: `coding-agents-and-ides`)
- Package file: `packages/{category}/{skill-name}.zip`

### SKILL.md Format

Use YAML frontmatter with only:

```yaml
---
name: {skill-name}
description: {when to use this skill, including trigger phrases}
---
```

Then define concise workflow instructions in markdown.

## Best Practices for Context Efficiency

- Keep `SKILL.md` concise; put detailed docs in `references/`.
- Make descriptions explicit so agents can trigger the correct skill reliably.
- Prefer scripts for repeated deterministic operations.
- Load only the references needed for the current task.

## Script Guidelines

- Prefer deterministic scripts with explicit arguments (`argparse` for Python scripts).
- Fail fast on invalid input and return clear error messages.
- Keep script output actionable for agents and humans.

## Packaging Skills (ZIP)

After creating or updating a skill, regenerate its ZIP package:

```bash
zip -rq packages/{category}/{skill-name}.zip skills/{category}/{skill-name} -x "*.DS_Store"
```

For this repo, keep these package artifacts updated:

- `packages/web-and-frontend-development/frontend-design.zip`
- `packages/web-and-frontend-development/brand-guidelines.zip`
- `packages/web-and-frontend-development/web-artifacts-builder.zip`
- `packages/web-and-frontend-development/theme-factory.zip`
- `packages/web-and-frontend-development/excalidraw.zip`
- `packages/coding-agents-and-ides/mintlify-docs-updater.zip`
- `packages/coding-agents-and-ides/skill-creator.zip`
- `packages/coding-agents-and-ides/mcp-builder.zip`
- `packages/browser-and-automation/webapp-testing.zip`
- `packages/image-and-video-generation/algorithmic-art.zip`
- `packages/image-and-video-generation/canvas-design.zip`
- `packages/image-and-video-generation/instagram-reel-editor.zip`
- `packages/image-and-video-generation/slack-gif-creator.zip`
- `packages/marketing-and-sales/instagram-posting.zip`
- `packages/pdf-and-documents/pdf.zip`
- `packages/pdf-and-documents/docx.zip`
- `packages/pdf-and-documents/xlsx.zip`
- `packages/pdf-and-documents/pptx.zip`
- `packages/pdf-and-documents/doc-coauthoring.zip`
- `packages/communication/internal-comms.zip`

## README Sync Requirements

When skill behavior changes, update `README.md` accordingly:

- `Available Skills` descriptions (capabilities and outcomes)
- `Installation`, `Usage`, `Skill Structure`, and `License` sections when relevant

## CLI (`bin/cli.js`)

The repo includes a zero-dependency Node.js CLI at `bin/cli.js` (npm bin: `eigent-skills`).

Key commands:
- `npx @eigent-ai/agent-skills install` — install all skills to detected agents
- `npx @eigent-ai/agent-skills update` — fetch latest from GitHub and update
- `npx @eigent-ai/agent-skills uninstall` — remove installed skills
- `npx @eigent-ai/agent-skills list` — list available skills
- `npx @eigent-ai/agent-skills eval` — run structural checks and show quality scores
- `npx @eigent-ai/agent-skills doctor` — check agent detection

The CLI auto-detects Claude Code, Cursor, Windsurf, Codex, and Copilot.
It stores `.eigent-skills.lock.json` in each agent's skill directory for update tracking.

Also compatible with the Skills ecosystem:

```bash
npx skills add eigent-ai/agent-skills
```

## Skill Evaluation System

Skills are scored across four pillars: Quality, Impact, Compatibility, and Community.
All evaluation data is stored separately from skill source code so that skill downloads
(ZIP packages) remain clean and do not include eval artifacts.

**No API keys required** — all LLM scoring is done interactively via Claude Code during PR review.

### Evaluation Workflow

When a user uploads a new skill, it opens as a PR. During review:

1. **CI runs structural checks** automatically (`.github/workflows/skill-review.yml`)
2. **Reviewer uses Claude Code** to run the full quality evaluation:

```bash
# Step 1: Run structural checks + output eval context
node evals/evaluate.js <skill-name>

# Step 2: Claude Code reads the judge prompts and scores the skill
#   - Read evals/judges/description-judge.md
#   - Read evals/judges/content-judge.md
#   - Score each dimension 0–3, compute normalizedScore

# Step 3: Save scores (pipe JSON to stdin)
echo '<judge-results-json>' | node evals/evaluate.js <skill-name> --save
```

The judge results JSON must have this shape:

```json
{
  "descriptionJudge": {
    "specificity": { "score": 0, "reasoning": "..." },
    "triggerCoverage": { "score": 0, "reasoning": "..." },
    "boundaryclarity": { "score": 0, "reasoning": "..." },
    "distinctiveness": { "score": 0, "reasoning": "..." },
    "totalScore": 0,
    "normalizedScore": 0.0,
    "summary": "..."
  },
  "contentJudge": {
    "actionability": { "score": 0, "reasoning": "..." },
    "completeness": { "score": 0, "reasoning": "..." },
    "codeQuality": { "score": 0, "reasoning": "..." },
    "conciseness": { "score": 0, "reasoning": "..." },
    "totalScore": 0,
    "normalizedScore": 0.0,
    "summary": "..."
  }
}
```

Quality score formula: `(descriptionJudge.normalizedScore * 0.3 + contentJudge.normalizedScore * 0.7) * 100`

Scores are committed as part of the PR so they are reviewed alongside the skill itself.

### Score Files (Separate from Skills)

Per-skill scores are stored **outside** the skill directories at:
```
evals/scores/{category}/{skill}/scores.json
```

This separation ensures:
- `skills/` directories stay clean for user downloads (ZIP packages exclude eval data)
- Eval data is centralized and easy to query programmatically

Scores are fetchable from the website via GitHub raw URLs:
```
https://raw.githubusercontent.com/eigent-ai/agent-skills/main/evals/scores/{category}/{skill}/scores.json
```

### Mapping: Skill → Score

The mapping between skills and their scores follows the same `{category}/{skill}` path:

| Skill Source | Score File |
|---|---|
| `skills/{category}/{skill}/SKILL.md` | `evals/scores/{category}/{skill}/scores.json` |

To fetch all scores for display on eigent.ai/skills, enumerate `evals/scores/` or use the GitHub API with a token.

### Eval File Structure

```
evals/
  judges/
    description-judge.md    # LLM prompt for description scoring
    content-judge.md        # LLM prompt for content scoring
    assessment-judge.md     # LLM prompt for impact eval rubric scoring (Phase 2)
  validators/
    structural.js           # Deterministic SKILL.md checks
  scorer.js                 # Score persistence and calculation
  evaluate.js               # Context builder for Claude Code evaluation
  scores/                   # Per-skill score files (mirrors skills/ structure)
    {category}/
      {skill}/
        scores.json
  scenarios/                # Per-skill eval scenarios (Phase 2)
    {category}/
      {skill}/
        *.yaml
  rubrics/                  # Per-skill eval rubrics (Phase 2)
    {category}/
      {skill}/
        *.yaml
  schema/
    scenario.schema.json    # YAML schema for eval scenarios (Phase 2)
    rubric.schema.json      # YAML schema for rubrics (Phase 2)
```

## License

This repository is licensed under Apache License 2.0.
See `LICENSE` for full terms.
