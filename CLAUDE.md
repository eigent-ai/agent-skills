# AGENTS.md

This file provides guidance to AI coding agents (Codex, Claude Code, Cursor, Copilot, etc.) when working with this repository.

## Repository Overview

This repository contains reusable AI agent skills for Eigent workflows.  
Each skill is defined in a `SKILL.md` file and may include helper scripts, references, and assets.  
Packaged ZIP artifacts for one-click download are stored in `packages/`.

## Current Skill Layout

```text
skills/
  eigent-design/
    SKILL.md
    references/
  eigent-blog-update/
    SKILL.md
    scripts/
    references/
  eigent-usecase-update/
    SKILL.md
    scripts/
    references/
    assets/
packages/
  eigent-design.zip
  eigent-blog-update.zip
  eigent-usecase-update.zip
```

## Creating or Updating a Skill

### Directory Structure

```text
skills/
  {skill-name}/
    SKILL.md              # Required: skill definition
    scripts/              # Optional: helper automation scripts
    references/           # Optional: supporting docs
    assets/               # Optional: templates/static resources
packages/
  {skill-name}.zip        # Distribution artifact for one-click download
```

### Naming Conventions

- Skill directory: `kebab-case` (for example: `eigent-blog-update`)
- Skill file: always `SKILL.md` (uppercase)
- Scripts: use clear task-oriented names (existing scripts use `snake_case.py`)
- Package file: `packages/{skill-name}.zip`

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
zip -rq packages/{skill-name}.zip skills/{skill-name} -x "*.DS_Store"
```

For this repo, keep these package artifacts updated:

- `packages/eigent-design.zip`
- `packages/eigent-blog-update.zip`
- `packages/eigent-usecase-update.zip`

## README Sync Requirements

When skill behavior changes, update `README.md` accordingly:

- `Available Skills` descriptions (capabilities and outcomes)
- `Available Packages (ZIP)` links
- `Installation`, `Usage`, `Skill Structure`, and `License` sections when relevant

## Installation (End Users)

Primary install method:

```bash
npx skills add eigent-ai/agent-skills
```

## License

This repository is licensed under Apache License 2.0.  
See `LICENSE` for full terms.
