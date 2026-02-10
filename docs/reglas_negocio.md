# Reglas de Negocio
## Sistema de Normalización de Datos de Afiliados

### 1. Introducción
Este documento define las reglas de negocio que deben cumplirse durante la validación y normalización de los datos de afiliados.

Las reglas de negocio aseguran la consistencia e integridad de la información almacenada en el sistema.

---

### 2. Reglas de identificación

RN1 — Cada afiliado debe tener un DNI único en el sistema.

RN2 — No se deben almacenar afiliados duplicados.

RN3 — El DNI debe contener solo valores numéricos.

---

### 3. Reglas de datos obligatorios

RN4 — El nombre del afiliado es obligatorio.

RN5 — El DNI del afiliado es obligatorio.

RN6 — El afiliado debe tener un estado definido.

---

### 4. Reglas de normalización

RN7 — Los nombres deben almacenarse en mayúsculas.

RN8 — Los textos no deben contener espacios al inicio ni al final.

RN9 — Los valores nulos deben transformarse en valores por defecto cuando corresponda.

RN10 — Los DNI deben almacenarse sin puntos ni guiones.

---

### 5. Reglas de validación

RN11 — Los registros con datos inválidos no deben persistirse.

RN12 — Los errores de validación deben registrarse.

RN13 — La importación de datos debe continuar aunque existan registros inválidos.

---

### 6. Reglas de sincronización

RN14 — Solo se sincronizan afiliados válidos.

RN15 — La sincronización no debe modificar datos locales.

RN16 — La eliminación de un afiliado debe realizarse mediante baja lógica, marcando su estado como inactivo.


