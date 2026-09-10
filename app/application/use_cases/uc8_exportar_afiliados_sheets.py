from datetime import date

from app.domain.exceptions import AfiliadoNoEncontradoError
from app.domain.models.afiliado_export_row import AfiliadoExportRow
from app.domain.ports.afiliado.afiliado_query_port import AfiliadoQueryPort
from app.domain.ports.sheet_export_port import SheetExportPort

ENCABEZADOS = ["Nombre y Apellido", "Edad", "DNI", "N° Legajo", "Email"]


def calcular_edad(fecha_nacimiento: date) -> int:
    hoy = date.today()
    return hoy.year - fecha_nacimiento.year - (
        (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
    )


class ExportarAfiliadosSheetsUseCase:
    """
    UC8 — Exportar tabla de afiliados a Google Sheets.

    AF-RN18 — Solo se exportan afiliados activos.
    AF-RN19 — La edad se calcula dinámicamente y no se persiste.
    AF-RN20 — Solo se exportan datos relevantes.
    AF-RN21 — Los afiliados se ordenan alfabéticamente por nombre y apellido.
    AF-RN22 — No se exportan duplicados (cada afiliado aparece una sola vez).
    """

    def __init__(
        self,
        afiliado_query_repo: AfiliadoQueryPort,
        sheet_export_port: SheetExportPort,
    ) -> None:
        self._afiliado_query = afiliado_query_repo
        self._sheet_export = sheet_export_port

    async def execute(self, titulo_hoja: str = "Afiliados") -> int:
        afiliados = await self._afiliado_query.obtener_activos()

        if not afiliados:
            raise AfiliadoNoEncontradoError(
                "No hay afiliados activos para exportar"
            )

        filas = sorted(
            [
                AfiliadoExportRow(
                    nombre_apellido=f"{a.apellido}, {a.nombre}",
                    edad=calcular_edad(a.fecha_nacimiento),
                    dni=a.dni,
                    numero_legajo=a.numero_legajo,
                    email=a.email or "",
                )
                for a in afiliados
            ],
            key=lambda f: f.nombre_apellido,
        )

        await self._sheet_export.exportar_tabla(
            titulo_hoja=titulo_hoja,
            encabezados=ENCABEZADOS,
            filas=filas,
        )

        return len(filas)
