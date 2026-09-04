# Vitácora Agéntica

> Historial cronológico y append-only. NUNCA se borra ni se reescribe una entrada pasada.
> Cada entrada corresponde a una sesión/tarea significativa de trabajo del agente sobre el proyecto.
> Cuando este archivo crezca demasiado, archivar entradas viejas en `vitacora_YYYY-QX.md` y dejar acá solo un índice + las últimas entradas.

---

## 2026-09-04 — Setup de entorno y creación de AGENTS.md

**Qué se hizo:** se preparó el entorno local y se documentaron las convenciones del repo. Se instaló Python 3.13.5 vía pyenv (definido en `app/.python-version`), se creó el venv en `./venv`, se instalaron las dependencias de `app/requirements.txt` y `pytest`, y se corrió la suite unitaria como sanity check (86 tests OK, 1 falla preexistente).

**Decisiones de arquitectura:** mantener imports absolutos `app.*` ejecutando todo desde la raíz del repo; el `AGENTS.md` se escribe en español para fijar convenciones (comandos, capas, gotchas).

**Archivos/módulos tocados:**
- `AGENTS.md` — creado con comandos, arquitectura, convenciones y gotchas del repo.

**Estado resultante:** entorno usable; queda documentada la falla preexistente de `tests/unit/domian/services/test_data_transformer.py` (ImportError de `SheetRow`).

---

## 2026-09-04 — Adaptación del skill di-architect-scaffold al proyecto

**Qué se hizo:** se reescribió `.agents/skills/di-architect-scaffold/SKILL.md`, que originalmente describía otro proyecto (SGVIR), para que refleje este repo: stacks/convenciones reales (FastAPI, SQLAlchemy async, ports con ABC, `ucN_*`, wiring en `dependency_injection.py`) y un flujo de trabajo de 6 pasos para implementar HUs. También se documentaron las 8 historias de usuario en `docs/historias_de_usuario.md` y se aprobó su formato.

**Decisiones de arquitectura:** el dominio no importa frameworks; los casos de uso reciben ports y las excepciones de dominio se mapean a HTTP solo en `handlers.py`.

**Archivos/módulos tocados:**
- `.agents/skills/di-architect-scaffold/SKILL.md` — reescrito y adaptado.

**Estado resultante:** listo para usar el skill en futuras implementaciones de casos de uso.

---

## 2026-09-04 — Reestructuración de docs al formato Benn (fase 2 y 3)

**Qué se hizo:** se reemplazó la documentación plana de `docs/` por el formato Benn del proyecto `plataforma_web_indumentaria_benn`, backend-only (sin `_requerimientos.md`, sin mockups ni uso de IA). Se crearon las carpetas numeradas (`01_global`, `02_tecnico/diagramas`, `03_procesos`, `04_historias_usuario/HU-01..HU-08`, `07_metodologia_agil`), se migraron los globales y se expandieron las 8 HUs a 5 archivos c/u (HU-0X, caso_uso_expandido, api, modelos_datos, pruevas). Al cierre se eliminaron los 12 archivos originales de la raíz de `docs/` y se actualizó la sección de estructura del README.

**Decisiones de arquitectura:** preservar `decisiones_tecnicas.md` en `02_tecnico/` y `alcance.md` en `01_global/`; integrar `pruebas.md` en cada HU; la raíz de `docs/` queda solo con carpetas numeradas.

**Archivos/módulos tocados:**
- `docs/01_global/`, `docs/02_tecnico/` (con `diagramas/`), `docs/03_procesos/`, `docs/07_metodologia_agil/` — migrados.
- `docs/04_historias_usuario/HU-01/..HU-08/` — 40 archivos nuevos (5 por HU).
- `README.md` — sección de estructura `docs/` actualizada.
- Raíz de `docs/` — 12 archivos eliminados (fusionados en HUs/globales).

**Estado resultante:** `docs/` 100% formato Benn; commits `8f5b45f`, `ff27413`, `1eab9f4`, `6999ff8` con prefijo `DOCUMENTACION:`.

---

## 2026-09-04 — Commits atómicos y memoria del proyecto

**Qué se hizo:** sobre la rama `feature/docs-formato-benn` se realizaron los commits atómicos pendientes: `AGENTS.md` y el directorio `.agents/` (skill adaptado + skills preexistentes) por separado. Luego se creó la memoria del proyecto: `docs/estado_actual_proyecto.md` (fuente de contexto, con funcionalidades, tests, gotchas y deuda técnica) y `docs/vitacora_agentica.md` (historial append-only, primera entrada de esta sesión).

**Decisiones de arquitectura:** un commit por unidad lógica; la memoria vive en la raíz de `docs/` tal como define el `AGENTS.md`.

**Archivos/módulos tocados:**
- `docs/estado_actual_proyecto.md` — creado.
- `docs/vitacora_agentica.md` — creado.

**Estado resultante:** working tree limpio; quedó definido el mecanismo de actualización del estado y la vitácora para las próximas sesiones.