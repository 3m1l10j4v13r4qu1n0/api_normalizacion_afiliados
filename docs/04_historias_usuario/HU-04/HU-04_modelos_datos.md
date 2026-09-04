# HU-04: Modelos de Datos (Actualizar afiliado)

## Entidades Involucradas
Basado en el modelo global, esta HU actualiza la entidad `Afiliado`:

### 1. Afiliado
- `id` (int): Identificador único del afiliado a actualizar. **(Campo crítico)**
- `apellido`, `nombre` (String): No pueden quedar vacíos al actualizar.
- `dni` (String): Único, sin puntos ni guiones.
- `numero_legajo` (String): Único.
- `email` (String, nullable): Único y con formato válido. **(Campo crítico de unicidad)**
- `telefono`, `fecha_ingreso`, `fecha_alta`, `titulo_obtenido` (opcionales).
- `id_genero`, `id_estado_civil`, `id_nivel_educativo`, `id_relacion_dependencia`, `id_estado_afiliado` (FK).

## Reglas de Integridad y Base de Datos
- `dni`, `email` y `numero_legajo` deben ser únicos (`UNIQUE` constraint).
- Al actualizar, se debe verificar que el email no esté en uso por **otro** afiliado (excluyendo el id actual).
- Nombre y apellido no pueden quedar vacíos (AF-RN05).
- Los datos deben almacenarse normalizados (AF-RN08, AF-RN09).