from copy import deepcopy

import pytest

from cool_delivery.models import Depot, Event
from cool_delivery.solvers import (BaseSolver, CTSPWithNearestNeighborSolver, CTSPWithBranchAndBoundSolver,
                                   CTSPWithMaximumDeliveryAndSinglePickupSolver)
from cool_delivery.solvers.ctsp_with_nearest_neighbor.path_manager import PathManager


class MockBaseSolver(BaseSolver):
    def solve(self):
        pass


@pytest.fixture
def base_solver(depot: Depot, event: Event):
    return MockBaseSolver(events=[event], depot=depot)


@pytest.fixture
def ctsp_with_nearest_neighbor_solver(depot: Depot, event: Event, vehicle, distance_matrix):
    return CTSPWithNearestNeighborSolver(events=[event], depot=depot, vehicle=vehicle, distance_matrix=distance_matrix)


@pytest.fixture
def path_manager(event: Event):
    return PathManager(capacity=10, path=[event])


@pytest.fixture
def ctsp_with_branch_and_bound_solver(depot: Depot, delivery_event: Event, vehicle, distance_matrix):
    event_1 = deepcopy(delivery_event)
    event_2 = deepcopy(delivery_event)
    event_2.id, event_2.location_index = 2, 2

    return CTSPWithBranchAndBoundSolver(events=[event_1, event_2], depot=depot, vehicle=vehicle, distance_matrix=distance_matrix)


@pytest.fixture
def ctsp_maximum_delivery_and_single_pickup(depot: Depot, delivery_event: Event, vehicle, distance_matrix):
    event_1 = deepcopy(delivery_event)
    event_2 = deepcopy(delivery_event)
    event_2.id, event_2.location_index = 2, 2

    return CTSPWithMaximumDeliveryAndSinglePickupSolver(events=[event_1, event_2], depot=depot, vehicle=vehicle,
                                                        distance_matrix=distance_matrix)
