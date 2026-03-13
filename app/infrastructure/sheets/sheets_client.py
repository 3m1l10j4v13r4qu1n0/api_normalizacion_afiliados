import gspread
from google.oauth2.service_account import Credentials
from typing import Any

from app.infrastructure.sheets.sheets_interface import ISheetsClient
from app.infrastructure.core.config import settings
from app.domain.exceptions import SincronizacionError

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class GspreadSheetsClient(ISheetsClient):
    """Implementación concreta usando gspread"""

    def __init__(self):
        self._hoja = self._conectar()

    def _conectar(self) -> gspread.Worksheet:
        try:
            credenciales = Credentials.from_service_account_file(
                settings.GOOGLE_CREDENTIALS_PATH,
                scopes=SCOPES
            )
            cliente      = gspread.authorize(credenciales)
            spreadsheet  = cliente.open_by_key(settings.GOOGLE_SHEETS_ID)
            return spreadsheet.sheet1
        except FileNotFoundError:
            raise SincronizacionError(
                f"No se encontró el archivo de credenciales: {settings.GOOGLE_CREDENTIALS_PATH}"
            )
        except gspread.exceptions.SpreadsheetNotFound:
            raise SincronizacionError(
                f"No se encontró la hoja con ID: {settings.GOOGLE_SHEETS_ID}"
            )
        except Exception as e:
            raise SincronizacionError(f"Error al conectar con Google Sheets: {str(e)}")

    def get_all_records(self) -> list[dict]:
        try:
            return self._hoja.get_all_records()
        except Exception as e:
            raise SincronizacionError(f"Error al leer registros: {str(e)}")

    def read_range(self, range_name: str) -> list[list[Any]]:
        try:
            return self._hoja.get(range_name)
        except Exception as e:
            raise SincronizacionError(f"Error al leer rango {range_name}: {str(e)}")

    def write_range(self, range_name: str, values: list[list[Any]]) -> None:
        try:
            self._hoja.update(values, range_name)
        except Exception as e:
            raise SincronizacionError(f"Error al escribir en rango {range_name}: {str(e)}")

    def append_rows(self, range_name: str, values: list[list[Any]]) -> None:
        try:
            self._hoja.append_rows(values)
        except Exception as e:
            raise SincronizacionError(f"Error al agregar filas: {str(e)}")

    def clear_range(self, range_name: str) -> None:
        try:
            self._hoja.clear()
        except Exception as e:
            raise SincronizacionError(f"Error al limpiar rango {range_name}: {str(e)}")