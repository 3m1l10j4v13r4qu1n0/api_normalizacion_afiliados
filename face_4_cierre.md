# Cierre Fase 4 — Pruebas y Validación

## 1. Objetivo
Dejar constancia de la finalización y validación de la Fase 4 del proyecto
api_normalizacion_afiliados, correspondiente a las pruebas unitarias del dominio
y la calidad del código.

## 2. Alcance de la validación

### Suite de tests unitarios
- Total: **111/111 tests OK** (`pytest -q` desde la raíz)
- Tests desacoplados de `DATABASE_URL` vía `tests/conftest.py` (fallback por defecto)
- Cobertura de dominio: normalización, validación, deduplicación, transformación de datos, mapeo de claves, marcación de errores y exportación

### Archivos de test

| Archivo | Responsabilidad |
|---|---|
| `test_normalizacion.py` | Normalización de datos (RF7/RF8), propagación de domicilio |
| `test_validacion.py` | Validación de campos obligatorios y reglas (RF3/RF4) |
| `test_data_transformer.py` | Transformación de filas crudas del Sheet |
| `test_data_key_mapper.py` | Mapeo de columnas del Sheet a campos del dominio |
| `test_marcar_errores_sheets.py` | Deduplicación y orden de filas con errores (HU-06) |
| `test_exportar_afiliados_sheets.py` | Cálculo de edad, orden alfabético, email opcional (HU-08) |

### Calidad de código
- `ruff check .` — **0 errores** (config: `pyproject.toml`, line-length=100, target py313)
- `black --check .` — **79 archivos formateados**
- Reglas SOLID aplicadas (`.agents/rules/reglas-solid.md`)

## 3. Criterios de validación aplicados
- Cada test aísla el dominio de la infraestructura (FakeRepository / in-memory)
- Tests puros no dependen de `DATABASE_URL` ni de conexión a BD
- Validación de reglas de negocio documentadas en `docs/01_global/reglas_negocio.md`
- Payload de errores verificado (uniforme `{"error": str}`)

## 4. Verificaciones operativas pendientes
Las siguientes verificaciones requieren entorno con base de datos real:

1. Probar `alembic upgrade head` contra PostgreSQL (migración `a1f2b3c4d5e6`)
2. Verificar comportamiento de `GET /afiliados/` con afiliados inactivos (¿filtra o muestra todos?)
3. Probar endpoints de Google Sheets con credenciales reales (`/sync/sheets/import`, `/sync/sheets/export`)
4. Merge de rama `feature/refactorizacion-arquitectonica` → `develop`

## 5. Resultado
Los tests unitarios del dominio fueron validados satisfactoriamente.
El código cumple con los estándares de calidad (ruff + black en verde).

## 6. Estado del proyecto
Fase 4 — Pruebas y validación: **FINALIZADA** (tests unitarios)

Las verificaciones operativas contra BD real quedan pendientes para entorno de integración.
