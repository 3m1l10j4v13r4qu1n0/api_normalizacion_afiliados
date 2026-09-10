from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ErrorValidacion:
    registro_origen: str  # fila original que falló
    campo: str  # qué campo tiene el error
    descripcion_error: str  # por qué falló
    id_importacion: int  # a qué importación pertenece
    row_number: int  # numero de fila original que falló

    fecha_error: datetime | None = None
    id: int | None = field(default=None)
