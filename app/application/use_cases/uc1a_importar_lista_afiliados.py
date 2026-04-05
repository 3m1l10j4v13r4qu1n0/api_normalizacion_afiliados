from typing import List, Dict
from app.domain.models.input_row import InputRow

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