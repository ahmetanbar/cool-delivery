from dataclasses import dataclass

from src.models.event import Event


@dataclass
class Delivery(Event):
    def __hash__(self):
        return hash((type(self), self.id))

    def __eq__(self, other):
        if isinstance(other, Delivery):
            return (type(self), self.id) == (type(other), other.id)
        return False

    @property
    def capacity_effect(self):
        return self.capacity
