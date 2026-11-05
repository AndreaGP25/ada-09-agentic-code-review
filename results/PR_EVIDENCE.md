# PR Evidence 

## Change 
Change ID: CR-01 (Normalize accents and diacritics in customer search)  
PR / Branch: `ada09/cr-01`  
Base commit: `8ffd87ca7aca1b87e049cb76006dc5424b7b45d9`  
Final commit: `627b9b6eb16c1d9777985646f6cb41aa5fa87707`  

## Requirements / Acceptance Criteria 
- FR-01: Searching customers using text query matching customer name or email address.
- FR-02: Case-insensitive and accent/diacritic-insensitive partial matching.
- FR-03: Query validation rejecting inputs shorter than 2 characters, whitespace-only, or collapsing to < 2 characters / empty after normalization.
- FR-04: Structured record output containing ID, name, and email.
- FR-05: Empty result set handling with clear user feedback when no matching records are found.
- FR-06: Graceful error handling returning descriptive messages without unhandled exceptions or crashes.
- NFR-01: Search performance execution time under 100 ms.
- NFR-02: Code coverage >= 90% across domain and search modules.
- NFR-03: Decoupled clean architecture separating domain logic from CLI presentation adapter.
- AC-01: Partial match by name or email ("ana" matches "Ana Silva" and "juliana@example.com").
- AC-02: Case-insensitive and accent-insensitive matching ("ALICE" matches "alice@example.com", "maría" matches "Maria Garcia", "sofia" matches "Sofía López").
- AC-03: Single-character queries ("a", decomposed "e\u0301"), whitespace, and combining-only marks raise validation errors and do not execute search.
- AC-04: Valid queries with no matches return an empty list without errors.
- AC-05: Core search execution finishes in < 100 ms (measured ~0.13 ms).
- AC-06: Automated test suite covers edge cases (accents, Unicode NFD decomposition, combining marks, whitespace, short queries, boundary values) with >= 90% coverage.

## Implementation 
Coder report: `results/coder-report.md`  
Files changed: 
- `CHANGE_REQUEST.md`: Formal approved change request for CR-01.
- `TASK_UNDER_TEST.md`: Synchronized task specification and human approval status.
- `src/services/search_service.py`: Text normalization helper (`_normalize_text`), accent-insensitive filtering, and post-normalization length and non-emptiness validation guards.
- `tests/unit/test_search_service.py`: Unit tests for accent normalization, edge cases, combining marks, single-character decomposed queries, and multi-character NFD queries.
- `tests/integration/test_interface.py`: CLI integration tests verifying accented queries, mixed case, and subprocess execution.
- `results/review-contract.md`: Code review criteria and constraints contract.
- `results/review-report.md`: Initial independent review report.
- `results/human-review-decisions.md`: Human review decisions on initial findings.
- `results/re-review-report.md`: Independent re-review report on the updated candidate.
- `results/coder-report.md`: Implementation and fix cycle report from Coder Agent.
- `results/verification-report.md`: Verification report artifact.
- `results/commits.txt`: Commit log.
- `results/pr.diff`: PR diff snapshot.

Commits: 
- `1ed6627 feat: implement CR-01`: Initial implementation of accent normalization, unit and CLI integration tests.
- `627b9b6 fix: address ADA-09 review findings`: Addressed review findings RF-01 and RF-02 (post-normalization guards, parameterized Unicode NFD/combining tests, clean repository tree).

## Verification 
Verification command: `& "C:\Program Files\Git\bin\bash.exe" scripts/verify_repo.sh`  
Final result: `VERIFY_REPO: PASS`  
Tests: 66 passed in 0.56s (0 failures, 100.00% statement and branch code coverage across `src/`)  
Lint: `ruff check .` (All checks passed cleanly, 0 errors, 0 warnings)  
Security / repo checks: `REPO_CONTRACT: PASS` (all 7 required files verified), zero new external runtime dependencies (relies strictly on Python standard library `unicodedata`), customer dataclass immutability preserved, zero hardcoded credentials or secrets.

## Independent Review 
Review report: `results/review-report.md`  
MUST FIX found: 2 
- RF-01: Combining-mark-only queries (e.g., `"\u0301\u0301"`) bypass length check, normalize to `""`, and dump 100% of the repository records.
- RF-02: Decomposed single-character queries (e.g., `"e\u0301"`, len=2) bypass initial length check, normalize to 1 char, and execute illegal single-letter query.

SHOULD FIX found: 3 
- RF-03: PR diff snapshot omission due to base commit code pre-inclusion.
- RF-04: Test suite lacked tests for decomposed Unicode (NFD) and combining-only marks.
- RF-05: Unstaged modifications in working tree for `scripts/verify_repo.sh`.

OPTIONAL found: 2 
- RF-06: In-loop redundant normalization ($2N$ calls per search).
- RF-07: Legacy route references in `docs/REPO_MAP.md`.

