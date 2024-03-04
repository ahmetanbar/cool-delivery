from copy import deepcopy

import pytest

from cool_delivery.constants.event import EventConstant
from cool_delivery.models import Event


@pytest.fixture
def event():
    return Event(id=1, x=1, y=1, location_index=1, capacity=10, type=EventConstant.EventType.EVENT)


@pytest.fixture
def depot_start_event(event):
    depot_start_event = deepcopy(event)
    depot_start_event.type = EventConstant.EventType.DEPOT_START
    return depot_start_event


@pytest.fixture
def depot_end_event(event):
    depot_end_event = deepcopy(event)
    depot_end_event.type = EventConstant.EventType.DEPOT_END
    return depot_end_event


@pytest.fixture
def pickup_event(event):
    pickup_event = deepcopy(event)
    pickup_event.type = EventConstant.EventType.PICKUP
    return pickup_event


@pytest.fixture
def delivery_event(event):
    delivery_event = deepcopy(event)
    delivery_event.type = EventConstant.EventType.DELIVERY
    return delivery_event
