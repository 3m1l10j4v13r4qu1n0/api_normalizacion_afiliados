# HU-06: Modelos de Datos (Hoja de pendientes de corrección en Google Sheets)

## Entidades Involucradas
Basado en el modelo global, esta HU usa la entidad `ErrorValidacion` para conocer qué filas volcar como pendientes:

### 1. ErrorValidacion
- `id` (int).
- `registro_origen` (String): Referencia al registro con error.
- `campo` (String): Campo que falló.
- `descripcion_error` (String).
- `row_number` (int): Número de fila original del sheet. **(Campo crítico para el ciclo de corrección)**
- `importacion_id` (FK a Importacion).

### 2. Hoja "Pendientes de corrección" (Google Sheets)
Hoja nueva dentro de la misma planilla (se crea con `add_worksheet` si no existe, se limpia y reescribe en cada importación). Estructura:

- Columnas originales del sheet de origen (las mismas que se importan).
- Columna extra `motivo del error` (String): descripción/es del porqué falló la fila (concatenación `campo: descripción`).
- Formato: todas las filas pendientes resaltadas con fondo rojo (batch `A{r}:Z{r}`).

## Reglas de Integridad y Base de Datos
- Los errores deben reflejarse en Google Sheets como pendientes de corrección, listas para ser editadas y reimportadas (SH-UC4b-RN1).
- La actualización de pendientes debe realizarse en forma masiva (batch) (SH-UC4b-RN2).
- Solo se vuelcan filas con errores en la hoja de pendientes (SH-UC4b-RN3).
- La operación no debe interrumpir el flujo principal de importación (SH-UC4b-RN4).
- La generación de pendientes no modifica los datos locales del sistema (AF-RN15).
- Las filas corregidas y reimportadas dejan de figurar como pendientes; solo permanecen las que siguen fallando.