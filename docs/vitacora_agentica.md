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

---

## 2026-09-04 — Plan de refactorización del proyecto (feedback + hoja de ruta)

**Qué se hizo:** se revisó el repo completo siguiendo las reglas del proyecto (`AGENTS.md`, skill `di-architect-scaffold`, `reglas-solid.md`, `estado_actual_proyecto.md`) y se entregó feedback con hallazgos ordenados por severidad, más un plan de refactorización en 6 fases. Se consensuaron tres decisiones clave con el usuario.

**Hallazgos críticos detectados:**
- Violación de pureza del dominio: `app/domain/ports/dominio_repository_port.py` importa `sqlalchemy.orm.DeclarativeBase`; además `core_importar_afiliado.py` instancia los ORMs (`GeneroORM`, etc.) dentro de la capa de aplicación.
- Bug AF-RN12: `ErrorRepository.registrar_error` no implementa el parámetro `row_number` exigido por `ErrorRepositoryPort`, por lo que se pierde el número de fila al persistir.
- LSP rota: `AfiliadoImportacionPort` define `save_importacion()` pero la implementación y el use case usan `save()`.
- Duplicación de arquitectura: dos `ImportarAfiliadoUseCase` "core" + wrappers triviales (`uc1a`, `uc1b`, `uc4`, `uc4a`) que solo agregan indirección.
- `gspread` y `google-auth` ausentes de `app/requirements.txt`; env de Google desincronizado entre `config.py` y `.env.example`.
- Test roto preexistente: `test_data_transformer.py` importa `SheetRow` (renombrado a `InputRow`).

**Decisiones de arquitectura:**
- Purificar el port de dominio usando un **enum `Dominio`** (Genero, EstadoCivil, NivelEducativo, RelacionDependencia, EstadoAfiliado) en lugar de recibir la clase ORM; el adapter mapea enum → ORM internamente.
- **Fusionar los wrappers** `uc1a/uc1b/uc4/uc4a` en los UCs core, eliminando la indirección redundante.
- Reordenar la prioridad: Fases 1+2 (puertos y bug) → Fase 3 (split del core/SRP) → Fase 4 (deuda operativa) → Fase 5 (endpoints) → Fase 6 (documentación).

**Plan de fases acordado (pendiente de implementar en una nueva sesión):**
- **F1 — Purificar dominio y alinear contratos:** enum `Dominio`, reescribir `resolver_o_crear(dominio, descripcion)`, quitar ORMs del use case, renombrar `save_importacion`→`save`.
- **F2 — Fix AF-RN12:** implementar `row_number` en `ErrorRepository` y verificar migración.
- **F3 — Split del core (SRP):** nuevo servicio de dominio puro `app/domain/services/importacion_pipeline.py`; `core_importar_afiliado` como orquestador; eliminar los wrappers de UC duplicados y recalibrar `dependency_injection.py` y routers.
- **F4 — Deuda operativa:** agregar `gspread`/`google-auth` a requirements; unificar env de Google; arreglar `test_data_transformer.py`; desacoplar `DATABASE_URL` de los tests puros; constantes de estados y limpieza de código muerto.
- **F5 — Endpoints:** uniformar payload de errores a `{"error": str}` (quitar anidado de `ImportacionError`); exponer lista de errores en `ImportResponse`.
- **F6 — Documentación:** actualizar `docs/estado_actual_proyecto.md` y agregar entrada de vitácora al finalizar.

**Estado resultante:** plan registrado y quedó listo para implementarse en una nueva sesión. **No se tocó código de aplicación** en esta entrada; solo documentación. Working tree sin cambios de código.

---

## 2026-09-07 — F1: Purificación del dominio y alineación de contratos

**Qué se hizo:** se implementó la **Fase 1** del plan de refactorización sobre la rama nueva `feature/refactorizacion-arquitectonica` (creada desde `develop`). Se purificó el dominio eliminando la dependencia de SQLAlchemy del port de valores controlados y se alineó el contrato de persistencia de afiliados.

