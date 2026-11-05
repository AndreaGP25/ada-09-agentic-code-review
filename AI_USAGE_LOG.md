# AI Usage Log — ADA-09 (Agentic Code Review · CR-01)

Este log documenta las decisiones de ingeniería, la supervisión humana y la interacción humano-agente durante el ciclo completo de review de la rama `ada09/cr-01` (Change Request CR-01: normalización de tildes y diacríticos en la búsqueda de clientes).

---

### Entrada 1 — Definición y refinamiento del Change Request

**Etapa:** Definición de CR-01 / `CHANGE_REQUEST.md`  
**Fecha:** 03/11/2026  
**Agente involucrado:** Coder Agent  
**Acción realizada:** Se solicitó al Coder Agent la formalización del Change Request para CR-01. El agente propuso inicialmente aplicar la normalización NFD también sobre los datos almacenados en `InMemoryCustomerRepository` (modificando los registros en memoria al momento de cargarlos) como estrategia de optimización para reducir llamadas a `_normalize_text` durante la búsqueda.  
**Decisión humana (Rechazo/Modificación):** Se rechazó la modificación de los registros almacenados porque violaba el principio de inmutabilidad de los datos del dominio establecido en `ARCHITECTURE.md` ("Customer instances are immutable dataclasses; underlying records stored in InMemoryCustomerRepository must not be mutated during normalization or search"). Se acordó que la normalización debe aplicarse únicamente en tiempo de evaluación durante la búsqueda, sin alterar los objetos `Customer` del repositorio.  
**Resultado:** `CHANGE_REQUEST.md` creado con el alcance correcto. Los registros del repositorio permanecen sin modificación.

---

### Entrada 2 — Plan del Coder Agent y decisión humana sobre el plan de implementación

**Etapa:** Plan de implementación (pre-commit `1ed6627`)  
**Fecha:** 03/11/2026  
**Agente involucrado:** Coder Agent  
**Acción realizada:** El Coder Agent presentó un plan de implementación en 7 pasos: (1) leer documentación de proyecto, (2) implementar `_normalize_text` usando `unicodedata` NFD + filtrado de categoría `Mn`, (3) aplicar normalización al query y a los campos `name`/`email` de cada cliente durante el filtrado, (4) preservar la secuencia de validación existente (trim → longitud ≥ 2 → no-whitespace) antes de la normalización, (5) agregar pruebas unitarias y de integración para todos los casos de uso de CR-01, (6) ejecutar linter, cobertura y verificación de contrato, y (7) registrar evidencia en `coder-report.md`.  
**Decisión humana (Aprobación):** El plan fue aprobado en su totalidad. Se validó que la dependencia elegida (`unicodedata`) es parte de la biblioteca estándar de Python, que no se requería ninguna dependencia externa nueva, y que el flujo de validación previa a la normalización era compatible con los requisitos de FR-03 y AC-03. El Coder Agent procedió con la implementación.  
**Resultado:** Implementación inicial completa en commit `1ed6627 feat: implement CR-01`. Suite con 54 pruebas, cobertura 100.00%.

---

### Entrada 3 — Implementación: sugerencia del agente aceptada (orden de validación post-normalización)

**Etapa:** Fix Cycle post-revisión (commit `627b9b6`)  
**Fecha:** 03/11/2026  
**Agente involucrado:** Coder Agent  
**Acción realizada:** Durante el fix cycle posterior a la revisión humana, el Coder Agent propuso dos variantes para resolver RF-01:
- **Variante A (propuesta por el agente):** Agregar dos guards *después* de `_normalize_text(trimmed_query)`: primero verificar que `normalized_query` no sea vacío, y luego verificar que `len(normalized_query) >= 2`. El agente argumentó que este orden permite mensajes de error diferenciados y exactos: `"Query cannot be empty or whitespace"` para queries que colapsan a cadena vacía, y `"Query must be at least 2 characters long"` para queries que colapsan a un solo carácter.
- **Variante B:** Reutilizar un único guard con lógica combinada (`if not normalized_query or len(normalized_query) < 2`), simplificando el código a expensas de un mensaje de error genérico.

**Decisión humana (Aceptación de Variante A):** Se aceptó la Variante A por dos razones: (1) los mensajes de error diferenciados son directamente trazables a los escenarios de prueba TS-05 y TS-06 en `SPEC.md`, y (2) los tests unitarios existentes en `test_validation.py` asumen mensajes específicos, por lo que la Variante B habría requerido debilitar esos tests.  
**Resultado:** Guards post-normalización implementados en `src/services/search_service.py:56-62` con mensajes exactos alineados a la especificación.

---

### Entrada 4 — Reviewer Agent: finding relevante y evidencia (RF-01)

