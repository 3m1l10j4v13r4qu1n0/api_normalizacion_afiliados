from abc import ABC, abstractmethod

from app.domain.models.dominio import Dominio


class DominioRepositoryPort(ABC):
    """
    Puerto de salida para la resolución de tablas de valores controlados.
    Ubicación: app/domain/ports/dominio_repository_port.py

    Resuelve cualquier tabla de dominio (generos, estados_civiles,
    niveles_educativos, relaciones_dependencia, estados_afiliado)
    buscando por descripción y creando el registro si no existe.

    Recibe un enum `Dominio` (abstracto) en lugar de la clase ORM para
    mantener el dominio desacoplado de SQLAlchemy; el adapter mapea el
    enum a la tabla concreta internamente.
    """

    @abstractmethod
    async def resolver_o_crear(
        self,
        dominio: Dominio,
        descripcion: str | None,
    ) -> int | None:
        """
        Busca un registro por descripción en la tabla correspondiente al dominio.
        Si no existe, lo crea.

        Parameters:
            dominio     : Dominio — Valor controlado a resolver (AF-RN17).
            descripcion : str     — Valor a buscar/crear (ej: "Masculino").

        Returns:
            int | None — ID del registro resuelto o creado.
                         None si descripcion es None o vacía.
        """
        ...
