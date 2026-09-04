# HU-03: Especificación de API (Consultar afiliados)

## Endpoint 1: Listar afiliados
- **Método**: `GET`
- **Ruta**: `/afiliados/`
- **Descripción**: Obtiene la lista de afiliados almacenados en el sistema.
- **Respuesta Éxito (200 OK)**:
```json
[
  {
    "id": 1,
    "apellido": "GARCIA",
    "nombre": "JUAN",
    "dni": "12345678",
    "numero_legajo": "L-001",
    "fecha_nacimiento": "1990-05-10",
    "email": "juan@test.com"
  }
]
```

## Endpoint 2: Obtener afiliado por ID
- **Método**: `GET`
- **Ruta**: `/afiliados/{afiliado_id}`
- **Descripción**: Obtiene los datos de un afiliado específico por su identificador.
- **Respuesta Éxito (200 OK)**: Objeto `AfiliadoResponse` con los datos del afiliado.
- **Respuesta Error (404 Not Found)**: El afiliado no existe.

## Notas
- La respuesta usa el schema `AfiliadoResponse`, que filtra campos internos y no expone datos sensibles.

---
