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

## UC4 — Sincronizar con Google Sheets

Actor principal:
Usuario Administrativo

Descripción:
El usuario administrativo inicia la acción a través de un sistema cliente.
Permite sincronizar los datos almacenados con Google Sheets.

Flujo principal:
1. El usuario inicia la sincronización.
2. El sistema obtiene afiliados válidos.
3. El sistema envía los datos a Google Sheets.
4. El sistema confirma la operación.

Resultado:
Datos sincronizados.

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

