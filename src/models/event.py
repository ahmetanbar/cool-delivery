from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Event(ABC):
    id: int
    x: int
    y: int
    capacity: int = 0

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Event) and self.id == other.id

    @property
    @abstractmethod
    def capacity_effect_to_vehicle(self):
        ...

    @property
    @abstractmethod
    def is_delivery(self):
        ...

    @property
    @abstractmethod
    def is_pickup(self):
        ...

    @property
    @abstractmethod
    def is_depot(self):
        ...
