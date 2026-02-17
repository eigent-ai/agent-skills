# Eigent UI Review Checklist

A page-by-page review checklist covering **token usage**, **usability**, **universal states**, **affordance & signifiers**, and **consistency**. Based on analysis of the actual codebase structure.

---

## Page & Folder Structure Overview

```
src/
├── components/
│   ├── Layout/index.tsx            ← App shell (TopBar + Outlet + HistorySidebar)
│   ├── TopBar/index.tsx            ← Title bar, navigation, project actions
│   ├── BottomBar/index.tsx         ← WorkSpaceMenu wrapper
│   ├── SideBar/index.tsx           ← Vertical icon menu (currently unused in layout)
│   ├── ChatBox/
│   │   ├── ProjectChatContainer    ← Multi-turn chat scroll container
│   │   ├── ProjectSection          ← Per-chat section renderer
│   │   ├── BottomBox/              ← Input area (input/splitting/confirm/running/finished)
│   │   ├── MessageItem/            ← AgentMessageCard, FeedbackCard, MarkDown
│   │   ├── TaskBox/                ← TaskCard, TaskItem, StreamingTaskList
│   │   ├── UserQueryGroup          ← Grouped user messages
│   │   └── FloatingAction          ← Scroll-to-bottom FAB
│   ├── AddWorker/index.tsx         ← Dialog for creating/editing worker agents
│   ├── TaskState/index.tsx         ← Task status filter pills (all/done/ongoing/failed/pending)
│   ├── WorkFlow/index.tsx          ← ReactFlow-based workflow visualization
│   ├── BrowserAgentWorkSpace/      ← Browser agent webview panel
│   ├── TerminalAgentWrokSpace/     ← Terminal agent workspace
│   ├── Folder/                     ← Document viewer with zoom controls
│   ├── WorkSpaceMenu/              ← Workspace switcher tabs
│   ├── Dialog/                     ← CloseNotice, EndNotice, Privacy
│   └── ui/                         ← Primitives (button, input, select, dialog, etc.)
├── pages/
│   ├── Home.tsx                    ← Main workspace (ChatBox + ResizablePanel + workspaces)
│   ├── Setting.tsx                 ← Settings shell (sidebar nav + tab content)
│   ├── Setting/
│   │   ├── General.tsx             ← Profile, language, appearance, proxy, IDE
│   │   ├── Privacy.tsx             ← Privacy settings
│   │   ├── Models.tsx              ← Model configuration
│   │   ├── MCP.tsx                 ← MCP server management
│   │   ├── MCPMarket.tsx           ← MCP marketplace
│   │   └── components/             ← MCPList, MCPAddDialog, MCPConfigDialog, etc.
│   ├── History.tsx                 ← Project history/dashboard
│   ├── Login.tsx / SignUp.tsx      ← Auth pages
│   └── Dashboard/                  ← Browser.tsx, Project.tsx
└── style/
    ├── token.css                   ← Design tokens (primitives + semantic + component)
    ├── index.css                   ← Global styles, utility classes, base layer
    └── markdown-styles.css         ← Markdown rendering styles
```

---

## 1. Global / Cross-Page Checks

### 1.1 Token Usage Compliance

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 1 | No hardcoded hex colors in component TSX/CSS (except `token.css`) | | |
| 2 | No raw `--colors-*` primitives used directly in components | | |
| 3 | Semantic tokens (`--text-*`, `--surface-*`, etc.) used for all color values | | |
| 4 | Component-specific tokens used for their intended component (e.g. `--button-primary-*` for buttons, `--input-*` for inputs) | | |
| 5 | Spacing tokens (`--spacing-xs/sm/md/lg/xl`) or Tailwind equivalents (`gap-sm`, `p-md`) used instead of arbitrary pixel values | | |
| 6 | Border radius tokens (`--borderRadius-sm/lg/xl`) or Tailwind (`rounded-lg`, `rounded-xl`) used consistently | | |
| 7 | Typography tokens used: `--fontSize-*`, `--fontWeight-*`, `--lineHeight-*` or their Tailwind mappings | | |
| 8 | Shadow tokens (`--shadow-perfect`, `--shadow-button`) used instead of inline box-shadow declarations | | |
| 9 | No `!important` overrides that bypass token values (except documented exceptions in `index.css`) | | |
| 10 | Domain colors use the 5-category system (`developer`, `browser`, `document`, `socialmedia`, `multimodal`) consistently | | |

