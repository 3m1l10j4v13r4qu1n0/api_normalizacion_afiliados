from dataclasses import dataclass
from typing import List, Any

@dataclass
class ListSheetRows:
    """Entidad pura del dominio - lista de datos crudos de la hoja de un rango espesifico ."""
    values: List[List[Any]]
    if not isinstance(values, list):
            raise ValueError("Invalid data")