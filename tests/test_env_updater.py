"""Tests for the ENV File Updater tool."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from moles_tools.env_updater import (
    find_example_env,
    main,
    parse_env_file,
    update_env_file,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def write_env(path: Path, content: str) -> None:
    """Write *content* (dedented) to *path*."""
    path.write_text(textwrap.dedent(content), encoding="utf-8")


# ---------------------------------------------------------------------------
# parse_env_file
# ---------------------------------------------------------------------------


class TestParseEnvFile:
    def test_basic_key_value(self, tmp_path: Path) -> None:
        f = tmp_path / ".env"
        write_env(f, "FOO=bar\nBAZ=qux\n")
        result = parse_env_file(f)
        assert result == {"FOO": "bar", "BAZ": "qux"}

    def test_skips_comments(self, tmp_path: Path) -> None:
        f = tmp_path / ".env"
        write_env(f, "# This is a comment\nFOO=bar\n")
        result = parse_env_file(f)
        assert result == {"FOO": "bar"}
        assert len(result) == 1

    def test_skips_blank_lines(self, tmp_path: Path) -> None:
        f = tmp_path / ".env"
        write_env(f, "\nFOO=bar\n\nBAZ=qux\n")
        result = parse_env_file(f)
        assert result == {"FOO": "bar", "BAZ": "qux"}

    def test_value_containing_equals(self, tmp_path: Path) -> None:
        f = tmp_path / ".env"
        write_env(f, "URL=http://example.com?a=1&b=2\n")
        result = parse_env_file(f)
        assert result == {"URL": "http://example.com?a=1&b=2"}

    def test_empty_value(self, tmp_path: Path) -> None:
        f = tmp_path / ".env"
        write_env(f, "EMPTY=\n")
        result = parse_env_file(f)
        assert result == {"EMPTY": ""}

    def test_file_not_found(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            parse_env_file(tmp_path / "nonexistent.env")

    def test_line_without_equals_raises(self, tmp_path: Path) -> None:
        f = tmp_path / ".env"
        write_env(f, "NODIVIDER\n")
        with pytest.raises(ValueError, match="no '=' separator"):
            parse_env_file(f)

    def test_empty_file(self, tmp_path: Path) -> None:
        f = tmp_path / ".env"
        f.write_text("", encoding="utf-8")
        assert parse_env_file(f) == {}


# ---------------------------------------------------------------------------
# update_env_file — happy paths
# ---------------------------------------------------------------------------


class TestUpdateEnvFileUpdates:
    def test_updates_existing_variable(self, tmp_path: Path) -> None:
        source = tmp_path / "source.env"
        target = tmp_path / "target.env"
        write_env(source, "FOO=new_value\n")
        write_env(target, "FOO=old_value\n")

        updated, added = update_env_file(source, target)

        assert updated == 1
        assert added == 0
        lines = target.read_text().splitlines()
        assert "FOO=new_value" in lines

    def test_adds_missing_variable(self, tmp_path: Path) -> None:
        source = tmp_path / "source.env"
        target = tmp_path / "target.env"
        write_env(source, "NEW_VAR=hello\n")
        write_env(target, "EXISTING=value\n")

        updated, added = update_env_file(source, target)

        assert updated == 0
        assert added == 1
        content = target.read_text()
        assert "NEW_VAR=hello" in content
        assert "EXISTING=value" in content

    def test_updates_and_adds(self, tmp_path: Path) -> None:
        source = tmp_path / "source.env"
        target = tmp_path / "target.env"
        write_env(source, "EXISTING=updated\nNEW=brand_new\n")
        write_env(target, "EXISTING=old\n")

        updated, added = update_env_file(source, target)

        assert updated == 1
        assert added == 1

    def test_preserves_comments(self, tmp_path: Path) -> None:
        source = tmp_path / "source.env"
        target = tmp_path / "target.env"
        write_env(source, "FOO=new\n")
        write_env(target, "# My comment\nFOO=old\n")

        update_env_file(source, target)

        content = target.read_text()
        assert "# My comment" in content
        assert "FOO=new" in content

    def test_preserves_blank_lines(self, tmp_path: Path) -> None:
        source = tmp_path / "source.env"
        target = tmp_path / "target.env"
        write_env(source, "BAR=new\n")
        write_env(target, "FOO=keep\n\nBAR=old\n")

        update_env_file(source, target)

        lines = target.read_text().splitlines()
        assert "" in lines  # blank line preserved

    def test_creates_target_when_missing(self, tmp_path: Path) -> None:
        source = tmp_path / "source.env"
        target = tmp_path / "new_target.env"
        write_env(source, "A=1\nB=2\n")

        assert not target.exists()
        updated, added = update_env_file(source, target)

        assert target.exists()
        assert updated == 0
        assert added == 2

    def test_no_change_when_values_identical(self, tmp_path: Path) -> None:
        source = tmp_path / "source.env"
        target = tmp_path / "target.env"
        write_env(source, "FOO=same\n")
        write_env(target, "FOO=same\n")

        updated, added = update_env_file(source, target)

        assert updated == 0
        assert added == 0

    def test_value_with_equals(self, tmp_path: Path) -> None:
        source = tmp_path / "source.env"
        target = tmp_path / "target.env"
        write_env(source, "URL=https://example.com?a=1&b=2\n")
        write_env(target, "URL=old\n")

        update_env_file(source, target)

        lines = target.read_text().splitlines()
        assert "URL=https://example.com?a=1&b=2" in lines

    def test_empty_target_gets_all_source_vars(self, tmp_path: Path) -> None:
        source = tmp_path / "source.env"
        target = tmp_path / "target.env"
        write_env(source, "A=1\nB=2\nC=3\n")
        target.write_text("", encoding="utf-8")

        updated, added = update_env_file(source, target)

        assert updated == 0
        assert added == 3


# ---------------------------------------------------------------------------
# update_env_file — error handling
# ---------------------------------------------------------------------------


class TestUpdateEnvFileErrors:
    def test_source_not_found_raises(self, tmp_path: Path) -> None:
        source = tmp_path / "missing.env"
        target = tmp_path / "target.env"
        target.write_text("", encoding="utf-8")

        with pytest.raises(FileNotFoundError, match="Source file not found"):
            update_env_file(source, target)

    def test_no_create_raises_when_target_missing(self, tmp_path: Path) -> None:
        source = tmp_path / "source.env"
        source.write_text("A=1\n", encoding="utf-8")
        target = tmp_path / "missing_target.env"

        with pytest.raises(FileNotFoundError, match="Target file not found"):
            update_env_file(source, target, create_target=False)


# ---------------------------------------------------------------------------
# CLI (main)
# ---------------------------------------------------------------------------


class TestMain:
    def test_cli_basic(self, tmp_path: Path) -> None:
        source = tmp_path / "source.env"
        target = tmp_path / "target.env"
        write_env(source, "FOO=new\nBAR=added\n")
        write_env(target, "FOO=old\n")

        rc = main([str(source), str(target)])

        assert rc == 0
        content = target.read_text()
        assert "FOO=new" in content
        assert "BAR=added" in content

    def test_cli_missing_source(self, tmp_path: Path) -> None:
        rc = main([str(tmp_path / "nope.env"), str(tmp_path / "target.env")])
        assert rc == 1

    def test_cli_no_create_fails(self, tmp_path: Path) -> None:
        source = tmp_path / "source.env"
        source.write_text("A=1\n", encoding="utf-8")
        target = tmp_path / "nonexistent.env"

        rc = main([str(source), str(target), "--no-create"])

        assert rc == 1

    def test_cli_quiet(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        source = tmp_path / "source.env"
        target = tmp_path / "target.env"
        write_env(source, "X=1\n")
        write_env(target, "X=0\n")

        rc = main([str(source), str(target), "--quiet"])

        assert rc == 0
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_cli_creates_target(self, tmp_path: Path) -> None:
        source = tmp_path / "source.env"
        target = tmp_path / "new.env"
        write_env(source, "KEY=val\n")

        rc = main([str(source), str(target)])

        assert rc == 0
        assert target.exists()
        assert "KEY=val" in target.read_text()


# ---------------------------------------------------------------------------
# find_example_env
# ---------------------------------------------------------------------------


class TestFindExampleEnv:
    def test_finds_dot_env_example(self, tmp_path: Path) -> None:
        (tmp_path / ".env.example").write_text("A=1\n", encoding="utf-8")
        assert find_example_env(tmp_path) == tmp_path / ".env.example"

    def test_finds_env_example(self, tmp_path: Path) -> None:
        (tmp_path / "env.example").write_text("A=1\n", encoding="utf-8")
        assert find_example_env(tmp_path) == tmp_path / "env.example"

    def test_prefers_dot_env_example(self, tmp_path: Path) -> None:
        (tmp_path / ".env.example").write_text("A=1\n", encoding="utf-8")
        (tmp_path / "env.example").write_text("A=2\n", encoding="utf-8")
        assert find_example_env(tmp_path) == tmp_path / ".env.example"

    def test_returns_none_when_not_found(self, tmp_path: Path) -> None:
        assert find_example_env(tmp_path) is None


# ---------------------------------------------------------------------------
# Auto-detect: main() without explicit TARGET
# ---------------------------------------------------------------------------


class TestAutoDetect:
    """Tests for the auto-detection logic when TARGET is omitted."""

    def test_case1_updates_existing_dot_env(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Case 1: .env exists → update it with UPDATE file."""
        monkeypatch.chdir(tmp_path)
        update = tmp_path / "update.env"
        dot_env = tmp_path / ".env"
        write_env(update, "FOO=new\nBAR=added\n")
        write_env(dot_env, "FOO=old\n")

        rc = main([str(update)])

        assert rc == 0
        content = dot_env.read_text()
        assert "FOO=new" in content
        assert "BAR=added" in content

    def test_case2_creates_dot_env_from_example(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Case 2: no .env, .env.example exists → create .env from it, then apply UPDATE."""
        monkeypatch.chdir(tmp_path)
        update = tmp_path / "update.env"
        example = tmp_path / ".env.example"
        write_env(update, "SECRET=override\n")
        write_env(example, "DB=postgres\nSECRET=changeme\n")

        rc = main([str(update)])

        assert rc == 0
        dot_env = tmp_path / ".env"
        assert dot_env.exists()
        content = dot_env.read_text()
        assert "DB=postgres" in content
        assert "SECRET=override" in content

    def test_case2_uses_env_example_fallback(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Case 2: env.example (no leading dot) is used as fallback."""
        monkeypatch.chdir(tmp_path)
        update = tmp_path / "update.env"
        (tmp_path / "env.example").write_text("X=1\n", encoding="utf-8")
        write_env(update, "X=2\n")

        rc = main([str(update)])

        assert rc == 0
        content = (tmp_path / ".env").read_text()
        assert "X=2" in content

    def test_case2_no_example_returns_error(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Case 2 failure: no .env and no example → exit 1."""
        monkeypatch.chdir(tmp_path)
        update = tmp_path / "update.env"
        write_env(update, "A=1\n")

        rc = main([str(update)])

        assert rc == 1

    def test_case3_copies_example_to_dot_env(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Case 3: no UPDATE, no .env → copy .env.example to .env."""
        monkeypatch.chdir(tmp_path)
        example = tmp_path / ".env.example"
        write_env(example, "HOST=localhost\nPORT=5432\n")

        rc = main([])

        assert rc == 0
        dot_env = tmp_path / ".env"
        assert dot_env.exists()
        assert dot_env.read_text() == example.read_text()

    def test_case3_dot_env_already_exists_noop(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Case 3: .env already exists, nothing to do."""
        monkeypatch.chdir(tmp_path)
        dot_env = tmp_path / ".env"
        write_env(dot_env, "A=1\n")

        rc = main([])

        assert rc == 0
        captured = capsys.readouterr()
        assert "nothing to do" in captured.out

    def test_case3_no_example_no_dot_env_returns_error(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Case 3 failure: no .env and no example → exit 1."""
        monkeypatch.chdir(tmp_path)

        rc = main([])

        assert rc == 1

    def test_case3_quiet_suppresses_output(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Case 3 with --quiet suppresses output."""
        monkeypatch.chdir(tmp_path)
        write_env(tmp_path / ".env.example", "A=1\n")

        rc = main(["--quiet"])

        assert rc == 0
        assert capsys.readouterr().out == ""
