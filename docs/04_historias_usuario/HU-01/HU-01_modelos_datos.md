# HU-01: Modelos de Datos (Importar afiliados desde API)

## Entidades Involucradas
Basado en el modelo global, esta HU impacta directamente las siguientes entidades:

### 1. Afiliado
- `id` (int): Identificador único.
- `apellido` (String): Apellido normalizado (mayúsculas). **(Campo crítico)**
- `nombre` (String): Nombre normalizado (mayúsculas).
- `dni` (String): Documento único, sin puntos ni guiones. **(Campo crítico de unicidad)**
- `numero_legajo` (String): Único.
- `fecha_nacimiento` (date): Fecha de nacimiento.
- `email` (String, nullable): Email único y con formato válido.
- `telefono`, `fecha_ingreso`, `fecha_alta`, `titulo_obtenido` (opcionales).
- `id_genero`, `id_estado_civil`, `id_nivel_educativo`, `id_relacion_dependencia`, `id_estado_afiliado` (FK a entidades de dominio).

### 2. Importacion
- `id` (int): Identificador del proceso de importación.
- `fecha_importacion` (Datetime).
- `cantidad_registros` (int).
- `cantidad_errores` (int).
- `estado` (String).

### 3. ErrorValidacion
- `id` (int).
- `registro_origen` (String): Referencia a la fila/índice del registro con error.
- `campo` (String): Campo que falló.
- `descripcion_error` (String): Detalle del error.
- `row_number` (int): Número de fila/índice del registro.
- `importacion_id` (FK a Importacion).

## Reglas de Integridad y Base de Datos
- `dni`, `email` y `numero_legajo` deben ser únicos (`UNIQUE` constraint).
- Los registros inválidos NO deben persistirse (AF-RN11).
- La importación debe continuar aunque existan registros inválidos (AF-RN13).
- Cada error debe poder asociarse al registro de origen mediante `row_number` / `registro_origen` (AF-RN12).