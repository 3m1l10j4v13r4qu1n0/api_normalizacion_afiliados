# presentation/routers/afiliados.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.connection import get_db
from app.presentation.schemas.afiliados_schema import (
    AfiliadoUpdate,
    AfiliadoResponse,
)
from app.presentation.schemas.importacion_schema import (
    ImportRequest,
    ImportResponse,
)
from app.application.services.afiliado_service import (
    listar_afiliados,
    obtener_afiliado_por_id,
    actualizar_afiliado,
    dar_baja_afiliado,
)
from app.application.services.importacion_service import importar_afiliados
from app.domain.exceptions import DatoInvalidoError, ImportacionError

router = APIRouter(prefix="/afiliados", tags=["Afiliados"])


@router.post("/import", response_model=ImportResponse, status_code=201)
async def importar_afiliados_endpoint(
    datos: ImportRequest,
    db: AsyncSession = Depends(get_db)
):
    if not datos.afiliados:
        raise DatoInvalidoError("La lista de afiliados no puede estar vacía")
    try:
        resultado = await importar_afiliados(
            db        = db,
            registros = [a.model_dump() for a in datos.afiliados]
        )
        return ImportResponse(
            cantidad_registros_procesados = resultado.cantidad_registros,
            cantidad_registros_validos    = resultado.cantidad_validos,
            cantidad_errores              = resultado.cantidad_errores
        )
    except Exception as e:
        raise ImportacionError(str(e))


@router.get("", response_model=list[AfiliadoResponse])
async def listar_afiliados_endpoint(db: AsyncSession = Depends(get_db)):
    return await listar_afiliados(db)


@router.get("/{afiliado_id}", response_model=AfiliadoResponse)
async def obtener_afiliado_endpoint(
    afiliado_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await obtener_afiliado_por_id(db, afiliado_id)


@router.put("/{afiliado_id}", response_model=AfiliadoResponse)
async def actualizar_afiliado_endpoint(
    afiliado_id: int,
    datos: AfiliadoUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await actualizar_afiliado(
        db          = db,
        afiliado_id = afiliado_id,
        datos       = datos.model_dump(exclude_none=True)  # ← solo campos que llegaron
    )


@router.delete("/{afiliado_id}", status_code=200)
async def dar_baja_afiliado_endpoint(
    afiliado_id: int,
    db: AsyncSession = Depends(get_db)
):
    await dar_baja_afiliado(db, afiliado_id)
    return {"mensaje": f"Afiliado {afiliado_id} marcado como inactivo"}
