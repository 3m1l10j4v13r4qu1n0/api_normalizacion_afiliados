# Modelo de Datos Conceptual  
## Sistema de Normalización de Datos de Afiliados

---

## 1. Introducción

Este documento describe el modelo de datos conceptual del sistema de normalización de datos de afiliados.

El objetivo es identificar las entidades principales del dominio, sus atributos relevantes y las relaciones entre ellas, manteniendo coherencia con el modelo lógico y el diseño arquitectónico del sistema.

El modelo conceptual representa la estructura del dominio sin entrar en detalles técnicos de implementación.

---

## 2. Entidades del sistema

---

## Afiliado

**Descripción:**  
Representa a una persona afiliada al sindicato.

**Atributos principales:**

- id (PK)
- apellido
- nombre
- fecha_nacimiento
- dni
- email
- telefono
- numero_legajo
- fecha_ingreso
- fecha_alta
- titulo_obtenido (opcional)
- marca_temporal_creacion
- marca_temporal_actualizacion

**Relaciones:**

- genero (relación con entidad Genero)
- estado_civil (relación con entidad EstadoCivil)
- nivel_educativo (relación con entidad NivelEducativo)
- relacion_dependencia (relación con entidad RelacionDependencia)
- estado_afiliado (relación con entidad EstadoAfiliado)
- domicilio (relación con entidad Domicilio)
- importacion (relación con entidad Importacion)

**Reglas relacionadas:**

- Nombre, apellido y DNI son obligatorios.
- DNI, email y número_legajo deben ser únicos.
- El afiliado debe tener un estado definido (activo/inactivo).
- Los datos deben almacenarse normalizados.

---

## Domicilio

**Descripción:**  
Representa la información domiciliaria del afiliado.

**Atributos:**

- id (PK)
- direccion
- codigo_postal

**Relaciones:**

- localidad (relación con entidad Localidad)

---

## Localidad

**Descripción:**  
Representa una ciudad o localidad.

**Atributos:**

- id (PK)
- nombre

**Relaciones:**

- provincia (relación con entidad Provincia)

---

## Provincia

**Descripción:**  
Representa una provincia del país.

**Atributos:**

- id (PK)
- nombre

---

## Importacion

**Descripción:**  
Representa un proceso de importación de datos de afiliados.

**Atributos:**

- id (PK)
- fecha_importacion
- cantidad_registros
- cantidad_errores
- estado

**Reglas relacionadas:**

- La importación debe continuar aunque existan errores.
- Debe registrarse el resultado del proceso.
- Puede generar múltiples afiliados válidos y múltiples errores de validación.

---

## ErrorValidacion

**Descripción:**  
Representa un error detectado durante la importación de datos.

**Atributos:**

- id (PK)
- registro_origen
- campo
- descripcion_error
- fecha_error

**Relaciones:**

- importacion (relación con entidad Importacion)

**Reglas relacionadas:**

- Los errores deben registrarse.
- Los registros inválidos no deben persistirse.
- Debe poder identificarse el registro de origen del error.

---

## Entidades de Dominio (Tablas de Valores Controlados)

Estas entidades representan valores controlados utilizados por Afiliado.

---

### Genero

- id (PK)
- descripcion

---

### EstadoCivil

- id (PK)
- descripcion

---

### NivelEducativo

- id (PK)
- descripcion

---

### RelacionDependencia

- id (PK)
- descripcion

---

### EstadoAfiliado

- id (PK)
- descripcion

---

## 3. Relaciones Conceptuales Principales

- Una Importacion puede generar múltiples Afiliados.
- Una Importacion puede generar múltiples ErrorValidacion.
- Un Afiliado tiene un único Genero.
- Un Afiliado tiene un único EstadoCivil.
- Un Afiliado tiene un único NivelEducativo.
- Un Afiliado tiene una única RelacionDependencia.
- Un Afiliado tiene un único EstadoAfiliado.
- Un Afiliado tiene un único Domicilio.
- Un Domicilio pertenece a una única Localidad.
- Una Localidad pertenece a una única Provincia.

---

## 4. Consideraciones de Normalización

El modelo conceptual refleja una estructura normalizada donde:

- Los valores repetitivos o categóricos se representan como entidades de dominio.
- La información geográfica se separa en entidades independientes.
- La entidad Afiliado mantiene únicamente sus datos propios y relaciones.

Este diseño garantiza consistencia, integridad referencial y alineación con el modelo lógico en tercera forma normal (3FN).