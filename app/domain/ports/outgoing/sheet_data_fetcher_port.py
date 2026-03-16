from abc import ABC, abstractmethod
from typing import Optional
from domain.models.raw_data import RawData

class SheetDataFetcherPort(ABC):
    """
    PUERTO DE SALIDA: Define cómo el dominio obtiene datos de hojas.
    El dominio depende de esta abstracción, no de implementaciones concretas.
    """
    
    @abstractmethod
    async def fetch(self, range_name: str) -> Optional[RawData]:
        """
        Obtiene datos de una hoja de cálculo.
        Retorna RawData (modelo del dominio) o None si no hay datos.
        """
        pass