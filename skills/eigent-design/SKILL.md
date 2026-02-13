---
name: eigent-design
description: UI/UX design companion for the Eigent product. Use this skill whenever the user wants to design a new UI component, page, or feature — it generates a design guide BEFORE implementation. Also use when the user wants to review an existing or newly built UI — it produces a structured review checklist. Trigger on phrases like "design guide", "design review", "UI review", "review this component", "plan the UI for", "design spec", "how should this look", "check the design", or any request to plan or evaluate a user interface. Even if the user just says "I'm building a new page" or "let me add a settings panel", proactively offer to generate a design guide first.
license: Apache-2.0
metadata:
  author: eigent-ai
  version: "1.0"
---

# UI/UX Design Skill

A two-mode skill for Eigent's product team: **Design Guide** (pre-implementation planning) and **Design Review** (post-implementation quality check). Both modes are grounded in Eigent's actual design token system and codebase conventions.

## When to Use

- **Design Guide mode** → The user is about to build something new (a page, component, dialog, feature). Generate a design guide *before* they write code so implementation is consistent from the start.
- **Design Review mode** → The user has built something (or is reviewing existing UI). Generate a checklist to audit quality across tokens, states, affordances, and consistency.

## Before You Start — Read the References

Both modes rely on Eigent's token system, review standards, and design psychology principles. Load the right reference file(s) before generating output:

```
references/DESIGN_TOKENS_GUIDE.md   — Full token system (colors, typography, spacing, components)
references/UI_REVIEW_CHECKLIST.md   — Review checklist structure and cross-cutting concerns
references/DESIGN_PSYCHOLOGY.md     — Design psychology principles mapped to review checks and Eigent patterns
```

Always read `DESIGN_TOKENS_GUIDE.md` first — it's the source of truth for what tokens exist and how to use them. Read `DESIGN_PSYCHOLOGY.md` when doing reviews — it provides the *why* behind each finding and maps principles like affordances, signifiers, feedback, and constraints to concrete Eigent tokens and severity levels.

---

## Mode 1: Design Guide

### Purpose

Produce a concrete, implementation-ready design specification for a new UI element. The guide tells the developer exactly which tokens, states, and patterns to use — eliminating guesswork and preventing "fix it in review" cycles.

### Trigger

The user describes something they want to build: a new page, component, dialog, panel, or feature. They may share wireframes, screenshots, or just a text description.

### Process

1. **Read** `references/DESIGN_TOKENS_GUIDE.md` to load the full token vocabulary.
2. **Clarify scope** — Ask briefly what the component/page is, where it lives in the app, and what states it needs to handle (or infer from context).
3. **Generate the design guide** using the template below.

### Design Guide Template

Generate a markdown document with these sections:

```markdown
# Design Guide: [Component/Page Name]

## Overview
Brief description of what this is, where it appears in the app, and its primary purpose.

## Layout & Structure
- Container dimensions, positioning, and responsive behavior
- How it relates to parent containers (e.g., sits inside ResizablePanel, fills a dialog)
- Grid/flex layout approach with specific spacing tokens

## Token Mapping

### Surfaces & Backgrounds
| Element | Token | Notes |
|---------|-------|-------|
| Container background | `--surface-secondary` | Matches sidebar pattern |
| Card background | `--surface-card` | With `--surface-card-hover` on hover |

### Text & Typography
| Element | Token(s) | Notes |
|---------|----------|-------|
| Title | `--text-heading` + `--fontSize-lg` + `--fontWeight-bold` | |
| Body | `--text-body` + `--fontSize-base` | |
| Label | `--text-label` + `--fontSize-sm` | |

### Borders
| Element | Token | Notes |
|---------|-------|-------|
| Card border | `--border-secondary` | |
| Focus ring | `--border-focus` | |

### Icons
| Element | Token | Notes |
|---------|-------|-------|
| Default icon | `--icon-secondary` | Switches to `--icon-primary` in buttons |

## Interaction States
For each interactive element, specify all four states:

| Element | Default | Hover | Active/Focus | Disabled |
|---------|---------|-------|--------------|----------|
| Primary button | `--button-primary-fill-default` | `--button-primary-fill-hover` | `--button-primary-fill-active` | `--button-primary-fill-disabled` |

## Universal States
Every view needs these. Specify what each looks like:

| State | Treatment |
|-------|-----------|
| **Empty** | What the user sees when there's no data (illustration, CTA, message) |
| **Loading** | Skeleton using `--fill-skeloten-default`, maintain layout dimensions |
| **Error** | Toast via `toast.error()` and/or inline with `--input-border-cuation` |
| **Success** | Toast via `toast.success()` or `--surface-success-subtle` feedback |

## Affordance & Signifiers
- What signals interactivity? (cursor changes, hover states, chevrons for expandable areas)
- What signals state? (color coding, icons, badges)
- Tooltip requirements (`TooltipSimple` wrapping for icon buttons)

## Theme Compatibility
- Light / Dark / Transparent considerations
- Image handling (`.theme-image-invert-dark` if needed)
- Verify no hardcoded colors — everything through semantic tokens

## Animations & Transitions
- Entry animations (`animate-in fade-in-0 slide-in-from-right-2` for panels)
- State transitions (`transition-all duration-300 ease-in-out`)
- Respect `prefers-reduced-motion`

## Accessibility
- Focus order and keyboard navigation
- Focus trap requirements (for dialogs)
- ARIA labels for icon-only buttons
- Minimum touch targets

## Domain Colors (if applicable)
If this component relates to a domain (developer, browser, document, socialmedia, multimodal), use the coordinated color set:
| Aspect | Token |
|--------|-------|
| Text | `--text-{domain}` |
| Icon | `--icon-{domain}` |
| Border | `--border-{domain}` |
| Fill | `--fill-{domain}` |
```

