from abc import ABC, abstractmethod
from app.domain.models.list_sheet_rows import ListSheetRows

class SheetDataPort(ABC):
    """Puerto para obtener filas desde una fuente de hojas de cálculo."""

    @abstractmethod
    def fetch_rows(self, range_name: str) -> ListSheetRows:
        """Lee datos de un rango específico en Google Sheets."""
        pass

    