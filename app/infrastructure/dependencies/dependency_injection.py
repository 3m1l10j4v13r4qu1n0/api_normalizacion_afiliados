from app.infrastructure.core.config import settings
from app.application.services.sheet_processor_service import SheetProcessorService
from infrastructure.google.google_sheets_client import GspreadSheetsClient
from infrastructure.google.google_sheets_fetcher_adapter import GoogleSheetsFetcherAdapter
from infrastructure.google.key_mapper_adapter import KeyMapperAdapter
from infrastructure.google.file_json_storage import FileJsonStorageAdapter

def setup_processor() -> SheetProcessorService:
    """Wire up de todas las dependencias."""
    
    # Adaptadores de salida
    sheets_client = GspreadSheetsClient(sheet_id=settings.GOOGLE_SHEETS_ID,
                                        credentials_path=settings.GOOGLE_CREDENTIALS_PATH
                                        )
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