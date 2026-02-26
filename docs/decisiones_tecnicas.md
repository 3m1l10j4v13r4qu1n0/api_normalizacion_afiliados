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
├── app/
│   ├── main.py                          # Punto de entrada de FastAPI
│   │
│   ├── presentation/                    # CAPA 1 - Presentación
│   │   ├── routers/                     # Endpoints HTTP
│   │   │   ├── afiliados.py             # GET, POST, PUT, DELETE /afiliados
│   │   │   └── sync.py                  # POST /sync/sheets/import y /export
│   │   └── schemas/                     # Esquemas Pydantic (request/response)
│   │       ├── afiliado_schema.py
│   │       └── importacion_schema.py
│   │
│   ├── application/                     # CAPA 2 - Casos de Uso
│   │   ├── uc1_importar_afiliados.py
│   │   ├── uc2_consultar_afiliados.py
│   │   ├── uc3_actualizar_afiliado.py
│   │   ├── uc4_importar_desde_sheets.py
│   │   ├── uc5_dar_baja_afiliado.py
│   │   └── uc6_sincronizar_hacia_sheets.py
│   │
│   ├── domain/                          # CAPA 3 - Dominio
│   │   ├── models/                      # Entidades del negocio
│   │   │   ├── afiliado.py
│   │   │   ├── importacion.py
│   │   │   └── error_validacion.py
│   │   └── rules/                       # Reglas puras de negocio
│   │       ├── validacion.py            # Qué es válido
│   │       └── normalizacion.py         # Cómo se normalizan los datos
│   │
│   └── infrastructure/                  # CAPA 4 - Infraestructura
│       ├── database/
│       │   ├── connection.py            # Configuración PostgreSQL
│       │   ├── orm_models/              # Modelos SQLAlchemy
│       │   │   ├── afiliado_orm.py
│       │   │   ├── importacion_orm.py
│       │   │   ├── error_validacion_orm.py
│       │   │   └── dominios_orm.py
│       │   └── repositories/            # Acceso a base de datos
│       │       ├── afiliado_repository.py
│       │       ├── importacion_repository.py
│       │       └── error_repository.py
│       ├── sheets/
│       │   └── sheets_client.py         # Cliente Google Sheets (gspread)
│       └── core/
│           └── config.py                # Variables de entorno
│
├── alembic/                             # Migraciones
├── tests/
│   ├── test_uc1_importar_afiliados.py
│   ├── test_uc4_importar_desde_sheets.py
│   └── test_uc6_sincronizar_sheets.py
├── .env
├── .env.example
├── docs/                                # Documentacion       
│   ├── actores.md        
│   ├── alcance.md              
│   ├── api.md                  
│   ├── caso_de_uso_expandidos.md              
│   ├── casos_de_uso.md                   
│   ├── diagramas/                       # Diagramas            
│   │   ├── arquitectura/               
│   │   │   ├── arquitectura_diagrama.png           
│   │   │   └── arquitectura_diagrama.puml           
│   │   ├── caso_uso/              
│   │   │   ├── caso_uso.png             
│   │   │   └── caso_uso.puml            
│   │   ├── diagrama_clases/                  
│   │   │   ├── clases_diagrama.png            
│   │   │   └── clases_diagrama.puml            
│   │   ├── diagrama_objetos/             
│   │   │   ├── objeto_diagrama.png            
│   │   │   └── objeto_diagrama.puml              
│   │   └── er/                
│   │       ├── er_diagrama.png                
│   │       └── er_diagrama.puml                     
│   ├── modelos_datos.md                       
│   ├── pruebas.md                    
│   ├── reglas_negocio.md               
│   ├── requerimientos.md                     
│   └── vision.md                
├── face_1_cierre.md                     # Estado del proyecto
├── requirements.txt
└── README.md
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