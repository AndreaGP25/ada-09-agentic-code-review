# Customer Search Feature Specification

## Goal
Provide a reliable, validated, and fast customer search mechanism (via CLI) allowing users to query customer records by partial name or email using in-memory data storage.

## Requirements Covered
- FR-01: Query by name or email
- FR-02: Case-insensitive partial matching
- FR-03: Query validation (minimum length and whitespace handling)
- FR-04: Structured record output (ID, Name, Email)
- FR-05: Empty result handling
- FR-06: Graceful error handling
- NFR-01: Fast execution (< 100 ms execution time)
- NFR-02: Automated test support (>= 90% coverage)
- NFR-03: Clean architecture separation (Decoupled core logic)

## Scope
- In-memory customer repository populated at startup with sample data.
- Core search service module containing input validation, normalization, and filtering logic.
- Basic user interface layer (CLI script) to execute queries.
- Automated unit and integration test suite using `pytest`.

## Out of Scope
- Database persistence (SQL/NoSQL).
- Pagination or advanced sorting of search results.
- Customer creation, update, or deletion (CRUD operations).
- User authentication and authorization.

## Domain Model
```json
Customer {
  "id": "string (UUID or auto-increment integer)",
  "name": "string (non-empty)",
  "email": "string (valid email format)"
}
```

## Search Rules 
- Query Normalization: Strip leading and trailing whitespace from the query term. Convert both the query and target fields to lowercase before comparison
- Field Matching: A customer matches if the query string is a substring of Customer.name OR Customer.email
- Empty Match: If no records match the criteria, return an empty list [] along with a status indicating zero results found.
 
## Validation Rules 
- Minimum Length: The trimmed search query must be at least 2 characters long (e.g., query "a" is invalid)
- Whitespace-only: Queries containing only spaces, tabs, or newlines must be rejected
- Null/Empty Check: Null or missing query parameters must trigger a validation error
 
## Error Handling 
- InvalidQueryError: Raised when a query fails validation rules (e.g., length < 2 or empty).
- User Interface Behavior: Print a friendly error message to standard error (stderr) and exit with status code 1 (or prompt for re-entry).
 
## Acceptance Criteria 
- AC-01: Searching for "ana" returns customers with names like "Ana Silva" and emails like "juliana@example.com".
- AC-02: Search logic is case-insensitive ("ALICE" matches "alice@example.com").
- AC-03: Submitting a single character query (e.g., "a") or blank spaces returns a validation error and does not execute the search.
- AC-04: Valid queries with no matches return an empty list without throwing an exception.
- AC-05: Core search function executes in less than 100 ms for standard mock dataset operations.
- AC-06: Automated unit tests cover edge cases (short strings, whitespace, special characters, no matches) with >= 90% coverage.

## Test Scenarios 
- **TS-01: Successful Partial Match by Name**
  - *Input:* `"mar"`
  - *Expected Result:* Returns records like `"Maria Garcia"` and `"Omar Lopez"`.
- **TS-02: Successful Partial Match by Email**
  - *Input:* `"gmail"`
  - *Expected Result:* Returns all customers with `@gmail.com` addresses. 
- **TS-03: Case Insensitivity Test**
  - *Input:* `"JOHNDOE"`
  - *Expected Result:* Matches `"johndoe@example.com"` or `"John Doe"`.
- **TS-04: No Match Found**
  - *Input:* `"xyz123"`
  - *Expected Result:* Returns an empty list `[]` without errors.
- **TS-05: Validation Failure - Query Too Short**
  - *Input:* `"a"`
  - *Expected Result:* Raises `InvalidQueryError` with message `"Query must be at least 2 characters long"`.
- **TS-06: Validation Failure - Whitespace Only**
  - *Input:* `"   "`
  - *Expected Result:* Raises `InvalidQueryError` with message `"Query cannot be empty or whitespace"`.
- **TS-07: Edge Case - Leading/Trailing Whitespace**
  - *Input:* `"  ana  "`
  - *Expected Result:* Query is automatically trimmed to `"ana"` and returns matching results.

## Constraints 
- **C-01:** No external database or persistent storage system allowed; data must live strictly in-memory.
- **C-02:** Zero external framework heavy dependencies required for core domain logic (plain Python).
- **C-03:** Local environment execution without complex deployment setup.

## Open Questions 
- **Q-01:** How many default sample records should be pre-loaded in the mock repository? (Default proposal: 10-20 records).
- **Q-02:** Should special characters (e.g., `@`, `.`, `-`) in search queries be escaped or stripped prior to matching? 
