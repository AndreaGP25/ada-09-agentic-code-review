# Agent Instructions 
 
## Read First 
1. REQUIREMENTS.md 
2. SPEC.md 
3. ARCHITECTURE.md 
4. TASKS.md 
5. docs/REPO_MAP.md  

# Sources of Truth 
- Requirements live only in REQUIREMENTS.md. 
- Verifiable behavior lives in SPEC.md. 
- Do not change requirements/spec merely to make tests pass. 

## Repository Map
- src/        implementation 
- tests/      automated tests 
- docs/       architecture and operational context 
- scripts/    deterministic checks 
- results/    generated evidence
 
## Standard Commands 
Install: ... 
Run: ... 
Test: ... 
Lint: ... 
Verify: ./scripts/verify_repo.sh 

## Change Rules 
- Keep changes scoped to the requested task. 
- Do not weaken existing tests. 
- Do not introduce new dependencies without justification. 
- Do not modify secrets or generated files. 

## Stop Conditions 
Stop and ask for human input when: 
- requirements conflict, 
- a destructive action is required, 
- an architecture boundary must change, 
- a required external system is unavailable. 
 
## Definition of Done 
- Relevant tests pass. 
- Acceptance criteria are covered. 
- No unrelated files are changed. 
- Documentation reflects final behavior.