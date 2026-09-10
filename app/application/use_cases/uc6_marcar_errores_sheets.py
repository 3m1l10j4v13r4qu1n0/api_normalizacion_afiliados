from app.domain.models.error_validacion import ErrorValidacion
from app.domain.ports.sheet_marking_port import SheetMarkingPort


class MarcarErroresSheetsUseCase:
    """
    Caso de uso UC6: marcar en Google Sheets las filas con errores de validación.

    Es un paso interno del flujo de importación desde Sheets (HU-06): extrae
    los `row_number` de los errores registrados, elimina duplicados y delega la
    marcación en `SheetMarkingPort`. El fallo al marcar no debe interrumpir el
    flujo principal de importación (SH-UC4b-RN4).

    Attributes:
        _sheet_marking_port : SheetMarkingPort — puerto de marcación en Sheets.
    """

    def __init__(
        self,
        sheet_marking_port: SheetMarkingPort,
    ) -> None:
        self._sheet_marking_port = sheet_marking_port

    async def execute(self, errores: list[ErrorValidacion]) -> None:
        """
        Marca las filas con errores en la hoja.

        Parameters:
            errores : list[ErrorValidacion] — errores registrados en la importación.
        """
        if not errores:
            return

        filas_con_error = sorted({error.row_number for error in errores})
        await self._sheet_marking_port.marcar_filas_con_errores(filas_con_error)
