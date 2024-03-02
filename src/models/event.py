from dataclasses import dataclass


@dataclass
class Event:
    id: int
    x: int
    y: int
    capacity: int = 0

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Event) and self.id == other.id

    @property
    def capacity_effect_to_vehicle(self):
        return self.capacity
