from dataclasses import dataclass
from typing import Any

@dataclass
class Int64:
    ...

@dataclass
class Datetime:
    time_unit: str = 'us'

    def __init__(self, time_unit: str='us'):
        self.time_unit = time_unit