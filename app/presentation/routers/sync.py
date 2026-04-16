from fastapi import APIRouter, Depends

from app.presentation.schemas.importacion_schema import ImportResponse
from app.application.use_cases.uc4_importar_afiliado import ImportarDesdeSheetUseCase

from app.infrastructure.dependencies.dependency_injection import get_importar_afiliado_uc4



router = APIRouter(prefix="/sync", tags=["Sincronización"])

@router.post("/sheets/import", response_model=ImportResponse, status_code=201)
async def importar_desde_sheets_endpoint(
    uc4: ImportarDesdeSheetUseCase = Depends(get_importar_afiliado_uc4)
):
    """UC4 — Importar afiliados desde Google Sheets"""

    # 🔹 UC4 → lógica de negocio
    resultado = await uc4.execute(range_name="Respuestas!A1:Z")

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
