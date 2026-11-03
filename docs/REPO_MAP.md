# Repository Map 

## Entry Points 
- src/app.py 
- application bootstrap 
- src/api/ 
- API routes 
- src/domain/ 
- business rules 
- src/storage/ 
- persistence 

## Tests 
- tests/unit/ 
- tests/integration/ 

## Change Guide 
If changing API behavior: 
1. Check REQUIREMENTS.md / SPEC.md 
2. Update src/api/ 
3. Update the domain layer only if business behavior changes 
4. Add or modify tests 
5. Run ./scripts/verify_repo.sh 

## Do Not Edit Directly 
- generated/ 
- .env 
- production configuration 