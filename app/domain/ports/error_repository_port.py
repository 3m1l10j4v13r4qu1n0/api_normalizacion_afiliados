from abc import ABC, abstractmethod


class ErrorRepositoryPort(ABC):
    """
    Puerto de salida para el repositorio de errores de validación.
    """

    @abstractmethod
    async def registrar_error(
        self,
        id_importacion: int,
        registro_origen: str,
        campo: str,
        descripcion_error: str,
        row_number: int,
    ) -> None:
        """
        Persiste un error de validación asociado a una importación.

        Parameters:
            id_importacion    : int — ID de la importación.
            registro_origen   : str — Fila original que falló (str del dict).
            campo             : str — Campo que tiene el error.
            descripcion_error : str — Descripción del error.
            row_number        : int — Numero de fila original que falló
        """
        ...
