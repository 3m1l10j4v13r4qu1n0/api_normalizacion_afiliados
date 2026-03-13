from abc import ABC, abstractmethod
from typing import Any


class ISheetsClient(ABC):
    """Interfaz abstracta para interactuar con Google Sheets"""

    @abstractmethod
    def read_range(self, range_name: str) -> list[list[Any]]:
        """Lee datos de un rango específico"""
        pass

    @abstractmethod
    def write_range(self, range_name: str, values: list[list[Any]]) -> None:
        """Escribe datos en un rango específico"""
        pass

    @abstractmethod
    def append_rows(self, range_name: str, values: list[list[Any]]) -> None:
        """Agrega filas al final de un rango"""
        pass

    @abstractmethod
    def clear_range(self, range_name: str) -> None:
        """Limpia un rango específico"""
        pass

    @abstractmethod
    def get_all_records(self) -> list[dict]:
        """Retorna todos los registros como lista de dicts"""
        pass