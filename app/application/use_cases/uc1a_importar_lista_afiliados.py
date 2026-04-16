from typing import List, Dict
from app.domain.models.input_row import InputRow

"""
SH-UC4a-RN1 — Los encabezados deben mapearse a variables internas del sistema.
SH-UC4a-RN2 — Cada fila debe mantener su número original (row_number).
SH-UC4a-RN3 — No se deben procesar filas vacías.

"""

class ImportarDesdeAPIUseCase:

    def __init__(self, core_uc):
        self.core_uc = core_uc

    async def execute(self, data: List[Dict]):

        rows = [
            InputRow(
                row_number=i + 1,
                values=item
            )
            for i, item in enumerate(data)
        ]

        return await self.core_uc.execute(rows)