### 1.2 Theme Compatibility

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 11 | All pages render correctly in **light** theme | | |
| 12 | All pages render correctly in **dark** theme | | |
| 13 | All pages render correctly in **transparent** theme (macOS only) | | |
| 14 | No white text on white background in any theme | | |
| 15 | No dark text on dark background in any theme | | |
| 16 | Images/logos that need inversion use `.theme-image-invert-dark` class | | |
| 17 | Gift icon uses `appearance === 'dark' ? giftWhiteIcon : giftIcon` pattern consistently | | |
| 18 | Logo uses `appearance === 'dark' ? logoWhite : logoBlack` pattern consistently | | |

### 1.3 Typography Consistency

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 19 | Page titles use `text-heading-sm` or larger with `font-bold` and `text-text-heading` | | |
| 20 | Section headings use `text-body-base font-bold text-text-heading` | | |
| 21 | Body text uses `text-text-body` or `text-text-primary` | | |
| 22 | Secondary/label text uses `text-text-label` or `text-text-secondary` | | |
| 23 | Placeholder/hint text uses `text-text-tertiary` or `text-text-disabled` | | |
| 24 | Font family is always Inter (no system font fallback leaks) | | |

---

## 2. Home Page (`pages/Home.tsx`)

### 2.1 Layout & Structure

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 25 | `px-2 pb-2 pt-10` padding accounts for TopBar height (36px) without overlap | | |
| 26 | ResizablePanel default split (30/70) is reasonable for chat vs workspace | | |
| 27 | ResizablePanel minimum size (20%) doesn't cause content clipping | | |
| 28 | `.custom-resizable-handle` uses `--border-information` on hover for clear resize affordance | | |

### 2.2 Universal States

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 29 | **Empty state**: When no active task, loading state is shown (currently bare `<div>Loading...</div>`) — needs proper skeleton or empty state UI | | |
| 30 | **Loading state**: `chatStore` null check shows generic "Loading..." — should use skeleton tokens (`--fill-skeloten-default`) | | |
| 31 | **Active workspace**: Workspace panel only renders when `activeWorkSpace` is set — empty right panel has no visual indication | | |
| 32 | Each workspace type (browser, developer, document, workflow) has entry animation (`animate-in fade-in-0 slide-in-from-right-2`) | | |

### 2.3 Affordance & Signifiers

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 33 | Resizable handle shows visual feedback on hover (color change to `--border-information`) | | |
| 34 | Resizable handle hides drag dots (`display: none !important` on child divs/svgs) — user relies solely on cursor change | | |
| 35 | Workspace panel transitions signal content switching (slide + fade animation) | | |

### 2.4 Token Usage

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 36 | Outer container uses `bg-surface-secondary` and `border-border-tertiary` | | |
| 37 | `h-[calc(100vh-104px)]` — verify this magic number still accounts for TopBar + BottomBar in all themes | | |
| 38 | `border-border-subtle-strong` used for document workspace border | | |
| 39 | `blur-bg bg-white-50` class on document workspace — verify `bg-white-50` maps to `--colors-white-50` via Tailwind config | | |

---

## 3. Chat Components

### 3.1 ProjectChatContainer

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 40 | `.scrollbar` class applied for auto-hiding scrollbar behavior | | |
| 41 | Scroll-to-bottom triggers on new user messages only (not agent messages) | | |
| 42 | `scrolling` class added/removed dynamically for scrollbar visibility | | |
| 43 | Empty project sections (no user messages) are correctly filtered out | | |

### 3.2 BottomBox (Input Area)

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 44 | **State-driven backgrounds**: `input` → `bg-input-bg-default`, `splitting` → `bg-input-bg-spliting`, `confirm` → `bg-input-bg-confirm` | | |
| 45 | All 5 states (input, splitting, confirm, running, finished) have distinct visual treatment | | |
| 46 | BoxAction only visible after initial input (not in bare `input` state) | | |
| 47 | Inputbox is always visible across all states (consistent anchor point) | | |

