# src/infrastructure/outgoing/google_sheets/google_sheets_fetcher_adapter.py
from domain.ports.outgoing.sheet_data_fetcher_port import SheetDataFetcherPort
from domain.models.raw_data import RawData
from infrastructure.outgoing.google_sheets.google_sheets_client import GoogleSheetsClient

class GoogleSheetsFetcherAdapter(SheetDataFetcherPort):
    """
    ADAPTADOR DE SALIDA: Implementa el puerto SheetDataFetcherPort
    usando la API real de Google Sheets.
    """
    
    def __init__(self, client: GoogleSheetsClient):
        self.client = client
    
    async def fetch(self, sheet_id: str, range_name: str) -> RawData:
        # Llamada real a la API externa
        response = await self.client.get_values(sheet_id, range_name)
        
        # Convierte la respuesta externa a nuestro modelo del dominio
        return RawData(
            values=response.get('values', []),
            source=f"google_sheets:{sheet_id}"
        )