### Guidelines for Writing Design Guides

- **Be specific** — Map every visible element to a concrete token. Don't say "use a blue color", say `--text-information` or `--border-information`.
- **Cover all states** — Every interactive element needs default/hover/active/disabled. Every view needs empty/loading/error/success.
- **Follow the hierarchy** — Primitives → Semantic → Component tokens. Components should use component tokens (e.g., `--button-primary-*` for buttons), not raw semantic tokens.
- **Match existing patterns** — Reference how similar components in the app already work. Settings cards use `rounded-2xl bg-surface-secondary px-6 py-4`. Dialogs use specific footer patterns. Match these.
- **Note the "cuation" spelling** — The token system uses `cuation` not "caution". Always match: `--text-cuation`, `--border-cuation`, `--surface-cuation`.
- **Omit sections that don't apply** — If there are no domain colors needed, skip that section. Keep the guide focused.

---

## Mode 2: Design Review

### Purpose

Audit an existing or newly built UI against Eigent's design standards. Produce a structured checklist with pass/fail results and specific findings.

### Trigger

The user has code, screenshots, or a component they want reviewed. They might say "review this", "check the design", "audit the UI", or share code files.

### Process

1. **Read** all three reference files:
   - `references/DESIGN_TOKENS_GUIDE.md` — to know correct token usage
   - `references/UI_REVIEW_CHECKLIST.md` — for the review structure and cross-cutting concerns
   - `references/DESIGN_PSYCHOLOGY.md` — for design principle violations and severity mapping
2. **Understand what's being reviewed** — A specific component? A full page? Ask if unclear.
3. **Inspect the code** — Look at the actual TSX/CSS for token usage, state handling, and patterns.
4. **Generate the review checklist** using the template below.
5. **For each finding**, reference the design psychology principle that's violated (e.g., "Signifiers §S1", "Feedback §F7") — this gives the developer the *why*, not just the *what*.

### Review Checklist Template

Generate a markdown document with these sections:

```markdown
# UI Review: [Component/Page Name]

## Summary
Brief overview: what was reviewed, overall impression, number of findings by severity.

## Token Usage Compliance
| # | Check | Pass | Notes |
|---|-------|------|-------|
| 1 | No hardcoded hex colors in component files | ✅/❌ | |
| 2 | No raw primitive tokens used directly | ✅/❌ | |
| 3 | Semantic tokens used for all color values | ✅/❌ | |
| 4 | Component-specific tokens used where available | ✅/❌ | |
| 5 | Spacing tokens or Tailwind equivalents used | ✅/❌ | |
| 6 | Border radius tokens used consistently | ✅/❌ | |
| 7 | Typography tokens used for font size/weight/line-height | ✅/❌ | |
| 8 | Shadow tokens used (not inline box-shadow) | ✅/❌ | |
| 9 | No `!important` overrides bypassing tokens | ✅/❌ | |

## Theme Compatibility
| # | Check | Pass | Notes |
|---|-------|------|-------|
| 10 | Renders correctly in light theme | ✅/❌ | |
| 11 | Renders correctly in dark theme | ✅/❌ | |
| 12 | Renders correctly in transparent theme | ✅/❌ | |
| 13 | No contrast issues in any theme | ✅/❌ | |
| 14 | Images use `.theme-image-invert-dark` where needed | ✅/❌ | |

## Universal States
| # | Check | Pass | Notes |
|---|-------|------|-------|
| 15 | Empty state has proper visual treatment | ✅/❌ | |
| 16 | Loading state uses skeleton UI (`--fill-skeloten-default`) | ✅/❌ | |
| 17 | Loading maintains layout dimensions (no shift) | ✅/❌ | |
| 18 | Error states use correct tokens and patterns | ✅/❌ | |
| 19 | Success feedback is shown where applicable | ✅/❌ | |

## Interaction States
| # | Check | Pass | Notes |
|---|-------|------|-------|
| 20 | All buttons have default/hover/active/disabled styles | ✅/❌ | |
| 21 | Inputs have default/hover/focus/error/disabled styles | ✅/❌ | |
| 22 | Disabled elements remove pointer cursor | ✅/❌ | |
| 23 | Focus rings use `--border-focus` | ✅/❌ | |

## Affordance & Signifiers
| # | Check | Pass | Notes |
|---|-------|------|-------|
| 24 | Interactive elements have clear hover state | ✅/❌ | |
| 25 | Expandable areas have chevron indicators | ✅/❌ | |
| 26 | Icon buttons have TooltipSimple wrapping | ✅/❌ | |
| 27 | Destructive actions use danger color (`--text-cuation`) | ✅/❌ | |
| 28 | External links are distinguishable | ✅/❌ | |

## Animations & Transitions
| # | Check | Pass | Notes |
|---|-------|------|-------|
| 29 | Entry animations follow app patterns | ✅/❌ | |
| 30 | Transitions are smooth (no jank or flash) | ✅/❌ | |
| 31 | `prefers-reduced-motion` respected | ✅/❌ | |

## Accessibility
| # | Check | Pass | Notes |
|---|-------|------|-------|
| 32 | Keyboard navigation works logically | ✅/❌ | |
| 33 | Dialog focus traps work correctly | ✅/❌ | |
| 34 | Escape key closes dialogs | ✅/❌ | |
| 35 | ARIA labels on icon-only buttons | ✅/❌ | |

## Consistency with App Patterns
| # | Check | Pass | Notes |
|---|-------|------|-------|
| 36 | Card styling matches Settings pattern (`rounded-2xl bg-surface-secondary px-6 py-4`) | ✅/❌ | |
| 37 | Dialog footer matches AddWorker pattern | ✅/❌ | |
| 38 | Button variants used correctly (primary/ghost/outline) | ✅/❌ | |
| 39 | Toast usage follows sonner patterns | ✅/❌ | |

## Findings

| # | Category | Severity | Principle | Description | Recommended Fix |
|---|----------|----------|-----------|-------------|-----------------|
| 1 | Token | P1 | — | Hardcoded `#222` in header | Use `--text-heading` |
| 2 | Affordance | P1 | Signifiers §S1 | Icon button has no tooltip | Wrap in `<TooltipSimple>` |
| 3 | Feedback | P2 | Feedback §F7 | Bare "Loading..." div | Use skeleton with `--fill-skeleton-default` |

