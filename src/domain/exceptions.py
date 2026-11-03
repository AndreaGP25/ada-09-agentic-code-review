"""Domain exceptions for customer search."""


class SearchDomainError(Exception):
    """Base domain exception."""
    pass


class InvalidQueryError(SearchDomainError):
    """Raised when a search query fails validation rules."""
    pass
