# HU-05: Modelos de Datos (Importar desde Google Sheets)

## Entidades Involucradas
Basado en el modelo global, esta HU usa la entidad `InputRow` como estructura intermedia y persiste en `Afiliado`, `Importacion` y `ErrorValidacion`.

### 1. Afiliado
- `id` (int): Identificador único.
- `apellido`, `nombre` (String): Normalizados (mayúsculas).
- `dni` (String): Único, sin puntos ni guiones. **(Campo crítico de unicidad)**
- `numero_legajo` (String): Único.
- `fecha_nacimiento` (date).
- `email` (String, nullable): Único.
- Valores controlados vía FK.
- `row_number` (int, representado en `ErrorValidacion`): referencia a la fila original del sheet.

### 2. InputRow (estructura intermedia de lectura)
- `row_number` (int): Índice/numero de fila original en la hoja. **(Campo crítico, SH-UC4a-RN2)**
- `value` (dict): Diccionario con los encabezados mapeados y sus valores.

### 3. Importacion / ErrorValidacion
- Registran el proceso y los errores, asociando cada error a su `row_number` / `registro_origen`.

## Reglas de Integridad y Base de Datos
- Los encabezados se mapean a variables internas del sistema (SH-UC4a-RN1).
- Cada fila conserva su `row_number` original (SH-UC4a-RN2).
- No se procesan filas vacías (SH-UC4a-RN3).
- Solo se persisten los registros válidos (AF-RN11) y la importación continúa ante errores (AF-RN13).