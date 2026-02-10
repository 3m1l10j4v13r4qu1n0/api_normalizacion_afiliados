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
RF14 — El sistema debe almacenar los datos en una base de datos SQLite.

---

#### Sincronización
RF15 — El sistema debe permitir sincronizar los datos de afiliados con Google Sheets.

---

#### API REST
RF16 — El sistema debe exponer endpoints REST para la gestión de afiliados.



---

### 3. Requerimientos no funcionales (básicos)

RNF1 — La API debe responder en formato JSON.

RNF2 — El sistema debe manejar errores de manera controlada.

RNF3 — El sistema debe registrar errores de validación.

RNF4 — El sistema debe ser modular y mantenible.
