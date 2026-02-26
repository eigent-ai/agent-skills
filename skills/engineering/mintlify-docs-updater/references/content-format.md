# Markdown Content Format

## Frontmatter

Use this minimal frontmatter unless the page needs extras:

```yaml
---
title: "Page Title"
description: "Short summary for page metadata."
icon: "optional-icon-name"
---
```

Required keys:

1. `title`
1. `description`

Optional keys:

1. `icon`

## Body Conventions

1. Keep top-level heading structure clear (`##`, `###`) for Mintlify table of contents.
1. Keep existing JSX/Mintlify blocks when relevant (`CardGroup`, `Card`, HTML `<img ... />` blocks).
1. Prefer image paths under `/docs/images/<file>`.
1. Avoid breaking existing route links when renaming pages.

## Navigation Update Rule

Whenever adding a new page file, also add its route string to `docs/docs.json` in the intended group or subgroup.
