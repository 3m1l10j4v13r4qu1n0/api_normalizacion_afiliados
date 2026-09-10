from fastapi import APIRouter, Depends

from app.application.use_cases.core_importar_afiliado import ImportarAfiliadoUseCase
from app.application.use_cases.uc4a_importar_afiliado import ImportSheetUseCase
from app.application.use_cases.uc6_marcar_errores_sheets import (
    MarcarErroresSheetsUseCase,
)
from app.application.use_cases.uc8_exportar_afiliados_sheets import (
    ExportarAfiliadosSheetsUseCase,
)
from app.domain.exceptions import SincronizacionError
from app.infrastructure.dependencies.dependency_injection import (
    get_exportar_afiliados_uc8,
    get_import_sheet_uc4a,
    get_importar_afiliado_uc4,
    get_marcar_errores_sheets_uc6,
)
from app.presentation.schemas.importacion_schema import (
    ExportResponse,
    ImportResponse,
    import_response_from_importacion,
)

router = APIRouter(prefix="/sync", tags=["Sincronización"])


@router.post("/sheets/import", response_model=ImportResponse, status_code=201)
async def importar_desde_sheets_endpoint(
    sheet_uc: ImportSheetUseCase = Depends(get_import_sheet_uc4a),
    core_uc: ImportarAfiliadoUseCase = Depends(get_importar_afiliado_uc4),
    marking_uc: MarcarErroresSheetsUseCase = Depends(get_marcar_errores_sheets_uc6),
):
    """UC4 — Importar afiliados desde Google Sheets"""

    # 🔹 UC4a — leer y transformar el sheet (source)
    sheet_rows = await sheet_uc.execute(range_name="Respuestas!A1:Z")

    # 🔹 CORE — lógica de negocio
    resultado = await core_uc.execute(sheet_rows)

    # 🔹 UC6 — marcar filas con errores en la hoja (HU-06)
    # SH-UC4b-RN4 — el fallo al marcar no interrumpe la importación
    try:
        await marking_uc.execute(resultado.errores)
    except SincronizacionError:
        pass

    return import_response_from_importacion(resultado)


@router.post("/sheets/export", response_model=ExportResponse, status_code=200)
async def exportar_a_sheets_endpoint(
    uc: ExportarAfiliadosSheetsUseCase = Depends(get_exportar_afiliados_uc8),
):
    """UC8 — Exportar tabla de afiliados activos a Google Sheets"""
    cantidad = await uc.execute()
    return ExportResponse(
        cantidad_registros_procesados=cantidad,
        mensaje="Tabla generada correctamente",
    )
