# Aplicación de REST design en este proyecto (FastAPI + Clean Architecture)

> Guía local para aplicar las buenas prácticas del skill a `api_normalizacion_afiliados`.
> Fuente de verdad: `app/presentation/routers/*.py`, `app/presentation/schemas/*.py`, `app/presentation/handlers.py`.

## Convenciones vigentes del repo

- **Prefijo**: los routers NO llevan `/api` ni `/v1` (se montan directo). Si en el futuro se versiona, usar URL path versioning (`/api/v1/...`), la opción recomendada por el skill.
- **Recursos**: sustantivos en plural, snake_case en campos: `/afiliados`, `/afiliados/{afiliado_id}`. Máx. 2 niveles de anidamiento.
- **Excepción justificada a "no verbs"**: `/sync/sheets/import` (y futuro `/export`) son acciones de sincronización, no CRUD de un recurso.
- **Métodos** (según resource-naming):
  - `GET /afiliados` → listar; `GET /afiliados/{id}` → obtener.
  - `POST /afiliados` → crear; `POST /afiliados/import` → acción de carga masiva.
  - `PATCH /afiliados/{id}` → actualización parcial (no `PUT`).
  - `DELETE /afiliados/{id}` → baja lógica (200 OK con confirmación, no 204, por decisión actual).
- **Fechas**: ISO 8601 (`YYYY-MM-DD` para `date`, con hora para timestamps).

## Status codes (mapeo por excepción de dominio → `handlers.py`)

| Excepción | HTTP | Payload |
|---|---|---|
| `AfiliadoNoEncontradoError` | 404 | `{"error": "<mensaje>"}` |
| `EmailDuplicadoError` | 409 | `{"error": "<mensaje>"}` |
| `DatoInvalidoError` / `FechaInvalidaError` | 422 | `{"error": "<mensaje>"}` |
| `SincronizacionError` | 500 | `{"error": "<mensaje>"}` |
| `ImportacionError` | 500 | `{"error": {"type": "...", "message": "..."}}` |
| Bug/error inesperado | 500 | default de FastAPI |

**Inconsistencia detectada**: `ImportacionError` expone un objeto anidado mientras el resto usa `{"error": str}`. Si se busca consistencia total, unificarlo a `{"error": "<mensaje>"}`.

## Reglas para endpoints nuevos

- ✅ Crea esquemas Pydantic dedicados por endpoint (input vs `*Response`), campos en snake_case, sin exponer ids internos ni datos sensibles.
- ✅ Validá la entrada con el schema (422 automático si falla) y validá el negocio con excepciones de dominio (mapeadas solo en `handlers.py`).
- ✅ Inyectá el caso de uso con `Depends(get_*)` desde `dependency_injection.py`; el router NO instancia adapters ni hace `try/except` de negocio.
- ✅ Respondé con el `status_code` que corresponde (201 al crear/importar, 200 al leer/actualizar/baja, 404/409/422/500 según tabla).
- ✅ Si el endpoint lista una colección, agregá filtros (`?estado=`, `?q=`) y paginación (`page`/`limit`) antes de que la colección crezca (hoy `/afiliados` no pagina).
- ❌ No uses verbos en rutas de CRUD simple (`/getAfiliado`, `/createAfiliado`).
- ❌ No devuelvas 200 para errores ni varíes el formato de error entre endpoints.
- ❌ No hagas sobre-anidado: `/afiliados/{id}/estado/{id}` — resolver con query params.
- ❌ No rompas backward compatibility sin versionar.

## Validación

- Para verificar el contrato de un endpoint nuevo, revisar el OpenAPI autogenerado en `/docs` (FastAPI) y correr la suite:

```bash
./venv/bin/python -m pytest -q
```

- Template de referencia: `templates/endpoint_fastapi.py`.