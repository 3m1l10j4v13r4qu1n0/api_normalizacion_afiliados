# Auditoría de Historias de Usuario

> Fecha: 2026-09-10
> Auditor: agente opencode
> Alcance: HU-01 a HU-08 (docs/04_historias_usuario/)

## 1. Resumen

Se verificó el estado de implementación de las 8 historias de usuario documentadas comparando contra el código fuente existente (endpoints, casos de uso, puertos, adapters, tests).

## 2. Resultado por HU

| HU | Descripción | Estado | Evidencia |
|---|---|---|---|
| HU-01 | Importar lista de afiliados (lotes) | ✅ | POST `/afiliados/import`, `ImportarAfiliadoUseCase.importar_desde_dicts()` en `core_importar_afiliado.py` |
| HU-02 | Registrar afiliado individual | ✅ | POST `/afiliados/`, `ImportarAfiliadoUseCase.agregar_afiliado()` en `core_importar_afiliado.py` |
| HU-03 | Consultar afiliados (listado y por ID) | ✅ | GET `/afiliados/` y GET `/afiliados/{afiliado_id}`, UC2 en `uc2_listar_afiliados.py` y `uc2_obtener_afiliado_por_id.py` |
| HU-04 | Modificar datos de afiliado | ✅ | PATCH `/afiliados/{afiliado_id}`, UC3 en `uc3_actualizar_afiliado.py` |
| HU-05 | Importar desde Google Sheets | ✅ | POST `/sync/sheets/import`, UC4a (`ImportSheetUseCase`) + UC4 (`ImportarAfiliadoUseCase.execute()`) |
| HU-06 | Marcar filas con errores en Sheets | ✅ | `SheetMarkingPort` + `SheetsMarkingAdapter` + `uc6_marcar_errores_sheets.py` (UC6) integrado en `POST /sync/sheets/import` (2026-09-10) |
| HU-07 | Dar de baja afiliado | ✅ | DELETE `/afiliados/{afiliado_id}`, UC5 en `uc5_dar_baja_afiliado.py` (baja lógica, `id_estado_afiliado=2`) |
| HU-08 | Generar tabla de afiliados en Sheets | 🔵 | Endpoint comentado en `sync.py:35-40`, sin caso de uso, puerto ni adapter |

## 3. Detalle de lo pendiente

### HU-08 — Generar tabla de afiliados en Google Sheets

**Qué falta:**
- Puerto `sheet_export_port.py` (contrato para escribir tabla)
- Adapter `sheets_export_adapter.py` (crear/limpiar hoja, escribir filas)
- Caso de uso `uc8_exportar_afiliados_sheets.py` (consultar activos, calcular edad, ordenar)
- Query port: agregar `obtener_activos()` al `AfiliadoQueryPort`
- Router: descomentar y conectar `POST /sync/sheets/export`

**Reglas de negocio aplicables:**
- AF-RN18: Solo afiliados activos
- AF-RN19: Edad calculada dinámicamente, no persistida
- AF-RN20: Solo datos relevantes
- AF-RN21: Orden alfabético por nombre y apellido
- AF-RN22: Sin duplicados

## 4. Verificaciones operativas pendientes

1. ✅ (2026-09-10) `alembic upgrade head` contra BD real — resuelto, esquema sincronizado (`alembic check` OK)
2. ✅ (2026-09-10) `GET /afiliados/` con inactivos — NO filtra, muestra todos (correcto según HU-03)
3. ✅ (2026-09-10) Merge de rama `feature/refactorizacion-arquitectonica` → `develop` — ya estaba mergeada, rama borrada
4. ✅ (2026-09-10) Endpoints de Google Sheets con credenciales reales — `/sync/sheets/import` (39 filas, 36 válidas) y `/sync/sheets/export` (35 activos) OK

## 5. Archivos modificados en esta auditoría / seguimiento

- `AGENTS.md` — se agregó tabla de estado de HUs + plan de implementación
- `docs/06_auditorias/auditoria-historias-usuario.md` — este informe

## 6. NOTA de seguimiento (2026-09-10)

- HU-06 fue **implementada**: `SheetMarkingPort` (`app/domain/ports/sheet_marking_port.py`), `SheetsMarkingAdapter` (`app/infrastructure/google/sheets_marking_adapter.py`), UC6 (`app/application/use_cases/uc6_marcar_errores_sheets.py`), integrado en `POST /sync/sheets/import`. Tests 104/104 OK.
- HU-08 fue **implementada** el mismo día: `SheetExportPort` + `SheetsExportAdapter` + UC8 (`uc8_exportar_afiliados_sheets.py`), endpoint `POST /sync/sheets/export` habilitado. Verificado con credenciales reales (35 activos exportados).
