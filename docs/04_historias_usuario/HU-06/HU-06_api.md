# HU-06: Especificación de API (Hoja de pendientes de corrección en Google Sheets)

## Endpoint 1: Importar y generar pendientes
- **Método**: `POST`
- **Ruta**: `/sync/sheets/import` (paso final del proceso de importación, UC4b)
- **Descripción**: Una vez procesados los registros, el sistema crea/actualiza la hoja "Pendientes de corrección" (misma planilla) con las filas que tuvieron errores de validación. Cada fila pendiente conserva sus columnas originales, incorpora una columna "motivo del error" y queda resaltada en rojo.
- **Respuesta Éxito (201 Created)**:
```json
{
  "cantidad_registros_procesados": 10,
  "cantidad_registros_validos": 8,
  "cantidad_errores": 2,
  "errores": [
    { "campo": "email", "descripcion_error": "email inválido", "row_number": 3 }
  ]
}
```
- **Respuesta**: La actualización de pendientes es una operación interna del flujo de importación; el error en esta etapa no interrumpe el resumen devuelto (SH-UC4b-RN4).

## Endpoint 2: Reimportar pendientes corregidas
- **Método**: `POST`
- **Ruta**: `/sync/sheets/reimport`
- **Descripción**: Lee la hoja "Pendientes de corrección" como fuente, aplica el mismo pipeline de validación/normalización/persistencia y regenera la hoja con lo que continúe fallando. Las filas corregidas se importan y desaparecen de las pendientes.
- **Respuesta Éxito (201 Created)**: mismo JSON del endpoint de importación.
- **Precondición**: haber ejecutado al menos una importación (la hoja de pendientes existe).
- **Respuesta de error**: si la hoja de pendientes no existe, se responde `SincronizacionError` (500).

## Notas
- La actualización de pendientes se realiza en forma masiva (batch) para optimizar rendimiento (SH-UC4b-RN2).
- Solo se vuelcan las filas con errores en la hoja de pendientes (SH-UC4b-RN3).
- El fallo al actualizar pendientes no interrumpe la importación (SH-UC4b-RN4).

---