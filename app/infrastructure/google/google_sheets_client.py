import gspread

from app.domain.models.sheet_raw_data import SheetRawData
from google.oauth2.service_account import Credentials
from app.infrastructure.core.config import settings
from app.domain.exceptions import SincronizacionError

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class GspreadSheetsClient:
    """Implementación concreta usando gspread"""

    def __init__(self, sheet_id, credentials_path):
        self._sheet_id = sheet_id
        self._credentials_path = credentials_path
        self._hoja = self._conectar()

    def _conectar(self) -> gspread.Worksheet:
        try:
            credenciales = Credentials.from_service_account_file(
                self._credentials_path, scopes=SCOPES
            )
            cliente = gspread.authorize(credenciales)
            spreadsheet = cliente.open_by_key(self._sheet_id)
            return spreadsheet.sheet1
        except FileNotFoundError:
            raise SincronizacionError(
                f"No se encontró el archivo de credenciales: {self._credentials_path}"
            )
        except gspread.exceptions.SpreadsheetNotFound:
            raise SincronizacionError(
                f"No se encontró la hoja con ID: {self._sheet_id}"
            )
        except Exception as e:
            raise SincronizacionError(f"Error al conectar con Google Sheets: {str(e)}")

    def read_range(self, range_name: str) -> SheetRawData:
        try:
            return self._hoja.get_values(range_name)
        except Exception as e:
            raise SincronizacionError(f"Error al leer rango {range_name}: {str(e)}")

    def marcar_filas_con_errores(self, row_numbers: list[int]) -> None:
        """Aplica fondo rojo a las filas indicadas, de forma masiva (batch)."""
        try:
            ranges = [
                (
                    f"A{row}:Z{row}",
                    {"backgroundColor": {"red": 1.0, "green": 0.0, "blue": 0.0}},
                )
                for row in row_numbers
            ]
            if ranges:
                self._hoja.batch_format(ranges)
        except Exception as e:
            raise SincronizacionError(f"Error al marcar filas con errores: {str(e)}")
