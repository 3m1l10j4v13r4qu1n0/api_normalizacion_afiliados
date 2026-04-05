# Casos de Uso Expandidos
## Sistema de Normalización de Datos de Afiliados

---

## UC1 — Importar Afiliado/s (expandido)
| Campo                               | Detalle           |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Caso de Uso**                     | UC1 — Importar Afiliado/s |
| **Actor Principal**                 | Sistema Cliente           |
| **Actores Secundarios**             | Usuario Administrativo (en caso de carga manual)|
| **Descripción**                     | Permite importar datos de uno o múltiples afiliados al sistema para su validación, normalización y almacenamiento, independientemente del origen de los datos (API o ingreso manual).|
| **Precondiciones**                  | - El sistema se encuentra operativo.<br>- Los datos enviados contienen la estructura mínima requerida.<br>- Existen reglas de validación definidas para afiliados. |
| **Postcondiciones**                 | - Los registros válidos son almacenados en el sistema.<br>- Los registros inválidos son rechazados y registrados como errores.<br>- Se genera un resultado con métricas del proceso.|
| **Flujo Principal**                 | 1. El sistema recibe datos de uno o múltiples afiliados.<br>2. El sistema identifica el tipo de entrada (individual o lista).<br>3. El sistema valida los datos recibidos según las reglas de negocio.<br>4. El sistema normaliza la información.<br>5. El sistema almacena los registros válidos.<br>6. El sistema registra errores en caso de existir.<br>7. El sistema devuelve el resultado del proceso.|
| **Flujos Alternativos**             | **A1 — Datos inválidos en registro individual**<br>1. El sistema detecta errores en los datos.<br>2. El sistema detiene el proceso.<br>3. Se informa el error al usuario.<br><br>**A2 — Datos inválidos en procesamiento masivo**<br>1. El sistema detecta errores en uno o más registros.<br>2. El sistema continúa procesando el resto.<br>3. Se registran los errores encontrados.<br><br>**A3 — Error inesperado del sistema**<br>1. Ocurre un error durante el procesamiento.<br>2. El sistema registra el error.<br>3. Se retorna una respuesta de fallo. |
| **Relación con otros casos de uso** | UC1a — Importar desde API (procesamiento batch).<br>UC1b — Registro manual (procesamiento individual).|
| **Resultado**                       | Datos de afiliado/s procesados y almacenados correctamente, con registro de errores en caso de existir. 

---

## UC4 — Importar desde Google Sheets

| Campo | Detalle |
|---|---|
| **Caso de Uso** | UC4: Importar desde Google Sheets |
| **Actor Principal** | Usuario Administrativo |
| **Actores Secundarios** | Google Sheets |
| **Descripción** | El usuario inicia la importación de datos desde una hoja de cálculo de Google Sheets. La API lee los registros, los valida, normaliza y almacena. |
| **Relación con otros casos de uso** | UC4a — Leer y transformar datos desde Google Sheets.<br>UC4b — Marcar errores en Google Sheets.|
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
### UC4a — Leer y transformar datos desde Google Sheets (expandido)

| Campo                   | Detalle |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Caso de Uso**         | UC4a — Leer y transformar datos desde Google Sheets |
| **Actor Principal**     | Sistema |
| **Actores Secundarios** | Google Sheets |
| **Descripción**         | El sistema se conecta a Google Sheets, obtiene los datos de un rango específico, valida la existencia de encabezados, los transforma a un formato interno y genera una colección de registros estructurados (`InputRow`).|
| **Precondiciones**      | - Existe conexión válida con Google Sheets.<br>- El rango especificado es accesible.<br>- La hoja contiene al menos una fila de encabezados. |
| **Postcondiciones**     | - Se obtiene una lista de `InputRow` con datos normalizados.<br>- Cada registro contiene su `row_number` correspondiente. 
| **Flujo Principal**     | 1. El sistema recibe el rango a consultar.<br>2. El sistema solicita los datos al servicio de Google Sheets.<br>3. El sistema verifica que existan datos en el rango.<br>4. El sistema separa encabezados y filas de datos.<br>5. El sistema transforma los encabezados a un formato interno (snake_case u otro estándar).<br>6. El sistema construye objetos `InputRow` asignando `row_number` real del Sheet.<br>7. El sistema retorna la lista de registros transformados. |
| **Flujos Alternativos** | **A1 — Rango sin datos**<br>1. El sistema detecta que no hay datos en el rango.<br>2. El sistema lanza una excepción de validación.<br><br>**A2 — Error de conexión con Google Sheets**<br>1. El sistema no puede obtener los datos.<br>2. Se lanza un error de sincronización. |
| **Reglas de Negocio**   | SH-UC4a-RN1 — Los encabezados deben mapearse a variables internas del sistema.<br>SH-UC4a-RN2 — Cada fila debe mantener su número original (`row_number`).<br>SH-UC4a-RN3 — No se deben procesar filas vacías.|
| **Resultado**           | Datos estructurados en una lista de `InputRow` listos para ser procesados por la lógica de negocio.                                                            
---
### UC4b — Marcar errores en Google Sheets (expandido)

