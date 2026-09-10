from app.domain.exceptions import AfiliadoNoEncontradoError
from app.domain.ports.afiliado.afiliado_command_port import AfiliadoCommandPort

"""
UC5  — Dar de baja afiliado
RF13 — Permitir dar de baja afiliados
AF-RN16 — La eliminación debe realizarse mediante baja lógica, marcando estado 
como inactivo
"""


class DarBajaAfiliadoUseCase:
    """
    UC5 — Baja lógica de un afiliado.
    AF-RN16 — Marca id_estado_afiliado = 2 (Inactivo — seed)
    Attributes:
        _repo : AfiliadoCommandPort
    """

    def __init__(self, repo: AfiliadoCommandPort) -> None:
        self._repo = repo

    async def execute(self, afiliado_id: int):
        afiliado = await self._repo.dar_baja(afiliado_id)

        if afiliado is None:
            raise AfiliadoNoEncontradoError(f"No existe afiliado con id={afiliado_id}")

        return afiliado
