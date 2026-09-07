from typing import Dict, Any, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.afiliado.afiliado_command_port import AfiliadoCommandPort
from app.infrastructure.database.orm_models.afiliado_orm import AfiliadoORM


class AfiliadoCommandRepository(AfiliadoCommandPort):
    """
    Implementación de escritura de afiliados con SQLAlchemy async.
    Solo implementa AfiliadoCommandPort — no puede consultar ni importar.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def update_afiliado( # type: ignore
        self, afiliado_id: int, datos: Dict[str, Any]
    ) -> Optional[AfiliadoORM]:
        """
        UC3  — Actualiza los campos recibidos en datos.
        RF12 — Permitir actualizar datos de afiliados.
        Solo modifica los campos presentes en datos (exclude_unset).
        """
        afiliado = await self._session.get(AfiliadoORM, afiliado_id)
        if afiliado is None:
            return None
        for campo, valor in datos.items():
            setattr(afiliado, campo, valor)
        await self._session.flush()
        return afiliado

    async def buscar_por_email_excluyendo_id( # type: ignore
        self, email: str, afiliado_id: int
    ) -> Optional[AfiliadoORM]:
        """
        Verifica que el email no esté en uso por otro afiliado.
        """
        resultado = await self._session.execute(
            select(AfiliadoORM)
            .where(AfiliadoORM.email == email)
            .where(AfiliadoORM.id != afiliado_id)
        )
        return resultado.scalar_one_or_none()
    

    async def dar_baja(self, afiliado_id: int) -> Optional[AfiliadoORM]: # type: ignore
        """
        UC5  — Baja lógica del afiliado
        AF-RN16 — La eliminación debe realizarse mediante baja lógica
        """
        afiliado = await self._session.get(AfiliadoORM, afiliado_id)
        if afiliado is None:
            return None
        afiliado.id_estado_afiliado = 2 # type: ignore
        await self._session.flush()
        return afiliado