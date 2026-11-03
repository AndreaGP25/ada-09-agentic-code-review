# Requirements - Customer Search 
 
## User Story 
As a user, 
I want to search customers by name or email, 
so that I can quickly find the customer record I need. 
 
## Functional Requirements 
FR-01: The system shall allow searching customers using a text query string that matches against customer name or email address.
FR-02: The search mechanism shall support case-insensitive partial matching (e.g., searching "ana" matches "Ana Maria" and "ana@example.com").
FR-03: The system shall validate input search queries, rejecting queries shorter than 2 characters or containing only whitespace.
FR-04: The system shall return a structured list of matching customer records containing at least ID, name, and email.
FR-05: The system shall return an empty result set with a clear indication when no matching records are found.
FR-06: The system shall gracefully handle invalid inputs by returning descriptive error messages without crashing.
 
## Non-Functional Requirements 
NFR-01: Performance - Search operations against local/in-memory data must execute and return results in less than 100 ms.
NFR-02: Testability - The search logic must achieve at least 90% unit test coverage using automated testing frameworks.
NFR-03: Maintainability - Code structure must decouple the search domain logic from the interface (CLI).
 
## Open Questions 
Q-01: Should the search return a maximum limit of results per query to avoid oversized payloads?
Q-02: Do we need to support exact field filtering (e.g., searching strictly by email field only) in future iterations?
 
## Constraints / Assumptions 
C-01: Constraint - The implementation must rely strictly on in-memory data structures without requiring an external database setup.
A-01: Assumption - Customer records are pre-seeded in memory or loaded from a static mock file (e.g., JSON) at startup.