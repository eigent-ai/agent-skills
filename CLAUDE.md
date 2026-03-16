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
    eigent-design/
      SKILL.md
      references/
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
  coding-agents-and-ides/
    mintlify-docs-updater/
      SKILL.md
      scripts/
      references/
    skill-creator/
      SKILL.md
      scripts/
      references/
  marketing-and-sales/
    eigent-blog-update/
      SKILL.md
      scripts/
      references/
    eigent-usecase-update/
      SKILL.md
      scripts/
      references/
      assets/
    weekly-growth-tweet/
      SKILL.md
  git-and-github/
    eigent-server-sync/
      SKILL.md
      scripts/
      references/
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
    slack-gif-creator/
      SKILL.md
      core/
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
  web-and-frontend-development/eigent-design.zip
  web-and-frontend-development/frontend-design.zip
  web-and-frontend-development/brand-guidelines.zip
  web-and-frontend-development/web-artifacts-builder.zip
  web-and-frontend-development/theme-factory.zip
  coding-agents-and-ides/mintlify-docs-updater.zip
  coding-agents-and-ides/skill-creator.zip
  marketing-and-sales/eigent-blog-update.zip
  marketing-and-sales/eigent-usecase-update.zip
  marketing-and-sales/weekly-growth-tweet.zip
  git-and-github/eigent-server-sync.zip
  browser-and-automation/webapp-testing.zip
  image-and-video-generation/algorithmic-art.zip
  image-and-video-generation/canvas-design.zip
  image-and-video-generation/slack-gif-creator.zip
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

- Skill directory: `kebab-case` (for example: `eigent-blog-update`)
- Skill file: always `SKILL.md` (uppercase)
- Scripts: use clear task-oriented names (existing scripts use `snake_case.py`)
- Category directory: `kebab-case` (for example: `marketing-and-sales`)
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

- `packages/web-and-frontend-development/eigent-design.zip`
- `packages/web-and-frontend-development/frontend-design.zip`
- `packages/web-and-frontend-development/brand-guidelines.zip`
- `packages/web-and-frontend-development/web-artifacts-builder.zip`
- `packages/web-and-frontend-development/theme-factory.zip`
- `packages/coding-agents-and-ides/mintlify-docs-updater.zip`
- `packages/coding-agents-and-ides/skill-creator.zip`
- `packages/marketing-and-sales/eigent-blog-update.zip`
- `packages/marketing-and-sales/eigent-usecase-update.zip`
- `packages/marketing-and-sales/weekly-growth-tweet.zip`
- `packages/git-and-github/eigent-server-sync.zip`
- `packages/browser-and-automation/webapp-testing.zip`
- `packages/image-and-video-generation/algorithmic-art.zip`
- `packages/image-and-video-generation/canvas-design.zip`
- `packages/image-and-video-generation/slack-gif-creator.zip`
- `packages/pdf-and-documents/pdf.zip`
- `packages/pdf-and-documents/docx.zip`
- `packages/pdf-and-documents/xlsx.zip`
- `packages/pdf-and-documents/pptx.zip`
- `packages/pdf-and-documents/doc-coauthoring.zip`
- `packages/communication/internal-comms.zip`

## README Sync Requirements

When skill behavior changes, update `README.md` accordingly:

- `Available Skills` descriptions (capabilities and outcomes)
- `Available Packages (ZIP)` links
- `Installation`, `Usage`, `Skill Structure`, and `License` sections when relevant

## CLI (`bin/cli.js`)

The repo includes a zero-dependency Node.js CLI at `bin/cli.js` (npm bin: `eigent-skills`).

Key commands:
- `npx @eigent-ai/agent-skills install` — install all skills to detected agents
- `npx @eigent-ai/agent-skills update` — fetch latest from GitHub and update
- `npx @eigent-ai/agent-skills uninstall` — remove installed skills
- `npx @eigent-ai/agent-skills list` — list available skills
- `npx @eigent-ai/agent-skills doctor` — check agent detection

The CLI auto-detects Claude Code, Cursor, Windsurf, Codex, and Copilot.
It stores `.eigent-skills.lock.json` in each agent's skill directory for update tracking.

Also compatible with the Skills ecosystem:

```bash
npx skills add eigent-ai/agent-skills
```

## License

This repository is licensed under Apache License 2.0.  
See `LICENSE` for full terms.
