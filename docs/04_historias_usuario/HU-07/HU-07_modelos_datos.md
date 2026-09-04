# HU-07: Modelos de Datos (Dar de baja afiliado)

## Entidades Involucradas
Basado en el modelo global, esta HU modifica el estado de la entidad `Afiliado`:

### 1. Afiliado
- `id` (int): Identificador único del afiliado a dar de baja. **(Campo crítico)**
- `id_estado_afiliado` (int): FK a `EstadoAfiliado`. Se asigna el valor inactivo (2) en la baja lógica. **(Campo crítico)**

### 2. EstadoAfiliado (entidad de dominio)
- `id` (int): Valor controlado (`1` = Activo, `2` = Inactivo).
- `descripcion` (String).

## Reglas de Integridad y Base de Datos
- La eliminación de un afiliado debe ser baja lógica, marcando su estado como inactivo (AF-RN16).
- El registro no se elimina físicamente.
- Los afiliados con estado inactivo no deben aparecer en los listados de activos (HU-03).