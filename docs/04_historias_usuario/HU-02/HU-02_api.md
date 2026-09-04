# HU-02: Especificación de API (Registrar afiliado manualmente)

## Endpoint 1: Registrar afiliado (alta manual)
- **Método**: `POST`
- **Ruta**: `/afiliados/`
- **Descripción**: Carga un afiliado individual para su validación, normalización y almacenamiento.
- **Request Body**:
```json
{
  "apellido": "garcia",
  "nombre": "juan",
  "dni": "12345678",
  "numero_legajo": "L-002",
  "fecha_nacimiento": "1990-05-10",
  "email": "juan@test.com",
  "id_estado_afiliado": 1
}
```
- **Respuesta Éxito (201 Created)**:
```json
{
  "cantidad_registros_procesados": 1,
  "cantidad_registros_validos": 1,
  "cantidad_errores": 0
}
```
- **Respuesta Error (409 Conflict)**: DNI duplicado.
- **Respuesta Error (422 Unprocessable Entity)**: Datos de entrada inválidos o con campos obligatorios faltantes.

## Notas
- El schema de entrada (`AfiliadoCreate`) hereda de `AfiliadoImportItem`.
- Los valores controlados (`id_genero`, `id_estado_civil`, `id_nivel_educativo`, `id_relacion_dependencia`, `id_estado_afiliado`) se envían como IDs.

---
