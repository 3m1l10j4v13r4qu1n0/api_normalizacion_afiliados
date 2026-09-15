from app.domain.models.error_validacion import ErrorValidacion
from app.domain.ports.sheet_correccion_port import SheetCorreccionPort


class ActualizarHojaPendientesUseCase:
    """
    Caso de uso UC6: generar la hoja de pendientes de corrección (HU-06).

    Tras importar desde Google Sheets, las filas que no pudieron importarse se
    vuelcan en la hoja "Pendientes de corrección" (misma planilla) con sus
    columnas originales más una columna "motivo del error", resaltadas en rojo,
    para que el usuario las edite/complete y las re-importe en una próxima
    importación. Si no hay errores, la hoja queda únicamente con los encabezados.

    Attributes:
        _sheet_correccion_port : SheetCorreccionPort — puerto de gestión de pendientes.
    """

    COLUMNA_MOTIVO = "motivo del error"

    def __init__(self, sheet_correccion_port: SheetCorreccionPort) -> None:
        self._sheet_correccion_port = sheet_correccion_port

    async def execute(
        self,
        encabezados: list[str],
        valores_crudos: list[list[str]],
        errores: list[ErrorValidacion],
    ) -> None:
        filas_pendientes = self._filas_pendientes(valores_crudos, errores)
        encabezados_pendientes = list(encabezados) + [self.COLUMNA_MOTIVO]
        await self._sheet_correccion_port.guardar_pendientes(
            encabezados_pendientes,
            filas_pendientes,
        )

    def _filas_pendientes(
        self,
        valores_crudos: list[list[str]],
        errores: list[ErrorValidacion],
    ) -> list[list[str]]:
        """Agrupa los errores por fila y arma las filas pendientes con su motivo."""
        errores_por_fila: dict[int, list[ErrorValidacion]] = {}
        for error in errores:
            errores_por_fila.setdefault(error.row_number, []).append(error)

        pendientes: list[list[str]] = []
        for row_number in sorted(errores_por_fila):
            motivo = "; ".join(
                f"{error.campo}: {error.descripcion_error}"
                for error in errores_por_fila[row_number]
            )
            fila_cruda = (
                valores_crudos[row_number - 2]
                if row_number - 2 < len(valores_crudos)
                else []
            )
            pendientes.append(list(fila_cruda) + [motivo])
        return pendientes
