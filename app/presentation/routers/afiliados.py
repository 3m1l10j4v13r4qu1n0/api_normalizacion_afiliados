from fastapi import APIRouter, Depends

from app.presentation.schemas.afiliados_schema import (
    AfiliadoUpdate,
    AfiliadoResponse,
)
from app.presentation.schemas.importacion_schema import (
    ImportRequest,
    AfiliadoCreate,
    ImportResponse,
)

from app.infrastructure.dependencies.dependency_injection import get_importar_desde_api_uc1a
from app.infrastructure.dependencies.dependency_injection import get_agregar_afiliado_uc1b
from app.infrastructure.dependencies.dependency_injection import get_listar_afiliados_uc2
from app.infrastructure.dependencies.dependency_injection import get_obtener_afiliado_por_id_uc2
from app.infrastructure.dependencies.dependency_injection import get_actualizar_afiliado_uc3
from app.infrastructure.dependencies.dependency_injection import get_dar_baja_afiliado_uc5
from app.application.use_cases.uc1a_importar_lista_afiliados import ImportarDesdeAPIUseCase
from app.application.use_cases.uc1b_agregar_afiliado import AgregarAfiliadoUseCase
from app.application.use_cases.uc2_obtener_afiliado_por_id import ObtenerAfiliadoPorIdUseCase
from app.application.use_cases.uc2_listar_afiliados import ListarAfiliadosUseCase
from app.application.use_cases.uc3_actualizar_afiliado import ActualizarAfiliadoUseCase
from app.application.use_cases.uc5_dar_baja_afiliado import DarBajaAfiliadoUseCase

router = APIRouter(prefix="/afiliados", tags=["Afiliados"])


@router.post("/import", response_model=ImportResponse, status_code=201)
async def importar_desde_api(
    request: ImportRequest,
    uc: ImportarDesdeAPIUseCase = Depends(get_importar_desde_api_uc1a),
):
    return await uc.execute(request.afiliados)

@router.post("/", response_model=ImportResponse, status_code=201)
async def agregar_afiliado(
    request: AfiliadoCreate,
    uc: AgregarAfiliadoUseCase = Depends(get_agregar_afiliado_uc1b)
):
    return await uc.execute(request.model_dump())


@router.get("/", response_model=list[AfiliadoResponse])
async def listar_afiliados_endpoint(
    uc: ListarAfiliadosUseCase = Depends(get_listar_afiliados_uc2)
):
    return await uc.execute()

@router.get("/{afiliado_id}", response_model=AfiliadoResponse)
async def obtener_afiliado_endpoint(
    afiliado_id: int,
    uc: ObtenerAfiliadoPorIdUseCase = Depends(get_obtener_afiliado_por_id_uc2)   
):
    return await uc.execute(afiliado_id)


@router.patch("/{afiliado_id}", response_model=AfiliadoResponse)
async def actualizar_afiliado_endpoint(
    afiliado_id: int,
    datos: AfiliadoUpdate,
    uc: ActualizarAfiliadoUseCase = Depends(get_actualizar_afiliado_uc3),
):
    datos
    return await uc.execute(afiliado_id, datos)


@router.delete("/{afiliado_id}", status_code=200)
async def dar_baja_afiliado(
    afiliado_id: int,
    uc: DarBajaAfiliadoUseCase = Depends(get_dar_baja_afiliado_uc5),
):
    return await uc.execute(afiliado_id)