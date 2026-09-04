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

---

## 2026-09-04 — Regla SOLID para Python integrada al proyecto

**Qué se hizo:** se creó `.agents/rules/reglas-solid.md` replicando la matriz de `.opencode/rules/reglas-solid.md` del frontend `web_ifts12_frontend`, adaptada a Python y al stack de este proyecto (Clean Architecture + Hexagonal, FastAPI, SQLAlchemy async, dataclasses, typing). Se referenció en `AGENTS.md` (Convenciones), se actualizó el estado del proyecto (sección 8) y se corrigió la nota obsoleta del skill `di-architect-scaffold` (ya adaptado, ya no describe SGVIR). El usuario optó por `.agents/rules/` en lugar de `.opencode/rules/`.

**Decisiones de arquitectura:** misma matriz del frontend (SRP, OCP, LSP, ISP, DIP, reglas específicas del lenguaje, cuándo no aplicar, smells, verificación), pero con smells propios del repo (import de frameworks en `domain/`, SQL en use cases, `try/except` de negocio fuera de `handlers.py`).

**Archivos/módulos tocados:**
- `.agents/rules/reglas-solid.md` — creado.
- `AGENTS.md` — referencia a la regla y corrección de nota SGVIR.
- `docs/estado_actual_proyecto.md` — sección 8 actualizada.
- `docs/vitacora_agentica.md` — esta entrada.

**Estado resultante:** la regla queda como convención vigente a aplicar en futuras implementaciones de casos de uso/HUs.

---

## 2026-09-04 — Instalación y adaptación del skill rest-api-design

**Qué se hizo:** se instaló el skill `rest-api-design` (aj-geddes/useful-ai-prompts, vía `npx skills add --yes`) en `.agents/skills/rest-api-design/` con su `skills-lock.json` y el symlink de Claude Code. Se revisó todo el skill (SKILL.md + 9 referencias) y se adaptó a este proyecto: nueva guía local `references/fastapi-conventions.md` (mapeo excepción de dominio → status code del `handlers.py` real, naming vigente `/afiliados`, `/sync/sheets/import`, inconsistencias detectadas), template nuevo `templates/endpoint_fastapi.py` con convenciones del repo, y sección "Applying to FastAPI (this project)" en el SKILL.md. Se referenció en AGENTS.md y en el estado del proyecto.

**Decisiones de arquitectura:** no modificar las referencias originales (Express/JS); agregarlas/adaptarlas con artefactos locales del proyecto (FastAPI + Clean Architecture + DI con `Depends(get_*)`). Se documentó la inconsistencia de `ImportacionError` (payload anidado vs `{"error": str}`) para unificar a futuro.

**Archivos/módulos tocados:**
- `.agents/skills/rest-api-design/references/fastapi-conventions.md` — nueva guía local.
- `.agents/skills/rest-api-design/templates/endpoint_fastapi.py` — nuevo scaffold.
- `.agents/skills/rest-api-design/SKILL.md` — tabla de guías y sección de aplicación al proyecto.
- `AGENTS.md` y `docs/estado_actual_proyecto.md` — referencias al skill adaptado.
- `.agents/skills/rest-api-design/` (instalación), `skills-lock.json`, `.claude/skills/rest-api-design` — commit previo `2baabc6`.

**Estado resultante:** el skill queda listo para diseñar endpoints nuevos del backend siguiendo convenciones REST y el mapeo real de errores del proyecto.