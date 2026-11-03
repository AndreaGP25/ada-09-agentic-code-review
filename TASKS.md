# Tasks 

## T-01 Project setup
- **Goal:** Initialize project structure, set up virtual environment, and configure testing dependencies.
- **Files:**  `requirements.txt`, `.gitignore`, `README.md`, directory structure (`src/`, `tests/`).
- **Acceptance:** Virtual environment creates cleanly, dependencies install without conflicts, and `pytest` executes successfully.
- **Verification:** Run `pytest` from root directory; it should discover test directories and return status code 0.


## T-02 Domain model
- **Goal:** Create the core `Customer` entity and the mock dataset repository interface.
- **Files:** `src/domain/models.py`, `src/repository/customer_repository.py`, `tests/unit/test_models.py`.
- **Acceptance:** `Customer` dataclass contains `id`, `name`, and `email`. Repository class initializes with a pre-seeded mock list of customer records.
- **Verification:** Run `pytest tests/unit/test_models.py` to confirm model instantiation and dataset availability.


## T-03 Search logic
- **Goal:** Implement core case-insensitive partial match search algorithm across name and email fields.
- **Files:** `src/services/search_service.py`, `tests/unit/test_search_service.py`.
- **Acceptance:** Searching `"ana"` returns records matching `"Ana Silva"` or `"juliana@example.com"`. Valid searches with no matches return `[]`.
- **Verification:** Execute unit tests with valid queries and verify matching records are accurately returned.


## T-04 Validation and errors
- **Goal:** Implement query input validation rules and custom exceptions.
- **Files:** `src/domain/exceptions.py`, `src/services/search_service.py`, `tests/unit/test_validation.py`.
- **Acceptance:** `InvalidQueryError` is raised when query length is less than 2 characters or consists solely of whitespace. Leading/trailing whitespace in valid queries is automatically trimmed.
- **Verification:** Run `pytest tests/unit/test_validation.py` to ensure validation rules raise expected exceptions.


## T-05 Entrypoint & CLI interface
- **Goal:** Build the interface adapter (CLI script) connecting user input to the search service.
- **Files:** `src/entrypoints/cli.py`, `tests/integration/test_interface.py`.
- **Acceptance:** Interface parses inputs, invokes `CustomerSearchService`, outputs formatted results, and gracefully handles `InvalidQueryError` with error messages and appropriate exit.
- **Verification:** Run CLI command (e.g., `python -m src.entrypoints.cli --query "ana"`).


## T-06 Automated tests & coverage
- **Goal:** Achieve minimum 90% unit and integration test coverage.
- **Files:** `tests/`, `.coveragerc`.
- **Acceptance:** All acceptance criteria and test scenarios (TS-01 to TS-07) pass. Test suite achieves >= 90% code coverage.
- **Verification:** Run `pytest --cov=src --cov-report=term-missing` and confirm overall coverage percentage meets or exceeds 90%.


## T-07 Documentation
- **Goal:** Update documentation with setup instructions, usage examples, and verification steps.
- **Files:** `README.md`.
- **Acceptance:** Clear instructions on how to install dependencies, run the application (CLI), and execute automated tests.
- **Verification:** Follow instructions in `README.md` on a fresh terminal session to confirm setup and execution steps work end-to-end.