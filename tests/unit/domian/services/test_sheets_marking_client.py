"""
Tests de GspreadSheetsClient.marcar_filas_con_errores (HU-06)

Cubre los criterios técnicos de la marcación sobre la hoja:
    - Actualización masiva: una sola llamada batch para todas las filas (SH-UC4b-RN2)
    - Fondo rojo en el rango A{r}:Z{r}
    - Lista vacía → no toca la hoja (filas válidas sin cambios, SH-UC4b-RN3)
    - Falla al actualizar → SincronizacionError
"""

from unittest.mock import MagicMock

import pytest

from app.domain.exceptions import SincronizacionError
from app.infrastructure.google.google_sheets_client import GspreadSheetsClient

FONDO_ROJO = {"backgroundColor": {"red": 1.0, "green": 0.0, "blue": 0.0}}


def _cliente_sin_conexion(sheet_id="fake-id", credentials_path="fake.json"):
    """Instancia GspreadSheetsClient sin conectar a Google (mocks la hoja)."""
    client = GspreadSheetsClient.__new__(GspreadSheetsClient)
    client._sheet_id = sheet_id
    client._credentials_path = credentials_path
    client._hoja = MagicMock()
    return client


class TestMarcarFilasConErroresCliente:

    def test_una_sola_actualizacion_masiva(self):
        client = _cliente_sin_conexion()
        client.marcar_filas_con_errores([2, 5, 7])

        client._hoja.batch_format.assert_called_once()

    def test_ranges_con_fondo_rojo(self):
        client = _cliente_sin_conexion()
        client.marcar_filas_con_errores([2, 5, 7])

        ranges = client._hoja.batch_format.call_args.args[0]
        assert ranges == [
            ("A2:Z2", FONDO_ROJO),
            ("A5:Z5", FONDO_ROJO),
            ("A7:Z7", FONDO_ROJO),
        ]

    def test_lista_vacia_no_actualiza_la_hoja(self):
        client = _cliente_sin_conexion()
        client.marcar_filas_con_errores([])

        client._hoja.batch_format.assert_not_called()

    def test_falla_la_actualizacion_lanza_sincronizacion_error(self):
        client = _cliente_sin_conexion()
        client._hoja.batch_format.side_effect = ValueError("boom")

        with pytest.raises(SincronizacionError):
            client.marcar_filas_con_errores([2])
