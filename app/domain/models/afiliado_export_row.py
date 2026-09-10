from dataclasses import dataclass


@dataclass
class AfiliadoExportRow:
    """Fila de datos lista para exportar a Google Sheets (HU-08)."""

    nombre_apellido: str
    edad: int
    dni: str
    numero_legajo: str
    email: str
