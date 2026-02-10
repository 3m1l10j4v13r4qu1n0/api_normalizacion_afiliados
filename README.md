# API Normalización de Afiliados

🔄 API REST para normalización de datos de afiliados  
📊 Sincronización con Google Sheets  
🏗️ Clean Architecture  
⚡ FastAPI  
🐍 Python  

---

## Descripción

Este proyecto implementa una API REST para la importación, validación, normalización y gestión de datos de afiliados.

El sistema actúa como una capa intermedia entre fuentes de datos externas y sistemas de consulta, garantizando la consistencia y calidad de la información almacenada.

El proyecto está diseñado como ejercicio práctico de **análisis funcional + desarrollo backend**, simulando un sistema real de gestión de datos administrativos.

El sistema actúa como una capa intermedia entre fuentes de datos externas y sistemas de consulta, garantizando la consistencia y calidad de la información almacenada.

**El alcance del proyecto se limita a la normalización, validación y persistencia de datos, sin reemplazar a un sistema completo de gestión de afiliados.**


---

## Objetivos del proyecto

- Normalizar datos de afiliados
- Validar información obligatoria
- Detectar duplicados
- Centralizar la gestión de datos normalizados de afiliados
- Sincronizar datos con Google Sheets
- Exponer funcionalidades mediante una API REST

---

## Documentación funcional

La documentación del análisis funcional se encuentra en la carpeta `docs/`.

Incluye:

- Documento de visión
- Alcance del sistema
- Actores
- Requerimientos funcionales
- Reglas de negocio
- Casos de uso
- Modelo de datos conceptual
- Especificación de API
- Casos de prueba

Esto simula la documentación generada por un **analista funcional junior en un proyecto real**.

---

## Funcionalidades principales

- Importación de afiliados
- Validación de datos
- Normalización de información
- Persistencia en base de datos SQLite
- Consulta de afiliados
- Actualización de afiliados
- Baja lógica de afiliados
- Sincronización con Google Sheets

---

## Arquitectura

El proyecto sigue principios de **Clean Architecture**, separando:

- Capa de dominio
- Capa de aplicación
- Capa de infraestructura
- Capa de API

Esto permite mantener el sistema modular y mantenible.

---

## Tecnologías utilizadas

- Python
- FastAPI
- SQLite
- Pydantic
- Google Sheets API

---

## Estructura del proyecto

api_normalizacion_afiliados                      
├── app                           
├── docs    
│   ├── actores.md  
│   ├── alcance.md  
│   ├── api.md   
│   ├── casos_de_uso.md  
│   ├── modelos_datos.md  
│   ├── pruebas.md  
│   ├── reglas_negocio.md  
│   ├── requerimientos.md  
│   └── vision.md  
├── README.md  
├── requirements.txt  
└── tests  


---

## Estado del proyecto

Proyecto en desarrollo con fines educativos y de portfolio.

---

## Autor

Emilio Javier Aquino   
Estudiante de Analista de Sistemas
