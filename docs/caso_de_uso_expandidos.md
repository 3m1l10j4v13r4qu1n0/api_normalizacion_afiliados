# Casos de Uso Expandidos
## Sistema de Normalización de Datos de Afiliados

---

## UC1 — Importar Afiliados

| Campo | Detalle |
|---|---|
| **Caso de Uso** | UC1: Importar Afiliados |
| **Actor Principal** | Sistema Cliente |
| **Actores Secundarios** | — |
| **Descripción** | Permite importar datos de afiliados al sistema para su validación, normalización y almacenamiento. |
| **Precondiciones** | El Sistema Cliente tiene datos de afiliados disponibles para enviar. |
| **Postcondiciones** | Los registros válidos quedan almacenados en la base de datos. Los errores quedan registrados. |

### Flujo Principal

| Paso | Actor | Acción |
|---|---|---|
| 1 | Sistema Cliente | Envía una lista de registros de afiliados via `POST /afiliados/import` |
| 2 | Sistema | Recibe los datos y los procesa uno a uno |
| 3 | Sistema | Valida los campos obligatorios de cada registro |
| 4 | Sistema | Normaliza el formato de los datos válidos (texto, DNI, fechas, etc.) |
| 5 | Sistema | Almacena los registros válidos en la base de datos PostgreSQL |
| 6 | Sistema | Devuelve un resumen con `cantidad_registros_procesados`, `cantidad_registros_validos` y `cantidad_errores` |

### Flujos Alternativos

| Paso | Condición | Acción |
|---|---|---|
| 3a | Un registro tiene campos obligatorios faltantes o inválidos | El sistema registra el error de validación con el campo y descripción, y continúa con el siguiente registro |
| 3b | El DNI del afiliado ya existe en la base de datos | El sistema registra el error como "DNI duplicado" y descarta el registro |
| 1a | El cuerpo del request está vacío o malformado | El sistema devuelve `400 Bad Request` con descripción del error |

### Excepciones

| Condición | Respuesta del Sistema |
|---|---|
| Error de conexión con la base de datos | Devuelve `500 Internal Server Error` |
| Todos los registros son inválidos | Devuelve resumen con `cantidad_registros_validos = 0` y todos los errores registrados |

---

## UC4 — Importar desde Google Sheets

| Campo | Detalle |
|---|---|
| **Caso de Uso** | UC4: Importar desde Google Sheets |
| **Actor Principal** | Usuario Administrativo |
| **Actores Secundarios** | Google Sheets |
| **Descripción** | El usuario inicia la importación de datos desde una hoja de cálculo de Google Sheets. La API lee los registros, los valida, normaliza y almacena. |
| **Precondiciones** | La hoja de Google Sheets existe, tiene el formato esperado y la API tiene credenciales de acceso configuradas. |
| **Postcondiciones** | Los registros válidos quedan almacenados en la base de datos. Los errores quedan registrados. |

### Flujo Principal

| Paso | Actor | Acción |
|---|---|---|
| 1 | Usuario Administrativo | Inicia la importación via `POST /sync/sheets/import` |
| 2 | Sistema | Se conecta a Google Sheets usando las credenciales configuradas |
| 3 | Google Sheets | Devuelve los registros de la hoja de cálculo |
| 4 | Sistema | Procesa los registros leídos uno a uno |
| 5 | Sistema | Valida los campos obligatorios de cada registro |
| 6 | Sistema | Normaliza el formato de los datos válidos |
| 7 | Sistema | Almacena los registros válidos en la base de datos PostgreSQL |
| 8 | Sistema | Devuelve un resumen con `cantidad_registros_procesados`, `cantidad_registros_validos` y `cantidad_errores` |

### Flujos Alternativos

| Paso | Condición | Acción |
|---|---|---|
| 5a | Un registro tiene campos obligatorios faltantes o inválidos | El sistema registra el error y continúa con el siguiente registro |
| 5b | El DNI del afiliado ya existe en la base de datos | El sistema registra el error como "DNI duplicado" y descarta el registro |
| 3a | La hoja de cálculo está vacía | El sistema devuelve un resumen con `cantidad_registros_procesados = 0` |

### Excepciones

| Condición | Respuesta del Sistema |
|---|---|
| Error de autenticación con Google Sheets | Devuelve `503 Service Unavailable` con descripción del error |
| La hoja de cálculo no existe o no es accesible | Devuelve `404 Not Found` con descripción del error |
| Error de conexión con la base de datos | Devuelve `500 Internal Server Error` |

---

## UC6 — Sincronizar cambios hacia Google Sheets

| Campo | Detalle |
|---|---|
| **Caso de Uso** | UC6: Sincronizar cambios hacia Google Sheets |
| **Actor Principal** | Usuario Administrativo |
| **Actores Secundarios** | Google Sheets |
| **Descripción** | El usuario sincroniza los datos modificados en el sistema de vuelta hacia la hoja de cálculo de Google Sheets para mantener la consistencia. |
| **Precondiciones** | Existen afiliados almacenados en la base de datos. La API tiene credenciales de acceso a Google Sheets configuradas. |
| **Postcondiciones** | La hoja de Google Sheets refleja el estado actual de los afiliados en el sistema. |

### Flujo Principal

| Paso | Actor | Acción |
|---|---|---|
| 1 | Usuario Administrativo | Inicia la sincronización via `POST /sync/sheets/export` |
| 2 | Sistema | Obtiene los afiliados activos y sus datos actualizados desde la base de datos |
| 3 | Sistema | Se conecta a Google Sheets usando las credenciales configuradas |
| 4 | Sistema | Actualiza las filas correspondientes en la hoja de cálculo |
| 5 | Google Sheets | Confirma la escritura de los datos |
| 6 | Sistema | Devuelve confirmación de la operación con cantidad de registros sincronizados |

### Flujos Alternativos

| Paso | Condición | Acción |
|---|---|---|
| 2a | No hay afiliados activos en la base de datos | El sistema devuelve una respuesta indicando que no hay datos para sincronizar |
| 4a | Un registro no puede escribirse en Sheets | El sistema registra el error y continúa con los demás registros |

### Excepciones

| Condición | Respuesta del Sistema |
|---|---|
| Error de autenticación con Google Sheets | Devuelve `503 Service Unavailable` con descripción del error |
| Error de conexión con la base de datos | Devuelve `500 Internal Server Error` |
| Fallo parcial en la escritura | Devuelve resumen indicando cuántos registros se sincronizaron y cuántos fallaron |