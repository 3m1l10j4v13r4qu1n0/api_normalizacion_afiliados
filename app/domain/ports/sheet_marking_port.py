from abc import ABC, abstractmethod


class SheetMarkingPort(ABC):
    """Puerto para marcar filas con errores en Google Sheets."""

    @abstractmethod
    async def marcar_filas_con_errores(
        self,
        row_numbers: list[int],
    ) -> None:
        """
        Marca filas con errores aplicando formato visual (fondo rojo).
        Operación batch masiva que no debe fallar la importación.

        Parameters:
            row_numbers: lista de números de fila a marcar (sin duplicados).
        """
        ...