**Decisiones de arquitectura:**
- Nuevo enum puro `app/domain/models/dominio.py` (`Dominio`: GENERO, ESTADO_CIVIL, NIVEL_EDUCATIVO, RELACION_DEPENDENCIA, ESTADO_AFILIADO) que identifica las tablas de valores controlados de forma abstracta.
- `DominioRepositoryPort.resolver_o_crear` ahora recibe `Dominio` en lugar de `Type[DeclarativeBase]`; esto elimina el import de `sqlalchemy.orm` del dominio. El adapter `DominioRepository` mapea enum → ORM internamente (dict `_ORM_POR_DOMINIO`), dejando los ORMs solo en infraestructura.
- `core_importar_afiliado.py` ya no importa ni instancia ORMs; llama `resolver_o_crear(Dominio.X, ...)`.
- Fix LSP: `AfiliadoImportacionPort.save_importacion()` se renombró a `save()`, alineando el contrato con la implementación (`AfiliadoImportacionRepository.save`) y el use case core, que ya usaba `save()`.

**Archivos/módulos tocados:**
- `app/domain/models/dominio.py` — creado (enum `Dominio`).
- `app/domain/ports/dominio_repository_port.py` — purificado (enum en vez de ORM).
- `app/infrastructure/database/repositories/dominio_repository.py` — mapeo enum → ORM.
- `app/application/use_cases/core_importar_afiliado.py` — quitados ORMs, usa enum.
- `app/domain/ports/afiliado/afiliado_importacion_port.py` — rename `save_importacion`→`save`.
- `docs/estado_actual_proyecto.md` — secciones 1, 3 actualizadas (rama activa, enum `Dominio`).

**Estado resultante:** dominio 100% puro (sin `sqlalchemy.orm.DeclarativeBase` fuera de infraestructura); suite 86/86 tests OK (excluyendo el `test_data_transformer.py` roto preexistente); imports de F1 verificados. Quedan pendientes F2 (fix AF-RN12 `row_number`), F3 (split core/SRP + eliminar wrappers), F4 (deuda operativa), F5 (endpoints), F6 (doc final).

---

## 2026-09-07 — F2: Fix AF-RN12 (se persiste row_number en errores de validación)

**Qué se hizo:** se implementó la **Fase 2** del plan de refactorización. Se corrigió el bug AF-RN12 por el cual `ErrorRepository.registrar_error` no implementaba el parámetro `row_number` exigido por `ErrorRepositoryPort`, por lo que el número de fila original se perdía al persistir los errores de validación.

**Decisiones de arquitectura:**
- El port ya exigía `row_number`, el use case core ya lo pasaba y el ORM ya definía la columna; solo faltaba que el repositorio lo aceptara y lo persistiera. Se alineó `ErrorRepository` con el contrato (LSP/ISP).
- Se detectó un desincronismo modelo ↔ migración: la migración inicial `6fecb555bfe0` no creaba la columna `row_number` en `errores_validacion` aunque el ORM la definía. Se agregó la migración manual `a1f2b3c4d5e6` (no autogenerate porque no hay BD configurada `.env`).

**Archivos/módulos tocados:**
- `app/infrastructure/database/repositories/error_repository.py` — se implementa `row_number` y se persiste.
- `alembic/versions/a1f2b3c4d5e6_agregar_row_number_errores.py` — creada (agrega columna `row_number`).
- `docs/estado_actual_proyecto.md` — nota AF-RN12 en entidad `ErrorValidacion`.

**Estado resultante:** AF-RN12 corregido; el número de fila original ahora persiste. Suite 86/86 tests OK; imports del repositorio verificados. Sin BD local no se pudo correr `alembic upgrade head` (queda pendiente verificarlo en entorno con BD). Pendientes: F3, F4, F5, F6.
---

## 2026-09-07 — F3: Split del core/SRP (pipeline de dominio puro + UC único)

**Qué se hizo:** se implementó la **Fase 3** del plan: se extrajo la lógica de pipeline de importación a un servicio de dominio puro, se convirtió `core_importar_afiliado.py` en el orquestador/UC único, y se eliminaron los wrappers de UC que agregaban indirección redundante.

