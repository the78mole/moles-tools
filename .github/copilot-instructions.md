# Copilot Instructions for moles-tools

## Project Overview

**moles-tools** is a collection of command-line Python utilities managed as a single
installable package. The project aims to provide simple, well-tested tools for
common developer tasks.

The package is published to **PyPI** as `moles-tools` and can be installed with:
```bash
pip install moles-tools
# or
uv add moles-tools
```

## Repository Layout

```
moles-tools/
├── .devcontainer/          # Dev container definition (Ubuntu 24.04)
├── .github/
│   ├── copilot-instructions.md
│   └── workflows/
│       ├── ci.yml          # Build, test, lint, publish to PyPI
│       └── docs.yml        # Build & deploy VitePress docs to GitHub Pages
├── docs/                   # VitePress documentation source
│   ├── .vitepress/config.ts
│   ├── index.md
│   └── tools/              # One page per tool
├── src/moles_tools/        # Main Python package (src layout)
│   ├── __init__.py
│   ├── __main__.py         # `python -m moles_tools` entry point
│   └── env_updater.py      # ENV File Updater tool
├── tests/                  # pytest test suite
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml          # Single source of truth for project metadata & deps
├── renovate.json           # Renovate dependency-update config
└── README.md
```

## Technology Stack

| Concern | Tool |
|---|---|
| Dependency management / venv | [`uv`](https://docs.astral.sh/uv/) |
| Build backend | [hatchling](https://hatch.pypa.io/) |
| Versioning | [paulhatch/semantic-version](https://github.com/paulhatch/semantic-version) |
| Linting | [ruff](https://docs.astral.sh/ruff/) |
| Formatting | [black](https://black.readthedocs.io/) |
| Type checking | [mypy](https://mypy.readthedocs.io/) (strict mode) |
| Testing | [pytest](https://docs.pytest.org/) + pytest-cov |
| Pre-commit hooks | [pre-commit](https://pre-commit.com/) |
| Dependency updates | [Renovate](https://docs.renovatebot.com/) |
| Documentation | [VitePress](https://vitepress.dev/) |

## Development Setup

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and enter the repo
git clone https://github.com/the78mole/moles-tools.git
cd moles-tools

# Create venv and install all dependencies (including dev)
uv sync --all-extras

# Install pre-commit hooks
uv run pre-commit install

# Run the tests
uv run pytest

# Run linters
uv run ruff check src/ tests/
uv run black --check src/ tests/
uv run mypy src/
```

## Coding Conventions

### Python

- **Python version**: ≥ 3.11.  Use modern type-hint syntax: `str | None`, `list[str]`,
  `tuple[int, ...]`, etc.
- **Type hints**: All public functions must have full type annotations.  Run `mypy --strict`.
- **Docstrings**: Google-style docstrings for all public classes, functions, and modules.
- **Formatting**: `black` with `line-length = 88`.
- **Linting**: `ruff` with the `E,F,I,N,W,B,UP` rule set enabled.
- **No bare `except`** — always catch specific exception types.
- **`from __future__ import annotations`** at the top of every source file.

### Adding a New Tool

1. Create `src/moles_tools/<tool_name>.py`.
2. Implement a `main(argv: list[str] | None = None) -> int` CLI entry point.
3. Register the CLI script in `pyproject.toml` under `[project.scripts]`.
4. Add a corresponding test file `tests/test_<tool_name>.py`.
5. Add a documentation page `docs/tools/<tool-name>.md`.
6. Link the new page in `docs/.vitepress/config.ts`.

### Commit Message Format

Commits follow the [Conventional Commits](https://www.conventionalcommits.org/) spec.
The semantic versioning workflow (`paulhatch/semantic-version`) uses special tokens:

| Token | Effect |
|---|---|
| `#major` anywhere in commit body | Bumps **major** version |
| `#minor` anywhere in commit body | Bumps **minor** version |
| Default | Bumps **patch** version |

### Tests

- Use `pytest` with the `tmp_path` fixture for file-based tests.
- Every public function must have at least one happy-path test and one error-path test.
- Coverage threshold is **80%** (enforced in CI).

## CI / CD Pipeline

1. **Every push / PR**: `ci.yml` runs linting, type-checking, and tests on a matrix of
   OS × Python-version combinations.
2. **Push to `main`**: additionally builds the wheel/sdist and publishes to PyPI via
   OIDC trusted publishing (no stored secrets required).
3. **Push to `main`**: `docs.yml` builds and deploys the VitePress site to GitHub Pages.

## Environment Variables / Secrets

| Name | Where | Purpose |
|---|---|---|
| *(none — uses OIDC)* | GitHub environment `pypi` | PyPI trusted publishing |

## Useful Commands

```bash
# Run a single test file
uv run pytest tests/test_env_updater.py -v

# Auto-fix lint issues
uv run ruff check --fix src/ tests/
uv run black src/ tests/

# Build the distribution packages locally
uv build

# Serve the docs locally
cd docs && npm run docs:dev
```
