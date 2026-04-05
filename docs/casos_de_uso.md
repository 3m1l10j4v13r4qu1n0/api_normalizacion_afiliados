# Casos de Uso
## Sistema de Normalización de Datos de Afiliados

### 1. Introducción
Este documento describe los casos de uso del sistema de normalización de datos de afiliados.

Los casos de uso representan las interacciones entre los actores externos y el sistema.

---

## UC1 — Importar Afiliado/s

Actor principal:
Sistema Cliente

Descripción:
Permite importar datos de afiliado/s al sistema para su validación, normalización y almacenamiento.

Flujo principal:
1. El sistema cliente envía datos de un afiliado o una lista de afiliados.
2. El sistema valida los datos.
3. El sistema normaliza la información.
4. El sistema almacena los registros válidos.
5. El sistema registra errores si existen.

Resultado:
Datos de afiliado/s almacenados correctamente.

## UC1a — Importar Afiliados desde API (lista)

Actor principal:
Sistema Cliente

Descripción:
Permite importar múltiples datos de afiliados al sistema mediante una API, para su validación, normalización y almacenamiento.

Flujo principal:
1. El sistema cliente envía una lista de afiliados.
2. El sistema valida los datos de cada registro.
3. El sistema normaliza la información.
4. El sistema almacena los registros válidos.
5. El sistema registra errores si existen.

Resultado
Datos de afiliados procesados y almacenados correctamente, con registro de errores en caso de existir.

## UC1b — Registrar Afiliado manualmente

Actor principal:
Usuario Administrativo

Descripción:
Permite registrar manualmente un afiliado en el sistema mediante la carga individual de sus datos, para su validación, normalización y almacenamiento.

Flujo principal
1. El usuario ingresa los datos de un afiliado.
2. El sistema valida los datos ingresados.
3. El sistema normaliza la información.
4. El sistema almacena el afiliado.
5. El sistema informa si existen errores.

Resultado
Afiliado registrado correctamente en el sistema o notificación de errores en los datos ingresados.
---

## UC2 — Consultar Afiliados

Actor principal:
Usuario Administrativo / Sistema Cliente

Descripción:
Permite consultar la información de afiliados almacenados.

Flujo principal:
1. El actor solicita la lista de afiliados.
2. El sistema obtiene los datos almacenados.
3. El sistema devuelve la información solicitada.

Resultado:
Listado de afiliados.

---

## UC3 — Actualizar Afiliado

Actor principal:
Usuario Administrativo / Sistema Cliente

Descripción:
Permite modificar la información de un afiliado existente.

Flujo principal:
1. El actor envía datos actualizados.
2. El sistema valida la información.
3. El sistema actualiza el afiliado.
4. El sistema confirma la actualización.

Resultado:
Afiliado actualizado.

---

## UC4 — Importar desde Google Sheets

Actor principal:
Usuario Administrativo

Descripción:
El usuario inicia la importación de datos desde una hoja de cálculo de Google Sheets. La API lee los registros, los valida, normaliza y almacena.

Flujo principal:
1. El usuario dispara la importación.
2. El sistema lee la hoja de calculo de Google Sheets.
3. El sistema normaliza y valida los datos obtenidos.
4. El sistema almasena los datos validados.
5. El sistema registra si hay errores.

Resultado:
Datos importados.



## UC4a — El sistema lee la hoja de cálculo de Google Sheets.

Descripción:
El usuario inicia la importación de datos desde una hoja de cálculo de Google Sheets. La API lee los registros,
verifica que los encabezados sean los mismos que las variables del modelo del sistema, si no. Los adapta al sistema,
crea un array con las filas de los registros de la hoja y los enumera



Flujo principal:
1. El sistema importa  todos los valores de la hoja  con un rango específico conectándose a actor externo Google Sheets.
2. El sistema define  los encabezados y las lista de valores
3. El sistema adacta los encabezados a variables más pytonicas
4. El sistema instacia el objeto SheetRow

Resultado:
Datos ordenados en un array que cada elemento del array es un objeto SheetRow que contiene la clave numbrer_row:int que
contiene el índice para identificar la fila después la clave value:Any que contiene un diccionario que contiene los encabezados y valores.

## UC4b — Marcar errores en Google Sheets.

Actor principal:
Sistema

Actores secundarios:
Google Sheets


Descripción:
Una vez finalizada la importación de datos (UC4), el sistema identifica los registros que presentaron errores de validación y realiza una actualización masiva sobre la hoja de cálculo de Google Sheets.

El sistema marca visualmente las filas o celdas correspondientes a los registros con errores, aplicando un formato distintivo (por ejemplo, fondo rojo), facilitando su identificación por parte del usuario.

Flujo principal:
1. El sistema finaliza la ejecución del proceso de importación (UC4).
2. El sistema obtiene la lista de errores de validación generados durante el proceso.
3. El sistema extrae los números de fila (row_number) asociados a cada error.
4. El sistema agrupa las filas con errores para optimizar la operación.
5. El sistema envía una actualización masiva a Google Sheets.
6. El sistema aplica formato visual (color rojo) a las filas o celdas correspondientes.

Flujo alternativo:
A1 — Error al actualizar Google Sheets

1. El sistema intenta aplicar el formato en Google Sheets.
2. Ocurre un error en la comunicación o actualización.
3. El sistema registra el error internamente.
4. El sistema no interrumpe la importación ni revierte los datos procesados.

Resultado:
Las filas que contienen errores de validación quedan visualmente marcadas en la hoja de cálculo (por ejemplo, con fondo rojo), permitiendo al usuario identificar rápidamente los registros problemáticos.
---

## UC5 — Dar de baja afiliado

Actor principal:
Usuario Administrativo / Sistema Cliente

Descripción:
Permite dar de baja un afiliado marcándolo como inactivo en el sistema.

Flujo principal:
1. El actor solicita la baja del afiliado.
2. El sistema verifica la existencia del afiliado.
3. El sistema marca el afiliado como inactivo.
4. El sistema confirma la operación.

Resultado:
Afiliado dado de baja lógicamente.

## UC6 — Generar tabla de afiliados en Google Sheets

Actor principal: 
Usuario Administrativo / Sistema Cliente

Descripción: 
El usuario puede generar una tabla en Google Sheets que contenga los afiliados almacenados en la base de datos.
Si la hoja no existe, el sistema la crea; si ya existe, la actualiza mostrando los datos estructurados.

Flujo principal:
1. El usuario inicia la generación de la tabla.
2. El sistema consulta los afiliados desde la base de datos.
3. El sistema ordena los afiliados alfabéticamente por nombre y apellido.
4. El sistema calcula la edad de cada afiliado a partir de su fecha de nacimiento y el año actual.
5. El sistema verifica si la hoja existe en Google Sheets:
    - Si no existe, la crea.
    - Si existe, la limpia o actualiza.

6. El sistema construye la tabla con la siguiente estructura:

| Nombre y Apellido | Edad | Datos Relevantes |
| ----------------- | ---- | ---------------- |

7. El sistema inserta los afiliados en la hoja respetando el orden alfabético.
8. El sistema confirma la operación.

Resultado:
Se genera o actualiza una hoja en Google Sheets con los afiliados ordenados, mostrando información clara y útil, incluyendo la edad calculada.
