import asyncio

from app.domain.models.sheet_raw_data import SheetRawData
from app.domain.ports.sheet_data_port import SheetDataPort
from app.infrastructure.google.google_sheets_client import GspreadSheetsClient


class GoogleSheetsAdapter(SheetDataPort):

    def __init__(self, client: GspreadSheetsClient):
        self.client = client

    async def fetch_rows(self, range_name: str) -> SheetRawData:
        loop = asyncio.get_event_loop()

        raw_values = await loop.run_in_executor(
            None, self.client.read_range, range_name
        )

        return SheetRawData(values=raw_values)
