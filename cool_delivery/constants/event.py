from enum import StrEnum


class EventConstant:
    class EventType(StrEnum):
        EVENT = "event"
        PICKUP = "pickup"
        DELIVERY = "delivery"
        DEPOT_START = "depot_start"
        DEPOT_END = "depot_end"
