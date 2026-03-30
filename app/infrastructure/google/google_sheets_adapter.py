import asyncio
from typing import List
from app.domain.models.input_row import InputRow
from app.domain.ports.sheet_data_port import SheetDataPort

class GoogleSheetsAdapter(SheetDataPort):

    def __init__(self, client):
        self.client = client

    async def fetch_rows(self, range_name: str) -> List[InputRow]:
        loop = asyncio.get_event_loop()

        raw_values = await loop.run_in_executor(
            None,
            self.client.read_range,
            range_name
        )
        InputRow.values=raw_values

        return List[InputRow]