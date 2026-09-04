# HU-06: Especificación de API (Marcar errores en Google Sheets)

## Endpoint 1: Marcar errores en Google Sheets
- **Método**: `POST`
- **Ruta**: `/sync/sheets/import` (paso final del proceso de importación, UC4b)
- **Descripción**: Como parte de la importación, una vez procesados los registros, el sistema marca de forma masiva en la hoja las filas que tuvieron errores de validación, aplicando formato visual (fondo rojo).
- **Respuesta Éxito (201 Created)**:
```json
{
  "cantidad_registros_procesados": 10,
  "cantidad_registros_validos": 8,
  "cantidad_errores": 2
}
```
- **Respuesta**: La marcación es una operación interna del flujo de importación; el error en esta etapa no interrumpe el resumen devuelto.

## Notas
- La actualización se realiza en forma masiva (batch) para optimizar rendimiento (SH-UC4b-RN2).
- Solo se marcan las filas con errores (SH-UC4b-RN3).
- El fallo al marcar no interrumpe la importación (SH-UC4b-RN4).

---