### 3.3 TaskCard

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 48 | Progress bar uses `--progress-*` tokens via `<Progress>` component | | |
| 49 | Task status colors map correctly: COMPLETED → `bg-task-fill-success`, FAILED → `bg-task-fill-error`, RUNNING → `bg-task-fill-running`, BLOCKED → `bg-task-fill-warning` | | |
| 50 | Hover borders match status: success → `hover:border-bg-fill-success-primary`, error → `hover:border-task-border-focus-error`, warning → `hover:border-task-border-focus-warning` | | |
| 51 | Status icons use correct icon tokens: `text-icon-information` (running), `text-icon-success` (completed), `text-icon-cuation` (failed), `text-icon-warning` (blocked), `text-icon-secondary` (empty/skipped) | | |
| 52 | Failed task text uses `text-text-cuation-default` | | |
| 53 | Expand/collapse chevron rotates smoothly (`transition-transform duration-300`) | | |
| 54 | Content height animation uses `transition-all duration-300 ease-in-out` without layout jank | | |

### 3.4 TaskState (Filter Pills)

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 55 | All filter states use consistent `bg-tag-surface` for selected state | | |
| 56 | Icon colors change on hover and selection (secondary → semantic color) | | |
| 57 | Text colors change on hover and selection (label → semantic color) | | |
| 58 | `clickable` prop correctly removes cursor pointer when false | | |
| 59 | Loader icon spins (`animate-spin`) only when task status is `running` | | |
| 60 | Pending state uses `text-primary-foreground` — verify this resolves correctly in dark theme | | |

---

## 4. Settings Page (`pages/Setting.tsx`)

### 4.1 Layout & Navigation

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 61 | Max width container (`max-w-[940px]`) centers content on wide screens | | |
| 62 | Sidebar navigation uses `VerticalNavigation` with sticky positioning (`sticky top-20`) | | |
| 63 | Active tab switches content without URL navigation (local state only) | | |
| 64 | Version button uses `bg-surface-tertiary` with `text-text-success` for tag icon | | |
| 65 | Logo button links to eigent.ai and has hover opacity transition | | |
| 66 | Bottom section has proper border separator (`border-t-[0.5px] border-border-secondary`) | | |

### 4.2 General Settings

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 67 | All setting sections use consistent card style: `rounded-2xl bg-surface-secondary px-6 py-4` | | |
| 68 | Section headings use `text-body-base font-bold text-text-heading` consistently | | |
| 69 | Profile section shows email with `text-text-information underline` styling | | |
| 70 | "Manage" button uses `variant="primary"` with `text-button-primary-icon-default` for icon | | |
| 71 | "Log Out" button uses `variant="outline"` with `text-button-tertiery-text-default` for icon | | |
| 72 | Theme picker images have `border-transparent` default and `border-bg-fill-info-primary` when active | | |
| 73 | Active theme text has `underline`, hover theme text has `group-hover:underline` | | |
| 74 | Language select uses `bg-input-bg-default` for dropdown background | | |
| 75 | Proxy input shows `note` text for restart hint after save | | |
| 76 | Proxy save button swaps between `variant="primary"` (save) and `variant="outline"` (restart) | | |
| 77 | IDE select dropdown uses same `bg-input-bg-default` pattern as language select | | |

### 4.3 Universal States

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 78 | Loading state: `chatStore` null renders "Loading..." — needs improvement | | |
| 79 | Proxy saving state: button shows `t('setting.saving')` text, disabled while saving | | |
| 80 | Proxy post-save state: shows restart hint note + restart button | | |
| 81 | **Error states**: Proxy invalid URL shows toast error — no inline validation styling | | |

### 4.4 Affordance & Signifiers

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 82 | Theme cards: cursor changes to pointer (`hover:cursor-pointer`) | | |
| 83 | Theme cards: selected border provides clear active indicator | | |
| 84 | Clickable external links (version, logo) have `hover:opacity-60` transition | | |
| 85 | Select components show chevron indicator for dropdown affordance | | |
| 86 | "Manage" button navigates to external URL — should this have an external link icon? | | |

