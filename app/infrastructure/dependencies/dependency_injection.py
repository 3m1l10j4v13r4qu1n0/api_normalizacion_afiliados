from app.domain.models.mapping import mapping
from app.domain.services.data_key_mapper import DataKeyMapper
from app.domain.services.data_transformer import DataTransformer
from app.domain.ports.sheet_data_port import SheetDataPort

from app.application.use_cases.importar_afiliado_uc4a import ImportSheetUseCase
from app.application.use_cases.importar_afiliado_uc4 import ImportarDesdeSheetUseCase
from app.application.use_cases.importar_afiliado_core import ImportarAfiliadoUseCase

from app.infrastructure.core.config import settings
from app.infrastructure.google.google_sheets_client import GspreadSheetsClient
from app.infrastructure.google.google_sheets_adapter import GoogleSheetsAdapter
from app.infrastructure.database.repositories.afiliado_repository import AfiliadoRepository 
from app.infrastructure.database.repositories.importacion_repository import ImportacionRepository
from app.infrastructure.database.repositories.error_repository import ErrorRepository
from app.infrastructure.database.repositories.domicilio_repository import DomicilioRepository
from app.infrastructure.database.repositories.dominio_repository import DominioRepository


def build_sheet_port() -> SheetDataPort:
    sheets_client = GspreadSheetsClient(
        sheet_id=settings.GOOGLE_SHEETS_ID,
        credentials_path=settings.GOOGLE_CREDENTIALS_PATH
    )
    return GoogleSheetsAdapter(sheets_client)


def build_transformer() -> DataTransformer:
    mapper = DataKeyMapper(mapping)
    return DataTransformer(mapper)


def setup_processor() -> ImportSheetUseCase:
    """Wire up de todas las dependencias."""
    return ImportSheetUseCase(
        sheet_port=build_sheet_port(),
        transformer=build_transformer(),
    )

def get_importar_afiliado_uc4() -> ImportarDesdeSheetUseCase:
    
    # 🔹 UC4a (leer sheet)
    sheet_uc = setup_processor()

    # 🔹 CORE (lógica de negocio)
    core_uc = ImportarAfiliadoUseCase(
        afiliado_repo=AfiliadoRepository(),
        importacion_repo=ImportacionRepository(),
        error_repo=ErrorRepository(),
        domicilio_repo=DomicilioRepository(),
        dominio_repo=DominioRepository(),
    )

    # 🔹 Wrapper (UC4 completo)
    return ImportarDesdeSheetUseCase(
        sheet_uc=sheet_uc,
        core_uc=core_uc
    )