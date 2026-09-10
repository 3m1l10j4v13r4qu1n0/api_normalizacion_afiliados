# AGENTS.md

API REST de normalización de afiliados en Python/FastAPI con Clean Architecture + Hexagonal (Ports & Adapters). Responder siempre en español (latino).

## Idioma y tono

- Responder siempre en español rioplatense, informal ("vos"). Nunca en inglés,
  aunque el código, logs o skills estén en inglés.

## Comandos

- Todo se ejecuta **desde la raíz del repo** (los imports son `app.*`), no desde `app/`.
- Levantar API: `uvicorn app.main:app --reload`
- Migraciones (Alembic ya está inicializado, **no** hacer `alembic init`):
  - `alembic revision --autogenerate -m "descripcion"`
  - `alembic upgrade head`
- Tests unitarios (puros, sin BD): `pytest` desde la raíz. Sanity check: `python -m pytest tests/unit/domian/services -q`
- Seed de datos iniciales: `python -m app.infrastructure.database.seed_runner`
- Lint y formato antes de cada commit:
  - `venv/bin/ruff check .`
  - `venv/bin/black --check .`
  - `venv/bin/python -m pytest -q`

## Setup / gotchas

- `requirements.txt` está en **`app/requirements.txt`** (no en la raíz). El README dice `pip install -r requirements.txt`, pero es inexacto.
- Python fijado a **3.13.5** (`app/.python-version`). No hay venv commitado.
- Config lee variables de entorno via pydantic-settings desde `.env` (ver `app/infrastructure/core/config.py`). Var obligatoria: `DATABASE_URL` (PostgreSQL async, `postgresql+asyncpg://...`).
- **Env de Google Sheets**: el código lee `GOOGLE_SHEETS_ID` y `GOOGLE_CREDENTIALS_PATH` (`config.py`, `google_sheets_client.py`), alineado con `.env.example`.
- **`gspread` y `google-auth`** están listados en `app/requirements.txt` (necesarios para los endpoints de sync).
- El pipeline de importación es un **UC único** (`ImportarAfiliadoUseCase` en `core_importar_afiliado.py`) que usa el servicio de dominio puro `importacion_pipeline.procesar_fila`; ya no hay wrappers `uc1a/uc1b/uc4`. La lectura del Sheet vive en `uc4a_importar_afiliado.py` (`ImportSheetUseCase`).
- Tests puros desacoplados de `DATABASE_URL` vía `tests/conftest.py` (fallback por defecto).
- La base usa SQLAlchemy 2.0 async (`AsyncSession`, `asyncpg`). `get_db()` en `connection.py` hace **commit automático al finalizar el request** — los casos de uso no deben commitear.

## Arquitectura

Capas (regla: el dominio no importa frameworks):

- `app/domain/` — entidades puras, servicios y **ports** (contratos). `exceptions.py` define excepciones de dominio (`DatoInvalidoError`, `AfiliadoNoEncontradoError`, etc.).
- `app/application/use_cases/` — casos de uso (nombres `ucN_*`). Reciben ports, no implementaciones concretas.
- `app/infrastructure/` — adapters: ORM + repositorios en `database/`, Google en `google/`, y el wiring en `dependencies/dependency_injection.py`.
- `app/presentation/` — routers FastAPI (`afiliados.py`, `sync.py`), schemas Pydantic, y `handlers.py` para traducir excepciones de dominio a HTTP.

Convenciones:

- Todo caso de uso nuevo debe cablearse en `dependency_injection.py` (función `get_*` con `Depends(get_db)`) e inyectarse en el router con `Depends`.
- Excepciones de dominio se mapean a HTTP solo en `handlers.py`; no usar `try/except` de negocio en routers/use cases.
- Tests unitarios usan `FakeRepository`/in-memory para aislar el dominio, sin BD (ver `tests/unit/domian/`; la carpeta se llama `domian` — tipeo original).
- Reglas SOLID aplicadas al escribir código Python: ver `.agents/rules/reglas-solid.md`.

