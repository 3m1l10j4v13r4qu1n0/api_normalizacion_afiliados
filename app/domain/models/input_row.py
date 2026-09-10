from dataclasses import dataclass
from typing import Any


@dataclass
class InputRow:
    """Entidad pura del dominio - datos crudos de la hoja."""

    row_number: int
    values: dict[str, Any]
