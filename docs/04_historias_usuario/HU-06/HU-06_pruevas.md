# HU-06: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Generar pendientes con filas con errores (Caso Positivo)
- **Dado** que la importación generó errores en ciertas filas (con su `row_number`).
- **Cuando** finaliza el proceso de importación.
- **Entonces** el sistema vuelca esas filas en la hoja "Pendientes de corrección" con sus columnas, el "motivo del error" y fondo rojo.

## Escenario 2: Actualización masiva (Caso de Rendimiento)
- **Dado** que existen múltiples filas con errores.
- **Cuando** se procede a volcarlas en la hoja de pendientes.
- **Entonces** el sistema realiza una única actualización masiva (batch) del contenido y del formato.

## Escenario 3: Filas válidas sin cambios (Caso Negativo)
- **Dado** que un registro es válido.
- **Cuando** se generan las pendientes.
- **Entonces** la fila del registro válido no se altera ni se vuelca como pendiente.

## Escenario 4: Error al actualizar la hoja (Caso Borde)
- **Dado** que falla la actualización en Google Sheets.
- **Cuando** ocurre el error.
- **Entonces** el sistema registra el fallo internamente.
- **Y** no interrumpe el proceso de importación (SH-UC4b-RN4).

## Escenario 5: Reimportar pendientes corregidas (Ciclo de corrección)
- **Dado** que el usuario corrigió filas en la hoja "Pendientes de corrección".
- **Cuando** se reimporta desde esa hoja (`POST /sync/sheets/reimport`).
- **Entonces** las filas corregidas se importan y desaparecen de las pendientes.
- **Y** solo permanecen resaltadas las que siguen fallando.

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [x] `test_actualizar_hoja_pendientes.py` — UC6: agrupa errores por fila, mapea `row_number` → fila cruda, arma motivo del error, guarda solo encabezados sin errores, no captura el error del port.
- [x] `test_sheets_correccion_adapter.py` — adapter: delega `guardar_pendientes`/`leer_pendientes` en el cliente y propaga `SincronizacionError`.
- [x] `test_sheets_correccion_client.py` — cliente gspread: crea la hoja si no existe (`add_worksheet`), reutiliza y limpia la existente, vuelca encabezados + filas en A1, resalta todas las pendientes en rojo con una sola `batch_format`, sin pendientes no resalta nada, `leer_pendientes` y resolución de rango por nombre de hoja.
- [x] `test_sync_sheets_import.py` — endpoints `/sync/sheets/import` y `/sync/sheets/reimport`: generan pendientes con filas y errores, el fallo al actualizar no interrumpe (RN4), sin errores deja pendientes vacías, y `/reimport` lee la hoja de pendientes como origen (SH-UC4b-RN1).

**Cobertura verificada (2026-09-11):** los 5 escenarios de aceptación están cubiertos, incluido el ciclo de corrección completo (importar → corregir en la hoja de pendientes → reimportar).