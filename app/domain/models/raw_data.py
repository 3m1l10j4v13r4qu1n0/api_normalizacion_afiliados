from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class RawData:
    """Entidad pura del dominio - datos crudos de la hoja."""
    values: List[List[Any]]
    source: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario (método puro del dominio)."""
        return {"source": self.source, "values": self.values}