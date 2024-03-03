from dataclasses import dataclass, field
from typing import List

from cool_delivery.models import Event


@dataclass
class Node:
    level: int = 0
    path: List[Event] = field(default_factory=list)
    bound: int = 0
    bound_without_returning: int = 0
    capacity: int = 0

    def __lt__(self, other):
        return self.bound < other.bound

    def add_event(self, event: Event) -> bool:
        """Adds an event to the path and updates the capacity. Returns True if the event was added, False otherwise.
        """
        is_added = False
        if self.can_add_event(event):
            self.path.append(event)
            self.capacity += event.capacity_effect_to_vehicle
            is_added = True
        return is_added

    def can_add_event(self, event: Event):
        return self.capacity + event.capacity_effect_to_vehicle >= 0
