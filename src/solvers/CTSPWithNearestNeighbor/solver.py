from dataclasses import dataclass, field
from typing import List

import numpy as np

from src.models.delivery import Delivery
from src.models.depot import Depot
from src.models.event import Event
from src.models.pickup import Pickup
from src.models.route import Route
from src.models.vehicle import Vehicle
from src.solvers.CTSPWithNearestNeighbor.models.path_manager import PathManager


@dataclass
class Solver:
    """
    Traveling Salesman Problem solver using Branch and Bound algorithm.
    The algorithm is used to solve the TSP for the given distance matrix and events.
    Events are the pickup and delivery events. The algorithm is used to find the optimal route for the vehicle to visit all the events.

    A route is a path that starts and ends at the depot.

    It doesn't use original Branch and Bound algorithm. It uses a modified version of the algorithm.
    Bounds are calculated using the distance matrix and the capacity of the vehicle.
    """
    depot: Depot
    events: List[Event]  # pickup and deliveries
    vehicle: Vehicle
    distance_matrix: np.ndarray

    depot_to_delivery: Depot = field(init=False)
    depot_to_return: Depot = field(init=False)

    def __post_init__(self):
        # Initialize depot events.
        self.initialize_depot_events()

    def initialize_depot_events(self):
        total_delivery_capacity = sum([event.capacity for event in self.events if isinstance(event, Delivery)])
        self.depot_to_delivery = Depot(id=self.depot.id, x=self.depot.x, y=self.depot.y, capacity=total_delivery_capacity)

        total_pickup_capacity = sum([event.capacity for event in self.events if isinstance(event, Pickup)])
        self.depot_to_return = Depot(id=self.depot.id, x=self.depot.x, y=self.depot.y, capacity=total_pickup_capacity, is_return=True)

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
        print(route)
        return route

    @staticmethod
    def put_back_unsuccessful_events(path_manager, unvisited_events):
        if len(path_manager.unsuccessful_events) > 0:
            unvisited_events.update(path_manager.unsuccessful_events)
