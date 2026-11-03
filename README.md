# Customer Search

A Python application providing a reliable, validated, and fast customer search mechanism via CLI, querying customer records by partial name or email using in-memory data storage.

## Architecture and Design

The application follows a clean, layered architecture:
- `src/domain/`: Pure data structures and domain models ([`Customer`](file:///D:/MisDocumentos/ADA-05_Spec_Driven_Feature/src/domain/models.py#L6-L23), [`InvalidQueryError`](file:///D:/MisDocumentos/ADA-05_Spec_Driven_Feature/src/domain/exceptions.py#L8-L10)).
- `src/repository/`: In-memory customer repository interface ([`CustomerRepositoryProtocol`](file:///D:/MisDocumentos/ADA-05_Spec_Driven_Feature/src/repository/customer_repository.py#L22-L28)) and implementation ([`InMemoryCustomerRepository`](file:///D:/MisDocumentos/ADA-05_Spec_Driven_Feature/src/repository/customer_repository.py#L31-L43)).
- `src/services/`: Core search service ([`CustomerSearchService`](file:///D:/MisDocumentos/ADA-05_Spec_Driven_Feature/src/services/search_service.py#L13-L60)) with normalization, validation, and filtering.
- `src/entrypoints/`: CLI interface adapter ([`cli.py`](file:///D:/MisDocumentos/ADA-05_Spec_Driven_Feature/src/entrypoints/cli.py)).
- `tests/`: Automated unit and integration tests.

For further architectural and requirements specifications, refer to:
- [REQUIREMENTS.md](file:///D:/MisDocumentos/ADA-05_Spec_Driven_Feature/REQUIREMENTS.md)
- [SPEC.md](file:///D:/MisDocumentos/ADA-05_Spec_Driven_Feature/SPEC.md)
- [ARCHITECTURE.md](file:///D:/MisDocumentos/ADA-05_Spec_Driven_Feature/ARCHITECTURE.md)
- [TASKS.md](file:///D:/MisDocumentos/ADA-05_Spec_Driven_Feature/TASKS.md)
- [AGENTS.md](file:///D:/MisDocumentos/ADA-05_Spec_Driven_Feature/AGENTS.md)

---

## Setup & Installation

### Prerequisites
- Python 3.10 or higher

### Environment Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows PowerShell:
   .\.venv\Scripts\Activate.ps1
   # On Unix / macOS:
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## CLI Usage

The application provides a command-line interface to search pre-loaded in-memory customer records by name or email.

### Running a Search
Use the `--query` (or `-q`) option:
```bash
python -m src.entrypoints.cli --query "ana"
```

**Example Output:**
```text
Found 2 matching customer(s):
- ID: 1 | Name: Ana Silva | Email: ana.silva@example.com
- ID: 2 | Name: Juliana Costa | Email: juliana@example.com
```

### Searching by Email Domain
```bash
python -m src.entrypoints.cli --query "gmail"
```

**Example Output:**
```text
Found 2 matching customer(s):
- ID: 4 | Name: Omar Lopez | Email: omar.lopez@gmail.com
- ID: 9 | Name: David Johnson | Email: david.j@gmail.com
```

### Searching with No Matches
```bash
python -m src.entrypoints.cli --query "xyz123"
```

**Example Output:**
```text
No customers found matching the query.
```

### Validation Error Handling
Queries shorter than 2 characters or containing only whitespace return an error on `stderr` and exit with status code 1:
```bash
python -m src.entrypoints.cli --query "a"
```

**Example Output (stderr, exit code 1):**
```text
Error: Query must be at least 2 characters long
```

---

## Testing & Verification

### Running the Test Suite
Execute all unit and integration tests with `pytest`:
```bash
pytest
```

### Running with Code Coverage
Execute all tests with code coverage analysis:
```bash
pytest --cov=src --cov-report=term-missing
```

### Verification Checklist
- Run `python -m src.entrypoints.cli --query "ana"` to confirm successful execution and formatted results.
- Run `python -m src.entrypoints.cli --query "a"` to confirm error exit code `1` and stderr message.
- Run `pytest --cov=src --cov-report=term-missing` to confirm 100% test pass rate and >= 90% code coverage.
