# Task Under Test

Change ID: CR-01

## Goal
Normalize accents and diacritics in customer search (normalizar tildes y diacríticos en búsqueda de clientes). Extend query and target field normalization during search matching so queries match customer names and emails regardless of accents or diacritical marks, without modifying the underlying stored records.

## Requirements Covered
- FR-01: Search customers using text query matching name or email (see REQUIREMENTS.md)
- FR-02: Case-insensitive partial matching (see REQUIREMENTS.md)
- AC-01: Partial match by name or email (see SPEC.md)
- AC-02: Case-insensitive search logic (see SPEC.md)
- AC-06: Automated unit tests covering edge cases and special characters with >= 90% coverage (see SPEC.md)

## Verification
- Automated unit tests (`pytest tests/unit/test_search_service.py`):
  - Accented query matches unaccented customer records (e.g., query `"maría"` matches `"Maria Garcia"`).
  - Unaccented query matches customer records stored with accents (e.g., query `"sofia"` matches `"Sofía López"`).
  - Combined mixed case and accent insensitivity (e.g., query `"mArÍa"` matches `"Maria Garcia"`).
- CLI integration tests (`pytest tests/integration/test_interface.py`):
  - CLI query execution with accented terms returns matching records and exits with code 0.
- Regression testing and coverage:
  - All existing test suite cases pass (`pytest`) with >= 90% code coverage.

## Constraints
- Use REQUIREMENTS.md and SPEC.md as the source of truth.
- Keep changes scoped to this task.
- Do not redefine requirements in this file.