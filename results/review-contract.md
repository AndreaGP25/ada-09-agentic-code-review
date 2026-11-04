# Review Contract 
 
## Change 
CR-01 (Accent and diacritic normalization in customer search)
 
## Requirements / Acceptance Criteria 
- FR-01: Search customers using a text query matching name or email address
- FR-02: Case-insensitive and accent-insensitive partial matching
- AC-01: Partial match by name or email
- AC-02: Case-insensitive and accent-insensitive search logic (e.g., query "maría" matches "Maria Garcia", query "sofia" matches "Sofía López")
- AC-06: Automated unit tests covering edge cases and special characters with >= 90% code coverage
 
## Architecture Constraints 
- Expected dependency flow: Entrypoint/CLI (`src/entrypoints/`) -> Service (`src/services/`) -> Domain (`src/domain/`) & Repository Protocol (`src/repository/`). Core domain logic must remain decoupled from presentation and CLI adapters.
- Business-rule location: Core search validation, diacritic normalization (`_normalize_text`), and partial matching logic reside strictly in `src/services/search_service.py`. Domain invariants reside in `src/domain/models.py`.
- Protected boundaries:
  - Domain records: `Customer` instances are immutable dataclasses; underlying records stored in `InMemoryCustomerRepository` must not be mutated during normalization or search.
  - Zero heavy external dependencies: Core domain logic must strictly use Python standard library (`unicodedata`, `dataclasses`, `typing`).
  - Interface separation: CLI adapter handles only CLI argument parsing and I/O exit codes, delegating all domain search and validation to `CustomerSearchService`.
 
## Review Rules 
- Verify requirement coverage.
- Verify every called API/dependency exists.
- Check architecture boundaries.
- Inspect tests for masking / false confidence.
- Check regression behavior.
- Identify unnecessary technical debt.
- Cite evidence for every finding.
 
## Severity 
MUST FIX: 
Requirement violation, regression, security/integrity risk, 
hallucinated API/dependency, broken architecture constraint, 
or defect that makes the change unsafe to approve. 
 
SHOULD FIX: 
Significant maintainability, coverage, design, or clarity issue 
that does not block the requested behavior. 
 
OPTIONAL: 
Non-blocking improvement outside the minimum acceptance threshold.