**Severity guide:**
- **P0** — Broken functionality, unusable in a theme, accessibility blocker
- **P1** — Incorrect token usage causing visual inconsistency across themes
- **P2** — Missing state handling (loading/error/empty), weak affordance
- **P3** — Minor polish: spacing inconsistency, animation timing, cosmetic

**Principle references** — see `references/DESIGN_PSYCHOLOGY.md` for full details:
- Affordances §A1–A4, Signifiers §S1–S6, Mapping §M1–M4, Constraints §C1–C5
- Conceptual Model §CM1–CM5, Feedback §F1–F7, Gulfs §G1–G5
- Slips §SL1–SL4, Mistakes §MS1–MS3, Knowledge §K1–K5, Modes §MO1–MO4
```

### Guidelines for Design Reviews

- **Be evidence-based** — Point to specific lines of code or elements. Don't just say "tokens are wrong", say which token is wrong and what it should be.
- **Name the principle** — For every finding, reference the design psychology principle it violates (e.g., "Signifiers §S1"). This helps developers understand *why* it matters, not just *what* to fix. See `references/DESIGN_PSYCHOLOGY.md`.
- **Prioritize findings** — P0 and P1 should be fixed before shipping. P2 should be addressed soon. P3 is nice-to-have. Use the severity mappings from the psychology reference for consistent grading.
- **Adapt the checklist** — Add component-specific checks based on what you're reviewing. The template is a starting point, not a rigid form. If reviewing a dialog, add dialog-specific checks. If reviewing a data table, add table-specific checks.
- **Check cross-cutting concerns** — Always audit against Section 8 of the full checklist (loading states, error states, disabled states, empty states, focus/keyboard, animations, responsive/edge cases).
- **Be constructive** — Every finding should include a concrete recommended fix with the exact token or pattern to use.

---

## Output Format

Both modes produce a **markdown file** saved to `/mnt/user-data/outputs/`. Name the file descriptively:

- Design Guide: `design-guide-[component-name].md`
- Design Review: `design-review-[component-name].md`

Present the file to the user after generation.

---

## Quick Reference: Common Patterns

These patterns appear repeatedly across the Eigent codebase. Use them as defaults:

| Pattern | Implementation |
|---------|---------------|
| Card container | `rounded-2xl bg-surface-secondary px-6 py-4` |
| Section heading | `text-body-base font-bold text-text-heading` |
| Page title | `text-heading-sm font-bold text-text-heading` |
| Ghost button | `variant="ghost" size="icon"` with `TooltipSimple` |
| Danger action | `text-text-cuation` text color, confirmation dialog |
| Info accent | `bg-button-fill-information text-button-fill-information-foreground` |
| Entry animation | `animate-in fade-in-0 slide-in-from-right-2` |
| Expand/collapse | `transition-all duration-300 ease-in-out` with chevron rotation |
| Skeleton loading | Use `--fill-skeloten-default` token, maintain layout dimensions |
| Error toast | `toast.error()` from sonner |
| Success toast | `toast.success()` from sonner |
| Form validation | `state="error"` prop on Input + `--input-border-cuation` |
| Scrollbar | `.scrollbar` class for auto-hiding slim scrollbar |
| Drag region | `.drag` on titlebar areas, `.no-drag` on interactive children |
