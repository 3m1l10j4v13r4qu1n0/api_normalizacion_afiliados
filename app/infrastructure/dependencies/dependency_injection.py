from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.connection import get_db

from app.domain.models.mapping import mapping
from app.domain.services.data_key_mapper import DataKeyMapper
from app.domain.services.data_transformer import DataTransformer
from app.domain.ports.sheet_data_port import SheetDataPort

from app.application.use_cases.core_importar_afiliado import ImportarAfiliadoUseCase

from app.application.use_cases.uc1a_importar_lista_afiliados import ImportarDesdeAPIUseCase
from app.application.use_cases.uc1b_agregar_afiliado import AgregarAfiliadoUseCase
from app.application.use_cases.uc2_listar_afiliados import ListarAfiliadosUseCase
from app.application.use_cases.uc2_obtener_afiliado_por_id import ObtenerAfiliadoPorIdUseCase
from app.application.use_cases.uc3_actualizar_afiliado import ActualizarAfiliadoUseCase
from app.application.use_cases.uc4a_importar_afiliado import ImportSheetUseCase
from app.application.use_cases.uc4_importar_afiliado import ImportarDesdeSheetUseCase
from app.application.use_cases.uc5_dar_baja_afiliado import DarBajaAfiliadoUseCase

from app.infrastructure.core.config import settings
from app.infrastructure.google.google_sheets_client import GspreadSheetsClient
from app.infrastructure.google.google_sheets_adapter import GoogleSheetsAdapter
from app.infrastructure.database.repositories.afiliado_command_repository import AfiliadoCommandRepository
from app.infrastructure.database.repositories.afiliado_query_repository import AfiliadoQueryRepository
from app.infrastructure.database.repositories.afiliado_importacion_repository import AfiliadoImportacionRepository
from app.infrastructure.database.repositories.importacion_repository import ImportacionRepository
from app.infrastructure.database.repositories.error_repository import ErrorRepository
from app.infrastructure.database.repositories.domicilio_repository import DomicilioRepository
from app.infrastructure.database.repositories.dominio_repository import DominioRepository

# ── UC1a Dependencias ──────────────────────────────────────────────
def get_importar_desde_api_uc1a(
        session: AsyncSession = Depends(get_db),
) -> ImportarDesdeAPIUseCase:

    core_uc = ImportarAfiliadoUseCase(
        afiliado_repo   =AfiliadoImportacionRepository(session),
        importacion_repo=ImportacionRepository(session),
        error_repo      =ErrorRepository(session),
        domicilio_repo  =DomicilioRepository(session),
        dominio_repo    =DominioRepository(session),
    )

    return ImportarDesdeAPIUseCase(core_uc=core_uc)

# ── UC1b Dependencias ──────────────────────────────────────────────
def get_agregar_afiliado_uc1b(
        session: AsyncSession = Depends(get_db),
) -> AgregarAfiliadoUseCase:

    core_uc = ImportarAfiliadoUseCase(
        afiliado_repo   =AfiliadoImportacionRepository(session),
        importacion_repo=ImportacionRepository(session),
        error_repo      =ErrorRepository(session),
        domicilio_repo  =DomicilioRepository(session),
        dominio_repo    =DominioRepository(session),
    )

    return AgregarAfiliadoUseCase(core_uc=core_uc)



# ── UC2 Dependencias ──────────────────────────────────────────────
def get_listar_afiliados_uc2(
    session: AsyncSession = Depends(get_db),
) -> ListarAfiliadosUseCase:
    repo = AfiliadoQueryRepository(session)
    return ListarAfiliadosUseCase(repo)

def get_obtener_afiliado_por_id_uc2(
        session: AsyncSession = Depends(get_db),
) -> ObtenerAfiliadoPorIdUseCase:
    repo = AfiliadoQueryRepository(session)
    return ObtenerAfiliadoPorIdUseCase(repo)



# ── UC3 Dependencias ──────────────────────────────────────────────
def get_actualizar_afiliado_uc3(
    session: AsyncSession = Depends(get_db),
) -> ActualizarAfiliadoUseCase:
    repo = AfiliadoCommandRepository(session)
    return ActualizarAfiliadoUseCase(repo)



# ── UC4 Dependencias ──────────────────────────────────────────────
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

def get_importar_afiliado_uc4(
        session: AsyncSession = Depends(get_db),
) -> ImportarDesdeSheetUseCase:
    
    # 🔹 UC4a (leer sheet)
    sheet_uc = setup_processor()

    # 🔹 CORE (lógica de negocio)
    core_uc = ImportarAfiliadoUseCase(
        afiliado_repo   =AfiliadoImportacionRepository(session),
        importacion_repo=ImportacionRepository(session),
        error_repo      =ErrorRepository(session),
        domicilio_repo  =DomicilioRepository(session),
        dominio_repo    =DominioRepository(session),
    )

    # 🔹 Wrapper (UC4 completo)
    return ImportarDesdeSheetUseCase(
        sheet_uc=sheet_uc,
        core_uc=core_uc
    )


# ── UC5 Dependencias ──────────────────────────────────────────────
def get_dar_baja_afiliado_uc5(
    session: AsyncSession = Depends(get_db),
) -> DarBajaAfiliadoUseCase:
    repo = AfiliadoCommandRepository(session)
    return DarBajaAfiliadoUseCase(repo)