**Etapa:** Independent Code Review (commit `1ed6627`)  
**Fecha:** 03/11/2026  
**Agente involucrado:** Reviewer Agent (Antigravity, independiente, solo lectura)  
**Finding reportado (RF-01 — MUST FIX):**  
El Reviewer Agent identificó que `CustomerSearchService.search()` validaba la longitud del query *antes* de la normalización de diacríticos, creando dos vectores de bypass:
1. Query `"\u0301\u0301"` (dos combining marks, `len = 2`): supera el guard `len >= 2`, se llama `_normalize_text()`, que filtra todos los caracteres de categoría `Mn`, produciendo una cadena vacía `""`. La evaluación `"" in _normalize_text(customer.name)` retorna `True` para **todos** los clientes, exponiendo los 12 registros completos del repositorio.
2. Query `"e\u0301"` (carácter base + combining mark, `len = 2`, forma NFD de `"é"`): supera el guard `< 2`, normaliza a `"e"` (longitud 1), ejecuta una búsqueda de un solo carácter retornando 11 registros, mientras que la forma precompuesta `"é"` (NFC, `len = 1`) es correctamente rechazada con `InvalidQueryError`.

**Evidencia citada:** Fragmento de código `src/services/search_service.py:49-66` (commit `1ed6627`), trazabilidad a FR-03 ("rejecting queries shorter than 2 characters"), FR-05 ("return an empty result set"), y AC-03.  
**Resultado:** Finding clasificado MUST FIX, incluido en `results/review-report.md`. Enviado a Human Review Gate.

---

### Entrada 5 — Human Review: finding RF-02 modificado de SHOULD FIX a MUST FIX

**Etapa:** Human Review Gate  
**Fecha:** 03/11/2026  
**Agente involucrado:** Revisora: Andrea Góngora (Human Reviewer)  
**Finding evaluado (RF-02):** El Reviewer Agent clasificó RF-02 como SHOULD FIX: la suite de pruebas reportaba 100% de cobertura, pero todos los tests de CR-01 usaban exclusivamente caracteres precompuestos NFC, sin ningún caso de prueba para caracteres descompuestos NFD ni para combining marks aislados. Esto significaba que la cobertura del 100% era una métrica de falsa confianza que enmascaraba los defectos reportados en RF-01.  
**Decisión humana (Modificación a MUST FIX):** Se elevó la severidad a MUST FIX. Razonamiento: CR-01 introduce específicamente normalización de diacríticos, y liberar la feature sin pruebas automatizadas que validen el comportamiento bajo las mismas formas Unicode que el código procesa (NFD, combining marks) contradice directamente el criterio de aceptación AC-06 ("Automated unit tests covering edge cases and special characters with >= 90% coverage"). La cobertura de línea no substituye la cobertura semántica de casos de borde Unicode.  
**Acción requerida definida por Human Reviewer:** Agregar tests parametrizados en `tests/unit/test_search_service.py` para: (1) rechazo de combining-only marks, (2) rechazo de single-char descompuesto NFD, (3) match correcto de multi-char descompuesto NFD. Limpiar working tree de `scripts/verify_repo.sh`.  
**Resultado:** Decisiones documentadas en `results/human-review-decisions.md`. Coder Agent devuelto al fix cycle.

---

### Entrada 6 — Fix cycle y re-review: qué cambió y cómo fue verificado

**Etapa:** Fix Cycle (commit `627b9b6`) + Independent Re-Review  
**Fecha:** 03/11/2026 – 04/11/2026  
**Agentes involucrados:** Coder Agent (fix) → Reviewer Agent (re-review, solo lectura)  
**Cambios implementados en fix cycle:**  
- `src/services/search_service.py`: Dos guards post-normalización añadidos en líneas 57-61. Cobertura de ramas verificada al 100%.  
- `tests/unit/test_search_service.py`: Tres funciones de test parametrizadas añadidas (líneas 256-309), totalizando 12 nuevas ejecuciones de prueba: `test_search_combining_characters_only_raises_invalid_query_error` (4 casos), `test_search_decomposed_single_character_query_raises_invalid_query_error` (5 casos), `test_search_decomposed_multicharacter_query_matches` (3 casos).  
- `scripts/verify_repo.sh`: Working tree limpiado; el script ejecuta determinísticamente en bash sin modificaciones pendientes.

**Resultados del fix cycle:** 66 tests passed (0 failures), 100.00% statement y branch coverage, `ruff check .` limpio, `REPO_CONTRACT: PASS`, `VERIFY_REPO: PASS`.

**Re-review (Reviewer Agent, independiente, solo lectura):**  
- **RF-01:** RESOLVED. Guards post-normalización verificados operacionalmente — query `"\u0301\u0301"` retorna exit code 1 con `"Error: Query cannot be empty or whitespace"`, query `"e\u0301"` retorna exit code 1 con `"Error: Query must be at least 2 characters long"`. Ningún registro expuesto.  
- **RF-02:** RESOLVED. 12 nuevos tests automatizados cubren los 3 escenarios requeridos. Working tree limpio confirmado con `git status`.  
- **RF-03 (DEFERRED):** Sin cambios en scope; deferred se mantiene conforme decisión humana.  
- **Nuevas regresiones MUST FIX:** Ninguna detectada.  
- **Recomendación final del Reviewer Agent:** `[X] READY FOR HUMAN REVIEW / MERGE`.  
**Resultado:** `results/re-review-report.md` generado. `results/PR_EVIDENCE.md` creado como evidencia integral del ciclo completo.
