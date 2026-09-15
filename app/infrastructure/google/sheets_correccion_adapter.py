import asyncio

from app.domain.models.sheet_raw_data import SheetRawData
from app.domain.ports.sheet_correccion_port import SheetCorreccionPort
from app.infrastructure.google.google_sheets_client import GspreadSheetsClient


class SheetsCorreccionAdapter(SheetCorreccionPort):
    """Adapter de la hoja de pendientes de corrección en Google Sheets."""

    def __init__(self, client: GspreadSheetsClient) -> None:
        self._client = client

    async def guardar_pendientes(
        self,
        encabezados: list[str],
        filas: list[list[str]],
    ) -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self._client.guardar_pendientes,
            encabezados,
            filas,
        )

    async def leer_pendientes(self, range_name: str) -> SheetRawData:
        loop = asyncio.get_event_loop()
        values = await loop.run_in_executor(
            None,
            self._client.leer_pendientes,
            range_name,
        )
        return SheetRawData(values=values)
