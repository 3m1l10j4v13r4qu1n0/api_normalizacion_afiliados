from fastapi import APIRouter, Depends

from app.application.use_cases.core_importar_afiliado import ImportarAfiliadoUseCase
from app.application.use_cases.uc2_listar_afiliados import ListarAfiliadosUseCase
from app.application.use_cases.uc2_obtener_afiliado_por_id import (
    ObtenerAfiliadoPorIdUseCase,
)
from app.application.use_cases.uc3_actualizar_afiliado import ActualizarAfiliadoUseCase
from app.application.use_cases.uc5_dar_baja_afiliado import DarBajaAfiliadoUseCase
from app.infrastructure.dependencies.dependency_injection import (
    get_actualizar_afiliado_uc3,
    get_dar_baja_afiliado_uc5,
    get_importar_afiliado_core,
    get_listar_afiliados_uc2,
    get_obtener_afiliado_por_id_uc2,
)
from app.presentation.schemas.afiliados_schema import (
    AfiliadoResponse,
    AfiliadoUpdate,
)
from app.presentation.schemas.importacion_schema import (
    AfiliadoCreate,
    ImportRequest,
    ImportResponse,
    import_response_from_importacion,
)

router = APIRouter(prefix="/afiliados", tags=["Afiliados"])


@router.post("/import", response_model=ImportResponse, status_code=201)
async def importar_desde_api(
    request: ImportRequest,
    core_uc: ImportarAfiliadoUseCase = Depends(get_importar_afiliado_core),
):
    datos = [afiliado.model_dump() for afiliado in request.afiliados]
    importacion = await core_uc.importar_desde_dicts(datos)
    return import_response_from_importacion(importacion)


@router.post("/", response_model=ImportResponse, status_code=201)
async def agregar_afiliado(
    request: AfiliadoCreate,
    core_uc: ImportarAfiliadoUseCase = Depends(get_importar_afiliado_core),
):
    importacion = await core_uc.agregar_afiliado(request.model_dump())
    return import_response_from_importacion(importacion)


@router.get("/", response_model=list[AfiliadoResponse])
async def listar_afiliados_endpoint(
    uc: ListarAfiliadosUseCase = Depends(get_listar_afiliados_uc2),
):
    return await uc.execute()


@router.get("/{afiliado_id}", response_model=AfiliadoResponse)
async def obtener_afiliado_endpoint(
    afiliado_id: int,
    uc: ObtenerAfiliadoPorIdUseCase = Depends(get_obtener_afiliado_por_id_uc2),
):
    return await uc.execute(afiliado_id)


@router.patch("/{afiliado_id}", response_model=AfiliadoResponse)
async def actualizar_afiliado_endpoint(
    afiliado_id: int,
    datos: AfiliadoUpdate,
    uc: ActualizarAfiliadoUseCase = Depends(get_actualizar_afiliado_uc3),
):
    return await uc.execute(afiliado_id, datos)


@router.delete("/{afiliado_id}", status_code=200)
async def dar_baja_afiliado(
    afiliado_id: int,
    uc: DarBajaAfiliadoUseCase = Depends(get_dar_baja_afiliado_uc5),
):
    return await uc.execute(afiliado_id)
