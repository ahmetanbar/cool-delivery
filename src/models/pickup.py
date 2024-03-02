from dataclasses import dataclass

from src.models.event import Event


@dataclass
class Pickup(Event):
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Event) and self.id == other.id

    @property
    def capacity_effect_to_vehicle(self):
        return -self.capacity
