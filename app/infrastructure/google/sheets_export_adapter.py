import asyncio

from app.domain.models.afiliado_export_row import AfiliadoExportRow
from app.domain.ports.sheet_export_port import SheetExportPort
from app.infrastructure.google.google_sheets_client import GspreadSheetsClient


class SheetsExportAdapter(SheetExportPort):
    """Adapter que implementa SheetExportPort usando gspread."""

    def __init__(self, client: GspreadSheetsClient) -> None:
        self._client = client

    async def exportar_tabla(
        self,
        titulo_hoja: str,
        encabezados: list[str],
        filas: list[AfiliadoExportRow],
    ) -> None:
        datos = [
            [fila.nombre_apellido, str(fila.edad), fila.dni, fila.numero_legajo, fila.email]
            for fila in filas
        ]
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self._client.exportar_tabla,
            titulo_hoja,
            encabezados,
            datos,
        )
