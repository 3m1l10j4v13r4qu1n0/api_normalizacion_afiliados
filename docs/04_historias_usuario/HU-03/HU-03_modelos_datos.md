# HU-03: Modelos de Datos (Consultar afiliados)

## Entidades Involucradas
Basado en el modelo global, esta HU consulta la entidad `Afiliado` (lectura, sin cambios de esquema):

### 1. Afiliado
- `id` (int): Identificador único de consulta. **(Campo crítico)**
- `apellido` (String): Apellido normalizado.
- `nombre` (String): Nombre normalizado.
- `dni` (String): Documento único.
- `numero_legajo` (String): Único.
- `fecha_nacimiento` (date).
- `email` (String, nullable).
- `telefono`, `fecha_ingreso`, `fecha_alta`, `titulo_obtenido` (opcionales).
- `id_genero`, `id_estado_civil`, `id_nivel_educativo`, `id_relacion_dependencia`, `id_estado_afiliado` (FK).

## Reglas de Integridad y Base de Datos
- La consulta por `id` debe aprovechar el índice de la clave primaria.
- Los afiliados con baja lógica (estado inactivo) no deben aparecer en los listados activos (AF-RN16).
- La respuesta no expone campos internos o sensibles fuera del `AfiliadoResponse`.