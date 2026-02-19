# Documento de Visión
## Sistema de Normalización de Datos de Afiliados

### 1. Introducción
Este documento describe la visión general del sistema de normalización de datos de afiliados. El objetivo es definir el problema, los usuarios involucrados y el valor que aportará la solución.

---

### 2. Problema
Los datos de afiliados se generan desde múltiples fuentes, como planillas, archivos importados y cargas manuales.  
Esto provoca inconsistencias en la información, registros duplicados y errores de formato que dificultan la gestión y consulta de los afiliados.

Además, la sincronización manual con herramientas externas como Google Sheets genera demoras y posibles errores humanos.

---

### 3. Objetivo del sistema
Desarrollar una API REST que permita:

- Importar datos de afiliados
- Validar información obligatoria
- Normalizar datos
- Persistir información de manera consistente
- Consultar afiliados
- Actualizar información de afiliados
- Sincronizar datos con Google Sheets
- Notificar errores de validación

El sistema funcionará como una capa intermedia de procesamiento y validación de datos.

---

### 4. Usuarios del sistema
Los usuarios y sistemas involucrados son:

- Usuario administrativo del sindicato
- Sistemas externos que consumen la API
- Google Sheets como sistema de sincronización

---

### 5. Beneficios esperados
La implementación del sistema permitirá:

- Mejorar la calidad de los datos
- Reducir registros duplicados
- Estandarizar formatos de información
- Centralizar la gestión de afiliados
- Automatizar procesos de sincronización
- Facilitar consultas de información confiable

---

### 6. Alcance del sistema
El sistema incluye:

- Normalización de datos de afiliados
- Validación de información
- Persistencia en base de datos PostgreSQL
- API REST para operaciones CRUD
- Sincronización con Google Sheets

El sistema no incluye:

- Interfaz gráfica de usuario
- Autenticación de usuarios
- Generación de reportes

---

### 7. Supuestos y restricciones

#### Supuestos
- Los datos de entrada tendrán una estructura definida.
- El sistema será utilizado en un entorno interno.
- La API será consumida por scripts o sistemas externos.

#### Restricciones
- Base de datos PostgreSQL
- Arquitectura basada en API REST
- Proyecto orientado a prototipo funcional para demostración
