"""
Tests de SheetsCorreccionAdapter (HU-06 — capa de infraestructura)

Cubre:
    - guardar_pendientes delega en el cliente con encabezados y filas
    - leer_pendientes delega y devuelve los datos crudos
    - Falla del cliente → se propaga SincronizacionError aguas arriba
"""

import asyncio
from unittest.mock import MagicMock

import pytest

from app.domain.exceptions import SincronizacionError
from app.infrastructure.google.sheets_correccion_adapter import SheetsCorreccionAdapter


@pytest.fixture
def gspread_client():
    return MagicMock()


@pytest.fixture
def adapter(gspread_client):
    return SheetsCorreccionAdapter(gspread_client)


class TestSheetsCorreccionAdapter:

    def test_guardar_pendientes_delega_en_cliente(self, adapter, gspread_client):
        asyncio.run(adapter.guardar_pendientes(["nombre"], [["Ana", "dni: inválido"]]))
        gspread_client.guardar_pendientes.assert_called_once_with(
            ["nombre"], [["Ana", "dni: inválido"]]
        )

    def test_leer_pendientes_delega_y_devuelve_datos(self, adapter, gspread_client):
        gspread_client.leer_pendientes.return_value = [["a"]]
        resultado = asyncio.run(adapter.leer_pendientes("A1:Z"))
        gspread_client.leer_pendientes.assert_called_once_with("A1:Z")
        assert resultado.values == [["a"]]

    def test_propaga_error_del_cliente(self, adapter, gspread_client):
        gspread_client.guardar_pendientes.side_effect = SincronizacionError("boom")
        with pytest.raises(SincronizacionError):
            asyncio.run(adapter.guardar_pendientes(["nombre"], [["Ana"]]))
