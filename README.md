# API Normalización de Afiliados

🔄 API REST para normalización de datos de afiliados  
📊 Sincronización con Google Sheets  
🏗️ Clean Architecture  
⚡ FastAPI  
🐍 Python  

---

## 📌 Descripción general

Este proyecto implementa una API REST para la importación, validación, normalización y gestión de datos de afiliados.

El sistema actúa como una capa intermedia entre fuentes de datos externas y sistemas de consulta, garantizando la consistencia y calidad de la información almacenada.

El proyecto está diseñado como ejercicio práctico de **análisis funcional + desarrollo backend**, simulando un sistema real de gestión de datos administrativos.

El sistema actúa como una capa intermedia entre fuentes de datos externas y sistemas de consulta, garantizando la consistencia y calidad de la información almacenada.

**El alcance del proyecto se limita a la normalización, validación y persistencia de datos, sin reemplazar a un sistema completo de gestión de afiliados.**


---

## 🎯 Objetivos del proyecto

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
- Persistencia en base de datos PostgreSQL
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
- PostgreSQL
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
│   ├── caso_de_uso_expandidos.md              
│   ├── casos_de_uso.md                   
│   ├── diagramas                 
│   │   ├── arquitectura               
│   │   │   ├── arquitectura_diagrama.png           
│   │   │   └── arquitectura_diagrama.puml           
│   │   ├── caso_uso              
│   │   │   ├── caso_uso.png             
│   │   │   └── caso_uso.puml            
│   │   ├── diagrama_clases                  
│   │   │   ├── clases_diagrama.png            
│   │   │   └── clases_diagrama.puml            
│   │   ├── diagrama_objetos             
│   │   │   ├── objeto_diagrama.png            
│   │   │   └── objeto_diagrama.puml              
│   │   └── er                
│   │       ├── er_diagrama.png                
│   │       └── er_diagrama.puml                     
│   ├── modelos_datos.md                       
│   ├── pruebas.md                    
│   ├── reglas_negocio.md               
│   ├── requerimientos.md                     
│   └── vision.md                
├── face_1_cierre.md               
├── README.md                     
├── requirements.txt               
└── tests                  


---

## ✅ Estado del proyecto

✔ Fase 1 — Documentación funcional: FINALIZADA

La documentación fue revisada y validada asegurando coherencia entre visión, alcance, reglas de negocio, casos de uso, API y modelo de datos.

📄 Ver detalle del cierre: [fase_1_cierre.md](face_1_cierre.md)


---

## 🗺️ Roadmap

- Fase 1: Documentación funcional ✔

- Fase 2: Diseño técnico y arquitectura (pendiente)

- Fase 3: Implementación API REST (pendiente)

- Fase 4: Pruebas y validación (pendiente)

---

## 🧠 Perfil objetivo

Este proyecto está pensado como material demostrativo para:

- Analista Funcional Jr

- Analista Técnico Funcional

- Primeros roles en proyectos de software administrativo

El foco está puesto en análisis, documentación, trazabilidad y coherencia funcional.

---

## Autor

Emilio Javier Aquino   
Estudiante de Analista de Sistemas

## 📄 Licencia

Proyecto de uso educativo y demostrativo.
