# Casos de Uso
## Sistema de Normalización de Datos de Afiliados

### 1. Introducción
Este documento describe los casos de uso del sistema de normalización de datos de afiliados.

Los casos de uso representan las interacciones entre los actores y el sistema para cumplir un objetivo funcional.

---

## UC0 — Ingresar Datos

Actor principal:
Sistema Cliente

Descripción:
Permite importar datos de afiliados al sistema.

Flujo principal:
1. El sistema cliente envía datos de afiliados.
2. El sistema recibe los datos.
3. El sistema valida los datos.
4. El sistema normaliza los datos.
5. El sistema almacena los datos válidos.
6. El sistema registra errores de validación si existen.

Flujo alternativo:
- Datos inválidos → registrar error y continuar importación.

Resultado:
Datos de afiliados almacenados correctamente.

---

## UC1 — Consultar Datos

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

## UC2 — Normalizar Datos

Actor principal:
Sistema

Descripción:
Proceso interno que estandariza los datos de afiliados.

Flujo principal:
1. Convertir textos a mayúsculas.
2. Eliminar espacios innecesarios.
3. Normalizar formato de DNI.
4. Preparar datos para almacenamiento.

Resultado:
Datos normalizados.

---

## UC3 — Validar Datos

Actor principal:
Sistema

Descripción:
Proceso interno que verifica la integridad de los datos.

Flujo principal:
1. Verificar campos obligatorios.
2. Validar formatos.
3. Detectar duplicados.
4. Registrar errores.

Resultado:
Datos validados.

---

## UC4 — Sincronizar con Google Sheets

Actor principal:
Usuario Administrativo

Descripción:
Permite sincronizar los datos almacenados con Google Sheets.

Flujo principal:
1. El usuario inicia la sincronización.
2. El sistema obtiene afiliados válidos.
3. El sistema envía los datos a Google Sheets.
4. El sistema confirma la operación.

Resultado:
Datos sincronizados.

---

## UC5 — Actualizar Afiliado

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
