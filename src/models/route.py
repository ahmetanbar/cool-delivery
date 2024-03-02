from dataclasses import field, dataclass
from typing import List

from src.models.event import Event


@dataclass
class Route:
    events: List[Event] = field(default_factory=list)
    total_cost: float = 0

    def __str__(self):
        event_info = ", ".join(f"({event.id}, {event.__class__.__name__})" for event in self.events)
        return f"Route:\n  -> Cost: {self.total_cost}\n  -> Path: {event_info}"
