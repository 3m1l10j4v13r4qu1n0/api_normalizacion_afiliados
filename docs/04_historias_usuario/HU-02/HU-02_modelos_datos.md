# HU-02: Modelos de Datos (Registrar afiliado manualmente)

## Entidades Involucradas
Basado en el modelo global, esta HU opera sobre la entidad `Afiliado`:

### 1. Afiliado
- `id` (int): Identificador único.
- `apellido` (String): Apellido normalizado (mayúsculas). **(Campo crítico)**
- `nombre` (String): Nombre normalizado (mayúsculas).
- `dni` (String): Documento único, sin puntos ni guiones. **(Campo crítico de unicidad)**
- `numero_legajo` (String): Único.
- `fecha_nacimiento` (date).
- `email` (String, nullable): Único y con formato válido.
- `telefono`, `fecha_ingreso`, `fecha_alta`, `titulo_obtenido` (opcionales).
- `id_genero`, `id_estado_civil`, `id_nivel_educativo`, `id_relacion_dependencia`, `id_estado_afiliado` (FK a entidades de dominio).

## Reglas de Integridad y Base de Datos
- `dni`, `email` y `numero_legajo` deben ser únicos (`UNIQUE` constraint).
- Nombre, apellido y DNI son obligatorios (AF-RN05).
- El afiliado debe tener un estado definido (AF-RN06).
- Los datos deben almacenarse normalizados (AF-RN08, AF-RN09, AF-RN10).
- Los valores controlados deben existir en sus tablas de dominio (AF-RN17).