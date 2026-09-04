# HU-01: Especificación de API (Importar afiliados desde API)

## Endpoint 1: Importar lista de afiliados
- **Método**: `POST`
- **Ruta**: `/afiliados/import`
- **Descripción**: Importa una lista de afiliados para su validación, normalización y almacenamiento. Los campos del payload son opcionales a propósito para permitir que lleguen datos "sucios" y que sea el dominio quien los valide.
- **Request Body**:
```json
{
  "afiliados": [
    {
      "apellido": "garcia",
      "nombre": "juan",
      "dni": "12.345.678",
      "numero_legajo": "L-001",
      "fecha_nacimiento": "1990-05-10",
      "email": "juan@test.com",
      "id_estado_afiliado": 1
    }
  ]
}
```
- **Respuesta Éxito (201 Created)**:
```json
{
  "cantidad_registros_procesados": 4,
  "cantidad_registros_validos": 3,
  "cantidad_errores": 1
}
```
- **Respuesta Error (422 Unprocessable Entity)**: Estructura de request inválida (ej. `afiliados` no es una lista).

## Campos relevantes del payload (AfiliadoImportItem)
- `apellido`, `nombre`, `dni`, `numero_legajo` (String, opcional).
- `fecha_nacimiento` (date, opcional).
- `email` (EmailStr, opcional — valida formato).
- `telefono`, `fecha_ingreso`, `fecha_alta`, `titulo_obtenido` (opcionales).
- `id_genero`, `id_estado_civil`, `id_nivel_educativo`, `id_relacion_dependencia`, `id_estado_afiliado` (int, opcionales).

---
