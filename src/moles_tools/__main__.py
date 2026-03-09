"""CLI entry point for moles-tools."""

import sys


def main() -> None:
    """Show available tools when moles-tools is called directly."""
    tools = {
        "env-updater": "Update ENV variables in a target file from a source file",
    }
    print("moles-tools - A collection of Python tools from the underground\n")
    print("Available tools:")
    for name, description in tools.items():
        print(f"  {name:<20} {description}")
    print("\nRun 'env-updater --help' for usage information.")
    sys.exit(0)


if __name__ == "__main__":
    main()
