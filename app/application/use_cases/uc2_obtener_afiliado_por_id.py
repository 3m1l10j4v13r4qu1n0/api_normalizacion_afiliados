from app.domain.ports.afiliado.afiliado_query_port import AfiliadoQueryPort
from app.domain.exceptions import AfiliadoNoEncontradoError

"""
UC2  — Obtener afiliado por ID
RF11 — Permitir consultar afiliado por identificador
"""

class ObtenerAfiliadoPorIdUseCase:
    """
    UC2 — Consulta un afiliado por su identificador.

    Attributes:
        _repo : AfiliadoQueryPort
    """

    def __init__(self, repo: AfiliadoQueryPort) -> None:
        self._repo = repo

    async def execute(self, afiliado_id: int):
        """
        Parámetros:
            afiliado_id : int — ID del afiliado a consultar.

        Returns:
            AfiliadoORM — El afiliado encontrado.

        Raises:
            AfiliadoNoEncontrado — Si no existe un afiliado con ese ID.
        """
        afiliado = await self._repo.obtener_por_id(afiliado_id)

        if afiliado is None:
            raise AfiliadoNoEncontradoError(
                f"No existe afiliado con id={afiliado_id}"
            )

        return afiliado