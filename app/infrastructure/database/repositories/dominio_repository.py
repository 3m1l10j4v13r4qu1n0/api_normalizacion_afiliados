from typing import ClassVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.dominio import Dominio
from app.domain.ports.dominio_repository_port import DominioRepositoryPort
from app.infrastructure.database.orm_models.dominios_orm import (
    EstadoAfiliadoORM,
    EstadoCivilORM,
    GeneroORM,
    NivelEducativoORM,
    RelacionDependenciaORM,
)

"""
AF-RN17 — Los atributos género, estado civil, nivel educativo, 
relación de dependencia y estado del afiliado deben pertenecer a 
valores controlados almacenados en entidades de dominio.

"""


class DominioRepository(DominioRepositoryPort):
    """
    Implementación concreta para resolver tablas de valores controlados.

    Recibe un enum `Dominio` (abstracto, definido en el dominio) y lo
    mapea internamente a la clase ORM correspondiente. De esta forma el
    dominio queda desacoplado de SQLAlchemy (solamente este adapter
    conoce los ORMs).

    Example:
        id_genero = await dominio_repo.resolver_o_crear(Dominio.GENERO, "Masculino")
        id_estado = await dominio_repo.resolver_o_crear(Dominio.ESTADO_CIVIL, "Soltero")
    """

    _ORM_POR_DOMINIO: ClassVar[dict] = {
        Dominio.GENERO: GeneroORM,
        Dominio.ESTADO_CIVIL: EstadoCivilORM,
        Dominio.NIVEL_EDUCATIVO: NivelEducativoORM,
        Dominio.RELACION_DEPENDENCIA: RelacionDependenciaORM,
        Dominio.ESTADO_AFILIADO: EstadoAfiliadoORM,
    }

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def resolver_o_crear(
        self,
        dominio: Dominio,
        descripcion: str | None,
    ) -> int | None:
        """
        Busca por descripción en la tabla del ORM correspondiente al dominio.
        Crea el registro si no existe. Retorna el ID.
        """
        if not descripcion or not descripcion.strip():
            return None

        descripcion = descripcion.strip().upper()
        orm_class = self._ORM_POR_DOMINIO[dominio]

        resultado = await self._session.execute(
            select(orm_class).where(orm_class.descripcion == descripcion)
        )
        registro = resultado.scalar_one_or_none()

        if registro is None:
            registro = orm_class(descripcion=descripcion)
            self._session.add(registro)
            await self._session.flush()

        return registro.id
