"""Unit tests for search query validation and exception handling."""

import pytest

from src.domain.exceptions import InvalidQueryError, SearchDomainError
from src.services.search_service import CustomerSearchService


def test_invalid_query_error_inheritance() -> None:
    """Verify InvalidQueryError inherits from SearchDomainError and Exception."""
    assert issubclass(InvalidQueryError, SearchDomainError)
    assert issubclass(InvalidQueryError, Exception)


@pytest.mark.parametrize("short_query", ["a", "z", " 1 "])
def test_validation_failure_query_too_short(short_query: str) -> None:
    """TS-05 & AC-03: Queries shorter than 2 characters raise InvalidQueryError."""
    service = CustomerSearchService()
    with pytest.raises(InvalidQueryError, match="Query must be at least 2 characters long"):
        service.search(short_query)


@pytest.mark.parametrize("whitespace_query", ["", "   ", "\t", "\n", " \t \n "])
def test_validation_failure_whitespace_only(whitespace_query: str) -> None:
    """TS-06 & AC-03: Empty or whitespace-only queries raise InvalidQueryError."""
    service = CustomerSearchService()
    with pytest.raises(InvalidQueryError, match="Query cannot be empty or whitespace"):
        service.search(whitespace_query)


def test_validation_failure_none_query() -> None:
    """Null/missing query raises InvalidQueryError."""
    service = CustomerSearchService()
    with pytest.raises(InvalidQueryError, match="Query cannot be empty or whitespace"):
        service.search(None)  # type: ignore[arg-type]


def test_validation_boundary_two_characters_passes() -> None:
    """A trimmed 2-character query is valid and should not raise validation errors."""
    service = CustomerSearchService()
    results = service.search("an")
    assert isinstance(results, list)
