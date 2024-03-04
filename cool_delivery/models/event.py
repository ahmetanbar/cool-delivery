from dataclasses import dataclass

from cool_delivery.constants.event import EventConstant


@dataclass
class Event:
    id: int
    x: int
    y: int
    location_index: int
    capacity: int = 0
    type: EventConstant.EventType.EVENT = EventConstant.EventType.EVENT

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Event) and self.id == other.id

    @property
    def capacity_effect_to_vehicle(self):
        if self.is_pickup or self.is_depot_start:
            return -self.capacity
        else:
            return self.capacity

    @property
    def is_delivery(self):
        return self.type == EventConstant.EventType.DELIVERY

    @property
    def is_pickup(self):
        return self.type == EventConstant.EventType.PICKUP

    @property
    def is_depot_start(self):
        return self.type == EventConstant.EventType.DEPOT_START

    @property
    def is_depot_end(self):
        return self.type == EventConstant.EventType.DEPOT_END
