from abc import ABC, abstractmethod
from typing import Optional, Type
from sqlalchemy.orm import DeclarativeBase


class DominioRepositoryPort(ABC):
    """
    Puerto de salida para la resolución de tablas de valores controlados.
    Ubicación: app/domain/ports/dominio_repository_port.py

    Resuelve cualquier tabla de dominio (generos, estados_civiles,
    niveles_educativos, relaciones_dependencia, estados_afiliado)
    buscando por descripción y creando el registro si no existe.
    """

    @abstractmethod
    async def resolver_o_crear(
        self,
        orm_class  : Type[DeclarativeBase],
        descripcion: Optional[str],
    ) -> Optional[int]:
        """
        Busca un registro por descripción en la tabla correspondiente al ORM.
        Si no existe, lo crea.

        Parameters:
            orm_class   : Type — Clase ORM de la tabla (ej: GeneroORM).
            descripcion : str  — Valor a buscar/crear (ej: "Masculino").

        Returns:
            int | None — ID del registro resuelto o creado.
                         None si descripcion es None o vacía.
        """
        ...