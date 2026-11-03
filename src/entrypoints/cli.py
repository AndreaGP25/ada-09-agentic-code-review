"""CLI entrypoint for Customer Search application."""

import argparse
import sys
from typing import Optional, Sequence, TextIO

from src.domain.exceptions import InvalidQueryError
from src.services.search_service import CustomerSearchService


def parse_args(args: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.
    
    Args:
        args: Sequence of argument strings to parse, or None for sys.argv[1:].
        
    Returns:
        argparse.Namespace containing parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Search customer records by name or email address."
    )
    parser.add_argument(
        "--query",
        "-q",
        type=str,
        required=True,
        help="Search query string (minimum 2 characters).",
    )
    return parser.parse_args(args)


def run_search(
    query: str,
    service: Optional[CustomerSearchService] = None,
    stdout: Optional[TextIO] = None,
    stderr: Optional[TextIO] = None,
) -> int:
    """Execute customer search and format output.
    
    Args:
        query: Search query string.
        service: CustomerSearchService instance (defaults to a new instance).
        stdout: Output stream for search results (defaults to sys.stdout).
        stderr: Error stream for error messages (defaults to sys.stderr).
        
    Returns:
        0 on success, 1 on validation error.
    """
    if stdout is None:
        stdout = sys.stdout
    if stderr is None:
        stderr = sys.stderr

    search_svc = service if service is not None else CustomerSearchService()

    try:
        results = search_svc.search(query)
    except InvalidQueryError as err:
        print(f"Error: {err}", file=stderr)
        return 1

    if not results:
        print("No customers found matching the query.", file=stdout)
        return 0

    print(f"Found {len(results)} matching customer(s):", file=stdout)
    for customer in results:
        print(
            f"- ID: {customer.id} | Name: {customer.name} | Email: {customer.email}",
            file=stdout,
        )

    return 0


def main(args: Optional[Sequence[str]] = None) -> int:
    """CLI entrypoint function.
    
    Args:
        args: Optional list of command-line arguments.
        
    Returns:
        Exit status code (0 for success, non-zero for error).
    """
    try:
        parsed = parse_args(args)
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 1

    return run_search(parsed.query)


if __name__ == "__main__":
    sys.exit(main())
