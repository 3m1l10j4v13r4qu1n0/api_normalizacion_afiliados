# API Normalización de Afiliados

🔄 API REST para normalización de datos de afiliados  
📊 Sincronización con Google Sheets  
🏗️ Clean Architecture  
⚡ FastAPI  
🐍 Python  

---

## 📌 Descripción general

Este proyecto implementa una API REST para la importación, validación, normalización y gestión de datos de afiliados.

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

La documentación del análisis funcional se encuentra en la carpeta `docs/`, en **formato Benn (backend-only)**:

- `01_global` — visión, actores, reglas de negocio, alcance
- `02_tecnico` — modelo de datos, decisiones técnicas, diagramas UML/ER
- `03_procesos` — definición de "listo" (DoS)
- `04_historias_usuario/HU-01..HU-08` — 8 historias de usuario (5 archivos c/u: HU, caso de uso expandido, api, modelos de datos, pruebas)
- `07_metodologia_agil` — método Kanban
- `estado_actual_proyecto.md` + `vitacora_agentica.md` — memoria del proyecto (foto actual + historial append-only)

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

## Endpoints principales

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/afiliados/import` | Importar afiliados por archivo/lista (UC1a) |
| POST | `/afiliados/` | Registrar afiliado manual (UC1b) |
| GET | `/afiliados/` | Listar afiliados (UC2) |
| GET | `/afiliados/{id}` | Obtener afiliado por ID (UC2) |
| PATCH | `/afiliados/{id}` | Actualizar afiliado (UC3) |
| DELETE | `/afiliados/{id}` | Dar de baja afiliado (UC5) |
| POST | `/sync/sheets/import` | Importar desde Google Sheets (UC4) |

> Las respuestas de error usan payload uniforme `{"error": "mensaje"}`. La importación responde con el detalle de errores de validación (campo, descripción y número de fila).

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

## 🚀 Instalación y configuración
```
# Clonar el repo
git clone ...

# Crear entorno virtual
python -m venv venv

# Linux 
source venv/bin/activate 

# Instalar dependencias (requirements.txt está dentro de app/)
pip install -r app/requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Correr migraciones (Alembic ya está inicializado, NO ejecutar `alembic init`)

# 1. genera una migración automática leyendo tus modelos
alembic revision --autogenerate -m "descripcion"

# 2. aplica la migración en PostgreSQL
alembic upgrade head

