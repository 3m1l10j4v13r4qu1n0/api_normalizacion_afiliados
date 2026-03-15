from abc import ABC, abstractmethod
from typing import Dict, Optional

class SheetToJsonPort(ABC):
    """
    PUERTO DE ENTRADA: Define el caso de uso principal.
    Expone la funcionalidad de mi aplicación al exterior.
    """
    
    @abstractmethod
    async def process_sheet(self, 
                           sheet_id: str, 
                           range_name: str, 
                           mapping: Dict[str, str],
                           models_name: str,
                           output_path: Optional[str] = None) -> str:
        """
        Procesa una hoja y genera JSON.
        Este es el contrato que mi app ofrece al mundo exterior.
        """
        pass