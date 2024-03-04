from dataclasses import field, dataclass
from typing import List

from cool_delivery.models import Event


@dataclass
class Route:
    events: List[Event] = field(default_factory=list)
    total_cost: float = 0

    def __lt__(self, other):
        return self.events and self.total_cost < other.total_cost

    def __str__(self):
        event_info = ", ".join(f"({event.id}, {event.type}, {event.capacity})" for event in self.events)
        return f"\nRoute:\n  -> Cost: {self.total_cost}\n  -> Path: {event_info}"
