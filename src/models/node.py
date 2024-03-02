from dataclasses import dataclass, field
from typing import List

from src.models.event import Event


@dataclass
class Node:
    level: int = 0
    path: List[Event] = field(default_factory=list)
    bound: int = 0
    bound_without_returning: int = 0
    capacity: int = 0

    def __lt__(self, other):
        return self.bound < other.bound

    def add_event(self, event: Event):
        self.capacity += event.capacity_effect
        self.path.append(event)

    def can_add_event(self, event: Event):
        return self.capacity + event.capacity_effect >= 0
