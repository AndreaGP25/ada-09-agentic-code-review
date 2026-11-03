from pathlib import Path 
import sys 

required = [ 
    "AGENTS.md", 
    "README.md", 
    "REQUIREMENTS.md", 
    "SPEC.md", 
    "ARCHITECTURE.md", 
    "TASKS.md", 
    "docs/REPO_MAP.md", 
] 

missing = [path for path in required if not Path(path).exists()] 

if missing: 
    print("REPO_CONTRACT: FAIL") 
    for path in missing: 
        print(f"Missing: {path}") 
    sys.exit(1) 
    
print("REPO_CONTRACT: PASS") 
sys.exit(0) 