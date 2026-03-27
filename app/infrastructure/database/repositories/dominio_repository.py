from typing import Optional, Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.domain.ports.dominio_repository_port import DominioRepositoryPort


class DominioRepository(DominioRepositoryPort):
    """
    Implementación genérica para resolver tablas de valores controlados.
    
    Funciona con cualquier ORM que tenga las columnas `id` y `descripcion`.
    Compatible con: GeneroORM, EstadoCivilORM, NivelEducativoORM,
                    RelacionDependenciaORM, EstadoAfiliadoORM.

    Example:
        id_genero = await dominio_repo.resolver_o_crear(GeneroORM, "Masculino")
        id_estado = await dominio_repo.resolver_o_crear(EstadoCivilORM, "Soltero")
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def resolver_o_crear(
        self,
        orm_class  : Type[DeclarativeBase],
        descripcion: Optional[str],
    ) -> Optional[int]:
        """
        Busca por descripción en la tabla del ORM dado.
        Crea el registro si no existe. Retorna el ID.
        """
        if not descripcion or not descripcion.strip():
            return None

        descripcion = descripcion.strip().upper()

        resultado = await self._session.execute(
            select(orm_class).where(orm_class.descripcion == descripcion)
        )
        registro = resultado.scalar_one_or_none()

        if registro is None:
            registro = orm_class(descripcion=descripcion)
            self._session.add(registro)
            await self._session.flush()

        return registro.id