from dataclasses import field, dataclass
from typing import List

from src.models.event import Event


@dataclass
class Route:
    events: List[Event] = field(default_factory=list)
    total_distance: float = 0
