# HU-08: Modelos de Datos (Generar tabla de afiliados en Sheets)

## Entidades Involucradas
Basado en el modelo global, esta HU lee la entidad `Afiliado` y exporta a una hoja de Google Sheets:

### 1. Afiliado (concepto derivado para la tabla)
- `nombre` (String): Usado para el nombre normalizado. **(Campo crítico)**
- `apellido` (String): Usado para el apellido normalizado. **(Campo crítico)**
- `fecha_nacimiento` (date): Usado solo para calcular la edad dinámicamente. **(Campo crítico de cálculo)**
- `dni` (String): Dato relevante a exportar.
- `numero_legajo` (String): Dato relevante a exportar.
- `id_estado_afiliado` (FK): Permite filtrar solo afiliados activos.
- `email` (String, nullable): Dato relevante a exportar.

### 2. Tabla de Google Sheets (destino)
- `Nombre y Apellido` (String): Concatena `nombre` y `apellido`.
- `Edad` (entero calculado): `edad = año_actual - año_nacimiento`.
- `Datos Relevantes`: Subconjunto de datos del afiliado (no todos los campos del sistema).

## Reglas de Integridad y Base de Datos
- Los afiliados deben ordenarse alfabéticamente por nombre y apellido (SH-UC6-RN1).
- Solo se actualiza una vez la tabla en Google Sheets; si el destino existe, se limpia y regraba (SH-UC6-RN2).
- La edad se calcula en tiempo de ejecución y no se persiste (AF-RN19).
- Solo se exportan datos relevantes, no todos los campos (AF-RN20).