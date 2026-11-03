"""Integration tests for the CLI entrypoint interface."""

import io
import subprocess
import sys

from src.entrypoints.cli import main, run_search


def test_cli_search_success_with_matches() -> None:
    """Test CLI search finds and prints matching customers."""
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_search("ana", stdout=stdout, stderr=stderr)

    assert exit_code == 0
    assert stderr.getvalue() == ""
    output = stdout.getvalue()
    assert "Found 2 matching customer(s):" in output
    assert "Ana Silva" in output
    assert "Juliana Costa" in output


def test_cli_search_no_matches() -> None:
    """Test CLI search with query that returns no matches."""
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_search("xyz123", stdout=stdout, stderr=stderr)

    assert exit_code == 0
    assert stderr.getvalue() == ""
    assert "No customers found matching the query." in stdout.getvalue()


def test_cli_search_query_too_short_prints_error_to_stderr() -> None:
    """Test CLI search with query shorter than 2 characters prints to stderr and exits with 1."""
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_search("a", stdout=stdout, stderr=stderr)

    assert exit_code == 1
    assert "Error: Query must be at least 2 characters long" in stderr.getvalue()


def test_cli_search_whitespace_only_prints_error_to_stderr() -> None:
    """Test CLI search with whitespace-only query prints to stderr and exits with 1."""
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_search("   ", stdout=stdout, stderr=stderr)

    assert exit_code == 1
    assert "Error: Query cannot be empty or whitespace" in stderr.getvalue()


def test_cli_main_argument_parsing_success() -> None:
    """Test main() parses --query argument and executes successfully."""
    exit_code = main(["--query", "ana"])
    assert exit_code == 0


def test_cli_main_short_flag_success() -> None:
    """Test main() parses -q flag and executes successfully."""
    exit_code = main(["-q", "ana"])
    assert exit_code == 0


def test_cli_main_missing_argument_fails() -> None:
    """Test main() returns non-zero when required argument is missing."""
    exit_code = main([])
    assert exit_code != 0


def test_cli_subprocess_end_to_end_success() -> None:
    """Execute CLI module via subprocess to verify end-to-end command-line behavior."""
    cmd = [sys.executable, "-m", "src.entrypoints.cli", "--query", "ana"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    assert result.returncode == 0
    assert "Found 2 matching customer(s):" in result.stdout
    assert "Ana Silva" in result.stdout
    assert "Juliana Costa" in result.stdout
    assert result.stderr == ""


def test_cli_subprocess_end_to_end_validation_failure() -> None:
    """Execute CLI module via subprocess with invalid query to verify exit code and stderr."""
    cmd = [sys.executable, "-m", "src.entrypoints.cli", "--query", "a"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    assert result.returncode == 1
    assert "Error: Query must be at least 2 characters long" in result.stderr


def test_cli_search_accented_query_success() -> None:
    """CR-01: CLI query execution with accented terms returns matching records and exits with code 0."""
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_search("maría", stdout=stdout, stderr=stderr)

    assert exit_code == 0
    assert stderr.getvalue() == ""
    output = stdout.getvalue()
    assert "Found 1 matching customer(s):" in output
    assert "Maria Garcia" in output


def test_cli_search_mixed_case_accented_query_success() -> None:
    """CR-01: CLI search with mixed case and accents matches records properly."""
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_search("mArÍa", stdout=stdout, stderr=stderr)

    assert exit_code == 0
    assert stderr.getvalue() == ""
    output = stdout.getvalue()
    assert "Found 1 matching customer(s):" in output
    assert "Maria Garcia" in output


def test_cli_subprocess_end_to_end_accented_query() -> None:
    """CR-01: Execute CLI subprocess with accented terms returns matching records and exits with code 0."""
    cmd = [sys.executable, "-m", "src.entrypoints.cli", "--query", "maría"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    assert result.returncode == 0
    assert "Found 1 matching customer(s):" in result.stdout
    assert "Maria Garcia" in result.stdout
    assert result.stderr == ""
