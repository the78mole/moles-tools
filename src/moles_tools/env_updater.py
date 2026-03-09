"""ENV File Updater: Updates ENV variables in a target file from a source file.

This tool reads all ENV variables from a source file and updates the
corresponding variables in a target file. Variables that exist in the source
but not in the target are appended at the end of the target file. Comments
and blank lines in the target file are preserved.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def parse_env_file(file_path: str | Path) -> dict[str, str]:
    """Parse an ENV file and return a dict of key-value pairs.

    Skips comments (lines starting with '#') and blank lines.
    Handles values containing '=' characters correctly.

    Args:
        file_path: Path to the ENV file to parse.

    Returns:
        Dictionary mapping variable names to their values.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If a non-comment, non-blank line lacks an '=' separator.
    """
    variables: dict[str, str] = {}
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as fh:
        for lineno, raw_line in enumerate(fh, start=1):
            line = raw_line.rstrip("\n")
            stripped = line.strip()

            # Skip blank lines and comment lines
            if not stripped or stripped.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(
                    f"{file_path}:{lineno}: Line has no '=' separator: {line!r}"
                )

            key, _, value = line.partition("=")
            variables[key.strip()] = value

    return variables


def update_env_file(
    source_path: str | Path,
    target_path: str | Path,
    *,
    create_target: bool = True,
) -> tuple[int, int]:
    """Update ENV variables in *target_path* with values from *source_path*.

    For each KEY=VALUE entry in the source file:
    - If KEY already exists in the target, its value is updated in place.
    - If KEY does not exist in the target, it is appended at the end.
    Comments and blank lines in the target are preserved unchanged.

    Args:
        source_path: Path to the source ENV file (read-only).
        target_path: Path to the target ENV file to update.
        create_target: If True and *target_path* does not exist, it is created.
            If False and *target_path* does not exist, FileNotFoundError is
            raised.

    Returns:
        A tuple ``(updated, added)`` with the count of variables that were
        updated in place and the count of new variables appended.

    Raises:
        FileNotFoundError: If *source_path* does not exist, or if
            *target_path* does not exist and *create_target* is False.
    """
    source = Path(source_path)
    target = Path(target_path)

    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    if not target.exists() and not create_target:
        raise FileNotFoundError(f"Target file not found: {target}")

    source_vars = parse_env_file(source)

    # Read the existing target lines (if any) --------------------------------
    target_lines: list[str] = []
    if target.exists():
        with target.open("r", encoding="utf-8") as fh:
            target_lines = [line.rstrip("\n") for line in fh]

    # Update existing keys in-place ------------------------------------------
    updated = 0
    found_keys: set[str] = set()

    for idx, line in enumerate(target_lines):
        stripped = line.strip()
        if stripped.startswith("#") or not stripped or "=" not in line:
            continue

        key, _, _ = line.partition("=")
        key = key.strip()
        found_keys.add(key)

        if key in source_vars:
            new_line = f"{key}={source_vars[key]}"
            if new_line != line:
                target_lines[idx] = new_line
                updated += 1

    # Append new keys --------------------------------------------------------
    added = 0
    new_lines: list[str] = []
    for key, value in source_vars.items():
        if key not in found_keys:
            new_lines.append(f"{key}={value}")
            added += 1

    if new_lines:
        # Add a blank separator line if the target is non-empty and does not
        # already end with a blank line.
        if target_lines and target_lines[-1].strip():
            target_lines.append("")
        target_lines.extend(new_lines)

    # Write the result -------------------------------------------------------
    content = "\n".join(target_lines)
    if content and not content.endswith("\n"):
        content += "\n"

    with target.open("w", encoding="utf-8") as fh:
        fh.write(content)

    return updated, added


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="env-updater",
        description=(
            "Update ENV variables in TARGET from SOURCE.\n\n"
            "Existing variables in TARGET are updated in place; new variables\n"
            "from SOURCE are appended at the end of TARGET."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "source",
        metavar="SOURCE",
        help="Source ENV file whose values take precedence.",
    )
    parser.add_argument(
        "target",
        metavar="TARGET",
        help="Target ENV file to update (created if it does not exist).",
    )
    parser.add_argument(
        "--no-create",
        dest="create_target",
        action="store_false",
        default=True,
        help="Fail if TARGET does not exist instead of creating it.",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        default=False,
        help="Suppress informational output.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for the env-updater tool.

    Args:
        argv: Argument list (defaults to sys.argv[1:]).

    Returns:
        Exit code (0 on success, non-zero on error).
    """
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        updated, added = update_env_file(
            args.source,
            args.target,
            create_target=args.create_target,
        )
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not args.quiet:
        target_name = os.path.basename(args.target)
        print(
            f"env-updater: {target_name} — "
            f"{updated} variable(s) updated, {added} variable(s) added."
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
