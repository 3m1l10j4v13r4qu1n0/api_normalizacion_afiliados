from abc import ABC, abstractmethod
from typing import List
from app.domain.models.input_row import InputRow

class SheetDataPort(ABC):
    """Puerto para obtener filas desde una fuente de hojas de cálculo."""

    @abstractmethod
    def fetch_rows(self, range_name: str) -> List[InputRow]:
        """Lee datos de un rango específico en Google Sheets."""
        ...

    