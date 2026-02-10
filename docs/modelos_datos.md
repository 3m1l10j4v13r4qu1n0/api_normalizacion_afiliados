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

**Atributos:**

- id (PK): Identificador único
- apellido (string, 50)
- nombre (string, 50)
- fecha_nacimiento (date)
- dni (string, 20)
- email (string, 150)
- telefono (string, 20)
- nacionalidad (string, 50)
- genero (string, 10)
- estado_civil (string, 20)
- provincia (string, 50)
- localidad (string, 50)
- direccion (string, 100)
- codigo_postal (string, 20)
- nivel_educativo (string, 50)
- titulo_obtenido (string, 100, opcional)
- numero_legajo (string, 50)
- fecha_ingreso (date)
- fecha_alta (date)
- comuna_donde_trabaja (string, 50)
- relacion_dependencia (string, 50)
- marca_temporal_creacion (datetime)
- marca_temporal_actualizacion (datetime)
- estado (enum: activo, inactivo)


**Reglas relacionadas:**

- Nombre, apellido y DNI son obligatorios
- DNI, email y número_legajo deben ser únicos
- Relación laboral puede ser: `monotributista`, `planta_transitoria`, `planta_permanente`
- Nivel educativo y género deben pertenecer a valores controlados
- Los datos deben almacenarse normalizados

---

## ErrorValidacion

Descripción:
Representa un error detectado durante la importación de datos.

**Atributos:**

- id
- registro_origen: Identificador del registro de entrada que originó el error 
  (fila, índice o identificador externo según la fuente de datos)
- campo
- descripcion_error
- fecha_error

Reglas relacionadas:
- Los errores deben registrarse
- Los registros inválidos no deben persistirse
- El registro_origen debe permitir identificar el registro de entrada con error

---

## Importacion

Descripción:
Representa un proceso de importación de datos de afiliados.

**Atributos:**

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
