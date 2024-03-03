from loguru import logger

from cool_delivery.models import Route
from cool_delivery.solvers import BaseSolver
from .path_manager import PathManager


class Solver(BaseSolver):
    """
    Capacitated Traveling Salesman Problem solver using Nearest Neighbor algorithm.
    The algorithm is used to find the optimal route for the vehicle to visit all the events. Events are the pickup and delivery events.
    The route is a path that starts and ends at the depot.
    """

    def __post_init__(self):
        super().__post_init__()
        total_delivery_capacity = sum([event.capacity for event in self.events if event.is_delivery])
        self.depot_to_delivery.capacity = total_delivery_capacity

        total_pickup_capacity = sum([event.capacity for event in self.events if event.is_pickup])
        self.depot_to_return.capacity = total_pickup_capacity

        if self.depot_to_delivery.capacity > self.vehicle.capacity or self.depot_to_return.capacity > self.vehicle.capacity:
            raise ValueError("Delivery or Pickup capacity exceeds vehicle capacity. Solution is not possible.")

    def solve(self) -> Route:
        num_events = len(self.events)
        unvisited_events = set(self.events)
        current_event = self.depot_to_delivery

        path_manager = PathManager(capacity=self.vehicle.capacity)
        _ = path_manager.add_event(self.depot_to_delivery)

        while len(path_manager.path) < num_events + 1:  # +1 for the depot at the start
            nearest_event = min(unvisited_events,
                                key=lambda event: self.distance_matrix[current_event.location_index][event.location_index])

            is_added = path_manager.add_event(nearest_event)
            if not is_added:
                path_manager.unsuccessful_events.append(nearest_event)
                unvisited_events.remove(nearest_event)
                continue

            unvisited_events.remove(nearest_event)
            current_event = nearest_event

            self.put_back_unsuccessful_events(path_manager, unvisited_events)

        _ = path_manager.add_event(self.depot_to_return)

        route_distance = sum(self.distance_matrix[path_manager.path[i].location_index][path_manager.path[i + 1].location_index]
                             for i in range(len(path_manager.path) - 1))
        route = Route(events=path_manager.path, total_cost=route_distance)

        logger.debug(route)
        return route

    @staticmethod
    def put_back_unsuccessful_events(path_manager, unvisited_events):
        if len(path_manager.unsuccessful_events) > 0:
            unvisited_events.update(path_manager.unsuccessful_events)
            path_manager.unsuccessful_events = []
