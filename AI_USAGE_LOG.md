# AI Usage Log — ADA-08

Este log documenta las decisiones de ingeniería, la supervisión humana y la validación de las respuestas del agente durante la preparación del repositorio Agent-Ready.


### Entrada 1: Auditoría Inicial y Detección de Conocimiento Implícito
* **Etapa:** Auditoría BEFORE & Baseline Definition.
* **Acción realizada:** Se ejecutó la auditoría de 8 dimensiones en `REPOSITORY_READINESS_AUDIT.md` (Puntaje: 40/100). Durante la ejecución BEFORE, el agente tuvo que inferir que el runner de pruebas era `pytest` leyendo la configuración de dependencias, ya que no estaba documentado formalmente.
* **Decisión humana:** Se registró este hallazgo en `results/implicit-knowledge.md` (IK-01) y se decidió que la manera de volver ejecutable este conocimiento implícito era mediante la creación de `AGENTS.md` y el script `verify_repo.sh`.


### Entrada 2: Diseño del Contrato Operativo (`AGENTS.md`)
* **Etapa:** Mejora 1 — Contexto e Instrucciones del Agente.
* **Acción realizada:** Se solicitó al agente una propuesta inicial para la estructura de `AGENTS.md`. El agente sugirió copiar el texto completo de `REQUIREMENTS.md` dentro de `AGENTS.md`.
* **Decisión humana (Rechazo/Modificación):** Se rechazó la duplicación de requisitos para evitar crear una "segunda fuente de verdad". En su lugar, se configuró `AGENTS.md` únicamente como un índice que apunta a `REQUIREMENTS.md` y `SPEC.md` como las fuentes primarias de verdad, definiendo únicamente comandos estándar y Stop Conditions.


### Entrada 3: Implementación de Guardrails Deterministas
* **Etapa:** Mejora 4 y 5 — Guardrails y Verificación Reproducible.
* **Acción realizada:** Se diseñó el script `scripts/check_repo_contract.py` para validar la presencia de archivos clave del repositorio (`AGENTS.md`, `REPO_MAP.md`, etc.) y se integró dentro de `scripts/verify_repo.sh`.
* **Decisión humana:** Se convirtió la regla natural de *"no romper la estructura del repositorio"* en un check automatizado con código de salida `0` (exitoso) o `1` (fallido), asegurando que tanto el desarrollador como el agente y la integración continua (CI) ejecuten exactamente el mismo contrato.


### Entrada 4: Evaluación de la Ejecución AFTER
* **Etapa:** Ejecución AFTER & Comparación de Procesos.
* **Acción realizada:** Se inició una sesión limpia con el mismo prompt oficial en la rama `feature/after-improvements`. El agente leyó `AGENTS.md`, inspeccionó `REPO_MAP.md`, realizó la modificación solicitada en `src/services/search_service.py` y ejecutó por iniciativa propia `bash scripts/verify_repo.sh`.
* **Decisión humana:** Se verificó que el agente no cometió errores de comandos ni realizó preguntas de aclaración. Se confirmó que el resultado de las pruebas unitarias y el contrato del proyecto retornaron `PASS`.


### Entrada 5: Evaluación Final y Limites de la Automatización
* **Etapa:** Auditoría AFTER & Reflexión Final.
* **Acción realizada:** Se completó la tabla AFTER en `REPOSITORY_READINESS_AUDIT.md` alcanzando un puntaje de 94/100 (Delta: +54 puntos).
* **Decisión humana:** Se analizó qué parte del proceso aún requiere supervisión humana. Se concluyó que, aunque el agente puede ejecutar pruebas y validar el contrato de forma autónoma, la decisión de modificar arquitectura de alto nivel o la aprobación final de un Pull Request sigue requiriendo un *Human Gate* obligatorio.