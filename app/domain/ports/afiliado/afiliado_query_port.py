from abc import ABC, abstractmethod
from typing import Any


class AfiliadoQueryPort(ABC):
    """
    Puerto para CONSULTAS.

    """

    @abstractmethod
    async def listar(self) -> list[Any]:
        """
        UC2 — Obtiene todos los afiliados almacenados
        RF10 — Permitir consultar afiliados
        """
        ...

    @abstractmethod
    async def obtener_por_id(self, afiliado_id: int) -> dict[str, str]:
        """
        UC2 — Obtiene un afiliado por su ID
        RF11 — Permitir consultar afiliado por identificador
        """
        ...
