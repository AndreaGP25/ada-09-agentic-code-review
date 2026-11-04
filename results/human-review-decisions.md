# Human Review Decisions 
 
## Change 
CR-01 (Normalize accents and diacritics in customer search)
 
### RF-01 
Reviewer severity: MUST FIX 
Human decision: ACCEPTED 
Reason: 
Confirmed critical defect and data exposure risk. When a query contains only Unicode combining marks (e.g., `"\u0301\u0301"`), it satisfies the initial `len >= 2` guard before normalization. `_normalize_text()` then strips all `Mn` marks, yielding an empty string `""`. In `CustomerSearchService.search()`, `"" in _normalize_text(customer.name)` evaluates to `True` for every customer, dumping all 12 records in the repository instead of rejecting the invalid query. Likewise, single-character decomposed queries (e.g., `"e\u0301"`, len=2) bypass the `< 2` check and execute a single-letter search returning 11 records, directly violating FR-03, FR-05, and AC-03.
Required action: 
Modify `CustomerSearchService.search()` in `src/services/search_service.py` to validate `normalized_query` after diacritic stripping. Ensure that if `normalized_query` is empty or has `len(normalized_query) < 2`, `InvalidQueryError` is raised before entering the repository filtering loop.
 
### RF-02 
Reviewer severity: SHOULD FIX 
Human decision: MODIFIED 
Reason: 
The Reviewer Agent classified missing automated tests for decomposed Unicode and combining marks as SHOULD FIX. However, because CR-01 specifically introduces accent and diacritic normalization into customer search, releasing this feature without regression tests asserting correct handling of decomposed characters (NFD) and rejection of combining-only marks leaves a significant gap in automated verification. The 100% code coverage reported by pytest gave false confidence precisely because these Unicode forms were not tested. For this reason, adding dedicated test coverage for these edge cases is non-negotiable.
Final severity: MUST FIX 
Required action: 
Add parameterized unit tests in `tests/unit/test_search_service.py` covering:
1. Rejection of combining-character-only queries (e.g., `"\u0301\u0301"`) raising `InvalidQueryError`.
2. Rejection of decomposed single characters (e.g., `unicodedata.normalize("NFD", "é")`) raising `InvalidQueryError`.
3. Successful matching of multi-character decomposed queries (e.g., `unicodedata.normalize("NFD", "maría")` matching `"Maria Garcia"`).
Also clean up uncommitted working tree modifications in `scripts/verify_repo.sh`.
 
### RF-03 
Reviewer severity: OPTIONAL 
Human decision: REJECTED / DEFERRED 
Reason: 
The Reviewer Agent flagged in-loop redundant normalization ($2N$ calls to `_normalize_text()` per search) and outdated paths in `docs/REPO_MAP.md`. While caching or pre-computing normalized fields would optimize performance for large datasets, current benchmark execution against the mock repository takes < 1 ms, well below the NFR-01 requirement (< 100 ms). Adding caching or altering repository data structures at this stage introduces premature optimization and unnecessary complexity out of scope for CR-01. Pre-existing documentation drift in `docs/REPO_MAP.md` will be addressed in a future repository maintenance task.
 
## Human Gate 
[X] Return to coder-agent 
[ ] Ready for final re-review 
[ ] Stop / escalate 