| Campo                   | Detalle |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Caso de Uso**         | UC4b — Marcar errores en Google Sheets |
| **Actor Principal**     | Sistema |
| **Actores Secundarios** | Google Sheets  |
| **Descripción**         | Una vez finalizado el proceso de importación, el sistema identifica los registros con errores de validación y aplica una actualización masiva sobre la hoja de cálculo, marcando visualmente las filas o celdas correspondientes. |
| **Precondiciones**      | - La importación (UC4) fue ejecutada.<br>- Existen errores registrados (`ErrorValidacion`).<br>- Cada error contiene un `row_number` válido. |
| **Postcondiciones**     | - Las filas o celdas con errores quedan visualmente marcadas (ej. fondo rojo).<br>- No se modifican los datos originales del usuario.|
| **Flujo Principal**     | 1. El sistema finaliza el proceso de importación (UC4).<br>2. El sistema obtiene la lista de errores generados.<br>3. El sistema extrae los `row_number` de cada error.<br>4. El sistema elimina duplicados de filas para optimizar la operación.<br>5. El sistema construye una solicitud de actualización masiva (batch).<br>6. El sistema envía la solicitud a Google Sheets.<br>7. El sistema aplica formato visual (por ejemplo, fondo rojo) a las filas o celdas afectadas. |
| **Flujos Alternativos** | **A1 — No hay errores**<br>1. El sistema detecta que no existen errores.<br>2. No se realiza ninguna actualización en el Sheet.<br><br>**A2 — Error al actualizar Google Sheets**<br>1. Ocurre un error durante la actualización.<br>2. El sistema registra el fallo.<br>3. El proceso de importación no se ve afectado. |
| **Reglas de Negocio**   | SH-UC4b-RN1 — Los errores deben reflejarse en el origen (Google Sheets).<br>SH-UC4b-RN2 — La actualización debe realizarse en forma masiva (batch).<br>SH-UC4b-RN3 — Solo se deben marcar filas con errores.<br>SH-UC4b-RN4 — La operación no debe interrumpir el flujo principal de importación. |
| **Resultado**           | Las filas con errores quedan visualmente identificadas en Google Sheets, facilitando su corrección por parte del usuario. |


---

## UC6 — Generar y sincronizar tabla de afiliados en Google Sheets

| Campo                   | Detalle |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Caso de Uso**         | UC6: Generar y sincronizar tabla de afiliados en Google Sheets |
| **Actor Principal**     | Usuario Administrativo  |
| **Actores Secundarios** | Google Sheets  |
| **Descripción**         | El usuario genera o actualiza una tabla en Google Sheets con los afiliados almacenados en el sistema, asegurando consistencia, orden y visualización de datos relevantes. |
| **Precondiciones**      | Existen afiliados almacenados en la base de datos. La API tiene credenciales de acceso a Google Sheets configuradas.                                                      |
| **Postcondiciones**     | La hoja de Google Sheets contiene una tabla actualizada, ordenada y consistente con los afiliados del sistema.                                                            |

### Flujo Principal

| Paso | Actor                  | Acción                                                                              |
| ---- | ---------------------- | ----------------------------------------------------------------------------------- |
| 1    | Usuario Administrativo | Inicia la operación vía `POST /sync/sheets/export`                                  |
| 2    | Sistema                | Obtiene los afiliados activos desde la base de datos                                |
| 3    | Sistema                | Ordena los afiliados alfabéticamente por nombre y apellido                          |
| 4    | Sistema                | Calcula la edad de cada afiliado a partir de su fecha de nacimiento                 |
| 5    | Sistema                | Construye la estructura de la tabla (Nombre y Apellido, Edad, Datos relevantes)     |
| 6    | Sistema                | Se conecta a Google Sheets usando las credenciales configuradas                     |
| 7    | Sistema                | Verifica si la hoja existe; si no existe, la crea; si existe, la limpia o actualiza |
| 8    | Sistema                | Inserta los datos en la hoja respetando el orden definido                           |
| 9    | Google Sheets          | Confirma la escritura de los datos                                                  |
| 10   | Sistema                | Devuelve confirmación con la cantidad de registros procesados                       |

### Flujos Alternativos

| Paso | Condición                | Acción                                                                 |
| ---- | ------------------------ | ---------------------------------------------------------------------- |
| 2a   | No hay afiliados activos | El sistema devuelve respuesta indicando que no hay datos para exportar |
| 7a   | La hoja no existe        | El sistema crea una nueva hoja antes de insertar los datos             |
| 8a   | Error en un registro     | El sistema registra el error y continúa con los demás registros        |

### Excepciones

| Condición                                | Respuesta del Sistema                                       |
| ---------------------------------------- | ----------------------------------------------------------- |
| Error de autenticación con Google Sheets | Devuelve `503 Service Unavailable` con detalle del error    |
| Error de conexión con la base de datos   | Devuelve `500 Internal Server Error`                        |
| Fallo parcial en la escritura            | Devuelve un resumen indicando registros exitosos y fallidos |
