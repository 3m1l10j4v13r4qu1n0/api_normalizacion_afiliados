from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.infrastructure.core.config import settings
from app.presentation.handlers import registrar_handlers
from app.presentation.routers.afiliados import router as afiliados_router
from app.presentation.routers.sync import router as sync_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Eventos de inicio y cierre de la aplicación
    Reemplaza el deprecado @app.on_event("startup")
    """
    # ── Inicio ──────────────────────────────────────
    print(f"🚀 Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"🔧 Modo DEBUG: {settings.DEBUG}")
    yield
    # ── Cierre ──────────────────────────────────────
    print("👋 Cerrando aplicación")


app = FastAPI(
    title       = settings.APP_NAME,
    version     = settings.APP_VERSION,
    debug       = settings.DEBUG,
    description = """
    API REST para la gestión y normalización de datos de afiliados.

    Permite importar, validar, normalizar, consultar y sincronizar
    datos de afiliados con Google Sheets.
    """,
    lifespan    = lifespan
)

# ── Handlers de errores ──────────────────────────────────────────────
registrar_handlers(app)

# ── Routers ──────────────────────────────────────────────────────────
app.include_router(afiliados_router)
app.include_router(sync_router)


# ── Health check ─────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def health_check():
    return {
        "estado"  : "ok",
        "app"     : settings.APP_NAME,
        "version" : settings.APP_VERSION,
    }