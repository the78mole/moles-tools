# Installation

## Requirements

- Python **3.11** or newer
- `pip`, `uv`, or `pipx`

## Install from PyPI

::: code-group

```bash [pip]
pip install moles-tools
```

```bash [uv]
uv add moles-tools
```

```bash [pipx (recommended for CLI tools)]
pipx install moles-tools
```

:::

## Verify the installation

```bash
moles-tools
```

You should see a list of all available tools.

## Development Installation

If you want to contribute or run from source:

```bash
# Clone the repository
git clone https://github.com/the78mole/moles-tools.git
cd moles-tools

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install all dependencies (including dev extras)
uv sync --all-extras

# Install pre-commit hooks
uv run pre-commit install

# Run the tests
uv run pytest
```

## Using the Dev Container

The repository ships with a ready-to-use
[Dev Container](https://containers.dev/) configuration for VS Code and
GitHub Codespaces.

1. Open the repository in VS Code.
2. Click **Reopen in Container** when prompted.
3. The container is based on **Ubuntu 24.04** and comes pre-installed with
   Python, uv, all linters, and the GitHub CLI.
