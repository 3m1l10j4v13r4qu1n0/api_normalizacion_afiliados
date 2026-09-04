# HU-04: Especificación de API (Actualizar afiliado)

## Endpoint 1: Actualizar afiliado
- **Método**: `PATCH`
- **Ruta**: `/afiliados/{afiliado_id}`
- **Descripción**: Actualiza los campos enviados de un afiliado existente. Todos los campos del payload son opcionales; solo se actualizan los que lleguen.
- **Request Body**:
```json
{
  "email": "nuevo@test.com",
  "telefono": "1122334455"
}
```
- **Respuesta Éxito (200 OK)**: Objeto `AfiliadoResponse` con el afiliado actualizado.
- **Respuesta Error (404 Not Found)**: El afiliado no existe.
- **Respuesta Error (409 Conflict)**: El email ya está en uso por otro afiliado.
- **Respuesta Error (422 Unprocessable Entity)**: Nombre o apellido vacío, o formato inválido.

## Notas
- El schema de entrada (`AfiliadoUpdate`) tiene todos los campos opcionales.
- `nombre` y `apellido` no pueden quedar vacíos (validación del schema).
- El email usa `EmailStr`, que valida el formato.

---
