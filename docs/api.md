# Especificación de API REST
## Sistema de Normalización de Datos de Afiliados

### 1. Introducción
Este documento describe los endpoints de la API REST para la gestión de afiliados.

La API permite importar, consultar, actualizar y sincronizar datos de afiliados.

Todas las respuestas de la API se devuelven en formato JSON.

---

### 2. Afiliados

---

## Importar afiliados

Endpoint:
```
POST /afiliados/import
```

Descripción:
Permite importar múltiples registros de afiliados para su validación y normalización.

Resultado esperado:
- Registros válidos almacenados
- Errores registrados

Respuesta esperada:
- cantidad_registros_procesados
- cantidad_registros_validos
- cantidad_errores

---

## Importar afiliado

Endpoint:
```
POST /afiliado/
```

Descripción:
Permite agregar a un afiliado para su validación y normalización.

Resultado esperado:
- Registros válidos almacenados
- Errores registrados

Respuesta esperada:
- cantidad_registros_procesados
- cantidad_registros_validos
- cantidad_errores

---

## Consultar afiliados

Endpoint:
```
GET /afiliados
```

Descripción:
Obtiene la lista de afiliados almacenados.

Respuesta esperada:
Lista de afiliados.

---

## Consultar afiliado por ID

Endpoint:
```
GET /afiliados/{id}
```

Descripción:
Obtiene la información de un afiliado específico.

Respuesta esperada:
Datos del afiliado.

---

## Actualizar afiliado

Endpoint:
```
PUT /afiliados/{id}
```

Descripción:
Actualiza los datos de un afiliado existente.

Resultado esperado:
Afiliado actualizado correctamente.

---

## Eliminar afiliado

Endpoint:
```
DELETE /afiliados/{id}
```

Descripción:
Marca un afiliado como inactivo en el sistema (baja lógica).

Resultado esperado:
- Afiliado marcado como inactivo
- El registro no se elimina físicamente de la base de datos

---

### 3. Sincronización

Importar desde Google Sheets

Endpoint:
```
POST /sync/sheets/import
```
Descripción: 
Lee los registros de afiliados desde una hoja de cálculo de Google Sheets, los valida, normaliza y almacena en la base de datos.

Resultado esperado:

- Registros válidos almacenados
- Errores registrados

Respuesta esperada:

- `cantidad_registros_procesados`
- `cantidad_registros_validos`
- `cantidad_errores`

---
## Sincronizar con Google Sheets

Endpoint:
```
POST /sync/sheets/export
```

Descripción:
El usuario puede generar una tabla en Google Sheets que contenga los afiliados almacenados en la base de datos.
Si la hoja no existe, el sistema la crea; si ya existe, la actualiza mostrando los datos estructurados.


Resultado esperado:
Se genera o actualiza una hoja en Google Sheets con los afiliados ordenados, mostrando información clara y útil, incluyendo la edad calculada.

---

### 4. Manejo de errores

La API debe devolver mensajes de error cuando:

- El afiliado no existe
- Los datos son inválidos
- La importación falla
- La sincronización falla

Formato general de error:

```
{
  "error": "descripcion del error"
}
```
