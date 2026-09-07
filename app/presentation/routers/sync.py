from fastapi import APIRouter, Depends

from app.presentation.schemas.importacion_schema import ImportResponse
from app.application.use_cases.core_importar_afiliado import ImportarAfiliadoUseCase
from app.application.use_cases.uc4a_importar_afiliado import ImportSheetUseCase

from app.infrastructure.dependencies.dependency_injection import (
    get_importar_afiliado_uc4,
    get_import_sheet_uc4a,
)


router = APIRouter(prefix="/sync", tags=["Sincronización"])

@router.post("/sheets/import", response_model=ImportResponse, status_code=201)
async def importar_desde_sheets_endpoint(
    sheet_uc: ImportSheetUseCase = Depends(get_import_sheet_uc4a),
    core_uc: ImportarAfiliadoUseCase = Depends(get_importar_afiliado_uc4),
):
    """UC4 — Importar afiliados desde Google Sheets"""

    # 🔹 UC4a — leer y transformar el sheet (source)
    sheet_rows = await sheet_uc.execute(range_name="Respuestas!A1:Z")

    # 🔹 CORE — lógica de negocio
    resultado = await core_uc.execute(sheet_rows)

    return ImportResponse(
        cantidad_registros_procesados=resultado.cantidad_registros,
        cantidad_registros_validos=resultado.cantidad_validos,
        cantidad_errores=resultado.cantidad_errores,
    )



# @router.post("/sheets/export", status_code=200)
# async def exportar_a_sheets_endpoint(db: AsyncSession = Depends(get_db)):
#     """UC6 — 
#       AF-RN14 — Solo se sincronizan afiliados válidos.
#       AF-RN15 — La sincronización no debe modificar datos locales.
#     """
