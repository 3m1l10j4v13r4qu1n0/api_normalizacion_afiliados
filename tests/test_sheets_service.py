from app.infrastructure.sheets.sheets_interface import ISheetsClient
from app.application.services.sheets_service import importar_desde_sheets

class MockSheetsClient(ISheetsClient):
    """Implementación falsa para tests — no necesita credenciales"""

    def get_all_records(self) -> list[dict]:
        return [
            {"apellido": "Pérez", "nombre": "Juan", "dni": "12345678", },
            {"apellido": "",      "nombre": "Ana",  "dni": "abc",      },
        ]

    def write_range(self, range_name, values): pass
    def clear_range(self, range_name):         pass
    def read_range(self, range_name):          return []
    def append_rows(self, range_name, values): pass


# El test usa el mock, no toca Google Sheets
async def test_importar_desde_sheets(db):
    resultado = await importar_desde_sheets(db, cliente=MockSheetsClient())
    assert resultado.cantidad_registros == 2
    assert resultado.cantidad_errores   == 1  # el registro con dni "abc"
