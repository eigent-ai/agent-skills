# Design Psychology Review Lens

A review-oriented reference based on principles from *The Design of Everyday Things*. Use this when performing a **Design Review** to explain *why* something is a problem and *how* to fix it — grounded in Eigent's token system and patterns.

Each section contains: the principle, what to look for during review, and the specific tokens/patterns that address it.

---

## Table of Contents

1. [Affordances & Perceived Affordances](#1-affordances--perceived-affordances)
2. [Signifiers](#2-signifiers)
3. [Mapping](#3-mapping)
4. [Constraints](#4-constraints)
5. [Conceptual Model](#5-conceptual-model)
6. [Feedback](#6-feedback)
7. [Gulfs of Execution & Evaluation](#7-gulfs-of-execution--evaluation)
8. [Slips vs Mistakes](#8-slips-vs-mistakes)
9. [Knowledge in the World vs in the Head](#9-knowledge-in-the-world-vs-in-the-head)
10. [Modes & Mode Errors](#10-modes--mode-errors)

---

## 1. Affordances & Perceived Affordances

**Principle**: An affordance is what an object allows a person to do. In UI, what matters is the *perceived* affordance — what people think they can do. If something is clickable, it must look clickable. If something is draggable, it must look draggable.

### Review Checks

| # | Check | What to look for |
|---|-------|-----------------|
| A1 | Every clickable element looks clickable | Buttons use `--button-*` tokens with hover states. Links use `--text-link` / `--text-link-hover`. Cursor changes to pointer on interactive elements. |
| A2 | Non-interactive elements don't look interactive | Static text doesn't use `--text-action` or link colors. Non-clickable cards don't have hover elevation changes. |
| A3 | Important actions are discoverable without hover | Primary actions are visible by default — not hidden behind hover, tooltips, or overflow menus. Icon-only buttons that perform critical actions should have visible labels or always-visible tooltips. |
| A4 | Draggable elements signal draggability | Resize handles use `--border-information` on hover. `.drag` / `.no-drag` classes are correctly applied. Drag affordance doesn't rely solely on cursor change. |

### Eigent Patterns

- Buttons: `--button-primary-fill-default` with `--button-primary-fill-hover` on hover
- Ghost actions: `variant="ghost"` must still show hover state via `--surface-hover-subtle`
- Resize handle: `.custom-resizable-handle` uses `--border-information` on hover
- Interactive icons: `--icon-action` default → `--icon-action-hover` on hover

### Severity Mapping

- Missing perceived affordance on a primary action → **P1**
- Non-interactive element that looks interactive (false affordance) → **P2**
- Hover-only discoverability for secondary actions → **P3**

---

## 2. Signifiers

**Principle**: Signifiers are the cues that tell users what actions are possible and where to perform them. A button shape, a link underline, an icon, a cursor change — these are all signifiers. Use the smallest signifier that removes ambiguity.

### Review Checks

| # | Check | What to look for |
|---|-------|-----------------|
| S1 | Icon-only buttons have tooltip labels | All icon buttons wrapped in `TooltipSimple` for label disclosure. |
| S2 | Expandable sections have chevron indicators | Collapsible areas use `ChevronDown`/`ChevronUp` with `transition-transform duration-300` rotation. |
| S3 | Destructive actions are visually distinct | Delete/end/remove actions use `--text-cuation` color and danger styling, not just a different label. |
| S4 | State is communicated through multiple channels | Don't rely on color alone. Combine color + icon + text (e.g., task status uses colored icon + status text + badge). |
| S5 | External links are distinguishable from internal navigation | External links should have `hover:opacity-60` transition or an external link icon. |
| S6 | Required fields are marked | Required form fields show `required` prop on Input component. |

### Eigent Patterns

- Tooltip: `<TooltipSimple>` wrapping on every `size="icon"` button
- Chevron: `ChevronDown`/`ChevronUp` from lucide-react
- Danger signifier: `text-text-cuation` + confirmation dialog for destructive actions
- Status signifiers: `--icon-information` (running), `--icon-success` (completed), `--icon-cuation` (failed), `--icon-warning` (blocked)
- Link styling: `--text-link` with `--text-link-hover`, `underline` for emphasis

### Severity Mapping

- Icon button without any label mechanism → **P1**
- Destructive action without visual danger signal → **P1**
- Color-only state signifier (no icon/text backup) → **P2**
- Missing chevron on expandable section → **P3**

---

## 3. Mapping

**Principle**: Mapping is the relationship between controls and their effects. Natural mapping means the layout mirrors the user's mental model — controls are near what they control, and spatial grouping shows what belongs together.

### Review Checks

| # | Check | What to look for |
|---|-------|-----------------|
| M1 | Controls are positioned near what they affect | Per-item actions (edit, delete) are on the same row as the item. Form save buttons are near the form, not at a distant page footer. |
| M2 | Spatial grouping reflects logical grouping | Related settings are in the same card (`rounded-2xl bg-surface-secondary px-6 py-4`). Unrelated settings are in separate cards with spacing between them. |
| M3 | Layout follows reading order for action flow | Primary action is on the right (confirm), secondary on the left (cancel) — matching the dialog footer pattern: `ghost` cancel + `primary` confirm. |
| M4 | Navigation structure matches content hierarchy | Sidebar navigation items map to content sections. Active tab highlights match visible content. |

### Eigent Patterns

- Settings cards: `rounded-2xl bg-surface-secondary px-6 py-4` groups related controls
- Dialog footer: Cancel (`variant="ghost"`) on left, Confirm (`variant="primary"`) on right
- Workspace tabs: `WorkSpaceMenu` tabs map 1:1 to workspace panels
- Per-item actions: TaskCard actions are on the task row, AddWorker edit is on the worker row

### Severity Mapping

- Controls that affect wrong element or are ambiguously placed → **P1**
- Poor spatial grouping causing confusion → **P2**
- Reversed or non-standard button ordering → **P2**

---

## 4. Constraints

**Principle**: Constraints limit possible actions to prevent errors and reduce cognitive load. Prefer constraints and defaults over warnings. If you must block an action, explain the requirement and provide a path to satisfy it.

### Review Checks

| # | Check | What to look for |
|---|-------|-----------------|
| C1 | Invalid actions are prevented, not just warned about | Buttons are disabled (`--button-*-fill-disabled`) when preconditions aren't met, not enabled with a post-click error. |
| C2 | Disabled states explain why | Disabled buttons have tooltips explaining the unmet requirement, or the unmet condition is visible nearby. |
| C3 | Form validation prevents submission of invalid data | Required fields use `required` prop. Validation happens on blur or submit with `state="error"` + `--input-border-cuation`. |
| C4 | Destructive actions have confirmation barriers | End project, delete, logout — all require confirmation dialog before executing. |
| C5 | Modal constraints are applied correctly | Dialogs that shouldn't be dismissed during processing: `outsideClick`, `escapeKey`, `pointerDown` all prevented during validating state. |

### Eigent Patterns

- Disabled button: `--button-primary-fill-disabled` + `--button-primary-text-disabled`, cursor removed
- Disabled input: `--input-border-*` tokens with visual dimming
- Validation error: `state="error"` on `<Input>` → renders with `--input-border-cuation`
- Confirmation dialog: `CloseNoticeDialog`, `EndNotice` patterns
- Processing lock: AddWorker `isValidating` state prevents dismissal

### Severity Mapping

- Destructive action without confirmation → **P0**
- Submittable form with no validation → **P1**
- Disabled state with no explanation → **P2**
- Missing `required` prop on mandatory field → **P2**

---

## 5. Conceptual Model

**Principle**: Users form an internal model of how the system works. The UI should make the correct model obvious through consistent naming, predictable behavior, and clear cause-and-effect relationships.

### Review Checks

| # | Check | What to look for |
|---|-------|-----------------|
| CM1 | Terminology is consistent | The same thing is called the same name everywhere. "Worker" not sometimes "Agent" and sometimes "Worker". "Project" not sometimes "Task" and sometimes "Project". |
| CM2 | Actions use consistent verbs | "Create" vs "Add" vs "New" — pick one and use it throughout. "End" vs "Close" vs "Stop" — be consistent. |
| CM3 | Visual language is consistent | Same token patterns for same concepts across pages. Success always green (`--surface-success`, `--icon-success`). Errors always use `cuation` tokens. Info always blue. |
| CM4 | State transitions are visible | When user does X, the result Y is immediately visible. Running → completed shows visual change. Form submit → success shows confirmation. |
| CM5 | System status is always communicated | Users should never wonder "did that work?" or "what's happening now?" Every action produces visible feedback. |

### Eigent Patterns

- Status color system: success=green, error=`cuation`(red), warning=yellow, info=blue — consistent across badges, icons, borders, fills
- Domain color system: developer/browser/document/socialmedia/multimodal — each with coordinated text/icon/border/fill tokens
- Task lifecycle: clear visual progression through PENDING → RUNNING → COMPLETED/FAILED with distinct badge tokens

### Severity Mapping

- Inconsistent terminology for core concepts → **P1**
- Same visual treatment for different meanings (e.g., blue for both links and info status) → **P2**
- Action with no visible result → **P1**

---

## 6. Feedback

**Principle**: Feedback tells people what happened after an action. Always provide immediate feedback for interactions (press/hover/loading). If an operation takes time, show progress or a clear waiting state. After success/failure, clearly state the outcome and the next step.

### Review Checks

| # | Check | What to look for |
|---|-------|-----------------|
| F1 | Every interactive element has hover feedback | Buttons show `--button-*-fill-hover`. Cards show `--surface-card-hover`. Links show `--text-link-hover`. |
| F2 | Click/press has immediate visual response | Active states: `--button-*-fill-active`. No "dead clicks" where nothing visual happens. |
| F3 | Async operations show loading state | Spinner (`animate-spin` on `LoaderCircle`), skeleton (`--fill-skeloten-default`), or progress bar (`--progress-*` tokens). |
| F4 | Loading states maintain layout | No layout shift when loading → loaded. Skeletons match content dimensions. |
| F5 | Success is confirmed | `toast.success()` for background operations. Visual state change for inline operations (e.g., status badge update). |
| F6 | Errors are communicated clearly | `toast.error()` for operation failures. `state="error"` + `--input-border-cuation` for form validation. Error messages explain what went wrong and what to do next. |
| F7 | No bare "Loading..." text | All loading states should use skeleton UI with `--fill-skeloten-default`, not raw text divs. |

### Eigent Patterns

- Hover feedback: every button variant has a `*-hover` token counterpart
- Loading spinner: `animate-spin` on `LoaderCircle` icon from lucide-react
- Skeleton: `--fill-skeloten-default` token for placeholder shapes
- Toast: `toast.success()` / `toast.error()` from sonner
- Progress: `<Progress>` component with `--progress-*` tokens
- Button loading: show loading text (e.g., `t('setting.saving')`) + disabled state

### Severity Mapping

- Async operation with no loading indicator → **P1**
- Error silently swallowed (no user-facing message) → **P0**
- Bare "Loading..." text instead of skeleton → **P2**
- Missing hover state on interactive element → **P2**

---

## 7. Gulfs of Execution & Evaluation

**Principle**: The execution gulf exists when users can't figure out how to do what they want. The evaluation gulf exists when users can't tell what happened or what state the system is in.

### Review Checks

| # | Check | What to look for |
|---|-------|-----------------|
| G1 | Primary actions have clear CTAs | Main actions use `variant="primary"` buttons with descriptive labels — not just icons. |
| G2 | Empty states guide the user to act | Empty lists show a CTA: "Add your first worker", "Install an MCP server". Not just blank space. |
| G3 | System state is always visible | Current task status visible in TopBar. Active workspace indicated. Running/paused/finished states are distinct. |
| G4 | Results of actions are immediately apparent | After creating a worker → it appears in the list. After ending a project → navigation changes. No ambiguous "did it work?" moments. |
| G5 | Users don't repeat actions from uncertainty | If users are likely to re-click a button because they're unsure it worked, the feedback loop is broken. Add loading → success transitions. |

### Diagnostic Framework

When reviewing, ask:

- **"Would a user hesitate here?"** → Execution gulf. Fix with: clearer signifiers, visible CTAs, simpler choices, better labels.
- **"Would a user wonder what happened?"** → Evaluation gulf. Fix with: loading states, status indicators, success/error feedback, clearer state transitions.

### Eigent Patterns

- Empty states: each list (tasks, workers, MCP, history) should have a visual CTA, not blank space
- Status visibility: TopBar shows task state (running/paused/finished), BottomBox reflects input state
- State-driven UI: BottomBox has 5 distinct states (input/splitting/confirm/running/finished) with different background tokens

### Severity Mapping

- No way to discover a critical action (hidden behind unlabeled icon) → **P1**
- No visible system status after a state change → **P1**
- Empty state as blank space with no guidance → **P2**

---

## 8. Slips vs Mistakes

**Principle**: A slip is when the goal is correct but the action goes wrong (fat-finger, wrong click). A mistake is when the mental model is wrong (user thinks the system works differently). Different problems need different solutions.

### Review Checks — Slips

| # | Check | What to look for |
|---|-------|-----------------|
| SL1 | Destructive actions have undo or confirmation | End project → `EndNotice` dialog. Delete → confirmation prompt. No one-click destruction. |
| SL2 | Click targets are large enough | Minimum touch target size. Buttons aren't crammed together. Icon buttons use `size="icon"` which provides consistent sizing. |
| SL3 | Adjacent actions with different consequences are spaced apart | "Save" and "Delete" aren't side by side without spacing/visual distinction. Destructive actions use `--text-cuation` to visually separate them. |
| SL4 | Drag regions don't overlap interactive elements | `.drag` class on titlebar, `.no-drag` on all buttons within it. No accidental window drags when trying to click buttons. |

### Review Checks — Mistakes

| # | Check | What to look for |
|---|-------|-----------------|
| MS1 | Labels match what the action actually does | "End Project" actually ends the project (not just pauses it). "Save" actually saves (not "save and restart"). |
| MS2 | Conceptual model is reinforced by layout | If tasks belong to projects, the hierarchy is visible. If workers are project-scoped, that's clear from where you create/manage them. |
| MS3 | Confusing terms are explained | If a concept is non-obvious (e.g., "MCP", "splitting"), there's a brief explanation, tooltip, or learn-more link. |

### Eigent Patterns

- Destructive confirmation: `CloseNoticeDialog` (close with running task), `EndNotice` (end project)
- Visual separation: destructive actions use `--text-cuation` red text, non-destructive use standard button variants
- Drag safety: `.drag` / `.no-drag` class system in TopBar

### Severity Mapping

- One-click destructive action with no undo/confirmation → **P0**
- Misleading label that causes wrong mental model → **P1**
- Tiny click targets causing frequent misclicks → **P2**

---

## 9. Knowledge in the World vs in the Head

**Principle**: Good design puts knowledge in the world — visible options, clear labels, previews, examples — rather than forcing users to remember things. Don't make users recall constraints; surface them at the point of decision.

### Review Checks

| # | Check | What to look for |
|---|-------|-----------------|
| K1 | Form fields show their constraints | Input validation rules are visible before submission (e.g., "Name is required" appears as placeholder or helper text, not only after submit). |
| K2 | Options are visible, not memorized | Select dropdowns show all choices. Don't require the user to type a value they'd need to look up. Model platform uses Select (visible options), model type uses Input (free-text is appropriate). |
| K3 | Current state is visible without interaction | Active theme has visible selection indicator (`border-bg-fill-info-primary`), not just a checked state you'd need to hover to discover. |
| K4 | Sensitive fields have visibility toggle | Password/token fields auto-mask with password type, with Eye/EyeOff toggle so users can verify what they entered. |
| K5 | Examples or previews are provided where helpful | If the user needs to enter a URL, proxy address, or configuration value, show the expected format as placeholder text. |

### Eigent Patterns

- Password toggle: `Eye`/`EyeOff` icons with `--button-transparent-icon-disabled` styling
- Sensitive field detection: fields with names matching `token`, `key`, `secret`, `password`, `id` auto-mask
- Theme picker: active theme card has `border-bg-fill-info-primary` border + `underline` text
- Proxy input: shows `note` helper text for restart requirement after save

### Severity Mapping

- Users must remember a value that could be shown → **P2**
- No format hint for structured input fields → **P3**
- Constraint only visible after error → **P2**

---

## 10. Modes & Mode Errors

**Principle**: Modes mean the same action produces different results depending on state. They cause errors when users don't realize which mode they're in. Avoid modes; if unavoidable, make mode state extremely visible and easy to exit.

### Review Checks

| # | Check | What to look for |
|---|-------|-----------------|
| MO1 | Mode state is highly visible | BottomBox has 5 states (input/splitting/confirm/running/finished) — each with a distinct background color token so the current mode is immediately obvious. |
| MO2 | Mode transitions are clear | When state changes (e.g., input → splitting → confirm), the visual shift is unambiguous. Different `bg-input-bg-*` tokens per state. |
| MO3 | Exiting a mode is obvious | If user is in a modal or mode, the escape route is visible: close button, cancel button, escape key. |
| MO4 | Same gesture doesn't do unexpected things across modes | Pressing Enter in `input` mode submits. Pressing Enter in `confirm` mode confirms. The mapping should be consistent or clearly labeled. |

### Eigent Patterns

- BottomBox modes: `input` → `bg-input-bg-default`, `splitting` → `bg-input-bg-spliting`, `confirm` → `bg-input-bg-confirm` — distinct visual per mode
- Task states: RUNNING shows spinner badge, COMPLETED shows green badge, FAILED shows red badge — mode is always visible
- Dialog modes: edit mode shows "Edit" header, create mode shows "New Worker" header — clear mode labeling

### Severity Mapping

- Mode state invisible or ambiguous → **P1**
- Same action produces different results without clear mode indicator → **P1**
- Difficult-to-exit mode (no visible escape) → **P2**

---

## Using This Reference During Reviews

When writing a **Design Review** finding, use this reference to strengthen your analysis:

1. **Identify the symptom** — What's wrong? (e.g., "users might not notice this is clickable")
2. **Name the principle** — Which design psychology principle is violated? (e.g., "Weak signifier — Signifiers §S1")
3. **Point to the code** — What specific element has the issue?
4. **Prescribe the fix** — Which Eigent token or pattern resolves it?
5. **Assign severity** — Use the severity mapping from the relevant section.

### Example Finding

| # | Category | Severity | Principle | Description | Recommended Fix |
|---|----------|----------|-----------|-------------|-----------------|
| 1 | Affordance | P1 | Signifiers §S1 | Settings gear icon button has no tooltip — users must guess its function | Wrap in `<TooltipSimple content="Settings">` |
| 2 | Feedback | P2 | Feedback §F7 | MCP list shows bare `Loading...` div while fetching | Replace with skeleton using `--fill-skeloten-default`, maintain list height |
| 3 | Constraint | P0 | Constraints §C4 | "Delete worker" executes immediately with no confirmation | Add confirmation dialog matching `EndNotice` pattern |
| 4 | Mapping | P2 | Mapping §M3 | Cancel and Confirm buttons are reversed (Confirm on left) | Swap to match standard: Cancel (`ghost`) left, Confirm (`primary`) right |