**Decisiones de arquitectura (vale la opción "Core como UC único + pipeline puro"):**
- Nuevo `app/domain/services/importacion_pipeline.py` → `procesar_fila()`: función pura del dominio que recibe los valores crudos + IDs de dominio/domicilio ya resueltos + DNIs, y devuelve `(dato_normalizado, errores)`. Encapsula normalización (RF7/RF8), validación (RF3/RF4) y dedupe por DNI (RF5). No toca repositorios ni frameworks.
- `core_importar_afiliado.py` (`ImportarAfiliadoUseCase`) queda como **orquestador único**: resuelve dominios y domicilio vía ports, delega la lógica por fila en `procesar_fila`, y persiste/ registra errores. Absorbe la conversión de input: `importar_desde_dicts()` (UC1a), `agregar_afiliado()` (UC1b), `execute(rows)` (UC4, recibe InputRow del Sheet).
- **Se eliminaron** `uc1a_importar_lista_afiliados.py`, `uc1b_agregar_afiliado.py`, `uc4_importar_afiliado.py`. **Se conservó** `uc4a_importar_afiliado.py` (`ImportSheetUseCase`): es el caso de uso de lectura/transformación del Sheet, NO un wrapper del core (el plan original lo listaba mal).
- `dependency_injection.py` recalibrado: `get_importar_afiliado_core` (fábrica única del core), `get_import_sheet_uc4a` (lectura del Sheet), y alias `get_importar_afiliado_uc4 = get_importar_afiliado_core`.
- Routers: `/afiliados/import` y `/afiliados/` apuntan al core (con `model_dump()`); `/sync/sheets/import` inyecta `ImportSheetUseCase` + core y los combina en el endpoint.

**Instalación de deps (anticipo de F4):** se instalaron `gspread` y `google-auth` en el venv para poder validar la app completa (antes el import de `dependency_injection.py` fallaba por no tenerlos). Aún NO se agregaron a `app/requirements.txt`.

**Archivos/módulos tocados:**
- `app/domain/services/importacion_pipeline.py` — creado (función pura `procesar_fila`).
- `app/application/use_cases/core_importar_afiliado.py` — reescrito como orquestador único.
- `app/application/use_cases/uc1a_importar_lista_afiliados.py`, `uc1b_agregar_afiliado.py`, `uc4_importar_afiliado.py` — eliminados.
- `app/infrastructure/dependencies/dependency_injection.py` — recalibrado.
- `app/presentation/routers/afiliados.py`, `sync.py` — recalibrados al core.
- `docs/estado_actual_proyecto.md` — sección 4 actualizada.

**Bug latente detectado (preexistente, fuera de F3):** `normalizar_afiliado` no incluye `id_domicilio` en su dict de salida, por lo que el domicilio resuelto no se persiste con el afiliado. Se preservó este comportamiento en el refactor (no cambia semántica en F3); queda como deuda para F4/HU corrección.

**Estado resultante:** suite 86/86 tests OK; pipeline validado (fila válida, inválida y duplicada); app completa carga con todos los endpoints. Pendientes: F4 (agregar deps a requirements, unificar env Google, arreglar test_data_transformer.py, bug domicilio, desacoplar DATABASE_URL de tests puros), F5, F6.

---

## 2026-09-07 — F4: Deuda operativa

**Qué se hizo:** se implementó la **Fase 4** del plan, resolviendo la deuda operativa documentada en el estado del proyecto y el AGENTS.md.