# Levantar la API
uvicorn app.main:app --reload
```
---

# 🏗️ Estructura del Proyecto — API Normalización de Afiliados

Este proyecto implementa una arquitectura basada en **Clean Architecture + Hexagonal (Ports & Adapters)**, separando claramente responsabilidades entre capas.

---

## 📦 Estructura General

```
api-normalizacion/
│
├── alembic/  
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│   💬 Migraciones de base de datos (versionado del esquema)
│
├── app/
│
│   ├── main.py  
│   💬 Punto de entrada de la aplicación (FastAPI)
│
│   ├── presentation/  🟦 CAPA DE PRESENTACIÓN (Delivery)
│   │   ├── routers/
│   │   │   ├── afiliados.py
│   │   │   └── sync.py
│   │   │   💬 Define endpoints REST (HTTP → Use Cases)
│   │   │
│   │   ├── schemas/
│   │   │   ├── afiliados_schema.py
│   │   │   └── importacion_schema.py
│   │   │   💬 DTOs de entrada/salida (Pydantic)
│   │   │
│   │   └── handlers.py
│   │       💬 Orquesta requests → casos de uso (opcional desacople de routers)
│   │
│   │   🎯 Responsabilidad:
│   │   - Recibir requests HTTP
│   │   - Validar formato (NO reglas de negocio)
│   │   - Invocar casos de uso
│
│   ├── application/  🟩 CAPA DE APLICACIÓN (Use Cases)
│   │   └── use_cases/
│   │       ├── core_importar_afiliado.py   ← UC único de importación (orquesta el pipeline)
│   │       ├── uc2_listar_afiliados.py
│   │       ├── uc2_obtener_afiliado_por_id.py
│   │       ├── uc3_actualizar_afiliado.py
│   │       ├── uc4a_importar_afiliado.py   ← lectura/transformación del Sheet (fuente)
│   │       └── uc5_dar_baja_afiliado.py
│   │
│   │       💬 Implementación de casos de uso del sistema
│   │       💬 El pipeline de importación es un UC único: absorbe UC1a (archivo),
│   │          UC1b (alta manual) y UC4 (Sheets) usando importacion_pipeline
│   │
│   │   🎯 Responsabilidad:
│   │   - Orquestar la lógica de negocio
│   │   - Coordinar servicios del dominio
│   │   - Usar repositorios (a través de puertos)
│   │   - NO depende de infraestructura concreta
│
│   ├── domain/  🟥 CAPA DE DOMINIO (Core del negocio)
│   │
│   │   ├── models/
│   │   │   ├── afiliado.py
│   │   │   ├── dominio.py          ← enum de valores controlados (puro)
│   │   │   ├── importacion.py
│   │   │   ├── error_validacion.py
│   │   │   ├── input_row.py
│   │   │   ├── sheet_raw_data.py
│   │   │   └── mapping.py
│   │   │   💬 Entidades y modelos del dominio (reglas puras)
│   │   │
│   │   ├── services/
│   │   │   ├── normalizacion.py
│   │   │   ├── validacion.py
│   │   │   ├── importacion_pipeline.py   ← lógica pura por fila (normalizar+validar+dup)
│   │   │   ├── data_transformer.py
│   │   │   └── data_key_mapper.py
│   │   │   💬 Lógica de negocio compleja desacoplada de entidades
│   │   │
│   │   ├── ports/
│   │   │   ├── afiliado/
│   │   │   │   ├── afiliado_command_port.py
│   │   │   │   ├── afiliado_importacion_port.py
│   │   │   │   └── afiliado_query_port.py
│   │   │   │
│   │   │   ├── importacion_repository_port.py
│   │   │   ├── error_repository_port.py
│   │   │   ├── domicilio_repository_port.py
│   │   │   ├── dominio_repository_port.py
│   │   │   └── sheet_data_port.py
│   │   │   💬 Interfaces (contratos) → patrón Ports & Adapters
│   │   │
│   │   ├── exceptions.py
│   │   │   💬 Excepciones propias del dominio
│   │
│   │   🎯 Responsabilidad:
│   │   - Contener las reglas de negocio
│   │   - Ser independiente de frameworks
│   │   - Definir contratos (ports)
│
│   ├── infrastructure/  🟨 CAPA DE INFRAESTRUCTURA (Adapters)
│   │
│   │   ├── core/
│   │   │   └── config.py
│   │   │   💬 Configuración global (env, settings)
│   │   │
│   │   ├── database/
│   │   │   ├── connection.py
│   │   │   💬 Conexión a la base de datos
│   │   │
│   │   │   ├── orm_models/
│   │   │   │   ├── afiliado_orm.py
│   │   │   │   ├── domicilio_orm.py
│   │   │   │   ├── dominios_orm.py
│   │   │   │   ├── error_validacion_orm.py
│   │   │   │   └── importacion_orm.py
│   │   │   │   💬 Modelos ORM (SQLAlchemy)
│   │   │   │
│   │   │   ├── repositories/
│   │   │   │   ├── afiliado_command_repository.py
│   │   │   │   ├── afiliado_importacion_repository.py
│   │   │   │   ├── afiliado_query_repository.py
│   │   │   │   ├── importacion_repository.py
│   │   │   │   ├── error_repository.py
│   │   │   │   ├── domicilio_repository.py
│   │   │   │   └── dominio_repository.py
│   │   │   │   💬 Implementaciones de los ports (Adapters)
│   │   │   │
│   │   │   ├── seed.py                 ← datos iniciales
│   │   │   └── seed_runner.py          ← script para ejecutar el seed
│   │   │   💬 Datos iniciales para la BD
│   │   │
│   │   ├── google/
│   │   │   ├── google_sheets_client.py
│   │   │   └── google_sheets_adapter.py
│   │   │   💬 Integración con Google Sheets (API externa)
│   │   │
│   │   ├── dependencies/
│   │   │   └── dependency_injection.py
│   │   │   💬 Inyección de dependencias (wiring de la app)
│   │
│   │   🎯 Responsabilidad:
│   │   - Implementar detalles técnicos (DB, APIs externas)
│   │   - Adaptar interfaces del dominio
│   │   - NO contener lógica de negocio
│
│   └── requirements.txt
│
├── docs/  formato Benn (backend-only)
│    ├── 01_global
│    │   ├── vision.md
│    │   ├── actores.md
│    │   ├── reglas_negocio.md
│    │   └── alcance.md
│    ├── 02_tecnico
│    │   ├── modelo_datos_global.md
│    │   ├── decisiones_tecnicas.md
│    │   └── diagramas
│    │       ├── arquitectura
│    │       ├── caso_uso
│    │       ├── diagrama_clases
│    │       ├── diagrama_objetos
│    │       ├── er
│    │       └── secuencia
│    ├── 03_procesos
│    │   └── definicion_listo.md
│    ├── 04_historias_usuario
│    │   ├── HU-01 .. HU-08 (5 archivos c/u: HU-0X, caso_uso_expandido, api, modelos_datos, pruevas)
│    └── 07_metodologia_agil
│        └── metodoKanban.md
│   💬 Documentación completa del sistema:
│   - 8 historias de usuario (formato Benn)
│   - Reglas de negocio
│   - Modelo de datos
│   - Diagramas UML y ER
│
├── tests/  🧪 TESTING
│   ├── conftest.py   ← aísla los tests de DATABASE_URL (valor por defecto)
│   └──  unit/
│        └── domian/
│            └── services/
│                ├── test_data_key_mapper.py
│                ├── test_data_transformer.py
│                ├── test_normalizacion.py
│                └── test_validacion.py
│   💬 Tests unitarios del dominio (normalización, validación, etc.)
│
│   🎯 Responsabilidad:
│   - Validar reglas de negocio
│   - Asegurar comportamiento correcto del sistema
│
├── face_1_cierre.md 
│   💬 Documentación faces del proyecto
│
├── README.md  
│   💬 Documentación principal del proyecto
│
└── alembic.ini  
    💬 Configuración de migraciones
