# ENV File Updater

The **ENV File Updater** (`env-updater`) reads all `KEY=VALUE` pairs from an
*update* ENV file and applies them to a *target* ENV file:

- **Existing keys** in the target file are updated **in place** — comments and
  blank lines around them are preserved.
- **New keys** that only exist in the update file are **appended** at the end of
  the target file.

Both arguments are optional. When omitted, the tool auto-detects what to do
based on the files present in the current working directory (see
[Auto-detect mode](#auto-detect-mode) below).

## Installation

```bash
pip install moles-tools
```

The `env-updater` command is available immediately after installation.

## Usage

```
env-updater [UPDATE] [TARGET] [--no-create] [--quiet]
```

| Argument / Flag | Description |
|---|---|
| `UPDATE` | ENV file whose values take precedence (optional). |
| `TARGET` | Target ENV file to update in-place. Auto-detected when omitted. Created if it doesn't exist (unless `--no-create` is set). |
| `--no-create` | Fail with an error if `TARGET` does not exist instead of creating it. |
| `--quiet`, `-q` | Suppress the summary output. |

## Auto-detect mode

When `TARGET` (and optionally `UPDATE`) is omitted, `env-updater` inspects the
current working directory and chooses an action automatically:

| Condition | Action |
|---|---|
| `UPDATE` given, `.env` **exists** | Update `.env` in-place with `UPDATE`. |
| `UPDATE` given, `.env` **missing**, `.env.example` / `env.example` found | Copy the example file to `.env`, then apply `UPDATE`. |
| No `UPDATE`, `.env` **missing**, example file found | Copy the example file to `.env` (no update applied). |
| No `UPDATE`, `.env` **already exists** | Nothing to do — exits successfully. |
| None of the above | Exits with an error. |

The tool prefers `.env.example` over `env.example` when both exist.

## Examples

### Basic update with explicit files

```bash
# .env.production contains the authoritative values
env-updater .env.production .env
```

After the command, `.env` contains all variables from `.env.production`. Any
variable already present in `.env` is updated; new variables are appended.

### Auto-update: apply an update file, target auto-detected

```bash
# .env already exists in the current directory
env-updater env.update
```

### Auto-bootstrap from example, then apply overrides

```bash
# No .env yet, but .env.example is present
env-updater env.update
# → copies .env.example to .env, then applies env.update
```

### Auto-bootstrap from example only (no overrides)

```bash
# No .env yet, but .env.example is present
env-updater
# → copies .env.example to .env
```

### Merge a partial override file

```bash
# Only override specific variables for a CI environment
cat ci-overrides.env
# CI=true
# DATABASE_URL=postgres://ci-host/ci_db

env-updater ci-overrides.env .env
```

### Fail fast if target is missing

```bash
env-updater defaults.env /etc/myapp/.env --no-create
```

### Quiet mode (for scripts)

```bash
env-updater new-defaults.env .env --quiet
echo "Exit code: $?"
```

## ENV File Format

The tool understands the standard `KEY=VALUE` format:

```env
# Database configuration
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=mydb

# Application
APP_SECRET_KEY=change-me-in-production
APP_DEBUG=false
```

Rules:
- Lines starting with `#` are treated as **comments** and are ignored when
  parsing variable names/values.
- **Blank lines** are ignored during parsing.
- Values may contain `=` characters (only the first `=` is treated as the
  key/value separator).
- Keys are not quoted; values are stored exactly as written (no quote stripping).

## Python API

You can also use `env-updater` as a library:

```python
from moles_tools.env_updater import update_env_file, parse_env_file

# Parse an ENV file into a dict
variables = parse_env_file("path/to/.env")
print(variables)  # {'KEY': 'value', ...}

# Update target from source
updated, added = update_env_file("source.env", "target.env")
print(f"{updated} variable(s) updated, {added} variable(s) added.")
```

### `parse_env_file(file_path)`

| Parameter | Type | Description |
|---|---|---|
| `file_path` | `str \| Path` | Path to the ENV file. |

**Returns** `dict[str, str]` — mapping of variable names to values.

**Raises** `FileNotFoundError` if the file does not exist, or `ValueError` if a
non-comment line has no `=` separator.

---

### `find_example_env(cwd)`

| Parameter | Type | Description |
|---|---|---|
| `cwd` | `Path` | Directory to search in. |

**Returns** `Path | None` — path to `.env.example` or `env.example` if found, otherwise `None`.
Prefers `.env.example` over `env.example` when both exist.

---

### `update_env_file(source_path, target_path, *, create_target=True)`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `source_path` | `str \| Path` | — | Source ENV file (read-only). |
| `target_path` | `str \| Path` | — | Target ENV file to update. |
| `create_target` | `bool` | `True` | Create target if it doesn't exist. |

**Returns** `tuple[int, int]` — `(updated, added)` counts.

**Raises** `FileNotFoundError` if either file is not found (subject to
`create_target`).
