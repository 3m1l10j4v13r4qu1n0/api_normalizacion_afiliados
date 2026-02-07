# Casos de Prueba Funcionales
## Sistema de Normalización de Datos de Afiliados

### 1. Introducción
Este documento describe los casos de prueba funcionales del sistema de normalización de datos de afiliados.

Los casos de prueba permiten verificar que el sistema cumple con los requerimientos definidos.

---

### 2. Casos de prueba

---

## CP1 — Importar afiliado válido

Requerimientos relacionados:
RF1, RF3, RF7, RF9

Descripción:
Verificar que un afiliado con datos correctos se importe correctamente.

Entrada:
Afiliado con nombre y DNI válidos.

Resultado esperado:
- Afiliado almacenado
- Sin errores de validación

---

## CP2 — Importar afiliado con DNI duplicado

Requerimientos relacionados:
RF5, RN1, RN2

Descripción:
Verificar que el sistema detecte afiliados duplicados.

Entrada:
Afiliado con DNI ya existente.

Resultado esperado:
- Registro no almacenado
- Error de validación registrado

---

## CP3 — Importar afiliado sin nombre

Requerimientos relacionados:
RF3, RN4

Descripción:
Verificar validación de campos obligatorios.

Entrada:
Afiliado sin nombre.

Resultado esperado:
- Error de validación registrado
- Registro no persistido

---

## CP4 — Consultar afiliados

Requerimientos relacionados:
RF10

Descripción:
Verificar que el sistema devuelva la lista de afiliados.

Entrada:
Solicitud de consulta.

Resultado esperado:
Lista de afiliados almacenados.

---

## CP5 — Actualizar afiliado

Requerimientos relacionados:
RF12

Descripción:
Verificar actualización de datos de afiliados.

Entrada:
Datos actualizados de un afiliado existente.

Resultado esperado:
Afiliado actualizado correctamente.

---

## CP6 — Sincronizar datos con Google Sheets

Requerimientos relacionados:
RF14, RN14

Descripción:
Verificar la sincronización de afiliados válidos.

Entrada:
Solicitud de sincronización.

Resultado esperado:
Datos sincronizados correctamente.
