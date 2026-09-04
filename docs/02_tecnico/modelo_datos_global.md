# Modelo de Datos Global (Entidades Base)

Estas entidades son la base sobre la cual se construyen las HU específicas.

- **Afiliado**: `id`, `apellido`, `nombre`, `fecha_nacimiento`, `dni` (único), `email` (único), `telefono`, `numero_legajo` (único), `fecha_ingreso`, `fecha_alta`, `titulo_obtenido`, `marca_temporal_creacion`, `marca_temporal_actualizacion`. Relaciones: `genero`, `estado_civil`, `nivel_educativo`, `relacion_dependencia`, `estado_afiliado`, `domicilio`, `importacion`.
- **Domicilio**: `id`, `direccion`, `codigo_postal`. Relación: `localidad`.
- **Localidad**: `id`, `nombre`. Relación: `provincia`.
- **Provincia**: `id`, `nombre`.
- **Importacion**: `id`, `fecha_importacion`, `cantidad_registros`, `cantidad_errores`, `estado`. Relaciones: genera `Afiliado` y `ErrorValidacion`.
- **ErrorValidacion**: `id`, `registro_origen`, `campo`, `descripcion_error`, `fecha_error`, `row_number`. Relación: `importacion`.
- **Genero / EstadoCivil / NivelEducativo / RelacionDependencia / EstadoAfiliado**: entidades de dominio, cada una con `id` y `descripcion`.

## Reglas de Integridad Globales
- `dni`, `email` y `numero_legajo` deben ser únicos.
- Nombre, apellido y DNI son obligatorios.
- Los valores controlados (género, estado civil, nivel educativo, relación de dependencia, estado del afiliado) se almacenan como entidades de dominio.
- La información geográfica se separa en entidades independientes (Domicilio → Localidad → Provincia).
- Los datos se almacenan normalizados (nombres en mayúsculas, DNI sin puntos ni guiones).