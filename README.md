# moles-tools

[![CI/CD](https://github.com/the78mole/moles-tools/actions/workflows/ci.yml/badge.svg)](https://github.com/the78mole/moles-tools/actions/workflows/ci.yml)
[![Documentation](https://github.com/the78mole/moles-tools/actions/workflows/docs.yml/badge.svg)](https://the78mole.github.io/moles-tools)
[![PyPI version](https://badge.fury.io/py/moles-tools.svg)](https://badge.fury.io/py/moles-tools)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A collection of Python tools from the underground. 🐾

📖 **[Full Documentation](https://the78mole.github.io/moles-tools)**

## Tools

| Tool | Description |
|---|---|
| [`env-updater`](https://the78mole.github.io/moles-tools/tools/env-updater) | Update ENV variables in a target file from a source file |

## Quick Start

```bash
# Install from PyPI
pip install moles-tools

# Or with uv
uv add moles-tools

# Update .env from .env.production
env-updater .env.production .env
```

## Development

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and set up
git clone https://github.com/the78mole/moles-tools.git
cd moles-tools

# Install all dependencies
uv sync --all-extras

# Install pre-commit hooks
uv run pre-commit install

# Run tests
uv run pytest
```

## License

[MIT](LICENSE)
