# AGENTS.md

This file provides guidance to AI coding agents (Codex, Claude Code, Cursor, Copilot, etc.) when working with this repository.

## Repository Overview

This repository contains reusable AI agent skills for Eigent workflows.  
Each skill is defined in a `SKILL.md` file and may include helper scripts, references, and assets.  
Packaged ZIP artifacts for one-click download are stored in `packages/`.

## Current Skill Layout

```text
skills/
  coding-agents-and-ides/
    mintlify-docs-updater/
      SKILL.md
      scripts/
      references/
    skill-creator/
      SKILL.md
      scripts/
      references/
packages/
  coding-agents-and-ides/mintlify-docs-updater.zip
  coding-agents-and-ides/skill-creator.zip
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

- `packages/coding-agents-and-ides/mintlify-docs-updater.zip`
- `packages/coding-agents-and-ides/skill-creator.zip`

## README Sync Requirements

When skill behavior changes, update `README.md` accordingly:

- `Available Skills` descriptions (capabilities and outcomes)
- `Installation`, `Usage`, `Skill Structure`, and `License` sections when relevant

## Installation (End Users)

Primary install method:

```bash
npx skills add eigent-ai/agent-skills
```

## License

This repository is licensed under Apache License 2.0.  
See `LICENSE` for full terms.
