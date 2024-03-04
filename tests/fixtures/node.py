from copy import deepcopy

import pytest

from cool_delivery.solvers.ctsp_with_branch_and_bound.node import Node


@pytest.fixture
def node(depot_start_event, delivery_event):
    delivery_event_1 = deepcopy(delivery_event)
    delivery_event_2 = deepcopy(delivery_event)
    delivery_event_1.location_index = 1
    delivery_event_2.location_index = 2

    events = [depot_start_event, delivery_event_1, delivery_event_2]
    return Node(path=events, capacity=100, level=2)
