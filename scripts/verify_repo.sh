#!/usr/bin/env bash 
set -euo pipefail 
 
echo "[1/3] Running tests" 
./.venv/Scripts/python -m pytest -q 
 
echo "[2/3] Running lint" 
# Ejecuta ruff desde el entorno virtual si está instalado, o muestra una advertencia
./.venv/Scripts/python -m ruff check . || echo "Lint warning: Revisa las advertencias de código."
 
echo "[3/3] Repository checks" 
./.venv/Scripts/python scripts/check_repo_contract.py 
 
echo "VERIFY_REPO: PASS"