## Flujo de implementación (reglas duras)

### Al recibir una tarea

1. **Leer `docs/estado_actual_proyecto.md`** completo antes de tocar código.
2. **Verificar** que la funcionalidad no exista ya (leer código relevante, no asumir).
3. **Planificar** en pasos chicos (un caso de uso, un endpoint, o un componente por vez).
4. **Preguntar** ante ambigüedad; no decidir por cuenta propia.

### Al escribir código

- **Un archivo = una responsabilidad** (SRP). No mezclar persistencia, dominio y transporte.
- **Ports chicos y específicos**: preferir varios puertos pequeños antes de uno gordo con métodos que nadie usa.
- **Dominio puro**: `app/domain/` NO importa FastAPI, SQLAlchemy, Pydantic ni gspread.
- **Inyección de dependencias**: cablear en `dependency_injection.py` con `Depends`, nunca instanciar adapters dentro de casos de uso.
- **Releer después de escribir**: verificar que el archivo quedó como se planeó.
- **Trabajo en pasos chicos**: mostrar qué se hizo y qué falta antes de seguir.

### Al commitear

- **Conventional Commits en español**, scope en minúscula:
  - `feat(domain): se agrega puerto SheetExportPort`
  - `fix(sync): se corrige filtrado de afiliados inactivos`
  - `test(usecase): se agrega test de UC8`
- **Un tema por commit** (commits atómicos). Si necesita "y", son dos commits.
- **Prohibido** mensajes vagos ("cambios", "update", "cosas varias").
- **Checklist** antes de commit:
  ```bash
  venv/bin/ruff check .
  venv/bin/black --check .
  venv/bin/python -m pytest -q
  ```

### Flujo de ramas y merges (regla dura: `.agents/rules/flujo-git.md`)

- **Prohibido** trabajar directo sobre `main` o `develop`.
- Crear `feature/<tema>` o `fix/<tema>` **siempre desde `develop`**.
- Una rama = una tarea/HU coherente. Mantener ramas cortas.
- **Antes de mergear a develop**:
  1. Integrar `origin/develop` dentro de la rama feature (`git fetch` + `git merge origin/develop`) y resolver conflictos ahí.
  2. Checklist en verde: `ruff check` · `black --check` · `pytest`.
  3. Solo entonces mergear a develop.
- **Push/merge SOLO con aprobación explícita del usuario**.

### Versionado por fases (regla dura: `.agents/rules/versionado-fases.md`)

- **Tag anotado** al cerrar cada fase, **no** push por ahora.
- Versión semver: cada fase incrementa la versión menor (`v1.0.0` → `v1.1.0` → `v1.2.0`).
- **Nunca** push de rama o tag sin aprobación explícita del usuario.
- Si una fase se corrige después del tag, versionar con patch (`vX.Y.Z+1`).

## Reglas de verificación y anti-alucinación (`.agents/rules/Reglas-anti-alucinacion.md`)

- **Verificar antes de afirmar**: leer el archivo/símbolo en la sesión actual, no asumir de memoria.
- **No inventar superficie de código**: nombres de clases, métodos, rutas, endpoints — solo si se vieron en código real o se marcan como "nuevo, a crear".
- **No inventar dependencias**: solo citar librerías verificadas en `requirements.txt`.
- **Ambigüedad → pregunta**: no decidir por cuenta propia.
- **Confirmación explícita en cambios transversales**: cambios que toquen más de una HU requieren OK del usuario.
- **Reporte de cada paso**: 1) qué se verificó, 2) qué se propone/cambió, 3) qué queda pendiente.

## Fuente de verdad

- `docs/` es la única fuente de verdad para requerimientos, especificaciones y reglas de negocio.
- No inventar endpoints, campos, tipos, textos ni contenido institucional.
- Si el código real contradice `docs/estado_actual_proyecto.md`, avisar antes de asumir cuál es la fuente.

