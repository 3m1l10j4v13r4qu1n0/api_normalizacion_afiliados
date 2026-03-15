# src/infrastructure/config/dependency_injection.py
from domain.ports.outgoing.sheet_data_fetcher_port import SheetProcessorService
from infrastructure.sheets.google_sheets_client import GoogleSheetsClient
from infrastructure.sheets.google_sheets_fetcher_adapter import GoogleSheetsFetcherAdapter
from infrastructure.sheets.key_mapper_adapter import KeyMapperAdapter
from infrastructure.sheets.file_json_storage import FileJsonStorageAdapter

def setup_processor() -> SheetProcessorService:
    """Wire up de todas las dependencias."""
    
    # Adaptadores de salida
    sheets_client = GoogleSheetsClient(credentials_path="credentials.json")
    fetcher = GoogleSheetsFetcherAdapter(sheets_client)
    mapper = KeyMapperAdapter()
    storage = FileJsonStorageAdapter()
    
    # Servicio de dominio (que expone el puerto de entrada)
    processor = SheetProcessorService(
        fetcher=fetcher,
        mapper=mapper,
        storage=storage
    )
    
    return processor