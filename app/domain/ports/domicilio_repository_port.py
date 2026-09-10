from abc import ABC, abstractmethod


class DomicilioRepositoryPort(ABC):
    """
    Puerto de salida para el repositorio de domicilios.
    """

    @abstractmethod
    async def resolver_o_crear(
        self,
        direccion: str | None,
        localidad: str | None,
        provincia: str | None,
        codigo_postal: str | None,
    ) -> int:
        """
        Busca un domicilio existente por localidad + provincia.
        Si no existe, crea la provincia, la localidad y el domicilio.

        Parameters:
            direccion     : str | None — Calle y número.
            localidad     : str | None — Nombre de la localidad.
            provincia     : str | None — Nombre de la provincia.
            codigo_postal : str | None — Código postal.

        Returns:
            int — ID del domicilio resuelto o creado.
        """
        ...
