import asyncio

from app.domain.ports.sheet_marking_port import SheetMarkingPort
from app.infrastructure.google.google_sheets_client import GspreadSheetsClient


class SheetsMarkingAdapter(SheetMarkingPort):
    """Adapter de marcación de filas con errores en Google Sheets."""

    def __init__(self, client: GspreadSheetsClient):
        self.client = client

    async def marcar_filas_con_errores(
        self,
        row_numbers: list[int],
    ) -> None:
        if not row_numbers:
            return

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self.client.marcar_filas_con_errores,
            row_numbers,
        )
