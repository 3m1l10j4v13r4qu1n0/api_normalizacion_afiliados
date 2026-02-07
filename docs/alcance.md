# Documento de Alcance
## Sistema de Normalización de Datos de Afiliados

### 1. Descripción general
El sistema de normalización de datos de afiliados será una API REST encargada de procesar información proveniente de distintas fuentes, validar su consistencia, normalizar los datos y almacenarlos en una base de datos local.

El sistema actuará como una capa de procesamiento intermedia entre las fuentes de datos y los sistemas de consulta o sincronización.

---

### 2. Funcionalidades incluidas
El sistema incluirá las siguientes funcionalidades:

- Importación de datos de afiliados
- Validación de información obligatoria
- Normalización de datos (formato de texto, identificación, etc.)
- Registro de errores de validación
- Almacenamiento de afiliados en base de datos SQLite
- Consulta de afiliados
- Actualización de datos de afiliados
- Sincronización de datos con Google Sheets
- API REST para acceso a la información

---

### 3. Funcionalidades fuera de alcance
El sistema no incluirá:

- Interfaz gráfica de usuario
- Sistema de autenticación o autorización
- Integración con sistemas externos adicionales
- Generación de reportes
- Migración de datos históricos
- Procesamiento en tiempo real
- Panel de administración

---

### 4. Límites del sistema
El sistema será responsable únicamente de la normalización, validación, almacenamiento y consulta de datos de afiliados.

La carga de datos, el consumo de la API y la visualización de información serán responsabilidad de sistemas externos.

---

### 5. Criterios de aceptación del alcance
El alcance del sistema se considerará cumplido cuando:

- La API permita importar datos de afiliados
- Los datos sean validados y normalizados correctamente
- Los afiliados puedan consultarse y actualizarse
- Los errores de validación sean registrados
- Los datos puedan sincronizarse con Google Sheets

