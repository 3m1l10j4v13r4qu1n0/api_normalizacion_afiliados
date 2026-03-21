from typing import List
from app.domain.ports.sheet_data_port import SheetDataPort


class ImportSheetUseCase:
    """
    Caso de uso: importar datos desde una hoja.
    Depende de un puerto, no de implementaciones concretas.
    """

    def __init__(self, sheet_port: SheetDataPort):
        self.sheet_port = sheet_port

    async def process_sheet(self, range_name: str) -> List:
        raw_data = await self.sheet_port.fetch_rows(range_name)

        if not raw_data:
            raise ValueError("No data found")

        return raw_data