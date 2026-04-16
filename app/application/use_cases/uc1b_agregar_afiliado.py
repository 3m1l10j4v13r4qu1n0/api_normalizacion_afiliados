
from app.domain.models.input_row import InputRow
from app.application.use_cases.core_importar_afiliado import ImportarAfiliadoUseCase

"""
UC1b — Agregar un afiliado manualmente
RF1  — Importar datos desde fuente externa
RF3  — Validar datos obligatorios
RF4  — Validar formato de datos
AF-RN11 — Registros inválidos no se persisten
"""

class AgregarAfiliadoUseCase:
    """
    UC1b — Alta manual de un único afiliado.
    Reutiliza el pipeline completo del core (validación + normalización).

    Attributes:
        _core_uc : ImportarAfiliadoUseCase
    """

    def __init__(self, core_uc: ImportarAfiliadoUseCase) -> None:
        self._core_uc = core_uc

    async def execute(self, datos: dict):
        row = InputRow(row_number=1, values=datos)
        return await self._core_uc.execute([row])