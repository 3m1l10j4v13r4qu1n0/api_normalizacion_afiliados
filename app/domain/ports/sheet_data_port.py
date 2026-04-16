from abc import ABC, abstractmethod
from app.domain.models.sheet_raw_data import SheetRawData

class SheetDataPort(ABC):
    """Puerto para obtener filas desde una fuente de hojas de cálculo."""

    @abstractmethod
    def fetch_rows(self, range_name: str) -> SheetRawData:
        """Lee datos de un rango específico en Google Sheets."""
        ...

    