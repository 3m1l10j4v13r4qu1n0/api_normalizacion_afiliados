# Casos de Uso
## Sistema de Normalización de Datos de Afiliados

### 1. Introducción
Este documento describe los casos de uso del sistema de normalización de datos de afiliados.

Los casos de uso representan las interacciones entre los actores externos y el sistema.

---

## UC1 — Importar Afiliados

Actor principal:
Sistema Cliente

Descripción:
Permite importar datos de afiliados al sistema para su validación, normalización y almacenamiento.

Flujo principal:
1. El sistema cliente envía datos de afiliados.
2. El sistema valida los datos.
3. El sistema normaliza la información.
4. El sistema almacena los registros válidos.
5. El sistema registra errores si existen.

Resultado:
Datos de afiliados almacenados correctamente.

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

## UC6 — Sincronizar cambios hacia Google Sheets

Actor principal: 
Usuario Administrativo

Descripción: 
Cuando se modifican o actualizan afiliados en el sistema, el usuario puede sincronizar esos cambios de vuelta a la hoja de cálculo de Google Sheets para mantener consistencia.

Flujo principal:
1. El usuario inicia sync.
2. El sistema obtiene los afiliados modificados.
3. el sistema actualiza las filas correspondientes en Gogle Sheets.
4. el sistema confirma la operación.

Resultado:
Datos sincronizados.
