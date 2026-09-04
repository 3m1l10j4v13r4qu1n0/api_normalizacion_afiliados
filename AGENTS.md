# AGENTS.md

API REST de normalización de afiliados en Python/FastAPI con Clean Architecture + Hexagonal (Ports & Adapters). Responder siempre en español (latino).

## Comandos

- Todo se ejecuta **desde la raíz del repo** (los imports son `app.*`), no desde `app/`.
- Levantar API: `uvicorn app.main:app --reload`
- Migraciones (Alembic ya está inicializado, **no** hacer `alembic init`):
  - `alembic revision --autogenerate -m "descripcion"`
  - `alembic upgrade head`
- Tests unitarios (puros, sin BD): `pytest` desde la raíz. Sanity check: `python -m pytest tests/unit/domian/services -q`
- Seed de datos iniciales: `python -m app.infrastructure.database.seed_runner`

## Setup / gotchas

- `requirements.txt` está en **`app/requirements.txt`** (no en la raíz). El README dice `pip install -r requirements.txt`, pero es inexacto.
- Python fijado a **3.13.5** (`app/.python-version`). No hay venv commitado.
- Config lee variables de entorno via pydantic-settings desde `.env` (ver `app/infrastructure/core/config.py`). Var obligatoria: `DATABASE_URL` (PostgreSQL async, `postgresql+asyncpg://...`).
- **Desincronismo de env de Google Sheets**: el código lee `GOOGLE_SHEETS_ID` y `GOOGLE_CREDENTIALS_PATH` (`google_sheets_client.py`, `dependency_injection.py`), pero `.env.example` define `GOOGLE_SHEET_ID` y `GOOGLE_SERVICE_ACCOUNT_FILE`. Corregir si se va a usar `GET /sync/sheets/import`.
- **`gspread` y `google-auth` no están en `requirements.txt`** aunque `google_sheets_client.py` los importa. Los endpoints de sync fallarán al importar sin instalarlos aparte.
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

## Notas

- `app/domain/models/mapping.py` + `data_key_mapper.py`/`data_transformer.py` manejan el mapeo de columnas de Google Sheets.
- `alembic/env.py` deriva la URL de `settings.DATABASE_URL`, no de `alembic.ini`.
- Commit messages del repo en español, descriptivos (ej. `USECASE: ...`, `DOCUMENTACION: ...`).
- El skill `di-architect-scaffold` en `.agents/skills/` describe **otro proyecto (SGVIR)** — sus reglas de negocio y versiones de Python no aplican aquí directamente.
