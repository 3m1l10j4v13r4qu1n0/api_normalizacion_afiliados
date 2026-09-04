# HU-08: Especificación de API (Generar tabla de afiliados en Sheets)

## Endpoint 1: Exportar tabla de afiliados a Google Sheets
- **Método**: `POST`
- **Ruta**: `/sync/sheets/export`
- **Descripción**: Genera o actualiza una hoja de Google Sheets con los afiliados almacenados, ordenados alfabéticamente, mostrando nombre y apellido concatenados, edad calculada y datos relevantes.
- **Respuesta Éxito (200 OK)**:
```json
{
  "cantidad_registros_procesados": 10,
  "mensaje": "Tabla generada correctamente"
}
```
- **Respuesta Error (404 Not Found)**: No hay afiliados activos para exportar.
- **Respuesta Error (503 Service Unavailable)**: Error de autenticación con Google Sheets.
- **Respuesta Error (500 Internal Server Error)**: Error de conexión con la base de datos.

## Estructura de la tabla generada
| Nombre y Apellido | Edad | Datos Relevantes |
| ----------------- | ---- | ---------------- |

## Notas
- Si la hoja no existe, el sistema la crea; si existe, la limpia o actualiza (RF17).
- La edad se calcula dinámicamente (`edad = año_actual - fecha_nacimiento.año`) y no se persiste (AF-RN19).
- Solo se exportan datos relevantes, no todos los campos del sistema (AF-RN20).

---