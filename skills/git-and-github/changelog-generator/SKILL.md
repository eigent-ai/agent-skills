---
name: changelog-generator
description: Transform git commit history into polished user-facing changelogs and release notes. Use when the user wants a CHANGELOG.md from a version tag or date range, weekly product updates, app store release notes, or Keep a Changelog formatted output with internal noise filtered out.
metadata:
  source-repo: https://github.com/ComposioHQ/awesome-claude-skills
---

# Changelog Generator

Scans commits across a date range or version tag, categorizes changes, strips internal noise, and rewrites technical language into plain prose.

## Source Repository

- **GitHub:** [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) (community collection)
- **Install upstream:** `npx skills add ComposioHQ/awesome-claude-skills`

---

## `/changelog`

Point at a commit range, version tag, or time window.

**Workflow:**
1. Gather commits via `git log` for the requested range.
2. Filter out internal noise — refactors, test-only, CI/chore commits unless user wants them.
3. Group by type: New Features, Improvements, Bug Fixes, Security.
4. Rewrite each entry in user-facing language (benefits, not implementation details).
5. Format per Keep a Changelog or the user's style guide if provided.
6. Output ready-to-commit `CHANGELOG.md` or alternate format (Notion post, app store notes).

**Grouping rules:**
| Commit signal | Category |
|---|---|
| `feat:`, new capability | New Features |
| `fix:`, regression | Bug Fixes |
| `perf:`, `refactor:` (user-visible) | Improvements |
| `security:`, CVE, auth fix | Security |
| `chore:`, `ci:`, `test:` | Filter out (default) |

---

## Example Prompts

- Generate a changelog for commits between v1.4.0 and v1.5.0. Group by features, improvements, bug fixes, security. User-facing language.
- Create release notes from commits in the past 7 days. Filter chore/ci/test. Output as a Notion-ready product update post.
- Write app store release notes for iOS v3.2 since the last tag. Max 200 words. Friendly and benefit-focused.

---

## Style Guide Support

If the user provides a style guide file, enforce:
- Terminology (feature names, product voice)
- Tone (formal vs casual)
- Formatting (bullet vs paragraph, emoji policy)

---

## Guardrails

- Run `git log` in the correct repo root — confirm with user if ambiguous.
- Do not invent features not present in commits.
- Flag breaking changes explicitly in a dedicated section.
- For app store notes, respect platform character limits.