**Cambios resueltos:**
1. **Deps de Google en requirements:** se agregaron `gspread==6.2.1` y `google-auth==2.57.1` a `app/requirements.txt` (antes el código los importaba pero no estaban listados; los endpoints de sync no cargaban).
2. **Env de Google alineado:** `.env.example` ahora define `GOOGLE_CREDENTIALS_PATH` y `GOOGLE_SHEETS_ID` (coincide con `config.py` y `google_sheets_client.py`). Se eliminó el desincronismo previo (`GOOGLE_SERVICE_ACCOUNT_FILE`/`GOOGLE_SHEET_ID`).
3. **Test roto preexistente arreglado:** `test_data_transformer.py` importaba `SheetRow` (renombrado a `InputRow`). Se actualizó el import y el `isinstance` de verificación.
4. **Bug latente de domicilio corregido:** `normalizar_afiliado` no incluía `id_domicilio` en su dict de salida, por lo que el domicilio resuelto se perdía al persistir el afiliado. Se agregó `id_domicilio` a la normalización; se actualizó/amplió `test_normalizacion.py` (claves esperadas + propagación del ID).
5. **`DATABASE_URL` desacoplada de tests puros:** nuevo `tests/conftest.py` que setea un `DATABASE_URL` por defecto antes de importar módulos, evitando que un import transitivo a `config.py` falle sin `.env`.

**Decisiones de arquitectura:**
- El desacople de `DATABASE_URL` se resolvió a nivel de `conftest.py` (fallback global) en lugar de modificar `config.py`, preservando el comportamiento productivo de requerir la var obligatoria.
- El bug de `id_domicilio` se corrigió en el servicio de dominio (`normalizar_afiliado`), que es el punto único por donde pasa todo dato normalizado — beneficiando a todos los puntos de importación.

**Archivos/módulos tocados:**
- `app/requirements.txt` — agregados `gspread` y `google-auth`.
- `.env.example` — renombradas vars de Google para alinear con código.
- `tests/unit/domian/services/test_data_transformer.py` — `SheetRow` → `InputRow`.
- `app/domain/services/normalizacion.py` — `id_domicilio` en la salida.
- `tests/unit/domian/services/test_normalizacion.py` — claves esperadas + nuevo test de propagación de domicilio.
- `tests/conftest.py` — creado (fallback de `DATABASE_URL`).
- `docs/estado_actual_proyecto.md` — secciones 5/6/7 actualizadas.

**Estado resultante:** suite completa **100/100 tests OK** (incluye el anteriormente roto); app carga con todos los endpoints; env de Google coherente; deps de instalación completa. Pendientes: F5 (endpoints), F6 (doc final).

---

## 2026-09-07 — F5: Endpoints (payload de errores unificado + lista de errores en respuesta)

**Qué se hizo:** se implementó la **Fase 5** del plan: se uniformó el payload de errores de las excepciones de dominio a `{"error": str}` y se expuso la lista de errores de validación en `ImportResponse`.

**Cambios:**
1. **Handler `ImportacionError`:** se eliminó el payload anidado (`{"error": {"type", "message"}}`); ahora devuelve `{"error": str(exc)}`, coherente con el resto de excepciones (`AfiliadoNoEncontradoError`, `DatoInvalidoError`, etc.).
2. **`ImportResponse`:** nuevos `ErrorValidacionResponse` (campo, descripcion_error, row_number — AF-RN12) y campo `errores: list[...]`.
3. **Helper `import_response_from_importacion(importacion)`:** proyección explícita del modelo de dominio `Importacion` al schema de respuesta, reutilizada en los 3 endpoints (`/afiliados/import`, `/afiliados/`, `/sync/sheets/import`). Antes `afiliados.py` devolvía el objeto `Importacion` directo con `response_model=ImportResponse` (los nombres de campo no coincidían con el schema); ahora se construye `ImportResponse` explícitamente en todos lados.

**Archivos/módulos tocados:**
- `app/presentation/handlers.py` — handler `ImportacionError` unificado a `{"error": str}`.
- `app/presentation/schemas/importacion_schema.py` — `ErrorValidacionResponse`, campo `errores` en `ImportResponse`, helper de proyección.
- `app/presentation/routers/afiliados.py`, `sync.py` — usan `import_response_from_importacion`.

**Estado resultante:** payload de errores 100% uniforme; los endpoints de importación exponen el detalle de errores con número de fila. Suite 100/100 tests OK; app carga con todos los endpoints. Pendientes: F6 (documentación final + merge).

---

## 2026-09-07 — F6: Cierre y documentación final del plan de refactorización

