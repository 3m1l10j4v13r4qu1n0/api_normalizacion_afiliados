# HU-06: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Marcar filas con errores (Caso Positivo)
- **Dado** que la importación generó errores en ciertas filas (con su `row_number`).
- **Cuando** finaliza el proceso de importación.
- **Entonces** el sistema marca esas filas en Google Sheets con fondo rojo.

## Escenario 2: Actualización masiva (Caso de Rendimiento)
- **Dado** que existen múltiples filas con errores.
- **Cuando** se procede a marcarlas.
- **Entonces** el sistema agrupa los `row_number` y realiza una única actualización masiva (batch).

## Escenario 3: Filas válidas sin cambios (Caso Negativo)
- **Dado** que un registro es válido.
- **Cuando** se marcan errores en la hoja.
- **Entonces** la fila del registro válido no se altera.

## Escenario 4: Error al actualizar la hoja (Caso Borde)
- **Dado** que falla la actualización en Google Sheets.
- **Cuando** ocurre el error.
- **Entonces** el sistema registra el fallo internamente.
- **Y** no interrumpe el proceso de importación.

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [x] `test_marcar_filas_con_errores()` — `tests/unit/domian/services/test_marcar_errores_sheets.py` + `test_sheets_marking_client.py` (fondo rojo en `A{r}:Z{r}`)
- [x] `test_actualizacion_masiva_de_filas()` — `test_sheets_marking_client.py::test_una_sola_actualizacion_masiva` (una sola `batch_format` para todas las filas)
- [x] `test_no_alterar_filas_validas()` — `test_marcar_errores_sheets.py` + `test_sheets_marking_adapter.py` (lista vacía no toca la hoja)

**Cobertura verificada (2026-09-11):** los 4 escenarios de aceptación están cubiertos, incluido el escenario 4 (SH-UC4b-RN4: el fallo al marcar no interrumpe la importación, verificado a nivel del router en `test_sync_sheets_import.py`).