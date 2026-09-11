"""
Tests de GspreadSheetsClient.guardar_pendientes / leer_pendientes (HU-06)

Cubre el ciclo de corrección sobre Google Sheets:
    - Crea la hoja de pendientes si no existe (add_worksheet)
    - Reutiliza y limpia la hoja existente
    - Vuelca encabezados + filas pendientes en A1
    - Resalta todas las filas pendientes en rojo (una sola batch)
    - Sin pendientes → no resalta nada
    - leer_pendientes devuelve el contenido y falla si la hoja no existe
    - Falla al actualizar → SincronizacionError
"""

from unittest.mock import MagicMock

import gspread
import pytest

from app.domain.exceptions import SincronizacionError
from app.domain.ports.sheet_correccion_port import TITULO_HOJA_PENDIENTES
from app.infrastructure.google.google_sheets_client import GspreadSheetsClient

FONDO_ROJO = {
    "backgroundColor": {"red": 1.0, "green": 0.0, "blue": 0.0},
}


def _cliente_sin_conexion():
    """Instancia GspreadSheetsClient sin conectar a Google (mocks la hoja)."""
    client = GspreadSheetsClient.__new__(GspreadSheetsClient)
    client._sheet_id = "fake-id"
    client._credentials_path = "fake.json"
    client._hoja = MagicMock()
    client._hoja.spreadsheet = MagicMock()
    return client


def _hoja_pendiente(client):
    hoja = MagicMock()
    client._hoja.spreadsheet.worksheet.return_value = hoja
    return hoja


class TestGuardarPendientesCliente:

    def test_crea_la_hoja_si_no_existe(self):
        client = _cliente_sin_conexion()
        client._hoja.spreadsheet.worksheet.side_effect = [
            gspread.exceptions.WorksheetNotFound(MagicMock())
        ]
        hoja = MagicMock()
        client._hoja.spreadsheet.add_worksheet.return_value = hoja

        client.guardar_pendientes(["nombre"], [["Ana", "dni: inválido"]])

        client._hoja.spreadsheet.add_worksheet.assert_called_once_with(
            title=TITULO_HOJA_PENDIENTES, rows=2, cols=1
        )
        hoja.update.assert_called_once()
        hoja.batch_format.assert_called_once()

    def test_reutiliza_y_limpia_la_hoja_existente(self):
        client = _cliente_sin_conexion()
        hoja = _hoja_pendiente(client)

        client.guardar_pendientes(["nombre"], [])

        client._hoja.spreadsheet.worksheet.assert_called_once_with(
            TITULO_HOJA_PENDIENTES
        )
        hoja.clear.assert_called_once()

    def test_vuelca_encabezados_y_filas_en_a1(self):
        client = _cliente_sin_conexion()
        hoja = _hoja_pendiente(client)

        client.guardar_pendientes(
            ["nombre", "dni", "motivo del error"],
            [["Ana", "1", "dni: inválido"]],
        )

        hoja.update.assert_called_once_with(
            range_name="A1",
            values=[
                ["nombre", "dni", "motivo del error"],
                ["Ana", "1", "dni: inválido"],
            ],
        )

    def test_resalta_todas_las_pendientes_en_rojo(self):
        client = _cliente_sin_conexion()
        hoja = _hoja_pendiente(client)

        client.guardar_pendientes(["nombre"], [["Ana"], ["Luis"]])

        ranges = hoja.batch_format.call_args.args[0]
        assert ranges == [
            ("A2:Z2", FONDO_ROJO),
            ("A3:Z3", FONDO_ROJO),
        ]

    def test_sin_pendientes_no_resalta_nada(self):
        client = _cliente_sin_conexion()
        hoja = _hoja_pendiente(client)

        client.guardar_pendientes(["nombre"], [])

        hoja.batch_format.assert_not_called()

    def test_falla_al_actualizar_lanza_sincronizacion_error(self):
        client = _cliente_sin_conexion()
        hoja = _hoja_pendiente(client)
        hoja.update.side_effect = ValueError("boom")

        with pytest.raises(SincronizacionError):
            client.guardar_pendientes(["nombre"], [["Ana"]])


class TestLeerPendientesCliente:

    def test_devuelve_contenido_de_la_hoja_pendiente(self):
        client = _cliente_sin_conexion()
        hoja = _hoja_pendiente(client)
        hoja.get_values.return_value = [["nombre"], ["Ana"]]

        resultado = client.leer_pendientes("A1:Z")

        client._hoja.spreadsheet.worksheet.assert_called_once_with(
            TITULO_HOJA_PENDIENTES
        )
        hoja.get_values.assert_called_once_with("A1:Z")
        assert resultado == [["nombre"], ["Ana"]]

    def test_sin_hoja_pendiente_lanza_error(self):
        client = _cliente_sin_conexion()
        client._hoja.spreadsheet.worksheet.side_effect = [
            gspread.exceptions.WorksheetNotFound(MagicMock())
        ]

        with pytest.raises(SincronizacionError):
            client.leer_pendientes()


class TestResolucionDeRango:

    def test_read_range_resuelve_hoja_por_nombre(self):
        client = _cliente_sin_conexion()
        hoja = _hoja_pendiente(client)
        hoja.get_values.return_value = [["a"]]

        resultado = client.read_range(f"{TITULO_HOJA_PENDIENTES}!A1:Z")

        client._hoja.spreadsheet.worksheet.assert_called_once_with(
            TITULO_HOJA_PENDIENTES
        )
        hoja.get_values.assert_called_once_with("A1:Z")
        assert resultado == [["a"]]

    def test_read_range_por_default_usa_sheet1(self):
        client = _cliente_sin_conexion()

        client.read_range("A1:Z")

        client._hoja.get_values.assert_called_once_with("A1:Z")
