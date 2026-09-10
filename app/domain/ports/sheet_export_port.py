from abc import ABC, abstractmethod

from app.domain.models.afiliado_export_row import AfiliadoExportRow


class SheetExportPort(ABC):
    """Puerto para exportar filas a una hoja de Google Sheets."""

    @abstractmethod
    async def exportar_tabla(
        self,
        titulo_hoja: str,
        encabezados: list[str],
        filas: list[AfiliadoExportRow],
    ) -> None:
        """
        HU-08 — Exporta una tabla completa a Google Sheets.
        Si la hoja no existe, la crea. Si existe, la limpia y regraba.

        Parameters:
            titulo_hoja: nombre de la hoja a crear/actualizar.
            encabezados: lista de nombres de columna.
            filas: datos a escribir (cada fila se serializa a lista de strings).
        """
        ...
