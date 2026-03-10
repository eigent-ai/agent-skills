---
name: eigent-server-sync
description: Transfer eigent server PRs to eigent_server. Use when syncing changes from eigent/server/ to eigent_server, when an eigent PR modifies server code that needs to be reflected in eigent_server, or when porting eigent server features.
license: Apache-2.0
---

# Eigent Server Sync

Transfer PR changes from `eigent/server/` to `eigent_server/server/`.

## Overview

This skill syncs server-side code between two repositories:
- **Source**: `eigent-ai/eigent` (specifically the `server/` directory)
- **Target**: `eigent-ai/eigent_server`

## Workflow

### Step 1: Parse Input

Accept either:
- Full GitHub PR URL: `https://github.com/eigent-ai/eigent/pull/123`
- PR number: `123` (assumes eigent-ai/eigent repo)

### Step 2: Validate Environment

Ensure `gh` CLI is authenticated:
```bash
gh auth status
```

### Step 3: Fetch PR Information

```bash
# Get PR metadata
gh pr view <PR_NUMBER> --repo eigent-ai/eigent --json title,body,files,baseRefName,headRefName,author,url

# Get PR diff for specific files
gh pr diff <PR_NUMBER> --repo eigent-ai/eigent
```

### Step 4: Analyze Changed Files

Filter files to only include those in `server/` directory. Use the file mapping rules below to determine target paths.

**File Mapping Rules:**

| eigent Path | eigent_server Path | Action |
|-------------|-------------------|--------|
| `server/app/controller/*.py` | `server/app/controller/*.py` | Sync |
| `server/app/model/*.py` | `server/app/model/*.py` | Sync |
| `server/app/component/*.py` | `server/app/component/*.py` | Sync |
| `server/app/service/*.py` | `server/app/service/*.py` | Sync |
| `server/app/type/*.py` | `server/app/type/*.py` | Sync |
| `server/app/command/*.py` | `server/app/command/*.py` | Sync |
| `server/app/middleware/*.py` | `server/app/middleware/*.py` | Sync |
| `server/app/exception/*.py` | `server/app/exception/*.py` | Sync |
| `server/alembic/*` | `server/alembic/*` | Sync |
| `server/main.py` | `server/main.py` | Sync |
| `server/cli.py` | `server/cli.py` | Sync |

For detailed mapping rules, see [file-mapping.md](references/file-mapping.md).

### Step 5: Check for Sync-able Changes

If no files in `server/` directory were modified:
- Inform user: "No server files found in this PR. Nothing to sync."
- Exit the workflow

### Step 6: Create Feature Branch

```bash
cd /path/to/eigent_server
git checkout -b sync/eigent-pr-<PR_NUMBER>
```

### Step 7: Implement Changes

For each changed file in `eigent/server/`:
1. Fetch the diff for that file
2. Apply the equivalent change to `eigent_server/server/`
3. Handle any conflicts or structural differences

### Step 8: Commit Changes

```bash
git add .
git commit -m "Sync from eigent PR #<PR_NUMBER>: <Brief description>"
```

### Step 9: Create Pull Request

```bash
gh pr create --repo eigent-ai/eigent_server \
  --title "Sync: <Original PR Title>" \
  --body "$(cat <<'EOF'
## Synced from eigent PR

Original PR: eigent-ai/eigent#<PR_NUMBER>

### Summary
<Brief summary of changes from original PR>

### Changes in eigent_server
- List of files modified/created
- Key changes

### Testing
- [ ] Verify changes work correctly
- [ ] Run test suite

🤖 Generated with eigent-server-sync skill
EOF
)"
```

## Script Reference

### analyze_pr.py

Analyzes a PR and generates a sync plan:

```bash
python scripts/analyze_pr.py <PR_URL_OR_NUMBER>
```

Outputs JSON with:
- PR metadata
- Changed files in `server/` directory
- Target paths in eigent_server
- Sync complexity estimate

## Error Handling

| Error | Resolution |
|-------|------------|
| `gh` not authenticated | Run `gh auth login` |
| PR not found | Verify PR number and repo access |
| No server files | Inform user, no sync needed |
| File doesn't exist in target | Create new file or skip |
| Merge conflicts | Report and provide guidance |

## Example Usage

```
User: Sync eigent PR 456 to eigent_server

Agent:
1. Fetches PR #456 from eigent-ai/eigent
2. Finds 3 files changed in server/
3. Creates branch sync/eigent-pr-456
4. Applies changes to eigent_server/server/
5. Creates PR with title "Sync: Add user authentication"
```