**Qué se hizo:** se completó la **Fase 6** (cierre): se verificó la consistencia de toda la documentación con el código resultante del plan F1–F5 y se actualizaron los artefactos que aún reflejaban el estado previo.

**Cambios:**
1. `docs/estado_actual_proyecto.md` — se eliminó del TODO (sección 7) el ítem de unificar el payload de `ImportacionError` (ya resuelto en F5).
2. `AGENTS.md` — se reemplazaron los gotchas resueltos: el desincronismo de env de Google Sheets y la ausencia de `gspread`/`google-auth` en requirements (ambos resueltos en F4). Se dejó la nota del pipeline como UC único.
3. Se limpiaron referencias cosméticas/obsoletas a `SheetRow` en docstrings (`uc4a_importar_afiliado.py`, `data_transformer.py`).
4. Verificación final: búsqueda global sin referencias rotas a wrappers eliminados ni a `save_importacion`/`SheetRow` en código funcional.

**Estado final del plan F1–F6:**
- F1 — Dominio purificado (enum `Dominio`, sin ORMs en el core, contrato `save` alineado). ✅
- F2 — Fix AF-RN12 (`row_number` persiste en errores) + migración. ✅
- F3 — Split core/SRP: `importacion_pipeline` puro + core como UC único, wrappers eliminados. ✅
- F4 — Deuda operativa: deps Google, env alineado, test roto reparado, bug de domicilio, `DATABASE_URL` desacoplada de tests. ✅
- F5 — Payload de errores unificado + lista de errores en `ImportResponse`. ✅
- F6 — Documentación final. ✅

**Archivos/módulos tocados:**
- `docs/estado_actual_proyecto.md` — TODO actualizado.
- `AGENTS.md` — gotchas actualizados.
- `app/application/use_cases/uc4a_importar_afiliado.py`, `app/domain/services/data_transformer.py` — docstrings.

**Estado resultante:** suite 100/100 tests OK; app carga con los 12 endpoints; documentación (estado, vitácora, AGENTS.md) coherente con el código. Plan de refactorización F1–F6 **completo**. Pendiente de decisión del usuario: merge de `feature/refactorizacion-arquitectonica` a `develop`.

---

## 2026-09-10 — Auditoría de historias de usuario (HU-01 a HU-08)

**Qué se hizo:** auditoría completa del estado de implementación de las 8 historias de usuario documentadas en `docs/04_historias_usuario/`. Se verificó cada HU contra el código fuente end-to-end (endpoints, casos de uso, puertos, adapters, tests).

**Resultado de la auditoría:**
- ✅ HU-01 a HU-05, HU-07 — completamente implementadas
- 🟡 HU-06 — parcial: `ErrorValidacion`+`row_number` se registra en BD, falta adapter para marcación visual (fondo rojo) en Google Sheets
- 🔵 HU-08 — no implementada: endpoint comentado, sin caso de uso ni adapter

**Archivos/módulos tocados:**
- `AGENTS.md` — se agregó tabla de estado de HUs verificada + sección de pendientes de implementación
- `docs/06_auditorias/auditoria-historias-usuario.md` — nuevo: informe de auditoría
- `docs/vitacora_agentica.md` — esta entrada

**Estado resultante:** el AGENTS.md ahora refleja el estado real de implementación de cada HU y detalla los pasos para completar HU-06 y HU-08.

---

## 2026-09-10 — Actualización de AGENTS.md con reglas del proyecto

**Qué se hizo:** se reescribió `AGENTS.md` para incorporar de manera integral todas las reglas del proyecto (`.agents/rules/`), Organizándolas en secciones claras:
- Flujo de implementación (tarea → código → commit → rama → merge → versionado)
- Reglas de verificación y anti-alucinación
- Referencias correctas a `.agents/rules/` (antes decía `.opencode/rules/`)

**Archivos/módulos tocados:**
- `AGENTS.md` — reescrito con reglas integradas

**Estado resultante:** AGENTS.md actualizado como guía completa para futuras implementaciones, alineado con todas las reglas duras del proyecto.

