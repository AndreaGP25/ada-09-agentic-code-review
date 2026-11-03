 ## IK-01 

What: 
Los archivos fuente del repositorio utilizan terminaciones de línea Windows CRLF (`\r\n`). Las operaciones de edición basada en texto exacto o reemplazos de bloques fallan si asumen LF (`\n`). 

How was it discovered: 
Una llamada a `edit_file` en `src/services/search_service.py` falló al no encontrar la cadena exacta. Al inspeccionar el archivo en binario (`repr(f.readline())`), se constató que usaba `\r\n`. 

Should this remain implicit? 
NO 

Where should it become explicit? 
AGENTS.md / .gitattributes 

Risk: 
Herramientas de edición automática o parches de agentes pueden fallar al modificar archivos existentes o introducir terminaciones mixtas. 



## IK-02 

What: 
El entorno de ejecución y pruebas depende del entorno virtual local ubicado en `.venv` (`.venv\Scripts\python` o `.venv/bin/python`), el cual contiene `pytest` y `pytest-cov`. 

How was it discovered: 
Al inspeccionar el árbol de directorios con `dir` y verificar la configuración de pytest con plugins instalados. 

Should this remain implicit? 
NO 

Where should it become explicit? 
AGENTS.md (sección "Validation") / scripts/verify_repo.ps1 

Risk: 
Un agente puede intentar invocar el `python` global del sistema, arriesgando fallos por dependencias faltantes o versiones no ￹coincidentes. 



## IK-03 

What: 
Existe un umbral estricto de cobertura mínima del 90.0% (`fail_under ￹= 90`) configurado en `.coveragerc`, que evalúa tanto ramas como ￹sentencias (`branch = True`). 

How was it discovered: 
Al ejecutar `pytest --cov=src --cov-report=term-missing` y revisar la ￹salida del plugin `pytest-cov`. 

Should this remain implicit? 
NO 

Where should it become explicit? 
AGENTS.md / README.md (sección de Testing) 

Risk: 
Un agente podría agregar código con tests que cubran solo el camino ￹feliz y reprobar la suite si la cobertura desciende por debajo de ￹90%. 



## IK-04 

What: 
En validación de longitud de caracteres unicode, caracteres con ￹diacríticos descompuestos (NFD, ej. `"a\u0301"`) tienen `len == 2` en ￹Python pero representan un único carácter visible. 

How was it discovered: 
Al analizar el reporte de cobertura de ramas en ￹`src/services/search_service.py` donde la condición ￹`len(normalized_query) < 2` no se cubría con caracteres precompuestos ￹(NFC). 

Should this remain implicit? 
NO 

Where should it become explicit? 
SPEC.md (Validation Rules) / ARCHITECTURE.md 

Risk: 

Consultas de un solo carácter descompuesto podrían eludir la ￹validación mínima de longitud si solo se valida `len(trimmed_query)`. 

Remediation: 
SPEC.md especificando que la validación de longitud mínima (>= 2) ￹aplica sobre la representación normalizada del texto. 