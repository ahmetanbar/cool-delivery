from dataclasses import dataclass

from loguru import logger

from src.models.route import Route
from src.solvers.BaseSolver.solver import BaseSolver
from src.solvers.CTSPWithNearestNeighbor.models.path_manager import PathManager


class Solver(BaseSolver):
    """
    Traveling Salesman Problem solver using Branch and Bound algorithm.
    The algorithm is used to solve the TSP for the given distance matrix and events.
    Events are the pickup and delivery events. The algorithm is used to find the optimal route for the vehicle to visit all the events.

    A route is a path that starts and ends at the depot.

    It doesn't use original Branch and Bound algorithm. It uses a modified version of the algorithm.
    Bounds are calculated using the distance matrix and the capacity of the vehicle.
    """

    def __post_init__(self):
        super().__post_init__()

        if self.depot_to_delivery.capacity > self.vehicle.capacity or self.depot_to_return.capacity > self.vehicle.capacity:
            raise ValueError("Delivery capacity exceeds vehicle capacity.")

    def solve(self) -> Route:
        num_events = len(self.events)
        unvisited_events = set(self.events)
        current_event = self.depot_to_delivery

        path_manager = PathManager(capacity=self.vehicle.capacity)
        _ = path_manager.add_event(self.depot_to_delivery)

        while len(path_manager.path) < num_events + 1:  # +1 for the depot at the start
            nearest_event = min(unvisited_events, key=lambda event: self.distance_matrix[current_event.id][event.id])

            is_added = path_manager.add_event(nearest_event)
            if not is_added:
                path_manager.unsuccessful_events.append(nearest_event)
                unvisited_events.remove(nearest_event)
                continue

            unvisited_events.remove(nearest_event)
            current_event = nearest_event

            self.put_back_unsuccessful_events(path_manager, unvisited_events)

        _ = path_manager.add_event(self.depot_to_return)

        route_distance = sum(self.distance_matrix[path_manager.path[i].id][path_manager.path[i + 1].id]
                             for i in range(len(path_manager.path) - 1))
        route = Route(events=path_manager.path, total_cost=route_distance)

        logger.debug(route)
        return route

    @staticmethod
    def put_back_unsuccessful_events(path_manager, unvisited_events):
        if len(path_manager.unsuccessful_events) > 0:
            unvisited_events.update(path_manager.unsuccessful_events)
            path_manager.unsuccessful_events = []
