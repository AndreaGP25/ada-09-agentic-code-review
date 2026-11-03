"""Unit tests for Customer domain model and InMemoryCustomerRepository."""

from dataclasses import FrozenInstanceError
import pytest

from src.domain.models import Customer
from src.repository.customer_repository import (
    CustomerRepositoryProtocol,
    InMemoryCustomerRepository,
)


def test_customer_creation_valid() -> None:
    """Test creating a Customer with valid attributes."""
    customer = Customer(id="c1", name="John Doe", email="john.doe@example.com")
    assert customer.id == "c1"
    assert customer.name == "John Doe"
    assert customer.email == "john.doe@example.com"


@pytest.mark.parametrize("invalid_id", ["", "   "])
def test_customer_empty_id_raises_error(invalid_id: str) -> None:
    """Test that invalid or blank ID raises ValueError."""
    with pytest.raises(ValueError, match="Customer id cannot be empty"):
        Customer(id=invalid_id, name="John Doe", email="john.doe@example.com")


@pytest.mark.parametrize("invalid_name", ["", "   "])
def test_customer_empty_name_raises_error(invalid_name: str) -> None:
    """Test that invalid or blank name raises ValueError."""
    with pytest.raises(ValueError, match="Customer name cannot be empty"):
        Customer(id="c1", name=invalid_name, email="john.doe@example.com")


@pytest.mark.parametrize("invalid_email", ["", "   "])
def test_customer_empty_email_raises_error(invalid_email: str) -> None:
    """Test that invalid or blank email raises ValueError."""
    with pytest.raises(ValueError, match="Customer email cannot be empty"):
        Customer(id="c1", name="John Doe", email=invalid_email)


def test_customer_immutability() -> None:
    """Test that Customer instances are immutable (frozen)."""
    customer = Customer(id="c1", name="John Doe", email="john.doe@example.com")
    with pytest.raises(FrozenInstanceError):
        customer.name = "Jane Doe"  # type: ignore[misc]


def test_in_memory_repository_default_seed() -> None:
    """Test that InMemoryCustomerRepository initializes with default seeded records."""
    repo = InMemoryCustomerRepository()
    records = repo.get_all()
    assert len(records) >= 10
    assert all(isinstance(c, Customer) for c in records)


def test_in_memory_repository_custom_seed() -> None:
    """Test that InMemoryCustomerRepository can be initialized with custom records."""
    custom_records = [
        Customer(id="1", name="Alice", email="alice@test.com"),
        Customer(id="2", name="Bob", email="bob@test.com"),
    ]
    repo = InMemoryCustomerRepository(customers=custom_records)
    records = repo.get_all()
    assert len(records) == 2
    assert records[0].name == "Alice"
    assert records[1].name == "Bob"


def test_in_memory_repository_implements_protocol() -> None:
    """Test that InMemoryCustomerRepository satisfies CustomerRepositoryProtocol."""
    repo = InMemoryCustomerRepository()
    assert isinstance(repo, CustomerRepositoryProtocol)


def test_in_memory_repository_returns_copy() -> None:
    """Test that mutating the returned list does not affect repository internal state."""
    repo = InMemoryCustomerRepository()
    initial_count = len(repo.get_all())
    records = repo.get_all()
    records.clear()
    assert len(repo.get_all()) == initial_count
