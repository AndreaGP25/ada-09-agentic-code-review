"""Unit tests for CustomerSearchService."""

import time
import unicodedata

import pytest

from src.domain.exceptions import InvalidQueryError
from src.domain.models import Customer
from src.repository.customer_repository import InMemoryCustomerRepository
from src.services.search_service import CustomerSearchService


def test_search_partial_match_by_name() -> None:
    """TS-01: Searching 'mar' returns 'Maria Garcia' and 'Omar Lopez'."""
    service = CustomerSearchService()
    results = service.search("mar")

    result_names = [c.name for c in results]
    assert "Maria Garcia" in result_names
    assert "Omar Lopez" in result_names


def test_search_partial_match_by_email() -> None:
    """TS-02: Searching 'gmail' returns all customers with @gmail.com addresses."""
    service = CustomerSearchService()
    results = service.search("gmail")

    assert len(results) >= 2
    for customer in results:
        assert "gmail" in customer.email.lower()


def test_search_case_insensitivity() -> None:
    """TS-03 & AC-02: Case-insensitive searching ('JOHNDOE' matches 'johndoe@example.com')."""
    service = CustomerSearchService()
    results = service.search("JOHNDOE")

    assert len(results) == 1
    assert results[0].name == "John Doe"
    assert results[0].email == "johndoe@example.com"


def test_search_case_insensitivity_mixed_casing() -> None:
    """Search matches regardless of query or record casing."""
    service = CustomerSearchService()
    results = service.search("aLiCe")

    assert len(results) == 1
    assert results[0].name == "Alice Smith"


def test_search_matches_both_name_and_email() -> None:
    """AC-01: Searching 'ana' matches both names ('Ana Silva') and emails ('juliana@example.com')."""
    service = CustomerSearchService()
    results = service.search("ana")

    result_names = [c.name for c in results]
    assert "Ana Silva" in result_names
    assert "Juliana Costa" in result_names


def test_search_no_match_returns_empty_list() -> None:
    """TS-04 & AC-04: Valid queries with no matches return empty list []."""
    service = CustomerSearchService()
    results = service.search("xyz123")

    assert results == []


def test_search_leading_trailing_whitespace_trimmed() -> None:
    """TS-07: Query with leading/trailing whitespace is trimmed and matches properly."""
    service = CustomerSearchService()
    results = service.search("  ana  ")

    result_names = [c.name for c in results]
    assert "Ana Silva" in result_names
    assert "Juliana Costa" in result_names


def test_search_performance_under_100ms() -> None:
    """NFR-01 & AC-05: Search executes and returns in less than 100 ms."""
    service = CustomerSearchService()
    start_time = time.perf_counter()
    results = service.search("ana")
    duration_ms = (time.perf_counter() - start_time) * 1000

    assert duration_ms < 100
    assert len(results) > 0


def test_search_with_custom_repository() -> None:
    """Verify CustomerSearchService with an injected custom repository."""
    custom_records = [
        Customer(id="101", name="Grace Hopper", email="grace@navy.mil"),
        Customer(id="102", name="Ada Lovelace", email="ada@analytical.org"),
    ]
    repo = InMemoryCustomerRepository(customers=custom_records)
    service = CustomerSearchService(repository=repo)

    results = service.search("hopper")
    assert len(results) == 1
    assert results[0].name == "Grace Hopper"

    results_none = service.search("maria")
    assert results_none == []


def test_search_special_characters_email_domain() -> None:
    """AC-06: Searching with special characters like '@' and '.' matches appropriately."""
    service = CustomerSearchService()
    results = service.search("@gmail.com")

    assert len(results) >= 2
    for customer in results:
        assert customer.email.endswith("@gmail.com")


def test_search_special_characters_dots_and_subdomain() -> None:
    """AC-06: Searching with '.' and hyphen or specific characters matches email addresses."""
    service = CustomerSearchService()
    results = service.search(".com")

    assert len(results) > 0
    for customer in results:
        assert ".com" in customer.email


def test_search_accented_query_matches_unaccented_records() -> None:
    """CR-01: Accented query matches unaccented customer records."""
    service = CustomerSearchService()

    # Query 'maría' matches 'Maria Garcia'
    results_maria = service.search("maría")
    result_names = [c.name for c in results_maria]
    assert "Maria Garcia" in result_names

    # Query 'lópez' matches 'Omar Lopez'
    results_lopez = service.search("lópez")
    assert "Omar Lopez" in [c.name for c in results_lopez]


def test_search_unaccented_query_matches_accented_records() -> None:
    """CR-01: Unaccented query matches customer records stored with accents."""
    custom_records = [
        Customer(id="201", name="Sofía López", email="sofia.lopez@example.com"),
        Customer(id="202", name="Andrés Gómez", email="andres.gomez@example.com"),
    ]
    repo = InMemoryCustomerRepository(customers=custom_records)
    service = CustomerSearchService(repository=repo)

    results = service.search("sofia")
    assert len(results) == 1
    assert results[0].name == "Sofía López"
    # Ensure underlying stored record is not modified
    assert results[0].name == "Sofía López"

    results_lopez = service.search("lopez")
    assert len(results_lopez) == 1
    assert results_lopez[0].name == "Sofía López"

    results_gomez = service.search("gomez")
    assert len(results_gomez) == 1
    assert results_gomez[0].name == "Andrés Gómez"