```

---

## 🧠 Resumen de Arquitectura

```
Presentation (FastAPI)
        ↓
Application (Use Cases)
        ↓
Domain (Entities + Rules + Ports)
        ↓
Infrastructure (DB, APIs externas)
```

---

## 🎯 Principios Aplicados

* ✔️ Separación de responsabilidades
* ✔️ Inversión de dependencias (DIP)
* ✔️ Arquitectura Hexagonal (Ports & Adapters)
* ✔️ Dominio desacoplado de frameworks
* ✔️ Código testeable y mantenible

---

## 🚀 Beneficios

* Escalable
* Testeable
* Independiente de tecnologías externas
* Fácil de mantener y extender


---

## ✅ Estado del proyecto

✔ Fase 1 — Documentación funcional: FINALIZADA

La documentación fue revisada y validada asegurando coherencia entre visión, alcance, reglas de negocio, casos de uso, API y modelo de datos.

📄 Ver detalle del cierre: [fase_1_cierre.md](face_1_cierre.md)

✔ Fase 2 — Diseño técnico y arquitectura: FINALIZADA

Clean Architecture + Hexagonal (Ports & Adapters), SQLAlchemy 2.0 async, DI con `Depends(get_*_ucN)`.

✔ Fase 3 — Implementación API REST: FINALIZADA

Casos de uso implementados y endpoints expuestos (ver sección de estructura). El pipeline de importación es un UC único con lógica de dominio pura en `importacion_pipeline.py`.

🔄 Fase 4 — Pruebas y validación: EN CURSO

Suite de tests unitarios de dominio: **100/100 OK** (`python -m pytest -q` desde la raíz).

---

## 🗺️ Roadmap

- Fase 1: Documentación funcional ✔
- Fase 2: Diseño técnico y arquitectura ✔
- Fase 3: Implementación API REST ✔
- Fase 4: Pruebas y validación (en curso)
- Pendientes: activar `POST /sync/sheets/export` (UC6), UC4b marcado de errores en la hoja

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
