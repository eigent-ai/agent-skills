# Eigent Mintlify Docs Structure

## Source of Truth

- Navigation and page ordering: `docs/docs.json`
- Content files: `docs/**/*.md`
- Static images: `docs/images/*`

## Current Navigation Map

Tab: `Documentation`

1. Group: `Get Started`
   - `/get_started/welcome`
   - `/get_started/installation`
   - `/get_started/quick_start`
1. Group: `Core`
   - `/core/concepts`
   - `/core/workforce`
   - Subgroup: `Models`
     - `/core/models/byok`
     - `/core/models/local-model`
     - `/core/models/gemini`
     - `/core/models/minimax`
     - `/core/models/kimi`
   - `/core/tools`
   - `/core/workers`
1. Group: `Troubleshooting`
   - `/troubleshooting/support`
   - `/troubleshooting/bug`

## Directory Layout

```text
docs/
  docs.json
  get_started/
  core/
    models/
  troubleshooting/
  images/
```

## Placement Rules

1. Keep docs pages in the section folder matching the route in `docs/docs.json`.
1. Store route `/core/example` as file `docs/core/example.md`.
1. Keep nested routes like `/core/models/provider` at `docs/core/models/provider.md`.
1. Use absolute page refs with leading slash inside `docs/docs.json`.
