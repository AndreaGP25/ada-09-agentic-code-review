"""In-memory customer repository implementation and protocol."""

from typing import List, Optional, Protocol, Sequence, runtime_checkable

from src.domain.models import Customer

DEFAULT_CUSTOMERS: tuple[Customer, ...] = (
    Customer(id="1", name="Ana Silva", email="ana.silva@example.com"),
    Customer(id="2", name="Juliana Costa", email="juliana@example.com"),
    Customer(id="3", name="Maria Garcia", email="maria.garcia@example.com"),
    Customer(id="4", name="Omar Lopez", email="omar.lopez@gmail.com"),
    Customer(id="5", name="John Doe", email="johndoe@example.com"),
    Customer(id="6", name="Alice Smith", email="alice@example.com"),
    Customer(id="7", name="Carlos Mendez", email="carlos.m@yahoo.com"),
    Customer(id="8", name="Beatriz Ramirez", email="beatriz@example.com"),
    Customer(id="9", name="David Johnson", email="david.j@gmail.com"),
    Customer(id="10", name="Elena Rostova", email="elena.r@corporate.org"),
    Customer(id="11", name="Fernando Torres", email="f.torres@sports.es"),
    Customer(id="12", name="Lucia Fernandez", email="lucia.f@company.net"),
)


@runtime_checkable
class CustomerRepositoryProtocol(Protocol):
    """Protocol for customer data access repository."""

    def get_all(self) -> Sequence[Customer]:
        """Retrieve all customer records."""
        ...


class InMemoryCustomerRepository:
    """In-memory implementation of customer repository."""

    def __init__(self, customers: Optional[Sequence[Customer]] = None) -> None:
        if customers is not None:
            self._customers: List[Customer] = list(customers)
        else:
            self._customers = list(DEFAULT_CUSTOMERS)

    def get_all(self) -> List[Customer]:
        """Return a copy of all stored customer records."""
        return list(self._customers)
