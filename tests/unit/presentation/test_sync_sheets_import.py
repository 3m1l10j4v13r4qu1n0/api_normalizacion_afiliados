"""
Tests de integración de POST /sync/sheets/import y /sync/sheets/reimport (HU-06)

Cubre los criterios de aceptación del ciclo de corrección a nivel de API:
    1. Al importar, se genera la hoja de pendientes con las filas con error.
    2. El fallo al actualizar pendientes NO interrumpe la importación (RN4):
       la respuesta sigue siendo 201 con el resumen original.
    3. Sin errores → las pendientes se guardan vacías (solo encabezados).
    4. /reimport lee la hoja de pendientes como origen y devuelve su resumen.
"""

from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.application.use_cases.uc4a_importar_afiliado import SheetLectura
from app.domain.exceptions import SincronizacionError
from app.domain.models.importacion import Importacion
from app.infrastructure.dependencies.dependency_injection import (
    get_actualizar_pendientes_uc6,
    get_import_sheet_uc4a,
    get_importar_afiliado_uc4,
)
from app.main import app
from app.presentation.routers.sync import RANGO_PENDIENTES


@pytest.fixture
def sync_client():
    sheet_uc = AsyncMock()
    core_uc = AsyncMock()
    correccion_uc = AsyncMock()

    importacion = Importacion(id=1, cantidad_registros=2)
    importacion.registrar_error(
        campo="dni",
        descripcion="dni inválido",
        registro_origen="{'dni': '1'}",
        row_number=2,
    )

    sheet_uc.execute.return_value = SheetLectura(
        input_rows=[],
        encabezados=["nombre", "dni"],
        valores_crudos=[["Ana", "1"]],
    )
    core_uc.execute.return_value = importacion

    app.dependency_overrides[get_import_sheet_uc4a] = lambda: sheet_uc
    app.dependency_overrides[get_importar_afiliado_uc4] = lambda: core_uc
    app.dependency_overrides[get_actualizar_pendientes_uc6] = lambda: correccion_uc

    yield TestClient(app), sheet_uc, core_uc, correccion_uc, importacion

    app.dependency_overrides.clear()


class TestImportarDesdeSheetsConPendientes:

    def test_genera_pendientes_con_filas_y_errores(self, sync_client):
        client, _sheet_uc, _core_uc, correccion_uc, importacion = sync_client

        response = client.post("/sync/sheets/import")

        assert response.status_code == 201
        correccion_uc.execute.assert_called_once_with(
            ["nombre", "dni"],
            [["Ana", "1"]],
            importacion.errores,
        )

    def test_devuelve_resumen_importacion(self, sync_client):
        client, _sheet_uc, _core_uc, _correccion_uc, _importacion = sync_client

        response = client.post("/sync/sheets/import")

        assert response.status_code == 201
        assert response.json()["cantidad_registros_procesados"] == 2
        assert response.json()["cantidad_errores"] == 1

    def test_error_al_actualizar_pendientes_no_interrumpe(self, sync_client):
        client, _sheet_uc, _core_uc, correccion_uc, _importacion = sync_client
        correccion_uc.execute.side_effect = SincronizacionError("no se pudo guardar")

        response = client.post("/sync/sheets/import")

        assert response.status_code == 201
        assert response.json()["cantidad_registros_procesados"] == 2
        correccion_uc.execute.assert_called_once()

    def test_sin_errores_guarda_pendientes_vacias(self, sync_client):
        client, _sheet_uc, core_uc, correccion_uc, _importacion = sync_client
        core_uc.execute.return_value = Importacion(id=2, cantidad_registros=1)

        response = client.post("/sync/sheets/import")

        assert response.status_code == 201
        correccion_uc.execute.assert_called_once_with(
            ["nombre", "dni"],
            [["Ana", "1"]],
            [],
        )


class TestReimportarPendientes:

    def test_lee_la_hoja_de_pendientes_como_origen(self, sync_client):
        client, sheet_uc, _core_uc, correccion_uc, importacion = sync_client

        response = client.post("/sync/sheets/reimport")

        assert response.status_code == 201
        sheet_uc.execute.assert_called_once_with(range_name=RANGO_PENDIENTES)
        correccion_uc.execute.assert_called_once_with(
            ["nombre", "dni"],
            [["Ana", "1"]],
            importacion.errores,
        )
