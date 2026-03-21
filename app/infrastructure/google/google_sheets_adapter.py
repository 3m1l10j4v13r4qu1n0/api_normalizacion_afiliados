import asyncio
from app.domain.models.list_sheet_rows import ListSheetRows
from app.domain.ports.sheet_data_port import SheetDataPort

class GoogleSheetsAdapter(SheetDataPort):

    def __init__(self, client):
        self.client = client

    async def fetch_rows(self, range_name: str) -> ListSheetRows:
        loop = asyncio.get_event_loop()

        raw_values = await loop.run_in_executor(
            None,
            self.client.read_range,
            range_name
        )

        return ListSheetRows(values=raw_values)