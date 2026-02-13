# Eigent Design Token Guidelines

This document describes the design token system defined in `token.css` and `index.css`. All tokens are CSS custom properties (variables) and support three themes: **light**, **dark**, and **transparent**.

---

## Table of Contents

1. [Theme Setup](#theme-setup)
2. [Color Primitives](#color-primitives)
3. [Semantic Tokens](#semantic-tokens)
   - [Text](#text)
   - [Surface](#surface)
   - [Border](#border)
   - [Icon](#icon)
   - [Fill](#fill)
   - [Background](#background)
4. [Typography](#typography)
5. [Spacing](#spacing)
6. [Border Radius](#border-radius)
7. [Shadows](#shadows)
8. [Component Tokens](#component-tokens)
9. [Category Tags (Domain Colors)](#category-tags-domain-colors)
10. [Utility Classes](#utility-classes)
11. [Rules & Best Practices](#rules--best-practices)

---

## Theme Setup

Themes are activated via the `data-theme` attribute on a parent element:

```html
<div data-theme="light">...</div>
<div data-theme="dark">...</div>
<div data-theme="transparent">...</div>
```

- **`light`** — Standard light theme (opaque off-white backgrounds).
- **`dark`** — Dark theme (deep blue-gray backgrounds with lighter foregrounds).
- **`transparent`** — Glassmorphism variant (semi-transparent off-white backgrounds with backdrop blur).

> Always use semantic tokens (e.g. `--text-body`) instead of primitives (e.g. `--colors-primary-default`). Semantic tokens automatically adapt across themes.

---

## Color Primitives

Primitives are the raw color palette. **Do not use these directly in components** — they exist to feed into semantic tokens.

| Scale | Token Pattern | Range |
|-------|--------------|-------|
| Red | `--colors-red-{50..950}`, `--colors-red-default` | `#fef2f2` → `#460809`, default `#e7000b` |
| Yellow | `--colors-yellow-{50..950}`, `--colors-yellow-default` | `#fefce8` → `#432004`, default `#d08700` |
| Green | `--colors-green-{50..950}`, `--colors-green-default` | `#f0fdf4` → `#032e15`, default `#00a63e` |
| Blue | `--colors-blue-{50..950}`, `--colors-blue-default` | `#eff6ff` → `#162456`, default `#155dfc` |
| Indigo | `--colors-indigo-{50..950}`, `--colors-indigo-default` | `#eef2ff` → `#1e1a4d`, default `#4f39f6` |
| Amber | `--colors-amber-{50..950}`, `--colors-amber-default` | `#fffbeb` → `#461901`, default `#e17100` |
| Emerald | `--colors-emerald-{50..950}`, `--colors-emerald-default` | `#ecfdf5` → `#002c22`, default `#009966` |
| Purple | `--colors-purple-{50..900}`, `--colors-purple-default` | `#faf5ff` → `#581c87`, default `#9333ea` |
| Orange | `--colors-orange-{50..950}`, `--colors-orange-default` | `#fff7ed` → `#441306`, default `#f54900` |
| Sky | `--colors-sky-{50..950}`, `--colors-sky-default` | `#f0f9ff` → `#052f4a`, default `#0084d1` |
| Fuchsia | `--colors-fuchsia-{50..950}`, `--colors-fuchsia-default` | `#fdf4ff` → `#4b004f`, default `#c800de` |
| Primary (Gray) | `--colors-primary-{1..11}`, `--colors-primary-default` | `#f5f5f5` → `#000000`, default `#222222` |

**Opacity scales** (hex alpha):

| Scale | Stops |
|-------|-------|
| `--colors-black-{0,10,30,50,80,100}` | Transparent → `#000000` |
| `--colors-white-{0,10,30,50,80,100}` | Transparent → `#ffffff` |
| `--colors-off-white-{0,10,30,50,80,100}` | Transparent → `#f5f5f5` |
| `--colors-off-black-{0,10,30,50,80,100}` | Transparent → `#1d1c1b` |

---

## Semantic Tokens

### Text

Use these for all text `color` values.

| Token | Purpose | When to Use |
|-------|---------|-------------|
| `--text-heading` | Page/section headings | `<h1>` – `<h6>` |
| `--text-body` | Default body text | Paragraphs, general content |
| `--text-label` | Secondary/label text | Form labels, captions, metadata |
| `--text-primary` | Alias for `--text-body` | Interchangeable with `--text-body` |
| `--text-secondary` | Alias for `--text-label` | Interchangeable with `--text-label` |
| `--text-tertiary` | Alias for `--text-disabled` | Placeholders, hints |
| `--text-disabled` | Disabled/inactive text | Disabled buttons, inactive items |
| `--text-action` | Interactive text (default) | Links, clickable text |
| `--text-action-hover` | Interactive text (hover) | Hover state on links/buttons |
| `--text-on-action` | Text on filled buttons | Primary button label |
| `--text-on-hover` | Text on filled buttons (hover) | Primary button hover label |
| `--text-on-disabled` | Text on disabled filled buttons | Disabled primary button label |
| `--text-inverse-primary` | Inverted text | Text on contrasting backgrounds |
| `--text-information` | Informational text | Info messages, blue-coded status |
| `--text-success` | Success text | Success messages, confirmations |
| `--text-warning` | Warning text | Warnings, caution notices |
| `--text-cuation` | Error/danger text | Errors, destructive action labels |
| `--text-error` | Error text (alias) | Form validation errors |
| `--text-muted` | Muted text | De-emphasized content |
| `--text-muted-strong` | Slightly stronger muted text | Subtle but readable secondary content |
| `--text-link` | Hyperlink color | Inline links |
| `--text-link-hover` | Hyperlink hover color | Link hover state |

**Domain-specific text colors:**

| Token | Domain |
|-------|--------|
| `--text-document` | Document/file type |
| `--text-socialmedia` | Social media type |
| `--text-browser` | Browser/web type |
| `--text-developer` | Developer/code type |
| `--text-multimodal` | Multimodal/AI type |

### Surface

Use these for `background-color` on cards, panels, modals, and containers.

| Token | Purpose |
|-------|---------|
| `--surface-primary` | Main content surface |
| `--surface-secondary` | Secondary/nested surface |
| `--surface-tertiary` | Elevated cards, popovers |
| `--surface-tertiary-hover` | Tertiary surface hover state |
| `--surface-card` | Card background |
| `--surface-card-hover` | Card hover state |
| `--surface-card-focus` | Card focused/selected state |
| `--surface-action` | Action-related surfaces |
| `--surface-action-hover` | Action hover state |
| `--surface-disabled` | Disabled element backgrounds |
| `--surface-success` | Success state background |
| `--surface-information` | Info state background |
| `--surface-warning` | Warning state background |
| `--surface-cuation` | Error state background |
| `--surface-error-subtle` | Subtle error background |
| `--surface-success-subtle` | Subtle success background |
| `--surface-hover-subtle` | Subtle hover overlay |
| `--surface-tertiary-subtle` | Very subtle tertiary background |

### Border

Use these for `border-color` and `outline-color`.

| Token | Purpose |
|-------|---------|
| `--border-primary` | Default visible border |
| `--border-secondary` | Lighter border (input default, dividers) |
| `--border-tertiary` | Very subtle border |
| `--border-disabled` | Disabled element border |
| `--border-focus` | Focus ring |
| `--border-action` | Action-related border |
| `--border-action-hover` | Action border on hover |
| `--border-information` | Info state border |
| `--border-success` | Success state border |
| `--border-warning` | Warning state border |
| `--border-cuation` | Error state border |
| `--border-transparent` | Invisible border (layout placeholder) |
| `--border-subtle` | Very light structural border |
| `--border-subtle-strong` | Slightly stronger structural border |

### Icon

Use these for icon `color` (or `stroke`/`fill` in SVGs).

| Token | Purpose |
|-------|---------|
| `--icon-primary` | Default icon color |
| `--icon-secondary` | Muted/de-emphasized icons |
| `--icon-action` | Interactive icon (default) |
| `--icon-action-hover` | Interactive icon (hover) |
| `--icon-disabled` | Disabled icon |
| `--icon-on-action` | Icon on filled button |
| `--icon-on-hover` | Icon on filled button (hover) |
| `--icon-on-disabled` | Icon on disabled filled button |
| `--icon-information` | Info icon |
| `--icon-success` | Success icon |
| `--icon-warning` | Warning icon |
| `--icon-cuation` | Error icon |

### Fill

Use these for interactive element backgrounds (buttons, toggles, progress bars).

| Token | Purpose |
|-------|---------|
| `--fill-default` | Base fill (usually white or dark surface) |
| `--fill-fill-primary` | Primary fill (dark/light depending on theme) |
| `--fill-fill-primary-hover` | Primary fill hover |
| `--fill-fill-primary-active` | Primary fill active/pressed |
| `--fill-fill-primary-disabled` | Primary fill disabled |
| `--fill-fill-secondary` | Secondary fill |
| `--fill-fill-secondary-hover/active/disabled` | Secondary fill states |
| `--fill-fill-tertiary` | Tertiary fill (subtle backgrounds) |
| `--fill-fill-tertiary-hover/active/disabled` | Tertiary fill states |
| `--fill-fill-transparent` | Transparent fill |
| `--fill-fill-transparent-hover/active/disabled` | Transparent fill states |
| `--fill-fill-success` | Success fill |
| `--fill-fill-warning` | Warning fill |
| `--fill-fill-cuation` | Error fill |
| `--fill-fill-information` | Info fill |
| `--fill-skeloten-default` | Skeleton loading placeholder |

### Background

Use these for page-level and layout backgrounds.

| Token | Purpose |
|-------|---------|
| `--bg-page` | Root page background |
| `--bg-page-default` | Default page background (opaque) |
| `--bg-primary` | Primary layout area |
| `--bg-secondary` | Secondary layout area |
| `--bg-tertiary` | Tertiary layout area |
| `--bg-dark` | Dark overlay |
| `--bg-dark-primary` | Dark primary overlay |
| `--bg-dark-secondary` | Dark secondary overlay |
| `--bg-dark-tertiary` | Dark tertiary overlay |
| `--bg-dark-default` | Full-dark background |

---

## Typography

### Font Family

The system uses **Inter** as the sole font family, set globally:

```css
font-family: 'Inter';
```

### Font Sizes

| Token | Value | Use Case |
|-------|-------|----------|
| `--fontSize-xs` | `10px` | Fine print, badges, mini labels |
| `--fontSize-sm` | `13px` | Small text, captions, metadata |
| `--fontSize-base` | `15px` | Default body text |
| `--fontSize-md` | `16px` | Slightly larger body text |
| `--fontSize-lg` | `18px` | Subheadings, emphasized text |
| `--fontSize-xl` | `20px` | Section headings |
| `--fontSize-2xl` | `24px` | Major headings |
| `--fontSize-3xl` | `28px` | Page titles |
| `--fontSize-4xl` | `36px` | Hero text |
| `--fontSize-5xl` | `44px` | Display text |

### Font Weights

| Token | Value | Use Case |
|-------|-------|----------|
| `--fontWeight-regular` | `400` | Body text |
| `--fontWeight-medium` | `500` | Emphasized labels, buttons |
| `--fontWeight-semibold` | `600` | Subheadings, strong emphasis |
| `--fontWeight-bold` | `700` | Headings, primary actions |

### Line Heights

Use named tokens for readability:

| Token | Value | Pairing |
|-------|-------|---------|
| `--lineHeight-tight` | `16px` | `--fontSize-xs`, `--fontSize-sm` |
| `--lineHeight-normal` | `20px` | `--fontSize-base`, `--fontSize-md` |
| `--lineHeight-relaxed` | `22px` | `--fontSize-lg` |
| `--lineHeight-loose` | `24px` | `--fontSize-xl` |
| `--lineHeight-xl` | `28px` | `--fontSize-2xl` |
| `--lineHeight-2xl` | `30px` | `--fontSize-3xl` |
| `--lineHeight-3xl` | `32px` | — |
| `--lineHeight-4xl` | `36px` | `--fontSize-4xl` |
| `--lineHeight-5xl` | `46px` | `--fontSize-5xl` |
| `--lineHeight-6xl` | `58px` | Display text |

---

## Spacing

| Token | Value | Use Case |
|-------|-------|----------|
| `--spacing-xs` | `4px` | Tight gaps, icon margins |
| `--spacing-sm` | `8px` | Small padding, compact layouts |
| `--spacing-md` | `16px` | Default padding, standard gaps |
| `--spacing-lg` | `32px` | Section padding, large gaps |
| `--spacing-xl` | `64px` | Major section breaks |

---

## Border Radius

| Token | Value | Use Case |
|-------|-------|----------|
| `--borderRadius-sm` | `4px` | Small elements (badges, tags, chips) |
| `--borderRadius-lg` | `8px` | Cards, inputs, buttons |
| `--borderRadius-xl` | `16px` | Modals, large cards, panels |

---

## Shadows

| Token | Use Case |
|-------|----------|
| `--shadow-perfect` | Elevated cards, dropdowns, modals — multi-layered realistic shadow |
| `--shadow-button` | Buttons with inset highlight and subtle drop shadow |

Usage:

```css
.card {
  box-shadow: var(--shadow-perfect);
}

.button {
  box-shadow: var(--shadow-button);
}
```

The `.perfect-shadow` utility class is also available for direct use in HTML.

---

## Component Tokens

Each major component has its own scoped token set. These reference semantic tokens internally, so they auto-adapt across themes. **Use component tokens when building these specific components.**

### Button

Four button variants, each with `fill`, `text`, and `icon` tokens across `default`, `hover`, `active`, and `disabled` states:

| Variant | Token Prefix | Example |
|---------|-------------|---------|
| Primary | `--button-primary-*` | `--button-primary-fill-default`, `--button-primary-text-hover` |
| Secondary | `--button-secondary-*` | `--button-secondary-fill-active` |
| Transparent | `--button-transparent-*` | `--button-transparent-icon-disabled` |
| Tertiary | `--button-tertiery-*` | `--button-tertiery-fill-hover` |

State colors for semantic buttons:

| Token | Purpose |
|-------|---------|
| `--button-fill-success` | Success button fill |
| `--button-fill-cuation` | Danger button fill |
| `--button-fill-warning` | Warning button fill |
| `--button-fill-information` | Info button fill |
| `--button-fill-*-foreground` | Text on semantic buttons |

### Input

| Token | Purpose |
|-------|---------|
| `--input-bg-default` | Default input background |
| `--input-bg-hover` | Input hover background |
| `--input-bg-input` | Active input background |
| `--input-border-default` | Default border |
| `--input-border-hover` | Hover border |
| `--input-border-focus` | Focus border (blue) |
| `--input-border-success` | Validation success |
| `--input-border-warning` | Validation warning |
| `--input-border-cuation` | Validation error |
| `--input-text-default` | Input text color |
| `--input-label-default` | Label text color |

### Badge

| Token | Purpose |
|-------|---------|
| `--badge-running-surface` / `--badge-running-surface-foreground` | Running status |
| `--badge-paused-surface` / `--badge-paused-surface-foreground` | Paused status |
| `--badge-error-surface` / `--badge-error-surface-foreground` | Error status |
| `--badge-complete-surface` / `--badge-complete-surface-foreground` | Complete status |
| `--badge-splitting-surface` / `--badge-splitting-surface-foreground` | Splitting status |

### Other Components

| Component | Prefix | Key Tokens |
|-----------|--------|------------|
| Switch | `--switch-{on,off,disabled}-*` | Track fill/border, thumb fill/border |
| Menu Tabs | `--menutabs-*` | Fill, border, text, icon per state |
| Menu Button | `--menubutton-*` | Fill and border per state |
| Dropdown | `--dropdown-*` | Background, border, item states |
| Search | `--search-*` | Background, border default/hover |
| Progress | `--progress-*` | Fill (default, complete, past, new) |
| Tag | `--tag-*` | Surface, foreground per semantic state |
| Task | `--task-*` | Surface, border, fill per state |
| Project | `--project-*` | Surface, border per state |
| Message | `--message-*` | Fill, border per state |
| Worker | `--worker-*` | Surface, border per state |
| Popup | `--popup-*` | Surface, background, border |
| Pill | `--pill-*` | Background, surface, border |
| Mask | `--mask-*` | Overlay backgrounds |
| Code | `--code-*` | Code block background, foreground |
| Log | `--log-default` | Log panel background |

---

## Category Tags (Domain Colors)

Five domain categories have coordinated text, icon, border, and fill tokens:

| Domain | Text | Icon | Border | Fill |
|--------|------|------|--------|------|
| Developer | `--text-developer` | `--icon-developer` | `--border-developer` | `--fill-developer` |
| Browser | `--text-browser` | `--icon-browser` | `--border-browser` | `--fill-browser` |
| Document | `--text-document` | `--icon-document` | `--border-document` | `--fill-document` |
| Social Media | `--text-socialmedia` | `--icon-socialmedia` | `--border-socialmedia` | `--fill-socialmedia` |
| Multimodal | `--text-multimodal` | `--icon-multimodal` | `--border-multimodal` | `--fill-multimodal` |

Shorthand aliases are also available: `--developer`, `--browser`, `--document`, `--multimodal`, `--socialmedia`.

---

## Utility Classes

Defined in `index.css`:

| Class | Purpose |
|-------|---------|
| `.blur` | Glassmorphism container with `backdrop-filter: blur(75px)` |
| `.blur-bg` | Lighter blur effect (`40px`) |
| `.blur-effect` | Heavy blur (`150px`) with inset shadow |
| `.perfect-shadow` | Multi-layered realistic elevation shadow |
| `.no-drag` / `.drag` | Electron window drag regions |
| `.scrollbar` | Auto-hiding slim scrollbar (6px, shows on scroll) |
| `.scrollbar-always-visible` | Persistent slim scrollbar |
| `.scrollbar-hide` | Completely hidden scrollbar |
| `.scrollbar-horizontal` | Horizontal scrollbar styling |
| `.hover-style-scrollbar` | Scrollbar that only appears on hover |
| `.terminal-scrollbar` | Terminal-style scrollbar (8px, subtle glow) |
| `.theme-image-invert-dark` | Inverts images in dark/transparent themes |

---

## Rules & Best Practices

### 1. Always use semantic tokens, never primitives

```css
/* DO */
color: var(--text-body);
background-color: var(--surface-primary);

/* DON'T */
color: var(--colors-primary-default);
background-color: var(--colors-off-white-80);
```

### 2. Use component tokens for their specific component

```css
/* DO — for a primary button */
background-color: var(--button-primary-fill-default);
color: var(--button-primary-text-default);

/* DON'T — for a button */
background-color: var(--fill-fill-primary);
color: var(--text-on-action);
```

### 3. Respect the token hierarchy

```
Primitives (--colors-*)
  → Semantic tokens (--text-*, --surface-*, --border-*, --icon-*, --fill-*, --bg-*)
    → Component tokens (--button-*, --input-*, --badge-*, etc.)
```

Each layer should only reference the layer above it.

### 4. Handle all interaction states

When building interactive elements, always provide styles for: **default**, **hover**, **active/focus**, and **disabled**.

```css
.my-button {
  background: var(--button-primary-fill-default);
}
.my-button:hover {
  background: var(--button-primary-fill-hover);
}
.my-button:active {
  background: var(--button-primary-fill-active);
}
.my-button:disabled {
  background: var(--button-primary-fill-disabled);
  color: var(--button-primary-text-disabled);
}
```

### 5. Use Lucide icons with the built-in base styles

Icons using the `.lucide` class automatically inherit `--icon-secondary` color with `stroke-width: 1.5`. Inside buttons/links they auto-switch to `--icon-primary`.

### 6. Form elements have base styles

Inputs, textareas, and selects automatically get:
- `color: var(--text-primary)`
- `background-color: var(--surface-primary)`
- `border: 1px solid var(--border-secondary)`
- Placeholder text uses `--text-tertiary`

### 7. Note on "cuation" spelling

The token system uses `cuation` (not "caution") consistently. An alias `--text-caution` exists for `--text-cuation`. When using error/danger tokens, always match the existing convention: `--*-cuation`.

### 8. Dark theme image handling

Use `.theme-image-invert-dark` on images/logos that need to be inverted (white-on-dark) in dark and transparent themes.

### 9. Page-level background

The root `#root` element uses `var(--bg-page)` with `backdrop-filter: blur(75px)` for the glassmorphism effect. Never override this unless intentionally changing the app shell.