---

## 5. AddWorker Dialog (`components/AddWorker/index.tsx`)

### 5.1 Token Usage

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 87 | Bot icon uses `text-icon-primary` correctly | | |
| 88 | Dialog content sections use `bg-white-100%` — verify this resolves to `--colors-white-100` in dark theme (may appear as white card on dark) | | |
| 89 | Footer uses `bg-white-100%` and `!rounded-b-xl` — verify dark theme compatibility | | |
| 90 | Eye/EyeOff icons use `text-button-transparent-icon-disabled` for password toggle | | |
| 91 | Name error state uses `state="error"` on Input component | | |
| 92 | MCP name text uses `text-text-action` for emphasis | | |

### 5.2 Universal States

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 93 | **Empty form**: Plus icon (`text-icon-primary`) + "New Worker" label (`text-text-body`) for trigger button | | |
| 94 | **Edit mode**: Edit icon + translated "Edit" text uses `variant="ghost"` button | | |
| 95 | **Validating state**: "Validating..." text shown on confirm button, dialog cannot be dismissed (outsideClick, escapeKey, pointerDown all prevented) | | |
| 96 | **Name validation**: Empty name shows translated error, duplicate name shows translated error | | |
| 97 | **Env config sub-screen**: Back button on dialog header, cancel/confirm footer buttons | | |
| 98 | **Loading/null chatStore**: Shows "Loading..." (needs improvement) | | |

### 5.3 Affordance & Signifiers

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 99 | Required fields show `required` prop on Input component | | |
| 100 | Sensitive fields (token, key, secret, password, id) auto-mask with password type | | |
| 101 | Password visibility toggle (Eye/EyeOff) provides clear show/hide affordance | | |
| 102 | Advanced model config uses chevron (ChevronDown/ChevronUp) to signal expandability | | |
| 103 | Cancel/Confirm footer buttons use distinct variants (`ghost` vs `primary`) | | |
| 104 | Model platform uses Select dropdown, model type uses free-text Input — appropriate for each | | |

---

## 6. TopBar (`components/TopBar/index.tsx`)

### 6.1 Token Usage

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 105 | Brand name uses `text-label-md font-bold text-text-heading` | | |
| 106 | "End Project" button uses `!text-text-cuation` for danger signifier | | |
| 107 | "Share" button uses `bg-button-fill-information !text-button-fill-information-foreground` | | |
| 108 | All icon buttons use `variant="ghost"` with `size="icon"` consistently | | |
| 109 | Linux window controls use `hover:bg-surface-hover-subtle` for hover state | | |

### 6.2 Universal States

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 110 | **No active task**: "End Project" button hidden, title shows "New Project" | | |
| 111 | **Task running/paused**: "End Project" button visible with Power icon | | |
| 112 | **Task finished**: "Share" button appears alongside "End Project" | | |
| 113 | **History page**: Left side shows back button (ChevronLeft), right side is empty | | |
| 114 | **End project flow**: Dialog confirmation before destructive action | | |
| 115 | **End project loading**: Loading state on dialog confirm button | | |

### 6.3 Affordance & Signifiers

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 116 | All action buttons have `TooltipSimple` wrapping for label disclosure | | |
| 117 | Active task title shows `ChevronDown` indicating it opens sidebar panel | | |
| 118 | Title truncates with `max-w-[300px] overflow-hidden text-ellipsis whitespace-nowrap` — tooltip shows full title | | |
| 119 | `.drag` / `.no-drag` classes correctly applied: titlebar is draggable, buttons are not | | |
| 120 | "End Project" uses red text (`text-cuation`) to signal destructive action | | |
| 121 | Platform-specific layout: macOS gets left padding for traffic lights, Linux gets custom window controls | | |

---

## 7. Layout Shell (`components/Layout/index.tsx`)