---

## 2026-09-10 — HU-06: marcación visual de errores en Google Sheets

**Qué se hizo:** se implementó la marcación visual de filas con errores en Google Sheets (HU-06), que estaba parcial:
- `app/domain/ports/sheet_marking_port.py` — nuevo puerto `SheetMarkingPort` (contrato `marcar_filas_con_errores`).
- `app/infrastructure/google/sheets_marking_adapter.py` — nuevo adapter `SheetsMarkingAdapter` (gspread, batch format, fondo rojo, ejecuta en executor para no bloquear el loop).
- `app/infrastructure/google/google_sheets_client.py` — se agregó método `marcar_filas_con_errores` al cliente gspread.
- `app/application/use_cases/uc6_marcar_errores_sheets.py` — nuevo UC6 `MarcarErroresSheetsUseCase` (deduplica y ordena `row_number`s).
- `app/infrastructure/dependencies/dependency_injection.py` — `build_marking_port()` + `get_marcar_errores_sheets_uc6()`.
- `app/presentation/routers/sync.py` — se integró UC6 al final de `POST /sync/sheets/import`; el fallo al marcar no interrumpe la importación (SH-UC4b-RN4, captura solo `SincronizacionError`).
- `tests/unit/domian/services/test_marcar_errores_sheets.py` — 4 tests unitarios (extracción, dedup, sin errores, orden).

**Decisiones:** la marcación es paso interno del flujo de importación (no endpoint separado, según HU-06_api); se captura `SincronizacionError` en el router porque es el fallo permitido de no interrupción. Se instalaron `ruff` y `black` en el venv (el repo tenía 257 errores de ruff / 67 archivos por formatear preexistentes que NO se tocaron).

**Commits:** `f7ca501` (puerto), `f8188c9` (adapter), `1e93fc1` (UC6), `26845b1` (DI), `4746ce4` (sync), `4e45d06` (test).

**Estado resultante:** 104/104 tests OK; app carga; HU-06 completa. Pendiente: HU-08 (exportar a Sheets) y verificaciones operativas.

## 2026-09-10 — Limpieza de estilo: ruff y black en verde

**Qué se hizo:** se resolvieron los 257 errores de ruff y los 67 archivos sin formato de black que existían previamente (deuda técnica detectada en la HU-06).
- Se creó `pyproject.toml` en la raíz con config de Ruff (`line-length=100`, `target-version=py313`).
- Se ignoró `B008` (patrón FastAPI `Depends()` como default, intencional en todo el repo) y `BLE001` solo en `google_sheets_client.py` (catch-all que envuelve errores de gspread en `SincronizacionError`).
- `ruff --fix` corrigió 234 errores auto-arreglables (imports, anotaciones PEP 604/585, placeholders).
- Correcciones manuales: `__all__` con re-exports explícitos en `orm_models/__init__.py` (necesarios para Alembic), `ClassVar` en `dominio_repository.py`, `except DatoInvalidoError` en lugar de `except Exception` en `importacion_pipeline.py`, línea inútil `datos` eliminada en `afiliados.py`.
- `black` reformateó 60 archivos.

**Decisión:** `B008` y el `BLE001` del adapter de Google son patrones intencionales del código, se configuran en `pyproject.toml` en lugar de forzar reescrituras que romperían la convención FastAPI del repo.

**Commits:** `dbf6760` `style(api): se aplican reglas de ruff y black` (62 archivos).

**Estado resultante:** `ruff check .` en verde, `black --check .` en verde (79 archivos), 104/104 tests OK. Pendiente: HU-08 (exportar a Sheets) y verificaciones operativas.

## 2026-09-10 — HU-08: exportar tabla de afiliados activos a Google Sheets

