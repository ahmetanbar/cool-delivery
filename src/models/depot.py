from dataclasses import dataclass

from src.models.event import Event


@dataclass
class Depot(Event):
    is_return: bool = False

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Event) and self.id == other.id

    @property
    def capacity_effect_to_vehicle(self):
        if self.is_return:
            return self.capacity
        return -self.capacity

    @property
    def is_delivery(self):
        return False

    @property
    def is_pickup(self):
        return False

    @property
    def is_depot(self):
        return True
