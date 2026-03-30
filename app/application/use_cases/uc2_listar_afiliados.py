from typing import List
from app.domain.ports.afiliado.afiliado_query_port import AfiliadoQueryPort

"""
UC2  — Listar afiliados
RF10 — Permitir consultar afiliados
"""

class ListarAfiliadosUseCase:
    """
    UC2 — Obtiene todos los afiliados almacenados.

    Attributes:
        _repo : AfiliadoQueryPort
    """

    def __init__(self, repo: AfiliadoQueryPort) -> None:
        self._repo = repo

    async def execute(self) -> List:
        return await self._repo.listar()