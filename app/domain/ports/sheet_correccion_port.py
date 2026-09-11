from abc import ABC, abstractmethod

from app.domain.models.sheet_raw_data import SheetRawData

TITULO_HOJA_PENDIENTES = "Pendientes de corrección"


class SheetCorreccionPort(ABC):
    """Puerto para gestionar la hoja de pendientes de corrección en Google Sheets (HU-06)."""

    @abstractmethod
    async def guardar_pendientes(
        self,
        encabezados: list[str],
        filas: list[list[str]],
    ) -> None:
        """
        Reemplaza el contenido de la hoja de pendientes de corrección con las
        filas indicadas, resaltándolas todas en rojo para su revisión.

        Si `filas` está vacía, la hoja queda únicamente con los encabezados
        (refleja que no hay pendientes de corrección).

        Parameters:
            encabezados : list[str] — encabezados de la hoja (incluye el motivo del error).
            filas       : list[list[str]] — filas pendientes de corrección.
        """
        ...

    @abstractmethod
    async def leer_pendientes(self, range_name: str) -> SheetRawData:
        """
        Lee el contenido actual de la hoja de pendientes de corrección.

        Raises:
            SincronizacionError — si la hoja de pendientes no existe todavía.
        """
        ...
