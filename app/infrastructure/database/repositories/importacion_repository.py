from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.importacion_repository_port import ImportacionRepositoryPort
from app.infrastructure.database.orm_models.importacion_orm import ImportacionORM


class ImportacionRepository(ImportacionRepositoryPort):
    """
    Implementación concreta del repositorio de importaciones.

    Responsabilidad: ciclo de vida de la importación (crear y completar).
    Los errores de validación los gestiona ErrorRepository.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def crear_importacion(self, cantidad_registros: int) -> int:
        """
        Crea un registro de importación en estado 'pendiente' y retorna su ID.
        """
        importacion = ImportacionORM(
            cantidad_registros=cantidad_registros,
            cantidad_errores=0,
            estado="pendiente",
        )
        self._session.add(importacion)
        await self._session.flush()
        return importacion.id

    async def completar_importacion(
        self,
        id_importacion: int,
        cantidad_errores: int,
    ) -> None:
        """
        Marca la importación como completada con el total de errores.
        """
        importacion = await self._session.get(ImportacionORM, id_importacion)
        if importacion is None:
            raise ValueError(f"Importación con id={id_importacion} no encontrada.")
        importacion.cantidad_errores = cantidad_errores
        importacion.estado = "completada"
        await self._session.flush()
