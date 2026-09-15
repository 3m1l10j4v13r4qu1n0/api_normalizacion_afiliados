from fastapi import APIRouter, Depends

from app.application.use_cases.core_importar_afiliado import ImportarAfiliadoUseCase
from app.application.use_cases.uc4a_importar_afiliado import ImportSheetUseCase
from app.application.use_cases.uc6_actualizar_hoja_pendientes import (
    ActualizarHojaPendientesUseCase,
)
from app.application.use_cases.uc8_exportar_afiliados_sheets import (
    ExportarAfiliadosSheetsUseCase,
)
from app.domain.exceptions import SincronizacionError
from app.domain.ports.sheet_correccion_port import TITULO_HOJA_PENDIENTES
from app.infrastructure.dependencies.dependency_injection import (
    get_actualizar_pendientes_uc6,
    get_exportar_afiliados_uc8,
    get_import_sheet_uc4a,
    get_importar_afiliado_uc4,
)
from app.presentation.schemas.importacion_schema import (
    ExportResponse,
    ImportResponse,
    import_response_from_importacion,
)

router = APIRouter(prefix="/sync", tags=["Sincronización"])

RANGO_PENDIENTES = f"{TITULO_HOJA_PENDIENTES}!A1:Z"


@router.post("/sheets/import", response_model=ImportResponse, status_code=201)
async def importar_desde_sheets_endpoint(
    sheet_uc: ImportSheetUseCase = Depends(get_import_sheet_uc4a),
    core_uc: ImportarAfiliadoUseCase = Depends(get_importar_afiliado_uc4),
    correccion_uc: ActualizarHojaPendientesUseCase = Depends(
        get_actualizar_pendientes_uc6
    ),
):
    """UC4 — Importar afiliados desde Google Sheets y generar pendientes (HU-06)"""

    # 🔹 UC4a — leer y transformar el sheet (source)
    lectura = await sheet_uc.execute(range_name="A1:Z")

    # 🔹 CORE — lógica de negocio
    resultado = await core_uc.execute(lectura.input_rows)

    # 🔹 UC6 — actualizar la hoja de pendientes de corrección (HU-06)
    await _actualizar_pendientes_sin_interrumpir(
        correccion_uc, lectura.encabezados, lectura.valores_crudos, resultado.errores
    )

    return import_response_from_importacion(resultado)


@router.post("/sheets/reimport", response_model=ImportResponse, status_code=201)
async def reimportar_pendientes_endpoint(
    sheet_uc: ImportSheetUseCase = Depends(get_import_sheet_uc4a),
    core_uc: ImportarAfiliadoUseCase = Depends(get_importar_afiliado_uc4),
    correccion_uc: ActualizarHojaPendientesUseCase = Depends(
        get_actualizar_pendientes_uc6
    ),
):
    """UC4 — Reimportar las filas corregidas desde la hoja de pendientes (HU-06)"""

    # 🔹 UC4a — leer y transformar la hoja de pendientes (source de corrección)
    lectura = await sheet_uc.execute(range_name=RANGO_PENDIENTES)

    # 🔹 CORE — lógica de negocio
    resultado = await core_uc.execute(lectura.input_rows)

    # 🔹 UC6 — dejar en la hoja de pendientes solo lo que sigue fallando
    await _actualizar_pendientes_sin_interrumpir(
        correccion_uc, lectura.encabezados, lectura.valores_crudos, resultado.errores
    )

    return import_response_from_importacion(resultado)


async def _actualizar_pendientes_sin_interrumpir(
    correccion_uc: ActualizarHojaPendientesUseCase,
    encabezados: list[str],
    valores_crudos: list[list[str]],
    errores,
) -> None:
    # HU-06 — el fallo al actualizar pendientes no interrumpe la importación
    try:
        await correccion_uc.execute(encabezados, valores_crudos, errores)
    except SincronizacionError:
        pass


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
