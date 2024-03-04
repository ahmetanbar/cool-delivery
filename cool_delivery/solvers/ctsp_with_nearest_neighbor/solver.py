from dataclasses import dataclass, field
from typing import List, Set

from loguru import logger

from cool_delivery.solvers import BaseSolver
from .path_manager import PathManager
from ...models import Event


@dataclass
class Solver(BaseSolver):
    """
    Capacitated Traveling Salesman Problem solver using Nearest Neighbor algorithm.
    The algorithm is used to find the optimal route for the vehicle to visit all the events. Events are the pickup and delivery events.
    The route is a path that starts and ends at the depot.
    """
    path_manager: PathManager = field(default_factory=PathManager)
    full_path_length: int = 0
    unvisited_events: Set[Event] = field(default_factory=set)
    skipped_events: List[Event] = field(default_factory=list)

    def solve(self):
        self.path_manager = PathManager(capacity=self.vehicle.capacity)
        self.full_path_length = len(self.events) + 2  # 2 is depot events at start and end
        self.unvisited_events = set(self.events)
        self.skipped_events = []

        current_event = self.start_route()

        while not self.is_path_completed():
            current_event = self.find_next_event(current_event)

        self.finalize_route()

        logger.debug(self.optimum_route)

    def is_path_completed(self) -> bool:
        return len(self.path_manager.path) >= self.full_path_length - 1  # -1 for the depot at the end

    def find_next_event(self, current_event: Event):
        nearest_event = self.find_nearest_event(current_event, self.unvisited_events)

        is_added = self.path_manager.add_event(nearest_event)
        if not is_added:
            self.skip_event(nearest_event)
            return current_event
        self.unvisited_events.remove(nearest_event)
        current_event = nearest_event

        self.unvisited_events.update(self.skipped_events)
        self.skipped_events = []

        return current_event

    def skip_event(self, event):
        self.skipped_events.append(event)
        self.unvisited_events.remove(event)

    def start_route(self):
        _ = self.path_manager.add_event(self.depot_to_delivery)
        current_event = self.depot_to_delivery
        return current_event

    def finalize_route(self):
        self.path_manager.add_event(self.depot_to_return)
        route_distance = self.calculate_route_distance()

        self.optimum_route.events = self.path_manager.path
        self.optimum_route.total_cost = route_distance

    def calculate_route_distance(self):
        route_distance = sum(self.distance_matrix[self.path_manager.path[i].location_index][self.path_manager.path[i + 1].location_index]
                             for i in range(len(self.path_manager.path) - 1))
        return route_distance

    def find_nearest_event(self, current_event: Event, events: Set[Event]):
        return min(events, key=lambda event: self.distance_matrix[current_event.location_index][event.location_index])

    def handle_skipped_event(self, event):
        self.skipped_events.append(event)
        self.unvisited_events.remove(event)

    def create_depot_events(self):
        super().create_depot_events()

        total_delivery_capacity = sum([event.capacity for event in self.events if event.is_delivery])
        self.depot_to_delivery.capacity = total_delivery_capacity

        total_pickup_capacity = sum([event.capacity for event in self.events if event.is_pickup])
        self.depot_to_return.capacity = total_pickup_capacity

        self.check_capacity_constraints()

    def check_capacity_constraints(self):
        if self.depot_to_delivery.capacity > self.vehicle.capacity or self.depot_to_return.capacity > self.vehicle.capacity:
            raise ValueError("Delivery or Pickup capacity exceeds vehicle capacity. Solution is not possible.")
