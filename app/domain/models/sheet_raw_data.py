from dataclasses import dataclass
from typing import List, Any

@dataclass
class SheetRawData:
    values: List[List[Any]]