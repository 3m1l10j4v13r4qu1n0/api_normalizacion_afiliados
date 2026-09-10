from abc import ABC, abstractmethod


class ImportacionRepositoryPort(ABC):
    """
    Puerto de salida para el repositorio de importaciones.

    Responsabilidad: ciclo de vida de la importación (crear y completar).
    Los errores de validación los gestiona ErrorRepositoryPort.
    """

    @abstractmethod
    async def crear_importacion(self, cantidad_registros: int) -> int:
        """
        Crea un registro de importación en estado 'pendiente'.

        Returns:
            int — ID de la importación creada.
        """
        ...

    @abstractmethod
    async def completar_importacion(
        self, id_importacion: int, cantidad_errores: int
    ) -> None:
        """
        Actualiza la importación con el resultado final.

        Parameters:
            id_importacion   : int — ID de la importación a cerrar.
            cantidad_errores : int — Total de filas que fallaron.
        """
        ...
