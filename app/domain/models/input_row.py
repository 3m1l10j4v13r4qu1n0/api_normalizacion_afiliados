from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class InputRow:
    """Entidad pura del dominio - datos crudos de la hoja."""
    row_number: int
    values: Dict[str, Any]
    
   