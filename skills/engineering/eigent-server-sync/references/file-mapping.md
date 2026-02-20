# File Mapping Reference

## Directory Structure Mapping

The `eigent/server/` directory maps directly to `eigent_server/server/`:

```
eigent/server/                    eigent_server/server/
├── app/                          ├── app/
│   ├── __init__.py              │   ├── __init__.py
│   ├── controller/              │   ├── controller/
│   │   ├── __init__.py          │   │   ├── __init__.py
│   │   └── *.py                 │   │   └── *.py
│   ├── model/                   │   ├── model/
│   │   ├── __init__.py          │   │   ├── __init__.py
│   │   └── *.py                 │   │   └── *.py
│   ├── component/               │   ├── component/
│   │   ├── __init__.py          │   │   ├── __init__.py
│   │   └── *.py                 │   │   └── *.py
│   ├── service/                 │   ├── service/
│   │   ├── __init__.py          │   │   ├── __init__.py
│   │   └── *.py                 │   │   └── *.py
│   ├── type/                    │   ├── type/
│   │   ├── __init__.py          │   │   ├── __init__.py
│   │   └── *.py                 │   │   └── *.py
│   ├── command/                 │   ├── command/
│   ├── middleware/              │   ├── middleware/
│   ├── exception/               │   ├── exception/
│   ├── schedule/                │   ├── schedule/
│   └── public/                  │   └── public/
├── alembic/                     ├── alembic/
│   └── versions/                │   └── versions/
├── lang/                        ├── lang/
├── main.py                      ├── main.py
└── cli.py                       └── cli.py
```

## Sync Rules

### Always Sync

Files in these directories should always be synced:

| Directory | Reason |
|-----------|--------|
| `app/controller/` | API endpoint definitions |
| `app/model/` | Data models and schemas |
| `app/component/` | Shared utilities and components |
| `app/service/` | Business logic |
| `app/type/` | Type definitions |
| `app/command/` | CLI commands |
| `app/middleware/` | Request/response middleware |
| `app/exception/` | Exception handlers |
| `alembic/` | Database migrations |
| `main.py` | Application entry point |
| `cli.py` | CLI entry point |

### Handle with Care

| File | Consideration |
|------|---------------|
| `app/schedule/` | May have environment-specific schedules |
| `app/public/` | Uploaded files - usually not synced |
| `lang/` | Translations - sync if new keys added |
| Config files | May have environment-specific values |

### Never Sync

Files outside `server/` directory:
- `eigent/backend/` (CAMEL backend - different purpose)
- `eigent/src/` (React frontend)
- `eigent/electron/` (Electron main process)
- Root config files

## Change Type Handling

### Added Files

When a new file is added in `eigent/server/`:
1. Check if file exists in `eigent_server/server/`
2. If not, create the file with same content
3. Ensure parent directories exist

### Modified Files

When a file is modified in `eigent/server/`:
1. Get the diff from the PR
2. Apply the same changes to `eigent_server/server/`
3. Handle any structural differences

### Deleted Files

When a file is deleted in `eigent/server/`:
1. Check if file exists in `eigent_server/server/`
2. If it does, delete it
3. Note any dependencies that might break

### Renamed Files

When a file is renamed in `eigent/server/`:
1. Check for rename in PR metadata
2. Apply same rename in `eigent_server/server/`
3. Update any imports

## Structural Differences

### eigent_server Extensions

`eigent_server` may have additional files not in `eigent/server/`:
- Additional controllers for user management, payments
- Extended models with multi-tenancy
- Additional services

These should NOT be deleted during sync.

### Import Path Updates

After syncing files, check if imports need updating:
- `from eigent.server.app...` may need adjustment
- Relative imports should work as-is

## Example Mappings

```
eigent/server/app/controller/chat_controller.py
  -> eigent_server/server/app/controller/chat_controller.py

eigent/server/app/model/user.py
  -> eigent_server/server/app/model/user.py

eigent/server/alembic/versions/abc123_add_users_table.py
  -> eigent_server/server/alembic/versions/abc123_add_users_table.py
```