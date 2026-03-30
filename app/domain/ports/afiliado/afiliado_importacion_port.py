from abc import ABC, abstractmethod
from typing import Set

class AfiliadoImportacionPort(ABC):
    """
    Puerto para Importacion.
    """

    @abstractmethod
    async def get_all_dnis(self) -> Set[str]:
        """
        Retorna el conjunto de DNIs ya registrados en el sistema.
        Usado para validar duplicados (RN1, RN2, RF5).

        Returns:
            Set[str] — DNIs existentes en la base de datos.
        """
        ...

    @abstractmethod
    async def save_importacion(self, datos: dict, id_importacion: int) -> None:
        """
        Persiste un afiliado validado y normalizado.

        Parameters:
            datos          : dict — Salida de normalizar_afiliado().
            id_importacion : int  — ID de la importación a la que pertenece.
        """
        ...