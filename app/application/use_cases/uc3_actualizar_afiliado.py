from app.domain.ports.afiliado.afiliado_command_port import AfiliadoCommandPort
from app.presentation.schemas.afiliados_schema import AfiliadoUpdate
from app.domain.exceptions import AfiliadoNoEncontradoError, EmailDuplicadoError

"""
UC3  — Actualizar afiliado
RF12 — Permitir actualizar datos de afiliados
"""

class ActualizarAfiliadoUseCase:
    """
    UC3 — Actualiza los datos de un afiliado existente.
    Solo modifica los campos que llegaron en el request.

    Attributes:
        _repo : AfiliadoCommandPort
    """

    def __init__(self, repo: AfiliadoCommandPort) -> None:
        self._repo = repo

    async def execute(self, afiliado_id: int, datos: AfiliadoUpdate):
        # Paso 1 — Si viene email, verificar que no esté en uso
        if datos.email is not None:
            en_uso = await self._repo.buscar_por_email_excluyendo_id(
                email      =datos.email,
                afiliado_id=afiliado_id,
            )
            if en_uso is not None:
                raise EmailDuplicadoError(
                    f"El email {datos.email} ya está registrado en otro afiliado"
                )

        # Paso 2 — Actualizar solo campos presentes en el request
        campos = datos.model_dump(exclude_unset=True)
        afiliado = await self._repo.update_afiliado(afiliado_id, campos)

        # Paso 3 — Verificar que el afiliado existe
        if afiliado is None:
            raise AfiliadoNoEncontradoError(
                f"No existe afiliado con id={afiliado_id}"
            )

        return afiliado