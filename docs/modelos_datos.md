# Modelo de Datos Conceptual
## Sistema de Normalización de Datos de Afiliados

### 1. Introducción
Este documento describe el modelo de datos conceptual del sistema de normalización de datos de afiliados.

El objetivo es identificar las entidades principales del sistema y sus atributos más relevantes.

---

### 2. Entidades del sistema

---

## Afiliado

Descripción:
Representa a una persona afiliada al sindicato.

Atributos:
- id
- nombre
- dni
- direccion
- telefono
- estado
- fecha_alta

Reglas relacionadas:
- El DNI debe ser único
- El nombre es obligatorio
- Los datos deben almacenarse normalizados

---

## ErrorValidacion

Descripción:
Representa un error detectado durante la importación de datos.

Atributos:
- id
- registro_origen
- campo
- descripcion_error
- fecha_error

Reglas relacionadas:
- Los errores deben registrarse
- Los registros inválidos no deben persistirse

---

## Importacion

Descripción:
Representa un proceso de importación de datos de afiliados.

Atributos:
- id
- fecha_importacion
- cantidad_registros
- cantidad_errores
- estado

Reglas relacionadas:
- La importación debe continuar aunque existan errores
- Debe registrarse el resultado del proceso

---

### 3. Relaciones conceptuales

Importacion
    |
    |--- procesa ---> Afiliado
    |
    |--- genera ----> ErrorValidacion

Un proceso de importación puede generar múltiples afiliados válidos y múltiples errores de validación.
