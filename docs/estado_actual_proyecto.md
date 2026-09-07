# Estado Actual del Proyecto

> Última actualización: 2026-09-07
> Este archivo es una FOTO del presente, no un historial. Para el historial de cambios ver `vitacora_agentica.md`.
> El agente debe leer este archivo completo al iniciar cualquier tarea sobre el proyecto.

## 1. Resumen del proyecto

API REST en Python/FastAPI para la normalización, validación y gestión de datos de afiliados de un sindicato. Actúa como capa intermedia entre fuentes externas (importación manual, Google Sheets y scripts clientes) y los sistemas de consulta. Stack: FastAPI + SQLAlchemy 2.0 async (asyncpg) + pydantic-settings, Python 3.13.5 (`app/.python-version`, venv en `./venv`). Rama activa: `feature/refactorizacion-arquitectonica`.

## 2. Arquitectura

Clean Architecture + Hexagonal (Ports & Adapters). El dominio no importa frameworks.

- `app/domain/` — entidades puras (dataclasses), servicios y **ports** (contratos `ABC` + `abstractmethod`). `exceptions.py` define excepciones de dominio.
- `app/application/use_cases/` — casos de uso `ucN_*.py` (clase `...UseCase` con `async def execute`), reciben ports, no implementaciones.
- `app/infrastructure/` — adapters: ORM + repositorios en `database/`, Google en `google/`, wiring en `dependencies/dependency_injection.py`.
- `app/presentation/` — routers FastAPI (`afiliados.py`, `sync.py`), schemas Pydantic y `handlers.py` (mapea excepciones de dominio → HTTP, payload `{"error": str(exc)}`).

Convenciones: todo caso de uso nuevo se cablea en `dependency_injection.py` y se inyecta con `Depends`; las excepciones de dominio solo se traducen en `handlers.py`; `get_db()` hace commit automático al finalizar el request (los casos de uso no commitean).

## 3. Entidades / Modelos de dominio

- `Afiliado` — datos normalizados del afiliado (apellido, nombre, dni, numero_legajo, fecha_nacimiento, email, valores controlados vía FK).
- `InputRow` — fila intermedia de lectura de Google Sheets (con `row_number` y `value`).
- `SheetRawData` — estructura de lectura de la hoja (encabezados + datos).
- `Importacion` — registro de un proceso de importación.
- `ErrorValidacion` — error de validación por registro/campo, asociado a `row_number`.
- `Dominio` — enum puro que identifica las tablas de valores controlados (GENERO, ESTADO_CIVIL, NIVEL_EDUCATIVO, RELACION_DEPENDENCIA, ESTADO_AFILIADO). Se inyecta al port `DominioRepositoryPort` en lugar de la clase ORM.
- Valores controlados (tablas de dominio en BD vía seed): estado afiliado, género, estado civil, nivel educativo, relación de dependencia.

## 4. Casos de uso / Servicios implementados

- [x] UC1a — importar afiliados por archivo (HU-01)
- [x] UC1b — registrar afiliado manual (HU-02)
- [x] UC2 — consultar afiliados, listado y por ID (HU-03)
- [x] UC3 — actualizar afiliado (HU-04)
- [x] UC4a/4b — importar desde Google Sheets + marcar errores en la hoja (HU-05/06, requiere `gspread`/`google-auth`)
- [x] UC5 — dar de baja afiliado (HU-07)
- [ ] UC6 — generar tabla en Google Sheets (HU-08, endpoint comentado en router)

## 5. Endpoints / Interfaces expuestas

| Método | Ruta | Descripción | Estado |
|---|---|---|---|
| POST | `/afiliados/import` | Importar afiliados por archivo (UC1a) | ✅ |
| POST | `/afiliados/` | Registrar afiliado manual (UC1b) | ✅ |
| GET | `/afiliados/` | Listar afiliados (UC2) | ✅ |
| GET | `/afiliados/{afiliado_id}` | Obtener afiliado por ID (UC2) | ✅ |
| PATCH | `/afiliados/{afiliado_id}` | Actualizar afiliado (UC3) | ✅ |
| DELETE | `/afiliados/{afiliado_id}` | Dar de baja afiliado (UC5) | ✅ |
| POST | `/sync/sheets/import` | Importar desde Google Sheets (UC4) | ⚠️ requiere deps |
| POST | `/sync/sheets/export` | Generar tabla en Sheets (UC6) | ❌ comentado |

## 6. Infraestructura / Integraciones

- PostgreSQL async (`DATABASE_URL`, var obligatoria; Alembic inicializado, `alembic upgrade head`).
- Google Sheets (`gspread` + `google-auth`): el código usa `GOOGLE_SHEETS_ID` y `GOOGLE_CREDENTIALS_PATH`, pero `.env.example` define `GOOGLE_SHEET_ID` y `GOOGLE_SERVICE_ACCOUNT_FILE`. **Desincronismo a corregir** antes de usar `GET /sync/sheets/import`.
- `requirements.txt` en `app/requirements.txt` (no en la raíz). `gspread`/`google-auth` NO están listados.
- Seed de datos iniciales: `python -m app.infrastructure.database.seed_runner`.

## 7. Pendientes / TODO conocidos

1. Agregar `gspread` y `google-auth` a `app/requirements.txt` y unificar nombres de env de Google Sheets (HU-05/06/08).
2. Activar e implementar `POST /sync/sheets/export` (HU-08).
3. Arreglar `tests/unit/domian/services/test_data_transformer.py`: `ImportError: cannot import name 'SheetRow'` (test desactualizado, preexistente). Suite: 86 tests OK, 1 falla.
4. Mantener migraciones de Alembic al día con el modelo.
5. Revisar semántica de baja lógica (seed: 1=Activo, 2=Inactivo).

## 8. Decisiones y convenciones vigentes

- Comandos siempre desde la raíz del repo (imports `app.*`, nunca desde `app/`); no repetir `alembic init`.
- `docs/` en formato Benn backend-only: `01_global`, `02_tecnico` (con `diagramas/`), `03_procesos`, `04_historias_usuario/HU-01..HU-08` (5 archivos c/u), `07_metodologia_agil`. No hay carpetas `05_mockups/` ni `06_uso_ia/`.
- Commit messages en español, descriptivos, con prefijo MAYÚSCULAS (ej. `USECASE: ...`, `DOCUMENTACION: ...`); commits atómicos por unidad lógica.
- El skill `di-architect-scaffold` describe el flujo de 6 pasos para implementar HUs (ya adaptado a este proyecto).
- Reglas SOLID para escribir código Python: `.agents/rules/reglas-solid.md` (misma matriz que `.opencode/rules/reglas-solid.md` del frontend web_ifts12).
- Skill `rest-api-design` adaptado a este repo: guía local en `references/fastapi-conventions.md` (mapeo status codes por excepción de dominio, naming vigente) + template `templates/endpoint_fastapi.py`. Inconsistencia detectada: `ImportacionError` usa payload anidado, el resto `{"error": str}`.
- `.agents/skills/pdf-to-markdown` y `virtualizacion`... no aplican como convención de producto; el skill `apa-software-doc`/`apa-formato` son plantillas de documentación.
- Al terminar trabajo relevante, actualizar este archivo (in-place) y agregar entrada a `vitacora_agentica.md` (append-only).