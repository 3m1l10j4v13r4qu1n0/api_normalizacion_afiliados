from typing import List
from app.domain.models.input_row import InputRow

from app.application.use_cases.uc4a_importar_afiliado import ImportSheetUseCase
from app.application.use_cases.core_importar_afiliado import ImportarAfiliadoUseCase


class ImportarDesdeSheetUseCase:

    def __init__(
            self, 
            sheet_uc: ImportSheetUseCase,
            core_uc: ImportarAfiliadoUseCase
            ) -> List[InputRow]:
        self._sheet_uc = sheet_uc
        self._core_uc = core_uc

    async def execute(self, range_name: str):

        # 🔹 1. Leer y transformar (UC4a)
        sheet_rows = await self._sheet_uc.execute(range_name)

        # 🔹 2. Ejecutar lógica de negocio (CORE)
        return await self._core_uc.execute(sheet_rows)