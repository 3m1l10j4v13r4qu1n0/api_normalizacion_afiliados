# Requerimientos Funcionales
## Sistema de Normalización de Datos de Afiliados

### 1. Introducción
Este documento describe los requerimientos funcionales de la API de normalización de datos de afiliados.

Los requerimientos definen las funcionalidades que el sistema debe proveer para permitir la importación, validación, normalización, almacenamiento, consulta y sincronización de datos.

---

### 2. Requerimientos funcionales

#### Importación de datos
RF1 — El sistema debe permitir importar datos de afiliados desde una fuente externa.

RF2 — El sistema debe procesar múltiples registros de afiliados en una misma importación.

---

#### Validación de datos
RF3 — El sistema debe validar la presencia de datos obligatorios de cada afiliado.

RF4 — El sistema debe validar el formato de los datos ingresados.

RF5 — El sistema debe detectar registros duplicados según DNI u otro identificador único.

RF6 — El sistema debe registrar errores de validación.

---

#### Normalización de datos
RF7 — El sistema debe normalizar los nombres de afiliados.

RF8 — El sistema debe normalizar los formatos de texto.

RF9 — El sistema debe almacenar los datos normalizados.

---

#### Gestión de afiliados
RF10 — El sistema debe permitir consultar afiliados.

RF11 — El sistema debe permitir consultar un afiliado por identificador.

RF12 — El sistema debe permitir actualizar datos de afiliados.

RF13 — El sistema debe permitir dar de baja afiliados.

---

#### Persistencia
RF14 — El sistema debe almacenar los datos en una base de datos PostgreSQL.

---

#### Sincronización
RF15 — El sistema debe permitir sincronizar los datos de afiliados con Google Sheets.

RF16 — El sistema debe permitir generar una tabla de afiliados en Google Sheets a partir de los datos almacenados en la base de datos.

RF17 — El sistema debe crear la hoja de cálculo si no existe o actualizarla si ya está creada.

RF18 — El sistema debe ordenar los afiliados alfabéticamente por nombre y apellido antes de exportarlos.

RF19 — El sistema debe calcular dinámicamente la edad de cada afiliado en base a su fecha de nacimiento.

RF20 — El sistema debe mostrar el nombre y apellido concatenados en una única columna dentro de la tabla.

RF21 — El sistema debe exportar únicamente datos relevantes para el usuario final.

RF22 — El sistema debe sobrescribir o actualizar completamente la tabla en cada ejecución para garantizar consistencia.

---

#### API REST
RF23 — El sistema debe exponer endpoints REST para la gestión de afiliados.



---

### 3. Requerimientos no funcionales (básicos)

RNF1 — La API debe responder en formato JSON.

RNF2 — El sistema debe manejar errores de manera controlada.

RNF3 — El sistema debe registrar errores de validación.

RNF4 — El sistema debe ser modular y mantenible.
