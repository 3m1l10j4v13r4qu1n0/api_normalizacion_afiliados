from abc import ABC, abstractmethod
from typing import Dict, Optional

from domain.models.raw_data import RawData
from domain.models.mapped_data import MappedData

class DataMapperPort(ABC):
    
    @abstractmethod
    def add_new_key(self, 
                   data: Optional[RawData], 
                   mapping: Dict, 
                   models_name: str
                   ) -> None:
      pass

    @abstractmethod
    def remap_keys(self) -> Optional[MappedData]:
      pass