# Contributing

Thank you for considering a contribution to **moles-tools**! 🎉

## Getting Started

1. **Fork** the repository and clone your fork.
2. Follow the [installation guide](./installation) to set up your dev environment.
3. Create a feature branch:
   ```bash
   git checkout -b feat/my-new-tool
   ```
4. Make your changes, add tests, and update the documentation.
5. Push your branch and open a **Pull Request** against `main`.

## Coding Conventions

- **Python ≥ 3.11** — use modern type-hint syntax.
- Full type annotations on all public functions (`mypy --strict`).
- Google-style docstrings.
- Formatting: `black` (`line-length = 88`).
- Linting: `ruff` with the `E,F,I,N,W,B,UP` rule set.
- No bare `except` — always catch specific exception types.

## Adding a New Tool

1. Create `src/moles_tools/<tool_name>.py`.
2. Implement a `main(argv: list[str] | None = None) -> int` CLI entry point.
3. Register it in `pyproject.toml` under `[project.scripts]`.
4. Add `tests/test_<tool_name>.py` with happy-path **and** error-path tests.
5. Add a documentation page at `docs/tools/<tool-name>.md`.
6. Link the new page in `docs/.vitepress/config.ts`.

## Commit Message Format

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.
The semantic-versioning workflow reads special tokens from the commit body:

| Token | Effect |
|---|---|
| `#major` | Bumps **major** version (breaking change) |
| `#minor` | Bumps **minor** version (new feature) |
| *(default)* | Bumps **patch** version (bug fix) |

## Running the Checks Locally

```bash
# All pre-commit hooks
uv run pre-commit run --all-files

# Tests with coverage
uv run pytest

# Individual linters
uv run ruff check src/ tests/
uv run black --check src/ tests/
uv run mypy src/
```

## CI Pipeline

Every pull request is checked by GitHub Actions (`ci.yml`):

- Linting (ruff, black)
- Type checking (mypy)
- Tests on **Ubuntu (latest & 22.04)**, **macOS**, and **Windows**,
  for Python **3.11** and **3.12**

All checks must pass before a PR can be merged.