**Qué se hizo:** se implementó la exportación de la tabla de afiliados activos a Google Sheets (HU-08), que estaba sin implementar:
- `app/domain/models/afiliado_export_row.py` — nueva entidad `AfiliadoExportRow` (nombre_apellido, edad, dni, numero_legajo, email).
- `app/domain/ports/sheet_export_port.py` — nuevo puerto `SheetExportPort` (contrato `exportar_tabla`).
- `app/domain/ports/afiliado/afiliado_query_port.py` — se agregó `obtener_activos()` al puerto.
- `app/infrastructure/google/sheets_export_adapter.py` — nuevo adapter `SheetsExportAdapter` (gspread, crea hoja si no existe, limpia y regraba, ejecuta en executor).
- `app/infrastructure/google/google_sheets_client.py` — se agregó método `exportar_tabla` al cliente gspread.
- `app/infrastructure/database/repositories/afiliado_query_repository.py` — implementación de `obtener_activos()` (filtra `id_estado_afiliado == 1`).
- `app/application/use_cases/uc8_exportar_afiliados_sheets.py` — UC8 `ExportarAfiliadosSheetsUseCase` (consulta activos, calcula edad, ordena alfabéticamente, delega al puerto de exportación).
- `app/infrastructure/dependencies/dependency_injection.py` — `build_export_port()` + `get_exportar_afiliados_uc8()`.
- `app/presentation/routers/sync.py` — se descomentó y habilitó `POST /sync/sheets/export` con `ExportResponse`.
- `app/presentation/schemas/importacion_schema.py` — nuevo schema `ExportResponse` (cantidad_registros_procesados, mensaje).
- `tests/unit/domian/services/test_exportar_afiliados_sheets.py` — 7 tests (calcular_edad, orden, sin activos, email opcional).

**Decisiones:** la columna "Datos Relevantes" se desglosó en 3 columnas separadas (DNI, N° Legajo, Email) para mayor claridad en la hoja de Sheets. La función `calcular_edad` vive en el caso de uso (no en el dominio) porque depende de `datetime.now()`. `AfiliadoNoEncontradoError` se reutiliza para el caso "no hay activos" (404 en la API).

**Commits:** `54b565c` (dominio), `5090adc` (infra), `54412c1` (UC8+DI), `36d53cc` (presentación), `b0ed084` (tests).

**Estado resultante:** 111/111 tests OK; `ruff check .` y `black --check .` en verde; endpoint `/sync/sheets/export` registrado. Pendiente: verificaciones operativas (BD real, merge a develop).

---

## 2026-09-10 — Cierre documental de fases 2, 3 y 4 + actualización de README

**Qué se hizo:** se crearon los documentos de cierre para las fases 2, 3 y 4 del proyecto (siguiendo el formato de `face_1_cierre.md`) y se actualizó el `README.md` con el estado real del proyecto.

**Cambios:**
1. `face_2_cierre.md` — cierre de Fase 2 (diseño técnico y arquitectura): Clean Architecture + Hexagonal, puertos/adapters, diagramas.
2. `face_3_cierre.md` — cierre de Fase 3 (implementación API REST): 8 HUs implementadas, 8 endpoints, pipeline de importación, refactorización F1–F6.
3. `face_4_cierre.md` — cierre de Fase 4 (pruebas y validación): 111/111 tests OK, ruff/black en verde.
4. `README.md` — actualizado:
   - Tabla de endpoints: agregado `POST /sync/sheets/export` (HU-08) + mención de HU-06 en import
   - Sección de estado: las 4 fases marcadas como FINALIZADA, con links a cierres
   - Roadmap: fase 4 completada, pendientes actualizados
   - Estructura del proyecto: agregados `06_auditorias/` y tests de HU-06/HU-08
   - Archivos de cierre: `face_2_cierre.md`, `face_3_cierre.md`, `face_4_cierre.md`

**Archivos/módulos tocados:**
- `face_2_cierre.md` — nuevo
- `face_3_cierre.md` — nuevo
- `face_4_cierre.md` — nuevo
- `README.md` — endpoints, estado, roadmap, estructura, tests

**Estado resultante:** las 4 fases del proyecto tienen su documento de cierre. El README refleja el estado real: 111/111 tests OK, 8 HUs implementadas, 8 endpoints. Pendientes: verificaciones operativas contra BD real y merge a develop.
