# Decisiones Técnicas
## Sistema de Normalización de Datos de Afiliados

---

### 1. Stack tecnológico

| Componente | Tecnología | Motivo |
|---|---|---|
| Lenguaje | Python 3.11+ | Amplio ecosistema para APIs y manejo de datos |
| Framework | FastAPI | Moderno, rápido, validación automática con Pydantic |
| Base de datos | PostgreSQL | Robusto, relacional, alineado con el modelo de datos definido |
| ORM | SQLAlchemy | Estándar en proyectos Python, compatible con Alembic |
| Migraciones | Alembic | Manejo de versiones del esquema de base de datos |
| Integración Google Sheets | gspread + Service Account | Simple de implementar, no requiere login manual, ideal para APIs |
| Validación de datos | Pydantic | Incluido en FastAPI, permite definir esquemas de entrada y salida |
| Variables de entorno | python-dotenv | Manejo seguro de credenciales y configuración |

---

### 2. Autenticación y autorización

Esta API es un **microservicio** que forma parte de un sistema más grande de administración de afiliados.

La autenticación y autorización de usuarios es responsabilidad de un **servicio externo** dentro de ese sistema. Esta API asume que todas las requests entrantes ya fueron autenticadas y autorizadas antes de llegar acá.

#### Lo que esta API NO hace:
- No maneja login ni sesiones de usuario
- No valida tokens JWT
- No gestiona roles ni permisos de usuarios

#### Lo que esta API SÍ hace para integrarse con el sistema mayor:
- Acepta headers como `X-User-ID` y `X-User-Role` enviados por el servicio de autenticación externo
- Registra en los logs quién ejecutó cada operación usando esos headers

---

### 3. Autenticación con Google Sheets

Se optó por **Service Account** en lugar de OAuth2 por los siguientes motivos:

- OAuth2 requiere intervención manual del usuario para autorizar el acceso cada vez que el token expira, lo cual es incompatible con una API que corre en servidor.
- Service Account es un usuario de servicio de Google que no expira y no requiere login interactivo.
- La integración se realiza compartiendo la hoja de cálculo con el email de la Service Account desde Google Drive.
- La librería `gspread` tiene soporte nativo para Service Account y simplifica la implementación.

> Nota: Service Account es exclusivamente para la integración con Google Sheets. No tiene relación con el sistema de login de usuarios del sistema mayor.

---

### 4. Arquitectura del proyecto

Se adoptó **Clean Architecture** (también conocida como Arquitectura Hexagonal), consistente con otros proyectos del sistema mayor. Este enfoque separa claramente las responsabilidades y permite que el dominio del negocio sea independiente de frameworks y servicios externos.

El flujo de una request es unidireccional:
```
Presentation → Application → Domain → Infrastructure
```

Cada capa solo conoce a la de abajo, nunca al revés.

| Capa | Carpeta | Responsabilidad |
|---|---|---|
| Presentación | `presentation/` | Recibe requests HTTP, define schemas de entrada/salida |
| Aplicación | `application/` | Orquesta los casos de uso |
| Dominio | `domain/` | Modelos y reglas puras del negocio, sin dependencias externas |
| Infraestructura | `infrastructure/` | Base de datos, Google Sheets, configuración |

### 5. Estructura de carpetas del proyecto

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
│   │       ├── core_importar_afiliado.py
│   │       ├── uc1a_importar_afiliados.py
│   │       ├── uc1b_importar_afiliado.py
│   │       ├── uc2_listar_afiliado.py
│   │       ├── uc2_obtener_afiliado.py
│   │       ├── uc3_actualizar_afiliado.py
│   │       ├── uc4_importar_afiliado.py
│   │       ├── uc4a_importar_afiliado.py
│   │       └── uc5_dar_baja_afiliado.py
│   │
│   │       💬 Implementación de casos de uso del sistema
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
│   │   │   ├── importacion.py
│   │   │   ├── error_validacion.py
│   │   │   ├── input_row.py
│   │   │   └── mapping.py
│   │   │   💬 Entidades y modelos del dominio (reglas puras)
│   │   │
│   │   ├── services/
│   │   │   ├── normalizacion.py
│   │   │   ├── validacion.py
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
│   │   │   ├── seed.py / seed_runner.py
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
├── docs/ 
│    ├── actores.md
│    ├── alcance.md
│    ├── api.md
│    ├── caso_de_uso_expandidos.md
│    ├── casos_de_uso.md
│    ├── decisiones_tecnicas.md
│    ├── diagramas
│    │   ├── arquitectura
│    │   │   ├── arquitectura_diagrama.png
│    │   │   └── arquitectura_diagrama.puml
│    │   ├── caso_uso
│    │   │   ├── caso_uso.png
│    │   │   └── caso_uso.puml
│    │   ├── diagrama_clases
│    │   │   ├── clases_diagrama.png
│    │   │   └── clases_diagrama.puml
│    │   ├── diagrama_objetos
│    │   │   ├── objeto_diagrama.png
│    │   │   └── objeto_diagrama.puml
│    │   └── er
│    │       ├── er_diagrama.png
│    │       └── er_diagrama.puml
│    ├── modelos_datos.md
│    ├── pruebas.md
│    ├── reglas_negocio.md
│    ├── requerimientos.md
│    └── vision.md
│   💬 Documentación completa del sistema:
│   - Casos de uso
│   - Reglas de negocio
│   - Modelo de datos
│   - Diagramas UML y ER
│
├── tests/  🧪 TESTING
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

### 6. Variables de entorno necesarias

```env
# Base de datos
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/afiliados_db

# Google Sheets
GOOGLE_SERVICE_ACCOUNT_FILE=credentials/service_account.json
GOOGLE_SHEET_ID=id_de_la_hoja_de_calculo
```

---

### 7. Dependencias principales

```txt
fastapi
uvicorn
sqlalchemy
alembic
psycopg2-binary
pydantic
python-dotenv
gspread
google-auth
```