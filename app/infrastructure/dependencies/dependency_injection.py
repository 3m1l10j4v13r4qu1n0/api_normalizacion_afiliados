from infrastructure.core.config import settings
from app.application.services.import_sheet_use_case import ImportSheetUseCase
from infrastructure.google.google_sheets_client import GspreadSheetsClient
from infrastructure.google.google_sheets_adapter import GoogleSheetsAdapter
from app.domain.ports.sheet_data_port import SheetDataPort

def build_sheet_port() -> SheetDataPort:
    # Adaptadores de salida
    sheets_client = GspreadSheetsClient(
        sheet_id=settings.GOOGLE_SHEETS_ID,
        credentials_path=settings.GOOGLE_CREDENTIALS_PATH
    )
    return GoogleSheetsAdapter(sheets_client)

def setup_processor() -> ImportSheetUseCase:
    """Wire up de todas las dependencias."""
    
    # Servicio de dominio (que expone el puerto de entrada)
    sheet_port = build_sheet_port()

    return ImportSheetUseCase(
        sheet_port=sheet_port
    )

