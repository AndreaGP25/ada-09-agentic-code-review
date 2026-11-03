"""Customer domain model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    """Represents a customer entity.
    
    Attributes:
        id: Unique identifier for the customer.
        name: Full name of the customer.
        email: Contact email address for the customer.
    """
    id: str
    name: str
    email: str

    def __post_init__(self) -> None:
        if not self.id or not str(self.id).strip():
            raise ValueError("Customer id cannot be empty.")
        if not self.name or not self.name.strip():
            raise ValueError("Customer name cannot be empty.")
        if not self.email or not self.email.strip():
            raise ValueError("Customer email cannot be empty.")
