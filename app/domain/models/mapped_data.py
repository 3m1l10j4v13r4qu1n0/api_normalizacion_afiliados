from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class MappedData:
    """Entidad pura del dominio - datos adaptados."""
    values: Any
    source: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario (método puro del dominio)."""
        return {"source": self.source, "values": self.values}
