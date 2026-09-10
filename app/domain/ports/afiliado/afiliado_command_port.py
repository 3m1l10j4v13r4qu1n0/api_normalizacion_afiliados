from abc import ABC, abstractmethod
from typing import Any


class AfiliadoCommandPort(ABC):
    @abstractmethod
    async def update_afiliado(self, afiliado: dict[str, Any]) -> dict[str, str]:
        """
        UC3 — Actualiza los datos de un afiliado existente
        RF12 — Permitir actualizar datos de afiliados
        """
        ...

    @abstractmethod
    async def buscar_por_email_excluyendo_id(
        self, email: str, afiliado_id: int
    ) -> dict[str, str]:
        """
        Verificar que el email no esté en uso por otro afiliado

        """
        ...

    @abstractmethod
    async def dar_baja(self, afiliado_id: int):
        """
        UC5  — Baja lógica del afiliado
        RF13 — Permitir dar de baja afiliados
        RN16 — Baja lógica marcando estado como inactivo
        """
        ...
