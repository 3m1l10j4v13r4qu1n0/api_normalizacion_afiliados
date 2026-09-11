import gspread
from google.oauth2.service_account import Credentials

from app.domain.exceptions import SincronizacionError
from app.domain.ports.sheet_correccion_port import TITULO_HOJA_PENDIENTES

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

FONDO_ROJO = {"red": 1.0, "green": 0.0, "blue": 0.0}


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
            raise SincronizacionError(f"Error al conectar con Google Sheets: {e!s}")

    def read_range(self, range_name: str) -> list[list]:
        try:
            hoja = self._resolver_hoja(range_name)
            return hoja.get_values(self._extraer_rango(range_name))
        except SincronizacionError:
            raise
        except Exception as e:
            raise SincronizacionError(f"Error al leer rango {range_name}: {e!s}")

    def guardar_pendientes(
        self,
        encabezados: list[str],
        filas: list[list[str]],
    ) -> None:
        """Vuelca las filas pendientes de corrección en la hoja homónima (HU-06)."""
        try:
            hoja = self._obtener_o_crear_hoja(
                TITULO_HOJA_PENDIENTES, filas, encabezados
            )
            hoja.update(range_name="A1", values=[encabezados] + filas)
            if filas:
                ranges = [
                    (f"A{r}:Z{r}", {"backgroundColor": FONDO_ROJO})
                    for r in range(2, len(filas) + 2)
                ]
                hoja.batch_format(ranges)
        except Exception as e:
            raise SincronizacionError(
                f"Error al actualizar la hoja de pendientes: {e!s}"
            )

    def leer_pendientes(self, range_name: str = "A1:Z") -> list[list]:
        """Lee el contenido actual de la hoja de pendientes de corrección (HU-06)."""
        try:
            spreadsheet = self._hoja.spreadsheet
            try:
                hoja = spreadsheet.worksheet(TITULO_HOJA_PENDIENTES)
            except gspread.exceptions.WorksheetNotFound:
                raise SincronizacionError(
                    "No se encontró la hoja de pendientes de corrección: "
                    "ejecutá primero una importación."
                )
            return hoja.get_values(range_name)
        except SincronizacionError:
            raise
        except Exception as e:
            raise SincronizacionError(f"Error al leer la hoja de pendientes: {e!s}")

    def exportar_tabla(
        self,
        titulo_hoja: str,
        encabezados: list[str],
        datos: list[list[str]],
    ) -> None:
        """Exporta una tabla completa a Google Sheets (HU-08)."""
        try:
            hoja = self._obtener_o_crear_hoja(titulo_hoja, datos, encabezados)
            hoja.update(range_name="A1", values=[encabezados] + datos)
        except Exception as e:
            raise SincronizacionError(f"Error al exportar tabla a Sheets: {e!s}")

    def _resolver_hoja(self, range_name: str) -> gspread.Worksheet:
        if "!" in range_name:
            nombre, _ = range_name.split("!", 1)
            try:
                return self._hoja.spreadsheet.worksheet(nombre)
            except gspread.exceptions.WorksheetNotFound:
                raise SincronizacionError(f"No se encontró la hoja '{nombre}'.")
        return self._hoja

    def _extraer_rango(self, range_name: str) -> str:
        return range_name.split("!", 1)[1] if "!" in range_name else range_name

    def _obtener_o_crear_hoja(
        self,
        titulo_hoja: str,
        filas: list,
        encabezados: list[str],
    ) -> gspread.Worksheet:
        spreadsheet = self._hoja.spreadsheet
        try:
            hoja = spreadsheet.worksheet(titulo_hoja)
            hoja.clear()
        except gspread.exceptions.WorksheetNotFound:
            hoja = spreadsheet.add_worksheet(
                title=titulo_hoja, rows=len(filas) + 1, cols=len(encabezados)
            )
        return hoja
