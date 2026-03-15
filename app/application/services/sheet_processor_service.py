from typing import Dict, Optional

from domain.ports.incoming.sheet_to_json_port import SheetToJsonPort
from domain.ports.outgoing.sheet_data_fetcher_port import SheetDataFetcherPort
from domain.ports.outgoing.data_mapper_port import DataMapperPort
from domain.ports.outgoing.json_storage_port import JsonStoragePort

class SheetProcessorService(SheetToJsonPort):
    """
    SERVICIO DEL DOMINIO: Implementa la lógica de negocio.
    Depende de PUERTOS (abstracciones), no de adaptadores concretos.
    """
    
    def __init__(self,
                 fetcher: SheetDataFetcherPort,      # Puerto de salida
                 mapper: DataMapperPort,              # Puerto de salida
                 storage: JsonStoragePort):           # Puerto de salida
        self.fetcher = fetcher
        self.mapper = mapper
        self.storage = storage
    
    async def process_sheet(self, 
                           sheet_id: str, 
                           range_name: str, 
                           mapping: Dict[str, str],
                           models_name: str,
                           output_path: Optional[str] = None) -> str:
        """
        Lógica de negocio pura:
        1. Obtener datos (a través del puerto)
        2. Mapear claves (a través del puerto)
        3. Guardar JSON (a través del puerto)
        """
        # Obtener datos - NO SABE CÓMO, SOLO SABE QUE USA EL PUERTO
        raw_data = await self.fetcher.fetch(sheet_id, range_name)
        if not raw_data:
            raise ValueError("No data found")
        
        # Mapear - NO SABE CÓMO SE HACE EL MAPEO
        mapped_data = await self.mapper.remap_keys(raw_data, mapping, models_name)
        
        # Guardar - NO SABE DÓNDE SE GUARDA
        json_result = await self.storage.save(mapped_data, output_path)
        
        return json_result