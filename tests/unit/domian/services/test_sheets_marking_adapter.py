"""
Tests de SheetsMarkingAdapter (HU-06 — capa de infraestructura)

Cubre:
    - Con filas → delega la marcación en el cliente de Sheets
    - Lista vacía → no toca el cliente (no altera filas válidas)
    - Falla del cliente → se propaga SincronizacionError aguas arriba
"""

import asyncio
from unittest.mock import MagicMock

import pytest

from app.domain.exceptions import SincronizacionError
from app.infrastructure.google.sheets_marking_adapter import SheetsMarkingAdapter


@pytest.fixture
def gspread_client():
    return MagicMock()


@pytest.fixture
def adapter(gspread_client):
    return SheetsMarkingAdapter(gspread_client)


class TestSheetsMarkingAdapter:

    def test_delega_marcacion_en_cliente(self, adapter, gspread_client):
        asyncio.run(adapter.marcar_filas_con_errores([2, 5, 7]))
        gspread_client.marcar_filas_con_errores.assert_called_once_with([2, 5, 7])

    def test_lista_vacia_no_toca_cliente(self, adapter, gspread_client):
        asyncio.run(adapter.marcar_filas_con_errores([]))
        gspread_client.marcar_filas_con_errores.assert_not_called()

    def test_propaga_error_del_cliente(self, adapter, gspread_client):
        gspread_client.marcar_filas_con_errores.side_effect = SincronizacionError(
            "error al marcar"
        )
        with pytest.raises(SincronizacionError):
            asyncio.run(adapter.marcar_filas_con_errores([2]))