## Notas

- `app/domain/models/mapping.py` + `data_key_mapper.py`/`data_transformer.py` manejan el mapeo de columnas de Google Sheets.
- `alembic/env.py` deriva la URL de `settings.DATABASE_URL`, no de `alembic.ini`.
- El skill `di-architect-scaffold` en `.agents/skills/` define el flujo de 6 pasos para implementar casos de uso/HUs en este proyecto (ya adaptado; originalmente describía otro proyecto).
- El skill `rest-api-design` (instalado de `aj-geddes/useful-ai-prompts`) tiene una guía local: `.agents/skills/rest-api-design/references/fastapi-conventions.md` + template `templates/endpoint_fastapi.py` (mapeo de status codes por excepción de dominio, naming vigente, convenciones REST para endpoints nuevos).

## Historias de Usuario — Estado verificado (auditoría 2026-09-10)

| HU | Descripción | Estado | Notas |
|---|---|---|---|
| HU-01 | Importar lista de afiliados (lotes) | ✅ | POST `/afiliados/import`, UC1a en `core_importar_afiliado.py` |
| HU-02 | Registrar afiliado individual | ✅ | POST `/afiliados/`, UC1b en `core_importar_afiliado.py` |
| HU-03 | Consultar afiliados (listado y por ID) | ✅ | GET `/afiliados/` y GET `/afiliados/{id}`, UC2 |
| HU-04 | Modificar datos de afiliado | ✅ | PATCH `/afiliados/{id}`, UC3 |
| HU-05 | Importar desde Google Sheets | ✅ | POST `/sync/sheets/import`, UC4a+UC4 (requiere credenciales reales) |
| HU-06 | Marcar filas con errores en Sheets | ✅ | `SheetMarkingPort` + `SheetsMarkingAdapter` + UC6, integrado en `POST /sync/sheets/import` (fondo rojo en batch) |
| HU-07 | Dar de baja afiliado | ✅ | DELETE `/afiliados/{id}`, UC5 (baja lógica, `id_estado_afiliado=2`) |
| HU-08 | Generar tabla de afiliados en Sheets | ✅ | `SheetExportPort` + `SheetsExportAdapter` + UC8, `POST /sync/sheets/export` (edad dinámica, solo activos) |

Leyenda: ✅ verificado en sesión | 🟡 parcial | 🔵 pendiente externo/no implementado | ⏳ en proceso

## Pendientes de implementación

Verificaciones operativas pendientes:
- Probar `alembic upgrade head` contra BD real
- Verificar si `GET /afiliados/` filtra inactivos o muestra todos

2. **Verificaciones operativas**:
   - Probar `alembic upgrade head` contra BD real
   - Verificar si `GET /afiliados/` filtra inactivos o muestra todos
   - Merge rama `feature/refactorizacion-arquitectonica` → `develop`

## Memoria del proyecto (docs/estado_actual_proyecto.md y docs/vitacora_agentica.md)

- Antes de tocar código, leer `docs/estado_actual_proyecto.md` completo para tener el contexto actual del proyecto.
- Al terminar una implementación, eliminación o edición relevante (nueva entidad, caso de uso, endpoint, refactor de arquitectura, dependencia core):
  1. Actualizar la sección correspondiente de `docs/estado_actual_proyecto.md` (editar in-place, no reescribir todo el archivo).
  2. Agregar una entrada nueva al final de `docs/vitacora_agentica.md` con: fecha, qué se hizo, decisiones tomadas, archivos tocados y estado resultante. Nunca editar entradas previas de la vitácora.
- No generar entradas de vitácora por cambios triviales (typos, formateo, renames cosméticos).
- Si el código real contradice lo que dice `estado_actual_proyecto.md`, avisar antes de asumir cuál es la fuente de verdad.
