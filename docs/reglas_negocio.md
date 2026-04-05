# Reglas de Negocio

## Sistema de Normalización de Datos de Afiliados

### 1. Introducción

Este documento define las reglas de negocio que deben cumplirse durante la validación, normalización y visualización de los datos de afiliados.

Las reglas de negocio aseguran la consistencia, integridad y correcta exposición de la información almacenada en el sistema.

---

### 2. Reglas de identificación

AF-RN01 — El DNI del afiliado debe ser único en el sistema.

AF-RN02 — No se deben almacenar afiliados duplicados.

AF-RN03 — El DNI debe contener solo valores numéricos.

AF-RN04 — El email debe tener un formato válido.

SH-UC4a-RN1 — Los encabezados deben mapearse a variables internas del sistema.
SH-UC4a-RN2 — Cada fila debe mantener su número original (row_number).
SH-UC4a-RN3 — No se deben procesar filas vacías.
---

### 3. Reglas de datos obligatorios


AF-RN05 — Los campos obligatorios no pueden estar vacíos.

AF-RN06 — El afiliado debe tener un estado definido.

AF-RN07 — El registro debe ser atómico (todo o nada).

---

### 4. Reglas de normalización

AF-RN08 — Los nombres deben almacenarse en mayúsculas.

AF-RN09 — Los textos no deben contener espacios al inicio ni al final.

AF-RN10 — Los DNI deben almacenarse sin puntos ni guiones.

---

### 5. Reglas de validación

AF-RN11 — Los registros con datos inválidos no deben persistirse.

AF-RN12 — Los errores deben registrarse con referencia a la fila o índice del registro.

AF-RN13 — La importación de datos debe continuar aunque existan registros inválidos.

---

### 6. Reglas de sincronización

AF-RN14 — Solo se sincronizan afiliados válidos.

AF-RN15 — La sincronización no debe modificar datos locales.

AF-RN16 — La eliminación de un afiliado debe realizarse mediante baja lógica, marcando su estado como inactivo.

AF-RN17 — Los atributos género, estado civil, nivel educativo, relación de dependencia y estado del afiliado deben pertenecer a valores controlados almacenados en entidades de dominio.

---

### 7. Reglas de visualización 

AF-RN18 — El sistema debe mostrar el nombre completo del afiliado en una única columna, resultante de la concatenación del nombre y el apellido.

AF-RN19 — La edad del afiliado debe calcularse dinámicamente en base a la fecha de nacimiento y el año actual.

Fórmula:

```python
edad = año_actual - fecha_nacimiento.año
```

Este valor no debe persistirse en la base de datos, sino calcularse en tiempo de ejecución.

AF-RN20 — El sistema debe mostrar únicamente información relevante para el usuario final en la tabla de afiliados. No es obligatorio exponer todos los campos del sistema.

AF-RN21 — Los afiliados deben visualizarse ordenados alfabéticamente por nombre y apellido en cada generación o actualización de la tabla.

AF-RN22 — En cada ejecución del proceso, la tabla debe reflejar el estado actual de la base de datos, sin duplicados y garantizando consistencia mediante la sobrescritura o actualización completa de la información.

---

### 8. Reglas de feedback visual al usuario

AF-RN23 — Si existe un error, el sistema debe informar inmediatamente al usuario.

SH-UC4b-RN1 — Los errores deben reflejarse en el origen de datos (Google Sheets).
SH-UC4b-RN2 — La marcación de errores debe realizarse de forma masiva para optimizar rendimiento.
SH-UC4b-RN3 — Solo se deben marcar las filas que contengan errores.
SH-UC4b-RN4 — La marcación no debe interrumpir el proceso de importación.
