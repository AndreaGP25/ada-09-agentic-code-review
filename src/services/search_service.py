"""Customer search service module."""

from typing import List, Optional
import unicodedata

from src.domain.exceptions import InvalidQueryError
from src.domain.models import Customer
from src.repository.customer_repository import (
    CustomerRepositoryProtocol,
    InMemoryCustomerRepository,
)


def _normalize_text(text: str) -> str:
    """Normalize text by stripping diacritics/accents and converting to lowercase."""
    nfd_text = unicodedata.normalize("NFD", text)
    return "".join(c for c in nfd_text if unicodedata.category(c) != "Mn").lower()


class CustomerSearchService:
    """Service responsible for searching customer records."""

    def __init__(self, repository: Optional[CustomerRepositoryProtocol] = None) -> None:
        """Initialize CustomerSearchService.
        
        Args:
            repository: Customer repository fulfilling CustomerRepositoryProtocol.
                        Defaults to InMemoryCustomerRepository.
        """
        self._repository: CustomerRepositoryProtocol = (
            repository if repository is not None else InMemoryCustomerRepository()
        )

    def search(self, query: str) -> List[Customer]:
        """Search customers by name or email using case-insensitive and accent-insensitive partial match.
        
        Args:
            query: The search query string.
            
        Returns:
            List of matching Customer records, or an empty list if no matches found.

        Raises:
            InvalidQueryError: If query is None, empty, whitespace-only, or < 2 characters.
        """
        if query is None:
            raise InvalidQueryError("Query cannot be empty or whitespace")

        trimmed_query = query.strip()
        if not trimmed_query:
            raise InvalidQueryError("Query cannot be empty or whitespace")

        if len(trimmed_query) < 2:
            raise InvalidQueryError("Query must be at least 2 characters long")

        normalized_query = _normalize_text(trimmed_query)

        results: List[Customer] = []
        for customer in self._repository.get_all():
            if (
                normalized_query in _normalize_text(customer.name)
                or normalized_query in _normalize_text(customer.email)
            ):
                results.append(customer)

        return results
