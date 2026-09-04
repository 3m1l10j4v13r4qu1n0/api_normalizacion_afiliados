# HU-06: Modelos de Datos (Marcar errores en Google Sheets)

## Entidades Involucradas
Basado en el modelo global, esta HU usa la entidad `ErrorValidacion` para conocer qué filas marcar:

### 1. ErrorValidacion
- `id` (int).
- `registro_origen` (String): Referencia al registro con error.
- `campo` (String): Campo que falló.
- `descripcion_error` (String).
- `row_number` (int): Número de fila original del sheet. **(Campo crítico para la marcación)**
- `importacion_id` (FK a Importacion).

## Reglas de Integridad y Base de Datos
- Los errores deben reflejarse en el origen de datos (Google Sheets) (SH-UC4b-RN1).
- La actualización debe realizarse en forma masiva (batch) (SH-UC4b-RN2).
- Solo se deben marcar filas con errores (SH-UC4b-RN3).
- La operación no debe interrumpir el flujo principal de importación (SH-UC4b-RN4).
- La marcación no modifica los datos locales del sistema (AF-RN15).