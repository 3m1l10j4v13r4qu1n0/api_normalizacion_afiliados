# HU-06: Caso de Uso Expandido (Marcar errores en Google Sheets)

**Actor Principal**: Sistema
**Precondición**: La importación (UC4/HU-05) fue ejecutada y existen errores registrados (`ErrorValidacion`) con su `row_number`.

## Flujo Principal (Éxito)
1. El sistema finaliza el proceso de importación.
2. El sistema obtiene la lista de errores de validación generados.
3. El sistema extrae los `row_number` de las filas con errores.
4. El sistema elimina duplicados de filas para optimizar la operación.
5. El sistema construye una solicitud de actualización masiva (batch).
6. El sistema envía la actualización a Google Sheets.
7. El sistema aplica formato visual (fondo rojo) a las filas o celdas afectadas.

## Flujo Alternativo 1: No hay errores
1. El sistema detecta que no hay errores registrados.
2. No se realiza ninguna actualización en la hoja.

## Flujo Alternativo 2: Error al actualizar Google Sheets
1. Ocurre un error durante la actualización.
2. El sistema registra el fallo.
3. El proceso de importación no se ve afectado.

## Postcondición
- Las filas con errores quedan visualmente marcadas (fondo rojo) en la hoja.
- No se modifican los datos originales de las filas válidas (AF-RN15).