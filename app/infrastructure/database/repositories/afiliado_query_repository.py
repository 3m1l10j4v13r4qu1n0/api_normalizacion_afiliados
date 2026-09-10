from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.afiliado.afiliado_query_port import AfiliadoQueryPort
from app.infrastructure.database.orm_models.afiliado_orm import AfiliadoORM


class AfiliadoQueryRepository(AfiliadoQueryPort):
    """
    Implementación de consultas de afiliados con SQLAlchemy async.

    Solo implementa AfiliadoQueryPort — no puede escribir ni importar.
    La sesión se inyecta desde el contenedor de dependencias.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def listar(self) -> list[AfiliadoORM]:
        """
        UC2  — Obtiene todos los afiliados almacenados
        RF10 — Permitir consultar afiliados
        """
        resultado = await self._session.execute(select(AfiliadoORM))
        return resultado.scalars().all()

    async def obtener_por_id(self, afiliado_id: int) -> AfiliadoORM | None:
        """
        UC2  — Obtiene un afiliado por su ID
        RF11 — Permitir consultar afiliado por identificador

        Returns:
            AfiliadoORM si existe, None si no.
            El use case es responsable de lanzar AfiliadoNoEncontrado.
        """
        return await self._session.get(AfiliadoORM, afiliado_id)
