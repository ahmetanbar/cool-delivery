import pytest

from cool_delivery.models import Depot, Event
from cool_delivery.solvers import BaseSolver, CTSPWithNearestNeighborSolver
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