## Human Decisions 
Accepted: 
- RF-01 (MUST FIX): Modify `CustomerSearchService.search()` to validate `normalized_query` length and non-emptiness after diacritic stripping.

Modified: 
- RF-02 (Promoted to MUST FIX): Add parameterized unit tests in `test_search_service.py` for combining-character queries, decomposed single characters, and multi-character NFD queries; clean up unstaged changes in `scripts/verify_repo.sh`.

Rejected: None  
Deferred: 
- RF-03 (Consolidating initial RF-06 and RF-07): In-loop normalization caching rejected as premature optimization given sub-millisecond execution (< 1 ms vs 100 ms limit); `docs/REPO_MAP.md` path drift deferred to general repository maintenance.

## Re-review 
Re-review report: `results/re-review-report.md`  
Resolved: 
- RF-01: Post-normalization checks (`if not normalized_query` and `if len(normalized_query) < 2`) inserted in `src/services/search_service.py:56-62`. Verified with combining-only marks and decomposed single characters.
- RF-02: Parameterized tests added in `tests/unit/test_search_service.py:256-309` covering combining marks, decomposed single characters, and multi-character NFD queries (12 new automated executions, all passing); working tree clean; `scripts/verify_repo.sh` passing.

Partially resolved: 0  
Not resolved: 0  
New MUST FIX: 0 (No regressions detected; 66/66 tests pass, 100% coverage, 0 lint warnings)  

## Traceability 

| Requirement / AC | Task / Change | Code | Test | Review Finding |
|---|---|---|---|---|
| **FR-01 / AC-01** | CR-01: Partial text search across name and email | `src/services/search_service.py:64-70` | `tests/unit/test_search_service.py:14-32, 53-62`<br>`tests/integration/test_interface.py:10-23` | Baseline |
| **FR-02 / AC-02** | CR-01: Case and accent insensitivity | `src/services/search_service.py:14-18, 66-68` | `tests/unit/test_search_service.py:34-51, 130-222, 287-309`<br>`tests/integration/test_interface.py:98-134` | RF-02 |
| **FR-03 / AC-03** | CR-01 / Fix Cycle: Input validation & diacritic stripping guards | `src/services/search_service.py:46-62` | `tests/unit/test_validation.py:15-36`<br>`tests/unit/test_search_service.py:256-285`<br>`tests/integration/test_interface.py:37-57, 89-96` | RF-01, RF-02 |
| **FR-04** | CR-01: Structured customer record representation | `src/domain/models.py:6-25`<br>`src/entrypoints/cli.py:67-73` | `tests/unit/test_models.py:13-19`<br>`tests/integration/test_interface.py:10-23, 77-87` | Baseline |
| **FR-05 / AC-04** | CR-01: Empty result set handling | `src/services/search_service.py:71`<br>`src/entrypoints/cli.py:63-65` | `tests/unit/test_search_service.py:63-69`<br>`tests/integration/test_interface.py:25-35` | Baseline / RF-01 |
| **FR-06 / AC-03** | CR-01: Graceful error handling without crashes | `src/domain/exceptions.py:9-11`<br>`src/entrypoints/cli.py:59-62` | `tests/unit/test_validation.py:9-13`<br>`tests/integration/test_interface.py:37-57` | Baseline / RF-01 |
| **NFR-01 / AC-05** | CR-01: Search performance < 100 ms | `src/services/search_service.py:64-70` | `tests/unit/test_search_service.py:81-90` (measured ~0.13 ms) | RF-03 / RF-06 |
| **NFR-02 / AC-06** | CR-01: Automated test coverage >= 90% | Entire suite in `tests/` | 66 passed, 100.00% statement and branch coverage | RF-02, RF-04 |
| **NFR-03** | CR-01: Decoupled architecture (CLI vs domain) | `src/entrypoints/cli.py`<br>`src/services/search_service.py` | `tests/integration/test_interface.py`<br>`tests/unit/test_models.py:70-74` | Baseline |

## Remaining Risks / Technical Debt 
- **Linear In-Memory Scanning:** Search iterates over records in memory ($O(N)$) and normalizes fields dynamically per query. Highly efficient for current dataset size (< 10,000 records, benchmarks at ~0.13 ms), but large-scale enterprise deployments would benefit from pre-normalized index structures or database indexing.
- **Documentation Path Drift:** `docs/REPO_MAP.md` references legacy entrypoints (`src/app.py`, `src/api/`). Acknowledged by Human Reviewer and deferred to repository maintenance.
- **Audit Metric Artifact Lag:** `results/verification-report.md` retains the initial 54-test count from commit `1ed6627`, while `results/coder-report.md` and `results/re-review-report.md` reflect the full 66-test count from commit `627b9b6`.

## Final Human Decision 
[ ] NOT READY 
[X] READY FOR HUMAN MERGE 

Approved by: Andrea Góngora  
Date: 04/11/2026
