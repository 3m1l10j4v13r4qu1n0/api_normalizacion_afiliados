# Cierre Fase 5 — Contenedorización

## 1. Objetivo
Dejar constancia de la finalización de la Fase 5 del proyecto
api_normalizacion_afiliados, correspondiente a la contenedorización de la API
para su despliegue en container (Docker).

## 2. Alcance de la validación

### Artefactos entregados

| Artefacto | Descripción |
|---|---|
| `Dockerfile` | Imagen base `python:3.13-slim`, `EXPOSE 8002`, `ENTRYPOINT ["/app/docker-entrypoint.sh"]`. Copia `app/requirements.txt` antes del código para reutilizar cache de capas. |
| `docker-entrypoint.sh` | Secuencia de arranque: espera conexión a PostgreSQL (hasta 30 intentos con 2s), `alembic upgrade head`, seed de datos iniciales (`seed_runner`) y `uvicorn app.main:app --host 0.0.0.0 --port 8002`. |
| `.dockerignore` | Excluye `venv/`, `.git/`, `.credentials/`, `tests/`, caches de ruff/pytest y archivos locales de entorno. |

### Comandos de uso

```bash
# Build de la imagen
docker build -t api-normalizacion-afiliados .

# Run del container (mapea el puerto 8002 y pasa las variables de entorno)
docker run -p 8002:8002 --env-file .env api-normalizacion-afiliados
```

## 3. Decisiones de arquitectura
- El container ejecuta **migraciones + seed en el entrypoint** antes de levantar la API
  (patrón para entornos Docker de un solo servicio).
- Puerta de entrada única: `docker-entrypoint.sh` (idioma neutro, `#!/bin/sh`).
- Puerto interno/expuesto: **8002** (coincide con la configuración de uvicorn del entrypoint).
- Las credenciales de Google y la BD se inyectan por entorno (`--env-file .env`); `.credentials/`
  queda excluida del build vía `.dockerignore`.

## 4. Criterios de validación aplicados
- La imagen usa la misma versión de Python que el entorno local (`3.13`, slim).
- El entrypoint respeta el flujo existente del proyecto: migraciones vía Alembic y seed
  con `seed_runner` (no duplica lógica).
- La suite sigue en verde sobre la base de la Fase 4 (139/139 tests OK).

## 5. Resultado
La API quedó lista para despliegue en container, manteniendo el flujo de
migraciones y datos iniciales automatizado.

## 6. Estado del proyecto
Fase 5 — Contenedorización: **FINALIZADA**

Se cierra con tag anotado **v2.4.0** (sin push). Pendiente externo: probar el ciclo
completo de HU-06 (importar → corregir → reimportar) contra Google Sheets real con credenciales.