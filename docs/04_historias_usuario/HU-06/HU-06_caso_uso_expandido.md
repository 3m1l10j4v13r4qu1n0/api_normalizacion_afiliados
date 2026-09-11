# HU-06: Caso de Uso Expandido (Hoja de pendientes de corrección en Google Sheets)

**Actor Principal**: Sistema
**Precondición**: La importación (UC4/HU-05) fue ejecutada y existen errores registrados (`ErrorValidacion`) con su `row_number`.

## Flujo Principal (Éxito)
1. El sistema finaliza el proceso de importación.
2. El sistema obtiene la lista de errores de validación generados.
3. El sistema agrupa los errores por fila (`row_number`), eliminando duplicados.
4. El sistema obtiene el contenido crudo de cada fila con error desde la fuente.
5. El sistema construye la hoja "Pendientes de corrección" (misma planilla): columnas originales + columna "motivo del error".
6. El sistema vuelca las filas pendientes con formato visual (fondo rojo) de forma masiva (batch).
7. Si la hoja ya existe, el sistema la limpia y la reescribe con las pendientes de la última importación.

## Flujo Alternativo 1: No hay errores
1. El sistema detecta que no hay errores registrados.
2. La hoja de pendientes queda únicamente con los encabezados (refleja "sin pendientes").

## Flujo Alternativo 2: Error al actualizar Google Sheets
1. Ocurre un error durante la actualización.
2. El sistema registra el fallo.
3. El proceso de importación no se ve afectado (SH-UC4b-RN4).

## Flujo Alternativo 3: Reimportación de pendientes corregidas
1. El usuario corrige/completa los datos en la hoja "Pendientes de corrección".
2. El sistema reimporta desde esa hoja (endpoint `POST /sync/sheets/reimport`).
3. Las filas que ahora son válidas se importan y desaparecen de las pendientes.
4. Las filas que siguen fallando permanecen en la hoja, resaltadas en rojo (se regenera la hoja).

## Postcondición
- Las filas con errores quedan en la hoja de pendientes de corrección, resaltadas en rojo, con su motivo.
- No se modifican los datos originales de las filas válidas ni los datos locales del sistema (AF-RN15).