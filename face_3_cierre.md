# Cierre Fase 3 — Implementación API REST

## 1. Objetivo
Dejar constancia de la finalización y validación de la Fase 3 del proyecto
api_normalizacion_afiliados, correspondiente a la implementación completa de la
API REST y las 8 historias de usuario.

## 2. Alcance de la validación
Se verificó la implementación end-to-end de cada HU contra el código fuente
(endpoints, casos de uso, puertos, adapters, DI, schemas, tests).

### Historias de usuario implementadas

| HU | Descripción | Endpoint | Caso de uso |
|---|---|---|---|
| HU-01 | Importar lista de afiliados (lotes) | POST `/afiliados/import` | `ImportarAfiliadoUseCase.importar_desde_dicts()` |
| HU-02 | Registrar afiliado individual | POST `/afiliados/` | `ImportarAfiliadoUseCase.agregar_afiliado()` |
| HU-03 | Consultar afiliados (listado y por ID) | GET `/afiliados/` y GET `/afiliados/{id}` | `ListarAfiliadosUseCase` + `ObtenerAfiliadoPorIdUseCase` |
| HU-04 | Modificar datos de afiliado | PATCH `/afiliados/{id}` | `ActualizarAfiliadoUseCase` |
| HU-05 | Importar desde Google Sheets | POST `/sync/sheets/import` | `ImportSheetUseCase` + `ImportarAfiliadoUseCase.execute()` |
| HU-06 | Ciclo de corrección: hoja de pendientes + reimportar | Integrado en `POST /sync/sheets/import` y `POST /sync/sheets/reimport` | `ActualizarHojaPendientesUseCase` (UC6) |
| HU-07 | Dar de baja afiliado | DELETE `/afiliados/{id}` | `DarBajaAfiliadoUseCase` |
| HU-08 | Generar tabla de afiliados activos en Sheets | POST `/sync/sheets/export` | `ExportarAfiliadosSheetsUseCase` (UC8) |

### Endpoints expuestos

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/afiliados/import` | Importar afiliados por archivo/lista |
| POST | `/afiliados/` | Registrar afiliado manual |
| GET | `/afiliados/` | Listar afiliados |
| GET | `/afiliados/{afiliado_id}` | Obtener afiliado por ID |
| PATCH | `/afiliados/{afiliado_id}` | Actualizar afiliado |
| DELETE | `/afiliados/{afiliado_id}` | Dar de baja afiliado |
| POST | `/sync/sheets/import` | Importar desde Google Sheets + generar pendientes de corrección (HU-06) |
| POST | `/sync/sheets/export` | Exportar tabla de afiliados activos a Sheets |

## 3. Arquitectura del pipeline de importación
- Pipeline de dominio puro: `app/domain/services/importacion_pipeline.py` (función `procesar_fila`)
- UC único orquestador: `ImportarAfiliadoUseCase` en `core_importar_afiliado.py`
- Wrappers eliminados: `uc1a`, `uc1b`, `uc4` (indirección redundante)
- `ImportSheetUseCase` (`uc4a`) se conserva como caso de uso de lectura del Sheet

## 4. Puertos e implementaciones

| Puerto | Adapter | Responsabilidad |
|---|---|---|
| `SheetDataPort` | `GoogleSheetsAdapter` | Leer datos del Sheet |
| `SheetCorreccionPort` | `SheetsCorreccionAdapter` | Hoja de pendientes de corrección (filas con error resaltadas) |
| `SheetExportPort` | `SheetsExportAdapter` | Exportar tabla de afiliados activos |
| `AfiliadoQueryPort` | `AfiliadoQueryRepository` | Consultar afiliados |
| `AfiliadoCommandPort` | `AfiliadoCommandRepository` | Modificar afiliados |
| `AfiliadoImportacionPort` | `AfiliadoImportacionRepository` | Persistir afiliados importados |
| `DominioRepositoryPort` | `DominioRepository` | Resolver valores controlados |
| `DomicilioRepositoryPort` | `DomicilioRepository` | Resolver domicilios |
| `ErrorRepositoryPort` | `ErrorRepository` | Registrar errores de validación |
| `ImportacionRepositoryPort` | `ImportacionRepository` | Registrar procesos de importación |

## 5. Refactorización F1–F6
Se completó un plan de refactorización arquitectónica que incluyó:
- F1: Purificación del dominio (enum `Dominio`, sin ORMs en el core)
- F2: Fix AF-RN12 (row_number persiste en errores de validación)
- F3: Split del core/SRP (pipeline puro + UC único)
- F4: Deuda operativa (deps, env, tests, bug de domicilio)
- F5: Payload de errores unificado (`{"error": str}`) + lista de errores en respuesta
- F6: Documentación final

## 6. Criterios de validación aplicados
- Cada HU tiene su documentación en `docs/04_historias_usuario/HU-0X/` (5 archivos c/u)
- Los endpoints expuestos coinciden con la especificación de la HU correspondiente
- La DI cablea correctamente cada caso de uso en `dependency_injection.py`
- Los schemas Pydantic validan entrada/salida sin exponer campos internos

## 7. Resultado
La implementación de la API REST fue validada satisfactoriamente.
Las 8 historias de usuario están implementadas y documentadas.

## 8. Estado del proyecto
Fase 3 — Implementación API REST: **FINALIZADA**

El proyecto queda habilitado para avanzar a la Fase 4: Pruebas y validación.
