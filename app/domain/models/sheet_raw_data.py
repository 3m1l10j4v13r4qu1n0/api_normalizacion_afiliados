from dataclasses import dataclass
from typing import Any


@dataclass
class SheetRawData:
    values: list[list[Any]]
