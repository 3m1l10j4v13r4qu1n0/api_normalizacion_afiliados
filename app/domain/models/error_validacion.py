from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ErrorValidacion:
    registro_origen  : str           # fila original que falló
    campo            : str           # qué campo tiene el error
    descripcion_error: str           # por qué falló
    id_importacion   : int           # a qué importación pertenece

    fecha_error      : Optional[datetime] = None
    id               : Optional[int] = field(default=None)