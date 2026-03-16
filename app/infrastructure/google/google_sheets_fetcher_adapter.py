from domain.ports.outgoing.sheet_data_fetcher_port import SheetDataFetcherPort
from domain.models.raw_data import RawData
from infrastructure.google.google_sheets_client import GspreadSheetsClient

class GoogleSheetsFetcherAdapter(SheetDataFetcherPort):
    """
    ADAPTADOR DE SALIDA: Implementa el puerto SheetDataFetcherPort
    usando la API real de Google Sheets.
    """
    
    def __init__(self, client: GspreadSheetsClient):
        self.client = client
    
    async def fetch(self, range_name: str) -> RawData:
        # Llamada real a la API externa
        response = await self.client.read_range(range_name)
        
        # Convierte la respuesta externa a nuestro modelo del dominio
        return RawData(
            values=response,
            source="raw_data"
        )