def test_search_combined_mixed_case_and_accent_insensitivity() -> None:
    """CR-01: Combined mixed case and accent insensitivity."""
    custom_records = [
        Customer(id="301", name="Maria Garcia", email="maria.garcia@example.com"),
        Customer(id="302", name="Sofía López", email="sofia.lopez@example.com"),
    ]
    repo = InMemoryCustomerRepository(customers=custom_records)
    service = CustomerSearchService(repository=repo)

    # Mixed case and accent on unaccented stored record
    results_maria = service.search("mArÍa")
    assert len(results_maria) == 1
    assert results_maria[0].name == "Maria Garcia"

    # Mixed case and unaccented query on accented stored record
    results_sofia = service.search("sOfIa")
    assert len(results_sofia) == 1
    assert results_sofia[0].name == "Sofía López"

    # Mixed case and accent on accented stored record
    results_sofia_accent = service.search("sOfÍa")
    assert len(results_sofia_accent) == 1
    assert results_sofia_accent[0].name == "Sofía López"


def test_search_accented_query_matches_accented_records() -> None:
    """CR-01: Accented query matches accented stored customer records."""
    custom_records = [
        Customer(id="401", name="Sofía López", email="sofia.lopez@example.com"),
    ]
    repo = InMemoryCustomerRepository(customers=custom_records)
    service = CustomerSearchService(repository=repo)

    results = service.search("sofía")
    assert len(results) == 1
    assert results[0].name == "Sofía López"


def test_search_accented_email_matching() -> None:
    """CR-01: Accent normalization applies to email matching as well."""
    custom_records = [
        Customer(id="501", name="Jose Perez", email="josé.pérez@empresa.es"),
    ]
    repo = InMemoryCustomerRepository(customers=custom_records)
    service = CustomerSearchService(repository=repo)

    # Search with unaccented term matches accented email
    results_unaccented = service.search("jose.perez")
    assert len(results_unaccented) == 1
    assert results_unaccented[0].email == "josé.pérez@empresa.es"

    # Search with accented term matches accented email
    results_accented = service.search("josé.pérez")
    assert len(results_accented) == 1
    assert results_accented[0].email == "josé.pérez@empresa.es"


def test_search_accented_with_surrounding_whitespace() -> None:
    """CR-01: Accented query with leading and trailing whitespace is trimmed and matches."""
    custom_records = [
        Customer(id="601", name="Ángel Morales", email="angel.morales@example.com"),
    ]
    repo = InMemoryCustomerRepository(customers=custom_records)
    service = CustomerSearchService(repository=repo)

    results = service.search("   ángel   ")
    assert len(results) == 1
    assert results[0].name == "Ángel Morales"

    # Match unaccented with surrounding whitespace
    results_unaccented = service.search("   angel   ")
    assert len(results_unaccented) == 1
    assert results_unaccented[0].name == "Ángel Morales"


def test_search_short_accented_valid_query() -> None:
    """CR-01: Two-character accented query passes validation and normalizes correctly."""
    custom_records = [
        Customer(id="701", name="Élise Dupont", email="elise@france.fr"),
    ]
    repo = InMemoryCustomerRepository(customers=custom_records)
    service = CustomerSearchService(repository=repo)

    results = service.search("él")
    assert len(results) == 1
    assert results[0].name == "Élise Dupont"


@pytest.mark.parametrize(
    "combining_query",
    ["\u0301\u0301", "\u0300\u0301\u0302", "   \u0301\u0301   ", "\t\u0303\u0308\t"],
)
def test_search_combining_characters_only_raises_invalid_query_error(
    combining_query: str,
) -> None:
    """RF-01 / RF-02: Queries composed only of combining marks normalize to empty and are rejected."""
    service = CustomerSearchService()
    with pytest.raises(InvalidQueryError, match="Query cannot be empty or whitespace"):
        service.search(combining_query)


@pytest.mark.parametrize(
    "decomposed_single_char",
    [
        unicodedata.normalize("NFD", "é"),
        unicodedata.normalize("NFD", "á"),
        unicodedata.normalize("NFD", "ó"),
        "e\u0301",
        "  a\u0301  ",
    ],
)
def test_search_decomposed_single_character_query_raises_invalid_query_error(
    decomposed_single_char: str,
) -> None:
    """RF-01 / RF-02: Decomposed single characters (len=2 raw, len=1 normalized) are rejected."""
    service = CustomerSearchService()
    with pytest.raises(InvalidQueryError, match="Query must be at least 2 characters long"):
        service.search(decomposed_single_char)


@pytest.mark.parametrize(
    ("decomposed_query", "expected_name"),
    [
        (unicodedata.normalize("NFD", "maría"), "Maria Garcia"),
        (unicodedata.normalize("NFD", "lópez"), "Omar Lopez"),
        (unicodedata.normalize("NFD", "élise"), "Élise Dupont"),
    ],
)
def test_search_decomposed_multicharacter_query_matches(
    decomposed_query: str, expected_name: str
) -> None:
    """RF-02: Multi-character decomposed Unicode (NFD) queries match unaccented and accented records."""
    custom_records = [
        Customer(id="801", name="Maria Garcia", email="maria@example.com"),
        Customer(id="802", name="Omar Lopez", email="omar@example.com"),
        Customer(id="803", name="Élise Dupont", email="elise@france.fr"),
    ]
    repo = InMemoryCustomerRepository(customers=custom_records)
    service = CustomerSearchService(repository=repo)

    results = service.search(decomposed_query)
    result_names = [c.name for c in results]
    assert expected_name in result_names
