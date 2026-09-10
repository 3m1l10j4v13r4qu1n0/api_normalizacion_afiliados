from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.domicilio_repository_port import DomicilioRepositoryPort
from app.infrastructure.database.orm_models.domicilio_orm import (
    DomicilioORM,
    LocalidadORM,
    ProvinciaORM,
)


class DomicilioRepository(DomicilioRepositoryPort):
    """
    Implementación concreta del repositorio de domicilios.

    Resuelve o crea provincia → localidad → domicilio en ese orden,
    garantizando integridad referencial.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def resolver_o_crear(
        self,
        direccion: str | None,
        localidad: str | None,
        provincia: str | None,
        codigo_postal: str | None,
    ) -> int:
        """
        Busca o crea provincia → localidad → domicilio y retorna el id_domicilio.
        """
        id_provincia = await self._resolver_o_crear_provincia(provincia)
        id_localidad = await self._resolver_o_crear_localidad(localidad, id_provincia)
        id_domicilio = await self._resolver_o_crear_domicilio(
            direccion, codigo_postal, id_localidad
        )
        return id_domicilio

    # -----------------------------------------------------------------------
    # Privados
    # -----------------------------------------------------------------------

    async def _resolver_o_crear_provincia(self, nombre: str | None) -> int | None:
        if not nombre:
            return None
        nombre = nombre.strip().upper()
        resultado = await self._session.execute(
            select(ProvinciaORM).where(ProvinciaORM.nombre == nombre)
        )
        provincia = resultado.scalar_one_or_none()
        if provincia is None:
            provincia = ProvinciaORM(nombre=nombre)
            self._session.add(provincia)
            await self._session.flush()
        return provincia.id

    async def _resolver_o_crear_localidad(
        self,
        nombre: str | None,
        id_provincia: int | None,
    ) -> int | None:
        if not nombre:
            return None
        nombre = nombre.strip().upper()
        resultado = await self._session.execute(
            select(LocalidadORM).where(
                LocalidadORM.nombre == nombre,
                LocalidadORM.id_provincia == id_provincia,
            )
        )
        localidad = resultado.scalar_one_or_none()
        if localidad is None:
            localidad = LocalidadORM(nombre=nombre, id_provincia=id_provincia)
            self._session.add(localidad)
            await self._session.flush()
        return localidad.id

    async def _resolver_o_crear_domicilio(
        self,
        direccion: str | None,
        codigo_postal: str | None,
        id_localidad: int | None,
    ) -> int | None:
        if not direccion and not id_localidad:
            return None
        domicilio = DomicilioORM(
            direccion=direccion.strip() if direccion else None,
            codigo_postal=codigo_postal.strip() if codigo_postal else None,
            id_localidad=id_localidad,
        )
        self._session.add(domicilio)
        await self._session.flush()
        return domicilio.id
