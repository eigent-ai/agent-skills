---
name: mintlify-docs-updater
description: Maintain this repository's Mintlify documentation from uploaded Markdown files. Use when asked to add, update, or organize docs pages in `docs/`, place new content under `get_started`, `core`, `core/models`, or `troubleshooting`, and keep `docs/docs.json` navigation in sync with new pages.
---

# Mintlify Docs Updater

## Overview

Use this skill to ingest user-provided Markdown into the Mintlify docs tree, enforce required frontmatter, and update navigation entries in `docs/docs.json`.
Prefer the included script for deterministic page placement and nav updates.

## Workflow

1. Read the current site map in `references/docs-structure.md`.
1. Decide the destination page path (for example, `core/new-feature` -> `docs/core/new-feature.md`).
1. Ingest the uploaded Markdown file with the script:

```bash
python3 scripts/ingest_markdown_doc.py \
  --source /absolute/path/to/upload.md \
  --page core/new-feature \
  --group "Core"
```

1. Use `--subgroup "Models"` when adding pages under `core/models`.
1. Use `--dry-run` first when the target placement is uncertain.
1. Validate changes:
   - Confirm the new file exists under `docs/`.
   - Confirm `docs/docs.json` includes the new `"/path/to/page"` entry in the right group.
   - Confirm frontmatter includes `title` and `description`.

## Commands

Add a new page and nav entry:

```bash
python3 scripts/ingest_markdown_doc.py \
  --source /absolute/path/to/upload.md \
  --page get_started/advanced-setup \
  --group "Get Started"
```

Add a new `Core > Models` page and place it after an existing page:

```bash
python3 scripts/ingest_markdown_doc.py \
  --source /absolute/path/to/model-guide.md \
  --page core/models/new-provider \
  --group "Core" \
  --subgroup "Models" \
  --insert-after /core/models/kimi
```

Preview changes without writing files:

```bash
python3 scripts/ingest_markdown_doc.py \
  --source /absolute/path/to/upload.md \
  --page troubleshooting/new-issue \
  --group "Troubleshooting" \
  --dry-run
```

## Editing Rules

1. Keep page files in `docs/<section>/<slug>.md`.
1. Keep page references in `docs/docs.json` as absolute doc routes (for example, `"/core/concepts"`).
1. Keep frontmatter keys minimal and compatible with current docs:
   - `title` (required)
   - `description` (required)
   - `icon` (optional)
1. Preserve existing Mintlify components and JSX blocks when present.
1. Use `/docs/images/<file>` for image paths in Markdown/HTML blocks.

## References

- `references/docs-structure.md`: Current Mintlify navigation map and folder structure for this repository.
- `references/content-format.md`: Frontmatter and content conventions for new docs pages.
- `scripts/ingest_markdown_doc.py`: Deterministic ingest/update script for uploaded Markdown files.
