from typing import Dict

from domain.ports.outgoing.data_mapper_port import DataMapperPort
from domain.models.raw_data import RawData
from domain.models.mapped_data import MappedData

class KeyMapperAdapter(DataMapperPort):
    """
    ADAPTADOR DE SALIDA: Implementa el mapeo de claves.
    """
    
    async def remap_keys(self, 
                        data: RawData, 
                        mapping: Dict[str, str], 
                        models_name: str) -> MappedData:
        # Lógica de mapeo
        mapped_values = {}
        # ... lógica de transformación ...
        
        return MappedData(
            values=mapped_values,
            model_name=models_name
        )