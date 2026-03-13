from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.connection import get_db
from app.infrastructure.sheets.sheets_client import GspreadSheetsClient
from app.presentation.schemas.importacion_schema import ImportResponse
from app.application.services.sheets_service import (
    importar_desde_sheets, 
    exportar_a_sheets,
)
from app.domain.exceptions import ImportacionError, SincronizacionError

router = APIRouter(prefix="/sync", tags=["Sincronización"])


@router.post("/sheets/import", response_model=ImportResponse, status_code=201)
async def importar_desde_sheets_endpoint(db: AsyncSession = Depends(get_db)):
    """UC4 — Importar afiliados desde Google Sheets"""
    try:
        cliente   = GspreadSheetsClient()       # ← instancia la implementación concreta
        resultado = await importar_desde_sheets(db, cliente=cliente)
        return ImportResponse(
            cantidad_registros_procesados = resultado.cantidad_registros,
            cantidad_registros_validos    = resultado.cantidad_validos,
            cantidad_errores              = resultado.cantidad_errores
        )
    except SincronizacionError:
        raise
    except Exception as e:
        raise ImportacionError(str(e))


@router.post("/sheets/export", status_code=200)
async def exportar_a_sheets_endpoint(db: AsyncSession = Depends(get_db)):
    """UC6 — Sincronizar afiliados activos hacia Google Sheets"""
    try:
        cliente = GspreadSheetsClient()         # ← instancia la implementación concreta
        return await exportar_a_sheets(db, cliente=cliente)
    except SincronizacionError:
        raise
    except Exception as e:
        raise SincronizacionError(str(e))