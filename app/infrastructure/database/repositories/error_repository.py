from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.error_repository_port import ErrorRepositoryPort
from app.infrastructure.database.orm_models.error_validacion_orm import (
    ErrorValidacionORM,
)


class ErrorRepository(ErrorRepositoryPort):
    """
    Implementación concreta del repositorio de errores de validación.

    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def registrar_error(
        self,
        id_importacion: int,
        registro_origen: str,
        campo: str,
        descripcion_error: str,
        row_number: int,
    ) -> None:
        """
        Persiste un error de validación asociado a la importación (AF-RN12).
        """
        error = ErrorValidacionORM(
            id_importacion=id_importacion,
            registro_origen=registro_origen[:500],
            campo=campo,
            descripcion_error=descripcion_error,
            row_number=row_number,
        )
        self._session.add(error)
        await self._session.flush()
