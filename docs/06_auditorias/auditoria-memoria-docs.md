# Auditoría de Memoria del Proyecto (docs/estado_actual_proyecto.md y bitácora)

> Fecha: 2026-09-17
> Auditor: agente opencode
> Alcance: `docs/estado_actual_proyecto.md`, `docs/bitacora_agentica.md`, `README.md`, `AGENTS.md`, cierres de fase

## 1. Resumen

El último trabajo registrado en la documentación era del **2026-09-11** (HU-06 ciclo de corrección),
pero el historial real de git muestra trabajo posterior sin reflejar: **contenedorización (2026-09-15)**,
merges a `develop` y `main`, y nuevos commits de reglas/estructura. Se corroboró cada hallazgo contra
el código y el historial antes de afirmar (regla anti-alucinación).

## 2. Desfases detectados

| # | Documento | Desfase | Verificado | Estado |
|---|---|---|---|---|
| 1 | `docs/estado_actual_proyecto.md` | Fecha de última actualización obsoleta (2026-09-11) | `git log` con commits del 2026-09-15 | ✅ corregido → 2026-09-17 |
| 2 | `docs/estado_actual_proyecto.md` | Rama activa decía `feature/tests-hus06` | HEAD de `main` = `6defbff` (merge develop); `feature/tests-hus06` contenida en `develop` (`0bccc08`) | ✅ corregido → `main` |
| 3 | `docs/estado_actual_proyecto.md` | Sin sección de contenedorización (Fase 5) | `Dockerfile`, `docker-entrypoint.sh`, `.dockerignore` presentes (commit `52f0b89`) | ✅ corregido → sección 6 |
| 4 | `docs/estado_actual_proyecto.md` | Sección 8 referenciaba `07_metodologia_agil` | Carpeta real es `docs/05_metodologia_agil` (renombrada en `7a618a1`) | ✅ corregido → `05_metodologia_agil` |
| 5 | `docs/estado_actual_proyecto.md` | Regla `auditoria-documentacion.md` no listada | Archivo existe en `.agents/rules/` (commit `11ff8b9`) | ✅ corregido → sección 8 |
| 6 | `docs/estado_actual_proyecto.md` | Versionado no reflejaba tags | Tags reales: v1.0.0, v2.0.0, v2.1.0, v2.2.0, v2.3.0, v2.3.1 | ✅ corregido → sección 8 (+ v2.4.0) |
| 7 | `docs/bitacora_agentica.md` | Faltaba entrada de contenedorización | Commits del 2026-09-15 no registrados | ✅ corregido → entradas 2026-09-15 y 2026-09-17 |
| 8 | `README.md` | Línea 43 referenciaba `07_metodologia_agil` | Carpeta real es `05_metodologia_agil` | ✅ corregido |
| 9 | `README.md` | Sin sección Docker ni Fase 5 | `Dockerfile`/entrypoint verificado | ✅ corregido |
| 10 | `AGENTS.md` | Sin comandos Docker ni referencia a `auditoria-documentacion.md` | Ruptura con regla dura existente | ✅ corregido |

## 3. Lo que NO era desfase (verificado)

- **Código vs HUs**: los 9 endpoints documentados coinciden con `afiliados.py` (6) + `sync.py` (3);
  `dependency_injection.py` cablea todos los UCs (core, UC2..UC8).
- **Rama borrada**: `feature/tests-hus06` y `feature/dockerfile` ya contenidas en `develop`/`main`
  (no se borró ninguna por decisión del usuario).

## 4. Contenedorización — cierre de Fase 5

Ante los hallazgos 3/6/7, se registró la contenedorización como **Fase 5 formal**:
- `face_5_cierre.md` — nuevo documento de cierre.
- Tag anotado **v2.4.0** (sin push) según `.agents/rules/versionado-fases.md`.
- La Fase 5 incrementa la menor: v2.3.1 → v2.4.0.

## 5. Verificación del código (no se tocó)

- `venv/bin/python -m pytest -q` → 139 passed.
- `docs/estado_actual_proyecto.md` completo releído antes y después de editar.

## 6. Archivos modificados en esta auditoría

- `docs/estado_actual_proyecto.md` — secciones 1, 6, 8.
- `docs/bitacora_agentica.md` — entrada 2026-09-17 (+ 2026-09-15).
- `face_5_cierre.md` — nuevo.
- `README.md` — línea 43, sección Docker, árbol de estructura, estado y roadmap.
- `AGENTS.md` — comandos Docker + regla de auditoría.
- `docs/06_auditorias/auditoria-memoria-docs.md` — este informe.

## 7. Pendiente externo (no bloqueado por esta auditoría)

- Probar el ciclo completo de HU-06 (importar → corregir → `reimport`) contra Google Sheets real
  con credenciales.