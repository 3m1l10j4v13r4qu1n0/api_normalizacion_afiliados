from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class SheetRow:
    """Entidad pura del dominio - datos crudos de la hoja."""
    row_number: int
    if not isinstance(row_number, int):
            raise ValueError("Invalid data")
    values: Dict[str, Any]
    if not isinstance(values, Dict):
            raise ValueError("Invalid data")
    
    
   