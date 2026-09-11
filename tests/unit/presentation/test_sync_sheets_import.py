"""
Tests de integración del endpoint POST /sync/sheets/import (HU-06)

Cubre los criterios de aceptación de la HU-06 a nivel de API:
    1. Filas con error se marcan en la hoja al cerrar la importación.
    2. El fallo al marcar NO interrumpe la importación (SH-UC4b-RN4):
       la respuesta sigue siendo 201 con el resumen original.
    3. Sin errores → no se marca nada.
"""

from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.domain.exceptions import SincronizacionError
from app.domain.models.importacion import Importacion
from app.infrastructure.dependencies.dependency_injection import (
    get_import_sheet_uc4a,
    get_importar_afiliado_uc4,
    get_marcar_errores_sheets_uc6,
)
from app.main import app


@pytest.fixture
def sync_client():
    sheet_uc = AsyncMock()
    core_uc = AsyncMock()
    marking_uc = AsyncMock()

    importacion = Importacion(id=1, cantidad_registros=3)
    importacion.registrar_error(
        campo="email",
        descripcion="email inválido",
        registro_origen="{'dni': '1'}",
        row_number=2,
    )
    importacion.registrar_error(
        campo="dni",
        descripcion="dni inválido",
        registro_origen="{dni: '2'}",
        row_number=5,
    )

    sheet_uc.execute.return_value = []
    core_uc.execute.return_value = importacion

    app.dependency_overrides[get_import_sheet_uc4a] = lambda: sheet_uc
    app.dependency_overrides[get_importar_afiliado_uc4] = lambda: core_uc
    app.dependency_overrides[get_marcar_errores_sheets_uc6] = lambda: marking_uc

    yield TestClient(app), sheet_uc, core_uc, marking_uc, importacion

    app.dependency_overrides.clear()


class TestImportarDesdeSheetsMarcandoErrores:

    def test_marca_las_filas_con_error(self, sync_client):
        client, _sheet_uc, _core_uc, marking_uc, importacion = sync_client

        response = client.post("/sync/sheets/import")

        assert response.status_code == 201
        marking_uc.execute.assert_called_once_with(importacion.errores)

    def test_devuelve_resumen_importacion(self, sync_client):
        client, _sheet_uc, _core_uc, _marking_uc, _importacion = sync_client

        response = client.post("/sync/sheets/import")

        assert response.status_code == 201
        assert response.json() == {
            "cantidad_registros_procesados": 3,
            "cantidad_registros_validos": 1,
            "cantidad_errores": 2,
            "errores": [
                {
                    "campo": "email",
                    "descripcion_error": "email inválido",
                    "row_number": 2,
                },
                {
                    "campo": "dni",
                    "descripcion_error": "dni inválido",
                    "row_number": 5,
                },
            ],
        }

    def test_error_al_marcar_no_interrumpe_la_importacion(self, sync_client):
        client, _sheet_uc, _core_uc, marking_uc, _importacion = sync_client
        marking_uc.execute.side_effect = SincronizacionError("no se pudo marcar")

        response = client.post("/sync/sheets/import")

        assert response.status_code == 201
        assert response.json()["cantidad_registros_procesados"] == 3
        marking_uc.execute.assert_called_once()

    def test_sin_errores_no_marca_nada(self, sync_client):
        client, _sheet_uc, core_uc, marking_uc, _importacion = sync_client
        core_uc.execute.return_value = Importacion(id=2, cantidad_registros=2)

        response = client.post("/sync/sheets/import")

        assert response.status_code == 201
        marking_uc.execute.assert_called_once_with([])
