# HU-05: Especificación de API (Importar desde Google Sheets)

## Endpoint 1: Importar desde Google Sheets
- **Método**: `POST`
- **Ruta**: `/sync/sheets/import`
- **Descripción**: Lee los registros de afiliados desde una hoja de Google Sheets, los valida, normaliza y almacena en la base de datos.
- **Request**: Sin body (el rango y la hoja se configuran en el sistema).
- **Respuesta Éxito (201 Created)**:
```json
{
  "cantidad_registros_procesados": 10,
  "cantidad_registros_validos": 8,
  "cantidad_errores": 2
}
```
- **Respuesta Error (503 Service Unavailable)**: Error de autenticación con Google Sheets.
- **Respuesta Error (404 Not Found)**: La hoja no existe o no es accesible.
- **Respuesta Error (500 Internal Server Error)**: Error de conexión con la base de datos.

## Notas
- El flujo de lectura devuelve una lista de `InputRow`, cada una con su `row_number` y un diccionario de encabezados/valores.
- Las filas vacías no se procesan (SH-UC4a-RN3).

---
