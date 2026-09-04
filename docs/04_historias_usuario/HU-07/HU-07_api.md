# HU-07: Especificación de API (Dar de baja afiliado)

## Endpoint 1: Dar de baja afiliado
- **Método**: `DELETE`
- **Ruta**: `/afiliados/{afiliado_id}`
- **Descripción**: Marca a un afiliado como inactivo (baja lógica). El registro no se elimina físicamente.
- **Respuesta Éxito (200 OK)**: Afiliado dado de baja correctamente.
- **Respuesta Error (404 Not Found)**: El afiliado no existe.

## Notas
- La baja se realiza marcando el `id_estado_afiliado = 2` (Inactivo, según seed).
- El registro permanece en la base de datos (AF-RN16).

---