### 7.1 Universal States

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 122 | **First launch**: Onboarding animation plays (`AnimationJson`) | | |
| 123 | **Installing**: `InstallDependencies` screen shown | | |
| 124 | **Waiting backend**: Install screen remains visible | | |
| 125 | **Installation error**: `InstallationErrorDialog` overlays with retry options | | |
| 126 | **Backend error**: Same dialog handles backend-specific errors | | |
| 127 | **Normal operation**: `Outlet` + `HistorySidebar` rendered | | |
| 128 | **Close with running task**: `CloseNoticeDialog` intercepts window close | | |
| 129 | **Loading/null chatStore**: Shows "Loading..." (needs improvement) | | |

---

## 8. Cross-Cutting Concerns

### 8.1 Loading States Audit

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 130 | All `Loading...` bare divs should be replaced with skeleton UI using `--fill-skeloten-default` token | | |
| 131 | Loading states maintain page layout dimensions (prevent layout shift) | | |
| 132 | Spinner animations use `animate-spin` consistently for `LoaderCircle` icons | | |

### 8.2 Error States Audit

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 133 | Form validation errors use `--input-border-cuation` / `state="error"` | | |
| 134 | Toast errors use `toast.error()` from sonner consistently | | |
| 135 | Toast success uses `toast.success()` consistently | | |
| 136 | Destructive actions (end project, log out) have confirmation dialogs | | |
| 137 | Network errors (API failures) show user-facing error messages | | |

### 8.3 Disabled States Audit

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 138 | Disabled buttons use `--button-*-fill-disabled` + `--button-*-text-disabled` tokens | | |
| 139 | Disabled inputs use `--input-border-*` tokens with appropriate visual dimming | | |
| 140 | Disabled icons use `--icon-disabled` or `--icon-on-disabled` | | |
| 141 | Disabled interactive elements remove cursor pointer | | |

### 8.4 Empty States Audit

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 142 | Chat with no messages: Appropriate empty state or onboarding prompt shown | | |
| 143 | Task list with no tasks: Visual indication (not just blank space) | | |
| 144 | History with no projects: Empty state message or illustration | | |
| 145 | Worker list with no workers: Clear CTA to add first worker | | |
| 146 | MCP list with no servers: Clear CTA to install first MCP server | | |

### 8.5 Focus & Keyboard Navigation

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 147 | `--border-focus` token used for focus rings on interactive elements | | |
| 148 | Dialog focus trap works (AddWorker, EndNotice, CloseNotice) | | |
| 149 | Escape key closes dialogs (except when `isValidating` in AddWorker) | | |
| 150 | Tab order follows visual layout in Settings page | | |
| 151 | Input components show focus state using `--input-border-focus` | | |

### 8.6 Animation & Transitions

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 152 | Workspace panel transitions use `animate-in fade-in-0 slide-in-from-right-2` consistently | | |
| 153 | Task list items use `animate-in fade-in-0 slide-in-from-left-2` for staggered entry | | |
| 154 | Expand/collapse uses `transition-all duration-300 ease-in-out` | | |
| 155 | No animations cause layout jank or content flash | | |
| 156 | Reduced motion preferences respected (`prefers-reduced-motion`) | | |

### 8.7 Responsive & Edge Cases

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 157 | Long task titles truncate with ellipsis (TopBar: `max-w-[300px]`) | | |
| 158 | Long worker names don't break AddWorker dialog layout | | |
| 159 | Many tasks in TaskCard don't cause performance issues (virtualization if needed) | | |
| 160 | Settings page scrolls properly with many content sections | | |
| 161 | ResizablePanel handles minimum size constraint gracefully | | |

---

## 9. Findings Template

Use this template to document issues found during review:

| # | Page/Component | Category | Severity | Description | Recommended Fix |
|---|----------------|----------|----------|-------------|-----------------|
| | | Token / Usability / State / Affordance | P0-P3 | | |

**Severity guide:**
- **P0** — Broken functionality, unusable in a theme, accessibility blocker
- **P1** — Incorrect token usage causing visual inconsistency across themes
- **P2** — Missing state handling (loading/error/empty), weak affordance
- **P3** — Minor polish: spacing inconsistency, animation timing, cosmetic
